from __future__ import annotations

import re
from typing import TYPE_CHECKING

from agent.arbiter import _rates_for
from baselines.react_poll_local import POLL_SYSTEM
from sandbox.event_trace import Trace
from sandbox.world import Event, World

if TYPE_CHECKING:
    from anthropic import Anthropic


class ReactPollClaude:
    """Strong baseline parallel to ReactPollLocal: every tick, ask Claude.

    M10 apples-to-apples cost denominator (runs/17 SHA 68d42e3): uses
    claude-opus-4-7 with the same poll system prompt (imported verbatim
    from baselines.react_poll_local) and the same parsing logic as
    ReactPollLocal. Only the underlying LLM call swaps from
    OllamaClient.chat to Anthropic.messages.create. Cost is real (not
    zero); reported via cost_usd at locked Opus rates.

    If `briefing` is set, its text is prepended to the system prompt for
    M3 fairness parity with ReactPollLocal — held available even though
    M10 does not exercise this path.
    """

    def __init__(
        self,
        client: Anthropic | None = None,
        model: str = "claude-opus-4-7",
        briefing: str | None = None,
    ) -> None:
        if client is None:
            from anthropic import Anthropic as _Anthropic
            client = _Anthropic()
        self.client = client
        self.model = model
        self.briefing = briefing
        self._pending: list[Event] = []
        self._reported_ids: set[str] = set()
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.dispatched_model: str | None = None

    @classmethod
    def from_trace(
        cls,
        trace: Trace,
        with_briefing: bool = False,
        client: Anthropic | None = None,
        **kwargs,
    ) -> "ReactPollClaude":
        briefing = trace.briefing if with_briefing else None
        if with_briefing and briefing is None:
            raise ValueError(f"trace {trace.name!r} has no briefing set")
        return cls(client=client, briefing=briefing, **kwargs)

    @property
    def name(self) -> str:
        return "react_poll_claude" + ("_briefing" if self.briefing else "")

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        for ev in observations:
            if ev.id not in self._reported_ids and ev not in self._pending:
                self._pending.append(ev)

        if not self._pending:
            user_msg = (
                f"Sim time: {sim_time:.0f}s. "
                "No pending events. Reply with the single word NONE."
            )
        else:
            pending_str = "\n".join(
                f"{i+1}. [t={ev.sim_time:.0f}s] {ev.content}"
                for i, ev in enumerate(self._pending)
            )
            user_msg = (
                f"Sim time: {sim_time:.0f}s. Pending events:\n{pending_str}\n\n"
                "Reply with comma-separated numbers to surface, or NONE."
            )

        system = POLL_SYSTEM
        if self.briefing:
            system = f"User briefing at start of day:\n{self.briefing}\n\n" + POLL_SYSTEM

        # `temperature` omitted: Opus 4.7 deprecates it (see runs/17 hardening).
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=20,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        if self.dispatched_model is None:
            self.dispatched_model = resp.model
        self.input_tokens += resp.usage.input_tokens
        self.output_tokens += resp.usage.output_tokens
        self.calls += 1
        response = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()

        nums = re.findall(r"\d+", response)
        to_surface: list[Event] = []
        for n in nums:
            idx = int(n) - 1
            if 0 <= idx < len(self._pending):
                to_surface.append(self._pending[idx])

        for ev in to_surface:
            world.surface(content=ev.content, event_id=ev.id)
            self._reported_ids.add(ev.id)
            self._pending.remove(ev)

    def cost_usd(self) -> float:
        input_rate, output_rate = _rates_for(self.model)
        return (
            self.input_tokens * input_rate
            + self.output_tokens * output_rate
        ) / 1_000_000

    def llm_stats(self) -> dict:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "dispatched_model": self.dispatched_model,
        }
