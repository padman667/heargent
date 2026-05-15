# Run 21 — M11a-extension: V4 prompt revision + N=20 expansion

**Pre-reg date:** 2026-05-15 (M11a-extension Commit A landing).
**Pre-reg SHA:** `{filled at this commit by post-commit doc-completeness backfill}`
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
