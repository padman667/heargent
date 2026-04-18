from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Event:
    id: str
    kind: str  # "email" | "calendar_update" | "world_event"
    content: str
    sim_time: float  # seconds from start of simulation
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Notification:
    content: str
    sim_time: float
    event_id: str | None = None


class World:
    def __init__(self) -> None:
        self.sim_time: float = 0.0
        self._pending: list[Event] = []
        self._observable: list[Event] = []
        self._notifications: list[Notification] = []
        self._all_events: list[Event] = []

    def load_trace(self, events: Iterable[Event]) -> None:
        self._pending = sorted(events, key=lambda e: e.sim_time)
        self._all_events = list(self._pending)

    def advance(self, dt: float) -> None:
        if dt < 0:
            raise ValueError("dt must be non-negative")
        self.sim_time += dt
        while self._pending and self._pending[0].sim_time <= self.sim_time:
            self._observable.append(self._pending.pop(0))

    def observe(self) -> list[Event]:
        out = self._observable
        self._observable = []
        return out

    def surface(self, content: str, event_id: str | None = None) -> Notification:
        note = Notification(content=content, sim_time=self.sim_time, event_id=event_id)
        self._notifications.append(note)
        return note

    @property
    def notifications(self) -> list[Notification]:
        return list(self._notifications)

    @property
    def all_events(self) -> list[Event]:
        return list(self._all_events)
