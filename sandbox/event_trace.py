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
    }
    if name not in traces:
        raise ValueError(f"Unknown trace {name!r}; options: {sorted(traces)}")
    return traces[name]()
