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
    briefing: str | None = None
    intents: tuple[str, ...] = ()

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
    briefing = (
        "Normal workday at the office. I've got a trip to Berlin later this "
        "week for some design review prep, the quarterly report is hanging "
        "over me, and I've got a couple of personal medical appointments "
        "squeezed into the calendar. Flag anything that actually needs my "
        "attention."
    )
    oracle_intents = (
        "physical safety while at the office",
        "upcoming international travel plans",
        "work meetings and design reviews",
        "quarterly work deliverables and deadlines",
        "personal medical appointments",
    )
    return Trace(
        name="dev_v2",
        events=all_events,
        ground_truth=gts,
        briefing=briefing,
        intents=oracle_intents,
    )


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
    briefing = (
        "On-call for the production rotation today. Waiting on some health "
        "follow-ups, got home-logistics stuff in progress, my son is at "
        "school for the usual day, and the monthly household bills are "
        "coming due soon."
    )
    oracle_intents = (
        "production on-call responsibilities",
        "personal health follow-ups",
        "household deliveries and logistics",
        "child's school day",
        "monthly household bills",
    )
    return Trace(
        name="test_v1",
        events=all_events,
        ground_truth=gts,
        briefing=briefing,
        intents=oracle_intents,
    )


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
    briefing = (
        "Working from home today. There's a quarterly board session on the "
        "calendar, my mother has some ongoing medical stuff I'm keeping tabs "
        "on, and there's been some flaky login behavior on my accounts. "
        "Flag urgent."
    )
    oracle_intents = (
        "physical safety at home",
        "scheduled work meetings and board sessions",
        "family member health",
        "account and login security",
        "urgent household incidents",
    )
    return Trace(
        name="test_v2",
        events=all_events,
        ground_truth=gts,
        briefing=briefing,
        intents=oracle_intents,
    )


def test_trace_v3() -> Trace:
    gts = [
        _gt(
            Event(id="passport_expiry", kind="email", sim_time=45.0,
                  content="Reminder from Travel Desk: your passport expires in 4 weeks, before your planned Tokyo trip next month. Renewal appointments are booking out 3+ weeks."),
            window_s=600.0, keywords=("passport", "expiring"),
        ),
        _gt(
            Event(id="prescription_urgent", kind="notification", sim_time=180.0,
                  content="Pharmacy: your blood pressure medication refill is ready for pickup today only. Store closes at 18:00 and you are on your last dose."),
            window_s=30.0, keywords=("prescription", "refill"),
        ),
        _gt(
            Event(id="car_recall", kind="alert", sim_time=300.0,
                  content="Manufacturer recall notice for your 2021 Subaru Forester: airbag inflator defect. Do not drive with front passenger until serviced. Free repair at any dealer."),
            window_s=300.0, keywords=("recall", "airbag"),
        ),
        _gt(
            Event(id="power_shutoff_planned", kind="world_event", sim_time=520.0,
                  content="Building management notice: planned electrical shutoff tonight 22:00–02:00 for panel replacement. All outlets and wifi will be offline."),
            window_s=400.0, keywords=("power", "shutoff"),
        ),
        _gt(
            Event(id="plumber_reschedule", kind="phone_message", sim_time=700.0,
                  content="Voicemail from Jorge at Ridgeline Plumbing: cannot make tomorrow's 09:00 dishwasher install; next available slot is in 9 days unless you confirm today."),
            window_s=300.0, keywords=("plumber", "reschedule"),
        ),
    ]
    distractors = [
        Event(id="spotify_weekly", kind="notification", sim_time=20.0,
              content="Your Discover Weekly playlist has refreshed with 30 new songs."),
        Event(id="app_version_note", kind="notification", sim_time=250.0,
              content="Messages app updated to version 14.2 — new sticker pack available."),
        Event(id="distant_birthday", kind="calendar_update", sim_time=400.0,
              content="Upcoming in 94 days: Aunt Linda's birthday (no action required)."),
        Event(id="photo_likes", kind="notification", sim_time=850.0,
              content="7 friends liked your photo from the weekend hike."),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    briefing = (
        "I'm working from home today while my partner is away on a work trip, so the household is on me. "
        "I've got a Tokyo vacation coming up next month that still needs prep, and a dishwasher install booked for tomorrow. "
        "I want to stay focused on deep work but not miss anything time-sensitive."
    )
    intents = (
        "prepare for Tokyo trip on schedule",
        "stay current on medication and health",
        "keep the home improvement work moving",
        "catch time-sensitive safety issues",
        "ignore routine app and social noise",
    )
    return Trace(name="test_v3", events=all_events, ground_truth=gts,
                 briefing=briefing, intents=intents)

def test_trace_v4() -> Trace:
    gts = [
        _gt(
            Event(id="parking_meter_oak", kind="alert", sim_time=180.0,
                  content="Parking meter at Oak Street lot expires in 30 minutes. Enforcement active in zone."),
            window_s=20.0, keywords=("parking", "meter", "expires"),
        ),
        _gt(
            Event(id="cover_standup_request", kind="email", sim_time=240.0,
                  content="Heading out on vacation tomorrow - can you cover the 9am standup and post the sprint tracker update in my place?"),
            window_s=420.0, keywords=("standup", "vacation"),
        ),
        _gt(
            Event(id="gym_class_cancelled", kind="notification", sim_time=380.0,
                  content="Pine Street Gym is closing at 5pm tonight for equipment maintenance. Your 6pm spin class is cancelled."),
            window_s=90.0, keywords=("gym", "maintenance"),
        ),
        _gt(
            Event(id="library_hold_expiring", kind="email", sim_time=520.0,
                  content="Your library hold on 'The Signal and the Noise' expires at midnight tonight if not picked up today."),
            window_s=180.0, keywords=("library", "hold", "expires"),
        ),
        _gt(
            Event(id="protest_commute_route", kind="world_event", sim_time=700.0,
                  content="Protest march planned 5-7pm along Market Street - significant detours expected on your usual commute home."),
            window_s=280.0, keywords=("protest", "market street"),
        ),
    ]
    distractors = [
        Event(id="linkedin_connections", kind="notification", sim_time=50.0,
              content="You have 3 new LinkedIn connection requests pending this week."),
        Event(id="github_repo_star", kind="notification", sim_time=310.0,
              content="alice-dev starred your repository 'toolkit-scripts'."),
        Event(id="designgrid_renewal", kind="email", sim_time=440.0,
              content="Your DesignGrid Pro subscription renewed for $12/month. Next charge April 2027."),
        Event(id="calendar_feature_tip", kind="notification", sim_time=820.0,
              content="Tip: enable working hours to auto-decline meetings scheduled outside 9am-6pm."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    briefing = (
        "I'm working from home today, juggling a few errands between meetings. "
        "My partner is out of town, so I'm handling pickups and logistics on my own. "
        "I've got a busy afternoon with a library stop, a workout, and an evening commute to plan around."
    )
    intents = (
        "stay on top of time-sensitive errands",
        "keep my workday on track",
        "avoid unnecessary interruptions",
        "plan my evening commute carefully",
        "protect my focus time",
    )
    return Trace(name="test_v4", events=events, ground_truth=gts, briefing=briefing, intents=intents)

def test_trace_v5() -> Trace:
    gts = [
        _gt(
            Event(id="babysitter_sick", kind="phone_message", sim_time=50.0,
                  content="Hey, it's Maya — I'm running a 102 fever and can't babysit Theo tonight at 6pm. So sorry to bail last minute!"),
            window_s=20.0, keywords=("babysit", "tonight"),
        ),
        _gt(
            Event(id="rail_strike", kind="world_event", sim_time=200.0,
                  content="Regional rail union announces a 24-hour strike starting tomorrow 04:00; all commuter lines suspended through Friday morning."),
            window_s=600.0, keywords=("strike", "rail"),
        ),
        _gt(
            Event(id="keynote_slot", kind="calendar_update", sim_time=350.0,
                  content="Your keynote slot at PyConf has been moved up from 15:00 to 11:00 — speakers requested to arrive by 10:00 for tech check."),
            window_s=180.0, keywords=("keynote", "moved"),
        ),
        _gt(
            Event(id="card_fraud", kind="alert", sim_time=500.0,
                  content="Suspicious $2,418 charge on your Visa ending 4471 at an electronics retailer in Lagos. Reply STOP within 1 minute if this was not you."),
            window_s=15.0, keywords=("suspicious", "charge"),
        ),
        _gt(
            Event(id="tax_extension", kind="notification", sim_time=700.0,
                  content="Your accountant flagged: state income tax extension expires tomorrow at midnight — your signature is still missing on Form 8453."),
            window_s=300.0, keywords=("tax", "expires"),
        ),
    ]
    distractors = [
        Event(id="icloud_storage", kind="notification", sim_time=120.0,
              content="You've used 47% of your 200GB iCloud storage. No action needed."),
        Event(id="ebook_receipt", kind="email", sim_time=275.0,
              content="Receipt for your $14.99 ebook 'The Pragmatic Programmer' from BookHub. Download link inside."),
        Event(id="bank_survey", kind="email", sim_time=420.0,
              content="How was your recent visit to MetroBank Oakridge branch? Take our 2-minute satisfaction survey."),
        Event(id="podcast_charge", kind="notification", sim_time=850.0,
              content="Heads up: your monthly Overcast Premium subscription processed successfully — $4.99 charged to card ending 4471."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v5",
        events=events,
        ground_truth=gts,
        briefing=(
            "I'm working from home today juggling kid logistics and a stack of admin debts I've been putting off. "
            "My partner is out of town until Wednesday, so I'm solo on Theo this evening. "
            "Tonight I'm also supposed to do a dry run of my conference talk before flying out next week."
        ),
        intents=(
            "keep evening childcare covered",
            "stay on top of conference logistics",
            "catch financial fraud quickly",
            "avoid missing tax deadlines",
            "adapt to transit disruptions",
        ),
    )


def get_trace(name: str) -> Trace:
    traces = {
        "dev_v1": dev_trace_v1,
        "dev_v2": dev_trace_v2,
        "test_v1": test_trace_v1,
        "test_v2": test_trace_v2,
        "test_v3": test_trace_v3,
        "test_v4": test_trace_v4,
        "test_v5": test_trace_v5,
    }
    if name not in traces:
        raise ValueError(f"Unknown trace {name!r}; options: {sorted(traces)}")
    return traces[name]()
