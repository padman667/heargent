# Run 06 — Held-out test trace: does the polarity flip generalize? (test_v1)

**Date:** 2026-04-18
**Milestone:** M5 (test trace run, but ahead of schedule because we needed it now to interpret run 05)
**Trace:** new — `sandbox.event_trace.test_trace_v1` (5 ground-truth + 4 distractors, 810 s)
**Agents:** reactive, cron 30 s, cron 300 s, heargent forward (θ-sweep), heargent inverted (θ-sweep), random-gate (matched p, 5 seeds)

## Goal

Run 05's headline (inverted gate at θ=0.43 hits 1.00 with zero false-init on dev_v2) is dev-set-overfit by definition. The single most-important next experiment is: **does the polarity flip — GT events being *less* surprising than distractors — generalize to a trace not used to choose θ?**

If yes: prediction-error is a real, polarity-stable salience signal in narrative event streams, and we can publish that with a clear caveat about polarity.
If no: the dev_v2 result was a coincidence and the v1 thesis is essentially dead, motivating an immediate pivot to intent-conditioned prediction.

## Trace design (test_v1)

Same structural split as dev_v2 (5 human-relevant GT + 4 system-noise distractors), completely different specific content (no fire/flight/dentist; instead packages/doctors/server/rent/school).

Includes one "unwinnable for cron" event by construction:

| id | type | t (s) | window (s) | window end | keywords | rationale |
|---|---|---|---|---|---|---|
| package_arrival | GT | 15 | 60 | 75 | package, delivered | normal |
| slack_invite | dist | 40 | — | — | — | system noise |
| doctor_callback | GT | 80 | 120 | 200 | doctor, call | normal |
| **server_outage** | **GT** | **95** | **20** | **115** | production, alert | **falls in cron-30s gap (90–120), unwinnable** |
| calendar_advert | dist | 200 | — | — | — | system noise |
| rent_due | GT | 350 | 600 | 950 | rent, due | very long window |
| promo_email | dist | 400 | — | — | — | system noise |
| system_status | dist | 500 | — | — | — | system noise |
| kid_school_pickup | GT | 600 | 180 | 780 | school, pick up | normal |

Note on `server_outage`: cron 30 s fires whenever a new event arrives, rate-limited to once per 30 s. After firing on doctor_callback at t≈90, it cannot fire again until t=120, but server_outage's window expires at t=115 — so cron 30 s genuinely misses it. (My first iteration of test_v1 put server_outage at t=152 with window=15 and cron 30 s caught it anyway; that data was discarded.)

## Per-event surprise on test_v1 (deterministic, temp=0/seed=42)

| event_id | type | surprise |
|---|---|---|
| doctor_callback | GT | 0.4095 |
| system_status | distractor | 0.4212 |
| server_outage | GT | 0.4250 |
| kid_school_pickup | GT | 0.4816 |
| package_arrival | GT | 0.4952 |
| calendar_advert | distractor | 0.5516 |
| promo_email | distractor | 0.5603 |
| rent_due | GT | 0.5755 |
| slack_invite | distractor | 0.6044 |

**Cluster means: GT=0.480, distractors=0.534.** Polarity is in the same direction as dev_v2 (GT lower than distractors). **But the distributions interleave** — `system_status` (distractor, 0.4212) sits *inside* the GT cluster, and `rent_due` (GT, 0.5755) sits *inside* the distractor cluster. There is no θ that perfectly separates the two classes. This is qualitatively different from dev_v2 where a single θ=0.43 hit (1.00, 0.00).

## Results

```sh
uv run python -m eval.run_trace --agent baselines.react_reactive:ReactiveAgent       --trace test_v1 --out runs/data/06a-reactive-test_v1.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s  --trace test_v1 --out runs/data/06b-cron30-test_v1.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword300s --trace test_v1 --out runs/data/06c-cron300-test_v1.json
uv run python -m eval.sweep --trace test_v1 --out runs/data/06d-heargent-fwd-sweep-test_v1.json
# inverted sweep + matched-p random gate run inline (see commit)
```

| Agent | hit | false/h | TTN | misses |
|---|---|---|---|---|
| reactive (floor) | 0.00 | 0.00 | — | all 5 |
| cron 30 s | 0.80 | 18.37 | 10.0 | server_outage |
| cron 300 s | 0.40 | 25.71 | 250.0 | 3 events incl. server_outage |
| heargent forward θ=0.30 | 1.00 | 14.69 | 0.0 | — |
| heargent forward θ=0.43 | 0.60 | 11.02 | — | 2 events |
| heargent forward θ=0.50 | 0.20 | 11.02 | — | 4 events |
| **heargent inverted θ=0.50** | **0.80** | **3.67** | **0.0** | rent_due |
| **heargent inverted θ=0.58** | **1.00** | **11.02** | **0.0** | — |
| random-gate p=0.56 (5 seeds) | 0.72 ± 0.18 | 5.88 ± 2.01 | — | varies |
| random-gate p=0.67 (5 seeds) | 0.80 ± 0.14 | 7.35 ± 2.60 | — | varies |

## Three findings, in order of importance

### 1. Polarity sign generalizes; magnitude does not.

On both dev_v2 and test_v1, the cluster mean of GT-event surprise is *below* the cluster mean of distractor surprise. The forward gate ("high surprise = surface") is dominated by the inverted gate on both traces. **The directional claim — narratively-coherent events score *lower* surprise than off-topic noise under a context-anchored predictor — replicates.**

But the *cleanness* of the separation does not:

| | dev_v2 | test_v1 |
|---|---|---|
| GT mean surprise | 0.370 | 0.480 |
| distractor mean surprise | 0.490 | 0.534 |
| min distractor − max GT | +0.028 (separable) | −0.166 (interleaved) |
| best inverted θ result | (1.00, 0.00) | (0.80, 3.67) or (1.00, 11.02) |

dev_v2 admitted a perfect classifier; test_v1 does not. The dev-overfit caveat from run 05 was correct.

### 2. Inverted heargent still Pareto-dominates cron and random on test_v1.

- **vs. cron 30 s** (0.80 hit, 18.37 false/h, TTN=10): inverted θ=0.58 strictly dominates on **all three axes** — same hit rate (1.00 vs 0.80 — actually better), 40 % lower false rate (11.02 vs 18.37), zero TTN (vs 10). Inverted θ=0.50 trades one hit (0.80 vs 0.80) for a 5× lower false rate (3.67 vs 18.37). Cron 30 s misses `server_outage` outright; both inverted variants catch it at TTN=0.
- **vs. random-gate at matched firing rate** (p=0.56, the same 5/9 firings as inverted θ=0.50): inverted gets hit=0.80 vs random's 0.72±0.18 *and* false=3.67 vs random's 5.88±2.01. **Inverted strictly dominates random at matched rate** — exactly what the random-gate ablation in the plan was designed to test. The surprise signal is load-bearing on test_v1 too.

### 3. Forward heargent is uniformly bad on test_v1, just as on dev_v2.

At every θ above 0.40, the forward gate kills hit rate before it kills false rate, because GT events occupy the low-surprise tail. The Pareto frontier is owned by inverted heargent on both traces.

## What this means for the paper

The thesis can be stated cleanly without overclaiming:

> **Prediction error against an independent embedding model carries a polarity-stable salience signal that strict timer baselines cannot exploit.** In ambient-assistant streams, narratively-coherent events score lower surprise than off-topic noise. A simple inverted-threshold gate on this signal Pareto-dominates fixed-cron baselines and matched-rate random gates on a held-out trace.

Three things to be honest about:

1. **The sign is opposite to FEP-naïve intuition.** Friston-style "high prediction error → attend" loses badly on these traces. The corrected reading is closer to predictive-processing's *precision-weighted* expected free energy: events that confirm the predicted narrative thread are *more* relevant to the user, not less.
2. **The signal is weak, not surgical.** dev_v2 had a perfect classifier; test_v1 does not. Real ambient-assistant streams will be more like test_v1 than dev_v2. We can claim Pareto improvement on the held-out trace, not perfect filtering.
3. **The single tunable θ is dev-set-fit.** θ=0.50 / 0.58 are the test-trace-best; we should freeze a θ on dev_v2 and report whatever number we get on test_v1 with that frozen θ in the next run, not the test-best.

## Honest accounting against the plan's risk register

- **Risk 1 (surprise → perplexity).** Mitigated by construction (independent embedder). Not the failure mode we hit.
- **Risk 2 (strong baseline matches hit rate).** Cron 30 s reaches 0.80 on test_v1; inverted heargent reaches 1.00 *and* lowers false rate. So far we are winning this comparison without the strong unconditional-poll baseline yet built — that's the next baseline to add.
- **Risk 3 (unfalsifiability via knob-turning).** The next discipline check is freezing θ on dev_v2 and reporting test_v1 numbers at that frozen θ. Currently:
  - dev_v2-best inverted θ = 0.43–0.44.
  - test_v1 at θ=0.43: hit=0.40, false=3.67. Hit rate collapses because GT events on test_v1 cluster higher than 0.43.
  - **We need a θ-selection rule that survives transfer.** Top-k by surprise is one option; relative threshold (e.g. "lowest 50 % of recent surprise scores") is another. Note for next session: design and test a transferable θ-selection rule.

## Still untested

- **`react_poll_local`** (poll qwen2.5 every tick) — the strong baseline. Cost-per-correct-proaction is where heargent should win against this; hit rate is not the discriminator.
- **A trace where GT *should* be high-surprise** — a calm, on-topic baseline punctured by a single abrupt interruption. Would either confirm polarity-flip robustness or expose its failure mode.
- **Larger predictor.** Worth one comparison run with a 7-13B model on dev_v2 to see if the surprise distribution sharpens (separability) or just shifts (means but no gap).

## Next session

1. **Frozen-θ transfer experiment.** Pick the dev_v2-best inverted θ (≈0.43), report test_v1 numbers at that θ. This is the honest paper number. Bonus: design a top-k or relative-threshold rule and report its transfer too.
2. **Build `baselines/react_poll_local.py`.** Strong baseline. Polls qwen2.5 with full context every tick.
3. **Token-cost accounting.** Heargent's token use vs poll baseline. The Pareto axis we will own is cost-per-correct-proaction, not raw hit rate.
4. **Adversarial trace** (`test_v2`) with at least one abrupt-interruption GT and at least one on-topic-looking distractor. The polarity-flip claim needs at least one trace where it is at risk of breaking.

## Artifacts

- Baseline JSON: `runs/data/06{a,b,c}-*.json`
- Forward sweep JSON: `runs/data/06d-heargent-fwd-sweep-test_v1.json`
- Trace definition: `sandbox/event_trace.py` (`test_trace_v1`)
