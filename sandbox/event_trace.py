from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.world import Event


@dataclass(frozen=True)
class GroundTruthEvent:
    event: Event
    proaction_window_s: float
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class Trace:
    name: str
    events: list[Event]
    ground_truth: list[GroundTruthEvent]

    @property
    def duration_s(self) -> float:
        if not self.ground_truth and not self.events:
            return 0.0
        last_gt = max(
            (g.event.sim_time + g.proaction_window_s for g in self.ground_truth),
            default=0.0,
        )
        last_ev = max((e.sim_time for e in self.events), default=0.0)
        return max(last_gt, last_ev) + 30.0


def _gt(event: Event, window_s: float, keywords: tuple[str, ...]) -> GroundTruthEvent:
    return GroundTruthEvent(event=event, proaction_window_s=window_s, keywords=keywords)


def dev_trace_v1() -> Trace:
    gts = [
        _gt(
            Event(id="flight_delay", kind="email", sim_time=10.0,
                  content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New departure: 14:30."),
            window_s=300.0, keywords=("flight", "delay"),
        ),
        _gt(
            Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,
                  content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),
            window_s=300.0, keywords=("meeting", "moved"),
        ),
        _gt(
            Event(id="weather_alert", kind="world_event", sim_time=120.0,
                  content="Weather alert: heavy rain expected tomorrow morning; expect travel delays."),
            window_s=300.0, keywords=("weather", "rain"),
        ),
        _gt(
            Event(id="deadline", kind="email", sim_time=300.0,
                  content="Reminder: Quarterly Report deadline is in 24 hours."),
            window_s=600.0, keywords=("deadline", "quarterly"),
        ),
        _gt(
            Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
                  content="Your dentist appointment today at 16:00 has been cancelled."),
            window_s=300.0, keywords=("dentist", "cancelled"),
        ),
    ]
    return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)


def dev_trace_v2() -> Trace:
    """Harder trace: tight windows, off-cron injections, distractors.

    Designed so a 30 s cron and a 300 s cron produce different hit rates, and
    any agent that replays observations verbatim will generate false initiations
    on the distractors.
    """
    gts = [
        _gt(
            Event(id="fire_alarm", kind="world_event", sim_time=5.0,
                  content="Fire alarm in building A triggered; evacuation in progress."),
            window_s=20.0, keywords=("fire", "alarm"),
        ),
        _gt(
            Event(id="flight_delay", kind="email", sim_time=35.0,
                  content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New departure: 14:30."),
            window_s=50.0, keywords=("flight", "delay"),
        ),
        _gt(
            Event(id="meeting_moved", kind="calendar_update", sim_time=100.0,
                  content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),
            window_s=180.0, keywords=("meeting", "moved"),
        ),
        _gt(
            Event(id="deadline", kind="email", sim_time=400.0,
                  content="Reminder: Quarterly Report deadline is in 24 hours."),
            window_s=600.0, keywords=("deadline", "quarterly"),
        ),
        _gt(
            Event(id="dentist_cancel", kind="calendar_update", sim_time=700.0,
                  content="Your dentist appointment today at 16:00 has been cancelled."),
            window_s=300.0, keywords=("dentist", "cancelled"),
        ),
    ]
    distractors = [
        Event(id="news_digest", kind="world_event", sim_time=50.0,
              content="Daily news digest updated."),
        Event(id="weather_nominal", kind="world_event", sim_time=200.0,
              content="Today's weather: sunny and mild, high 22°C."),
        Event(id="marketing_newsletter", kind="email", sim_time=350.0,
              content="Newsletter from the marketing team: latest trends in agentic AI."),
        Event(id="system_heartbeat", kind="world_event", sim_time=550.0,
              content="System heartbeat: all services nominal."),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(name="dev_v2", events=all_events, ground_truth=gts)


def test_trace_v1() -> Trace:
    """Held-out test trace. Same structural split as dev_v2 (human-relevant GT
    vs system-noise distractors) with completely different specific content.

    Used to check whether the polarity-flip discovered on dev_v2 generalizes:
    if GT events again score systematically lower surprise than distractors,
    the inverted gate's win on dev_v2 is not pure overfit.

    Includes one tight-window event (server_outage, 30 s) analogous to fire_alarm
    in dev_v2, so the time-to-notice axis stays meaningful.
    """
    gts = [
        _gt(
            Event(id="package_arrival", kind="notification", sim_time=15.0,
                  content="Amazon package delivered to your front door."),
            window_s=60.0, keywords=("package", "delivered"),
        ),
        _gt(
            Event(id="doctor_callback", kind="email", sim_time=80.0,
                  content="Doctor Hayes called regarding your test results; please call back today."),
            window_s=120.0, keywords=("doctor", "call"),
        ),
        _gt(
            Event(id="server_outage", kind="alert", sim_time=95.0,
                  content="Production alert: api.example.com returning 500 errors; on-call engineer paged."),
            window_s=20.0, keywords=("production", "alert"),
        ),
        _gt(
            Event(id="rent_due", kind="email", sim_time=350.0,
                  content="Reminder: your monthly rent payment is due in 2 days."),
            window_s=600.0, keywords=("rent", "due"),
        ),
        _gt(
            Event(id="kid_school_pickup", kind="phone_message", sim_time=600.0,
                  content="Lincoln Elementary called: please pick up your son from school early; he is unwell."),
            window_s=180.0, keywords=("school", "pick up"),
        ),
    ]
    distractors = [
        Event(id="slack_invite", kind="notification", sim_time=40.0,
              content="You have been invited to the #general channel on Slack."),
        Event(id="calendar_advert", kind="notification", sim_time=200.0,
              content="New feature available in Calendar: dark mode is now supported."),
        Event(id="promo_email", kind="email", sim_time=400.0,
              content="Promotional offer: 20% off on premium subscription this week only."),
        Event(id="system_status", kind="world_event", sim_time=500.0,
              content="Cloud platform status: all services operating normally."),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(name="test_v1", events=all_events, ground_truth=gts)


def test_trace_v2() -> Trace:
    """Adversarial held-out trace. Inverts the structural split of dev_v2 /
    test_v1: distractors here are mundane routine noise (status pings, daily
    briefings, newsletters) that the predictor can learn to expect, and GT
    events are abrupt interruptions (fire, burst pipe, ER call, security
    breach) that DO break the narrative context.

    On this trace, the polarity-flip hypothesis from runs 05/06 is at risk:
    if abrupt GT events score *higher* surprise than the calm distractors,
    the inverted gate fails and forward heargent (or a polarity-agnostic
    |z| > threshold gate) should win.

    First distractor burst (t=10, 60, 85) primes the predictor on routine
    and also loads cron 30 s so that fire_kitchen at t=95 (window=20, [95,115])
    falls in cron's 30 s dead-zone after its t=90 fire — genuinely unwinnable.
    """
    gts = [
        _gt(
            Event(id="fire_kitchen", kind="world_event", sim_time=95.0,
                  content="FIRE detected in your kitchen; evacuate immediately."),
            window_s=20.0, keywords=("fire", "kitchen"),
        ),
        _gt(
            Event(id="board_meeting", kind="calendar_update", sim_time=250.0,
                  content="URGENT: Board meeting moved to start NOW in conference room A."),
            window_s=60.0, keywords=("board", "meeting"),
        ),
        _gt(
            Event(id="water_burst", kind="notification", sim_time=400.0,
                  content="Emergency: main water line burst in apartment 3B, flooding the hallway."),
            window_s=120.0, keywords=("water", "burst"),
        ),
        _gt(
            Event(id="er_call", kind="phone_message", sim_time=550.0,
                  content="Hospital called: your mother has been admitted to the ER; please call urgently."),
            window_s=300.0, keywords=("hospital", "mother"),
        ),
        _gt(
            Event(id="security_breach", kind="alert", sim_time=750.0,
                  content="Security alert: unauthorized access detected on your account from an unknown device."),
            window_s=180.0, keywords=("security", "unauthorized"),
        ),
    ]
    distractors = [
        Event(id="daily_briefing", kind="email", sim_time=10.0,
              content="Daily briefing: no urgent items for today."),
        Event(id="status_ok", kind="notification", sim_time=60.0,
              content="System status: all services operating nominally."),
        Event(id="uptime_ping", kind="notification", sim_time=85.0,
              content="Weekly uptime report: 99.99% availability maintained."),
        Event(id="newsletter", kind="email", sim_time=350.0,
              content="Weekly industry newsletter: trends and updates delivered."),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(name="test_v2", events=all_events, ground_truth=gts)


def get_trace(name: str) -> Trace:
    traces = {
        "dev_v1": dev_trace_v1,
        "dev_v2": dev_trace_v2,
        "test_v1": test_trace_v1,
        "test_v2": test_trace_v2,
    }
    if name not in traces:
        raise ValueError(f"Unknown trace {name!r}; options: {sorted(traces)}")
    return traces[name]()
