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


def test_trace_v6() -> Trace:
    gts = [
        _gt(
            Event(id="vet_emergency", kind="phone_message", sim_time=50.0,
                  content="Dr. Patel from Bayside Vet called. Your dog Rufus needs emergency surgery and they need verbal authorization within 10 minutes before they can proceed — please call back."),
            window_s=30.0, keywords=("vet", "surgery"),
        ),
        _gt(
            Event(id="concert_swap", kind="email", sim_time=180.0,
                  content="Hey — any chance we can swap our concert tickets for Saturday night? I have row C aisle, you have row M center. Need to know before 5pm so I can confirm with the resale buyer."),
            window_s=300.0, keywords=("concert", "swap"),
        ),
        _gt(
            Event(id="elevator_outage", kind="alert", sim_time=300.0,
                  content="Building alert: the main elevator will be out of service for emergency cable repair starting at 16:00 today through tomorrow morning. Use the service elevator near the loading dock if you need to move anything heavy."),
            window_s=600.0, keywords=("elevator", "out of service"),
        ),
        _gt(
            Event(id="auction_ending", kind="notification", sim_time=420.0,
                  content="The online auction for the vintage Leica camera you've been watching is ending in 10 minutes; you are currently the top bidder at $340 with two competing bidders active."),
            window_s=30.0, keywords=("auction", "ending"),
        ),
        _gt(
            Event(id="wedding_rsvp", kind="email", sim_time=600.0,
                  content="Final reminder: RSVP for Sara and Mark's wedding next month closes at midnight tonight. Please confirm attendance and meal selection (chicken, salmon, or vegetarian) through the link."),
            window_s=300.0, keywords=("wedding", "rsvp"),
        ),
    ]
    distractors = [
        Event(id="reddit_digest", kind="notification", sim_time=30.0,
              content="Your weekly r/woodworking digest is ready: 12 new top posts from the past week."),
        Event(id="steam_sale", kind="email", sim_time=240.0,
              content="Steam Summer Sale starts Friday — wishlist items up to 80% off, plus free demos for select indie titles."),
        Event(id="bank_statement", kind="notification", sim_time=480.0,
              content="Your June checking statement (account ending 4567) is now available to view in the mobile app."),
        Event(id="twitter_followers", kind="notification", sim_time=720.0,
              content="You have 4 new followers this week on X. Tap to see who followed you."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v6",
        events=events,
        ground_truth=gts,
        briefing=(
            "I'm working from my apartment today, mixing personal errands between a light meeting load. "
            "My dog Rufus is at Bayside Vet for routine bloodwork this morning, "
            "and I'm tracking an online auction I've been bidding on for a while. "
            "A few weekend social plans also need to get locked in before the day gets away from me."
        ),
        intents=(
            "respond promptly to urgent personal phone calls",
            "lock in weekend social commitments before deadlines",
            "monitor active online auctions I'm leading",
            "stay aware of building service disruptions affecting my unit",
            "coordinate ticket and event plans with close friends",
        ),
    )


def test_trace_v7() -> Trace:
    gts = [
        _gt(
            Event(id="sister_pickup", kind="phone_message", sim_time=50.0,
                  content="Voicemail from Maya (sister): she landed early at SFO and needs airport pickup by 22:00 tonight, no rideshare option."),
            window_s=15.0, keywords=("sister", "airport"),
        ),
        _gt(
            Event(id="mortgage_rate_lock", kind="email", sim_time=100.0,
                  content="From the broker: your mortgage rate lock expires today at 17:00; final signed disclosures must be returned before then or the rate resets."),
            window_s=600.0, keywords=("mortgage", "expires"),
        ),
        _gt(
            Event(id="jury_duty", kind="email", sim_time=200.0,
                  content="Superior Court: a jury duty summons has been issued for next Thursday; confirm or request postponement online by tomorrow noon."),
            window_s=720.0, keywords=("jury", "duty"),
        ),
        _gt(
            Event(id="airbnb_cancelled", kind="notification", sim_time=250.0,
                  content="Airbnb: your Lisbon host has cancelled your reservation for next weekend; refund issued and you'll need to rebook accommodations."),
            window_s=300.0, keywords=("airbnb", "cancelled"),
        ),
        _gt(
            Event(id="wedding_rehearsal", kind="calendar_update", sim_time=400.0,
                  content="Hana's wedding rehearsal dinner has been rescheduled from Saturday 12:00 to Friday 18:00 at the same venue."),
            window_s=120.0, keywords=("wedding", "rehearsal"),
        ),
    ]
    distractors = [
        Event(id="poll_civic_reminder", kind="notification", sim_time=20.0,
              content="Reminder: the city council's annual transit survey is open through the end of the month if you'd like to weigh in."),
        Event(id="recipe_app_tip", kind="notification", sim_time=180.0,
              content="Tip of the week from your meal-planner app: try the new spring pasta collection we added on Monday."),
        Event(id="loyalty_points_summary", kind="email", sim_time=350.0,
              content="Your April loyalty account summary: 240 points earned, 1,820 total balance, no rewards changing status this period."),
        Event(id="podcast_episode_drop", kind="notification", sim_time=600.0,
              content="New episode of 'In Our Time' available now; this week's topic is the Antikythera mechanism."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v7",
        events=events,
        ground_truth=gts,
        briefing=(
            "I'm working from home in San Francisco today while my sister Maya is in town visiting for the week. "
            "I'm in the middle of refinancing the condo, so anything from the mortgage broker is time-sensitive. "
            "I'm also helping coordinate logistics for my cousin Hana's wedding next month."
        ),
        intents=(
            "close the mortgage refinance on time",
            "be available for sister Maya during her visit",
            "help coordinate cousin Hana's wedding",
            "stay on top of legal and civic obligations",
            "protect upcoming personal travel plans",
        ),
    )


def test_trace_v8() -> Trace:
    gts = [
        _gt(
            Event(id="vet_luna_tomorrow", kind="calendar_update", sim_time=50.0,
                  content="Reminder: Your vet appointment for Luna is tomorrow at 9:30 AM. Please bring her vaccination records and a stool sample."),
            window_s=600.0, keywords=("vet", "luna"),
        ),
        _gt(
            Event(id="earthquake_local", kind="alert", sim_time=200.0,
                  content="Earthquake detected: M4.2, epicenter 12 miles north. Light shaking expected in your area within the next minute. Drop, cover, hold on."),
            window_s=20.0, keywords=("earthquake", "shaking"),
        ),
        _gt(
            Event(id="mom_birthday_heads_up", kind="notification", sim_time=320.0,
                  content="Heads up: tomorrow is your mother's birthday. No card has been ordered, no call is on your calendar, and last year you forgot until the evening."),
            window_s=400.0, keywords=("mother", "birthday"),
        ),
        _gt(
            Event(id="bridgers_presale_window", kind="email", sim_time=500.0,
                  content="The presale window for Phoebe Bridgers tickets at the Greek Theatre opens in 10 minutes. Your saved access code: PBSALE2026. Two-ticket limit per account."),
            window_s=30.0, keywords=("presale", "tickets"),
        ),
        _gt(
            Event(id="photographer_voicemail_jen", kind="phone_message", sim_time=700.0,
                  content="Voicemail from photographer Jen Cho: 'A client just dropped, so I have a Saturday morning slot open for your engagement shoot — I need to know by 6pm tonight or I'll offer it to someone else.'"),
            window_s=250.0, keywords=("photographer", "engagement"),
        ),
    ]
    distractors = [
        Event(id="soundcloud_app_update", kind="notification", sim_time=80.0,
              content="SoundCloud 2026.5.1 is available. Tap to update at your convenience."),
        Event(id="stitches_loyalty_statement", kind="email", sim_time=250.0,
              content="Your monthly Stitches Coffee loyalty statement: 2,340 points total (140 earned this month). No expiring rewards. No action needed."),
        Event(id="strava_new_follower", kind="notification", sim_time=380.0,
              content="Marcus T. started following you on Strava. View profile."),
        Event(id="reading_streak_47", kind="notification", sim_time=850.0,
              content="Nice — your reading streak just hit 47 days. Keep going to unlock the bookworm badge."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v8",
        events=events,
        ground_truth=gts,
        briefing=(
            "It's a slow Saturday at home and I'm working through a backlog of personal admin between cups of coffee. "
            "I've got my dog Luna, my parents on the East Coast, and a couple of half-made plans with my partner all circling in the back of my mind. "
            "Mostly I just don't want to drop any of the small commitments I've already loosely made."
        ),
        intents=(
            "remember key family dates",
            "act on time-sensitive ticket and booking offers",
            "respond promptly to personal voicemails",
            "stay alert to local emergencies",
            "keep pet care on track",
        ),
    )


def test_trace_v11() -> Trace:
    gts = [
        _gt(
            Event(id="locksmith_buzzer", kind="phone_message", sim_time=50.0,
                  content="Locksmith voicemail: 'I'm downstairs at your building's front door right now but the buzzer doesn't work. Please come let me in or call me back immediately.'"),
            window_s=25.0, keywords=("locksmith", "buzzer"),
        ),
        _gt(
            Event(id="spanish_tutoring_shift", kind="calendar_update", sim_time=200.0,
                  content="Your Spanish tutoring session originally at 15:00 today has been moved to 15:30 by your tutor."),
            window_s=180.0, keywords=("tutoring", "moved"),
        ),
        _gt(
            Event(id="bistro_wallet_holding", kind="notification", sim_time=350.0,
                  content="Lighthouse Bistro lost & found: a navy wallet matching your reservation name was turned in last night. Pickup available at the host stand until close at 23:00 today."),
            window_s=400.0, keywords=("wallet", "pickup"),
        ),
        _gt(
            Event(id="city_marathon_closures", kind="world_event", sim_time=600.0,
                  content="City marathon tomorrow morning closes most downtown streets from 7:00 to 11:30. Plan alternate routes if you're commuting through the core."),
            window_s=300.0, keywords=("marathon", "closes"),
        ),
        _gt(
            Event(id="pitch_slides_review_ask", kind="email", sim_time=820.0,
                  content="Hey — could you give feedback on the investor pitch slides before tomorrow at 9am? I'd really appreciate one last read-through with fresh eyes."),
            window_s=120.0, keywords=("slides", "feedback"),
        ),
    ]
    distractors = [
        Event(id="chess_puzzle_nudge", kind="notification", sim_time=120.0,
              content="Daily puzzle reminder from your chess app: today's mate-in-three hasn't been solved yet."),
        Event(id="printworks_payment_ack", kind="email", sim_time=280.0,
              content="Hi — just confirming we received last week's payment, thanks again for being a great client. — Mara, PrintWorks"),
        Event(id="trivia_league_round", kind="notification", sim_time=500.0,
              content="Pub Trivia League: the next casual online round opens Saturday at 19:00. Drop in if you're free."),
        Event(id="sam_article_forward", kind="email", sim_time=750.0,
              content="Sam forwarded you a link: 'Why monorepos are making a comeback'. Thought you might enjoy reading it sometime."),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v11",
        events=all_events,
        ground_truth=gts,
        briefing="I'm working from home in Portland this week while juggling a small side project and a few household errands. My partner is out of town, so apartment access, vendor visits, and stray logistics are all on me. Tomorrow I also have a downtown commute and I'm helping a friend prep for an investor pitch.",
        intents=(
            "stay reachable for time-sensitive home services",
            "support my friend's investor pitch prep",
            "recover the lost wallet before the bistro closes",
            "navigate tomorrow's downtown commute changes",
            "keep the Spanish tutoring schedule on track",
        ),
    )


def test_trace_v12() -> Trace:
    gts = [
        _gt(
            Event(id="garage_open_overnight", kind="alert", sim_time=50.0,
                  content="Smart home alert: Your garage door has been open for 47 minutes after sunset."),
            window_s=25.0, keywords=("garage", "open"),
        ),
        _gt(
            Event(id="friend_hospitalized", kind="phone_message", sim_time=180.0,
                  content="Voicemail from Sarah: Mike was hospitalized this morning with chest pains. He is stable at Memorial and she is calling close friends to update them."),
            window_s=300.0, keywords=("hospitalized", "mike"),
        ),
        _gt(
            Event(id="license_expires_today", kind="notification", sim_time=300.0,
                  content="DMV reminder: Your driver's license expires today at midnight. Online renewal must be completed before then or you cannot legally drive tomorrow."),
            window_s=600.0, keywords=("license", "expires"),
        ),
        _gt(
            Event(id="hoa_assessment_vote", kind="email", sim_time=420.0,
                  content="HOA emergency assessment vote closes today at 8pm: $3,400 special assessment per unit for foundation repair. Vote required from each owner."),
            window_s=400.0, keywords=("hoa", "vote"),
        ),
        _gt(
            Event(id="margin_account_warning", kind="email", sim_time=550.0,
                  content="Brokerage notice: Margin account requires a $4,200 deposit within 2 hours to avoid forced liquidation of held positions."),
            window_s=80.0, keywords=("margin", "deposit"),
        ),
    ]
    distractors = [
        Event(id="screen_time_report", kind="notification", sim_time=110.0,
              content="Your weekly screen time report: 4h 12m daily average, down 8% from last week."),
        Event(id="photo_backup_complete", kind="notification", sim_time=240.0,
              content="Cloud storage backup completed: 1,247 photos synced to album 'Family 2025'."),
        Event(id="grocer_back_in_stock", kind="email", sim_time=360.0,
              content="FreshGrocer: Your favorite item 'Avocado' is back in stock at your local store this week."),
        Event(id="calendar_yoga_suggest", kind="calendar_update", sim_time=500.0,
              content="Calendar suggestion: 'Yoga with Anna' on Tuesdays — would you like to add this as a recurring event?"),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v12",
        events=all_events,
        ground_truth=gts,
        briefing=(
            "I'm working from home today on a deep-focus draft for a client deliverable. "
            "The house is quiet and I want to keep distractions to a minimum. "
            "A handful of errands and life-admin items are floating in the background."
        ),
        intents=(
            "finish client draft",
            "minimize interruptions",
            "stay on top of household admin",
            "respond to genuine emergencies",
            "protect deep work blocks",
        ),
    )


def test_trace_v13() -> Trace:
    gts = [
        _gt(
            Event(id="counter_offer", kind="phone_message", sim_time=80.0,
                  content="Voicemail from agent Sara: seller submitted a counter-offer on the maple house — they want $12k more and need an answer by 5pm today."),
            window_s=600.0, keywords=("counter-offer", "agent"),
        ),
        _gt(
            Event(id="interview_confirm", kind="email", sim_time=180.0,
                  content="From Nora Patel (recruiter): confirming your onsite interview Thursday 9am. Please reply by end of day so we can release your slot if needed."),
            window_s=480.0, keywords=("interview", "reply"),
        ),
        _gt(
            Event(id="book_club_host", kind="notification", sim_time=310.0,
                  content="Book club at your place tomorrow 19:00 — you're host this round; folks expect snacks and you still owe the group a book selection."),
            window_s=240.0, keywords=("book club", "host"),
        ),
        _gt(
            Event(id="figmaster_trial", kind="alert", sim_time=420.0,
                  content="Heads up: your Figmaster trial converts to paid in 25 minutes — switch to your team's Pro seat first so tomorrow's client mockups stay on the shared workspace."),
            window_s=25.0, keywords=("trial", "converts"),
        ),
        _gt(
            Event(id="ryobi_warranty", kind="email", sim_time=700.0,
                  content="Reminder from RyobiCare: warranty on your circular saw must be registered today at midnight to retain full coverage; otherwise it drops to base 90-day."),
            window_s=300.0, keywords=("warranty", "registered"),
        ),
    ]
    distractors = [
        Event(id="meditation_nudge", kind="notification", sim_time=50.0,
              content="Insight Timer: you haven't meditated in 3 days. Take 5 minutes now?"),
        Event(id="cantina_review", kind="email", sim_time=240.0,
              content="How was Cantina Verde? Rate your meal from last Tuesday."),
        Event(id="phone_battery_low", kind="notification", sim_time=380.0,
              content="Battery at 20%. Plug in soon to keep notifications running."),
        Event(id="calendar_week_digest", kind="notification", sim_time=800.0,
              content="Your week ahead: 12 events between Wednesday and Sunday."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v13",
        events=events,
        ground_truth=gts,
        briefing=(
            "It's a Wednesday in mid-spring and I'm working from home while a real estate offer on a house we love is in active back-and-forth. "
            "I have a recruiter pushing for confirmation on a Thursday interview and a client demo I need to be ready for tomorrow morning. "
            "I want the assistant to flag only things that actually need a decision before end of day."
        ),
        intents=(
            "close the maple house deal",
            "lock in the Thursday interview",
            "be ready for tomorrow's client demo",
            "honor small social commitments",
            "ignore routine noise",
        ),
    )


def test_trace_v14() -> Trace:
    gts = [
        _gt(
            Event(id="backup_codes_rotating", kind="notification", sim_time=40.0,
                  content="Account two-factor backup codes are being rotated in 25 seconds; once rotation completes, current codes become invalid — save or print the new codes shown on screen now."),
            window_s=20.0, keywords=("backup", "codes"),
        ),
        _gt(
            Event(id="inspector_walkthrough_advanced", kind="calendar_update", sim_time=150.0,
                  content="Today's 1:30 PM walkthrough of 426 Pine with the structural inspector has been moved up to 11:30 AM at the seller's request; bring the punch list and the disclosure packet."),
            window_s=120.0, keywords=("walkthrough", "inspector"),
        ),
        _gt(
            Event(id="movers_swap_slot", kind="phone_message", sim_time=220.0,
                  content="Voicemail from Hiroshi at City Movers: 'Driver opened up a 7 AM slot tomorrow instead of your 2 PM booking — needs a yes or no in the next hour or it goes to someone else.'"),
            window_s=240.0, keywords=("movers", "slot"),
        ),
        _gt(
            Event(id="bond_purchase_confirm", kind="email", sim_time=380.0,
                  content="Your Treasury Direct purchase order for $10,000 in Series I savings bonds requires final confirmation by end of business today (5:00 PM ET); without it the order will be cancelled and the rate locked-in window will be forfeited."),
            window_s=600.0, keywords=("bond", "confirmation"),
        ),
        _gt(
            Event(id="boil_water_zip", kind="world_event", sim_time=480.0,
                  content="Public utility advisory: a boil-water notice is now in effect for your zip code through tomorrow evening; do not consume tap water or use it for cooking without boiling for at least one minute."),
            window_s=480.0, keywords=("boil-water", "tap"),
        ),
    ]
    distractors = [
        Event(id="beanwise_promo_20pct", kind="email", sim_time=15.0,
              content="Promotional: 20% off your next refill at Beanwise — use code GRIND20 at checkout, expires Friday."),
        Event(id="sticker_packs_added", kind="notification", sim_time=95.0,
              content="Your messaging app added three new sticker packs you can use in DMs; tap to browse."),
        Event(id="editor_focus_tip", kind="notification", sim_time=310.0,
              content="Tip: try the new 'focus mode' in your editor for distraction-free writing — tap to learn more."),
        Event(id="design_weekly_digest", kind="email", sim_time=720.0,
              content="Design Weekly: seven articles you might enjoy in product design this week, plus a roundup of new component libraries."),
    ]
    all_events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v14",
        events=all_events,
        ground_truth=gts,
        briefing="I'm working from my home office in Chicago today while juggling a small move next week and an active offer on a unit on Pine Street. My inbox fills up with low-signal newsletters and app tips, so I rely on Claude to flag what genuinely needs me. Treasury Direct, the movers, and a structural walkthrough are all in motion in parallel.",
        intents=(
            "Don't miss high-stakes financial confirmation windows",
            "Keep moving logistics and same-day reschedules on track",
            "Protect attention from app, promo, and newsletter noise",
            "Surface account-security alerts within seconds",
            "Be ready to act on public health or utility advisories",
        ),
    )


def test_trace_v15() -> Trace:
    gts = [
        _gt(
            Event(id="skip_level_addition", kind="calendar_update", sim_time=55.0,
                  content="Skip-level 1:1 with Ravi added to your calendar at 2:00 PM today. Tentative — accept, decline, or propose a new time before end of day."),
            window_s=600.0, keywords=("1:1", "skip-level"),
        ),
        _gt(
            Event(id="baby_shower_gift_close", kind="email", sim_time=120.0,
                  content="Last call for Priya's baby shower group gift — the collection closes at 11:30 today before we place the order. Venmo @teampriya if you're chipping in."),
            window_s=420.0, keywords=("baby shower", "collection"),
        ),
        _gt(
            Event(id="visa_autopay_low_balance", kind="alert", sim_time=230.0,
                  content="Heads up: your Visa auto-payment of $843 is scheduled for tonight, but your checking balance is currently $612. Move funds or the payment will reverse."),
            window_s=480.0, keywords=("auto-payment", "balance"),
        ),
        _gt(
            Event(id="olia_reservation_hold", kind="notification", sim_time=360.0,
                  content="Your reservation at Olia tonight at 7:30 will auto-cancel in 15 minutes unless you tap Confirm."),
            window_s=30.0, keywords=("reservation", "auto-cancel"),
        ),
        _gt(
            Event(id="brake_job_approval", kind="phone_message", sim_time=510.0,
                  content="This is Sal at Pinewood Auto — your brake pads are shot. If you approve the $480 brake job before 3 PM I can finish it today, otherwise it pushes to next Tuesday."),
            window_s=120.0, keywords=("brake", "approve"),
        ),
    ]
    distractors = [
        Event(id="utility_usage_summary", kind="email", sim_time=25.0,
              content="Your April electricity usage was 312 kWh — 4% below your 12-month average. No action needed."),
        Event(id="coffee_subscription_promo", kind="email", sim_time=180.0,
              content="Spring beans are here — take 15% off your next Roastery House bag with code BLOOM15. Offer good through the month."),
        Event(id="streaming_new_releases", kind="notification", sim_time=295.0,
              content="New this week on Plume: 4 series and 9 films added in your watchlist's genres. Open the app to browse."),
        Event(id="smart_speaker_firmware", kind="notification", sim_time=470.0,
              content="Your Lumen Mini speaker installed firmware 8.4.1 overnight. Voice quality improvements; no setup required."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v15",
        events=events,
        ground_truth=gts,
        briefing=(
            "Working from home today between calls and an evening dinner I still haven't confirmed. "
            "A few small commitments are piling up — a coworker's group gift closing midmorning, a calendar surprise from my skip-level, and a car at the shop waiting on my call. "
            "I'd like to be left alone unless something genuinely needs me to act in the next hour."
        ),
        intents=(
            "act on today-only windows before they close",
            "respond to humans waiting on my decision",
            "avoid surfacing routine digests and promos",
            "keep money from bouncing or being wasted",
            "follow through on commitments to family and coworkers",
        ),
    )


def test_trace_v21() -> Trace:
    gts = [
        _gt(
            Event(id="gas_leak_kitchen_sensor", kind="alert", sim_time=15.0,
                  content="Sensor in kitchen detected a natural-gas leak — concentration above safety threshold. Open windows; do NOT operate switches or appliances. Evacuate and call the gas company immediately."),
            window_s=60.0, keywords=("gas", "leak"),
        ),
        _gt(
            Event(id="cardio_appt_rescheduled", kind="phone_message", sim_time=100.0,
                  content="Voicemail from Northwest Cardiology: your appointment with Dr. Park scheduled for Thursday 10am has been rescheduled to Friday 2pm. Please call back to confirm the new slot."),
            window_s=600.0, keywords=("appointment", "rescheduled"),
        ),
        _gt(
            Event(id="vinyl_drop_press_today", kind="notification", sim_time=200.0,
                  content="Vinyl drop alert: Sault's 'Earth' double-LP first pressing — 250 copies, dropping at 14:30 today. The shop's purchase queue is open for 30 minutes; first-come, first-served. Once gone, no second pressing."),
            window_s=25.0, keywords=("vinyl", "drop"),
        ),
        _gt(
            Event(id="student_loan_repayment_resume", kind="email", sim_time=250.0,
                  content="Your federal student loan auto-debit resumes in 48 hours after the COVID pause. Current minimum payment: $342/month. To request an income-driven repayment plan instead, you must apply at studentaid.gov within the next 48 hours."),
            window_s=480.0, keywords=("loan", "repayment"),
        ),
        _gt(
            Event(id="legal_doc_courier_signature", kind="notification", sim_time=400.0,
                  content="Courier from Whitfield & Holst delivering certified legal documents requiring your signature is at the lobby. They can only release to you in person and will wait 15 minutes before returning to sender."),
            window_s=20.0, keywords=("courier", "signature"),
        ),
    ]
    distractors = [
        Event(id="restock_camping_lantern", kind="email", sim_time=50.0,
              content="Good news — the Goal Zero Lighthouse Mini lantern you saved last fall is back in stock at Adventure Outfitters. We've replenished the stock; browse when ready. No purchase deadline or quantity limit at this time."),
        Event(id="calendar_running_club_recur", kind="notification", sim_time=150.0,
              content="Calendar suggestion: I noticed you've gone running with Maya three Thursdays in a row. Add 'Thursday run with Maya' as a recurring weekly event? Suggestion only — dismiss or set up later."),
        Event(id="arcade_meetup_kira", kind="notification", sim_time=300.0,
              content="Kira's organizing a casual arcade night at Quarterworld this Saturday around 7pm. No commitment, no RSVP — show up if you're free."),
        Event(id="discord_unread_digest", kind="notification", sim_time=700.0,
              content="You have 12 unread messages across 3 Discord servers: #react-discussion (4), #portland-coffee (5), and #book-recs (3). Open the app to catch up when you have time."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v21",
        events=events,
        ground_truth=gts,
        briefing=(
            "Friday morning at home in Portland. "
            "I've blocked the day for a stack of personal errands and an evening commitment with friends. "
            "My phone's on do-not-disturb but I want anything genuinely urgent to surface so I don't miss it."
        ),
        intents=(
            "knock through Friday errands",
            "DND mode for noise",
            "evening commitment with friends",
            "don't miss urgent items",
            "no late fees or missed slots",
        ),
    )


def test_trace_v22() -> Trace:
    gts = [
        _gt(
            Event(id="grandpa_90th_birthday_tomorrow", kind="notification", sim_time=80.0,
                  content="Reminder pinned by Mom in the family chat: Grandpa Walter's 90th birthday party is tomorrow at 1pm at the Riverview Country Club ballroom. All five siblings and twelve cousins are flying or driving in; you signed up to give the toast at the cake-cutting. You haven't written it yet, and the rehearsal-dinner photos confirm everyone is expecting it."),
            window_s=480.0, keywords=("grandpa", "birthday"),
        ),
        _gt(
            Event(id="flash_flood_warning_overnight", kind="alert", sim_time=220.0,
                  content="NWS flash flood warning issued for King County through 6am Friday: 4-6 inches of rain expected overnight; low-lying roads on the I-5 corridor expected to close; your morning commute route on Westlake Avenue is inside the warning zone. Local authorities advise the I-405 alternate."),
            window_s=300.0, keywords=("flood", "warning"),
        ),
        _gt(
            Event(id="datastore_replica_failover_p1", kind="alert", sim_time=380.0,
                  content="PagerDuty P1 [primary-postgres-001]: database failover triggered at 04:47 UTC; writes failing with SQLSTATE 08006; on-call rotation lists you as primary for the payments-data shard. Promotion ETA is 10 minutes; estimated customer-facing downtime ~12 minutes if not resolved by 04:57."),
            window_s=60.0, keywords=("database", "failover"),
        ),
        _gt(
            Event(id="aging_parent_fall_alert_emergency_pendant", kind="alert", sim_time=480.0,
                  content="Medical-alert pendant for your father (Robert) triggered fall-detection at 6:42am; automatic EMS dispatch was confirmed; you are listed as the primary emergency contact. The pendant operator is on the line awaiting your callback to coordinate hospital handoff; ambulance ETA to his address is 8 minutes."),
            window_s=30.0, keywords=("fall", "pendant"),
        ),
        _gt(
            Event(id="property_tax_installment_due_today", kind="notification", sim_time=560.0,
                  content="King County Treasurer reminder: your property tax first-installment payment of $3,180 is due today by 5pm. Pay via the online portal at kingcounty.gov/treasury or in person at the courthouse cashier. Late-payment penalty of 10% applies if not paid by today's 5pm cutoff; certified collection notice mails on day 31."),
            window_s=300.0, keywords=("property", "tax"),
        ),
    ]
    distractors = [
        Event(id="sneakers_wishlist_back_in_stock_email", kind="email", sim_time=20.0,
              content="Good news from SneakerVault: your wishlist item, the Nike Air Max 90 (size 11, Triple White), is back in stock. We've restocked plenty of pairs; no rush, no quantity limit. Shop when you're ready — orders ship within 5-7 business days at standard prices."),
        Event(id="calendar_coffee_lisa_weekly_suggest", kind="notification", sim_time=140.0,
              content="Google Calendar suggestion: We noticed you have met Lisa for coffee five Wednesdays in a row at 9am at Heart Coffee. Would you like to add 'Wednesday coffee with Lisa' as a recurring weekly event? Options: Add weekly / Add once / Dismiss. No deadline — suggestion only."),
        Event(id="pickup_basketball_saturday_open", kind="notification", sim_time=300.0,
              content="Text from Marco: hey, we're running pickup 5-on-5 at the Wallingford courts Saturday at 10am. Totally casual, no commitment — show up if you feel like it, ignore if you're busy. Same crew as last month."),
        Event(id="chrome_extension_marketplace_update", kind="email", sim_time=680.0,
              content="Chrome announcement: we've updated the extension review system in the Chrome Web Store. Visit the marketplace homepage to browse newly featured extensions and read the updated reviewer guidelines. No action required."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v22",
        events=events,
        ground_truth=gts,
        briefing=(
            "Tuesday morning at home in Seattle. "
            "Code review due by EOD on a payments-data migration, and I'm also on the on-call rotation through tonight. "
            "Focus mode is on for my IM apps; I want only urgent items or genuine time-sensitive obligations to break through — routine pings and casual social can wait until evening."
        ),
        intents=(
            "ship the payments-data review by EOD",
            "on-call rotation tonight",
            "focus mode for IM noise",
            "don't miss urgent items",
            "no missed deadlines or family obligations",
        ),
    )


def test_trace_v23() -> Trace:
    gts = [
        _gt(
            Event(id="court_hearing_moved_same_day_default_risk", kind="email", sim_time=120.0,
                  content="Court clerk email: your small-claims hearing #SC-24-3812 (Acme Plumbing vs. you, $4,200) originally scheduled for today 2pm has been moved to today 11am on Judge Calderon's reassigned docket. Confirm appearance by 10am via the eFile portal or you will be in default; default judgment plus collection proceedings follow automatically."),
            window_s=300.0, keywords=("court", "hearing"),
        ),
        _gt(
            Event(id="homeowner_insurance_lapse_72h_notice", kind="email", sim_time=260.0,
                  content="Liberty Mutual insurance notice: your homeowner insurance auto-debit failed at last billing cycle (the linked checking transfer was returned NSF) and the policy will lapse in 72 hours unless payment of $2,470 clears via the carrier portal. After lapse, your mortgage lender is auto-notified and force-placed coverage begins at $300 per month above your prior premium."),
            window_s=600.0, keywords=("insurance", "lapse"),
        ),
        _gt(
            Event(id="partner_voicemail_ring_pickup_jeweler", kind="phone_message", sim_time=380.0,
                  content="Voicemail from your partner Mira: please swing by Goldsmiths on Roosevelt Row this afternoon for the pickup of the resized wedding ring; her own 3pm meeting ran long. The shop closes at 5pm sharp with no weekend hours, so if the ring is not collected today it sits in the safe until next Friday. She asked you to call back to confirm."),
            window_s=240.0, keywords=("ring", "pickup"),
        ),
        _gt(
            Event(id="dust_storm_warning_freeway_visibility", kind="alert", sim_time=540.0,
                  content="NWS dust storm warning for Maricopa County through 8pm tonight: sustained 50+ mph wind gusts kicking up dense dust along I-10 between Phoenix and Tucson; visibility may drop below a quarter-mile. Driver advisory: pull off the freeway and turn lights off if caught in zero-visibility. Your afternoon drive to the Tucson conference passes through the warned corridor."),
            window_s=200.0, keywords=("dust", "storm"),
        ),
        _gt(
            Event(id="tls_cert_expiry_3hr_customer_endpoint", kind="alert", sim_time=720.0,
                  content="PagerDuty P2 from Datadog synthetic monitor: the TLS certificate for api.acmewidgets.com (your team's customer-facing billing-webhook endpoint) expires at 16:32 PST today; current time 13:14 PST leaves 3 hours 18 minutes to issue and deploy the renewal via cert-manager. Customer billing webhooks will return 502 on expiry; the rotation runbook lists you as primary."),
            window_s=120.0, keywords=("tls", "expiry"),
        ),
    ]
    distractors = [
        Event(id="cloud_backup_daily_success_digest", kind="email", sim_time=60.0,
              content="Daily backup digest from CloudStash: yesterday's incremental snapshot completed successfully — 2.3 GB across 14,820 files; zero errors; next snapshot tonight at 2am. All systems normal. Manage notification preferences in your account settings."),
        Event(id="kitchen_gear_quarterly_digital_magazine", kind="email", sim_time=180.0,
              content="Fresh off the press: Kitchen Gear Quarterly Spring issue — 28 pages on stand-mixer testing, knife sharpening across budget tiers, and a roundup of seasonal cookbook reviews. Read at your leisure online or download the PDF for offline browsing. Unsubscribe at any time from the footer link."),
        Event(id="morning_briefing_no_urgent_items_today", kind="notification", sim_time=440.0,
              content="Wednesday morning briefing: your calendar has 2 scheduled items (10am team standup, 3pm 1:1 with Sara); inbox sits at 47 unread; outdoor air quality moderate. No time-sensitive items flagged for today. Have a productive day."),
        Event(id="notion_new_dashboard_feature_tour", kind="email", sim_time=620.0,
              content="Notion product announcement: our new analytics dashboard is rolling out to every workspace this month. Take the 2-minute interactive tour to explore the pivot views and AI-generated summaries. No action required on your end — the feature is opt-in via the workspace settings menu whenever you are ready."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v23",
        events=events,
        ground_truth=gts,
        briefing=(
            "Wednesday afternoon at home in Phoenix. "
            "I'm prepping for a small-claims hearing this afternoon, expecting a customer-facing TLS rotation handoff before EOD, and a couple of personal admin items are lingering. "
            "Notifications are muted by default — only obviously urgent or genuinely time-bound items should break through; routine digests and promotional emails can wait."
        ),
        intents=(
            "represent myself at the small-claims hearing today",
            "TLS cert rotation handoff before end of day",
            "keep heads-down on focused work between commitments",
            "do not miss urgent or hard-deadline items",
            "minimal interruption from routine pings and promos",
        ),
    )


def test_trace_v24() -> Trace:
    gts = [
        _gt(
            Event(id="carbon_monoxide_alarm_evacuate_call_gas_company", kind="alert", sim_time=80.0,
                  content="Indoor carbon monoxide alarm triggered in the basement utility room: sensor reads 95 ppm CO and climbing; the safe threshold is 9 ppm. Evacuate the house immediately with all family members and pets, leave doors open behind you, and dial the gas company emergency line from outside. Do not re-enter until first responders give the all-clear."),
            window_s=180.0, keywords=("carbon", "monoxide"),
        ),
        _gt(
            Event(id="pediatrician_visit_advanced_today_4pm", kind="email", sim_time=210.0,
                  content="Pediatrician's office: we've advanced your child's 4-year-old wellness visit from Tuesday next week to today at 4pm because Dr. Albright had a cancellation and wants to fit you in before her two-week leave begins tomorrow. Please confirm or call back to decline by 1pm so we can offer the open slot to another family on the waitlist."),
            window_s=300.0, keywords=("pediatrician", "advanced"),
        ),
        _gt(
            Event(id="hospital_grandmother_hip_fracture_next_of_kin_callback", kind="phone_message", sim_time=340.0,
                  content="Voicemail from St. Vincent's hospital admitting desk: your grandmother Eleanor was admitted through emergency in the last hour with a left hip fracture from a fall at home; she is stable but the chart lists you as next-of-kin proxy. Charge nurse Tanya asked that you call ward 4-North directly to discuss surgical consent and transfer logistics before evening rounds at 8pm."),
            window_s=240.0, keywords=("hospital", "grandmother"),
        ),
        _gt(
            Event(id="tornado_watch_tri_county_peak_risk_tonight", kind="alert", sim_time=500.0,
                  content="National Weather Service tornado watch issued for your tri-county area through 11pm tonight: rotation-supported supercells moving east-northeast at 55 mph with hail to two-inch diameter; peak tornado risk window 4pm to 9pm. A watch is not yet a warning, but conditions strongly favor tornado development — review your shelter plan, charge devices, and monitor radio for upgrades."),
            window_s=300.0, keywords=("tornado", "watch"),
        ),
        _gt(
            Event(id="disk_space_critical_var_log_api_host_oom_90min", kind="alert", sim_time=720.0,
                  content="PagerDuty P2 from infra-mon: disk space critical on api-prod-host-07 — /var/log is filling at roughly 200 MB per minute thanks to a runaway debug-log flag in the new release; current free space 1.4 GB on a 40 GB partition; projected OOM-style kill on the request handler within 90 minutes if not addressed. You are listed as primary on the storage-rotation runbook this week."),
            window_s=150.0, keywords=("disk", "space"),
        ),
    ]
    distractors = [
        Event(id="ssl_monitor_weekly_digest_no_rotations_required", kind="email", sim_time=30.0,
              content="Weekly SSL monitor digest: all 47 certificates across your managed properties are valid; the longest-lived expires in 84 days; no rotations are required this week; one scheduled renewal is queued for next Tuesday's automation window. No action items at this time. Configure digest cadence or recipients in the monitor console."),
        Event(id="tea_club_monthly_subscriber_tasting_newsletter", kind="email", sim_time=160.0,
              content="Steeped & Found Tea Club: your March subscriber edition is on its way — three single-estate Darjeeling first-flush samples, brewing notes from the head taster, and an interview with the harvest manager in Kurseong. The tracking number will arrive separately when your box ships. Manage cadence or pause shipments anytime from your account dashboard."),
        Event(id="evening_briefing_no_pending_items_tomorrow_clear", kind="notification", sim_time=430.0,
              content="End-of-day briefing: your inbox is down to 8 unread; tomorrow's calendar holds one 10:30 am 1:1 and otherwise the day's blocks are clear; outdoor air quality forecast is good across the metro; no items pending your action and nothing time-sensitive is flagged before tomorrow morning. Wind down well."),
        Event(id="slack_frontend_weekly_community_invite", kind="email", sim_time=600.0,
              content="You've been invited to join the Frontend Weekly Slack community — about 12,000 engineers swapping reviews, code samples, and meetup announcements across React, Vue, and Svelte. Membership is free; introductions thread runs on Mondays. Accept the invite link in the footer or simply ignore this message if it isn't relevant."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v24",
        events=events,
        ground_truth=gts,
        briefing=(
            "Thursday morning at home. "
            "The kid is at school today and I'm working from the home office, with our infrastructure on-call rotation handing the storage-runbook duty over to me at lunchtime. "
            "Notifications are filtered to urgent: family-safety, hospital-family, severe-weather, and production-incident signals should break through, and routine digests, marketing, and casual invites can stack up for later."
        ),
        intents=(
            "respond to genuine family-safety and family-medical signals immediately",
            "cover the production storage-rotation duty through the rest of today",
            "stay focused on the spec review draft due tomorrow",
            "do not lose any hard-deadline items in the noise",
            "let routine digests and promotional pings wait until the end of the day",
        ),
    )


def test_trace_v25() -> Trace:
    gts = [
        _gt(
            Event(id="parents_fiftieth_anniversary_dinner_tomorrow_toast_request", kind="phone_message", sim_time=120.0,
                  content="Voicemail from your sister Diane: this is the final reminder about Mom and Dad's fiftieth wedding anniversary dinner tomorrow night at 7pm at Boulevard — you're the only one Mom's asked to give the family toast, Mark and Carol are both flying in from Seattle and Boston for this single evening and heading straight back Friday morning, and the only time the four of you will be together all year is between courses. Please confirm by tomorrow noon so the maître d' can finalize seating and Mom can stop worrying."),
            window_s=240.0, keywords=("anniversary", "fiftieth"),
        ),
        _gt(
            Event(id="child_medication_ingestion_poison_control_emergency_call", kind="phone_message", sim_time=320.0,
                  content="Found your three-year-old in the bathroom with the cap off your migraine antihistamines and at least four pills missing from the pack. Poison Control just called back: bring the child and the medication bottle to the emergency room right now — do not induce vomiting at home. Estimated ingestion under twenty minutes ago; ER triage is expecting you and the medication when you arrive, and is asking you to call back from the car with a weight estimate."),
            window_s=120.0, keywords=("medication", "ingestion"),
        ),
        _gt(
            Event(id="dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency", kind="phone_message", sim_time=480.0,
                  content="Voicemail from Dr. Patel's oral surgery office: your dental implant procedure scheduled for tomorrow 8am must be pushed because the surgeon is being called into an emergency case this evening for another patient. The earliest slot we can offer is next Wednesday 7am or the following Thursday 11am — please call back by 6pm today to lock one in, otherwise we'll need to release the anesthesia booking and you'll be at the back of next month's queue."),
            window_s=180.0, keywords=("dental", "implant"),
        ),
        _gt(
            Event(id="quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm", kind="email", sim_time=620.0,
                  content="IRS reminder: your Q3 quarterly estimated tax payment is due by 5pm Eastern today via EFTPS for the 1040-ES installment covering July through September. Failing to pay by the 5pm cutoff triggers underpayment penalty calculation back to the April safe-harbor anchor plus a charge of roughly half a percent per month against the shortfall until the balance is paid. Bank ACH cutoff for next-day settlement is 8pm; the EFTPS receipt arrives within 24 hours of submission."),
            window_s=200.0, keywords=("quarterly", "tax"),
        ),
        _gt(
            Event(id="redis_memory_saturation_eviction_cascade_120min_outage_risk", kind="alert", sim_time=790.0,
                  content="PagerDuty P1 from infra-mon: redis-prod-cluster-01 memory saturation alert — used memory at 13.4 GB on a 14 GB allocation; the allkeys-lru eviction policy is throwing OOM errors back to the API gateway at roughly 200 evictions per second; session-cache hit rate has collapsed from 98% to 41% over the last ten minutes and queue depth is climbing. You're listed as primary on the cache-tier runbook this week; full session outage projected if the working set hits the 14 GB hard cap within roughly 120 minutes at the current write rate."),
            window_s=180.0, keywords=("redis", "memory"),
        ),
    ]
    distractors = [
        Event(id="kubernetes_autoscaler_monthly_cluster_health_report_nominal", kind="email", sim_time=60.0,
              content="Monthly cluster-health digest for prod-k8s-01: all 47 node groups stayed within HPA target bands; the cluster-autoscaler scaled up 8 times and down 12 times this period with no failed scaling events; spot-instance interrupt rate at 0.3%, inside the historical 0.2 to 0.4 percent band; control-plane API latency p99 at 84ms. No anomalies were detected this cycle. The next health digest is scheduled for the first of next month."),
        Event(id="inkwell_indie_bookstore_quarterly_preorder_catalog_winter", kind="email", sim_time=240.0,
              content="Inkwell Books winter preorder catalog is live: 23 forthcoming titles handpicked by our staff, including new releases from Marisa Crane and Tony Tulathimutte, plus exclusive signed bookplates for the first 50 preorders of each title. Shipping in late December or early January depending on the publisher schedule. Browse the catalog at your leisure and reply with any questions. Manage email cadence in your account preferences."),
        Event(id="friday_weekly_recap_briefing_no_outstanding_items", kind="notification", sim_time=550.0,
              content="Friday afternoon recap: this week you closed 14 tickets, attended 11 meetings averaging 38 minutes each, and sent 87 emails with a 92 percent reply rate within 24 hours. Inbox is at 4 unread; next week's calendar shows two heads-down blocks and one cross-team review on Wednesday. No outstanding items are flagged for your attention before Monday morning. Enjoy the weekend."),
        Event(id="vscode_marketplace_verified_publisher_tab_launch_announcement", kind="notification", sim_time=710.0,
              content="Visual Studio Code marketplace: we've launched a new Verified Publisher tab in the extensions sidebar — extensions from publishers with multi-factor account verification and signed publisher manifests now surface in a curated panel for easier discovery. Existing extension installation flows are unchanged and no migration is needed. The feature is on by default and can be toggled in the marketplace settings panel."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v25",
        events=events,
        ground_truth=gts,
        briefing=(
            "Tuesday afternoon at home in Madison. "
            "Our three-year-old is just back from preschool and napping, I'm covering the cache-tier production rotation this week, the Q3 estimated-tax window closes today, and the family group chat has been buzzing about a milestone family dinner tomorrow night. "
            "Notifications are filtered for urgent: child-safety, family-personal, hard-deadline financial, and production-incident signals should break through; routine reports and promotional emails can stack up for later."
        ),
        intents=(
            "respond instantly to any child-safety signal",
            "hold the cache-tier production rotation through end of day",
            "do not miss any hard-deadline financial or medical-admin item",
            "be present for the family-milestone obligation from the group chat",
            "let routine reports and promotional emails wait until the end of the day",
        ),
    )


def test_trace_v26() -> Trace:
    gts = [
        _gt(
            Event(id="lagavulin_single_cask_allocation_38min_window_distillery", kind="email", sim_time=210.0,
                  content="Lagavulin distillery cask-share allocation notice for registered members: the 2002 vintage single-cask special release has just opened a thirty-eight minute allocation window. Exactly three hundred and twelve bottles were produced, one bottle per member, with claim-or-release rolling at sixty-second intervals once the queue advances. You are currently at position forty-seven and your hold expires in roughly thirty-eight minutes if you do not claim; once the window closes the remaining bottles route to the trade-only secondary list and are not offered back to the member queue."),
            window_s=240.0, keywords=("lagavulin", "allocation"),
        ),
        _gt(
            Event(id="mother_in_law_chemo_infusion_ride_request_voicemail_6pm", kind="phone_message", sim_time=440.0,
                  content="Voicemail from your mother-in-law Elena: hi sweetie, I hate to ask but my regular ride to oncology fell through and the chemo infusion is at eight in the morning tomorrow at Memorial. The protocol is roughly four hours in the chair, so I need someone who can stay through and drive me home because I am too groggy to do it on my own afterward. Please call back tonight before six if you can take me; otherwise I need to call the patient-transport line and they cut off bookings at seven sharp."),
            window_s=200.0, keywords=("chemo", "infusion"),
        ),
        _gt(
            Event(id="wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter", kind="alert", sim_time=360.0,
                  content="NWS AirNow advisory for your zip code: particulate-matter readings from the Hazelnut Ridge wildfire smoke plume have pushed the regional Air Quality Index from two-forty up to four-twenty-one over the last hour, well into the hazardous tier above the very-unhealthy band. All outdoor activity is discouraged for the next four hours minimum; close exterior windows, run HVAC on recirculate with HEPA filtration if available, and N95 masks are recommended for any unavoidable outdoor exposure. Sensitive groups, infants, and anyone with cardiac or respiratory conditions should shelter indoors until the AQI drops back below one-fifty."),
            window_s=240.0, keywords=("wildfire", "smoke"),
        ),
        _gt(
            Event(id="iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying", kind="email", sim_time=520.0,
                  content="Email from Carta equity admin: your incentive stock option grant from your March separation has its post-termination ISO exercise window expiring tomorrow at five in the afternoon Pacific. The remaining grant balance is twenty-four hundred shares at a strike price of fourteen dollars and twenty cents per share; partial exercise is allowed in lots of one hundred shares with same-day funded clearing. Failure to exercise by the deadline forfeits the entire remaining balance and the disqualifying-disposition treatment for current-tax-year ISO conversions will not apply to the lapsed shares. Wire instructions are in the attached one-page PDF."),
            window_s=220.0, keywords=("iso", "exercise"),
        ),
        _gt(
            Event(id="partner_anaphylaxis_epipen_911_dispatched_second_dose_needed", kind="alert", sim_time=620.0,
                  content="Your partner just collapsed at the kitchen counter after eating from a takeout container labeled pad thai with peanuts; visible facial swelling and severe wheezing within ninety seconds, classic anaphylaxis presentation. EpiPen administered to the outer thigh; nine-one-one dispatched and confirmed paramedics six minutes out. The home kit has only one EpiPen and the live nine-one-one dispatcher is asking on speaker whether you have a second dose somewhere in the house because symptoms are not responding to the first injection within the expected three-minute window."),
            window_s=90.0, keywords=("anaphylaxis", "epipen"),
        ),
    ]
    distractors = [
        Event(id="monday_week_lookahead_briefing_no_priority_items_flagged", kind="notification", sim_time=30.0,
              content="Monday morning week-look-ahead briefing: you have nine meetings scheduled this week, down from thirteen last week, three of them recurring one-on-ones and two cross-team syncs already on the books. Calendar shows three two-hour heads-down blocks Tuesday through Thursday. Inbox is at twelve unread with all twelve categorized routine. No priority items are flagged from your project list, OKR scorecards, or stakeholder asks. Have a focused week."),
        Event(id="datadog_synthetic_monitoring_daily_heartbeat_all_pass_digest", kind="email", sim_time=75.0,
              content="Daily DataDog synthetic-monitoring digest for prod-monitoring-pipeline: two-hundred-and-forty-seven synthetic browser checks completed in the last twenty-four hours with two-hundred-and-forty-seven of two-hundred-and-forty-seven passing on first attempt across all geographic regions, including us-east, us-west, eu-central, and ap-southeast. API endpoint checks: one-thousand-eight-hundred-twenty-four of one-thousand-eight-hundred-twenty-four returned expected status codes within the p95 latency budget. No alerts triggered. The next synthetic-monitoring digest sends tomorrow at the same time."),
        Event(id="mastodon_instance_follow_suggestion_weekly_digest_kind_strangers", kind="notification", sim_time=110.0,
              content="Your Mastodon instance hachyderm.io weekly digest: based on the accounts you already follow and your reading patterns, we suggest following these eight accounts this week — three software-engineering generalists from federated instances, two technical writers, two systems-engineering folks, and one cybersecurity researcher. Click through to preview each account's last fifty posts; no auto-follow happens. The digest sends every Sunday and you can mute the suggestion stream in notification preferences if you find it noisy."),
        Event(id="aperture_camera_gear_spring_catalog_email_no_action_required", kind="email", sim_time=290.0,
              content="Aperture Photo Supply spring catalog is now available — explore sixty-four new releases from Fujifilm, Sony, and Sigma, plus seasonal accessory bundles featuring rebated lighting kits and entry-level tripod packages. The catalog includes detailed lens-comparison charts, sample image galleries, and a community-contributed buying-guide for first-time mirrorless purchasers. Browse at your leisure; unsubscribe from seasonal mailings in your account preferences if you prefer fewer messages."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v26",
        events=events,
        ground_truth=gts,
        briefing=(
            "Monday morning at home in Bend, Oregon. "
            "Recently separated from my prior startup employer in March, navigating the post-termination ISO exercise window and a parallel cap-table cleanup; my partner with a documented peanut allergy lives with me and we keep a stocked EpiPen kit in the kitchen. "
            "The Hazelnut Ridge fire complex is burning thirty miles west and the air-quality has been roller-coastering all week. My mother-in-law in Portland started a new chemo protocol last month and her transport options are unreliable. "
            "Notifications are filtered for urgent: medical-emergency, hard-deadline financial, weather alerts that change my plans, and personal voicemails from family should break through; routine status pings, marketing emails, social-channel digests, and the daily briefing can wait."
        ),
        intents=(
            "respond instantly to any medical-emergency involving my partner with the EpiPen kit and 911 coordination",
            "do not let the ISO exercise window expire — partial-exercise lots are funded but the deadline is firm",
            "act on any AQI hazardous-tier wildfire-smoke alert with indoor shelter and HEPA HVAC",
            "take any family-elder voicemail in time to respond before tonight's cutoff",
            "let routine status, social-channel digests, marketing catalogs, and the briefing wait until evening",
        ),
    )


def test_trace_v27() -> Trace:
    gts = [
        _gt(
            Event(id="self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics", kind="alert", sim_time=660.0,
                  content="Sudden onset of chest pressure radiating down the left arm with cold sweat and a wave of nausea while you were sitting at the kitchen table; classic acute coronary presentation in a person with documented family history of premature myocardial infarction. Nine-one-one has already been called from your phone and the live dispatcher is on speaker walking you through the protocol: chew one full-strength aspirin tablet immediately, unlock the building lobby door so paramedics do not lose minutes at the buzzer, and have your medication list and primary-care contact number ready when they arrive. Ambulance estimated arrival is four minutes; the dispatcher is asking whether anyone else is in the house with you who can ride along to the hospital."),
            window_s=90.0, keywords=("aspirin", "dispatcher"),
        ),
        _gt(
            Event(id="uscis_naturalization_interview_rescheduled_friday_8am_field_office", kind="email", sim_time=220.0,
                  content="USCIS field-office adjudications officer notice for receipt number MSC-2024-22-XXXX: your N-400 naturalization interview originally scheduled for tomorrow morning at eight a.m. has been rescheduled to Friday morning at eight a.m. due to officer reassignment in your panel. Reply to confirm acceptance of the new slot before tomorrow noon Pacific or the rescheduled slot defaults to a forced cancellation and the case returns to the back of the field-office docket with an estimated six-month delay to reschedule. Bring the original civic-knowledge documents listed in the prior interview notice plus two updated passport-style photographs to the rescheduled appointment at the downtown Seattle field office."),
            window_s=240.0, keywords=("uscis", "interview"),
        ),
        _gt(
            Event(id="fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k", kind="email", sim_time=480.0,
                  content="Email from your federal tax preparer with FinCEN-114 FBAR filing materials attached: this is the final-day reminder that your foreign-bank-account aggregate balance exceeded the ten-thousand-dollar reportable threshold at multiple points during last calendar year and the extended October fifteenth deadline lapses at eleven fifty-nine tonight Pacific. The FBAR form has been pre-filled with the residual Berlin postdoc-era account plus the dormant Lisbon savings sub-account from the sabbatical year; sign the e-file authorization through the secure portal link below to submit before the cutoff. Willful-failure-to-file civil penalties run to the greater of one-hundred-twenty-nine-thousand-two-hundred-ten dollars per violation or fifty percent of the foreign account balance per year not reported; do not let this slip past midnight."),
            window_s=220.0, keywords=("fbar", "foreign"),
        ),
        _gt(
            Event(id="tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow", kind="phone_message", sim_time=560.0,
                  content="Voicemail from your tenant-defense attorney's paralegal at Henderson and Park: the emergency eviction-stay motion paperwork is ready for your in-person signature at the downtown office before five p.m. closing today; the show-cause hearing the landlord requested is calendared for tomorrow morning at nine in housing court and the motion has to be on the clerk's desk by start-of-business or the writ-of-restitution issues by default. Bring photo identification and the maintenance-escrow receipts from the past three months. Office is on the ninth floor of the Smith Tower at Second and Yesler; the attorney expects to be available between three and four-thirty if you want to walk through the strategy before signing."),
            window_s=240.0, keywords=("attorney", "eviction"),
        ),
        _gt(
            Event(id="kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m", kind="alert", sim_time=380.0,
                  content="PagerDuty P1 incident on order-fulfillment Kafka cluster prod-orders-kafka-01: the broker fleet has been reporting unstable partition-leadership elections across the cluster for the last fifteen minutes with two-hundred under-replicated partitions and consumer-lag climbing past eight million messages on the checkout-event topic. The on-call runbook escalates to engineering leadership at the seventy-five-minute mark if the broker quorum is not stabilized; storage-tier dashboards show I/O wait spikes correlated with the disk-controller firmware push from Monday evening. You are the primary on-call this week; the secondary has just paged you and expects a phone-handshake on the bridge within two minutes per the SEV1 protocol."),
            window_s=200.0, keywords=("kafka", "broker"),
        ),
    ]
    distractors = [
        Event(id="wednesday_midweek_checkpoint_briefing_no_priority_flagged_calendar_clear", kind="notification", sim_time=30.0,
              content="Wednesday midweek-checkpoint briefing: you have four meetings remaining this week, two heads-down focus blocks Thursday and Friday morning, and inbox is at eighteen unread with all eighteen messages categorized routine by the triage classifier. Calendar is clear for the rest of today and tomorrow morning. The sprint board, stakeholder-ask queue, and personal-task list all show no urgent items pending, and no overdue tasks were detected anywhere in the workflows you supervise. Have a productive second half of the week."),
        Event(id="github_actions_weekly_workflow_health_digest_all_green_zero_flaky_rerun", kind="email", sim_time=80.0,
              content="GitHub Actions weekly workflow-health digest for the order-fulfillment-platform organization: twelve workflows across nine repositories ran cleanly with zero flaky-rerun rate over the past seven days. Cron-triggered jobs completed within their scheduled windows; pull-request validation workflows averaged four minutes to green; deployment workflows reported no manual approvals pending. Self-hosted runner fleet utilization peaked at sixty-three percent on Wednesday afternoon and remained idle overnight on the weekend. The next workflow-health digest sends next Monday at the same time."),
        Event(id="postman_workspace_collection_runner_v11_javascript_runtime_announcement_no_action", kind="email", sim_time=140.0,
              content="Postman product team announcement: the Collection Runner has been upgraded to version eleven with a refreshed UI, a new JavaScript runtime for pre-request and test scripts, and inline diff-views for collection-version comparison. Existing collections continue to run on the legacy runtime through end-of-year and no migration action is required at this time. See the changelog for the full list of behavioral changes and opt-in toggles for the new diff-view; workspace administrators will be notified separately if any workspace-level settings require attention."),
        Event(id="goldleaf_stationery_quarterly_catalog_handmade_paper_fountain_pen_spring_no_action", kind="email", sim_time=300.0,
              content="Goldleaf Stationery quarterly catalog for the spring season is now live online: handmade-paper journals in five new cover-stock options, the fountain-pen ink-of-the-month subscription with three featured shimmer colors this quarter, and limited-run leather portfolio cases priced for early-spring promotion. Browse at your leisure; orders placed before the end of the month qualify for complimentary monogramming on most leather items. If our catalog cadence has become too noisy, the mailing frequency can be dropped to twice-yearly or fully paused through the footer link below."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v27",
        events=events,
        ground_truth=gts,
        briefing=(
            "Wednesday midday at home in Seattle. "
            "Mid-stage USCIS naturalization applicant with the field-office interview just rescheduled by the adjudications officer; primary on-call engineering rotation this week for the order-fulfillment Kafka cluster and the broker fleet has been showing leadership-instability flickers since the storage-tier firmware push on Monday. "
            "Federal tax preparer flagged a deferred FBAR filing for residual foreign-bank accounts left over from a postdoc year in Berlin and a sabbatical in Lisbon; the extended October fifteenth deadline lapses at midnight Pacific tonight. "
            "Landlord filed an eviction notice last week over a disputed maintenance-escrow balance and the tenant-defense attorney is drafting an emergency stay motion against tomorrow's show-cause hearing. "
            "Family history of premature coronary disease on my father's side; cardiologist ordered a stress test last month but I never followed up for the results. "
            "Notifications are filtered for urgent: cardiac-emergency symptoms, P1 production on-call alerts, hard-deadline legal-pickup or federal-filing windows, and the USCIS rescheduled-interview confirmation should break through; routine engineering digests, marketing catalogs, product feature announcements, and the midweek briefing can wait."
        ),
        intents=(
            "call nine-one-one and chew aspirin per dispatcher instructions if I get cardiac MI red flags (chest pressure with arm radiation, cold sweat)",
            "acknowledge any P1 on-call alert from the order-fulfillment Kafka broker fleet within two minutes of the page",
            "file the FBAR FinCEN-114 before eleven fifty-nine Pacific tonight; partial filings are not accepted and the willful-violation penalty is per-account-per-year",
            "pick up the tenant-attorney eviction-stay motion paperwork in person by five today so tomorrow's show-cause hearing is on the schedule",
            "confirm the rescheduled USCIS naturalization interview slot before tomorrow noon and let routine engineering digests, marketing catalogs, product feature announcements, and the midweek briefing wait until evening",
        ),
    )


def test_trace_v28() -> Trace:
    gts = [
        _gt(
            Event(id="noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel", kind="alert", sim_time=640.0,
                  content="National Weather Service has upgraded the overnight freezing-rain advisory to a full ice-storm warning for the metro area through tomorrow afternoon. The latest convective-model run shows an extended overrunning event laying down between one-quarter and three-quarter inch of glaze on every untreated surface across the urban core and the foothill towns between two and seven in the morning. Utility planners are staging for a thirty-six-hour outage projection on the suburban distribution feeders once the glaze depth crosses the half-inch threshold; tree-limb-on-powerline incidents climb steeply above that mark. A no-unnecessary-travel advisory is now in effect statewide; emergency-room visits from falls on glazed sidewalks during the last comparable ice storm tripled within four hours of the first accretion. Charge phones, set indoor heat now, and stage candles and battery-lanterns inside the house tonight."),
            window_s=90.0, keywords=("ice", "glaze"),
        ),
        _gt(
            Event(id="mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay", kind="email", sim_time=210.0,
                  content="Mortgage-underwriting team email: the closing on the Westwood Avenue property originally on today's three-p.m. calendar has been rescheduled to Friday morning at ten a.m. at the title-company office downtown. Final underwriting conditions came in late from the appraisal-review desk last night and required an additional twenty-four-hour funding clearance through the warehouse line. Reply to confirm the Friday slot before noon today or the lender will release the rate-lock back into the pool with a two-business-day grace before re-pricing against current rate-sheet quotes. Bring the certified-funds cashier's check at the revised closing-cost-disclosure amount circulated this morning by the loan officer, the homeowners-policy declaration page from your insurance agent, plus a government-issued photo identification. The seller's attorney has been notified through the title-company portal and confirmed the slot is open on their calendar."),
            window_s=200.0, keywords=("mortgage", "closing"),
        ),
        _gt(
            Event(id="elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min", kind="alert", sim_time=470.0,
                  content="PagerDuty severity-one incident on the customer-facing search-platform Elasticsearch cluster prod-search-es-east-01 fired at fifteen-thirty-five UTC: index status flipped to RED with two primary shards on the catalog-search index marked unassigned and zero automatic shard-recovery progress logged in the last six minutes. Storefront search API five-xx error rate has climbed past forty percent; downstream recommendation and personalization services are degrading to cold-cache fallback paths. Engineering leadership receives a parallel page at the fifty-minute mark per the SEV-one playbook and the customer-experience PMO is notified separately if storefront-search latency SLO is breached for longer than ten consecutive minutes. You hold the secondary on-call pager this rotation; the primary just opened the war-room bridge link and asked for a phone-handshake confirmation within ninety seconds. The shard-allocation explain output is pointing at a disk-high-watermark trigger on three hot-tier nodes — quorum re-balancing may require manual cluster.reroute steps once the watermark threshold clears."),
            window_s=220.0, keywords=("elasticsearch", "shard"),
        ),
        _gt(
            Event(id="older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback", kind="phone_message", sim_time=540.0,
                  content="Voicemail from your older sister Tess, who is the named executor of your late father's estate: the certified appraiser engaged through the probate court for the safe-deposit-box contents at the downtown First National branch is only able to do the inventory tomorrow at nine in the morning before he leaves town for the holiday weekend. Both surviving siblings need to be present per the probate court order — the box holds the original signed will, the wedding-band collection, and the two gold coins the estate's interim valuation has not been able to confirm without in-person inspection by a certified appraiser. Tess asked for a callback before this evening if you can be at the branch by nine; otherwise she will reschedule the appraiser into next week and the estate-distribution timeline pushes a full month due to probate-court calendar congestion. Bring a photo identification that matches the named-beneficiary list on file and a black ballpoint pen for the chain-of-custody log."),
            window_s=240.0, keywords=("executor", "appraiser"),
        ),
        _gt(
            Event(id="heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email", kind="email", sim_time=370.0,
                  content="Notice from your home-equity-line-of-credit lender: the HELOC draw period on the 2014-originated line expires at five p.m. Friday and the line will automatically convert to a fifteen-year amortization schedule at the variable prime-plus-one-point-five rate currently quoted. Election of the alternative two-step product — a fifteen-year fixed-rate term lock at six-point-eight-five percent on the current outstanding balance with no further draws permitted — must be submitted through the secure-message portal before the same five-p.m. deadline. The unused portion of the original draw cap reverts to the bank at conversion and cannot be reinstated without a fresh application and an updated home appraisal. Outstanding balance at the time of conversion becomes the basis for the new amortization-payment recalculation; current balance is on the bank-attached account statement; signed acceptance of either path must be returned through the portal before the deadline or the default amortization terms apply automatically."),
            window_s=240.0, keywords=("heloc", "draw"),
        ),
    ]
    distractors = [
        Event(id="terraform_state_drift_weekly_scan_zero_resources_modified_clean_all_workspaces", kind="notification", sim_time=30.0,
              content="Terraform Cloud weekly state-drift scan summary for the platform-infrastructure organization: fourteen workspaces scanned across the dev, staging, and prod environments. Zero resources reported as drifted in any workspace this week; provider plans returned plans-no-changes on every successful run. The drift-detection cron is scheduled to fire again at the start of next week and no operator action is required from this report. Average plan time held at two minutes ten seconds across the prod workspaces and four minutes flat across the staging workspaces."),
        Event(id="bluesky_starter_pack_invite_curator_recommended_follow_data_journalism_circle", kind="notification", sim_time=75.0,
              content="A college friend named Anna shared a Bluesky starter-pack she curated for the data-journalism circle — twelve recommended-follow accounts including two former colleagues from your data-team days. Joining the starter-pack auto-follows the bundled accounts in one tap; the bundle can be un-followed individually later or skipped as a whole. There is no time pressure attached to this invite; Bluesky surfaces these as evergreen recommendations and the share-link does not expire on any fixed deadline."),
        Event(id="meridian_games_summer_catalog_strategy_titles_2026_no_action_required", kind="email", sim_time=140.0,
              content="The Meridian Games summer-season catalog has just been published online: three new strategy titles in the eighteen-and-up release window, two reprint runs of the deeper Eurogame backlog that sold through last winter, and a second-edition rules update for the long-out-of-print heritage co-op title that fans have been asking after for several years. Browse the lineup at your own pace; pre-orders placed during catalog week qualify for a discounted shipping rate on the full Eurogame line. The summer catalog is the second of three planned for this calendar year — the fall and holiday catalogs follow on the established Meridian publishing cadence. Replies and product questions can be directed to the catalog-mailbox alias maintained by the customer-support team."),
        Event(id="thursday_pre_weekend_wrap_briefing_no_overdue_items_focus_blocks_clear_tomorrow_light", kind="notification", sim_time=600.0,
              content="Thursday pre-weekend wrap briefing: three remaining meetings tomorrow all carry an opt-in flag from the team — none are mandatory and each has a written summary pre-circulated in the team channel. Your engineering one-to-one and the architecture-review walkthrough have been auto-pre-read into the inbox. The two heads-down focus blocks on Friday afternoon are unblocked and the sprint board reflects only items that auto-advance over the weekend without any human intervention. Nothing on the personal-task list or the stakeholder backlog requires a response before next Monday's standup. Plan for a low-touch end-of-week — earned, well."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v28",
        events=events,
        ground_truth=gts,
        briefing=(
            "Late Thursday afternoon at home; rolling end-of-week with the mortgage closing schedule and the estate-administration timeline both moving at once. "
            "Mid-stage homebuyer with the underwriter's late conditions just pushing the closing into Friday morning; the home-equity-line of credit on the current property hits its scheduled draw-period expiry the same Friday afternoon. "
            "Father passed last spring and the older sister is acting as named executor; the certified appraiser for the safe-deposit-box inventory is tomorrow morning and both surviving siblings need to be present per the probate court order. "
            "Holding the secondary on-call rotation for the customer-facing storefront search platform this week; the Elasticsearch cluster has been showing index-status hiccups since the disk-tier capacity push last Friday. "
            "Local forecast just upgraded the overnight freezing-rain advisory to a full ice-storm warning that runs through tomorrow afternoon. "
            "Notifications are filtered for urgent: ice-storm warning impact on tomorrow's mortgage-closing-and-sibling-appraiser commute, severity-one production on-call pages on the search platform, hard-deadline financial elections on the HELOC draw-period conversion, lender confirmation on the rescheduled closing slot, and the estate-executor callback to the older sister; routine state-drift scans, social-platform starter-pack invites, board-game catalog releases, and Thursday wrap-up briefings can wait."
        ),
        intents=(
            "answer the storefront-search SEV-one bridge within ninety seconds of the next page from the Elasticsearch primary on-call",
            "confirm the rescheduled mortgage-closing slot with the underwriter team before noon today or lose the rate-lock to the re-pricing pool",
            "return the older sister's voicemail before tonight so the estate-executor appraiser can keep the nine-a.m. safe-deposit-box inventory tomorrow",
            "submit the HELOC draw-period election (default amortization or fixed-rate term-lock conversion) through the lender's secure-message portal before five p.m. Friday",
            "shelter in place tomorrow as the ice-storm glaze accretion crosses the half-inch threshold per the NWS warning; otherwise the routine terraform-state-drift digest, the Bluesky starter-pack invite, the Meridian Games summer catalog, and the Thursday pre-weekend wrap briefing can all wait",
        ),
    )


def test_trace_v29() -> Trace:
    gts = [
        _gt(
            Event(id="nike_snkrs_zoom_kobe_5_protro_mamba_day_verified_buyer_sneaker_raffle_40min_180pair", kind="notification", sim_time=420.0,
                  content="SNKRS app push for verified-buyer accounts only: the Mamba-Day commemorative Zoom Kobe 5 Protro sneaker raffle has just opened a forty-minute entry window and closes at eleven-fifty Pacific sharp. Total release across every available size is one hundred eighty pairs; the deepest inventory sits at sizes ten through eleven, while sizes eight and thirteen each hold four pairs and are expected to clear well before the timer expires. Size selection locks at raffle entry — no swap once the window closes — and confirmed winners receive a ninety-second push-and-email handshake with a ten-minute payment-confirm grace before the slot rolls to the runner-up queue. Any surface-released inventory after the final notify wave auto-routes to the trade-resale list and is not offered back to the verified-buyer raffle queue."),
            window_s=240.0, keywords=("sneaker", "raffle"),
        ),
        _gt(
            Event(id="partner_stroke_fast_protocol_facial_droop_speech_slur_911_dispatcher_tpa_3hr_window_speaker", kind="alert", sim_time=640.0,
                  content="Your partner just slumped forward at the kitchen table — right-side facial droop, right arm hanging limp at her side, slurred speech when you asked her to repeat a short sentence — textbook fast-protocol stroke presentation, with symptom onset inside the last ninety seconds. You have her seated upright with her head supported and have dialed nine-one-one; the dispatcher is on speaker and confirmed paramedics are six minutes out. The dispatcher asked you to write down the exact symptom-onset timestamp because tPA — the tissue-plasminogen-activator clot-busting agent — has a three-hour eligibility window from onset for ischemic-stroke patients at the regional comprehensive stroke center. She is conscious and tracking your eyes. Do not give aspirin or any anticoagulant until paramedics on arrival image-confirm ischemic versus hemorrhagic; her documented prior TIA and family history of early-onset stroke are in the home medical binder on the counter."),
            window_s=90.0, keywords=("stroke", "tpa"),
        ),
        _gt(
            Event(id="orthopedist_knee_mri_consult_moved_up_730am_tomorrow_specialist_sabbatical_pre_op_meniscectomy", kind="email", sim_time=320.0,
                  content="Email from the orthopedist's scheduling office at the Sutter Sports-Medicine clinic: Dr. Reyes had a same-day cancellation on tomorrow morning's seven-thirty slot and the clinic is offering you that opening to discuss the recent knee-MRI imaging and walk through the pre-op decision on the partial-meniscectomy arm versus the conservative-care arm. The original consult was on the books for next Tuesday afternoon; the seven-thirty opening is the only consult opportunity before Dr. Reyes leaves for a two-week medical-education sabbatical and the next available consult after the sabbatical is the third week of next month. Confirm by five-p.m. today through the patient-portal scheduling tab or the slot releases to the surgical-coordinator backup queue with no further reminders sent. The knee-MRI radiology report and the annotated image series have been auto-attached to the patient-portal medical-record entry so you can pre-read them tonight."),
            window_s=220.0, keywords=("orthopedist", "mri"),
        ),
        _gt(
            Event(id="roth_ira_conversion_election_5pm_deadline_year_end_recharacterization_no_longer_permitted_tcja", kind="email", sim_time=210.0,
                  content="Year-end notice from your IRA custodian: today is the December-thirty-first calendar deadline for any Roth-conversion election to be applied to the current tax-year, and the secure-message portal cuts conversion-submission acceptance at five p.m. Pacific. Recharacterization-back-to-Traditional is no longer permitted under the 2017 federal tax-code revision once a Roth conversion is filed, so the election is functionally one-way once the five-p.m. timestamp lands; the corresponding tax liability flows onto the next-April-fifteen filing without any unwind option. A pro-forma worksheet from the custodian's tax-projection module is attached with the converted-balance tax-bracket impact and a safe-harbor estimated-quarterly adjustment for the current tax-year. The custodian-side conversion desk also suggests submitting before three p.m. to leave room for two resubmission attempts in case the portal returns a settlement-validation error on first pass; the conversion-submission queue runs noticeably slower on the year-end timestamp surge."),
            window_s=240.0, keywords=("roth", "conversion"),
        ),
        _gt(
            Event(id="vault_pki_secrets_engine_lease_renewal_cascade_failure_storefront_auth_outage_p1_75min_dns_zone_drift", kind="alert", sim_time=510.0,
                  content="PagerDuty SEV-one incident on the platform-security HashiCorp Vault cluster vault-prod-us-east-1a at sixteen-twelve UTC: the PKI secrets-engine lease-renewal pipeline has dropped into a cascade-failure pattern across the regional service mesh — three thousand four hundred consumer-pod leases failed renewal in the last six minutes, and authentication-handshake fallback to the staging-tier replica is throwing certificate-trust errors because the primary intermediate CA's issuing-chain is partially expired in the failover zone. Storefront-API service-account authentication has climbed to twenty-six-percent failure rate and is still trending up; downstream order-processing and inventory-sync are queueing against the auth-fallback retry backoff. The seventy-five-minute runbook escalation auto-pages the security-platform incident commander if lease-renewal recovery has not stabilized inside the first thirty minutes. You hold the primary on-call this rotation; the secondary just opened the war-room bridge and the security-platform PM is monitoring on the storefront PagerDuty channel. Preliminary diagnosis points at a DNS-zone caching mismatch between the primary and standby clusters following last night's authoritative record-set update."),
            window_s=220.0, keywords=("vault", "lease"),
        ),
    ]
    distractors = [
        Event(id="aws_config_compliance_daily_evaluation_digest_zero_drift_all_accounts_no_action_required", kind="notification", sim_time=30.0,
              content="Daily AWS Config compliance-evaluation digest for the platform-org payer account: every managed rule across all forty-two member accounts evaluated COMPLIANT on the overnight run with zero drift events and zero remediation actions queued by the AWS Config rules engine. The s3-bucket-encryption rule cleared on every bucket; the iam-password-policy rule cleared on every member; the encrypted-volumes rule cleared on every EBS volume. The next compliance-evaluation cycle is on the calendar for the same overnight window and the report will land in this inbox at the same morning timestamp."),
        Event(id="substack_notes_weekly_follow_recommendation_digest_writers_education_circle_no_time_pressure", kind="notification", sim_time=70.0,
              content="Substack Notes sends you a weekly follow-recommendation bundle from a Notes-stack curator you already follow: nine writers in the education-and-policy circle, including two former colleagues from your earlier classroom-research years and one writer whose newsletter you have read on-and-off without subscribing. The follow-recommendation list can be browsed individually; nothing auto-follows and the bundle does not expire on any fixed deadline. Substack pushes the follow-recommendation digest every Sunday and the notification stream can be muted under the reader preferences if the digest cadence feels too noisy."),
        Event(id="outdoor_voices_summer_apparel_quarterly_catalog_email_no_action_required_browse_at_pace", kind="email", sim_time=130.0,
              content="The Outdoor Voices summer-season apparel catalog dropped on the brand site overnight: a refreshed everyday-running silhouette returns in three new colorways, the lightweight technical-shorts revival the community has been asking after since last fall is finally on the page, and the brand's heritage-pastel matching set is back in a second-edition cut. Pace the browsing however your week settles — the launch-window expedited-shipping perk runs across the full summer line for any order placed while the catalog sits in promotional rotation, with no fixed countdown timer attached. Two further seasonal catalogs are queued for later in the year under the brand's standard release rhythm, spanning the early-fall and the holiday-gifting horizon. Sizing questions, exchange requests, and customer-service follow-ups route through the help-center contact form linked from the brand site footer."),
        Event(id="linear_app_cycles_2026_planning_view_launch_announcement_quarterly_release_notes_no_action", kind="email", sim_time=580.0,
              content="Linear product-update email: the Cycles 2026 planning view is now available on every workspace and gives team leads a single-pane view of in-flight cycle progress, projected cycle-completion velocity, and carryover-issue density across the upcoming three cycles. The planning view is opt-in at the workspace level and can be toggled on under the workspace-settings cycle preferences; no migration step is needed and existing cycle data is preserved bytewise. The accompanying quarterly release notes cover four other smaller updates landing on the same release train, including the project-roadmap-export refresh and the issue-template-library expansion. The launch retrospective writeup is published on the Linear engineering blog under the Cycles 2026 launch-week tag."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v29",
        events=events,
        ground_truth=gts,
        briefing=(
            "Wednesday morning at home in Oakland; rolling year-end retirement-account close and a knee-injury arc with the orthopedist after last month's MRI imaging. "
            "Currently holding the primary on-call rotation for the storefront-platform security infrastructure; the Vault PKI cluster has been showing lease-renewal latency drift since last night's authoritative DNS-zone update. "
            "Partner has a documented prior TIA and a family history of early-onset stroke on her father's side; the home medical binder with her anticoagulant-protocol notes is on the kitchen counter. "
            "Signed up for the SNKRS verified-buyer raffle list last week ahead of the Mamba-Day commemorative drop. "
            "Notifications are filtered for urgent: any fast-protocol stroke symptoms in my partner, severity-one Vault PKI on-call pages, hard-deadline financial elections on the year-end Roth conversion, same-day specialist consults from the orthopedist, and the SNKRS sneaker-raffle entry window inside its forty-minute timer; routine AWS-Config compliance digests, Outdoor Voices catalog releases, Linear product-launch announcements, and Substack Notes follow-recommendation digests can wait."
        ),
        intents=(
            "respond instantly to any fast-protocol stroke symptoms in my partner — the tPA three-hour ischemic-stroke window is the critical clock and the dispatcher is already on speaker",
            "answer the Vault PKI SEV-one bridge well inside the first thirty minutes before the seventy-five-minute runbook auto-pages the security-platform incident commander",
            "confirm the seven-thirty orthopedist consult tomorrow before five p.m. today through the patient portal or the slot releases to the surgical-coordinator backup queue",
            "submit the Roth IRA conversion election through the custodian's secure-message portal before five p.m. Pacific today; recharacterization-back-to-Traditional is no longer a permitted unwind path",
            "enter the SNKRS verified-buyer sneaker raffle inside the forty-minute entry window before surface-released inventory auto-routes to the trade-resale list; otherwise the daily AWS Config digest, the Outdoor Voices summer catalog, the Linear Cycles 2026 announcement, and the Substack Notes follow-recommendation digest can all wait",
        ),
    )


def test_trace_v30() -> Trace:
    gts = [
        _gt(
            Event(id="brother_phd_defense_doctoral_graduation_tomorrow_930am_committee_reception_family_toast_obligation", kind="email", sim_time=220.0,
                  content="Email from your younger brother Marcus: his PhD defense at the Stanford Linguistics department is on the calendar for tomorrow morning at nine-thirty in the Margaret Jacks Hall seminar room, with advisor Dr. Petra Vasquez and the three-member dissertation committee presiding. The post-defense reception with the committee and the immediate family is set to follow at the department-lounge from eleven-thirty through the early afternoon, and the family has unanimously asked you, as the eldest sibling, to deliver the first toast as the designated family speaker. The PhD defense is the once-in-life closing chapter on six years of doctoral work and the only ceremony you and the parents can collectively attend; there is no make-up event in any future quarter and the department does not host a separate hooding ceremony for cross-program reasons. Marcus is asking for confirmation by end-of-day today so he can finalize the lounge-catering headcount and let the committee know which family members are attending. The toast runs three to four minutes in the family's expectations; Marcus would just like a heads-up tonight if you want him to forward any committee-context bio details that might help shape what you say about the dissertation arc."),
            window_s=240.0, keywords=("phd", "toast"),
        ),
        _gt(
            Event(id="adoption_agency_caseworker_placement_finalization_meeting_tomorrow_9am_both_parents_required_paperwork_signing", kind="notification", sim_time=340.0,
                  content="Voicemail from Renee, your caseworker at the Bay Area Family Connections adoption agency: the placement-finalization meeting with the birth-mother and the agency-attorney has been scheduled for tomorrow morning at nine in the agency's downtown office, and both prospective adoptive parents are required to be present in person for the final paperwork signing and the birth-mother consent verification. The court-filing window for the placement order closes at the end of next week per the county family-court calendar, and rescheduling the meeting moves the placement into the next monthly court-filing cycle which adds a minimum of four additional weeks before the home-bringing date is set. Renee asked you to call back tonight to confirm both parents will attend; her direct caseworker line stays open until nine p.m. tonight and the on-call agency rotation covers any after-hours messages on the same number."),
            window_s=220.0, keywords=("adoption", "placement"),
        ),
        _gt(
            Event(id="brokerage_tax_loss_harvest_year_end_settle_t1_4pm_wash_sale_30day_lot_sale_deadline", kind="email", sim_time=430.0,
                  content="Year-end tax-loss-harvest reminder from your Schwab portfolio advisor: today is the calendar deadline for any sale to settle within the current tax year under the T-plus-one settlement convention, which means the brokerage cuts harvest-eligible sell orders at four p.m. Eastern today regardless of after-hours queue depth. The current-year unrealized losses on the international-equity sleeve sit at roughly twenty-three thousand dollars across three specific tax-lot identifications eligible for a partial harvest; harvesting those losses against the year's realized short-term gains brings the net short-term capital-gains line down to roughly the three-thousand-dollar ordinary-income offset cap with the residual carrying forward to next year. The 30-day wash-sale clock applies to any substantially-identical replacement purchase, so the post-harvest re-entry plan needs either a non-substantially-identical proxy fund inside the wash-sale exclusion or a thirty-day wait before repurchase. The Schwab tax-advisor desk is staffed through six p.m. today if you want the harvest order routed through the advised-side rather than the self-directed portal; otherwise the self-directed trade-confirmation interface accepts specific-lot identification at order-placement time."),
            window_s=240.0, keywords=("harvest", "wash"),
        ),
        _gt(
            Event(id="nws_excessive_heat_warning_heat_dome_index_112f_3day_persistence_grid_load_shed_outdoor_risk", kind="alert", sim_time=520.0,
                  content="NWS upgraded the prior heat-advisory to a full excessive-heat warning for the metro Sacramento valley through Sunday evening with a heat-dome ridge anchoring overhead and forecast heat-index readings hitting one-hundred-twelve Fahrenheit in the afternoon shade peaks across all three days. The CAISO grid-operator issued a parallel Flex Alert for the same window calling for voluntary conservation between four p.m. and nine p.m. each evening, and a rotating-load-shed event response is on standby if demand outpaces the available interchange-import margin. Elderly relatives in the cooling-vulnerable category and pets in non-air-conditioned spaces face the highest risk per the NWS HeatRisk tier-four guidance; outdoor-work and youth-sports practices should follow the hourly hydration cadence in the city heat-action playbook. The local cooling-center map at the city emergency-services portal lists nine air-conditioned public sites with extended evening hours for the duration of the warning."),
            window_s=220.0, keywords=("heat", "index"),
        ),
        _gt(
            Event(id="spouse_asthma_severe_exacerbation_rescue_inhaler_failing_peak_flow_below_50pct_status_asthmaticus_911_call", kind="alert", sim_time=650.0,
                  content="Your spouse just used her albuterol rescue inhaler for the fourth time in twenty minutes and is still in audible respiratory distress at the kitchen sink — pursed-lip breathing, tripod posture, accessory-muscle retraction visible at the neck — with a peak-flow meter reading dropping from her normal three-eighty into the one-eighty range, well under the fifty-percent red-zone threshold on her written asthma-action plan. She has a prior status-asthmaticus admission from three winters ago that required intubation in the emergency department, and her pulmonologist's written instructions on the refrigerator door direct you to call nine-one-one rather than self-transport once the peak-flow reading crosses into the red zone with rescue-inhaler failure. The 911 dispatcher is on the line confirming paramedic transport eight minutes out and asking you to keep her seated upright on the floor against the cabinet wall, no oral medication or fluid administration, and to bring her current pulmonology medication list and the most recent spirometry printout from the home medical-binder when paramedics arrive."),
            window_s=90.0, keywords=("asthma", "rescue"),
        ),
    ]
    distractors = [
        Event(id="aws_cloudtrail_weekly_log_delivery_health_report_zero_dropped_events_no_action_required", kind="notification", sim_time=35.0,
              content="Weekly AWS CloudTrail log-delivery health report for the platform-org trail aggregation: across the rolling seven-day window, every multi-region trail delivered to the central audit-bucket without a single dropped event, the S3-delivery-failure metric stayed flat at zero, and the cross-account CloudWatch metric-filter delivery latency held inside the sub-minute SLO percentile band. The report includes the per-account event-count histogram and the management-event versus data-event breakdown for the platform-org member accounts as informational appendices. Audit-engineering owns the weekly cadence on this report; the CloudTrail-platform team rotates each Saturday's snapshot into the shared mailbox the audit-team compliance-evidence runbook reads from first thing Monday."),
        Event(id="artisan_origins_coffee_quarterly_seasonal_roast_subscription_newsletter_summer_releases_no_action", kind="email", sim_time=80.0,
              content="The Artisan Origins coffee roastery has dropped its summer seasonal-roast line for subscribers on the brand site: a Yirgacheffe natural-process single-origin returns under a refreshed lighter-roast curve, two Central-American washed-process blends rotate in for the warm-weather espresso menu, and a small-lot decaffeinated Brazilian arrives as a sample-size add-on for the home-tasting members. The subscription cadence stays on the same quarterly rhythm and any flavor-profile swap, grind-size change, or roast-darkness preference can be adjusted through the subscriber-account brewing-preferences panel any time before the next quarter's pre-ship cutoff. Coffee preference adjustments, shipping address changes, and tasting-note feedback all run through the subscriber-account messaging thread that the roastery customer-care team works through first thing in the Pacific morning."),
        Event(id="saturday_weekend_prep_briefing_no_overdue_items_calendar_open_for_household_errands", kind="notification", sim_time=140.0,
              content="Saturday morning weekend-prep briefing: the calendar through Sunday evening shows no scheduled meetings, no holds, and no time-sensitive obligations from any of the household project lists. The weekly retrospective ran clean — the personal task tracker rolled over with no overdue rows, the home-improvement punch list cleared yesterday afternoon, and the household project-board sits empty of any timing-dependent items through the weekend horizon. The weekend itself is fully open for household errands, the patio garden re-pot session you've been planning, and the optional Sunday-afternoon walk-and-coffee with the friend group, none of which carry hard timing dependencies. The next personal-calendar pulse reopens with the Monday-kickoff cadence after the weekend horizon clears."),
        Event(id="figma_auto_layout_v3_launch_announcement_quarterly_product_update_no_action_required", kind="email", sim_time=595.0,
              content="Figma product-update email: auto-layout version-three is now rolled out on every team workspace, bringing the long-requested grid-direction toggle, the per-row-and-per-column spacing override, and the nested-stack reflow improvements design teams have been asking for since the auto-layout-v2 release. The new behaviors are opt-in at the file-template level and any existing auto-layout-v2 file continues to render with the legacy spacing engine unchanged; migration to the v3 grid model is a per-component decision and the legacy renderer is not on any sunset path. Each of the four smaller landings on the same release train — the variables-import refresh, the dev-mode-comments threading update, the prototype-flow connector polish, and the file-history search refinement — has its own walkthrough on the Figma engineering blog, linked under the auto-layout-v3 changelog entry at the bottom of this announcement."),
    ]
    events = sorted([g.event for g in gts] + distractors, key=lambda e: e.sim_time)
    return Trace(
        name="test_v30",
        events=events,
        ground_truth=gts,
        briefing=(
            "Saturday morning at home in the Sacramento area; spouse has had a multi-day uptick in asthma symptom-frequency this week and her peak-flow meter has been trending down despite the daily-controller and rescue-inhaler regimen. "
            "Younger brother Marcus is defending his Linguistics PhD at Stanford tomorrow morning and the family has asked the eldest sibling to deliver the first toast at the post-defense department-lounge reception. "
            "In the middle of a year-end financial close — Schwab has the international-equity tax-loss-harvest window cutting at four p.m. Eastern today under T-plus-one settlement — and the adoption-agency placement-finalization meeting with the birth-mother is on the verge of being scheduled tomorrow with the agency-attorney. "
            "NWS has been escalating a heat-dome ridge over the metro valley through the weekend and the CAISO grid-operator is signaling Flex-Alert conservation windows in the late-afternoon peak. "
            "Notifications are filtered for urgent: any acute respiratory decompensation in my spouse with rescue-inhaler failure or peak-flow into the red zone, the PhD-defense ceremony-confirmation request from my brother, the year-end tax-loss-harvest brokerage cutoff, the adoption-agency placement-finalization callback, and the NWS excessive-heat warning that maps onto elderly-relative and outdoor-work risk; routine AWS CloudTrail delivery digests, Artisan Origins coffee seasonal-roast emails, the Saturday weekend-prep briefing, and the Figma auto-layout product-update announcement can wait."
        ),
        intents=(
            "respond instantly to any acute respiratory decompensation in my spouse — rescue-inhaler failure plus peak-flow under fifty percent is the status-asthmaticus threshold and her prior intubation history means 911 over self-transport per the pulmonologist's written plan",
            "confirm brother Marcus's PhD-defense reception attendance and family-speaker toast role by end-of-day tonight so he can finalize the department-lounge catering headcount before the once-in-life ceremony tomorrow morning",
            "place the year-end tax-loss-harvest sell orders through the brokerage portal before the four-p.m. Eastern T-plus-one settlement cut, choosing specific-lot identification for the three international-equity lots inside the wash-sale exclusion plan",
            "call the adoption agency back tonight before nine p.m. to confirm both prospective parents attend the placement-finalization meeting tomorrow nine a.m., since rescheduling pushes the court-filing into the next monthly cycle and adds four weeks to the home-bringing date",
            "track the NWS excessive-heat warning through the weekend and the CAISO Flex-Alert windows; otherwise the weekly AWS CloudTrail delivery digest, the Artisan Origins seasonal-roast email, the Saturday weekend-prep briefing, and the Figma auto-layout-v3 product-update announcement can all wait",
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
        "test_v6": test_trace_v6,
        "test_v7": test_trace_v7,
        "test_v8": test_trace_v8,
        "test_v11": test_trace_v11,
        "test_v12": test_trace_v12,
        "test_v13": test_trace_v13,
        "test_v14": test_trace_v14,
        "test_v15": test_trace_v15,
        "test_v21": test_trace_v21,
        "test_v22": test_trace_v22,
        "test_v23": test_trace_v23,
        "test_v24": test_trace_v24,
        "test_v25": test_trace_v25,
        "test_v26": test_trace_v26,
        "test_v27": test_trace_v27,
        "test_v28": test_trace_v28,
        "test_v29": test_trace_v29,
        "test_v30": test_trace_v30,
    }
    if name not in traces:
        raise ValueError(f"Unknown trace {name!r}; options: {sorted(traces)}")
    return traces[name]()
