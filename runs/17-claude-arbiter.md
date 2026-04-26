# Run 17 — Claude-API Arbiter (Model-Scale Lever, Opus 4.7) + Externally-Authored Held-Out Trace `test_v5` (M10)

**Date:** 2026-04-26 (pre-registration). Results sections (Commit B regression + test_v4 attribution + in-distribution cost denominator; Commit D test_v5 eval) appended post-eval.
**Milestone:** M10 — replace the qwen2.5:3b-instruct local arbiter with a Claude-API arbiter (Opus 4.7) under both V2 closed-enumeration and V3 principled-criterion prompts, holding everything else (predictor, surprise scorer, band, frozen M7 config) constant. Validated in two stages: (B) in-distribution V2-Opus regression gate against the three co-developed traces + V2-Opus / V3-Opus H1/H2 attribution on `test_v4` + poll-Opus apples-to-apples cost denominator on the three co-developed traces; (D) externally-authored `test_v5` under the same M8b three-commit protocol. **Hard path-C posture: zero within-milestone iteration budget; any halt closes M10 at the corresponding paper-line row.** Run once at each stage. No retuning of V2 or V3.
**Pre-registration SHA:** Commit A landed at SHA `68d42e3` (model lock + API params + locked rates + V2/V3 prompt references + cell matrix + cost framework + Commit-B regression bars + `test_v4` attribution table + `test_v5` P1–P4 + decision rules + paper-line per outcome + reviewer-vulnerable defenses committed together; no code changes and no eval runs before that commit). **Defenses-hardened at:** this commit, post-connectivity-smoke (Commit B pre-flight; no harness cell with discriminative content has yet fired). Forced amendments to two API-parameter assumptions discovered at the connectivity smoke; details in §"API parameters" amendment, §"Model ID lock for reproducibility" amendment, and §"Connectivity-smoke observations" below. Mirrors M9's `e66afc1` hardening pattern (pre-Commit-B refinements landed as a separate commit on top of the original pre-reg). **Predecessors:** M9 close SHA `aaa6232` (path-C close on V3 at 3B), defenses-hardened at `e66afc1`; M8b results SHA `ad70d67`.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3` (both retained for predictor + surprise scorer + V2-3B baseline cell #11). Claude API: `anthropic` SDK (added at Commit B), `ANTHROPIC_API_KEY` env var, model alias `claude-opus-4-7` — fully-dated dispatch ID (e.g., `claude-opus-4-7-2026MMDD`) recorded post-first-call in this doc's "Commit B environment" sub-block. Anthropic rates locked at this commit: Opus 4.7 = $15 / M input tokens, $75 / M output tokens (source: anthropic.com/api pricing as of 2026-04-26). temp=0, predictor seed=42, deterministic throughout. Identical to M9's environment for the local pipeline; new at M10 is the Claude API path.

## Context

M9 (runs/16, commit `aaa6232`) closed with the principled-criterion redesign (V3 prompt) falsified at the 3B model scale on round 0. `arbiter_yes_rate` collapsed to 0.00 / 0.12 / 0.14 across the three co-developed traces; the qwen2.5:3b-instruct arbiter pattern-matched on V3's regret-list example words rather than resolving the abstract AND-gate. Per scientifically-conservative path-C close, the pre-reg's 2-round within-form redesign budget was held in reserve and the falsification taken at face value.

M8b (runs/15, commit `ad70d67`) had earlier falsified V2's four-trace extension on the externally-authored `test_v4` (hit = 0.40 vs poll/random/cron all at 1.00; three V2-prompt-coverage gaps tagged: urban warnings, colleague social asks, civil-disruption commute alerts).

The two falsifications motivate two competing hypotheses, neither resolvable from existing data:

- **H1 (prompt-form)**: closed enumeration is fundamentally narrow; principled criterion (V3) is the right form but needs a stronger model to resolve abstract conjuncts.
- **H2 (model-scale)**: 3B can't resolve the principled form regardless of phrasing; closed enumeration was a model-scale workaround whose narrowness is itself the bottleneck on out-of-enumeration content.

M10 is the experiment that distinguishes H1 from H2 by holding everything else frozen at M6a/M7 and varying **only** the arbiter model — replacing the qwen2.5:3b-instruct arbiter with a Claude-API arbiter at the most capable model available in the Claude 4.x family.

## Thesis

> Replacing the 3B local arbiter with a Claude-API arbiter (Opus 4.7) under the same V2 closed-enumeration prompt either (a) closes the M8b coverage gap on `test_v4` and on a fresh externally-authored `test_v5` — confirming H2 (model scale was the bottleneck) — or (b) leaves the gap unclosed, which under V3-Opus (run as a paired attribution cell on both `test_v4` and `test_v5`) further distinguishes whether the principled-criterion form rescues the gap at scale. The cost dimension introduced by Claude API ($/hit) is reported as a second Pareto axis alongside the existing tok/hit, with poll-Opus added as the apples-to-apples cost baseline on every trace where V2-Opus runs.

Architectural lever: arbiter model only. Everything else — predictor (qwen2.5:3b), surprise scorer (nomic-embed-text), `HeargentZAWide`, band `[−0.5, +1.5]`, predictor temp/seed, V2 closed-enumeration prompt as the M10 default arbiter prompt, V3 principled-criterion prompt (retained as named constant from M9) for paired attribution — frozen at the M7 / M9-close state.

## Frozen design choices (locked at this commit)

### Arbiter model — Opus 4.7, sole Claude model in M10

- **Primary and only**: `claude-opus-4-7` (alias). Most capable model in the Claude 4.x family at the M10 commit date. The H1/H2 question is best answered at the strongest available scale: if Opus 4.7 closes the M8b external coverage gap, model-scale was the bottleneck (H2); if Opus 4.7 fails, the gap is not solely a model-scale issue even at the strongest 4.x model. Either outcome is a publishable headline.
- **Not used**: Sonnet 4.6, Haiku 4.5, Opus 4.5 / 4.6. A cost-curve sweep across Claude family members is M10b / M11 scope — distinct pre-reg, distinct run number. M10 reports a single Pareto point at the strongest model, not a Pareto curve. This forecloses the "did you really try the strongest?" review attack and the symmetric "you only tested the most expensive — what about cheaper?" attack (which the paper-line and cost framework explicitly scope to a single Opus 4.7 data point as a future-work hand-off).
- **Model ID lock for reproducibility — amended at this hardening commit, post-connectivity-smoke.** The pre-reg originally expected the API to return a fully-dated dispatch ID via `response.model` (e.g. `claude-opus-4-7-2026MMDD`, mirroring the older `claude-3-5-sonnet-20241022` convention). Empirically, Opus 4.7's API returns the alias verbatim — `response.model = 'claude-opus-4-7'` with no date suffix. Other reproducibility markers in the response: per-request `response.id`; `usage.service_tier='standard'`; `usage.inference_geo='global'`. We record what the API actually returns in §"Connectivity-smoke observations" below, plus the verbatim connectivity-smoke output bytes (output text, input/output tokens, stop_reason) so any future cross-validation can compare against the byte-level baseline. Pre-Commit-D sanity (already in §"Reproduce") includes a bit-identical re-run of one Commit-B V2-Opus cell against its recorded JSON; that re-run also serves as a model-version-drift detector across the Commit B → D boundary.

### API parameters

- **`temperature` parameter — amended at this hardening commit, post-connectivity-smoke.** The pre-reg originally locked `temperature = 0` (matching the 3B's `temp=0/seed=42` posture). Opus 4.7 deprecates this parameter and rejects requests that include it: `anthropic.BadRequestError: 'temperature' is deprecated for this model` (verbatim error from the Commit B pre-flight connectivity smoke). The lock is therefore unenforceable; the parameter is dropped from the API call (both `ClaudeArbiter` and `react_poll_claude`). Determinism is independently verified: 3 identical V0-prompt calls on `fire_alarm` content returned 3 byte-identical outputs (see §"Connectivity-smoke observations" below); further hardened at the V2-vs-V3 probe by running it twice and comparing every (event, prompt) decision byte-for-byte. The pre-reg's determinism claim survives via empirical verification rather than via the (now-impossible) parameter setting.
- `max_tokens = 5` (token contract is "Output exactly YES or NO" — generous slack vs the single-token YES/NO output expected). Pre-flight probe at Commit B (see "Verification" §) verifies actual output shape before harness cells fire.
- `system = ARBITER_SYSTEM_PROMPT_V2` (verbatim from `agent/arbiter.py:8`), `user = event_content`. This is wire-up choice (a) from `runs/16-v3-prompt.md:51-53` — chat-template parity with V2-3B (system = rules; user = event content). For V3-Opus attribution cells, the same wire-up: `system = ARBITER_SYSTEM_PROMPT_V3`, `user = event_content`.
- **No prompt caching** for arbiter calls. Rationale recorded for the paper: at ~250 input tokens × ~50–100 calls per cell, raw API cost is ~$0.40 per cell at Opus rates; caching would drop input cost ~10× but adds a cache-control field to every call and complicates per-call accounting. We accept higher API cost for simpler accounting; the reported `usd_per_hit` is without-cache and would be lower with caching. This is a pre-registered design choice, not a post-hoc cost-flattering one.
- API key from `ANTHROPIC_API_KEY` env var. Failure-on-missing-key is loud (no silent fallback to a different arbiter).

### Anthropic rates locked at pre-reg

For cost reproducibility:

- Opus 4.7: **$15 / M input tokens, $75 / M output tokens**.
- Source: anthropic.com/api pricing page as of this commit's date (2026-04-26). If rates change post-pre-reg, the paper reports rates-at-pre-reg for `usd_per_hit` and notes any post-pre-reg change in a footnote — does not retroactively recompute under new rates.

### Prompts

- **V2 closed enumeration** (`ARBITER_SYSTEM_PROMPT_V2` from `agent/arbiter.py:8`): the M10 default. Same text the 3B uses; isolates the model-scale lever cleanly.
- **V3 principled criterion** (`ARBITER_SYSTEM_PROMPT_V3` retained from M9 in `agent/arbiter.py`): paired attribution cell on `test_v4` AND `test_v5`. Tests whether the principled form rescues at scale on both an in-the-record external trace and a fresh one. Eliminates the M10b loose end an earlier draft of this plan left open.
- No new prompts authored for M10. Both V2 and V3 are frozen artifacts from prior milestones. Prompt-architecture is **not** the M10 lever.

### Code changes (Commit B scope)

- New `ClaudeArbiter` class in `agent/arbiter.py`, parallel to `ContentArbiter` and `RandomArbiter`. Same interface (`classify(text) -> bool`, `yes_rate` property, parser identical via shared `_DECISION` regex). Uses `anthropic` SDK. Ctor takes `system_prompt: str = ARBITER_SYSTEM_PROMPT_V2` so V3 cells pass `system_prompt=ARBITER_SYSTEM_PROMPT_V3` explicitly (V3 reproduction pattern from M9 close).
- New CLI flag `--arbiter-mode claude` in `eval/run_trace.py`, dispatching to `ClaudeArbiter`. Optional `--arbiter-system-prompt {v2,v3}` selector (defaults to `v2`) for the V3-Opus attribution cells. Existing `--arbiter-mode content / random` paths unchanged.
- New baseline `baselines/react_poll_claude.py` (parallel to `react_poll_local.py`) for the apples-to-apples cost comparisons. Same poll structure, swap the local 3B model call for an Opus 4.7 call with the same poll prompt.
- Add `anthropic` to `pyproject.toml` deps.
- New JSON fields in cell output: `arbiter_input_tokens`, `arbiter_output_tokens` under `llm_stats`; top-level `cost_usd` (currently 0.0) populated from per-call token counts × locked Opus rates.

### Connectivity-smoke observations (recorded at this hardening commit, pre-Commit-B-cells)

Captured pre-harness, before any cell with discriminative content fires. Forces the two amendments above (`temperature` parameter dropped; `response.model` returns alias only).

**Call 1** — V0 prompt (`"Output exactly YES or NO."`), content `"Test."`:
- `response.model`: `claude-opus-4-7` (alias only; no date suffix — see "Model ID lock for reproducibility" amendment above)
- `response.content[0].text`: `'YES'`
- `response.usage`: `{input_tokens: 26, output_tokens: 2, service_tier: 'standard', inference_geo: 'global', cache_*_input_tokens: 0, server_tool_use: None}`
- `response.stop_reason`: `'max_tokens'`

**Calls 2-4** — V0 prompt, content `"Fire alarm in building A triggered; evacuation in progress."`, run 3 times back-to-back through the same `Anthropic` client instance:
- All three returned `response.content[0].text='NO'`, `usage.input_tokens=44`, `usage.output_tokens=2`, `stop_reason='max_tokens'`. **Byte-identical across all three.**
- Determinism on V0 prompt with identical content is empirically confirmed without explicit `temperature=0`.

**Observed quirks (documented as observed-not-load-bearing):**
- `stop_reason='max_tokens'` despite `output_tokens=2 < max_tokens=5`. Anthropic API quirk; the visible content is clean and matches the parser's regex (`\b(YES|NO)\b` against `first_line.upper()`). `usage` has no `thinking_tokens` field — no hidden reasoning is consuming budget. No remediation needed.
- The V0 prompt `"Output exactly YES or NO."` is non-discriminative — `'YES'` on `"Test."` and `'NO'` on `fire_alarm` content reflect default model behavior with no surfacing criterion, not arbiter behavior. The V2-vs-V3 8-event probe (next pre-flight) provides the discriminative read on the actual M10 prompts.

**Determinism on actual M10 prompts (V2 + V3) — hardened at the doubled probe.** The V2-vs-V3 8-event off-harness probe (mandatory pre-flight per §"Reproduce" → "Pre-Commit-B sanity (3)") is run twice, back-to-back, through the same `ClaudeArbiter` instances. Every (event, prompt) decision is compared byte-for-byte between runs (16 paired equalities). If all 16 hold, determinism on V2 and V3 is empirically confirmed on the prompts the M10 cells actually use. The probe-doubling is added at this hardening commit as the strongest available substitute for the (now-impossible) `temperature=0` lock. **Probe outputs (both runs) are appended to this section after the probe completes** (next commit, alongside the Commit B code).

## Four-commit protocol

| Commit | Content | Gates |
|---|---|---|
| **A** | This pre-reg doc → `runs/17-claude-arbiter.md` (model lock + API params + locked rates + V2/V3 prompt references + cell matrix + cost framework + bars + decision rules + paper-line per outcome + reviewer defenses). No code. | — |
| **B** | `ClaudeArbiter` class + CLI flag + `react_poll_claude` baseline + dep add. Pre-flight V2-3B smoke (bit-identical to `12a-...-dev_v2.json`) + Opus connectivity smoke + V2-vs-V3 8-event off-harness probe. Then 8 cells: in-distribution V2-Opus regression (3 traces) + `test_v4` H1/H2 attribution (V2-Opus + V3-Opus) + poll-Opus apples-to-apples in-distribution cost denominator (3 traces). | Regression gate: hit no-regression vs M6a, +5/h symmetric tolerance on false/h. **Hard halt on any failure.** |
| **C** | Externally-authored `test_v5` (fresh Claude Code session, /clear, paste runs/16's Commit-A-frozen authoring prompt verbatim, audit, paste into `sandbox/event_trace.py`, register). | Audit: 11 hard structural constraints + 3 banned lists from runs/16. Reject + log on any violation; no prompt edits. |
| **D** | 6-cell `test_v5` matrix: V2-Opus content / V3-Opus content / V2-3B content / random p=0.75 seed=42 / poll-Opus / cron30s. Score P1–P4 verbatim. Append paper-update section. | Verbatim evaluation against frozen rules. |

**Cells 9-14 (Commit C / D) are conditional on:** (Commit B regression gate PASS on all three in-distribution traces) **AND** (at least one of the two `test_v4` attribution cells reaches `hit_rate ≥ 0.80`). If either condition fails, M10 closes at end of Commit B with the in-distribution and `test_v4` results as the headline; cells 9-14 do not run. This mirrors M9's path-C close: take the falsification at face value, do not paper over it with a follow-up trace.

## Path-C posture (zero iteration budget)

M10 has **zero within-milestone iteration budget**, in contrast to M9's pre-registered 2-round within-form redesign budget (which was held in reserve and never spent). Reasons:

- V2 and V3 are both frozen artifacts from prior milestones. There is no "within-form redesign" available — neither prompt was authored in M10, so neither can be tuned by M10.
- The arbiter model is the sole architectural lever. Iterating on the model (e.g., switching to Sonnet on Opus failure) would mix the M10 lever with M10b/M11 scope and undermine the H1/H2 attribution.
- Hard path-C is the most defensible posture: any Commit B regression failure or `test_v4` joint failure closes M10 immediately, the falsification stands as-is, and the paper line for that outcome is locked at this pre-reg.

If M10 closes at Commit B (path-C), the published result is the in-distribution and `test_v4` data; cells 9-14 do not run; the M10b candidate is named as future work.

## Cost framework (drafted at pre-reg, before any cell fires)

The current Pareto figure has a single cost axis (tok/hit) where the arbiter contributes zero $$ (3B-local is free). M10 adds a $/hit dimension. Drafted before any cell runs to avoid "cost framework chosen post-hoc."

**Per-cell metrics**:
- `tok_per_hit` — total local tokens (predictor + surprise) / n_hits. Carries forward from M6a; covers the always-on local pipeline. Identical computation to runs/12-15.
- `usd_per_hit` — total Claude API cost / n_hits. Cost = `arbiter_input_tokens × $15/M + arbiter_output_tokens × $75/M`, using the locked Opus 4.7 rates. Reported per cell.
- For poll-Opus cells: same `usd_per_hit` definition; the poll path makes one Claude call per event, so the cost grows linearly with event count (vs the surprise-gated path which calls Claude only on in-band + bootstrap events).

**Per-trace Pareto comparisons**:
- V2-Opus content vs V2-3B content (same trace, same prompt, different model) → quantifies the scale upgrade's cost-coverage trade. Reported on dev_v2 / test_v1 / test_v2 / test_v4 (V2-3B numbers carry forward from M6a / M8b) and test_v5 (V2-3B cell #11 added explicitly so the same-trace delta on the external trace is direct).
- V2-Opus content vs poll-Opus (same trace, same arbiter model, different gating policy) → quantifies surprise-gating's cost savings vs unconditional polling at matched arbiter capability. Reported on dev_v2 / test_v1 / test_v2 (poll-Opus cells #6-8 added explicitly so the in-distribution cost story is fully apples-to-apples) and test_v5 (cell #13).
- V3-Opus content vs V2-Opus content (same trace, same model, different prompt) → quantifies the prompt-form effect at Opus scale. Reported on test_v4 (cells #4-5) and test_v5 (cells #9-10).

**Total expected M10 API spend** (drafted before any cell fires for accountability):
- Surprise-gated cells (V2-Opus, V3-Opus): ~5-10 arbiter calls × ~250 input + ~1 output tokens. Per cell: input cost = 10 × 250 × $15/M ≈ $0.04; output ≈ negligible. ≈ $0.04 / cell × 7 surprise-gated Claude cells (3 in-dist + 2 test_v4 + 2 test_v5; cell 11 V2-3B is local-only) ≈ $0.30.
- poll-Opus cells (4: 3 in-dist + 1 test_v5): ~50-100 events × ~500 input + ~10 output tokens per cell. Per cell: ≈ 100 × 500 × $15/M = $0.75 input + 100 × 10 × $75/M = $0.075 output ≈ $0.83. Total: ≈ $3.30.
- Off-harness V2-vs-V3 probe (8 events × 2 prompts = 16 calls): negligible.
- **Total ballpark: $3-5 across the full Commit B + D matrix.** Tight enough that "we ran the experiment under a fixed sub-$10 budget" is itself a cost-framework data point.

**Paper-line cost framing pre-registered**:
> *"Surprise-gated selective initiation under a Claude-API arbiter (Opus 4.7) delivers hit ≥ 0.80 on [N] traces at $X / hit (arbiter API), vs poll-Opus at $Y / hit (matched arbiter capability, ungated) — a Z× cost saving from the surprise gate at matched arbiter quality. The 3B-local arbiter (V2 closed enumeration, M6a) delivers hit ≥ 0.80 on the three co-developed traces at $0 / hit but falls to 0.40 on the externally-authored `test_v4`; the model-scale upgrade closes [if H2 holds] / does not close [if it fails] that external coverage gap."*

## Cell matrix (13 LLM/local cells + 1 cron = 14 total)

Cell file names use the `17b-` prefix for Commit B and `17d-` prefix for Commit D, matching the runs/16 convention.

### Commit B cells (8)

| # | Cell file | Agent | Arbiter | Trace | Purpose |
|---|---|---|---|---|---|
| 1 | `17b-content-opus-v2-dev_v2.json` | HeargentZAWide | Opus V2 | dev_v2 | In-dist regression |
| 2 | `17b-content-opus-v2-test_v1.json` | HeargentZAWide | Opus V2 | test_v1 | In-dist regression |
| 3 | `17b-content-opus-v2-test_v2.json` | HeargentZAWide | Opus V2 | test_v2 | In-dist regression |
| 4 | `17b-content-opus-v2-test_v4.json` | HeargentZAWide | Opus V2 | test_v4 | H2 attribution |
| 5 | `17b-content-opus-v3-test_v4.json` | HeargentZAWide | Opus V3 | test_v4 | H1 attribution |
| 6 | `17b-poll-opus-dev_v2.json` | react_poll_claude | (poll Opus) | dev_v2 | In-dist cost denominator |
| 7 | `17b-poll-opus-test_v1.json` | react_poll_claude | (poll Opus) | test_v1 | In-dist cost denominator |
| 8 | `17b-poll-opus-test_v2.json` | react_poll_claude | (poll Opus) | test_v2 | In-dist cost denominator |

### Commit D cells (6, conditional on B PASS ∧ ≥1 test_v4 attribution cell ≥ 0.80)

| # | Cell file | Agent | Arbiter | Trace | Purpose |
|---|---|---|---|---|---|
| 9 | `17d-content-opus-v2-test_v5.json` | HeargentZAWide | Opus V2 | test_v5 | **Primary (P1)** |
| 10 | `17d-content-opus-v3-test_v5.json` | HeargentZAWide | Opus V3 | test_v5 | H1/H2 on external trace |
| 11 | `17d-content-3b-v2-test_v5.json` | HeargentZAWide | 3B V2 | test_v5 | Same-trace model-scale delta on external |
| 12 | `17d-random-test_v5.json` | HeargentZAWide | random p=0.75 seed=42 | test_v5 | P3 (no API) |
| 13 | `17d-poll-opus-test_v5.json` | react_poll_claude | (poll Opus) | test_v5 | P2 cost anchor |
| 14 | `17d-cron30-test_v5.json` | CronKeyword30s | — | test_v5 | P4 (no LLM) |

## In-distribution regression bars (Commit B, cells 1-3)

Mirror M9's bars verbatim — V2-Opus must not regress in-distribution vs V2-3B's M6a numbers.

| trace | M6a V2-3B hit | M6a V2-3B false/h | V2-Opus bar |
|---|---:|---:|---|
| `dev_v2` | 1.00 | 0.00 | hit ≥ 1.00, false/h ≤ 5.0 |
| `test_v1` | 0.80 | 3.67 | hit ≥ 0.80, false/h ≤ 8.67 (= 3.67 + 5.0) |
| `test_v2` | 1.00 | 0.00 | hit ≥ 1.00, false/h ≤ 5.0 |

+5/h symmetric tolerance is justified the same way as M9: pre-registered as the anticipated cost of the lever (here a stronger model that may be more permissive on borderline content), well below random's ~14/h, preserves the C3 single-seed claim if Opus holds. The +5/h tolerance also doubles as a YES-bias check: if Opus reads V2's enumeration as "be more permissive" relative to the 3B, false/h on co-developed traces will breach the bar and Commit B halts.

**Decision rule on in-distribution regression** (hard path-C):
- **All three pass.** V2-Opus is a clean drop-in for V2-3B in-distribution. Proceed to test_v4 attribution evaluation (cells 4-5 already ran in Commit B, scored against attribution table below).
- **Any trace fails the hit bar.** Halt M10. Do **not** redesign V2 (frozen since M5; if Opus reads it differently than 3B, that itself is the headline). Possible explanations: Opus reads V2's enumeration differently than 3B; chat-template behavior differs at scale; rare-case YES/NO disagreement at borderline content. Mandatory off-harness diagnostic probe (mirror runs/16's V2-vs-V3 probe — already part of pre-flight) is documented; the paper line for this outcome is "in-distribution regression under Opus" (row 7 of the paper-line table). Commit C/D do not run.
- **All three pass hit but one or more fails the false/h bar.** Halt M10. Same path-C close; paper line records Opus's permissiveness as the in-distribution finding.

No within-milestone iteration. No "let's re-run with a tweaked wire-up." If the gate fails, the falsification is the result.

## `test_v4` attribution rules (Commit B, cells 4-5)

The two `test_v4` cells (V2-Opus, V3-Opus) are **attribution-only** — not gated against P1-P4 bars. They distinguish H1 from H2 and (combined with V3-Opus on `test_v5`, cell #10) provide a complete attribution readout. Pre-registered interpretation:

| V2-Opus `test_v4` hit | V3-Opus `test_v4` hit | Attribution |
|---|---|---|
| ≥ 0.80 | ≥ 0.80 | **H2 confirmed + V3 also viable at scale.** Both prompt forms work at Opus scale. M8b coverage gap closes by scale alone; closed enumeration is sufficient at 4.x. V3-at-Opus is a viable alternative (V3's 3B falsification was model-capability, not prompt-form). |
| ≥ 0.80 | < 0.80 | **H2 confirmed + V3 falsified at any scale.** V2 enumeration is structurally robust at scale; V3 phrasing is broken not just at 3B but at Opus too. M9's principled-criterion thesis closes as falsified at any scale, not 3B-specific. |
| < 0.80 | ≥ 0.80 | **H1 confirmed.** Principled criterion was the right form but needed Claude to resolve. V3 vindicated; V2's enumeration is structurally narrow at any scale. M9's V3 close at 3B was a model-capability falsification; V3 at Opus rescues. |
| < 0.80 | < 0.80 | **Neither lever closes the M8b gap on `test_v4`.** Deeper architectural issue: the M8b coverage failure is not solely a prompt-form or model-scale problem. **Closes M10 at end of Commit B** (path-C); cells 9-14 do not run. Paper line: "neither V2 nor V3 at Opus 4.7 closes the M8b external coverage gap; M11 candidate is band-edge audit / multi-arbiter routing / content-aware surprise scoring." |

Both `test_v4` cells are reported verbatim with `usd_per_hit` and `arbiter_yes_rate` for mechanism support, regardless of attribution outcome.

## `test_v5` P1-P4 (Commit D, cells 9-14)

Let `c9 = 17d-content-opus-v2-test_v5.json` (HeargentZAWide, Opus V2 arbiter), `c12 = 17d-random-test_v5.json` (random p=0.75 seed=42), `c13 = 17d-poll-opus-test_v5.json` (poll-Opus), `c14 = 17d-cron30-test_v5.json` (cron 30s).

- **P1 — Primary**: `hit_rate(c9) ≥ 0.80`. Re-establishes the headline under M10 if it passes; falsifies M10's external-coverage claim if it doesn't.
- **P2 — Pareto**: `usd_per_hit(c9) ≤ usd_per_hit(c13) / 3`. Apples-to-apples cost comparison: V2-Opus content vs poll-Opus on the same trace, both using Opus 4.7 as the arbiter. Surprise-gating must be at least 3× cheaper than unconditional polling at matched arbiter capability. M6a's V2-3B vs poll-local ratio was 6.8–11.3× on the local-tok axis; 3× is a conservative floor on the new $/hit axis.
- **P3 — Tertiary (report-only)**: C3 single-seed. Either `hit_rate(c9) − hit_rate(c12) ≥ 0.20` OR `false_initiation_rate_per_hour(c9) − false_initiation_rate_per_hour(c12) ≤ −5.0`. Random p=0.75 is matched to V2-3B's empirical yes-rate from M6a (cross-milestone comparability — see defense #7); a single-seed P3 does not gate paper framing.
- **P4 — Sanity gate**: `hit_rate(c13) ≥ 0.80`. Poll-Opus is the strongest baseline on `test_v5`; if it falls below 0.80, the trace is ambiguous to even unconditional-call-Opus-on-everything, and the primary verdict is read through that lens. (Mirrors M8b/M9 P4 — but stronger because the baseline is now Opus, not the 3B-poll baseline used in earlier milestones.)

Cells 10 (V3-Opus on test_v5) and 11 (V2-3B on test_v5) are **attribution-only** — reported verbatim, no P1-P4 bar attached, used for the cross-prompt and cross-model interpretation in the paper-line table.

## Decision rules (`test_v5`, frozen; no post-hoc redefinition)

- **P1 PASS** (`hit(c9) ≥ 0.80`). External-trace headline re-established under M10. Paper line: per row 1, 2, or 3 of the per-outcome table below (depending on test_v4 attribution).
- **P1 `0.60 ≤ hit(c9) < 0.80`.** External coverage partially closed under V2-Opus. Paper softens to "hit ≥ 0.80 on co-developed traces; partial recovery on externally-authored content under Opus." Cross-reference cell 10 (V3-Opus on test_v5): if `hit(c10) ≥ 0.80`, headline shifts to V3-Opus as the primary result; if `hit(c10) < 0.80`, both prompt forms partially fail at Opus on external content.
- **P1 `hit(c9) < 0.60`.** External coverage not closed under M10 V2-Opus. Cross-reference cell 10: if V3-Opus rescues (`hit(c10) ≥ 0.80`), headline pivots to V3-Opus and paper line maps to row 3. If V3-Opus also fails on test_v5, both prompt forms fail at Opus on this external trace; cross-reference test_v4 attribution to determine whether this is a generalization failure (test_v4 worked but test_v5 didn't) or a deeper architectural limit.
- **P2 FAIL.** Surprise-gating's cost saving vs poll-Opus is below 3×. Headline softens; report verbatim ratio. Doesn't change P1 verdict.
- **P3 PASS or FAIL.** Reported either way; single-seed P3 doesn't gate the paper.
- **P4 FAIL.** Trace fairness questioned; report all six cells (9-14), primary verdict on P1 still stands, kept-as-artifact (mirrors M8b's `test_v4` discipline).
- **In-distribution regression FAIL (Commit B, cells 1-3)**: see in-distribution decision rules above. Hard path-C; closes M10 before `test_v4` attribution work continues to test_v5.
- **Both `test_v4` attribution cells fail** (`< 0.80` on cells 4 AND 5): hard path-C; closes M10 at end of Commit B; cells 9-14 do not run.

**Protocol-failure rule (M10-specific).** If `test_v5` surfaces a third novel failure class distinct from M8's keyword/content scoring gap and M8b's V2-coverage gap (e.g., both V2 and V3 misfire on a structurally distinct cohort even at Opus scale), iterate the spec further (`test_v6`) rather than retune the arbiter. Protocol converges; arbiter does not chase trace-specific residuals.

No raising of cell count, no seed substitution on P3, no post-hoc bar redefinition, no trace regeneration in response to eval outcome.

## Pre-registered paper framing per outcome (locked at Commit A)

Drafted at pre-registration. No post-hoc paragraph editing in response to actual numbers. Each row restates the decision-rule consequences encoded in the sections above as the publishable headline.

| In-dist regression | `test_v4` attribution | `test_v5` P1 | Paper framing |
|---|---|---|---|
| Pass | V2≥0.80, V3≥0.80 | ≥ 0.80 | **H2 confirmed + V3 also viable at Opus scale + 4-trace headline.** *"Surprise-gated selective initiation with a Claude-API arbiter (Opus 4.7) under V2 closed enumeration delivers hit ≥ 0.80 on all three co-developed traces and one externally-authored trace at $X/hit (arbiter), vs poll-Opus at $Y/hit (matched arbiter, ungated). The 3B-local M6a arbiter delivered the same in-distribution result at $0/hit but failed on the externally-authored test_v4 (hit = 0.40); model-scale upgrade closes the M8b external coverage gap. M9's V3 principled-criterion redesign was a model-capability falsification at 3B scale, not a prompt-form falsification — V3 at Opus also reaches hit ≥ 0.80 on test_v4 and test_v5. Both prompt forms are viable at Opus scale; M6a's V2 closed enumeration is the cheaper-input lower-bound, V3 principled criterion is the more general form."* |
| Pass | V2≥0.80, V3<0.80 | ≥ 0.80 | **H2 confirmed + V3 falsified at any scale + 4-trace headline.** *"Surprise-gated selective initiation with a Claude-API arbiter (Opus 4.7) under V2 closed enumeration delivers hit ≥ 0.80 on all three co-developed traces and one externally-authored trace at $X/hit (arbiter), vs poll-Opus at $Y/hit. V3 principled-criterion form fails at Opus on both test_v4 and test_v5; M9's V3 falsification at 3B scale is now confirmed at Opus scale — V3's principled criterion is structurally not the right form for this task at any model scale tested, not just at 3B. M6a's V2 closed enumeration is itself load-bearing across model scales."* |
| Pass | V2<0.80, V3≥0.80 | ≥ 0.80 (V3-Opus primary) | **H1 confirmed + 4-trace headline under V3-Opus.** *"V3 principled-criterion arbiter at Opus 4.7 scale closes the external coverage gap (hit ≥ 0.80 on test_v4 and test_v5); V3 at 3B scale (M9) was a model-capability falsification, not a prompt-architecture falsification. V2 enumeration is structurally narrow at any scale; M6a's V2 success on co-developed traces was a co-development artifact that didn't generalize to externally-authored content. Cost: $X/hit at Opus 4.7."* (Headline cell becomes c10, not c9; P1 evaluated against c10.) |
| Pass | V2<0.80 AND V3<0.80 | n/a | **Neither prompt form closes the gap at Opus scale.** *"Closed enumeration (V2) and principled criterion (V3) both fail on externally-authored content (test_v4) even at Opus 4.7 scale. The M8b coverage gap is not solely a prompt-form or arbiter-scale issue; deeper architectural lever needed. Candidate next levers: band-edge audit (z<−0.5 auto-surface false-init path observed in runs/15 §5), multi-arbiter routing, content-aware surprise scoring."* M10 closes at end of Commit B (cells 9-14 do not run); test_v4 attribution alone delivers the falsification. |
| Pass | per row 1, 2, or 3 | `0.60 ≤ hit < 0.80` | **Partial external recovery at Opus scale.** *"Headline cell achieves hit ∈ [0.60, 0.80) on test_v5 — partial closure of the M8b coverage gap at Opus scale. Per-miss tags determine whether residuals are V3-vs-V2 prompt-form sensitive (cross-reference cell 10), trace-specific structural patterns the spec doesn't yet capture (M10b candidate: tighten test_v5 spec further), or a generalization wall at Opus 4.7 scale (M11 candidate: cross-model sweep or alternative architecture)."* |
| Pass | per row 1, 2, or 3 | `hit < 0.60` | **External coverage not closed under M10.** *"Even Opus 4.7 fails to close the M8b external coverage gap on test_v5 under either V2 or V3 prompt; the in-distribution and test_v4 results stand as headline (paper-line cell from regression-pass row), but the M8b external-authoring protocol surfaces a generalization wall on test_v5 that M10's model-scale lever does not close. M11 candidate: deeper architectural lever (band-edge / multi-arbiter / content-aware surprise) or alternative arbiter family entirely."* |
| **Fail** | n/a | n/a | **In-distribution regression under Opus (path-C close).** *"Opus 4.7 reads V2's enumeration sufficiently differently from qwen2.5:3b that V2-Opus does not preserve M6a's three-trace recall under +5/h tolerance. M6a's V2 closed-enumeration claim is reported as 3B-specific in this regard; cross-model robustness of V2's prompt is not assumed. M10 closes at Commit B without test_v4 attribution or test_v5; M11 candidate is V2 prompt re-validation or re-elicitation across model scales."* |

## Reviewer-vulnerable surfaces and pre-registered defenses

Mirroring the defense-hardening pass M9 did at `e66afc1` — pre-emptively address the attacks a harsh reviewer will run.

1. **"You only ran one Claude model; results don't generalize across the family."** Defense: locked Opus 4.7 by alias and recorded dispatched model ID before running; the M10 claim is about Opus 4.7 specifically as the strongest available 4.x model, not "Claude in general." Cost-curve sweep across the family is M10b / M11+ scope, explicitly named in this pre-reg as future work and not folded into M10.

2. **"You frozen-tested Opus at temp=0; that's deterministic but bare. Seed sweep?"** Defense: Opus at temp=0 is deterministic per Anthropic's API contract; no equivalent of seed=42. Cross-cell variance under the same prompt + temp=0 is structurally zero (same input → same output). N=20 sweep is meaningful for the random-arbiter ablation (which is in cell 12) but not for the Opus content cells. Reported explicitly in this doc as a deliberate non-sweep on the deterministic axis.

3. **"You added a new baseline (poll-Opus) — that's tuning the comparison."** Defense: pre-registered before any cell fires (this commit). Used on every trace where V2-Opus runs (in-distribution and test_v5) for fully apples-to-apples cost comparison. poll-local stays as the existing baseline carried forward from M6a (preserves cross-milestone comparability for the local-only Pareto). Adding a new baseline that uses the same arbiter as the experimental cell is the *cleaner* cost comparison than the alternative ("poll-local at 3B vs V2-Opus at 4.7" which mixes model scales).

4. **"Cost framework was chosen to flatter the result."** Defense: dual-axis (tok/hit, usd/hit) drafted in this pre-reg before any cell runs, with explicit poll-Opus apples-to-apples baseline on every trace where V2-Opus runs. Anthropic rates locked at pre-reg ($15/M input, $75/M output for Opus 4.7); rate changes after pre-reg are footnoted but don't retroactively change `usd_per_hit`. Total expected M10 spend ($3-5) drafted before any cell fires, in this doc. Paper-line per outcome locked in the 7-row table above.

5. **"V3-Opus on test_v4 was post-hoc."** Defense: pre-registered in this commit as the H1 attribution cell; runs alongside V2-Opus in Commit B before any test_v5 work. The cell's outcome is read against the pre-registered 4-row attribution table, not interpreted ad-hoc. V3-Opus on test_v5 (cell 10) is *also* pre-registered here so all four attribution branches resolve within M10 — no M10b loose-end.

6. **"You held the M9 redesign budget in reserve, then went to a different lever instead. Is that ducking the M9 hypothesis?"** Defense: M9 closed honestly under path-C (runs/16); M10 is the orthogonal architectural lever. M9 tested *prompt form* at fixed model; M10 tests *model scale* at fixed prompts (both V2 and V3). If M10 confirms H1 (V3 rescues at scale), M9's V3 falsification is reframed as model-capability not prompt-form — the M9 redesign budget would have been wasted on a 3B that couldn't resolve any principled phrasing. The two milestones are not redundant — they isolate different levers cleanly.

7. **"Random p=0.75 was matched to V2-3B yes-rate, not V2-Opus — biases the C3 comparison."** Defense: matching the random ablation to V2-3B's empirical yes-rate is the explicit cross-milestone comparability choice; matching to V2-Opus's yes-rate would make the random cell incomparable with M7's 20-seed sweep on the same value and would drift the random-baseline anchor across milestones. The C3 claim is interpreted as "vs the same matched-firing-rate ablation as M6a/M7/M8b/M9," not as "vs Opus's empirical yes-rate." Decision recorded at this pre-reg.

8. **"V2-Opus's in-distribution PASS could be Opus's YES-bias artifact, not a clean drop-in."** Defense: the +5/h symmetric tolerance on `false_initiation_rate_per_hour` is precisely the YES-bias check. If Opus is biased YES relative to the 3B, false/h on co-developed traces breaches the bar and Commit B halts (hard path-C). The in-distribution gate doubles as a bias check; pre-registered, not post-hoc.

9. **"Cell matrix could grow during execution to make the result work."** Defense: 14 cells locked in this commit, mapped 1:1 to file names in the cell-matrix table. No cells added or removed during execution. If a result motivates an additional cell post-Commit-B (e.g., V3-Opus on co-developed traces, or a Sonnet/Haiku cost-curve), it is M10b — distinct pre-reg, distinct run number, distinct PR. M10 is closed when its 14 cells are evaluated against this doc's bars.

10. **"You're inferring the V2-3B → V2-Opus model-scale delta on the external trace by comparing test_v4 (V2-3B from M8b) with test_v5 (V2-Opus) — different traces."** Defense: cell 11 (V2-3B on test_v5) is pre-registered explicitly as the same-trace V2-3B-vs-V2-Opus delta on the external trace. $0 cost (local model). Closes the cross-trace inference attack.

## Pre-registered artifacts for `test_v5` (frozen by reference to runs/16 SHA `3653880`)

`test_v5`'s authoring prompt, 11 hard structural constraints, and 3 banned lists (46 banned event ids / 27 banned content themes / 26 banned keyword tuples) are **carried forward verbatim from `runs/16-v3-prompt.md` Commit-A SHA `3653880`** (M9's pre-reg, where these artifacts were frozen as an unused pre-reg artifact when M9 closed at Commit B path-C). M10 reuses them unchanged. Specifically:

- **Authoring prompt**: `runs/16-v3-prompt.md` SHA `3653880`, §"Authoring prompt (verbatim — pasted unmodified into the fresh Claude Code session at Commit C)". Pasted verbatim into the fresh Claude Code session at M10 Commit C as its first user message. Any edit invalidates the protocol; if the fresh session's first output fails audit, log the rejection and open another fresh session — no prompt edits.
- **Frozen trace spec (11 hard structural constraints)**: `runs/16-v3-prompt.md` SHA `3653880`, §"Frozen trace spec (extends M8b)". Audited at Commit C before merge.
- **Banned lists (3 × extended at M9)**: `runs/16-v3-prompt.md` SHA `3653880`, §"Banned event ids" / §"Banned content themes" / §"Banned keyword tuples". 46 / 27 / 26 entries respectively, unchanged for M10.
- **Authoring protocol (Commit C)**: `runs/16-v3-prompt.md` SHA `3653880`, §"Authoring protocol (Commit C)". 6 steps, unchanged. M10 Commit C step 6 commit message becomes "M10: externally-authored test_v5 (fresh session, <timestamp>)" instead of M9's "M9: …".

The carry-forward is intentional: `test_v5`'s authoring prompt was already pre-registered and committed under runs/16 before any M10 work began, so it cannot be tuned to M10's expected outcome. This is the strongest possible "test_v5 was not designed to flatter M10" defense — the prompt was frozen for a milestone (M9) that closed before M10 was conceived.

### Rejections log

(Populated during Commit C. Each rejection notes: fresh-session timestamp, first violated constraint, one-sentence description of the violation. A rejected generation is not merged; the generator code is not kept.)

_None yet._

## Critical files

- `agent/arbiter.py` (Commit B) — new `ClaudeArbiter` class. Existing `ContentArbiter` and `RandomArbiter` not touched. `ARBITER_SYSTEM_PROMPT_V2` and `ARBITER_SYSTEM_PROMPT_V3` constants reused verbatim.
- `eval/run_trace.py` (Commit B) — new `--arbiter-mode claude` dispatch path + `--arbiter-system-prompt {v2,v3}` selector. Existing dispatches unchanged.
- `baselines/react_poll_claude.py` (Commit B) — new file, parallel structure to `react_poll_local.py`. Same poll prompt; arbiter swapped for Opus 4.7.
- `pyproject.toml` (Commit B) — `anthropic` SDK added.
- `sandbox/event_trace.py` (Commit C) — appends `def test_trace_v5() -> Trace:` + `"test_v5": test_trace_v5` registry entry. `test_trace_v1/v2/v3/v4` not touched.
- `runs/17-claude-arbiter.md` (Commit A → D) — pre-reg doc landed at this commit (Commit A); Commit B / D results appended.
- `runs/README.md` (Commit D) — row 17 added; status block updated; paper framing updated per pre-registered per-outcome line.
- `agent/loop.py`, `agent/predictor.py`, `agent/surprise.py`, `sandbox/world.py`, existing baselines (`react_reactive`, `react_cron_keyword`, `react_poll_local`), `test_trace_v1/v2/v3/v4` — **not touched.**

## Reproduce

### Pre-Commit-B sanity (after `ClaudeArbiter` lands; before any harness cell fires)

```sh
# (1) V2-3B regression smoke (must be bit-identical to runs/data/12a-...-dev_v2.json)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode content --out /tmp/smoke-pre-M10.json
# Compare hit_rate, false_initiation_rate_per_hour, total_notifications, misses,
# llm_stats.arbiter_calls, llm_stats.arbiter_yes_rate against
# runs/data/12a-heargent-za-v2wide-dev_v2.json — must match exactly.

# (2) Opus connectivity smoke (single arbiter call; no harness)
uv run python -c "from anthropic import Anthropic; c = Anthropic(); \
  r = c.messages.create(model='claude-opus-4-7', max_tokens=5, \
    system='Output exactly YES or NO.', messages=[{'role':'user','content':'Test.'}]); \
  print(r.model, r.content[0].text)"
# Must print the dated dispatch ID (e.g. claude-opus-4-7-2026MMDD) followed by YES or NO.
# Record the dispatched model ID in this doc's "Commit B environment" sub-block before proceeding.

# (3) Off-harness V2-vs-V3 8-event probe (parser sanity + prompt-form contrast)
# Mirrors runs/16-v3-prompt.md:454 diagnostic. 8 representative events × 2 prompts = 16 calls.
# Events: fire_alarm, flight_delay, meeting_moved, news_digest, rent_due, package_arrival,
#         parking_meter_oak (test_v4 GT), cover_standup_request (test_v4 GT).
# Run and record verbatim outputs in this doc under "V2-vs-V3 Opus probe" section.
# Confirms: (a) parser handles Opus's actual output shape (must be YES/NO per parser regex);
# (b) Opus reads V2 closer to YES than 3B reads V2 on these representative cases (sanity);
# (c) V3 at Opus does NOT exhibit the 3B's pattern-matching-on-regret-list-words mode
#     observed in M9 (sanity check before V3-Opus harness cells fire).
```

### Commit B — regression gate + test_v4 attribution + in-dist cost denominator

```sh
# Cells 1-3 — V2-Opus, in-dist regression
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out runs/data/17b-content-opus-v2-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v1 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out runs/data/17b-content-opus-v2-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v2 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out runs/data/17b-content-opus-v2-test_v2.json

# Score against the regression gate. Hard halt on any failure.

# Cells 4-5 — V2-Opus + V3-Opus on test_v4 (H1/H2 attribution)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v4 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out runs/data/17b-content-opus-v2-test_v4.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v4 --arbiter-mode claude --arbiter-system-prompt v3 \
  --out runs/data/17b-content-opus-v3-test_v4.json

# Cells 6-8 — poll-Opus, in-dist cost denominator
uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
  --trace dev_v2 --out runs/data/17b-poll-opus-dev_v2.json
uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
  --trace test_v1 --out runs/data/17b-poll-opus-test_v1.json
uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
  --trace test_v2 --out runs/data/17b-poll-opus-test_v2.json
```

After Commit B: score regression bars on cells 1-3, score attribution table on cells 4-5. If either gate fails per path-C posture, halt M10 and write up the close in this doc.

### Pre-Commit-D sanity (after `test_v5` lands at Commit C)

```sh
# Schema check
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v5'); \
  print(len(t.ground_truth), len(t.events), round(t.duration_s, 1))"
# Must print: 5 9 <value ≤ ~1030>

# Keyword/content alignment audit (M8b constraint, retained verbatim from runs/16)
uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v5'); \
  [print(gt.event.id, kw, kw.lower() in gt.event.content.lower()) \
   for gt in t.ground_truth for kw in gt.keywords]"
# Every line must end in True. Any False → reject the generation, log in Rejections, open new fresh session.

# Bit-identical re-run of one Commit-B V2-Opus cell (e.g. dev_v2)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out /tmp/smoke-pre-D.json
# Compare hit_rate, false_initiation_rate_per_hour, total_notifications, misses, llm_stats
# against runs/data/17b-content-opus-v2-dev_v2.json — must match exactly. Confirms no API drift
# between Commit B and Commit D. (Determinism is per Anthropic's temp=0 contract; any
# divergence is a model-version drift signal and must be investigated before Commit D fires.)
```

### Commit D — `test_v5` 6-cell matrix

```sh
# Cell 9 — V2-Opus content (primary, P1)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v5 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out runs/data/17d-content-opus-v2-test_v5.json

# Cell 10 — V3-Opus content (H1/H2 on external trace)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v5 --arbiter-mode claude --arbiter-system-prompt v3 \
  --out runs/data/17d-content-opus-v3-test_v5.json

# Cell 11 — V2-3B content (same-trace model-scale delta)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v5 --arbiter-mode content \
  --out runs/data/17d-content-3b-v2-test_v5.json

# Cell 12 — random p=0.75 seed=42 (P3, no API)
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v5 --arbiter-mode random --arbiter-random-p 0.75 --arbiter-random-seed 42 \
  --out runs/data/17d-random-test_v5.json

# Cell 13 — poll-Opus (P2 cost anchor)
uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
  --trace test_v5 --out runs/data/17d-poll-opus-test_v5.json

# Cell 14 — cron 30s (P4, no LLM)
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s \
  --trace test_v5 --out runs/data/17d-cron30-test_v5.json
```

## Non-goals for this pass

- **Multi-arbiter / hierarchical routing** (3B-local first, escalate to Claude on borderline). Different paper. M11+ scope.
- **Cross-model Claude sweep** (Opus + Sonnet + Haiku × all cells). Pre-emptively de-scoped to M10b / M11 to keep M10's H1/H2 attribution clean. M10 reports a single Pareto point at Opus 4.7.
- **Prompt redesign at Claude scale.** V2 and V3 are the only prompts in M10. If both fail at Opus on test_v4, that's the result; do not author V4 mid-M10. Hard path-C.
- **Within-milestone iteration budget.** Zero rounds. Any halt closes M10 immediately at the corresponding paper-line row.
- **Reopening test_v3 / test_v4** for re-scoring or re-curation. Both stay as artifacts.
- **Retuning V2 or V3 against any external trace.** Same M8b/M9 discipline; held-out content is held out.
- **Changing band, surprise scorer, predictor model, predictor temp/seed, or any frozen M7 component.** Arbiter model is the sole architectural lever in M10.
- **Folding the auto-surface false-init audit (runs/15 §5) into M10.** Different lever (band edge, not arbiter). Separate future pass.
- **Skipping pre-flight V2-3B smoke** under the Commit B tree. Environmental drift between M9 close and M10 Commit B must be ruled out before any Claude cell fires.
- **Skipping the off-harness V2-vs-V3 Opus probe.** Parser sanity check is mandatory; without it, a parser-induced FAIL at Commit B is indistinguishable from a model-scale FAIL.

This pass is comparable in code-delta scope to M8b / M9 (one new arbiter class, one new CLI flag, one new baseline file, one dep added; no harness or sandbox edits). Cell-matrix scope is wider than M9 (14 vs 7) because M10 absorbs both the in-distribution-regression pattern AND the test_v4 attribution AND the test_v5 evaluation in a single milestone, with poll-Opus apples-to-apples cost cells added on every trace where V2-Opus runs.

## Results — Commit B regression gate + test_v4 attribution + in-dist cost denominator

_Populated after Commit B's 8 cells run + pre-flight smokes complete. Captures: pre-flight V2-3B bit-identical smoke result, Opus connectivity smoke output (incl. dispatched model ID), V2-vs-V3 8-event probe outputs, 8-cell results table, regression-gate verdict, test_v4 attribution verdict, path-C close decision (if applicable)._

_Not yet executed._

## Results — Commit D `test_v5` eval

_Populated after Commit D's 6 cells run, conditional on Commit B PASS ∧ ≥1 test_v4 cell ≥ 0.80. Captures: 6-cell results table, P1/P2/P3/P4 verdicts, paper-line per pre-reg outcome row, M10 close summary._

_Not yet executed (conditional on Commit B + test_v4 attribution outcomes)._

## Artifacts (final)

_Populated post-close. Lists: `runs/data/17b-*.json` and `runs/data/17d-*.json` cells produced; agent/arbiter.py code state; sandbox/event_trace.py state; runs/README.md updates; final paper-line per outcome row matched._

_Not yet finalized._
