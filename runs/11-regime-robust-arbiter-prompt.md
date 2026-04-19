# Run 11 — Regime-Robust Arbiter Prompt (M5)

**Date:** 2026-04-19 (pre-registration); evaluation TBD.
**Milestone:** M5 — rewrite the M4 arbiter prompt to be regime-robust (cover scheduling, deliveries, deadlines, callbacks explicitly in the YES column) without destroying the test_v2 win or over-firing on adversarial-trace distractors.
**Status:** pre-registration only; matrix not yet executed.
**Pre-registration SHA:** TBD (this commit). **Implementation SHA:** TBD. **Predecessor:** M4 impl SHA `17e7e52`, M4 results SHA `3da1b90`.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, seed=42, deterministic throughout (predictor, arbiter, random-ablation Bernoulli). Local-only; no Claude API.

## Goal

Recover the dev_v2 and test_v1 regressions that M4's pre-registered prompt produced (dev_v2 1.00 → 0.60; test_v1 0.80 → 0.40) **without sacrificing M4's test_v2 win** (0.80 / 0.00 / 770 tok/hit, 10× cheaper than poll at matching quality). The mechanism under test: a single broader arbiter prompt that explicitly covers the within-24-hour scheduling phrasings which the M4 prompt's "imminent action required" clause read narrowly. Every other piece of the M4 stack — band, window, predictor, surprise scorer, bootstrap policy, HeargentZA wiring, random-arbiter ablation — stays frozen. One moving part, one hypothesis.

## Design reasoning (why a prompt-only change, why this prompt)

M4 closed as partial success. The pre-eval isolation probe (runs/10 Results, committed in `3da1b90`) documented the failure mechanism in advance: the 3B arbiter fires YES on right-this-moment interrupt language ("FIRE", "URGENT", "Emergency", "Hospital called", "Security alert") and NO on within-24-hour scheduling phrasings ("tomorrow", "in 24 hours", "in 2 days", "today at 16:00"). Every M4-missed regime-aligned GT (flight_delay, meeting_moved, deadline, dentist_cancel, package_arrival, doctor_callback, rent_due) lives in the second category. The M4 prompt's four YES clauses — safety, personal-life interruption, imminent financial/scheduling obligation, production alert — do not explicitly name the scheduling/delivery/deadline category.

The M5 bet: **the arbiter prompt is the lever that was under-specified.** Add four explicit YES categories covering the M4 failure modes (schedule change, deadline obligation within the next few days, personal message/delivery, weather/external condition) while reinforcing the NO list against the adversarial-trace distractors that might leak through the broader YES language. The prompt-only change preserves M4's controlled-comparison discipline: if M5 passes primary criterion 1, the prompt wording is the only viable attribution for the dev_v2 / test_v1 recovery.

Alternative architectural levers — larger predictor, Claude-API arbiter, two-prompt dispatcher, Reflect loop — are all available and all more expensive. M5 exhausts the cheapest single-dimension lever first. If M5 fails, the exhaustion is informative: the single-prompt 3B arbiter design is at its ceiling and M6 moves to the next lever.

**Nothing else about the architecture is changing.** The three-way band `z ∈ [−0.5, +1.0]` held its structural promise on M4 (max 7 arbiter calls, well under the budget of 12). The rolling-window z gate catches every regime-aligned strong-negative GT. The bootstrap-phase arbiter correctly filtered all three test_v2 bootstrap distractors under V1. Every one of those mechanisms stays in place — only the YES/NO classifier's prompt string differs.

## Pre-registered artifacts (frozen before any eval run)

Everything in this section is committed before M5 eval begins. Any post-hoc modification is a protocol deviation and will be called out explicitly.

### Borderline band (unchanged from M4)

```
z < -0.5          → auto-surface (trust strong negative z)
-0.5 ≤ z ≤ +1.0   → arbiter decides
z > +1.0          → auto-skip (trust strong positive z)
z is None         → arbiter decides   (bootstrap, first min_window=4 events)
```

### Arbiter system prompt (V2, new)

```
You are a triage filter for a proactive assistant. Decide whether a
single observed event warrants surfacing to the user right now.

Surface (YES) if the event describes any of:
 - an urgent safety or security issue (fire, break-in, medical
   emergency, security breach, unauthorized access)
 - a schedule change affecting the user personally (meeting moved,
   meeting cancelled, flight delayed, appointment rescheduled,
   appointment cancelled)
 - a financial or deadline obligation the user must act on within
   the next few days (bill due, rent due, report deadline,
   payment reminder)
 - a message or delivery directed personally to the user (package
   delivered, callback requested, voicemail or phone message,
   hospital calling about a family member)
 - a weather alert or external condition that would plausibly
   change the user's planned day
 - a production/on-call alert or outage for a system the user owns

Do NOT surface (NO) if the event is:
 - routine status, uptime, heartbeat, or "all systems normal" pings
 - marketing, promotional, or newsletter content
 - generic daily briefings that explicitly state no urgent items
 - feature announcements, app updates, or social/channel invites

Output exactly YES or NO, uppercase, on a single line. No explanation.
```

**YES-column design (each clause targets a specific M4 failure mode):**
- *schedule change* — covers `flight_delay`, `meeting_moved`, `dentist_cancel` (the three M4-missed dev_v2 GTs).
- *financial or deadline obligation within the next few days* — covers `deadline` and `rent_due`. The "next few days" phrasing is deliberately broader than M4's "imminent" without opening the gate to all promotional content (which has no deadline).
- *message or delivery directed personally to the user* — covers `package_arrival` and `doctor_callback`. The "directed personally" qualifier is intended to keep `slack_invite` and `calendar_advert` out.
- *weather alert or external condition that would plausibly change the user's planned day* — covers `weather_alert` on dev_v1; the "plausibly change the user's planned day" qualifier is intended to distinguish it from `weather_nominal` on dev_v2.

**NO-column reinforcements (each clause targets a specific distractor that might leak under the broader YES language):**
- *"all systems normal" pings* — guards against `system_heartbeat`, `status_ok`, `uptime_ping`, `system_status` slipping in under the broader language.
- *generic daily briefings that explicitly state no urgent items* — direct guard against `daily_briefing` on test_v2 ("Daily briefing: no urgent items for today.") flipping to YES under the broader schedule-change clause.
- *feature announcements, app updates, or social/channel invites* — guards against `calendar_advert` and `slack_invite` sneaking in under the delivery/message clause.

Same model (`qwen2.5:3b-instruct`), temperature=0.0, seed=42, max_tokens=5. Same parse rule (first uppercase YES/NO on line 1; malformed → NO default-skip). Same user message shape (raw event content string, nothing else; no kind field, no sim_time, no briefing, no intent list, no prior observations, no prior prediction).

### Frozen agent config (unchanged from M4 except arbiter prompt)

**HeargentZA V2 (content arbiter):**
- Gate: rolling-window z-score, `window=16`, `min_window=4`. Identical math to HeargentZ.
- Band: `[−0.5, +1.0]` as above.
- Arbiter: `ContentArbiter` with V2 prompt.
- Predictor: qwen2.5:3b-instruct, temperature=0.0, seed=42. Unchanged.
- Surprise scorer: nomic-embed-text. Unchanged.
- One config, three traces. No per-trace tuning.

**HeargentZA V2-random (null ablation):**
- Identical gate + band + predictor + surprise.
- `ContentArbiter` replaced by `RandomArbiter(p, seed=42)` where `p` is the empirical YES-rate of the V2 content arbiter on **the M5 dev_v2 run** (measured from `runs/data/11a-heargent-za-v2-dev_v2.json` and frozen before the random-ablation cells run). Matched firing rate; only the content signal differs.
- Same seed across all three random-ablation traces; the Bernoulli stream is deterministic given the fixed event order.

M4's `p = 0.25` is **not** reused — the broader V2 prompt will almost certainly fire YES more often, and the ablation must match the V2 firing rate to isolate the content signal.

### Pre-flight isolation probe (go/no-go gate, pre-registered)

Before any matrix cell fires, run a 27-string isolation probe on `ContentArbiter.classify` covering every GT and every distractor across the three evaluation traces. The probe extends M4's 17-string probe with additional per-trace distractor lines to catch over-firing on routine-status variants that might slip past under the broader YES language.

**Expected outcomes (pinned before the probe runs):**

| Trace | Event | Role | Expected |
|---|---|---|---|
| dev_v2 | fire_alarm | GT | YES (unchanged from M4) |
| dev_v2 | flight_delay | GT | **YES (M4 was NO)** |
| dev_v2 | news_digest | dist | NO (unchanged) |
| dev_v2 | meeting_moved | GT | **YES (M4 was NO)** |
| dev_v2 | weather_nominal | dist | NO (unchanged) |
| dev_v2 | marketing_newsletter | dist | NO (unchanged) |
| dev_v2 | deadline | GT | **YES (M4 was NO)** |
| dev_v2 | system_heartbeat | dist | NO (unchanged) |
| dev_v2 | dentist_cancel | GT | **YES (M4 was NO)** |
| test_v1 | package_arrival | GT | **YES (M4 was NO)** |
| test_v1 | slack_invite | dist | NO (unchanged) |
| test_v1 | doctor_callback | GT | **YES (M4 was NO)** |
| test_v1 | server_outage | GT | YES (unchanged) |
| test_v1 | calendar_advert | dist | NO (unchanged) |
| test_v1 | promo_email | dist | NO (unchanged) |
| test_v1 | rent_due | GT | **YES (M4 was NO)** |
| test_v1 | system_status | dist | NO (unchanged) |
| test_v1 | kid_school_pickup | GT | YES (unchanged) |
| test_v2 | daily_briefing | dist | NO (unchanged) |
| test_v2 | status_ok | dist | NO (unchanged) |
| test_v2 | uptime_ping | dist | NO (unchanged) |
| test_v2 | fire_kitchen | GT | YES (unchanged) |
| test_v2 | board_meeting | GT | YES (unchanged) |
| test_v2 | newsletter | dist | NO (unchanged) |
| test_v2 | water_burst | GT | YES (unchanged) |
| test_v2 | er_call | GT | YES (unchanged) |
| test_v2 | security_breach | GT | YES (unchanged) |

27 strings total. **Go-bar: ≥ 25 / 27 (≥ 93 %) correct under V2.** If the probe fails the bar, the matrix is **not run** and the V2 prompt is re-pre-registered as a new M5b. No modification of the V2 prompt based on probe results within this pre-reg. The probe is a pre-committed sanity check, not a tuning step.

### Pre-registered success criteria

Frozen before any M5 matrix cell runs. Each headline claim will cite which criterion it passed/failed, verbatim.

1. **Primary — no regression on regime-aligned traces.** HeargentZA V2 hit ≥ HeargentZ hit − 0.20 on both dev_v2 (≥ 0.80) and test_v1 (≥ 0.60). This is the single thing M5 exists to solve; failure collapses M5 to "broader prompt didn't broaden enough."
2. **Preserve M4 win on test_v2.** HeargentZA V2 hit ≥ 0.80 **and** tok/hit < 7629 on test_v2. Losing this would mean the broader prompt solves regime-aligned at the cost of adversarial — a different lose, not a win.
3. **Content signal load-bearing, multi-trace.** HeargentZA V2 beats HeargentZA V2-random on at least two of the three traces by Δhit ≥ 0.20 **or** Δfalse/h ≥ 5.0. Stricter than M4's test_v2-only check because the broader prompt fires YES more often, and the real arbiter must do real work across regimes — a matched-firing-rate random that beats it on any single trace undermines the V2 prompt's claim.
4. **False-init bound, per-trace.** HeargentZA V2 false/h on each trace ≤ plain HeargentZ false/h + 5.0. The broader prompt could over-fire on distractor categories; this bounds how much.
5. **Budget bound.** Arbiter calls per trace ≤ 12, same as M4. Since the band is unchanged, this should hold structurally; a budget breach means the `[−0.5, +1.0]` band is interacting with the new prompt in a way not anticipated.

**Decision rules (binding, written in advance):**
- All 5 pass → M5 validated. Single-config regime-robust agent across all three structurally distinct traces. Paper frame becomes the full headline: *selective initiation at matching quality, 10× cheaper than poll, across three structurally distinct traces.*
- C1 passes, C2 fails → broader prompt sacrifices the adversarial trace. M6 pivots to a two-prompt dispatcher (out-of-band selector chooses arbiter prompt per observation category) or abandons the single-config claim and reports a per-regime prompt family.
- C2 passes, C1 fails → broader prompt didn't broaden enough. M6 pivots to Claude-API arbiter (10–50× cost per arbiter call but same call count; total cost still well under poll).
- C3 fails on both regime-aligned traces → content signal under V2 is not load-bearing; broader prompt is effectively a firing-rate widening. Null result, no headline claim. M6 pivots to larger predictor.
- C4 fails on any trace → report regression, new pre-reg with NO-column tightening.
- Isolation probe fails the 25/27 go-bar → matrix not run; re-pre-register as M5b with a revised prompt.

## Evaluation matrix

Frozen config on every cell. Each cell = one run, one JSON output in `runs/data/11-*.json`. 6 new cells; the V1 rows are cited, not re-executed.

| Agent | dev_v2 | test_v1 | test_v2 |
|---|---|---|---|
| cron 30 s | (cited, run 02/03/08) | (cited, run 06) | (cited, run 08) |
| HeargentZ (no arbiter) | (cited, run 07) | (cited, run 07) | (cited, run 08) |
| HeargentZA V1 prompt (M4) | (cited, run 10a) | (cited, run 10b) | (cited, run 10c) |
| react_poll_local | (cited, run 07) | (cited, run 07) | (cited, run 08) |
| **HeargentZA V2 prompt (content)** | new | new | new |
| **HeargentZA V2 random ablation** | new | new | new |

M4 rows cited for direct V1-vs-V2 delta. M5's random-ablation `p` is defined as the content arbiter's measured YES-rate on `runs/data/11a-heargent-za-v2-dev_v2.json` once 11a lands, then pinned for the three random cells. This one value is intentionally *not* frozen before eval, because it is defined as a measurement on a prior cell.

Each new JSON includes: git commit SHA, ollama version, model digests, and per-event `(prediction, observation, surprise, z, arbiter_call, arbiter_decision, surfaced)` dumps.

## Architecture changes (additive only)

Smallest possible change. One new constant, one optional kwarg, one default flip.

1. **`agent/arbiter.py`** — add `ARBITER_SYSTEM_PROMPT_V2` next to the existing `ARBITER_SYSTEM_PROMPT` (left untouched so `git blame` for M4 stays clean). `ContentArbiter.__init__` gains a `system_prompt: str = ARBITER_SYSTEM_PROMPT_V2` kwarg; default flips to V2. `.classify` uses `self.system_prompt` instead of the module-level constant. M4 reproducibility relies on SHA `17e7e52`, which does not have V2; M4 reruns from that SHA still use V1. M5 reruns from the M5 implementation SHA use V2.

2. **`agent/loop.py`** — unchanged. `HeargentZA` constructs `ContentArbiter` via its `from_trace` classmethod; the kwarg default carries V2 through without a code change.

3. **`eval/run_trace.py`** — unchanged. `--arbiter-mode {content,random}` is sufficient; there is no V1/V2 CLI flag. V2 is simply the new default. M4 reruns checkout the pre-M5 SHA.

No changes to baselines, cron, plain `HeargentZ`, `HeargentZIntent`, the predictor, the surprise scorer, or the scoring harness. If M5 falsifies, reverting is a one-line default flip.

## Results

_(pre-registration only; to be filled in after the isolation probe + 6-cell matrix land.)_

### Pre-eval isolation probe

TBD. Probe output (27 strings, expected vs actual YES/NO) to be recorded verbatim here before any matrix cell runs. Go-bar: ≥ 25 / 27.

### Full 6-cell matrix

TBD.

### Per-event prediction / surprise / arbiter — regime-aligned traces (V1 vs V2)

TBD. Focus tables: dev_v2 and test_v1, contrasting M4 V1 misses with M5 V2 decisions on the same events.

### Pre-registered success criteria — evaluation

TBD. Five criteria evaluated verbatim against the rules frozen in the pre-registration commit. No post-hoc redefinition.

### Headline findings

TBD.

### What this means for M5 and what comes next

TBD.

## Reproduce

Ollama 0.21.0 must be running locally with `qwen2.5:3b-instruct` and `nomic-embed-text` pulled. All runs deterministic (temp=0, seed=42).

```sh
# HeargentZA V2 (content arbiter) × 3 traces
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace dev_v2  --arbiter-mode content --out runs/data/11a-heargent-za-v2-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v1 --arbiter-mode content --out runs/data/11b-heargent-za-v2-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v2 --arbiter-mode content --out runs/data/11c-heargent-za-v2-test_v2.json

# HeargentZA V2-random (null ablation) × 3 traces.
# Requires `p` measured on runs/data/11a-heargent-za-v2-dev_v2.json first.
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace dev_v2  --arbiter-mode random --arbiter-random-p <p> --out runs/data/11d-heargent-za-v2-random-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v1 --arbiter-mode random --arbiter-random-p <p> --out runs/data/11e-heargent-za-v2-random-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v2 --arbiter-mode random --arbiter-random-p <p> --out runs/data/11f-heargent-za-v2-random-test_v2.json
```

## Artifacts

- `runs/data/11a-heargent-za-v2-dev_v2.json` … `11f-heargent-za-v2-random-test_v2.json` — full 6-cell matrix (to be written).
- Every JSON contains `surprise_log` (per-event prediction/observation/surprise/z/arbiter_call/arbiter_decision/surfaced), `arbiter_yes_rate` (on the content cells), and standard eval scoring.
- Baselines cited for comparison: `runs/data/07c-heargent-comparison.json`, `runs/data/08f-heargent-z-sweep-test_v2.json` (HeargentZ rows), `runs/data/07a-poll-dev_v2.json`, `runs/data/07b-poll-test_v1.json`, `runs/data/08d-poll-test_v2.json` (poll rows), `runs/data/10a-heargent-za-dev_v2.json` … `10c-heargent-za-test_v2.json` (HeargentZA V1 rows).
- Code: `agent/arbiter.py` (V2 prompt added + `ContentArbiter.system_prompt` parameterized). Committed at the implementation SHA, a strict descendant of this pre-registration SHA.
