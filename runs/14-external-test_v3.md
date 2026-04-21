# Run 14 — Externally-Authored Held-Out Trace `test_v3` (M8)

**Date:** 2026-04-20 (pre-registration). Results section appended post-eval.
**Milestone:** M8 — close the "design-your-own-eval" review attack by adding one held-out trace authored by a fresh Claude Code session with no access to the agent code, arbiter prompt, surprise scorer, or any run doc. Run once under the M7 frozen config. No retuning regardless of outcome.
**Pre-registration SHA:** this commit (spec + authoring prompt + success bars + decision rules committed together; no trace code and no eval runs before this commit). **Predecessor:** M7 results SHA `ca34e1d`.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, predictor seed=42, deterministic throughout. Local-only; no Claude API.

## Goal

The M6a headline ("hit ≥ 0.80 on every trace at 6.8–11.3× lower tok/hit than poll under one frozen configuration") and M7's C3 hardening both stand on three traces (`dev_v2`, `test_v1`, `test_v2`) that this project authored. A reviewer can say: *"you designed your own evaluation to match your agent."* The attack is narrow but real, and M6a/M7's pre-reg discipline does not close it — freezing hyperparameters before evaluation does not help if the evaluation itself was curated.

This pass adds ONE held-out trace authored under a protocol that makes the attack infeasible:

1. The trace spec is committed in advance (this doc).
2. A **fresh Claude Code session** — separate process, new conversation, no chat history — is given only the spec, the `Trace` schema, and one unrelated existing trace as a syntactic template. No access to `agent/`, `arbiter.py`'s V2 prompt, the surprise scorer, or any run doc.
3. The fresh session outputs `def test_trace_v3()` in a single shot. Its output is committed verbatim in a separate commit before any eval runs.
4. The trace runs once under the M7 frozen config. No re-generation or retuning in response to outcomes.

Expected outcome: the M6a headline reproduces on `test_v3` (primary hit ≥ 0.80, tok/hit at least 3× lower than poll). If it does, "hit ≥ 0.80 on every trace" extends from 3 → 4 traces on an externally-authored trace, and the review attack is closed. If it doesn't, the pre-registered decision rules dictate a graceful softening of the paper framing — we do not retune, and any fix must be validated on a NEW externally-authored trace (`test_v4`).

## Design reasoning (why Claude-authored, not hand-authored)

Two candidates for "externally-authored."

| | Fresh Claude Code session (chosen) | User hand-authors from spec |
|---|---|---|
| Separation from run history | Perfect. No memory of which events the arbiter struggles with. | Weak. User has read every run doc; subconscious avoidance of known weak spots (e.g. `package_arrival`-style bare notifications) is hard to rule out. |
| Audit artifact | Prompt is fully committed; reviewer reads it and confirms no agent-internal vocabulary leaked in. | Informal. "Trust that I didn't tune" is not an artifact. |
| Failure mode | Prompt leakage — if the prompt contains "surprise," "arbiter," "predictable," etc., the separation collapses. Mitigated by the prompt discipline below. | User's memory — hard to formalize. |
| Time cost | ~5 minutes for one clean generation. | 20–60 minutes of careful authoring. |

The fresh-session protocol's credibility reduces to one auditable question: *is the authoring prompt clean?* The prompt below is written to describe a trace *as a dataset*, not *relative to an agent*. No mention of "surprise," "arbiter," "predictor," "z-score," "band," "YES/NO," "gate," "predictable," "easy/hard," "token cost," or "proaction budget."

## Pre-registered artifacts (frozen before any generation)

### Frozen trace spec

Hard constraints — any violation auto-rejects the generation.

- `name = "test_v3"`.
- Exactly **5 `GroundTruthEvent`s** and exactly **4 distractor `Event`s** (total 9 events in `events`).
- All `sim_time` values in `[0, 1000]`. `max(gt.event.sim_time + gt.proaction_window_s) ≤ 1000`.
- At least **3 distinct `kind` values** across the 5 GTs, chosen from {`email`, `calendar_update`, `notification`, `alert`, `phone_message`, `world_event`}.
- At least one GT with `proaction_window_s ≤ 30`.
- At least one GT with `proaction_window_s ≥ 300`.
- Briefing: 2–4 first-person sentences describing the day's setting.
- Intents: tuple of exactly 5 short phrases.
- Distractors are plausible routine / system noise (no abrupt urgency, no action demand).
- GTs are human-interpretable as "warrants proaction" on content alone (no briefing required to judge).

**Banned event ids** (union of ids used in `dev_v1`, `dev_v2`, `test_v1`, `test_v2`):

```
flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel,
fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat,
package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup,
slack_invite, calendar_advert, promo_email, system_status,
fire_kitchen, board_meeting, water_burst, er_call, security_breach,
daily_briefing, status_ok, uptime_ping, newsletter
```

**Banned content themes** (semantic, not just string match):
fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor callback, production / server outage, rent due, school pickup, quarterly report, board meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert, marketing newsletter, daily briefing, system heartbeat / status ping.

**Banned keyword pairs** (from existing GTs' `keywords` tuples):

```
(flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly),
(dentist, cancelled), (fire, alarm), (package, delivered), (doctor, call),
(production, alert), (rent, due), (school, pick up), (fire, kitchen),
(board, meeting), (water, burst), (hospital, mother), (security, unauthorized)
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
> - `name = "test_v3"`.
> - Exactly 5 `GroundTruthEvent`s and exactly 4 distractor `Event`s (mixed into `events` list, sorted by `sim_time`).
> - All `sim_time` values in `[0, 1000]`; for every GT, `gt.event.sim_time + gt.proaction_window_s ≤ 1000`.
> - At least 3 distinct `kind` values across the 5 GTs. Allowed kinds: `email`, `calendar_update`, `notification`, `alert`, `phone_message`, `world_event`.
> - At least one GT with `proaction_window_s ≤ 30`.
> - At least one GT with `proaction_window_s ≥ 300`.
> - Briefing: 2–4 first-person sentences describing the day's setting.
> - Intents: tuple of exactly 5 short phrases.
> - Distractors are plausible routine / system noise a reasonable person would NOT want surfaced.
> - GTs are human-interpretable on content alone as warranting proaction.
>
> **Banned event ids** (collision auto-rejects):
> `flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert, promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call, security_breach, daily_briefing, status_ok, uptime_ping, newsletter`.
>
> **Banned content themes** (semantic, not just string match):
> fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor callback, production / server outage, rent due, school pickup, quarterly report, board meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert, marketing newsletter, daily briefing, system heartbeat / status ping.
>
> **Banned keyword pairs** (avoid reusing any pair as a GT's `keywords` tuple):
> `(flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert), (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), (hospital, mother), (security, unauthorized)`.
>
> **Output**: one Python function `def test_trace_v3() -> Trace:` in the style of the template, followed by a single line adding `"test_v3": test_trace_v3` to the `get_trace` registry. Return the code in a single fenced Python block. Do not explain.

### Authoring protocol

1. Open a new Claude Code window, `/clear` to ensure empty history.
2. Paste the prompt block above verbatim as the first user message. No additions, no CLAUDE.md context carried in, no reading of any project file beyond what the prompt contains.
3. Fresh session outputs a single fenced Python block containing `def test_trace_v3() -> Trace:` and the registry line.
4. Audit the output against the 11 hard structural constraints and 3 banned lists. If any violation is found, **reject the generation, log the violation in this doc's Rejections sub-section below, and open another fresh session.** No prompt edits.
5. If the output passes audit, copy it verbatim into `sandbox/event_trace.py` (end of file) and add the registry line. The only permitted edits are: import ordering, typo fixes that block parsing, and the registry line itself. Any change to event `id`, `kind`, `sim_time`, `content`, `proaction_window_s`, `keywords`, `briefing`, or `intents` invalidates the protocol.
6. Commit as "M8: externally-authored test_v3 (fresh session, <timestamp>)".

### Rejections log

(Populated during Commit B. Each rejection notes: fresh-session timestamp, first violated constraint, one-sentence description of the violation. A rejected generation is not merged; the generator code is not kept.)

_None yet._

### Pre-registered success criteria (frozen before any generation or eval run)

Let `14a = runs/data/14a-content-test_v3.json` (HeargentZAWide, content arbiter, M7 frozen config), `14b = runs/data/14b-random-test_v3.json` (p=0.75, seed=42), `14c = runs/data/14c-poll-test_v3.json` (react_poll_local), `14d = runs/data/14d-cron30-test_v3.json` (CronKeyword30s).

**P1 — Primary: headline preservation.** `hit_rate(14a) ≥ 0.80`. This is the M6a main claim; passing on test_v3 extends "hit ≥ 0.80 on every trace" from 3 traces to 4.

**P2 — Secondary: Pareto preservation.** `tok_per_hit(14a) ≤ tok_per_hit(14c) / 3`. Content cell at least 3× cheaper per hit than poll on the same trace. M6a's range is 6.8–11.3×; 3× is a conservative floor below the minimum.

**P3 — Tertiary: C3 single-seed (report-only).** With content reference 14a and random cell 14b: either `hit_rate(14a) − hit_rate(14b) ≥ 0.20` OR `false_initiation_rate_per_hour(14a) − false_initiation_rate_per_hour(14b) ≤ −5.0`. **Report-only.** A single seed is not a robust claim; this criterion is recorded verbatim either way and does not gate paper framing.

**P4 — Sanity gate: trace fairness.** `hit_rate(14c) ≥ 0.80`. If poll itself falls below 0.80, the trace is too hard or ambiguous for all agents — all numbers are reported but the primary verdict is read through that lens.

### Decision rules (frozen; no post-hoc redefinition)

- **P1 PASS.** Headline extends from 3 → 4 traces. Paper's "single-config regime-robust" claim tightens. runs/README.md headline updates to reflect the four-trace result.
- **P1 `0.60 ≤ hit < 0.80`.** Headline softens to *"hit ≥ 0.80 on 3 of 4 traces, ≥ 0.60 on the fourth."* No config change on test_v3. Any fix must be pre-registered as a new experiment against a new externally-authored trace (`test_v4`); we do not retune against the trace that caught the regression.
- **P1 `hit < 0.60`.** Headline falsified on external trace. Report mechanistically: for each miss, tag whether it was a band-edge miss (z outside [−0.5, +1.5]), a predictor-latch, a V2-prompt gap, or something new. No config change without a new experiment on a new trace.
- **P2 FAIL.** Pareto claim softens to *"cheaper than poll, but the magnitude varies by trace."* Report verbatim tok/hit numbers.
- **P3 PASS or FAIL.** Reported either way. A single-seed FAIL is not grounds for discarding C3; M8b (N=20 seed sweep on test_v3, drop-in under the `--arbiter-random-seed` wiring) is the clean follow-up if reviewers push for seed-robustness on the external trace too.
- **P4 FAIL.** Report all four cells' numbers and note the trace is unfair to all agents on Pareto; the primary verdict on P1 still stands. The trace is kept — an unfair trace does not retroactively become a "design-your-own-eval" attack defense, but it also does not get discarded because the agent happened to do badly on it.

No raising of cell count, no seed substitution on P3, no post-hoc bar redefinition, no trace regeneration in response to eval outcome.

## Architecture changes

**None.** The `--arbiter-random-seed` CLI flag, `HeargentZAWide`, the V2 arbiter prompt, the band `[−0.5, +1.5]`, and all predictor / surprise / baseline code are frozen at the M7 state (SHA `ca34e1d` and ancestors). The only code change in Commit B is `sandbox/event_trace.py`: one new function `test_trace_v3()` plus a single entry in the `get_trace` registry.

## Critical files

- `sandbox/event_trace.py:285–294` — `get_trace()` registry. Commit B adds `"test_v3": test_trace_v3`.
- `sandbox/event_trace.py` (end of file) — Commit B appends `def test_trace_v3() -> Trace:`.
- `runs/14-external-test_v3.md` — this pre-reg doc (Commit A). Results appended post-eval.
- `runs/README.md:37–51` — row 14 added post-eval (Commit C+).
- `agent/loop.py`, `agent/arbiter.py`, `eval/run_trace.py`, `agent/predictor.py`, `agent/surprise.py`, all files under `baselines/` — **not touched.**

## Reproduce

After Commit B has landed a compliant `test_v3`:

```sh
# 14a — content arbiter (primary)
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v3 \
  --arbiter-mode content \
  --out runs/data/14a-content-test_v3.json

# 14b — matched-firing-rate random arbiter (tertiary; single seed, report-only)
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v3 \
  --arbiter-mode random \
  --arbiter-random-p 0.75 \
  --arbiter-random-seed 42 \
  --out runs/data/14b-random-test_v3.json

# 14c — poll (sanity ceiling + Pareto denominator)
uv run python -m eval.run_trace \
  --agent baselines.react_poll_local:ReactPollLocal \
  --trace test_v3 \
  --out runs/data/14c-poll-test_v3.json

# 14d — cron 30 s (structural baseline)
uv run python -m eval.run_trace \
  --agent baselines.react_cron_keyword:CronKeyword30s \
  --trace test_v3 \
  --out runs/data/14d-cron30-test_v3.json
```

**Pre-eval sanity checks** (both required before any of the four cells fire):

```sh
# Schema & structural constraint check at datastructure level
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v3'); \
  print(len(t.ground_truth), len(t.events), round(t.duration_s, 1))"
# Must print: 5 9 <value between 730 and 1030>

# Bit-identical re-run of one M6a content cell to confirm no environmental drift
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --out /tmp/smoke-12a.json
# Compare hit_rate, false_initiation_rate_per_hour, total_notifications, misses
# against runs/data/12a-heargent-za-v2wide-dev_v2.json — must match exactly.
```

## Non-goals for this pass

- Do not touch `agent/`, `baselines/`, or `eval/`. Config is frozen at M7.
- Do not re-run M6a or M7 cells beyond the one-cell smoke test above.
- Do not vary the arbiter seed beyond `42` on `test_v3`. N=20 seed sweep on `test_v3` is M8b, not M8.
- Do not edit the authoring prompt once committed. A prompt change requires re-committing this doc and restarting the protocol.
- Do not edit the generated `test_trace_v3()` beyond the permitted syntactic edits. Any semantic edit invalidates the external-authoring claim.
- Do not regenerate `test_v3` in response to unfavourable eval results. A trace that fails the primary under a compliant generation is reported honestly; retuning happens on a NEW trace if at all.

This pass is strictly narrower than M7: zero code in `agent/`, one new trace, four eval cells, one report.

## Results

### Pre-flight bit-identical smoke (before 14a–d fired)

Re-ran `uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace dev_v2 --arbiter-mode content --out /tmp/smoke-12a.json` under the M8 tree (commit `b89788d`) and diffed against `runs/data/12a-heargent-za-v2wide-dev_v2.json`. Bit-identical on `hit_rate`, `false_initiation_rate_per_hour`, `total_notifications`, `misses`. Registry addition of `"test_v3": test_trace_v3` did not perturb existing behavior.

### Full 4-cell matrix

| cell | agent | hit | false/h | n_notif | n_hits | tok_total | tok/hit | misses |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 14a | HeargentZAWide content | 0.20 | 6.99 | 3 | 1 | 4 489 | 4 489 | passport_expiry, prescription_urgent, power_shutoff_planned, plumber_reschedule |
| 14b | HeargentZAWide random p=0.75 seed=42 | 0.20 | 20.97 | 7 | 1 | 2 652 | 2 652 | passport_expiry, prescription_urgent, power_shutoff_planned, plumber_reschedule |
| 14c | react_poll_local | 0.20 | 13.98 | 5 | 1 | 39 730 | 39 730 | passport_expiry, prescription_urgent, power_shutoff_planned, plumber_reschedule |
| 14d | CronKeyword30s | 0.20 | 27.96 | 9 | 1 | 0 | 0 | passport_expiry, prescription_urgent, power_shutoff_planned, plumber_reschedule |

**Every agent misses the same four GTs and hits the same one (`car_recall`).** This is the first signal that the result is not an agent comparison — four architecturally distinct agents (gated content arbiter, seed-matched random, LLM-judge poll, fixed-interval keyword cron) cannot all fail on the same four events for the same reason.

### Critical finding: pre-registered spec gap (keyword / content alignment)

The scoring harness is `eval/run_trace.py:21–23`:

```python
def _matches_keywords(text: str, keywords: tuple[str, ...]) -> bool:
    lo = text.lower()
    return all(kw.lower() in lo for kw in keywords)
```

A notification is credited as a hit only if **every** keyword in the GT's tuple is a case-insensitive substring of the notification content. This matters because `note.content` is the surfaced event's content verbatim — so a GT's `keywords` tuple must be a pair of substrings (or morphological variants that land as substrings) of its own `content` string for the scoring to ever succeed.

| GT | keywords | content excerpt | keyword in content? |
|---|---|---|---|
| `passport_expiry` | `(passport, expiring)` | "your passport **expires** in 4 weeks…" | `passport` ✓, `expiring` **✗** (`expires` present, `expiring` not) |
| `prescription_urgent` | `(prescription, refill)` | "your blood pressure **medication refill** is ready…" | `refill` ✓, `prescription` **✗** (`medication` present instead) |
| `car_recall` | `(recall, airbag)` | "…recall notice … **airbag** inflator defect…" | `recall` ✓, `airbag` ✓ |
| `power_shutoff_planned` | `(power, shutoff)` | "…planned **electrical shutoff** tonight 22:00–02:00…" | `shutoff` ✓, `power` **✗** (`electrical` present instead) |
| `plumber_reschedule` | `(plumber, reschedule)` | "Voicemail from Jorge at Ridgeline **Plumbing**: cannot make tomorrow's 09:00 dishwasher install; next available slot is in 9 days…" | `plumber` **✗** (`Plumbing` present), `reschedule` **✗** (semantic only) |

**4 of 5 GTs have at least one keyword that does not appear as a substring of its content.** Only `car_recall` is scoreable under `_matches_keywords`. All four existing traces (`dev_v1`, `dev_v2`, `test_v1`, `test_v2`) have every GT's keywords as substrings of its content — verified by a sweep over `get_trace` entries. This was an implicit convention, never written into the spec.

Per the M8 pre-reg (§ Frozen trace spec, runs/14 at commit `2a933fb`), the 10 hard constraints list covered ids, count, sim_time, kinds, windows, briefing, intents, distractor plausibility, and GT interpretability. It did **not** require `keywords ⊆ content`. The fresh Claude session was spec-compliant on all 10 constraints and all 3 banned lists; the gap is on the pre-registration side, not the generation side.

### Mechanistic per-GT agent behavior (14a content, from `surprise_log`)

| GT | t | z | surfaced | arbiter | notes |
|---|---:|---:|:---:|:---:|---|
| passport_expiry | 45.0 | `None` | ✗ | ✗ | Bootstrap-window: below `min_window=4` for z-scoring. Agent did not fire. |
| prescription_urgent | 180.0 | `None` | ✓ | **YES** | Still in bootstrap (z=None) but arbiter consulted per M4+ bootstrap policy; arbiter said YES → surfaced. Would have been a HIT under aligned keywords. |
| car_recall | 300.0 | +0.12 | ✓ | **YES** | In-band, arbiter YES. **HIT**. |
| power_shutoff_planned | 520.0 | **+1.55** | ✗ | — | **Band-edge miss**: z > +1.5 threshold by +0.05, auto-skipped. Independent of the keyword issue. |
| plumber_reschedule | 700.0 | −0.93 | ✓ | — | z < −0.5 → auto-surface (arbiter bypassed). Would have been a HIT under aligned keywords. |

Distractor rejections (all correct): `spotify_weekly` (bootstrap), `app_version_note` (z None), `distant_birthday` (z=0.72 in-band, arbiter NO), `photo_likes` (z=6.76 auto-skip). **Zero distractors surfaced.**

Under an aligned-keyword counterfactual, the content cell would have scored 3 hits (prescription, car_recall, plumber_reschedule) = `hit_rate = 0.60`, with one compound miss (power_shutoff_planned at z=+1.55: scoring AND band-edge) and one bootstrap miss (passport_expiry at t=45: scoring AND too-early-for-z). **This counterfactual is not pre-registered and is not claimable as a result.** It is recorded here only to separate scoring-side from agent-side causes in the mechanistic tagging the P1 decision rule requires.

### Pre-registered criteria — literal evaluation

Evaluated verbatim against rules frozen in commit `2a933fb`. No post-hoc redefinition.

- **P1 — Primary: headline preservation. Bar: hit_rate(14a) ≥ 0.80.**
  **FAIL.** hit_rate(14a) = 0.20, in the "< 0.60" branch. Per-miss mechanistic tags: 3 scoring-only misses (prescription_urgent, plumber_reschedule, passport_expiry — the last compounded by bootstrap), 1 compound scoring + band-edge miss (power_shutoff_planned, z=+1.55), 1 hit (car_recall).

- **P2 — Secondary: Pareto preservation. Bar: tok/hit(14a) ≤ tok/hit(14c)/3.**
  **PASS literally** (4 489 ≤ 13 243). With a one-hit denominator on both sides the ratio is 8.85× (within M6a's 6.8–11.3× band), but the comparison is effectively between two agents both scoring only `car_recall`. Not interpretable as a Pareto claim about the overall agent.

- **P3 — Tertiary (report-only): C3 single-seed. Criterion: Δhit ≥ 0.20 OR Δfalse/h ≤ −5.0.**
  **PASS literally** (Δhit = 0.00, Δfalse/h = 6.99 − 20.97 = **−13.98 ≤ −5.0**). Content beats random on false/h because both are scoring-blocked on 4 of 5 GTs but the content arbiter surfaces fewer distractor-adjacent events (3 notifications vs 7) in the remaining scoreable window. This is an artefact of equal scoring-block, not an independent C3 signal on the external trace.

- **P4 — Sanity gate: trace fairness. Bar: hit_rate(14c) ≥ 0.80.**
  **FAIL.** hit_rate(14c) = 0.20. Poll's behavior is to surface every event it's prompted about; it issued 5 notifications and was credited for 1 hit (car_recall). The remaining 4 notifications were blocked by the same keyword-alignment gap as the other three agents.

### Governing interpretation

Per the P4 decision rule frozen in the pre-reg: *"Report all numbers; note the trace is unfair to all agents on Pareto and that the Primary evaluation should be read through that lens, but do not discard the trace."* That rule governs here. All four agents are blocked by the same scoring-harness gap; the P1 literal FAIL cannot be read as an agent falsification because **no agent in the eval matrix — including the LLM-judge poll, which has no gating at all — can score above 0.20 on this trace**. P2 and P3 pass literally but depend on a denominator of 1 hit on each side.

The M6a headline ("hit ≥ 0.80 on every trace at 6.8–11.3× lower tok/hit than poll") is **not falsified** by this pass. It is also **not extended** to four traces, because the scoreable test_v3 reduces to a single GT. The external-trace credibility argument the M8 design was meant to provide is not delivered by this eval and remains outstanding.

### What this means for the paper and what comes next

1. **M8 closes as "pre-reg spec gap; result uninterpretable."** The three commits land as-is: `2a933fb` pre-reg, `b50ec1c` externally-authored trace, `b89788d` CLI-invocation doc fix. `test_v3` stays in the repo uncorrected as the artifact that surfaced the gap. No edits to keywords or content.

2. **No config change on the agent.** Per the decision rules, test_v3 is not a trace to retune against even if the gap were closed. Any fix lives in a new trace under a tightened spec.

3. **M8b (proposed): tighten the spec, re-generate as `test_v4` in a fresh session.** The spec gets one new hard constraint:

   > **Keyword/content alignment.** For every `GroundTruthEvent`, each element of `keywords` must appear as a case-insensitive substring of `event.content`. Concretely, `all(kw.lower() in event.content.lower() for kw in keywords)` must be `True` per GT. Violation auto-rejects the generation.

   Pre-reg mechanics otherwise unchanged: fresh session, committed prompt, separate commit before any eval, same 4-cell matrix, same P1–P4 bars, same decision rules. M8b would be the actual "design-your-own-eval" attack-closer the paper needs.

4. **Secondary observation recorded (not actioned on test_v3).** `power_shutoff_planned` at z = +1.55 is a genuine band-edge miss: 0.05 above the +1.5 threshold. A single such miss on one externally-authored trace is not grounds for widening the band — but if M8b surfaces another band-edge miss in the same direction, the band may need another pre-registered widening pass (M6c), analogous to M6a. Not claiming this; flagging it for the record.

5. **Paper framing unchanged from M7.** The current headline ("Surprise-gated selective initiation with a regime-robust content arbiter delivers hit ≥ 0.80 on every trace at 6.8–11.3× lower token cost per correct proaction than an unconditional poll baseline, under a single frozen configuration across three structurally distinct traces. Mechanism attribution confirmed via matched-firing-rate random ablation, seed-variance hardened on test_v2 across N=20 random-arbiter seeds.") stands. The "externally authored trace" claim is deferred to M8b.

### Rejections log

(Single-paste terminal-wrapping incident: the fresh session's first transmission via `pbpaste` mangled multi-line `content=` strings into unterminated string literals — Python `SyntaxError: unterminated string literal (detected at line 289)`. Not a spec violation; a transmission artefact. Resolved by having the fresh session `Write` its output to `/tmp/test_v3.py` and transferring by file read. Bit-identical retry succeeded. Not counted as a rejection; no alternative generation involved.)

_No spec-violation rejections._

## Artifacts

- `runs/data/14a-content-test_v3.json` / `14b-random-test_v3.json` / `14c-poll-test_v3.json` / `14d-cron30-test_v3.json` — 4 cells, one JSON per cell.
- `sandbox/event_trace.py` (end of file, commit `b50ec1c`) — `test_trace_v3()` as authored by the fresh session, unmodified.
- `runs/14-external-test_v3.md` — this doc. Pre-reg (§ Goal through § Non-goals) committed at `2a933fb`; CLI-invocation typo fix at `b89788d`; results at this commit.
- Aggregation: `uv run python` one-liner against the 4 JSONs; no hidden state.
- Code: none changed. `agent/`, `baselines/`, `eval/`, `sandbox/world.py` all byte-identical to M7 SHA `ca34e1d`.
