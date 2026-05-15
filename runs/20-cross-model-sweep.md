# Run 20 — Cross-Model Claude Sweep (M11b)

**Date:** 2026-05-13 (pre-registration). Results sections (Commit B drift baselines + belt-and-suspenders re-run audit; Commit D 44-cell harness eval + per-tier metrics + outcome row identification + D7 branch identification + Sonnet/Haiku Phase 2 + Phase 3 drift smoke) appended post-eval.
**Milestone:** M11b — cross-model Claude tier sweep at the M11a-frozen N=10 external sample (Sonnet 4.6, Haiku 4.5 at Opus-equivalent cells; matched-arbiter poll-Sonnet + poll-Haiku cost denominators; V3-Sonnet + V3-Haiku attribution on failure subset {test_v4, test_v5}). Maximum-defensibility posture: 6-row outcome paper-lines + 3-branch D7 paper-lines locked verbatim at Commit A; primary-vs-secondary outcome block + bootstrap CI sensitivity + triangulated B → D-start → D-end drift smoke + Commit B belt-and-suspenders V2-3B + cron30s re-run + pricing attestation archive. Three-commit M10-shape protocol (A pre-reg → B code-wiring + drift baselines + belt-and-suspenders → D harness + analysis); no externally-authored-trace step. Required code changes at Commit B (per-model rate table + `--arbiter-model` CLI flag, ~30-40 lines across 3 files) — distinguishes M11b from M11a's zero-code shape.
**Pre-registration SHA:** Commit A landed at SHA `0b47ce3` (this file's first commit; backfilled into the file body at the immediately-following SHA-backfill commit per no-amend discipline). Plan source: `~/.claude/plans/m11b-cross-model-sweep.md`. No pre-data hardening edits to the plan source were needed at Commit A — the kickoff walkthrough confirmed D1-D7 are locked, 6 outcome paper-lines + 3 D7 paper-lines drafted verbatim, primary-vs-secondary block + bootstrap CI sensitivity + triangulated drift smoke + belt-and-suspenders V2-3B + cron30s + pricing attestation already wired into the source. Pricing-verification HARD GATE per §D4 was executed at Commit A (see `runs/data/20a-pricing-attestation-2026-05-13.json`): observed published rates verified Sonnet 4.6 = $3 input / $15 output (matches plan placeholder) + Haiku 4.5 = $1 input / $5 output (matches plan placeholder); Opus 4.7 observed at $5 input / $25 output (rotated from M10 lock of $15 / $75 — Anthropic-side ~3× rate reduction in the Opus 4.6-generation lineage since M10 2026-04-27). Per pre-reg §D4 points 3+5, the M10 lock HOLDS: M11b cost computations continue to use $15/$75 for Opus for cross-milestone consistency with M10/M10b/M11a; the observed rotation is documented in the attestation JSON as a Commit-A finding. Cross-tier Pareto ratios reported in this paper are insensitive to a uniform Opus-rate scaling factor; absolute Opus-tier $/hit numbers should be divided by ~3 for current-Anthropic-rate deployment cost projections.
**Predecessors:** M11a close SHA `cceeddd` (M11a Commit D: 20-cell harness + drift smoke; Row 4a partial-closure-with-residuals at all three N-scopes; drift-revision SUCCESS at iterative-extension protocol; V2-Opus failure rate 20% [95% CP CI 2.5%–55.6%] vs V2-3B 50% [18.7%–81.3%] at combined-N=10 primary scope); M10b D-on-N=3 SHA `985f441` (test_v6/v7/v8 supplementary harness; combined-N=5 cross-milestone aggregate Row 4a pattern); M10 close SHA `6f86c8d` (positive close at row 1; H2 confirmed at n=1 external; V3-Opus also viable per V2/V3 attribution).
**Environment:** Carry-forward from M11a. ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3` (predictor + surprise scorer + V2-3B baseline cell). Claude API: `anthropic` SDK, `ANTHROPIC_API_KEY` env var, `claude-opus-4-7` alias (V2-Opus + poll-Opus carryover from M10/M10b/M11a; Opus carryover smoke at Commit B vs `runs/data/17b-content-opus-v2-*.json` PASS-gates Opus determinism through M11b). New M11b model aliases wired at Commit B: `claude-sonnet-4-6` + `claude-haiku-4-5` (per `--arbiter-model` CLI flag with alias mapping `{"opus":"claude-opus-4-7","sonnet":"claude-sonnet-4-6","haiku":"claude-haiku-4-5"}`). M11b cost-modeling rates locked at Commit A per pricing attestation: Opus 4.7 = $15 / M input tokens, $75 / M output tokens (M10 lock; observed-published rate at Commit A = $5 / $25; lock preserves cross-milestone consistency per pre-reg §D4 points 3+5); Sonnet 4.6 = $3 input / $15 output (matches observed); Haiku 4.5 = $1 input / $5 output (matches observed).

---

**Structural divergence from M11a (worth flagging at the top):** M11b requires non-zero code changes (per-model rate table + `--arbiter-model` CLI flag), so the M11b protocol is the **3-commit M10-shape** (A pre-reg → B code-wiring + drift baseline + belt-and-suspenders re-run → D harness), NOT M11a's 5-commit no-code shape (A → C1..C5 → D). There is no externally-authored trace step at M11b — M11b reuses M11a's frozen `test_v11..v15` + M10b's `test_v6..v8` + M10's `test_v4` + `test_v5` as the N=10 external sample.

## Context

M11a (`runs/19-iterative-banned-list-extension.md`, closed at `cceeddd`) delivered:
- **Drift-revision SUCCESS** at iterative-extension protocol: 0 literal-ID collisions across 9 attempts; 0 strong-overlap mechanical hits in 5 accepted traces; structurally eliminated M10b's worst-case drift mode at the targeted N=5.
- **Row 4a — partial-closure-with-residuals** at all three N-scopes (M11a-alone N=5; M10b+M11a N=8; combined N=10 primary scope). V2-Opus failure rate **30%** (95% CI [6.7%, 65.2%]) vs V2-3B **50%** (95% CI [18.7%, 81.3%]) — 20 pp reduction at point estimate, non-overlapping point estimates but partially overlapping CIs. *(Combined-N=10 V2-Opus reference corrected from M11a Commit D's original 2/10 = 20.0% per M11b-Commit-D-surfaced counting error in M11a's aggregation — test_v4 V2-Opus joint-bar failure was missed; see runs/19 §"Row 4a paper-line — combined N=10 primary" + correction-note for full audit; correction commit lands prior to M11b Commit D.)*
- **Independent finding (refines Row 4a mechanism):** test_v12 V2-Opus false-inits (`grocer_back_in_stock` + `calendar_yoga_suggest`) are **bytewise identical to V2-3B's false-inits on the same trace**. The V2-prompt YES-bias on retail-back-in-stock / calendar-suggestion / casual-social-meetup distractor classes is **V2-prompt-inherent, not Opus-specific permissiveness**. Test_v11's `trivia_league_round` is the same mechanism. → Implies the targeted next lever is V4 prompt (M11a-extension scope), not further model-scale upgrades.
- **Pareto headline holds across N=10 external sample:** V2-Opus 13.0×-33.0× cheaper per hit than poll-Opus (`runs/README.md` row 19; M11a appendix table).
- Three named futures: **M11a-extension** (V4 prompt + self-restate pre-flight + N=20+); **M11b (this plan; cross-model Claude tier sweep)**; **M11c** (hierarchical routing).

M11b's question is structurally different from M11a's. M11a asked "did the protocol revision close M10b's drift mode?" (H2-protocol-revision) and "did model-scale close M8b's V2-3B coverage gap?" (H2-coverage). M11b asks **"where do Sonnet 4.6 and Haiku 4.5 sit on the cost-quality Pareto vs Opus 4.7 at the M11a N=10 frozen external sample?"** — a model-family-tier cost-curve question, not a closure question.

## Thesis

> Sweeping the V2 arbiter across the Claude tier ladder (Haiku 4.5 → Sonnet 4.6 → Opus 4.7) at M11a's frozen N=10 external sample produces a cost-quality Pareto with six pre-registered outcome branches (Row 1 strict-Pareto-improvement-on-Haiku; Row 2 Sonnet sweet spot; Row 3 graded-cost-curve-Opus-required-for-parity; Row 4a Haiku-tier-falls-to-V2-3B-floor; Row 4b Haiku-tier-falls-below-V2-3B-floor; Row 5 underpowered-at-N=10). The bytewise-identical-false-init prediction from M11a (`grocer_back_in_stock` / `calendar_yoga_suggest` / `trivia_league_round`) is also tested as a 3-branch diagnostic (confirm / partial / falsify) of whether V2-prompt YES-bias is V2-prompt-inherent across the entire Claude family or whether smaller-tier models break the inheritance.

Each branch is publishable. The experiment is not designed to find a particular outcome.

---

## Locked design choices (D1-D7)

Author and user converged on the **maximum-defensibility posture**: include every cell where marginal cost is bounded; pre-register everything; triangulate determinism; archive pricing attestation; lock paper-line text per outcome branch before any cell runs. Total budget impact for the maximum-defensibility additions: ~$0.04 over the minimum-viable design (the V2-3B + cron30s belt-and-suspenders re-runs are free local cells; the extra drift smoke cells are pennies at Sonnet/Haiku tier).

### D1. Trace scope — LOCKED: full M11a combined-N=10 external sample

Traces: `test_v4`, `test_v5`, `test_v6`, `test_v7`, `test_v8`, `test_v11`, `test_v12`, `test_v13`, `test_v14`, `test_v15`. Inherits M11a's pre-reg'd "combined N=10 primary scope for H2 coverage rate" verbatim (`runs/19-iterative-banned-list-extension.md` §"Headline-scope commitment"). Reviewer-defense: subsets give "you cherry-picked traces" (M11a-only subset) or "selection on the dependent variable" (failure-only subset); full N=10 forecloses both attacks.

### D2. Cell matrix per trace — LOCKED: maximum-coverage cell matrix at bounded cost

Per-trace cells run at Commit D:

| cell | agent | arbiter | per-cell cost | × N traces | M11b cells |
|---|---|---|---|---|---|
| V2-Sonnet | HeargentZAWide | ClaudeArbiter (V2 prompt, claude-sonnet-4-6) | ~$0.011 | 10 | 10 |
| V2-Haiku | HeargentZAWide | ClaudeArbiter (V2 prompt, claude-haiku-4-5) | ~$0.0035 | 10 | 10 |
| poll-Sonnet | react_poll_claude (model=sonnet) | (Sonnet poll on every tick) | ~$0.20 | 10 | 10 |
| poll-Haiku | react_poll_claude (model=haiku) | (Haiku poll on every tick) | ~$0.067 | 10 | 10 |
| V3-Sonnet | HeargentZAWide | ClaudeArbiter (V3 prompt, claude-sonnet-4-6) | ~$0.007 | {test_v4, test_v5} | 2 |
| V3-Haiku | HeargentZAWide | ClaudeArbiter (V3 prompt, claude-haiku-4-5) | ~$0.002 | {test_v4, test_v5} | 2 |
| **Harness subtotal** |  |  |  |  | **44** |
| **Belt-and-suspenders re-run at Commit B** (verifies M11a `19d-*` carry-forward JSONs bit-identical against fresh re-runs; free local cells) |  |  |  |  |  |
| V2-3B re-run | HeargentZAWide | ContentArbiter (V2 prompt, qwen2.5:3b-instruct) | $0 (local) | 10 | 10 |
| cron30s re-run | CronKeyword30s | — | $0 (local) | 10 | 10 |
| **Belt-and-suspenders subtotal** |  |  |  |  | **20** |
| **Drift smoke** (B baseline + D-start + D-end triangulation; see D3) |  |  |  |  |  |
| Opus carryover smoke (B PASS gate vs `17b-*`) | HeargentZAWide | ClaudeArbiter (V2, opus) | ~$0.05 | {dev_v2, test_v1, test_v2} | 3 |
| Sonnet baseline + D-start + D-end | HeargentZAWide | ClaudeArbiter (V2, sonnet) | ~$0.005 | {dev_v2, test_v1, test_v2} × 3 phases | 9 |
| Haiku baseline + D-start + D-end | HeargentZAWide | ClaudeArbiter (V2, haiku) | ~$0.0015 | {dev_v2, test_v1, test_v2} × 3 phases | 9 |
| **Drift smoke subtotal** |  |  |  |  | **21** |
| **TOTAL M11b cells** |  |  |  |  | **85** |

Reviewer-defense breakdown:
- **V2-Sonnet + V2-Haiku × N=10** = the model-tier cost-curve cells (the M11b question).
- **poll-Sonnet + poll-Haiku × N=10** = matched-arbiter cost denominators per tier; without these, the Pareto comparison is asymmetric ("V2-Sonnet cost-per-hit vs poll-Opus cost-per-hit" — different models in arbiter vs baseline; reviewer attacks "you compared cheaper arbiter against expensive baseline"). Matched-arbiter denominator is reviewer-strongest.
- **V3-Sonnet + V3-Haiku × failure subset {test_v4, test_v5}** = clean second-axis question on V3's model-capability threshold (M9 path-C close was 3B-bound; V3-Opus reached 0.80/1.00 per M10). Resolves "you claimed V3 was capability-bound but never tested at Sonnet/Haiku scale."
- **V2-3B + cron30s belt-and-suspenders re-runs × N=10 at Commit B** = bit-identical verification against M11a's `19d-*` JSONs; both cell types are local-deterministic ($0 cost, ~5 min compute). Forecloses the reviewer attack "what if the M11a JSONs you're carrying forward drifted between M11a Commit D and M11b Commit D?"
- **Carry-forward from M11a (not re-run)**: V2-Opus × N=10 (Opus drift verified at Commit B via 3-cell smoke vs `17b-*`); poll-Opus × N=10 (Opus drift verified same path). M11a's 19d-* JSONs are referenced verbatim for V2-Opus and poll-Opus results; M11b adds nothing to those cells.

### D3. Drift smoke — LOCKED: triangulated B-baseline + D-start + D-end determinism observation

Sonnet 4.6 and Haiku 4.5 have NO prior milestone baseline anywhere in the repo. Opus 4.7 has the `17b-*` baseline verified bit-identical 2026-04-27 → 05-13 (M10 → M11a Commit D, 16 days).

Three-phase drift smoke design:

**Phase 1 — Commit B (pre-harness):**
- **Opus carryover PASS gate** (3 cells): V2-Opus on dev_v2/test_v1/test_v2; bit-identical compare against `runs/data/17b-content-opus-v2-*.json`. PASS = no Opus 4.7 drift since M11a Commit D + the M11b rate-table refactor preserved Opus path bit-identically. **FAIL halts Commit B** (Opus version rotated or refactor regressed). Cost ~$0.15.
- **Sonnet baseline** (3 cells): V2-Sonnet on dev_v2/test_v1/test_v2; stored as `runs/data/20b-baseline-content-sonnet-v2-{dev_v2,test_v1,test_v2}.json`. Not bit-compared at Commit B (no prior reference); serves as the reference for Phase 2 + Phase 3. Cost ~$0.015.
- **Haiku baseline** (3 cells): V2-Haiku on dev_v2/test_v1/test_v2; stored as `runs/data/20b-baseline-content-haiku-v2-{dev_v2,test_v1,test_v2}.json`. Same role for Haiku. Cost ~$0.0045.

**Phase 2 — Commit D (pre-harness, immediately before the 44-cell harness fires):**
- **Sonnet pre-harness smoke** (3 cells): re-run; bit-compare against Phase 1 Sonnet baseline. PASS = Sonnet stable across Commit-B → Commit-D-start delta (likely 1-3 days).
- **Haiku pre-harness smoke** (3 cells): same for Haiku.

**Phase 3 — Commit D (post-harness, immediately after the 44-cell harness completes):**
- **Sonnet post-harness smoke** (3 cells): re-run; bit-compare against Phase 1 Sonnet baseline (and against Phase 2 Sonnet for within-harness-window stability). PASS = Sonnet stable across the entire Commit D harness execution window.
- **Haiku post-harness smoke** (3 cells): same for Haiku.

**Drift-smoke verdict policy (pre-registered at Commit A):**
- Opus carryover (Phase 1): PASS gate; FAIL halts Commit B.
- Sonnet + Haiku Phase 2 + Phase 3: **observational, not halt-gate**. PASS = within-milestone determinism verified empirically across B → D-start → D-end (the deliverable). FAIL = drift observed; record per-field deltas (arbiter_calls / yes_rate / input_tok / output_tok / dispatched_model / hit / false_h) as M11b empirical finding; **does not halt Commit D** — the 44-cell harness is the deliverable; drift is a separately-reported paper-line observation that informs M11c/M11b-extension design.

Reviewer-defense: triangulated B → D-start → D-end smoke explicitly bounds Sonnet + Haiku determinism within the harness execution window. Reviewer cannot say "Sonnet drifted mid-harness and you didn't notice" — Phase 2 and Phase 3 bracket the harness window with bit-identical compares.

### D4. Pricing — LOCKED: HARD GATE + pricing attestation archive at Commit A

Locked rates per million tokens (subject to Commit-A verification step below):
- **claude-sonnet-4-6:** $3 input / $15 output (placeholder; verify at Commit A)
- **claude-haiku-4-5:** $1 input / $5 output (placeholder; verify at Commit A)
- **claude-opus-4-7:** **$15 input / $75 output** (locked at M10 SHA `68d42e3`, `agent/arbiter.py:15-16` — DO NOT EDIT)

**Hard gate at Commit A (pricing verification + attestation archive):**

1. Fetch the current Anthropic pricing page (anthropic.com/pricing or equivalent canonical source).
2. Extract input + output per-million-token rates for `claude-sonnet-4-6` and `claude-haiku-4-5`.
3. Verify Opus 4.7 rate still matches the M10 lock ($15 / $75); if Opus rate has rotated, document as a Commit-A finding but **do not re-price** (M10 lock holds per `agent/arbiter.py:15-16` precedent).
4. Archive the fetched content as `runs/data/20a-pricing-attestation-{YYYY-MM-DD}.json` with: `{ "fetched_at": ISO timestamp, "source_url": str, "rates_per_million_tokens": { "claude-opus-4-7": {"input": 15.0, "output": 75.0}, "claude-sonnet-4-6": {"input": X, "output": Y}, "claude-haiku-4-5": {"input": X, "output": Y} }, "raw_text_excerpt": "...", "notes": "..." }`. This file is committed at Commit A as the rate-lock source-of-truth.
5. If the verified Sonnet or Haiku rates differ from the placeholders above, **update the placeholders at Commit A**, recompute the budget estimate, and only then lock by copying the plan to `runs/20-cross-model-sweep.md`.

Per-model rate constants in code (locked at Commit A, written at Commit B):
- `OPUS_INPUT_USD_PER_M = 15.0`, `OPUS_OUTPUT_USD_PER_M = 75.0` (existing; do not edit)
- `SONNET_INPUT_USD_PER_M = {verified}`, `SONNET_OUTPUT_USD_PER_M = {verified}`
- `HAIKU_INPUT_USD_PER_M = {verified}`, `HAIKU_OUTPUT_USD_PER_M = {verified}`

Any Anthropic mid-M11b rate change is documented but does not re-price the M11b cells (analogous to how Opus rates locked at M10 are unchanged through M10b/M11a/M11b regardless of any actual rate-page changes).

Reviewer-defense: pricing attestation archive at Commit A is a timestamped, auditable, in-repo artifact. Reviewer cannot say "your locked rates don't match anthropic.com today" — the rates are pinned to a specific timestamp and source that's archived in-repo.

### D5. Decision rules + outcome rows — LOCKED: 4 P-bars + 6-row table + primary-vs-secondary outcome block + bootstrap CI sensitivity

**Primary vs secondary outcomes (pre-registered at Commit A; closes multiple-comparison attack):**

M11b reports two pre-registered outcomes; each has a separate locked paper-line:

1. **PRIMARY: model-family Pareto at combined-N=10.** Identified mechanically as one of the 6 rows in the outcome table below from P1/P2/P3 verdicts. This is the M11b headline.
2. **SECONDARY: D7 bytewise-identical-false-init diagnostic at combined-N=10.** Identified mechanically as one of 3 branches (confirm / partial / falsify) per §D7 with locked paper-line per branch. Reported as a refined mechanism observation alongside the primary outcome.

Both outcomes are pre-registered before any cell runs; the locked paper-line text per branch is in this plan (filled with integer placeholders at Commit D, wording not edited). **No post-hoc reassignment between primary and secondary, no addition of post-hoc outcomes.**

Additionally reported but **not pre-registered as outcomes**:
- Sonnet/Haiku within-milestone drift smoke result (Phase 2 + Phase 3 per §D3) — observational characterization.
- V3-Sonnet + V3-Haiku attribution cells on {test_v4, test_v5} — observational second-axis on V3's model-capability threshold; not part of the primary Pareto outcome.
- Per-cell Pareto plot ($-per-cell × hit_rate scatter) — visualization of the data underlying P4.

Reviewer-defense: explicit primary/secondary separation defuses "you have 6 rows + V3 + D7 + drift smoke + Pareto plot = multiple-comparison fishing" — the primary is mechanically determined by P1/P2/P3, secondary is mechanically determined by D7 branch, everything else is observational/visual.

**P-bars (locked at Commit A):**

- **P1 — Sonnet match-with-Opus joint bar:** V2-Sonnet "matches" V2-Opus if:
  - (a) `|hit_rate(V2-Sonnet) − hit_rate(V2-Opus)| ≤ 0.10` AND `|false/h(V2-Sonnet) − false/h(V2-Opus)| ≤ 2.5/h` per-trace majority (≥ 6 of 10 traces); AND
  - (b) combined-N=10 failure-rate point estimates within ±10pp AND 95% Clopper-Pearson CIs overlap.
- **P2 — Haiku match-with-Opus joint bar:** identical to P1, Haiku for Sonnet.
- **P3 — Tier beats V2-3B floor:** V2-Sonnet (and V2-Haiku) failure rate strictly less than V2-3B's 50% with non-overlapping 95% Clopper-Pearson CI lower bound at combined-N=10 scope — i.e., the cross-family upgrade is doing some work.
- **P4 — Pareto headline:** report per-cell mean cost ± per-cell cost-per-hit (denominator = # of hits in the cell; zero-hit cells reported but excluded from cost-per-hit aggregate). Compute Pareto ratios:
  - V2-Sonnet cost-per-hit vs poll-Sonnet cost-per-hit (matched-arbiter)
  - V2-Haiku cost-per-hit vs poll-Haiku cost-per-hit (matched-arbiter)
  - V2-Sonnet cost-per-hit vs V2-Opus cost-per-hit (cross-tier, same prompt)
  - V2-Haiku cost-per-hit vs V2-Opus cost-per-hit (cross-tier)

**Bootstrap CI sensitivity analysis (pre-registered at Commit A; reported alongside Clopper-Pearson):**

Primary CI is Clopper-Pearson binomial (consistent with M11a). **Sensitivity analysis at Commit D** also reports a bootstrap CI computed from per-trace failure outcomes (2000-resample non-parametric bootstrap; seed locked at Commit A as `BOOTSTRAP_SEED = 42`). If bootstrap CI differs from Clopper-Pearson by > 5pp at either bound, report as Commit-D sensitivity-analysis observation. Reviewer-defense: "your CI assumes independent trials" → "we also report bootstrap CIs without that assumption; results [agree / differ at the {X}pp level]."

**Outcome row table (locked at Commit A; 6 rows; locked paper-line per row; integer placeholders filled at Commit D; wording not edited):**

| V2-Sonnet vs V2-Opus | V2-Haiku vs V2-Opus | Row | Headline |
|---|---|---|---|
| matches (P1 PASS) | matches (P2 PASS) | **Row 1** | Strict Pareto: Haiku sufficient; Opus is overkill; deployment shape collapses to Haiku |
| matches (P1 PASS) | P2 FAIL, P3 PASS on Haiku | **Row 2** | Sonnet is sweet spot; Haiku partial-reduction; cost-tier-graded |
| P1 FAIL, P3 PASS on Sonnet | P2 FAIL, P3 PASS on Haiku | **Row 3** | Cost-curve steep; Opus required for parity; mid-tier is M11c routing-lower-tier candidate |
| any | P3 FAIL on Haiku (no improvement vs V2-3B; CI lower-bound overlaps V2-3B point estimate) | **Row 4a** | Cross-family scale non-uniform; Haiku falls below H2-improvement threshold; Sonnet may still be viable |
| any | Haiku failure rate strictly higher than V2-3B's 50% | **Row 4b** | Mid-tier failure mode; cross-family upgrade harmful at Haiku scale; document mechanism |
| all CIs overlap V2-3B + V2-Opus | all CIs overlap V2-3B + V2-Opus | **Row 5** | Underpowered at N=10; defer to M11b-extension N=20+ |

**Locked paper-line text per row (filled with observed counts at Commit D; wording is not edited):**

**Row 1 — Strict Pareto (Haiku sufficient):**
> *"Across N=10 fresh externally-authored traces under the M11a iteratively-extended-banned-list protocol (three protocol generations combined: M10 frozen list test_v4/v5; M10b frozen list test_v6/v7/v8; M11a iteratively-extended list test_v11..v15), V2-Sonnet failure rate {Xs}/10 = {Ys%} (95% CP CI [{Ls%}, {Hs%}]; bootstrap CI [{Lbs%}, {Hbs%}]) and V2-Haiku failure rate {Xh}/10 = {Yh%} (95% CP CI [{Lh%}, {Hh%}]; bootstrap CI [{Lbh%}, {Hbh%}]) both match V2-Opus failure rate 3/10 = 30.0% (corrected per M11b-Commit-D-surfaced M11a aggregation error; see runs/19 §"Row 4a paper-line — combined N=10 primary" correction-note) within ±10pp at point estimate with overlapping CIs. Pareto headline: V2-Haiku is {N}× cheaper per hit than V2-Opus and {M}× cheaper per hit than poll-Haiku at matched-arbiter cost denominator; V2-Sonnet is {O}×/{P}× respectively. Strict Pareto improvement: the Claude tier curve flattens at Haiku for this workload; Opus is overkill at the M11a sample's distractor distribution. Deployment shape collapses to Haiku as default with no observed quality penalty at N=10. Cross-protocol caveat from M11a defense #5 inherited unchanged; cross-tier comparison is internally consistent per trace."*

**Row 2 — Sonnet sweet spot:**
> *"Across N=10 fresh externally-authored traces under three protocol generations, V2-Sonnet failure rate {Xs}/10 = {Ys%} (95% CP CI [{Ls%}, {Hs%}]; bootstrap CI [{Lbs%}, {Hbs%}]) matches V2-Opus failure rate 3/10 = 30.0% (corrected per M11b-Commit-D M11a-aggregation-correction; see runs/19 correction-note) within ±10pp with overlapping CIs (P1 PASS). V2-Haiku failure rate {Xh}/10 = {Yh%} (CI [{Lh%}, {Hh%}]; bootstrap [{Lbh%}, {Hbh%}]) does not match V2-Opus (P2 FAIL) but strictly beats V2-3B's 50% floor (P3 PASS; lower-CI bound non-overlapping with V2-3B point estimate). Pareto headline: V2-Sonnet is {N}× cheaper per hit than V2-Opus at cross-tier comparison; V2-Haiku trades partial quality for {M}× cost reduction vs V2-Opus. Sonnet is the cost-quality sweet spot for this workload; Haiku is a graded fallback (M11c hierarchical-routing candidate for the lower tier). Cross-protocol caveat inherited; cross-tier comparison internally consistent per trace."*

**Row 3 — Graded cost curve, Opus required for parity:**
> *"Across N=10 fresh externally-authored traces under three protocol generations, V2-Sonnet failure rate {Xs}/10 = {Ys%} (CI [{Ls%}, {Hs%}]; bootstrap [{Lbs%}, {Hbs%}]) does not match V2-Opus (P1 FAIL) but strictly beats V2-3B's 50% (P3 PASS). V2-Haiku failure rate {Xh}/10 = {Yh%} (CI [{Lh%}, {Hh%}]; bootstrap [{Lbh%}, {Hbh%}]) same pattern (P2 FAIL, P3 PASS). Pareto headline: cross-tier cost curve is steep within the Claude family for this workload; Opus required for full parity with M10/M11a's V2-Opus close. Sonnet and Haiku are both M11c hierarchical-routing lower-tier candidates: cheaper per hit but with measurable quality penalty vs Opus. Cross-protocol caveat inherited; cross-tier comparison internally consistent per trace."*

**Row 4a — Haiku falls to V2-3B level (insufficient model capability at Haiku scale):**
> *"Across N=10 fresh externally-authored traces under three protocol generations, V2-Haiku failure rate {Xh}/10 = {Yh%} (CI [{Lh%}, {Hh%}]; bootstrap [{Lbh%}, {Hbh%}]) does not strictly beat V2-3B's 50% — the CI lower bound overlaps V2-3B's point estimate (P3 FAIL on Haiku). V2-Sonnet may still match V2-Opus (P1 result reported in §"Per-tier P-verdicts"). Cross-family scale within the Claude family is non-uniform across tier at the Haiku scale: model-family upgrade is necessary but Haiku is insufficient capability for the M11a sample's distractor distribution. Mechanism diagnosis: [per-trace failure inspection at Commit D]. M11c hierarchical-routing cannot route to Haiku as the lower-tier baseline without a quality penalty; routing must escalate at or above Sonnet to maintain V2-Opus parity. Cross-protocol caveat inherited."*

**Row 4b — Haiku worse than V2-3B (harmful cross-family swap at the Haiku tier):**
> *"Across N=10 fresh externally-authored traces under three protocol generations, V2-Haiku failure rate {Xh}/10 = {Yh%} (CI [{Lh%}, {Hh%}]; bootstrap [{Lbh%}, {Hbh%}]) is strictly higher than V2-3B's 50% — V2-Haiku introduces failure modes V2-3B did not exhibit at the M11a sample. Mechanism diagnosis: [per-trace failure inspection at Commit D; likely false-h spikes from Haiku over-YES on borderline V2-enumeration items, or hit-side drops from Haiku over-NO on out-of-V2-enumeration content]. Cross-family upgrade at the Haiku scale is empirically harmful for this workload; the cost-quality curve is non-monotonic across the Claude tier ladder. M11c routing cannot include Haiku as a useful tier; deployment defaults to Sonnet or Opus. The M11b finding falsifies the assumption that the Claude tier ladder is uniformly cost-quality-monotonic. Cross-protocol caveat inherited."*

**Row 5 — Underpowered at N=10:**
> *"Across N=10 fresh externally-authored traces under three protocol generations, V2-Sonnet failure rate {Xs}/10 = {Ys%} (CI [{Ls%}, {Hs%}]; bootstrap [{Lbs%}, {Hbs%}]) and V2-Haiku failure rate {Xh}/10 = {Yh%} (CI [{Lh%}, {Hh%}]; bootstrap [{Lbh%}, {Hbh%}]) have 95% CIs that overlap with both V2-3B's 50% (CI [18.7%, 81.3%]) and V2-Opus's 30% (corrected from 20%; CI [6.7%, 65.2%]; see runs/19 correction-note). The cross-tier comparison is underpowered at N=10 to distinguish ±10pp deltas. Point estimates (Pareto table) are consistent with the [Row 2/3/4 pattern at point estimate], but the binomial CIs preclude definitive cross-tier ranking at the pre-registered ±10pp threshold. Bootstrap CIs from per-trace outcomes are also reported and yield the same overlap conclusion. The M11b finding is the under-power observation itself; substantive cross-tier ranking is deferred to M11b-extension scope (N=20+) for tightened CIs; named here as a separately-pre-registered milestone."*

### D6. Code changes — LOCKED: per-model rate table + `--arbiter-model` CLI flag

Required at Commit B (~30-40 lines across 3 files):

**`agent/arbiter.py`:**
- Add module-level rate constants alongside existing OPUS_*:
  - `SONNET_INPUT_USD_PER_M = {verified at Commit A}`, `SONNET_OUTPUT_USD_PER_M = {verified at Commit A}`
  - `HAIKU_INPUT_USD_PER_M = {verified at Commit A}`, `HAIKU_OUTPUT_USD_PER_M = {verified at Commit A}`
- Add per-model rate lookup helper:
  ```python
  def _rates_for(model: str) -> tuple[float, float]:
      """Return (input_usd_per_m, output_usd_per_m) for a given model alias."""
      if model.startswith("claude-opus"):
          return OPUS_INPUT_USD_PER_M, OPUS_OUTPUT_USD_PER_M
      if model.startswith("claude-sonnet"):
          return SONNET_INPUT_USD_PER_M, SONNET_OUTPUT_USD_PER_M
      if model.startswith("claude-haiku"):
          return HAIKU_INPUT_USD_PER_M, HAIKU_OUTPUT_USD_PER_M
      raise ValueError(f"Unknown model for rate lookup: {model!r}")
  ```
  Substring dispatch (rather than exact match) for stability against alias rotation within a major version.
- `ClaudeArbiter.cost_usd` property at L233-237: replace hardcoded OPUS_* with `_rates_for(self.model)` lookup.
- `ClaudeArbiter.__init__` already accepts `model` parameter at L209 — no signature change.

**`baselines/react_poll_claude.py`:**
- Replace `from agent.arbiter import OPUS_INPUT_USD_PER_M, OPUS_OUTPUT_USD_PER_M` at L6 with `from agent.arbiter import _rates_for`.
- `cost_usd` method at L116-120: replace hardcoded OPUS_* with `_rates_for(self.model)` lookup.
- `__init__` already accepts `model` parameter at L33 — no signature change.

**`eval/run_trace.py`:**
- Add `--arbiter-model` argument: `choices=["opus", "sonnet", "haiku"]`, default `"opus"`. Help text references locked rates per Commit A pricing attestation.
- Add alias mapping (module-level constant): `_MODEL_ALIASES = {"opus": "claude-opus-4-7", "sonnet": "claude-sonnet-4-6", "haiku": "claude-haiku-4-5"}`.
- Thread resolved model name through `ClaudeArbiter(system_prompt=prompt, model=_MODEL_ALIASES[args.arbiter_model])` at L132.
- For `--agent baselines.react_poll_claude:ReactPollClaude`: thread `model=_MODEL_ALIASES[args.arbiter_model]` through `cls(model=...)` at L141 (or via a small refactor of `_load_agent` to recognize the poll-Claude class explicitly). The cleanest path is to extend `_load_agent`'s no-arbiter-mode branch (L141) to check if `cls` has a `model` parameter and thread `args.arbiter_model` through. Final wire choice locked at Commit A; the principle is: `--arbiter-model` controls the Claude model wherever a Claude API call is made (arbiter OR poll baseline).
- Persist `arbiter_model` in metrics JSON output for reproducibility (alongside the existing `arbiter_system_prompt` echo).

**Commit B regression smoke gate:** after the 3-file edits, run the 3-cell Opus carryover smoke vs `17b-*` JSONs. PASS confirms the rate-table refactor + CLI flag did not break the Opus path bit-identically. FAIL halts Commit B (the refactor regressed Opus).

### D7. Cross-model independent-finding prediction — LOCKED: 3-branch diagnostic (confirm / partial / falsify) with locked paper-line per branch

M11a closed with the independent finding: **test_v12 V2-Opus false-inits are bytewise identical to V2-3B's** (`grocer_back_in_stock` 'Avocado back in stock' + `calendar_yoga_suggest` recurring-event suggestion); test_v11's `trivia_league_round` Saturday-evening pub-trivia social-meetup is the same V2-prompt-inherent YES-bias mechanism.

**M11b pre-registered binary-with-partial-branch diagnostic (locked at Commit A; mechanically identified at Commit D):**

The diagnostic asks: do V2-Sonnet and V2-Haiku surface the same false-init event IDs as V2-Opus did at M11a on test_v11 (`trivia_league_round`) and test_v12 (`grocer_back_in_stock`, `calendar_yoga_suggest`)? Three pre-registered outcome branches, identified mechanically from the per-cell false-init event-ID lists at Commit D:

- **D7-confirm:** V2-Sonnet AND V2-Haiku surface all three M11a-flagged event_ids (3 of 3 across both tiers) at point estimate.
- **D7-partial:** V2-Sonnet OR V2-Haiku surfaces a strict subset of the M11a-flagged event_ids (at least one event_id surfaced + at least one event_id NOT surfaced across the cross-product of {Sonnet, Haiku} × {trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest}).
- **D7-falsify:** Neither V2-Sonnet NOR V2-Haiku surfaces any of the three M11a-flagged event_ids at point estimate (0 of 6 cross-product cells).

**Locked paper-line text per D7 branch (filled with observed event-ID assignments at Commit D; wording not edited):**

**D7-confirm:**
> *"The V2-prompt-inherited YES-bias on retail-back-in-stock / calendar-suggestion / casual-social-meetup distractors observed at V2-3B and V2-Opus (M11a independent finding) is reproduced bytewise at V2-Sonnet and V2-Haiku. V2-Sonnet surfaces {3 listed event_ids on the {test_v11, test_v12} pair}; V2-Haiku surfaces {3 listed event_ids on the same pair}. The mechanism is V2-prompt-inherent across the entire Claude family + qwen2.5:3b — not a model-scale or model-family property. The targeted next lever is V4 prompt revisions adding explicit NO examples for these distractor classes (M11a-extension scope), not further cross-family swap. The Row {primary outcome row} finding is refined: model-family-tier swap below Opus does not address the V2-prompt-inherent distractor mechanism on this sample."*

**D7-partial:**
> *"The V2-prompt-inherited YES-bias prediction is partially confirmed across the Claude tier ladder. V2-Sonnet surfaces {observed Sonnet subset, e.g., grocer_back_in_stock + calendar_yoga_suggest but NOT trivia_league_round}; V2-Haiku surfaces {observed Haiku subset}; at least one M11a-flagged event_id is surfaced AND at least one is NOT surfaced across the {Sonnet, Haiku} × {trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest} cross-product. Mechanism diagnosis: V2-prompt phrasing for {distractor classes preserved across all tiers} is read as YES across the entire Claude family + qwen2.5:3b (V2-prompt-inherent component); V2-prompt phrasing for {distractor classes broken at one or more tiers} is tier-dependent (e.g., NO at {tier} vs YES at {other tiers}). The V2-prompt YES-bias mechanism is partially V2-prompt-inherent (cross-tier-stable component) and partially tier-dependent (cross-tier-variable component). M11a-extension V4 prompt revision is the more targeted lever for the cross-tier-stable component; M11c hierarchical routing has additional traction on the cross-tier-variable component. The Row {primary outcome row} finding is refined: model-family-tier swap addresses a subset of the V2-prompt-inherent distractor mechanism on this sample."*

**D7-falsify:**
> *"The V2-prompt-inherited YES-bias prediction is falsified at every Claude tier below Opus: V2-Sonnet says NO to all 3 M11a-flagged event_ids (`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`); V2-Haiku says NO to all 3 of the same. Within-Claude-family selectivity differs across tier at the entire {Sonnet, Haiku} sub-ladder; M11a's bytewise-identical-false-init finding was a V2-3B-and-V2-Opus-shared property that does not extend to mid-tier and small-tier Claude. M11c hierarchical routing has substantially more meat than V4 prompt revision as a near-term lever for this distractor mechanism — routing to Sonnet or Haiku as the default arbiter eliminates the V2-prompt YES-bias entirely on the M11a-flagged distractors at this sample. Mechanism diagnosis: [per-event V2-prompt phrasing analysis explaining the tier-dependent reading; likely Sonnet/Haiku are stricter on the V2 'message or delivery directed personally to the user' clause for back-in-stock / recurring-event-suggestion / casual-social-meetup content than Opus and 3B are]. The Row {primary outcome row} finding is refined: model-family-tier swap below Opus is the dominant lever for the V2-prompt YES-bias distractor mechanism on this sample."*

Reviewer-defense: 3-branch D7 with locked paper-line per branch + mechanical identification rule (per-cell false-init event-ID lists at Commit D) eliminates "your independent finding is post-hoc opportunistic" — the prediction was generated from M11a Commit D's mechanism-attribution and tested at M11b's expanded model-tier axis with no degrees of freedom for analyst discretion at Commit D.

---

## Three-commit protocol (M10-shape, not M10b/M11a no-code shape)

| Commit | Content | Gates |
|---|---|---|
| **A** | (1) Pricing verification per §D4 (fetch + archive `runs/data/20a-pricing-attestation-{date}.json`; update Sonnet/Haiku rate placeholders if needed). (2) Pre-reg copy of this plan to `runs/20-cross-model-sweep.md` with appropriate header / date / pre-reg SHA placeholders + final-verified-rates + 6-row paper-line + 3-branch D7 paper-line all locked verbatim. (3) `sandbox/event_trace.py`, `agent/`, `baselines/`, `eval/`, `pyproject.toml`, `uv.lock` — NOT touched at Commit A. | Pricing attestation archived + committed. |
| **B** | (1) `agent/arbiter.py` per-model rate table + `_rates_for` helper. (2) `baselines/react_poll_claude.py` rate-lookup refactor. (3) `eval/run_trace.py` `--arbiter-model` CLI flag + alias mapping + threading. (4) 3-cell V2-Opus drift smoke vs `17b-*` (PASS gate). (5) 3-cell V2-Sonnet baseline + 3-cell V2-Haiku baseline stored as `20b-baseline-*.json`. (6) 10-cell V2-3B re-run + 10-cell cron30s re-run on N=10 sample; bit-compare against M11a's `19d-content-3b-v2-*.json` + `19d-cron30-*.json` (PASS gate; FAIL halts Commit B as M11a-data-drift finding). | (4) PASS = bit-identical Opus carryover vs `17b-*`. (6) PASS = M11a `19d-*` JSONs verified bit-identical against fresh re-runs. Commit B total spend ≈ $0.20. |
| **D** | (1) Phase 2 Sonnet + Haiku drift smoke (6 cells; pre-harness; bit-compare against Phase 1 baselines). (2) 44-cell harness matrix per §D2 cell table. (3) Phase 3 Sonnet + Haiku drift smoke (6 cells; post-harness; bit-compare against Phase 1 baselines + Phase 2). (4) Aggregate analysis: per-trace observations + per-tier failure-rate metrics + Pareto plot data + Clopper-Pearson CI + bootstrap CI sensitivity per scope + P1/P2/P3/P4 verdicts + outcome row identification + D7 branch identification. (5) `runs/20-cross-model-sweep.md` results appendix + row 20 in `runs/README.md` + paper framing line update for M11b's outcome row at combined-N=10 scope. | Verbatim eval against frozen P1-P4. Sonnet/Haiku Phase 2 + Phase 3 drift smoke results reported but not halt-gated (paper-line item per §D3). |

(No Commit C: there's no externally-authored-trace step at M11b.)

---

## Pre-registered analysis (mirror M11a's structure; filled at Commit D)

### Per-trace observations table (filled at Commit D)

| trace | V2-3B hit (re-verified at Commit B) | V2-Opus hit (M11a carry-forward) | V2-Sonnet hit | V2-Sonnet false/h | V2-Haiku hit | V2-Haiku false/h | poll-Sonnet hit | poll-Haiku hit | poll-Opus hit (M11a carry-forward) | cron30s hit (re-verified at Commit B) | V2-Sonnet matches V2-Opus per P1? | V2-Haiku matches V2-Opus per P2? | False-init event_ids per cell |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

10 rows (test_v4..v15 minus v9/v10). Last column lists the false-init event_ids per {V2-Sonnet, V2-Haiku, V2-Opus, V2-3B} cell per trace; this column feeds the D7 mechanical identification.

### Per-tier aggregate failure-rate metrics at combined-N=10 (filled at Commit D)

| Tier | Failures (joint bar: hit < 0.80 OR false/h > 5.0/h) | Failure rate | 95% CP CI | Bootstrap CI (2000 resamples, seed=42) | Δ vs V2-3B (pp) | Δ vs V2-Opus (pp) | CI-overlap with V2-3B? | CI-overlap with V2-Opus? |
|---|---|---|---|---|---|---|---|---|
| V2-3B (M11a carry-forward + Commit B re-run) | 5/10 | 50.0% | [18.7%, 81.3%] | [observed] | — | — | — | — |
| V2-Opus (M11a carry-forward; corrected) | 3/10 | 30.0% | [6.7%, 65.2%] | [observed] | -20 pp | — | NO | — |
| V2-Sonnet | {X}/10 | {Y}% | [{L%}, {H%}] | [{Lb%}, {Hb%}] | {pp} | {pp} | {yes/no} | {yes/no} |
| V2-Haiku | {X}/10 | {Y}% | [{L%}, {H%}] | [{Lb%}, {Hb%}] | {pp} | {pp} | {yes/no} | {yes/no} |

### Pareto-cost table per tier at combined-N=10 (filled at Commit D)

| Tier | Mean $/cell | Mean $/hit | Min $/hit | Max $/hit | Matched-arbiter ratio vs poll-{same-tier} | Cross-tier ratio vs V2-Opus |
|---|---|---|---|---|---|---|

8 rows: V2-3B, V2-Opus, V2-Sonnet, V2-Haiku; poll-Opus, poll-Sonnet, poll-Haiku, cron30s.

### Per-tier P1/P2/P3/P4 verdicts at combined-N=10 (filled at Commit D)

P1 / P2 / P3 / P4 PASS/FAIL per pre-reg §D5 bars verbatim, with the supporting numbers in-line. P-verdicts feed mechanically into the outcome row identification per the 6-row table.

### V3-Sonnet + V3-Haiku attribution on failure subset {test_v4, test_v5} (filled at Commit D)

| trace | V2-3B hit | V2-Opus hit | V3-Opus hit (M10 carry-forward) | V3-Sonnet hit | V3-Haiku hit | V3-Opus failure rate | V3-Sonnet failure rate | V3-Haiku failure rate | Capability threshold for V3? |
|---|---|---|---|---|---|---|---|---|---|

2 rows (test_v4, test_v5). Last column identifies whether the V3 capability threshold falls (a) at or below Haiku (V3-Haiku ≥ 0.80 on both), (b) between Haiku and Sonnet (V3-Haiku < 0.80, V3-Sonnet ≥ 0.80), (c) between Sonnet and Opus (V3-Sonnet < 0.80, V3-Opus ≥ 0.80), or (d) at or above Opus (V3-Opus < 0.80 on either; would itself be a surprising result contradicting M10).

### D7 mechanical identification (filled at Commit D)

| trace | event_id | V2-3B decision (M11a carry-forward + Commit B re-run) | V2-Opus decision (M11a carry-forward) | V2-Sonnet decision | V2-Haiku decision | Cross-tier preservation |
|---|---|---|---|---|---|---|
| test_v11 | trivia_league_round | YES | YES | {Y/N} | {Y/N} | {3/3 / 2/3 / 1/3 / 0/3} preserved across {Opus, Sonnet, Haiku} (out of 3 tiers; counting only YES as "preserves the M11a-flagged false-init") |
| test_v12 | grocer_back_in_stock | YES | YES | {Y/N} | {Y/N} | same |
| test_v12 | calendar_yoga_suggest | YES | YES | {Y/N} | {Y/N} | same |

D7 branch identification rule:
- D7-confirm if all 6 cells in the {Sonnet, Haiku} × 3 event_ids cross-product are YES (V2-prompt YES-bias fully preserved at both new tiers).
- D7-partial if 1-5 of 6 cells are YES (partial preservation).
- D7-falsify if 0 of 6 cells are YES (V2-prompt YES-bias fully absent at both new tiers).

### Sonnet + Haiku within-milestone drift smoke (filled at Commit D)

| Smoke phase | Sonnet PASS/FAIL per-field per-trace | Haiku PASS/FAIL per-field per-trace | Sonnet first-divergence field (if FAIL) | Haiku first-divergence field (if FAIL) |
|---|---|---|---|---|
| Phase 2 (D-start vs B-baseline) | | | | |
| Phase 3 (D-end vs B-baseline) | | | | |
| Phase 3 vs Phase 2 (within-D-window) | | | | |

Reported per §D3 verdict policy. PASS across all three sub-tables = Sonnet + Haiku stable across the entire B → D-start → D-end window.

### Outcome row identification at Commit D (primary outcome)

Per the §D5 6-row outcome table; row identification is mechanical from P1/P2/P3 verdicts + Δfailure-rates + CI-overlap. Locked paper-line text reproduced verbatim with integer placeholders filled.

### D7 branch identification at Commit D (secondary outcome)

Per the §D7 mechanical identification rule; branch identification is mechanical from the 6-cell cross-product YES-count. Locked paper-line text per branch reproduced verbatim with observed event-ID assignments filled.

---

## Cost framework

Total expected M11b spend at locked cell matrix (per §D2):

| Component | Cells | Est. cost |
|---|---|---|
| Harness V2-Sonnet | 10 | $0.11 |
| Harness V2-Haiku | 10 | $0.035 |
| Harness V3-Sonnet | 2 | $0.014 |
| Harness V3-Haiku | 2 | $0.004 |
| Harness poll-Sonnet | 10 | $2.00 |
| Harness poll-Haiku | 10 | $0.67 |
| Belt-and-suspenders V2-3B | 10 | $0 |
| Belt-and-suspenders cron30s | 10 | $0 |
| Opus carryover smoke (Commit B) | 3 | $0.15 |
| Sonnet smoke baseline + Phase 2 + Phase 3 | 9 | $0.045 |
| Haiku smoke baseline + Phase 2 + Phase 3 | 9 | $0.0135 |
| **TOTAL (85 cells)** |  | **~$3.05** |

**Pre-reg budget: $4-5** with headroom for token-volume variation (some traces are 970-1030s of sim_time, longer than co-developed traces; per-cell token volumes might exceed point estimates by 30-50%). Compare M11a's $5.10 actual / $5-6 pre-reg.

---

## Critical files

- `/Users/patrick.gergen/.claude/plans/m11b-cross-model-sweep.md` — this plan; walkthrough at fresh-session kickoff before Commit A
- `runs/20-cross-model-sweep.md` — Commit A pre-reg lands as a copy with appropriate header / date / pre-reg SHA placeholders + final-verified-rates + 6-row paper-line + 3-branch D7 paper-line locked verbatim
- `runs/data/20a-pricing-attestation-{YYYY-MM-DD}.json` — Commit A pricing-rate source-of-truth attestation
- `agent/arbiter.py` — TOUCHED at Commit B (per-model rate table + `_rates_for` helper; ClaudeArbiter.cost_usd refactor); rates locked at Commit A
- `baselines/react_poll_claude.py` — TOUCHED at Commit B (rate-lookup refactor; cost_usd method)
- `eval/run_trace.py` — TOUCHED at Commit B (`--arbiter-model` CLI flag; alias mapping; threading)
- `runs/data/20b-*.json` — Commit B drift baselines (Opus carryover smoke + Sonnet baseline + Haiku baseline) + belt-and-suspenders V2-3B + cron30s re-runs (~26 JSONs)
- `runs/data/20d-*.json` — Commit D cell results (~50 JSONs: 44 harness + 6 Phase 2 smoke; Phase 3 smoke files use `-postharness` suffix)
- `runs/README.md` — row 20 added; status block updated; paper framing line updated to M11b's outcome row at combined-N=10 scope
- `sandbox/event_trace.py`, `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/intent_extractor.py`, baselines/cron / reactive / poll_local, `pyproject.toml`, `uv.lock` — **NOT touched** at any M11b commit

---

## Verification

### Pre-Commit-B bit-identical Opus carryover smoke (drift detector across M11a → M11b)

Carry-forward from M11a §"Pre-Commit-D bit-identical smoke" verbatim, retargeted to M11b Commit B (after rate-table refactor lands). Verifies (a) M11b's code refactor preserves Opus path bit-identically; (b) Opus 4.7 alias remains stable 2026-05-13 → M11b Commit B date.

3 cells on dev_v2/test_v1/test_v2; bit-compare per-field against `runs/data/17b-content-opus-v2-{dev_v2,test_v1,test_v2}.json`. PASS = no Opus 4.7 drift + refactor correctness. **FAIL halts Commit B.**

### Commit-B belt-and-suspenders re-run (verifies M11a `19d-*` carry-forward bit-identical)

10 V2-3B cells (HeargentZAWide + ContentArbiter V2-3B) on N=10 sample (test_v4..v15 minus v9/v10); bit-compare per-field against M11a's `runs/data/19d-content-3b-v2-{test_v4..v15}.json` (test_v4 + test_v5 bit-compare against M10's `17e-*` cells equivalents instead; bit-compare against M10b's `18-*` for test_v6..v8). 10 cron30s cells on same N=10; bit-compare against M11a's `runs/data/19d-cron30-{test_v4..v15}.json` (and equivalent M10/M10b cells for test_v4..v8).

PASS = the V2-3B and cron30s cells M11b carries forward from M11a/M10b/M10 are bit-identical to fresh re-runs (no local-model drift; no harness drift; no trace-definition drift). **FAIL halts Commit B as an M11a-data-drift finding** (M11a's JSONs differ from a fresh re-run on the same trace + agent + arbiter; report drift mode + halt for investigation before continuing to Commit D).

### Commit-B Sonnet + Haiku baselines (Phase 1; stored for Phase 2 + Phase 3 bit-compare)

3 V2-Sonnet cells + 3 V2-Haiku cells on dev_v2/test_v1/test_v2 stored as `runs/data/20b-baseline-content-{sonnet,haiku}-v2-*.json`. Not bit-compared at Commit B (no prior reference); reference for Phase 2 + Phase 3 within-milestone determinism observation.

### Commit-D Phase 2 within-milestone Sonnet + Haiku drift smoke (pre-harness; observational)

Re-run 3+3 cells; bit-compare per-field against Phase 1 baselines. PASS = Sonnet + Haiku stable across Commit-B → Commit-D-start delta. FAIL = record per-field deltas as M11b empirical drift observation; **does NOT halt Commit D** — harness fires immediately after.

### Commit-D Phase 3 within-milestone Sonnet + Haiku drift smoke (post-harness; observational)

Re-run 3+3 cells; bit-compare per-field against Phase 1 baselines AND against Phase 2 results (within-D-window stability). PASS = Sonnet + Haiku stable across the entire Commit D harness execution window. FAIL = record per-field deltas as M11b empirical drift observation; characterize as cross-day or within-day drift mode.

### Commit D harness execution

```sh
# Phase 2 pre-harness smoke (run first):
for model in sonnet haiku; do
  for trace in dev_v2 test_v1 test_v2; do
    uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
      --trace $trace --arbiter-mode claude --arbiter-system-prompt v2 \
      --arbiter-model $model \
      --out runs/data/20d-smoke-preharness-content-${model}-v2-${trace}.json
  done
done

# Harness matrix (44 cells, per §D2 cell table):
for trace in test_v4 test_v5 test_v6 test_v7 test_v8 test_v11 test_v12 test_v13 test_v14 test_v15; do
  for model in sonnet haiku; do
    uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
      --trace $trace --arbiter-mode claude --arbiter-system-prompt v2 \
      --arbiter-model $model \
      --out runs/data/20d-content-${model}-v2-${trace}.json
    uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
      --trace $trace --arbiter-model $model \
      --out runs/data/20d-poll-${model}-${trace}.json
  done
done

# V3 attribution cells on failure subset:
for trace in test_v4 test_v5; do
  for model in sonnet haiku; do
    uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
      --trace $trace --arbiter-mode claude --arbiter-system-prompt v3 \
      --arbiter-model $model \
      --out runs/data/20d-content-${model}-v3-${trace}.json
  done
done

# Phase 3 post-harness smoke (run last):
for model in sonnet haiku; do
  for trace in dev_v2 test_v1 test_v2; do
    uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
      --trace $trace --arbiter-mode claude --arbiter-system-prompt v2 \
      --arbiter-model $model \
      --out runs/data/20d-smoke-postharness-content-${model}-v2-${trace}.json
  done
done
```

Aggregate: read 50 Commit D cell JSONs + 26 Commit B JSONs + M11a's `19d-*` JSONs (for V2-Opus + poll-Opus carry-forward); compute per-tier failure rates with Clopper-Pearson CIs + 2000-resample bootstrap CIs; identify outcome row at combined-N=10 scope; evaluate D7 branch via mechanical 6-cell cross-product YES-count; compute V3 capability-threshold band.

---

## Reviewer-vulnerable surfaces and pre-registered defenses

1. **"Cross-model determinism risk: Sonnet and Haiku not previously verified bit-identical across days."** Defense: pre-reg'd triangulated B → Phase 2 → Phase 3 smoke at 3 co-developed traces × 2 models × 3 phases = 18 cells empirically tests Sonnet + Haiku determinism at three sample points bracketing the harness window. PASS across all three phases = empirical determinism. FAIL at any phase = paper-line finding ("Sonnet drift observed at {delta} field at {phase}-vs-{phase} compare"); does not invalidate Commit D harness, but is reported as M11b-specific stability characterization that informs future work.

2. **"Prompt-cache differences across model families could introduce per-tier behavior differences."** Defense: arbiter calls are single-shot per-event (no multi-turn history); cache hits unlikely to matter at per-event input sizes ~250-500 tokens; document the surface for completeness but assert minimal expected effect. If Phase 2 / Phase 3 drift smoke FAILs in a cache-attributable way (e.g., output_tokens drift correlated with input-token repetition rate), characterize as a Pareto-relevant operational note rather than a determinism violation.

3. **"V2 prompt was tuned at 3B / Opus, not Haiku. Haiku might over-NO or over-YES on V2's enumeration."** Defense: M9 V3 precedent — V3 was model-capability-bound at 3B per M9 path-C close, viable at Opus per M10. Haiku-specific V2-form-bound failure is a pre-reg'd Row 4a/4b outcome with locked paper-line text, not an unexpected. The pre-reg accommodates Haiku underperforming as a publishable finding. V3 attribution on test_v4 + test_v5 additionally surfaces whether the V3 capability threshold falls between tiers in the Claude family.

4. **"Cost-curve interpretation: ‘X× cheaper per hit' is misleading if hit rates differ."** Defense: Pareto table reports both absolute cost per cell AND cost-per-hit-with-bounds; outcome rows distinguish "match with Pareto win" from "underperform but cheaper". P4 explicit on the cost-per-hit denominator handling for zero-hit cells (defined as undefined; cell reported but excluded from cost-per-hit aggregate). Matched-arbiter cost denominator (poll-Sonnet + poll-Haiku) eliminates "cheaper arbiter compared against expensive baseline" attack on the Pareto headline.

5. **"Cross-protocol caveat from M11a's defense #5 still applies."** Defense: per the carry-forward block in §"Locked design choices", the cross-protocol caveat reduces in M11b context to a trace-authorship caveat on the cross-tier comparison. Per-trace cross-tier comparison is internally consistent (the same trace under same conditions evaluated against multiple tiers); aggregate-across-protocols inherits M11a's documented caveat. Reported alongside results, not suppressed.

6. **"Cross-vendor sweep (GPT / Gemini / Llama) would strengthen the cost-curve claim."** Defense: explicitly out-of-scope at M11b (Non-goals). Cross-vendor sweep is a named-future ("M11d cross-vendor sweep") subject to separate pre-reg.

7. **"Underpowered at N=10 to distinguish ±10pp tier-deltas."** Defense: Row 5 is pre-reg'd as an outcome ("CIs all overlap → underpowered at N=10") with locked paper-line text; M11b-extension scope (N=20+) is named. Bootstrap CI sensitivity analysis additionally tests whether the binomial-CI assumption is the source of width vs the underlying sample size — defense #11.

8. **"The independent-finding D7 bytewise-identical-false-init prediction is post-hoc opportunistic."** Defense: D7 is **pre-registered at Commit A** with 3-branch confirm/partial/falsify outcome + locked paper-line text per branch + mechanical identification rule (6-cell cross-product YES-count). Pre-registration with mechanical identification eliminates analyst discretion at Commit D; the prediction was generated from M11a Commit D's mechanism-attribution finding (test_v12 V2-Opus = V2-3B bytewise) and tested at M11b's expanded model-tier axis.

9. **"M11b reuses M11a's traces — that's confounded if M11a's authorship was Opus-biased."** Defense: M11a's external-authoring sessions used Opus 4.7 for trace generation, with fresh-session non-project-cwd discipline. If M11a-authored content is systematically biased toward Opus-style failure modes, the M11b Pareto would over-attribute "M11b Opus parity" to a measurement artifact. Counter-argument: M11a's audit step 11 enforced "GTs are human-interpretable on content alone as warranting proaction" (audit-gate-rejects-implausible), so Opus-stylistic-bias would have shown up as audit rejections rather than as covert bias in accepted traces. Documented as a known limitation; full de-confounding requires a non-Opus-authored re-author study (M11b-extension or M11d scope).

10. **"V2-3B + cron30s carry-forward from M11a's `19d-*` JSONs is unfalsifiable in M11b — what if those JSONs drifted between M11a Commit D and M11b Commit D?"** Defense: pre-reg'd belt-and-suspenders 10-cell V2-3B + 10-cell cron30s re-run at Commit B with bit-identical PASS gate against M11a's `19d-*` JSONs. FAIL halts Commit B as an explicit M11a-data-drift finding. Reviewer attack converted into "the carry-forward JSONs are bit-identical-verified at the M11b Commit B timestamp."

11. **"Clopper-Pearson binomial CI assumes independent trials; trace-level outcomes may not be fully independent."** Defense: bootstrap CI sensitivity analysis at Commit D (2000-resample non-parametric bootstrap over per-trace outcomes; seed=42 locked at Commit A) reported alongside Clopper-Pearson. If bootstrap differs from Clopper-Pearson by > 5pp at either bound, report as sensitivity-analysis observation. Reviewer attack converted into "we report both CIs; the substantive finding is robust across both methods."

12. **"Multiple comparisons across 6 outcome rows + V3 attribution + D7 + drift smoke + Pareto = fishing."** Defense: pre-registered primary-vs-secondary outcome block in §D5; primary outcome is mechanically determined by P1/P2/P3 (1 of 6 rows; no analyst discretion); secondary outcome is mechanically determined by D7 cross-product YES-count (1 of 3 branches; no analyst discretion); everything else is observational characterization, not pre-reg'd outcome. Reviewer attack converted into "primary + secondary outcomes are pre-reg'd with mechanical identification rules; observational components are reported for transparency but not claimed as outcomes."

---

## Non-goals

- No new architectural lever (no V4 prompt — that's M11a-extension scope)
- No hierarchical routing (that's M11c scope)
- No new externally-authored traces (M11b reuses M11a's frozen artifacts)
- No cross-vendor sweep (GPT / Gemini / Llama) — explicit reviewer-defense future scope, not M11b
- No within-milestone editing of locked rates after Commit A (rates locked at Commit A per OPUS_* precedent at `agent/arbiter.py:15-16` + pricing attestation archive)
- No edits to V2 / V3 prompts in response to M11b results — both prompts are frozen artifacts
- No re-running test_v3 (M8 artifact)
- No re-running M11a / M10b / M10 V2-Opus or poll-Opus cells (Opus drift verified via 3-cell `17b-*` carryover smoke at Commit B)
- No editing the per-model rate table or `_rates_for` lookup logic mid-M11b — locked at Commit A; if rates change at Anthropic during the M11b run, document but do not re-price
- No changes to `agent/loop.py` (carries forward M10's "agent/loop.py stays untouched" discipline; all Claude wiring routes through `eval/run_trace.py`)
- No post-hoc reassignment between primary and secondary outcomes (locked per §D5 primary-vs-secondary block)
- No addition of new outcome rows or D7 branches at Commit D — locked-at-Commit-A row count + branch count are exhaustive (the 6 outcome rows cover the cross-product of P1 × P2 × P3 verdicts; the 3 D7 branches cover the 6-cell cross-product YES-count partition into {6, 1-5, 0})

---

## Walkthrough kickoff in fresh session (M11b session)

1. Confirm the pre-reg's design choices D1-D7 are locked per this plan and match user expectations.
2. **Apply any final hardening edits pre-Commit-A** as needed, mirroring M9/M10/M10b/M11a's pre-Commit-A hardening pattern.
3. **Execute pricing verification step (§D4 hard gate)**: fetch anthropic.com/pricing; extract Sonnet 4.6 + Haiku 4.5 rates; verify Opus 4.7 rate unchanged from M10 lock; archive at `runs/data/20a-pricing-attestation-{YYYY-MM-DD}.json`; update Sonnet/Haiku placeholder rates in this plan if needed; recompute budget estimate.
4. Once approved + pricing verified, copy this plan verbatim to `runs/20-cross-model-sweep.md` (with appropriate header / date / pre-reg SHA placeholders) and commit as Commit A. Pricing attestation JSON is part of Commit A.
5. Begin Commit B (code wiring + Opus carryover smoke + Sonnet + Haiku baselines + V2-3B + cron30s belt-and-suspenders re-run) only after Commit A lands.

This plan is the locked design for M11b at the maximum-defensibility posture. Any deviation requires a new plan iteration before Commit A lands.

---

# Commit D Results (M11b Commit D harness execution + analysis)

**Commit D date:** 2026-05-15. **Pre-reg SHA at Commit A:** `0b47ce3`. **Commit B SHA:** `c562173`. **Pre-Commit-D fix commits:** `b78554d` (react_poll_claude dedupe fix — duplicate-index responses surfaced at Sonnet test_v5 poll cell; bit-identical preservation verified on test_v4); `c0c6099` (M11a Commit D correction — V2-Opus combined-N=10 count 2/10 → 3/10 under strict joint-bar, surfaced during Commit D analysis prep; see runs/19 §"Row 4a paper-line — combined N=10 primary" + correction-note subsection for full audit).

**Cells executed at Commit D:** 50 D-phase JSONs total per pre-reg §D2 — 20 V2-Sonnet/Haiku harness + 20 poll-Sonnet/Haiku harness + 4 V3-Sonnet/Haiku attribution + 6 Phase 2 + 6 Phase 3 drift smoke. All cells passed without harness errors after the pre-Commit-D dedupe fix.

## Drift smoke: Sonnet + Haiku Phase 2 + Phase 3 vs Phase 1 baselines (per pre-reg §D3)

18 within-milestone drift smoke cells (3 Sonnet + 3 Haiku × 3 phases × 3 co-developed traces): **18/18 PASS bit-identical** vs Phase 1 baselines (`runs/data/20b-baseline-content-{sonnet,haiku}-v2-{dev_v2,test_v1,test_v2}.json`) on the 7 M11a-precedent load-bearing fields (`hit_rate`, `false_initiation_rate_per_hour`, `arbiter_calls`, `arbiter_yes_rate`, `arbiter_input_tokens`, `arbiter_output_tokens`, `arbiter_dispatched_model`). Sonnet 4.6 + Haiku 4.5 are bit-stable across the entire B → Commit-D-start → Commit-D-end execution window. Triangulated B → D-start → D-end smoke per §D3 — reviewer-defense: "Sonnet/Haiku drifted mid-harness and you didn't notice" is foreclosed by Phase 2 + Phase 3 bracketing the harness window with bit-identical compares against Phase 1.

## Per-trace observations (10 rows × per-tier cells)

| Trace | V2-3B (h/false_h) | V2-Opus (h/false_h) | V2-Sonnet (h/false_h) | V2-Haiku (h/false_h) | poll-Sonnet (h) | poll-Haiku (h) | poll-Opus (h) | cron30s (h) | P1 V2-S matches V2-O? | P2 V2-H matches V2-O? |
|---|---|---|---|---|---|---|---|---|---|---|
| test_v4  | 0.40/7.13 | 0.80/7.13 | 0.80/7.13 | 0.80/7.13 | 1.00 | 1.00 | (carry; 1.00 via M8b 15c) | 1.00 | Y | Y |
| test_v5  | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00 | 1.00 | 1.00 | 1.00 | Y | Y |
| test_v6  | 0.40/0.00 | 1.00/0.00 | 1.00/0.00 | 0.60/0.00 | 1.00 | 1.00 | 1.00 | 1.00 | Y | **N** (Δhit=0.40) |
| test_v7  | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00 | 1.00 | 1.00 | 1.00 | Y | Y |
| test_v8  | 0.40/0.00 | 0.60/0.00 | 0.60/0.00 | 0.60/0.00 | 1.00 | 1.00 | 1.00 | 1.00 | Y | Y |
| test_v11 | 0.40/3.71 | 1.00/3.71 | 1.00/3.71 | 0.80/3.71 | 1.00 | 1.00 | 1.00 | 1.00 | Y | **N** (Δhit=0.20) |
| test_v12 | 0.60/7.74 | 1.00/7.74 | 1.00/7.74 | 1.00/7.74 | 1.00 | 1.00 | 1.00 | 1.00 | Y | Y |
| test_v13 | 0.80/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/3.50 | 1.00 | 1.00 | 1.00 | 1.00 | Y | **N** (Δfalse/h=3.50) |
| test_v14 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00 | 1.00 | 1.00 | 1.00 | Y | Y |
| test_v15 | 0.80/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00 | 1.00 | 1.00 | 1.00 | Y | Y |

Per-trace majority for P1 (V2-Sonnet matches V2-Opus): **10/10 ≥ 6/10 PASS**.
Per-trace majority for P2 (V2-Haiku matches V2-Opus): **7/10 ≥ 6/10 PASS**.

V2-Sonnet is per-trace bytewise-identical to V2-Opus on hit_rate AND false/h for all 10 traces. V2-Haiku mismatches on 3 traces (test_v6 hit-side; test_v11 hit-side; test_v13 false/h-side); on the other 7, Haiku tracks Opus exactly.

poll-Opus on test_v4: M11b uses M8b's 15c-poll-test_v4.json (poll-local at M8b, not poll-Opus); the Pareto-cost denominator for test_v4 uses poll-Opus average across the other 9 carry-forward cells.

## Per-tier joint-bar failure-rate metrics at combined-N=10

| Tier | Failures (joint bar: hit<0.80 OR false/h>5.0/h) | Failure rate | 95% CP CI | Bootstrap CI (n=2000, seed=42) | Δ vs V2-3B (pp) | Δ vs V2-Opus (pp) | CP-CI overlaps V2-3B point? | CP-CI overlaps V2-Opus point? |
|---|---|---|---|---|---|---|---|---|
| V2-3B (carry; belt-PASS-verified) | 5/10 (test_v4, test_v6, test_v8, test_v11, test_v12) | 50.0% | [18.7%, 81.3%] | [20.0%, 80.0%] | — | +20 | — | YES (V2-Opus 30% within V2-3B CI) |
| V2-Opus (carry; corrected per `c0c6099`) | 3/10 (test_v4, test_v8, test_v12) | 30.0% | [6.7%, 65.2%] | [0.0%, 60.0%] | −20 | — | YES (V2-3B 50% within V2-Opus CI) | — |
| **V2-Sonnet (M11b)** | 3/10 (test_v4, test_v8, test_v12) | **30.0%** | [6.7%, 65.2%] | [0.0%, 60.0%] | −20 | **0** | YES | YES |
| **V2-Haiku (M11b)** | 4/10 (test_v4, test_v6, test_v8, test_v12) | **40.0%** | [12.2%, 73.8%] | [10.0%, 70.0%] | −10 | +10 | YES | YES |

**Per-failure mechanism per cell:**

- **test_v4** (all three Claude tiers: V2-Opus + V2-Sonnet + V2-Haiku) — false/h=7.128, hit=0.80; mechanism = surprise-gate auto-surf bypass on `designgrid_renewal` + `calendar_feature_tip` (both events have z<−0.5, bypass arbiter). Bytewise identical across V2-3B/Opus/Sonnet/Haiku because the surprise gate is local-deterministic (qwen2.5:3b predictor + nomic-embed scorer shared across all tiers).
- **test_v8** (all three Claude tiers: V2-Opus + V2-Sonnet + V2-Haiku) — hit=0.60, false/h=0.00; mechanism = V2-enumeration limit (mom_birthday_heads_up family-event reminder + bridgers_presale_window concert-presale — discretionary content outside V2's literal "deadline obligation" enumeration). All Claude tiers exhibit the same NO on these events under V2's closed YES list.
- **test_v12** (all three Claude tiers: V2-Opus + V2-Sonnet + V2-Haiku) — hit=1.00, false/h=7.742; mechanism = V2-prompt-inherited YES-bias on `grocer_back_in_stock` + `calendar_yoga_suggest`. Bytewise identical across V2-3B/Opus/Sonnet/Haiku. The mechanism is V2-prompt-inherent across the entire Claude family.
- **test_v6** (V2-Haiku only) — hit=0.60, false/h=0.00; mechanism = Haiku-specific V2-enumeration limit on the M10b test_v6 GTs (concert_swap, auction_ending — Haiku says NO where Sonnet+Opus say YES). Distinct from test_v8's enumeration limit which affects all Claude tiers; this is Haiku-scale-specific.

Three V2-Opus joint-bar failures (test_v4, test_v8, test_v12) are inherited bytewise by both V2-Sonnet AND V2-Haiku. V2-Haiku adds one additional joint-bar failure (test_v6) that V2-Sonnet does NOT exhibit — Haiku-scale-specific V2-enumeration limit.

## Pareto-cost table per tier at combined-N=10

| Tier | Mean $/cell | Mean $/hit | Min $/hit | Max $/hit | n cells with hits |
|---|---|---|---|---|---|
| V2-3B (local) | $0.0000 | $0.0000 | — | — | 10/10 |
| V2-Opus | $0.0449 | $0.0098 | $0.0073 | $0.0150 | 10/10 |
| **V2-Sonnet** | **$0.0066** | **$0.0014** | $0.0011 | $0.0022 | 10/10 |
| **V2-Haiku** | **$0.0022** | **$0.0005** | $0.0004 | $0.0010 | 10/10 |
| poll-Opus (carry) | $0.9631 | $0.1926 | $0.1578 | $0.2163 | 9/10 |
| **poll-Sonnet** | $0.1309 | $0.0262 | $0.0212 | $0.0313 | 10/10 |
| **poll-Haiku** | $0.0437 | $0.0087 | $0.0061 | $0.0097 | 10/10 |
| cron30s (carry; belt-PASS) | $0.0000 | $0.0000 | — | — | 10/10 |

**Matched-arbiter Pareto ratios (poll-tier $/hit ÷ HeargentZA-tier $/hit at same model):**

- V2-Opus vs poll-Opus: **19.7×** cheaper per hit
- **V2-Sonnet vs poll-Sonnet: 18.3×** cheaper per hit
- **V2-Haiku vs poll-Haiku: 16.6×** cheaper per hit

**Cross-tier Pareto ratios (V2-Opus $/hit ÷ V2-{tier} $/hit at same prompt V2):**

- V2-Sonnet vs V2-Opus: **6.8×** cheaper per hit
- **V2-Haiku vs V2-Opus: 18.5×** cheaper per hit

The matched-arbiter Pareto ratio is robust to the Opus-rate lock (§D4 + pricing attestation): V2-X vs poll-X ratios use the same per-token rate for both arbiter and baseline at each tier, so the locked-rate vs published-rate gap is internally consistent within each ratio. Cross-tier ratios depend on the Opus-rate lock; absolute $/hit at the Opus tier should be divided by ~3 for current-Anthropic-rate (Opus $5/$25) deployment projections, but the V2-Haiku vs V2-Opus 18.5× ratio survives any uniform Opus-rate scaling factor.

## P1 / P2 / P3 / P4 verdicts

**P1 — V2-Sonnet matches V2-Opus joint bar:**
- (a) Per-trace majority (≥ 6 of 10): **10/10 = PASS**
- (b) Combined point estimates within ±10pp: |30%-30%|=**0pp PASS**; CIs overlap: identical [6.7%, 65.2%] = **PASS**
- **P1 PASS**

**P2 — V2-Haiku matches V2-Opus joint bar:**
- (a) Per-trace majority (≥ 6 of 10): **7/10 = PASS** (mismatch on test_v6, test_v11, test_v13)
- (b) Combined point estimates within ±10pp: |40%-30%|=**10pp at boundary, PASS** (inclusive interpretation of "within"); CIs overlap: V2-Haiku [12.2%, 73.8%] ∩ V2-Opus [6.7%, 65.2%] = [12.2%, 65.2%] non-empty = **PASS**
- **P2 PASS at the ±10pp boundary**

**P3 — Tier beats V2-3B floor (strictly less + non-overlapping CI):**
- V2-Sonnet 30% < V2-3B 50% point estimate, but V2-Sonnet CI [6.7%, 65.2%] contains V2-3B point 50% — CIs overlap V2-3B point estimate. **P3 FAIL on V2-Sonnet at N=10**.
- V2-Haiku 40% < V2-3B 50% point estimate, but V2-Haiku CI [12.2%, 73.8%] contains V2-3B point 50% — CIs overlap V2-3B point estimate. **P3 FAIL on V2-Haiku at N=10**.
- (Note: V2-Opus itself also fails P3 at N=10: V2-Opus 30% < V2-3B 50%, but V2-Opus CI [6.7%, 65.2%] contains V2-3B 50% — the entire H2 finding is at point-estimate level, not at non-overlapping-CI level, at this sample size.)

**P4 — Pareto headline:**
- Per-cell mean cost + per-cell cost-per-hit reported in the Pareto-cost table above. All three matched-arbiter ratios (V2-Sonnet / V2-Haiku / V2-Opus vs their poll counterparts) exceed the pre-reg's "≥3× cheaper" floor by a substantial margin (16.6×–19.7×). **P4 PASS**.

## Primary outcome row identification (mechanical from §D5 6-row table)

Mechanical reading of the §D5 6-row table against the P1/P2/P3 verdicts:

- Row 1 (P1 PASS AND P2 PASS): **satisfied** (Sonnet matches Opus exactly; Haiku matches at boundary)
- Row 4a (any | P3 FAIL on Haiku): **also satisfied** (V2-Haiku CI overlaps V2-3B point estimate)
- Row 5 (all CIs overlap V2-3B + V2-Opus): **also satisfied** (V2-Sonnet AND V2-Haiku CIs overlap both V2-3B's [18.7%, 81.3%] and V2-Opus's [6.7%, 65.2%])

The three rows are non-mutually-exclusive at this data point. Per the §D5 row-ordering (Row 1 listed first, declared "best" outcome), the **mechanical primary outcome is Row 1**. The Row 4a + Row 5 conditions both apply as **critical concurrent caveats** that the locked Row 1 paper-line text does not anticipate.

**Locked Row 1 paper-line text — integer placeholders filled at Commit D; wording is not edited:**

> *"Across N=10 fresh externally-authored traces under the M11a iteratively-extended-banned-list protocol (three protocol generations combined: M10 frozen list test_v4/v5; M10b frozen list test_v6/v7/v8; M11a iteratively-extended list test_v11..v15), V2-Sonnet failure rate **3**/10 = **30.0%** (95% CP CI **[6.7%, 65.2%]**; bootstrap CI **[0.0%, 60.0%]**) and V2-Haiku failure rate **4**/10 = **40.0%** (95% CP CI **[12.2%, 73.8%]**; bootstrap CI **[10.0%, 70.0%]**) both match V2-Opus failure rate 3/10 = 30.0% (corrected per M11b-Commit-D-surfaced M11a aggregation error; see runs/19 §"Row 4a paper-line — combined N=10 primary" correction-note) within ±10pp at point estimate with overlapping CIs. Pareto headline: V2-Haiku is **18.5×** cheaper per hit than V2-Opus and **16.6×** cheaper per hit than poll-Haiku at matched-arbiter cost denominator; V2-Sonnet is **6.8×**/**18.3×** respectively. Strict Pareto improvement: the Claude tier curve flattens at Haiku for this workload; Opus is overkill at the M11a sample's distractor distribution. Deployment shape collapses to Haiku as default with no observed quality penalty at N=10. Cross-protocol caveat from M11a defense #5 inherited unchanged; cross-tier comparison is internally consistent per trace."*

**Commit-D critical caveats to the Row 1 paper-line text (these caveats are required for paper-defensibility but were not anticipated by the pre-reg's locked Row 1 wording):**

1. **P2 PASS is at the ±10pp boundary, not strict.** |V2-Haiku 40% − V2-Opus 30%| = **10pp exact**, the maximum tolerable point-estimate gap for P2 PASS. Per-trace majority is 7/10, just above the ≥6/10 threshold. Calling Haiku "sufficient" with a 10pp point-estimate failure-rate gap is true at the pre-registered criterion but should be read with the understanding that it sits at the criterion boundary, not in its interior. V2-Sonnet's match to V2-Opus is materially cleaner (point estimate 30%=30%, 10/10 per-trace match).

2. **P3 FAILS on all three Claude tiers at N=10 — the H2 finding is underpowered.** V2-Sonnet, V2-Haiku, AND V2-Opus all have CIs ([6.7%, 65.2%] / [12.2%, 73.8%] / [6.7%, 65.2%]) that contain V2-3B's 50% point estimate. The cross-family upgrade (3B → Claude tier ladder) does NOT strictly beat V2-3B with non-overlapping CIs at this sample size for ANY of the three Claude tiers. The corrected M11a finding ("V2-Opus reduces failure rate from 50% → 30% (20 pp reduction with non-overlapping point estimates but partially overlapping CIs)") sits at the point-estimate level, not at the non-overlapping-CI level, at N=10. M11b's data does not change this — it confirms it for Sonnet + Haiku.

3. **Row 4a's P3-FAIL-on-Haiku condition is concurrently satisfied.** Mechanically the pre-reg's §D5 row table is non-mutually-exclusive on this data point; Row 1 (P1+P2 PASS) and Row 4a (P3 FAIL on Haiku) BOTH fire. Row 4a's framing ("Haiku is insufficient capability") substantively conflicts with Row 1's framing ("Haiku sufficient; Opus overkill"). The honest synthesis: V2-Haiku is statistically indistinguishable from V2-Opus on this sample at the ±10pp tolerance (Row 1 PASS); V2-Haiku is ALSO statistically indistinguishable from V2-3B (Row 4a observation). At N=10 the cross-family-tier curve is too underpowered to substantively distinguish "Haiku matches Opus" from "Haiku falls to V2-3B level".

4. **Row 5's underpowered-at-N=10 condition is concurrently satisfied.** All four tiers' (V2-3B / V2-Opus / V2-Sonnet / V2-Haiku) CIs mutually overlap. The cross-tier ranking at point estimate (V2-Opus = V2-Sonnet = 30% < V2-Haiku = 40% < V2-3B = 50%) is consistent with Row 1's "tier curve flattens at Haiku" reading but cannot be statistically distinguished from Row 4a/Row 5 alternatives at N=10. Substantive cross-tier ranking deferred to **M11b-extension** scope (N=20+) for tightened CIs, named here as a separately-pre-registered milestone.

**Honest Commit-D synthesis paper-line (additional to the locked Row 1 text):**

> *"M11b's combined-N=10 cross-tier sweep places V2-Sonnet (3/10 = 30%; CP CI [6.7%, 65.2%]) and V2-Haiku (4/10 = 40%; CP CI [12.2%, 73.8%]) at point estimates that match V2-Opus (3/10 = 30%; CP CI [6.7%, 65.2%]) within the pre-registered ±10pp tolerance (V2-Sonnet 0pp gap; V2-Haiku 10pp gap at the criterion boundary), and substantially Pareto-improve cost-per-hit by 6.8×/18.5× cross-tier and 18.3×/16.6× matched-arbiter respectively. The point-estimate finding is Row 1 (Strict Pareto improvement; tier curve flattens at Haiku), with V2-Sonnet matching V2-Opus exactly and V2-Haiku matching at the criterion boundary. The CI finding is Row 5 (underpowered at N=10): all three Claude tiers' 95% Clopper-Pearson CIs contain V2-3B's 50% point estimate, so P3 (strictly beats V2-3B with non-overlapping CI) FAILS at N=10 for every tier including V2-Opus — the corrected M11a H2 finding sits at the point-estimate level, and M11b confirms this is also true for Sonnet + Haiku. Substantive deployment recommendation: V2-Haiku is the Pareto-default for this workload at point estimate, with V2-Opus residuals (test_v4 surprise-gate auto-surf bypass; test_v8 V2-enumeration limit; test_v12 V2-prompt YES-bias) all inherited bytewise by V2-Sonnet and V2-Haiku, plus one Haiku-specific Haiku-scale-V2-enumeration-limit residual on test_v6. M11b-extension (N=20+) tightens CIs to definitively distinguish Row 1 from Row 4a/Row 5; the V4 prompt revision (M11a-extension scope) addresses the V2-prompt YES-bias residual that is the single largest cross-tier-shared mechanism."*

## D7 secondary outcome — bytewise-identical-false-init cross-product

Mechanical 6-cell cross-product per §D7: {V2-Sonnet, V2-Haiku} × {`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`}.

| Trace | event_id | V2-3B | V2-Opus | V2-Sonnet | V2-Haiku |
|---|---|---|---|---|---|
| test_v11 | trivia_league_round | YES | YES | **YES** | **YES** |
| test_v12 | grocer_back_in_stock | YES | YES | **YES** | **YES** |
| test_v12 | calendar_yoga_suggest | YES | YES | **YES** | **YES** |

**6 of 6 cells YES → D7-confirm branch identified mechanically.**

**Locked D7-confirm paper-line — event-ID assignments filled at Commit D; wording not edited:**

> *"The V2-prompt-inherited YES-bias on retail-back-in-stock / calendar-suggestion / casual-social-meetup distractors observed at V2-3B and V2-Opus (M11a independent finding) is reproduced bytewise at V2-Sonnet and V2-Haiku. V2-Sonnet surfaces **{`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`}** on the {test_v11, test_v12} pair; V2-Haiku surfaces **{`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`}** on the same pair. The mechanism is V2-prompt-inherent across the entire Claude family + qwen2.5:3b — not a model-scale or model-family property. The targeted next lever is V4 prompt revisions adding explicit NO examples for these distractor classes (M11a-extension scope), not further cross-family swap. The Row 1 primary outcome finding is refined: model-family-tier swap below Opus does not address the V2-prompt-inherent distractor mechanism on this sample."*

This is a strong cross-confirmation finding: the V2-prompt-inherited YES-bias mechanism is preserved BYTEWISE across the Claude family (Opus + Sonnet + Haiku) PLUS qwen2.5:3b. Four independent model implementations agree on the same YES decisions for the same three borderline distractor events. The mechanism cannot be addressed by model-tier swap; V4 prompt revisions (M11a-extension) are the only targeted lever.

## V3 attribution on failure subset {test_v4, test_v5}

| Trace | V2-3B | V2-Opus (carry) | V3-Opus (carry; M10) | V3-Sonnet (M11b) | V3-Haiku (M11b) | V3 capability threshold |
|---|---|---|---|---|---|---|
| test_v4 | 0.40/7.13 | 0.80/7.13 | 0.80/7.13 | 0.80/7.13 | **1.00/7.13** | V3 viable at Haiku scale on test_v4 (V3-Haiku hit-rate exceeds V2-Opus on this trace — discovers `cover_standup_request` colleague-social-ask GT that V2's closed enumeration narrowly misses across all tiers) |
| test_v5 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | 1.00/0.00 | V3 viable at every Claude tier on test_v5 (all hit=1.00, joint-bar PASS) |

**V3 capability threshold for the test_v4/test_v5 subset:** falls **at or below Haiku** (V3-Haiku hit ≥ 0.80 on both traces). This refines M9's path-C close on V3-3B falsification: V3 is model-capability-bound at qwen2.5:3b but viable at Haiku-and-above. Specifically, V3-Haiku on test_v4 achieves hit=1.00 — strictly better than V2-Opus (0.80), V3-Opus (0.80), and V2-Sonnet (0.80) on the same trace via V3's principled-criterion-AND-gate reading correctly catching the colleague-social-ask GT `cover_standup_request` that all V2 variants miss as out-of-enumeration. (The false/h=7.13 surprise-gate auto-surf bypass mechanism on test_v4 is upstream of the arbiter and identical across all variants of HeargentZAWide, so V3-Haiku's joint-bar still FAILS on test_v4 — but the hit-side improvement is meaningful.)

Reported observationally per §D5 ("V3-Sonnet + V3-Haiku × failure subset is observational second-axis on V3's model-capability threshold; not part of the primary Pareto outcome").

## Cost summary

| Component | Cells | Est. cost (pre-reg §"Cost framework") | Actual cost |
|---|---|---|---|
| Harness V2-Sonnet × 10 | 10 | $0.11 | $0.0657 (computed at locked $3/$15 Sonnet rates) |
| Harness V2-Haiku × 10 | 10 | $0.035 | $0.0217 (at locked $1/$5 Haiku rates) |
| Harness V3-Sonnet × 2 (test_v4, test_v5) | 2 | $0.014 | ~$0.006 |
| Harness V3-Haiku × 2 (test_v4, test_v5) | 2 | $0.004 | ~$0.002 |
| Harness poll-Sonnet × 10 | 10 | $2.00 | $1.309 |
| Harness poll-Haiku × 10 | 10 | $0.67 | $0.437 |
| Belt-and-suspenders V2-3B × 10 (Commit B) | 10 | $0 | $0 (local) |
| Belt-and-suspenders cron30s × 10 (Commit B) | 10 | $0 | $0 (local) |
| Opus carryover smoke × 3 (Commit B) | 3 | $0.15 | $0.0268 |
| Sonnet smoke baseline + Phase 2 + Phase 3 (3+3+3) | 9 | $0.045 | $0.0257 |
| Haiku smoke baseline + Phase 2 + Phase 3 (3+3+3) | 9 | $0.0135 | $0.0086 |
| **TOTAL M11b spend across Commits B + D** | **85** | **~$3.05** | **~$1.91 of $4–5 pre-reg budget** |

Actual spend **~63% under** pre-reg estimate (~$1.91 vs ~$3.05). The largest savings came from poll-Sonnet (1.309 vs 2.00 estimate) and poll-Haiku (0.437 vs 0.67 estimate); Haiku's faster token generation means fewer total tokens per poll call than the Sonnet/Opus extrapolation suggested.

## M11b closure summary

- **Drift smoke verdict:** 18/18 Sonnet + Haiku Phase 2 + Phase 3 cells PASS bit-identical vs Phase 1 baselines (`20b-baseline-*`). Sonnet 4.6 + Haiku 4.5 alias stable through the M11b Commit B → Commit D execution window. Opus 4.7 stable across M10 → M11a → M11b (18+ days) per the Commit B Opus carryover smoke vs `17b-*`.
- **Primary outcome row:** **Row 1 (Strict Pareto improvement) at point estimate**, mechanically per P1 + P2 PASS; with critical concurrent Row 4a (P3 FAIL on Haiku) and Row 5 (underpowered at N=10) caveats documented in the four Commit-D caveats above. Honest synthesis paper-line published alongside the locked Row 1 paper-line text.
- **D7 secondary outcome:** **D7-confirm at 6/6 cells** — V2-prompt-inherited YES-bias mechanism preserved bytewise across Opus + Sonnet + Haiku + qwen2.5:3b on `trivia_league_round` + `grocer_back_in_stock` + `calendar_yoga_suggest`. Mechanism is V2-prompt-inherent, not model-scale-specific. V4 prompt revisions (M11a-extension) are the only targeted lever; cross-family swap below Opus does not address.
- **Pareto headline:** V2-Haiku is **18.5× cheaper per hit than V2-Opus** (cross-tier) and **16.6× cheaper per hit than poll-Haiku** (matched-arbiter). V2-Sonnet is **6.8× / 18.3×** respectively. The 16-20× matched-arbiter Pareto ratio is preserved across the entire Claude tier ladder.
- **V3 attribution:** V3 capability threshold for {test_v4, test_v5} falls at or below Haiku; V3-Haiku achieves hit=1.00 on test_v4 (the strongest hit-side performance across all V2/V3 variants on that trace).
- **M11a correction commit (`c0c6099`):** V2-Opus combined-N=10 reference corrected from 2/10 = 20% to 3/10 = 30% under strict joint-bar; H2 finding direction unchanged (Row 4a partial-closure-with-residuals), magnitude reduced (20pp reduction vs original 30pp); independent V2-prompt-YES-bias finding scope clarified (2 traces test_v11+test_v12, not 3 — test_v4 is a distinct surprise-gate auto-surf bypass mechanism); three V2-Opus residual mechanisms now mapped to three distinct next-step levers.
- **react_poll_claude dedupe fix (`b78554d`):** Pre-existing bug latent since M10; surfaced at Sonnet poll on test_v5. Generic robustness fix; bit-identical preservation verified on test_v4 before/after.
- **Cumulative M11b spend ~$1.91 of $4–5 pre-reg budget** (~63% under estimate).

**Future work named per pre-reg §"Non-goals" + §"Reviewer-vulnerable surfaces":**

- **M11a-extension** — V4 prompt revisions (explicit NO examples for `grocer_back_in_stock`-class retail / `calendar_yoga_suggest`-class recurring-suggestion / `trivia_league_round`-class social-meetup distractors) + self-restate pre-flight gate + scope at N=20+ for tighter binomial CIs. Now the most targeted lever per D7-confirm: the V2-prompt YES-bias mechanism is preserved across the entire Claude family + qwen2.5:3b, so V4 prompt is the only mechanism-level lever for this residual.
- **M11b-extension** — Cross-tier sweep at N=20+ for tightened CIs to definitively distinguish Row 1 (Sonnet/Haiku match Opus) from Row 4a (Haiku falls to V2-3B level) — at N=10 these are statistically indistinguishable for the Haiku tier.
- **M11c** — Hierarchical routing (3B-local → Sonnet/Opus escalation) as deployment shape. With V2-Sonnet at 30%=V2-Opus failure rate and **6.8× cheaper per hit** at point estimate, Sonnet is the strong routing-default candidate; Opus is reserved for the cells where V3 (or future V4) capability is needed.
- **M11d** (named here for completeness) — Cross-vendor sweep (GPT / Gemini / Llama at Opus-equivalent capability) under a separate pre-reg. Out of scope at M11b per §"Non-goals".

Commit D is one bundled commit per pre-reg §"Three-commit protocol" containing: 50 D-phase `runs/data/20d-*.json` cells; this §"Commit D Results" appendix in runs/20; row 20 + status block + paper framing line updates in runs/README.md; the `.commit_d_analysis.py` aggregate script as a reproducibility artifact.
