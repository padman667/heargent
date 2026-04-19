# Run 10 — Surprise + Lightweight-Content Arbiter (M4)

**Date:** 2026-04-19 (pre-registration).
**Milestone:** M4 — surprise + lightweight-content arbiter, targeting the test_v2 failure from runs 08/09.
**Status:** pre-registered; eval not yet executed.
**Pre-registration SHA:** TBD (this commit). **Implementation SHA:** TBD (subsequent commit).
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, seed=42, deterministic.

## Goal

Recover test_v2 hit rate from 0.40 (plain HeargentZ, run 08) to ≥ 0.80 **at a total token cost per hit lower than `react_poll_local` (7629 tok/hit)**, without regressing dev_v2 / test_v1, and without introducing Claude API or a larger local model. The mechanism under test: use HeargentZ's rolling-window z as a cheap first stage and call a second 3B content classifier on events whose z sits in a pre-registered borderline band, skipping the classifier entirely for confident-surf and confident-skip events.

## Design reasoning (why content, why borderline-only)

Run 09 falsified intent-conditioned prediction three ways: the primary test_v2 criterion (hit ≥ 0.80) failed at 0.40; the A-vs-B oracle ceiling failed (both < 0.80); and the placebo-null failed in the opposite direction (placebo 0.60 > briefing 0.40). Per-event logs showed every intent cell emitting the same "FIRE … evacuate …" prediction after fire_kitchen regardless of what the intent list said. **Conclusion from run 09:** anchoring the predictor via system-prompt text does not stop the 3B predictor from latching on recent-observation context, and user-context text in a prompt actively hurts a poller (poll+briefing degraded plain poll on dev_v2 and test_v1).

This run takes the opposite architectural bet: leave the predictor alone (with its known latching behaviour), and add a **post-hoc content arbiter** that never sees the prediction at all. Only the event text. The arbiter's job is decoupled from the gate's failure mode by construction: it cannot latch on a prior prediction because it never reads one.

The three-way split is motivated by the run 09 per-event z distribution. All missed GTs across traces sit in `z ∈ [+0.02, +0.85]`. All confidently-skipped distractors sit at `z > +1.76` (dev_v2) or at extreme-positive z (test_v1 `promo +11.70`). Strong-negative z's (−1.52, −2.76, −6.03) are all GTs that HeargentZ already catches. So:
- The **surface side** of the gate is already working; auto-surf on `z < −0.5` preserves every current hit at zero arbiter cost.
- The **skip side** fails precisely in the narrow band near zero, where latched predictions produce mildly positive z on events that would be obvious to a content-aware classifier (ER calls, security breaches, rent reminders, board meetings).
- The confidently-high positive z region (`z > +1.0`) is where clear distractors cluster (newsletters, marketing, routine status pings dissimilar to the rolling baseline). Auto-skip there preserves current skip accuracy and, again, costs zero arbiter calls.

The borderline `z ∈ [−0.5, +1.0]` band is where the latching predictor is producing ambiguous z and the content arbiter earns its keep.

**Bootstrap phase (first `min_window=4` events, z undefined) routes to the arbiter as well.** HeargentZ's bootstrap policy is "surface everything" — on test_v2 that contributes 3 of the 4 bootstrap false inits (`daily_briefing`, `status_ok`, `uptime_ping`). If the content arbiter works at all, it should catch these without further plumbing.

**Local-only again for M4.** qwen2.5:3b-instruct for the arbiter, nomic-embed-text for surprise. No Claude API; M4 extends the "cheap local stack is sufficient" paper frame. If M4 succeeds, the story reads: *pure local agent, pipeline total < 3k tokens per correct proaction on the adversarial trace where a local poller needs 7.6k*.

## Pre-registered artifacts (frozen before any eval run)

Everything in this section is committed before M4 eval begins. Any post-hoc modification is a protocol deviation and will be called out explicitly.

### Borderline band

```
z < -0.5          → auto-surface (trust strong negative z)
-0.5 ≤ z ≤ +1.0   → arbiter decides
z > +1.0          → auto-skip (trust strong positive z)
z is None         → arbiter decides   (bootstrap, first min_window=4 events)
```

Asymmetric around z=0 because strong-negative z is HeargentZ's working regime and every missed GT in run 09 sat on the positive side within `[+0.02, +0.85]`. The `+1.0` upper bound gives the missed GTs a comfortable margin (max +0.85 is 0.15 below the threshold) while placing clear distractors `weather_nominal +2.59`, `marketing_newsletter +1.76`, `system_heartbeat +1.76`, `promo_email +11.70` cleanly in auto-skip.

### Arbiter system prompt

```
You are a triage filter for a proactive assistant. Decide whether a
single observed event warrants surfacing to the user right now.

Surface (YES) if the event describes:
 - an urgent physical safety or security issue (fire, break-in, breach)
 - an unexpected interruption to the user's personal life (medical,
   family emergency, home problem, childcare)
 - a financial or scheduling obligation with imminent action required
 - a production/on-call alert or outage

Do NOT surface (NO) if the event is:
 - routine status, uptime, or heartbeat notifications
 - marketing, promotional, or newsletter content
 - generic "all systems normal" or daily briefing summaries

Output exactly YES or NO, uppercase, on a single line. No explanation.
```

Arbiter user message: the event content string, verbatim. No kind field, no sim_time, no briefing, no intent list, no prior observations, no prior prediction.

Model: qwen2.5:3b-instruct. temperature=0.0, seed=42, max_tokens=5.

**Parsing:** search the first line of the response for the first standalone `YES` or `NO` (uppercase). Match → corresponding bool. No match (empty or malformed) → `False` (default-skip). Defaulting skip is deliberate: it prevents a malformed output from cascading into runaway false inits and biases toward silence on ambiguous output — the project's cost model already penalises unhelpful surfacings.

### Frozen agent config

**HeargentZA (content arbiter):**
- Gate: rolling-window z-score, `window=16`, `min_window=4`. Identical window math to `HeargentZ` from run 08.
- Band: `[−0.5, +1.0]` as above.
- Arbiter: `ContentArbiter` with the frozen prompt above.
- Predictor: qwen2.5:3b-instruct, temperature=0.0, seed=42. Unchanged from HeargentZ.
- Surprise scorer: nomic-embed-text. Unchanged.
- One config, three traces. No per-trace tuning.

**HeargentZA-random (null ablation):**
- Identical gate + band + predictor + surprise.
- `ContentArbiter` replaced by `RandomArbiter(p, seed=42)` where `p` is the empirical YES-rate of the real content arbiter on **dev_v2 only** (measured during the HeargentZA dev_v2 run and frozen before running the random ablation). Firing rate is matched; only the content signal differs.
- Same seed across all three random-ablation traces; the Bernoulli stream is deterministic given the fixed event order.

This mirrors run 05's random-gate ablation precisely: matched firing rate, isolated mechanism.

### Pre-registered success criteria

1. **Primary — test_v2 recovery.** HeargentZA on test_v2 hit ≥ 0.80 **and** tok/hit < 7629 (react_poll_local tok/hit on test_v2). This is the full falsifiable M4 claim: recover cron-30s hit rate on the adversarial trace at a total token cost below poll.
2. **No regression.** HeargentZA hit ≥ HeargentZ hit − 0.20 on each of dev_v2 and test_v1. The arbiter is additive over the plain gate and must not undo existing wins.
3. **Arbiter-content load-bearing.** HeargentZA beats HeargentZA-random on test_v2 by at least one of: Δhit ≥ 0.20, or Δfalse/h ≥ 5.0. If matched, arbiter content is not the mechanism — the arbiter is effectively a firing-rate knob.
4. **False-init bound on test_v2.** HeargentZA false/h on test_v2 ≤ cron 30 s (18.75). The bootstrap-phase arbiter must clean up at least two of the three bootstrap false inits (`daily_briefing`, `status_ok`, `uptime_ping`); failing to do so means the arbiter prompt is too permissive on routine-status content and the run is compromised even if primary passes.
5. **Arbiter-call budget realised.** Arbiter call count per trace ≤ 12 (bootstrap ≤ 4 + borderline band upper bound 8). Budget blowup means the `[−0.5, +1.0]` band is wider in practice than pre-analysis suggested and the cost claim loses its structural footing.

**Decision rules (written in advance, binding):**
- All five pass → M4 validated. Update paper framing: *surprise-gating + content triage recovers adversarial-regime performance at < 1 k tok/hit; local stack only.*
- Criterion 1 passes, 3 fails → content signal is null; arbiter is a firing-rate trick. Next session: report as null result, pivot to larger predictor (7–13B).
- Criterion 1 fails, 3 passes → arbiter is real signal but too weak alone on test_v2. Next session: pair content arbiter with a stronger predictor, or add Reflect loop (plan-C revival with a motivated reason).
- Criterion 1 fails, 3 fails → surprise-gating on 3B stack is not recoverable; open Claude-API work: Claude-as-arbiter on the same band, or Claude poll with aggressive context trimming.
- Criterion 2 fails → rollback; report regression.
- Criterion 4 fails → re-prompt the arbiter *after* full results are in (post-hoc; no M4 headline claim permitted from that variant).
- Criterion 5 fails → re-run with a tighter band as a *new* pre-registration (not an M4 amendment).

## Evaluation matrix

Frozen config on every cell. Each cell = one run, one JSON output in `runs/data/10-*.json`.

| Agent | dev_v2 | test_v1 | test_v2 |
|---|---|---|---|
| cron 30 s | (existing, run 02/03/08) | (existing, run 06) | (existing, run 08) |
| HeargentZ (no arbiter, frozen) | (existing, run 07) | (existing, run 07) | (existing, run 08) |
| react_poll_local | (existing, run 07) | (existing, run 07) | (existing, run 08) |
| **HeargentZA (content arbiter)** | new | new | new |
| **HeargentZA-random (null ablation)** | new | new | new |

6 new runs. Existing runs re-cited, not re-executed.

Each new JSON includes: git commit SHA (pre-registration commit), ollama version, model digests, and per-event `(prediction, observation, surprise, z, arbiter_call, arbiter_decision, surfaced)` dumps. The arbiter YES-rate on dev_v2 (from the HeargentZA dev_v2 run) is the pre-committed `p` for the random ablation — this is the one value that is intentionally *not* frozen before eval, because it is defined as a measurement on a prior cell.

## Architecture changes (additive only)

1. **`agent/arbiter.py`** (new) — `ContentArbiter(client, model)` with `classify(text: str) -> bool`, implementing the frozen prompt above. Same module exposes `RandomArbiter(p: float, seed: int = 42)` with the same `classify(text: str) -> bool` signature, for the ablation. Both are pure functions of their inputs; neither touches the predictor, the surprise scorer, or the trace.
2. **`agent/loop.py`** — add `HeargentZA(client, arbiter, z_surf_threshold=-0.5, z_skip_threshold=1.0, window=16, min_window=4, predictor_model=…, surprise_model=…)`. The gate decision is:
   ```
   z = self._z(s)
   if z is None:
       decision = arbiter.classify(ev.content)
   elif z < self.z_surf_threshold:
       decision = True
   elif z > self.z_skip_threshold:
       decision = False
   else:
       decision = arbiter.classify(ev.content)
   ```
   Rolling-window z math is copied verbatim from `HeargentZ._z` (not inherited — keeps HeargentZA self-contained so its pre-reg is not entangled with future changes to HeargentZ). `surprise_log` gains `arbiter_call` (bool) and `arbiter_decision` (bool | None).
3. **`eval/run_trace.py`** — one new flag `--arbiter-mode {content,random}`. The random mode pulls `p` from the corresponding dev_v2 content-arbiter JSON (hard-coded filename convention) and constructs `RandomArbiter(p, seed=42)`. If `HeargentZA` is loaded without `--arbiter-mode`, it defaults to `content`.

No changes to baselines, cron, plain `HeargentZ`, `HeargentZIntent`, the predictor, the surprise scorer, or the scoring harness. If M4 falsifies, reverting is a one-class + one-module delete.

## Results

*(To be filled in after the 6 new eval cells complete. Pre-registration is committed before any result is recorded.)*

### Full 6-cell matrix

| Agent | dev_v2 (hit / false-h / TTN / tok/hit) | test_v1 (hit / false-h / TTN / tok/hit) | test_v2 (hit / false-h / TTN / tok/hit) |
|---|---|---|---|
| *(baseline)* HeargentZ (no arbiter) | 1.00 / 0.00 / 0 / 444 | 0.80 / 7.35 / 0 / 260 | 0.40 / 7.50 / 0 / 1039 |
| *(baseline)* react_poll_local | 1.00 / 0.00 / 0 / 7711 | 1.00 / 0.00 / 0 / 7575 | 1.00 / 0.00 / 0 / 7629 |
| **HeargentZA (content arbiter)** | TBD | TBD | TBD |
| **HeargentZA-random (null ablation)** | TBD | TBD | TBD |

### Per-event prediction / surprise / arbiter — test_v2

*(To be filled in from `runs/data/10-*-test_v2.json` after eval.)*

### Pre-registered success criteria — evaluation

*(To be evaluated verbatim after eval. Each criterion passes or fails exactly as written above; no post-hoc redefinition.)*

1. Primary: **TBD**.
2. No regression: **TBD**.
3. Arbiter-content load-bearing: **TBD**.
4. False-init bound: **TBD**.
5. Arbiter-call budget: **TBD**.

### Headline findings

*(One paragraph per finding, each citing which criterion it ties to.)*

## Reproduce

Ollama 0.21.0 must be running locally with `qwen2.5:3b-instruct` and `nomic-embed-text` pulled. All runs deterministic (temp=0, seed=42).

```sh
# HeargentZA (content arbiter) × 3 traces
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace dev_v2  --arbiter-mode content --out runs/data/10a-heargent-za-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v1 --arbiter-mode content --out runs/data/10b-heargent-za-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v2 --arbiter-mode content --out runs/data/10c-heargent-za-test_v2.json

# HeargentZA-random (null ablation) × 3 traces.
# Requires `p` measured on runs/data/10a-heargent-za-dev_v2.json first.
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace dev_v2  --arbiter-mode random --out runs/data/10d-heargent-za-random-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v1 --arbiter-mode random --out runs/data/10e-heargent-za-random-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZA --trace test_v2 --arbiter-mode random --out runs/data/10f-heargent-za-random-test_v2.json
```

## Artifacts

- `runs/data/10a-heargent-za-dev_v2.json` … `10f-heargent-za-random-test_v2.json` — full 6-cell matrix (to be written).
- Every JSON contains `surprise_log` (per-event prediction/observation/surprise/z/arbiter_call/arbiter_decision/surfaced), `arbiter_yes_rate` (on the content cells), and standard eval scoring.
- Baselines cited for comparison: `runs/data/07c-heargent-comparison.json`, `runs/data/08f-heargent-z-sweep-test_v2.json` (HeargentZ rows), `runs/data/07a-poll-dev_v2.json`, `runs/data/07b-poll-test_v1.json`, `runs/data/08d-poll-test_v2.json` (plain poll rows).
- Code: `agent/arbiter.py` (new), `agent/loop.py::HeargentZA` (new), `eval/run_trace.py::--arbiter-mode` (new). All committed at the implementation SHA, which is a strict descendant of this pre-registration SHA.
