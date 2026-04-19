from __future__ import annotations

import random
import re

from agent.llm import OllamaClient

ARBITER_SYSTEM_PROMPT = (
    "You are a triage filter for a proactive assistant. Decide whether a\n"
    "single observed event warrants surfacing to the user right now.\n"
    "\n"
    "Surface (YES) if the event describes:\n"
    " - an urgent physical safety or security issue (fire, break-in, breach)\n"
    " - an unexpected interruption to the user's personal life (medical,\n"
    "   family emergency, home problem, childcare)\n"
    " - a financial or scheduling obligation with imminent action required\n"
    " - a production/on-call alert or outage\n"
    "\n"
    "Do NOT surface (NO) if the event is:\n"
    " - routine status, uptime, or heartbeat notifications\n"
    " - marketing, promotional, or newsletter content\n"
    " - generic \"all systems normal\" or daily briefing summaries\n"
    "\n"
    "Output exactly YES or NO, uppercase, on a single line. No explanation."
)


_DECISION = re.compile(r"\b(YES|NO)\b")


class ContentArbiter:
    """Pure-content binary classifier for proactive surfacing.

    Ignores the predictor's output, the rolling history, any user briefing,
    and any intent list — only the event content text is fed in. This is the
    mechanism isolation from run 09: user-context injection hurt every cell
    it touched there, so the arbiter is deliberately context-free.
    """

    def __init__(
        self,
        client: OllamaClient,
        model: str = "qwen2.5:3b-instruct",
        *,
        temperature: float = 0.0,
        seed: int = 42,
    ) -> None:
        self.client = client
        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.yes_count = 0
        self.no_count = 0

    @property
    def yes_rate(self) -> float:
        total = self.yes_count + self.no_count
        return self.yes_count / total if total else 0.0

    def classify(self, text: str) -> bool:
        raw = self.client.chat(
            system=ARBITER_SYSTEM_PROMPT,
            user=text,
            model=self.model,
            max_tokens=5,
            temperature=self.temperature,
            seed=self.seed,
        )
        first_line = raw.strip().splitlines()[0] if raw.strip() else ""
        m = _DECISION.search(first_line.upper())
        decision = bool(m and m.group(1) == "YES")
        if decision:
            self.yes_count += 1
        else:
            self.no_count += 1
        return decision


class RandomArbiter:
    """Null-ablation arbiter: Bernoulli draw with pre-committed firing rate.

    Matches the M4 null-ablation role of run 05's random-gate. `p` is set to
    the empirical YES-rate of the content arbiter on dev_v2, so firing rate
    is controlled; only the content signal differs between this and the real
    arbiter.
    """

    def __init__(self, p: float, seed: int = 42) -> None:
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p must be in [0, 1]; got {p}")
        self.p = p
        self.seed = seed
        self._rng = random.Random(seed)
        self.yes_count = 0
        self.no_count = 0

    @property
    def yes_rate(self) -> float:
        total = self.yes_count + self.no_count
        return self.yes_count / total if total else 0.0

    def classify(self, text: str) -> bool:
        del text  # random arbiter ignores content by design
        decision = self._rng.random() < self.p
        if decision:
            self.yes_count += 1
        else:
            self.no_count += 1
        return decision
