# Run 08 — Adversarial test_v2: polarity-flip falsified, surprise gate breaks down

**Date:** 2026-04-18
**Milestone:** M5 — adversarial held-out trace stress-testing the surprise-gate thesis.
**Trace:** `test_v2` (held out, structurally inverted from dev_v2 / test_v1)
**New code:** `sandbox/event_trace.py::test_trace_v2`. No new agents — re-uses `HeargentAgent`, `HeargentZ`, `react_poll_local`, baselines, and a one-off polarity-agnostic z-gate (`abs(z) > threshold`) wired inline in the sweep.

## Goal

Run 07 ended with the most important caveat in the project flagged but unaddressed: **dev_v2 and test_v1 share the same structural split** — human-relevant GT vs. system-noise distractors. The polarity flip (GT → low surprise, distractors → high surprise) might be an artifact of that split.

`test_v2` is the adversarial inverse:

- **Distractors** are mundane routine the predictor *should* learn to expect: daily briefings, "all systems nominal", weekly uptime reports, newsletters.
- **GT events** are abrupt interruptions that genuinely break narrative context: kitchen fire, urgent board meeting moved to NOW, burst water main, ER call about a parent, security breach.

If the polarity-flip thesis is real, GT events here should score *higher* surprise than distractors — i.e. the inverted gate from runs 05–07 should fail and the *forward* gate should win. If neither single-polarity gate works, the surprise signal isn't load-bearing in any direction.

## Trace design

| t (s) | id | kind | role | window |
|---|---|---|---|---|
| 10 | daily_briefing | email | distractor | — |
| 60 | status_ok | notification | distractor | — |
| 85 | uptime_ping | notification | distractor | — |
| 95 | **fire_kitchen** | world_event | GT | 20 |
| 250 | **board_meeting** | calendar_update | GT | 60 |
| 350 | newsletter | email | distractor | — |
| 400 | **water_burst** | notification | GT | 120 |
| 550 | **er_call** | phone_message | GT | 300 |
| 750 | **security_breach** | alert | GT | 180 |

The first three distractors prime the predictor on routine and load cron 30 s such that `fire_kitchen` (t=95, window [95, 115]) falls in the dead zone after cron's t=90 fire — making `fire_kitchen` cron-unwinnable, mirroring `server_outage` in test_v1.

## Per-event surprise (qwen2.5:3b predictor at temp=0/seed=42, nomic-embed-text)

| t | id | role | surprise | predictor anchor |
|---|---|---|---|---|
| 10 | daily_briefing | dist | 0.3762 | "No notable events expected in the next minute." |
| 60 | status_ok | dist | 0.4778 | "No notable events expected in the next minute." |
| 85 | uptime_ping | dist | 0.4668 | "No notable events expected in the next minute." |
| **95** | **fire_kitchen** | **GT** | **0.4822** | "No notable events expected in the next minute." |
| **250** | **board_meeting** | **GT** | **0.3955** | "FIRE continues to escalate…" |
| 350 | newsletter | dist | 0.4749 | "FIRE detected in kitchen; evacuation ongoing." |
| **400** | **water_burst** | **GT** | **0.3552** | "FIRE detected in kitchen; evacuate immediately." |
| **550** | **er_call** | **GT** | **0.4909** | "Emergency response team dispatched for main water line burst…" |
| **750** | **security_breach** | **GT** | **0.4645** | "Emergency response team dispatched due to main water line burst…" |

Aggregates:

|  | mean | min | max |
|---|---|---|---|
| GT (5) | 0.4377 | 0.3552 | 0.4909 |
| Distractors (4) | 0.4489 | 0.3762 | 0.4778 |

GT mean is still slightly *below* distractor mean (the polarity-flip sign holds in aggregate), but the **distributions are heavily overlapping** and the per-event polarity is unstable: `fire_kitchen` and `er_call` are HIGH-surprise (forward-polarity), `board_meeting` and `water_burst` are LOW-surprise (inverted-polarity), `security_breach` is mid-pack.

The mechanism is visible in the predictor anchor column. Once `fire_kitchen` lands, the predictor latches onto "fire / emergency response" and stays there. Subsequent emergency-flavored GT events (`board_meeting` urgency, `water_burst`) score *low* surprise because they semantically resemble the latched prediction — even though they are completely unrelated emergencies. `er_call` re-shifts the anchor to "water burst response", so `security_breach` (also unrelated) scores high again. Single-polarity gates can only catch the half of GT events that happen to align with their assumed direction.

## Results — full battery, no per-trace tuning

| Agent | hit | false/h | TTN (s) | notifs | LLM calls | tokens (in/out) | tokens/hit |
|---|---|---|---|---|---|---|---|
| reactive | 0.00 | 0.00 | — | 0 | 0 | 0 / 0 | ∞ |
| cron 30 s | 0.80 | 18.75 | 0 | 9 | 0 | 0 / 0 | 0 |
| cron 300 s | 0.60 | 22.50 | 50 | 9 | 0 | 0 / 0 | 0 |
| **HeargentZ inverted z_thr=0.0 (frozen from dev_v2)** | **0.40** | **7.50** | **0** | **4** | 9 | 1947 / 130 | 1039 |
| HeargentZ forward z_thr=0.0 | 0.60 | 15.00 | 0 | 7 | 9 | 1947 / 130 | 692 |
| HeargentZ \|z\| z_thr=0.0 | 1.00 | 15.00 | 0 | 9 | 9 | 1947 / 130 | 415 |
| HeargentZ \|z\| z_thr=0.5 | 0.80 | 15.00 | 0 | 8 | 9 | 1947 / 130 | 519 |
| HeargentZ \|z\| z_thr=1.0 | 0.60 | 7.50 | 0 | 5 | 9 | 1947 / 130 | 692 |
| **react_poll_local** | **1.00** | **0.00** | **0** | **5** | **192** | **37753 / 393** | **7629** |
| random p=0.44 (matches inverted firing rate; n=5 seeds) | 0.40 | 8.25 | — | ~4.2 | 0 | 0 / 0 | 0 |
| random p=0.89 (matches \|z\|@0.5; n=5 seeds) | 0.96 | 13.50 | — | ~8.4 | 0 | 0 / 0 | 0 |
| random p=1.00 | 1.00 | 15.00 | — | 9 | 0 | 0 / 0 | 0 |

(`tokens/hit` is in-tokens divided by hits; included for cost intuition, not in the original metric set.)

## Headline findings

### 1. Frozen inverted gate collapses on adversarial trace.

| Trace | Frozen HeargentZ inverted z_thr=0.0 hit |
|---|---|
| dev_v2 (calibration) | 1.00 |
| test_v1 (held out, same structural split) | 0.80 |
| **test_v2 (held out, inverted structural split)** | **0.40** |

This is the failure run 07 explicitly flagged: *"if abrupt GT events score higher surprise than the calm distractors, the inverted gate fails and forward heargent (or a polarity-agnostic |z| > threshold gate) should win."* That risk has now landed.

### 2. No single-polarity gate works on test_v2.

| Gate | hit | false/h |
|---|---|---|
| Inverted z_thr=0.0 | 0.40 | 7.50 |
| Forward z_thr=0.0 | 0.60 | 15.00 |

The two polarities catch *complementary* GT subsets — inverted catches `board_meeting` + `water_burst` (low-surprise emergencies), forward catches `fire_kitchen` + `er_call` + `security_breach` (high-surprise interruptions). Neither catches all five. The polarity per event is set by what the predictor happens to be anchored on at that moment, which is itself a function of the trace history — i.e., you can't pre-register a polarity.

### 3. The polarity-agnostic |z| gate matches random.

|z| z_thr=0.0 hits 1.00 / false 15.00 — but so does random p=1.00 (always-fire). The signal is not load-bearing at low thresholds.

At higher thresholds the signal does discriminate slightly above random:

| Gate | hit | false/h | Random match | random hit | random false/h |
|---|---|---|---|---|---|
| \|z\| z_thr=0.5 | 0.80 | 15.00 | p=0.89 | 0.96 ± 0.09 | 13.50 ± 4.4 |
| \|z\| z_thr=1.0 | 0.60 | 7.50 | p=0.56 | (not run) | — |

|z|@0.5 sits *inside* the random@0.89 spread — random's mean hit (0.96) is actually *higher* than |z|'s 0.80, at similar false rates. The surprise signal does not separate signal from noise on this trace at any threshold tested.

### 4. Cron 30 s is the heargent-relative winner among non-LLM agents.

cron 30 s achieves (0.80, 18.75, TTN=0) on test_v2, beating every single-polarity HeargentZ on hit rate. It misses only `fire_kitchen` (cron-unwinnable by construction) and surfaces every distractor as a false positive. Heargent loses the cost story too — the inverted-frozen rule produces 1039 tokens/hit because hits are halved, while cron pays zero tokens.

### 5. Poll is the only agent that wins this trace.

`react_poll_local` again hits 1.00 / 0.00 / TTN=0. The local 3B predictor, given the full pending-event queue and instructed to skip routine, correctly classifies all 5 GT events on test_v2 — including `fire_kitchen` (the cron-unwinnable one). Cost: 7629 tokens/hit. There is no surprise-gate configuration that beats this on quality.

## What this means for the v1 thesis

The plan's one-claim thesis was:

> Gating self-initiation on model-expressed surprise about expected world state produces better proactive behavior than gating on time elapsed, at lower token cost than unconditional polling.

After three traces (dev_v2, test_v1, test_v2), the evidence is split:

- **Two traces** (dev_v2, test_v1, structurally homogeneous: human-relevant GT vs system-noise distractors) → HeargentZ matches poll at 17–29× lower cost. Thesis confirmed in this regime.
- **One trace** (test_v2, structurally heterogeneous: GT and distractors both occupy a wide semantic range relative to the rolling prediction) → HeargentZ collapses; surprise carries no useful signal in any single polarity; polarity-agnostic |z| does not separate from random.

This is the "if v1 fails or barely beats baselines, the neuroscience stack does not save it" branch of the plan. The honest paper-shaped claim is now narrower than the original thesis:

> **HeargentZ delivers near-poll proactive behavior at ~20× lower token cost on traces where the GT-vs-distractor split is structurally consistent (human-relevant vs system-noise). When that split is mixed — when distractors include calm-routine messages and GT events span both calm-aligned and disruption-aligned semantics relative to the rolling prediction — single-step embedding surprise is no longer a sufficient gate signal, and unconditional polling is the only configuration that matches the quality ceiling.**

This is more useful as a research result than a clean win would have been: it identifies a concrete failure mode of the surprise-gate approach (per-event polarity instability driven by predictor latching) and points at the next architectural primitive (intent-conditioned prediction, longer-horizon prediction, or a learned arbiter that combines surprise + content classification).

## Risk register update

- **Risk 1 (surprise = perplexity).** Still mitigated. The failure mode here is not a perplexity artifact — it is a real property of single-step embedding surprise under predictor latching.
- **Risk 2 (strong baseline matches hit rate).** Reinforced. Poll matches or beats heargent on hit rate on all three traces. The cost story (17–29× cheaper) only holds where the surprise signal is informative.
- **Risk 3 (unfalsifiability via knob-turning).** The pre-registered freeze rule from run 07 produced an honest failure on test_v2 — this is exactly what the freeze rule is for. We did not search test_v2 for a θ that "rescues" the inverted gate.

## Still untested / what this surfaces

- **Intent-conditioned prediction** is now the most natural next architectural step, not an optional polish item. The latching failure on test_v2 is a direct consequence of the predictor having no notion of "user goals are X, watch for Y" — it just continues whatever surface narrative dominated the last few observations.
- **Larger predictor (7–13B).** Might shift the surprise distributions enough to make a single-polarity gate work on test_v2, but the *mechanism* (predictor latching → polarity instability) is unlikely to disappear at a larger size. Still worth one comparison run.
- **Arbiter that combines surprise + lightweight content classification.** A 3B model called *only when surprise is borderline* could likely catch what the embedding-only gate misses, at far less than poll's cost.
- **Per-stream polarity detection.** If certain event kinds (alerts, world_events) reliably score one polarity and others (calendar_updates, emails) the other, a kind-conditioned z-rule might outperform the polarity-agnostic |z|. The data is too thin (5 GT × 3 traces) to settle this.

## Reproduce

```sh
# Baselines
uv run python -m eval.run_trace --agent baselines.react_reactive:ReactiveAgent       --trace test_v2 --out runs/data/08a-reactive-test_v2.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s  --trace test_v2 --out runs/data/08b-cron30-test_v2.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword300s --trace test_v2 --out runs/data/08c-cron300-test_v2.json

# Strong baseline (~70 s)
uv run python -m eval.run_trace --agent baselines.react_poll_local:ReactPollLocal --trace test_v2 --out runs/data/08d-poll-test_v2.json

# Per-event surprise dump + HeargentZ polarity sweep + random-gate ablation
# (see inline scripts at end of this run; raw JSONs in runs/data/08e/f/g)
```

## Artifacts

- `runs/data/08a-reactive-test_v2.json`, `08b-cron30-test_v2.json`, `08c-cron300-test_v2.json` — non-LLM baselines.
- `runs/data/08d-poll-test_v2.json` — strong baseline.
- `runs/data/08e-test_v2-surprise.json` — per-event surprise + predictor anchor.
- `runs/data/08f-heargent-z-sweep-test_v2.json` — HeargentZ inverted / forward / |z| sweep.
- `runs/data/08g-random-sweep-test_v2.json` — random-gate matched-firing-rate ablation.
- `sandbox/event_trace.py::test_trace_v2` — adversarial trace definition.
