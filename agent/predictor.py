from __future__ import annotations

from dataclasses import dataclass

from agent.llm import OllamaClient
from sandbox.world import Event

BOOTSTRAP = "No notable events expected in the next minute."

SYSTEM_PROMPT = (
    "You are a prediction module for a proactive assistant. "
    "Given recent observations, output EXACTLY ONE SHORT SENTENCE (under 20 words) "
    "describing the next notable event you expect. "
    "If nothing notable is expected, reply exactly: "
    '"No notable events expected in the next minute." '
    "No preamble, no reasoning, no lists, no quotes. Output only the sentence."
)

INTENT_SYSTEM_PROMPT_TEMPLATE = (
    "You are a prediction module for a proactive assistant.\n\n"
    "The user's active concerns today are:\n"
    "{intents}\n\n"
    "Given recent observations, output EXACTLY ONE SHORT SENTENCE (under 20 words) "
    "describing the next notable event you expect that would be relevant to any of "
    "those concerns. If nothing notable is expected, reply exactly: "
    '"No notable events expected in the next minute." '
    "No preamble, no reasoning, no lists, no quotes. Output only the sentence."
)


def _render_intent_system_prompt(intents: tuple[str, ...]) -> str:
    bullets = "\n".join(f"- {i}" for i in intents)
    return INTENT_SYSTEM_PROMPT_TEMPLATE.format(intents=bullets)


def _format_history(history: list[Event], max_items: int = 8) -> str:
    if not history:
        return "(no prior events)"
    recent = history[-max_items:]
    lines = [f"- t={ev.sim_time:.0f}s [{ev.kind}]: {ev.content}" for ev in recent]
    return "\n".join(lines)


@dataclass
class Prediction:
    text: str
    sim_time: float


class Predictor:
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

    def predict(
        self,
        history: list[Event],
        sim_time: float,
        intents: tuple[str, ...] = (),
    ) -> Prediction:
        user_msg = (
            "Recent observations:\n"
            + _format_history(history)
            + f"\n\nCurrent sim_time: {sim_time:.0f}s."
            + "\n\nOne-sentence prediction of the next notable event:"
        )
        system = _render_intent_system_prompt(intents) if intents else SYSTEM_PROMPT
        text = self.client.chat(
            system=system,
            user=user_msg,
            model=self.model,
            max_tokens=50,
            temperature=self.temperature,
            seed=self.seed,
        )
        cleaned = text.strip().splitlines()[0].strip() if text.strip() else BOOTSTRAP
        if cleaned.lower().startswith("prediction:"):
            cleaned = cleaned[len("prediction:") :].strip()
        return Prediction(text=cleaned or BOOTSTRAP, sim_time=sim_time)

    @staticmethod
    def bootstrap(sim_time: float = 0.0) -> Prediction:
        return Prediction(text=BOOTSTRAP, sim_time=sim_time)
