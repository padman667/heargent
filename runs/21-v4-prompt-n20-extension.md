# Run 21 — M11a-extension: V4 prompt revision + N=20 expansion

**Pre-reg date:** 2026-05-15 (M11a-extension Commit A landing).
**Pre-reg SHA:** `b1d2521`
**Source plan:** `~/.claude/plans/m11a-extension-v4-prompt-n20.md` (locked source; this file is the verbatim pre-reg copy per §D13 Commit A step 2; any further plan revision happens at the locked-plan path and back-propagates to this file via §D13's pre-Commit-D fix discipline).
**Predecessor state:** M11b Commit D at HEAD `2d79690` (Row 1 at point estimate with Row 4a + Row 5 caveats; D7-confirm 6/6 cells; V2-Opus combined-N=10 corrected to 3/10 = 30% per `c0c6099`).
**Pricing attestation:** `runs/data/21a-pricing-attestation-2026-05-15.json` (zero observed-published-rate drift vs M11b's `20a-...-2026-05-13.json`; M10 lock $15/$75 Opus preserved for cross-milestone consistency; Sonnet $3/$15 + Haiku $1/$5 matched to M11b lock).
**D14 hardening pass status:** LOCKED at this Commit A. 7 substantive edits landed in the source plan (H1 verbatim V4 prompt text drafted; H2 Row 3 m=0 paper-line clarity; H3 MECHANISM_CONFIRM tightened ≥4/5 → strict 5/5; H4 COMPLIANT_NO_REGRESSION tightened ±1 → strict +0; H7 self-restate helper locked at `eval/author_trace.py`; H8 trace numbering locked at `test_v21..test_v30`; H9 added Surface #13 cross-milestone Claude alias drift); H5/H6/H10 confirmed no-edit.
**Frozen artifacts at Commit A:** `agent/`, `baselines/`, `eval/`, `sandbox/`, `pyproject.toml`, `uv.lock` — NOT touched. Commit A modifies only `runs/21-v4-prompt-n20-extension.md` (NEW) + `runs/data/21a-pricing-attestation-2026-05-15.json` (NEW) + `runs/README.md` (UPDATE — row 21 entry).

---

# M11a-extension: V4 prompt revision + N=20 expansion

**Status:** LOCKED post-D14 hardening pass (2026-05-15). 14 design decisions + 6 outcome-row paper-lines + 3-branch V4-mechanism + 3-branch cross-tier-V4 paper-lines + 13 reviewer-vulnerable-surfaces (12 base + #13 cross-milestone alias drift) drafted verbatim. D14 hardening pass surfaced 7 substantive edits (H1 verbatim V4 prompt text drafted; H2 Row 3 m=0 paper-line clarity; H3 MECHANISM_CONFIRM tightened ≥4/5 → strict 5/5; H4 COMPLIANT_NO_REGRESSION tightened ±1 → strict +0; H7 self-restate helper locked at `eval/author_trace.py`; H8 trace numbering locked at `test_v21..test_v30`; H9 added Surface #13). H5/H6/H10 confirmed no-edit. Ready for Commit A landing.

**Final landing path:** `zippy-tumbling-lagoon.md` is the system-mandated plan-mode draft location. After convergence + hardening pass, this file should be copied to `~/.claude/plans/m11a-extension-v4-prompt-n20.md` as the locked source. Commit A landing (which will copy this plan to `runs/21-v4-prompt-n20-extension.md` or similar) happens in a future fresh session, mirroring M11b's session structure.

**Pre-reference state (locked at draft time, 2026-05-15):**
- main HEAD `2d79690` (M11b Commit D); working tree clean
- M11b complete; D7-confirm 6/6; V2-Opus combined-N=10 corrected to 3/10 = 30% per `c0c6099`
- Latest pricing attestation: `runs/data/20a-pricing-attestation-2026-05-13.json` (M11b Commit A)
- All M11b code paths intact: `--arbiter-mode {content,random,claude}` + `--arbiter-system-prompt {v2,v3}` + `--arbiter-model {opus,sonnet,haiku}` + react_poll_claude dedupe fix
- Frozen artifacts NOT to touch in Commit A/B/C/D except as enumerated: `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `sandbox/event_trace.py` (existing test_v4..v15 definitions); new traces `test_v21..test_v30` (locked at D14-H8) added at Commit C

---

## Context

M11a-extension exists because M11b surfaced two distinct findings that converge on a single targeted next-step lever: V4 prompt revision.

**Finding 1 — D7-confirm at 6/6 cells (M11b §"Commit D Results", lines 627, 642):** The V2-prompt YES-bias on retail-back-in-stock + calendar-recurring-suggestion + casual-social-meetup distractor classes is preserved BYTEWISE across V2-Opus + V2-Sonnet + V2-Haiku + V2-3B (qwen2.5:3b) on the {test_v11, test_v12} cells. V2-Sonnet surfaces {`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`}; V2-Haiku surfaces the same three; V2-Opus and V2-3B surfaced these same three at M11a. The mechanism is V2-prompt-inherent across the entire Claude family + qwen2.5:3b — not a model-scale or model-family property. **The targeted next lever is V4 prompt revisions; cross-family swap below Opus does not address this residual.**

**Finding 2 — H2 finding sits at point-estimate only (M11b §"Commit D Results", lines 617-618):** V2-Sonnet, V2-Haiku, AND V2-Opus all have 95% CP CIs that contain V2-3B's 50% point estimate at combined N=10. The cross-family upgrade does NOT strictly beat V2-3B with non-overlapping CIs at N=10 for ANY Claude tier. The H2 finding ("model-scale closes M8b's coverage gap") is confirmed in direction but not in absolute at point estimate (Row 4a partial-closure with residuals).

**M11a-extension's role:** Test whether V4 prompt revision — designed from the D7-confirm + test_v8 V2-enumeration-limit evidence pre-registered as M11a/M11b future work — closes the V2-prompt-inherent residual class AND tightens the H2 finding via N=20+ combined scope. If V4 succeeds the paper has a complete causal chain: M11b D7-confirm establishes mechanism; M11a-extension V4 fixes it. If V4 fails or backfires that's a publishable null with mechanism diagnostic. Either outcome is a paper-shaped result.

**Paper-shape goal:** M11a-extension closure + M11b + M11a + M10b + M10 + M8b together produce the defensible first paper draft. No further empirical milestones planned after M11a-extension; next step is paper drafting.

---

## Thesis

V4 prompt revision (single-shot pre-reg; no path-C reserve; designed verbatim from the D7-confirm + test_v8 residuals BEFORE any N=10 fresh data is written) + N=20 combined scope at all three Claude tiers tests whether two pre-registered V2-prompt-mechanism residuals close under a single coherent targeted prompt revision. Cross-tier coverage symmetric with M11b's V2 cross-tier dimension.

**Question:** Does V4 reduce V2-Opus failure rate by > 10pp on combined N=20 AND fix the M11b D7-confirm distractor mechanism (0/3 surfaced at test_v11+test_v12 cells) AND fix the test_v8 V2-enumeration-limit residual (mom_birthday + bridgers_presale correctly YES-classified) AND not regress on V2-passing compliant content?

---

## Locked design choices (D1-D14)

### D1. V4 prompt text scope

**Recommended:** V4 addresses BOTH (a) the three M11b D7-confirm distractor classes (explicit NO examples for retail-back-in-stock / calendar-recurring-suggestion / casual-social-meetup) AND (b) the test_v8 V2-enumeration-limit residual (extended YES enumeration covering "discretionary-deadline obligations": family milestones with social cost; scarcity-bounded opportunities with limited windows).

**Defense:** Both residuals are V2-prompt-form-mechanism-class (not surprise-gate-mechanism-class per (c) below). Addressing both in a single coherent V4 revision is more defensible than addressing one and leaving the other for V5 because (i) the alternative requires V5-extension to be a separate milestone, doubling pre-reg overhead; (ii) V4 designed from the union of M10b/M11a/M11b residuals is more honestly "designed from pre-registered future work" than V4 designed from a strict subset; (iii) cleaner reviewer narrative — "V4 addresses two pre-registered residuals; the surprise-gate residual (test_v4) is a different mechanism deferred to a separately-named milestone."

**Risk surfaced:** V4 mechanism could fix test_v12 distractors but break test_v7-class compliant content (false-positive risk; pre-registered explicit no-regression check at D9.f).

**V4 prompt text — verbatim (locked at this D14 hardening pass per D8 lock policy; compiles bytewise into `agent/arbiter.py` at Commit B as `ARBITER_SYSTEM_PROMPT_V4` with no further editing between Commit A and Commit B):**

```python
ARBITER_SYSTEM_PROMPT_V4 = (
    "You are a triage filter for a proactive assistant. Decide whether a\n"
    "single observed event warrants surfacing to the user right now.\n"
    "\n"
    "Surface (YES) if the event describes any of:\n"
    " - an urgent safety or security issue (fire, break-in, medical\n"
    "   emergency, security breach, unauthorized access)\n"
    " - a schedule change affecting the user personally (meeting moved,\n"
    "   meeting cancelled, flight delayed, appointment rescheduled,\n"
    "   appointment cancelled)\n"
    " - a financial or deadline obligation the user must act on within\n"
    "   the next few days (bill due, rent due, report deadline,\n"
    "   payment reminder)\n"
    " - a message or delivery directed personally to the user (package\n"
    "   delivered, callback requested, voicemail or phone message,\n"
    "   hospital calling about a family member)\n"
    " - a weather alert or external condition that would plausibly\n"
    "   change the user's planned day\n"
    " - a production/on-call alert or outage for a system the user owns\n"
    " - a discretionary-deadline obligation: a family milestone with\n"
    "   social cost (birthday or anniversary heads-up) OR a\n"
    "   scarcity-bounded opportunity with a limited window (presale or\n"
    "   queue offer with a ticket limit and a window under one hour)\n"
    "\n"
    "Do NOT surface (NO) if the event is:\n"
    " - routine status, uptime, heartbeat, or \"all systems normal\" pings\n"
    " - marketing, promotional, or newsletter content\n"
    " - generic daily briefings that explicitly state no urgent items\n"
    " - feature announcements, app updates, or social/channel invites\n"
    " - a back-in-stock or restock notification without an explicit\n"
    "   scarcity window (e.g., \"your favorite item is back in stock\")\n"
    " - a recurring-event calendar suggestion or app suggestion\n"
    "   (e.g., \"add as recurring?\")\n"
    " - a casual social-meetup notification without time-pressure\n"
    "   (e.g., \"pub trivia tonight at 7pm\")\n"
    "\n"
    "Output exactly YES or NO, uppercase, on a single line. No explanation."
)
```

**Construction principles applied above (retained for audit transparency):**
1. Retain V2's six closed-enumeration YES classes verbatim (urgent safety/security; schedule change personal; financial/deadline obligation; message/delivery directed personally; weather alert; production/on-call alert).
2. Retain V2's four NO classes verbatim (routine status; marketing/promotional; generic daily briefings; feature announcements/social invites) and ADD three explicit NO subclauses with one canonical example each (back-in-stock without scarcity window; recurring-event calendar suggestion; casual social-meetup without time-pressure) — each subclause maps 1:1 to one M11b D7-confirm distractor class.
3. Extend YES enumeration with a seventh class: discretionary-deadline obligation (family milestone with social cost OR scarcity-bounded opportunity, window < 1 hour) — maps to the two M11a test_v8 V2-enumeration-limit events (`mom_birthday_heads_up` + `bridgers_presale_window`).
4. Output format unchanged: single line, `YES` or `NO` uppercase, no explanation. Chat-template segmentation (system+user via `client.chat(system=..., user=text)`) bytewise identical to V2 per M9 wire-up choice (a) at `agent/arbiter.py` line 96 carry-forward.

**Bytewise verification at Commit B:** copy the Python-literal block above verbatim into `agent/arbiter.py` between `ARBITER_SYSTEM_PROMPT_V3` and the `_DECISION` regex line. The pre-flight V2-Opus carryover smoke (§D12 Phase 1, §D13 Commit B step 4) verifies the V4 wiring did not disturb the V2 code path — V2 byte-identical to `runs/data/17b-content-opus-v2-*.json` after V4 wiring.

**Reviewer-defense (post-hoc opportunism):** V4 designed from D7-confirm + test_v8 residuals that were ALSO pre-registered as future work at M10b §"Future work" + M11a §"Future work" + M11b §"Future work" (per `runs/20-cross-model-sweep.md` line 689 verbatim). V4 design is constrained by pre-registered mechanism evidence, not opportunistic post-hoc tuning.

### D2. Cross-tier V4 coverage

**Recommended:** V4 at all three Claude tiers (Opus + Sonnet + Haiku) at N=20 combined scope.

**Defense:** Symmetric with M11b's cross-tier-V2 dimension (cross-tier-prompt-swap parallels cross-tier-model-swap). D7-confirm proved V2-prompt YES-bias is bytewise-identical across all three Claude tiers; V4 should be tested at all three tiers to characterize whether V4 mechanism is also tier-stable (cross-tier-V4-confirm: V4 fixes mechanism uniformly across tiers) or tier-dependent (cross-tier-V4-partial / cross-tier-V4-falsify: V4 effect differs across tiers, suggesting prompt-mechanism interacts with model-scale).

**Cost trade-off:** V4-Opus-only at N=20 = ~$2.16; V4 at three tiers at N=20 = ~$2.51 (Sonnet ~$0.22; Haiku ~$0.07; per M11b's per-cell averages). Cross-tier coverage adds <$0.50 to the milestone budget for a substantively important diagnostic. The scientifically-defensible choice has clear marginal-cost dominance.

**Fallback (if budget tightens):** V4-Opus-only at N=20 + V4-Sonnet/Haiku at N=10 each (M11a-extension-alone scope, not combined). This preserves the cross-tier dimension at reduced power.

### D3. N=20+ scope mechanics

**Recommended:** Pre-register **combined N=20 as the primary headline scope** at Commit A. M11a-extension-alone N=10 fresh as a secondary sensitivity-check scope (also pre-registered at Commit A as a parallel reported metric).

**Defense:** M11b's row table had multiple N-scopes reported in parallel which created the Row 1 + Row 4a + Row 5 concurrent-fire ambiguity. M11a-extension avoids this by **declaring one headline scope before the data is written**: combined N=20 (M10's test_v4/v5 + M10b's test_v6/v7/v8 + M11a's test_v11..v15 + M11a-extension's 10 new fresh-session-authored traces).

**Combined N=20 protocol details:**
- 10 new fresh-session-authored traces under M11a iterative-extension protocol (acceptance rate ~56% per runs/19; expect 12-18 fresh sessions to land 10 accepted traces)
- Numbering: **test_v21..test_v30 (locked at D14-H8 hardening pass)**. Rationale: preserves strict chronological ordering across milestones — M11a closed at test_v15, so M11a-extension resumes the sequence; the v9/v10 gap remains as a transparent historical artifact (test_v9 was M10b's halt-attempt-#2 sequence; test_v10 was never authored). Gap-filling (the test_v16..v20 + test_v21..v25 alternative) would create a non-monotonic numbering scheme that future readers must learn; chronological resumption is the simpler reviewer-facing choice.
- Banned-list extension carries forward: M10's frozen list ∪ M10b's frozen list ∪ M11a's iteratively-extended list ∪ M11a-extension's iteratively-extended additions
- Audit-gate enforced at Commit C per M11a's protocol; fresh-session structural-parsing-failure rate logged

**Sensitivity scope:** M11a-extension-alone N=10 fresh failure rate reported alongside combined N=20 as the "protocol-revision-at-larger-N" sensitivity check. If M11a-extension-alone N=10 differs substantively from combined N=20, surface as a Commit-D sensitivity observation.

### D4. Self-restate pre-flight gate

**Recommended:** INCLUDE at Commit B as a small code addition (~10-30 LOC).

**Defense:** M11a had 33% structural-parsing-failure rate (3/9 fresh-session attempts: test_v11 #1 walrus syntax; test_v13 #2 arithmetic; test_v15 #1 arithmetic). At N=10 fresh-session-authored-trace target with 33% structural-parsing-failure rate, the fresh-session attempt budget could exceed 15 attempts before banned-list saturation halts the milestone under defense #4. The defensibility cost of NOT including a self-restate pre-flight gate: future reviewer asks "why did you continue using a protocol with a known 33% structural-parsing-failure rate when you knew about it at M11a?" Easier to include the fix at Commit B with a transparent diff than to defend the omission.

**Implementation sketch (locked at Commit A, wired at Commit B):** Before the fresh-session author opens, the protocol issues a self-restate prompt: "You will author one EventTrace for the heargent harness. Per M11a iterative-extension protocol, your trace must (a) use only Python expressions parseable by sandbox/event_trace.py; (b) not use walrus operator; (c) not use arithmetic in event_id strings; (d) avoid reusing event_ids from the iteratively-extended banned list (provided below). Restate (a)-(d) in your own words before authoring." Self-restate response logged as a Commit C artifact alongside the trace.

**File location (locked at D14-H7 hardening pass):** `eval/author_trace.py` (NEW; ~20 LOC). Rationale: `eval/` is the existing repo-root harness-script directory (housing `eval/run_trace.py`, `eval/sweep.py`, `eval/probes/`); `scripts/` does not exist at repo root, and creating it would introduce a second harness-script directory inconsistent with M10/M10b/M11a/M11b precedent. The self-restate helper is a harness-side pre-flight step, fitting `eval/`'s purpose. Module entry point: `python -m eval.author_trace --banned-list <path>` per `eval/run_trace.py` invocation pattern.

**Cost:** Negligible harness time (~1-2 additional API calls per fresh-session attempt at sub-cent unit cost).

### D5. V4 path-C reserve

**Recommended:** SINGLE-SHOT pre-registration. NO path-C reserve.

**Defense:** Three reasons:
1. **D7-confirm at 6/6 makes V4 mechanism well-motivated.** We have STRONG evidence what V4 should look like (explicit NO for the three D7-confirm distractor classes). M9 V3 had weak prior evidence about what V3 should fix; M11a-extension V4 has bytewise-identical 6/6 cross-product evidence about what V4 should fix.
2. **Path-C reserve opens "p-hacking by iteration" attack surface.** Up-to-2-redesign-rounds-on-data is a flexible-stopping-rule pattern that reviewers correctly flag as biased. Single-shot is stricter and provides cleaner falsification.
3. **M9 V3 path-C reserve was held unused anyway.** M9 hit a single-shot null on round 0 and the path-C reserve was documented but not exercised. Empirical precedent supports single-shot for V4.

**Implication:** If V4-Opus single-shot fires Row 4 (NO IMPROVEMENT) or Row 6 (BACKFIRE), M11a-extension publishes that result as-is. V5 (if needed) is a separate future milestone with its own pre-reg, not a continuation of M11a-extension under a flexible-stopping rule.

### D6. Surprise-gate-bypass residual (test_v4 mechanism)

**Recommended:** DEFER to a separately-named milestone. Include in M11a-extension §"Non-goals" + §"Future work" as a named residual.

**Defense:** test_v4 V2-Opus joint-bar failure (false/h = 7.128 > 5.0/h) is driven by `designgrid_renewal` + `calendar_feature_tip` events bypassing the arbiter entirely via z<−0.5 surprise-gate auto-surf (per runs/19 line 1854 mechanism breakdown item (c)). V4 prompt revision does not address this residual because the arbiter is never consulted on these events. Expanding M11a-extension scope to include a surprise-gate fix would (i) introduce a confounding mechanism intervention; (ii) require additional code changes to `agent/surprise.py` (frozen artifact); (iii) inflate cost and complexity beyond the M11a-extension thesis. **Reviewer-defense:** "We address two of three pre-registered residuals; the third (surprise-gate auto-surf bypass) is a different mechanism named M11d-surprise-gate-retuning as future work."

### D7. Outcome row table — mutual exclusivity design

**Recommended:** 6 rows mutually exclusive BY CONSTRUCTION via predicate composition + strict precedence rule (first-match-wins) for edge cases. Avoids M11b's Row 1 + Row 4a + Row 5 concurrent-fire ambiguity.

**Predicates (locked at Commit A; computed mechanically at Commit D):**

| Predicate | Definition |
|---|---|
| `DELTA_PE` | V4-Opus failure rate − V2-Opus failure rate (signed; combined N=20; joint-bar `hit < 0.80 OR false/h > 5.0/h` per M11a line 224) |
| `IMPROVEMENT` | `DELTA_PE < −10pp` |
| `NEUTRAL` | `|DELTA_PE| ≤ 10pp` |
| `REGRESSION` | `DELTA_PE > +10pp` |
| `WIDE_CI` | V4-Opus 95% Clopper-Pearson CI width > 30pp |
| `MECHANISM_CONFIRM` | V4-Opus surfaces 0/3 of {`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`} at test_v11+test_v12 cells AND V4-Opus correctly YES-classifies BOTH `mom_birthday_heads_up` + `bridgers_presale_window` at test_v8 cell (**strict 5/5** of the 5 flagged events corrected vs V2-Opus; tightened at D14 hardening pass per H3 — single-shot temperature=0 inference is deterministic so noise-tolerance argument does not apply, and the V4 design has a 1:1 clause-to-event mapping so any single miss IS a clause-level mechanism failure) |
| `MECHANISM_PARTIAL` | 1-4 of the 5 flagged events corrected vs V2-Opus |
| `MECHANISM_FALSIFY` | 0 of the 5 flagged events corrected (V4-Opus bytewise-identical to V2-Opus on all 5) |
| `COMPLIANT_NO_REGRESSION` | V4-Opus joint-bar failure count on traces other than {test_v8, test_v11, test_v12} ≤ V2-Opus failure count (**strict no-regression; +0 tolerance**; tightened at D14 hardening pass per H4 — single-shot temperature=0 inference is deterministic so any trace-level delta is real signal not Bernoulli noise; +1 wiggle was unprincipled p-hacking room) |

**Strict-precedence row identification (first-match-wins, evaluated top to bottom):**

| Order | Row | Predicate composition |
|---|---|---|
| 1 | **Row 6 (BACKFIRE)** | `REGRESSION` (CI width caveat in paper-line if `WIDE_CI`) |
| 2 | **Row 5 (UNDERPOWERED)** | `NEUTRAL` ∧ `WIDE_CI` |
| 3 | **Row 1 (STRICT SUCCESS)** | `IMPROVEMENT` ∧ `MECHANISM_CONFIRM` ∧ `COMPLIANT_NO_REGRESSION` |
| 4 | **Row 3 (PARTIAL SUCCESS — REDUCTION ONLY)** | `IMPROVEMENT` ∧ (¬`MECHANISM_CONFIRM` ∨ ¬`COMPLIANT_NO_REGRESSION`) |
| 5 | **Row 2 (MECHANISM-ONLY, NET NEUTRAL)** | `NEUTRAL` ∧ ¬`WIDE_CI` ∧ (`MECHANISM_CONFIRM` ∨ `MECHANISM_PARTIAL`) |
| 6 | **Row 4 (NO IMPROVEMENT)** | `NEUTRAL` ∧ ¬`WIDE_CI` ∧ `MECHANISM_FALSIFY` |

**Exhaustiveness check:** every (DELTA_PE class × WIDE_CI × MECHANISM class × COMPLIANT_NO_REGRESSION) combination maps to exactly one row. `REGRESSION` → Row 6. `IMPROVEMENT` → Row 1 or Row 3 depending on mechanism+regression check. `NEUTRAL` → Row 5 if wide CI, else Row 2 or Row 4 depending on mechanism. **Verified exhaustive AND mutually exclusive.**

### D8. Locked paper-line text per row + per branch

**Recommended:** Draft verbatim AT THIS PRE-REG (filed at Commit A); integer placeholders filled at Commit D; wording NOT edited. Mirror M11b §D5 template.

**Per outcome row (verbatim; integer placeholders `{}`):**

**Row 1 (STRICT SUCCESS):**
> "Across N=20 fresh externally-authored traces under four protocol generations (M10 frozen list test_v4/v5; M10b frozen list test_v6/v7/v8; M11a iteratively-extended list test_v11..v15; M11a-extension iteratively-extended list {trace IDs}), V4-Opus failure rate **{Xo}**/20 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**; bootstrap CI **[{Lbo%}, {Hbo%}]**) reduces V2-Opus failure rate {Xv2}/20 = {Yv2%} (95% CP CI [{Lv2%}, {Hv2%}]) by **{D}pp** at point estimate. V4-Opus mechanism check: 0/3 of the M11b D7-confirm flagged distractors ({trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest}) surfaced at test_v11+test_v12 cells; both mom_birthday_heads_up + bridgers_presale_window correctly YES-classified at test_v8 cell. V4-Opus compliant-content no-regression check: failure count on traces other than {test_v8, test_v11, test_v12} = {Xc} (V2-Opus baseline {Xv2c}). The V2-prompt-inherent YES-bias residual (M11b D7-confirm 6/6) AND the V2-enumeration-limit residual (M11a test_v8) both close under V4 prompt revision at the Opus tier. Cross-tier-V4 consistency: {V4-Sonnet result vs V4-Opus delta; V4-Haiku result vs V4-Opus delta — fills via §"Cross-tier-V4 consistency diagnostic" branch identification}. Strict success: V4 prompt revision is the targeted lever that closes the V2-prompt-mechanism residual class without compliant-content regression on this sample."

**Row 2 (MECHANISM-ONLY, NET NEUTRAL):**
> "Across N=20 fresh externally-authored traces under four protocol generations, V4-Opus failure rate **{Xo}**/20 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**) is within ±10pp of V2-Opus failure rate {Xv2}/20 = {Yv2%} (delta {D}pp at point estimate). V4-Opus mechanism check passes ({m of 5} of the 5 M11b/M11a-flagged events corrected vs V2-Opus; MECHANISM_CONFIRM threshold is strict 5/5 per D14-H3; this row admits MECHANISM_CONFIRM at m=5 or MECHANISM_PARTIAL at 1≤m≤4). V4-Opus compliant-content failure count on traces other than {test_v8, test_v11, test_v12} = {Xc} (V2-Opus baseline {Xv2c}; delta +{Xc-Xv2c} traces; strict +0 no-regression per D14-H4 broken since DELTA_PE is NEUTRAL not IMPROVEMENT). V4 prompt revision fixes the targeted mechanism cells but introduces compensating regression on compliant content; net failure rate unchanged. Mechanism-level success without overall success: V4 trades V2-prompt-mechanism residual for compliant-content false-suppress residual. The V4 prompt revision is mechanism-targeted but not deployment-ready as drafted; V5 prompt revision should retain V4's NO-class additions while reverting the YES-enumeration extension that caused compliant-content over-suppression. Cross-tier-V4 consistency: {V4-Sonnet result vs V4-Opus delta; V4-Haiku result vs V4-Opus delta}."

**Row 3 (PARTIAL SUCCESS — REDUCTION ONLY):**
> "Across N=20 fresh externally-authored traces under four protocol generations, V4-Opus failure rate **{Xo}**/20 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**) reduces V2-Opus failure rate {Xv2}/20 = {Yv2%} by **{D}pp** at point estimate. V4-Opus mechanism check is sub-MECHANISM_CONFIRM: {m of 5} of the 5 M11b/M11a-flagged events corrected vs V2-Opus (strict 5/5 MECHANISM_CONFIRM threshold per D14-H3 not met; this row admits m=0 MECHANISM_FALSIFY through m=4 MECHANISM_PARTIAL co-occurring with IMPROVEMENT — empirically rare for m=0 but admitted for completeness) OR compliant-content no-regression check fails (V4-Opus failure count on traces other than {test_v8, test_v11, test_v12} = {Xc}; V2-Opus baseline {Xv2c}; delta +{Xc-Xv2c} traces breaks strict +0 no-regression bar per D14-H4). V4 prompt revision reduces overall failure rate but the mechanism-level explanation does not fully account for the improvement (or the improvement comes with a compliant-content regression that the headline metric doesn't surface). Reduction-only finding is publishable but motivates V5 with refined mechanism targeting. Cross-tier-V4 consistency: {V4-Sonnet result vs V4-Opus delta; V4-Haiku result vs V4-Opus delta}."

**Row 4 (NO IMPROVEMENT):**
> "Across N=20 fresh externally-authored traces under four protocol generations, V4-Opus failure rate **{Xo}**/20 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**) is within ±10pp of V2-Opus failure rate {Xv2}/20 = {Yv2%} (delta {D}pp at point estimate; CI width {(Ho-Lo)pp} ≤ 30pp tolerance). V4-Opus mechanism check FAILS: 0 of the 5 M11b/M11a-flagged events corrected vs V2-Opus (V4-Opus bytewise-identical to V2-Opus on all 5 flagged cells). V4 prompt revision does NOT close the V2-prompt-mechanism residual class on this sample at sufficient sample size to discriminate ±10pp deltas. Mechanism diagnosis: V4's added explicit NO subclauses + extended YES enumeration are not load-bearing for the model's classification on the flagged events; the V2-prompt YES-bias is robust to the targeted prompt revision. M11c hierarchical routing or non-prompt mechanism interventions are the remaining lever for the V2-prompt-mechanism residual. Cross-tier-V4 consistency: {V4-Sonnet result vs V4-Opus delta; V4-Haiku result vs V4-Opus delta}."

**Row 5 (UNDERPOWERED):**
> "Across N=20 fresh externally-authored traces under four protocol generations, V4-Opus failure rate **{Xo}**/20 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**; CI width **{(Ho-Lo)pp}** > 30pp tolerance) is within ±10pp of V2-Opus failure rate {Xv2}/20 = {Yv2%} at point estimate but the binomial CI is too wide to discriminate the ±10pp threshold. The cross-prompt comparison is underpowered at N=20 to distinguish V4-vs-V2 deltas at the pre-registered ±10pp resolution. Bootstrap CI from per-trace outcomes also reported and yields the same wide-CI conclusion. Mechanism diagnosis from V4-mechanism-branch identification: {V4-confirm/V4-partial/V4-falsify}. The M11a-extension finding is the under-power observation itself; substantive cross-prompt ranking is deferred to M11a-extension-extension (N=40+) for tightened CIs. Cross-tier-V4 consistency: {V4-Sonnet result vs V4-Opus delta; V4-Haiku result vs V4-Opus delta}."

**Row 6 (BACKFIRE):**
> "Across N=20 fresh externally-authored traces under four protocol generations, V4-Opus failure rate **{Xo}**/20 = **{Yo%}** (95% CP CI **[{Lo%}, {Ho%}]**) is strictly higher than V2-Opus failure rate {Xv2}/20 = {Yv2%} by **{D}pp** at point estimate (delta exceeds +10pp regression tolerance{; CI overlaps V2-Opus point estimate but PE direction is unambiguous if WIDE_CI also holds}). V4-Opus mechanism check: {V4-confirm/V4-partial/V4-falsify}. Per-failure mechanism: V4 prompt revision introduces failure modes V2-Opus did not exhibit. Mechanism diagnosis: V4's added explicit NO subclauses or extended YES enumeration cause over-correction (e.g., V4-Opus over-suppresses {test_v* trace IDs} because V4's NO-class additions catch compliant content that V2's enumeration correctly classified). Cross-prompt upgrade at the V4 design is empirically harmful for this workload at the Opus tier; M11c hierarchical routing is the remaining lever for the V2-prompt-mechanism residual. Critical finding: the V4 prompt revision designed from M11b D7-confirm + M11a test_v8 evidence is FALSIFIED as a deployment-ready intervention; V5 prompt revision must address V4's failure mechanism. Cross-tier-V4 consistency: {V4-Sonnet result vs V4-Opus delta; V4-Haiku result vs V4-Opus delta}."

### D9. Reviewer-vulnerable surfaces and pre-registered defenses

13 surfaces enumerated (Surface #13 added at D14-H9 hardening pass: cross-milestone Claude model alias drift between M11b and M11a-extension; M11a-extension is the first milestone in the series where the cross-milestone interval crosses an Anthropic published-rate rotation, raising the question of whether a same-alias model dispatch in 2026-05-15+ is bytewise the same as in 2026-05-13). Each has a pre-registered defense locked at Commit A.

1. **V4 post-hoc opportunism: "you designed V4 after seeing V2's residuals."** Defense: V4 designed from D7-confirm + test_v8 residuals that were pre-registered as future work at M10b/M11a/M11b BEFORE M11a-extension's data is written. Mechanism evidence (M11b D7-confirm 6/6 bytewise across 4 model implementations) constrains V4 design to a mechanism-targeted intervention, not opportunistic post-hoc tuning. V4 prompt text frozen verbatim at Commit A landing time.

2. **V4 prompt-tuning-on-residuals: "your V4 prompt is tuned on the specific event_ids that V2 failed."** Defense: residuals were pre-registered as future work at M10b §"Future work", M11a §"Future work" (runs/19 line 1872 — V2-prompt-inherited YES-bias finding), and M11b §"Future work" (runs/20 line 689). V4 design is constrained by THREE prior pre-registrations of the residual mechanism, not by post-hoc data inspection. V4 prompt text adds explicit NO subclauses for the distractor CLASSES (retail-back-in-stock, calendar-recurring-suggestion, casual-social-meetup), not for specific event_ids; V4 should generalize to NEW distractors of the same class authored at M11a-extension's Commit C.

3. **Cross-protocol caveat at 4 protocol generations: "M10 frozen → M10b frozen → M11a iterative → M11a-extension iterative is too many protocol revisions."** Defense: this is a feature, not a bug, of the cross-protocol robustness story. M10b was the protocol-frozen baseline; M11a's iterative-extension protocol structurally eliminated the literal-ID collision mode (0/9 vs M10b's 2/6 = 33%); M11a-extension's iterative-extension carries forward unchanged. The combined N=20 sample is honest about the protocol generations from which it draws and reports cross-protocol caveats verbatim per M11a defense #5. Cross-protocol findings that are stable across protocol generations are MORE robust than within-protocol findings.

4. **M11a-extension itself under-power risk at N=20: "what if N=20 is still underpowered to discriminate ±10pp deltas?"** Defense: Row 5 (UNDERPOWERED) is a pre-registered outcome with locked paper-line. M11a-extension-extension at N=40 is named as future work in §"Future work" — mirror M11b-extension naming pattern. Bootstrap CI sensitivity analysis at Commit D tests binomial-CI assumption.

5. **M11b cross-tier carry-forward bit-identical re-run at Commit B: "are M11b's V2-Sonnet/Haiku JSONs still bit-identical when re-run?"** Defense: belt-and-suspenders 10+10+10 re-run at Commit B with bit-identical PASS gate against M11b's `runs/data/20*-content-{opus,sonnet,haiku}-v2-*.json`. FAIL halts Commit B as explicit M11b-data-drift finding. Mirrors M11b's M11a-data-drift belt-and-suspenders gate.

6. **V4 mechanism could fix test_v12 but break test_v7-class compliant content: "false-positive risk."** Defense: explicit strict no-regression check (`COMPLIANT_NO_REGRESSION` predicate, D7; tightened to +0 tolerance at D14-H4) requires V4-Opus joint-bar failure count on traces other than {test_v8, test_v11, test_v12} ≤ V2-Opus failure count (zero tolerance — any non-flagged-subset regression at single-shot temperature=0 is real signal not noise). If COMPLIANT_NO_REGRESSION fails, Row 1 cannot fire — Row 3 fires instead. The reviewer's concern is encoded as a row-level gate.

7. **Prompt-cache differences across model families: "V4 vs V2 deltas could be cache-hit artifacts at single-shot per-event arbiter calls."** Defense: arbiter calls are single-shot per-event (~250-500 tokens); cache hits unlikely to materially affect per-call latency or per-call response. If drift smoke FAILs cache-attributably (Phase 2 vs Phase 3 differs at per-field level), characterize as operational note in Commit D; does not halt Row identification.

8. **V4 prompt was tuned on M11a/M11b residuals: "might over-fit to specific event_ids vs new fresh-session distractors."** Defense: M11a-extension's Commit C authoring step generates 10 NEW fresh-session-authored distractor traces under iterative-extension protocol. V4 must perform on these UNSEEN distractors at the combined-N=20 metric. If V4 only fixes the M10/M10b/M11a-known event_ids but fails on M11a-extension's new event_ids, Row 3 (PARTIAL SUCCESS — REDUCTION ONLY) fires due to MECHANISM_CONFIRM partial → over-fit-to-known-events flagged in paper-line.

9. **Cost-curve interpretation: "'cheaper per hit' is misleading if hit rates differ between V2 and V4."** Defense: Pareto table reports absolute $/hit + cost-per-hit-with-bounds; zero-hit cells excluded from cost-per-hit aggregate; matched-arbiter cost denominator (V4-tier vs V2-tier at same model + same arbiter) eliminates cheaper-arbiter attack.

10. **Underpowered at N=20 to distinguish ±5pp tier-deltas: "your CI at N=20 is still ~30pp wide."** Defense: ±10pp threshold is the pre-registered resolution, not ±5pp. Row 5 fires explicitly when CI width > 30pp AND PE in NEUTRAL band. M11a-extension-extension N=40 named for ±5pp resolution.

11. **Bootstrap CI assumes per-trace independence: "trace-level outcomes may correlate via shared distractor distributions."** Defense: bootstrap CI sensitivity analysis at Commit D (2000-resample non-parametric bootstrap; seed locked at Commit A as `BOOTSTRAP_SEED = 42`). If bootstrap CI differs from Clopper-Pearson by > 5pp at either bound, reported as Commit-D sensitivity observation. Reviewer-defense: "your CI assumes independent trials" → "we also report bootstrap CIs without that assumption; results [agree / differ at the {X}pp level]."

12. **Multiple comparisons: 6 outcome rows + V4 mechanism + cross-tier-V4 + drift smoke + Pareto = fishing.** Defense: primary outcome mechanically determined by D7 row identification (1 of 6 rows; first-match-wins precedence). Secondary outcomes mechanically determined by V4-mechanism diagnostic (1 of 3 branches) + cross-tier-V4 diagnostic (1 of 3 branches). Observational components (drift smoke, Pareto cost ratios) reported for transparency but not claimed as primary outcomes. Total reported metric count = 1 row + 2 diagnostic branches = 3 testable outcomes per pre-reg, not 18+ cell combinations.

13. **Cross-milestone Claude model alias drift between M11b and M11a-extension: "V4-Opus vs V2-Opus deltas at M11a-extension could reflect Anthropic-side `claude-opus-4-7` alias rotation between M11b Commit D (2026-05-15) and M11a-extension Commit D, not the V4 prompt mechanism."** Added at D14-H9 hardening pass. Defense: two-layer triangulation. (Layer 1 — cross-milestone) Commit B belt-and-suspenders bit-identical V2 re-run gates V2-Opus + V2-Sonnet + V2-Haiku against M11b's `runs/data/20*-content-{opus,sonnet,haiku}-v2-*.json` (Surface #5). PASS = no cross-milestone alias drift between M11b Commit D and M11a-extension Commit B. FAIL halts Commit B as explicit M11b-data-drift finding (mirrors M11b's M11a-data-drift halt pattern). (Layer 2 — within-milestone) Triangulated drift smoke at Phase 2 + Phase 3 (§D12) bit-compares V4-Sonnet + V4-Haiku across the Commit B → Commit D-start → Commit D-end execution window. PASS = no within-milestone drift during V4 harness execution. If Layer 1 PASS but Layer 2 FAIL, V4-vs-V2 delta is reported with the within-milestone-drift caveat. If Layer 1 FAIL, V4 vs V2 delta cannot be attributed to V4 mechanism because the cross-milestone V2 baseline itself has drifted. Reviewer-defense: "we mechanically separate cross-milestone Claude alias drift (Layer 1) from within-milestone harness-execution drift (Layer 2); each has its own halt-gate or caveat-tag."

### D10. Cost framework + budget

**Per-cell unit-cost estimates (M11b actuals as lower bound):**

| Component | Cells | Est. cost |
|---|---|---|
| **V4 harness — primary** | | |
| V4-Opus N=20 (M10/M10b/M11a carry-forward + M11a-extension new) | 20 | $0.45 |
| V4-Sonnet N=20 (matched) | 20 | $0.22 |
| V4-Haiku N=20 (matched) | 20 | $0.07 |
| **V4 harness — sensitivity** | | |
| V4-Opus N=10 M11a-extension-alone (subset of above; no extra cost) | 0 | $0 |
| **Belt-and-suspenders V2 carry-forward re-run** | | |
| V2-Opus N=20 (vs M10/M10b/M11a/M11b JSONs; bit-identical gate) | 20 | $0.45 |
| V2-Sonnet N=10 (vs M11b JSONs; bit-identical gate) | 10 | $0.11 |
| V2-Haiku N=10 (vs M11b JSONs; bit-identical gate) | 10 | $0.035 |
| **Drift smoke (triangulated 3-phase)** | | |
| Opus carryover Phase 1 (vs `17b-*`; PASS gate) | 3 | $0.15 |
| Sonnet baseline Phase 1 + Phase 2 + Phase 3 | 9 | $0.045 |
| Haiku baseline Phase 1 + Phase 2 + Phase 3 | 9 | $0.0135 |
| **Fresh-session trace authoring (Commit C)** | | |
| ~15 fresh-session attempts × ~$0.05 each (Sonnet 4.6 author) | 15 | $0.75 |
| Self-restate pre-flight gate API calls (~30 extra calls) | — | $0.05 |
| **Pricing attestation fetch (Commit A)** | | |
| Anthropic pricing page fetch + extraction | 1 | $0.01 |
| **TOTAL (~117 cells)** | | **~$2.36** |

**Pre-reg budget: $4 with 70% safety margin** (M11a's $5.10 actual / $5-6 pre-reg precedent; M11b's $3.05 estimate). User-stated headline target: total spend ≤ $10. Recommended budget ($4) is comfortably under. **Cross-tier V4 coverage selected; budget allows.**

### D11. Pricing attestation refresh

**Recommended:** Re-execute the §D11 HARD GATE at Commit A. Confirm M11b's cross-milestone-locked rates ($15/$75 Opus per M10 lock; $3/$15 Sonnet; $1/$5 Haiku per M11b 2026-05-13 attestation) are still the right reference choice for M11a-extension internal cost modeling, **OR** pivot to current-published rates with a clean argument.

**Recommended decision (locked at Commit A based on fresh fetch):** Continue M10-locked Opus rate ($15/$75) for M11a-extension internal cost modeling to preserve cross-milestone consistency with M10/M10b/M11a/M11b cost numbers in runs/17,18,19,20. Document any observed-published-rate drift in `runs/data/21a-pricing-attestation-{YYYY-MM-DD}.json` `notes` field. The cross-milestone-consistency defense ages at each milestone; at M11a-extension this is a fresh decision because the M11b-published Opus rate already shows ~3× re-pricing vs the M10 lock (per `20a-pricing-attestation-2026-05-13.json` notes). Argue: M11a-extension is the FINAL empirical milestone before paper drafting; preserving M10 lock through paper-line cost numbers maintains internal consistency through the whole milestone series. Paper appendix can document the observed-published-rate divergence as a deployment-cost-projection caveat.

**HARD GATE at Commit A (mirror M11b §D4):**
1. Fetch current Anthropic pricing page (anthropic.com/pricing or canonical equivalent).
2. Extract input + output per-million-token rates for `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`.
3. Verify Opus 4.7, Sonnet 4.6, Haiku 4.5 rates against M11b's archived attestation. If any rate has rotated, document as Commit-A finding but **do not re-price** for internal cost modeling (M10 lock + M11b lock hold).
4. Archive fetched content as `runs/data/21a-pricing-attestation-{YYYY-MM-DD}.json` with same JSON schema as `20a-*` attestation: `fetched_at`, `source_url`, `corroborating_source_url`, `rates_per_million_tokens`, `m11a_extension_internal_cost_modeling_rates_per_million_tokens`, `raw_text_excerpt`, `notes`.
5. If verified rates differ from internal-cost-modeling rates, recompute D10 budget estimate and update `notes` field with delta.

### D12. Triangulated drift smoke

**Recommended:** Mirror M11b §D3 verbatim — 18 cells (Phase 1 baseline + Phase 2 pre + Phase 3 post × 3 tiers).

**Phase 1 — Commit B (pre-harness):**
- Opus carryover PASS gate (3 cells): V4-Opus on dev_v2/test_v1/test_v2; bit-identical compare against `runs/data/17b-content-opus-v2-*.json` after V4-prompt-routing verification step. **Note:** the bit-identical compare is against V2-Opus (not V4-Opus) — purpose is to verify the V4 prompt revision did not disturb the V2 code path. PASS = V2 path bit-identical to M10/M10b/M11a/M11b across the V4 code wiring delta. **FAIL halts Commit B**. Cost ~$0.15.
- Sonnet baseline (3 cells): V4-Sonnet on dev_v2/test_v1/test_v2; stored as `runs/data/21b-baseline-content-sonnet-v4-{dev_v2,test_v1,test_v2}.json`. Reference for Phase 2 + Phase 3.
- Haiku baseline (3 cells): V4-Haiku on dev_v2/test_v1/test_v2; stored as `runs/data/21b-baseline-content-haiku-v4-{dev_v2,test_v1,test_v2}.json`. Same role.

**Phase 2 — Commit D (pre-harness, immediately before the V4 N=20×3-tier harness fires):**
- Sonnet pre-harness smoke (3 cells): re-run V4-Sonnet on dev_v2/test_v1/test_v2; bit-compare against Phase 1 Sonnet baseline. PASS = V4-Sonnet stable across Commit-B → Commit-D-start delta.
- Haiku pre-harness smoke (3 cells): same for V4-Haiku.

**Phase 3 — Commit D (post-harness, immediately after the harness completes):**
- Sonnet post-harness smoke (3 cells): re-run V4-Sonnet; bit-compare against Phase 1 Sonnet baseline (and against Phase 2 for within-harness-window stability). PASS = V4-Sonnet stable across the entire Commit D harness execution window.
- Haiku post-harness smoke (3 cells): same for V4-Haiku.

**Drift-smoke verdict policy (mirror M11b lines 83-87):** Opus carryover (Phase 1): PASS gate; FAIL halts Commit B. Sonnet + Haiku Phase 2 + Phase 3: observational, NOT halt-gate. PASS = within-milestone V4 determinism verified empirically across B → D-start → D-end. FAIL = drift observed; record per-field deltas (arbiter_calls / yes_rate / input_tok / output_tok / dispatched_model / hit / false_h) as M11a-extension empirical finding; does not halt Commit D.

### D13. Four-commit M10-shape protocol

**Recommended:** A pre-reg + pricing → B code wiring + drift baselines + belt-and-suspenders + self-restate code → **C fresh-session trace authoring** → D harness + analysis. Mirror M11b verbatim with Commit C inserted for the trace-authoring step (M11b had no Commit C because it didn't author new traces).

| Commit | Content | Gates |
|---|---|---|
| **A** | (1) Pricing verification per §D11 (fetch + archive `runs/data/21a-pricing-attestation-{date}.json`; update Sonnet/Haiku rate placeholders if needed). (2) Pre-reg copy of this plan to `runs/21-v4-prompt-n20-extension.md` with appropriate header / date / pre-reg SHA placeholders + final-verified-rates + 6-row paper-line + 3-branch V4-mechanism paper-line + 3-branch cross-tier-V4 paper-line all locked verbatim. (3) `sandbox/event_trace.py`, `agent/`, `baselines/`, `eval/`, `pyproject.toml`, `uv.lock` — NOT touched at Commit A. | Pricing attestation archived + committed. |
| **B** | (1) `agent/arbiter.py`: add `ARBITER_SYSTEM_PROMPT_V4` constant verbatim per D1 lock. Estimated ~30 LOC for the prompt text + ~5 LOC for the prompt routing. (2) `eval/run_trace.py`: extend `--arbiter-system-prompt` CLI choices `{v2, v3}` → `{v2, v3, v4}` and update `_load_agent` mapping. ~10 LOC. (3) Self-restate pre-flight gate code per D4 (~20 LOC) at **`eval/author_trace.py` (NEW, locked at D14-H7)**. (4) 3-cell V2-Opus drift smoke vs `17b-*` (PASS gate; verifies V4 wiring did not disturb V2 path). (5) 3-cell V4-Sonnet baseline + 3-cell V4-Haiku baseline stored as `21b-baseline-*.json`. (6) Belt-and-suspenders re-run: 10-cell V2-Opus on combined-N=10 (M10/M10b/M11a; the M11a-extension new traces do not exist yet at Commit B, so the belt-and-suspenders scope is the N=10 sample that DOES exist at Commit B time) + 10-cell V2-Sonnet + 10-cell V2-Haiku, all bit-compared against M11b's `20*-content-{opus,sonnet,haiku}-v2-*.json` (PASS gate). | (4) PASS = bit-identical Opus carryover vs `17b-*` (V4 wiring did not disturb V2). (6) PASS = M11b `20*-*` JSONs verified bit-identical against fresh re-runs. Commit B total spend ≈ $0.65. |
| **C** | (1) Fresh-session-authored trace authoring per M11a iterative-extension protocol with self-restate pre-flight gate (per D4; helper at `eval/author_trace.py`). (2) Iterate until 10 accepted traces authored under audit-gate (acceptance rate ~56% per M11a; expect 12-18 fresh sessions). (3) New traces named **`test_v21..test_v30` (locked at D14-H8; preserves chronological ordering across milestones; v9/v10 gap remains as transparent historical artifact)**. (4) Each accepted trace committed with a separate transparent commit including the self-restate response artifact + audit-gate PASS log. (5) Banned-list extension carries forward at each acceptance per M11a iterative-extension protocol. | Audit-gate PASS for each accepted trace. Banned-list saturation halt-condition (defense #4): if after 25 fresh-session attempts < 10 traces are accepted, milestone halts pending banned-list-protocol revision (out-of-scope for this pre-reg; would be M11a-extension-revision). |
| **D** | (1) Phase 2 V4-Sonnet + V4-Haiku drift smoke (6 cells; pre-harness; bit-compare against Phase 1 baselines). (2) V4 N=20×3-tier harness matrix per §D2 cell table (60 cells total: V4-Opus 20 + V4-Sonnet 20 + V4-Haiku 20). (3) Phase 3 V4-Sonnet + V4-Haiku drift smoke (6 cells; post-harness; bit-compare against Phase 1 baselines + Phase 2). (4) Aggregate analysis: per-trace observations + per-tier failure-rate metrics + Pareto cost ratios + Clopper-Pearson CI + bootstrap CI sensitivity per scope + DELTA_PE/MECHANISM/COMPLIANT_NO_REGRESSION predicate computation + outcome row identification (D7) + V4-mechanism branch identification + cross-tier-V4 branch identification. (5) `runs/21-v4-prompt-n20-extension.md` results appendix + row 21 in `runs/README.md` + paper framing line update for M11a-extension's outcome row at combined-N=20 scope. | Verbatim eval against frozen D7 predicates. Sonnet/Haiku Phase 2 + Phase 3 drift smoke results reported but not halt-gated (paper-line item per §D12). |

**Pre-Commit-D fix discipline (carries forward from M11b):** Any bug surfaced during execution gets a separate transparent commit with bit-identical preservation proof (mirror M11b `b78554d` — react_poll_claude dedupe fix preserving bit-identical V2 path).

**Aggregation-error-correction discipline (carries forward from M11b):** Any prior-milestone aggregation error surfaced during M11a-extension Commit D analysis gets a separate transparent correction commit (mirror M11b `c0c6099` — V2-Opus combined-N=10 2/10 → 3/10 strict-joint-bar correction).

### D14. Pre-data hardening discipline

**Recommended:** Schedule one honest hardening pass between Plan-drafted and Commit-A-landed. Don't pre-commit to zero edits; surface anything that needs polish in a separate session before Commit A.

**Defense:** M11a landed 13 pre-Commit-A hardening edits to its source plan; M11b landed 0. The variance is expected — some plans converge in one pass, others surface issues during walkthrough. Plan for the possibility, don't presume.

**Walkthrough trigger for hardening pass:** before Commit A landing, the user opens this plan in a fresh session, walks through D1-D14 + the row table + the locked paper-lines + the reviewer-vulnerable-surfaces enumeration ONE MORE TIME with adversarial-reviewer mindset. Anything surfaced gets edited into the plan (still in `~/.claude/plans/m11a-extension-v4-prompt-n20.md` location). Then Commit A copies the plan verbatim to `runs/21-v4-prompt-n20-extension.md`.

---

## V4-mechanism diagnostic (3-branch; pre-registered with locked paper-lines)

The V4-mechanism diagnostic asks: did V4-Opus correct the 5 pre-registered V2-Opus failure events at the cell level? Three branches:

- **V4-confirm:** strict 5/5 of {`trivia_league_round`, `grocer_back_in_stock`, `calendar_yoga_suggest`, `mom_birthday_heads_up`, `bridgers_presale_window`} corrected vs V2-Opus baseline (tightened at D14-H3 to match V4's 1:1 clause-to-event design; deterministic single-shot inference makes any miss a clause-level mechanism failure). Mechanism intervention fully validated at cell level.
- **V4-partial:** 1-4/5 of the 5 flagged events corrected.
- **V4-falsify:** 0/5 corrected (V4-Opus bytewise-identical to V2-Opus on all 5).

**Locked paper-line per branch:**

**V4-confirm:**
> "V4 prompt revision corrects all 5/5 M11b D7-confirm + M11a test_v8 flagged events at V2-Opus baseline (strict 5/5 threshold met per D14-H3). V4-Opus surfaces 0/3 of {trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest} at test_v11+test_v12 cells (V2-Opus surfaced all 3 bytewise per M11b D7-confirm); V4-Opus correctly YES-classifies {mom_birthday_heads_up, bridgers_presale_window} at test_v8 cell (V2-Opus failed both per M11a Row 4a). The mechanism intervention (V4 prompt revision adding explicit NO subclauses for the three D7-confirm distractor classes + extended YES enumeration for discretionary-deadline obligations) is fully validated at the cell level. The V2-prompt-mechanism residual class closes at the cell level under V4 prompt revision; whether overall failure rate also closes is determined by §\"Outcome row table\" Row 1 vs Row 2 vs Row 3 identification."

**V4-partial:**
> "V4 prompt revision corrects {m of 5} of the 5 M11b D7-confirm + M11a test_v8 flagged events at V2-Opus baseline (1≤m≤4; strict 5/5 V4-confirm threshold per D14-H3 not met). Cell-level breakdown: {per-event corrected/uncorrected list with verbatim event_id and YES/NO outcomes for V4-Opus vs V2-Opus}. Mechanism intervention is partially validated: {distractor class addressed; distractor class not addressed} of the V4 prompt revision's three explicit-NO subclauses or extended-YES-enumeration clause are load-bearing. Mechanism diagnosis: {analysis of WHICH V4 prompt clause failed to fix WHICH event_id and WHY based on event content}. V5 prompt revision should refine the failed clauses while retaining the successful ones."

**V4-falsify:**
> "V4 prompt revision fails to correct ANY of the 5 M11b D7-confirm + M11a test_v8 flagged events at V2-Opus baseline (0/5; V4-Opus bytewise-identical to V2-Opus on all 5 flagged cells). The V2-prompt-mechanism residual class is robust to the targeted V4 prompt revision at the cell level. Mechanism diagnosis: V4's added explicit NO subclauses + extended YES enumeration are not load-bearing for the model's classification on the flagged events; the model's V2-baseline classifications are not driven by the V2 prompt's enumeration of YES/NO classes but by some other prompt feature (e.g., the {message or delivery directed personally to the user} clause matching back-in-stock content via implicit personalization, regardless of V4's added NO subclause). M11c hierarchical routing or non-prompt mechanism interventions are the remaining lever. Reviewer-defense: V4-falsify on N=5 flagged cells is a substantively important falsification of the prompt-revision-as-fix hypothesis at the Opus tier; cross-tier-V4 diagnostic determines whether falsification is tier-specific or tier-uniform."

---

## Cross-tier-V4 consistency diagnostic (3-branch; pre-registered with locked paper-lines)

The cross-tier-V4 diagnostic asks: does V4 mechanism behavior reproduce bytewise across {Opus, Sonnet, Haiku} the way V2 mechanism behavior did at M11b D7-confirm?

- **CT-V4-confirm:** V4-Sonnet AND V4-Haiku surface the SAME set of M11b/M11a-flagged events as V4-Opus does (bytewise-identical mechanism response across tier).
- **CT-V4-partial:** V4-Sonnet OR V4-Haiku differs from V4-Opus on at least one flagged event but not all.
- **CT-V4-falsify:** V4-Sonnet AND V4-Haiku both differ from V4-Opus on ALL 5 flagged events (mechanism response is fully tier-dependent; V4 effect at Opus does not generalize).

**Locked paper-line per branch:**

**CT-V4-confirm:**
> "V4-Sonnet AND V4-Haiku reproduce V4-Opus's mechanism response bytewise across the 5 M11b/M11a-flagged events. Cross-tier-V4 mechanism is V4-prompt-inherent across the Claude family the way V2-prompt mechanism was at M11b D7-confirm 6/6. The V4 prompt revision's mechanism effect is tier-stable; V4 deployment can collapse to the cheapest tier (Haiku) without quality penalty at the mechanism cells. Cross-tier symmetric to M11b D7-confirm with V4 substituted for V2."

**CT-V4-partial:**
> "V4-Sonnet OR V4-Haiku differs from V4-Opus on at least one M11b/M11a-flagged event but not all 5. Per-tier per-event breakdown: {V4-Sonnet correct/incorrect per flagged event; V4-Haiku correct/incorrect per flagged event}. V4 prompt revision's mechanism effect is partially tier-dependent: {clause class} addressed uniformly across tiers; {clause class} addressed at {tier subset} only. Mechanism diagnosis: {analysis of which V4 prompt clause requires Opus-scale capability vs which generalizes across tier}. Tier-graded V4 deployment: {tier} is the lower-bound deployable tier with V4 mechanism guarantees; below {tier} requires V5 or hierarchical-routing fallback to {next-up tier}."

**CT-V4-falsify:**
> "V4-Sonnet AND V4-Haiku BOTH differ from V4-Opus on ALL 5 M11b/M11a-flagged events. V4 prompt revision's mechanism effect is fully tier-dependent: V4 effect at Opus does not generalize to Sonnet or Haiku. The V4 prompt addition requires Opus-scale capability to correctly read the explicit NO subclauses + extended YES enumeration. Mechanism diagnosis: V4 prompt is too long or too nuanced for sub-Opus tiers; V5 prompt should be either (a) shorter / less nuanced for cross-tier deployment, or (b) accepted as Opus-only with M11c hierarchical-routing for sub-Opus tiers reverting to V2 + arbiter-escalation. Cross-tier asymmetric to M11b D7-confirm: V2 prompt mechanism was tier-stable, V4 prompt mechanism is not."

---

## Pre-registered analysis (Commit D)

1. **Per-trace observations:** for each trace (combined N=20 × 3 tiers = 60 cells), report joint-bar metric (hit, false/h), arbiter call counts, V4-vs-V2 deltas at the per-event level for the 5 flagged cells.

2. **Per-tier failure-rate metrics:** V4-Opus combined-N=20 failure rate; V4-Sonnet combined-N=20 failure rate; V4-Haiku combined-N=20 failure rate; and matched V2-* baselines from M11b carry-forward.

3. **Pareto cost ratios:** matched-arbiter $/hit at each tier × prompt cell; cross-tier and cross-prompt ratios.

4. **CI computation:** Clopper-Pearson 95% CI for each per-tier failure rate at combined N=20 + N=10 sensitivity scope. Bootstrap CI sensitivity (2000-resample non-parametric; `BOOTSTRAP_SEED = 42` locked at Commit A) reported alongside.

5. **Predicate computation:** mechanically compute DELTA_PE, IMPROVEMENT/NEUTRAL/REGRESSION, WIDE_CI, MECHANISM_CONFIRM/PARTIAL/FALSIFY, COMPLIANT_NO_REGRESSION per D7 definitions.

6. **Outcome row identification:** apply first-match-wins precedence rule from D7 to identify exactly one row.

7. **V4-mechanism diagnostic branch identification:** apply 3-branch rule.

8. **Cross-tier-V4 diagnostic branch identification:** apply 3-branch rule.

9. **Drift smoke verdict:** Phase 2 + Phase 3 vs Phase 1 baseline bit-comparison per tier.

10. **Belt-and-suspenders verdict:** Commit-B re-run vs M11b `20*-*` JSONs bit-comparison verdict.

11. **Paper-line filling:** mechanically fill integer placeholders in identified row's locked paper-line + identified diagnostic branches' locked paper-lines.

---

## Critical files

**Modified at Commit A:**
- `runs/21-v4-prompt-n20-extension.md` (NEW — pre-reg copy of this plan)
- `runs/data/21a-pricing-attestation-{YYYY-MM-DD}.json` (NEW — fresh attestation)

**Modified at Commit B:**
- `agent/arbiter.py` (add `ARBITER_SYSTEM_PROMPT_V4` constant ~30 LOC; add v4 routing ~5 LOC)
- `eval/run_trace.py` (extend `--arbiter-system-prompt` choices; ~10 LOC)
- `eval/author_trace.py` (NEW — self-restate pre-flight gate helper; ~20 LOC; locked at D14-H7)
- `runs/data/17b-content-opus-v2-*.json` (READ; bit-compare reference for Opus carryover)
- `runs/data/20*-content-{opus,sonnet,haiku}-v2-*.json` (READ; bit-compare reference for belt-and-suspenders)
- `runs/data/21b-baseline-content-{sonnet,haiku}-v4-*.json` (NEW — Phase 1 baselines)

**Modified at Commit C:**
- `sandbox/event_trace.py` (NEW trace definitions `test_v21..test_v30`, locked at D14-H8; ~250-400 LOC additions)
- Per-trace audit-gate PASS log + self-restate response artifact files (location set at Commit B alongside `eval/author_trace.py`; suggested `runs/data/21c-author-{test_v??}-{attempt,accepted}.json` for transcripts)

**Modified at Commit D:**
- `runs/data/21d-content-{opus,sonnet,haiku}-v4-test_v*-*.json` (NEW — V4 harness output; 60 files)
- `runs/data/21d-drift-{sonnet,haiku}-v4-{phase2,phase3}-{dev_v2,test_v1,test_v2}.json` (NEW — drift smoke; 12 files)
- `runs/21-v4-prompt-n20-extension.md` (UPDATE — Commit D Results appendix appended)
- `runs/README.md` (UPDATE — row 21 entry)

**NOT touched at any commit (frozen):** `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`. `sandbox/event_trace.py` test_v4..test_v15 definitions are committed reference (only NEW trace definitions are added at Commit C).

---

## Verification

**Pre-Commit-B smoke (Commit-B step 4):** 3-cell V2-Opus on dev_v2/test_v1/test_v2 vs `runs/data/17b-content-opus-v2-*.json`; bit-identical PASS = V4 wiring did not disturb V2 path.

**Commit-B belt-and-suspenders (Commit-B step 6):** 30 cells (V2-Opus + V2-Sonnet + V2-Haiku × N=10 each) vs M11b `20*-*` JSONs; bit-identical PASS = M11b data still reproducible at HEAD M11a-extension Commit B.

**Commit-B baselines (Commit-B step 5):** 6 V4 baseline cells stored as `21b-baseline-*.json` for Phase 2 + Phase 3 drift smoke reference.

**Commit-D phases:**
- Phase 2 (pre-harness): 6 V4 cells bit-compared against Phase 1 baselines.
- Harness: 60 V4 cells (N=20 × 3 tiers).
- Phase 3 (post-harness): 6 V4 cells bit-compared against Phase 1 + Phase 2.
- Aggregate analysis per §"Pre-registered analysis".

---

## Non-goals

1. **Surprise-gate auto-surf bypass fix (test_v4 mechanism per D6).** Different mechanism class; named M11d-surprise-gate-retuning as future work.
2. **Cross-vendor V4 sweep (GPT / Gemini / Llama).** Out-of-scope; M11d-cross-vendor named as future work.
3. **V5 prompt revision design.** Single-shot pre-reg per D5; V5 (if needed based on Row 6 BACKFIRE or Row 4 NO IMPROVEMENT outcome) is a separate future milestone.
4. **N=40+ scope.** M11a-extension-extension named for tightened CI resolution.
5. **Hierarchical-routing deployment shape.** M11c is the named milestone for routing experiments.
6. **External-reviewer audit of V4 prompt design.** Internal pre-reg only; external review happens at paper-draft stage.

---

## Future work (named residuals deferred from this milestone)

1. **M11a-extension-extension** — N=40+ scope for ±5pp CI resolution. Triggered if Row 5 (UNDERPOWERED) fires at M11a-extension.
2. **M11d-surprise-gate-retuning** — addresses test_v4 V2-Opus surprise-gate auto-surf bypass residual (M11a Row 4a per runs/19 line 1854 mechanism (c)). Different mechanism class; out-of-scope for V4 prompt.
3. **M11d-cross-vendor** — V4 + V2 sweep at GPT-4-class / Gemini-1.5-Pro-class / Llama-3.1-70B-class for cross-vendor robustness.
4. **M11c-hierarchical-routing** — 3B-local → Sonnet/Opus escalation deployment shape.
5. **V5 prompt revision** (conditional on M11a-extension Row 4 / Row 6 outcome) — separate future milestone with own pre-reg.
6. **Paper drafting** — first paper draft from M8b + M10 + M10b + M11a + M11b + M11a-extension closure.

---

## Walkthrough kickoff

**Pre-Commit-A convergence checklist:**

1. ✅ User reads Plan-drafted output; surfaces objections to D1-D14 recommendations.
2. ✅ User and assistant converged on D1-D14 decisions (no AskUserQuestion escalations needed).
3. ✅ Plan locked at `~/.claude/plans/m11a-extension-v4-prompt-n20.md` as locked source (prior plan-mode session).
4. ✅ D14 hardening pass complete (2026-05-15 fresh session): H1-H10 audit; 7 substantive edits landed (H1/H2/H3/H4/H7/H8/H9); H5/H6/H10 confirmed no-edit.
5. ⏳ Commit A landing: pricing fetch → archive → pre-reg copy from locked plan to `runs/21-v4-prompt-n20-extension.md`.

**State to confirm at Commit A kickoff (next session):**
- main HEAD at 2d79690 (M11b Commit D); working tree clean
- Pricing attestation re-executed; `21a-pricing-attestation-{YYYY-MM-DD}.json` archived
- Plan landed at `~/.claude/plans/m11a-extension-v4-prompt-n20.md`
- D14 hardening pass complete

---

## Appendix: M11b → M11a-extension carry-forward summary

| M11b artifact | M11a-extension role |
|---|---|
| V2-Opus + V2-Sonnet + V2-Haiku N=10 JSONs (`runs/data/20*-content-*-v2-*.json`) | Belt-and-suspenders bit-identical re-run reference (Commit B) + V2 baseline carry-forward for combined N=20 |
| `runs/data/17b-content-opus-v2-*.json` | Opus carryover bit-identical reference (Commit B Phase 1) |
| Pricing attestation `runs/data/20a-pricing-attestation-2026-05-13.json` | Cross-milestone-locked rate reference (D11) |
| `agent/arbiter.py` rate table + `_rates_for` helper | Inherited unchanged; V4 prompt added as additional constant |
| `--arbiter-system-prompt {v2,v3}` CLI choice | Extended to `{v2,v3,v4}` at Commit B |
| `--arbiter-model {opus,sonnet,haiku}` CLI choice | Inherited unchanged |
| `react_poll_claude` dedupe fix (`b78554d`) | Inherited unchanged |
| M11b cross-tier carry-forward bit-identical pattern | Mirrored as M11a-extension belt-and-suspenders |
| M11b 18-cell triangulated drift smoke | Mirrored verbatim (D12) |
| M11b 6-row outcome paper-line lock template | Mirrored with V4-vs-V2 row predicates (D7-D8) |
| M11b 12-surface reviewer-vulnerable enumeration | Mirrored + 3 M11a-extension-specific additions (D9.1, D9.2, D9.6 = post-hoc opportunism + prompt-tuning + false-positive risk) + D14-H9 addition (D9.13 = cross-milestone Claude alias drift) → 13 surfaces total |
| M11b cost framework | Mirrored with V4 cells substituted (D10) |
| M11b 3-commit M10-shape protocol | Extended to 4-commit with Commit C trace authoring inserted (D13) |
| M11b transparent-bug-fix discipline (`b78554d`) | Carries forward (D13) |
| M11b transparent-correction-commit discipline (`c0c6099`) | Carries forward (D13) |

---

## Commit B Results — V4 prompt wiring + drift baselines + belt-and-suspenders

**Commit B date:** 2026-05-15 (M11a-extension Commit B landing). Per pre-reg §D13 Commit B scope: code wiring (~50 LOC across 3 files; ~30 prompt + ~5 routing in `agent/arbiter.py`, ~10 in `eval/run_trace.py`, ~25 NEW in `eval/author_trace.py`) + Opus carryover PASS gate vs `17b-*` + V4-Sonnet/Haiku Phase 1 baselines + 30-cell V2 cross-milestone belt-and-suspenders PASS gate per §D9 Surface #5 + §D9 Surface #13. No fresh-session trace authoring at Commit B; that is Commit C scope per the four-commit M10-shape protocol (§D13).

**Pre-Commit-B SHA backfill (Phase 0 of this session per §D13 + M11b a782fc0 / M11a 7c24d08 / M10b 629e0e4 precedent):** `15484b6` — replaced two SHA placeholders (`{filled at this commit by post-commit doc-completeness backfill}` in this file header line 4 + `{filled at this commit}` in `runs/README.md` row 21) with literal `b1d2521` (Commit A SHA). Mirrors M11b's a782fc0 single-file SHA-backfill discipline; no-amend invariant preserved (amending Commit A would invalidate `b1d2521`).

### (1) `agent/arbiter.py` — `ARBITER_SYSTEM_PROMPT_V4` constant added per §D1 verbatim lock

Inserted between `ARBITER_SYSTEM_PROMPT_V3` (line 126 closing paren) and `_DECISION` regex (now line ~145) at the structural position mirroring V3's. **Bytewise-verified** against the locked plan §D1 Python-literal block at `~/.claude/plans/m11a-extension-v4-prompt-n20.md` lines 51-89: **sha256 = `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6`** (1851 bytes). Match: True. Any future revision to the V4 prompt text happens at the locked-plan path and back-propagates here per §D13 pre-Commit-D fix discipline.

V4 design summary (per §D1 construction principles 1-4): retains V2's six closed-enumeration YES classes + four NO classes verbatim; adds a seventh YES class for *discretionary-deadline obligations* (family milestones with social cost OR scarcity-bounded opportunities under one hour) targeting the M11a test_v8 V2-enumeration limit; adds three explicit NO subclauses with one canonical example each (back-in-stock without scarcity window; recurring-event calendar suggestion; casual social-meetup without time-pressure) — each subclause maps 1:1 to one M11b D7-confirm distractor class. Output format unchanged (`YES` or `NO` uppercase, single line). Chat-template wire-up (`system=rules, user=event_content`) bytewise identical to V2/V3 per M9 wire-up choice (a).

### (2) `eval/run_trace.py` — `--arbiter-system-prompt {v2,v3,v4}` CLI routing

Extended argparse choices `{v2,v3}` → `{v2,v3,v4}`; `_load_agent` claude-mode dispatch routes `v4` → `ARBITER_SYSTEM_PROMPT_V4` via explicit if/elif/else chain (mirrors V3 routing pattern). Verified at CLI help: `--arbiter-system-prompt {v2,v3,v4}` surfaces.

### (3) `eval/author_trace.py` (NEW) — self-restate pre-flight gate per §D4 + D14-H7

~25 LOC at `eval/author_trace.py`. Module entry point: `python -m eval.author_trace --banned-list <path>`. Emits the locked §D4 self-restate prompt verbatim with the iteratively-extended banned list inlined; fresh-session authoring sessions read the emitted text, restate constraints (a)-(d) in their own words BEFORE authoring, and persist the restate response as a Commit C audit artifact alongside the authored trace. Targets the M11a structural-parsing-failure rate of 3/9 = 33% (runs/19 attempts log) at the M11a-extension N=10-fresh target. Smoke-tested at Commit B with a synthetic 2-line banned list: prompt + banned-list contents emit cleanly.

### (4) 3-cell V2-Opus carryover smoke vs `runs/data/17b-content-opus-v2-*.json` — **PASS gate**

V2-Opus on `{dev_v2, test_v1, test_v2}` after V4 wiring; per-field bit-compare on M11b-precedent 7 load-bearing fields (`hit_rate`, `false_initiation_rate_per_hour`, `arbiter_calls`, `arbiter_yes_rate`, `arbiter_input_tokens`, `arbiter_output_tokens`, `arbiter_dispatched_model`). Output JSONs: `runs/data/21b-smoke-content-opus-v2-{dev_v2,test_v1,test_v2}.json`.

| Trace | hit_rate | false/h | arbiter_calls | yes_rate | in_tok | out_tok | dispatched_model | Verdict |
|---|---|---|---|---|---|---|---|---|
| dev_v2 | 1.0 | 0.0 | 4 | 0.75 | 1854 | 8 | `claude-opus-4-7` | PASS (7/7 bit-identical) |
| test_v1 | 1.0 | 3.6735 | 8 | 0.625 | 3677 | 16 | `claude-opus-4-7` | PASS (7/7 bit-identical) |
| test_v2 | 1.0 | 0.0 | 7 | 0.4286 | 3208 | 14 | `claude-opus-4-7` | PASS (7/7 bit-identical) |

**Verdict: 3/3 PASS** — V4 wiring did NOT disturb the V2 path. Opus 4.7 alias additionally stable across M10 (2026-04-27) → M11a (2026-05-08-13) → M11b (2026-05-13-15) → M11a-extension Commit B (2026-05-15) over 18 days at the V2 code path.

### (5) V4-Sonnet + V4-Haiku Phase 1 baselines (observational; §D12 Phase 1)

3-cell V4-Sonnet + 3-cell V4-Haiku on `{dev_v2, test_v1, test_v2}` archived as Phase 1 reference for Commit D Phase 2 + Phase 3 within-milestone drift smoke (§D12 triangulated B → D-start → D-end). No bit-compare gate at Commit B (no prior reference; V4 is new). Output JSONs: `runs/data/21b-baseline-content-{sonnet,haiku}-v4-{dev_v2,test_v1,test_v2}.json` (6 files). `arbiter_dispatched_model` verified per cell: Sonnet returns `claude-sonnet-4-6` (alias); Haiku returns `claude-haiku-4-5-20251001` (dated suffix per `_rates_for` substring dispatch per M11b §D6).

### (6) 30-cell V2 cross-milestone belt-and-suspenders — **PASS gate per §D9 Surface #5 + Surface #13**

V2-Opus + V2-Sonnet + V2-Haiku re-runs on the combined-N=10 sample existing at Commit B time (M10 `test_v4` + M10 `test_v5` + M10b `test_v6/v7/v8` + M11a `test_v11..v15`); per-field bit-compare on the 7 load-bearing fields vs cross-milestone references:

| Tier | Reference JSONs | Cells | PASS |
|---|---|---|---|
| V2-Opus | M10 `17b-content-opus-v2-test_v4` + M10 `17d-content-opus-v2-test_v5` + M10b `18d-content-opus-v2-test_v{6,7,8}` + M11a `19d-content-opus-v2-test_v{11..15}` | 10 | **10/10 PASS** |
| V2-Sonnet | M11b `20d-content-sonnet-v2-test_v{4,5,6,7,8,11,12,13,14,15}` | 10 | **10/10 PASS** |
| V2-Haiku | M11b `20d-content-haiku-v2-test_v{4,5,6,7,8,11,12,13,14,15}` | 10 | **10/10 PASS** |

Output JSONs: `runs/data/21b-belt-content-{opus,sonnet,haiku}-v2-test_v{4,5,6,7,8,11,12,13,14,15}.json` (30 files).

**Verdict: 30/30 PASS bit-identical.** §D9 Surface #5 (M11b-data-drift halt-gate) cleared. §D9 Surface #13 (cross-milestone Claude alias drift between M11b 2026-05-13/15 and M11a-extension 2026-05-15) cleared at Layer 1: V2-Opus / V2-Sonnet / V2-Haiku alias dispatch stable across the cross-milestone interval at the load-bearing-field level. Layer 2 (within-milestone V4 determinism via §D12 triangulated drift smoke at Phase 2 + Phase 3) remains for Commit D. Reviewer attack "V4-vs-V2 deltas at M11a-extension could reflect Anthropic-side `claude-opus-4-7` alias rotation between M11b and M11a-extension, not the V4 prompt mechanism" is mechanically converted into a bit-identical-verified cross-milestone V2 baseline.

### Cost

| Step | Cells | Spend |
|---|---|---|
| Step 4 — V2-Opus carryover smoke (vs `17b-*`) | 3 | $0.1339 |
| Step 5 — V4-Sonnet Phase 1 baseline | 3 | $0.0283 |
| Step 5 — V4-Haiku Phase 1 baseline | 3 | $0.0094 |
| Step 6 — V2-Opus belt-and-suspenders | 10 | $0.4487 |
| Step 6 — V2-Sonnet belt-and-suspenders | 10 | $0.0659 |
| Step 6 — V2-Haiku belt-and-suspenders | 10 | $0.0219 |
| **Total** | **39** | **$0.7081** |

Cumulative M11a-extension spend through Commit B: pricing-attestation fetch $0 (no API spend) + Commit B $0.7081 = **$0.7081 of the $4 pre-reg budget** (~18% utilized; cross-milestone-locked Opus rate $15/$75 per M10 lock; Sonnet $3/$15 + Haiku $1/$5 per M11b/M11a-extension lock; no observed-published-rate drift vs M11b per `21a-pricing-attestation-2026-05-15.json`).

### Frozen artifacts at Commit B (NOT touched, per §D13 staging discipline)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py` — frozen throughout milestone.
- `sandbox/event_trace.py` — frozen at Commit B; new `test_v21..test_v30` definitions added at Commit C only.
- `baselines/` — no `react_poll_claude.py` edit at Commit B (M11b's `b78554d` dedupe fix carries forward unchanged; rate-table inherited from M11b's `c562173` `_rates_for` substring dispatch).
- `pyproject.toml`, `uv.lock` — no dependency changes at Commit B.

### Next: Commit C — fresh-session trace authoring `test_v21..test_v30`

Per §D13: 10 fresh-session-authored traces under M11a iterative-extension protocol with self-restate pre-flight gate at `eval/author_trace.py`. Acceptance rate ~56% per M11a empirical → expected 12-18 fresh-session attempts to land 10 accepted traces. Numbering locked at `test_v21..test_v30` per D14-H8 (chronological resumption preserving v9/v10 historical gap). Banned-list extension carries forward at each acceptance. Audit-gate enforced per accepted trace. Defense-#4 halt-condition: > 25 attempts → milestone halts pending banned-list-protocol revision.

Commit C lands one accepted trace per transparent commit per M11a `2042dc5` precedent. C-protocol governance decisions D-C1.1..D-C1.6 locked at C1 first-land (see Commit C1 below) and inherited by C2..C10 unchanged.

## Commit C1 — test_v21 (2026-05-16)

**Verdict: test_v21 ACCEPTED at attempt 1/3; audit-gate 8/8 PASS.** Cumulative milestone attempt count 1/25; 9 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at attempt #1 (M11a-extension structural-parsing-failure rate to date: 0/1 attempts).

### C-protocol governance decisions (D-C1.1..D-C1.6 locked at C1 first-land)

Locked at this commit and inherited by C2..C10 without further deliberation (mirror M11a iterative-extension discipline — "no protocol revisions mid-milestone"). Full rationale + alternatives-considered table archived at `~/.claude/plans/adaptive-discovering-key.md`.

| Decision | Lock |
|---|---|
| **D-C1.1 Banned-list provenance/storage** | Extract M11a end-state (127 IDs / 72 themes / 71 tuples) into NEW human-readable `runs/data/21c-banned-list-pre-c{N}.txt` at each C-step land time; parallel `.json` for programmatic audit. Each accepted trace's contributions extend the file at the NEXT C-step's commit (state at C{N} attempt 1 is bit-identical reproducible via single-file path + SHA256). |
| **D-C1.2 Self-restate response persistence schema** | Per-attempt artifact at `runs/data/21c-author-test_v{NN}-attempt-{N}-{accepted,rejected}.json`. Fields: `attempt_number`, `attempted_at_utc`, `verdict`, `banned_list_path` + `banned_list_sha256_at_attempt` + `banned_list_state_counts`, `self_restate_prompt_sha256`, `self_restate_response_verbatim`, `authored_trace_verbatim`, `audit_gate_result` (per-step PASS/FAIL with evidence), `gt_regime_classification`, `defensibility_self_check_per_locked_plan_d9_defense_8`, `fresh_session_metadata`, `milestone_attempt_count_running`. Mirror M11a runs/19 §"Per-attempt drift log" per-attempt transparency. |
| **D-C1.3 Audit-gate precise checklist** | Lock M11a's 6-step audit verbatim from runs/19 §"Per-trace structural audit", augmented with drift strong-overlap rubric (a)+(b) as **explicit reject criteria** (8 items total). Self-restate response is NOT used as an audit reject criterion (pre-flight gate ≠ audit gate; conflation would break attribution per locked plan §D4). |
| **D-C1.4 Retry-cap policy per trace** | Retry-cap = 3 per trace for non-literal-ID rejection reasons. M11a verbatim carry-forward. Literal-ID collision HALTS milestone (per D-C1.5 #1), does not consume retry budget. Single protocol-lever change (self-restate gate addition) preserves attribution of structural-parsing-failure rate to that gate alone. |
| **D-C1.5 Halt-conditions** | Three halts tracked: (1) literal-ID collision → drift-revision-failure milestone halt (M11a carry); (2) >25 cumulative attempts AND <10 accepted → banned-list-saturation milestone halt (locked plan §D9 defense #4); (3) retry-cap-3 exhausted on current trace → session-halt (the trace abandoned), milestone continues with next `test_v{NN+1}`. Each C-step commit message surfaces cumulative attempts + per-trace attempts + structural-parsing-failure-rate-to-date. |
| **D-C1.6 Commit shape** | Single C-step commit bundling: (i) banned-list-pre-c{N}.txt+.json (created or NEW), (ii) per-attempt artifact JSON(s), (iii) `sandbox/event_trace.py` test_v{NN} append + registry-line addition, (iv) `runs/21-*.md` Commit C{N} subsection append, (v) `runs/README.md` row 21 Status update. Mirror M11a `2042dc5` precedent. |

### Banned-list starting state (M11a end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c1.txt` (SHA256 `be3f6f5b4263066fe71aa31ee677e85af0bd296aac44a3ad6b512e27e68dad46`; 9884 bytes; 127 banned event_ids + 72 banned themes + 71 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c1.json` (same content in `{event_ids: [...], themes: [...], tuples: [...]}` schema; 10014 bytes).
- Provenance chain: runs/16 (M8b/M9: 46 IDs / 27 themes / 26 tuples) → runs/18 (+ M10b test_v5: 55 / 32 / 31) → runs/19 §"Banned lists for M11a (starting state)" (+ M10b test_v6/v7/v8: 82 / 47 / 46) → runs/19 §"Banned-list timeline" (+ M11a test_v11..v15: 127 / 72 / 71). Bit-identical to runs/19 §"State at end-of-M11a (post-C5; final cumulative banned-list state)".

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c1.txt > /tmp/m11a-ext-c1-restate-prompt.txt`
- Rendered prompt SHA256: `1175e4808ff75c678dd4b5fe6108225926b5ce07e0c247976745e027421cb98c` (10293 bytes)
- Self-restate response (verbatim restating of constraints (a)-(d) in author's own words; archived in `runs/data/21c-author-test_v21-attempt-1-accepted.json` `self_restate_response_verbatim` field).
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered at attempt #1; schema check via `get_trace('test_v21')` passes on first import.

### Attempt #1 — ACCEPTED (audit-gate 8/8 PASS)

**Verdict:** Accept (strict-letter; 8 of 8 audit-gate items PASS).

**Audit-gate results:**

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v21')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v21'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v21 9 5 760.0` with no exception. |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 (kw, content.lower()) substring checks pass: (`gas`, `leak`); (`appointment`, `rescheduled`); (`vinyl`, `drop`); (`loan`, `repayment`); (`courier`, `signature`). |
| 3a | Banned event_id literal review (vs 127 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v21's 9 event_ids. |
| 3b | Banned theme semantic review (vs 72 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_evidence`. GT 3 (`vinyl_drop_press_today`) is the V4 NEW YES-class generalization target per locked plan §D9 defense #8 — distinct from test_v8's banned theme "10-min ticket presale window opening with access code" on all 4 qualifiers (30-min window vs 10-min, vinyl product release vs ticket, drop vs presale, open queue vs access code). All 4 distractors distinct from any banned theme. |
| 3c | Banned keyword tuple bytewise review (vs 71 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples. |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical grep of 9 event_ids vs union of dev_v1/dev_v2/test_v1/v2/v3/v4/v5/v6/v7/v8/v11..v15 event_ids: 0 collisions. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c; explicit redundant cross-trace check confirms 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v21 has 237 unique 8-grams across content+briefing fields; prior dev/test traces have 1922 unique 8-grams; overlap = 0. |

**GT-regime classification (audit step 7; for Commit D per-trace observations table):**
- GT 1 `gas_leak_kitchen_sensor` — urgent safety/security issue: household natural-gas-leak detection with immediate evacuation imperative.
- GT 2 `cardio_appt_rescheduled` — schedule change affecting the user personally: medical specialty (cardiology) appointment rescheduled at provider request.
- GT 3 `vinyl_drop_press_today` — discretionary-deadline obligation (V4 NEW YES-class): scarcity-bounded opportunity with queue offer + product limit (250 copies) + window under one hour (30 min).
- GT 4 `student_loan_repayment_resume` — financial/deadline obligation: federal student loan auto-debit resumption + 48-hour IDR plan application deadline.
- GT 5 `legal_doc_courier_signature` — message/delivery directed personally: certified legal documents requiring in-person signature + 15-minute lobby wait before return-to-sender.

**Defensibility self-check per §D9 defense #8 (audit step 8; V4 NEW NO-subclause generalization):**
- Distractor `restock_camping_lantern` tests V4 NEW NO subclause "back-in-stock notification without explicit scarcity window" under NEW phrasing/event_id (Goal Zero Lighthouse Mini at Adventure Outfitters with "replenished the stock; browse when ready; no purchase deadline or quantity limit") vs test_v12's `grocer_back_in_stock`.
- Distractor `calendar_running_club_recur` tests V4 NEW NO subclause "recurring-event calendar suggestion or app suggestion" under NEW phrasing/event_id (running with Maya on Thursdays + "Suggestion only — dismiss or set up later") vs test_v12's `calendar_yoga_suggest`.
- Distractor `arcade_meetup_kira` tests V4 NEW NO subclause "casual social-meetup notification without time-pressure" under NEW phrasing/event_id (casual arcade night at Quarterworld Saturday with "No commitment, no RSVP — show up if you're free") vs test_v11's `trivia_league_round`.
- GT `vinyl_drop_press_today` tests V4 NEW YES subclause "scarcity-bounded opportunity with window under one hour" under NEW phrasing/event_id (vinyl record drop, open queue, 30-min window) vs test_v8's `bridgers_presale_window` (10-min ticket presale with access code).
- Coverage summary: all 3 V4 NEW NO subclauses + 1 V4 NEW YES subclause covered at test_v21 — maximal V4-mechanism coverage in a single 5-GT-4-distractor trace under the §D9 defense #8 brief.

**Per-attempt artifact:** `runs/data/21c-author-test_v21-attempt-1-accepted.json` (full audit-gate evidence + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check archived).

### Banned-list state delta at C1

- Pre-C1 (M11a end-state, ships at C1): 127 IDs / 72 themes / 71 tuples.
- C1 contributions from accepted test_v21 (to be incorporated into `21c-banned-list-pre-c2.txt` at C2 land time per D-C1.1):
  - **+9 IDs:** `gas_leak_kitchen_sensor`, `cardio_appt_rescheduled`, `vinyl_drop_press_today`, `student_loan_repayment_resume`, `legal_doc_courier_signature`, `restock_camping_lantern`, `calendar_running_club_recur`, `arcade_meetup_kira`, `discord_unread_digest`.
  - **+5 themes (GT-regime regime column verbatim):** urgent safety/security issue — household natural-gas-leak detection with immediate evacuation imperative; schedule change affecting the user personally — medical specialty (cardiology) appointment rescheduled at provider request; discretionary-deadline obligation — scarcity-bounded opportunity, queue offer with product limit and window under one hour; financial/deadline obligation — federal student loan auto-debit resumption + IDR plan application deadline; message/delivery directed personally — certified legal documents requiring in-person signature + 15-minute lobby wait before return-to-sender.
  - **+5 tuples (GT keyword tuples verbatim):** `(gas, leak)`, `(appointment, rescheduled)`, `(vinyl, drop)`, `(loan, repayment)`, `(courier, signature)`.
- Post-C1 (input state for C2): 136 IDs / 77 themes / 76 tuples. File ships at C2 land time as `runs/data/21c-banned-list-pre-c2.{txt,json}` per D-C1.1 invariant ("no file mutates after the C-step that created it").

### Halt-condition status at C1

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (1 cumulative milestone attempt < 25; 1 accepted trace toward target of 10).
- Retry-cap-3 on test_v21 (D-C1.5 #3): **not exhausted** (1/3 used; PASS at attempt #1).

### Cumulative milestone-spend through Commit C1

Commit C1 spend: $0 (no API spend at Commit C1 — author session in-process; self-restate gate rendered locally without API calls; audit-gate checks are local Python). Cumulative M11a-extension spend through Commit C1: $0.7081 (unchanged from Commit B; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C1 (NOT touched, per locked plan §D13)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 definitions — frozen historical artifacts (only NEW `test_trace_v21` added at C1, plus the registry line `"test_v21": test_trace_v21,`).
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C1.

### Next: Commit C2 — fresh-session trace authoring `test_v22`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c2.{txt,json}` (NEW; reflects test_v21 contributions) as the pre-C2 starting state. Self-restate gate rendered against the pre-C2 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 1/25 carries forward.

Commit C2 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.

---

## Commit C2 — test_v22 (2026-05-17)

**Verdict: test_v22 ACCEPTED at attempt 2/3; audit-gate 8/8 PASS at the accepting attempt. Attempt 1/3 REJECTED at audit-gate step 2 (M8b keyword/content alignment) on 2 of 10 keyword pairs — D-C1.3 audit-gate working as designed; rejection artifact ships in this commit bundle per D-C1.2 + D-C1.6 transparency.** Cumulative milestone attempt count 3/25 through Commit C2 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2); 8 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at all attempts (M11a-extension structural-parsing-failure rate to date: 0/3 attempts — the C2 attempt-1 rejection was step-2 M8b alignment, NOT structural-parsing-failure per §D4 design; self-restate gate addresses audit-gate step 1 territory only).

### C-protocol governance decisions inherited from C1

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) and inherited VERBATIM at C2 with no re-litigation per "no scope drift within a milestone" operating principle.

### C2 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C2.B locked subclause coverage brief (inherited from C2 attempt #1 Plan; verbatim)** | Option (a) within-V4-class power: 1 V4 NEW YES family-milestone-with-social-cost subclass GT (NEW phrasing/event_id vs test_v8 `mom_birthday_heads_up` banned predecessor) + 4 V2/V4 EXISTING YES compliant-content controls (prefer weather alert + production/on-call subclasses C1 did NOT cover); 2-3 V4 NEW NO subclause repeats (back-in-stock-without-scarcity + recurring-event-calendar-suggest + casual-social-meetup) under NEW phrasing/event_id vs BOTH M11a banned predecessors AND test_v21 NEW choices; 1-2 V2/V4 EXISTING NO compliant-content controls. |
| **D-C2.attempt2.A state-confirm checklist (NEW)** | Pre-attempt-#2 state confirmed via three on-disk sha256 verifications (pre-C2 banned-list `.txt` `e98e5b10...`; `.json` `e9cadf8d...`; attempt-1-rejected.json `9c93c3f0...`) — confirms attempt #1's on-disk artifacts persisted through the fresh-session restart bit-identical to attempt-#1-session end state, satisfying "no file mutates after the C-step that created it" extended to "no file mutates after the session that created it". `sandbox/event_trace.py` confirmed HEAD bit-identical (`7384e504...`) before authoring. |
| **D-C2.attempt2.C Step 3.5 pre-flight keyword literal-substring verification (NEW per-attempt author discipline)** | After Step 3 (author trace) and BEFORE Step 4 (run audit-gate), mechanically verify that every GT keyword tuple element appears as case-insensitive substring of that GT's `Event.content`. Implementation: `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v22'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Author-discipline pre-flight only — does NOT modify the audit-gate locked at D-C1.3; does NOT consume retry-cap budget per D-C1.4 (the retry-cap counts audit-gate-submitted attempts only). Reviewer-defense: mirrors M11a test_v11 #1 walrus-syntax failure → all subsequent M11a fresh-session attempts adopted "no walrus operator" as a per-attempt pre-flight without modifying the audit-gate. Attribution remains clean: self-restate gate → structural-parsing (audit step 1 territory); Step 3.5 → M8b keyword/content alignment (audit step 2 territory). |
| **D-C2.attempt2.D commit shape extension** | D-C2.D commit shape inherits VERBATIM with one extension: the C2 commit bundles BOTH attempt-1-rejected.json AND the accepting attempt-N-accepted.json (and any intermediate attempt-{2..N-1}-rejected.json) per D-C1.2 + D-C1.6 transparency. C2 commit message names "attempt N / N total attempts" showing the rejection trajectory. |

### Banned-list starting state (C1 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c2.txt` (SHA256 `e98e5b10125ef34cefc85234fa95b7c7d22d1b2e9d3796b8c8353b973d4b185d`; 11173 bytes; 136 banned event_ids + 77 banned themes + 76 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c2.json` (SHA256 `e9cadf8daaaace5439b50cbddd10fd79cf357e090ad33ddcf6c49638bab4b51e`; 11160 bytes; same content in structured schema).
- Provenance: bit-identical to C1 end-state per D-C1.1 invariant; ships at C2 (was authored at C2-attempt-#1 session and persisted untracked through the fresh-session-restart for attempt-#2).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c2.txt > /tmp/m11a-ext-c2-restate-prompt.txt`
- Rendered prompt SHA256: `3bafb3ff59d3ef1cc82b3e94633d24bd8ddbea8c766e7e5db9f8a14ebb681148` (11582 bytes)
- Re-rendered against the on-disk pre-C2 banned-list file at attempt #2 session — bytewise identical to the prompt rendered at attempt #1 session (file path + file sha256 unchanged; helper `eval/author_trace.py` unchanged since Commit B).
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered at either attempt; schema check via `get_trace('test_v22')` passes on first import at attempt #2.

### Attempt #1 — REJECTED (audit-gate step 2 FAIL on 2 of 10 keyword pairs)

**Verdict:** Reject at first-match-rejection per D-C1.3 audit-gate semantics. First violated check: `step_2_keyword_content_alignment`.

**Audit-gate trace at rejection:**

| Step | Item | Verdict |
|---|---|---|
| 1 | Schema check via `get_trace('test_v22')` | PASS — 9 events / 5 GTs / duration 950.0s |
| 2 | Keyword/content alignment (M8b hard constraint) | **FAIL** — 8 of 10 pairs PASS; 2 FAIL |
| 3a | Banned event_id literal review | PASS — 0 collisions vs 136 banned IDs |
| 3b | Banned theme semantic review | not_evaluated (first-match-rejection at step 2) |
| 3c | Banned keyword tuple bytewise review | PASS — 0 collisions vs 76 banned tuples |
| 4 | Cross-trace literal-ID collision (HALT-gate) | PASS — HALT not triggered |
| 5 | Drift strong-overlap (a) GT tuple bytewise | PASS |
| 6 | Drift strong-overlap (b) ≥8-word verbatim | PASS |

**Rejection reason (verbatim from artifact `rejection_reason_verbatim`):** "Two GT keyword-content alignment failures: GT 3 `payments_webhook_alert_oncall` has keywords=('webhook', 'alert') but the literal word 'alert' does not appear in the GT's `Event.content` (the content uses 'PagerDuty P1', '5xx', 'SLO at risk' but never the word 'alert'); GT 4 `power_disconnect_tomorrow_notice` has keywords=('utility', 'disconnect') but the literal word 'utility' does not appear in the GT's `Event.content` (the utility provider is named 'Seattle City Light' but the generic word 'utility' is absent). M8b's keyword/content alignment hard constraint requires every keyword tuple element to appear as a case-insensitive substring of the GT's content; this is the M8b structural prerequisite for harness scoring (keyword-match-on-content is the join key between GT and arbiter-tagged events). Both keyword pairs need either the content revised to include the literal word, or the keyword replaced with a word that appears in the content."

**Per-attempt artifact:** `runs/data/21c-author-test_v22-attempt-1-rejected.json` (SHA256 `9c93c3f0c22f32b437f7c3627bb6d15b7b54360fa919f421e3ade719559f4031`; full audit-gate evidence + self-restate response verbatim + authored-trace verbatim + post-rejection-actions-taken archived; ships with this C2 commit bundle per D-C1.2 + D-C1.6 transparency).

**Reviewer-defense (D-C1.3 audit-gate working as designed):** The audit-gate caught an author oversight at the pre-submission gate before it could corrupt harness data. The rejection artifact ships in the C2 commit bundle (not hidden, not amended away); the cumulative-milestone attempt count includes attempt #1 transparently (3/25 through Commit C2 — C1 attempt-1 + C2 attempt-1 + C2 attempt-2 — not 2/25). Per locked plan §D9 defense #4 + D-C1.5 #2, banned-list saturation halt counts CUMULATIVE attempts not just accepted-trace count; this rejection contributes to the 25-attempt cap toward the 10-accepted-trace target.

### Attempt #2 — ACCEPTED (audit-gate 8/8 PASS)

**Verdict:** Accept (strict-letter; 8 of 8 audit-gate items PASS). Authored in a fresh session restart from scratch per M11a iterative-extension protocol with NO carryover of specific event_ids, content phrasings, keyword tuples, sim_times, briefing, or intents from attempt #1.

**Step 3.5 pre-flight keyword literal-substring verification (per D-C2.attempt2.C):**

Mechanical check before audit-gate invocation — all 10 keyword/content pairs print `True`:

| Keyword | GT event_id | Pre-flight verdict |
|---|---|---|
| `grandpa` | `grandpa_90th_birthday_tomorrow` | True |
| `birthday` | `grandpa_90th_birthday_tomorrow` | True |
| `flood` | `flash_flood_warning_overnight` | True |
| `warning` | `flash_flood_warning_overnight` | True |
| `database` | `datastore_replica_failover_p1` | True |
| `failover` | `datastore_replica_failover_p1` | True |
| `fall` | `aging_parent_fall_alert_emergency_pendant` | True |
| `pendant` | `aging_parent_fall_alert_emergency_pendant` | True |
| `property` | `property_tax_installment_due_today` | True |
| `tax` | `property_tax_installment_due_today` | True |

**Audit-gate results (8/8 PASS):**

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v22')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v22'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v22 9 5 890.0` with no exception. |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 (kw, content.lower()) substring checks pass (Step 3.5 pre-flight + audit-gate verification both PASS): `(grandpa, grandpa_90th_birthday_tomorrow)`; `(birthday, grandpa_90th_birthday_tomorrow)`; `(flood, flash_flood_warning_overnight)`; `(warning, flash_flood_warning_overnight)`; `(database, datastore_replica_failover_p1)`; `(failover, datastore_replica_failover_p1)`; `(fall, aging_parent_fall_alert_emergency_pendant)`; `(pendant, aging_parent_fall_alert_emergency_pendant)`; `(property, property_tax_installment_due_today)`; `(tax, property_tax_installment_due_today)`. |
| 3a | Banned event_id literal review (vs 136 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v22's 9 event_ids. |
| 3b | Banned theme semantic review (vs 77 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_evidence`. GT 1 `grandpa_90th_birthday_tomorrow` is the V4 NEW YES family-milestone-with-social-cost subclass NEW phrasing/event_id vs test_v8's banned `mom_birthday_heads_up` (subject grandpa vs mother; specific 90th milestone vs unspecified; toast-at-cake-cutting obligation vs forgetting concern; Riverview Country Club venue vs unspecified). GT 2 flash flood warning is NEW specific incident vs M8b's generic 'weather alert' class-level placeholder. GT 3 database failover P1 is NEW specific incident vs M8b's generic 'production / server outage'. GT 4 medical-alert pendant fall-detection is NEW sub-class vs M8b 'ER call' generic, vs M11a test_v12 hospitalized-friend informational-only, vs C1 gas_leak_kitchen_sensor different sub-class. GT 5 property-tax first-installment is NEW specific incident vs M8b 'rent due' generic / M10b test_v5 tax-extension IRS-side / M11a test_v12 DMV-license-renewal / M11a test_v13 warranty-registration / C1 student_loan federal-loan. |
| 3c | Banned keyword tuple bytewise review (vs 76 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(grandpa, birthday), (flood, warning), (database, failover), (fall, pendant), (property, tax)]`. Note `(mother, birthday)` banned but `(grandpa, birthday)` bytewise-distinct; `(production, alert)` banned but `(database, failover)` bytewise-distinct; `(tax, expires)` banned but `(property, tax)` bytewise-distinct. |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical grep of 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21 event_ids: 0 collisions against 136 prior event_ids. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (76 unique across dev_v1..test_v21): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v22 has 378 unique 8-grams across content+briefing fields; prior dev/test traces have 2159 unique 8-grams; overlap = 0. |

**GT-regime classification (audit step 7; for Commit D per-trace observations table):**

- GT 1 `grandpa_90th_birthday_tomorrow` — **discretionary-deadline obligation (V4 NEW YES, family-milestone-with-social-cost subclass)**: proactive heads-up for grandfather Walter's 90th milestone birthday party tomorrow with toast-at-cake-cutting obligation; all siblings + cousins committed/travelled.
- GT 2 `flash_flood_warning_overnight` — **weather alert (V2 EXISTING YES)**: NWS flash flood warning for King County with 4-6" overnight rain, low-lying I-5 corridor road closures expected, user's Westlake Avenue commute in warning zone, I-405 alternate advised.
- GT 3 `datastore_replica_failover_p1` — **production/on-call alert (V2 EXISTING YES)**: PagerDuty P1 database failover on primary-postgres-001 with SQLSTATE 08006 write-failures; user primary on-call for payments-data shard; 12-min SLO downtime impact.
- GT 4 `aging_parent_fall_alert_emergency_pendant` — **urgent safety/security issue (V2 EXISTING YES — medical-emergency sub-class)**: medical-alert pendant for elderly father (Robert) triggered fall-detection with auto-EMS-dispatch; user primary emergency contact; pendant operator awaiting callback for hospital handoff.
- GT 5 `property_tax_installment_due_today` — **financial/deadline obligation (V2 EXISTING YES)**: King County Treasurer property-tax first-installment $3,180 due today 5pm; 10% late penalty + day-31 certified collection notice if missed.

**Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism subclause coverage):**

V4 NEW YES coverage at C2:
- GT `grandpa_90th_birthday_tomorrow` tests V4 NEW YES subclause "family milestone with social cost (birthday or anniversary heads-up)" under NEW phrasing/event_id vs test_v8 `mom_birthday_heads_up` banned predecessor. **Cross-trace V4 NEW YES coverage at C1+C2: C1 covered the scarcity-bounded-opportunity subclause (`vinyl_drop_press_today`); C2 covers the family-milestone-with-social-cost subclause — together C1+C2 cover BOTH V4 NEW YES subclauses across the M11a-extension 10-trace new set.**

V4 NEW NO coverage at C2 (all 3 V4 NEW NO subclauses repeated under NEW phrasing/event_id vs M11a banned predecessors AND C1 test_v21 NEW choices):
- Distractor `sneakers_wishlist_back_in_stock_email` tests V4 NEW NO subclause "back-in-stock notification without explicit scarcity window" under NEW phrasing/event_id (SneakerVault email re: Nike Air Max 90 wishlist item; "no rush, no quantity limit, ships 5-7 business days") vs test_v12's `grocer_back_in_stock` (M11a banned) AND vs test_v21's `restock_camping_lantern` (C1 NEW choice).
- Distractor `calendar_coffee_lisa_weekly_suggest` tests V4 NEW NO subclause "recurring-event calendar suggestion or app suggestion" under NEW phrasing/event_id (Google Calendar suggesting weekly Wednesday coffee with Lisa based on 5-Wednesday history at Heart Coffee; "Add weekly / Add once / Dismiss") vs test_v12's `calendar_yoga_suggest` (M11a banned) AND vs test_v21's `calendar_running_club_recur` (C1 NEW choice).
- Distractor `pickup_basketball_saturday_open` tests V4 NEW NO subclause "casual social-meetup notification without time-pressure" under NEW phrasing/event_id (text from Marco re: pickup 5-on-5 basketball at Wallingford courts Saturday 10am; "totally casual, no commitment, ignore if busy") vs test_v11's `trivia_league_round` (M11a banned) AND vs test_v21's `arcade_meetup_kira` (C1 NEW choice).

V2 EXISTING NO compliant-content control at C2:
- Distractor `chrome_extension_marketplace_update` tests V2 EXISTING NO "feature announcements, app updates, or social/channel invites" — Chrome Web Store extension-review-system update with marketplace homepage browse suggestion; no action required.

**Coverage summary at C2:** 1 V4 NEW YES family-milestone-with-social-cost (NEW phrasing) + 3 V4 NEW NO subclauses (back-in-stock + recurring-calendar-suggest + casual-social-meetup, all 3 covered with NEW phrasing vs M11a banned predecessors AND vs C1 NEW choices) + 1 V2 EXISTING NO control + 4 V2 EXISTING YES compliant-content controls (weather alert + production/on-call alert + urgent safety medical-emergency + financial/deadline obligation) — maximal V4-mechanism coverage at C2 + cross-trace V4 NEW YES subclass complementarity vs C1 (both V4 NEW YES subclauses covered across the C1+C2 pair).

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v22-attempt-2-accepted.json` (SHA256 `c2b474c3eab0ef70252b8ecd9c869cdb485dc786f23958c1db15c26e27da6246`; 22447 bytes; full audit-gate evidence + Step 3.5 pre-flight verification log + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata archived).

### Banned-list state delta at C2

- Pre-C2 (C1 end-state, ships at C2): 136 IDs / 77 themes / 76 tuples.
- C2 contributions from accepted test_v22 (to be incorporated into `21c-banned-list-pre-c3.txt` at C3 land time per D-C1.1):
  - **+9 IDs:** `grandpa_90th_birthday_tomorrow`, `flash_flood_warning_overnight`, `datastore_replica_failover_p1`, `aging_parent_fall_alert_emergency_pendant`, `property_tax_installment_due_today`, `sneakers_wishlist_back_in_stock_email`, `calendar_coffee_lisa_weekly_suggest`, `pickup_basketball_saturday_open`, `chrome_extension_marketplace_update`.
  - **+5 themes (GT-regime regime column verbatim):** discretionary-deadline obligation (V4 NEW YES, family-milestone subclass) — proactive heads-up for grandfather's 90th milestone birthday party tomorrow with toast obligation; weather alert (V2 EXISTING YES) — NWS flash flood warning for King County with 4-6" overnight rain and commute-route impact; production/on-call alert (V2 EXISTING YES) — PagerDuty P1 database failover on primary-postgres-001 with SLO-bound resolution window; urgent safety/security issue (V2 EXISTING YES, medical-emergency sub-class) — medical-alert pendant fall-detection auto-EMS-dispatch + primary-contact callback obligation for elderly father; financial/deadline obligation (V2 EXISTING YES) — county property tax first-installment payment with end-of-day 5pm cutoff + 10% late penalty.
  - **+5 tuples (GT keyword tuples verbatim):** `(grandpa, birthday)`, `(flood, warning)`, `(database, failover)`, `(fall, pendant)`, `(property, tax)`.
- Post-C2 (input state for C3): 145 IDs / 82 themes / 81 tuples. File ships at C3 land time as `runs/data/21c-banned-list-pre-c3.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C2

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at the accepting attempt; attempt-1 also PASSed step 4).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (3 cumulative milestone attempts < 25; 2 accepted traces toward target of 10).
- Retry-cap-3 on test_v22 (D-C1.5 #3): **not exhausted** (2/3 used; PASS at attempt #2 / 1 retry remaining had attempt #2 not accepted).

### Cumulative milestone-spend through Commit C2

Commit C2 spend: $0 at attempt #1 + $0 at attempt #2 (both attempts in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C2: $0.7081 (unchanged from Commit C1; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C2 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21 definitions — frozen historical artifacts (only NEW `test_trace_v22` added at C2, plus the registry line `"test_v22": test_trace_v22,`).
- `runs/data/21c-banned-list-pre-c1.{txt,json}` + `runs/data/21c-author-test_v21-*.json` — frozen at C1; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C2.

### Next: Commit C3 — fresh-session trace authoring `test_v23`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c3.{txt,json}` (NEW; reflects test_v21 + test_v22 contributions; 145 IDs / 82 themes / 81 tuples) as the pre-C3 starting state. Self-restate gate rendered against the pre-C3 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 3/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C) carries forward as a per-attempt author discipline (not a C-protocol governance change).

Commit C3 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.

---

## Commit C3 — test_v23 (2026-05-17)

**Verdict: test_v23 ACCEPTED at attempt 1/3; audit-gate 8/8 PASS.** Cumulative milestone attempt count 4/25 through Commit C3 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2 + C3 attempt-1); 7 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at this attempt (M11a-extension structural-parsing-failure rate to date: 0/4 attempts). Step 3.5 pre-flight keyword literal-substring verification (D-C3.attempt1.C inheriting verbatim from D-C2.attempt2.C) caught one keyword/content misalignment at first run and was iterated in-session before audit-gate invocation — the explicit intended workflow per the locked author-discipline addition; does NOT consume retry-cap budget per D-C1.4.

### C-protocol governance decisions inherited from C1 + C2

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) inherit VERBATIM at C3 with no re-litigation per "no scope drift within a milestone" operating principle. D-C2.A..D-C2.D (locked at C2 attempt-#1 Plan) and D-C2.attempt2.A..D-C2.attempt2.D (locked at C2 attempt-#2 Plan `f9808c8`) also inherit VERBATIM at C3. The per-attempt author discipline added at C2 attempt #2 (Step 3.5 pre-flight) carries forward as standing author discipline through C3..C10.

### C3 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C3.attempt1.A state-confirm checklist** | Pre-attempt-#1 state confirmed via four on-disk verifications: main HEAD `f9808c8` (M11a-extension Commit C2); working tree clean; `sandbox/event_trace.py` sha256 `42332303ff83f9e0e90b2149fe4293839f357ca082a77968e1ed73f4499367af` (58368 bytes; HEAD-bit-identical post-C2 incl. `test_trace_v22` + registry line); V4 prompt string sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; bytewise-identical to §D1 lock — `agent/arbiter.py` last touched at `adc1cba` Commit B, unchanged through C1+C2). D-C2.attempt2.A precedent mirrored verbatim. |
| **D-C3.attempt1.B subclause coverage brief inheritance + C3-specific content recommendation** | D-C2.B brief inherits VERBATIM (within-V4-class power + V2/V4 EXISTING YES compliant-content controls + V4 NEW NO subclause repeats + V2/V4 EXISTING NO compliant-content controls). C3-specific (locked at Plan): C3 prioritizes compliant-content controls — 5 GTs across 5 V2 EXISTING YES classes under NEW specific incidents distinct from C1+C2 within-class predecessors, plus 4 V2 EXISTING NO distractors across 4 V2 NO classes; zero V4 NEW NO subclause repeats (3 subclauses already covered 2x each at C1+C2); zero V4 NEW YES subclause coverage (both subclauses already covered singularly at C1+C2). Defensibility framing: H4 COMPLIANT_NO_REGRESSION strict-+0 (per D14-H4) gates Row 1 firing regardless of MECHANISM_CONFIRM verdict; a single non-flagged-trace regression at single-shot temperature=0 inference sinks the headline to Row 3 PARTIAL SUCCESS; C3 maximizes the H4 denominator with V2 EXISTING YES + V2 EXISTING NO compliant-content cells. |
| **D-C3.attempt1.C Step 3.5 pre-flight keyword literal-substring verification** | Inherits VERBATIM from D-C2.attempt2.C. Mechanically verify every GT keyword tuple element appears as case-insensitive substring of that GT's Event.content via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v23'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Does NOT consume retry-cap budget per D-C1.4. |
| **D-C3.attempt1.D commit shape** | D-C2.attempt2.D commit shape inherits VERBATIM with normal attempt-#1-accepts trajectory (no rejected-attempt bundling since attempt #1 accepted). |

### Banned-list starting state (C2 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c3.txt` (SHA256 `603498b434b45ddde7ba0be350403b6253351d99a58f37485593219be470d7dd`; 12661 bytes; 145 banned event_ids + 82 banned themes + 81 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c3.json` (SHA256 `b24f24c142a32f388da95de1c1dd371cddb6d7a80a112881a3d1c7268e1e2ca7`; 12552 bytes; same content in structured schema).
- Provenance: extended at C3-attempt-#1 session by appending C2's accepted test_v22 contributions (+9 IDs / +5 themes / +5 tuples) to the pre-C2 banned-list (`e98e5b10…` / `e9cadf8d…`, 136/77/76) per D-C1.1 invariant. Pre-C2 files NOT mutated (verified bit-identical pre and post C3 authoring).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c3.txt > /tmp/m11a-ext-c3-restate-prompt.txt`
- Rendered prompt SHA256: `de8d3d16f8f77dcc71735e0b5b506c684d8f9f2cf6112a63304312eb864737a0` (13070 bytes).
- Self-restate response authored in own words distinct from C1's response + C2 attempt-#1's response + C2 attempt-#2's response per fresh-session-restart-from-scratch discipline; full text archived verbatim in artifact `21c-author-test_v23-attempt-1-accepted.json` `self_restate_response_verbatim` field.
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered; schema check via `get_trace('test_v23')` passes on first import.

### Step 3.5 pre-flight keyword literal-substring verification (D-C3.attempt1.C in-session iteration)

| Run | Outcome | Detail |
|---|---|---|
| 1 | **FAIL** on 1 of 10 pairs | `('pickup', partner_voicemail_ring_pickup_jeweler): False` — content used "pick up" (two words with space) but keyword tuple element is `pickup` (one word without space); literal substring check requires bytewise match. |
| 1 → 2 | **Corrective action** | In-session edit to GT 3 content: "to pick up the resized wedding ring" → "for the pickup of the resized wedding ring"; preserves semantic meaning; revised in-place per D-C3.attempt1.C explicit allowance ("revise GT content OR replace keyword; re-author Step 3; re-run Step 3.5"); does NOT consume retry-cap budget per D-C1.4. |
| 2 | **PASS** — all 10 pairs print `True` | `('court', court_hearing_moved_same_day_default_risk) True; ('hearing', court_hearing_moved_same_day_default_risk) True; ('insurance', homeowner_insurance_lapse_72h_notice) True; ('lapse', homeowner_insurance_lapse_72h_notice) True; ('ring', partner_voicemail_ring_pickup_jeweler) True; ('pickup', partner_voicemail_ring_pickup_jeweler) True; ('dust', dust_storm_warning_freeway_visibility) True; ('storm', dust_storm_warning_freeway_visibility) True; ('tls', tls_cert_expiry_3hr_customer_endpoint) True; ('expiry', tls_cert_expiry_3hr_customer_endpoint) True`. |

**Reviewer-defense (Step 3.5 working as designed):** Step 3.5 caught a misalignment that would have rejected at audit-gate step 2 if the trace had been submitted directly — the explicit purpose of the D-C2.attempt2.C author-discipline addition (mirror of M11a test_v11 #1 walrus-syntax → per-attempt-pre-flight discipline carry-forward). The in-session iteration is the intended workflow; the iteration is transparently logged in the per-attempt artifact + this subsection. Attribution remains clean: self-restate gate → structural-parsing (audit step 1 territory); Step 3.5 → M8b keyword/content alignment (audit step 2 territory).

### Audit-gate results (8/8 PASS)

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v23')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v23'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v23 9 5 890.0` with no exception. |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 `(kw, content.lower())` substring checks pass (Step 3.5 pre-flight + audit-gate verification both PASS at the re-run). Pairs: `(court, court_hearing_moved_same_day_default_risk)`; `(hearing, court_hearing_moved_same_day_default_risk)`; `(insurance, homeowner_insurance_lapse_72h_notice)`; `(lapse, homeowner_insurance_lapse_72h_notice)`; `(ring, partner_voicemail_ring_pickup_jeweler)`; `(pickup, partner_voicemail_ring_pickup_jeweler)`; `(dust, dust_storm_warning_freeway_visibility)`; `(storm, dust_storm_warning_freeway_visibility)`; `(tls, tls_cert_expiry_3hr_customer_endpoint)`; `(expiry, tls_cert_expiry_3hr_customer_endpoint)`. |
| 3a | Banned event_id literal review (vs 145 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v23's 9 event_ids. |
| 3b | Banned theme semantic review (vs 82 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_evidence`. All 5 GT themes pass with distinguishing qualifiers documented vs nearest banned predecessors (sub-cell-distinct for each: schedule-change court-default-risk vs C1 cardio-rescheduled; financial/deadline homeowner-insurance-lapse vs C1 student-loan + C2 property-tax + M11a test_v15 Visa-autopay; message/delivery partner-jeweler-pickup vs M10b family-voicemail-airport + M11a test_v14 movers + M11a test_v15 auto-mechanic + M11a test_v13 real-estate-counter + C1 courier-signature; weather alert dust-storm-Maricopa-County vs C2 flash-flood-King-County; production/on-call TLS-cert-expiry vs C2 database-failover-postgres). |
| 3c | Banned keyword tuple bytewise review (vs 81 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(court, hearing), (insurance, lapse), (ring, pickup), (dust, storm), (tls, expiry)]`. Note semantically-adjacent bytewise-distinct cases: `(wallet, pickup)` banned (M11a test_v11) but `(ring, pickup)` bytewise-distinct on first element; `(license, expires)` + `(passport, expiring)` banned but `(tls, expiry)` bytewise-distinct on both elements + `'expiry'` ≠ `'expires'` / `'expiring'` as tokens; `(weather, rain)` banned but `(dust, storm)` bytewise-distinct on both elements; `(production, alert)` banned but `(tls, expiry)` bytewise-distinct on both elements + different fault class. |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical grep of 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21/v22 event_ids: 0 collisions against 145 prior event_ids. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (81 unique across dev_v1..test_v22): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v23 has 528 unique 8-grams across content+briefing+intents fields; prior dev/test traces have 4004 unique 8-grams; overlap = 0. |

### GT-regime classification (audit step 7; for Commit D per-trace observations table)

- GT 1 `court_hearing_moved_same_day_default_risk` — **schedule change affecting the user personally (V2 EXISTING YES)**: court clerk email moving today's 2pm small-claims hearing to today 11am on Judge Calderon's reassigned docket; user on $4,200 case (Acme Plumbing vs. user); confirm appearance by 10am via eFile portal or default judgment + collection proceedings follow.
- GT 2 `homeowner_insurance_lapse_72h_notice` — **financial/deadline obligation (V2 EXISTING YES)**: Liberty Mutual notice — homeowner insurance auto-debit failed last billing cycle (linked checking transfer NSF); policy lapses in 72 hours unless $2,470 clears via carrier portal; mortgage lender notified on lapse + force-placed coverage at +$300/mo above prior premium.
- GT 3 `partner_voicemail_ring_pickup_jeweler` — **message or delivery directed personally to the user (V2 EXISTING YES)**: voicemail from partner Mira asking user to swing by Goldsmiths on Roosevelt Row this afternoon for the pickup of the resized wedding ring; her 3pm meeting ran long; shop closes at 5pm sharp with no weekend hours; one-week delay if missed; explicit callback request.
- GT 4 `dust_storm_warning_freeway_visibility` — **weather alert (V2 EXISTING YES)**: NWS dust storm warning for Maricopa County through 8pm tonight — 50+ mph wind gusts kicking up dense dust along I-10 between Phoenix and Tucson; visibility may drop below quarter-mile; driver advisory; user's afternoon drive to Tucson conference passes through warned corridor.
- GT 5 `tls_cert_expiry_3hr_customer_endpoint` — **production/on-call alert (V2 EXISTING YES)**: PagerDuty P2 from Datadog synthetic monitor — TLS certificate for api.acmewidgets.com (user's team's customer-facing billing-webhook endpoint) expires at 16:32 PST today; current time 13:14 PST leaves 3hr 18min to issue and deploy renewal via cert-manager; customer billing webhooks 502 on expiry; on-call rotation runbook lists user as primary.

### Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism + V2-class subclause coverage)

**V4 NEW YES coverage at C3:** **NONE** (intentional per D-C3.attempt1.B defensibility framing). Both V4 NEW YES subclauses already covered singularly across C1+C2 (scarcity-bounded-opportunity at C1 `vinyl_drop_press_today`; family-milestone-with-social-cost at C2 `grandpa_90th_birthday_tomorrow`); a third instance at C3 would over-weight V4 NEW YES vs the H4 COMPLIANT_NO_REGRESSION denominator.

**V4 NEW NO coverage at C3:** **NONE** (intentional per D-C3.attempt1.B). All 3 V4 NEW NO subclauses already covered 2x each at C1+C2 under NEW phrasing per subclass: back-in-stock-without-scarcity (`restock_camping_lantern` at C1 + `sneakers_wishlist_back_in_stock_email` at C2); recurring-event-calendar-suggestion (`calendar_running_club_recur` at C1 + `calendar_coffee_lisa_weekly_suggest` at C2); casual-social-meetup-without-time-pressure (`arcade_meetup_kira` at C1 + `pickup_basketball_saturday_open` at C2). Additional repeats yield less marginal H4 value than compliant-content additions; defensibility framing prioritizes H4 denominator-building at C3.

**V2 EXISTING YES compliant-content coverage at C3 (5 GTs across 5 distinct V2 YES classes):**
- GT `court_hearing_moved_same_day_default_risk` tests V2 schedule-change-affecting-user-personally class under NEW specific incident distinct from C1's medical-specialty cardio reschedule.
- GT `homeowner_insurance_lapse_72h_notice` tests V2 financial/deadline-obligation class under NEW specific incident distinct from C1's federal student loan + C2's county property tax + M11a's mortgage-rate / Visa-autopay / HOA / margin / bond / warranty.
- GT `partner_voicemail_ring_pickup_jeweler` tests V2 message/delivery-directed-personally class under NEW specific incident distinct from C1's certified legal courier + M10b's family-airport-voicemail / personal-6pm-voicemail / photographer-voicemail + M11a's real-estate / movers / auto-mechanic / hospitalized-friend voicemails.
- GT `dust_storm_warning_freeway_visibility` tests V2 weather-alert class under NEW specific incident distinct from C2's flash-flood-King-County (different geography Maricopa vs King; different meteorology dust-storm vs flash-flood; different driving hazard zero-visibility vs road-closure).
- GT `tls_cert_expiry_3hr_customer_endpoint` tests V2 production/on-call-alert class under NEW specific incident distinct from C2's database-failover-postgres (different fault class TLS-cert-expiry vs DB-replica-failover; different remediation cert-manager-renewal vs DB-promotion; different urgency-mechanism 3hr-to-issue+deploy vs 10min-promotion-ETA).

**V2 EXISTING NO compliant-content distractor coverage at C3 (4 distractors across 4 distinct V2 NO classes):**
- Distractor `cloud_backup_daily_success_digest` tests V2 "routine status, uptime, heartbeat, or 'all systems normal' pings" — CloudStash daily backup digest with successful snapshot; explicit "All systems normal" framing.
- Distractor `kitchen_gear_quarterly_digital_magazine` tests V2 "marketing, promotional, or newsletter content" — Kitchen Gear Quarterly Spring digital magazine issue; explicit unsubscribe-footer framing.
- Distractor `morning_briefing_no_urgent_items_today` tests V2 "generic daily briefings that explicitly state no urgent items" — Wednesday morning briefing explicitly stating "No time-sensitive items flagged for today".
- Distractor `notion_new_dashboard_feature_tour` tests V2 "feature announcements, app updates, or social/channel invites" — Notion analytics dashboard feature rollout announcement; explicit "No action required" framing.

**Coverage summary at C3:** Maximal H4 COMPLIANT_NO_REGRESSION evidence-base contribution at a single trace cell — 5 V2 EXISTING YES GTs across 5 distinct V2 YES classes + 4 V2 EXISTING NO distractors across 4 distinct V2 NO classes; zero V4 NEW YES or V4 NEW NO repeats. Cross-trace coverage state through C3: **V4 NEW YES 2/2 subclauses covered** (singular-each via C1+C2); **V4 NEW NO 3/3 subclauses covered** (each 2x via C1+C2 under NEW phrasing); **V2 EXISTING YES classes coverage across C1+C2+C3**: urgent-safety (C1+C2), schedule-change (C1+C3), financial/deadline (C1+C2+C3), message/delivery (C1+C3), weather-alert (C2+C3), production/on-call (C2+C3), discretionary-deadline-V4-YES (C1+C2); **V2 EXISTING NO classes coverage across C1+C2+C3**: routine-status/heartbeat (C3 first coverage), marketing/newsletter (C3 first coverage), generic-daily-briefing-explicitly-no-urgent (C3 first coverage), feature-announcement/app-update (C2+C3), discord-social-channel (C1).

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v23-attempt-1-accepted.json` (SHA256 `6767e7d1882285cac54d1ea8c63cc77d211c9b51ebcd5d84638ee088a39426ee`; 31455 bytes; full audit-gate evidence + Step 3.5 pre-flight verification iteration log + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata archived).

### Banned-list state delta at C3

- Pre-C3 (C2 end-state, ships at C3): 145 IDs / 82 themes / 81 tuples.
- C3 contributions from accepted test_v23 (to be incorporated into `21c-banned-list-pre-c4.txt` at C4 land time per D-C1.1):
  - **+9 IDs:** `court_hearing_moved_same_day_default_risk`, `homeowner_insurance_lapse_72h_notice`, `partner_voicemail_ring_pickup_jeweler`, `dust_storm_warning_freeway_visibility`, `tls_cert_expiry_3hr_customer_endpoint`, `cloud_backup_daily_success_digest`, `kitchen_gear_quarterly_digital_magazine`, `morning_briefing_no_urgent_items_today`, `notion_new_dashboard_feature_tour`.
  - **+5 themes (GT-regime regime column verbatim):** schedule change affecting the user personally (V2 EXISTING YES) — court clerk same-day moving small-claims hearing from 2pm to 11am with 10am confirm deadline and default-judgment-plus-collection risk; financial/deadline obligation (V2 EXISTING YES) — homeowner insurance auto-debit failed last billing cycle, 72-hour policy lapse risk + force-placed-coverage penalty + mortgage-lender notification; message/delivery directed personally to the user (V2 EXISTING YES) — partner voicemail requesting cross-town jeweler pickup of resized wedding ring before 5pm closing + one-week delay penalty + callback request; weather alert (V2 EXISTING YES) — NWS dust storm warning for Maricopa County with 50+ mph gusts and zero-visibility risk on I-10 between Phoenix and Tucson; production/on-call alert (V2 EXISTING YES) — TLS certificate for customer-facing billing-webhook endpoint expiring in 3 hours with on-call primary on cert-manager rotation.
  - **+5 tuples (GT keyword tuples verbatim):** `(court, hearing)`, `(insurance, lapse)`, `(ring, pickup)`, `(dust, storm)`, `(tls, expiry)`.
- Post-C3 (input state for C4): 154 IDs / 87 themes / 86 tuples. File ships at C4 land time as `runs/data/21c-banned-list-pre-c4.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C3

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at the accepting attempt).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (4 cumulative milestone attempts < 25; 3 accepted traces toward target of 10).
- Retry-cap-3 on test_v23 (D-C1.5 #3): **not exhausted** (1/3 used; PASS at attempt #1 / 2 retries remaining had attempt #1 not accepted).

### Cumulative milestone-spend through Commit C3

Commit C3 spend: $0 at attempt #1 (in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C3: $0.7081 (unchanged from Commit C2; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C3 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21 + test_v22 definitions — frozen historical artifacts (only NEW `test_trace_v23` added at C3, plus the registry line `"test_v23": test_trace_v23,`).
- `runs/data/21c-banned-list-pre-c{1,2}.{txt,json}` + `runs/data/21c-author-test_v{21,22}-*.json` — frozen at C1+C2; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C3.

### Next: Commit C4 — fresh-session trace authoring `test_v24`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c4.{txt,json}` (NEW; reflects test_v21 + test_v22 + test_v23 contributions; 154 IDs / 87 themes / 86 tuples) as the pre-C4 starting state. Self-restate gate rendered against the pre-C4 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 4/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C / D-C3.attempt1.C) carries forward as standing per-attempt author discipline.

Commit C4 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.
