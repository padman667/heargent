# Run 15 — Externally-Authored Held-Out Trace `test_v4` (M8b)

**Date:** 2026-04-22 (pre-registration). Results section appended post-eval.
**Milestone:** M8b — re-run the M8 three-commit external-authoring protocol under a tightened spec that closes the keyword/content substring-alignment gap surfaced by M8. Goal unchanged from M8: close the "design-your-own-eval" review attack by adding one held-out trace authored by a fresh Claude Code session with no access to the agent code, arbiter prompt, surprise scorer, or any run doc. Run once under the M7 frozen config. No retuning regardless of outcome.
**Pre-registration SHA:** this commit (spec + authoring prompt + success bars + decision rules committed together; no trace code and no eval runs before this commit). **Predecessor:** M8 results SHA `9487094`.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, predictor seed=42, deterministic throughout. Local-only; no Claude API.

## Goal

M8 (`test_v3`, runs/14) landed the three-commit protocol cleanly but did not deliver its intended payload. The content arbiter actually surfaced 3 of 5 GTs and rejected all 4 distractors — but the hit-rate scorer (`eval/run_trace.py:21–23`, `_matches_keywords`, AND-substring) could only credit 1 of those hits because 4 of 5 GT `keywords` tuples the fresh Claude authored did not appear as case-insensitive substrings of their own `content` (e.g. `("plumber","reschedule")` vs content `"Voicemail from Jorge at Ridgeline Plumbing: cannot make tomorrow's 09:00 dishwasher install..."` — semantically aligned, substring-misaligned). All 4 existing in-repo traces use keyword/content substring alignment by implicit convention; the M8 prompt failed to state it as a hard constraint.

Per the M8 pre-reg P4 sanity-gate decision rule, the M6a headline was not falsified (poll = 0.20 on the same four unscoreable GTs) and the trace was not discarded. `test_v3` stays in the repo uncorrected as the artifact that surfaced the gap. The external-trace credibility argument the M8 design was meant to provide is still outstanding.

M8b repeats the protocol against a fresh trace `test_v4`, with **one** new hard constraint added to the spec and **one** new line added to the pre-eval verification step. Everything else — the frozen M7 config, the 4 eval cells, the pre-registered bars, and the decision rules — is copied verbatim from M8. This is deliberate: M8b is a protocol repeat, not a new experiment.

## Design reasoning (abbreviated — see runs/14 for the long-form)

Two candidates for "externally-authored": fresh Claude Code session (chosen) vs user hand-authors from spec. The fresh-session protocol's credibility reduces to one auditable question: *is the authoring prompt clean?* The M8b prompt is — like M8's — written to describe a trace *as a dataset*, not *relative to an agent*: no mention of "surprise," "arbiter," "predictor," "z-score," "band," "YES/NO," "gate," "predictable/unpredictable," "easy/hard," "token cost," or "proaction budget." The new keyword-alignment constraint is phrased as a dataset property (matches the scorer's semantics without naming the scorer).

## Pre-registered artifacts (frozen before any generation)

### Frozen trace spec

Hard constraints — any violation auto-rejects the generation.

- `name = "test_v4"`.
- Exactly **5 `GroundTruthEvent`s** and exactly **4 distractor `Event`s** (total 9 events in `events`).
- All `sim_time` values in `[0, 1000]`. `max(gt.event.sim_time + gt.proaction_window_s) ≤ 1000`.
- At least **3 distinct `kind` values** across the 5 GTs, chosen from {`email`, `calendar_update`, `notification`, `alert`, `phone_message`, `world_event`}.
- At least one GT with `proaction_window_s ≤ 30`.
- At least one GT with `proaction_window_s ≥ 300`.
- **NEW — Keyword/content alignment.** For every `GroundTruthEvent gt`, every string `kw` in `gt.keywords` must satisfy `kw.lower() in gt.event.content.lower()`. Check is purely substring-based — if the keyword's characters don't literally appear in the content, it fails.
- Briefing: 2–4 first-person sentences describing the day's setting.
- Intents: tuple of exactly 5 short phrases.
- Distractors are plausible routine / system noise (no abrupt urgency, no action demand).
- GTs are human-interpretable as "warrants proaction" on content alone (no briefing required to judge).

**Banned event ids** (union of ids used in `dev_v1`, `dev_v2`, `test_v1`, `test_v2`, **`test_v3`**):

```
flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel,
fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat,
package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup,
slack_invite, calendar_advert, promo_email, system_status,
fire_kitchen, board_meeting, water_burst, er_call, security_breach,
daily_briefing, status_ok, uptime_ping, newsletter,
passport_expiry, prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule,
spotify_weekly, app_version_note, distant_birthday, photo_likes
```

**Banned content themes** (semantic, not just string match):
fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor callback, production / server outage, rent due, school pickup, quarterly report, board meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert, marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned building electrical / power shutoff, plumber or appliance-install reschedule.

**Banned keyword pairs** (from existing GTs' `keywords` tuples):

```
(flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly),
(dentist, cancelled), (fire, alarm), (package, delivered), (doctor, call),
(production, alert), (rent, due), (school, pick up), (fire, kitchen),
(board, meeting), (water, burst), (hospital, mother), (security, unauthorized),
(passport, expiring), (prescription, refill), (recall, airbag),
(power, shutoff), (plumber, reschedule)
```

### Authoring prompt (verbatim — pasted unmodified into the fresh Claude Code session)

The block below is the exact text the fresh session receives as its first user message. Any edit to this prompt before or during Commit B invalidates the protocol and the trace must be re-generated from scratch.

> You are authoring one Python function that returns a `Trace` object. This is a held-out evaluation trace for a project you have no other context about. Author it single-shot; do not ask clarifying questions, do not iterate, do not explain your choices.
>
> **Schema** (from `sandbox/event_trace.py`):
>
> ```python
> from dataclasses import dataclass
> from sandbox.world import Event
>
> @dataclass(frozen=True)
> class GroundTruthEvent:
>     event: Event
>     proaction_window_s: float
>     keywords: tuple[str, ...]
>
> @dataclass(frozen=True)
> class Trace:
>     name: str
>     events: list[Event]
>     ground_truth: list[GroundTruthEvent]
>     briefing: str | None = None
>     intents: tuple[str, ...] = ()
> ```
>
> `Event` has fields `id: str`, `kind: str`, `sim_time: float`, `content: str`.
>
> **Syntactic template** (one unrelated example for style only — do not reuse its ids, content, or themes):
>
> ```python
> def dev_trace_v1() -> Trace:
>     gts = [
>         _gt(
>             Event(id="flight_delay", kind="email", sim_time=10.0,
>                   content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New departure: 14:30."),
>             window_s=300.0, keywords=("flight", "delay"),
>         ),
>         _gt(
>             Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,
>                   content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),
>             window_s=300.0, keywords=("meeting", "moved"),
>         ),
>         _gt(
>             Event(id="weather_alert", kind="world_event", sim_time=120.0,
>                   content="Weather alert: heavy rain expected tomorrow morning; expect travel delays."),
>             window_s=300.0, keywords=("weather", "rain"),
>         ),
>         _gt(
>             Event(id="deadline", kind="email", sim_time=300.0,
>                   content="Reminder: Quarterly Report deadline is in 24 hours."),
>             window_s=600.0, keywords=("deadline", "quarterly"),
>         ),
>         _gt(
>             Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
>                   content="Your dentist appointment today at 16:00 has been cancelled."),
>             window_s=300.0, keywords=("dentist", "cancelled"),
>         ),
>     ]
>     return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)
> ```
>
> `_gt` is a local helper equivalent to `GroundTruthEvent(event=event, proaction_window_s=window_s, keywords=keywords)`; you may use it or construct `GroundTruthEvent` directly.
>
> **Structural requirements** (hard constraints; violating any auto-rejects):
>
> - `name = "test_v4"`.
> - Exactly 5 `GroundTruthEvent`s and exactly 4 distractor `Event`s (mixed into `events` list, sorted by `sim_time`).
> - All `sim_time` values in `[0, 1000]`; for every GT, `gt.event.sim_time + gt.proaction_window_s ≤ 1000`.
> - At least 3 distinct `kind` values across the 5 GTs. Allowed kinds: `email`, `calendar_update`, `notification`, `alert`, `phone_message`, `world_event`.
> - At least one GT with `proaction_window_s ≤ 30`.
> - At least one GT with `proaction_window_s ≥ 300`.
> - **Keyword/content alignment**: for every `GroundTruthEvent gt`, every string `kw` in `gt.keywords` must satisfy `kw.lower() in gt.event.content.lower()`. Check is purely substring-based — if the keyword's characters don't literally appear in the content, it fails.
> - Briefing: 2–4 first-person sentences describing the day's setting.
> - Intents: tuple of exactly 5 short phrases.
> - Distractors are plausible routine / system noise a reasonable person would NOT want surfaced.
> - GTs are human-interpretable on content alone as warranting proaction.
>
> **Banned event ids** (collision auto-rejects):
> `flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert, promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call, security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry, prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule, spotify_weekly, app_version_note, distant_birthday, photo_likes`.
>
> **Banned content themes** (semantic, not just string match):
> fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor callback, production / server outage, rent due, school pickup, quarterly report, board meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert, marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned building electrical / power shutoff, plumber or appliance-install reschedule.
>
> **Banned keyword pairs** (avoid reusing any pair as a GT's `keywords` tuple):
> `(flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert), (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), (hospital, mother), (security, unauthorized), (passport, expiring), (prescription, refill), (recall, airbag), (power, shutoff), (plumber, reschedule)`.
>
> **Output**: one Python function `def test_trace_v4() -> Trace:` in the style of the template, followed by a single line adding `"test_v4": test_trace_v4` to the `get_trace` registry. Return the code in a single fenced Python block. Do not explain.

### Authoring protocol

1. Open a new Claude Code window, `/clear` to ensure empty history.
2. Paste the prompt block above verbatim as the first user message. No additions, no CLAUDE.md context carried in, no reading of any project file beyond what the prompt contains.
3. Fresh session outputs a single fenced Python block containing `def test_trace_v4() -> Trace:` and the registry line.
4. Audit the output against the 11 hard structural constraints (including the new keyword/content alignment constraint) and 3 banned lists. If any violation is found, **reject the generation, log the violation in this doc's Rejections sub-section below, and open another fresh session.** No prompt edits.
5. If the output passes audit, copy it verbatim into `sandbox/event_trace.py` (end of file) and add the registry line. The only permitted edits are: import ordering, typo fixes that block parsing, and the registry line itself. Any change to event `id`, `kind`, `sim_time`, `content`, `proaction_window_s`, `keywords`, `briefing`, or `intents` invalidates the protocol.
6. Commit as "M8b: externally-authored test_v4 (fresh session, <timestamp>)".

### Rejections log

(Populated during Commit B. Each rejection notes: fresh-session timestamp, first violated constraint, one-sentence description of the violation. A rejected generation is not merged; the generator code is not kept.)

_None yet._

### Pre-registered success criteria (frozen before any generation or eval run)

Let `15a = runs/data/15a-content-test_v4.json` (HeargentZAWide, content arbiter, M7 frozen config), `15b = runs/data/15b-random-test_v4.json` (p=0.75, seed=42), `15c = runs/data/15c-poll-test_v4.json` (react_poll_local), `15d = runs/data/15d-cron30-test_v4.json` (CronKeyword30s).

**P1 — Primary: headline preservation.** `hit_rate(15a) ≥ 0.80`. This is the M6a main claim; passing on test_v4 extends "hit ≥ 0.80 on every trace" from 3 traces to 4 (externally authored + spec-aligned).

**P2 — Secondary: Pareto preservation.** `tok_per_hit(15a) ≤ tok_per_hit(15c) / 3`. Content cell at least 3× cheaper per hit than poll on the same trace. M6a's range is 6.8–11.3×; 3× is a conservative floor below the minimum.

**P3 — Tertiary: C3 single-seed (report-only).** With content reference 15a and random cell 15b: either `hit_rate(15a) − hit_rate(15b) ≥ 0.20` OR `false_initiation_rate_per_hour(15a) − false_initiation_rate_per_hour(15b) ≤ −5.0`. **Report-only.** A single seed is not a robust claim; this criterion is recorded verbatim either way and does not gate paper framing.

**P4 — Sanity gate: trace fairness.** `hit_rate(15c) ≥ 0.80`. If poll itself falls below 0.80, the trace is too hard or ambiguous for all agents — all numbers are reported but the primary verdict is read through that lens.

### Decision rules (frozen; no post-hoc redefinition)

- **P1 PASS.** Headline extends from 3 → 4 traces. Paper's "single-config regime-robust" claim tightens. runs/README.md headline updates to reflect the four-trace result.
- **P1 `0.60 ≤ hit < 0.80`.** Headline softens to *"hit ≥ 0.80 on 3 of 4 traces, ≥ 0.60 on the fourth."* No config change on test_v4. Any fix must be pre-registered as a new experiment against a new externally-authored trace (`test_v5`); we do not retune against the trace that caught the regression.
- **P1 `hit < 0.60`.** Headline falsified on external trace. Report mechanistically: for each miss, tag whether it was a band-edge miss (z outside [−0.5, +1.5]), a predictor-latch, a V2-prompt gap, or something new. No config change without a new experiment on a new trace.
- **P2 FAIL.** Pareto claim softens to *"cheaper than poll, but the magnitude varies by trace."* Report verbatim tok/hit numbers.
- **P3 PASS or FAIL.** Reported either way. A single-seed FAIL is not grounds for discarding C3; a 20-seed sweep on `test_v4` (drop-in under the existing `--arbiter-random-seed` wiring) is the clean follow-up if reviewers push for seed-robustness on the external trace too.
- **P4 FAIL.** Report all four cells' numbers and note the trace is unfair to all agents on Pareto; the primary verdict on P1 still stands. The trace is kept — an unfair trace does not retroactively become a "design-your-own-eval" attack defense, but it also does not get discarded because the agent happened to do badly on it.

**Protocol-failure rule (M8b-specific).** If the M8-style misalignment happens again under the updated spec (the new constraint is met but hit-rate collapses for a distinct new reason that maps to yet another implicit convention), the next iteration tightens the spec further and re-runs as `test_v5`. We do not retune against a trace that surfaces a new gap. This is how the protocol converges.

No raising of cell count, no seed substitution on P3, no post-hoc bar redefinition, no trace regeneration in response to eval outcome.

## Architecture changes

**None.** The `--arbiter-random-seed` CLI flag, `HeargentZAWide`, the V2 arbiter prompt, the band `[−0.5, +1.5]`, and all predictor / surprise / baseline code are frozen at the M7 state (SHA `ca34e1d` and ancestors); M8 added no architecture changes either. The only code change in Commit B is `sandbox/event_trace.py`: one new function `test_trace_v4()` plus a single entry in the `get_trace` registry. `test_trace_v3()` and the existing `"test_v3"` registry entry are **not touched**.

## Critical files

- `sandbox/event_trace.py:340–350` — `get_trace()` registry. Commit B adds `"test_v4": test_trace_v4`.
- `sandbox/event_trace.py` (end of file, after `test_trace_v3()`) — Commit B appends `def test_trace_v4() -> Trace:`.
- `runs/15-external-test_v4.md` — this pre-reg doc (Commit A). Results appended post-eval.
- `runs/README.md` — row 15 added post-eval (Commit C+).
- `agent/loop.py`, `agent/arbiter.py`, `eval/run_trace.py`, `agent/predictor.py`, `agent/surprise.py`, all files under `baselines/`, `sandbox/event_trace.py`'s existing `test_trace_v3()` — **not touched.**

## Reproduce

After Commit B has landed a compliant `test_v4`:

```sh
# 15a — content arbiter (primary)
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v4 \
  --arbiter-mode content \
  --out runs/data/15a-content-test_v4.json

# 15b — matched-firing-rate random arbiter (tertiary; single seed, report-only)
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v4 \
  --arbiter-mode random \
  --arbiter-random-p 0.75 \
  --arbiter-random-seed 42 \
  --out runs/data/15b-random-test_v4.json

# 15c — poll (sanity ceiling + Pareto denominator)
uv run python -m eval.run_trace \
  --agent baselines.react_poll_local:ReactPollLocal \
  --trace test_v4 \
  --out runs/data/15c-poll-test_v4.json

# 15d — cron 30 s (structural baseline)
uv run python -m eval.run_trace \
  --agent baselines.react_cron_keyword:CronKeyword30s \
  --trace test_v4 \
  --out runs/data/15d-cron30-test_v4.json
```

**Pre-eval sanity checks** (all three required before any of the four cells fire):

```sh
# Schema & structural constraint check at datastructure level
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v4'); \
  print(len(t.ground_truth), len(t.events), round(t.duration_s, 1))"
# Must print: 5 9 <value ≤ ~1030>

# NEW — Keyword/content alignment audit (M8b's addition)
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v4'); \
  [print(gt.event.id, kw, kw.lower() in gt.event.content.lower()) \
   for gt in t.ground_truth for kw in gt.keywords]"
# Every line must end in True. Any False → reject the generation, log in Rejections, open new fresh session.

# Bit-identical re-run of one M6a content cell to confirm no environmental drift
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode content --out /tmp/smoke-12a.json
# Compare hit_rate, false_initiation_rate_per_hour, total_notifications, misses
# against runs/data/12a-heargent-za-v2wide-dev_v2.json — must match exactly.
```

## Non-goals for this pass

- Do not touch `agent/`, `baselines/`, or `eval/`. Config is frozen at M7.
- Do not edit `sandbox/event_trace.py`'s existing `test_trace_v3()` or its registry entry. `test_v3` stays in the repo as the artifact that surfaced the keyword-alignment gap; "fixing" it would undermine the audit trail.
- Do not re-run M6a or M7 cells beyond the one-cell smoke test above.
- Do not vary the arbiter seed beyond `42` on `test_v4`. N=20 seed sweep on `test_v4` is a future pass, not M8b.
- Do not edit the authoring prompt once committed. A prompt change requires re-committing this doc and restarting the protocol.
- Do not edit the generated `test_trace_v4()` beyond the permitted syntactic edits. Any semantic edit invalidates the external-authoring claim.
- Do not regenerate `test_v4` in response to unfavourable eval results. A trace that fails the primary under a compliant generation is reported honestly; retuning happens on a NEW trace if at all.

This pass is strictly narrower than M7: zero code in `agent/`, one new trace, four eval cells, one report. It is also strictly narrower than M8 — the only meaningful spec delta is one new hard constraint.

## Results

_Pending Commit B (externally-authored `test_v4`) and Commit C+ (eval runs)._
