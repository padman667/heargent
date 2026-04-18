# Run 01 — Reactive Baseline Sanity Check

**Date:** 2026-04-18
**Milestone:** M1 vertical slice (first end-to-end pipeline run)
**Agent:** `baselines.react_reactive:ReactiveAgent`
**Trace:** `sandbox.event_trace.dev_trace_v1` (5 hand-crafted events)

## Goal

Prove the M1 pipeline works end-to-end: `World` → scripted event injection → `observe()` → agent `tick()` → scoring → metrics JSON. The reactive agent is the *floor* baseline — it never self-initiates — so this run is specifically a **negative control**. It should produce zero proactive hits and zero false initiations. Anything else would mean the scoring logic is broken.

## What was built in this session

| File | Purpose |
|---|---|
| `sandbox/world.py` | Minimal `World` with `advance()`, `observe()`, `surface()` + `Event`/`Notification` dataclasses |
| `sandbox/event_trace.py` | `dev_trace_v1()` — 5 ground-truth events with proaction windows + keywords |
| `eval/run_trace.py` | Harness: runs any agent against a trace, keyword-matches notifications to events, emits metrics JSON |
| `baselines/react_reactive.py` | `ReactiveAgent` — `tick()` is a no-op; cost $0 |

No LLM calls. No API key needed. Pure Python, stdlib only.

## Trace definition

Five events injected at these sim-times, each with a proaction window (the window within which a notification counts as a hit):

| # | id | kind | sim_time (s) | window (s) | keywords |
|---|---|---|---|---|---|
| 1 | `flight_delay` | email | 10 | 300 | "flight", "delay" |
| 2 | `meeting_moved` | calendar_update | 60 | 300 | "meeting", "moved" |
| 3 | `weather_alert` | world_event | 120 | 300 | "weather", "rain" |
| 4 | `deadline` | email | 300 | 600 | "deadline", "quarterly" |
| 5 | `dentist_cancel` | calendar_update | 480 | 300 | "dentist", "cancelled" |

Total sim duration: **930 s** (last event end + 30 s buffer). Tick granularity: 5 s → 186 ticks.

## Command

```sh
uv run python -m eval.run_trace --agent baselines.react_reactive:ReactiveAgent
```

First invocation also created the `.venv` automatically (uv).

## Raw output (verbatim)

```json
{
  "hit_rate": 0.0,
  "false_initiation_rate_per_hour": 0.0,
  "median_time_to_notice_s": null,
  "total_notifications": 0,
  "total_events": 5,
  "hits": [],
  "misses": [
    "flight_delay",
    "meeting_moved",
    "weather_alert",
    "deadline",
    "dentist_cancel"
  ],
  "agent_name": "reactive",
  "cost_usd": 0.0,
  "tick_dt_s": 5.0,
  "trace_duration_s": 930.0
}
```

Wall-clock runtime: sub-second (no LLM calls, no I/O).

## What this validates

- **World / trace / observation plumbing**: events are loaded, `advance()` correctly moves `sim_time` forward, `observe()` drains the observable buffer once per tick, nothing crashes across 186 ticks.
- **Scoring harness**: correctly lists all 5 events as `misses` when the agent produces no notifications. `total_events` matches the trace length.
- **Agent protocol**: the harness can instantiate any class with `tick(observations, world, sim_time)` + `cost_usd()` + `name` attributes via `--agent module:Class`. Works for non-LLM agents out of the box.
- **Floor confirmed**: `hit_rate = 0.0` exactly, `total_notifications = 0`. The reactive agent is correctly useless, as the plan predicted.

## What this does *not* yet validate

- **True-positive path**: the scorer has never assigned a hit. We'll know the keyword-matching logic is right only after we run an agent that actually surfaces events. First real test will be the cron baseline.
- **False-positive path**: `false_initiation_rate_per_hour = 0.0` is trivially true when no notifications are emitted. Needs an agent that emits spurious notifications to verify.
- **`median_time_to_notice_s = null`** — expected given zero hits, but the percentile logic is also untested.

These are next session's job (cron baseline + first agent that produces notifications).

## Notes for next session

- `ollama` not installed; `ANTHROPIC_API_KEY` not set. Neither is needed for the cron baseline (pure keyword-rule) — we can keep going LLM-free for one more step.
- The keyword matcher is case-insensitive AND-match on all keywords in a tuple. Consider whether `("meeting", "moved")` is too strict once we add noisy agents — a less constrained OR-match may be fairer. Revisit after cron baseline produces real notifications.
- Hit-to-notification matching is first-come-first-served: the first notification that lands in a window and matches keywords "claims" that event. Spurious earlier notifications for the same event would be counted as false initiations, which is the intended behavior.
