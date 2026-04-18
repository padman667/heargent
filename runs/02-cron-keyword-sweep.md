# Run 02 — Cron Keyword Baseline Sweep

**Date:** 2026-04-18
**Milestone:** M2 (baselines running)
**Agent:** `baselines.react_cron_keyword:CronKeywordAgent` at 30 s and 300 s intervals
**Trace:** `sandbox.event_trace.dev_trace_v1` (unchanged from run 01)

## Goal

Second baseline: the steelmanned Hong Su "fixed-timer" approach without any LLM in the loop. Agent accumulates observations each tick and, every `interval_s` sim-seconds, surfaces one notification per unreported event (verbatim content). Skips firing when its queue is empty, so it emits no noise between real events.

Specific aims:
1. Exercise the **true-positive path** of the scoring harness — run 01 only tested misses.
2. Produce the first real Pareto-shaped comparison: shorter cron interval = higher hit rate but lower time-to-notice; longer interval = lower hit rate or delayed.
3. Establish whether the current dev trace is sensitive enough to differentiate cron intervals.

## Commands

```sh
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s  \
  --out runs/data/02a-cron-30s.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword300s \
  --out runs/data/02b-cron-300s.json
```

## Results summary

| interval | hit_rate | false_init/h | median TTN | total_notifs | misses |
|---|---|---|---|---|---|
| 30 s  | 1.00 | 0.00 | 0.0 s   | 5 | 0 |
| 300 s | 1.00 | 0.00 | 180.0 s | 5 | 0 |

Raw JSON in `runs/data/02a-cron-30s.json` and `runs/data/02b-cron-300s.json`.

### 30 s interval (verbatim)

```json
{
  "hit_rate": 1.0,
  "false_initiation_rate_per_hour": 0.0,
  "median_time_to_notice_s": 0.0,
  "total_notifications": 5,
  "total_events": 5,
  "hits": [
    {"event_id": "flight_delay",   "notification_sim_time": 30.0,  "time_to_notice_s": 20.0},
    {"event_id": "meeting_moved",  "notification_sim_time": 60.0,  "time_to_notice_s": 0.0},
    {"event_id": "weather_alert",  "notification_sim_time": 120.0, "time_to_notice_s": 0.0},
    {"event_id": "deadline",       "notification_sim_time": 300.0, "time_to_notice_s": 0.0},
    {"event_id": "dentist_cancel", "notification_sim_time": 480.0, "time_to_notice_s": 0.0}
  ],
  "misses": [],
  "agent_name": "cron_keyword_30s",
  "cost_usd": 0.0,
  "tick_dt_s": 5.0,
  "trace_duration_s": 930.0
}
```

### 300 s interval (verbatim)

```json
{
  "hit_rate": 1.0,
  "false_initiation_rate_per_hour": 0.0,
  "median_time_to_notice_s": 180.0,
  "total_notifications": 5,
  "total_events": 5,
  "hits": [
    {"event_id": "flight_delay",   "notification_sim_time": 300.0, "time_to_notice_s": 290.0},
    {"event_id": "meeting_moved",  "notification_sim_time": 300.0, "time_to_notice_s": 240.0},
    {"event_id": "weather_alert",  "notification_sim_time": 300.0, "time_to_notice_s": 180.0},
    {"event_id": "deadline",       "notification_sim_time": 300.0, "time_to_notice_s": 0.0},
    {"event_id": "dentist_cancel", "notification_sim_time": 600.0, "time_to_notice_s": 120.0}
  ],
  "misses": [],
  "agent_name": "cron_keyword_300s",
  "cost_usd": 0.0,
  "tick_dt_s": 5.0,
  "trace_duration_s": 930.0
}
```

## What this validates

- **True-positive path works**: all 5 events correctly matched across both intervals. Keyword matching is case-insensitive AND-match against each event's tuple; verbatim event content satisfies it.
- **Time-to-notice computed correctly**: for the 300 s run, `flight_delay` was injected at `sim_time=10`, next cron fire at `sim_time=300`, so TTN = 290 s. The `deadline` event was injected exactly at a fire (`sim_time=300`), TTN = 0 s. The median computation (`180 s`) is plausible for 5 samples.
- **Queue + event-id dedup**: no duplicate notifications for the same event across ticks. `total_notifications == total_events == 5`.
- **`cost_usd = 0`**: wiring for cost reporting works.

## What this surfaces as a problem

**The dev trace cannot differentiate cron intervals.** Both 30 s and 300 s achieve `hit_rate = 1.0`. The reason: every event in `dev_trace_v1` has a proaction window ≥ 300 s, so even a 300 s-interval agent catches them all — it just reports later. The Pareto frontier collapses to a single point on hit-rate.

**Why this matters:** the paper's thesis ("prediction-error gate beats timer gate on the cost–quality Pareto") requires a trace where timer gates *miss events* or *fire spuriously*. The current trace tests neither. Both the cron baseline and (later) heargent will trivially score 100%.

**Fix (deferred to next session):** harden `dev_trace_v1` into `dev_trace_v2` with:
1. At least two events with windows < 300 s (so 300 s cron must miss them).
2. At least one event with a window < 60 s (so 30 s cron can miss too).
3. Events injected between cron-fire boundaries (to reveal latency penalty, not just miss penalty).
4. Distractor "world events" that are *not* ground-truth-flagged, to give an agent something to be spuriously excited about (tests false-initiation path).

Currently `false_initiation_rate_per_hour = 0.0` in both runs — the false-initiation scoring path is **still untested**. Needed for the evaluation to be credible.

## Why the cron baseline was built without an LLM

Two reasons: (a) Ollama was still installing in the background, and (b) it isolates the *cron cadence effect* from LLM reasoning quality. The pure-structural cron baseline establishes what "just timing, no intelligence" achieves on this trace. The next step is a cron baseline that replaces "verbatim replay" with "LLM decides whether to notify," which puts a real reasoner in the heartbeat and makes the comparison to heargent honest.

## Next session

- Harden trace → `dev_trace_v2` (tight windows + distractors).
- Re-run cron sweep on v2; expect hit-rate spread across intervals and non-zero false-initiation path exercised.
- Only then build `baselines/react_cron_llm.py` (LLM-in-the-heartbeat variant) — needs ollama + qwen3:4b ready.

## Tooling status

- `ollama 0.21.0` installed this session; server running in background.
- `qwen3:4b` pull in progress at end-of-session (~3 GB download).
- `nomic-embed-text` not yet pulled.
- `ANTHROPIC_API_KEY` still not set (not yet needed).
