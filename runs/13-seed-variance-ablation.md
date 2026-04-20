# Run 13 — Seed-Variance Ablation on the M6a C3 Content-vs-Random Claim (M7)

**Date:** 2026-04-20 (pre-registration). Results section appended post-eval.
**Milestone:** M7 — harden M6a's C3 claim ("content signal load-bearing under the widened band") across N=20 RandomArbiter seeds. Same frozen config as M6a; only `RandomArbiter.seed` varies.
**Pre-registration SHA:** *to be filled in at the pre-reg commit* (pre-reg doc + `--arbiter-random-seed` CLI wiring committed together as one SHA; no eval before this commit). **Predecessor:** M6a results SHA `d7252f7`.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, predictor seed=42, deterministic throughout. Local-only; no Claude API. Only `RandomArbiter.seed` varies across the 60 random-arbiter cells.

## Goal

M6a (runs/12, SHA `d7252f7`) closed as a full success: hit ≥ 0.80 on every trace at 6.8–11.3× lower tok/hit than poll, all 5 pre-registered criteria pass under one frozen config. The C3 claim ("content signal load-bearing; content beats V2-wide random on ≥ 2 of 3 traces by Δhit ≥ 0.20 OR Δfalse/h ≥ 5.0") currently rests on a single Bernoulli stream (`RandomArbiter(p=0.75, seed=42)`). A reviewer can reasonably say: *seed=42 was lucky; resample random and the delta shrinks below the bar.*

This pass hardens C3 by running the random-arbiter cells across N=20 pre-committed seeds under the otherwise-frozen M6a config, then evaluating a robust version of C3 against the distribution. It is not a new mechanism — same frozen config, same band, same V2 prompt, same predictor / surprise / bootstrap policy as M6a. Only the seed of the null-ablation arbiter varies.

Expected outcome: the C3 passes on test_v1 and test_v2 survive in the vast majority of seeds; dev_v2 remains at-or-below the bar in every seed (GT-dense trace; not a lucky seed). If instead C3 is seed-fragile, the paper must report that honestly and the main attribution claim softens.

## Design reasoning (why 20 real runs, not offline replay)

Two viable approaches; chose the first for traceability.

| | CLI flag + N=20 real runs (chosen) | Offline replay from 12d/e/f surprise_log |
|---|---|---|
| Code path | identical to every existing M4/M5/M6 random cell | new tool, needs equivalence proof |
| N feasible | ~20 (each run takes ~30–60 s; 60 cells ≈ 45 min) | 1000+ (offline, microseconds per seed) |
| Reviewer trust | one codepath, one schema, same per-event JSON dumps | "your replay ≠ real runs" is a free attack surface |
| Determinism verification | seed=42 in the batch must match 12d/e/f byte-for-byte | same check also needed, plus replay correctness |
| Risk | ollama transient failures across 60 runs | replay bug that silently produces wrong numbers |

Real runs are the defensible path. N=20 is enough for a usable quantile-based CI and cheap enough to run unattended.

## Pre-registered artifacts (frozen before any seed runs)

### Seed list (committed before any eval)

```
SEEDS = [42, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
```

20 seeds; `seed=42` first so that the first batch of 3 runs is a seed=42 equivalence check against M6a's `12d/e/f`. No post-hoc seed addition or removal.

### Frozen config (unchanged from M6a)

- Agent: `agent.loop:HeargentZAWide` (M6a, `z_skip=+1.5`, band `[−0.5, +1.5]`).
- Arbiter mode: `random` with **`p = 0.75`** (pinned from run 12a, same as M6a).
- Predictor: qwen2.5:3b-instruct, temp=0, seed=42. Unchanged.
- Surprise: nomic-embed-text. Unchanged.
- Window=16, min_window=4. Unchanged.
- Traces: dev_v2, test_v1, test_v2. Unchanged.

Only `RandomArbiter.seed` varies across the 60 cells. The content-arbiter cells (`12a/b/c`) are **not** re-run; their numbers are the fixed reference for Δ computations.

Content reference (fixed, from runs/data/12a/b/c):
- dev_v2: hit = 1.00, false/h = 0.00, misses = [].
- test_v1: hit = 0.80, false/h = 3.67, misses = [`package_arrival`].
- test_v2: hit = 1.00, false/h = 0.00, misses = [].

### Pre-flight determinism check (go/no-go gate)

Before any multi-seed claim is made, the three `seed=42` runs in the new batch (`13-seed42-<trace>.json`) must **bit-match M6a's `12d/e/f`** on `hit_rate`, `false_initiation_rate_per_hour`, `total_notifications`, and `misses` (exact list):

| Trace | M6a (12d/e/f) hit / false-h / notif / misses |
|---|---|
| dev_v2 | 1.00 / 3.4951456310679614 / 6 / [] |
| test_v1 | 1.00 / 11.020408163265307 / 8 / [] |
| test_v2 | 0.80 / 15.0 / 8 / [`security_breach`] |

If seed=42 does not match, **halt immediately** — the `--arbiter-random-seed` wiring is broken or the RandomArbiter's classify order has drifted. Investigate before any further seed runs; do not report.

### Pre-registered success criteria (frozen before any multi-seed run)

Frozen before any of the 20 seeds execute. Each headline claim cites which criterion it passed / failed.

Let `Δhit(trace, seed) = hit_content(trace) − hit_random(trace, seed)` and `Δfalse(trace, seed) = false_content(trace) − false_random(trace, seed)` (positive Δhit and negative Δfalse both mean "content better" under the sign convention that false/h is lower-is-better). For the content values use `12a/b/c`; for the random values use the 20-seed batch.

**S1 — Determinism: seed=42 equivalence.** seed=42 run matches `12d/e/f` on the four named fields exactly. Hard gate; non-match halts the matrix.

**S2 — C3 on test_v1, seed-robust.** Across 20 seeds, the fraction of seeds where test_v1 `(content_false/h − random_false/h) ≤ −5.0` (i.e. content_false/h at least 5.0/h lower than random_false/h) is **≥ 0.90** (≥ 18 of 20 seeds).

**S3 — C3 on test_v2, seed-robust.** Across 20 seeds, the fraction of seeds where either `hit_content − hit_random ≥ 0.20` **or** `content_false/h − random_false/h ≤ −5.0` is **≥ 0.90** (≥ 18 of 20 seeds).

**S4 — Honest reporting of dev_v2.** Across 20 seeds, the fraction of seeds where dev_v2 meets the C3 bar (`content_false/h − random_false/h ≤ −5.0`) is reported as a number. No pass/fail threshold; this is a sanity check that the M6a observation ("GT-dense trace; random at high p can tie content on hit rate") is a regime effect, not a seed artifact.

**S5 — Budget bound invariant.** Random-arbiter call count per trace is invariant across seeds (structural; seed only changes YES/NO choices, not which events go to the arbiter). Verification: `arbiter_calls` across all 60 cells must equal exactly **{dev_v2: 4, test_v1: 8, test_v2: 7}**. A single deviation indicates a bug.

### Decision rules (binding, written in advance)

- **S1 fails** → halt; do not report multi-seed result. Fix the wiring.
- **S1 passes, S2 and S3 both pass** → C3 robustness established. Headline tightens to "content signal load-bearing in ≥ 90 % of RandomArbiter seed draws on two of three traces."
- **S1 passes, exactly one of S2 / S3 passes** → partial hardening. Report explicitly: which trace holds, which doesn't. C3 claim in the paper becomes trace-specific.
- **S1 passes, neither S2 nor S3 passes** → C3 was seed-fragile. Primary M6a attribution claim softens in the paper; the Δfalse/h CI becomes the headline, not the point estimate. This is the null-result outcome.
- **S5 fails** → bug in gate logic; halt and investigate.

No raising of N, no seed substitution, no post-hoc criterion redefinition.

## Architecture changes (minimal, additive)

Three-line change across two files. Random-arbiter seeding is already supported (`RandomArbiter(p, seed=42)` accepts a seed); only the threading from CLI down needs wiring.

1. **`agent/loop.py` — `HeargentZA.from_trace`**: add keyword parameter `random_seed: int = 42` and pass through to `RandomArbiter(random_p, seed=random_seed)`. `HeargentZAWide` inherits this verbatim. `HeargentZA` default behaviour (seed=42) preserved so M4 / M5 / M6a reruns produce identical output.

2. **`eval/run_trace.py`**:
   - Add `arbiter_random_seed: int | None = None` parameter to `_load_agent`.
   - Thread `random_seed=arbiter_random_seed` through the `from_trace` call when `mode == "random"` and the seed is not None.
   - Add `--arbiter-random-seed` CLI argument (type=int, default=None) after `--arbiter-random-p`.
   - Propagate to `metrics["arbiter_random_seed"] = args.arbiter_random_seed` so each JSON records the seed used.

3. **`agent/arbiter.py`** — unchanged. `RandomArbiter.__init__(self, p, seed=42)` already accepts seed.

Nothing else changes. Content arbiter code path, predictor, surprise scorer, `HeargentZAWide` / `HeargentZA` / `HeargentZ` / `HeargentZIntent` / `HeargentAgent`, all baselines, scoring harness — all untouched.

**Backward compatibility:** omitting `--arbiter-random-seed` passes `None` through, which routes to `from_trace`'s default `random_seed=42`. Existing invocations (M4 / M5 / M6a) produce byte-identical output.

## Critical files

- `agent/loop.py:362–385` — `HeargentZA.from_trace`. Add `random_seed=42` kw.
- `eval/run_trace.py:94–120` — `_load_agent`. Add seed param + thread through.
- `eval/run_trace.py:123–167` — `main`. Add `--arbiter-random-seed` arg.
- `agent/arbiter.py:111–141` — `RandomArbiter`. **Not touched.**
- `runs/data/12d/e/f*.json` — reference for S1 equivalence check. **Not touched.**

## Reproduce

Ollama 0.21.0 must be running locally with `qwen2.5:3b-instruct` and `nomic-embed-text` pulled. All runs deterministic (temp=0, predictor seed=42; arbiter seed varies by cell).

```sh
# HeargentZAWide random-arbiter batch, 20 seeds × 3 traces = 60 cells.
for seed in 42 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do
  for trace in dev_v2 test_v1 test_v2; do
    uv run python -m eval.run_trace \
      --agent agent.loop:HeargentZAWide \
      --trace $trace \
      --arbiter-mode random \
      --arbiter-random-p 0.75 \
      --arbiter-random-seed $seed \
      --out runs/data/13-seed${seed}-${trace}.json
  done
done
```

## Non-goals for this pass

- Do not touch the content-arbiter cells (`12a/b/c`). They are the fixed reference.
- Do not vary `p`. `p = 0.75` is fixed by the matched-firing-rate protocol.
- Do not vary predictor seed / temperature. Predictor is temp=0 / seed=42 throughout.
- Do not add new traces. Same three traces as M6a.
- Do not change the band. `[−0.5, +1.5]` is the M6a frozen band.
- Do not rerun the content cells. If C3 robustness fails, the headline softens — we do not attempt to compensate by retuning.
- Do not change `RandomArbiter`'s internal RNG (stdlib `random.Random`). Its seed stream is the null ablation; changing it would invalidate the ablation's pedigree.

This pass is strictly narrower than M6a: one axis (RandomArbiter.seed), 60 cells, one verification gate (S1), three criteria (S2 / S3 / S4), one report.

## Results

*Filled in after the 60-cell matrix runs.*
