from __future__ import annotations

import math
from collections import deque

from agent.intent_extractor import PLACEBO_BRIEFING, extract_intents
from agent.llm import OllamaClient
from agent.predictor import Prediction, Predictor
from agent.surprise import SurpriseScorer
from sandbox.event_trace import Trace
from sandbox.world import Event, World


class HeargentAgent:
    """heargent v1: prediction-error-gated proactive agent.

    Each tick:
    1. For every new observation, compute surprise = cosine distance between
       the prior prediction (emitted on the previous tick) and the observation
       text. If surprise > theta, surface the observation immediately.
    2. After all new observations are folded into history, emit a fresh
       prediction conditioned on the updated history.

    Predictor (qwen2.5:3b-instruct) and surprise scorer (nomic-embed-text) are
    deliberately independent models — mitigates Risk 1 from the plan (surprise
    collapsing to predictor-perplexity).
    """

    def __init__(
        self,
        client: OllamaClient | None = None,
        theta: float = 0.3,
        predictor_model: str = "qwen2.5:3b-instruct",
        surprise_model: str = "nomic-embed-text",
        invert: bool = False,
    ) -> None:
        self.client = client or OllamaClient()
        self.theta = theta
        self.invert = invert
        self.predictor = Predictor(self.client, model=predictor_model)
        self.surprise = SurpriseScorer(self.client, model=surprise_model)
        self.history: list[Event] = []
        self.last_prediction: Prediction = Predictor.bootstrap(sim_time=0.0)
        self.reported_ids: set[str] = set()
        self.surprise_log: list[dict] = []

    @property
    def name(self) -> str:
        polarity = "inv" if self.invert else "fwd"
        return f"heargent_v1_{polarity}_theta{self.theta:.2f}"

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        if not observations:
            return

        for ev in observations:
            s = self.surprise.score(self.last_prediction.text, ev.content)
            passes_gate = (s < self.theta) if self.invert else (s > self.theta)
            surfaced = passes_gate and ev.id not in self.reported_ids
            self.surprise_log.append(
                {
                    "sim_time": sim_time,
                    "event_id": ev.id,
                    "prediction": self.last_prediction.text,
                    "observation": ev.content,
                    "surprise": s,
                    "surfaced": surfaced,
                }
            )
            if surfaced:
                world.surface(content=ev.content, event_id=ev.id)
                self.reported_ids.add(ev.id)
            self.history.append(ev)

        self.last_prediction = self.predictor.predict(self.history, sim_time)

    def cost_usd(self) -> float:
        return 0.0

    def llm_stats(self) -> dict:
        s = self.client.stats
        return {
            "calls": s.calls,
            "prompt_tokens": s.prompt_tokens,
            "completion_tokens": s.completion_tokens,
            "total_duration_s": s.total_duration_ns / 1e9,
        }


class HeargentV1(HeargentAgent):
    """Default heargent v1 config (theta=0.30)."""

    def __init__(self) -> None:
        super().__init__(theta=0.30)


class HeargentZ:
    """Inverted gate using a rolling-window z-score on surprise.

    Motivation: absolute-θ does not transfer between traces with different
    surprise distributions (run 06). A z-score is scale-invariant and adapts
    online to whatever surprise distribution the predictor is producing.

    Surfaces an observation when its surprise is at least `z_threshold`
    standard deviations *below* the rolling mean of recent surprises. During
    bootstrap (window size < min_window), surfaces every observation
    (high-recall calibration phase).
    """

    def __init__(
        self,
        client: OllamaClient | None = None,
        z_threshold: float = 0.5,
        window: int = 16,
        min_window: int = 4,
        predictor_model: str = "qwen2.5:3b-instruct",
        surprise_model: str = "nomic-embed-text",
    ) -> None:
        self.client = client or OllamaClient()
        self.z_threshold = z_threshold
        self.window_size = window
        self.min_window = min_window
        self.predictor = Predictor(self.client, model=predictor_model)
        self.surprise = SurpriseScorer(self.client, model=surprise_model)
        self.history: list[Event] = []
        self.last_prediction: Prediction = Predictor.bootstrap(sim_time=0.0)
        self.reported_ids: set[str] = set()
        self.surprise_log: list[dict] = []
        self._window: deque[float] = deque(maxlen=window)

    @property
    def name(self) -> str:
        return f"heargent_z_thr{self.z_threshold:.2f}_w{self.window_size}"

    def _z(self, s: float) -> float | None:
        if len(self._window) < self.min_window:
            return None
        mu = sum(self._window) / len(self._window)
        var = sum((x - mu) ** 2 for x in self._window) / len(self._window)
        sd = math.sqrt(var)
        if sd == 0.0:
            return 0.0
        return (s - mu) / sd

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        if not observations:
            return

        for ev in observations:
            s = self.surprise.score(self.last_prediction.text, ev.content)
            z = self._z(s)
            if z is None:
                passes_gate = True  # bootstrap: always surface
            else:
                passes_gate = z < -self.z_threshold
            surfaced = passes_gate and ev.id not in self.reported_ids
            self.surprise_log.append(
                {
                    "sim_time": sim_time,
                    "event_id": ev.id,
                    "prediction": self.last_prediction.text,
                    "observation": ev.content,
                    "surprise": s,
                    "z": z,
                    "surfaced": surfaced,
                }
            )
            if surfaced:
                world.surface(content=ev.content, event_id=ev.id)
                self.reported_ids.add(ev.id)
            self.history.append(ev)
            self._window.append(s)

        self.last_prediction = self.predictor.predict(self.history, sim_time)

    def cost_usd(self) -> float:
        return 0.0

    def llm_stats(self) -> dict:
        s = self.client.stats
        return {
            "calls": s.calls,
            "prompt_tokens": s.prompt_tokens,
            "completion_tokens": s.completion_tokens,
            "total_duration_s": s.total_duration_ns / 1e9,
        }


class HeargentZIntent:
    """HeargentZ with an intent-conditioned predictor.

    Identical gate logic to `HeargentZ` (rolling-window inverted z-score on
    surprise); the only change is that the predictor's system prompt is
    anchored in a fixed list of user intents instead of pure recent-history
    conditioning. Intents are frozen at construction time — no Reflect /
    mid-trace updates in M3.

    Use `from_trace(trace, mode, client=...)` to construct with the M3
    intent-source semantics: `mode="oracle"` reads `trace.intents`,
    `mode="briefing"` extracts from `trace.briefing`, and `mode="placebo"`
    extracts from the shared placebo briefing.
    """

    def __init__(
        self,
        intents: tuple[str, ...],
        client: OllamaClient | None = None,
        z_threshold: float = 0.0,
        window: int = 16,
        min_window: int = 4,
        predictor_model: str = "qwen2.5:3b-instruct",
        surprise_model: str = "nomic-embed-text",
        intent_mode: str = "oracle",
    ) -> None:
        if not intents:
            raise ValueError("HeargentZIntent requires a non-empty intent list")
        self.client = client or OllamaClient()
        self.intents = tuple(intents)
        self.intent_mode = intent_mode
        self.z_threshold = z_threshold
        self.window_size = window
        self.min_window = min_window
        self.predictor = Predictor(self.client, model=predictor_model)
        self.surprise = SurpriseScorer(self.client, model=surprise_model)
        self.history: list[Event] = []
        self.last_prediction: Prediction = Predictor.bootstrap(sim_time=0.0)
        self.reported_ids: set[str] = set()
        self.surprise_log: list[dict] = []
        self._window: deque[float] = deque(maxlen=window)

    @classmethod
    def from_trace(
        cls,
        trace: Trace,
        mode: str = "oracle",
        client: OllamaClient | None = None,
        **kwargs,
    ) -> "HeargentZIntent":
        client = client or OllamaClient()
        if mode == "oracle":
            if not trace.intents:
                raise ValueError(f"trace {trace.name!r} has no oracle intents set")
            intents = trace.intents
        elif mode == "briefing":
            if not trace.briefing:
                raise ValueError(f"trace {trace.name!r} has no briefing set")
            intents = extract_intents(client, trace.briefing)
        elif mode == "placebo":
            intents = extract_intents(client, PLACEBO_BRIEFING)
        else:
            raise ValueError(
                f"unknown intent mode {mode!r}; expected oracle|briefing|placebo"
            )
        return cls(intents=intents, client=client, intent_mode=mode, **kwargs)

    @property
    def name(self) -> str:
        return (
            f"heargent_z_intent_{self.intent_mode}"
            f"_thr{self.z_threshold:.2f}_w{self.window_size}"
        )

    def _z(self, s: float) -> float | None:
        if len(self._window) < self.min_window:
            return None
        mu = sum(self._window) / len(self._window)
        var = sum((x - mu) ** 2 for x in self._window) / len(self._window)
        sd = math.sqrt(var)
        if sd == 0.0:
            return 0.0
        return (s - mu) / sd

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        if not observations:
            return

        for ev in observations:
            s = self.surprise.score(self.last_prediction.text, ev.content)
            z = self._z(s)
            if z is None:
                passes_gate = True
            else:
                passes_gate = z < -self.z_threshold
            surfaced = passes_gate and ev.id not in self.reported_ids
            self.surprise_log.append(
                {
                    "sim_time": sim_time,
                    "event_id": ev.id,
                    "prediction": self.last_prediction.text,
                    "observation": ev.content,
                    "surprise": s,
                    "z": z,
                    "surfaced": surfaced,
                }
            )
            if surfaced:
                world.surface(content=ev.content, event_id=ev.id)
                self.reported_ids.add(ev.id)
            self.history.append(ev)
            self._window.append(s)

        self.last_prediction = self.predictor.predict(
            self.history, sim_time, intents=self.intents
        )

    def cost_usd(self) -> float:
        return 0.0

    def llm_stats(self) -> dict:
        s = self.client.stats
        return {
            "calls": s.calls,
            "prompt_tokens": s.prompt_tokens,
            "completion_tokens": s.completion_tokens,
            "total_duration_s": s.total_duration_ns / 1e9,
        }
