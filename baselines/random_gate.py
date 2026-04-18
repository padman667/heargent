from __future__ import annotations

import random

from sandbox.world import Event, World


class RandomGateAgent:
    """Random-gate ablation: surfaces each new observation with fixed probability.

    Used to test whether heargent's surprise *signal* carries information beyond
    just its firing *frequency*. If a random gate at the same firing rate
    matches heargent's hit rate, the surprise gate is no better than noise.
    """

    def __init__(self, p: float, seed: int = 0) -> None:
        self.p = p
        self.seed = seed
        self._rng = random.Random(seed)
        self._reported_ids: set[str] = set()

    @property
    def name(self) -> str:
        return f"random_gate_p{self.p:.2f}_seed{self.seed}"

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        for ev in observations:
            if ev.id in self._reported_ids:
                continue
            if self._rng.random() < self.p:
                world.surface(content=ev.content, event_id=ev.id)
                self._reported_ids.add(ev.id)

    def cost_usd(self) -> float:
        return 0.0
