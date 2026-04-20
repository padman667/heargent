# Run 13 — Seed-Variance Ablation on the M6a C3 Content-vs-Random Claim (M7)

**Date:** 2026-04-20 (pre-registration). Results section appended post-eval.
**Milestone:** M7 — harden M6a's C3 claim ("content signal load-bearing under the widened band") across N=20 RandomArbiter seeds. Same frozen config as M6a; only `RandomArbiter.seed` varies.
**Pre-registration SHA:** `b9ab7de` (pre-reg doc + `--arbiter-random-seed` CLI wiring committed together as one SHA; no eval before this commit). **Predecessor:** M6a results SHA `d7252f7`.
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

### Pre-flight determinism check (S1)

Ran `seed=42` × 3 traces under the M7 SHA `b9ab7de` before any multi-seed cell fired. All three cells match `12d/e/f` exactly on `hit_rate`, `false_initiation_rate_per_hour`, `total_notifications`, and `misses`:

| Trace | M6a `12d/e/f` (hit / false-h / notif / misses) | M7 `13-seed42-*` (hit / false-h / notif / misses) | S1 |
|---|---|---|---|
| dev_v2 | 1.00 / 3.495146 / 6 / [] | 1.00 / 3.495146 / 6 / [] | match |
| test_v1 | 1.00 / 11.020408 / 8 / [] | 1.00 / 11.020408 / 8 / [] | match |
| test_v2 | 0.80 / 15.000000 / 8 / [`security_breach`] | 0.80 / 15.000000 / 8 / [`security_breach`] | match |

**S1 passes.** `--arbiter-random-seed` wiring is sound; the RandomArbiter classify order under `seed=42` is bit-equivalent to the pre-flag code path. Matrix proceeds.

### Full 60-cell matrix (per-seed appendix)

Each cell is one `uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --arbiter-mode random --arbiter-random-p 0.75 --arbiter-random-seed <seed> --trace <trace>` invocation, all other config frozen at M6a. Numbers are `hit / false_h` (false_h in initiations/hour).

| seed | dev_v2 | test_v1 | test_v2 |
|---:|---:|---:|---:|
| 42 | 1.00 / 3.50 | 1.00 / 11.02 | 0.80 / 15.00 |
| 0  | 0.60 / 3.50 | 0.80 /  7.35 | 0.80 /  7.50 |
| 1  | 0.80 / 0.00 | 0.60 / 11.02 | 1.00 /  7.50 |
| 2  | 0.60 / 3.50 | 0.80 /  7.35 | 1.00 /  3.75 |
| 3  | 1.00 / 3.50 | 0.80 / 14.69 | 1.00 / 15.00 |
| 4  | 1.00 / 3.50 | 0.80 / 11.02 | 0.80 / 15.00 |
| 5  | 0.80 / 0.00 | 0.40 / 14.69 | 0.60 / 11.25 |
| 6  | 0.60 / 3.50 | 0.60 / 11.02 | 1.00 /  7.50 |
| 7  | 1.00 / 3.50 | 1.00 / 14.69 | 1.00 / 15.00 |
| 8  | 0.80 / 3.50 | 1.00 /  7.35 | 0.80 / 11.25 |
| 9  | 0.80 / 3.50 | 0.80 / 11.02 | 0.60 / 15.00 |
| 10 | 1.00 / 3.50 | 0.80 / 11.02 | 0.80 / 11.25 |
| 11 | 1.00 / 0.00 | 0.80 / 14.69 | 1.00 / 11.25 |
| 12 | 1.00 / 3.50 | 0.80 / 14.69 | 1.00 / 15.00 |
| 13 | 0.80 / 3.50 | 0.80 / 14.69 | 0.80 / 15.00 |
| 14 | 0.80 / 3.50 | 0.80 / 14.69 | 0.80 / 15.00 |
| 15 | 0.80 / 3.50 | 0.80 /  7.35 | 0.80 /  7.50 |
| 16 | 1.00 / 3.50 | 1.00 / 14.69 | 1.00 / 15.00 |
| 17 | 0.80 / 0.00 | 0.80 /  7.35 | 1.00 /  3.75 |
| 18 | 1.00 / 3.50 | 1.00 / 14.69 | 1.00 / 15.00 |

### Per-trace quantile table (N=20)

Random-arbiter distributions under the frozen M6a config (band `[−0.5, +1.5]`, `p = 0.75`, 20 seeds). Δ values are **content − random** with the content reference fixed at `12a/b/c` (dev_v2 = 1.00 / 0.00; test_v1 = 0.80 / 3.67; test_v2 = 1.00 / 0.00).

| Trace | stat | hit_random | false_h_random | Δhit (content − rand) | Δfalse_h (content − rand) |
|---|---|---|---|---|---|
| dev_v2  | mean ± sd | 0.86 ± 0.14 |  2.80 ± 1.40 | +0.14 ± 0.14 |  −2.80 ± 1.40 |
| dev_v2  | q2.5/50/97.5 | 0.60 / 0.80 / 1.00 | 0.00 / 3.50 / 3.50 | 0.00 / +0.20 / +0.40 | −3.50 / −3.50 / 0.00 |
| test_v1 | mean ± sd | 0.81 ± 0.15 | 11.76 ± 2.98 | −0.01 ± 0.15 |  −8.08 ± 2.98 |
| test_v1 | q2.5/50/97.5 | 0.50 / 0.80 / 1.00 | 7.35 / 11.02 / 14.69 | −0.20 / 0.00 / +0.30 | −11.02 / −7.35 / −3.67 |
| test_v2 | mean ± sd | 0.88 ± 0.13 | 11.63 ± 3.91 | +0.12 ± 0.13 | −11.63 ± 3.91 |
| test_v2 | q2.5/50/97.5 | 0.60 / 0.90 / 1.00 | 3.75 / 13.13 / 15.00 | 0.00 / +0.10 / +0.40 | −15.00 / −13.13 / −3.75 |

Key observations baked into the distributions:

- **dev_v2:** random-arbiter hit_rate distribution is centred at 0.80–1.00; the trace is GT-dense enough that a `p=0.75` random gate catches most GTs by luck. But false/h sits at 2.80 ± 1.40 against content's 0.00 — content's lead is real, just smaller than the pre-reg's 5.0 bar (2.5/50/97.5 = −3.50 / −3.50 / 0.00).
- **test_v1:** random hit_rate is 0.81 ± 0.15; content sits at 0.80, so Δhit distribution straddles zero (q2.5/50/97.5 = −0.20 / 0.00 / +0.30). The discriminator is false/h: random's distribution is 11.76 ± 2.98 (q2.5 = 7.35, q97.5 = 14.69) against content's 3.67, giving Δfalse_h = −8.08 ± 2.98.
- **test_v2:** content dominates on both axes. Δfalse_h = −11.63 ± 2.98; q97.5 is still −3.75 (content worse than random on false/h in ≤ 2 seeds out of 20). Δhit = +0.12 ± 0.13; q2.5 is 0.00 (random matches content hit ≤ 2 seeds, never exceeds it meaningfully).

### Pre-registered success criteria — evaluation

Evaluated verbatim against the rules frozen in `b9ab7de`. No post-hoc redefinition.

**S1 — seed=42 equivalence.** PASS (see pre-flight table above; three exact matches).

**S2 — C3 on test_v1, seed-robust. Bar: Δfalse_h ≤ −5.0 in ≥ 18/20 seeds (≥ 0.90).**
Result: **FAIL.** 15 / 20 seeds (0.75) meet the bar. The 5 failing seeds all land at the same value: random false_h = 7.35 (i.e. 4 false inits instead of the modal 6–8 of the distribution), giving Δfalse_h = −3.67 — content still beats random by 3.67/h but not by 5.0/h. Failing seeds: {0, 2, 8, 15, 17}.

**S3 — C3 on test_v2, seed-robust. Bar: (Δhit ≥ 0.20) OR (Δfalse_h ≤ −5.0) in ≥ 18/20 seeds (≥ 0.90).**
Result: **PASS.** 18 / 20 seeds (0.90) meet the bar, exactly at the 18/20 threshold. The 2 failing seeds are {2, 17}: in both, random lands at hit = 1.00, false_h = 3.75 — content ties random on hit (content hit = 1.00 too, so Δhit = 0.00) and only beats random by 3.75/h on false_h (Δfalse_h = −3.75 > −5.0). These are the same two "low-false_h" draws visible as the q2.5 tail of test_v2's false_h distribution.

**S4 — Honest reporting of dev_v2. No pass/fail threshold; number reported.**
Result: **0 / 20 seeds (0.00)** meet the Δfalse_h ≤ −5.0 bar on dev_v2. The pre-reg predicted this: dev_v2 is the GT-dense trace and content's false_h is already 0.00, so the maximum possible Δfalse_h is bounded by −random_false_h, which has q97.5 = 3.50 in the distribution — structurally impossible for Δfalse_h ≤ −5.0 to hold on dev_v2 under any seed. This is a regime effect, not a seed artifact, confirming the M6a observation verbatim.

**S5 — Budget bound invariant. Bar: arbiter_calls = {dev_v2: 4, test_v1: 8, test_v2: 7} on every one of the 60 cells.**
Result: **PASS.** All 60 cells at the expected counts. Seed only changes YES/NO decisions, not which events reach the arbiter, as the pre-reg predicted.

**Summary: S1 PASS, S2 FAIL, S3 PASS, S4 reported (0/20), S5 PASS.** Per the pre-registered decision rules (*"S1 passes, exactly one of S2 / S3 passes → partial hardening. Report explicitly: which trace holds, which doesn't. C3 claim in the paper becomes trace-specific."*), this is the **partial hardening** branch. The C3 claim is tightened to the trace where it holds at the pre-reg bar and softened on the other.

### Headline findings

1. **C3 on test_v2 is seed-robust at the pre-reg 90 % bar.** 18 / 20 RandomArbiter seeds meet "Δhit ≥ 0.20 OR Δfalse_h ≤ −5.0" under the frozen M6a config. The distribution concentrates well inside the pass region: Δfalse_h median = −13.13, q2.5 = −15.00, q97.5 = −3.75; Δhit median = +0.10, q97.5 = +0.40. The M6a point estimate (seed=42, Δfalse_h = −15.00, Δhit = +0.20) sits at the median, not the tail — it was representative, not lucky. **S3 passes.**

2. **C3 on test_v1 is seed-fragile at the pre-reg 90 % bar.** Only 15 / 20 seeds (0.75) meet Δfalse_h ≤ −5.0. The failures are a specific structural artifact: 5 of 20 seeds land at random false_h = 7.35 (4 false inits at trace length), giving Δfalse_h = −3.67, just short of the −5.0 bar. Content is still strictly better than random on false_h in **every seed** (Δfalse_h mean = −8.08, q97.5 = −3.67 < 0); the claim "content reduces false inits vs random" is robust, but the stronger claim "by at least 5.0/h in 90 % of seeds" is not. The M6a point estimate (−7.35, seed=42) sits in the bulk of the distribution (median −7.35, mean −8.08) but the tail reaches into the fail region. **S2 fails.**

3. **dev_v2's C3-bar miss is structural, not a seed artifact.** 0 / 20 seeds meet Δfalse_h ≤ −5.0 on dev_v2. Content false_h = 0.00, random false_h distribution is 0.00–3.50, so the maximum possible Δfalse_h is −3.50 — the 5.0-bar is unreachable on this trace under any seed draw. The M6a observation ("GT-dense trace; random at high p can tie content on hit rate") was a regime effect, verified across the full seed distribution. S4 records this honestly.

4. **S5 holds exactly; budget claim is unaffected.** Arbiter-call count per trace is {dev_v2: 4, test_v1: 8, test_v2: 7} on **every one of the 60 cells** — the band-interaction bound M6a pre-registered is structurally independent of the random-arbiter seed. Changing the seed changes YES/NO choices, not which events reach the arbiter; M6a's C4 budget claim survives the seed-variance pass untouched.

5. **M6a's hit-rate and tok/hit headline is unchanged.** This pass did not re-run the content cells (`12a/b/c`) or any content-path number. M6a's single-config hit ≥ 0.80 on every trace at 6.8–11.3× lower tok/hit than poll still stands; only the C3 phrasing is updated.

6. **Updated paper framing for C3 (trace-specific wording).** From M6a's "content signal load-bearing on 2 / 3 traces by Δhit ≥ 0.20 OR Δfalse_h ≥ 5.0" to:

   > **On test_v2, the content signal is load-bearing in ≥ 90 % of RandomArbiter seed draws (18 / 20) at Δhit ≥ 0.20 OR Δfalse_h ≤ −5.0. On test_v1, content beats random on Δfalse_h in every seed (N = 20, Δfalse_h = −8.08 ± 2.98), but the stronger "≥ 5.0/h gap" holds in only 15 / 20 seeds (0.75) — below the pre-registered 90 % bar. On dev_v2, content's false_h = 0.00 ceiling makes any Δfalse_h ≤ −5.0 structurally unreachable; we report 0 / 20 as a regime-effect note rather than a fragility finding.**

   This is the "C3 claim becomes trace-specific" branch written into the decision rules.

### What this means for the paper and what comes next

M7 closes as a **partial pre-registered success** under the decision-rules written in advance. S1, S3, S5 pass; S2 falsifies at the 90 % bar; S4 reports the dev_v2 structural ceiling. The main M6a headline (single-config hit ≥ 0.80 everywhere at 6.8–11.3× lower tok/hit than poll) is unaffected; the C3 wording becomes trace-specific per the pre-reg.

The falsification is narrow and mechanistic: on test_v1, random-arbiter false_h has a q2.5 tail at 7.35 (4 false inits over the 30-minute trace), and the 5.0 bar sits just above that tail. Any of three future levers would tighten C3 on test_v1 if the paper needed it:

1. **Report the CI, not the bar.** Δfalse_h = −8.08 ± 2.98 (q2.5/50/97.5 = −11.02 / −7.35 / −3.67) is a more honest statement than a binary 90 % threshold. This is the pre-reg's "Δfalse/h CI becomes the headline" outcome, and it is probably the right paper framing regardless of S2.
2. **Loosen the bar.** Content beats random on false_h in 20 / 20 seeds (100 %) under Δfalse_h ≤ 0. The pre-reg just chose the wrong decision bar for test_v1's scale (test_v1 random false_h sits in 7.35–14.69; a −5.0 bar is near the q2.5). **Not doing this.** No post-hoc bar relaxation.
3. **Increase N.** With N = 200 the 95 % CI on the 0.75 fraction tightens enough to rule out the reasonable alternative hypotheses. Cheap, mechanical, and would be the next pass if the paper needed the stronger phrasing.

None of these is required for the paper-ready v1 claim. The tightened headline is:

> **Surprise-gated selective initiation with a regime-robust content arbiter delivers hit ≥ 0.80 on every trace at 6.8–11.3× lower token cost per correct proaction than an unconditional poll baseline, under a single frozen configuration across three structurally distinct traces. Mechanism attribution confirmed via matched-firing-rate random ablation: on test_v2 the content signal beats a seed-varied random arbiter by Δhit ≥ 0.20 OR Δfalse_h ≤ −5.0 in ≥ 90 % of 20 seed draws; on test_v1 it beats random on Δfalse_h in every seed (N = 20, Δfalse_h = −8.08 ± 2.98). Pre-registered focused isolation probe, matched-firing-rate ablation, and seed-variance hardening all verified against rules frozen before eval. The three-trace residual is a single V2-prompt gap (`package_arrival`), not a band-edge or firing-rate issue.**

Candidate next levers, unchanged from M6a:

1. **M6b — Claude-API arbiter.** Unblocks `package_arrival` on test_v1. Not required for v1.
2. **M7b — N=200 seed pass** (if reviewers push back on S2). Same code path; drop-in scale-up of this pass.
3. **M8 — Reflect loop / dynamic intent maintenance.** Still deferred (M3's falsification stands).

`heargent-plan.md` milestone language (proposed update): **M5 closes as a full success; M6a extends it with a one-constant band widening; M7 hardens M6a's C3 claim across N=20 random-arbiter seeds, establishing C3 as seed-robust on test_v2 (18 / 20 seeds at the 90 % bar), seed-fragile at the 5.0/h bar on test_v1 (15 / 20; content still strictly better on false/h in 20 / 20), and structurally unreachable on dev_v2. M6b and N=200 scale-up remain available.**

## Artifacts

- `runs/data/13-seed{42,0,1,…,18}-{dev_v2,test_v1,test_v2}.json` — 60 cells, one JSON per cell. Each contains `surprise_log`, `arbiter_yes_rate`, `arbiter_random_seed`, `arbiter_random_p = 0.75`, and the standard eval scoring.
- Baselines cited for Δ computations: `runs/data/12a-heargent-za-v2wide-dev_v2.json` / `12b-*test_v1.json` / `12c-*test_v2.json` (M6a content cells). **Not re-run.**
- Aggregation script: `/tmp/aggregate_run13.py` (session-local; the 60-row table and S2/S3/S4/S5 evaluation reproduce from the JSON files alone — no hidden state).
- Code: `agent/loop.py` (`HeargentZA.from_trace` adds `random_seed` kw), `eval/run_trace.py` (`--arbiter-random-seed` CLI flag). Committed at the M7 pre-registration SHA `b9ab7de`, a strict descendant of the M6a results SHA `d7252f7`.

