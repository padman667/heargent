# Run 03 — Cron Sweep on Hardened Trace (dev_v2)

**Date:** 2026-04-18
**Milestone:** M2 (baselines producing differentiable results)
**Trace:** `sandbox.event_trace.dev_trace_v2` — tighter windows, off-cron injections, 4 distractors
**Agents:** `react_reactive`, `cron_keyword_30s`, `cron_keyword_300s`

## Goal

Run 02 showed `dev_trace_v1` couldn't differentiate cron intervals (both 30 s and 300 s hit 100 %). This run hardens the trace and re-measures. Concrete aims:

1. First event has a **20 s window** — even 30 s cron should miss it.
2. Off-cron-boundary injections (`flight_delay` at t=35, `meeting_moved` at t=100) create miss opportunities for 300 s cron.
3. Four **distractor** events (not ground-truth-flagged) mixed into the observation stream — any agent that replays observations verbatim will generate false initiations on them.
4. Verify the false-initiation path (`false_initiation_rate_per_hour`) is now computed from a non-zero baseline.

## Trace v2 structure

**Ground truth (5):**

| id | sim_time (s) | window (s) | window end | keywords |
|---|---|---|---|---|
| fire_alarm | 5 | 20 | 25 | fire, alarm |
| flight_delay | 35 | 50 | 85 | flight, delay |
| meeting_moved | 100 | 180 | 280 | meeting, moved |
| deadline | 400 | 600 | 1000 | deadline, quarterly |
| dentist_cancel | 700 | 300 | 1000 | dentist, cancelled |

**Distractors (4):** `news_digest` (t=50), `weather_nominal` (t=200), `marketing_newsletter` (t=350), `system_heartbeat` (t=550).

Trace duration: 1030 s. Tick: 5 s → 206 ticks.

## Refactor to support distractors

Run 02 exposed a type conflation: `dev_trace_v1()` returned `list[GroundTruthEvent]`, so "events to inject into the world" and "events the agent should be scored against" were the same list. Distractors break that — they need to be observed but not scored.

Introduced `sandbox.event_trace.Trace`:

```python
@dataclass(frozen=True)
class Trace:
    name: str
    events: list[Event]               # everything injected into the world
    ground_truth: list[GroundTruthEvent]  # subset with window + keywords
    duration_s: float                 # derived property
```

`eval/run_trace.py` now loads `trace.events` into the world but only scores against `trace.ground_truth`. CLI gained `--trace dev_v1|dev_v2`. Regression-tested: reactive agent on dev_v1 still reports `hit_rate=0.0, total_events=5, distractors=0` (unchanged from run 01).

## Commands

```sh
uv run python -m eval.run_trace --agent baselines.react_reactive:ReactiveAgent      --trace dev_v2 --out runs/data/03a-reactive-v2.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s  --trace dev_v2 --out runs/data/03b-cron30-v2.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword300s --trace dev_v2 --out runs/data/03c-cron300-v2.json
```

## Results

| Agent | hit_rate | false_init/h | median TTN (s) | notifs | misses |
|---|---|---|---|---|---|
| reactive | 0.00 | 0.00 | — | 0 | all 5 |
| cron 30s | **0.80** | 17.48 | 0.0 | 9 | `fire_alarm` |
| cron 300s | 0.40 | 24.47 | 200.0 | 9 | `fire_alarm`, `flight_delay`, `meeting_moved` |

Raw JSON in `runs/data/03{a,b,c}-*.json`.

### Notification accounting (sanity)

Each cron variant emits exactly 9 notifications: 5 ground-truth events + 4 distractors. The scorer then partitions:

- **cron 30 s (9 notifs):** 4 hits + 5 false.
  - 5 false = 4 distractors + 1 `fire_alarm` (replayed at t=30, outside its [5,25] window — correctly counted as a false initiation, not a late hit).
- **cron 300 s (9 notifs):** 2 hits + 7 false.
  - 7 false = 4 distractors + `fire_alarm` (reported at t=300) + `flight_delay` (t=300, window was [35,85]) + `meeting_moved` (t=300, window was [100,280]).
  - Hits: `deadline` (t=600, in [400,1000]) and `dentist_cancel` (t=900, in [700,1000]).

False-initiation rate units: 5 false / (1030 s / 3600 s/h) = 17.48/h ✓.

## What this validates

- **False-initiation path** now non-zero and reconciles with hand arithmetic. The scoring harness is now fully exercised (hits, misses, false initiations, out-of-window late reports).
- **`Trace` abstraction** cleanly separates injected events from scored events; distractors pass through `world.observe()` to agents unchanged.
- **Tight-window sensitivity**: `fire_alarm` with a 20 s window is missed by every cron interval we've tested (30 s and 300 s). This is the event type where a prediction-error-gated agent should shine: no fixed timer can respond in < 5 s after injection, but a surprise gate firing on new observations can.

## Notes on `median_time_to_notice_s`

Populated for both cron variants (cron 30 s: 0.0 s; cron 300 s: 200.0 s). The 200 s for cron 300 s reflects the two surviving hits landing mid-interval (`deadline` at t=600 injected at 400 → TTN=200; `dentist_cancel` at t=900 injected at 700 → TTN=200). Median of a 2-sample list with current logic takes the upper sample, so both being 200 gives exactly 200.

## What this clarifies about the project thesis

Before v2, the baselines were ties. Now:

- There's already a clean Pareto story between **cron 30 s** (more hits, still 17/h false) and **cron 300 s** (fewer hits, more false — dominated on both axes because it misses more events that it still reports outside-window).
- **Cron 300 s is Pareto-dominated** by cron 30 s on this trace. So for the paper: the interesting comparison is not "heargent vs. cron at multiple intervals" but "heargent vs. cron 30 s (the best cron on this trace) vs. LLM-polled cron."
- The `fire_alarm` event is the single most discriminative case — it's already unwinnable for timer-based approaches given the 5 s tick granularity, but an agent that gates on **surprise over each new observation** can notify within one tick. That's the cleanest qualitative case study in the paper.

## Tooling status (end of session)

- `ollama 0.21.0` running (background).
- `qwen3:4b` installed (2.5 GB), verified via HTTP API with `"think": false` flag — responds in ~1 s for short prompts.
- `nomic-embed-text` pulled, not yet integrated.
- `ANTHROPIC_API_KEY` still unset (not yet needed).

## Next session

1. Build `agent/predictor.py` — wrap ollama qwen3:4b as a predictor that emits a one-sentence prediction of the next observable event given rolling context.
2. Build `agent/surprise.py` — use nomic-embed-text to compute cosine distance between prediction and actual observation.
3. Wire into `agent/loop.py` as heargent v1 with a simple rule-based arbiter (surprise > θ → surface).
4. Run heargent v1 on dev_v2. Specifically measure: does it catch `fire_alarm` within the 20 s window?
5. Decide: local qwen3 predictor vs. Claude Haiku predictor A/B (see plan Risk 1: surprise collapsing to perplexity — mitigate by keeping predictor and surprise-scorer independent).
