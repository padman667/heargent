# heargent — Prediction-Error-Gated Proactive LLM Agent

## Context

Hong Su's paper *Heartbeat-Driven Autonomous Thinking Activity Scheduling* (arXiv 2604.14178, Mar 2026) frames an interesting idea — give LLM agents a continuous internal rhythm so they stop being purely reactive — but the "biological" analogy is skin-deep (a fixed timer + learned dispatcher), the evaluation uses a toy LSTM on synthetic categorical traces, and no real LLM is ever in the loop.

This project takes the idea seriously. The goal is a **working LLM-agent prototype plus publishable paper** demonstrating that a neuroscience-grounded initiation signal — specifically, a **prediction-error gate** grounded in Friston's Free Energy Principle — produces meaningfully better proactive behavior than either reactive agents or Hong Su-style fixed-timer "heartbeats," at competitive cost.

User resources: local small model (Qwen2.5-7B or Llama-3.1-8B) for the always-on loop, Claude API for high-quality escalations and LLM-judge evaluation.

## Core thesis (one claim)

> **Gating self-initiation on model-expressed surprise about expected world state produces better proactive behavior than gating on time elapsed, at lower token cost than unconditional polling.**

Everything in v1 exists to test this single falsifiable claim. Decorative neuroscience analogies are cut.

## Architecture (v1 — deliberately minimal)

A single persistent Python loop. Two timescales: a **fast tick** (~5s) and a **slow consolidation pass** (end-of-episode).

At each fast tick:

1. **Observe** → pull new events from the world (sandbox: simulated inbox/calendar + scripted event stream; later: real adapters).
2. **Predict** → local model emits a one-sentence prediction of the next observable event + expected time-to-event, conditioned on a rolling memory window + intent stack.
3. **Score surprise** → on the next tick with a real observation, compute surprise as semantic distance between the prior prediction and the new observation, measured by an **independent embedding model** (not the acting model's own logprobs — see Risk 1).
4. **Arbiter (rule-based in v1)** → if `surprise > θ` OR the intent stack has a due item OR an explicit user turn arrived, escalate to Claude for an Act/Reflect decision. Otherwise keep predicting silently.
5. **Act or Reflect** → Claude produces either an external action (send message, create calendar entry, surface a notification) or an internal reflection (update intent stack, rewrite memory summary).
6. **Log** → persist `(tick, observation, prediction, surprise, action, outcome)` to SQLite.

Slow pass (end of episode or idle-threshold): summarize recent ticks into a memory entry, prune the intent stack, no counterfactual replay.

### What is *not* in v1 (deliberately deferred)

- Dopamine / ACh / 5HT neuromodulator scalars — numerology risk, re-introduce only if a v1 ablation shows a concrete deficit.
- Default Mode Network as a distinct module — it's already just the "low-surprise, non-empty-intent-stack" branch of the arbiter.
- Hippocampal-style counterfactual replay — own research project; out of scope for v1.
- Learned arbiter / RL over the policy — rule-based arbiter first; only learn if the rule hits a ceiling.
- Four-scale oscillator stack — two scales (tick + consolidation) is enough to test the thesis.

## Evaluation

**Environment: ambient-assistant sandbox.** A scripted world with an inbox, calendar, and injected event stream (flight delays, meeting moves, deadline approaches) with ground-truth-annotated "should have noticed" events at known times. Each agent runs against the same event trace for a fixed compressed-time budget (e.g. 2 hours sim-time).

Rejected alternatives: Voyager/Minecraft (stripping prompts invalidates comparison to prior Voyager numbers); a bespoke "living world" (a year of engineering, reviewers will suspect tuning).

**Primary metrics:**

| Metric | Definition |
|---|---|
| Proactive hit rate | Fraction of ground-truth events surfaced *before* the user asks, inside a policy window |
| False initiation rate | Unsolicited actions per hour that a held-out LLM-judge rates unhelpful |
| Time-to-notice | Median seconds between event injection and agent surfacing |
| Cost per correct proaction | Tokens + $ per true-positive initiation |

Hit rate / false rate / time-to-notice form a clean precision / recall / latency triple. Cost per correct proaction is what kills the "poll Claude every tick" baseline without needing to argue.

## Baselines (minimum credible set)

1. **Reactive ReAct** — acts only on explicit user turn. Floor.
2. **ReAct + fixed cron** — Hong Su's heartbeat, evaluated at 30s, 5min, and 30min intervals. Must beat the Pareto frontier, not just one interval.
3. **ReAct + unconditional poll** — asks Claude "anything worth doing?" every tick with full context. The *strong* baseline. Reviewers will claim heargent is just this with extra steps; beating it on cost-per-correct-proaction is where the surprise gate earns its keep.
4. **Random-gate ablation of heargent itself** — replace the surprise gate with a random gate matched to heargent's firing rate. Proves the *signal* matters, not just the firing frequency.

Skip Voyager / AutoGPT comparisons — different problem, wasted pages.

## Risk register

1. **Surprise collapses to perplexity.** If surprise is computed from the acting model's own logprobs, it's just dressed-up perplexity and trivially gamed. **Mitigation:** compute surprise via an independent embedding model or separate judge LLM. Pre-register the metric before any test runs.
2. **Strong baseline (unconditional polling) matches hit rate.** Then the story collapses to "ours is cheaper." **Mitigation:** embrace it. Frame the paper as *selective initiation at Nx lower cost*, not as a new capability. Cost-quality Pareto plots are publishable and honest.
3. **Unfalsifiability via knob-turning.** Threshold θ, tick rate, and memory window are all tunable. **Mitigation:** freeze all hyperparameters on a dev event trace before running the test trace. Report a single frozen config plus one sensitivity sweep. This is the single most common failure mode of agent papers and the one Hong Su's work exemplifies.

## Milestones

| # | Duration | Deliverable |
|---|---|---|
| M1 | 2 wks | Sandbox + event generator + ground-truth annotation + scoring harness. **Build this before the agent.** |
| M2 | 3 wks | Baselines 1–3 running end-to-end on a dev trace. First Pareto plot — already a partial paper. |
| M3 | 3 wks | heargent v1: fast tick + prediction + independent-embedding surprise + rule-based arbiter + intent stack + SQLite. Local model on fast path, Claude on escalation. |
| M4 | 3 wks | Ablations: random-gate, surprise-from-logprobs-only, no-intent-stack, θ sweep. Freeze config on dev. |
| M5 | 2 wks | Test trace run, final numbers, 3–4 qualitative case studies where heargent proactively acts and baselines don't. |
| M6 | 3 wks | Paper draft + figures + open-source release of code *and sandbox*. The sandbox is half the contribution. |

Total: ~16 focused weeks to a submittable draft. Double for realistic slippage.

## Files to create first

Greenfield directory. Build in this order — the sandbox before the agent:

- `sandbox/event_trace.py` — ground-truth event generator + scoring harness
- `sandbox/world.py` — simulated inbox/calendar state + observation API
- `baselines/react_cron.py` — Hong Su heartbeat at configurable intervals (direct comparison target)
- `baselines/react_reactive.py` — pure reactive ReAct (floor)
- `baselines/react_poll.py` — unconditional poll-every-tick (strong baseline)
- `agent/predictor.py` — local-model prediction head + independent-embedding surprise scorer
- `agent/arbiter.py` — rule-based salience arbiter + intent stack
- `agent/loop.py` — the single persistent tick loop tying it all together
- `agent/storage.py` — SQLite episodic log schema
- `eval/run_trace.py` — runs any agent against an event trace, emits metrics JSON
- `eval/plot_pareto.py` — produces the cost-quality Pareto figures

## Verification

- **Sandbox unit tests:** deterministic event traces replay identically; scoring harness correctly identifies hand-seeded true/false positives.
- **Baseline sanity:** reactive ReAct scores zero proactive hits; ReAct+cron@30s matches unconditional polling on hit rate but loses badly on cost; these are pre-conditions for the experiment being valid at all.
- **End-to-end demo:** 30-minute compressed sandbox run of heargent vs. the three baselines, producing a Pareto plot and at least one qualitative case where heargent surfaces a seeded event the cron baseline misses within its window.
- **Ablation sanity:** random-gate heargent matches firing *rate* but degrades hit-rate — this is the key internal check that the surprise signal is load-bearing. If it doesn't, the thesis is falsified and we pivot before writing the paper.

## Scope boundary

This plan covers **v1 only**: the minimum system capable of falsifying (or validating) the one-claim thesis above. Neuromodulators, replay, learned arbiters, multi-scale oscillators, and Dream Mode are **deliberately out of scope** and gated behind v1 results. If v1 fails or barely beats baselines, the neuroscience stack does not save it — it makes it harder to debug.
