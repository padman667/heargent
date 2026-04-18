from __future__ import annotations

from sandbox.world import Event, World


class ReactiveAgent:
    """Floor baseline: never self-initiates. Acts only on explicit user turns.

    Our sandbox has no user turns in v1, so this agent surfaces nothing and
    provides the zero-proaction floor that every other agent must beat.
    """

    name = "reactive"

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        return None

    def cost_usd(self) -> float:
        return 0.0
