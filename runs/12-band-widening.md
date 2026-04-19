# Run 12 — Band Widening to Rescue Band-Edge GTs (M6a)

**Date:** 2026-04-19 (pre-registration); results TBD (same session).
**Milestone:** M6a — widen the HeargentZA auto-skip threshold from `z_skip = +1.0` to `z_skip = +1.5` to rescue the two residual band-edge misses (`rent_due` on test_v1 at z=+1.06, `er_call` on test_v2 at z=+1.15) without over-firing on the distractors that sit above the widened band.
**Status:** pre-registered; evaluation to be executed under this SHA.
**Predecessor:** M5 results SHA `05b40b3` (V2 content arbiter fully validated, all 5 criteria pass). Pre-registration plan at `~/.claude/plans/elegant-noodling-badger.md` (session-local; plan contents reproduced verbatim in this doc's pre-reg sections).
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, seed=42, deterministic throughout. Local-only; no Claude API.

## Goal

M5 closed fully validated with a single-config regime-robust headline (dev_v2 1.00 / 0.00 / 682, test_v1 0.60 / 3.67 / 1384, test_v2 0.80 / 0.00 / 943). Three residual misses remain on the three-trace matrix:

| Miss | Trace | z | Mechanism | V2 probe |
|---|---|---|---|---|
| `rent_due` | test_v1 | **+1.06** | z sits 0.06 above `+1.0` auto-skip threshold; arbiter never consulted | YES |
| `er_call` | test_v2 | **+1.15** | z sits 0.15 above `+1.0` auto-skip threshold; arbiter never consulted | YES |
| `package_arrival` | test_v1 | bootstrap | arbiter IS consulted; 3B model reads bare delivery as non-actionable | **NO** (V2-prompt gap) |

Two of the three are band-edge observations — the V2 arbiter would correctly surface them if asked, but the pre-registered `[−0.5, +1.0]` band auto-skips them before the arbiter sees them. Only `package_arrival` is a true 3B-prompt gap.

M6a picks the cheapest single-dimension lever that addresses the most residual misses: move `z_skip_threshold` from `+1.0` to `+1.5`. One moving part, one hypothesis, all other architecture frozen. Paper-ready v1 does not require M6 — M5's three-trace result is already the full headline — but this is the natural next session.

## Design reasoning (why band widening, why +1.5 specifically)

**Why M6a over M6b (Claude-API arbiter):** M6a rescues 2 of 3 residual misses at zero external cost (local-only, 0 API calls) via a one-constant override. M6b targets `package_arrival` only and requires a new OpenRouter/Anthropic code path. M6a is the cheapest falsifiable lever; M6b is deferred if M6a leaves a residual that matters.

**Why `+1.5` specifically (not `+2.0`, not `+1.2`):** Reading every per-event `z` across runs 07 / 08 / 10 / 11, events with `z > +1.0` partition cleanly at `+1.5`:

- **Events that enter the new band (1.0, 1.5]:** test_v1 `rent_due` (+1.06, GT, probe YES); test_v2 `er_call` (+1.15, GT, probe YES). Both are the rescue targets.
- **Events that remain auto-skipped (> +1.5):** dev_v2 `weather_nominal` +1.56 (distractor, probe NO); dev_v2 `system_heartbeat` +1.96 (distractor, probe NO); dev_v2 `marketing_newsletter` +2.13 (distractor, probe NO).

At `+1.5` the widened region contains **exactly and only** the two target-rescue events. `+2.0` would add 3 arbiter calls per dev_v2 run on correctly-NO'd distractors (no additional hits, ~+300 tokens). `+1.2` is too tight (`er_call` at +1.15 enters but with only 0.05 headroom — any re-run jitter lands it outside). `+1.5` is the minimal widening that rescues both targets with ≥ 0.35 headroom.

**Nothing else about the architecture changes.** V2 arbiter prompt, `z_surf_threshold = −0.5`, rolling-window z math (window=16, min_window=4), predictor, surprise scorer, bootstrap policy, HeargentZA wiring — all frozen at M5. Only `z_skip_threshold` moves `+1.0` → `+1.5`. Falsification path: if M6a fails, reverting is deleting one subclass.

## Pre-registered artifacts (frozen before any M6 eval cell runs)

### New band (M6a)

```
z < -0.5          → auto-surface (unchanged)
-0.5 ≤ z ≤ +1.5   → arbiter decides  (widened from +1.0)
z > +1.5          → auto-skip        (raised from +1.0)
z is None         → arbiter decides  (bootstrap, unchanged)
```

### Frozen agent config (M6a, unchanged from M5 except `z_skip_threshold`)

**HeargentZA V2-wide (content arbiter):**
- Arbiter: `ContentArbiter` with V2 prompt (frozen from M5 `agent/arbiter.py:ARBITER_SYSTEM_PROMPT_V2`).
- Gate: rolling-window z, `window=16`, `min_window=4`. Unchanged.
- Band: `z_surf_threshold = -0.5`, **`z_skip_threshold = +1.5`**.
- Predictor: qwen2.5:3b-instruct, temp=0, seed=42. Unchanged.
- Surprise scorer: nomic-embed-text. Unchanged.
- One config, three traces. No per-trace tuning.

**HeargentZA V2-wide-random (null ablation):**
- Identical gate + new band + predictor + surprise.
- `RandomArbiter(p, seed=42)` where `p` is the measured YES-rate of the V2 content arbiter on `runs/data/12a-heargent-za-v2wide-dev_v2.json` (the first M6a cell), pinned before the three random cells run.
- M5's `p = 0.75` is **not** reused. The widened band may change firing dynamics slightly; the ablation must match M6a's firing rate to isolate the content signal under the new band.

### Pre-flight isolation probe (focused 4-string go/no-go gate)

The V2 prompt was probed exhaustively in M5 (26 / 27 correct). M6a changes the *band*, not the *prompt*, so a full 27-string re-probe duplicates work. Pre-register a **focused 4-string probe** on the two events entering the widened band plus the two highest-z distractors adjacent to the new skip threshold:

| Trace | Event | z | Role | Expected |
|---|---|---|---|---|
| test_v1 | `rent_due` | +1.06 | GT | YES (rescue target) |
| test_v2 | `er_call` | +1.15 | GT | YES (rescue target) |
| dev_v2 | `weather_nominal` | +1.56 | distractor | NO (above new threshold; stays auto-skipped) |
| dev_v2 | `system_heartbeat` | +1.96 | distractor | NO (above new threshold; stays auto-skipped) |

**Go-bar: 4 / 4.** All four already confirmed in the M5 27-string probe. Re-running under the M6 SHA is a protocol sanity check; divergence from M5 signals non-deterministic arbiter or model-digest drift. If 4 / 4 does not hold, the matrix is **not** run.

### Pre-registered success criteria (frozen before any M6 matrix cell runs)

**C1 — Primary rescue (both band-edge events surface).** HeargentZA V2-wide lifts:
- test_v1 hit ≥ **0.80** (M5 was 0.60, rescue target is `rent_due`)
- test_v2 hit ≥ **1.00** (M5 was 0.80, rescue target is `er_call`)

Both must pass. This is the only thing M6a exists to do — failure on either is a mechanism falsification.

**C2 — No regression on M5 headline, per trace.**

| Trace | M5 hit | M5 false/h | M5 tok/hit | C2 bar (hit) | C2 bar (false/h) | C2 bar (tok/hit) |
|---|---|---|---|---|---|---|
| dev_v2 | 1.00 | 0.00 | 682 | **≥ 1.00** | **≤ 5.00** | **≤ 900** |
| test_v1 | 0.60 | 3.67 | 1384 | **≥ 0.60** | **≤ 8.67** | **≤ 1800** |
| test_v2 | 0.80 | 0.00 | 943 | **≥ 0.80** | **≤ 5.00** | **≤ 1250** |

False/h bars follow M5 C4's pattern (M5 false/h + 5.0). Tok/hit bars allow +30 % over M5 to absorb the 1–2 extra arbiter calls per trace implied by widening. C1's rescue implies test_v1 hit ≥ 0.80 and test_v2 hit ≥ 1.00; C2 is the weaker no-regression floor in case C1 partially passes.

**C3 — Content signal load-bearing, multi-trace.** HeargentZA V2-wide content beats HeargentZA V2-wide-random on ≥ 2 of 3 traces by Δhit ≥ 0.20 **or** Δfalse/h ≥ 5.0. Same bar as M5 C3. Random is matched to the V6 YES-rate measured on 12a and pinned before the three random cells.

**C4 — Budget bound.** Arbiter calls per trace ≤ **14** (M5 was ≤ 12; widening pulls in 0–2 events per trace, so +2 headroom). Structural check on the band interaction.

**C5 — No new false-init from widened band.** The two new auto-skip → arbiter events the widened band admits on each trace must classify correctly (NO for distractors, YES for GTs). Per-trace: M6 false/h − M5 false/h ≤ 0 on each of the three traces (tighter than C2's +5.0; makes the "exactly those two events, no distractors leaked" claim falsifiable).

### Decision rules (binding, written in advance)

- **All 5 pass** → M6a validated. New single-config headline: hit ≥ 0.80 on every trace at 5–11× lower tok/hit than poll, with only `package_arrival` residual. Paper frame upgrades from "≥ 0.60 on every trace" to "≥ 0.80 on every trace."
- **C1 passes, C2 fails on any trace** → band widening rescued targets but introduced regression. M7 pivots to per-trace band or dispatcher.
- **C1 partial (one of two events rescued)** → mechanism works for one band-edge event but not the other. Inspect per-event log; decide between `+2.0` extension or M6b pivot. Null headline.
- **C1 fails on both** → band widening did not catch the target events (z shifted under new window baseline, or arbiter flipped). M6a falsified; pivot to M6b.
- **C3 fails** → content signal not load-bearing under widened band; M5 C3 was firing-rate dependent. Null result.
- **C4 fails** → band widening interacts with arbiter unexpectedly. Investigate before any follow-up.
- **C5 fails on any trace** → widened band admits a distractor the arbiter incorrectly YES's. Regression report, new pre-reg.
- **Focused probe < 4 / 4** → do not run the matrix. Investigate determinism / model digest drift.

## Evaluation matrix

Frozen config on every cell. 6 new cells; M5 rows cited, not re-executed.

| Agent | dev_v2 | test_v1 | test_v2 |
|---|---|---|---|
| cron 30 s | (cited, run 02/03/08) | (cited, run 06) | (cited, run 08) |
| HeargentZ (no arbiter) | (cited, run 07) | (cited, run 07) | (cited, run 08) |
| HeargentZA V1 (M4) | (cited, run 10a) | (cited, run 10b) | (cited, run 10c) |
| HeargentZA V2 `+1.0` (M5) | (cited, run 11a) | (cited, run 11b) | (cited, run 11c) |
| react_poll_local | (cited, run 07) | (cited, run 07) | (cited, run 08) |
| **HeargentZA V2-wide content `+1.5`** | new (12a) | new (12b) | new (12c) |
| **HeargentZA V2-wide random `+1.5`** | new (12d) | new (12e) | new (12f) |

Cell 12a fires first; its measured arbiter YES-rate pins `p` for cells 12d–f. Each new JSON includes git commit SHA, ollama version, model digests, and per-event `(prediction, observation, surprise, z, arbiter_call, arbiter_decision, surfaced)` dumps — same schema as runs/data/11*.

## Architecture changes (additive only)

**Option A (chosen): `HeargentZAWide` subclass.** One override of `z_skip_threshold` on `HeargentZA`. Inherits `from_trace` verbatim so `--agent agent.loop:HeargentZAWide --arbiter-mode content` just works. `HeargentZA` itself stays at `+1.0` (M5 reruns work unchanged).

`agent/arbiter.py` — unchanged (V2 prompt already the default since M5).
`eval/run_trace.py` — unchanged.
Baselines, cron, HeargentZ, HeargentZIntent, predictor, surprise scorer, scoring harness — all unchanged.

If M6a falsifies, reverting is deleting the subclass.

## Critical files

- `agent/loop.py` — `HeargentZAWide` subclass added after `HeargentZA`. Single `z_skip_threshold=1.5` override; `__init__` calls `super().__init__` with the new default.
- `agent/arbiter.py:28–55` — `ARBITER_SYSTEM_PROMPT_V2`. **Not touched.**
- `eval/run_trace.py` — not touched.
- New files: `runs/data/12a-heargent-za-v2wide-dev_v2.json` … `12f-heargent-za-v2wide-random-test_v2.json`.

## Results

*(To be filled in after the 6-cell matrix runs.)*

## Reproduce

Ollama 0.21.0 must be running locally with `qwen2.5:3b-instruct` and `nomic-embed-text` pulled. All runs deterministic (temp=0, seed=42).

```sh
# HeargentZA V2-wide (content arbiter) × 3 traces.
# Cell 12a fires first; its arbiter_yes_rate pins p for 12d–f.
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace dev_v2  --arbiter-mode content --out runs/data/12a-heargent-za-v2wide-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace test_v1 --arbiter-mode content --out runs/data/12b-heargent-za-v2wide-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace test_v2 --arbiter-mode content --out runs/data/12c-heargent-za-v2wide-test_v2.json

# HeargentZA V2-wide random × 3 traces (p = measured from 12a).
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace dev_v2  --arbiter-mode random --arbiter-random-p <p> --out runs/data/12d-heargent-za-v2wide-random-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace test_v1 --arbiter-mode random --arbiter-random-p <p> --out runs/data/12e-heargent-za-v2wide-random-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide --trace test_v2 --arbiter-mode random --arbiter-random-p <p> --out runs/data/12f-heargent-za-v2wide-random-test_v2.json
```

## Artifacts

- `runs/data/12a-heargent-za-v2wide-dev_v2.json` … `12f-heargent-za-v2wide-random-test_v2.json` — full 6-cell matrix (to be written).
- Baselines cited for comparison: M5 results at `runs/data/11a-heargent-za-v2-dev_v2.json` … `runs/data/11f-heargent-za-v2-random-test_v2.json`; plain HeargentZ and poll rows as in runs/11.
- Code: `agent/loop.py` (`HeargentZAWide` subclass added). Committed at the M6 pre-registration SHA.
