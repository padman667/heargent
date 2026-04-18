from __future__ import annotations

from sandbox.world import Event, World


class CronKeywordAgent:
    """Fixed-interval 'heartbeat' baseline, no LLM.

    Accumulates observations each tick; every `interval_s` sim-seconds,
    surfaces one notification per unreported event (content verbatim).
    Emits nothing between firings and nothing when its queue is empty.

    This is the steelmanned structural Hong Su baseline: time-driven,
    but not gratuitously noisy. It tests the *cron cadence* effect
    independent of LLM reasoning quality.
    """

    def __init__(self, interval_s: float = 30.0) -> None:
        self.interval_s = interval_s
        self._queue: list[Event] = []
        self._last_fire_s: float = 0.0
        self._reported_ids: set[str] = set()

    @property
    def name(self) -> str:
        return f"cron_keyword_{int(self.interval_s)}s"

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None:
        for ev in observations:
            if ev.id not in self._reported_ids:
                self._queue.append(ev)

        if sim_time - self._last_fire_s >= self.interval_s and self._queue:
            for ev in self._queue:
                world.surface(content=ev.content, event_id=ev.id)
                self._reported_ids.add(ev.id)
            self._queue.clear()
            self._last_fire_s = sim_time

    def cost_usd(self) -> float:
        return 0.0


class CronKeyword30s(CronKeywordAgent):
    def __init__(self) -> None:
        super().__init__(interval_s=30.0)


class CronKeyword300s(CronKeywordAgent):
    def __init__(self) -> None:
        super().__init__(interval_s=300.0)
