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

---

## Commit C4 — test_v24 (2026-05-17)

**Verdict: test_v24 ACCEPTED at attempt 1/3; audit-gate 8/8 PASS.** Cumulative milestone attempt count 5/25 through Commit C4 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2 + C3 attempt-1 + C4 attempt-1); 6 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at this attempt (M11a-extension structural-parsing-failure rate to date: 0/5 attempts). Step 3.5 pre-flight keyword literal-substring verification (D-C4.attempt1.C inheriting verbatim from D-C2.attempt2.C / D-C3.attempt1.C) PASSed on first run with no in-session iteration required — content was authored with explicit attention to keyword literal-substring placement (each GT's keyword-tuple elements appear in content using the exact one-word forms specified in the tuple); contrast C3 attempt-1 where `('pickup', partner_voicemail_ring_pickup_jeweler)` FAILed at run 1 and required in-session content revision before PASS at run 2.

### C-protocol governance decisions inherited from C1 + C2 + C3

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) inherit VERBATIM at C4 with no re-litigation per "no scope drift within a milestone" operating principle. D-C2.A..D-C2.D (locked at C2 attempt-#1 Plan) + D-C2.attempt2.A..D-C2.attempt2.D (locked at C2 attempt-#2 Plan `f9808c8`) + D-C3.attempt1.A..D-C3.attempt1.D (locked at C3 attempt-#1 Plan `9f84a01`) also inherit VERBATIM at C4. The per-attempt author discipline added at C2 attempt #2 (Step 3.5 pre-flight) carries forward as standing author discipline through C4..C10.

### C4 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C4.attempt1.A state-confirm checklist** | Pre-attempt-#1 state confirmed via four on-disk verifications: main HEAD `9f84a01` (M11a-extension Commit C3); working tree clean; `sandbox/event_trace.py` sha256 `a94e602310c9e0662a99f4d3540d0731289f7093f4f4cc636069bd4732daed87` (63778 bytes; HEAD-bit-identical post-C3 incl. `test_trace_v23` + registry line); V4 prompt string sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; bytewise-identical to §D1 lock — `agent/arbiter.py` last touched at `adc1cba` Commit B, unchanged through C1+C2+C3). D-C3.attempt1.A precedent mirrored verbatim. |
| **D-C4.attempt1.B subclause coverage brief inheritance + C4-specific path-lock** | D-C2.B / D-C3.attempt1.B brief inherits VERBATIM. C4-specific path-lock (locked at Plan): **PATH (a)** — continue C3's H4-priority compliant-content discipline with explicit V2 EXISTING NO 1x→2x triangulation focus. Trace shape: 5 GTs across 5 distinct V2 EXISTING YES classes (urgent safety/security + schedule-change + message/delivery + weather alert + production/on-call) under NEW within-class incidents distinct from C1+C2+C3 + 4 distractors prioritizing 1x→2x coverage on routine-status (SSL-monitor weekly vs C3 cloud-backup daily) + marketing/newsletter (tea-club subscriber vs C3 kitchen-gear magazine) + generic-daily-briefing (evening-EOD vs C3 morning) + social-channel-invite (Slack community vs C1 discord-digest). Zero V4 NEW YES + zero V4 NEW NO this attempt (both V4 NEW YES subclauses singularly covered C1+C2; all 3 V4 NEW NO subclauses 2x at C1+C2; H4 denominator-growth dominates 3rd-repeat marginal info). Defensibility framing: H4 COMPLIANT_NO_REGRESSION strict-+0 (per D14-H4) gates Row 1 firing regardless of MECHANISM_CONFIRM verdict; C4 maximizes the H4 denominator with V2 EXISTING YES + V2 EXISTING NO compliant-content cells AND uses the V2 NO 1x→2x triangulation slot to tighten C3's weakest cross-trace coverage cells. |
| **D-C4.attempt1.C Step 3.5 pre-flight keyword literal-substring verification** | Inherits VERBATIM from D-C2.attempt2.C / D-C3.attempt1.C. Mechanically verify every GT keyword tuple element appears as case-insensitive substring of that GT's Event.content via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v24'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Does NOT consume retry-cap budget per D-C1.4. |
| **D-C4.attempt1.D commit shape** | D-C3.attempt1.D commit shape inherits VERBATIM with normal attempt-#1-accepts trajectory (no rejected-attempt bundling since attempt #1 accepted). |

### Banned-list starting state (C3 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c4.txt` (SHA256 `0fe5c277679a30c66e498d5735dd8fb4173fd04b757e85ad0cf8c3981f7da42d`; 14342 bytes; 154 banned event_ids + 87 banned themes + 86 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c4.json` (SHA256 `24aced6004d8e82a87147af6082f3e2c6e47ece8ab9eaab5637f03c1a44aa3a1`; 14136 bytes; same content in structured schema; counts mechanically verified unique).
- Provenance: extended at C4-attempt-#1 session by appending C3's accepted test_v23 contributions (+9 IDs / +5 themes / +5 tuples) to the pre-C3 banned-list (`603498b4…` / `b24f24c1…`, 145/82/81) per D-C1.1 invariant. Pre-C3 files NOT mutated (verified bit-identical pre and post C4 authoring).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c4.txt > /tmp/m11a-ext-c4-restate-prompt.txt`
- Rendered prompt SHA256: `0a0d742bfd188acfa50e10144442ecf36793f403e7165c14c5448c6715a2181b` (14751 bytes).
- Self-restate response authored in own words distinct from C1's response + C2 attempt-#1's response + C2 attempt-#2's response + C3 attempt-#1's response per fresh-session-restart-from-scratch discipline; full text archived verbatim in artifact `21c-author-test_v24-attempt-1-accepted.json` `self_restate_response_verbatim` field.
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered; schema check via `get_trace('test_v24')` passes on first import.

### Step 3.5 pre-flight keyword literal-substring verification (D-C4.attempt1.C; first-run PASS)

| Run | Outcome | Detail |
|---|---|---|
| 1 | **PASS** — all 10 pairs print `True` | `('carbon', carbon_monoxide_alarm_evacuate_call_gas_company) True; ('monoxide', carbon_monoxide_alarm_evacuate_call_gas_company) True; ('pediatrician', pediatrician_visit_advanced_today_4pm) True; ('advanced', pediatrician_visit_advanced_today_4pm) True; ('hospital', hospital_grandmother_hip_fracture_next_of_kin_callback) True; ('grandmother', hospital_grandmother_hip_fracture_next_of_kin_callback) True; ('tornado', tornado_watch_tri_county_peak_risk_tonight) True; ('watch', tornado_watch_tri_county_peak_risk_tonight) True; ('disk', disk_space_critical_var_log_api_host_oom_90min) True; ('space', disk_space_critical_var_log_api_host_oom_90min) True`. No in-session iteration required. |

**Reviewer-defense (Step 3.5 working as designed):** Step 3.5 PASSed on first run for C4 because content was authored with explicit attention to keyword literal-substring placement — each GT's keyword tuple elements appear in content using the exact one-word forms specified in the tuple (e.g., GT 3 keyword `(hospital, grandmother)` aligned with content "Voicemail from St. Vincent's hospital admitting desk: your grandmother Eleanor…"; GT 4 keyword `(tornado, watch)` aligned with content "National Weather Service tornado watch issued for your tri-county area…"). Contrast C3 attempt-1 where `('pickup', partner_voicemail_ring_pickup_jeweler)` FAILed at run 1 because content used the two-word "pick up" form while the keyword was single-word "pickup". The author-discipline carry-forward from D-C2.attempt2.C → D-C3.attempt1.C → D-C4.attempt1.C is mechanically self-improving — the C3 iteration log surfaced the two-word/one-word failure mode, and C4 attempt-1 author internalized the lesson at draft time. Attribution remains clean: self-restate gate → structural-parsing (audit step 1 territory); Step 3.5 → M8b keyword/content alignment (audit step 2 territory).

### Audit-gate results (8/8 PASS)

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v24')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v24'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v24 9 5 900.0` with no exception. |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 `(kw, content.lower())` substring checks pass (Step 3.5 pre-flight + audit-gate verification both PASS at the single run). Pairs: `(carbon, carbon_monoxide_alarm_evacuate_call_gas_company)`; `(monoxide, carbon_monoxide_alarm_evacuate_call_gas_company)`; `(pediatrician, pediatrician_visit_advanced_today_4pm)`; `(advanced, pediatrician_visit_advanced_today_4pm)`; `(hospital, hospital_grandmother_hip_fracture_next_of_kin_callback)`; `(grandmother, hospital_grandmother_hip_fracture_next_of_kin_callback)`; `(tornado, tornado_watch_tri_county_peak_risk_tonight)`; `(watch, tornado_watch_tri_county_peak_risk_tonight)`; `(disk, disk_space_critical_var_log_api_host_oom_90min)`; `(space, disk_space_critical_var_log_api_host_oom_90min)`. |
| 3a | Banned event_id literal review (vs 154 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v24's 9 event_ids. |
| 3b | Banned theme semantic review (vs 87 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_evidence`. All 5 GT themes pass with distinguishing qualifiers documented vs nearest banned predecessors (sub-cell-distinct for each: urgent-safety CO-basement-evacuation vs C1 natural-gas-leak-kitchen-evacuation + C2 medical-pendant-fall-EMS-callback; schedule-change pediatrician-advance-1pm-deadline vs C1 cardiology-reschedule + C3 court-hearing-same-day-default-risk + M11a Spanish-tutoring-time-shift; message/delivery hospital-grandmother-next-of-kin vs M11a friend-hospitalized-informational + M10b family-airport / personal-6pm / photographer voicemails + C1 legal-courier-signature + C3 partner-jeweler-pickup; weather-alert tornado-watch-tri-county vs C2 flash-flood-King-County + C3 dust-storm-Maricopa-County; production/on-call disk-space-OOM vs C2 datastore-replica-failover-postgres + C3 TLS-cert-expiry-customer-endpoint). |
| 3c | Banned keyword tuple bytewise review (vs 86 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(carbon, monoxide), (pediatrician, advanced), (hospital, grandmother), (tornado, watch), (disk, space)]`. Note semantically-adjacent bytewise-distinct cases: `(fire, alarm)` banned (M8b) + `(gas, leak)` banned (C1) but `(carbon, monoxide)` bytewise-distinct on both elements; `(hospital, mother)` banned (M8b) + `(hospitalized, mike)` banned (M11a test_v12) but `(hospital, grandmother)` bytewise-distinct on second element (`grandmother ≠ mother`) AND bytewise-distinct from `(hospitalized, mike)` on both elements (`hospital ≠ hospitalized` bytewise as keyword tokens); `(appointment, rescheduled)` banned (C1) but `(pediatrician, advanced)` bytewise-distinct on both elements; `(weather, rain)` + `(flood, warning)` + `(dust, storm)` banned but `(tornado, watch)` bytewise-distinct from all on both elements; `(production, alert)` + `(database, failover)` + `(tls, expiry)` banned but `(disk, space)` bytewise-distinct from all on both elements + different fault class. |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical grep of 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21/v22/v23 event_ids: 0 collisions against 154 prior event_ids. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (86 unique across dev_v1..test_v23): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v24 has 640 unique 8-grams across content+briefing+intents fields; prior dev/test traces have 4855 unique 8-grams; overlap = 0. |

### GT-regime classification (audit step 7; for Commit D per-trace observations table)

- GT 1 `carbon_monoxide_alarm_evacuate_call_gas_company` — **urgent safety/security issue (V2 EXISTING YES)**: indoor CO alarm triggered in basement utility room with sensor reading 95 ppm CO (safe threshold 9 ppm) and climbing; evacuate the house immediately with all family members and pets, leave doors open, dial gas company emergency line from outside; do not re-enter until first responders give all-clear.
- GT 2 `pediatrician_visit_advanced_today_4pm` — **schedule change affecting the user personally (V2 EXISTING YES)**: pediatrician's office advances child's 4-year-old wellness visit from Tuesday next week to today 4pm because Dr. Albright had a cancellation before her two-week leave begins tomorrow; 1pm-confirm-or-decline deadline so the slot can be offered to another waitlist family.
- GT 3 `hospital_grandmother_hip_fracture_next_of_kin_callback` — **message or delivery directed personally to the user (V2 EXISTING YES)**: voicemail from St. Vincent's hospital admitting desk — user's grandmother Eleanor admitted via emergency in the last hour with a left hip fracture from a fall at home; she is stable but the chart lists user as next-of-kin proxy; charge nurse Tanya asked for callback to ward 4-North to discuss surgical consent and transfer logistics before evening rounds at 8pm.
- GT 4 `tornado_watch_tri_county_peak_risk_tonight` — **weather alert (V2 EXISTING YES)**: National Weather Service tornado watch issued for tri-county area through 11pm tonight — rotation-supported supercells moving east-northeast at 55 mph with two-inch-diameter hail; peak tornado-development risk window 4pm-9pm; watch is not warning but conditions strongly favor tornado development; review shelter plan, charge devices, monitor radio for upgrades to warnings.
- GT 5 `disk_space_critical_var_log_api_host_oom_90min` — **production/on-call alert (V2 EXISTING YES)**: PagerDuty P2 from infra-mon — disk space critical on api-prod-host-07; /var/log filling at roughly 200 MB per minute due to runaway debug-log flag in new release; current free space 1.4 GB on 40 GB partition; OOM-style kill on request handler projected within 90 minutes if not addressed; user listed primary on storage-rotation runbook this week.

### Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism + V2-class subclause coverage)

**V4 NEW YES coverage at C4:** **NONE** (intentional per D-C4.attempt1.B defensibility framing). Both V4 NEW YES subclauses already covered singularly across C1+C2 (scarcity-bounded-opportunity at C1 `vinyl_drop_press_today`; family-milestone-with-social-cost at C2 `grandpa_90th_birthday_tomorrow`); a third instance at C4 would over-weight V4 NEW YES vs the H4 COMPLIANT_NO_REGRESSION denominator.

**V4 NEW NO coverage at C4:** **NONE** (intentional per D-C4.attempt1.B). All 3 V4 NEW NO subclauses already covered 2x each at C1+C2 (back-in-stock-without-scarcity: C1 `restock_camping_lantern` + C2 `sneakers_wishlist_back_in_stock_email`; recurring-event-calendar-suggestion: C1 `calendar_running_club_recur` + C2 `calendar_coffee_lisa_weekly_suggest`; casual-social-meetup-without-time-pressure: C1 `arcade_meetup_kira` + C2 `pickup_basketball_saturday_open`). 3rd-repeat triangulation (path b) yields less marginal H4 evidence than path (a) at C4; deferred to C5/C6 once V2 NO classes have stable 2x coverage.

**V2 EXISTING YES compliant-content coverage at C4 (5 GTs across 5 distinct V2 YES classes):**
- GT `carbon_monoxide_alarm_evacuate_call_gas_company` tests V2 urgent-safety/security class under NEW specific incident distinct from C1 natural-gas-leak (different gas: CO vs methane; different location: basement-utility-room vs kitchen-sensor; different fault mechanism: combustion-byproduct buildup vs appliance/line leak) and C2 medical-alert-pendant-fall (different incident class: atmospheric hazard household-evacuation vs medical-emergency EMS-dispatch).
- GT `pediatrician_visit_advanced_today_4pm` tests V2 schedule-change class under NEW specific incident distinct from C1 cardiology-rescheduled (different specialty: pediatric-wellness vs cardiology; different direction: advanced-earlier vs rescheduled) and C3 court-hearing-same-day-default-risk (different institution: medical-clinic vs court; different consequence: waitlist-offer vs default-judgment-plus-collection).
- GT `hospital_grandmother_hip_fracture_next_of_kin_callback` tests V2 message/delivery class under NEW specific incident distinct from M11a friend-hospitalized-informational (different urgency: action-required next-of-kin-proxy vs informational-only), M10b family-airport / personal-6pm / photographer voicemails (different caller + different incident), C1 legal-courier-signature (different mode: voicemail vs courier; different subject: hospital-family-medical vs legal-document), C3 partner-jeweler-pickup (different caller: hospital-admit-desk vs partner; different subject: surgical-consent-decision vs personal-errand). Maps to V4 prompt's explicit "hospital calling about a family member" example.
- GT `tornado_watch_tri_county_peak_risk_tonight` tests V2 weather-alert class under NEW specific incident distinct from C2 flash-flood-King-County (different meteorology: tornado-supercell vs flash-flood; different alert-level: watch vs warning; different impact: shelter-in-place vs commute-route) and C3 dust-storm-Maricopa-County (different meteorology: tornado vs dust-storm; different geography: tri-county vs Maricopa-County; different impact: shelter-in-place vs zero-freeway-visibility-driving-hazard).
- GT `disk_space_critical_var_log_api_host_oom_90min` tests V2 production/on-call class under NEW specific incident distinct from C2 database-failover-postgres (different fault class: disk-space-OOM vs DB-replica-failover; different remediation: log-rotation/debug-flag-flip vs DB-promotion; different urgency-mechanism: 90-min-OOM-projection vs 10-min-promotion-ETA) and C3 TLS-cert-expiry-customer-endpoint (different fault class: storage-saturation vs TLS-cert-expiry; different remediation: log-rotation vs cert-manager-renewal; different urgency-mechanism: 90-min-OOM vs 3hr-to-issue-and-deploy).

**V2 EXISTING NO compliant-content distractor coverage at C4 (4 distractors across 4 distinct V2 NO classes; explicit 1x→2x triangulation focus):**
- Distractor `ssl_monitor_weekly_digest_no_rotations_required` tests V2 "routine status, uptime, heartbeat, or 'all systems normal' pings" class at **1x→2x** triangulation (C3 first-covered via `cloud_backup_daily_success_digest`; C4 covers under NEW sub-cell — SSL certificate monitoring vs cloud backup; weekly vs daily cadence; "No action items at this time" vs "All systems normal" framing).
- Distractor `tea_club_monthly_subscriber_tasting_newsletter` tests V2 "marketing, promotional, or newsletter content" class at **1x→2x** triangulation (C3 first-covered via `kitchen_gear_quarterly_digital_magazine`; C4 covers under NEW sub-cell — subscription-box product newsletter for tea vs digital magazine for kitchen gear; monthly subscriber edition vs quarterly digital issue).
- Distractor `evening_briefing_no_pending_items_tomorrow_clear` tests V2 "generic daily briefings that explicitly state no urgent items" class at **1x→2x** triangulation (C3 first-covered via `morning_briefing_no_urgent_items_today`; C4 covers under NEW sub-cell — end-of-day evening briefing vs morning briefing; tomorrow-calendar-clear vs today-no-time-sensitive-items target horizon).
- Distractor `slack_frontend_weekly_community_invite` tests V2 "feature announcements, app updates, or social/channel invites" class at **1x→2x** triangulation on the social-channel-invite subclass (C1 first-covered via `discord_unread_digest`; C4 covers under NEW sub-cell — Slack Frontend Weekly community invite vs Discord unread digest; community-membership-invite sub-cell vs activity-digest sub-cell within social-channel V2 NO class).

**Coverage summary at C4:** Maximal H4 COMPLIANT_NO_REGRESSION evidence-base contribution at a single trace cell with explicit V2 EXISTING NO 1x→2x triangulation lift — 5 V2 EXISTING YES GTs across 5 distinct V2 YES classes (3 of those 5 classes lifted to 3x cross-trace coverage at C4) + 4 V2 EXISTING NO distractors with 4-of-4 slots filling 1x→2x triangulation gaps from C1+C2+C3; zero V4 NEW YES or V4 NEW NO repeats. Cross-trace coverage state through C4: **V4 NEW YES 2/2 subclauses covered** (singular-each via C1+C2); **V4 NEW NO 3/3 subclauses covered** (each 2x via C1+C2 under NEW phrasing); **V2 EXISTING YES classes coverage across C1+C2+C3+C4**: urgent-safety (C1+C2+C4 — 3x), schedule-change (C1+C3+C4 — 3x), financial/deadline (C1+C2+C3 — 3x), message/delivery (C1+C3+C4 — 3x), weather-alert (C2+C3+C4 — 3x), production/on-call (C2+C3+C4 — 3x), discretionary-deadline-V4-YES (C1+C2 — 2x); **V2 EXISTING NO classes coverage across C1+C2+C3+C4**: routine-status/heartbeat (C3+C4 — 2x), marketing/newsletter (C3+C4 — 2x), generic-daily-briefing-explicitly-no-urgent (C3+C4 — 2x), feature-announcement/app-update (C2+C3 — 2x), social-channel-invite (C1+C4 — 2x). All 5 V2 EXISTING NO classes lifted to 2x cross-trace coverage at C4 (versus C3 end-state where 3 of 5 were at 1x). 6 traces remain for combined-N=20 closure; future C5..C10 may shift away from path (a) toward V4 NEW NO 3rd-repeat triangulation (path b) now that V2 NO 1x cells are saturated.

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v24-attempt-1-accepted.json` (SHA256 `8ac04d97835015bdbeef4199cd6be918954b3343e6edd2dff9749acccd38be06`; 33634 bytes; full audit-gate evidence + Step 3.5 pre-flight first-run-PASS log + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata archived).

### Banned-list state delta at C4

- Pre-C4 (C3 end-state, ships at C4): 154 IDs / 87 themes / 86 tuples.
- C4 contributions from accepted test_v24 (to be incorporated into `21c-banned-list-pre-c5.txt` at C5 land time per D-C1.1):
  - **+9 IDs:** `carbon_monoxide_alarm_evacuate_call_gas_company`, `pediatrician_visit_advanced_today_4pm`, `hospital_grandmother_hip_fracture_next_of_kin_callback`, `tornado_watch_tri_county_peak_risk_tonight`, `disk_space_critical_var_log_api_host_oom_90min`, `ssl_monitor_weekly_digest_no_rotations_required`, `tea_club_monthly_subscriber_tasting_newsletter`, `evening_briefing_no_pending_items_tomorrow_clear`, `slack_frontend_weekly_community_invite`.
  - **+5 themes (GT-regime regime column verbatim):** urgent safety/security issue (V2 EXISTING YES) — indoor carbon monoxide alarm in basement utility room with 95 ppm sensor reading and household-evacuation imperative + gas company emergency dial; schedule change affecting the user personally (V2 EXISTING YES) — pediatrician's office advances child's 4yo wellness visit from next-Tuesday to today-4pm at provider request with 1pm-confirm-or-decline deadline; message or delivery directed personally to the user (V2 EXISTING YES) — St. Vincent's hospital admitting-desk voicemail about grandmother's hip-fracture admission with next-of-kin proxy + surgical-consent decision before 8pm rounds; weather alert (V2 EXISTING YES) — NWS tornado watch for tri-county area with rotation-supported supercells at 55mph + 2-inch hail + peak risk 4-9pm tonight; production/on-call alert (V2 EXISTING YES) — PagerDuty P2 disk-space critical on api-prod-host-07 with /var/log filling at 200MB/min and 90-min OOM-projection on storage-rotation runbook.
  - **+5 tuples (GT keyword tuples verbatim):** `(carbon, monoxide)`, `(pediatrician, advanced)`, `(hospital, grandmother)`, `(tornado, watch)`, `(disk, space)`.
- Post-C4 (input state for C5): 163 IDs / 92 themes / 91 tuples. File ships at C5 land time as `runs/data/21c-banned-list-pre-c5.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C4

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at the accepting attempt).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (5 cumulative milestone attempts < 25; 4 accepted traces toward target of 10).
- Retry-cap-3 on test_v24 (D-C1.5 #3): **not exhausted** (1/3 used; PASS at attempt #1 / 2 retries remaining had attempt #1 not accepted).

### Cumulative milestone-spend through Commit C4

Commit C4 spend: $0 at attempt #1 (in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C4: $0.7081 (unchanged from Commit C3; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C4 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21 + test_v22 + test_v23 definitions — frozen historical artifacts (only NEW `test_trace_v24` added at C4, plus the registry line `"test_v24": test_trace_v24,`).
- `runs/data/21c-banned-list-pre-c{1,2,3}.{txt,json}` + `runs/data/21c-author-test_v{21,22,23}-*.json` — frozen at C1+C2+C3; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C4.

### Next: Commit C5 — fresh-session trace authoring `test_v25`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c5.{txt,json}` (NEW; reflects test_v21 + test_v22 + test_v23 + test_v24 contributions; 163 IDs / 92 themes / 91 tuples) as the pre-C5 starting state. Self-restate gate rendered against the pre-C5 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 5/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C) carries forward as standing per-attempt author discipline. With C4 lifting all 5 V2 EXISTING NO classes to 2x cross-trace coverage, C5 may shift toward path (b) V4 NEW NO 3rd-repeat triangulation OR continue path (a) compliant-content discipline at 3x V2 EXISTING NO; defended at the C5 Plan.

Commit C5 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.

---

## Commit C5 — test_v25 (2026-05-17)

**Verdict: test_v25 ACCEPTED at attempt 1/3; audit-gate 8/8 PASS.** Cumulative milestone attempt count 6/25 through Commit C5 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2 + C3 attempt-1 + C4 attempt-1 + C5 attempt-1); 5 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at this attempt (M11a-extension structural-parsing-failure rate to date: 0/6 attempts). Step 3.5 pre-flight keyword literal-substring verification (D-C5.attempt1.C inheriting verbatim from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C) PASSed on first run with no in-session iteration required — mirrors C4 attempt-1 first-run PASS precedent; content was authored with explicit single-word keyword-substring attention at draft time.

### C-protocol governance decisions inherited from C1 + C2 + C3 + C4

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) inherit VERBATIM at C5 with no re-litigation per "no scope drift within a milestone" operating principle. D-C2.A..D-C2.D (locked at C2 attempt-#1 Plan) + D-C2.attempt2.A..D-C2.attempt2.D (locked at C2 attempt-#2 Plan `f9808c8`) + D-C3.attempt1.A..D-C3.attempt1.D (locked at C3 attempt-#1 Plan `9f84a01`) + D-C4.attempt1.A..D-C4.attempt1.D (locked at C4 attempt-#1 Plan `e998a07`) also inherit VERBATIM at C5. The per-attempt author discipline added at C2 attempt #2 (Step 3.5 pre-flight) carries forward as standing author discipline through C5..C10.

### C5 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C5.attempt1.A state-confirm checklist** | Pre-attempt-#1 state confirmed via on-disk verifications: main HEAD `e998a07` (M11a-extension Commit C4); working tree clean; `sandbox/event_trace.py` sha256 `f99a4f8ccb491c47ba877445087730d58a94fbe81396520b6e02f78a994e74d1` (69666 bytes; HEAD-bit-identical post-C4 incl. `test_trace_v24` + registry line); V4 prompt string sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; bytewise-identical to §D1 lock — `agent/arbiter.py` last touched at `adc1cba` Commit B, unchanged through C1+C2+C3+C4); `runs/data/21c-banned-list-pre-c4.{txt,json}` sha256 `0fe5c277…` + `24aced60…` / 154/87/86 counts verified. D-C4.attempt1.A precedent mirrored verbatim. |
| **D-C5.attempt1.B subclause coverage brief inheritance + C5-specific path-lock** | D-C2.B / D-C3.attempt1.B / D-C4.attempt1.B brief inherits VERBATIM. C5-specific path-lock (locked at Plan): **PATH (c)** — V4 NEW YES 3rd-repeat triangulation under the family-milestone-with-social-cost subclause + 4 V2 EXISTING YES + 4 V2 EXISTING NO compliant-content. Trace shape: 1 V4 NEW YES GT (parents' 50th wedding anniversary milestone dinner with toast obligation + siblings traveling in for one-evening-only joint marriage milestone) + 4 V2 EXISTING YES GTs across urgent-safety + schedule-change + financial/deadline + production/on-call (each lifting 3x→4x cross-trace) + 4 V2 EXISTING NO distractors across routine-status + marketing/newsletter + generic-daily-briefing + feature-announcement (each lifting 2x→3x). Defensibility framing: V4 NEW YES was the asymmetrically-weakest mechanism-evidence cell at C4 end (2 instances vs V4 NEW NO 6); 3rd-instance lift (2→3 total V4 NEW YES) is strictly higher marginal info than 3rd-repeat V4 NEW NO (6→7) at the same trace cost. Family-milestone subclass picked over scarcity-bounded because it is the closer cross-trace analog to M11a test_v8's mom_birthday_heads_up residual cell — the V4 prompt's literal named target for V2-enumeration-limit closure on discretionary-social family obligations. Path (a) deferred to later C-steps; path (b) deferred indefinitely (V4 NEW NO 6 already saturated); path (d) skipped per C4-discussed reviewer-flag risk. Skipped at C5 V2 NO class: social-channel-invite (stays at 2x; C6+ lift). |
| **D-C5.attempt1.C Step 3.5 pre-flight keyword literal-substring verification** | Inherits VERBATIM from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C. Mechanically verify every GT keyword tuple element appears as case-insensitive substring of that GT's Event.content via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v25'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Does NOT consume retry-cap budget per D-C1.4. |
| **D-C5.attempt1.D commit shape** | D-C4.attempt1.D commit shape inherits VERBATIM with normal attempt-#1-accepts trajectory (no rejected-attempt bundling since attempt #1 accepted). |

### Banned-list starting state (C4 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c5.txt` (SHA256 `62065485743afa7a264a345857b18dcc1a882e2065359fe95ccd43541467514b`; 16162 bytes; 163 banned event_ids + 92 banned themes + 91 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c5.json` (SHA256 `baee65241a78bf07d9a3a33c96321e45c06e1b32ca2b28f72800071405fd2162`; 15859 bytes; same content in structured schema; counts mechanically verified unique).
- Provenance: extended at C5-attempt-#1 session by appending C4's accepted test_v24 contributions (+9 IDs / +5 themes / +5 tuples) to the pre-C4 banned-list (`0fe5c277…` / `24aced60…`, 154/87/86) per D-C1.1 invariant. Pre-C4 files NOT mutated (verified bit-identical pre and post C5 authoring).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c5.txt > /tmp/m11a-ext-c5-restate-prompt.txt`
- Rendered prompt SHA256: `511d3ff4d2cc566c640757e01a9b9e35d37fe31b96b8f69ed892ef53520c062f` (16571 bytes).
- Self-restate response authored in own words distinct from C1's response + C2 attempt-#1's response + C2 attempt-#2's response + C3 attempt-#1's response + C4 attempt-#1's response per fresh-session-restart-from-scratch discipline; full text archived verbatim in artifact `21c-author-test_v25-attempt-1-accepted.json` `self_restate_response_verbatim` field.
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered; schema check via `get_trace('test_v25')` passes on first import.

### Step 3.5 pre-flight keyword literal-substring verification (D-C5.attempt1.C; first-run PASS)

| Run | Outcome | Detail |
|---|---|---|
| 1 | **PASS** — all 10 pairs print `True` | `('anniversary', parents_fiftieth_anniversary_dinner_tomorrow_toast_request) True; ('fiftieth', parents_fiftieth_anniversary_dinner_tomorrow_toast_request) True; ('medication', child_medication_ingestion_poison_control_emergency_call) True; ('ingestion', child_medication_ingestion_poison_control_emergency_call) True; ('dental', dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency) True; ('implant', dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency) True; ('quarterly', quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm) True; ('tax', quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm) True; ('redis', redis_memory_saturation_eviction_cascade_120min_outage_risk) True; ('memory', redis_memory_saturation_eviction_cascade_120min_outage_risk) True`. No in-session iteration required. |

**Reviewer-defense (Step 3.5 working as designed):** Step 3.5 PASSed on first run for C5, mirroring C4 attempt-1's first-run PASS precedent (vs C3 attempt-1's in-session iteration on `('pickup', partner_voicemail_ring_pickup_jeweler)` two-word/one-word misalignment). Content authored with explicit single-word keyword-substring attention at draft time: `("anniversary", "fiftieth")` aligned with "fiftieth wedding anniversary dinner"; `("medication", "ingestion")` aligned with "the medication bottle to the emergency room" + "Estimated ingestion under twenty minutes ago"; `("dental", "implant")` aligned with "your dental implant procedure"; `("quarterly", "tax")` aligned with "Q3 quarterly estimated tax payment"; `("redis", "memory")` aligned with "redis-prod-cluster-01 memory saturation". Discipline carry-forward from D-C2.attempt2.C → D-C3.attempt1.C → D-C4.attempt1.C → D-C5.attempt1.C remains mechanically self-improving; attribution clean: self-restate gate → structural-parsing (audit step 1 territory); Step 3.5 → M8b keyword/content alignment (audit step 2 territory).

### Audit-gate results (8/8 PASS)

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v25')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v25'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v25 9 5 1000.0` with no exception. |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 `(kw, content.lower())` substring checks pass (Step 3.5 pre-flight + audit-gate verification both PASS at the single run). Pairs: `(anniversary, parents_fiftieth_anniversary_dinner_tomorrow_toast_request)`; `(fiftieth, parents_fiftieth_anniversary_dinner_tomorrow_toast_request)`; `(medication, child_medication_ingestion_poison_control_emergency_call)`; `(ingestion, child_medication_ingestion_poison_control_emergency_call)`; `(dental, dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency)`; `(implant, dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency)`; `(quarterly, quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm)`; `(tax, quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm)`; `(redis, redis_memory_saturation_eviction_cascade_120min_outage_risk)`; `(memory, redis_memory_saturation_eviction_cascade_120min_outage_risk)`. |
| 3a | Banned event_id literal review (vs 163 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v25's 9 event_ids. |
| 3b | Banned theme semantic review (vs 92 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_banned_theme_semantic_review`. All 5 GT themes pass with distinguishing qualifiers vs nearest banned predecessors: GT1 V4 NEW YES family-milestone parents'-50th-anniversary distinct from C2 grandpa-90th-birthday + M10b test_v8 mom-birthday on family-tier + milestone-type + social-cost-mechanism; GT2 urgent-safety child-medication-ingestion distinct from C1 gas-leak + C2 medical-pendant + C4 CO-alarm on fault class + patient + protocol; GT3 schedule-change dental-implant-surgery-rescheduled distinct from C1 cardio + C3 court + C4 pediatrician on specialty + direction + procedure type + consequence; GT4 financial/deadline IRS-Q3-quarterly-estimated-tax distinct from C1 student-loan + C2 property-tax + C3 homeowner-insurance on tax type + penalty mechanism + counterparty; GT5 production/on-call redis-memory-saturation distinct from C2 DB-failover + C3 TLS-cert + C4 disk-space on tier + fault mechanism + urgency window + runbook. |
| 3c | Banned keyword tuple bytewise review (vs 91 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(anniversary, fiftieth), (medication, ingestion), (dental, implant), (quarterly, tax), (redis, memory)]`. Note semantically-adjacent bytewise-distinct cases: `(mother, birthday)` + `(grandpa, birthday)` banned but `(anniversary, fiftieth)` bytewise-distinct on both elements; `(dentist, cancelled)` banned (M8b) but `(dental, implant)` bytewise-distinct on both; `(deadline, quarterly)` + `(property, tax)` + `(tax, expires)` banned but `(quarterly, tax)` bytewise-distinct from all (different order vs `(deadline, quarterly)`, different first-element vs `(property, tax)`, different second-element + order vs `(tax, expires)`); `(database, failover)` + `(disk, space)` + `(production, alert)` + `(tls, expiry)` banned production/on-call tuples but `(redis, memory)` bytewise-distinct on both elements vs all four; `(prescription, refill)` banned but `(medication, ingestion)` bytewise-distinct on both. |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical grep of 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21..v24 event_ids: 0 collisions against 163 prior event_ids. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (91 unique across dev_v1..test_v24): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v25 has 679 unique 8-grams across content+briefing+intents fields; prior dev/test traces have 3471 unique 8-grams; overlap = 0. |

### GT-regime classification (audit step 7; for Commit D per-trace observations table)

- GT 1 `parents_fiftieth_anniversary_dinner_tomorrow_toast_request` — **discretionary-deadline obligation (V4 NEW YES, family-milestone-with-social-cost subclass)**: proactive heads-up about parents' fiftieth milestone wedding anniversary dinner tomorrow night with explicit toast obligation + two siblings flying in from Seattle and Boston for one-evening-only joint marriage milestone + tomorrow-noon confirm deadline so the venue can finalize seating.
- GT 2 `child_medication_ingestion_poison_control_emergency_call` — **urgent safety/security issue (V2 EXISTING YES)**: accidental ingestion by three-year-old of migraine antihistamines under 20 minutes ago with Poison Control directive to bring child + medication bottle directly to ER (do not induce vomiting) + ER triage expecting callback with weight estimate.
- GT 3 `dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency` — **schedule change affecting the user personally (V2 EXISTING YES)**: dental implant procedure scheduled for tomorrow 8am pushed to next week 7am (Wednesday) or following Thursday 11am at oral surgeon request (emergency surgery for another patient this evening) + 6pm-today-confirm-or-lose-anesthesia-booking deadline.
- GT 4 `quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm` — **financial/deadline obligation (V2 EXISTING YES)**: IRS Q3 quarterly estimated tax payment due 5pm-ET today via EFTPS for the 1040-ES installment covering July-September + underpayment-penalty calculation back to April safe-harbor anchor + 0.5%/month late charge on the shortfall + 8pm ACH cutoff for next-day settlement.
- GT 5 `redis_memory_saturation_eviction_cascade_120min_outage_risk` — **production/on-call alert (V2 EXISTING YES)**: PagerDuty P1 redis-prod-cluster-01 memory saturation at 13.4 GB of 14 GB allocation + allkeys-lru eviction policy throwing OOM errors back to API gateway at 200 evictions/sec + session-cache hit rate collapsed 98%→41% over 10 minutes + queue depth climbing + full session outage projected within 120 minutes if working set hits 14 GB hard cap; user listed primary on cache-tier runbook this week.

### Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism + V2-class subclause coverage)

**V4 NEW YES coverage at C5:** **1 instance** under family-milestone-with-social-cost subclause (`parents_fiftieth_anniversary_dinner_tomorrow_toast_request`). Lifts that subclause cross-trace coverage 1x→2x (C2 grandpa_90th_birthday_tomorrow + C5 parents_fiftieth_anniversary_dinner); lifts total V4 NEW YES cross-trace instance count from 2 to 3. **Defensibility:** V4 NEW YES was the asymmetrically-weakest mechanism-evidence cell at C4 end (2 instances vs V4 NEW NO 6 total instances); a 50% lift on the weaker side strengthens MECHANISM_CONFIRM more than a 17% lift on the stronger side would. Family-milestone subclass picked over scarcity-bounded because it is the closer cross-trace analog to M11a test_v8's `mom_birthday_heads_up` residual cell — the V4 prompt's literal named target for V2-enumeration-limit closure on discretionary-social family obligations.

**V4 NEW NO coverage at C5:** **NONE** (intentional per D-C5.attempt1.B locked path-(c) choice). All 3 V4 NEW NO subclauses already 2x each at C1+C2; total 6 V4 NEW NO instances cross-trace post-C2. The diminishing-marginal-info argument from C3+C4 inverts at C5 only for the V4 NEW YES side because of the asymmetric-weakness situation; V4 NEW NO 6→7 would not move the symmetric-evidence needle.

**V2 EXISTING YES compliant-content coverage at C5 (4 GTs across 4 distinct V2 YES classes; each 3x→4x):**
- GT `child_medication_ingestion_poison_control_emergency_call` tests V2 urgent-safety/security class under NEW within-class incident distinct from C1 gas-leak (different fault: medication-ingestion vs atmospheric gas leak), C2 medical-pendant-fall (different patient: toddler vs elderly father; different protocol: Poison Control + ER transport vs auto-EMS-dispatch + medical-pendant), C4 carbon-monoxide (different fault: medication ingestion vs CO atmospheric poisoning; different response: ER transport vs evacuation + gas company emergency dial). **3x→4x cross-trace lift** (C1+C2+C4+C5).
- GT `dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency` tests V2 schedule-change class under NEW within-class incident distinct from C1 cardio-appt-rescheduled (different specialty: dental implant surgery vs cardiology follow-up; different procedure: surgical vs office visit; different consequence: lose-anesthesia-booking + next-month-queue vs unspecified), C3 court-hearing-moved (different institution: medical vs court; different direction: next-week-pushed vs same-day-advanced), C4 pediatrician-advanced (different specialty + patient + direction + procedure). **3x→4x cross-trace lift** (C1+C3+C4+C5).
- GT `quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm` tests V2 financial/deadline class under NEW within-class incident distinct from C1 student-loan-resume (different obligation: federal income estimated tax vs federal student loan IDR), C2 property-tax-installment (different tax type: federal income vs county property; different penalty: underpayment-calculation vs 10% flat-late), C3 homeowner-insurance-lapse (different obligation type: estimated tax vs lapsed insurance remediation; different timeline: 5pm-today vs 72-hour-window). **3x→4x cross-trace lift** (C1+C2+C3+C5).
- GT `redis_memory_saturation_eviction_cascade_120min_outage_risk` tests V2 production/on-call class under NEW within-class incident distinct from C2 datastore-replica-failover (different tier: cache vs DB; different fault: memory saturation + eviction cascade vs replica failover; different remediation: cache-restart/eviction-adjustment vs DB-promotion; different urgency window: 120-min full-outage vs 10-min replica promotion ETA), C3 TLS-cert-expiry (different fault class: memory saturation vs TLS-cert; different remediation), C4 disk-space-critical (different resource: RAM/cache vs disk; different rate: `200 evictions per second` vs `200 MB per minute`; different urgency window: 120-min full-outage vs 90-min disk-OOM; different runbook: cache-tier vs storage-rotation). **3x→4x cross-trace lift** (C2+C3+C4+C5).

**V2 EXISTING NO compliant-content distractor coverage at C5 (4 distractors across 4 distinct V2 NO classes; each 2x→3x):**
- Distractor `kubernetes_autoscaler_monthly_cluster_health_report_nominal` tests V2 routine-status/heartbeat class at **2x→3x** triangulation (C3 cloud_backup_daily + C4 ssl_monitor_weekly + C5 K8s-autoscaler-monthly; distinct on platform, cadence, and infra-domain).
- Distractor `inkwell_indie_bookstore_quarterly_preorder_catalog_winter` tests V2 marketing/newsletter class at **2x→3x** triangulation (C3 kitchen_gear_quarterly_digital_magazine + C4 tea_club_monthly_subscriber + C5 indie-bookstore-quarterly-preorder; distinct on product category, commerce model, cadence).
- Distractor `friday_weekly_recap_briefing_no_outstanding_items` tests V2 generic-daily-briefing class at **2x→3x** triangulation (C3 morning-briefing + C4 evening-briefing + C5 weekly-Friday-recap; distinct on cadence and target horizon).
- Distractor `vscode_marketplace_verified_publisher_tab_launch_announcement` tests V2 feature-announcement/app-update class at **2x→3x** triangulation (C2 chrome-extension-marketplace-update + C3 notion-dashboard-feature-tour + C5 VS-Code-verified-publisher-tab; distinct on product, feature type, update class).

**V2 NO class skipped at C5:** social-channel-invite stays at 2x (C1 discord + C4 slack_frontend_weekly_community_invite). C5 path-(c) selected 4 of 5 V2 NO classes for the 2x→3x triangulation lift; the 5th can lift at C6..C10.

**Coverage summary at C5:** Maximal MECHANISM_CONFIRM evidence-base lift on the asymmetrically-weakest V4 mechanism cell (V4 NEW YES family-milestone 1x→2x; total V4 NEW YES 2→3) + 4 V2 EXISTING YES classes lifted 3x→4x + 4 V2 EXISTING NO classes lifted 2x→3x. Cross-trace coverage state through C5: **V4 NEW YES**: 3 total instances (scarcity-bounded 1x at C1; family-milestone 2x at C2+C5); **V4 NEW NO**: 6 total instances (3 subclauses × 2x each at C1+C2); **V2 EXISTING YES classes**: urgent-safety 4x (C1+C2+C4+C5), schedule-change 4x (C1+C3+C4+C5), financial/deadline 4x (C1+C2+C3+C5), production/on-call 4x (C2+C3+C4+C5), message/delivery 3x (C1+C3+C4), weather-alert 3x (C2+C3+C4); **V2 EXISTING NO classes**: routine-status 3x (C3+C4+C5), marketing/newsletter 3x (C3+C4+C5), generic-daily-briefing 3x (C3+C4+C5), feature-announcement 3x (C2+C3+C5), social-channel-invite 2x (C1+C4). 5 traces remain for combined-N=20 closure; future C6..C10 may continue path (a) compliant-content discipline (4x→5x on 3x-class candidates) OR pursue social-channel-invite 2x→3x lift OR pursue 2nd V4 NEW YES under scarcity-bounded subclass.

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v25-attempt-1-accepted.json` (SHA256 `69a1d4b7af877d7e02f1df4fa8ea320e4a27b80db2971eb94b1d983cd8d06dc1`; 33453 bytes; D-C1.2 schema with step_3_5_pre_flight first-run-PASS log + V4 NEW YES + V2 EXISTING YES/NO compliant-content coverage with explicit asymmetric-weakness defense + 3x→4x V2 YES lift + 2x→3x V2 NO lift + full audit-gate evidence + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata).

### Banned-list state delta at C5

- Pre-C5 (C4 end-state, ships at C5): 163 IDs / 92 themes / 91 tuples.
- C5 contributions from accepted test_v25 (to be incorporated into `21c-banned-list-pre-c6.txt` at C6 land time per D-C1.1):
  - **+9 IDs:** `parents_fiftieth_anniversary_dinner_tomorrow_toast_request`, `child_medication_ingestion_poison_control_emergency_call`, `dental_implant_surgery_rescheduled_tomorrow_8am_surgeon_emergency`, `quarterly_estimated_tax_q3_payment_eod_irs_penalty_5pm`, `redis_memory_saturation_eviction_cascade_120min_outage_risk`, `kubernetes_autoscaler_monthly_cluster_health_report_nominal`, `inkwell_indie_bookstore_quarterly_preorder_catalog_winter`, `friday_weekly_recap_briefing_no_outstanding_items`, `vscode_marketplace_verified_publisher_tab_launch_announcement`.
  - **+5 themes (GT-regime regime column verbatim):** discretionary-deadline obligation (V4 NEW YES, family-milestone-with-social-cost subclass) — parents' fiftieth milestone wedding anniversary dinner tomorrow with toast obligation + multi-sibling travel-in for one-evening-only joint marriage milestone + tomorrow-noon confirm; urgent safety/security issue (V2 EXISTING YES) — accidental three-year-old ingestion of migraine antihistamines under 20 minutes ago with Poison Control directive to bring child + medication bottle directly to ER; schedule change affecting the user personally (V2 EXISTING YES) — dental implant procedure pushed from tomorrow 8am to next week 7am at oral surgeon request with 6pm-confirm-or-lose-anesthesia-booking deadline; financial/deadline obligation (V2 EXISTING YES) — IRS Q3 quarterly estimated tax payment due 5pm-ET today via EFTPS + underpayment-penalty calculation back to April safe-harbor + 0.5%/month late charge; production/on-call alert (V2 EXISTING YES) — PagerDuty P1 redis-prod-cluster-01 memory saturation at 13.4 GB / 14 GB cap with allkeys-lru eviction policy throwing OOM errors at 200 evictions/sec + session-cache hit rate collapse + 120-min full-outage projection.
  - **+5 tuples (GT keyword tuples verbatim):** `(anniversary, fiftieth)`, `(medication, ingestion)`, `(dental, implant)`, `(quarterly, tax)`, `(redis, memory)`.
- Post-C5 (input state for C6): 172 IDs / 97 themes / 96 tuples. File ships at C6 land time as `runs/data/21c-banned-list-pre-c6.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C5

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at the accepting attempt).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (6 cumulative milestone attempts < 25; 5 accepted traces toward target of 10).
- Retry-cap-3 on test_v25 (D-C1.5 #3): **not exhausted** (1/3 used; PASS at attempt #1 / 2 retries remaining had attempt #1 not accepted).

### Cumulative milestone-spend through Commit C5

Commit C5 spend: $0 at attempt #1 (in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C5: $0.7081 (unchanged from Commit C4; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C5 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21 + test_v22 + test_v23 + test_v24 definitions — frozen historical artifacts (only NEW `test_trace_v25` added at C5, plus the registry line `"test_v25": test_trace_v25,`).
- `runs/data/21c-banned-list-pre-c{1,2,3,4}.{txt,json}` + `runs/data/21c-author-test_v{21,22,23,24}-*.json` — frozen at C1+C2+C3+C4; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C5.

### Next: Commit C6 — fresh-session trace authoring `test_v26`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c6.{txt,json}` (NEW; reflects test_v21 + test_v22 + test_v23 + test_v24 + test_v25 contributions; 172 IDs / 97 themes / 96 tuples) as the pre-C6 starting state. Self-restate gate rendered against the pre-C6 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 6/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C) carries forward as standing per-attempt author discipline. With C5 lifting V4 NEW YES family-milestone subclause to 2x cross-trace coverage (asymmetric-weakness gap closed) + 4 V2 EXISTING YES classes to 4x + 4 V2 EXISTING NO classes to 3x, C6 may pursue (1) scarcity-bounded V4 NEW YES 1x→2x for symmetric V4 NEW YES subclause closure, (2) social-channel-invite V2 NO 2x→3x lift to complete the V2 NO triangulation table, or (3) continue compliant-content discipline at remaining 3x classes (message/delivery + weather-alert); defended at the C6 Plan.

Commit C6 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.


## Commit C6 — test_v26 (2026-05-18)

**Verdict: test_v26 ACCEPTED at attempt 1/3; audit-gate 8/8 PASS.** Cumulative milestone attempt count 7/25 through Commit C6 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2 + C3 attempt-1 + C4 attempt-1 + C5 attempt-1 + C6 attempt-1); 4 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at this attempt (M11a-extension structural-parsing-failure rate to date: 0/7 attempts). Step 3.5 pre-flight keyword literal-substring verification (D-C6.attempt1.C inheriting verbatim from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C) PASSed on first run with no in-session iteration required — mirrors C4 + C5 attempt-1 first-run-PASS precedents; content was authored with explicit single-word keyword-substring attention at draft time.

### C-protocol governance decisions inherited from C1 + C2 + C3 + C4 + C5

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) inherit VERBATIM at C6 with no re-litigation per "no scope drift within a milestone" operating principle. D-C2.A..D-C2.D (locked at C2 attempt-#1 Plan) + D-C2.attempt2.A..D-C2.attempt2.D (locked at C2 attempt-#2 Plan `f9808c8`) + D-C3.attempt1.A..D-C3.attempt1.D (locked at C3 attempt-#1 Plan `9f84a01`) + D-C4.attempt1.A..D-C4.attempt1.D (locked at C4 attempt-#1 Plan `e998a07`) + D-C5.attempt1.A..D-C5.attempt1.D (locked at C5 attempt-#1 Plan `b349b23`) also inherit VERBATIM at C6. The per-attempt author discipline added at C2 attempt #2 (Step 3.5 pre-flight) carries forward as standing author discipline through C6..C10.

### C6 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C6.attempt1.A state-confirm checklist** | Pre-attempt-#1 state confirmed via on-disk verifications: main HEAD `b349b23` (M11a-extension Commit C5); working tree clean; `sandbox/event_trace.py` sha256 `624efc600058782d7950ab72033283c39ab86b24de1b9d7292f5260a05a8efc9` (76743 bytes; HEAD-bit-identical post-C5 incl. `test_trace_v25` + registry line); V4 prompt string sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; bytewise-identical to §D1 lock — `agent/arbiter.py` last touched at `adc1cba` Commit B, unchanged through C1+C2+C3+C4+C5); `runs/data/21c-banned-list-pre-c5.{txt,json}` sha256 `62065485…` + `baee6524…` / 163/92/91 counts verified. D-C5.attempt1.A precedent mirrored verbatim. |
| **D-C6.attempt1.B subclause coverage brief inheritance + C6-specific path-lock** | D-C2.B / D-C3.attempt1.B / D-C4.attempt1.B / D-C5.attempt1.B brief inherits VERBATIM. C6-specific path-lock (locked at Plan): **PATH (c)** — V4 NEW YES 2nd-subclause symmetric closure: lift scarcity-bounded-opportunity subclause 1x→2x (total V4 NEW YES 3→4); closes the within-V4-NEW-YES asymmetry C5 opened (family-milestone 2x vs scarcity-bounded 1x). Trace shape: 1 V4 NEW YES GT (Lagavulin distillery 2002 single-cask member-allocation 38-min queue offer + 312-bottle limit + position-47 hold) + 4 V2 EXISTING YES GTs across message/delivery + weather-alert + urgent-safety + financial/deadline (message/delivery + weather-alert lifting 3x→4x; urgent-safety + financial/deadline lifting 4x→5x) + 4 V2 EXISTING NO distractors (social-channel-invite 2x→3x completing V2 NO triangulation table at ≥3x for ALL 5 V2 NO classes; routine-status + marketing/newsletter + generic-daily-briefing each lifting 3x→4x). Defensibility framing: MECHANISM_CONFIRM is the PRIMARY outcome predicate (D7 row identification strict-5/5 per D14-H3); V4 NEW YES is its load-bearing mechanism evidence. C5 closed the cross-V4-mechanism asymmetric-weakness gap (V4 NEW YES 2→3) but OPENED a new within-V4-NEW-YES asymmetry (family-milestone 2x vs scarcity-bounded 1x); that within-subclass asymmetry is the new asymmetrically-weakest mechanism-evidence cell at C5 end. Symmetric closure at 2x each yields strongest reviewer-defensible "all V4 NEW YES subclauses tested ≥2x AND total V4 NEW YES instances at 4" claim. Path (a) deferred cleanly to C7 (social-channel-invite 2x→3x done here as accompanying compliant-content but not the primary lever; full path-(a) compliant-content focus picks up at C7); path (b) explicitly rejected (V4 NEW NO 6 already saturated; 3rd-repeat dominated by H4 denominator growth); path (d) explicitly rejected (5-GT-under-one-V2-class trace shape over-weights one class at single-trace scope). Skipped at C6 V2 NO class: feature-announcement/app-update (stays at 3x; C7+ lift candidate). |
| **D-C6.attempt1.C Step 3.5 pre-flight keyword literal-substring verification** | Inherits VERBATIM from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C. Mechanically verify every GT keyword tuple element appears as case-insensitive substring of that GT's `Event.content` via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v26'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Does NOT consume retry-cap budget per D-C1.4. |
| **D-C6.attempt1.D commit shape** | D-C5.attempt1.D commit shape inherits VERBATIM with normal attempt-#1-accepts trajectory (no rejected-attempt bundling since attempt #1 accepted). |

### Banned-list starting state (C5 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c6.txt` (SHA256 `c1b782d0745599c1b40c7880f0beacca62d9d253d57209b32321533835c4e3f6`; 18275 bytes; 172 banned event_ids + 97 banned themes + 96 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c6.json` (SHA256 `a411ad0a19356205121fec7ccb6b7801f8a4c79044a180e37fa24cb0151f1ad4`; 17993 bytes; same content in structured schema; counts mechanically verified unique).
- Provenance: extended at C6-attempt-#1 session by appending C5's accepted test_v25 contributions (+9 IDs / +5 themes / +5 tuples) to the pre-C5 banned-list (`62065485…` / `baee6524…`, 163/92/91) per D-C1.1 invariant. Pre-C5 files NOT mutated (verified bit-identical pre and post C6 authoring).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c6.txt > /tmp/m11a-ext-c6-restate-prompt.txt`
- Rendered prompt SHA256: `ad0ac2d312f784b052fb71919767458fa3ed0d94ef68d0cd3dd3ef9d409f7de9` (18684 bytes).
- Self-restate response authored in own words distinct from C1's response + C2 attempt-#1's response + C2 attempt-#2's response + C3 attempt-#1's response + C4 attempt-#1's response + C5 attempt-#1's response per fresh-session-restart-from-scratch discipline; full text archived verbatim in artifact `21c-author-test_v26-attempt-1-accepted.json` `self_restate_response_verbatim` field.
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered; schema check via `get_trace('test_v26')` passes on first import.

### Step 3.5 pre-flight keyword literal-substring verification (D-C6.attempt1.C; first-run PASS)

| Run | Outcome | Detail |
|---|---|---|
| 1 | **PASS** — all 10 pairs print `True` | `('lagavulin', lagavulin_single_cask_allocation_38min_window_distillery) True; ('allocation', lagavulin_single_cask_allocation_38min_window_distillery) True; ('chemo', mother_in_law_chemo_infusion_ride_request_voicemail_6pm) True; ('infusion', mother_in_law_chemo_infusion_ride_request_voicemail_6pm) True; ('wildfire', wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter) True; ('smoke', wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter) True; ('iso', iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying) True; ('exercise', iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying) True; ('anaphylaxis', partner_anaphylaxis_epipen_911_dispatched_second_dose_needed) True; ('epipen', partner_anaphylaxis_epipen_911_dispatched_second_dose_needed) True`. No in-session iteration required. |

**Reviewer-defense (Step 3.5 working as designed):** Step 3.5 PASSed on first run for C6, mirroring C4 + C5 attempt-1 first-run-PASS precedents (vs C3 attempt-1's in-session iteration on `('pickup', partner_voicemail_ring_pickup_jeweler)` two-word/one-word misalignment). Content authored with explicit single-word keyword-substring attention at draft time: `("lagavulin", "allocation")` aligned with "Lagavulin distillery cask-share allocation notice"; `("chemo", "infusion")` aligned with "chemo infusion is at eight in the morning"; `("wildfire", "smoke")` aligned with "Hazelnut Ridge wildfire smoke plume"; `("iso", "exercise")` aligned with "ISO exercise window expiring tomorrow"; `("anaphylaxis", "epipen")` aligned with "classic anaphylaxis presentation. EpiPen administered". Discipline carry-forward from D-C2.attempt2.C → D-C3.attempt1.C → D-C4.attempt1.C → D-C5.attempt1.C → D-C6.attempt1.C remains mechanically self-improving; attribution clean: self-restate gate → structural-parsing (audit step 1 territory); Step 3.5 → M8b keyword/content alignment (audit step 2 territory).

### Audit-gate results (8/8 PASS)

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v26')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v26'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v26 9 5 770.0` with no exception. duration_s=770.0 is the correctly computed `Trace.duration_s` property `max(last_gt_completion, last_event_time) + 30.0` for the test_v26 sim_time + window distribution (5 GTs at 210/440/360/520/620 with windows 240/200/240/220/90 yields last_gt_completion 740.0; events at 30/75/110/210/290/360/440/520/620 yields last_event_time 620.0; max(740, 620) + 30 = 770). |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 `(kw, content.lower())` substring checks pass (Step 3.5 pre-flight + audit-gate verification both PASS at the single run). Pairs: `(lagavulin, lagavulin_single_cask_allocation_38min_window_distillery)`; `(allocation, lagavulin_single_cask_allocation_38min_window_distillery)`; `(chemo, mother_in_law_chemo_infusion_ride_request_voicemail_6pm)`; `(infusion, mother_in_law_chemo_infusion_ride_request_voicemail_6pm)`; `(wildfire, wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter)`; `(smoke, wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter)`; `(iso, iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying)`; `(exercise, iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying)`; `(anaphylaxis, partner_anaphylaxis_epipen_911_dispatched_second_dose_needed)`; `(epipen, partner_anaphylaxis_epipen_911_dispatched_second_dose_needed)`. |
| 3a | Banned event_id literal review (vs 172 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v26's 9 event_ids. |
| 3b | Banned theme semantic review (vs 97 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_banned_theme_semantic_review.per_gt_distinguishing_qualifiers`. All 5 GT themes pass with distinguishing qualifiers vs nearest banned predecessors: GT1 V4 NEW YES scarcity-bounded Lagavulin cask-share allocation distinct from C1 vinyl_drop_press_today on product class + mechanism + scarcity + constituency + settlement (closes within-V4-NEW-YES asymmetry C5 opened); GT2 message/delivery MIL chemo voicemail distinct from C1 legal-courier + C3 partner-jeweler-voicemail + C4 hospital-grandmother + M10b sister-airport + M10b photographer on sender + reason + decision + relation; GT3 weather-alert wildfire-smoke AQI-421 distinct from C2 flash-flood + C3 dust-storm + C4 tornado-watch + M10b earthquake + M11a boil-water on hazard mechanism + metric + mitigation + window + issuing authority; GT4 urgent-safety partner-anaphylaxis-EpiPen distinct from C1 gas-leak + C2 medical-pendant + C4 CO-alarm + C5 child-medication-ingestion on patient + fault class + allergen + protocol + response-class; GT5 financial/deadline ISO-exercise-2400-shares distinct from C1 student-loan + C2 property-tax + C3 homeowner-insurance + C5 IRS-quarterly-tax on obligation + mechanism + counterparty + penalty + amount + domain. |
| 3c | Banned keyword tuple bytewise review (vs 96 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(lagavulin, allocation), (chemo, infusion), (wildfire, smoke), (iso, exercise), (anaphylaxis, epipen)]`. Note semantically-adjacent bytewise-distinct cases: `(vinyl, drop)` banned (scarcity-bounded sister-tuple) but `(lagavulin, allocation)` bytewise-distinct on both elements; `(mother, birthday)` + `(grandpa, birthday)` + `(hospital, mother)` + `(hospital, grandmother)` banned but `(chemo, infusion)` bytewise-distinct on both; `(weather, rain)` + `(flood, warning)` + `(dust, storm)` + `(tornado, watch)` banned weather tuples but `(wildfire, smoke)` bytewise-distinct on both elements vs all four; `(loan, repayment)` + `(property, tax)` + `(quarterly, tax)` + `(tax, expires)` + `(deadline, quarterly)` + `(insurance, lapse)` + `(mortgage, "rate lock")` + `(counter-offer, agent)` + `(hoa, vote)` + `(auto-payment, balance)` + `(approve, brake)` + `(bond, confirmation)` + `(warranty, registered)` banned financial/deadline tuples but `(iso, exercise)` bytewise-distinct from all; `(prescription, refill)` + `(medication, ingestion)` + `(hospital, mother)` + `(hospital, grandmother)` + `(carbon, monoxide)` + `(gas, leak)` + `(fall, pendant)` + `(fire, alarm)` + `(fire, kitchen)` banned urgent-safety tuples but `(anaphylaxis, epipen)` bytewise-distinct on both elements vs all. |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical grep of 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21..v25 event_ids: 0 collisions against 172 prior event_ids across 20 prior trace definitions. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (96 unique across dev_v1..test_v25): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v26 has 898 unique 8-grams across content+briefing+intents fields; prior dev/test traces have 5877 unique 8-grams; overlap = 0. |

### GT-regime classification (audit step 7; for Commit D per-trace observations table)

- GT 1 `lagavulin_single_cask_allocation_38min_window_distillery` — **discretionary-deadline obligation (V4 NEW YES, scarcity-bounded-opportunity subclass)**: Lagavulin distillery member cask-share allocation for the 2002 vintage single-cask special release with thirty-eight-minute window + 312-bottle one-per-member limit + queue position 47 + sixty-second rolling claim-or-release + secondary-list trade-only fallback. Lifts scarcity-bounded subclause cross-trace 1x→2x (closes within-V4-NEW-YES asymmetry); total V4 NEW YES 3→4.
- GT 2 `mother_in_law_chemo_infusion_ride_request_voicemail_6pm` — **message or delivery directed personally to the user (V2 EXISTING YES)**: mother-in-law Elena voicemail asking the user to drive her to and stay through tomorrow morning's four-hour-in-chair chemo infusion at Memorial (too groggy to drive home alone) with before-six-tonight callback or she falls back to the patient-transport line cutoff at seven sharp. 3x→4x cross-trace lift.
- GT 3 `wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter` — **weather alert (V2 EXISTING YES)**: NWS AirNow advisory with PM2.5 from the Hazelnut Ridge wildfire smoke plume lifting regional AQI from 240 to 421 over an hour (hazardous tier above very-unhealthy) + four-hour-minimum indoor-shelter + HEPA HVAC recirculate + N95-mask recommendation + sensitive-groups (infants + cardiac + respiratory) shelter-until-AQI-below-150. 3x→4x cross-trace lift.
- GT 4 `iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying` — **financial/deadline obligation (V2 EXISTING YES)**: Carta equity admin email notifying that the post-termination ISO exercise window for 2,400 shares from the March separation expires tomorrow at 5pm Pacific with $14.20 strike + partial-exercise lots of 100 + full-grant forfeiture on miss + AMT-disqualifying-disposition treatment for current-tax-year ISO conversions lapses. 4x→5x cross-trace lift.
- GT 5 `partner_anaphylaxis_epipen_911_dispatched_second_dose_needed` — **urgent safety/security issue (V2 EXISTING YES)**: partner anaphylaxis from peanut allergen in pad thai takeout container with visible facial swelling + severe wheezing within ninety seconds + EpiPen administered to outer thigh + 911 dispatched + paramedics six minutes out + live dispatcher asking on speaker about second-dose availability since first injection not responding within expected three-minute window. 4x→5x cross-trace lift.

### Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism + V2-class subclause coverage)

**V4 NEW YES coverage at C6:** **1 instance** under scarcity-bounded-opportunity subclause (`lagavulin_single_cask_allocation_38min_window_distillery`). Lifts that subclause cross-trace coverage 1x→2x (C1 vinyl_drop_press_today + C6 lagavulin_single_cask_allocation); lifts total V4 NEW YES cross-trace instance count from 3 to 4. **Defensibility:** V4 NEW YES had a new within-subclass asymmetry at C5 end (family-milestone 2x at C2+C5 vs scarcity-bounded 1x at C1 only) opened by C5's PATH (c) choice picking family-milestone for the asymmetric-weakness-closure lift. PATH (c) at C6 closes the within-V4-NEW-YES asymmetry by 1x→2x lift on the scarcity-bounded-opportunity subclause; both V4 NEW YES subclauses now sit symmetrically at 2x each. Yields strongest reviewer-defensible MECHANISM_CONFIRM evidence-base claim: all V4 NEW YES subclauses tested ≥2x cross-trace AND total V4 NEW YES instances at 4. MECHANISM_CONFIRM is the PRIMARY outcome predicate (D7 row identification depends on it strict-5/5 per D14-H3); strengthening evidence for the primary outcome dominates strengthening evidence for the secondary outcome (COMPLIANT_NO_REGRESSION). Scarcity-bounded subclause picked at C6 because the within-V4-NEW-YES asymmetry IS the new asymmetrically-weakest mechanism-evidence cell at C5 end; symmetric closure at 2x each maximizes mechanism-coverage defensibility per trace cost.

**V4 NEW NO coverage at C6:** **NONE** (intentional per D-C6.attempt1.B locked path-(c) choice). All 3 V4 NEW NO subclauses already 2x each at C1+C2; total 6 V4 NEW NO instances cross-trace post-C2. 3rd-repeat lift dominated by H4 denominator growth (each compliant-content distractor added is a +1 H4 sample whose information density is preserved regardless of which V4 NEW NO subclause it represents at 3rd repeat); path (b) explicitly rejected at C6 Plan.

**V2 EXISTING YES compliant-content coverage at C6 (4 GTs across 4 distinct V2 YES classes; 2 lifts at 3x→4x + 2 lifts at 4x→5x):**
- GT `mother_in_law_chemo_infusion_ride_request_voicemail_6pm` tests V2 message/delivery class under NEW within-class incident distinct from C1 legal_doc_courier_signature (different mechanism: voicemail-callback vs courier-lobby-wait; different reason: chemo-ride vs legal-doc-signature), C3 partner_voicemail_ring_pickup_jeweler (different sender: MIL vs partner; different reason: chemo-treatment-day-ride vs jeweler-pickup errand), C4 hospital_grandmother_hip_fracture (different sender: MIL voicemail vs hospital admitting-desk; different reason: outpatient chemo ride vs hip-fracture surgical-consent; different relation: mother-in-law vs grandmother), M10b sister_pickup (different relation + reason + window), M10b photographer_voicemail_jen (different sender + reason). **3x→4x cross-trace lift** (C1+C3+C4+C6).
- GT `wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter` tests V2 weather-alert class under NEW within-class incident distinct from C2 flash-flood (precipitation), C3 dust-storm (mineral-wind-driven dust), C4 tornado-watch (convective-supercell rotation), M10b earthquake (tectonic), M11a boil-water (utility microbial). **3x→4x cross-trace lift** (C2+C3+C4+C6).
- GT `partner_anaphylaxis_epipen_911_dispatched_second_dose_needed` tests V2 urgent-safety class under NEW within-class incident distinct from C1 gas-leak (atmospheric vs medical-emergency), C2 aging_parent_fall_alert (different patient + auto-dispatch vs in-home EpiPen + live-911-coordinate), C4 carbon-monoxide (atmospheric), C5 child_medication_ingestion (different patient + ER-transport-protocol vs in-home-EpiPen-+-911-coordinate-+-second-dose-availability-check). **4x→5x cross-trace lift** (C1+C2+C4+C5+C6).
- GT `iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying` tests V2 financial/deadline class under NEW within-class incident distinct from C1 student_loan_repayment_resume (consumer-debt vs employer-equity-grant), C2 property_tax_installment (gov-tax vs employer-equity), C3 homeowner_insurance_lapse (insurance vs equity-grant), C5 quarterly_estimated_tax (federal-tax vs equity-grant; ongoing vs one-time). **4x→5x cross-trace lift** (C1+C2+C3+C5+C6).

**V2 EXISTING NO compliant-content distractor coverage at C6 (4 distractors; 1 social-channel-invite lift 2x→3x to complete V2 NO triangulation table + 3 distractors lifting 3x→4x):**
- Distractor `mastodon_instance_follow_suggestion_weekly_digest_kind_strangers` tests V2 social-channel-invite class at **2x→3x triangulation** (C1 discord_unread_digest + C4 slack_frontend_weekly_community_invite + C6 mastodon-instance-weekly-digest; distinct on platform Discord/Slack/Mastodon, federation model centralized vs centralized vs federated, channel type unread vs frontend-channel vs follow-suggestion). **Completes V2 NO triangulation table at ≥3x for ALL 5 V2 NO classes post-C6.**
- Distractor `datadog_synthetic_monitoring_daily_heartbeat_all_pass_digest` tests V2 routine-status/heartbeat class at **3x→4x** triangulation (C3 cloud_backup_daily + C4 ssl_monitor_weekly + C5 K8s-autoscaler-monthly + C6 DataDog-synthetic-daily; distinct on tool, monitoring class, cadence, infra-domain).
- Distractor `aperture_camera_gear_spring_catalog_email_no_action_required` tests V2 marketing/newsletter class at **3x→4x** triangulation (C3 kitchen_gear_quarterly + C4 tea_club_monthly + C5 indie-bookstore-quarterly-preorder + C6 camera-gear-spring-catalog; distinct on product category, commerce model, cadence).
- Distractor `monday_week_lookahead_briefing_no_priority_items_flagged` tests V2 generic-daily-briefing class at **3x→4x** triangulation (C3 morning-briefing + C4 evening-briefing + C5 friday-weekly-recap + C6 Monday-week-lookahead; distinct on cadence, target horizon).

**V2 NO class skipped at C6:** feature-announcement/app-update stays at 3x (C2 chrome_extension_marketplace_update + C3 notion_new_dashboard_feature_tour + C5 vscode_marketplace_verified_publisher_tab). C6 path-(c) selected 3 of the 4 V2 NO 3x-classes for the 3x→4x lift + 1 V2 NO 2x-class (social-channel-invite) for the 2x→3x lift; feature-announcement defers to C7+ for the 3x→4x lift.

**Coverage summary at C6:** Maximal MECHANISM_CONFIRM evidence-base lift on the asymmetrically-weakest V4 mechanism cell (within-V4-NEW-YES asymmetry: scarcity-bounded-opportunity subclause 1x→2x; total V4 NEW YES 3→4; both V4 NEW YES subclauses now symmetrically at 2x each) + 2 V2 EXISTING YES classes lifted 3x→4x (message/delivery + weather-alert; closes V2 YES 3x→4x gap on the 2 remaining 3x classes) + 2 V2 EXISTING YES classes lifted 4x→5x (urgent-safety + financial/deadline) + V2 NO triangulation table completed at ≥3x for ALL 5 V2 NO classes (social-channel-invite 2x→3x) + 3 V2 EXISTING NO classes lifted 3x→4x (routine-status + marketing/newsletter + generic-daily-briefing). Cross-trace coverage state through C6: **V4 NEW YES**: 4 total instances (scarcity-bounded 2x at C1+C6; family-milestone 2x at C2+C5 — symmetric); **V4 NEW NO**: 6 total instances (3 subclauses × 2x each at C1+C2); **V2 EXISTING YES classes**: urgent-safety 5x (C1+C2+C4+C5+C6), schedule-change 4x (C1+C3+C4+C5), financial/deadline 5x (C1+C2+C3+C5+C6), production/on-call 4x (C2+C3+C4+C5), message/delivery 4x (C1+C3+C4+C6), weather-alert 4x (C2+C3+C4+C6); **V2 EXISTING NO classes**: routine-status 4x (C3+C4+C5+C6), marketing/newsletter 4x (C3+C4+C5+C6), generic-daily-briefing 4x (C3+C4+C5+C6), feature-announcement 3x (C2+C3+C5), social-channel-invite 3x (C1+C4+C6). 4 traces remain for combined-N=20 closure; future C7..C10 may continue compliant-content discipline at the 4x V2 YES classes (5x lift candidates: schedule-change + production/on-call) OR lift remaining 3x V2 NO class (feature-announcement 3x→4x) OR pursue 3rd-repeat V4 NEW YES (after this symmetric closure) OR consider higher-order GT-shape changes only if H4 evidence-base saturation warrants it.

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v26-attempt-1-accepted.json` (SHA256 `d583f20d2a3b97de72d61c0f02fbac806667be0dd2b65cd1e33b08b7c8e616d9`; 42164 bytes; D-C1.2 schema with step_3_5_pre_flight first-run-PASS log + V4 NEW YES scarcity-bounded 1x→2x within-V4-NEW-YES symmetric-closure defense + V2 EXISTING YES/NO compliant-content coverage with explicit path-(c) within-subclass-asymmetry-closure defense + 3x→4x V2 YES lift on the 2 remaining 3x classes + 4x→5x V2 YES lift on urgent-safety + financial/deadline + V2 NO triangulation-table completion at ≥3x for all 5 V2 NO classes + full audit-gate evidence + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata).

### Banned-list state delta at C6

- Pre-C6 (C5 end-state, ships at C6): 172 IDs / 97 themes / 96 tuples.
- C6 contributions from accepted test_v26 (to be incorporated into `21c-banned-list-pre-c7.txt` at C7 land time per D-C1.1):
  - **+9 IDs:** `lagavulin_single_cask_allocation_38min_window_distillery`, `mother_in_law_chemo_infusion_ride_request_voicemail_6pm`, `wildfire_smoke_advisory_aqi_421_hazardous_4hr_shelter`, `iso_exercise_window_expires_tomorrow_5pm_2400_shares_disqualifying`, `partner_anaphylaxis_epipen_911_dispatched_second_dose_needed`, `monday_week_lookahead_briefing_no_priority_items_flagged`, `datadog_synthetic_monitoring_daily_heartbeat_all_pass_digest`, `mastodon_instance_follow_suggestion_weekly_digest_kind_strangers`, `aperture_camera_gear_spring_catalog_email_no_action_required`.
  - **+5 themes (GT-regime regime column verbatim):** discretionary-deadline obligation (V4 NEW YES, scarcity-bounded-opportunity subclass) — Lagavulin distillery 2002 single-cask member cask-share allocation 38-minute window + 312-bottle one-per-member limit + position-47 queue + 60-second rolling claim-or-release + trade-only secondary list fallback; message or delivery directed personally to the user (V2 EXISTING YES) — mother-in-law Elena voicemail asking for tomorrow-morning chemo-infusion ride at Memorial with four-hour-in-chair commit + before-6pm callback or patient-transport-7pm-cutoff fallback; weather alert (V2 EXISTING YES) — NWS AirNow advisory with PM2.5 from Hazelnut Ridge wildfire smoke plume lifting AQI 240→421 (hazardous tier) + 4-hour-min indoor shelter + HEPA recirculate + N95-mask + sensitive-groups shelter-until-AQI-below-150; financial/deadline obligation (V2 EXISTING YES) — Carta equity admin email: post-termination ISO exercise window for 2,400 shares expires tomorrow 5pm Pacific + $14.20 strike + partial-exercise lots of 100 + full-grant-forfeiture + AMT-disqualifying-disposition lapse; urgent safety/security issue (V2 EXISTING YES) — partner anaphylaxis from peanut-allergen pad-thai takeout + EpiPen administered + 911 dispatched 6-min-out + dispatcher requesting second-dose-availability since first-injection not responding within 3-min window.
  - **+5 tuples (GT keyword tuples verbatim):** `(lagavulin, allocation)`, `(chemo, infusion)`, `(wildfire, smoke)`, `(iso, exercise)`, `(anaphylaxis, epipen)`.
- Post-C6 (input state for C7): 181 IDs / 102 themes / 101 tuples. File ships at C7 land time as `runs/data/21c-banned-list-pre-c7.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C6

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at the accepting attempt).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (7 cumulative milestone attempts < 25; 6 accepted traces toward target of 10).
- Retry-cap-3 on test_v26 (D-C1.5 #3): **not exhausted** (1/3 used; PASS at attempt #1 / 2 retries remaining had attempt #1 not accepted).

### Cumulative milestone-spend through Commit C6

Commit C6 spend: $0 at attempt #1 (in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C6: $0.7081 (unchanged from Commit C5; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C6 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21 + test_v22 + test_v23 + test_v24 + test_v25 definitions — frozen historical artifacts (only NEW `test_trace_v26` added at C6, plus the registry line `"test_v26": test_trace_v26,`).
- `runs/data/21c-banned-list-pre-c{1,2,3,4,5}.{txt,json}` + `runs/data/21c-author-test_v{21,22,23,24,25}-*.json` — frozen at C1+C2+C3+C4+C5; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C6.

### Next: Commit C7 — fresh-session trace authoring `test_v27`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c7.{txt,json}` (NEW; reflects test_v21 + test_v22 + test_v23 + test_v24 + test_v25 + test_v26 contributions; 181 IDs / 102 themes / 101 tuples) as the pre-C7 starting state. Self-restate gate rendered against the pre-C7 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 7/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C / D-C6.attempt1.C) carries forward as standing per-attempt author discipline. With C6 closing the within-V4-NEW-YES asymmetry (both subclauses now at 2x each; total V4 NEW YES 4) + lifting 4 V2 YES classes (3x→4x on message/delivery + weather-alert; 4x→5x on urgent-safety + financial/deadline) + completing V2 NO triangulation table at ≥3x for all 5 classes + lifting 3 V2 NO classes 3x→4x, C7 may pursue (1) continued compliant-content discipline lifting schedule-change + production/on-call V2 YES 4x→5x, (2) feature-announcement V2 NO 3x→4x to complete V2 NO triangulation at ≥4x for the 4 already-≥4x classes (mirror PATH (a) closure), (3) 3rd-repeat V4 NEW YES (after the symmetric closure at C6) only if defensible vs H4 denominator growth, or (4) higher-order GT-shape changes if H4 evidence-base saturation warrants; defended at the C7 Plan.

Commit C7 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.


---

## Commit C7 — test_v27 (2026-05-18)

**Verdict: test_v27 ACCEPTED at attempt 2/3; audit-gate 8/8 PASS at the accepting attempt. Attempt 1/3 REJECTED at audit-gate step 6 (drift strong-overlap b ≥8-word verbatim phrase) on 8 of test_v27's 1245 unique 8-grams overlapping with C6 distractor boilerplate — D-C1.3 audit-gate working as designed; rejection artifact ships in this commit bundle per D-C1.2 + D-C1.6 transparency.** Cumulative milestone attempt count 9/25 through Commit C7 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2 + C3 attempt-1 + C4 attempt-1 + C5 attempt-1 + C6 attempt-1 + C7 attempt-1 + C7 attempt-2); 3 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at all attempts (M11a-extension structural-parsing-failure rate to date: 0/9 attempts — both C2 attempt-1 (step-2 M8b) and C7 attempt-1 (step-6 8-gram drift) rejections are NOT counted as structural-parsing-failure per §D4 design; self-restate gate addresses audit-gate step 1 territory only).

### C-protocol governance decisions inherited from C1 + C2 + C3 + C4 + C5 + C6

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) inherit VERBATIM at C7 with no re-litigation per "no scope drift within a milestone" operating principle. D-C2.A..D-C2.D (locked at C2 attempt-#1 Plan) + D-C2.attempt2.A..D-C2.attempt2.D (locked at C2 attempt-#2 Plan `f9808c8`) + D-C3.attempt1.A..D-C3.attempt1.D (locked at C3 attempt-#1 Plan `9f84a01`) + D-C4.attempt1.A..D-C4.attempt1.D (locked at C4 attempt-#1 Plan `e998a07`) + D-C5.attempt1.A..D-C5.attempt1.D (locked at C5 attempt-#1 Plan `b349b23`) + D-C6.attempt1.A..D-C6.attempt1.D (locked at C6 attempt-#1 Plan `d8ce8a4`) also inherit VERBATIM at C7. The per-attempt author discipline added at C2 attempt #2 (Step 3.5 pre-flight) carries forward as standing author discipline through C7..C10.

### C7 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C7.attempt1.A state-confirm checklist** | Pre-attempt-#1 state confirmed via on-disk verifications: main HEAD `d8ce8a4` (M11a-extension Commit C6); working tree clean; `sandbox/event_trace.py` sha256 `7bf685cd183f300a9f4774ec29def8be4e87f6cb2db4432828d58e9296d94853` (85203 bytes; HEAD-bit-identical post-C6 incl. `test_trace_v26` + registry line); V4 prompt string sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; bytewise-identical to §D1 lock — `agent/arbiter.py` last touched at `adc1cba` Commit B, unchanged through C1+C2+C3+C4+C5+C6); `runs/data/21c-banned-list-pre-c6.{txt,json}` sha256 `c1b782d0…` + `a411ad0a…` / 172/97/96 counts verified. D-C6.attempt1.A precedent mirrored verbatim. |
| **D-C7.attempt1.B subclause coverage brief inheritance + C7-specific path-lock** | D-C2.B / D-C3.attempt1.B / D-C4.attempt1.B / D-C5.attempt1.B / D-C6.attempt1.B brief inherits VERBATIM. C7-specific path-lock (locked at Plan): **PATH (a) — compliant-content lift**. Trace shape: 5 V2 EXISTING YES GTs across 5 distinct V2 YES classes (schedule-change 4x→5x + production/on-call 4x→5x as **path-(a) primary lifts**; urgent-safety 5x→6x + financial/deadline 5x→6x as saturating-but-class-diversity-enforced lifts; message/delivery 4x→5x as 5-GT-shape-constraint lift) + **zero V4 mechanism GTs** (preserves C6's symmetric V4 NEW YES closure at 2x each subclause AND the V4 NEW NO saturated state at 2x each of 3 subclauses) + 4 V2 EXISTING NO distractors (feature-announcement 3x→4x as **path-(a) primary distractor lift** closing V2 NO ≥4x for 4 of 5 classes + 3 V2 NO 4x classes lifted 4x→5x: routine-status + marketing/newsletter + generic-daily-briefing). Defensibility framing: PATH (a) targets the asymmetrically-weakest still-3x V2 NO + still-4x V2 YES cells WITHOUT re-opening any prior asymmetric closure (PATH (b) V4 NEW YES 3rd-repeat explicitly rejected at C7 Plan as it would re-open the within-V4-NEW-YES asymmetry C6 just closed; PATH (c) V4 NEW NO 3rd-repeat explicitly rejected at C5/C6/C7 as dominated by H4 denominator growth; PATH (d) within-V2-class 5-GT triangulation explicitly rejected per standing C2..C6 reviewer-flag-risk basis). Net post-C7 coverage state: **5 of 6 V2 YES classes lifted to ≥5x (only weather-alert at 4x); 4 of 5 V2 NO classes lifted to ≥4x (only social-channel-invite at 3x); V4 NEW YES symmetric closure preserved at 2x each subclause (total 4); V4 NEW NO saturated state preserved at 2x each of 3 subclauses (total 6)** — STRONGER reviewer-defensible endpoint claim than kickoff's recommended "4 of 6 V2 YES at ≥5x with remaining 2 at 4x" state. |
| **D-C7.attempt1.C Step 3.5 pre-flight keyword literal-substring verification** | Inherits VERBATIM from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C / D-C6.attempt1.C. Mechanically verify every GT keyword tuple element appears as case-insensitive substring of that GT's `Event.content` via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v27'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Does NOT consume retry-cap budget per D-C1.4. |
| **D-C7.attempt1.D commit shape extension (multi-attempt)** | D-C2.attempt2.D commit shape (multi-attempt bundling) inherits VERBATIM for the C7 attempt-1-rejected + attempt-2-accepted trajectory. C7 commit bundles BOTH `runs/data/21c-author-test_v27-attempt-1-rejected.json` AND `runs/data/21c-author-test_v27-attempt-2-accepted.json` per D-C1.2 + D-C1.6 transparency; C7 commit message names "attempt N / N total attempts" showing the rejection trajectory. |

### Banned-list starting state (C6 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c7.txt` (SHA256 `e03a28c4f6ee02a35a6c1fe3dd3e5f0c3678d9886ff442c09d56b3379a9dfa39`; 20577 bytes; 181 banned event_ids + 102 banned themes + 101 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c7.json` (SHA256 `2c0f02dccbe2ee0025a9560280429cdcd1a98463cfe639bdc2eb4fd7a874d1a9`; 20220 bytes; same content in structured schema; counts mechanically verified unique).
- Provenance: extended at C7-attempt-#1 session by appending C6's accepted test_v26 contributions (+9 IDs / +5 themes / +5 tuples) to the pre-C6 banned-list (`c1b782d0…` / `a411ad0a…`, 172/97/96) per D-C1.1 invariant. Pre-C6 files NOT mutated (verified bit-identical pre and post C7 authoring).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c7.txt > /tmp/m11a-ext-c7-restate-prompt.txt`
- Rendered prompt SHA256: `dd4d29f3efb3083f41690ae77231454d4fa462e374c76232a15c9cce62ea3050` (20986 bytes).
- Self-restate response authored in own words distinct from C1..C6 responses per fresh-session-restart-from-scratch discipline; full text archived verbatim in both per-attempt artifacts `self_restate_response_verbatim` field.
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered at either C7 attempt; schema check via `get_trace('test_v27')` passes on first import at both attempts.

### Attempt #1 — REJECTED (audit-gate step 6 FAIL: 8 8-gram boilerplate overlaps with C6)

**Verdict:** Reject at first-match-rejection per D-C1.3 audit-gate semantics. First violated check: `step_6_drift_strong_overlap_b_8gram_verbatim`.

**Audit-gate trace at rejection:**

| Step | Item | Verdict |
|---|---|---|
| 1 | Schema check via `get_trace('test_v27')` | PASS — 9 events / 5 GTs / duration 830.0s |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS — 10/10 pairs True (Step 3.5 first-run PASS) |
| 3a | Banned event_id literal review | PASS — 0 collisions vs 181 banned IDs |
| 3b | Banned theme semantic review | PASS — per-GT distinguishing qualifiers archived |
| 3c | Banned keyword tuple bytewise review | PASS — 0 collisions vs 101 banned tuples |
| 4 | Cross-trace literal-ID collision (HALT-gate per D-C1.5 #1) | PASS — HALT NOT triggered (0 collisions vs 181 prior IDs across 21 prior trace definitions) |
| 5 | Drift strong-overlap (a) GT tuple bytewise | PASS — 0 collisions vs 101 prior GT tuples |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | **FAIL** — 8 of test_v27's 1245 unique 8-grams overlap with prior dev/test traces' 7187 unique 8-grams (overlap = 8) |

**Rejection reason (verbatim from artifact `rejection_reason_verbatim`):** Audit-gate step 6 (drift strong-overlap b: ≥8-word verbatim phrase cross-trace) detected 8 overlapping 8-grams between test_v27 attempt-1 distractor content and C6 (test_v26) distractor content. Two formulaic boilerplate phrases were carried over from C6 verbatim at draft time without single-word author-discipline attention: (a) the standard "unsubscribe from seasonal mailings in your account preferences if you prefer fewer messages" marketing-email closer reused from C6 Aperture catalog into C7 Goldleaf catalog (6 overlapping 8-grams); (b) the "no priority items are flagged from your project list, [X], or stakeholder asks" generic-daily-briefing template phrase reused from C6 Monday-week-lookahead briefing into C7 Wednesday-midweek-checkpoint briefing (2 overlapping 8-grams). Both are distractor-content (not GT content), but audit step 6 mechanically counts all 8-gram overlaps across content + briefing + intents fields without distinguishing GT vs distractor. Reviewer-defense note: this is exactly the failure mode audit step 6 is locked to catch (formulaic marketing-newsletter / briefing-template phrasings that an author would naturally re-use across traces without unique-phrase author-discipline); the rejection is the audit-gate working as designed at this step, parallel to C2 attempt-#1's audit-gate-step-2 keyword-alignment rejection working as designed.

**Specific 8-gram overlaps (attempt-1 → prior C-trace cross-trace overlap):**

| 8-gram | Source in C7 attempt-1 | Source in prior trace |
|---|---|---|
| `('seasonal','mailings','in','your','account','preferences','if','you')` + 5 sibling 8-grams in the same 13-word phrase | D3 goldleaf_stationery closing sentence | C6 aperture_camera_gear closing sentence |
| `('no','priority','items','are','flagged','from','your','project')` + 1 sibling 8-gram | D4 wednesday_midweek_checkpoint_briefing middle sentence | C6 monday_week_lookahead_briefing middle sentence |

**Per-attempt artifact:** `runs/data/21c-author-test_v27-attempt-1-rejected.json` (SHA256 `b11d4742b9fcd893cb9438043502b227b5f523b7f635ba46029e03343f1398a6`; 20113 bytes; full audit-gate evidence at attempt-1 + Step 3.5 first-run-PASS log + self-restate response verbatim + authored-trace verbatim summary + specific 8-gram overlap detail + post-rejection-actions-taken archived; ships with this C7 commit bundle per D-C1.2 + D-C1.6 transparency).

**Reviewer-defense (D-C1.3 audit-gate working as designed at step 6):** The audit-gate caught a draft-time boilerplate-template-phrasing convergence at the pre-submission gate before it could corrupt cross-trace independence. The rejection artifact ships in the C7 commit bundle (not hidden, not amended away); the cumulative-milestone attempt count includes attempt #1 transparently (9/25 through Commit C7 — C1+C2 attempt-1+C2 attempt-2+C3+C4+C5+C6+C7 attempt-1+C7 attempt-2 — not 8/25). Per locked plan §D9 defense #4 + D-C1.5 #2, banned-list saturation halt counts CUMULATIVE attempts not just accepted-trace count; this rejection contributes to the 25-attempt cap toward the 10-accepted-trace target. **In-place revision discipline note:** between attempt-1 and attempt-2 the sandbox/event_trace.py was edited in-line at the two offending distractor content fields only (D3 goldleaf closing + D4 wednesday-briefing middle sentence); GT content + briefing + intents + 5 other event content fields preserved bytewise. Functionally equivalent end-state vs C2 attempt-1→attempt-2's full revert-and-re-author pattern. Both patterns are within-protocol per D-C1.4 retry-cap consumption rules.

### Attempt #2 — ACCEPTED (audit-gate 8/8 PASS)

**Verdict:** Accept (strict-letter; 8 of 8 audit-gate items PASS) after targeted in-line revision of the two attempt-1 boilerplate-overlap distractor phrases. GT keyword content + briefing + intents + 5 other event content fields preserved bytewise from attempt-1.

**Revised distractor content (attempt-2):**
- D3 goldleaf_stationery closing rewritten: "Unsubscribe from seasonal mailings in your account preferences if you prefer fewer messages from us." → "If our catalog cadence has become too noisy, the mailing frequency can be dropped to twice-yearly or fully paused through the footer link below."
- D4 wednesday_midweek_checkpoint_briefing middle sentence rewritten: "No priority items are flagged from your project list, sprint board, or stakeholder asks, and no overdue tasks were detected in the personal-task queue." → "The sprint board, stakeholder-ask queue, and personal-task list all show no urgent items pending, and no overdue tasks were detected anywhere in the workflows you supervise."

### Step 3.5 pre-flight keyword literal-substring verification (D-C7.attempt1.C; first-run PASS at attempt-1 + re-PASS at attempt-2)

| Run | Attempt | Outcome | Detail |
|---|---|---|---|
| 1 | attempt-1 | **PASS** — all 10 pairs print `True` | `('aspirin', self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics) True; ('dispatcher', self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics) True; ('uscis', uscis_naturalization_interview_rescheduled_friday_8am_field_office) True; ('interview', uscis_naturalization_interview_rescheduled_friday_8am_field_office) True; ('fbar', fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k) True; ('foreign', fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k) True; ('attorney', tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow) True; ('eviction', tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow) True; ('kafka', kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m) True; ('broker', kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m) True`. No in-session iteration required. |
| 2 | attempt-2 | **PASS** | Keywords + GT content unchanged between attempt-1 and attempt-2 (only distractor content fields revised); all 10 pairs still print `True`. |

**Reviewer-defense (Step 3.5 working as designed; attempt-1 rejection was at downstream Step 6, NOT at Step 3.5):** Step 3.5 PASSed on first run at attempt-1 for C7, mirroring C4 + C5 + C6 attempt-1 first-run-PASS precedents (vs C3 attempt-1's in-session iteration on `('pickup', partner_voicemail_ring_pickup_jeweler)` two-word/one-word misalignment). Content authored with explicit single-word keyword-substring attention at draft time: `("aspirin", "dispatcher")` aligned with "chew one full-strength aspirin tablet" + "the live dispatcher is on speaker"; `("uscis", "interview")` aligned with "USCIS field-office adjudications officer notice" + "N-400 naturalization interview"; `("fbar", "foreign")` aligned with "FinCEN-114 FBAR filing materials" + "foreign-bank-account aggregate balance"; `("attorney", "eviction")` aligned with "your tenant-defense attorney's paralegal" + "emergency eviction-stay motion paperwork"; `("kafka", "broker")` aligned with "order-fulfillment Kafka cluster" + "broker fleet has been reporting unstable partition-leadership elections". Discipline carry-forward from D-C2.attempt2.C → D-C3.attempt1.C → D-C4.attempt1.C → D-C5.attempt1.C → D-C6.attempt1.C → D-C7.attempt1.C unbroken. Attribution clean: self-restate gate → structural-parsing (audit step 1 territory; PASS at attempt-1+attempt-2); Step 3.5 → M8b keyword/content alignment (audit step 2 territory; PASS at attempt-1+attempt-2); attempt-1 rejection at audit step 6 is a SEPARATE drift-overlap concern downstream of both Step 3.5 and audit step 2.

### Audit-gate results at accepting attempt (attempt-2; 8/8 PASS)

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v27')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v27'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v27 9 5 830.0` with no exception. duration_s=830.0 is the correctly computed `Trace.duration_s` property `max(last_gt_completion, last_event_time) + 30.0` for the test_v27 sim_time + window distribution (5 GTs at 660/220/480/560/380 with windows 90/240/220/240/200 yields last_gt_completion 800.0 [tenant_attorney 560+240]; events at 30/75/...not exactly — events at 30/80/140/220/300/380/480/560/660 yields last_event_time 660.0; max(800, 660) + 30 = 830). |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 `(kw, content.lower())` substring checks pass at run 2 (post-revision; keyword + GT content unchanged between attempts). Pairs: `(aspirin, self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics)`; `(dispatcher, self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics)`; `(uscis, uscis_naturalization_interview_rescheduled_friday_8am_field_office)`; `(interview, uscis_naturalization_interview_rescheduled_friday_8am_field_office)`; `(fbar, fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k)`; `(foreign, fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k)`; `(attorney, tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow)`; `(eviction, tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow)`; `(kafka, kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m)`; `(broker, kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m)`. |
| 3a | Banned event_id literal review (vs 181 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v27's 9 event_ids. |
| 3b | Banned theme semantic review (vs 102 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_banned_theme_semantic_review.per_gt_distinguishing_qualifiers`. All 5 GT themes pass with distinguishing qualifiers vs nearest banned predecessors: GT1 V2 urgent-safety self-chest-pressure cardiac-MI-911-aspirin distinct from C1 gas-leak + C2 fall-pendant + C4 CO-alarm + C5 child-medication + C6 partner-anaphylaxis on patient (self) + mechanism (cardiac vs atmospheric/allergic/pediatric/senior) + intervention (911-coordinate + chewed aspirin per dispatcher vs auto-EMS/EpiPen/Poison-Control); GT2 V2 schedule-change USCIS-naturalization-interview-rescheduled distinct from C1 cardio + C3 court-hearing + C4 pediatrician + C5 dental-implant on domain (federal-immigration vs medical/civil-court) + stakeholder (adjudications-officer vs hospital/clerk/oral-surgeon); GT3 V2 financial/deadline FBAR-FinCEN-114 distinct from C1 student-loan + C2 property-tax + C3 homeowner-insurance + C5 IRS-quarterly + C6 ISO-exercise on domain (FBAR foreign-account-reporting vs federal-loan/property-tax/insurance/IRS-quarterly/employer-equity) + counterparty (FinCEN vs Dept-of-Ed/county/insurer/IRS/Carta); GT4 V2 message/delivery tenant-attorney-eviction-stay distinct from C1 legal-doc-courier + C3 partner-jeweler + C4 hospital-grandmother + C6 MIL-chemo on sender (tenant-defense-attorney paralegal vs courier/partner/hospital/MIL) + reason (eviction-stay-motion-pickup vs civil-doc-signature/ring-pickup/surgical-consent/chemo-ride); GT5 V2 production/on-call Kafka-broker-election distinct from C2 Postgres-failover + C3 TLS-expiry + C4 disk-space + C5 redis-memory on technology (Kafka vs Postgres/cert/disk/Redis) + mechanism (partition-leadership-instability + consumer-lag vs failover/cert-rotation/storage-OOM/cache-saturation). |
| 3c | Banned keyword tuple bytewise review (vs 101 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(aspirin, dispatcher), (uscis, interview), (fbar, foreign), (attorney, eviction), (kafka, broker)]`. All 5 tuples bytewise-distinct vs all 101 banned predecessors including the semantically-adjacent banned tuples in same V2 classes (urgent-safety: `(gas, leak)` + `(fall, pendant)` + `(carbon, monoxide)` + `(medication, ingestion)` + `(anaphylaxis, epipen)`; schedule-change: `(appointment, rescheduled)` + `(court, hearing)` + `(pediatrician, advanced)` + `(dental, implant)`; financial/deadline: `(loan, repayment)` + `(property, tax)` + `(insurance, lapse)` + `(quarterly, tax)` + `(iso, exercise)`; message/delivery: `(courier, signature)` + `(ring, pickup)` + `(hospital, grandmother)` + `(chemo, infusion)`; production/on-call: `(database, failover)` + `(tls, expiry)` + `(disk, space)` + `(redis, memory)`). |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical set-intersection of test_v27's 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21..v26 event_ids: 0 collisions against 181 prior event_ids across 21 prior trace definitions. **HALT-trigger NOT fired** at either attempt-1 or attempt-2. |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (101 unique across dev_v1..test_v26): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v27 has 1258 unique 8-grams across content+briefing+intents fields; prior dev/test traces have 7187 unique 8-grams; overlap = 0. Both attempt-1 boilerplate overlaps cleared: D3 goldleaf closing rewritten (6 attempt-1 overlapping 8-grams with C6 Aperture → 0 in attempt-2); D4 wednesday-briefing middle sentence rewritten (2 attempt-1 overlapping 8-grams with C6 Monday-briefing → 0 in attempt-2). |

### GT-regime classification (audit step 7; for Commit D per-trace observations table)

- GT 1 `self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics` — **urgent safety/security issue (V2 EXISTING YES)**: user-self acute coronary syndrome MI symptoms (chest pressure with left-arm radiation + cold sweat + nausea) with documented family history of premature MI; live nine-one-one dispatcher walking through chewed-aspirin + lobby-unlock + medication-list + ride-along protocol; paramedic ETA four minutes. 5x→6x cross-trace lift.
- GT 2 `uscis_naturalization_interview_rescheduled_friday_8am_field_office` — **schedule change affecting the user personally (V2 EXISTING YES)**: USCIS field-office adjudications officer notice rescheduling N-400 naturalization interview from tomorrow 8am to Friday 8am due to officer reassignment; reply-to-confirm before tomorrow-noon Pacific or forced-cancellation default + 6-month back-of-docket queue. 4x→5x cross-trace lift. **PATH (a) primary lift #1.**
- GT 3 `fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k` — **financial/deadline obligation (V2 EXISTING YES)**: federal tax preparer email with FinCEN-114 FBAR filing materials for foreign-bank-account aggregate balance exceeding $10k threshold (residual Berlin postdoc account + dormant Lisbon sabbatical account); extended October-15 deadline lapses at 11:59pm Pacific tonight; willful penalty $129,210 per violation or 50% of foreign account balance per year. 5x→6x cross-trace lift.
- GT 4 `tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow` — **message or delivery directed personally to the user (V2 EXISTING YES)**: tenant-defense attorney's paralegal voicemail with emergency eviction-stay motion paperwork ready for in-person signature at downtown office before 5pm closing; landlord show-cause hearing tomorrow 9am housing court; writ-of-restitution issues by default if motion not on clerk's desk by start-of-business; bring photo ID + maintenance-escrow receipts. 4x→5x cross-trace lift.
- GT 5 `kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m` — **production/on-call alert (V2 EXISTING YES)**: PagerDuty P1 on order-fulfillment Kafka cluster prod-orders-kafka-01 with unstable partition-leadership elections for 15 minutes + 200 under-replicated partitions + consumer-lag past 8M messages on checkout-event topic; runbook 75-min escalation; storage-tier I/O wait spikes correlated with Monday disk-controller firmware push. 4x→5x cross-trace lift. **PATH (a) primary lift #2.**

### Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism + V2-class subclause coverage)

**V4 NEW YES coverage at C7:** **ZERO instances** (intentional per D-C7.attempt1.B locked path-(a) compliant-content focus). Cross-trace state: V4 NEW YES total instances **4 (UNCHANGED)** — scarcity-bounded-opportunity 2x at C1+C6; family-milestone-with-social-cost 2x at C2+C5; symmetric closure achieved at C6 PRESERVED at C7. **Defensibility:** PATH (b) V4 NEW YES 3rd-repeat was explicitly rejected at C7 Plan adversarial-reviewer walkthrough — re-opening the within-V4-NEW-YES asymmetry that C6 closed would dominate any 4→5 marginal-info gain on cross-V4-mechanism asymmetry vs V4 NEW NO 6. PATH (a) compliant-content focus protects the C6 symmetric closure as a load-bearing reviewer-defensible MECHANISM_CONFIRM-evidence-base feature.

**V4 NEW NO coverage at C7:** **ZERO instances** (intentional per D-C7.attempt1.B locked path-(a) compliant-content focus). Cross-trace state: V4 NEW NO total instances **6 (UNCHANGED)** — 3 subclauses × 2x each at C1+C2; saturated state preserved through C3..C7. **Defensibility:** PATH (c) V4 NEW NO 3rd-repeat was explicitly rejected at C5/C6/C7 Plans (saturated 3/3 at 2x; 3rd-repeat dominated by H4 denominator growth where any compliant-content distractor adds equivalent H4 sample-density regardless of V4 NEW NO subclause representation).

**V2 EXISTING YES compliant-content coverage at C7 (5 GTs across 5 distinct V2 YES classes; 3 lifts at 4x→5x + 2 lifts at 5x→6x):**
- GT `self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics` tests V2 urgent-safety class under NEW within-class incident distinct from C1 gas_leak (atmospheric vs cardiac), C2 aging_parent_fall_alert (different patient + auto-dispatch vs live-dispatcher walkthrough), C4 carbon_monoxide_alarm (atmospheric vs cardiac), C5 child_medication_ingestion (different patient + ER-transport protocol vs in-home + paramedic-pickup), C6 partner_anaphylaxis (different patient + mechanism + intervention — partner-anaphylaxis-EpiPen vs self-MI-aspirin). **5x→6x cross-trace lift** (C1+C2+C4+C5+C6+C7).
- GT `uscis_naturalization_interview_rescheduled_friday_8am_field_office` tests V2 schedule-change class under NEW within-class incident distinct from C1 cardio_appt_rescheduled (medical-cardiology vs federal-immigration), C3 court_hearing_moved_same_day (state civil court vs USCIS), C4 pediatrician_visit_advanced_today_4pm (pediatric-medicine vs USCIS), C5 dental_implant_surgery_rescheduled (oral surgery vs USCIS). **4x→5x cross-trace lift** (C1+C3+C4+C5+C7). **PATH (a) primary lift #1.**
- GT `fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k` tests V2 financial/deadline class under NEW within-class incident distinct from C1 student_loan_repayment_resume (federal-loan vs FBAR), C2 property_tax_installment (gov property-tax vs FBAR), C3 homeowner_insurance_lapse (insurance vs FBAR), C5 quarterly_estimated_tax (IRS Title-26 vs FinCEN Title-31), C6 iso_exercise_window (employer-equity vs foreign-account reporting). **5x→6x cross-trace lift** (C1+C2+C3+C5+C6+C7).
- GT `tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow` tests V2 message/delivery class under NEW within-class incident distinct from C1 legal_doc_courier_signature (unspecified courier civil-doc vs tenant-defense attorney-paralegal eviction-stay motion), C3 partner_voicemail_ring_pickup_jeweler (partner-domestic-errand vs attorney-civil-litigation), C4 hospital_grandmother_hip_fracture (hospital-medical vs attorney-legal-pickup), C6 mother_in_law_chemo_infusion_ride_request (MIL-medical-ride vs attorney-legal-pickup). **4x→5x cross-trace lift** (C1+C3+C4+C6+C7).
- GT `kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m` tests V2 production/on-call class under NEW within-class incident distinct from C2 datastore_replica_failover_p1 (Postgres failover vs Kafka broker election), C3 tls_cert_expiry_3hr_customer_endpoint (TLS cert vs Kafka), C4 disk_space_critical_var_log (single-host disk vs distributed-broker-fleet), C5 redis_memory_saturation_eviction_cascade (Redis cache OOM vs Kafka broker quorum). **4x→5x cross-trace lift** (C2+C3+C4+C5+C7). **PATH (a) primary lift #2.**

**V2 EXISTING NO compliant-content distractor coverage at C7 (4 distractors; 1 feature-announcement lift 3x→4x as path-(a) primary distractor + 3 V2 NO 4x classes lifted 4x→5x):**
- Distractor `postman_workspace_collection_runner_v11_javascript_runtime_announcement_no_action` tests V2 feature-announcement/app-update class at **3x→4x triangulation** (C2 chrome_extension_marketplace_update + C3 notion_new_dashboard_feature_tour + C5 vscode_marketplace_verified_publisher_tab_launch + C7 postman_collection_runner_v11; distinct on product / category / mechanism). **PATH (a) primary distractor lift.** Closes V2 NO ≥4x for 4 of 5 classes; social-channel-invite still at 3x (reserved for C8/C9/C10 lift).
- Distractor `github_actions_weekly_workflow_health_digest_all_green_zero_flaky_rerun` tests V2 routine-status/heartbeat class at **4x→5x** triangulation (C3 cloud_backup_daily + C4 ssl_monitor_weekly + C5 K8s_autoscaler_monthly + C6 datadog_synthetic_daily + C7 github_actions_weekly; distinct on platform, monitoring class, cadence).
- Distractor `goldleaf_stationery_quarterly_catalog_handmade_paper_fountain_pen_spring_no_action` tests V2 marketing/newsletter class at **4x→5x** triangulation (C3 kitchen_gear + C4 tea_club + C5 inkwell_indie_bookstore + C6 aperture_camera_gear + C7 goldleaf_stationery; distinct on product category + commerce model).
- Distractor `wednesday_midweek_checkpoint_briefing_no_priority_flagged_calendar_clear` tests V2 generic-daily-briefing class at **4x→5x** triangulation (C3 morning_briefing + C4 evening_briefing + C5 friday_weekly_recap + C6 monday_week_lookahead + C7 wednesday_midweek_checkpoint; distinct on cadence + target horizon).

**V2 NO class skipped at C7:** social-channel-invite stays at 3x (C1 discord_unread_digest + C4 slack_frontend_weekly_community_invite + C6 mastodon_instance_follow_suggestion). C7 path-(a) selected feature-announcement V2 NO for the 3x→4x lift; social-channel-invite defers to C8/C9/C10 (3x→4x lift would complete V2 NO ≥4x for ALL 5 classes).

**Coverage summary at C7:** Maximal H4-evidence-base lift on the asymmetrically-weakest V2 YES + V2 NO compliant-content cells under PATH (a) discipline: schedule-change V2 YES 4x→5x + production/on-call V2 YES 4x→5x (closes V2 YES ≥5x for 4 of 6 classes) + feature-announcement V2 NO 3x→4x (closes V2 NO ≥4x for 4 of 5 classes); ADDITIONAL saturating lifts: urgent-safety + financial/deadline V2 YES 5x→6x + message/delivery V2 YES 4x→5x (5-GT-shape-constraint lift) + routine-status + marketing/newsletter + generic-daily-briefing V2 NO 4x→5x. Cross-trace coverage state through C7: **V4 NEW YES**: 4 total instances (UNCHANGED; scarcity-bounded 2x at C1+C6 + family-milestone 2x at C2+C5; symmetric closure preserved); **V4 NEW NO**: 6 total instances (UNCHANGED; 3 subclauses × 2x each at C1+C2; saturated state preserved); **V2 EXISTING YES classes**: urgent-safety 6x (C1+C2+C4+C5+C6+C7), schedule-change 5x (C1+C3+C4+C5+C7), financial/deadline 6x (C1+C2+C3+C5+C6+C7), production/on-call 5x (C2+C3+C4+C5+C7), message/delivery 5x (C1+C3+C4+C6+C7), weather-alert 4x UNCHANGED (C2+C3+C4+C6; reserved for C8 4x→5x lift); **V2 EXISTING NO classes**: routine-status 5x (C3+C4+C5+C6+C7), marketing/newsletter 5x (C3+C4+C5+C6+C7), generic-daily-briefing 5x (C3+C4+C5+C6+C7), feature-announcement 4x (C2+C3+C5+C7), social-channel-invite 3x UNCHANGED (C1+C4+C6; reserved for C8/C9/C10 3x→4x lift to complete V2 NO ≥4x for ALL 5 classes). 3 traces remain for combined-N=20 closure; future C8..C10 may continue compliant-content discipline at the remaining 4x V2 YES class (weather-alert 4x→5x candidate) AND remaining 3x V2 NO class (social-channel-invite 3x→4x candidate); C10 has free shape for V4 mechanism 3rd-repeat or higher-order shape changes.

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v27-attempt-2-accepted.json` (SHA256 `66316c238fad8b6224bc8d8cf9a6c1dff7045fd8207abd1391f2de3a42a3f3e1`; 49119 bytes; D-C1.2 schema with step_3_5_pre_flight run-1 first-run-PASS + run-2 re-PASS log + V4-mechanism-zero + V2 EXISTING YES/NO compliant-content coverage with explicit path-(a) defensibility self-check + 4x→5x V2 YES lift on 2 path-(a) primary classes + 5x→6x V2 YES lift on 2 saturating classes + 4x→5x V2 YES lift on 1 shape-constraint class + 3x→4x V2 NO path-(a) primary distractor + 4x→5x V2 NO lift on 3 saturating distractor classes + full audit-gate evidence + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata).

### Banned-list state delta at C7

- Pre-C7 (C6 end-state, ships at C7): 181 IDs / 102 themes / 101 tuples.
- C7 contributions from accepted test_v27 (to be incorporated into `21c-banned-list-pre-c8.txt` at C8 land time per D-C1.1):
  - **+9 IDs:** `self_chest_pressure_left_arm_radiating_911_aspirin_chewed_4min_eta_paramedics`, `uscis_naturalization_interview_rescheduled_friday_8am_field_office`, `fbar_fincen_114_foreign_account_oct_15_deadline_aggregate_above_10k`, `tenant_attorney_eviction_stay_motion_paperwork_5pm_show_cause_court_tomorrow`, `kafka_order_pipeline_broker_election_under_replicated_p1_consumer_lag_8m`, `wednesday_midweek_checkpoint_briefing_no_priority_flagged_calendar_clear`, `github_actions_weekly_workflow_health_digest_all_green_zero_flaky_rerun`, `postman_workspace_collection_runner_v11_javascript_runtime_announcement_no_action`, `goldleaf_stationery_quarterly_catalog_handmade_paper_fountain_pen_spring_no_action`.
  - **+5 themes (GT-regime regime column verbatim):** urgent safety/security issue (V2 EXISTING YES) — user-self acute coronary syndrome MI symptoms with live 911 dispatcher + chewed-aspirin protocol + 4-min paramedic ETA; schedule change affecting the user personally (V2 EXISTING YES) — USCIS N-400 naturalization interview moved by adjudications officer with tomorrow-noon confirm-or-default-cancellation deadline; financial/deadline obligation (V2 EXISTING YES) — FBAR FinCEN-114 foreign-bank-account reporting deadline at midnight Pacific tonight with $129,210/violation willful penalty; message or delivery directed personally to the user (V2 EXISTING YES) — tenant-defense attorney paralegal voicemail with eviction-stay motion pickup-and-signature by 5pm before tomorrow show-cause hearing; production/on-call alert (V2 EXISTING YES) — PagerDuty P1 on Kafka broker fleet with unstable partition-leadership election + 200 under-replicated partitions + 8M consumer-lag + 75-min runbook escalation.
  - **+5 tuples (GT keyword tuples verbatim):** `(aspirin, dispatcher)`, `(uscis, interview)`, `(fbar, foreign)`, `(attorney, eviction)`, `(kafka, broker)`.
- Post-C7 (input state for C8): 190 IDs / 107 themes / 106 tuples. File ships at C8 land time as `runs/data/21c-banned-list-pre-c8.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C7

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at both attempts).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (9 cumulative milestone attempts < 25; 7 accepted traces toward target of 10).
- Retry-cap-3 on test_v27 (D-C1.5 #3): **not exhausted** (2/3 used; FAIL at attempt #1 step 6 → PASS at attempt #2; 1 retry remaining had attempt #2 not accepted).

### Cumulative milestone-spend through Commit C7

Commit C7 spend: $0 at attempt #1 + $0 at attempt #2 (both attempts in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C7: $0.7081 (unchanged from Commit C6; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C7 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21..test_v26 definitions — frozen historical artifacts (only NEW `test_trace_v27` added at C7, plus the registry line `"test_v27": test_trace_v27,`).
- `runs/data/21c-banned-list-pre-c{1,2,3,4,5,6}.{txt,json}` + `runs/data/21c-author-test_v{21,22,23,24,25,26}-*.json` — frozen at C1+C2+C3+C4+C5+C6; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C7.

### Next: Commit C8 — fresh-session trace authoring `test_v28`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c8.{txt,json}` (NEW; reflects test_v21..v27 contributions; 190 IDs / 107 themes / 106 tuples) as the pre-C8 starting state. Self-restate gate rendered against the pre-C8 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 9/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C / D-C6.attempt1.C / D-C7.attempt1.C) carries forward as standing per-attempt author discipline. C7 attempt-1's step-6 8-gram drift rejection at distractor-boilerplate-template-phrasing is a NEW author-discipline reminder for C8+ — formulaic marketing-email/briefing-template closing phrases should be paraphrased per-trace rather than copied verbatim across C-traces (especially for the V2 NO marketing/newsletter + generic-daily-briefing classes where formulaic-closer phrasing is common). With C7 lifting V2 YES schedule-change + production/on-call to 5x (path-(a) primary lifts) + feature-announcement V2 NO to 4x (path-(a) primary distractor lift) + 4 saturating lifts (urgent-safety + financial/deadline 5x→6x; message/delivery 4x→5x; 3 V2 NO classes 4x→5x), C8 may pursue (1) weather-alert V2 YES 4x→5x to close V2 YES ≥5x for ALL 6 classes, (2) social-channel-invite V2 NO 3x→4x to complete V2 NO ≥4x for ALL 5 classes, (3) 3rd-repeat V4 NEW YES (after the symmetric closure at C6 + path-(a) protected at C7) only if defensible vs H4 denominator growth, or (4) higher-order GT-shape changes if H4 evidence-base saturation warrants; defended at the C8 Plan.

Commit C8 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.


---

## Commit C8 — test_v28 (2026-05-18)

**Verdict: test_v28 ACCEPTED at attempt 1/3; audit-gate 8/8 PASS.** Cumulative milestone attempt count 10/25 through Commit C8 (C1 attempt-1 + C2 attempt-1 + C2 attempt-2 + C3 attempt-1 + C4 attempt-1 + C5 attempt-1 + C6 attempt-1 + C7 attempt-1 + C7 attempt-2 + C8 attempt-1); 2 traces remaining for combined-N=20 closure. Self-restate pre-flight gate per §D4 prevented the M11a-class structural-parsing-failure mode at this attempt (M11a-extension structural-parsing-failure rate to date: 0/10 attempts). Step 3.5 pre-flight keyword literal-substring verification (D-C8.attempt1.C inheriting verbatim from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C / D-C6.attempt1.C / D-C7.attempt1.C) PASSed on first run with no in-session iteration required — mirrors C4 + C5 + C6 + C7-attempt-1 first-run-PASS precedents. **D-C8.attempt1.C boilerplate-paraphrase author-discipline (NEW at C8 per C7-attempt-1-step-6 rejection; pre-flight authoring discipline only, NOT a C-protocol governance change) applied at draft time to D3 marketing/newsletter closing + D4 generic-daily-briefing middle sentence; audit-gate step 6 PASSed first-run with 0 8-gram overlaps vs prior dev/test traces — demonstrates draft-time paraphrase discipline effective at preventing the C7-attempt-1 boilerplate-template convergence mode.**

### C-protocol governance decisions inherited from C1 + C2 + C3 + C4 + C5 + C6 + C7

D-C1.1..D-C1.6 locked at C1 first-land (`1fefe6e`) inherit VERBATIM at C8 with no re-litigation per "no scope drift within a milestone" operating principle. D-C2.A..D-C2.D (locked at C2 attempt-#1 Plan) + D-C2.attempt2.A..D-C2.attempt2.D (locked at C2 attempt-#2 Plan `f9808c8`) + D-C3.attempt1.A..D-C3.attempt1.D (locked at C3 attempt-#1 Plan `9f84a01`) + D-C4.attempt1.A..D-C4.attempt1.D (locked at C4 attempt-#1 Plan `e998a07`) + D-C5.attempt1.A..D-C5.attempt1.D (locked at C5 attempt-#1 Plan `b349b23`) + D-C6.attempt1.A..D-C6.attempt1.D (locked at C6 attempt-#1 Plan `d8ce8a4`) + D-C7.attempt1.A..D-C7.attempt1.D (locked at C7 attempt-#1 Plan `3d1b1ad`) also inherit VERBATIM at C8. The per-attempt author discipline added at C2 attempt #2 (Step 3.5 pre-flight) carries forward as standing author discipline through C8..C10.

### C8 attempt-specific Plan locks (per-attempt discipline; not C-protocol governance)

| Decision | Lock |
|---|---|
| **D-C8.attempt1.A state-confirm checklist** | Pre-attempt-#1 state confirmed via on-disk verifications: main HEAD `3d1b1ad` (M11a-extension Commit C7); working tree clean; `sandbox/event_trace.py` sha256 `77e319f37d04c891098a76421890ba5719386dfa04a9c43b5bf29e3dfca2f59d` (95595 bytes; HEAD-bit-identical post-C7 incl. `test_trace_v27` + registry line); V4 prompt string sha256 `09be309de5609a3c599d401e93ee4b35e655be24232ece6570a51893f80f56a6` (1851 bytes; bytewise-identical to §D1 lock — `agent/arbiter.py` last touched at `adc1cba` Commit B, unchanged through C1+C2+C3+C4+C5+C6+C7); `runs/data/21c-banned-list-pre-c7.{txt,json}` sha256 `e03a28c4…` + `2c0f02dc…` / 181/102/101 counts verified. D-C7.attempt1.A precedent mirrored verbatim. |
| **D-C8.attempt1.B subclause coverage brief inheritance + C8-specific path-lock** | D-C2.B / D-C3.attempt1.B / D-C4.attempt1.B / D-C5.attempt1.B / D-C6.attempt1.B / D-C7.attempt1.B brief inherits VERBATIM. C8-specific path-lock (locked at Plan): **PATH (a) — compliant-content lift CONTINUATION (from C7)**. Trace shape: 5 V2 EXISTING YES GTs across 5 distinct V2 YES classes (**weather-alert 4x→5x as path-(a) primary lift #1 — closes V2 YES ≥5x for ALL 6 V2 YES classes**; schedule-change 5x→6x + production/on-call 5x→6x + message/delivery 5x→6x as saturating lifts; financial/deadline 6x→7x as saturating lift) + **zero V4 mechanism GTs** (preserves C6's symmetric V4 NEW YES closure at 2x each subclause AND the V4 NEW NO saturated state at 2x each of 3 subclauses; identical to C7 zero-V4 shape) + 4 V2 EXISTING NO distractors (**social-channel-invite 3x→4x as path-(a) primary distractor lift — closes V2 NO ≥4x for ALL 5 V2 NO classes**; routine-status + marketing/newsletter + generic-daily-briefing each lifting 5x→6x as saturating lifts). Defensibility framing: PATH (a) at C8 targets the **LAST remaining 4x V2 YES class (weather-alert)** AND the **LAST remaining 3x V2 NO class (social-channel-invite)** in a single trace — strongest reviewer-defensible compliant-content endpoint achievable in one C-trace. PATH (b) V4 NEW YES 3rd-repeat explicitly rejected at C8 Plan adversarial-reviewer walkthrough (re-opens within-V4-NEW-YES symmetric closure C6 deliberately closed; C9 can pursue this defensibly post-path-(a) completion); PATH (c) V4 NEW NO 3rd-repeat explicitly rejected (saturated; dominated by H4 denominator growth); PATH (d) within-V2-class 5-GT triangulation explicitly rejected (reviewer-flag risk; over-weights one class at single-trace scope). Skipped at C8 V2 NO class: feature-announcement (stays at 4x post-C7; already ≥4x — no additional lift needed under path-(a) closure). Net post-C8 coverage state: **V2 YES 6 of 6 classes at ≥5x AND V2 NO 5 of 5 classes at ≥4x** + V4 NEW YES symmetric closure preserved at 2x each subclause + V4 NEW NO saturated state preserved at 2x each of 3 subclauses. |
| **D-C8.attempt1.C Step 3.5 pre-flight keyword literal-substring verification + NEW boilerplate-paraphrase author-discipline** | Inherits VERBATIM from D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C / D-C6.attempt1.C / D-C7.attempt1.C. Mechanically verify every GT keyword tuple element appears as case-insensitive substring of that GT's `Event.content` via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v28'); [print(f'{kw!r} in {g.event.id}: {kw.lower() in g.event.content.lower()}') for g in t.ground_truth for kw in g.keywords]"`. ALL must print `True`. ANY `False` → revise GT content OR replace keyword; revert `sandbox/event_trace.py` if schema check was attempted; re-author Step 3; re-run Step 3.5. Does NOT consume retry-cap budget per D-C1.4. **NEW C8 author-discipline reminder per C7 step-6 rejection precedent (NOT a C-protocol governance change; pre-flight authoring discipline only): paraphrase formulaic distractor closing-sentence and template middle-sentence phrasings per-trace, especially for V2 NO marketing/newsletter + generic-daily-briefing classes where formulaic-closer phrasings are common. Single-sentence test: would the closing sentence of a marketing email or briefing read the same regardless of trace? If YES → paraphrase per-trace. The audit-gate step 6 still catches 8-gram convergence mechanically at the pre-submission gate; this discipline is the draft-time pre-flight to avoid the C7-attempt-1-class rejection mode.** |
| **D-C8.attempt1.D commit shape** | D-C7.attempt1.D commit shape extension (multi-attempt-capable; identical to D-C2.attempt2.D bundling pattern) inherits VERBATIM. Normal attempt-#1-accepts trajectory at C8 — single accepted-attempt artifact bundled in C8 commit per D-C1.6 acceptance discipline; no rejected-attempt bundling required since attempt #1 accepted on first audit-gate run. Multi-attempt-capability preserved in commit shape; would have engaged at attempt-#1 rejection but did not fire at C8. |

### Banned-list starting state (C7 end-state)

- Source artifact: `runs/data/21c-banned-list-pre-c8.txt` (SHA256 `12e385aba23486d5d075687dd765d21b18498f5ab8c0e8df1b5ae6cb09ca115f`; 22614 bytes; 190 banned event_ids + 107 banned themes + 106 banned keyword tuples).
- Parallel structured artifact: `runs/data/21c-banned-list-pre-c8.json` (SHA256 `e1c10669e68d4be99f061359a8f97da4e09db52dd8db64a99eaa53cda58d59f6`; 22022 bytes; same content in structured schema; counts mechanically verified unique).
- Provenance: extended at C8-attempt-#1 session by appending C7's accepted test_v27 contributions (+9 IDs / +5 themes / +5 tuples) to the pre-C7 banned-list (`e03a28c4…` / `2c0f02dc…`, 181/102/101) per D-C1.1 invariant. Pre-C7 files NOT mutated (verified bit-identical pre and post C8 authoring; sha256 round-trip confirms `e03a28c4…` + `2c0f02dc…` unchanged).

### Self-restate pre-flight gate (§D4 + D14-H7)

- Command: `uv run python -m eval.author_trace --banned-list runs/data/21c-banned-list-pre-c8.txt > /tmp/m11a-ext-c8-restate-prompt.txt`
- Rendered prompt SHA256: `5384c2a517cd0edf9620a552225325d487bf353a1959331b3c871a36e04981d5` (23023 bytes).
- Self-restate response authored in own words distinct from C1's response + C2 attempt-#1's response + C2 attempt-#2's response + C3 attempt-#1's response + C4 attempt-#1's response + C5 attempt-#1's response + C6 attempt-#1's response + C7 attempt-#1's response + C7 attempt-#2's response per fresh-session-restart-from-scratch discipline; full text archived verbatim in artifact `21c-author-test_v28-attempt-1-accepted.json` `self_restate_response_verbatim` field.
- Outcome: structural-parsing-failure mode (M11a 3/9 = 33% baseline) NOT triggered; schema check via `get_trace('test_v28')` passes on first import.

### Step 3.5 pre-flight keyword literal-substring verification (D-C8.attempt1.C; first-run PASS)

| Run | Outcome | Detail |
|---|---|---|
| 1 | **PASS** — all 10 pairs print `True` | `('ice', noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel) True; ('glaze', noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel) True; ('mortgage', mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay) True; ('closing', mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay) True; ('elasticsearch', elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min) True; ('shard', elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min) True; ('executor', older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback) True; ('appraiser', older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback) True; ('heloc', heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email) True; ('draw', heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email) True`. No in-session iteration required. |

**Reviewer-defense (Step 3.5 working as designed):** Step 3.5 PASSed on first run for C8, mirroring C4 + C5 + C6 + C7-attempt-1 first-run-PASS precedents (vs C3 attempt-1's in-session iteration on `('pickup', partner_voicemail_ring_pickup_jeweler)` two-word/one-word misalignment). Content authored with explicit single-word keyword-substring attention at draft time: `("ice", "glaze")` aligned with "ice-storm warning" + "three-quarter inch of glaze" + "glazed sidewalks"; `("mortgage", "closing")` aligned with "Mortgage-underwriting team email: the closing on the Westwood Avenue property"; `("elasticsearch", "shard")` aligned with "customer-facing search-platform Elasticsearch cluster" + "two primary shards on the catalog-search index marked unassigned"; `("executor", "appraiser")` aligned with "the named executor of your late father's estate" + "the certified appraiser engaged through the probate court"; `("heloc", "draw")` aligned with "home-equity-line-of-credit lender: the HELOC draw period on the 2014-originated line". Discipline carry-forward from D-C2.attempt2.C → D-C3.attempt1.C → D-C4.attempt1.C → D-C5.attempt1.C → D-C6.attempt1.C → D-C7.attempt1.C → D-C8.attempt1.C unbroken; attribution clean: self-restate gate → structural-parsing (audit step 1 territory); Step 3.5 → M8b keyword/content alignment (audit step 2 territory); NEW C8 boilerplate-paraphrase author-discipline → drift-overlap-b (audit step 6 territory) pre-flight only.

### Audit-gate results (8/8 PASS)

| Step | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema check via `get_trace('test_v28')` | PASS | `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v28'); print(t.name, len(t.events), len(t.ground_truth), t.duration_s)"` yields `test_v28 9 5 810.0` with no exception. duration_s=810.0 is the correctly computed `Trace.duration_s` property `max(last_gt_completion, last_event_time) + 30.0` for the test_v28 sim_time + window distribution (5 GTs at 210/370/470/540/640 with windows 200/240/220/240/90 yields last_gt_completion 780.0 [older_sister_executor at 540+240]; events at 30/75/140/210/370/470/540/600/640 yields last_event_time 640.0; max(780, 640) + 30 = 810). |
| 2 | Keyword/content alignment (M8b hard constraint) | PASS | All 10 `(kw, content.lower())` substring checks pass (Step 3.5 pre-flight + audit-gate verification both PASS at the single run). Pairs: `(ice, noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel)`; `(glaze, noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel)`; `(mortgage, mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay)`; `(closing, mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay)`; `(elasticsearch, elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min)`; `(shard, elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min)`; `(executor, older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback)`; `(appraiser, older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback)`; `(heloc, heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email)`; `(draw, heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email)`. |
| 3a | Banned event_id literal review (vs 190 banned IDs) | PASS | Mechanical set-intersection: 0 collisions across test_v28's 9 event_ids. |
| 3b | Banned theme semantic review (vs 107 banned themes) | PASS | Per-GT hand-audit verdicts archived in artifact `audit_gate_result.step_3b_banned_theme_semantic_review.per_gt_distinguishing_qualifiers`. All 5 GT themes pass with distinguishing qualifiers vs nearest banned predecessors: GT1 V2 weather-alert ice-storm-glaze-accretion distinct from C2 flash-flood + C3 dust-storm + C4 tornado-watch + C6 wildfire-smoke + M10b earthquake + M11a boil-water on hazard mechanism (ice-storm freezing-rain glaze vs precipitation/mineral/convective-rotation/PM2.5/tectonic/utility-microbial); GT2 V2 schedule-change mortgage-closing-rescheduled distinct from C1 cardio + C3 court + C4 pediatrician + C5 dental + C7 USCIS on domain (real-estate-financing closing vs medical-specialty/civil-court/pediatric-medicine/oral-surgery/federal-immigration); GT3 V2 production/on-call Elasticsearch-shard-RED distinct from C2 Postgres-failover + C3 TLS-expiry + C4 disk-space + C5 redis-memory + C7 Kafka-broker on technology (Elasticsearch search-platform shard-allocation vs RDBMS-failover/cert-rotation/storage-OOM/cache-saturation/event-stream-quorum); GT4 V2 message/delivery older-sister-executor-callback distinct from C1 courier + C3 partner-jeweler + C4 hospital-grandmother + C6 MIL-chemo + C7 tenant-attorney + M10b sister-airport + M10b photographer on sender + reason + relation (sibling-as-executor + probate-court-ordered-appraiser-appointment vs courier/partner/hospital/MIL/attorney/airport-pickup/photographer-engagement); GT5 V2 financial/deadline HELOC-draw-period distinct from C1 student-loan + C2 property-tax + C3 homeowner-insurance + C5 IRS-quarterly + C6 ISO-exercise + C7 FBAR on domain (HELOC draw-period-conversion-election vs federal-loan/property-tax/insurance/IRS-quarterly/employer-equity/FBAR-Title-31). |
| 3c | Banned keyword tuple bytewise review (vs 106 banned tuples) | PASS | Mechanical set-intersection: 0 bytewise collisions across 5 GT tuples `[(ice, glaze), (mortgage, closing), (elasticsearch, shard), (executor, appraiser), (heloc, draw)]`. All 5 tuples bytewise-distinct vs all 106 banned predecessors including the semantically-adjacent banned tuples in same V2 classes (weather: `(weather, rain)` + `(flood, warning)` + `(dust, storm)` + `(tornado, watch)` + `(wildfire, smoke)`; schedule-change: `(appointment, rescheduled)` + `(court, hearing)` + `(pediatrician, advanced)` + `(dental, implant)` + `(uscis, interview)`; production/on-call: `(database, failover)` + `(tls, expiry)` + `(disk, space)` + `(redis, memory)` + `(kafka, broker)`; message/delivery: `(courier, signature)` + `(ring, pickup)` + `(hospital, grandmother)` + `(chemo, infusion)` + `(attorney, eviction)`; financial/deadline: `(loan, repayment)` + `(property, tax)` + `(insurance, lapse)` + `(quarterly, tax)` + `(iso, exercise)` + `(fbar, foreign)`). |
| 4 | **Cross-trace literal-ID collision check** (HALT-gate per D-C1.5 #1) | PASS | Mechanical set-intersection of test_v28's 9 event_ids vs union of dev_v1/dev_v2/test_v1..v8/v11..v15/v21..v27 event_ids: 0 collisions against 190 prior event_ids across 22 prior trace definitions. **HALT-trigger NOT fired.** |
| 5 | Drift strong-overlap (a) GT tuple bytewise (cross-trace) | PASS | Same mechanical set-intersection as 3c against the union-of-prior-GT-tuples (106 unique across dev_v1..test_v27): 0 collisions. |
| 6 | Drift strong-overlap (b) ≥8-word verbatim phrase | PASS | 8-gram set-intersection: test_v28 has 1370 unique 8-grams across content+briefing+intents fields (lowercased, word-token regex `[\w'-]+` tokenization); prior dev/test traces have 7937 unique 8-grams; overlap = 0. **D-C8.attempt1.C boilerplate-paraphrase author-discipline (added at C8 per C7-attempt-1 step-6 rejection precedent) effective at draft time:** D3 Meridian Games marketing-email closing authored without "unsubscribe...seasonal mailings...account preferences" template (rewritten as "Replies and product questions can be directed to the catalog-mailbox alias maintained by the customer-support team."); D4 Thursday-pre-weekend-wrap briefing middle sentence authored without "no priority items are flagged from your project list, sprint board, or stakeholder asks" template (rewritten as "Nothing on the personal-task list or the stakeholder backlog requires a response before next Monday's standup."). Step 6 first-run PASS at attempt-1 with 0 overlaps demonstrates draft-time discipline effective at preventing the C7-attempt-1 boilerplate-template convergence mode at the pre-submission gate. |

### GT-regime classification (audit step 7; for Commit D per-trace observations table)

- GT 1 `noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel` — **weather alert (V2 EXISTING YES)**: NWS upgraded the overnight freezing-rain advisory to a full ice-storm warning for the metro area through tomorrow afternoon; one-quarter to three-quarter inch glaze accretion across the urban core and foothill towns between 2am and 7am; thirty-six-hour outage projection on suburban distribution feeders once glaze depth crosses the half-inch threshold; no-unnecessary-travel advisory in effect; ER visits from falls on glazed sidewalks during the last comparable storm tripled within four hours of first accretion. **4x→5x cross-trace lift (C2+C3+C4+C6+C8).** **PATH (a) primary lift #1 — closes V2 YES ≥5x for ALL 6 V2 YES classes.**
- GT 2 `mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay` — **schedule change affecting the user personally (V2 EXISTING YES)**: mortgage-underwriting team email; Westwood Avenue property closing rescheduled from today 3pm to Friday 10am at the title-company office downtown; final underwriting conditions came in late from the appraisal-review desk + 24-hour funding clearance through the warehouse line; noon-today reply-or-lose-rate-lock-grace-period deadline; certified-funds cashier's check + homeowners-policy declaration page + government-issued photo ID required at closing. **5x→6x cross-trace lift (C1+C3+C4+C5+C7+C8) — saturating lift.**
- GT 3 `elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min` — **production/on-call alert (V2 EXISTING YES)**: PagerDuty severity-one incident on customer-facing search-platform Elasticsearch cluster prod-search-es-east-01 at fifteen-thirty-five UTC; index status RED with 2 primary shards on catalog-search index unassigned + zero automatic shard-recovery progress; storefront search API 5xx past 40% + downstream recommendation/personalization cold-cache fallback; engineering leadership pages at 50-min mark per SEV-one playbook; secondary on-call pager this rotation + primary on war-room bridge requesting 90-second phone-handshake; shard-allocation explain output points at disk-high-watermark trigger on 3 hot-tier nodes. **5x→6x cross-trace lift (C2+C3+C4+C5+C7+C8) — saturating lift.**
- GT 4 `older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback` — **message or delivery directed personally to the user (V2 EXISTING YES)**: voicemail from older sister Tess (named executor of late father's estate); certified appraiser engaged through probate court can only do safe-deposit-box inventory at downtown First National branch tomorrow 9am before leaving town for holiday weekend; both surviving siblings required present per probate-court order; box holds original signed will + wedding-band collection + two unconfirmed gold coins; callback before this evening required or appraiser reschedules next week + estate-distribution timeline pushes one full month due to probate-court calendar congestion. **5x→6x cross-trace lift (C1+C3+C4+C6+C7+C8) — saturating lift.**
- GT 5 `heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email` — **financial/deadline obligation (V2 EXISTING YES)**: notice from home-equity-line-of-credit lender; HELOC draw period on 2014-originated line expires Friday 5pm Pacific + line automatically converts to 15-year amortization at prime+1.5; alternative two-step product (15-year fixed-rate term-lock at 6.85% on current balance with no further draws) must be submitted through secure-message portal before same 5pm deadline; unused original draw cap reverts to bank at conversion + cannot be reinstated without fresh application + updated home appraisal. **6x→7x cross-trace lift (C1+C2+C3+C5+C6+C7+C8) — saturating lift.**

### Defensibility self-check per §D9 defense #8 (audit step 8; V4-mechanism + V2-class subclause coverage)

**V4 NEW YES coverage at C8:** **ZERO instances** (intentional per D-C8.attempt1.B locked path-(a) compliant-content focus, mirror of C7 zero-V4 path-(a) lock). Cross-trace state: V4 NEW YES total instances **4 (UNCHANGED)** — scarcity-bounded-opportunity 2x at C1+C6; family-milestone-with-social-cost 2x at C2+C5; symmetric closure achieved at C6 + preserved at C7 + preserved at C8. **Defensibility:** PATH (b) V4 NEW YES 3rd-repeat was explicitly rejected at C8 Plan adversarial-reviewer walkthrough — re-opening the within-V4-NEW-YES symmetric closure C6 closed would dominate any 4→5 marginal-info gain on cross-V4-mechanism asymmetry vs V4 NEW NO 6. PATH (a) compliant-content lift is dominant for the LAST remaining 4x V2 YES (weather-alert) AND LAST remaining 3x V2 NO (social-channel-invite) classes — single-trace simultaneous closure at C8 delivers strongest reviewer-defensible compliant-content endpoint achievable in one C-trace.

**V4 NEW NO coverage at C8:** **ZERO instances** (intentional per D-C8.attempt1.B locked path-(a) compliant-content focus). Cross-trace state: V4 NEW NO total instances **6 (UNCHANGED)** — 3 subclauses × 2x each at C1+C2; saturated state preserved through C3..C8. **Defensibility:** PATH (c) V4 NEW NO 3rd-repeat was explicitly rejected at C5/C6/C7/C8 Plans (saturated 3/3 at 2x; 3rd-repeat dominated by H4 denominator growth where any compliant-content distractor adds equivalent H4 sample-density regardless of V4 NEW NO subclause representation).

**V2 EXISTING YES compliant-content coverage at C8 (5 GTs across 5 distinct V2 YES classes; 1 path-(a) primary lift at 4x→5x + 4 saturating lifts at 5x→6x or 6x→7x):**
- GT `noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel` tests V2 weather-alert class under NEW within-class incident distinct from C2 flash-flood (precipitation), C3 dust-storm (mineral wind-driven), C4 tornado-watch (convective-supercell rotation), C6 wildfire-smoke (PM2.5 air-quality plume). **4x→5x cross-trace lift** (C2+C3+C4+C6+C8). **PATH (a) primary lift #1.**
- GT `mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay` tests V2 schedule-change class under NEW within-class incident distinct from C1 cardio (cardiology medical), C3 court-hearing (state civil-court), C4 pediatrician (pediatric medicine), C5 dental-implant (oral surgery), C7 USCIS (federal immigration). **5x→6x cross-trace lift** (C1+C3+C4+C5+C7+C8) — saturating.
- GT `elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min` tests V2 production/on-call class under NEW within-class incident distinct from C2 Postgres (RDBMS failover), C3 TLS (cert expiry), C4 disk (single-host disk-space), C5 Redis (cache OOM), C7 Kafka (broker fleet partition-leadership). **5x→6x cross-trace lift** (C2+C3+C4+C5+C7+C8) — saturating.
- GT `older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback` tests V2 message/delivery class under NEW within-class incident distinct from C1 legal-courier (courier civil-doc), C3 partner-jeweler (partner-domestic-errand), C4 hospital-grandmother (hospital admitting-desk), C6 MIL-chemo (MIL-medical-ride), C7 tenant-attorney (attorney-paralegal). **5x→6x cross-trace lift** (C1+C3+C4+C6+C7+C8) — saturating.
- GT `heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email` tests V2 financial/deadline class under NEW within-class incident distinct from C1 student-loan (federal-loan), C2 property-tax (county-tax), C3 homeowner-insurance (insurance auto-debit), C5 IRS-quarterly (federal-tax), C6 ISO-exercise (employer-equity), C7 FBAR (FinCEN-Title-31 foreign-account). **6x→7x cross-trace lift** (C1+C2+C3+C5+C6+C7+C8) — saturating.

**V2 EXISTING NO compliant-content distractor coverage at C8 (4 distractors; 1 path-(a) primary distractor lift at 3x→4x + 3 saturating lifts at 5x→6x):**
- Distractor `bluesky_starter_pack_invite_curator_recommended_follow_data_journalism_circle` tests V2 social-channel-invite class at **3x→4x triangulation** (C1 discord_unread_digest + C4 slack_frontend_weekly + C6 mastodon_instance_follow_suggestion + C8 bluesky_starter_pack_invite; distinct on platform Discord/Slack/Mastodon/Bluesky, federation model centralized/centralized/federated/AT-Protocol, channel type unread/frontend-channel/follow-suggestion/starter-pack-bundle). **PATH (a) primary distractor lift — closes V2 NO ≥4x for ALL 5 V2 NO classes post-C8.**
- Distractor `terraform_state_drift_weekly_scan_zero_resources_modified_clean_all_workspaces` tests V2 routine-status/heartbeat class at **5x→6x** triangulation (C3 cloud-backup-daily + C4 ssl-monitor-weekly + C5 K8s-autoscaler-monthly + C6 datadog-synthetic-daily + C7 github-actions-workflow-weekly + C8 terraform-state-drift-weekly; distinct on tool, monitoring class, cadence, infra-domain).
- Distractor `meridian_games_summer_catalog_strategy_titles_2026_no_action_required` tests V2 marketing/newsletter class at **5x→6x** triangulation (C3 kitchen-gear + C4 tea-club + C5 inkwell-bookstore + C6 aperture-camera + C7 goldleaf-stationery + C8 meridian-games; distinct on product category, commerce model, cadence). **D-C8.attempt1.C boilerplate-paraphrase discipline applied:** closing rewritten without "unsubscribe...seasonal mailings...account preferences" template — instead "Replies and product questions can be directed to the catalog-mailbox alias maintained by the customer-support team."
- Distractor `thursday_pre_weekend_wrap_briefing_no_overdue_items_focus_blocks_clear_tomorrow_light` tests V2 generic-daily-briefing class at **5x→6x** triangulation (C3 morning + C4 evening + C5 friday-weekly-recap + C6 monday-week-lookahead + C7 wednesday-midweek-checkpoint + C8 thursday-pre-weekend-wrap; distinct on cadence + target horizon). **D-C8.attempt1.C boilerplate-paraphrase discipline applied:** middle sentence rewritten without "no priority items are flagged from your project list, sprint board, or stakeholder asks" template — instead "Nothing on the personal-task list or the stakeholder backlog requires a response before next Monday's standup."

**V2 NO class skipped at C8:** feature-announcement V2 NO stays at 4x (C2 chrome-ext + C3 notion + C5 vscode + C7 postman) — already ≥4x post-C7; no additional lift needed at C8 path-(a) saturating coverage.

**Coverage summary at C8:** Maximal compliant-content lift on the asymmetrically-weakest V2 YES + V2 NO cells under PATH (a) discipline: weather-alert V2 YES 4x→5x (path-(a) primary lift #1) + social-channel-invite V2 NO 3x→4x (path-(a) primary distractor lift); ADDITIONAL saturating lifts: schedule-change + production/on-call + message/delivery V2 YES 5x→6x + financial/deadline V2 YES 6x→7x + 3 V2 NO classes 5x→6x. Cross-trace coverage state through C8: **V4 NEW YES**: 4 total instances (UNCHANGED; scarcity-bounded 2x at C1+C6 + family-milestone 2x at C2+C5; symmetric closure preserved); **V4 NEW NO**: 6 total instances (UNCHANGED; 3 subclauses × 2x each at C1+C2; saturated state preserved); **V2 EXISTING YES classes**: urgent-safety 6x (C1+C2+C4+C5+C6+C7), schedule-change 6x (C1+C3+C4+C5+C7+C8), financial/deadline 7x (C1+C2+C3+C5+C6+C7+C8), production/on-call 6x (C2+C3+C4+C5+C7+C8), message/delivery 6x (C1+C3+C4+C6+C7+C8), weather-alert 5x (C2+C3+C4+C6+C8 — **NEWLY CLOSED at C8**); **V2 EXISTING NO classes**: routine-status 6x (C3+C4+C5+C6+C7+C8), marketing/newsletter 6x (C3+C4+C5+C6+C7+C8), generic-daily-briefing 6x (C3+C4+C5+C6+C7+C8), feature-announcement 4x UNCHANGED (C2+C3+C5+C7), social-channel-invite 4x (C1+C4+C6+C8 — **NEWLY CLOSED at C8**). **Net post-C8 reviewer-defensible endpoint claim: V2 YES 6 of 6 classes at ≥5x AND V2 NO 5 of 5 classes at ≥4x + V4 NEW YES symmetric closure preserved at 2x each subclause + V4 NEW NO saturated state preserved at 2x each of 3 subclauses — STRONGEST achievable single-trace compliant-content endpoint per D-C8.attempt1.B PATH (a) lock; matches kickoff's anticipated path-(a) endpoint exactly.** 2 traces remain for combined-N=20 closure; C9 + C10 freed to pursue (1) V4 NEW YES 3rd-repeat under deliberate cross-V4-mechanism asymmetry lift framing (now defensible after path-(a) compliant-content saturation complete at C8), (2) V4 NEW NO 3rd-repeat only if H4 denominator-growth argument is paired with mechanism-evidence asymmetry argument, or (3) higher-order GT-shape changes only if H4 evidence-base saturation warrants — defended at each subsequent C-Plan.

**Per-attempt artifact (accepting):** `runs/data/21c-author-test_v28-attempt-1-accepted.json` (SHA256 `46fd761e373c3ae31d8a0e1e21acf68a46fce70658f24f89b0923481498b7294`; 43896 bytes; D-C1.2 schema with step_3_5_pre_flight first-run-PASS log + V4-mechanism-zero defense + V2 EXISTING YES/NO compliant-content coverage with explicit path-(a) primary lift weather-alert 4x→5x + path-(a) primary distractor social-channel-invite 3x→4x + 4 saturating V2 YES lifts + 3 saturating V2 NO lifts + D-C8.attempt1.C boilerplate-paraphrase author-discipline applied at D3 + D4 + full audit-gate evidence + self-restate response verbatim + authored-trace verbatim + GT-regime classification + defensibility self-check + fresh-session-restart metadata).

### Banned-list state delta at C8

- Pre-C8 (C7 end-state, ships at C8): 190 IDs / 107 themes / 106 tuples.
- C8 contributions from accepted test_v28 (to be incorporated into `21c-banned-list-pre-c9.txt` at C9 land time per D-C1.1):
  - **+9 IDs:** `noaa_ice_storm_warning_freezing_rain_quarter_inch_glaze_36hr_outage_no_travel`, `mortgage_closing_rescheduled_friday_10am_underwriter_final_conditions_funding_delay`, `elasticsearch_index_status_red_primary_shard_unassigned_p1_search_outage_50min`, `older_sister_executor_father_estate_safe_deposit_box_appraiser_tomorrow_9am_callback`, `heloc_draw_period_expires_friday_5pm_conversion_amortization_terms_lock_decision_lender_email`, `terraform_state_drift_weekly_scan_zero_resources_modified_clean_all_workspaces`, `bluesky_starter_pack_invite_curator_recommended_follow_data_journalism_circle`, `meridian_games_summer_catalog_strategy_titles_2026_no_action_required`, `thursday_pre_weekend_wrap_briefing_no_overdue_items_focus_blocks_clear_tomorrow_light`.
  - **+5 themes (GT-regime regime column verbatim):** weather alert (V2 EXISTING YES) — NWS ice-storm warning upgrade from freezing-rain advisory with 1/4-3/4 inch glaze accretion + 36-hour suburban-distribution-feeder outage projection + no-unnecessary-travel advisory + glazed-sidewalk fall-injury triple in past comparable storm; schedule change affecting the user personally (V2 EXISTING YES) — mortgage-underwriting team rescheduling Westwood property closing from today 3pm to Friday 10am at title-company office with rate-lock-grace-period deadline + certified-funds cashier's-check + homeowners-policy declaration page required; production/on-call alert (V2 EXISTING YES) — PagerDuty SEV-one on customer-facing Elasticsearch search-platform cluster prod-search-es-east-01 with index status RED + 2 primary catalog-search shards unassigned + storefront API 5xx past 40% + downstream recommendation cold-cache fallback + disk-high-watermark trigger on 3 hot-tier nodes; message or delivery directed personally to the user (V2 EXISTING YES) — older sister Tess (named executor of late father's estate) voicemail with probate-court-ordered safe-deposit-box appraiser appointment tomorrow 9am requiring both surviving siblings present + callback-tonight-or-reschedule-next-week + 1-month estate-distribution delay; financial/deadline obligation (V2 EXISTING YES) — HELOC lender notice with draw-period expiry Friday 5pm + automatic 15-year amortization conversion at prime+1.5 vs alternative 15-year fixed-rate term-lock at 6.85% election decision + unused draw cap reverts at conversion + fresh application + appraisal required for reinstatement.
  - **+5 tuples (GT keyword tuples verbatim):** `(ice, glaze)`, `(mortgage, closing)`, `(elasticsearch, shard)`, `(executor, appraiser)`, `(heloc, draw)`.
- Post-C8 (input state for C9): 199 IDs / 112 themes / 111 tuples. File ships at C9 land time as `runs/data/21c-banned-list-pre-c9.{txt,json}` per D-C1.1 invariant.

### Halt-condition status at C8

- Literal-ID collision halt (D-C1.5 #1): **not triggered** (audit step 4 PASS at the accepting attempt).
- Banned-list-saturation halt (D-C1.5 #2 = §D9 defense #4, >25 attempts AND <10 accepted): **not triggered** (10 cumulative milestone attempts < 25; 8 accepted traces toward target of 10).
- Retry-cap-3 on test_v28 (D-C1.5 #3): **not exhausted** (1/3 used; PASS at attempt #1 / 2 retries remaining had attempt #1 not accepted).

### Cumulative milestone-spend through Commit C8

Commit C8 spend: $0 at attempt #1 (in-session author + local Python audit-gate; self-restate gate rendered locally; no API spend). Cumulative M11a-extension spend through Commit C8: $0.7081 (unchanged from Commit C7; ~18% of $4 pre-reg budget).

### Frozen artifacts at Commit C8 (NOT touched, per locked plan §D13 + D-C1.6 carry-forward)

- `agent/loop.py`, `agent/llm.py`, `agent/predictor.py`, `agent/surprise.py`, `agent/arbiter.py` — frozen throughout milestone.
- `eval/run_trace.py`, `eval/author_trace.py` — frozen at Commit C (CLI choices + self-restate gate locked at Commit B).
- `sandbox/event_trace.py` test_v4..test_v15 + test_v21..test_v27 definitions — frozen historical artifacts (only NEW `test_trace_v28` added at C8, plus the registry line `"test_v28": test_trace_v28,`; verified APPEND-ONLY 62-line diff via `git diff --stat sandbox/event_trace.py` = 1 file changed, 62 insertions, 0 deletions).
- `runs/data/21c-banned-list-pre-c{1,2,3,4,5,6,7}.{txt,json}` + `runs/data/21c-author-test_v{21,22,23,24,25,26,27}-*.json` — frozen at C1+C2+C3+C4+C5+C6+C7; do NOT mutate.
- `baselines/`, `pyproject.toml`, `uv.lock` — no changes at Commit C8.

### Next: Commit C9 — fresh-session trace authoring `test_v29`

Per locked plan §D13 + D-C1.1: future session opens with `runs/data/21c-banned-list-pre-c9.{txt,json}` (NEW; reflects test_v21..v28 contributions; 199 IDs / 112 themes / 111 tuples) as the pre-C9 starting state. Self-restate gate rendered against the pre-C9 file. Same C-protocol governance decisions (D-C1.1..D-C1.6) apply unchanged. Cumulative milestone attempt count 10/25 carries forward. Step 3.5 pre-flight keyword literal-substring verification (D-C2.attempt2.C / D-C3.attempt1.C / D-C4.attempt1.C / D-C5.attempt1.C / D-C6.attempt1.C / D-C7.attempt1.C / D-C8.attempt1.C) carries forward as standing per-attempt author discipline. D-C8.attempt1.C boilerplate-paraphrase author-discipline (added at C8 per C7-attempt-1-step-6 rejection precedent) also carries forward as standing per-attempt author discipline (pre-flight to audit step 6). With C8 closing V2 YES ≥5x for ALL 6 V2 YES classes (path-(a) primary weather-alert 4x→5x) + V2 NO ≥4x for ALL 5 V2 NO classes (path-(a) primary social-channel-invite 3x→4x) + 4 saturating V2 YES lifts + 3 saturating V2 NO lifts, C9 may pursue (1) 3rd-repeat V4 NEW YES (now defensible after path-(a) compliant-content saturation complete; framing as deliberate cross-V4-mechanism asymmetry lift rather than within-subclause-asymmetry re-opening), (2) 3rd-repeat V4 NEW NO if H4 denominator-growth argument is paired with mechanism-evidence asymmetry argument, (3) within-V2-class 5-GT triangulation (path-(d) — reviewer-flag risk; defensible only if specific mechanism evidence warrants), or (4) higher-order GT-shape changes (e.g., 6+ event count, sub-90s tight-window, alternative kind-mix) only if H4 evidence-base saturation warrants — defended at the C9 Plan.

Commit C9 is deferred to a future fresh session per M10-shape protocol + auto-memory `feedback_new_session_for_arch_work.md`.
