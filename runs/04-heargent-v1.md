# Run 04 — Heargent v1 first thesis test (dev_v2)

**Date:** 2026-04-18
**Milestone:** M3 (first LLM in the loop — prediction-error-gated agent end-to-end)
**Trace:** `sandbox.event_trace.dev_trace_v2`
**Agent:** `agent.loop:HeargentV1` (θ=0.30, predictor=qwen2.5:3b-instruct, surprise=nomic-embed-text)

## Goal

First real test of the thesis: does a prediction-error-gated agent catch `fire_alarm` (20 s window) — the one event every cron baseline misses?

## Architecture under test

Two-model loop, end-to-end via ollama HTTP:

```
tick():
    for each new observation:
        surprise = cosine_distance( embed(last_prediction) , embed(obs) )
        if surprise > θ and not already reported:
            world.surface(obs.content)
    last_prediction = predictor.predict(history, sim_time)
```

- **Predictor:** `qwen2.5:3b-instruct` (chosen over `qwen3:4b` after qwen3 proved ignore instruction-following — reasoning tokens bleed into `content` even with `think=false`). Temperature 0.4, one-sentence constraint via system prompt.
- **Surprise scorer:** `nomic-embed-text` — deliberately independent of predictor (Risk 1 mitigation: if we scored surprise from the predictor's own logprobs, it would just be perplexity).
- **Bootstrap:** `last_prediction = "No notable events expected in the next minute."` (so the first real observation has *something* to be surprising vs.).
- **θ = 0.30** — picked as the midpoint between "similar pair" (0.12) and "unrelated pair" (0.45) in a pre-run calibration. **Not frozen; first-pass.**

## Commands

```sh
uv run python -m eval.run_trace --agent agent.loop:HeargentV1 --trace dev_v2 --out runs/data/04-heargent-v1-dev_v2.json
```

Wall clock: ~5 s for the full 1030 s trace (9 predictor calls + 18 embedding calls, all local).

## Headline result

| Agent | hit_rate | false_init/h | median TTN (s) | notifs | misses |
|---|---|---|---|---|---|
| reactive (floor) | 0.00 | 0.00 | — | 0 | all 5 |
| cron 30 s | 0.80 | 17.48 | 0.0 | 9 | `fire_alarm` |
| cron 300 s | 0.40 | 24.47 | 200.0 | 9 | 3 events |
| **heargent v1 (θ=0.30)** | **1.00** | **13.98** | **0.0** | 9 | — |

**Heargent v1 Pareto-dominates every cron baseline on every metric:** strictly higher hit rate, strictly lower false-initiation rate, equal or better time-to-notice. Crucially, `fire_alarm` is caught at TTN=0 s — inside its 20 s window — which no timer-based agent can do on a 5 s tick with interval ≥ 30 s.

## Per-event surprise values (the interesting bit)

All nine events in the trace, sorted by surprise (threshold θ=0.30):

| event_id | type | surprise | surfaced? | prior prediction |
|---|---|---|---|---|
| deadline | GT | 0.321 | ✓ | "Flight UA123 delay will officially be announced..." |
| meeting_moved | GT | 0.339 | ✓ | "Flight UA123 passengers informed about new departure time." |
| flight_delay | GT | 0.385 | ✓ | "Building A evacuation continues..." |
| fire_alarm | GT | 0.403 | ✓ | "No notable events expected in the next minute." (bootstrap) |
| dentist_cancel | GT | 0.406 | ✓ | "Flight delay for UA123 to Berlin set to end..." |
| news_digest | distractor | 0.429 | ✓ | — |
| weather_nominal | distractor | 0.486 | ✓ | — |
| marketing_newsletter | distractor | 0.516 | ✓ | — |
| system_heartbeat | distractor | 0.532 | ✓ | — |

All 9 are above θ=0.30, so all 9 fire. **The thesis would be cleanly supported if GT events were systematically more surprising than distractors. They are not.** On this trace the ordering is actually *inverted*: all four distractors have higher surprise than every GT event.

## What this validates

1. **End-to-end pipeline works with an LLM in the loop.** Predictor emits clean one-sentence predictions; embedder scores them deterministically against observations; the Agent protocol surfaces notifications correctly; scoring harness accepts the output unchanged. ~5 s wall clock for 1030 s of sim time is comfortably within budget.

2. **The thesis's strongest point is robust: prediction-error gating catches tight-window events that *no* fixed timer can.** Fire alarm is notified at TTN=0 s — the first observation tick after injection. Cron 30 s cannot match this because it only fires every 30 s; cron 300 s can't match either. This is the cleanest qualitative case for the paper.

3. **Selectivity is not yet validated.** At θ=0.30, the agent surfaces everything. The "heargent is Pareto-better than cron 30 s" result is partly driven by cron 30 s *also* emitting a late fire_alarm notification as a 5th false-init, while heargent's fire_alarm is in-window. It is not driven (yet) by surprise discriminating signal from noise.

## The problem this surfaces

**Raw semantic surprise alone does not separate relevance from novelty.** This was foreseeable in hindsight: a marketing newsletter *is* semantically distant from "flight delay" predictions. So is a fire alarm. The embedder doesn't know which kinds of distance the user cares about.

There is no choice of θ on this trace that catches the 5 GT events and rejects the 4 distractors — they are **interleaved** (deadline at 0.321 ≪ news_digest at 0.429 ≪ fire_alarm at 0.403). Raising θ to reject distractors also rejects every GT event.

This is a **falsification of the naïve v1 thesis** ("surprise alone gates initiation well") and a **validation of the strong v1 thesis** ("surprise gating catches sub-heartbeat events that timers can't").

## Interpretation for the paper

The thesis splits cleanly into two sub-claims, and only one survives this run:

| Sub-claim | Status |
|---|---|
| (a) Surprise-gated initiation catches events too fast for any fixed timer. | **Supported** — fire_alarm, TTN=0 s. |
| (b) Surprise alone discriminates signal from noise better than a random gate would. | **Not supported at θ=0.30 on dev_v2.** All 4 distractors also pass. |

Sub-claim (a) is already publishable-novel — no prior work on LLM heartbeats tests this. Sub-claim (b) requires either a stronger surprise signal (intent-conditioned prediction) or a second gate (relevance check) — **which is exactly the role the plan reserves for the "arbiter" / intent-stack / escalation-to-Claude step deferred past v1 minimum**. That future work is now well-motivated, not speculative.

## Still untested / open

- **Reproducibility of surprise values.** Predictor temperature = 0.4 introduces per-run variance in the prediction text, which in turn shifts surprise scores slightly. For the frozen-config test we should re-run with `temperature=0.0` and log the scores.
- **Strong baseline missing.** `react_poll` (unconditional Claude-every-tick) is still the reviewer's obvious counter-argument. Heargent should beat it on cost-per-correct-proaction, not hit rate.
- **θ sweep.** We should plot hit rate and false rate as functions of θ ∈ {0.25, 0.30, 0.35, 0.40, 0.45, 0.50} to show the gate's ROC curve explicitly.
- **Random-gate ablation** (matched firing rate) — proves whether the surprise *signal* (not just the firing *frequency*) is load-bearing. Given that distractors score higher than GT, a random gate might plausibly match on this trace.

## Next session

1. Re-run with `temperature=0.0` in predictor for deterministic surprise scores.
2. θ sweep on dev_v2 → ROC curve figure.
3. Random-gate ablation: same firing rate (9/1030 s), random selection — does it match heargent's hit rate?
4. Build `baselines/react_poll_local.py` — the strong baseline (poll qwen2.5 every tick).
5. Start planning the intent-stack / relevance gate (deferred from v1 but now well-motivated by this run's negative result on sub-claim (b)).

## Artifacts

- Metrics JSON: `runs/data/04-heargent-v1-dev_v2.json`
- Code: `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/loop.py`
