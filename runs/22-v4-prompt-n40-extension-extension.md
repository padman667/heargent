# Run 22 — M11a-extension-extension: V4 prompt revision + N=40 CI tightening

**Pre-reg date:** 2026-05-22 (M11a-extension-extension Commit A landing).
**Pre-reg SHA:** `{COMMIT_A_SHA}` (backfilled in a follow-up commit per M11a-extension Commit-A landing precedent `b1d2521` → SHA-backfill `15484b6`).
**Source plan:** `~/.claude/plans/m11a-extension-extension-n40.md` (locked source; this file is the verbatim pre-reg copy per §D13 Commit A step 2; any further plan revision happens at the locked-plan path and back-propagates to this file via §D13's pre-Commit-D fix discipline).
**Predecessor state:** M11a-extension Commit D at HEAD `c056851` (Row 5 UNDERPOWERED at N=20: V4-Opus 6/20 = 30.0% CP CI [11.9%, 54.3%] width 42.4pp > 30pp; V2-Opus 7/20 = 35.0% CP CI [15.4%, 59.2%]; DELTA_PE −5.0pp NEUTRAL ∧ WIDE_CI → Row 5 first per first-match-wins; V4-mechanism diagnostic: V4-partial 1/5; cross-tier-V4 diagnostic: CT-V4-confirm).
**Pricing attestation:** `runs/data/22a-pricing-attestation-2026-05-22.json` (zero observed-published-rate drift vs M11a-extension `21a-pricing-attestation-2026-05-15.json`; M10 lock $15/$75 Opus preserved for cross-milestone consistency; Sonnet $3/$15 + Haiku $1/$5 matched to M11a-extension lock; published Opus 4.7 rate $5/$25 unchanged across the M11b 2026-05-13 → M11a-extension 2026-05-15 → M11a-extension-extension 2026-05-22 9-day three-Commit-A chain).
**D14 hardening pass status:** LOCKED at this Commit A. 6 substantive edits landed in the source plan (H1 Row 1 STRICT SUCCESS unreachable-at-this-milestone disclosure under MECHANISM_CONFIRM-tied-to-M11a-extension-5-events carry-forward; H2 Commit-E trigger 2D failure-mode table over (CI width, |DELTA_PE|) plane; H3 CT-V4-{confirm,partial,falsify} at N=40 defined over union of M11a-extension 5 events ∪ new test_v31..v50 joint-bar cells; H4 Commit-B git-diff-zero gate added alongside V4 SHA gate; H5 Sonnet/Haiku belt-and-suspenders observational-not-halt verdict policy carry-forward from §D12; H6 conditional Commit E does NOT require new plan-kickoff session + supersedes Commit-D paper-line on trigger fire).
**Frozen artifacts at Commit A:** `agent/`, `baselines/`, `eval/`, `sandbox/`, `pyproject.toml`, `uv.lock` — NOT touched. Commit A modifies only `runs/22-v4-prompt-n40-extension-extension.md` (NEW) + `runs/data/22a-pricing-attestation-2026-05-22.json` (NEW) + `runs/README.md` (UPDATE — row 22 entry + headline status block).

---

# M11a-extension-extension: N=40+ CI tightening for the V4-vs-V2 cross-prompt headline

**Status:** LOCKED post-D14 hardening pass (2026-05-22). 6 substantive D14 edits landed (H1 Row 1 STRICT SUCCESS unreachable-at-this-milestone disclosure under MECHANISM_CONFIRM-tied-to-M11a-extension-5-events carry-forward; H2 Commit-E trigger 2D failure-mode table; H3 CT-V4-{confirm,partial,falsify} at N=40 defined over union of M11a-extension 5 events ∪ new test_v31..v50 joint-bar cells; H4 Commit-B git-diff-zero gate added alongside V4 SHA gate; H5 Sonnet/Haiku belt-and-suspenders observational-not-halt verdict policy carry-forward from §D12; H6 conditional Commit E does NOT require new plan-kickoff session + supersedes Commit-D paper-line on trigger fire). Mirrors M11a-extension's D1-D14 structure verbatim where load-bearing; deviations from the M11a-extension template are flagged inline with rationale. Ready for Commit A landing.

**Final landing path:** `~/.claude/plans/m11a-extension-extension-n40.md` is the locked source. Commit A copies the plan to `runs/22-v4-prompt-n40-extension-extension.md` mirroring M11a-extension's structure.

**Pre-reference state (locked at draft time, 2026-05-22):**
- main HEAD `c056851` (M11a-extension Commit D); working tree clean except untracked `paper/`
- M11a-extension CLOSED at Row 5 UNDERPOWERED + V4-partial 1/5 + CT-V4-confirm
- Latest pricing attestation: `runs/data/21a-pricing-attestation-2026-05-15.json`
- All M11a-extension code paths intact: `--arbiter-system-prompt {v2,v3,v4}` + `--arbiter-model {opus,sonnet,haiku}` + `eval/author_trace.py` self-restate gate + V4 prompt sha256 09be309d... frozen
- Frozen artifacts NOT to touch except as enumerated: `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py`, `eval/run_trace.py`, `eval/author_trace.py`, `sandbox/event_trace.py` existing test_v4..v15 + test_v21..v30 definitions. New traces `test_v31..test_v50` added at Commit C (locked at D8 below).

---

## Context

M11a-extension closed at **Row 5 UNDERPOWERED** + **V4-partial 1/5** + **CT-V4-confirm**. The Row 5 paper-line is unambiguous about the next milestone: *"substantive cross-prompt ranking is deferred to M11a-extension-extension (N=40+) for tightened CIs."* The paper's `\section{Limitations}` and `\section{Future work}` both name this milestone first and explicitly tie it to the 42.4pp CP CI width at N=20 that fails to discriminate the ±10pp pre-registered threshold.

**The headline question this milestone exists to resolve:** is V4-Opus's 30.0% failure rate at N=20 a real ~5pp reduction vs V2-Opus's 35.0%, or noise consistent with anything from substantial V4 improvement to substantial V4 backfire? Tightening N=20 → N=40 narrows the binomial CP CI from ~42pp to ~28pp (back-of-envelope at 30% point estimate); doubling further to N=60 narrows to ~24pp. The Plan picks N=40 as the primary scope (a single Plan-cycle doubling of the existing combined sample) with N=60 as a pre-registered conditional extension if N=40 lands in a discriminative-but-borderline region.

**What this milestone does NOT do:** it does not introduce V5, surprise-gate-bypass interventions, hierarchical routing, or cross-vendor sweep. V4 prompt remains frozen at sha256 09be309d...; the surprise-gate-bypass family at §D6 of M11a-extension remains a pre-registered Non-goal addressed by the separately-named M11d-surprise-gate-retuning milestone. This plan is the targeted CI-tightening continuation, nothing more.

**Paper-shape goal:** outcomes feed directly into Paper v2 §sec:m11a-extension or a new §sec:m11a-extension-extension subsection. The Row 5 paper-line currently filling the paper would be **superseded** at one of: Row 1 (STRICT SUCCESS) at tightened CI, Row 2 (MECHANISM-ONLY NET NEUTRAL) at tightened CI, Row 3 (PARTIAL REDUCTION) at tightened CI, Row 4 (NO IMPROVEMENT) at tightened CI, or Row 6 (BACKFIRE). Row 5 firing again at N=40 would itself motivate either N=60 conditional extension or a substantive methodology paper-line about binomial CI behavior at small-N AB tests in this setting.

---

## Thesis

Doubling combined N from 20 to 40 with 20 additional fresh-session-authored traces (test_v31..test_v50) under the M11a-extension iterative-extension protocol + self-restate pre-flight gate tightens the V4-Opus vs V2-Opus Clopper-Pearson CI from ~42pp to ~28pp width at the 30% point estimate, enabling mechanical discrimination of the ±10pp pre-registered threshold and superseding M11a-extension's Row 5 UNDERPOWERED verdict.

**Question:** With N=40 binomial CI ≤ 30pp width (the M11a-extension §D7 `WIDE_CI` predicate switches off), which of Rows 1, 2, 3, 4, 6 fires under the same first-match-wins predicate composition?

---

## Locked design choices (D1-D14)

### D1. V4 prompt text scope

**Recommended:** V4 prompt frozen verbatim from M11a-extension at sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes). NO changes.

**Defense:** This milestone is a sample-size extension of the M11a-extension headline comparison, NOT a prompt revision. Editing V4 between M11a-extension and M11a-extension-extension would (i) reset the N=20 sample to N=20+20 of two different V4 variants, blocking the combined-N=40 aggregation; (ii) reintroduce the post-hoc-opportunism reviewer attack M11a-extension's single-shot discipline closed; (iii) confound CI-tightening with prompt-change effect. Single-shot V4 carries forward bytewise.

**Bytewise verification at Commit B (D14-H4 strengthened):** Commit B "no code wiring" assertion is verified by TWO mechanical gates: (a) re-load `ARBITER_SYSTEM_PROMPT_V4` from `agent/arbiter.py` and verify sha256 matches the locked hash `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes); (b) `git diff c056851 -- agent/ eval/ baselines/ sandbox/event_trace.py pyproject.toml uv.lock` produces ZERO output (no accidental rate-table edits, no z-band threshold drift, no eval reporting changes, no banned-list edits in sandbox/event_trace.py existing-trace definitions). BOTH gates HALT Commit B on FAIL. Defense rationale: SHA on the prompt alone does not cover sibling-file drift; the git-diff-zero gate is the broader assertion that this milestone touches NO code at Commit B.

### D2. Cross-tier V4 coverage

**Recommended:** V4 at all three Claude tiers (Opus + Sonnet + Haiku) at combined N=40, mirroring M11a-extension symmetric coverage. M11a-extension's CT-V4-confirm result (V4-Sonnet AND V4-Haiku bytewise-identical mechanism response to V4-Opus on all 5 flagged events) holds bytewise at the M11a-extension N=20 cells; at N=40 we test whether this cross-tier mechanism stability **carries forward to the new 20 traces** (test_v31..test_v50). If it does (CT-V4-confirm at N=40), V4-Haiku consolidates as the cost-leader deployment recommendation. If it does NOT (CT-V4-partial or CT-V4-falsify at the new cells), the cross-tier stability finding was specific to the M11a-extension trace distribution.

**CT-V4-{confirm,partial,falsify} cell set at N=40 (D14-H3 definitional clarification):** the cross-tier-V4 diagnostic at N=40 evaluates the bytewise-identical-tier-response criterion over the UNION:
 - **(a)** the 5 M11a-extension-flagged events (test_v8 × {mom_birthday_heads_up, bridgers_presale_window}, test_v11 × trivia_league_round, test_v12 × {grocer_back_in_stock, calendar_yoga_suggest}) — inherited bytewise from M11a-extension's belt-and-suspenders carry-forward; AND
 - **(b)** any new test_v31..v50 event where ANY V4 tier (Opus OR Sonnet OR Haiku) produces a joint-bar verdict (`hit < 0.80 OR false/h > 5.0/h` at the trace level — surfaced via per-trace observation at Commit D).
- **CT-V4-confirm at N=40** = V4-Sonnet AND V4-Haiku produce bytewise-identical mechanism response to V4-Opus on ALL events in (a) ∪ (b).
- **CT-V4-partial at N=40** = bytewise-identical response on (a) but NOT on (b), OR partial agreement on (b).
- **CT-V4-falsify at N=40** = at least one (a) event diverges (M11a-extension carry-forward broken) OR substantial disagreement on (b).
The "ANY V4 tier joint-bar fires" inclusion criterion in (b) ensures we don't inflate CT-V4-confirm trivially by restricting to cells where all three tiers happen to all-pass. The expected case at N=40 is (a) holds bytewise (carry-forward gate) and (b) is the substantive new evidence.

**Cost trade-off:** V4-Opus N=40 incremental = ~$1.30 (per M11a-extension actual $1.29 for N=20 → linear extrapolation $1.29 × 1 = $1.29 for the 20 new cells); V4-Sonnet ~$0.19; V4-Haiku ~$0.06. Cross-tier adds ~$0.25 to the V4-Opus-only marginal cost. The cross-tier diagnostic preserves the CT-V4-confirm carry-forward gate cheaply.

**Fallback (if budget tightens):** V4-Opus-only at N=40 + V4-Sonnet/Haiku at N=20-incremental only on test_v31..v40 (half the new traces). Preserves the cross-tier dimension at reduced N=30 cross-tier scope.

### D3. N=40+ scope mechanics

**Recommended:** Pre-register **combined N=40 as the primary headline scope** at Commit A. Conditional-extension N=60 scope pre-registered as a tertiary option if N=40 lands in a discriminative-but-borderline region (defined below).

**Combined N=40 protocol details:**
- 20 new fresh-session-authored traces under M11a-extension iterative-extension protocol + self-restate pre-flight gate (acceptance rate ~77% per M11a-extension; expect 24-30 fresh sessions to land 20 accepted traces; M11a-extension's self-restate gate eliminated structural-parsing failures so the acceptance-rate denominator is dominated by drift-overlap and audit rejections)
- Numbering: **test_v31..test_v50 (locked at D14-H8)**. Rationale: preserves strict chronological ordering across milestones (M11a-extension closed at test_v30); the v9/v10 + v16..v20 gap remains as a transparent historical artifact per M11a-extension D14-H8 locked precedent.
- Banned-list extension carries forward unchanged: M10 ∪ M10b ∪ M11a ∪ M11a-extension iteratively-extended list (M11a-extension end-state 217 IDs / 122 themes / 121 tuples) ∪ M11a-extension-extension additions
- Audit-gate (8 checks) enforced verbatim per M11a-extension protocol; structural-parsing failure rate logged (expected 0/N per M11a-extension self-restate gate success)

**Conditional N=60 extension predicate (locked at Commit A):** if combined-N=40 V4-Opus CP CI width falls in (20pp, 30pp] AND |DELTA_PE| ∈ (5pp, 15pp), trigger conditional Commit-E for an additional 20 traces (test_v51..v70). This narrow region is the one where N=40 has SOME power but borderline-discriminates the ±10pp threshold; N=60 gives definitive resolution. Outside that region (CI ≤ 20pp = strong result OR CI > 30pp = M11a-extension-extension-extension scope) Commit E does not fire.

**D14-H2 closed-form 2D trigger table (locked at Commit A; covers the (CI width, |DELTA_PE|) plane exhaustively):**

| | |DELTA_PE| ≤ 5pp | 5pp < |DELTA_PE| ≤ 10pp | 10pp < |DELTA_PE| < 15pp | |DELTA_PE| ≥ 15pp |
|---|---|---|---|---|
| **CI ≤ 20pp** | Row 2 or Row 4 lands confidently (NEUTRAL + strong CI); Commit E does NOT fire | Row 2 or Row 4 lands confidently (NEUTRAL + strong CI); Commit E does NOT fire | Row 1 (or 3) or Row 6 lands confidently (IMPROVEMENT/REGRESSION + strong CI); Commit E does NOT fire | Row 1 (or 3) or Row 6 lands strongly (effect size large + strong CI); Commit E does NOT fire |
| **20pp < CI ≤ 30pp** | NEUTRAL with moderate CI; row identification stable at N=40 (Row 2 or Row 4); Commit E does NOT fire (N=60 cannot meaningfully shift NEUTRAL → IMPROVEMENT) | **Commit E FIRES** (borderline-reduction region; N=60 disambiguates Row 2/Row 4 vs Row 3) | **Commit E FIRES** (borderline-IMPROVEMENT or borderline-REGRESSION; N=60 disambiguates Row 1/Row 3 or Row 6) | Strong effect + moderate CI; row identification stable at N=40 (Row 6 if REGRESSION; Row 1/Row 3 if IMPROVEMENT); Commit E does NOT fire |
| **CI > 30pp (WIDE_CI)** | Row 5 UNDERPOWERED + PE near zero; Commit E does NOT fire — M11a-extension-extension-extension at N=80 named as separately-pre-registered future milestone (in Future Work) | Row 5 UNDERPOWERED + PE moderate; Commit E does NOT fire — M11a-extension-extension-extension at N=80 named | Row 5 UNDERPOWERED + PE substantial-but-CI-very-wide; Commit E does NOT fire — M11a-extension-extension-extension at N=80 named | Row 5 UNDERPOWERED + huge PE + very wide CI; Commit E does NOT fire (extreme outlier; treat as M11a-extension-extension-extension scope) — M11a-extension-extension-extension at N=80 named |

**Defense (reviewer-vulnerable Surface #14 — see §D9):** the Commit-E trigger predicate is mechanically computable from the N=40 result at end-of-Commit-D, with NO additional design decisions. Two cells fire Commit E; ten cells either land the Commit-D paper-line directly OR name M11a-extension-extension-extension as future work. The N=40 → N=60 escalation is bounded; M11a-extension-extension-extension (N=80) requires its own pre-reg milestone.

**Sensitivity scopes:** M11a-extension-extension-alone N=20 (test_v31..v50 only) reported alongside combined N=40 as the "double-protocol-revision-at-larger-N" sensitivity check.

### D4. Self-restate pre-flight gate

**Recommended:** INHERITED unchanged from M11a-extension at `eval/author_trace.py`. NO code changes at Commit B.

**Defense:** M11a-extension's self-restate gate dropped structural-parsing failure rate from 3/9 = 33% (M11a) to 0/13 (M11a-extension Commit C series). This is a stable infrastructure investment; no further hardening is warranted at this scale. If structural-parsing failures recur in M11a-extension-extension Commit C, surface as Commit-C operational finding without modifying the helper.

### D5. V4 path-C reserve

**Recommended:** SINGLE-SHOT pre-registration. NO path-C reserve. Mirrors M11a-extension's D5 verbatim.

**Defense:** V4 prompt is frozen bytewise from M11a-extension; this milestone is a sample-size extension not a prompt revision. The path-C reserve question is moot since there is no prompt-revision lever to flex.

**Implication:** If V4-Opus N=40 fires Row 6 (BACKFIRE) or Row 4 (NO IMPROVEMENT), M11a-extension-extension publishes that result as-is. V5 (if needed) remains a separate future milestone with its own pre-reg, NOT a continuation of M11a-extension-extension.

### D6. Surprise-gate-bypass residual

**Recommended:** DEFER unchanged per M11a-extension D6. Surprise-gate-bypass residual remains a pre-registered Non-goal addressed by separately-named M11d-surprise-gate-retuning milestone.

**Defense:** Adding sample size does not affect the structural-mechanism residual M11a-extension's V4-partial diagnostic identified at the cell level (3 z<-1 auto-surface + 1 surprise-gate-skip events at the 5-flagged-event cell breakdown). N=40 will confirm the V4-partial 1/5 cell-level finding at higher confidence but cannot resolve the surprise-gate-bypass mechanism since V4 cannot intervene on bypass cells. Reviewer-defense identical to M11a-extension D6.

### D7. Outcome row table — mutual exclusivity design

**Recommended:** SAME 6-row table inherited verbatim from M11a-extension §D7 with the SAME predicate definitions, SAME first-match-wins precedence. The only delta is the empirical N=40 input changes which predicates fire.

**Predicates (locked at Commit A; computed mechanically at Commit D):** mirror M11a-extension verbatim:

| Predicate | Definition |
|---|---|
| `DELTA_PE` | V4-Opus failure rate − V2-Opus failure rate (signed; combined N=40; joint-bar `hit < 0.80 OR false/h > 5.0/h`) |
| `IMPROVEMENT` | `DELTA_PE < −10pp` |
| `NEUTRAL` | `|DELTA_PE| ≤ 10pp` |
| `REGRESSION` | `DELTA_PE > +10pp` |
| `WIDE_CI` | V4-Opus 95% Clopper-Pearson CI width > 30pp |
| `MECHANISM_CONFIRM` | V4-Opus surfaces 0/3 of {trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest} at test_v11+test_v12 cells AND V4-Opus correctly YES-classifies BOTH mom_birthday_heads_up + bridgers_presale_window at test_v8 cell (strict 5/5) |
| `MECHANISM_PARTIAL` | 1-4 of the 5 flagged events corrected vs V2-Opus |
| `MECHANISM_FALSIFY` | 0 of the 5 flagged events corrected |
| `COMPLIANT_NO_REGRESSION` | V4-Opus joint-bar failure count on traces other than {test_v8, test_v11, test_v12} ≤ V2-Opus failure count (strict +0 tolerance) |

**Note on MECHANISM_CONFIRM at N=40:** the 5 flagged events live in the M11a-extension N=20 sample (test_v8, test_v11, test_v12 cells from M10b/M11a). The N=40 extension adds 20 NEW traces (test_v31..v50) with potentially NEW mechanism-flagged events. The pre-registered mechanism check inherits the SAME 5 events from M11a-extension; any new mechanism residuals surfaced by test_v31..v50 are reported as M11a-extension-extension-discovered residuals in Commit-D's per-trace observations table but do NOT enter the MECHANISM_CONFIRM/PARTIAL/FALSIFY predicate at this milestone. Future milestones (M11a-extension-extension-extension at N=80 or V5 prompt revision) would aggregate the new residuals.

**D14-H1 Row 1 STRICT SUCCESS reachability disclosure (load-bearing):** M11a-extension landed at V4-partial = 1/5 on the 5 flagged events. The Commit-B belt-and-suspenders carry-forward gate (§D13) re-executes V4-Opus + V4-Sonnet + V4-Haiku on the M11a-extension N=20 cells with PASS = bit-identical to `runs/data/21d-content-{opus,sonnet,haiku}-v4-*.json`. PASS preserves V4-partial = 1/5 deterministically; FAIL halts Commit B at a cross-milestone-drift finding (a separate residual paper-line, not a normal-completion path). Consequence: under normal Commit-B PASS, MECHANISM_CONFIRM at N=40 is **deterministically inherited at PARTIAL** = 1/5; **Row 1 STRICT SUCCESS is structurally unreachable at this milestone** (Row 1 requires strict 5/5). This is by design — the M11a-extension-extension scope is CI-tightening on the V4-vs-V2 headline at the same 5-event mechanism reference; mechanism-residual closure is M11d-surprise-gate-retuning + V5 future-work scope (Non-goal #1 + #2). Row 1's paper-line at §D8 is included for paper-line exhaustiveness and for the counterfactual case where the Commit-B belt-and-suspenders gate FAILS and the M11a-extension cells re-execute to strict 5/5 (cross-milestone-drift-attributable improvement) — see §D9 Surface #14 hardening for that residual mode. Under the expected path (Commit-B belt-and-suspenders PASSes bit-identical), the relevant target rows at this milestone are Row 3 (PARTIAL SUCCESS — reduction only with PARTIAL mechanism), Row 2 (NEUTRAL with PARTIAL mechanism), Row 4 (NEUTRAL with FALSIFY mechanism — would require regression on the 5 events vs M11a-extension), Row 5 (still UNDERPOWERED), or Row 6 (BACKFIRE).

**Strict-precedence row identification (first-match-wins):** identical to M11a-extension D7.

**Exhaustiveness check:** verified exhaustive AND mutually exclusive per M11a-extension D7.

### D8. Locked paper-line text per row + per branch

**Recommended:** Draft verbatim AT THIS PRE-REG (filed at Commit A); integer placeholders filled at Commit D; wording NOT edited. Mirror M11a-extension §D8 template with N=40 substitution + protocol-generation enumeration extended to FIVE protocol generations (M10 frozen list test_v4/v5; M10b frozen list test_v6/v7/v8; M11a iteratively-extended list test_v11..v15; M11a-extension iteratively-extended list test_v21..v30; M11a-extension-extension iteratively-extended list test_v31..v50).

**Per outcome row (verbatim; integer placeholders `{}`):**

**Row 1 (STRICT SUCCESS) — (unreachable at this milestone under expected Commit-B belt-and-suspenders PASS per D14-H1; included for paper-line exhaustiveness; would fire only on the counterfactual cross-milestone-drift path where the M11a-extension belt-and-suspenders re-execution itself produces strict 5/5 on the M11a-extension N=20 cells):**
> "Across N=40 fresh externally-authored traces under five protocol generations (M10 frozen list test_v4/v5; M10b frozen list test_v6/v7/v8; M11a iteratively-extended list test_v11..v15; M11a-extension iteratively-extended list test_v21..v30; M11a-extension-extension iteratively-extended list test_v31..v50), V4-Opus failure rate **{Xo}**/40 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**; CI width **{(Ho-Lo)pp}** ≤ 30pp; bootstrap CI **[{Lbo%}, {Hbo%}]**) reduces V2-Opus failure rate {Xv2}/40 = {Yv2%} (95% CP CI [{Lv2%}, {Hv2%}]) by **{D}pp** at point estimate. The M11a-extension Row 5 UNDERPOWERED verdict is **superseded** at the tightened N=40 CI. V4-Opus mechanism check: strict 5/5 of {trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest, mom_birthday_heads_up, bridgers_presale_window} corrected vs V2-Opus baseline at the M11a-extension flagged cells. V4-Opus compliant-content no-regression check: failure count on traces other than {test_v8, test_v11, test_v12} = {Xc} ≤ V2-Opus baseline {Xv2c}. Strict success: V4 prompt revision is the targeted lever that closes the V2-prompt-mechanism residual class without compliant-content regression at decisive N=40 statistical power. Cross-tier-V4 consistency: {V4-Sonnet vs V4-Opus delta; V4-Haiku vs V4-Opus delta — fills via cross-tier-V4 branch identification at N=40}."

**Row 2 (MECHANISM-ONLY, NET NEUTRAL):**
> "Across N=40 fresh externally-authored traces under five protocol generations, V4-Opus failure rate **{Xo}**/40 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**; CI width **{(Ho-Lo)pp}**) is within ±10pp of V2-Opus failure rate {Xv2}/40 = {Yv2%} (delta {D}pp at point estimate; ¬WIDE_CI per N=40 tightening). V4-Opus mechanism check passes ({m of 5} of the 5 flagged events corrected). V4-Opus compliant-content failure count on traces other than {test_v8, test_v11, test_v12} = {Xc} (V2-Opus baseline {Xv2c}; delta +{Xc-Xv2c} traces breaks +0 no-regression bar at N=40 power). V4 prompt revision fixes the targeted mechanism cells but introduces compensating regression on compliant content at decisive N=40 power; net failure rate unchanged. The M11a-extension Row 5 UNDERPOWERED → Row 2 transition at tightened CI provides confident evidence that V4's mechanism intervention is real-but-not-net-improving. V5 prompt revision should retain V4's NO-class additions while reverting the YES-enumeration extension causing compliant-content over-suppression. Cross-tier-V4 consistency: {V4-Sonnet vs V4-Opus; V4-Haiku vs V4-Opus}."

**Row 3 (PARTIAL SUCCESS — REDUCTION ONLY):**
> "Across N=40 fresh externally-authored traces under five protocol generations, V4-Opus failure rate **{Xo}**/40 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**) reduces V2-Opus failure rate {Xv2}/40 = {Yv2%} by **{D}pp** at point estimate AND CI width ≤ 30pp per N=40 tightening (M11a-extension Row 5 superseded). V4-Opus mechanism check is sub-MECHANISM_CONFIRM ({m of 5} corrected; strict 5/5 not met) OR compliant-content no-regression check fails (V4-Opus failure count on non-flagged traces {Xc} > V2-Opus baseline {Xv2c}). V4 prompt revision reduces overall failure rate at decisive N=40 power but the mechanism explanation does not fully account for the improvement (or the improvement comes with compliant-content regression). Reduction-only finding at tightened CI is publishable and motivates V5 with refined mechanism targeting. Cross-tier-V4 consistency: {V4-Sonnet vs V4-Opus; V4-Haiku vs V4-Opus}."

**Row 4 (NO IMPROVEMENT):**
> "Across N=40 fresh externally-authored traces under five protocol generations, V4-Opus failure rate **{Xo}**/40 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**; CI width ≤ 30pp per N=40 tightening) is within ±10pp of V2-Opus failure rate {Xv2}/40 = {Yv2%} (delta {D}pp at point estimate). V4-Opus mechanism check FAILS: 0 of 5 flagged events corrected vs V2-Opus. V4 prompt revision does NOT close the V2-prompt-mechanism residual class at decisive N=40 power. The M11a-extension Row 5 UNDERPOWERED → Row 4 transition at tightened CI provides confident evidence that V4's prompt-form intervention is not load-bearing for this residual class. M11c hierarchical routing or M11d-surprise-gate-retuning are the remaining levers. Cross-tier-V4 consistency: {V4-Sonnet vs V4-Opus; V4-Haiku vs V4-Opus}."

**Row 5 (UNDERPOWERED, residual):**
> "Across N=40 fresh externally-authored traces under five protocol generations, V4-Opus failure rate **{Xo}**/40 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**; CI width **{(Ho-Lo)pp}** > 30pp tolerance — N=40 tightening insufficient at the observed point estimate). The pre-registered N=60 conditional extension predicate {fires/does not fire}: V4-Opus CP CI width = {(Ho-Lo)pp} {∈/∉} (20pp, 30pp] AND |DELTA_PE| = {|D|}pp {∈/∉} (5pp, 15pp). {If fires: M11a-extension-extension Commit E adds test_v51..v70 for definitive resolution. If does not fire: M11a-extension-extension publishes the residual-underpower observation; tightening to N=80 named as M11a-extension-extension-extension.} Cross-tier-V4 consistency: {V4-Sonnet vs V4-Opus; V4-Haiku vs V4-Opus}."

**Row 6 (BACKFIRE):**
> "Across N=40 fresh externally-authored traces under five protocol generations, V4-Opus failure rate **{Xo}**/40 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**) is strictly higher than V2-Opus failure rate {Xv2}/40 = {Yv2%} by **{D}pp** at point estimate (delta exceeds +10pp regression tolerance{; CI width caveat if WIDE_CI also holds}). V4-Opus mechanism check: {V4-confirm/V4-partial/V4-falsify}. V4 prompt revision introduces failure modes V2-Opus did not exhibit at decisive N=40 power. The M11a-extension Row 5 UNDERPOWERED → Row 6 BACKFIRE transition at tightened CI is a clean falsification of V4 as a deployment-ready intervention. V5 prompt revision must address V4's failure mechanism. Cross-tier-V4 consistency: {V4-Sonnet vs V4-Opus; V4-Haiku vs V4-Opus}."

**V4-mechanism diagnostic + cross-tier-V4 diagnostic:** branch definitions + paper-lines INHERITED verbatim from M11a-extension §"V4-mechanism diagnostic" + §"Cross-tier-V4 consistency diagnostic". The 5 flagged events are the SAME inherited from M11a-extension cells; the diagnostic at N=40 RE-RUNS the cell-level mechanism check across the full combined sample.

### D9. Reviewer-vulnerable surfaces and pre-registered defenses

15 surfaces enumerated (post-D14-H1 hardening; was 14 pre-hardening). Surfaces #1-#13 inherited verbatim from M11a-extension §D9. NEW Surfaces #14 (N=40 still-wide-CI residual + N=60 conditional trigger) and #14b (Row 1 reachability under M11a-extension carry-forward) specific to this milestone:

1-13. Inherited verbatim from M11a-extension §D9 with N=20 → N=40 substitution where N appears in the defense text. Surfaces #5 (M11a-extension carry-forward bit-identical) + #13 (cross-milestone Claude alias drift between M11a-extension and M11a-extension-extension) gain a fresh re-execution at Commit B against M11a-extension's `runs/data/21d-*-v{2,4}-*.json`.

14. **N=40 still wide-CI: "you said N=40 would resolve it; what if N=40 fires Row 5 again?"** Defense: N=60 conditional extension predicate is pre-registered at D3 with a mechanical trigger condition (CI ∈ (20pp, 30pp] AND |DELTA_PE| ∈ (5pp, 15pp)); the 2D closed-form trigger table at D14-H2 enumerates the predicate over the full (CI, |DELTA_PE|) plane. Outside the firing region the milestone publishes the residual-underpower observation as-is and names M11a-extension-extension-extension at N=80 as a separately-pre-registered future milestone. The N=40 → N=60 conditional path is bounded; this is not an open-ended sample-size escalation.

**14b. Row 1 reachability: "Row 1 STRICT SUCCESS is structurally unreachable at this milestone — you've pre-committed to a milestone that can't land its strongest outcome."** Defense per D14-H1: Row 1 unreachability is a TRANSPARENT consequence of M11a-extension having already landed V4-partial = 1/5; the M11a-extension belt-and-suspenders carry-forward gate at Commit B preserves V4-partial deterministically; mechanism-residual closure is not this milestone's scope (Non-goals #1 + #2 name M11d-surprise-gate-retuning + V5 as the appropriate next levers). The milestone's stated scope is CI-tightening on the V4-vs-V2 headline; the target rows are Row 3 (PARTIAL SUCCESS — reduction at tightened CI), Row 2 (NEUTRAL with PARTIAL mechanism), Row 4 (NEUTRAL with FALSIFY mechanism), Row 5 (still UNDERPOWERED), Row 6 (BACKFIRE). Row 1's paper-line is retained at §D8 for exhaustiveness AND to cover the counterfactual case where the Commit-B belt-and-suspenders gate FAILS bit-identical AND the cross-milestone-drift-attributable re-execution lands V4-Opus at strict 5/5 on the M11a-extension cells (this would itself be a paper-line about Claude alias drift, not a clean Row 1 success — disclosed at the Row 1 paper-line header).

### D10. Cost framework + budget

**Per-cell unit-cost estimates (M11a-extension actuals as basis):**

| Component | Cells | Est. cost |
|---|---|---|
| **V4 harness — incremental N=20 → N=40** | | |
| V4-Opus 20 new cells (test_v31..v50) | 20 | $1.30 |
| V4-Sonnet 20 new cells (matched) | 20 | $0.19 |
| V4-Haiku 20 new cells (matched) | 20 | $0.06 |
| **V2 baseline extension at N=40** | | |
| V2-Opus 20 new cells (test_v31..v50) | 20 | $1.00 |
| **Belt-and-suspenders carry-forward re-run** | | |
| V4-Opus N=20 vs `21d-*-v4-opus-*.json` (bit-identical gate) | 20 | $1.30 |
| V4-Sonnet N=20 vs M11a-extension JSONs (bit-identical gate) | 20 | $0.19 |
| V4-Haiku N=20 vs M11a-extension JSONs (bit-identical gate) | 20 | $0.06 |
| V2-Opus N=20 vs M11a-extension `21d-content-opus-v2-*.json` (gate) | 20 | $0.50 |
| **Drift smoke (triangulated 3-phase)** | | |
| Opus carryover Phase 1 + 2 + 3 (vs `17b-*` carry-forward) | 9 | $0.45 |
| Sonnet baseline Phase 1 + 2 + 3 | 9 | $0.05 |
| Haiku baseline Phase 1 + 2 + 3 | 9 | $0.02 |
| **Fresh-session trace authoring (Commit C)** | | |
| ~28 fresh-session attempts × ~$0.05 (Sonnet 4.6 author) | 28 | $1.40 |
| Self-restate pre-flight gate API calls | — | $0.10 |
| **Pricing attestation fetch (Commit A)** | | |
| Anthropic pricing page fetch + extraction | 1 | $0.01 |
| **TOTAL (~196 cells)** | | **~$6.62** |
| **Conditional Commit E (N=60 extension)** | | |
| V4-Opus + V4-Sonnet + V4-Haiku + V2-Opus 20 new cells each | 80 | ~$2.55 |
| Fresh-session authoring × ~26 attempts | 26 | $1.30 |
| **CONDITIONAL TOTAL if Commit E fires** | | **~$10.47** |

**Pre-reg budget: $8 (covers Commit A-D primary) + $4 conditional reserve (Commit E if N=60 trigger fires) = $12 hard cap.** User-stated headline target: total spend ≤ $10 per milestone is the historical pattern; this milestone may push past that on the conditional Commit E path. Cumulative project spend M10→M11a-extension is ~$15.50 per the paper's cost summary; M11a-extension-extension primary commits $6.62 carries to ~$22 cumulative, well within reasonable bounds.

### D11. Pricing attestation refresh

**Recommended:** Re-execute the §D11 HARD GATE at Commit A. Confirm M10-locked Opus rate ($15/$75) + M11b-locked Sonnet rate ($3/$15) + Haiku rate ($1/$5) remain the right reference for internal cost modeling to preserve cross-milestone consistency through paper-line cost numbers in runs/17,18,19,20,21,22.

**HARD GATE at Commit A (mirror M11a-extension §D11):**
1. Fetch current Anthropic pricing page.
2. Extract input + output per-million-token rates for `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`.
3. Verify rates against M11a-extension's archived attestation. If any rate has rotated, document as Commit-A finding but **do not re-price** for internal cost modeling (M10/M11b lock holds through paper-v1+v2).
4. Archive fetched content as `runs/data/22a-pricing-attestation-{YYYY-MM-DD}.json` matching M11a-extension schema.
5. If verified rates differ from internal-cost-modeling rates, recompute D10 budget estimate and update `notes` field with delta.

### D12. Triangulated drift smoke

**Recommended:** Mirror M11a-extension §D12 verbatim — 9 cells Phase 1 + 6 cells Phase 2 + 6 cells Phase 3 = 21 cells across 3 phases × 3 tiers.

**Phase 1 — Commit B (pre-harness):**
- Opus carryover PASS gate (3 cells): V4-Opus on dev_v2/test_v1/test_v2; bit-identical compare against M11a-extension's `21d-baseline-content-opus-v4-*.json` (if exists) OR re-run as fresh Phase 1 baseline. **Note:** the bit-identical compare is against V4-Opus (not V2-Opus) — this milestone's V4 is identical bytewise to M11a-extension's V4 so the compare is symmetric. **FAIL halts Commit B**. Cost ~$0.15.
- Sonnet baseline (3 cells): V4-Sonnet on dev_v2/test_v1/test_v2; stored as `runs/data/22b-baseline-content-sonnet-v4-{dev_v2,test_v1,test_v2}.json`.
- Haiku baseline (3 cells): V4-Haiku on dev_v2/test_v1/test_v2; stored as `runs/data/22b-baseline-content-haiku-v4-{dev_v2,test_v1,test_v2}.json`.

**Phase 2 — Commit D (pre-harness):**
- Sonnet pre-harness smoke (3 cells): re-run V4-Sonnet on dev_v2/test_v1/test_v2; bit-compare against Phase 1 Sonnet baseline.
- Haiku pre-harness smoke (3 cells): same for V4-Haiku.

**Phase 3 — Commit D (post-harness):**
- Sonnet post-harness smoke (3 cells): re-run V4-Sonnet; bit-compare against Phase 1 + Phase 2.
- Haiku post-harness smoke (3 cells): same for V4-Haiku.

**Drift-smoke verdict policy:** mirror M11a-extension D12 verbatim. Opus carryover Phase 1 = HALT gate. Sonnet + Haiku Phase 2 + Phase 3 = observational, NOT halt-gate. M11a-extension Commit D observed Layer-2 within-milestone drift at test_v1+test_v2 on Sonnet+Haiku tiers in the 5-day Commit-B → Commit-D-end interval; if observed again at this milestone, characterize as same Surface #13 Layer-2 finding for paper-v2 framing.

**NEW for this milestone:** add a Layer-3 cross-milestone Claude alias drift smoke at Commit B comparing fresh V4 on dev_v2/test_v1/test_v2 against M11a-extension's `21b-baseline-content-*-v4-*.json` PASS gate. PASS = no cross-milestone Claude alias drift between M11a-extension 2026-05-15 and M11a-extension-extension Commit B execution date. FAIL halts Commit B as cross-milestone-drift finding (mirrors M11a-extension Surface #13 Layer-1 belt-and-suspenders).

### D13. Five-commit M10-shape protocol (with Commit E conditional)

**Recommended:** A pre-reg + pricing → B code wiring + drift baselines + belt-and-suspenders → C fresh-session trace authoring (test_v31..v50) → D harness + analysis → **E (conditional) N=60 extension if D3 trigger fires**. Mirror M11a-extension D13 with Commit E added as a pre-registered conditional.

| Commit | Content | Gates |
|---|---|---|
| **A** | (1) Pricing verification per §D11. (2) Pre-reg copy of this plan to `runs/22-v4-prompt-n40-extension-extension.md`. (3) NO touch to `sandbox/`, `agent/`, `baselines/`, `eval/`, `pyproject.toml`, `uv.lock`. | Pricing attestation archived + committed. |
| **B** | (1) **NO code changes** to `agent/arbiter.py`, `eval/run_trace.py`, `eval/author_trace.py` (all frozen from M11a-extension). (2) Verify `ARBITER_SYSTEM_PROMPT_V4` sha256 matches locked 09be309d... hash AND `git diff c056851 -- agent/ eval/ baselines/ sandbox/event_trace.py pyproject.toml uv.lock` is empty (D14-H4 dual gate). (3) 3-cell V4-Opus drift smoke vs M11a-extension `21b-baseline-content-opus-v4-*.json` if available, OR vs `17b-content-opus-v2-*.json` (V2 path; V4 bit-identical to M11a-extension is the V4-specific gate). (4) 3-cell V4-Sonnet baseline + 3-cell V4-Haiku baseline stored as `22b-baseline-*.json`. (5) Belt-and-suspenders 30-cell V4 re-run + 20-cell V2-Opus re-run vs M11a-extension `21d-*` JSONs. **Verdict policy per D14-H5:** V4-Opus belt-and-suspenders + V2-Opus belt-and-suspenders are HALT-gates on FAIL (Opus alias stable across milestones per M11a/M11b/M11a-extension empirical track record); V4-Sonnet + V4-Haiku belt-and-suspenders are OBSERVATIONAL on FAIL (mirrors M11a-extension §D12 Layer-2 within-milestone drift verdict policy — Sonnet+Haiku × test_v1+test_v2 drift observed Commit-B → Commit-D in M11a-extension, so cross-milestone Sonnet/Haiku drift is empirically expected and characterized as Surface #13 Layer-1 finding for paper-v2 framing, NOT halt). (6) NEW Layer-3 cross-milestone smoke per D12. | (3) PASS = V4 wiring carries forward unchanged. (5) PASS at Opus tier = halt-gate; PASS/FAIL at Sonnet/Haiku tier = observational. (6) PASS = cross-milestone Claude alias stable. Commit B total spend ≈ $2.05. |
| **C** | (1) Fresh-session-authored trace authoring per M11a-extension iterative-extension protocol + self-restate gate. (2) Iterate until 20 accepted traces authored under audit-gate (acceptance rate ~77% per M11a-extension; expect 24-30 fresh sessions). (3) New traces named `test_v31..test_v50` (locked at D14-H8 mirror). (4) Each accepted trace committed with separate transparent commit including self-restate response artifact + audit-gate PASS log. (5) Banned-list extension carries forward at each acceptance. | Audit-gate PASS for each accepted trace. Banned-list saturation halt-condition (defense #4 inherited): if after 50 fresh-session attempts < 20 traces are accepted, milestone halts pending banned-list-protocol revision. |
| **D** | (1) Phase 2 V4-Sonnet + V4-Haiku drift smoke (6 cells). (2) V4 N=40×3-tier harness matrix (60 incremental cells over M11a-extension carry-forward; combined 120 cells). (3) V2-Opus N=40 extension (20 incremental cells). (4) Phase 3 V4-Sonnet + V4-Haiku drift smoke (6 cells). (5) Aggregate analysis: per-trace observations + per-tier failure-rate metrics + Pareto cost ratios + CP CI + bootstrap CI + DELTA_PE/MECHANISM/COMPLIANT_NO_REGRESSION predicate computation + outcome row identification + V4-mechanism branch + cross-tier-V4 branch + N=60 conditional trigger evaluation. (6) `runs/22-v4-prompt-n40-extension-extension.md` results appendix + row 22 in `runs/README.md` + paper framing line update. | Verbatim eval against frozen D7 predicates. Conditional Commit E trigger evaluated per D3 predicate. |
| **E (conditional)** | Triggered iff D3 predicate fires (CI ∈ (20pp, 30pp] AND |DELTA_PE| ∈ (5pp, 15pp)). (1) 20 additional fresh-session-authored traces test_v51..v70 under M11a-extension protocol carry-forward. (2) V4×3-tier + V2-Opus N=60 harness extension (80 incremental cells). (3) Re-run §D7 outcome row identification at combined N=60. (4) Append results appendix to `runs/22-*.md`. | Conditional; only fires if D3 predicate true at Commit D. |

**D14-H6 Commit-E execution discipline (locked here; no new milestone-level kickoff required):**
- The Commit-E trigger is mechanically computed at end-of-Commit-D from the D3 predicate. If FIRES, Commit E proceeds within THIS milestone (M11a-extension-extension) using THIS plan as its locked source. NO separately-pre-registered plan is required. Splitting Commit E into a new plan would re-open post-data design tweaks; pre-registering Commit E here (with trigger + content fully specified) preserves pre-reg integrity.
- The fresh-session discipline applies to **trace authoring** (each test_v51..v70 acceptance is authored in a fresh session under the M11a-extension iterative-extension + self-restate gate protocol — ~26 fresh sessions expected per D10). The milestone-level design is locked at Commit A here; no fresh "kickoff" session is needed between Commit D and Commit E.
- If Commit E fires and lands a result, the Commit-E N=60 paper-line **SUPERSEDES** the Commit-D N=40 paper-line in `runs/22-*.md` "Headline outcome" framing and in paper v2 §sec:m11a-extension-extension. The Commit-D N=40 paper-line remains in the runs doc body as the intermediate-N appendix (transparent audit trail), but the milestone's headline outcome is the N=60 row.
- If Commit E does NOT fire (10 of 12 cells in the D14-H2 trigger table), the Commit-D N=40 paper-line IS the milestone headline; M11a-extension-extension-extension at N=80 is named as future work (in Future Work §) for the four CI > 30pp cells.

**Pre-Commit-D fix discipline:** carries forward from M11a-extension verbatim. Any bug surfaced gets separate transparent commit with bit-identical preservation proof.

**Aggregation-error-correction discipline:** carries forward verbatim.

### D14. Pre-data hardening discipline

**Recommended:** Schedule one honest hardening pass between Plan-drafted and Commit-A-landed. Don't pre-commit to zero edits; surface anything needing polish in a separate session before Commit A.

**Defense:** M11a-extension landed 7 substantive D14 edits to its source plan. M11b landed 0. Variance expected.

**Walkthrough trigger:** before Commit A landing, user opens this plan in a fresh session, walks through D1-D14 + the row table + locked paper-lines + reviewer-vulnerable-surfaces enumeration with adversarial-reviewer mindset. Anything surfaced gets edited into the plan at `~/.claude/plans/m11a-extension-extension-n40.md`. Then Commit A copies the plan to `runs/22-*.md`.

**D14 hardening pass landed at 2026-05-22 pre-Commit-A session:** 6 substantive edits applied to the locked source plan:
- **H1 (D7 + Row 1 paper-line header + Surface #14b):** Row 1 STRICT SUCCESS structurally unreachable at this milestone under expected Commit-B belt-and-suspenders PASS (M11a-extension landed V4-partial = 1/5; carry-forward preserves PARTIAL deterministically); disclosed at Row 1 paper-line header + Surface #14b reviewer-defense. Design choice preserved (CI-tightening scope, NOT mechanism-extension); consequence made explicit.
- **H2 (D3):** Closed-form 2D trigger table over (CI width, |DELTA_PE|) plane enumerating Commit-E-fires / Commit-D-lands / future-work-named for all 12 cells. Defends against "what about case X?" attacks.
- **H3 (D2):** CT-V4-{confirm,partial,falsify} cell set at N=40 defined over union of (a) M11a-extension 5 flagged events ∪ (b) new test_v31..v50 cells where ANY V4 tier produces joint-bar verdict. Resolves "what counts as a CT-V4 cell at N=40?" ambiguity.
- **H4 (D1):** Commit-B "no code wiring" gate strengthened from SHA-only to (a) ARBITER_SYSTEM_PROMPT_V4 SHA + (b) `git diff c056851 -- agent/ eval/ baselines/ sandbox/event_trace.py pyproject.toml uv.lock` empty (dual gate). Catches sibling-file drift the SHA alone cannot.
- **H5 (D10 / D12 / D13 Commit-B verdict policy):** Belt-and-suspenders verdict asymmetry pre-registered: V4-Opus + V2-Opus = HALT-gate on FAIL; V4-Sonnet + V4-Haiku = OBSERVATIONAL on FAIL (mirrors M11a-extension §D12 Layer-2 within-milestone drift verdict policy; M11a-extension empirically observed Sonnet/Haiku × test_v1/test_v2 drift Commit-B → Commit-D so cross-milestone Sonnet/Haiku drift is expected).
- **H6 (D13 Commit-E execution discipline):** Conditional Commit E does NOT require new plan-kickoff session; design locked in THIS plan with mechanical trigger; if fires, Commit-E N=60 paper-line SUPERSEDES Commit-D N=40 paper-line at milestone headline (transparent N=40 audit trail retained in body). Trace-authoring fresh-session discipline applies per-trace, not per-Commit.

No changes to D5 (single-shot pre-reg + no path-C reserve), D6 (surprise-gate-bypass deferred), D11 (pricing attestation refresh — re-executed at Commit A), or the Future Work / Non-goals lists. The §D8 row paper-line texts (Rows 2-6) are unchanged; Row 1 gets a header annotation only. The §"V4-mechanism diagnostic" + §"Cross-tier-V4 consistency diagnostic" inheritance from M11a-extension is unchanged (with D14-H3 clarifying the cell set for CT-V4-confirm at N=40).

---

## V4-mechanism diagnostic (3-branch; pre-registered with locked paper-lines)

INHERITED verbatim from M11a-extension §"V4-mechanism diagnostic". The 5 flagged events are the same cells from M10b/M11a (test_v8 + test_v11 + test_v12). At N=40 the cell-level mechanism check RE-RUNS at the full combined sample to verify M11a-extension's V4-partial 1/5 finding holds with the new V4 runs (M11a-extension's actual N=20 cells re-execute as Commit B belt-and-suspenders bit-identical gate; the 5-flagged-event mechanism check is therefore preserved bytewise from M11a-extension).

---

## Cross-tier-V4 consistency diagnostic (3-branch; pre-registered with locked paper-lines)

INHERITED verbatim from M11a-extension §"Cross-tier-V4 consistency diagnostic". M11a-extension landed at CT-V4-confirm (V4-Sonnet AND V4-Haiku bytewise-identical mechanism response to V4-Opus on all 5 flagged events). M11a-extension-extension tests whether CT-V4-confirm holds for the 20 NEW traces (test_v31..v50) at the cells where mechanism residuals surface — if no NEW residual cells appear, CT-V4-confirm inherits from M11a-extension. If new cells appear at the test_v31..v50 distribution, CT-V4-{confirm,partial,falsify} re-identified at combined N=40.

---

## Pre-registered analysis (Commit D)

1. **Per-trace observations:** combined N=40 × 3 tiers = 120 cells (V4) + 40 cells (V2-Opus baseline) = 160 cells total reported.
2. **Per-tier failure-rate metrics:** V4-Opus N=40; V4-Sonnet N=40; V4-Haiku N=40; V2-Opus N=40 baseline.
3. **Pareto cost ratios:** matched-arbiter $/hit at each tier × prompt cell; cross-tier and cross-prompt ratios at N=40 scope.
4. **CI computation:** Clopper-Pearson 95% CI for each per-tier failure rate at combined N=40 + N=20 sensitivity scope (M11a-extension-alone). Bootstrap CI (2000-resample non-parametric; `BOOTSTRAP_SEED = 42` inherited).
5. **Predicate computation:** mechanically compute DELTA_PE, IMPROVEMENT/NEUTRAL/REGRESSION, WIDE_CI, MECHANISM_*, COMPLIANT_NO_REGRESSION.
6. **Outcome row identification:** apply first-match-wins precedence (Row 6 → 5 → 1 → 3 → 2 → 4).
7. **V4-mechanism diagnostic branch identification:** apply 3-branch rule.
8. **Cross-tier-V4 diagnostic branch identification:** apply 3-branch rule.
9. **Drift smoke verdict:** Phase 2 + Phase 3 vs Phase 1 baseline + Layer-3 cross-milestone bit-comparison.
10. **Belt-and-suspenders verdict:** Commit-B re-run vs M11a-extension `21d-*` JSONs bit-comparison verdict.
11. **N=60 conditional trigger evaluation:** apply D3 predicate to N=40 result; if fires, Commit E pre-registered execution.
12. **Paper-line filling:** mechanically fill integer placeholders in identified row's locked paper-line + identified diagnostic branches' locked paper-lines.

---

## Critical files

**Modified at Commit A:**
- `runs/22-v4-prompt-n40-extension-extension.md` (NEW — pre-reg copy of this plan)
- `runs/data/22a-pricing-attestation-{YYYY-MM-DD}.json` (NEW — fresh attestation)

**Modified at Commit B:**
- NO code changes to `agent/`, `eval/` (all frozen from M11a-extension; SHA verification only)
- `runs/data/22b-baseline-content-{sonnet,haiku}-v4-*.json` (NEW — Phase 1 baselines)

**Modified at Commit C:**
- `sandbox/event_trace.py` (NEW trace definitions test_v31..v50; ~500-800 LOC additions)
- Per-trace audit-gate PASS log + self-restate response artifact files (`runs/data/22c-author-test_v{31..50}-*.json`)
- `runs/data/22c-banned-list-pre-c{1..20}.{txt,json}` (NEW — iterative banned-list snapshots)

**Modified at Commit D:**
- `runs/data/22d-content-{opus,sonnet,haiku}-v4-test_v{31..50}.json` (NEW — V4 harness output; 60 files)
- `runs/data/22d-content-opus-v2-test_v{31..50}.json` (NEW — V2-Opus N=40 extension; 20 files)
- `runs/data/22d-smoke-{preharness,postharness}-content-{sonnet,haiku}-v4-*.json` (NEW — drift smoke; 12 files)
- `runs/data/22d-analysis-summary.json` (NEW — aggregated analysis)
- `runs/22-v4-prompt-n40-extension-extension.md` (UPDATE — Commit D Results appendix)
- `runs/README.md` (UPDATE — row 22 entry + headline status block)

**Modified at Commit E (conditional):**
- `sandbox/event_trace.py` (NEW trace definitions test_v51..v70)
- Per-trace authoring artifacts mirroring Commit C
- `runs/data/22e-*.json` (NEW — N=60 extension harness)
- `runs/22-*.md` UPDATE Commit E Results appendix

**NOT touched at any commit (frozen):** `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py`, `eval/run_trace.py`, `eval/author_trace.py`. `sandbox/event_trace.py` existing test_v4..v15 + test_v21..v30 definitions = committed reference (only NEW trace definitions added).

---

## Non-goals

1. **V5 prompt revision.** V4 frozen verbatim per D1. V5 (if motivated by Row 4/6 outcome at N=40) is a separate future milestone.
2. **Surprise-gate-bypass fix (test_v4 mechanism + 3 z<-1 + 1 surprise-gate-skip events).** M11d-surprise-gate-retuning named as future work per M11a-extension D6 inheritance.
3. **Cross-vendor V4 sweep.** M11d-cross-vendor-mini-author-only named as future work; out-of-scope here.
4. **N=80+ scope.** Conditional N=60 covered at Commit E if trigger fires; N=80 would be a separately-pre-registered M11a-extension-extension-extension milestone.
5. **Hierarchical-routing deployment.** M11c named.
6. **External-reviewer audit of V4 prompt.** Internal pre-reg only.

---

## Future work (named residuals deferred from this milestone)

1. **M11a-extension-extension-extension at N=80+** — triggered iff this milestone fires Row 5 again at N=40 AND N=60 conditional trigger does not fire (i.e., very wide CI AND PE near zero OR near ±15pp). Outside the natural CI-narrowing trajectory; methodology paper-line on binomial CI behavior at small-N AB tests.
2. **M11d-surprise-gate-retuning** — addresses the 4-of-5 surprise-gate-bypass family identified at M11a-extension V4-partial breakdown. Loop-logic intervention at `agent/loop.py` z<-1 auto-surface path + surprise-gate-skip path.
3. **M11d-cross-vendor-mini-author-only** — see separate plan at `~/.claude/plans/m11d-cross-vendor-mini-author-only.md`.
4. **M11c-hierarchical-routing** — qwen2.5:3b-local → Sonnet/Opus escalation deployment shape.
5. **V5 prompt revision** — conditional on Row 4/6 outcome at this milestone OR M11d-surprise-gate-retuning closing the bypass residuals such that V5's marginal prompt-tuning gains a path to surface.
6. **Paper v2 update** — incorporate M11a-extension-extension outcome row into §sec:m11a-extension or new §sec:m11a-extension-extension subsection; supersede M11a-extension's Row 5 paper-line; update §sec:limitations statistical-power paragraph; update §sec:future M11a-extension-extension entry to "CLOSED at {row}".

---

## Walkthrough kickoff

**Pre-Commit-A convergence checklist:**

1. ⏳ User reads Plan-drafted output; surfaces objections to D1-D14 recommendations.
2. ⏳ User and assistant converge on D1-D14 decisions (no AskUserQuestion escalations expected; this plan is sample-size extension of M11a-extension's locked design).
3. ⏳ Plan locked at `~/.claude/plans/m11a-extension-extension-n40.md` (this file) as locked source.
4. ⏳ D14 hardening pass (separate fresh session) — audit D1-D14 + paper-lines + reviewer-defense surfaces.
5. ⏳ Commit A landing: pricing fetch → archive → pre-reg copy from locked plan to `runs/22-v4-prompt-n40-extension-extension.md`.

**State to confirm at Commit A kickoff (next session):**
- main HEAD at `c056851` (M11a-extension Commit D); working tree clean modulo untracked `paper/`
- Pricing attestation re-executed; `22a-pricing-attestation-{YYYY-MM-DD}.json` archived
- Plan landed at `~/.claude/plans/m11a-extension-extension-n40.md`
- D14 hardening pass complete

---

## Appendix: M11a-extension → M11a-extension-extension carry-forward summary

| M11a-extension artifact | M11a-extension-extension role |
|---|---|
| `ARBITER_SYSTEM_PROMPT_V4` sha256 09be309d... (1851 bytes) | Bytewise frozen; SHA verification gate at Commit B |
| `eval/author_trace.py` self-restate gate | Inherited unchanged |
| `runs/data/21d-content-{opus,sonnet,haiku}-v4-*.json` | Belt-and-suspenders bit-identical re-run reference (Commit B) + V4 baseline carry-forward for combined N=40 |
| `runs/data/21d-content-opus-v2-*.json` | V2-Opus baseline carry-forward for combined N=40 |
| `runs/data/21d-analysis-summary.json` | Predicate computation reference; M11a-extension Row 5 / V4-partial / CT-V4-confirm starting state |
| `runs/data/21c-banned-list-pre-c{1..10}.{txt,json}` | Iterative banned-list state input at Commit C iteration 1 (217 IDs / 122 themes / 121 tuples) |
| `runs/data/21a-pricing-attestation-2026-05-15.json` | Cross-milestone-locked rate reference (D11) |
| `agent/arbiter.py` rate table + `_rates_for` helper | Inherited unchanged |
| `--arbiter-system-prompt {v2,v3,v4}` CLI choice | Inherited unchanged |
| `--arbiter-model {opus,sonnet,haiku}` CLI choice | Inherited unchanged |
| `react_poll_claude` dedupe fix (`b78554d`) | Inherited unchanged |
| M11a-extension cross-tier carry-forward bit-identical pattern | Mirrored as M11a-extension-extension belt-and-suspenders + NEW Layer-3 V4-prompt-specific cross-milestone gate |
| M11a-extension triangulated drift smoke | Mirrored verbatim (D12) + Layer-3 cross-milestone smoke added |
| M11a-extension 6-row outcome paper-line lock template | Mirrored verbatim with N=20 → N=40 + protocol-generation count 4 → 5 |
| M11a-extension 13-surface reviewer-vulnerable enumeration | Mirrored + Surface #14 (N=40 still-wide-CI residual + N=60 conditional trigger) + D14-H1 Surface #14b (Row 1 reachability under M11a-extension carry-forward) → 15 surfaces total |
| M11a-extension cost framework | Mirrored with N=40 incremental cells + conditional Commit E reserve (D10) |
| M11a-extension 4-commit M10-shape protocol | Extended to 5-commit with conditional Commit E (D13) |
| M11a-extension transparent-bug-fix discipline (carry-forward of M11b `b78554d`) | Carries forward (D13) |
| M11a-extension transparent-correction-commit discipline (carry-forward of M11b `c0c6099`) | Carries forward (D13) |

---

## Commit B — SHA verification + drift baselines + belt-and-suspenders + Layer-3 cross-milestone smoke (2026-05-22)

**Pre-Commit-B reference state:** main HEAD `3fde41a` (M11a-extension-extension Commit A); working tree clean modulo untracked `paper/`. ARBITER_SYSTEM_PROMPT_V4 sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; unchanged since M11a-extension Commit B `adc1cba` 2026-05-15). Pre-reg budget for Commit B ≈ $2.05 per §D10.

### Gate (1) — Dual no-code-wiring (D14-H4) → PASS

- **(1a) V4 SHA verification:** in-process import + `hashlib.sha256(ARBITER_SYSTEM_PROMPT_V4.encode())` returns `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes) — bit-identical to locked value per §D1.
- **(1b) git diff-zero gate:** `git diff c056851 -- agent/ eval/ baselines/ sandbox/event_trace.py pyproject.toml uv.lock` produces 0 bytes. No sibling-file drift the SHA alone could miss.
- **Verdict:** PASS. Commit B is mechanically asserted "no code wiring".

### Gate (2) — Phase 1 V4-Opus carryover smoke → PASS (no halt-gate; reference absent)

Per §D12 fallback path: M11a-extension Commit B did not archive a `21b-baseline-content-opus-v4-*.json` reference (only Sonnet+Haiku Phase 1 baselines exist). The 3 cells (dev_v2, test_v1, test_v2) execute fresh as the Phase 1 V4-Opus baseline for Commit D Phase 2/3 within-milestone drift compare. Archived as `runs/data/22b-baseline-content-opus-v4-{dev_v2,test_v1,test_v2}.json` (3 files; HeargentZAWide skip+1.5; agent_name `heargent_za_content_surf-0.50_skip+1.50_w16`; cost $0.0610 total).

| Trace | hit_rate | arbiter_calls | cost_usd |
|---|---|---|---|
| dev_v2 | 1.0 | 4 | $0.01940 |
| test_v1 | 1.0 | 8 | $0.02112 |
| test_v2 | 1.0 | 7 | $0.02043 |

### Gate (3) — Phase 1 V4-Sonnet + V4-Haiku baselines → ARCHIVED

6 cells archived as `runs/data/22b-baseline-content-{sonnet,haiku}-v4-{dev_v2,test_v1,test_v2}.json` for the Commit D Phase 2/3 drift smoke reference. HeargentZAWide skip+1.5 (matches M11a-extension Commit B 21b-baseline convention). Cost $0.0357 total ($0.0282 Sonnet + $0.0094 Haiku).

| Tier | Trace | hit_rate | arbiter_calls | cost_usd |
|---|---|---|---|---|
| sonnet | dev_v2 | 1.0 | 4 | $0.00597 |
| sonnet | test_v1 | 1.0 | 8 | $0.01191 |
| sonnet | test_v2 | 1.0 | 7 | $0.01037 |
| haiku | dev_v2 | 1.0 | 4 | $0.00199 |
| haiku | test_v1 | 1.0 | 8 | $0.00396 |
| haiku | test_v2 | 1.0 | 7 | $0.00345 |

### Gate (5) — Layer-3 cross-milestone smoke (NEW) → PASS 6/6 bit-identical

`22b-baseline-content-{sonnet,haiku}-v4-*.json` (this Commit B; 2026-05-22) bit-compared against `21b-baseline-content-{sonnet,haiku}-v4-*.json` (M11a-extension Commit B; 2026-05-15). All 6 cells bit-identical on every deterministic field (`hit_rate`, `false_initiation_rate_per_hour`, `hits`, `misses`, `arbiter_calls`, `arbiter_yes_rate`, `arbiter_input_tokens`, `arbiter_output_tokens`, `arbiter_dispatched_model`, `cost_usd`, `agent_name`). Cross-milestone Claude alias drift between M11a-extension 2026-05-15 and M11a-extension-extension 2026-05-22 (7-day window): NONE.

**Empirical finding — Layer-2 within-milestone drift was transient and has recovered:**
M11a-extension Commit D §D12 (2026-05-20, 5 days post-21b-baseline) observed Phase 2/3 drift smoke FAIL at 4/6 cells (Sonnet+Haiku × test_v1+test_v2; hit 1.0→0.8; arb_calls n→n-1; characterized as observational per §D12 verdict policy). Today's fresh re-run on the SAME cells (2026-05-22, 7 days post-21b-baseline; 2 days post-21d-smoke FAIL) recovers bit-identical PASS to the 2026-05-15 baseline. The drift was TRANSIENT (~5-day window of altered Claude-side state that has reverted) and the cross-milestone Claude alias is stable on either side of the drift episode. This finding strengthens the Surface #13 carry-forward defense: Layer-2 drift episodes are bounded in time, not persistent alias rotations.

### Gate (4) — Belt-and-suspenders carry-forward (D14-H5) → PASS modulo metadata schema evolution + local-predictor-token variation

80 cells: V4 × 3 tiers × 20 traces (60) + V2-Opus × 20 traces (test_v4..v15 + test_v21..v30). Bit-comparison vs M11a-extension `21d-content-*-v{2,4}-*.json` (test_v21..v30) and M10/M10b/M11a `17b-/18d-/19d-content-opus-v2-*.json` (test_v4..v15).

**CRITICAL FINDING surfaced at Commit B execution — Surface #16 NEW (M11a-extension Commit D agent-variant regression):**

M11a-extension Commit B baselines (`21b-baseline-*`) used `agent.loop:HeargentZAWide` (skip threshold +1.5; the M6a band-edge-rescue variant locked across M10/M10b/M11a/M11b evaluation milestones). M11a-extension Commit D harness (`21d-content-*-v{2,4}-*` 60 V4 + 10 V2-Opus extension files) used `agent.loop:HeargentZA` base (skip threshold +1.0; the unrescued variant). M11a-extension Commit D §D12 drift smoke (`21d-smoke-*`) also used HeargentZA base. This is an unnoticed authoring oversight in M11a-extension Commit D — no documented switch to HeargentZA base, no defensive reasoning in the M11a-extension §D14 hardening pass.

**Load-bearing consequence for M11a-extension's published headline:** the §D7 Row 5 outcome (V4-Opus 6/20 = 30.0% + V2-Opus 7/20 = 35.0% + DELTA_PE −5.0pp NEUTRAL + WIDE_CI fires Row 5) was computed with skip+1.0 for V4 (all 20 cells) AND for V2-Opus test_v21..v30 (10 cells); but skip+1.5 was inherited from 17b/18d/19d for the V2-Opus test_v4..v15 baseline (10 cells). The M11a-extension N=20 V2-Opus combined sample is therefore a MIX of two agent variants. Skip+1.5 produces HIGHER hit rates per Commit B empirical comparison (M6a band-edge rescue effect: multiple cells show 0.8→1.0 hit-rate improvement under skip+1.5; cf. the discarded first-attempt 80-cell belt run that surfaced the regression).

**Commit B carry-forward methodology choice (load-bearing):** bit-identical reproduction of the M11a-extension Commit D measurement infrastructure as filed. V4 belt-and-suspenders (60 cells) + V2-Opus belt-and-suspenders test_v21..v30 (10 cells) re-run with `HeargentZA` base (skip+1.0) to bit-match `21d-content-*`. V2-Opus belt-and-suspenders test_v4..v15 (10 cells) re-run with `HeargentZAWide` (skip+1.5) to bit-match `17b/18d/19d-content-*`. This preserves bit-identical reproducibility of M11a-extension's filed measurement at the cost of inheriting the variant-mix in the V2-Opus baseline. The agent-variant regression is documented at Surface #16 below and pre-registered for paper-v2 §sec:limitations disclosure. A separate future-work milestone `M11a-extension-restate-baseline` is named to re-derive the M11a-extension headline at uniform skip+1.5 (out of scope here per CI-tightening primary objective).

**Discarded first-attempt sunk cost:** 70 cells of the initial 80-cell belt-and-suspenders attempt (V4 × 60 + V2-Opus test_v21..v30 × 10) were authored at HeargentZAWide (skip+1.5) following the M11a-extension Commit B baseline convention; these failed bit-comparison vs 21d because 21d used skip+1.0. Files deleted post-detection; cells re-authored with HeargentZA base. The 10 V2-Opus test_v4..v15 cells from the first attempt (correctly skip+1.5 to match 17b/18d/19d) were preserved. Sunk cost estimated at ~$2.25 from the first attempt's $1.4164 V4-Opus + ~$0.21 V4-Sonnet + ~$0.07 V4-Haiku + ~$0.55 V2-Opus test_v21..v30 totals (per the discarded JSONs' cost_usd fields, since deleted).

**Per-(gate × tier) bit-comparison results:**

| Bucket | Gate kind | Cells | Bit-identical | Metadata-only or local-token only | Mechanism divergent | Verdict |
|---|---|---|---|---|---|---|
| V4-OPUS (vs `21d-content-opus-v4-*`) | HALT | 20 | **20/20** | 0 | 0 | PASS |
| V4-SONNET (vs `21d-content-sonnet-v4-*`) | OBS | 20 | **20/20** | 0 | 0 | PASS |
| V4-HAIKU (vs `21d-content-haiku-v4-*`) | OBS | 20 | 19/20 | 1 (test_v13 completion_tokens 158→161; arbiter response + hit + cost bit-identical) | 0 | PASS (OBS) |
| V2-OPUS test_v21..v30 (vs `21d-content-opus-v2-*`) | HALT | 10 | **10/10** | 0 | 0 | PASS |
| V2-OPUS test_v4..v15 (vs `17b-/18d-/19d-content-opus-v2-*`) | HALT | 10 | 1/10 | 9 (arbiter_model field absent in 17b/18d/19d pre-M11b; mechanism bit-identical) | 0 | PASS (metadata schema evolution) |
| **TOTAL** | — | **80** | **70/80** | **10/80** | **0/80** | **PASS** |

**Belt-and-suspenders verdict:** 0 mechanism-divergent cells across all 80. 10 metadata-only divergences attributable to (a) `arbiter_model` field added at M11b post-dating 17b/18d/19d (9 cells; V2-Opus test_v4..v15 except test_v5 which has the 21b-belt post-M11b reference); (b) 3-token completion_tokens delta in V4-Haiku test_v13 attributable to local Ollama qwen2.5:3b-instruct predictor non-determinism (arbiter response + hit + cost all bit-identical). Both HALT-gates (V4-Opus + V2-Opus combined-N=20) clear on mechanism response. OBS Sonnet PASSES bit-identical; OBS Haiku PASSES modulo 1 local-predictor cell (within the §D12 observational policy for Sonnet/Haiku).

**Belt-and-suspenders cost (final 80-cell completion):** $2.4925 ($1.2922 V4-Opus + $0.1870 V4-Sonnet + $0.0622 V4-Haiku + $0.5023 V2-Opus test_v21..v30 + $0.4487 V2-Opus test_v4..v15).

### Cost framework — actual vs §D10 estimate

| Component | §D10 estimate | Actual at Commit B |
|---|---|---|
| Phase 1 V4-Opus carryover (3 cells) | $0.15 | $0.061 |
| Phase 1 V4-Sonnet baseline (3 cells) | $0.02 | $0.028 |
| Phase 1 V4-Haiku baseline (3 cells) | $0.01 | $0.009 |
| Belt-and-suspenders V4-Opus N=20 | $1.30 | $1.292 |
| Belt-and-suspenders V4-Sonnet N=20 | $0.19 | $0.187 |
| Belt-and-suspenders V4-Haiku N=20 | $0.06 | $0.062 |
| Belt-and-suspenders V2-Opus N=20 | $0.50 | $0.951 (split: $0.502 test_v21..v30 + $0.449 test_v4..v15) |
| **Subtotal (Commit B as filed)** | **$2.23** | **$2.591** |
| Sunk cost (first-attempt 70 cells at HeargentZAWide skip+1.5, deleted) | — | ~$2.250 (Surface #16 discovery overhead) |
| **TOTAL COMMIT B (including Surface #16 sunk cost)** | **~$2.23** | **~$4.84** |

Variance: +$2.61 (+117%) vs §D10 estimate. The overrun is fully attributable to the Surface #16 M11a-extension Commit D agent-variant regression discovery, which triggered a 70-cell re-run with the corrected agent variant. Cumulative milestone spend post-Commit-B: ~$4.84 of $8 primary + $4 conditional = $12 hard-cap pre-reg budget (~40%; ~$7.16 headroom remaining for Commits C/D ± conditional E).

### Halt-condition status at Commit B

- **D14-H4 dual no-code-wiring HALT-gate:** PASSED.
- **§D12 Phase 1 V4-Opus carryover HALT-gate:** N/A (reference absent; fresh baseline archived).
- **D14-H5 belt-and-suspenders V4-Opus HALT-gate:** PASSED 20/20 bit-identical.
- **D14-H5 belt-and-suspenders V2-Opus HALT-gate (combined):** PASSED on mechanism response (20/20 mechanism bit-identical; 9 cells metadata-only divergent on `arbiter_model` field schema evolution; documented as carry-forward variance, not a Claude-side drift).
- **§D12 Layer-3 cross-milestone HALT-gate:** PASSED 6/6 bit-identical.
- **Sonnet/Haiku belt-and-suspenders OBSERVATIONAL gates:** Sonnet 20/20 bit-identical; Haiku 19/20 + 1 local-predictor-token cell.

**Commit B outcome: PROCEED TO COMMIT C.**

### Surface #16 NEW — paper-v2 §sec:limitations disclosure (load-bearing pre-registration for Commit D)

**Title:** M11a-extension Commit D agent-variant regression (HeargentZA base skip+1.0 vs HeargentZAWide skip+1.5).

**Disclosure text (verbatim; to be inserted at paper-v2 §sec:limitations after the existing Surface #15 entry):**

> "M11a-extension's published Row 5 UNDERPOWERED + V4-partial 1/5 + CT-V4-confirm headline was measured with `agent.loop:HeargentZA` base (skip threshold +1.0) for the V4 N=20 harness (all 60 V4 cells × 3 tiers) and for the V2-Opus N=10 extension on test_v21..v30; the V2-Opus N=10 baseline on test_v4..v15 was inherited bit-identical from M10/M10b/M11a at `agent.loop:HeargentZAWide` (skip threshold +1.5; the M6a band-edge-rescue variant). The N=20 V2-Opus combined sample is therefore a mix of two agent variants. Skip+1.5 produces higher hit rates than skip+1.0 on the evaluation cells per M11a-extension-extension Commit B empirical comparison (multiple cells show 0.8→1.0 hit-rate improvement under skip+1.5). The variant mix in M11a-extension's N=20 V2-Opus baseline is an authoring oversight discovered at M11a-extension-extension Commit B (2026-05-22) during belt-and-suspenders bit-identical re-run; M11a-extension-extension proceeds with bit-identical reproduction of the M11a-extension Commit D measurement infrastructure (V4 + V2-Opus test_v21..v30 at skip+1.0; V2-Opus test_v4..v15 at skip+1.5) to preserve carry-forward integrity of the N=20 baseline. A separately-pre-registered future-work milestone `M11a-extension-restate-baseline` is named to re-derive the M11a-extension headline at uniform skip+1.5 to test whether the variant choice changes the Row 5 verdict at combined N=40; this is out of scope at M11a-extension-extension whose primary objective is CI tightening on the inherited measurement infrastructure."

**Future-work milestone (NEW pre-registration at this Commit B):** `M11a-extension-restate-baseline` — N=20 (or N=40) V4-Opus + V2-Opus re-derivation at uniform `agent.loop:HeargentZAWide` (skip+1.5) measurement infrastructure to test sensitivity of the §D7 outcome row to the agent-variant choice. Pre-reg if/when M11a-extension-extension closes and the variant question is judged paper-relevant.

### Frozen artifacts at Commit B (NOT touched, per locked plan §D13 Commit B row + D14-H4 dual gate)

`agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` (V4 prompt sha256 09be309d... unchanged); `eval/run_trace.py`, `eval/author_trace.py` (CLI choices + self-restate gate inherited verbatim from M11a-extension Commit B `adc1cba`); `sandbox/event_trace.py` (test_v4..v15 + test_v21..v30 definitions bit-identical pre and post Commit B execution); `baselines/`; `pyproject.toml`; `uv.lock`. All verified by D14-H4(b) `git diff c056851 -- agent/ eval/ baselines/ sandbox/event_trace.py pyproject.toml uv.lock` returning 0 bytes.

### Artifacts at Commit B (NEW)

- `runs/data/22b-baseline-content-{opus,sonnet,haiku}-v4-{dev_v2,test_v1,test_v2}.json` (9 NEW Phase 1 V4 baseline JSONs; Gate 2 + Gate 3 outputs)
- `runs/data/22b-belt-content-{opus,sonnet,haiku}-v4-test_v{4,5,6,7,8,11,12,13,14,15,21,22,23,24,25,26,27,28,29,30}.json` (60 NEW V4 belt-and-suspenders JSONs; HeargentZA base skip+1.0; bit-match `21d-content-*-v4-*`)
- `runs/data/22b-belt-content-opus-v2-test_v{4..v15,v21..v30}.json` (20 NEW V2-Opus belt-and-suspenders JSONs; test_v4..v15 at HeargentZAWide skip+1.5 matching 17b/18d/19d; test_v21..v30 at HeargentZA base skip+1.0 matching 21d)
- `runs/data/22b-belt-analysis-summary.json` (NEW; aggregated Commit B verdict artifact mechanically computed from the 89 input data files: per-gate verdicts + per-bucket bit-comparison + spend + Surface #16 + Layer-3 drift-recovery finding)

### Commit-C kickoff (next session)

Per locked plan §D13 Commit C row + locked `feedback_new_session_for_arch_work` memory:
- Open a FRESH session.
- Open `~/.claude/plans/m11a-extension-extension-n40.md` + read `runs/22-v4-prompt-n40-extension-extension.md` Commit B Results appendix (this section) for current state.
- Execute Commit C: 20 fresh-session-authored traces `test_v31..test_v50` under the M11a-extension iterative-extension protocol + self-restate pre-flight gate per `eval/author_trace.py` D-C1.3 / D-C1.4 / D-C1.5 governance carried forward from M11a-extension Commit C series.
- Banned-list starting state at C1 input: 217 IDs / 122 themes / 121 tuples (M11a-extension end-state per `runs/data/21c-banned-list-pre-c10.json` + C10 acceptance increments).
- Per-trace authoring discipline: each accepted trace gets a separate transparent commit including the self-restate response artifact + audit-gate PASS log + per-attempt count + banned-list-state-at-input + banned-list-state-after-acceptance.
- Acceptance rate per M11a-extension: ~77% (10 accepted / 13 attempts); expect ~24-30 fresh sessions to land 20 accepted traces.
- Halt-conditions to monitor: literal-ID collision (D-C1.5 #1); banned-list saturation (D-C1.5 #2 = §D9 defense #4; 50-attempt cap pre-registered); retry-cap 3 per trace (D-C1.5 #3).
- Per-trace fresh-session-discipline applies per-trace (each test_v3X acceptance is authored in a separate fresh session); MILESTONE-level kickoff between Commits B → C does NOT require a fresh kickoff per D14-H6 (the plan-design at `~/.claude/plans/m11a-extension-extension-n40.md` is the locked source; this Commit B appendix provides the operational state to resume).
- Pre-Commit-D fix discipline + transparent-correction-commit discipline carry forward unchanged from M11a-extension.

