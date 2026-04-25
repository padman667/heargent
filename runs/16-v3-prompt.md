# Run 16 — V3 Arbiter Prompt (Principled Criterion) + Externally-Authored Held-Out Trace `test_v5` (M9)

**Date:** 2026-04-25 (pre-registration). Results sections (Commit B regression, Commit D test_v5 eval) appended post-eval.
**Milestone:** M9 — re-architect the arbiter prompt from a closed enumeration of YES regimes (V2, frozen since M5) to a principled AND-gate criterion (*actionable* AND *time-bounded with regret*). Validated in two stages: (B) regression gate against the three co-developed traces under V3 + frozen M7 config; (D) externally-authored `test_v5` under the same M8b three-commit protocol. Run once at each stage. No retuning of V3 against `test_v5` regardless of outcome.
**Pre-registration SHA:** this commit (V3 prompt text + Commit-B regression bars + `test_v5` trace spec + authoring prompt + P1–P4 + decision rules committed together; no code changes and no eval runs before this commit). **Predecessor:** M8b results SHA `ad70d67`.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, predictor seed=42, deterministic throughout. Local-only; no Claude API. Identical to M8b's environment block; any divergence at Commit B is a smoke-test failure.

## Goal

M8b (`test_v4`, runs/15, commit `ad70d67`) falsified the M6a four-trace extension on an externally-authored, spec-compliant trace. Content arbiter hit = 0.40 on `test_v4`; poll / random / cron all reach 1.00; P4 PASSes so no "unfair trace" defense is available. `llm_stats.arbiter_yes_rate = 0.0` — the V2 arbiter said NO to every event it was consulted on (2 correct NOs on distractors, 3 wrong NOs on GTs). All three misses (`parking_meter_oak`, `cover_standup_request`, `protest_commute_route`) tag as **V2-prompt coverage gaps** (urban warnings, colleague social asks, civil-disruption commute alerts); zero band-edge, zero predictor-latch.

V2's closed list of YES regimes (scheduling / personal deliveries / weather alerts / on-call alerts / safety / financial deadlines) is narrower than the GT distribution an external author naturally produces. The three-trace M6a claim stands on `dev_v2` / `test_v1` / `test_v2`; the four-trace extension is withdrawn.

M9 tests one architectural lever: replace V2's closed enumeration with a principled criterion. If the criterion captures the abstract property *"warrants user attention within a bounded time window with regret on miss"*, it should generalize to GT distributions outside V2's example set without requiring re-enumeration — covering both the existing three-trace regimes and the three `test_v4` misses by the same principle. Prompt is the **sole** lever in M9; band, surprise scorer, predictor, seed, model, baselines all stay frozen at the M7 state.

## Thesis

> Moving the arbiter from a closed YES-enumeration prompt (V2) to a principled AND-gate criterion (V3: *actionable* AND *time-bounded with regret*) restores hit ≥ 0.80 on an externally-authored trace (`test_v5`) while preserving the M6a single-config no-regression hit-rate floor on the three co-developed traces, at modest false-init cost (≤ +5/h tolerance per trace).

If the principled criterion fails on `test_v5`, the honest finding is that the 3B arbiter at this model scale cannot close the external-trace gap under a principled prompt either; M10 (Claude-API arbiter) becomes the next architectural lever, with V3 framed as the 3B prompt-architecture ceiling.

## V3 prompt (FROZEN — pre-registered verbatim text)

The block below is the exact textual artifact frozen by this commit. Any semantic edit before Commit B invalidates the pre-registration; minor formatting normalization required to land it as a Python string literal in `agent/arbiter.py` (whitespace, line breaks for source readability, escaping) is permitted as long as the rendered prompt the model receives is byte-identical.

```
You judge whether a single notification warrants proactive surfacing to a user.

Surface (YES) if the content meets BOTH of these conditions:
1. Actionable — the content implies a decision, response, or adjustment the user could make.
2. Time-bounded with regret — ignoring it for the next few hours could cost the user something they would notice (money, missed obligation, missed opportunity, safety).

Do NOT surface (NO) if the content is routine status (service heartbeats, all-clear pings, uptime reports), social / ambient (app promotions, reaction notifications, friend activity, newsletters, subscription billing notices), or purely informational with nothing the user must decide or act on within hours.

Output exactly one token: YES or NO.

Content: {content}

YES or NO:
```

### Design rationale (frozen with the text)

- **AND-gate on *actionable* + *time-bounded with regret*.** Rules out chronic / open-ended content (actionable but no deadline → newsletters, generic ambient social) and instant-regret noise the user can't act on (unactionable system alerts). Both conjuncts must hold; either alone is insufficient for YES.
- **"Next few hours"** as the time anchor. Tuned to match the trace duration envelope (≤1000 s sim-time, framed as a few real hours of an ambient-assistant session). Avoids both "any deadline ever" (too loose) and "imminent minute" (too tight — would strict-read out package deliveries and tomorrow-shaped colleague asks). Reading is "the next few hours of decision/response window matter," not "must complete the action within the next few hours" — the prompt is judged on whether the 3B picks the looser, more useful reading.
- **Explicit NO bucket** with three named classes (routine status, social/ambient, purely informational). V2's NO was the implicit complement of YES; the 3B evidently could not reliably resolve out-of-enumeration content into NO without an explicit "else" target. The three NO classes named here are the dominant distractor classes across `dev_v2`, `test_v1`, `test_v2`, and `test_v4`'s observed distractors (`linkedin_connections`, `github_repo_star`, `designgrid_renewal`, `calendar_feature_tip`).
- **"Output exactly one token: YES or NO."** Token contract: parser is `re.compile(r"\b(YES|NO)\b")` matched against `first_line.upper()` in `agent/arbiter.py:58, 102`; this contract is bit-compatible with V2's parsing path (V2 said "Output exactly YES or NO, uppercase, on a single line"). No parser changes in Commit B.

### Implementation note for Commit B

`ContentArbiter.__init__` currently takes `system_prompt: str = ARBITER_SYSTEM_PROMPT_V2` and the wire-up is `client.chat(system=self.system_prompt, user=text, …)` (`agent/arbiter.py:77, 92–100`). The V3 text above is a single-string completion-style template containing a `{content}` placeholder. Commit B's wire-up choice is implementation, not pre-registered: either (a) drop the trailing `Content: {content}\n\nYES or NO:` block, keep the rules + criterion + NO bucket + token-contract sentence as the system prompt, and let the existing `system=…, user=text` chat-template wire-up provide the content turn (V2 wire-up parity); or (b) keep V3 as a single template and pass `system=ARBITER_SYSTEM_PROMPT_V3.format(content=text), user=…` with a minimal user payload. Either is consistent with "V3 verbatim" because the *semantic content the model is conditioned on* (rules + criterion + NO bucket + token contract + the event content) is identical; the wire-up only changes how the chat template segments it. Commit B will pick (a) for minimal code delta and explicit wire-up parity with V2, and that choice is recorded in the Commit B results section below. If (a) does not pass the regression gate and (b) does on the same V3 text, that's reported honestly as a wire-up sensitivity finding, not a V3 failure.

Why (a) is the right default beyond minimal code delta: (a) preserves V2's chat-template segmentation byte-for-byte (system = rules; user = event content), so any V2 → V3 delta in cell metrics attributes cleanly to the prompt-architecture change (closed YES enumeration → principled AND-gate criterion + explicit NO bucket). Under (b), `.format(content=text)` inlines the event content inside the system message; combined with the chat-template's user-turn injection this either shows the content to the model twice (once inlined in system, once as a user turn) or shifts the system-vs-user role boundary V2 was never tested under. Either confound mixes "V3's principled criterion changed cell metrics" with "V3's wire-up shape changed cell metrics." Choosing (a) by default keeps V3 a clean prompt-architecture lever rather than a prompt-architecture-plus-wire-up lever.

## Four-commit protocol

| Commit | Content | Gates |
|---|---|---|
| **A** | This pre-reg doc (V3 prompt text + Commit-B regression bars + `test_v5` spec + authoring prompt + P1–P4 + decision rules). No code. | — |
| **B** | Replace `ARBITER_SYSTEM_PROMPT_V2` with `ARBITER_SYSTEM_PROMPT_V3` as the default in `ContentArbiter`. Run three co-developed traces under V3 + frozen config + content arbiter. | Regression gate: all three traces must clear bars (below) before any test_v5 work. |
| **C** | Externally-authored `test_v5` (fresh Claude Code session, /clear, paste authoring prompt verbatim, audit, paste into `sandbox/event_trace.py`, register). | Audit: 11 hard structural constraints + 3 banned lists. Reject + log on any violation; no prompt edits. |
| **D** | 4-cell matrix on `test_v5` under V3 + frozen config. Score P1–P4. | Verbatim evaluation against frozen rules. |

If Commit B's regression gate fails on any trace, halt: redesign V3 against the three co-developed traces only (legitimate continuation of M5/M6a iteration, since these traces were already part of V2's tuning loop), re-freeze V3 text in this doc as a versioned amendment with a new SHA, re-run gate. **Do not begin Commit C until the gate passes.** This serializes the architectural and external-trace concerns: the architectural lever (prompt) is validated in-distribution before being subjected to the external-trace test.

## Commit B regression gate (frozen bars)

Files: `runs/data/16b-content-dev_v2.json`, `runs/data/16b-content-test_v1.json`, `runs/data/16b-content-test_v2.json` — three content cells under `HeargentZAWide`, V3 prompt, frozen config.

| trace | M6a hit (V2) | M6a false/h (V2) | V3 bar (hit) | V3 bar (false/h) |
|---|---:|---:|---|---|
| `dev_v2` | 1.00 | 0.00 | ≥ **1.00** (no-regression) | ≤ **5.0** |
| `test_v1` | 0.80 | 3.67 | ≥ **0.80** (no-regression) | ≤ **8.67** (= 3.67 + 5.0) |
| `test_v2` | 1.00 | 0.00 | ≥ **1.00** (no-regression) | ≤ **5.0** |

**Hit bars are flat against M6a — V3 is required not to regress on recall in-distribution.** No-regression on hit is non-negotiable: V3's claim is "broader criterion that still covers the V2-co-developed regimes." A hit-rate regression on any of the three would falsify that.

**+5/h symmetric tolerance on `false_initiation_rate_per_hour`** is pre-registered as the anticipated cost of broadening the criterion. Anchoring:
1. Pre-registered in this commit, not curve-fit after observing V3 numbers.
2. Below random's empirical firing rate (~14/h on these traces in M7 with `--arbiter-random-p 0.75`). 5/h preserves "content beats matched-firing-rate random on false/h" by a meaningful margin if V3 holds — the C3 single-seed claim retains in-distribution support.
3. Symmetric across traces. No bar-level per-trace tuning.
4. Encodes the M9 trade explicitly as a budget: V3 may cost up to ~5 extra unhelpful surfaces / hour in-distribution per trace in exchange for closing the external coverage gap on `test_v5`.

**Decision rules for Commit B (frozen, no post-hoc redefinition):**

- **All three pass.** V3 prompt text is frozen as `ARBITER_SYSTEM_PROMPT_V3`. Commit B SHA + the three JSONs (`16b-content-{dev_v2,test_v1,test_v2}.json`) + the wire-up choice (a or b above) are recorded in this doc's Commit B results section before Commit C is opened.
- **Any one trace fails the hit bar.** Halt. V3 does not preserve in-distribution recall under a principled-criterion redesign on the lossy trace. Redesign V3 against the three co-developed traces, re-freeze, re-run gate. Up to two redesign rounds permitted; a third failure means the principled-criterion thesis is falsified at the 3B model scale and M9 closes here without test_v5.
- **All three pass hit but one or more fails the false/h bar.** Halt. V3's broader criterion costs more than the +5/h pre-reg envelope on at least one trace. Same redesign discipline as hit-bar failure.
- **All three pass hit and false/h but `dev_v2` content false/h > 0.00.** Pass — pre-reg explicitly anticipates this (V3 is broader; dev_v2's 0.00 floor under V2 is allowed to soften within the +5/h envelope). The C3 claim is re-evaluated on `test_v2` at Commit D, not on `dev_v2`.

**Why redesign-on-failure is not in-distribution overfitting.** V3 is a *form change* (closed enumeration of YES regimes → principled AND-gate criterion + explicit NO bucket), not a text edit of V2 within the same form. Iterating V3's text on Commit B failure to maintain in-distribution recall — staying within the principled-criterion form, never reverting to enumeration of regimes — is within-form tuning, structurally the same kind of co-developed-trace iteration M5 → M6a did within the closed-enumeration form (NO-bucket re-wording, additional YES categories covering known regimes, band-edge adjustments at M6a). The M9 thesis is whether the *form change* generalizes to externally-authored content; whatever V3 text emerges from Commit B is subject to the test_v5 P1–P4 bars verbatim, with the externally-authored trace untouched by the iteration. The 2-round cap means a third in-distribution failure exhausts the within-form tuning budget — the form change is judged unable to preserve V2's three-trace recall under any short principled-criterion phrasing the 3B can resolve, and M9 closes here without test_v5 with the principled-criterion thesis falsified at the 3B scale. This framing distinguishes M9's iteration discipline from the "design-your-own-eval" attack surface: the held-out test (test_v5) is generated by a fresh session against this commit's authoring prompt regardless of how many redesign rounds Commit B takes, so V3 cannot leak into test_v5 via the in-distribution iteration.

## Pre-registered artifacts for `test_v5` (frozen before any generation)

### Frozen trace spec (extends M8b)

Hard constraints — any violation auto-rejects the generation. **Identical to M8b's spec** (runs/15 §"Frozen trace spec") except `name = "test_v5"` and the banned lists below.

- `name = "test_v5"`.
- Exactly **5 `GroundTruthEvent`s** and exactly **4 distractor `Event`s** (total 9 events in `events`).
- All `sim_time` values in `[0, 1000]`. `max(gt.event.sim_time + gt.proaction_window_s) ≤ 1000`.
- At least **3 distinct `kind` values** across the 5 GTs, chosen from {`email`, `calendar_update`, `notification`, `alert`, `phone_message`, `world_event`}.
- At least one GT with `proaction_window_s ≤ 30`.
- At least one GT with `proaction_window_s ≥ 300`.
- **Keyword/content alignment** (M8b constraint, retained verbatim). For every `GroundTruthEvent gt`, every string `kw` in `gt.keywords` must satisfy `kw.lower() in gt.event.content.lower()`. Check is purely substring-based — if the keyword's characters don't literally appear in the content, it fails.
- Briefing: 2–4 first-person sentences describing the day's setting.
- Intents: tuple of exactly 5 short phrases.
- Distractors are plausible routine / system noise (no abrupt urgency, no action demand).
- GTs are human-interpretable as "warrants proaction" on content alone (no briefing required to judge).

**Banned event ids** — 46 = 37 from M8b (union of `dev_v1`, `dev_v2`, `test_v1`, `test_v2`, `test_v3`) + 9 from `test_v4` (5 GTs + 4 distractors).

```
flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel,
fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat,
package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup,
slack_invite, calendar_advert, promo_email, system_status,
fire_kitchen, board_meeting, water_burst, er_call, security_breach,
daily_briefing, status_ok, uptime_ping, newsletter,
passport_expiry, prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule,
spotify_weekly, app_version_note, distant_birthday, photo_likes,
parking_meter_oak, cover_standup_request, gym_class_cancelled, library_hold_expiring, protest_commute_route,
linkedin_connections, github_repo_star, designgrid_renewal, calendar_feature_tip
```

**Banned content themes** — 27 = 22 from M8b + 5 from `test_v4`.

fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor callback, production / server outage, rent due, school pickup, quarterly report, board meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert, marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned building electrical / power shutoff, plumber or appliance-install reschedule, parking meter expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or fitness class cancellation for facility maintenance, library hold expiring today, protest or civil disruption affecting commute.

**Banned keyword tuples** — 26 = 21 from M8b + 5 from `test_v4` (the M8b list was 2-tuples; `test_v4` introduced 3-tuples, so the M9 list is "tuples" not "pairs"). Avoid reusing any tuple as a GT's `keywords` field.

```
(flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly),
(dentist, cancelled), (fire, alarm), (package, delivered), (doctor, call),
(production, alert), (rent, due), (school, pick up), (fire, kitchen),
(board, meeting), (water, burst), (hospital, mother), (security, unauthorized),
(passport, expiring), (prescription, refill), (recall, airbag),
(power, shutoff), (plumber, reschedule),
(parking, meter, expires), (standup, vacation), (gym, maintenance),
(library, hold, expires), (protest, market street)
```

### Authoring prompt (verbatim — pasted unmodified into the fresh Claude Code session at Commit C)

The block below is the exact text the fresh session receives as its first user message. Any edit to this prompt before or during Commit C invalidates the protocol and the trace must be re-generated from scratch. **Identical structure to M8b's prompt** with three substitutions: `test_v4` → `test_v5` in name and function; banned-id list extended to 46; banned-themes list extended to 27; banned-keyword-tuple list extended to 26.

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
> - `name = "test_v5"`.
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
> `flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert, promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call, security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry, prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule, spotify_weekly, app_version_note, distant_birthday, photo_likes, parking_meter_oak, cover_standup_request, gym_class_cancelled, library_hold_expiring, protest_commute_route, linkedin_connections, github_repo_star, designgrid_renewal, calendar_feature_tip`.
>
> **Banned content themes** (semantic, not just string match):
> fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor callback, production / server outage, rent due, school pickup, quarterly report, board meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert, marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned building electrical / power shutoff, plumber or appliance-install reschedule, parking meter expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or fitness class cancellation for facility maintenance, library hold expiring today, protest or civil disruption affecting commute.
>
> **Banned keyword tuples** (avoid reusing any tuple as a GT's `keywords` field):
> `(flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert), (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), (hospital, mother), (security, unauthorized), (passport, expiring), (prescription, refill), (recall, airbag), (power, shutoff), (plumber, reschedule), (parking, meter, expires), (standup, vacation), (gym, maintenance), (library, hold, expires), (protest, market street)`.
>
> **Output**: one Python function `def test_trace_v5() -> Trace:` in the style of the template, followed by a single line adding `"test_v5": test_trace_v5` to the `get_trace` registry. Return the code in a single fenced Python block. Do not explain.

### Authoring protocol (Commit C)

1. Open a new Claude Code window, `/clear` to ensure empty history.
2. Paste the prompt block above verbatim as the first user message. No additions, no CLAUDE.md context carried in, no reading of any project file beyond what the prompt contains.
3. Fresh session outputs a single fenced Python block containing `def test_trace_v5() -> Trace:` and the registry line.
4. Audit the output against the 11 hard structural constraints (including the keyword/content alignment constraint) and 3 banned lists. If any violation is found, **reject the generation, log the violation in this doc's Rejections sub-section below, and open another fresh session.** No prompt edits.
5. If the output passes audit, copy it verbatim into `sandbox/event_trace.py` (end of file) and add the registry line. The only permitted edits are: import ordering, typo fixes that block parsing, and the registry line itself. Any change to event `id`, `kind`, `sim_time`, `content`, `proaction_window_s`, `keywords`, `briefing`, or `intents` invalidates the protocol.
6. Commit as "M9: externally-authored test_v5 (fresh session, <timestamp>)".

### Rejections log

(Populated during Commit C. Each rejection notes: fresh-session timestamp, first violated constraint, one-sentence description of the violation. A rejected generation is not merged; the generator code is not kept.)

_None yet._

### Pre-registered success criteria for `test_v5` (frozen before any generation or eval run)

Let `16d-a = runs/data/16d-content-test_v5.json` (HeargentZAWide, content arbiter, V3, frozen config), `16d-b = runs/data/16d-random-test_v5.json` (p=0.75, seed=42), `16d-c = runs/data/16d-poll-test_v5.json` (react_poll_local), `16d-d = runs/data/16d-cron30-test_v5.json` (CronKeyword30s).

**P1 — Primary: external-trace headline.** `hit_rate(16d-a) ≥ 0.80`. This is M9's main claim; passing on `test_v5` re-establishes "hit ≥ 0.80 on every co-developed trace AND one externally-authored trace" under V3. M8b's V2 result on `test_v4` was 0.40; the V3 redesign is judged against this bar at Commit D.

**P2 — Secondary: Pareto preservation.** `tok_per_hit(16d-a) ≤ tok_per_hit(16d-c) / 3`. Content cell at least 3× cheaper per hit than poll on the same trace. M6a's range was 6.8–11.3×; 3× is a conservative floor.

**P3 — Tertiary: C3 single-seed (report-only).** With content reference 16d-a and random cell 16d-b: either `hit_rate(16d-a) − hit_rate(16d-b) ≥ 0.20` OR `false_initiation_rate_per_hour(16d-a) − false_initiation_rate_per_hour(16d-b) ≤ −5.0`. **Report-only.** A single seed is not a robust claim; this criterion is recorded verbatim either way and does not gate paper framing.

**P4 — Sanity gate: trace fairness.** `hit_rate(16d-c) ≥ 0.80`. If poll itself falls below 0.80, the trace is too hard or ambiguous for all agents — all numbers are reported but the primary verdict is read through that lens.

### Decision rules for `test_v5` (frozen; no post-hoc redefinition)

- **P1 PASS.** Headline re-established under V3: *"Single frozen configuration with V3 principled-criterion arbiter delivers hit ≥ 0.80 on every co-developed trace AND one externally-authored trace."* V3 becomes the production prompt. `runs/README.md` headline updates to reflect the four-trace V3 result. M6a's V2 three-trace claim is preserved as the predecessor result; the four-trace claim is now V3-conditioned.
- **P1 `0.60 ≤ hit < 0.80`.** Headline partially re-established. Report mechanistically: tag each miss as band-edge / predictor-latch / V3-prompt gap (residual coverage gap of the principled criterion) / wire-up sensitivity / something new. No retune of V3 against `test_v5`. Optional follow-up: M10 (Claude-API arbiter) if residual tags as model-scale-limited rather than prompt-architecture-limited; honest reading is "V3 partially closes the external-trace gap at the 3B scale."
- **P1 `hit < 0.60`.** V3 principled criterion also fails externally. Honest finding: at the 3B model scale, the principled-criterion redesign does not close the external-trace coverage gap that the closed-enumeration prompt failed on. M10 (Claude-API arbiter) is the next architectural lever; V3 is recorded as the 3B prompt-architecture ceiling. No retune of V3 against `test_v5`.
- **P2 FAIL.** Pareto claim softens to *"cheaper than poll, but the magnitude varies by trace."* Report verbatim tok/hit numbers. Does not change the P1 verdict.
- **P3 PASS or FAIL.** Reported either way. A single-seed FAIL on `test_v5` is not grounds for discarding C3; a 20-seed sweep on `test_v5` (drop-in under the existing `--arbiter-random-seed` wiring) is the clean follow-up if reviewers push for seed-robustness on the external trace under V3 too.
- **P4 FAIL.** Report all four cells' numbers and note the trace is unfair to all agents on Pareto; the primary verdict on P1 still stands. The trace is kept — an unfair trace does not retroactively become a "design-your-own-eval" attack defense, but it also does not get discarded because the agent happened to do badly on it. M8b's `test_v4` cleared P4 (poll = 1.00); if `test_v5` does not, that itself is data on how well the M8b-tightened spec generalizes to a third externally-authored generation.

**Protocol-failure rule (M9-specific).** If `test_v5` surfaces a third novel failure class distinct from M8's keyword/content scoring gap and M8b's V2-coverage gap (e.g., the principled criterion misfires on a structurally distinct cohort the prompt does not anticipate), iterate the spec further (`test_v6`) rather than retune V3. Protocol converges; agent does not chase trace-specific residuals.

No raising of cell count, no seed substitution on P3, no post-hoc bar redefinition, no trace regeneration in response to eval outcome.

### Pre-registered paper framing per outcome

Drafted at pre-registration to lock the publishable headline for each branch of the joint Commit B + test_v5 P1 outcome. No post-hoc paragraph editing in response to the actual numbers. Each row restates the decision-rule consequences encoded in the sections above as the publishable headline; pre-registering the paper line forecloses the most common review attack on agent papers — that the framing was chosen post-hoc to flatter the result.

| Commit B | test_v5 P1 | Paper framing |
|---|---|---|
| Pass | hit ≥ 0.80 | *Single frozen configuration with V3 principled-criterion arbiter delivers hit ≥ 0.80 on every co-developed trace AND one externally-authored trace, at modest false-init cost (≤ +5/h per trace vs M6a). The M8b external-authoring protocol is now load-bearing in the positive direction: the principled-criterion redesign motivated by M8b's V2-coverage gap is validated under the same protocol that surfaced the gap.* |
| Pass | 0.60 ≤ hit < 0.80 | *V3 preserves V2's in-distribution recall and partially closes the external-trace gap (hit > V2's 0.40 on test_v4, < the 0.80 bar on test_v5). Honest reading: principled-criterion redesign is a partial fix at the 3B scale; per-miss tags determine whether residuals are model-scale-limited (M10 Claude-API arbiter is the next lever) or prompt-architecture-limited (V3 itself has residual coverage gaps within the principled form).* |
| Pass | hit < 0.60 | *V3 preserves V2's in-distribution recall but does not close the external-trace gap at the 3B scale. The principled-criterion redesign is not the load-bearing lever for external generalization at this model scale; M10 Claude-API arbiter is the next architectural lever, with V3 framed as the 3B prompt-architecture ceiling. M6a's V2 three-trace claim and M8b's external-trace falsification both stand unchanged.* |
| Fail (after 2 redesigns) | n/a | *The principled-criterion form does not preserve V2's three-trace recall at the 3B scale under any short phrasing the 3B can resolve in 2 within-form redesign rounds. M6a's V2 closed-enumeration prompt is itself load-bearing for the three-trace claim — it cannot be replaced by a principled-form prompt without recall loss at 3B. M10 (Claude-API arbiter) is the next lever; M9 closes without test_v5. M6a's V2 three-trace claim and M8b's external-trace falsification both stand unchanged.* |

## Architecture changes

**One** code change in M9, scoped to Commit B: replace `ARBITER_SYSTEM_PROMPT_V2` with `ARBITER_SYSTEM_PROMPT_V3` as the default `system_prompt` argument in `ContentArbiter.__init__` (`agent/arbiter.py:77`), and add the V3 text as a new module-level constant. V2 stays in the source as a named constant for reproducibility (so re-running the M6a / M7 / M8b cells against pre-M9 state is one parameter override away). No changes to `agent/loop.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/llm.py`, `eval/run_trace.py`, any baseline, or `sandbox/`. The `--arbiter-random-seed` CLI flag, `HeargentZAWide`, the band `[−0.5, +1.5]`, predictor / surprise / model choice all stay frozen at the M7 state.

Commit B's regression-gate JSONs (`runs/data/16b-content-{dev_v2,test_v1,test_v2}.json`) replace M6a's content cells as the in-distribution V3 baseline; M6a's `runs/data/12*` JSONs are not regenerated and stay as the V2 reference for any V2-vs-V3 comparison the paper needs.

## Critical files

- `agent/arbiter.py` — Commit B edit point. New constant `ARBITER_SYSTEM_PROMPT_V3` (verbatim text from §"V3 prompt" above, normalized to a Python string literal), `ContentArbiter.__init__` default flips from `ARBITER_SYSTEM_PROMPT_V2` to `ARBITER_SYSTEM_PROMPT_V3`. **Sole code change in M9.**
- `sandbox/event_trace.py` — Commit C appends `def test_trace_v5() -> Trace:` and adds `"test_v5": test_trace_v5` to the `get_trace` registry. `test_trace_v1/v2/v3/v4` and existing registry entries **not touched**.
- `runs/16-v3-prompt.md` — this doc. Pre-reg (this commit). Commit B results appended after regression gate. Commit D results appended after `test_v5` eval.
- `runs/README.md` — row 16 added post-Commit-D. Headline updates only on P1 PASS.
- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `eval/run_trace.py`, all files under `baselines/`, `sandbox/world.py`, existing `test_trace_v1/v2/v3/v4` — **not touched.**

## Reproduce

### Pre-Commit-B sanity check

```sh
# Confirm V2 baseline is bit-identical to runs/data/12a-heargent-za-v2wide-dev_v2.json under
# the unchanged tree (no V3 in play yet). One-cell smoke against M6a reference.
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode content --out /tmp/smoke-pre-B.json
# Compare hit_rate, false_initiation_rate_per_hour, total_notifications, misses
# against runs/data/12a-heargent-za-v2wide-dev_v2.json — must match exactly.
```

### Commit B — regression gate (after V3 swap lands in agent/arbiter.py)

```sh
# 16b dev_v2 — V3, content arbiter
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace dev_v2 \
  --arbiter-mode content \
  --out runs/data/16b-content-dev_v2.json

# 16b test_v1 — V3, content arbiter
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v1 \
  --arbiter-mode content \
  --out runs/data/16b-content-test_v1.json

# 16b test_v2 — V3, content arbiter
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v2 \
  --arbiter-mode content \
  --out runs/data/16b-content-test_v2.json
```

Score against the regression gate bars (above). All three must pass before Commit C is opened.

### Pre-Commit-D sanity checks (after `test_v5` lands at Commit C)

```sh
# Schema & structural constraint check at datastructure level
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v5'); \
  print(len(t.ground_truth), len(t.events), round(t.duration_s, 1))"
# Must print: 5 9 <value ≤ ~1030>

# Keyword/content alignment audit (M8b constraint, retained)
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v5'); \
  [print(gt.event.id, kw, kw.lower() in gt.event.content.lower()) \
   for gt in t.ground_truth for kw in gt.keywords]"
# Every line must end in True. Any False → reject the generation, log in Rejections, open new fresh session.

# Bit-identical re-run of one Commit-B content cell to confirm no environmental drift
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode content --out /tmp/smoke-pre-D.json
# Compare hit_rate, false_initiation_rate_per_hour, total_notifications, misses
# against runs/data/16b-content-dev_v2.json — must match exactly.
```

### Commit D — `test_v5` eval matrix (after Commit C lands a compliant `test_v5` and pre-Commit-D smokes pass)

```sh
# 16d-a — content arbiter (primary)
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v5 \
  --arbiter-mode content \
  --out runs/data/16d-content-test_v5.json

# 16d-b — matched-firing-rate random arbiter (tertiary; single seed, report-only)
uv run python -m eval.run_trace \
  --agent agent.loop:HeargentZAWide \
  --trace test_v5 \
  --arbiter-mode random \
  --arbiter-random-p 0.75 \
  --arbiter-random-seed 42 \
  --out runs/data/16d-random-test_v5.json

# 16d-c — poll (sanity ceiling + Pareto denominator)
uv run python -m eval.run_trace \
  --agent baselines.react_poll_local:ReactPollLocal \
  --trace test_v5 \
  --out runs/data/16d-poll-test_v5.json

# 16d-d — cron 30 s (structural baseline)
uv run python -m eval.run_trace \
  --agent baselines.react_cron_keyword:CronKeyword30s \
  --trace test_v5 \
  --out runs/data/16d-cron30-test_v5.json
```

## Non-goals for this pass

- Do not touch the band `[−0.5, +1.5]`, surprise scorer, predictor, model choice, seeds, or any baseline. **V3 prompt is the sole architectural lever in M9.**
- Do not iterate V3 against `test_v5` under any outcome. Iteration is permitted only against the three co-developed traces at Commit B (legitimate continuation of M5/M6a tuning).
- Do not fold the Claude-API arbiter (M10 concept) into M9. Orthogonal architectural lever; muddling prompt-architecture and model-scale in one experiment loses attribution.
- Do not revisit the `z < −0.5` auto-surface false-init leakage observed on `test_v4` (`designgrid_renewal`, `calendar_feature_tip`). That is a band-lower-edge lever, not a prompt lever. V3 only fires through the arbiter; the auto-surface path bypasses V3 by design (runs/15 §5).
- Do not reopen `test_v3` or `test_v4`. Both stay uncorrected as the artifacts that surfaced their respective failure modes.
- Do not regenerate the V2 cells (`runs/data/12*`). V2 stays as the predecessor reference; M9's claims are V3-conditioned.
- Do not vary the arbiter seed beyond `42` on `test_v5`. N=20 seed sweep on `test_v5` is a future pass, not M9.
- Do not edit the V3 prompt text once Commit B passes the regression gate. Any change after that point requires a new pre-reg doc and a new run number.
- Do not edit the authoring prompt for `test_v5` once this commit lands. A prompt change requires re-committing this doc and restarting the protocol.
- Do not edit the generated `test_trace_v5()` beyond the permitted syntactic edits. Any semantic edit invalidates the external-authoring claim.
- Do not regenerate `test_v5` in response to unfavourable eval results. A trace that fails the primary under a compliant generation is reported honestly; retuning happens on a NEW trace if at all.

This pass is strictly narrower than M7 (no new CLI flag, no random-arbiter wiring change) and comparable in code-delta scope to M8b (one constant added, one default flipped, one trace function appended; no harness or baseline edits).

## Results — Commit B regression gate

### Pre-flight bit-identical smoke (before V3 swap)

Re-ran `uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace dev_v2 --arbiter-mode content --out /tmp/smoke-pre-B.json` under the unchanged tree (post-`e66afc1`, pre-V3-swap) and diffed against `runs/data/12a-heargent-za-v2wide-dev_v2.json`. **Bit-identical** on `hit_rate` (1.00), `false_initiation_rate_per_hour` (0.00), `total_notifications` (5), `misses` ([]), hits list (`fire_alarm, flight_delay, meeting_moved, deadline, dentist_cancel`), `llm_stats.arbiter_calls` (4), `llm_stats.arbiter_yes_rate` (0.75). Environment matches M6a / M7 / M8b state; any V3 regression is the V3 prompt's effect, not environmental drift.

### V3 implementation: code state

Wire-up choice **(a)** used per §"Implementation note for Commit B." `ARBITER_SYSTEM_PROMPT_V3` added as a new module-level constant in `agent/arbiter.py`; the system-prompt body is byte-identical to Commit A's frozen V3 text up through "Output exactly one token: YES or NO." (verified at runtime via Python equality against the pre-reg text — 751 chars). The trailing `Content: {content}\n\nYES or NO:` block from the pre-reg text is dropped; content reaches the model via the chat-template user turn exactly as it does under V2 (`client.chat(system=..., user=text)`), preserving V2's chat-template segmentation byte-for-byte. `ContentArbiter.__init__` default flipped from `ARBITER_SYSTEM_PROMPT_V2` to `ARBITER_SYSTEM_PROMPT_V3` for the regression cells. No other code change.

### Three regression cells — V3 vs M6a V2 baseline

| trace | V2 hit | V3 hit | V2 false/h | V3 false/h | V2 tok/hit | V3 tok/hit | V2 arb_calls | V3 arb_calls | V2 arb_yes | V3 arb_yes | V3 misses |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `dev_v2`  | 1.00 | **0.40** | 0.00 | 0.00 | 682  | 1 472 | 4 | 4 | 0.75 | **0.00** | fire_alarm, flight_delay, meeting_moved |
| `test_v1` | 0.80 | **0.20** | 3.67 | 3.67 | 1 112 | 3 512 | 8 | 8 | 0.50 | **0.12** | package_arrival, doctor_callback, server_outage, kid_school_pickup |
| `test_v2` | 1.00 | **0.60** | 0.00 | 0.00 | 814  | 1 083 | 7 | 7 | 0.43 | **0.14** | fire_kitchen, er_call |

`arbiter_calls` is invariant V2 → V3 (the bootstrap policy and band routing didn't change); only the per-call YES/NO decision shifts under V3.

### Gate verdict per pre-reg

| trace | hit bar | hit | hit pass | false/h bar | false/h | false/h pass | overall |
|---|---|---:|:---:|---|---:|:---:|:---:|
| `dev_v2`  | ≥ 1.00 | 0.40 | **FAIL** | ≤ 5.00 | 0.00 | PASS | **FAIL** |
| `test_v1` | ≥ 0.80 | 0.20 | **FAIL** | ≤ 8.67 | 3.67 | PASS | **FAIL** |
| `test_v2` | ≥ 1.00 | 0.60 | **FAIL** | ≤ 5.00 | 0.00 | PASS | **FAIL** |

Hit-bar FAIL on all three traces. False/h-bar PASS on all three because V3 is too NO-biased to leak distractors through the arbiter — false-init structure on `dev_v2` and `test_v2` is unchanged (0.00; the only false-init paths are auto-surface, both unchanged from V2), and `test_v1`'s 3.67/h matches V2 exactly (the leaked distractor is `system_status` via `z < −0.5` auto-surface, not via arbiter YES). Per-trace overall FAIL; gate FAIL.

### Hit-source breakdown

The few V3 hits across the three traces decompose as:

| trace | V3 n_hits | via arbiter YES | via z<−0.5 auto-surface | events |
|---|---:|---:|---:|---|
| `dev_v2`  | 2 | 0 | 2 | auto-surf: deadline, dentist_cancel |
| `test_v1` | 1 | 1 | 0 | arb-YES: rent_due |
| `test_v2` | 3 | 1 | 2 | arb-YES: security_breach; auto-surf: board_meeting, water_burst |

**Total arbiter-YES hits across all three traces: 2** (rent_due, security_breach). Both events whose content includes a word that appears verbatim in V3's regret-list examples ("money" / "safety"). Every other arbiter consultation under V3 resolved NO. Arbiter contribution to overall V3 hits is essentially nil; the cells' hit numbers come almost entirely from the unchanged `z < −0.5` auto-surface branch (which bypasses the arbiter by design).

### Off-harness diagnostic probe (wire-up sanity check)

Direct V3-vs-V2 probe on 8 representative events through the same `OllamaClient` instance, single Python session, no harness:

| event | V3 | V2 |
|---|:---:|:---:|
| `fire_alarm` ("Fire alarm in building A triggered; evacuation in progress.") | NO | YES |
| `flight_delay` ("Flight UA123 to Berlin tomorrow has been delayed by 3 hours…") | NO | YES |
| `meeting_moved` ("Meeting 'Design Review' tomorrow moved from 10:00 to 14:00.") | NO | YES |
| `news_digest` ("Daily news digest updated.") | NO | NO |
| `rent_due` ("Reminder: rent payment of $1450 is due tomorrow.") | YES | YES |
| `package_arrival` ("Your package has been delivered to your door.") | NO | NO |
| `parking_meter_oak` (test_v4 GT, urban warning) | NO | NO |
| `cover_standup_request` (test_v4 GT, colleague ask) | NO | NO |

V2 cleanly fires YES on `fire_alarm` / `flight_delay` / `meeting_moved` on the same client where V3 says NO. **Wire-up is sound; V3's NO-bias is the prompt itself.** V3 also does not rescue `parking_meter_oak` or `cover_standup_request` (the test_v4 V2-coverage misses V3 was specifically designed to address), so on the off-harness probe V3 is empirically *worse* than V2 on the in-distribution traces and *no better* than V2 on the test_v4 misses that motivated the redesign.

### Mechanistic interpretation

The 3B (qwen2.5:3b-instruct) over-strict-reads V3's abstract AND-gate. Three failure modes observed, all consistent with pattern-matching rather than abstract-conjunct resolution:

1. **Safety content read as informational, not actionable.** `fire_alarm` ("Fire alarm in building A triggered; evacuation in progress.") → NO. The 3B does not recognize "evacuation in progress" as user-actionable in V3's abstract framing. Under V2's enumerated "urgent safety or security issue" category, the same content cleanly fires YES — the 3B locks onto the named pattern.

2. **Strict-reading of "next few hours" excludes tomorrow-shaped scheduling.** `flight_delay` and `meeting_moved` (both "tomorrow") → NO. This is the exact failure mode flagged in chat at Commit A review and waved off on the plan author's design rationale ("'next few hours' avoids 'imminent minute (too tight — misses packages, colleague asks)'"). Empirical 3B behavior at this phrasing strict-reads the time anchor as "literally within the next few clock hours," not as "the relevant decision window before action becomes too late."

3. **NO-bias absent enumeration patterns; pattern-matching on regret-list examples.** When content does not match a regret-list example word, the 3B defaults to NO. The two arbiter-YESs across all three traces both match a regret-list example word verbatim: `rent_due` matches "money," `security_breach` matches "safety." The 3B treats the regret-list more like a closed enumeration of YES-trigger words than as a criterion guide.

The principled-criterion form, at this phrasing, fails to give the 3B usable patterns for resolving content the V2 enumeration handles cleanly. V3's NO-bias is structural across safety, scheduling, urban warnings, and colleague asks — and notably does not rescue test_v4's V2-coverage misses (off-harness probe confirms `parking_meter_oak` and `cover_standup_request` both → NO under V3).

### Decision per pre-reg: scientifically-conservative path-C close

The pre-reg permitted up to 2 within-form redesign rounds in response to Commit B failure (defended via the form-vs-within-form distinction in `e66afc1`). **We choose not to spend that budget.** Rationale recorded for the paper:

- **Single-shot falsification produces the cleaner scientific story.** Spending the redesign budget would produce either (a) a longer success story (round 1 closes regression, test_v5 P1 ≥ 0.80 — joint best-case estimated at ~15–20%) requiring the form-preservation argument to win with reviewers, or (b) an iterated null result spread across multiple in-distribution refinements that is harder to defend on form-preservation grounds than a single-shot fail. Under uncertainty, the pre-reg's "Fail (after 2 redesigns)" branch outcome is reachable from round 0 by holding the budget in reserve, with a strictly more conservative iteration record than the pre-reg permitted.
- **The 3B's NO-bias is structural, not phrasing-specific.** The arbiter said NO to safety, scheduling, urban-warning, and colleague-ask content under V3 — the same regimes it cleanly handles under V2's enumeration. Closing this gap within the principled-criterion form without recovering enumeration-style patterns appears unlikely given the pattern-matching behavior observed; the available within-form refinements (softening the time anchor, adding a "default to YES on uncertainty" instruction) target specific failure modes but do not address the structural pattern-matching limitation.
- **M10 (Claude-API arbiter) is the principled next architectural lever.** Stronger model scale should resolve abstract conjuncts more reliably; this cleanly isolates "is the gap prompt-form or model-scale?" The V3 Commit B result reframes M9 from *"is the principled criterion right?"* to *"can a 3B local arbiter resolve a principled criterion at all?"* — answered NO; M10 is the natural test of the orthogonal question.

### What stands

| Pre-M9 result | Status post-M9 |
|---|---|
| M6a V2 three-trace hit ≥ 0.80 (`dev_v2` / `test_v1` / `test_v2`) at 6.8–11.3× lower tok/hit than poll | **Unchanged.** `ContentArbiter.__init__` default reverted to `ARBITER_SYSTEM_PROMPT_V2`; production reproduces M6a / M7 / M8b bit-identically. Pre-flight smoke verified. |
| M7 N=20 RandomArbiter seed-variance on `test_v2` (18/20 seeds C3 PASS) | **Unchanged.** No code path that affects M7 was modified. |
| M8b V2 four-trace extension falsified on `test_v4` | **Unchanged.** `test_v4` stays in repo uncorrected. |

### What is added to the record

| New M9 result | Implication |
|---|---|
| V3 (principled AND-gate, frozen at Commit A SHA `3653880`) fails Commit B regression on round 0 across all three co-developed traces. | The principled-criterion form does not preserve V2's three-trace recall at the 3B model scale on first attempt under a reasonable single-shot phrasing motivated by M8b's V2-coverage gap analysis. |
| Arbiter contribution to V3 hits = 2 events out of 13 GTs across three traces; both match V3 regret-list example words verbatim. | The 3B treats abstract criterion examples as a closed pattern set. Pattern-matching, not abstract-conjunct resolution, is the mode in which a 3B local arbiter operates at this phrasing. |
| Off-harness diagnostic confirms wire-up is sound (V2 cleanly YES on the same client where V3 says NO). | V3 failure attributes to the prompt itself, not to a wiring regression introduced at Commit B. |
| Pre-reg's 2-round within-form redesign budget held in reserve. | Iteration record for M9 is round 0 only — strictly more conservative than the pre-reg permitted. |

### Paper line for this outcome (locked at pre-reg, modified for round-0 close)

Maps to the pre-reg's per-outcome table cell *"Fail (after 2 redesigns)"* (§"Pre-registered paper framing per outcome") — modified to *"fail on round 0, no within-form redesigns spent"*, which is strictly more conservative than what the pre-reg's iteration budget permitted.

> *The principled-criterion form (V3 prompt: actionable AND time-bounded with regret + explicit NO bucket) fails to preserve V2's three-trace recall at the 3B (qwen2.5:3b-instruct) model scale on first attempt under a single-shot phrasing motivated by M8b's V2-coverage gap analysis. arbiter_yes_rate collapsed to 0.00 on `dev_v2`, 0.12 on `test_v1`, 0.14 on `test_v2`; the 3B over-strict-reads abstract conjuncts (NO on `fire_alarm` despite clear safety + bounded time; NO on `flight_delay` / `meeting_moved` for tomorrow-shaped scheduling) and pattern-matches on regret-list example words rather than resolving the abstract criterion (the 2 arbiter-YESs observed across three traces both match a regret-list example word verbatim). The pre-reg permitted up to 2 within-form redesign rounds; we chose not to spend that budget, taking the falsification at face value. M6a's V2 closed-enumeration prompt is reported as itself load-bearing for the three-trace claim at the 3B scale — the principled-criterion form does not substitute for it without recall loss. M10 (Claude-API arbiter) is the next architectural lever: increasing model scale to test whether abstract-conjunct resolution recovers under a stronger arbiter is the orthogonal experiment that V3's 3B failure motivates. M6a's three-trace claim and M8b's external-trace falsification of the four-trace extension both stand unchanged.*

### Code state at close

- `agent/arbiter.py`: `ARBITER_SYSTEM_PROMPT_V3` retained as named constant for paper reference and reproduction; `ContentArbiter.__init__` default reverted to `ARBITER_SYSTEM_PROMPT_V2`. Reproduce M9's falsification by passing `system_prompt=ARBITER_SYSTEM_PROMPT_V3` explicitly to `ContentArbiter`.
- `runs/data/16b-content-{dev_v2,test_v1,test_v2}.json`: retained as the falsification evidence.
- `runs/data/16d-*-test_v5.json`: not produced. M9 closes at Commit B; Commit C / D do not run.
- `sandbox/event_trace.py`: not touched. `test_v5` not authored.

### Rejections log (N/A)

Not reached. The Commit C fresh-session authoring step does not run on path-C close.

## Results — Commit D `test_v5` eval

**Not executed.** Commit B's regression gate FAIL on round 0 closed M9 before Commit C could open. No `test_v5` was authored, no eval cells fired. The Commit-A-frozen `test_v5` authoring prompt and banned-list extensions remain in §"Pre-registered artifacts for `test_v5`" as an unused pre-reg artifact — available for re-use under any future M9-like attempt at this architectural lever (e.g., M10 Claude-API arbiter validation under a similar external-authoring protocol). The pre-reg discipline of generating the held-out trace only after the in-distribution gate passes is preserved: no externally-authored trace is committed under an unvalidated arbiter configuration.

## Artifacts (final)

- `runs/data/16b-content-{dev_v2,test_v1,test_v2}.json` — three regression-gate cells (Commit B). Falsification evidence; retained.
- `runs/data/16d-*-test_v5.json` — **not produced**. Commit D did not run; M9 closed at Commit B per path-C decision.
- `agent/arbiter.py` (this commit) — `ARBITER_SYSTEM_PROMPT_V3` constant added (byte-identical to the Commit-A-frozen V3 system-prompt body, wire-up choice (a)); `ContentArbiter.__init__` default reverted to `ARBITER_SYSTEM_PROMPT_V2` after the regression gate failed. V2 remains the production prompt; V3 is reproducible via explicit `system_prompt=` argument.
- `sandbox/event_trace.py` — **not touched**. `test_trace_v5()` not authored; no registry entry added. The Commit-A-frozen `test_v5` authoring prompt is held as an unused pre-reg artifact.
- `runs/16-v3-prompt.md` — this doc. Pre-reg at Commit A SHA `3653880`; defenses hardened at `e66afc1`; Commit B results + path-C close at this commit. Pre-reg sections (§"Goal" through §"Non-goals") byte-identical to Commit A; this commit only appends results and updates the Commit D / Artifacts placeholders to reflect non-execution.
