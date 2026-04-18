from __future__ import annotations

import re

from agent.llm import OllamaClient
from sandbox.world import Event, World

POLL_SYSTEM = (
    "You are a proactive notification assistant. Each tick you receive a list "
    "of pending events. Decide which (if any) should be surfaced to the user "
    "RIGHT NOW as a notification. "
    "Reply with the comma-separated NUMBERS of events to surface (e.g. '1,3'), "
    "or the single word NONE if nothing is worth surfacing. "
    "Do not surface routine system noise (newsletters, status pings, "
    "promotional emails). Surface time-sensitive personal or work events."
)


class ReactPollLocal:
    """Strong baseline: every tick, ask the local LLM what to surface.

    Calls qwen2.5:3b-instruct EVERY tick (not just when observations arrive),
    with the full pending-event queue as context. This is the reviewer's
    obvious counter-argument ('heargent is just polling with extra steps')
    and the cost ceiling heargent must beat on tokens-per-correct-proaction.
    """

    def __init__(
        self,
        client: OllamaClient | None = None,
        model: str = "qwen2.5:3b-instruct",
    ) -> None:
        self.client = client or OllamaClient()
        self.model = model
        self._pending: list[Event] = []
        self._reported_ids: set[str] = set()

    @property
    def name(self) -> str:
        return "react_poll_local"

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

        response = self.client.chat(
            system=POLL_SYSTEM,
            user=user_msg,
            model=self.model,
            max_tokens=20,
            temperature=0.0,
            seed=42,
        )

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
        return 0.0

    def llm_stats(self) -> dict:
        s = self.client.stats
        return {
            "calls": s.calls,
            "prompt_tokens": s.prompt_tokens,
            "completion_tokens": s.completion_tokens,
            "total_duration_s": s.total_duration_ns / 1e9,
        }
