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

### Pre-flight bit-identical smoke (before 15a–d fired)

Re-ran `uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace dev_v2 --arbiter-mode content --out /tmp/smoke-12a.json` under the M8b tree (post-Commit-B, `cdf689e`) and diffed against `runs/data/12a-heargent-za-v2wide-dev_v2.json`. Bit-identical on `hit_rate` (1.0), `false_initiation_rate_per_hour` (0.0), `total_notifications` (5), `misses` ([]). Registry addition of `"test_v4": test_trace_v4` did not perturb existing behavior.

### Full 4-cell matrix

| cell | agent | hit | n_hits | false/h | n_notif | tok_total | tok/hit | misses |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 15a | HeargentZAWide content | 0.40 | 2 | 7.13 | 4 | 3 859 | 1 930 | parking_meter_oak, cover_standup_request, protest_commute_route |
| 15b | HeargentZAWide random p=0.75 seed=42 | 1.00 | 5 | 14.26 | 9 | 2 361 | 472 | — |
| 15c | react_poll_local | 1.00 | 5 | 3.56 | 6 | 35 640 | 7 128 | — |
| 15d | CronKeyword30s | 1.00 | 5 | 14.26 | 9 | 0 | 0 | — |

Poll, random, and cron all reach hit = 1.00. The content arbiter alone misses 3 of 5. This rules out the M8-style "unfair trace" interpretation — `test_v4` is scoreable by every other agent in the matrix, and `_matches_keywords` passes for all 5 GTs (the new alignment constraint worked).

### Mechanistic per-event behavior (15a content cell, from `surprise_log`)

| event | role | t | z | arbiter_call | arbiter_decision | surfaced | tag |
|---|---|---:|---:|:---:|:---:|:---:|---|
| linkedin_connections | distractor | 50.0 | `None` (bootstrap) | yes | NO | ✗ | correct NO |
| **parking_meter_oak** | **GT** | **180.0** | **`None` (bootstrap)** | **yes** | **NO** | **✗** | **miss — V2-prompt gap** |
| **cover_standup_request** | **GT** | **240.0** | **`None` (bootstrap)** | **yes** | **NO** | **✗** | **miss — V2-prompt gap** |
| github_repo_star | distractor | 310.0 | `None` (bootstrap) | yes | NO | ✗ | correct NO |
| gym_class_cancelled | GT | 380.0 | −1.69 | no (auto-surf) | — | ✓ | HIT |
| designgrid_renewal | distractor | 440.0 | −0.64 | no (auto-surf) | — | ✓ | false init — auto-surface on routine-templated distractor |
| library_hold_expiring | GT | 520.0 | −1.66 | no (auto-surf) | — | ✓ | HIT |
| **protest_commute_route** | **GT** | **700.0** | **−0.06 (in-band)** | **yes** | **NO** | **✗** | **miss — V2-prompt gap** |
| calendar_feature_tip | distractor | 820.0 | −1.31 | no (auto-surf) | — | ✓ | false init — auto-surface on routine-templated distractor |

`llm_stats.arbiter_calls = 5`, `arbiter_yes_rate = 0.0`. **The arbiter said NO to every event it was consulted on.** Two of those NOs are correct (distractors); three are wrong (GTs). Separately, the z < −0.5 auto-surface branch fires twice on routine-templated distractors (`designgrid_renewal`, `calendar_feature_tip`) whose content is linguistically predictable enough to land well inside the auto-surface region — the arbiter is bypassed by design, so these never get a NO.

### Per-miss mechanistic tags (as required by the P1 `< 0.60` decision rule)

- **`parking_meter_oak`** (t=180, z=`None`, window=20 s): V2-prompt gap. Content: *"Parking meter at Oak Street lot expires in 30 minutes. Enforcement active in zone."* Urban personal time-sensitive warnings (parking, ticketing, etc.) are not among the V2 prompt's YES categories (scheduling, personal deliveries, weather alerts, …). Compounded by bootstrap — the rolling window had accumulated only one prior event, so arbiter was consulted under the M4+ bootstrap policy. Not a band-edge miss (no z to check); not a predictor-latch.
- **`cover_standup_request`** (t=240, z=`None`, window=420 s): V2-prompt gap. Content: colleague asking the user to cover tomorrow's standup and post a sprint tracker update while the colleague is on vacation. Social asks from colleagues with a concrete deadline do not map onto any V2 YES category. Bootstrap-phase consultation again (two priors at time of call).
- **`protest_commute_route`** (t=700, z=−0.06, window=280 s): V2-prompt gap. Content: protest march 5–7pm along Market Street, expected commute detours. Civil-disruption alerts affecting planned activities are not a V2 YES category (V2 covers weather alerts but not civil/street disruption). In-band (z well inside [−0.5, +1.5]), arbiter consulted, NO. Not a band-edge miss.

All three misses are the same failure mode: **the V2 prompt's YES enumeration is narrower than the test_v4 GT distribution.** None are band-edge misses, none are predictor-latches, none are "something new" — they are the M4 → M5 failure pattern ("regime-selective gaps on phrasings outside the prompt's examples") recurring on an externally-authored trace.

### Pre-registered criteria — literal evaluation

Evaluated verbatim against rules frozen in commit `33926fc`. No post-hoc redefinition.

- **P1 — Primary: headline preservation. Bar: hit_rate(15a) ≥ 0.80.**
  **FAIL**, in the `< 0.60` branch (hit = 0.40). Per the decision rule: headline falsified on external trace; report mechanistically. Mechanistic tags above: 3 × V2-prompt gap, 0 × band-edge, 0 × predictor-latch, 0 × novel. No config change on `test_v4`.

- **P2 — Secondary: Pareto preservation. Bar: tok/hit(15a) ≤ tok/hit(15c) / 3.**
  **PASS** literally (1 930 ≤ 2 376). Ratio 3.69× (below M6a's 6.8–11.3× band and just above the 3× floor). With a 2-hit denominator on 15a vs 5-hit on 15c, the number is meaningful but narrow — the content arbiter is cheaper per correct hit than poll on this trace, but only because it's surfacing less of everything, not because it's selecting well.

- **P3 — Tertiary (report-only): C3 single-seed. Criterion: Δhit ≥ 0.20 OR Δfalse/h ≤ −5.0.**
  **PASS** literally (Δfalse/h = −7.13 ≤ −5.0). However, Δhit = **−0.60** — content **loses three hits** relative to random on this trace. This is a pyrrhic literal pass: the random arbiter (which YES's 75 % of in-band + bootstrap events) catches all 5 GTs by accepting more events, while content's NO-bias rejects three GTs along with the two distractors. The letter of P3 holds; the spirit does not. Report-only per the pre-reg.

- **P4 — Sanity gate: trace fairness. Bar: hit_rate(15c) ≥ 0.80.**
  **PASS** (hit = 1.00). Poll, random, and cron all reach 1.00; cron's keyword list even happens to match all 5 GTs' lexicon. `test_v4` is fair to every agent in the matrix except the content arbiter. Unlike M8, there is no trace-unfairness escape hatch.

### Governing interpretation

P1 fails cleanly in the `< 0.60` branch on a trace that passes P4, was authored by a fresh session under a spec-compliant protocol, and is scored correctly by every other baseline in the matrix. Per the pre-reg decision rule, the M6a headline **is falsified on an externally-authored, spec-compliant trace**. No "trace unfairness" defense is available here; the M8 sanity-gate loophole does not apply.

What is preserved:
1. **M6a's three-trace claim stands as a three-trace claim.** Hit ≥ 0.80 on `dev_v2`, `test_v1`, `test_v2` at 6.8–11.3× lower tok/hit than poll remains bit-identical to M6a. The 12a smoke test earlier in this doc confirms no drift.
2. **M7's C3 seed-variance result on test_v2 stands** unchanged (18/20 seeds on the `Δhit ≥ 0.20 OR Δfalse/h ≤ −5.0` bar; trace-specific).
3. **The external-authoring protocol itself is validated.** M8b's three-commit protocol (pre-reg → fresh session generates → eval) with the tightened keyword/content-alignment constraint produced a trace that is scoreable, fair, and genuinely discriminative. The M8 scoring-gap regression did not recur. This is the outcome the protocol was designed to produce when the agent has a real weakness — surface the weakness honestly without letting curation hide it.

What is falsified:
- The broad "hit ≥ 0.80 on every trace under a single frozen configuration" extension to externally-authored trace(s). The V2 prompt's YES enumeration does not generalize to urban warnings, colleague social asks, or civil-disruption commute alerts.

### What this means for the paper and what comes next

1. **M8b closes as "P1 falsified in the < 0.60 branch; V2-prompt gap (not band-edge, not predictor-latch); no config change on this trace."** The three commits land as: `33926fc` pre-reg, `cdf689e` externally-authored trace, this commit results. `test_v4` stays in the repo uncorrected as the artifact that falsified the V2 prompt's coverage claim.

2. **No config change on the agent in response to `test_v4`.** Per the decision rules, `test_v4` is not a trace to retune against. Any prompt-coverage fix lives in a new experiment under a new externally-authored trace (`test_v5`) with correspondingly extended bans (test_v4's 5 GT + 4 distractor ids and their themes/pairs).

3. **M9 candidate (next pass, NOT landed here): re-architect the V2 prompt from a closed list of YES categories to a broader criterion, validate on `test_v5` under the M8b protocol.** The V2 prompt as frozen at M5/M6a works for the three traces it was co-developed against (scheduling / personal deliveries / weather / a few more) but not for the broader distribution surfaced by an external author (urban warnings, colleague asks, civil disruption). A re-architected V3 prompt would move from "list of YES regimes" to a principled criterion (e.g. "warrants user attention within the next N hours AND requires a decision or action the user would regret missing"), tested single-shot on `test_v5`.

4. **Paper framing update.** The previous headline — *"single-config regime-robust content arbiter delivers hit ≥ 0.80 on every trace at 6.8–11.3× lower token cost per correct proaction than poll, under a single frozen configuration across three structurally distinct traces"* — remains accurate as a three-trace claim. The external-trace extension is **withdrawn** (previously deferred to M8b; now falsified on M8b). The honest framing for this version of the paper:

   > *Surprise-gated selective initiation with a content arbiter (V2 prompt, co-developed on three curated traces) delivers hit ≥ 0.80 on every co-developed trace at 6.8–11.3× lower tok/hit than poll. Mechanism attribution confirmed via matched-firing-rate random ablation, seed-variance hardened on test_v2 across N = 20 random-arbiter seeds. **Under the M8b external-authoring protocol (fresh Claude Code session authors a spec-compliant trace with no agent context), the V2 prompt's coverage fails on urban warnings / colleague asks / civil-disruption alerts: hit drops to 0.40 on an externally-authored trace where poll, random, and cron all reach 1.00. All three misses tag as V2-prompt-coverage gaps, not band-edge or predictor-latch. The external-authoring protocol is presented as the methodological contribution that surfaced this.***

   This is a better paper than the unfalsifiable-sounding "every trace" claim. The external-authoring protocol is now demonstrated to be load-bearing: it surfaced a weakness that curated-trace validation could not. That is the review-attack closer M8 was meant to provide, just in the honest direction (prompt-coverage brittleness confirmed rather than denied).

5. **Secondary observation recorded (not actioned on test_v4).** 2 false initiations came through the `z < −0.5` auto-surface branch on routine-templated distractors (`designgrid_renewal`, `calendar_feature_tip`) whose content is predictable enough to land deep in the auto-surface region without arbiter consultation. The inverted-polarity auto-surface rule (the M6a band's lower edge) has a precision cost on routine-templated distractors. A single externally-authored trace is not grounds for revisiting the lower band edge, but this is flagged for the record; it would be the companion lever to the V2 prompt re-work if M9/M10 widens scope.

### Rejections log

_No rejections. The fresh session's first output passed the 11 hard structural constraints (including the new keyword/content alignment constraint) and 3 banned lists on first audit._

## Artifacts

- `runs/data/15a-content-test_v4.json` / `15b-random-test_v4.json` / `15c-poll-test_v4.json` / `15d-cron30-test_v4.json` — 4 cells, one JSON per cell.
- `sandbox/event_trace.py` (end of file, commit `cdf689e`) — `test_trace_v4()` as authored by the fresh session, unmodified.
- `runs/15-external-test_v4.md` — this doc. Pre-reg (§ Goal through § Non-goals) committed at `33926fc`; results at this commit.
- Aggregation: `uv run python` one-liner against the 4 JSONs; no hidden state.
- Code: none changed. `agent/`, `baselines/`, `eval/`, `sandbox/world.py`, `sandbox/event_trace.py`'s existing `test_trace_v1/v2/v3` all byte-identical to pre-M8b state.
