# Run 19 — Iterative Within-Protocol Banned-List Extension (M11a)

**Date:** 2026-05-08 (pre-registration). Results sections (Commit C1-C5 audit logs + per-session attestations + per-attempt drift log; Commit D 20-cell harness eval + paper-line per outcome row at each N-scope) appended post-eval.
**Milestone:** M11a — drift-resistant external-authoring protocol revision. Five fresh externally-authored traces (test_v11 through test_v15) under the **iteratively-extended-banned-list** protocol — banned IDs / themes / keyword tuples extended after each accepted trace before the next fresh session opens, applying M8b/M10's between-milestone extension model within-milestone. Zero new architectural levers; zero code changes (sandbox + harness + arbiters all unchanged from M10 close `6f86c8d`). The protocol revision targets M10b's defense-#7 systematic-drift activation (halt at 3/5 traces, commit `24fe688`); root cause was M10b's frozen single-list-per-N-traces design producing cross-trace overlap drift as accepted traces accumulated. M11a tests whether iterative extension structurally precludes the literal-ID and strong-overlap drift modes M10b empirically surfaced. Pre-data hardening: 13 edits made to the source plan before Commit A (mirrors M9 `e66afc1` / M10 `1615c45` / M10b pre-Commit-A pattern); all hardening edits are stricter, clarifying, or honest-weakening — none relax the pre-registered drift-revision criteria or the P1/P2 buckets.
**Pre-registration SHA:** Commit A landed at SHA `a49895d` (this file's first commit; backfilled into the file body at the immediately-following SHA-backfill commit per no-amend discipline). Plan source: `~/.claude/plans/m11a-iterative-banned-list-extension.md`. The 13 pre-data hardening edits are documented in this plan and were landed in the source before any cell ran. None change the 0.80 hit threshold, the P1/P2 N-scope buckets, the drift-revision success/partial/failure criteria, or the halt trigger; all are stricter, clarifying, or honest-weakening — audit-table-verified zero goalpost-moving risk.
**Predecessors:** M10b halt SHA `24fe688` (defense-#7 systematic-drift activation at 3/5 traces; frozen-banned-list design produces empirically-detectable cross-trace overlap drift); M10b D-on-N=3 SHA `985f441` (12-cell harness on test_v6/v7/v8 + drift smoke PASS + Row-4a "partial-closure with residuals" pattern; combined N=5 V2-3B failure rate 60% / V2-Opus failure rate 20% with wide binomial CIs); M10 close SHA `6f86c8d` (positive close at row 1, H2 confirmed at n=1 external trace); M8b results SHA `ad70d67` (test_v4 falsification at V2-3B).
**Environment:** Carry-forward from M10b (runs/18). ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3` (predictor + surprise scorer + V2-3B baseline cell). Claude API: `anthropic` SDK, `ANTHROPIC_API_KEY` env var, `claude-opus-4-7` alias (M11a arbiter + authoring; per-call dispatch ID echoed `claude-opus-4-7` at M10b close 2026-05-07, re-verified at M11a authoring/eval). Anthropic rates: Opus 4.7 = $15 / M input tokens, $75 / M output tokens (M10b pre-reg lock; no rate change observed in the 1-day gap M10b → M11a).

## Context

M10b (`runs/18-n-trace-external.md`, halt commit `24fe688`, D-on-N=3 commit `985f441`) halted at 3 of 5 traces under defense-#7 systematic-drift activation:
- 6 fresh-session attempts produced 9+ thematic + 2 literal-ID cross-trace overlaps with monotonically-worsening severity
- 2 of 6 attempts (33%) hit literal-ID collisions with already-committed M10b traces (test_v7 attempt #1 `wedding_rsvp` ↔ test_v6; test_v9 attempt #2 `mortgage_rate_lock` ↔ test_v7)
- Halt was pre-registered behavior under defense #7, not a protocol failure
- D-on-N=3 supplementary harness on test_v6/v7/v8 yielded the qualitative Row-4a "partial-closure with residuals" pattern (V2-Opus closes 1 of 2 V2-3B failures; V2-Opus introduces 0 new failures); aggregate combined N=5 (M10's test_v4/v5 + M10b's test_v6/v7/v8): V2-3B failure rate 60%, V2-Opus failure rate 20%, both with wide binomial CIs

**Root cause of M10b's drift**: the banned lists were locked at M10b Commit A and not iteratively extended within-M10b. Each successive fresh session saw the same M10b-frozen list (55 IDs / 32 themes / 31 keyword tuples), so as accepted traces accumulated, fresh sessions independently reached for thematically-adjacent or literal-collision content because the "novel content" space available to them shrank without the banned list reflecting that shrinkage.

**M8b/M10 used between-milestone iterative extension** (each milestone's banned list was extended with the prior milestone's contributions). M10b deliberately froze this within-milestone for a single-list-per-N-traces design. The empirical M10b finding is that the freeze fails at N=5; the natural fix is to apply the M8b/M10 between-milestone extension model **within-milestone** — extending the banned list after each accepted M11a trace before the next fresh session opens.

M11a is the protocol revision implementing this fix. It is not an architectural lever change — it's a protocol-design change. Same arbiters, same harness, same model (Opus 4.7), same cell matrix per trace.

## Thesis

> Iterative within-protocol banned-list extension reduces the systematic content drift observed in M10b across 5 fresh-session-authored traces, enabling a credible N=5 (or N=8 / N=10 combined) external-authoring evaluation of V2-3B vs V2-Opus coverage variance with tightened binomial CIs.

The thesis is testable in three branches per the pre-registered analysis below. Each branch is publishable; the experiment is not designed to find a particular outcome.

## Frozen design choices (locked at this commit)

### Trace count: 5 new externally-authored traces (test_v11 through test_v15)

Skip `test_v9` and `test_v10` — both are M10b halt artifacts (test_v9 had 2 rejected attempts logged in M10b's Rejections log; test_v10 was never attempted). Starting at `test_v11` makes M11a's traces visually distinct from M10b's halted-attempt namespace and avoids any reader confusion about whether `test_v9` / `test_v10` exist as authored content.

Hard cap N=5; no extension after eval. Pre-registered before any cell runs. Same N target as M10b's pre-reg, so M11a's success/failure on hitting N=5 directly tests whether the protocol revision works at the originally-targeted scope.

### Cell matrix per trace: 4 cells × 5 traces = 20 cells

| cell | agent | arbiter | per-cell cost |
|---|---|---|---|
| V2-3B content | HeargentZAWide | ContentArbiter (V2 prompt, qwen2.5:3b-instruct) | $0 (local) |
| V2-Opus content | HeargentZAWide | ClaudeArbiter (V2 prompt, claude-opus-4-7) | ~$0.05 |
| poll-Opus | react_poll_claude | (Opus poll on every tick) | ~$1 |
| cron30s | CronKeyword30s | — | $0 |

**Skipped on purpose** (carry-forward from M10b's rationale; unchanged):
- V3-Opus: M10's test_v4 attribution + test_v5 cells already established that V3-Opus tracks V2-Opus event-for-event at Opus scale
- Random ablation: M7's N=20 seed-variance + M10's test_v5 random cell already characterize random's behavior
- V2-3B vs V2-Opus on co-developed traces: not the M11a question; pinned by M10 Commit B regression and re-verified at M10b D drift smoke

### Authoring protocol per trace (carry-forward from M10b with iterative-extension addition)

Carry-forward (unchanged from M10b §"Authoring protocol per trace"):
- **Model**: Opus 4.7 (`claude-opus-4-7` alias) for the authoring session; substitution recorded if alias rotated
- **Discipline**: 1 fresh Claude Code session per trace; no batched-with-/clear
- **Cwd / context isolation**: non-project cwd; no project CLAUDE.md, no auto-memory; `/clear` at session start
- **Per-session attestation**: timestamp + cwd + dispatched response.model + /clear confirmation per trace
- Single-shot output; one mechanical name substitution; audit against 11 hard structural constraints + 3 banned lists; reject + log + retry on violation; retry-cap 3 per trace **for non-literal-ID rejection reasons only** (structural-constraint violations, banned-theme/tuple violations, trace-fairness concerns). **A literal-ID collision triggers the §Drift-monitoring §Halt trigger and does not consume retry budget — it halts M11a as a drift-revision-failure finding** (see §Drift-monitoring criterion); retry-cap-3 does not override the halt rule

**M11a-specific additions:**

- **The fresh session's authoring prompt is regenerated for each trace**, embedding the **current banned-list state** at the moment of authoring. This is the protocol revision's central mechanism. Per-trace banned-list snapshots are logged in runs/19 §"Banned-list timeline" so the prompt for each accepted trace is exactly reproducible.
- **Iterative extension rule (locked at this commit)**: after each accepted trace commits (C1 → C5), before the next fresh session opens, the banned lists are extended with the just-accepted trace's contributions:
  - **Banned IDs**: append all event IDs from the accepted trace (5 GT IDs + 4 distractor IDs = 9 IDs per accepted trace)
  - **Banned content themes**: append the GT-regime classifications from the accepted trace's audit step 4 (5 distinct regime tags per trace, one per GT, no collapsing; the classification text is reused verbatim from the runs/19 §"GT-regime classification" regime column as the banned theme — mirrors the M10b → M11a extension precedent in §"Banned lists for M11a")
  - **Banned keyword tuples**: append all GT keyword tuples from the accepted trace (5 per trace)
- **Per-trace audit responsibility expands**: the working session's audit must additionally verify no literal-ID collision with all prior accepted M11a traces (and with M10b's accepted traces test_v6/v7/v8). This is mechanical — grep the new trace's IDs against the full accumulated banned ID list.

### Banned lists for M11a (starting state at Commit A)

Starting state inherits **M10b end-state** (M10b-frozen list + M10b's accepted-trace contributions):

**Banned event IDs (82 = 55 from M10b-pre-reg + 27 from M10b's accepted test_v6/v7/v8):**

```
[M10b's frozen 55 IDs verbatim — see runs/18 §"Banned lists for M10b"]
+ test_v6's 9: vet_emergency, concert_swap, elevator_outage, auction_ending, wedding_rsvp,
                reddit_digest, steam_sale, bank_statement, twitter_followers
+ test_v7's 9: sister_pickup, mortgage_rate_lock, jury_duty, airbnb_cancelled, wedding_rehearsal,
                poll_civic_reminder, recipe_app_tip, loyalty_points_summary, podcast_episode_drop
+ test_v8's 9: vet_luna_tomorrow, earthquake_local, mom_birthday_heads_up,
                bridgers_presale_window, photographer_voicemail_jen, soundcloud_app_update,
                stitches_loyalty_statement, strava_new_follower, reading_streak_47
```

**Banned content themes (47 = 32 from M10b + 15 from test_v6/v7/v8 GT-regime classifications, locked at Commit A; mechanical extraction from runs/18 §"GT-regime classification" tables, one tag per GT, no collapsing; theme strings reproduced verbatim from runs/18's regime-column text):**

```
[M10b's frozen 32 themes verbatim]
+ test_v6 (5 themes; verbatim from runs/18):
  - pet medical emergency + callback request, 10-min auth window
  - friend social ticket-swap with hard 5pm deadline
  - building elevator emergency-cable-repair service disruption
  - online auction ending in 10 min, top bidder, financial decision
  - wedding RSVP deadline tonight at midnight + meal selection
+ test_v7 (5 themes; verbatim from runs/18):
  - family voicemail with airport pickup, 15-min window
  - financial deadline 17:00 today (mortgage rate lock)
  - civic obligation; confirm/postpone by tomorrow noon
  - travel reservation cancellation for next weekend
  - family event rescheduled Sat 12:00 → Fri 18:00
+ test_v8 (5 themes; verbatim from runs/18):
  - personal voicemail with hard 6pm-tonight deadline
  - M4.2 earthquake alert with imminent shaking instruction
  - 10-min ticket presale window opening with access code
  - reminder for tomorrow's vet appointment + prep needed (records, stool sample)
  - proactive heads-up for mother's birthday tomorrow + history of forgetting
```

The 15 added theme strings are locked verbatim at Commit A; mechanical extraction from runs/18's regime-column text precludes post-hoc theme inflation or paraphrasing.

**Banned keyword tuples**: M10b's 31 + test_v6/v7/v8's 15 GT keyword tuples = **46 starting tuples**:

```
[M10b's frozen 31 tuples verbatim]
+ test_v6: (vet, surgery), (concert, swap), (elevator, "out of service"), (auction, ending), (wedding, rsvp)
+ test_v7: (sister, airport), (mortgage, "rate lock"), (jury, duty), (airbnb, cancelled), (wedding, rehearsal)
+ test_v8: (vet, luna), (earthquake, shaking), (mother, birthday), (presale, tickets), (photographer, engagement)
```

### Banned-list growth trajectory (predicted, locked at this commit)

If all 5 M11a traces accept on first attempt (each accepted trace adds 9 IDs + 5 themes + 5 keyword tuples):
- Commit A starting state: 82 IDs / 47 themes / 46 tuples
- Before C2 (test_v12 fresh session): 91 IDs / 52 themes / 51 tuples
- Before C3 (test_v13): 100 IDs / 57 themes / 56 tuples
- Before C4 (test_v14): 109 IDs / 62 themes / 61 tuples
- Before C5 (test_v15): 118 IDs / 67 themes / 66 tuples
- End of M11a: 127 IDs / 72 themes / 71 tuples

If any trace requires multiple attempts (per retry-cap-3), the trajectory is the same; only accepted traces extend the list. Rejected attempts don't contribute to extension (mirrors how M10b handled rejection logging — rejected generators don't extend the banned list since the trace isn't merged).

**Saturation risk**: at 127 banned IDs and 72 themes, the fresh session still has wide latitude for novel content (life events / scenarios are effectively open-ended). Saturation is unlikely to be the limiting factor at N=5; it would be at N=20+. M11a-extension scope (future) handles N=20+.

### Code changes

**Zero (same as M10b).** M11a reuses every component of M10/M10b unchanged:
- `agent/arbiter.py` ClaudeArbiter — unchanged
- `baselines/react_poll_claude.py` — unchanged
- `eval/run_trace.py` CLI — unchanged
- All baselines, predictor, surprise scorer, sandbox/world.py — unchanged
- `sandbox/event_trace.py` — only appends `test_trace_v11` … `test_trace_v15` and registry entries; no edits to existing trace functions

The protocol revision is in the **authoring prompt generation + audit step**, both of which live in the working-session human-in-the-loop pipeline, not in the harness code.

## Five-commit protocol (carry-forward from M10b structure)

| Commit | Content | Gates |
|---|---|---|
| **A** | This pre-reg → `runs/19-iterative-banned-list-extension.md` (frozen design choices + iterative-extension rule + starting banned lists from M10b end-state + cell matrix + decision rules + paper-line per outcome). No code. | — |
| **C1-C5** | Five externally-authored traces (one commit per trace). Each via fresh session with the **current banned-list state** embedded in its prompt. After each accept, the banned list is extended with that trace's contributions before the next fresh session opens. | Audit gate per trace: 11 structural constraints + cumulative banned lists + cross-trace literal-ID check. Reject + log + retry on non-literal-ID violations (retry-cap 3 per trace); **literal-ID collisions trigger the §Drift-monitoring §Halt trigger and halt M11a as a drift-revision-failure finding** (no retry). |
| **D** | 20-cell harness matrix run after all 5 traces lands; results table + per-trace verdict + aggregate analysis (M11a alone N=5; combined M10+M10b+M11a N=10) appended to runs/19. | Verbatim evaluation against frozen P1 / P2 rules. |

(Note the absence of a "Commit B": M11a adds no code, mirroring M10b. The Commit B equivalent is implicit in M10's `f28689e` — that's the code state M11a runs on.)

## Pre-registered analysis (carry-forward from M10b with three N-scopes — 5 / 8 / 10)

### Per-trace observations table (filled at Commit D)

| trace | V2-3B hit | V2-3B false/h | V2-Opus hit | V2-Opus false/h | poll-Opus hit | cron30s hit | GT-regime in V2's YES enumeration? (independent inspection) | V2-Opus closes V2-3B failures? |
|---|---|---|---|---|---|---|---|---|

Each row is one of test_v11 … test_v15. The "GT-regime in V2's YES enumeration?" column is filled per trace at audit step 4 (mirrors M10b verbatim — independent classification before any harness cell on that trace runs).

### Aggregate metrics (filled at Commit D; three scopes)

**Scope 1 — M11a alone (N=5):**
- V2-3B failure rate: # of fair-trace-subset traces with `hit_rate(V2-3B) < 0.80`
- V2-Opus failure rate: # of fair-trace-subset traces with `hit_rate(V2-Opus) < 0.80` OR `false_initiation_rate_per_hour(V2-Opus) > 5.0`
- 95% Clopper-Pearson binomial CIs on each rate
- Δfailure-rate (V2-3B − V2-Opus) at point estimate
- V2-Opus closes V2-3B failures: count

**Scope 2 — M10b + M11a combined (N=8):**
- Same metrics; sample = test_v6/v7/v8 + test_v11/v12/v13/v14/v15 (fair-trace subsets within each milestone)
- Bridges the M10b-finding milestone with M11a's revised-protocol milestone; tighter CIs than either alone

**Scope 3 — M10 + M10b + M11a combined (N=10):**
- Same metrics; sample = test_v4 + test_v5 + test_v6/v7/v8 + test_v11/v12/v13/v14/v15
- Strongest external-coverage estimate; **primary scope for the H2-coverage-rate question per §Pre-registered decision rules §Headline-scope commitment**. Computed on N_fair_10 (the fair-trace subset within scope 3); P3 fairness is per-scope, not a precondition for using N=10 as primary
- Cross-protocol caveat documented (M10 used M9-frozen banned list; M10b used M10b-frozen banned list; M11a uses iteratively-extended banned list); see defense #5

### Pre-registered decision rules (frozen; carry-forward from M10b verbatim with N-scope expansion)

**P-numbering** (carry-forward from M10b unchanged):
- P1: V2-3B failure-rate buckets
- P2: V2-Opus failure rate (joint hit + false/h bar)
- P3: poll-Opus trace-fairness sanity (evaluated FIRST; gates the fair-trace subset for P1/P2)

**Headline-scope commitment (pre-registered at Commit A; closes scope-shopping):**

M11a addresses two distinct empirical questions; each has a pre-registered primary scope:

1. **"Did the iterative-extension protocol revision work?"** → Primary scope = **M11a-alone N=5**. This is a single-protocol, clean-causal-inference question. Combined N=8 / N=10 scopes do not bear on the protocol-revision question because they mix protocols.
2. **"What is the H2 (V2-3B vs V2-Opus) external-coverage rate?"** → Primary scope = **combined N=10** (M10's test_v4/v5 + M10b's test_v6/v7/v8 + M11a's test_v11–v15). This is the broadest external-authoring sample available; the cross-protocol caveat is documented (defense #5) but the point estimate at N=10 is the strongest single estimate. M11a-alone N=5 is reported as sensitivity; combined N=8 (M10b + M11a) is reported as intermediate sensitivity.

The headline scope per question is locked at Commit A; no post-hoc reassignment is permitted.

**P3 — Trace-fairness sanity (evaluated FIRST; per-scope fair-trace subset).** Carry-forward from M10b §"P3" with explicit per-scope handling:
- Fair-trace subset = traces with poll-Opus hit ≥ 0.80, computed *within each N-scope*.
- **N_fair_5 = |{trace ∈ test_v11..test_v15 : poll-Opus hit ≥ 0.80}|** (M11a-alone scope)
- **N_fair_8 = |{trace ∈ test_v6..test_v8 ∪ test_v11..test_v15 : poll-Opus hit ≥ 0.80}|** (M10b + M11a combined scope)
- **N_fair_10 = |{trace ∈ test_v4, test_v5 ∪ test_v6..test_v8 ∪ test_v11..test_v15 : poll-Opus hit ≥ 0.80}|** (M10 + M10b + M11a combined scope)
- All P1/P2 metrics computed on the fair-trace subset within each scope.
- Sensitivity analysis reports both included-all and fair-subset-only variants at each N-scope; headline P1/P2 verdicts are read off the fair-subset numbers at the scope's primary question.

**P1 buckets at N=5 (M11a alone; primary scope for protocol-revision question)** — identical to M10b's pre-reg buckets verbatim:
- ≥ 40% (≥ 2 of N_fair_5 with V2-3B hit < 0.80): H2 confirmed at point estimate
- = 20% (1 of N_fair_5): H2 modestly confirmed at point estimate
- = 0% (0 of N_fair_5): H2 weakly confirmed; reframe Opus as insurance

**P1 buckets at N=8 (M10b + M11a combined; intermediate sensitivity scope)** — pre-registered here at Commit A:
- ≥ 38% (≥ 3 of N_fair_8 with V2-3B hit < 0.80): H2 confirmed
- = 13-25% (1-2 of N_fair_8): H2 modestly confirmed
- = 0% (0 of N_fair_8): H2 weakened; reframe Opus as insurance
- (Integer-count thresholds: ≥3/8 = 37.5%; 2/8 = 25%; 1/8 = 12.5%; 0/8 = 0%; the percentage labels round to the nearest cell.)

**P1 buckets at N=10 (M10 + M10b + M11a combined; primary scope for H2-coverage-rate question)** — pre-registered here at Commit A:
- ≥ 40% (≥ 4 of N_fair_10 with V2-3B hit < 0.80): H2 confirmed under the strongest available external sample
- = 20-30% (2-3 of N_fair_10): H2 modestly confirmed
- = 0-10% (0-1 of N_fair_10): H2 weakened; M10's positive close softens significantly
- (Integer-count quantization at N=10 forces the lowest bucket to lump 0/10 and 1/10; documented here as a known consequence of the integer-count constraint.)

**P2 — V2-Opus failure rate (joint bar; identical at every N-scope)** — identical to M10b verbatim:
> V2-Opus failure = `hit < 0.80 OR false/h > 5.0/h`. The +5/h ceiling is the YES-bias check.

P2 thresholds at each N-scope are computed via the same integer-count mapping as P1 (M11a-alone N=5: 0/N_fair_5 expected; combined N=8: ≤1/N_fair_8 expected; combined N=10: ≤1/N_fair_10 expected). Any V2-Opus joint-bar failure triggers the Row-4a/4b mechanism diagnosis at the relevant scope.

### Outcome interpretation lookup table (5 rows; locked paper-line text at Commit A)

Five rows; structure carry-forward from M10b. Each row's paper-line text is **locked verbatim at Commit A** and reported at both primary scopes (M11a-alone N=5 for the protocol-revision question; combined N=10 for the H2-coverage-rate question). Integer placeholders `{X}`, `{Y}`, `{N_fair}`, `{L%}`, `{H%}` are filled at Commit D from observed counts and 95% Clopper-Pearson binomial CIs; **wording is not edited at Commit D**. Combined N=8 sensitivity is reported with the same row identification, no separate paper-line text.

| V2-3B failure rate (at primary scope) | V2-Opus failure count | Row | Headline |
|---|---|---|---|
| ≥ 40% (≥ 2/N_fair_5 or ≥ 4/N_fair_10) | 0 | **Row 1** | H2 confirmed at point estimate; model-scale uniformly load-bearing on M8b out-of-V2-enum failures in this sample |
| = 20% (1/N_fair_5) or = 20-30% (2-3/N_fair_10) | 0 | **Row 2** | H2 modestly confirmed at point estimate |
| = 0% (0/N_fair_5) or = 0-10% (0-1/N_fair_10) | 0 | **Row 3** | H2 weakened to rare-failure-rescue; M8b/test_v4 was atypical |
| any | > 0 AND ≤ V2-3B failure count | **Row 4a** | Partial-closure with residuals; model-scale upgrade is load-bearing-but-not-sufficient |
| any | > V2-3B failure count | **Row 4b** | Model-scale upgrade insufficient or harmful; H2 falsified in this direction |

**Locked paper-line text per row (filled with observed counts at Commit D):**

**Row 1 — H2 confirmed (M11a-alone N=5 primary):**
> *"Across N={N_fair_5} fresh externally-authored traces under the M11a iteratively-extended-banned-list protocol (fair-trace subset; see Methods), V2-3B coverage failed (hit < 0.80) on {X}/{N_fair_5} (point estimate; 95% binomial CI [{L%}, {H%}], wide due to small N). V2-Opus closed every failure (joint bar: hit ≥ 0.80 AND false/h ≤ 5.0/h on {X}/{X} of those traces). Combined with M10's test_v4 and M10b's test_v6/v7/v8, the H2 (model-scale) claim rests on N={N_fair_10} externally-authored traces under three protocol generations; M11a's iteratively-extended protocol is the most drift-resistant. The M8b/test_v4 failure mode is replicable in M11a; tighter rate estimates require N=20+ future work (M11a-extension scope)."*

**Row 1 — H2 confirmed (combined N=10 primary):**
> *"Across N={N_fair_10} fresh externally-authored traces under three protocol generations (M10 frozen list; M10b frozen list; M11a iteratively-extended list), V2-3B coverage failed (hit < 0.80) on {X}/{N_fair_10} (point estimate; 95% binomial CI [{L%}, {H%}]). V2-Opus closed every failure (joint bar: hit ≥ 0.80 AND false/h ≤ 5.0/h on {X}/{X} of those traces) at $0.0073-$0.0150/hit, 13-33× cheaper per hit than poll-Opus across the matched-arbiter cost denominator. The H2 (model-scale closes M8b coverage gap) claim is confirmed at point estimate under the strongest available external sample; cross-protocol heterogeneity is documented (see defense #5) but the qualitative finding is consistent across protocol generations."*

**Row 2 — H2 modestly confirmed (M11a-alone N=5 primary):**
> *"Across N={N_fair_5} fresh externally-authored traces under the M11a iteratively-extended-banned-list protocol, V2-3B coverage failed on 1/{N_fair_5} (point estimate; 95% binomial CI [{L%}, {H%}]). V2-Opus closed it (joint bar pass on 1/1). Aggregated with M10 + M10b's prior 5 external traces, the V2-3B failure rate sits at {X}/{N_fair_10} ≈ {Y%} (combined N=10 estimate; 95% CI [{L%}, {H%}]). H2 is modestly confirmed at point estimate; V2-Opus is load-bearing when out-of-enumeration content surfaces, but in-enumeration draws are the more common case at the M11a protocol generation. CI is wide; M11a-extension scope tightens at N=20+."*

**Row 2 — H2 modestly confirmed (combined N=10 primary):**
> *"Across N={N_fair_10} fresh externally-authored traces under three protocol generations, V2-3B coverage failed on {X}/{N_fair_10} ({Y%} point estimate; 95% binomial CI [{L%}, {H%}]). V2-Opus closed all V2-3B failures (joint bar pass on {X}/{X}). H2 is modestly confirmed under the strongest available external sample. The Pareto headline (V2-Opus 13-33× cheaper per hit than poll-Opus) holds across the full sample. CI is wide; M11a-extension scope tightens at N=20+."*

**Row 3 — H2 weakened to insurance (M11a-alone N=5 primary):**
> *"Across N={N_fair_5} fresh externally-authored traces under the M11a iteratively-extended-banned-list protocol, V2-3B coverage held at hit ≥ 0.80 on every trace. Aggregated with M10 + M10b's prior 5 external traces, V2-3B failure rate is {X}/{N_fair_10} ≈ {Y%}. M8b/test_v4 (and any M10b residual failures) read as rare failure modes at the 3B scale rather than consistent properties of external authoring. V2-Opus serves as insurance against rare out-of-enumeration content rather than a uniform requirement; the in-distribution and Pareto headlines (M10) hold without modification, but H2 weakens to 'rare-failure-mode rescue' rather than 'consistent gap closure.' The methodological contribution is M11a's drift-resistant external-authoring protocol; the empirical finding is that the failure rate at 3B is lower than M10b's N=3 finding suggested. CI is wide; M11a-extension scope tightens at N=20+."*

**Row 3 — H2 weakened to insurance (combined N=10 primary):**
> *"Across N={N_fair_10} fresh externally-authored traces under three protocol generations, V2-3B failure rate is {X}/{N_fair_10} ({Y%} point estimate; 95% binomial CI [{L%}, {H%}]). The M8b/test_v4 + M10b residual failures read as rare failure modes rather than consistent properties of external authoring at this N. V2-Opus serves as insurance against rare out-of-enumeration content rather than a uniform requirement; M10's in-distribution + Pareto headlines hold; H2 weakens to 'rare-failure-mode rescue.' M10b's halt-as-finding methodology contribution stands; M11a's iterative-extension protocol is the drift-resistant continuation. CI is wide; M11a-extension scope tightens at N=20+."*

**Row 4a — Partial-closure with residuals (M11a-alone N=5 primary):**
> *"On {X}/{N_fair_5} M11a traces, V2-Opus failed the joint bar (hit < 0.80 OR false/h > 5.0/h) — extending M10b's test_v8 finding into the M11a sample. V2-Opus failure count ({X}) ≤ V2-3B failure count ({Y}); model-scale is load-bearing-but-not-sufficient. Per-failure mechanism: [tags from per-trace inspection]. Combined N=10 V2-Opus failure rate sits at {Z}/{N_fair_10} ({Y%}). The H2 claim updates from 'V2-Opus closes M8b's gap' to 'V2-Opus closes M8b's gap on most external-authored content but exhibits residual gaps on [classified failure modes].' Future work (M11+) addresses these via routing / V4 prompt expansion / model-family upgrade."*

**Row 4a — Partial-closure with residuals (combined N=10 primary):**
> *"Across N={N_fair_10} fresh externally-authored traces, V2-Opus failed the joint bar on {X}/{N_fair_10} traces. V2-Opus failure count ({X}) ≤ V2-3B failure count ({Y}); model-scale is load-bearing-but-not-sufficient under the strongest available external sample. Per-failure mechanism: [tags from per-trace inspection]. M10b's test_v8 partial-closure pattern replicates in the M11a sample; combined-N=10 V2-3B failure rate is {Y}/{N_fair_10} ({A%}) and V2-Opus failure rate is {X}/{N_fair_10} ({B%}), both with 95% CIs [{L%}, {H%}]. H2 is confirmed in direction (V2-Opus reduces failure rate) but not in absolute (residuals remain). Future work (M11+) addresses via routing / V4 prompt / model-family upgrade."*

**Row 4b — Model-scale insufficient or harmful (M11a-alone N=5 primary):**
> *"On {X}/{N_fair_5} M11a traces, V2-Opus failed the joint bar AND the V2-Opus failure count ({X}) > V2-3B failure count ({Y}) — V2-Opus introduces *more* joint-bar failures than V2-3B at the M11a protocol generation (e.g., V2-Opus permissive on borderline content driving false/h spikes, or V2-Opus over-NO on regimes V2-3B happened to pass). H2 falsified in this direction. Combined N=10 picture: V2-Opus failure rate {Z}/{N_fair_10} > V2-3B failure rate {W}/{N_fair_10}. M10's positive close is overturned by the M11a sample; the paper updates to report the falsification as the headline finding. Future work (M11+) re-elicits prompts across model scales or pursues a different lever entirely."*

**Row 4b — Model-scale insufficient or harmful (combined N=10 primary):**
> *"Across N={N_fair_10} fresh externally-authored traces under three protocol generations, V2-Opus failed the joint bar on {X}/{N_fair_10} traces AND V2-Opus failure count > V2-3B failure count. The model-scale lever is empirically insufficient or actively harmful at the M11a-protocol-revision sample. H2 is falsified in this direction; M10's positive close is overturned. Mechanism diagnosis: [tags from per-trace inspection of every V2-Opus failure]. The paper updates to report the falsification as the headline finding; M11a's iterative-extension protocol is reported as a methodology contribution but the substantive H2 claim does not survive the expanded sample. Future work pursues a different architectural lever."*

These row paper-lines are locked at Commit A; Commit D fills the integer placeholders and the row identification, no other text edits.

### Drift-monitoring criterion (M11a-specific addition)

A successful M11a outcome requires not just hitting N=5 traces but doing so **with reduced cross-trace overlap relative to M10b**. Drift-quantification metrics are pre-registered with a **mechanical severity grading rubric** (strong = bytewise objective; mild = judgment-only) so severity calls are not post-hoc.

**Severity grading rubric (locked at Commit A; mechanical for strong, judgment for mild):**

A cross-trace overlap is graded against all prior committed M11a traces + M10b's accepted test_v6/v7/v8. Three severity classes:

- **Literal-ID collision** (mechanical): the new trace contains an event ID (GT or distractor) that bytewise-matches an event ID in any prior committed trace. Pure string-equality check.
- **Strong overlap** (mechanical; either sub-criterion triggers): (a) the new trace contains a GT keyword tuple that bytewise-matches (order-independent, lowercased) a GT keyword tuple in any prior committed trace; OR (b) the new trace contains a GT whose content text contains **≥8 consecutive verbatim words** matching a prior committed GT's content text (lowercased, whitespace-normalized).
- **Mild overlap** (judgment-only): the new trace's GT shares a broad-domain tag (e.g., wedding, earthquake, vet, financial-deadline) with a prior committed trace's GT, but no strong sub-criterion fires. Judgment-only because broad-domain tagging is inherently classifier-dependent; mild calls are reported but **do not gate** any pre-reg threshold.

The mechanical classes (literal-ID + strong sub-criteria a and b) collectively cover every overlap mode that drove M10b rejections (test_v7 #1: literal-ID; test_v9 #1: identical keyword tuple + ≥8-word verbatim earthquake instruction; test_v9 #2: literal-ID). Banned-theme substring matches against GT content are *not* in the mechanical strong-overlap rubric — naturalistic GT prose almost never contains a banned-theme description as substring, so a sub-criterion of that form would be inert; theme-level overlap is handled by the existing audit-step-3 manual review against the cumulative banned-theme list (a separate gate on banned-theme reuse). Mild is the residual category for paper-transparency reporting.

**Drift-quantification metrics (computed from the per-attempt drift log):**

- **Literal-ID collision count**: count of M11a fresh-session attempts (accepted + rejected) hitting any literal-ID collision with prior committed traces. Denominator = total attempts (1 to 15 over the M11a run).
- **Strong-overlap count in accepted traces**: count of M11a *accepted* traces with any strong-overlap sub-criterion (a or b) firing. Denominator = accepted-trace count (1 to 5).
- **Mild-overlap rate in accepted traces** (report-only, does not gate): fraction of accepted M11a traces with at least one mild overlap.

**Pre-registered M11a success criteria for the protocol revision (tightened from initial draft; closes "tolerance for the failure mode the revision was designed to fix" attack):**

- **Drift-revision success**: 0 literal-ID collisions across all M11a attempts AND 0 strong overlaps in accepted traces. (Compare M10b: 2 literal-ID collisions in 6 attempts → 33%; multiple strong overlaps in rejected attempts; the iterative-extension protocol must structurally preclude both.)
- **Drift-revision partial success**: 0 literal-ID collisions across all attempts AND 1 strong overlap in accepted traces (i.e., the iterative-extension protocol prevents the worst-case mode but a strong-overlap sub-criterion still fires once at N=5).
- **Drift-revision failure**: ≥ 1 literal-ID collision under iterative extension (regardless of attempt outcome), OR ≥ 2 strong overlaps in accepted traces, OR M11a halts at N<5 under retry-cap exhaustion or under the halt trigger below. In any failure case, the iterative-extension protocol revision is empirically not sufficient; M11a-extension scope would investigate stricter measures — V4 prompt redesign with explicit out-of-banned-domain instruction; direct human curation of GT pool; etc.

**Halt trigger (pre-registered at Commit A; analogous to M10b defense #7 systematic-drift activation, but stronger because iterative extension structurally precludes the collision):**

- **First literal-ID collision under iterative extension = automatic drift-revision-failure halt.** The iterative-extension banned list is regenerated and embedded in the fresh session's prompt before each attempt; a fresh session producing a literal-ID collision *despite* the explicit banned list constitutes a fresh-session prompt-following failure that the protocol revision was specifically designed to prevent. Halting on the first occurrence is correct because (a) continuing to retry would spend retry budget on an empirically-broken protocol revision, and (b) M10b's halt-as-finding precedent established that protocol-design failures are themselves publishable findings; M11a's halt would be the parallel finding for the iterative-extension protocol generation.
- The halt trigger fires regardless of which attempt # produces the collision; the trigger is the collision itself, not retry-cap exhaustion.
- The halt-as-finding paper-line is **pre-registered at Commit A** (see below) and is the headline if the trigger fires.

**Halt-as-finding paper-line (locked at Commit A; fires only if halt trigger activates):**

> *"M11a halted at the first literal-ID collision under the iteratively-extended-banned-list protocol ({trace, attempt #}, collision with {prior committed trace}). The collision occurred despite the iterative-extension protocol explicitly banning the prior committed trace's IDs in the fresh session's prompt — a fresh-session prompt-following failure that the protocol revision was specifically designed to prevent. M11a's iterative-extension protocol is empirically not sufficient at N={traces-completed-before-halt}; the halt is itself the finding (parallel to M10b defense #7 systematic-drift activation but at a stricter trigger because the iterative extension structurally precludes the collision). M11a-extension scope investigates stricter measures: V4 authoring prompt with explicit out-of-banned-domain instruction; direct human curation of GT pool; cross-author session diversification."*

**Drift criteria status note** — these criteria *do* gate the pre-registered drift-revision verdict (success/partial/failure) and the halt trigger; they **do not** gate the P1/P2 verdicts on V2-3B vs V2-Opus coverage variance. The latter are evaluated on whichever traces are accepted before halt (per the M10b precedent of evaluating Commit D on the N=3 committed set despite halt-at-3-of-5).

## Cost framework (carry-forward from M10b verbatim)

Per-trace expected spend: ~$1.05 (V2-3B $0 + V2-Opus ~$0.05 + poll-Opus ~$1 + cron30s $0). 5 traces × $1.05 = ~$5-6 total. Pre-Commit-D drift smoke ~$0.13 marginal (3-trace V2-Opus bit-identical check vs M10's `17b-*` JSONs).

Total expected M11a spend: ~$5-6, identical to M10b's pre-reg budget (and consistent with M10b's actual spend of ~$0.86, which was much lower due to compact M10b-trace event counts; M11a may also under-spend if traces are similarly compact).

## Critical files

- `~/.claude/plans/m11a-iterative-banned-list-extension.md` — this plan; walkthrough at fresh-session kickoff before Commit A
- `runs/19-iterative-banned-list-extension.md` — Commit A pre-reg lands as a copy of this plan with appropriate header / date / pre-reg SHA
- `sandbox/event_trace.py` — appends `test_trace_v11` … `test_trace_v15` + registry entries. Existing trace functions and registry entries (test_v6/v7/v8 from M10b included) **not touched**.
- `runs/data/19*.json` — 20 cell results.
- `runs/README.md` — row 19 added; status block updated; paper framing updated to row 1/2/3/4a/4b of M11a's outcome at the dominant N-scope (N=10 combined preferred).
- `agent/`, `baselines/`, `eval/`, `pyproject.toml`, `uv.lock` — **not touched** at any M11a commit.

## Verification

### Pre-Commit-D bit-identical smoke (drift detector across M10b → M11a)

Carry-forward from M10b §"Pre-Commit-D bit-identical smoke" verbatim (3 co-developed traces vs `runs/data/17b-content-opus-v2-{dev_v2,test_v1,test_v2}.json`). Now also verifies model-stability across M10 close (2026-04-27) → M10b D run (2026-05-08) → M11a D run.

### Per-trace structural audit (carry-forward from M10b with iterative-extension addition)

Per trace authored:
1. Schema check via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_v{N}'); print(...)"`.
2. Keyword/content alignment audit (`all(kw.lower() in event.content.lower() for kw in keywords)` per GT, M8b's hard constraint).
3. Banned-ID, banned-keyword-tuple, banned-theme manual review against the **current cumulative banned lists** (starting state for C1; extended for C2-C5).
4. **NEW: Cross-trace literal-ID collision check** — explicit grep of new trace's IDs against all prior accepted M11a traces' IDs + M10b's test_v6/v7/v8 IDs. **Any literal-ID collision triggers the §Drift-monitoring §Halt trigger** (drift-revision-failure halt + halt-as-finding paper-line); the collision does not consume retry budget. M10b's test_v7 attempt #1 + test_v9 attempt #2 precedents are reclassified under M11a as halt triggers, not retries, because under iterative extension the prior IDs are explicitly banned in the fresh session's prompt — a collision is structurally precluded by the protocol revision and any occurrence is a fresh-session prompt-following failure.
5. **Independent GT-regime classification** for the per-trace observations table (carry-forward from M10b).
6. Reject + log + retry on any violation **other than literal-ID collision** (e.g., structural-constraint violations, banned-theme/tuple violations not at literal-ID level). No prompt edits. Retry cap: 3 audit attempts per trace for non-literal-ID rejection reasons; literal-ID rejections halt M11a per audit step 4.

### Drift-quantification log (M11a-specific addition)

For each fresh-session attempt (accepted + rejected), the working session logs in runs/19 §"Per-attempt drift log":
- Attempt number for the trace
- Per-overlap-severity counts (literal-ID, strong, mild) with specific trace+ID references
- Verdict (PASS / REJECT)

This log feeds the drift-revision-success/partial/failure criteria pre-registered above.

### Commit D harness execution

```sh
# Per trace: 4 cells (V2-3B, V2-Opus, poll-Opus, cron30s)
for trace in test_v11 test_v12 test_v13 test_v14 test_v15; do
  uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
    --trace $trace --arbiter-mode content \
    --out runs/data/19d-content-3b-v2-${trace}.json
  uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
    --trace $trace --arbiter-mode claude --arbiter-system-prompt v2 \
    --out runs/data/19d-content-opus-v2-${trace}.json
  uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
    --trace $trace --out runs/data/19d-poll-opus-${trace}.json
  uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s \
    --trace $trace --out runs/data/19d-cron30-${trace}.json
done
```

Aggregate: read 20 cell JSONs + M10b's 12 cells + M10's test_v4/v5 cells, compute per-N-scope metrics, populate observations tables, identify outcome row at the N=10 combined scope.

## Reviewer-vulnerable surfaces and pre-registered defenses

Carry-forward of M10b's 8 defenses (still applicable at M11a) plus new M11a-specific defenses.

### Carry-forward from M10b (still applicable; abbreviated; full text in runs/18)

1. "Five external traces is still small N" — pre-registered hard cap; combined N=10 is the preferred aggregate scope; M11a-extension scope handles N=20+ if reviewers push
2. "Subtle steering of fresh sessions" — same protocol as M10b: 1 fresh session per trace, non-project cwd, /clear, single-message prompt, per-session attestation
3. "Only V2-3B vs V2-Opus" — V3 question closed at Opus scale per M10
4. "No cross-model" — M11b scope (separate milestone)
5. "Outcome table coverage" — 5-row table at each N-scope; integer-count buckets cover all cells
6. "GT-regime tagging is manual" — observation-only per pre-reg defense #6
7. "Iterative extension changes the protocol mid-stream" — addressed below in M11a-specific defense #1
8. "Why M11a after M10b's positive-aspect findings?" — addressed below in M11a-specific defense #2

### M11a-specific (new at this pre-reg)

1. **"Iterative extension is just adding rules during the run; that's goalpost-moving."** Defense: iterative extension is **mechanical and pre-registered at this commit** (each accepted trace's IDs/themes/tuples appended; no human judgment in the extension). The mechanism mirrors M8b/M10's between-milestone extension model — well-established repo precedent — applied within-milestone. The pre-registered extension rule is fully deterministic; no analyst discretion at any extension step. Far from goalpost-moving, this is a tightening of the protocol (each successive trace has more constraints, not fewer) that makes the experimental claim *harder* to support, not easier.

2. **"Why M11a if M10b's halt + N=5 combined was enough?"** Defense: M10b's combined-N=5 confidence intervals are very wide (V2-3B failure rate [14.7%, 94.7%]; V2-Opus failure rate [0.5%, 71.6%]). The H2 (model-scale) claim at point-estimate is "modestly confirmed" but the CI is too wide for a paper-headline statement. M11a tightens the CI by extending to N=8 (M10b + M11a) or N=10 (M10 + M10b + M11a). Without M11a, the paper's external-coverage section says "we ran 5 external traces but our CI is [0.5%, 72%]" — a fair reviewer attack. With M11a, the paper says "we ran 10 external traces under a drift-resistant protocol; CI tightened to [X%, Y%]." Substantially stronger.

3. **"M11a could itself drift and you'd just halt again."** Defense: pre-registered drift-quantification criteria above operationalize the success threshold mechanically. **Drift-revision success requires 0 literal-ID collisions across all attempts AND 0 strong overlaps in accepted traces** (per §Drift-monitoring criterion); the halt trigger fires automatically on the first literal-ID collision under iterative extension. If M11a drift continues despite iterative extension, that itself is a publishable deeper finding — "iterative banned-list extension is empirically not sufficient to prevent cross-trace drift in external-authoring at N=5; protocol-failure-mode 2 is identified, M11a-extension scope investigates stricter measures." The reviewer attack "your protocol still drifted" is converted into "our protocol revision was tested with mechanical zero-tolerance criteria at N=5; the outcome is one of {drift-revision success, partial success, halt-as-finding} pre-registered at Commit A." Either branch is defensible.

4. **"Banned-list saturation could push fresh sessions toward less-realistic content."** Defense: at end-of-M11a (127 IDs / 72 themes / 71 tuples; locked trajectory per §Banned-list growth trajectory), the banned-list constraint is meaningful but does not exhaust the space of plausible life-event scenarios. If M11a fresh sessions produce visibly-contrived content (e.g., bizarre scenarios chosen only to avoid banned themes), that surfaces in audit step 11 ("GTs are human-interpretable on content alone as warranting proaction"); the audit gate rejects implausible content regardless of banned-list status. **No saturation-driven implausibility is acceptable**; if it occurs, that's a finding (and the trace is rejected per audit). M11a-extension scope at N=20+ is where saturation may genuinely become limiting; M11a's N=5 is well below the saturation threshold.

5. **"Cross-protocol aggregation (M10 + M10b + M11a → N=10) is methodologically suspect because the protocols differ."** Defense: each milestone's protocol is documented in detail (M10 used M9-frozen banned list; M10b used M10b-frozen list; M11a uses iteratively-extended list). The combined N=10 aggregate is reported with **explicit cross-protocol caveat**: "the underlying coverage rate may differ across protocol generations; the combined aggregate is treated as a point estimate with the across-protocol heterogeneity noted." Sensitivity analysis can report each N-scope (5/8/10) separately so the reader can choose their preferred scope. The combined N=10 is offered as the **strongest** external-coverage estimate, not the *only* one.

6. **"Why not include random ablation in M11a too?"** Defense: M7's N=20 seed-variance + M10's test_v5 random cell + M10b's skipped-random-by-design already pin the random-arbiter behavior. Adding random in M11a would duplicate prior work without adding information specific to the iterative-extension question. M11a focuses on the protocol-revision question, not on re-confirming random-ablation findings.

7. **"You knew about M10b's structural-parsing failure mode (test_v7 attempt #2 burned a retry on it) and didn't add a self-restate pre-flight gate to M11a — that's an oversight."** Defense: it is a *named deferral*, not an oversight. M10b surfaced two distinct authoring failure modes — (a) banned-list pressure causing cross-trace overlap drift; (b) fresh-session structural-constraints parsing variability. M11a's iterative-extension rule addresses (a) only. Adding a self-restate pre-flight gate (prompt the fresh session to enumerate the 11 hard structural constraints back before generating) would address (b) but would change two protocol levers simultaneously, confounding attribution of any drift-revision improvement to the iterative-extension rule in isolation. The cleanest experimental design isolates one protocol change per milestone; M11a is the iterative-extension milestone. Self-restate is explicitly named as **M11a-extension scope** with its own pre-reg. If M11a authoring hits structural-parsing failures (test_v7-attempt-#2-class), they are logged in §"Per-attempt drift log" as observation; the structural-parsing failure rate at M11a's N≤15 attempts becomes a pre-data measurement informing M11a-extension's pre-reg. Either branch (M11a clean of structural-parsing failures, or M11a hits them at observable rate) is a legitimate empirical input to the next protocol-revision step.

## Non-goals (carry-forward from M10b with M11a additions)

Carry-forward (unchanged from M10b):
- No new architectural lever
- No prompt redesign (V2 and V3 stay frozen)
- No cross-model sweep (M11b scope)
- No hierarchical routing (M11c scope)
- No coverage-variance estimate at N=20+ (M11a-extension scope; pre-reg this if reviewer pushes)
- No re-running test_v3 / test_v4 / test_v5 (artifacts)
- No edits to V2 / V3 prompts in response to M11a results

M11a-specific additions:
- **No re-running M10b's test_v6 / test_v7 / test_v8** — these are already evaluated at M10b D-on-N=3; M11a treats them as fixed external evaluation artifacts
- **No editing the iterative-extension rule mid-M11a** — the extension rule is locked at M11a Commit A; if extension behaves badly in C2-C5, that's a finding, not grounds for tweaking the rule
- **No exclusion of "inconvenient" rejected traces from the per-attempt drift log** — every fresh-session attempt is logged whether accepted or rejected, mirroring M10b's full-transparency Rejections log
- **No self-restate pre-flight gate added in M11a** — M10b's test_v7 attempt #2 surfaced a second failure mode (fresh-session structural-constraints parsing variability) distinct from banned-list-pressure drift. A self-restate gate (prompt the fresh session to enumerate the 11 hard structural constraints back before generating) would address it, but adding it *here* would change two protocol levers at once and confound attribution of any drift improvement to the iterative-extension rule alone. Explicitly deferred to **M11a-extension scope** as a separately-pre-registered protocol layer; if M11a hits structural-parsing failures during authoring they are reported as observation, not scope creep, and will inform M11a-extension's pre-reg

## Authoring sessions

(Populated during Commits C1-C5. One row per fresh session. Per-session attestation per §"Authoring protocol per trace": timestamp + cwd + dispatched response.model + /clear confirmation per trace. Dispatched response.model is verified at the API level — not just at the Claude Code TUI /model line. Mirrors runs/18 §"Authoring sessions" structure verbatim with the dispatched-model clarification carried forward from M11a pre-reg line 9.)

| trace | fresh-session timestamp | cwd | session model (user-confirmed) | /clear confirmation | audit attempt # | audit verdict |
|---|---|---|---|---|---|---|
| test_v11 | 2026-05-08 19:19 | `/Users/patrick.gergen/Pictures` | `claude-opus-4-7` (Opus 4.7, user-confirmed) | confirmed | 2 of 3 (attempt #1 rejected for structural-parsing; see §"Per-attempt drift log") | PASS (with 5 transparent borderline-theme notes; see §"Mechanism notes") |
| test_v12 | 2026-05-09 08:41 | `/Users/patrick.gergen/Pictures` | `claude-opus-4-7` (Opus 4.7, user-confirmed) | confirmed | 1 | PASS (with 5 transparent borderline-theme notes; see §"Mechanism notes") |
| test_v13 | 2026-05-12 19:34 | `/Users/patrick.gergen/Pictures` | `claude-opus-4-7` (Opus 4.7, user-confirmed) | confirmed | 3 of 3 (attempts #1 + #2 rejected; see §"Per-attempt drift log") | PASS (with 5 transparent borderline-theme notes; see §"Mechanism notes") |
| test_v14 | 2026-05-12 19:51 | `/Users/patrick.gergen/Pictures` | `claude-opus-4-7` (Opus 4.7, user-confirmed) | confirmed | 1 | PASS (with 5 transparent borderline-theme notes; see §"Mechanism notes") |
| test_v15 | 2026-05-12 20:09 | `/Users/patrick.gergen/Pictures` | `claude-opus-4-7` (Opus 4.7, user-confirmed) | confirmed | 2 of 3 (attempt #1 rejected; see §"Per-attempt drift log") | PASS (with 5 transparent borderline-theme notes; see §"Mechanism notes") |

## Per-attempt drift log

(Populated during Commits C1-C5. One entry per fresh-session attempt — accepted AND rejected — per §"Drift-quantification log" full-transparency requirement; extends M10b's Rejections log discipline at runs/18 §"Rejections log" to also capture accepted-attempt drift content. Each entry notes: attempt number, fresh-session timestamp, verdict (PASS / REJECT), first violated audit step (if REJECT), per-overlap-severity counts (literal-ID / strong / mild) with specific trace+ID references, and a one-sentence description. A rejected generation is not merged; the generator code is not kept — carry-forward of M10b's discipline at runs/18 §"Rejections log" line 296.)

### test_v11 — attempt #1 (2026-05-08 18:27)

**Verdict:** Reject (strict-letter; structural-parsing violation — audit step 1 schema check fails).

**First violated audit step (audit-checklist order):** Audit step 1 — schema check. The trace as authored does not parse at import time: the `travel_visa_window` GT's `Event(...)` construction contains a stray walrus expression `sim_function := None or "notification"` interleaved between keyword arguments, producing a `SyntaxError`. The audit's standard schema-check command (`uv run python -c "from sandbox.event_trace import get_trace; get_trace('test_v11')"`) fails on parse before any keyword/content, banned-list, or cross-trace literal-ID audit gate can run.

**Per-overlap-severity counts:** literal-ID 0 / strong 0 / mild 0 (audit gates 2-5 not reached due to step-1 parse failure; no overlap evaluation possible).

**Description:** Fresh session (Pictures cwd, 2026-05-08 18:27, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed) produced a single-shot trace whose visa GT line read `Event(id="travel_visa_window", kind="notification", sim_function := None or "notification", sim_time=520.0, content=...)` — an invalid Event construction dropping a walrus assignment between keyword args. Structural-parsing failure mode (test_v7-attempt-#2 class per runs/18 §"Failure-mode analysis"), not a banned-list-pressure signal: the bug is at the Python-syntax layer, not the content layer. Counts toward the retry cap. Pre-reg §"Reviewer-vulnerable surfaces and pre-registered defenses" defense #7 explicitly anticipates this failure mode at M11a's N≤15 attempts as M11a-extension scope input.

### test_v11 — attempt #2 (2026-05-08 19:19)

**Verdict:** PASS (audit-PASS with 5 transparent borderline-theme notes; see §"Mechanism notes" → test_v11 subsection).

**First violated audit step:** N/A — all six audit steps pass strict-letter (schema, keyword/content alignment, banned-ID + banned-tuple bytewise review, cross-trace literal-ID grep, GT-regime classification independent). The 5 borderline-theme notes are mild structural overlaps, judgment-only per §"Drift-monitoring criterion" rubric line 285, and do not gate audit.

**Per-overlap-severity counts (mechanical, against committed test_v6/v7/v8 GT pool — 15 prior committed GTs):**
- Literal-ID 0 / strong 0 / mild 5.
- Strong-overlap (a) GT keyword tuple bytewise match (order-independent, lowercased): 0 hits across `{locksmith,buzzer}`, `{tutoring,moved}`, `{wallet,pickup}`, `{marathon,closes}`, `{slides,feedback}` vs the 15 prior committed GT tuples.
- Strong-overlap (b) ≥8-word verbatim phrase (lowercased, whitespace-normalized): 0 hits across the 5 new GT contents vs the 15 prior committed GT contents.
- Mild overlap: 5 (one per GT; structural-pattern parallels with banned themes; see §"Mechanism notes" → test_v11 for per-GT diagnoses).
- Cross-trace literal-ID collision (audit step 4): 0 collisions across 9 new IDs vs the 27 prior committed-trace IDs (test_v6/v7/v8).

**Description:** Fresh session (Pictures cwd, 2026-05-08 19:19, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed) produced a single-shot trace passing strict-letter audit on first read at attempt #2 (after attempt #1's structural-parsing rejection). Variable name `all_events` preserved verbatim from fresh-session emission per the M10 permitted-edits rule (only registry-line addition required during integration; runs/16 line 239 protocol carry-forward). Mechanical drift rubric — 0 literal-ID collisions, 0 strong-overlap (a), 0 strong-overlap (b) — fully clean for M11a's drift-revision-success criterion (which requires 0 literal-ID across all attempts AND 0 strong overlaps in accepted traces, per §"Drift-monitoring criterion"). Trace accepted as M11a's first committed trace (C1).

### test_v11 — retry-cap status: 2 / 3 attempts used; 1 remaining (attempt #2 accepted)

### test_v12 — attempt #1 (2026-05-09 08:41)

**Verdict:** PASS (audit-PASS with 5 transparent borderline-theme notes; see §"Mechanism notes" → test_v12 subsection).

**First violated audit step:** N/A — all six audit steps pass strict-letter (schema, keyword/content alignment, banned-ID + banned-tuple bytewise review against 91 IDs / 51 tuples, cross-trace literal-ID grep against 36 prior committed IDs, GT-regime classification independent). The 5 borderline-theme notes are mild structural overlaps, judgment-only per §"Drift-monitoring criterion" rubric line 285, and do not gate audit.

**Per-overlap-severity counts (mechanical, against committed test_v6/v7/v8/v11 GT pool — 20 prior committed GTs):**
- Literal-ID 0 / strong 0 / mild 5.
- Strong-overlap (a) GT keyword tuple bytewise match (order-independent, lowercased): 0 hits across `{garage,open}`, `{hospitalized,mike}`, `{expires,license}`, `{hoa,vote}`, `{deposit,margin}` vs the 20 prior committed GT tuples.
- Strong-overlap (b) ≥8-word verbatim phrase (lowercased, whitespace-normalized): 0 hits across the 5 new GT contents vs the 20 prior committed GT contents.
- Mild overlap: 5 (one per GT; structural-pattern parallels with banned themes; see §"Mechanism notes" → test_v12 for per-GT diagnoses).
- Cross-trace literal-ID collision (audit step 4): 0 collisions across 9 new IDs vs the 36 prior committed-trace IDs (test_v6/v7/v8 + test_v11).

**Description:** Fresh session (Pictures cwd, 2026-05-09 08:41 CEST = 06:41 UTC, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/da1af815-472f-4efe-97c5-2f39a3991611.jsonl`) produced a single-shot trace passing strict-letter audit on first read. Variable name `all_events` preserved verbatim from fresh-session emission per the M10 permitted-edits rule (only registry-line addition required during integration; runs/16 line 239 protocol carry-forward). Mechanical drift rubric — 0 literal-ID collisions, 0 strong-overlap (a), 0 strong-overlap (b) — fully clean for M11a's drift-revision-success criterion. Trace accepted as M11a's second committed trace (C2).

**Prompt-formatting transparency note (whitespace-only paste artifact, not a content drift):** The actual fresh-session prompt SHA256 was `a626f6110d16d1f21fe611712ed6ed8252404c8cb79f2a3a5854712a50b84e4f` (18,719 chars), differing byte-wise from the C2-prompt SHA `39068ab7daa0db40ea773c814bdb1d2f9e4b1169033d8ff5cced36fe2eab228e` (12,449 chars) that was generated by mechanical extension of C1. Whitespace-normalized SHA matches exactly between actual-fresh-session and expected-generated: `637151c6091d9bc9348f0a87f961e4461d87b876157e97ab50ce8e9759e01201`. Diff is 100% whitespace: 4-space indent vs 2-space indent + extra blank lines from markdown→terminal paste rendering. All structural markers identical: 91 banned IDs (zero set diff), 51 banned tuples, identical test_v12 / test_trace_v12 / banned-list-anchor-ID counts, identical 5-section structure. Documented as a paste-induced format artifact rather than a prompt-content drift. Forward fix: C3-C5 prompts will be supplied as a file path the user can `cat` to clipboard rather than pasting from rendered markdown, eliminating indent-doubling.

### test_v12 — retry-cap status: 1 / 3 attempts used; 2 remaining (attempt #1 accepted)

### test_v13 — attempt #1 (2026-05-09 09:26 CEST = 07:26 UTC)

**Verdict:** Reject (audit step 3c banned-theme reuse).

**First flagged violation:** Audit step 3c — banned-theme manual review. GT `frost_advisory_garden` ("Frost advisory for your area tonight: temperatures dropping to 29F. Cover sensitive outdoor plants before 22:00.") falls within the literal banned theme "weather alert/forecast/precipitation" (M10b-pre-reg banned theme #14, embedded verbatim in the C3 fresh-session prompt). The "/forecast/precipitation" qualifier on the literal banned-theme text signals broad coverage including weather-forecast events; a frost advisory IS a weather forecast about cold-temperature conditions. Strict-letter banned-theme reuse, distinct from the M10b wedding-theme precedent (M10b's wedding_rsvp + wedding_rehearsal accepted as mild because no literal "wedding event" banned theme existed; here, "weather alert" IS a literal banned theme covering frost).

**Additional borderline notes (not load-bearing on the rejection itself):** GT `brother_layover_text` ("Hey, my layover got shortened — landing at SFO 19:40 instead of 21:15. Can you still grab me from arrivals?") shows strong structural overlap with banned theme "family voicemail with airport pickup, 15-min window" (test_v7) — sub-categories distinct (brother text vs sister voicemail; layover-shortened-arriving-early vs landed-early; 600s vs 15-min) but the broad domain "family member airport pickup with tight window" is identical. Combined with frost_advisory, two strong-borderlines in a single attempt.

**Per-overlap-severity counts (mechanical, against committed test_v6/v7/v8/v11/v12 GT pool — 25 prior committed GTs):** literal-ID 0 / strong 0 / mild 5 (one per GT; strong-overlap rubric a+b mechanically PASSED at zero hits; all overlap classification is via judgment-based banned-theme review).

**Description:** Fresh session (Pictures cwd, 2026-05-09 09:26 CEST, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/b476c861-705a-48ea-92f0-83182cf34c90.jsonl`, prompt SHA `2b5b6c5f2a87618482ade211ae9dd2100639e7c246dd94906cd452fca7fcc627`). Single-shot output passed mechanical drift rubric + cross-trace literal-ID check + structural constraints, but failed strict-letter banned-theme review on `frost_advisory_garden` ≈ "weather alert/forecast/precipitation". Counts toward retry cap. Pre-reg defense #4 (banned-list saturation) and §"Drift-monitoring criterion" rubric line 285 (mild vs strong-mechanical distinction) both relevant: the rubric explicitly makes strong-overlap mechanical-only (a or b), so noun-substitution attacks are MILD by rubric; but banned-theme **REUSE** at the literal-text level is a separate gate via audit step 3c, and here the frost advisory falls within the literal "weather alert/forecast/precipitation" coverage.

### test_v13 — attempt #2 (2026-05-09 09:35 CEST = 07:35 UTC)

**Verdict:** Reject (audit step 1 structural-constraint violation).

**First violated constraint (audit-checklist order):** Audit step 1 / hard structural constraint #3 — "for every GT, gt.event.sim_time + gt.proaction_window_s ≤ 1000". GT `zoom_link_changed` has sim_time=410.0 + window=600.0 = **1010.0 > 1000** — fails the inequality. Hard constraint violation; auto-rejects regardless of other audit steps.

**Additional banned-theme borderline notes (not load-bearing on the rejection; constraint #3 supersedes):** GT `zoom_link_changed` (Zoom link changed for investor sync) shows strict-letter banned-theme reuse candidate vs "work meeting time/location change" (M10b banned theme #2, embedded verbatim in C3 prompt) — a Zoom link change IS a virtual-meeting location change. GT `bridge_lane_closure` (Hawthorne Bridge lane closure affecting commute today) shows strong structural overlap with banned theme "parking meter or civil disruption affecting commute" (M10b) + "civic-event affecting tomorrow's commute (planned street closures)" (test_v11). GT `contractor_arrival_window` (landscaping contractor 15-min out) shows strong structural overlap with test_v11 "vendor on-site at building entry, callback request to grant access, tight window". GT `freezer_door_ajar` shows structural overlap with test_v12 "smart-home alert: garage door left open after sunset". Recorded for transparency; the constraint #3 violation alone is sufficient for reject under hard-constraint auto-reject rule.

**Per-overlap-severity counts:** literal-ID 0 / strong 0 / mild 5 (audit step 4 cross-trace literal-ID PASS, strong-overlap rubric a+b PASS; theme-reuse via judgment, structural overlap dominant).

**Description:** Fresh session (Pictures cwd, 2026-05-09 09:35 CEST, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/ecc027ec-a384-4935-ba51-a0cef117a052.jsonl`, prompt SHA `2b5b6c5f...` byte-identical to attempt #1 per "no prompt edits between retries"). Structural-parsing failure mode (test_v7-attempt-#2 class per runs/18 §"Failure-mode analysis"): the fresh session miscounted the sim_time+window arithmetic for `zoom_link_changed` (410+600=1010, off-by-10 from the cap). Counts toward retry cap. Pre-reg defense #7 explicitly anticipates this failure mode at M11a's N≤15 attempts as M11a-extension scope input.

### test_v13 — attempt #3 (2026-05-12 19:34 CEST = 17:34 UTC)

**Verdict:** PASS (audit-PASS with 5 transparent borderline-theme notes; see §"Mechanism notes" → test_v13 subsection).

**First violated audit step:** N/A — all six audit steps pass strict-letter (schema, keyword/content alignment, banned-ID + banned-tuple bytewise review against 100 IDs / 56 tuples, cross-trace literal-ID grep against 45 prior committed IDs, GT-regime classification independent). The 5 borderline-theme notes are mild structural overlaps with prior accepted traces — broad-domain tag overlap, no strong sub-criterion fires — judgment-only per §"Drift-monitoring criterion" rubric line 285, and do not gate audit. **Critically: NO literal banned-theme reuse** (distinct from attempts #1 + #2; this is the qualitative improvement that enabled acceptance).

**Per-overlap-severity counts (mechanical, against committed test_v6/v7/v8/v11/v12 GT pool — 25 prior committed GTs):**
- Literal-ID 0 / strong 0 / mild 5.
- Strong-overlap (a) GT keyword tuple bytewise match (order-independent, lowercased): 0 hits across `{agent,counter-offer}`, `{interview,reply}`, `{book club,host}`, `{converts,trial}`, `{registered,warranty}` vs the 25 prior committed GT tuples.
- Strong-overlap (b) ≥8-word verbatim phrase (lowercased, whitespace-normalized): 0 hits across the 5 new GT contents vs the 25 prior committed GT contents.
- Mild overlap: 5 (one per GT; structural-template parallels with prior accepted traces' themes; see §"Mechanism notes" → test_v13 for per-GT diagnoses; closest calls are `book_club_host` ≈ test_v8 "tomorrow vet appointment + prep" template and `ryobi_warranty` ≈ test_v12 "DMV license renewal deadline today at midnight" template).
- Cross-trace literal-ID collision (audit step 4): 0 collisions across 9 new IDs vs the 45 prior committed-trace IDs.

**Description:** Fresh session (Pictures cwd, 2026-05-12 19:34 CEST, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/fcd09e33-9a7a-4761-8305-ea1d361c3f96.jsonl`, prompt SHA `2b5b6c5f...` byte-identical to attempts #1 + #2 per "no prompt edits between retries"). Single-shot output passing strict-letter audit on third read after attempts #1 (banned-theme reuse) and #2 (structural-constraint violation) rejections. Variable name `events` (not `all_events`) preserved verbatim from fresh-session emission per the M10 permitted-edits rule. Mechanical drift rubric — 0 literal-ID collisions, 0 strong-overlap (a), 0 strong-overlap (b) — fully clean for M11a's drift-revision-success criterion. Trace accepted as M11a's third committed trace (C3).

### test_v13 — retry-cap status: 3 / 3 attempts used; 0 remaining (attempt #3 accepted at retry-cap boundary)

**Trajectory note for M11a-extension scope:** test_v13 consumed the full retry-cap-3 budget to land an accepted trace. The two prior rejections are independently legitimate per pre-reg defenses #4 (banned-list saturation: attempt #1's frost_advisory → "weather alert/forecast/precipitation" reuse) and #7 (structural-parsing variability: attempt #2's sim_time+window=1010 arithmetic miss). The 3-attempts-to-accept pattern is consistent with M10b's test_v7 experience (also 3 attempts) and is within pre-reg expectations, but the qualitative pattern across M11a so far — test_v11 (2 attempts: structural-parsing + accept), test_v12 (1 attempt: accept), test_v13 (3 attempts: theme-reuse + structural-parsing + accept) — suggests fresh-session prompt-following reliability has high variance at the C2+ banned-list size (100/56). The pattern across rejected attempts is the empirical input to M11a-extension scope's self-restate pre-flight gate decision (deferred per pre-reg §"M11a-specific defenses" #7).

### test_v13 — cross-attempt informational drift observations (rejected attempts #1 + #2; INFORMATIONAL — rejected attempts do not extend the banned list per pre-reg §"Banned-list growth trajectory" line 131)

1. **`cloud_photos_synced` distractor ID convergence:** Both rejected attempt #1 ("412 photos from last weekend have finished syncing to your archive") and rejected attempt #2 ("218 photos from last weekend have finished syncing to your cloud library") independently produced the identical distractor ID `cloud_photos_synced`. Different fresh sessions (different sessionIds, different timestamps), different content (different photo counts, different sync destinations), but byte-identical distractor ID. Independent fresh-session convergence on the same identifier despite no shared transcript context. Not a protocol violation (rejected attempts don't extend the banned list; accepted attempt #3 does not contain `cloud_photos_synced`).

2. **`("oven", "preheating")` keyword tuple convergence:** Both rejected attempt #1 (GT `oven_preheat_done`) and rejected attempt #2 (GT `oven_preheat_stuck`) independently produced the identical keyword tuple `("oven", "preheating")`. Different GT IDs, different sub-categories (preheat-done-casserole-ready vs preheat-stuck-no-cooking), but byte-identical tuple. Independent fresh-session convergence on the smart-oven domain. Not a protocol violation; accepted attempt #3 does not contain oven-related GTs.

3. **5pm/EOD-today-deadline pattern:** All 3 attempts (rejected + accepted) included a GT with a "deadline today around 5pm" or "EOD today" framing. Attempt #1's brother_layover_text had an implicit afternoon-arrival pickup. Attempt #2's hoa-style today-deadlines. Attempt #3's counter_offer (5pm today), interview_confirm (EOD today), ryobi_warranty (midnight today). Suggests fresh-session preference for "today-deadline" content scaffolding.

These convergence signals are documented for paper transparency and as M11a-extension scope inputs; they do not gate the trace acceptance per protocol (rejected-attempt content does not enter the banned list).

### test_v14 — attempt #1 (2026-05-12 19:51 CEST = 17:51 UTC; transcript-paste 17:49:35Z UTC)

**Verdict:** PASS (audit-PASS with 5 transparent borderline-theme notes; see §"Mechanism notes" → test_v14 subsection).

**First violated audit step:** N/A — all six audit steps pass strict-letter (schema, keyword/content alignment, banned-ID + banned-tuple bytewise review against 109 IDs / 61 tuples, cross-trace literal-ID grep against 54 prior committed IDs, GT-regime classification independent). The 5 borderline-theme notes are mild structural overlaps with prior accepted traces — broad-domain tag overlap, no strong sub-criterion fires — judgment-only per §"Drift-monitoring criterion" rubric line 285, and do not gate audit. **NO literal banned-theme reuse.**

**Per-overlap-severity counts (mechanical, against committed test_v6/v7/v8/v11/v12/v13 GT pool — 30 prior committed GTs):**
- Literal-ID 0 / strong 0 / mild 5.
- Strong-overlap (a) GT keyword tuple bytewise match (order-independent, lowercased): 0 hits across `{backup,codes}`, `{inspector,walkthrough}`, `{movers,slot}`, `{bond,confirmation}`, `{boil-water,tap}` vs the 30 prior committed GT tuples.
- Strong-overlap (b) ≥8-word verbatim phrase (lowercased, whitespace-normalized): 0 hits across the 5 new GT contents vs the 30 prior committed GT contents.
- Mild overlap: 5 (one per GT; structural-template parallels with prior accepted traces' themes; see §"Mechanism notes" → test_v14 for per-GT diagnoses; closest call is `bond_purchase_confirm` ≈ test_v7 "financial deadline 17:00 today (mortgage rate lock)" template — both share "rate locked-in" terminology + 5pm-today deadline + financial-decision-or-forfeit; sub-categories distinct: Treasury Direct bond purchase vs mortgage rate-lock signing).
- Cross-trace literal-ID collision (audit step 4): 0 collisions across 9 new IDs vs the 54 prior committed-trace IDs.

**Description:** Fresh session (Pictures cwd, 2026-05-12 19:51 CEST = 17:51 UTC user-reported, transcript prompt-arrival timestamp 17:49:35.878Z UTC — 1-2 min log/local variance, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/958b81be-c001-4a6c-944a-77e0ed81f72e.jsonl`, prompt SHA `70e1139038bcc57cbbcc0f59fe2019a8f3f5869d3b50d2389d4dd16638b002dd` byte-identical to mechanically-generated C4 prompt). Single-shot output passing strict-letter audit on first read. Variable name `all_events` preserved verbatim from fresh-session emission per the M10 permitted-edits rule. 5 distinct GT kinds (notification, calendar_update, phone_message, email, world_event) — matches test_v13 attempt #3 diversity, exceeds test_v11/v12. Mechanical drift rubric — 0 literal-ID collisions, 0 strong-overlap (a), 0 strong-overlap (b) — fully clean for M11a's drift-revision-success criterion. Trace accepted as M11a's fourth committed trace (C4).

### test_v14 — retry-cap status: 1 / 3 attempts used; 2 remaining (attempt #1 accepted)

### test_v15 — attempt #1 (2026-05-12 20:01 CEST = 18:01 UTC)

**Verdict:** Reject (audit step 1 hard structural constraint #3 violation).

**First violated constraint:** Audit step 1 / hard structural constraint #3 — "for every GT, gt.event.sim_time + gt.proaction_window_s ≤ 1000". GT `thesis_advisor_swap` has sim_time=540.0 + window=600.0 = **1140.0 > 1000** — off-by-140 arithmetic miss. Hard-constraint auto-reject; supersedes all other audit steps. Same test_v7-attempt-#2 class failure mode as test_v13 attempt #2's `zoom_link_changed` (410+600=1010). Third structural-parsing failure across M11a (after test_v11 attempt #1 and test_v13 attempt #2).

**Additional informational observations (not load-bearing on the rejection):**
- GT IDs `oven_preheat_stuck` and `freezer_door_ajar` are byte-identical to rejected test_v13-attempt-#2 IDs (independent fresh sessions ~3 days apart converging on the same 2 IDs). Rejected attempts don't formally extend the banned list per pre-reg §"Banned-list growth trajectory" line 131, so this is NOT a literal-ID violation against accepted traces. But it is the strongest cross-rejected-attempt ID convergence signal seen across M11a (stronger than test_v13's `cloud_photos_synced` distractor convergence; here two GTs converged).
- 9 events / 5 GTs / 4 distractors structural shape OK; keyword/content alignment all PASS; only constraint #3 fails.

**Per-overlap-severity counts:** literal-ID 0 / strong 0 / mild N/A (audit gates 2-5 not reached due to step-1 constraint-#3 failure on `thesis_advisor_swap`).

**Description:** Fresh session (Pictures cwd, 2026-05-12 20:01 CEST, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/65576cec-c8a2-45b3-8f16-8eada4f68d03.jsonl`, prompt SHA `8fa7a76e466d6d9f461d3bab4e74d75c9eeafc70ee719a212af675454456fc2e` byte-identical to mechanically-generated C5 prompt). Structural-parsing failure mode: fresh session miscounted sim_time+window arithmetic for `thesis_advisor_swap` (540+600=1140, off-by-140 from cap). Counts toward retry cap. Pre-reg defense #7 explicitly anticipates this failure mode at M11a's N≤15 attempts as M11a-extension scope input — this is the **third** structural-parsing failure across M11a's 8 attempts so far (test_v11 attempt #1 + test_v13 attempt #2 + this one) → structural-parsing-failure rate 3/8 = 37.5% before attempt #2 (now 3/9 = 33.3% after attempt #2 PASS).

### test_v15 — attempt #2 (2026-05-12 20:09 CEST = 18:05 UTC transcript-paste)

**Verdict:** PASS (audit-PASS with 5 transparent borderline-theme notes; see §"Mechanism notes" → test_v15 subsection).

**First violated audit step:** N/A — all six audit steps pass strict-letter (schema, keyword/content alignment, banned-ID + banned-tuple bytewise review against 118 IDs / 66 tuples, cross-trace literal-ID grep against 63 prior committed IDs, GT-regime classification independent). The 5 borderline-theme notes are mild structural overlaps with prior accepted traces — broad-domain tag overlap, no strong sub-criterion fires — judgment-only per §"Drift-monitoring criterion" rubric line 285, and do not gate audit. **NO literal banned-theme reuse.**

**Per-overlap-severity counts (mechanical, against committed test_v6/v7/v8/v11/v12/v13/v14 GT pool — 35 prior committed GTs):**
- Literal-ID 0 / strong 0 / mild 5.
- Strong-overlap (a) GT keyword tuple bytewise match: 0 hits across `{1:1, skip-level}`, `{baby shower, collection}`, `{auto-payment, balance}`, `{auto-cancel, reservation}`, `{approve, brake}` vs the 35 prior committed GT tuples.
- Strong-overlap (b) ≥8-word verbatim phrase: 0 hits across the 5 new GT contents vs the 35 prior committed GT contents.
- Mild overlap: 5 (one per GT; structural-template parallels with prior accepted traces' themes; see §"Mechanism notes" → test_v15 for per-GT diagnoses; closest calls are `visa_autopay_low_balance` ≈ test_v12 "brokerage margin call requiring 2-hour deposit" template and `brake_job_approval` ≈ test_v14 "voicemail from movers offering swap of moving-day slot" template).
- Cross-trace literal-ID collision (audit step 4): 0 collisions across 9 new IDs vs the 63 prior committed-trace IDs.

**Description:** Fresh session (Pictures cwd, 2026-05-12 20:09 CEST user-reported, prompt-arrival 2026-05-12T18:05:51.757Z UTC, dispatched response.model `claude-opus-4-7` user-verified, /clear confirmed; transcript `~/.claude/projects/-Users-patrick-gergen-Pictures/36903292-2d8f-4355-836a-de21f1eca6a2.jsonl`, prompt SHA `8fa7a76e466d6d9f461d3bab4e74d75c9eeafc70ee719a212af675454456fc2e` byte-identical to attempt #1 per "no prompt edits between retries"). Single-shot output passing strict-letter audit on first read at attempt #2 (after attempt #1's constraint #3 rejection). Variable name `events` preserved verbatim from fresh-session emission per the M10 permitted-edits rule. Mechanical drift rubric — 0 literal-ID collisions, 0 strong-overlap (a), 0 strong-overlap (b) — fully clean for M11a's drift-revision-success criterion. **Trace accepted as M11a's fifth and final committed trace (C5).**

### test_v15 — retry-cap status: 2 / 3 attempts used; 1 remaining (attempt #2 accepted)

### test_v15 — cross-attempt informational drift observations (rejected attempts; INFORMATIONAL — rejected attempts do not extend the banned list per pre-reg §"Banned-list growth trajectory" line 131)

1. **Cross-trace ID convergence test_v13-attempt-#2 → test_v15-attempt-#1:** Rejected test_v13 attempt #2 (May 9) had GT IDs `oven_preheat_stuck` and `freezer_door_ajar`; rejected test_v15 attempt #1 (May 12, ~3 days later) reproduced both byte-identical IDs in independent fresh sessions with no shared transcript context. Strongest cross-rejected-attempt ID-space convergence observed across M11a (two GTs simultaneously, not just one distractor). Suggests under banned-list saturation at C5-state-prompt (118/67/66), fresh-session ID-space has nontrivial attractor structure around smart-home appliance state alerts.

2. **Cross-trace distractor ID convergence test_v13-attempt-#2 → test_v15-attempt-#2:** Rejected test_v13 attempt #2 had distractor `utility_usage_summary`; accepted test_v15 attempt #2 also produced distractor `utility_usage_summary` (different content: weekly-electricity-12%-lower vs April-312kWh-4%-below-12mo-average; same byte-identical ID). Independent fresh sessions converging on the same distractor ID despite different banned-list states (test_v13-attempt-#2 saw 91/52/51; test_v15-attempt-#2 saw 118/67/66).

3. **No cross-attempt convergence test_v15-attempt-#1 → test_v15-attempt-#2 IDs:** Both rejected attempt #1 and accepted attempt #2 of test_v15 produced fully disjoint ID sets — same prompt, same banned-list state, different fresh sessions, content fully diverged. (Distinct from test_v13 attempts #1↔#2 which had no ID overlap either, and from the cross-trace convergences observed elsewhere.) This intra-trace consistency suggests within-trace fresh-session content variance is high even under identical prompt + banned-list state — the cross-trace convergences are not just "the protocol always converges" but reflect content-attractor structure conditional on banned-list saturation.

These three cross-rejected-attempt convergence signals across M11a (test_v13's `cloud_photos_synced`; v13→v15-#1's `oven_preheat_stuck` + `freezer_door_ajar`; v13→v15-#2's `utility_usage_summary`) are the strongest paper-level finding within defense #4 (banned-list saturation) ambit. They do not gate any pre-reg threshold and do not constitute literal-ID violations under the protocol (rejected attempts don't extend the banned list), but they are M11a-extension scope material: under N=20+ scope or stricter protocol revisions, these informal-attractor signals would inform whether rejected-attempt-IDs should be promoted to formal banned-list status.

## GT-regime classification

Independent classification of each GT's regime against V2's literal YES list (`agent/arbiter.py`, `ARBITER_SYSTEM_PROMPT_V2`), performed before any harness cell on that trace runs (per per-trace structural audit step 5). V2's YES enumeration has 6 categories: (1) urgent safety/security; (2) personal schedule changes; (3) financial/deadline obligations within next few days; (4) personal messages/deliveries; (5) weather/external conditions changing planned day; (6) production/on-call alerts. Per-trace subsections appended at each accepted Commit C1-C5; the regime column is mechanically reused as the appended banned-theme entry under the iterative-extension rule (per §"Authoring protocol per trace" → "Banned content themes" extension rule).

### test_v11 (5 GTs)

| GT id | regime | V2 category match | classification |
|---|---|---|---|
| locksmith_buzzer | vendor on-site at building entry, callback request to grant access, tight window | clean: cat 4 (personal messages/deliveries) — voicemail directed personally with urgent callback ask | **IN-V2-enum** |
| spanish_tutoring_shift | tutoring session time-shift today (+30 min), personal-services schedule change | clean: cat 2 (personal schedule changes) — appointment-time-shift in personal-services domain | **IN-V2-enum** |
| bistro_wallet_holding | lost-item recovery deadline today, tonight's-close pickup window | partial: cat 3 (deadline obligation) spirit match (pickup-by-tonight today-deadline; not a financial obligation in V2's bill/rent/report literal-example sense); cat 4 (personal deliveries) partial (lost-item-pickup is delivery-adjacent) | **PARTIALLY in-V2-enum** |
| city_marathon_closures | civic-event affecting tomorrow's commute (planned street closures) | clean: cat 5 (weather/external conditions changing planned day) — civic event with published street closures fits the "external condition affecting planned day" framing | **IN-V2-enum** |
| pitch_slides_review_ask | friend's professional-favor request with tomorrow-morning deadline | partial: cat 3 (deadline obligation) spirit match (tomorrow-9am deadline on slides review; not literal V2 example which lists bill/rent/report/payment); cat 4 (personal messages) partial match (friend's email ask) | **PARTIALLY in-V2-enum** |

**Aggregate (test_v11):** 3 clean-in (locksmith_buzzer, spanish_tutoring_shift, city_marathon_closures) + 2 partial-in (bistro_wallet_holding, pitch_slides_review_ask) + 0 borderline-out. Slightly more in-enum-tilted than test_v6 (1+2+2) and test_v8 (1+2+2), closer to test_v7 (2+2+1). M11a-relevant prediction: V2-3B might land 0.60-1.00 (bistro_wallet_holding + pitch_slides_review_ask are the at-risk GTs); V2-Opus expected 0.80-1.00.

### test_v12 (5 GTs)

| GT id | regime | V2 category match | classification |
|---|---|---|---|
| garage_open_overnight | smart-home alert: garage door left open after sunset, household-security check-on with tight window | clean: cat 1 (urgent safety/security) — smart-home security-adjacent alert about own-property state | **IN-V2-enum** |
| friend_hospitalized | voicemail update about close friend hospitalized for chest pains, informational (no immediate-action demand) | clean: cat 4 (personal messages/deliveries) — voicemail directed personally; cat 1 (urgent safety) partial spirit match (medical info about close friend) | **IN-V2-enum** |
| license_expires_today | DMV driver's license renewal deadline today at midnight, legal/regulatory requirement | partial: cat 3 (financial/deadline obligations within next few days) spirit match (today-deadline regulatory obligation; not literal V2 example which lists bill/rent/report/payment) | **PARTIALLY in-V2-enum** |
| hoa_assessment_vote | HOA emergency assessment vote with today-deadline financial-obligation decision | partial: cat 3 (financial obligation deadline) spirit match (HOA assessment is financial obligation with today deadline; not literal V2 example) | **PARTIALLY in-V2-enum** |
| margin_account_warning | brokerage margin call requiring 2-hour deposit to avoid forced liquidation | partial: cat 3 (financial obligation, deadline within next few days) spirit match (financial obligation with tight deadline; not literal V2 example which lists bill/rent/report/payment) | **PARTIALLY in-V2-enum** |

**Aggregate (test_v12):** 2 clean-in (garage_open_overnight, friend_hospitalized) + 3 partial-in (license_expires_today, hoa_assessment_vote, margin_account_warning) + 0 borderline-out. Slightly more partial-tilted than test_v11 (3+2+0); aggregate spread across M11a so far at 5+5=10 GTs is 5 clean-in / 5 partial-in / 0 borderline-out — moderately more in-enum-tilted than M10b's combined N=3 (4 clean / 6 partial / 5 borderline-out across 15 GTs). M11a-relevant prediction: V2-3B might land 0.40-0.80 (license + hoa + margin are the at-risk GTs given financial-deadline literal-example mismatch); V2-Opus expected 0.80-1.00.

### test_v13 (5 GTs)

| GT id | regime | V2 category match | classification |
|---|---|---|---|
| counter_offer | voicemail about real-estate counter-offer with 5pm-today deadline, financial decision | clean: cat 3 (financial/deadline obligations) — real-estate financial decision deadline today; cat 4 (personal messages) — voicemail directed personally with agent contact | **IN-V2-enum** |
| interview_confirm | recruiter email confirming scheduled interview, reply-or-lose-slot by EOD | partial: cat 3 (deadline obligation) spirit match (confirm-by-EOD-or-lose-slot is a deadline-with-consequence; not literal V2 example which lists bill/rent/report/payment); cat 4 (personal messages) partial match (recruiter email directed personally) | **PARTIALLY in-V2-enum** |
| book_club_host | notification reminder about hosting book club tomorrow + prep needed | partial: cat 2 (personal schedule changes) spirit match (tomorrow personal-event reminder; not literally a schedule change but a hosting-prep heads-up); cat 5 (external conditions changing planned day) weak match (tomorrow event affects planned day prep) | **PARTIALLY in-V2-enum** |
| figmaster_trial | SaaS trial conversion alert with tight-window pro-seat switch action | partial: cat 3 (financial/deadline obligations) spirit match (trial converts to paid in 25 min = financial-stake action deadline; not literal V2 example); cat 6 (production/on-call alerts) partial match (tech-tool transition affecting team workspace) | **PARTIALLY in-V2-enum** |
| ryobi_warranty | consumer-warranty registration deadline today at midnight, coverage-drop consequence | partial: cat 3 (financial/deadline obligations within next few days) spirit match (consumer warranty obligation deadline tonight; not literal V2 example which lists bill/rent/report/payment) | **PARTIALLY in-V2-enum** |

**Aggregate (test_v13):** 1 clean-in (counter_offer) + 4 partial-in (interview_confirm, book_club_host, figmaster_trial, ryobi_warranty) + 0 borderline-out. Continues the partial-tilt trend observed across M11a: test_v11 (3+2+0), test_v12 (2+3+0), test_v13 (1+4+0) — defense #4 saturation signal as cumulative banned-list grows. Aggregate M11a N=3 (15 GTs): 6 clean-in / 9 partial-in / 0 borderline-out. M11a-relevant prediction: V2-3B might land 0.40-0.80 (partial-in GTs are the at-risk ones given non-literal-V2-example status); V2-Opus expected 0.80-1.00.

### test_v14 (5 GTs)

| GT id | regime | V2 category match | classification |
|---|---|---|---|
| backup_codes_rotating | account-security 2FA backup-code rotation with 25-second action window | clean: cat 1 (urgent safety/security) — account-security alert with imminent invalidation of access credentials | **IN-V2-enum** |
| inspector_walkthrough_advanced | real-estate inspector walkthrough moved up by 2 hours same-day at seller request | clean: cat 2 (personal schedule changes) — appointment time-shift today | **IN-V2-enum** |
| movers_swap_slot | voicemail from movers offering swap of moving-day slot, decision within an hour | clean: cat 2 (personal schedule changes) — schedule swap offer; cat 4 (personal messages/deliveries) — voicemail directed personally with contractor name | **IN-V2-enum** |
| bond_purchase_confirm | Treasury Direct Series I bond purchase confirmation deadline 5pm ET today, rate-locked-in window forfeited if missed | partial: cat 3 (financial/deadline obligations within next few days) spirit match (investment decision deadline with consequence; not literal V2 example which lists bill/rent/report/payment) | **PARTIALLY in-V2-enum** |
| boil_water_zip | public utility boil-water advisory for zip code through tomorrow evening, do not consume tap water | partial: cat 5 (weather/external conditions changing planned day) spirit match (utility advisory affecting daily activities; not literally weather but public-utility external condition); cat 1 (urgent safety/security) partial spirit match (public-health advisory) | **PARTIALLY in-V2-enum** |

**Aggregate (test_v14):** 3 clean-in (backup_codes_rotating, inspector_walkthrough_advanced, movers_swap_slot) + 2 partial-in (bond_purchase_confirm, boil_water_zip) + 0 borderline-out. **Trend reversal** from test_v12 (2+3+0) and test_v13 (1+4+0) partial-tilt — test_v14's mix has more clean-in events (security, schedule change, voicemail-with-schedule-swap). Aggregate M11a N=4 (20 GTs): 9 clean-in / 11 partial-in / 0 borderline-out. M11a-relevant prediction: V2-3B might land 0.60-1.00 (partial-in GTs are the at-risk ones; bond_purchase_confirm + boil_water_zip are the at-risk GTs given non-literal-V2-example status); V2-Opus expected 0.80-1.00.

### test_v15 (5 GTs)

| GT id | regime | V2 category match | classification |
|---|---|---|---|
| skip_level_addition | work-meeting calendar-add with accept/decline/propose options before EOD | clean: cat 2 (personal schedule changes) — calendar invitation with EOD decision deadline | **IN-V2-enum** |
| baby_shower_gift_close | social-event group-gift contribution deadline today, financial chip-in via Venmo | partial: cat 3 (financial/deadline obligations within next few days) spirit match (today-deadline financial contribution; not literal V2 example which lists bill/rent/report/payment) | **PARTIALLY in-V2-enum** |
| visa_autopay_low_balance | Visa autopay tonight, insufficient checking balance, move funds or reverse | clean: cat 3 (financial/deadline obligations within next few days) — bill-payment-due-style content matching V2's literal "bill due" example via autopay reverse-risk framing | **IN-V2-enum** |
| olia_reservation_hold | restaurant reservation auto-cancel in 15 minutes unless confirm | partial: cat 2 (personal schedule changes) spirit match (reservation auto-cancel is a schedule-state change with default-cancel-unless-act mechanism); not literal V2 example which connotes user-initiated changes | **PARTIALLY in-V2-enum** |
| brake_job_approval | voicemail from auto mechanic offering same-day brake job completion with 3pm decision deadline | clean: cat 4 (personal messages/deliveries) — voicemail directed personally from named contractor; cat 3 (financial obligation) partial spirit match ($480 decision) | **IN-V2-enum** |

**Aggregate (test_v15):** 3 clean-in (skip_level_addition, visa_autopay_low_balance, brake_job_approval) + 2 partial-in (baby_shower_gift_close, olia_reservation_hold) + 0 borderline-out. Same shape as test_v14 (3+2+0) and test_v11 (3+2+0).

**Aggregate M11a N=5 final (25 GTs):** 12 clean-in / 13 partial-in / 0 borderline-out. test_v11 (3+2+0), test_v12 (2+3+0), test_v13 (1+4+0), test_v14 (3+2+0), test_v15 (3+2+0). Mixed in/partial spread comparable to M10b combined N=3 (4 clean / 6 partial / 5 borderline-out across 15 GTs) but with materially fewer borderline-out events (0 vs 5) — M11a's GT-regime distribution is more concentrated within V2's literal YES enumeration than M10b's was. M11a-relevant prediction: V2-3B might land 0.50-1.00 across the 5 traces (partial-in GTs are the at-risk ones); V2-Opus expected 0.80-1.00.




## Mechanism notes

(Populated during Commits C1-C5 per accepted trace. One subsection per accepted M11a trace, documenting borderline-theme transparency notes — overlaps that do not rise to a strict banned-theme violation but are documented for paper-level transparency, mirroring M10b's §"Mechanism notes" pattern at runs/18 §"Mechanism notes" lines 391+. Borderline notes are judgment-only per §"Drift-monitoring criterion" rubric line 285 ("mild calls are reported but do not gate any pre-reg threshold") and do not gate audit; the strong-overlap rubric (a tuple-bytewise + b 8-word-verbatim) gates audit mechanically.)

### test_v11 — borderline-theme notes (audit PASS at attempt #2 with transparency)

The audit accepted test_v11's second attempt with five transparent borderline-theme notes (attempt #1 was rejected for structural-parsing per §"Per-attempt drift log" → test_v11 attempt #1; attempt #2 passed strict-letter audit on first read). All five notes are mild overlaps under the §"Drift-monitoring criterion" rubric line 285 ("broad-domain tag overlap, no strong sub-criterion fires") — judgment-only, do not gate. The strong-overlap rubric (a tuple-bytewise + b ≥8-word-verbatim) mechanically PASSED with zero hits across the new trace's 5 GTs vs the 15 prior committed GTs. Documented for paper-level transparency, mirroring M10b's full-disclosure pattern at runs/18 §"Mechanism notes" lines 393-462.

1. **GT `locksmith_buzzer` vs banned themes "pet medical emergency + callback request 10-min auth window" / "family voicemail with airport pickup 15-min window".** All three involve a voicemail-with-tight-callback structural pattern. Domain genuinely distinct (locksmith access vs vet medical vs airport pickup); locksmith vendor-at-door is a new sub-category not present in either banned theme. Documented as mild-overlap because reviewers may push that "voicemail + sub-30s callback" is the load-bearing pattern regardless of domain; the literal banned-theme text refers specifically to vet/family-airport contexts that this GT does not match.

2. **GT `spanish_tutoring_shift` vs banned theme "work meeting time/location change" + banned tuple `(meeting, moved)`.** Strongest of the 5 mild calls under the structural-overlap lens. The content template "Your X session originally at Y has been moved to Z by W" is identical to "your work meeting at Y has been moved to Z" with the noun substituted (tutoring session vs work meeting). The keyword tuple `(tutoring, moved)` shares only its 2nd element with banned `(meeting, moved)` — **NOT a bytewise match** (1st element differs); strong-overlap rubric (a) does not fire. Documented as mild-overlap because the structural template is near-identical to a banned theme; defense is the genuine domain distinction (Spanish tutoring is an educational service, not a work meeting; the 30-minute today-shift is independently realistic for tutoring scheduling) plus the rubric's deliberate choice to make strong-overlap mechanical-bytewise rather than structural (per §"Drift-monitoring criterion" line 287: noun-substitution attacks are mild by rubric-design intent, not strong).

3. **GT `bistro_wallet_holding` vs banned theme "library hold expires" / banned tuple `(library, hold, expires)`.** Both share an item-pickup-with-today-deadline structural pattern. Domain distinct (lost-and-found wallet at restaurant vs library hold). Documented as mild-overlap because reviewers may push that "item-pickup-deadline-today" is the load-bearing pattern; the literal banned-theme text is library-hold-specific.

4. **GT `city_marathon_closures` vs banned theme "parking meter or civil disruption affecting commute".** A planned permitted city marathon closing downtown streets is structurally similar to "civil disruption affecting commute" — the banned theme uses "OR" covering both parking-meter scenarios and broader civil-disruption scenarios, and a marathon affecting commute could plausibly read as the latter. **Closest call of the 5 borderlines** under strict literal-text reading. Defense: "civil disruption" typically connotes hostile/unplanned events (protests, strikes); a planned permitted civic event with published-in-advance street closures is semantically distinct and is a different sub-category of "external conditions affecting commute" than the banned theme's protest/strike examples (banned tuple `(protest, market street)` makes the protest-specific framing explicit). Documented as mild-overlap because the literal banned-theme text could plausibly be read to cover this GT; the audit-step-3 verdict of strict-letter PASS rests on the marathon-not-disruption distinction.

5. **GT `pitch_slides_review_ask` vs banned theme "work deadline tomorrow/today/quarterly" + banned tuple `(deadline, quarterly)`.** Both share a tomorrow-morning-deadline-on-professional-task structural pattern. Domain distinction: this GT is a friend's favor-ask (request for feedback on slides) rather than the user's own work deadline; the keyword tuple `(slides, feedback)` is fully novel and the asker-as-friend-not-employer framing is distinct from the banned theme's "work deadline" framing. Documented as mild-overlap because reviewers may push that "tomorrow-morning deadline on professional work" is the load-bearing pattern; defense is the asker-relationship distinction.

### test_v12 — borderline-theme notes (audit PASS at attempt #1 with transparency)

The audit accepted test_v12's first attempt with five transparent borderline-theme notes. All five are mild overlaps under the §"Drift-monitoring criterion" rubric line 285 ("broad-domain tag overlap, no strong sub-criterion fires") — judgment-only, do not gate. The strong-overlap rubric (a tuple-bytewise + b ≥8-word-verbatim) mechanically PASSED with zero hits across the new trace's 5 GTs vs the 20 prior committed GTs (test_v6/v7/v8/v11). Documented for paper-level transparency, mirroring test_v11's pattern at C1 SHA `2042dc5`.

1. **GT `garage_open_overnight` vs banned themes "fire alarm/safety", "security breach / unauthorized access".** Smart home alert about own garage door left open after sunset — a household-property security-adjacent alert. Domain genuinely distinct from fire-safety alarm or unauthorized-access break-in scenarios; the banned theme "security breach / unauthorized access" connotes an external party gaining unauthorized access, while this GT is the user's own smart-home-state alert (door left open by user/family, no external threat). Documented as mild-overlap because the literal banned-theme text ("fire alarm/safety", "security breach / unauthorized access") could plausibly cover smart-home-security alerts under broad reading; defense rests on the own-property-state vs external-threat distinction.

2. **GT `friend_hospitalized` vs banned theme "ER call" + multiple voicemail-format banned themes ("personal voicemail with hard 6pm-tonight deadline" test_v8, "family voicemail with airport pickup 15-min window" test_v7, "friend's professional-favor request with tomorrow-morning deadline" test_v11).** **STRONGEST CALL of the 5.** The literal "ER call" banned theme covers ER-related medical phone communications; this GT is structurally a friend's voicemail update about a close friend's hospitalization (Mike, chest pains, stable at Memorial). Defense: "ER call" connotes an active emergency phone call (the user being summoned to ER); this GT is an informational voicemail update about a hospitalized friend who is stable, with no active demand on the user. The "voicemail" format is structurally similar to test_v7/v8/v11 voicemail themes but with distinct sub-category (medical update vs deadline/favor/pickup). Documented as mild-overlap because the literal banned-theme text could plausibly be read to cover this GT; the audit-step-3 verdict of strict-letter PASS rests on the active-emergency vs informational-update distinction.

3. **GT `license_expires_today` vs banned theme "passport renewal or visa".** Both are government-issued identity-document renewal deadlines. **Second-strongest call.** Sub-category distinct (state-DMV driver's license vs federal-StateDept passport/visa); different agency, different document type, different renewal cycle. The keyword tuple `(license, expires)` shares "expires" with banned `(passport, expiring)`, `(tax, expires)`, `(library, hold, expires)` — but bytewise different (different first element). Documented as mild-overlap because reviewers may push that "government-document renewal deadline" is the load-bearing pattern; the literal banned-theme text says "passport renewal or visa" specifically (driver's license is neither passport nor visa).

4. **GT `hoa_assessment_vote` vs banned theme "civic obligation; confirm/postpone by tomorrow noon" (test_v7).** Both are governance-vote-with-deadline structural patterns. Sub-category distinct: HOA is private/community-association governance (homeowners' association vote on emergency assessment), not strictly civic in the public-sector sense the banned theme exemplifies (jury-duty-style civic obligation). Documented as mild-overlap because reviewers may construe "civic" broadly to include community governance; defense is the public-sector vs private-association distinction.

5. **GT `margin_account_warning` vs banned themes "financial deadline 17:00 today (mortgage rate lock)" (test_v7) + "online auction ending in 10 min top bidder financial decision" (test_v6).** All three share a tight-window financial-deadline-with-stakes structural pattern. Sub-category distinct: brokerage margin call (forced liquidation if undeposited) vs mortgage rate-lock signing (refinance-rate consequence) vs auction top-bidder (purchase decision) — different financial mechanisms, different consequences, different industry domains. Documented as mild-overlap because the structural template "tight-deadline financial decision with adverse consequence" is shared; literal banned-theme text refers to mortgage and auction specifically.

### test_v13 — borderline-theme notes (audit PASS at attempt #3 with transparency; attempts #1 + #2 rejected)

The audit accepted test_v13's third attempt with five transparent borderline-theme notes after attempts #1 (banned-theme reuse on `frost_advisory_garden`) and #2 (structural-constraint #3 violation on `zoom_link_changed` arithmetic) were rejected. All five borderline-theme notes for the accepted attempt #3 are mild overlaps under the §"Drift-monitoring criterion" rubric line 285 ("broad-domain tag overlap, no strong sub-criterion fires") — judgment-only, do not gate. The strong-overlap rubric (a tuple-bytewise + b ≥8-word-verbatim) mechanically PASSED with zero hits across the new trace's 5 GTs vs the 25 prior committed GTs (test_v6/v7/v8/v11/v12). **Critically: no GT in attempt #3 falls within a literal banned-theme description verbatim** — this is the qualitative improvement that distinguishes attempt #3 from attempts #1 + #2. Documented for paper-level transparency, mirroring test_v11/test_v12 patterns at C1/C2.

1. **GT `counter_offer` vs banned themes "financial deadline 17:00 today (mortgage rate lock)" (test_v7) + "personal voicemail with hard 6pm-tonight deadline" (test_v8).** All three share a voicemail-or-message-with-today's-financial-deadline structural pattern. Sub-categories distinct: real-estate counter-offer-acceptance (this GT) vs mortgage rate-lock-signing (test_v7) vs ambiguous personal-deadline voicemail (test_v8). Different financial mechanisms (counter-offer accept/reject vs rate-lock disclosure signing vs unspecified personal-deadline action). Documented as mild-overlap because the structural template "voicemail + financial-deadline-today" is shared; literal banned-theme text refers to mortgage rate-lock specifically.

2. **GT `interview_confirm` vs banned theme "civic obligation; confirm/postpone by tomorrow noon" (test_v7).** Both share a confirm-by-deadline-or-lose-opportunity structural pattern. Sub-category distinct: jury-duty-style civic obligation (test_v7) vs recruiter-interview confirmation (this GT). Different domains: public-sector civic (jury summons) vs private-sector employment (recruiter). Documented as mild-overlap because the structural template "confirm by [deadline] or [consequence]" is shared; literal banned-theme text says "civic obligation" specifically (recruiter interview is private employment, not civic).

3. **GT `book_club_host` vs banned theme "reminder for tomorrow's vet appointment + prep needed (records, stool sample)" (test_v8).** **Strongest structural call of the 5.** Both share a "reminder for tomorrow's [event] + prep needed" template — near-identical scaffolding. Sub-categories distinct: vet medical appointment off-site (test_v8) vs book club social event at user's place (this GT). Different prep types (vaccination records + stool sample vs snacks + book selection). Different event classes (medical vs social). Documented as mild-overlap because the structural template "tomorrow event reminder + prep heads-up" is near-identical; defense rests on the medical-vs-social sub-category distinction. By the M10b wedding-theme precedent (test_v6 wedding_rsvp + test_v7 wedding_rehearsal accepted as mild with distinct sub-categories), this is the same pattern: shared template, distinct sub-category.

4. **GT `figmaster_trial` vs banned themes "10-min ticket presale window opening with access code" (test_v8) + "online auction ending in 10 min top bidder financial decision" (test_v6).** All three share a tight-window opportunity-or-financial-action structural pattern. Sub-categories distinct: SaaS trial conversion (this GT) vs ticket presale opening (test_v8) vs auction ending (test_v6). Different industry domains: SaaS/B2B tool (Figmaster) vs concert tickets (Phoebe Bridgers) vs consumer auction. Documented as mild-overlap because the structural template "X happens in 10-25 min, action required" is shared; literal banned-theme text refers to ticket presale and auction specifically.

5. **GT `ryobi_warranty` vs banned theme "DMV driver's license renewal deadline today at midnight, legal/regulatory requirement" (test_v12).** **Second strongest structural call.** Both share an "X registration deadline today at midnight, coverage-or-consequence" structural template. Sub-categories distinct: state-DMV driver's license (legal, mandatory) vs RyobiCare circular-saw warranty (consumer, opt-in). Different consequences: cannot legally drive tomorrow (test_v12) vs warranty drops to base 90-day (this GT). Different authority types (government vs consumer-products vendor). Documented as mild-overlap because the structural template is near-identical; defense rests on the legal-vs-consumer sub-category distinction.

### test_v14 — borderline-theme notes (audit PASS at attempt #1 with transparency)

The audit accepted test_v14's first attempt with five transparent borderline-theme notes. All five are mild overlaps under the §"Drift-monitoring criterion" rubric line 285 ("broad-domain tag overlap, no strong sub-criterion fires") — judgment-only, do not gate. The strong-overlap rubric (a tuple-bytewise + b ≥8-word-verbatim) mechanically PASSED with zero hits across the new trace's 5 GTs vs the 30 prior committed GTs (test_v6/v7/v8/v11/v12/v13). **No GT in attempt #1 falls within a literal banned-theme description verbatim** — same qualitative profile as test_v11 attempt #2, test_v12 attempt #1, and test_v13 attempt #3 (all M11a-accepted traces share this strict-letter clean-audit pattern). Documented for paper-level transparency.

1. **GT `backup_codes_rotating` vs banned themes "10-min ticket presale window opening with access code" (test_v8) + "SaaS trial conversion alert with tight-window pro-seat switch action" (test_v13).** All three share a tight-window-action-required structural pattern. Sub-categories genuinely distinct: account-security 2FA rotation (this GT) vs ticket presale opening (test_v8) vs SaaS trial conversion (test_v13). Different domains: account-security infrastructure vs consumer ticketing vs B2B SaaS. Documented as mild-overlap because the structural template "X happens in seconds-to-minutes, action required" is shared; literal banned-theme text refers to presale/trial specifically.

2. **GT `inspector_walkthrough_advanced` vs banned theme "tutoring session time-shift today (+30 min), personal-services schedule change" (test_v11) + M10b "work meeting time/location change".** Both test_v11 theme and M10b theme cover same-day appointment time-shift patterns. Sub-categories distinct: real-estate inspector walkthrough (this GT) vs Spanish tutoring session (test_v11) vs work meeting (M10b). Different professional domains: real-estate service vs educational service vs work. The keyword tuple `(walkthrough, inspector)` is fully novel and shares no element with banned tuples `(tutoring, moved)` or `(meeting, moved)`. Documented as mild-overlap because the structural template "today's [scheduled service] moved [direction]" is shared; literal banned-theme text refers to work meeting and tutoring specifically.

3. **GT `movers_swap_slot` vs banned themes "plumber or appliance-install reschedule" (M10b) + "personal voicemail with hard 6pm-tonight deadline" (test_v8) + "friend's professional-favor request with tomorrow-morning deadline" (test_v11) + "voicemail about real-estate counter-offer with 5pm-today deadline" (test_v13).** All share a voicemail-from-contractor-or-personal-contact-with-tight-decision-window structural pattern. Sub-categories distinct: movers offering proactive slot swap (this GT) vs plumber reschedule (M10b) vs hard-deadline personal voicemail (test_v8) vs friend-favor (test_v11) vs real-estate counter-offer (test_v13). Different mechanisms (proactive offer vs reschedule vs deadline notification vs favor ask vs counter-offer). Documented as mild-overlap because the structural template "voicemail + tight-window decision" is shared; literal banned-theme text refers to specific contractor types and scenarios distinct from movers offering slot swaps.

4. **GT `bond_purchase_confirm` vs banned theme "financial deadline 17:00 today (mortgage rate lock)" (test_v7).** **Strongest structural call of the 5.** Both share a 5pm-today financial-deadline-or-forfeit structural pattern, AND both feature "rate locked-in" terminology (test_v7's banned theme literal text says "(mortgage rate lock)"; this GT's content includes "the rate locked-in window will be forfeited"). Sub-categories distinct: Treasury Direct Series I bond purchase confirmation (this GT) vs mortgage rate-lock signing (test_v7). Different financial mechanisms: investment-purchase confirmation vs home-loan rate-lock disclosure. Different industries: federal-government savings bonds vs private-sector mortgage broker. Mechanical drift rubric (b) ≥8-word verbatim check PASSED at 0 hits — no consecutive 8-word phrase shared between this GT's content and test_v7's content. The shared "rate locked-in" + "5pm/17:00 today" + "forfeit if missed" structural template is the load-bearing similarity. Documented as mild-overlap because the rubric explicitly classifies broad-domain template overlap without bytewise-mechanical hit as mild; defense rests on Treasury-bond-vs-mortgage-rate-lock sub-category distinction. Also overlaps test_v13's "voicemail about real-estate counter-offer with 5pm-today deadline" theme and test_v12's "brokerage margin call requiring 2-hour deposit" theme — all 5pm-today financial-decision-or-forfeit structural patterns.

5. **GT `boil_water_zip` vs banned theme "M4.2 earthquake alert with imminent shaking instruction" (test_v8).** Both are world_event-kind public-utility-style hazard advisories with action instructions. Sub-categories distinct: water-quality (this GT, boil-water for at least one minute) vs seismic (test_v8, Drop-cover-hold-on). Different mechanisms (water-utility advisory through tomorrow evening vs imminent seismic shaking). Different time-scales (multi-day advisory vs imminent <1-min action). Also borderline structural overlap with M10b banned themes "weather alert/forecast/precipitation" (different mechanism: water-quality vs meteorological) and "planned building electrical / power shutoff" (different utility: water vs electrical). Documented as mild-overlap because the structural template "world_event public-safety advisory with action instruction" is shared with test_v8; defense rests on the seismic-vs-water-quality sub-category distinction.

### test_v15 — borderline-theme notes (audit PASS at attempt #2 with transparency; attempt #1 rejected)

The audit accepted test_v15's second attempt with five transparent borderline-theme notes after attempt #1 was rejected on hard structural constraint #3 (`thesis_advisor_swap` sim_time+window=1140>1000). All five borderline-theme notes for the accepted attempt #2 are mild overlaps under the §"Drift-monitoring criterion" rubric line 285 ("broad-domain tag overlap, no strong sub-criterion fires") — judgment-only, do not gate. The strong-overlap rubric (a tuple-bytewise + b ≥8-word-verbatim) mechanically PASSED with zero hits across the new trace's 5 GTs vs the 35 prior committed GTs (test_v6/v7/v8/v11/v12/v13/v14). **No GT falls within a literal banned-theme description verbatim** — same qualitative profile as test_v11 attempt #2, test_v12 attempt #1, test_v13 attempt #3, test_v14 attempt #1 (all M11a-accepted traces share this strict-letter clean-audit pattern). Documented for paper-level transparency.

1. **GT `skip_level_addition` vs banned themes "work meeting time/location change" (M10b) + "tutoring session time-shift today" (test_v11) + "real-estate inspector walkthrough moved up by 2 hours" (test_v14).** All share work/personal-schedule structural patterns. Sub-category distinct: ADDING a new meeting (this GT — Skip-level 1:1 newly added to calendar, accept/decline/propose-new-time response options) vs CHANGING/SHIFTING an existing meeting (test_v11 tutoring-shift, test_v14 inspector-walkthrough-moved-up, M10b meeting_moved). The add-vs-change semantic distinction is the load-bearing differentiator; literal banned-theme text refers to time/location *change* of existing meetings, not new additions.

2. **GT `baby_shower_gift_close` vs banned theme "wedding RSVP deadline tonight at midnight + meal selection" (test_v6).** Both share a social-event group-contribution-or-RSVP-with-today-deadline structural pattern. Sub-category distinct: baby shower group gift collection (this GT) vs wedding RSVP with meal selection (test_v6). Different social-event types (baby shower vs wedding), different mechanisms (financial Venmo chip-in vs RSVP attendance confirmation), different time-windows (11:30 today midmorning vs midnight tonight). Documented as mild-overlap because the structural template "social-event today-deadline action" is shared; literal banned-theme text refers to wedding RSVP specifically.

3. **GT `visa_autopay_low_balance` vs banned theme "brokerage margin call requiring 2-hour deposit to avoid forced liquidation" (test_v12) + M10b "rent due".** **Strong structural call.** Both test_v12 and this GT share an insufficient-funds-action-or-adverse-financial-outcome pattern. Sub-category distinct: consumer credit-card autopay reverse-prevention (this GT — Visa autopay $843 scheduled, checking balance $612, move funds or reverse) vs brokerage margin call forced-liquidation-prevention (test_v12 — margin account $4,200 deposit needed within 2 hours). Different industries (consumer credit vs brokerage); different consequence severity (payment reverse + late fee/credit-score-hit vs forced liquidation of held positions). The keyword tuple `(auto-payment, balance)` is fully novel and shares no element with banned `(margin, deposit)`. Documented as mild-overlap because the structural template "insufficient funds + action-or-consequence" is shared; literal banned-theme text refers to brokerage margin specifically.

4. **GT `olia_reservation_hold` vs banned themes "10-min ticket presale window opening with access code" (test_v8) + "SaaS trial conversion alert with tight-window pro-seat switch action" (test_v13) + "account-security 2FA backup-code rotation with 25-second action window" (test_v14).** All share a tight-window default-action-unless-user-acts structural pattern (auto-cancel-unless-confirm). Sub-categories distinct: restaurant reservation auto-cancel (this GT) vs ticket presale (test_v8) vs SaaS trial conversion (test_v13) vs 2FA rotation (test_v14). Different industries; different defaults (presale opens vs trial converts vs codes invalidate vs reservation cancels). Documented as mild-overlap because the structural template "X happens automatically in N minutes/seconds unless user takes action Y" is shared; literal banned-theme text refers to specific industries and mechanisms distinct from restaurant-reservation auto-cancel.

5. **GT `brake_job_approval` vs banned theme "voicemail from movers offering swap of moving-day slot, decision within an hour" (test_v14) + M10b "plumber or appliance-install reschedule".** **Strong structural call.** Both test_v14 and this GT share a phone_message-from-contractor-with-decision-deadline-and-same-day-vs-fallback-option pattern. Sub-category distinct: auto mechanic offering same-day brake job vs next-Tuesday fallback (this GT — Sal at Pinewood Auto, $480 decision before 3 PM) vs movers offering 7 AM swap vs original 2 PM (test_v14 — Hiroshi at City Movers, decision in next hour). Different contractor industries (auto repair vs moving services); different deadline scales (3 PM vs in-an-hour); different fallback consequences (push to next Tuesday vs lose to someone else). The keyword tuple `(approve, brake)` is fully novel and shares no element with banned `(movers, slot)` or `(plumber, reschedule)`. Documented as mild-overlap because the structural template "phone_message contractor + same-day vs delayed decision" is shared; literal banned-theme text refers to movers and plumber/appliance-install specifically.

## Banned-list timeline

Per-trace banned-list state at the moment each fresh-session authoring prompt was sent. The fresh session for trace N+1 sees the post-N extended state. Per pre-reg §"Authoring protocol per trace" iterative-extension rule: after each accepted Commit C(N), append the just-accepted trace's 9 IDs + 5 GT-regime themes (verbatim from §"GT-regime classification" regime column) + 5 GT keyword tuples before the next fresh session opens. Section header added at C1 (the first commit at which timeline content exists); pre-reg reference at line 62.

### State at C1 fresh-session prompts (test_v11 attempts #1 and #2)

= **M11a Commit A starting state (82 IDs / 47 themes / 46 tuples)**, verbatim from §"Banned lists for M11a (starting state at Commit A)". No iterative extension applied — test_v11 is M11a's first trace; the C1 fresh session for both attempt #1 and attempt #2 saw the Commit-A starting state unchanged. (Attempt #1 was rejected for structural-parsing, not banned-list-pressure; rejected attempts do not extend the banned list per §"Banned-list growth trajectory" line 131.)

### State at C2 fresh-session prompt (test_v12; post-C1 extension)

= **post-C1 extended state (91 IDs / 52 themes / 51 tuples)**, applying the iterative-extension rule with test_v11's accepted-attempt-#2 contributions:

**Banned IDs (+9 from accepted test_v11; full new list 82 + 9 = 91):**
```
locksmith_buzzer, spanish_tutoring_shift, bistro_wallet_holding,
city_marathon_closures, pitch_slides_review_ask,
chess_puzzle_nudge, printworks_payment_ack, trivia_league_round, sam_article_forward
```

**Banned content themes (+5 from test_v11 GT-regime classification regime column, verbatim; full new list 47 + 5 = 52):**
- vendor on-site at building entry, callback request to grant access, tight window
- tutoring session time-shift today (+30 min), personal-services schedule change
- lost-item recovery deadline today, tonight's-close pickup window
- civic-event affecting tomorrow's commute (planned street closures)
- friend's professional-favor request with tomorrow-morning deadline

**Banned keyword tuples (+5 from accepted test_v11 GT keywords; full new list 46 + 5 = 51):**
```
(locksmith, buzzer), (tutoring, moved), (wallet, pickup), (marathon, closes), (slides, feedback)
```

### State at C3 fresh-session prompt (test_v13; post-C2 extension)

= **post-C2 extended state (100 IDs / 57 themes / 56 tuples)**, applying the iterative-extension rule with test_v12's accepted-attempt-#1 contributions:

**Banned IDs (+9 from accepted test_v12; full new list 91 + 9 = 100):**
```
garage_open_overnight, friend_hospitalized, license_expires_today,
hoa_assessment_vote, margin_account_warning,
screen_time_report, photo_backup_complete, grocer_back_in_stock, calendar_yoga_suggest
```

**Banned content themes (+5 from test_v12 GT-regime classification regime column, verbatim; full new list 52 + 5 = 57):**
- smart-home alert: garage door left open after sunset, household-security check-on with tight window
- voicemail update about close friend hospitalized for chest pains, informational (no immediate-action demand)
- DMV driver's license renewal deadline today at midnight, legal/regulatory requirement
- HOA emergency assessment vote with today-deadline financial-obligation decision
- brokerage margin call requiring 2-hour deposit to avoid forced liquidation

**Banned keyword tuples (+5 from accepted test_v12 GT keywords; full new list 51 + 5 = 56):**
```
(garage, open), (hospitalized, mike), (license, expires), (hoa, vote), (margin, deposit)
```

### State at C4 fresh-session prompt (test_v14; post-C3 extension)

= **post-C3 extended state (109 IDs / 62 themes / 61 tuples)**, applying the iterative-extension rule with test_v13's accepted-attempt-#3 contributions (rejected attempts #1 + #2 do not extend per pre-reg §"Banned-list growth trajectory" line 131):

**Banned IDs (+9 from accepted test_v13; full new list 100 + 9 = 109):**
```
counter_offer, interview_confirm, book_club_host, figmaster_trial, ryobi_warranty,
meditation_nudge, cantina_review, phone_battery_low, calendar_week_digest
```

**Banned content themes (+5 from test_v13 GT-regime classification regime column, verbatim; full new list 57 + 5 = 62):**
- voicemail about real-estate counter-offer with 5pm-today deadline, financial decision
- recruiter email confirming scheduled interview, reply-or-lose-slot by EOD
- notification reminder about hosting book club tomorrow + prep needed
- SaaS trial conversion alert with tight-window pro-seat switch action
- consumer-warranty registration deadline today at midnight, coverage-drop consequence

**Banned keyword tuples (+5 from accepted test_v13 GT keywords; full new list 56 + 5 = 61):**
```
(counter-offer, agent), (interview, reply), (book club, host), (trial, converts), (warranty, registered)
```

### State at C5 fresh-session prompt (test_v15; post-C4 extension)

= **post-C4 extended state (118 IDs / 67 themes / 66 tuples)**, applying the iterative-extension rule with test_v14's accepted-attempt-#1 contributions:

**Banned IDs (+9 from accepted test_v14; full new list 109 + 9 = 118):**
```
backup_codes_rotating, inspector_walkthrough_advanced, movers_swap_slot,
bond_purchase_confirm, boil_water_zip,
beanwise_promo_20pct, sticker_packs_added, editor_focus_tip, design_weekly_digest
```

**Banned content themes (+5 from test_v14 GT-regime classification regime column, verbatim; full new list 62 + 5 = 67):**
- account-security 2FA backup-code rotation with 25-second action window
- real-estate inspector walkthrough moved up by 2 hours same-day at seller request
- voicemail from movers offering swap of moving-day slot, decision within an hour
- Treasury Direct Series I bond purchase confirmation deadline 5pm ET today, rate-locked-in window forfeited if missed
- public utility boil-water advisory for zip code through tomorrow evening, do not consume tap water

**Banned keyword tuples (+5 from accepted test_v14 GT keywords; full new list 61 + 5 = 66):**
```
(backup, codes), (walkthrough, inspector), (movers, slot), (bond, confirmation), (boil-water, tap)
```

### State at end-of-M11a (post-C5; final cumulative banned-list state)

= **post-C5 extended state (127 IDs / 72 themes / 71 tuples)**, applying the iterative-extension rule with test_v15's accepted-attempt-#2 contributions. **This matches the pre-reg's predicted end-of-M11a banned-list size verbatim** (§"Banned-list growth trajectory" line 121: "If all 5 M11a traces accept on first attempt (each accepted trace adds 9 IDs + 5 themes + 5 keyword tuples)... ends at 127 IDs / 72 themes / 71 tuples"). The actual trajectory hit this target despite test_v11, test_v13, and test_v15 needing multiple attempts (9 total fresh-session attempts to land 5 accepted traces); rejected attempts do not contribute to extension per pre-reg line 131, so the final size is independent of attempt count.

**Banned IDs (+9 from accepted test_v15; full new list 118 + 9 = 127):**
```
skip_level_addition, baby_shower_gift_close, visa_autopay_low_balance,
olia_reservation_hold, brake_job_approval,
utility_usage_summary, coffee_subscription_promo, streaming_new_releases, smart_speaker_firmware
```

**Banned content themes (+5 from test_v15 GT-regime classification regime column, verbatim; full new list 67 + 5 = 72):**
- work-meeting calendar-add with accept/decline/propose options before EOD
- social-event group-gift contribution deadline today, financial chip-in via Venmo
- Visa autopay tonight, insufficient checking balance, move funds or reverse
- restaurant reservation auto-cancel in 15 minutes unless confirm
- voicemail from auto mechanic offering same-day brake job completion with 3pm decision deadline

**Banned keyword tuples (+5 from accepted test_v15 GT keywords; full new list 66 + 5 = 71):**
```
(1:1, skip-level), (baby shower, collection), (auto-payment, balance), (auto-cancel, reservation), (approve, brake)
```

**M11a authoring phase closed at C5.** No further banned-list extensions during M11a; the next protocol action is Commit D (the 20-cell harness eval across test_v11/v12/v13/v14/v15) per pre-reg §"Five-commit protocol" line 151. The post-C5 state above is the M11a-final banned-list snapshot; any M11a-extension scope work (N=20+, self-restate pre-flight gate, etc.) would inherit this 127/72/71 state.

## Per-trace authoring prompts (verbatim, SHA256-attested)

The pre-reg at line 60 references this content as the operationalization of "the prompt for each accepted trace is exactly reproducible." Prompts are preserved verbatim in Claude Code's session transcript JSONL files at `~/.claude/projects/-Users-patrick-gergen-Pictures/<sessionId>.jsonl`; the JSONL filesystem mtime + the per-message ISO timestamps pre-date this backfill commit by hours, providing tamper-resistance against the hostile-reviewer attack "how do I trust the retrieval pipeline?". Each subsection pastes the verbatim user message that opened the fresh session and includes a SHA256 of the byte sequence for cross-attestation.

**This is a post-data documentation correction, not a data correction.** The prompt artifact is byte-identical to what was sent at the fresh session; only its storage location is being moved (from Claude Code's transcript store into the repo). The original prompts existed at the documented JSONL paths before this commit landed; backfill does not modify any pre-reg parameters, trace data, banned-list state, or audit verdicts. The C1 commit at SHA `2042dc5` already documented the trace + audit + drift-log entries; this backfill closes the prompt-storage gap that section §"Banned-list timeline" line 60 referenced but never operationalized.

**Forward discipline (C2-C5):** each per-trace authoring prompt is to be committed alongside its trace at the same C-commit, not backfilled. C1 is the only backfill case; C2 onward will land prompts at their natural C-commit time.

### test_v11 (attempts #1 and #2 used byte-identical prompt)

- **SHA256:** `d4fa393225a0e710b4d8c8d13ad078d8940cc51dc46456e021a2712d7ddba3ec`
- **Length:** 11787 chars
- **Attempt #1 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/9c2745a1-ad7e-44ac-8046-f7a87c8a6d0c.jsonl`, first authoring user-message at message index 7, timestamp `2026-05-08T16:27:47.416Z` UTC (= 18:27 CEST)
- **Attempt #2 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/4e906d63-41ca-40b8-a193-e56fba4eeeae.jsonl`, first authoring user-message at message index 5, timestamp `2026-05-08T17:17:29.311Z` UTC (= 19:17 CEST; user-reported 19:19 — within 2-min log/local clock variance)
- **Byte-identical between attempts:** confirmed (SHA256 match across both transcripts) — protocol-compliant "no prompt edits between retries" per pre-reg §"Authoring protocol per trace"
- **Reproduction:** `python3 -c "import json,hashlib,sys; d=[json.loads(l) for l in open(sys.argv[1])]; m=[x for x in d if x.get('type')=='user' and 'You are authoring' in str(x.get('message',{}).get('content',''))][0]; c=m['message']['content']; t=' '.join(x.get('text','') for x in c) if isinstance(c,list) else c; print(hashlib.sha256(t.encode()).hexdigest())" <transcript-path>` — should match the SHA256 above for either transcript path.

````text
You are authoring one Python function that returns a `Trace` object. This is a held-out    
  evaluation trace for a project you have no other context about. Author it single-shot; do  
  not ask clarifying questions, do not iterate, do not explain your choices.                 
                                                                                             
  **Schema** (from `sandbox/event_trace.py`):                                                
                                                                                             
  ```python                                                                                  
  from dataclasses import dataclass                                                          
  from sandbox.world import Event                                                            
                                                                                             
  @dataclass(frozen=True)                                                                    
  class GroundTruthEvent:                                                                    
      event: Event                                                                           
      proaction_window_s: float
      keywords: tuple[str, ...]                                                              
                               
  @dataclass(frozen=True)                                                                    
  class Trace:           
      name: str                                                                              
      events: list[Event]
      ground_truth: list[GroundTruthEvent]
      briefing: str | None = None                                                            
      intents: tuple[str, ...] = ()
                                                                                             
  Event has fields id: str, kind: str, sim_time: float, content: str.                        
                                                                                             
  Syntactic template (one unrelated example for style only — do not reuse its ids, content,  
  or themes):                                                                                
                                                                                             
  def dev_trace_v1() -> Trace:
      gts = [                                                                                
          _gt(
              Event(id="flight_delay", kind="email", sim_time=10.0,                          
                    content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New
   departure: 14:30."),                                                                      
              window_s=300.0, keywords=("flight", "delay"),
          ),                                                                                 
          _gt(    
              Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,               
                    content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),  
              window_s=300.0, keywords=("meeting", "moved"),                                 
          ),                                                                                 
          _gt(                                                                               
              Event(id="weather_alert", kind="world_event", sim_time=120.0,
                    content="Weather alert: heavy rain expected tomorrow morning; expect     
  travel delays."),                                                                          
              window_s=300.0, keywords=("weather", "rain"),                                  
          ),                                                                                 
          _gt(    
              Event(id="deadline", kind="email", sim_time=300.0,
                    content="Reminder: Quarterly Report deadline is in 24 hours."),          
              window_s=600.0, keywords=("deadline", "quarterly"),                            
          ),                                                                                 
          _gt(                                                                               
              Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
                    content="Your dentist appointment today at 16:00 has been cancelled."),  
              window_s=300.0, keywords=("dentist", "cancelled"),                             
          ),                                                                                 
      ]                                                                                      
      return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)
                                                                                             
  _gt is a local helper equivalent to GroundTruthEvent(event=event,                          
  proaction_window_s=window_s, keywords=keywords); you may use it or construct               
  GroundTruthEvent directly.                                                                 
                  
  Structural requirements (hard constraints; violating any auto-rejects):                    
   
  - name = "test_v11".                                                                       
  - Exactly 5 GroundTruthEvents and exactly 4 distractor Events (mixed into events list,
  sorted by sim_time).                                                                       
  - All sim_time values in [0, 1000]; for every GT, gt.event.sim_time + gt.proaction_window_s
   ≤ 1000.                                                                                   
  - At least 3 distinct kind values across the 5 GTs. Allowed kinds: email, calendar_update,
  notification, alert, phone_message, world_event.                                           
  - At least one GT with proaction_window_s ≤ 30.
  - At least one GT with proaction_window_s ≥ 300.                                           
  - Keyword/content alignment: for every GroundTruthEvent gt, every string kw in gt.keywords 
  must satisfy kw.lower() in gt.event.content.lower(). Check is purely substring-based — if  
  the keyword's characters don't literally appear in the content, it fails.                  
  - Briefing: 2–4 first-person sentences describing the day's setting.                       
  - Intents: tuple of exactly 5 short phrases.                                               
  - Distractors are plausible routine / system noise a reasonable person would NOT want
  surfaced.                                                                                  
  - GTs are human-interpretable on content alone as warranting proaction.
                                                                                             
  Banned event ids (collision auto-rejects):
  flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm,          
  news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival,     
  doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert,
   promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call,            
  security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry, 
  prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule, spotify_weekly,
   app_version_note, distant_birthday, photo_likes, parking_meter_oak, cover_standup_request,
   gym_class_cancelled, library_hold_expiring, protest_commute_route, linkedin_connections,
  github_repo_star, designgrid_renewal, calendar_feature_tip, babysitter_sick, rail_strike,
  keynote_slot, card_fraud, tax_extension, icloud_storage, ebook_receipt, bank_survey,
  podcast_charge, vet_emergency, concert_swap, elevator_outage, auction_ending, wedding_rsvp,
   reddit_digest, steam_sale, bank_statement, twitter_followers, sister_pickup,
  mortgage_rate_lock, jury_duty, airbnb_cancelled, wedding_rehearsal, poll_civic_reminder,
  recipe_app_tip, loyalty_points_summary, podcast_episode_drop, vet_luna_tomorrow,
  earthquake_local, mom_birthday_heads_up, bridgers_presale_window,
  photographer_voicemail_jen, soundcloud_app_update, stitches_loyalty_statement,
  strava_new_follower, reading_streak_47.

  Banned content themes (semantic, not just string match):
  fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor
  callback, production / server outage, rent due, school pickup, quarterly report, board     
  meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert,
   marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or 
  visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned
  building electrical / power shutoff, plumber or appliance-install reschedule, parking meter
   expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or
  fitness class cancellation for facility maintenance, library hold expiring today, protest
  or civil disruption affecting commute, babysitter cancellation / evening childcare
  emergency, rail strike or labor-action transit disruption, conference keynote /
  speaking-slot schedule change, credit card fraud or consumer financial fraud alert, tax
  extension or accountant-flagged tax-filing deadline, pet medical emergency + callback
  request 10-min auth window, friend social ticket-swap with hard 5pm deadline, building
  elevator emergency-cable-repair service disruption, online auction ending in 10 min top
  bidder financial decision, wedding RSVP deadline tonight at midnight + meal selection,
  family voicemail with airport pickup 15-min window, financial deadline 17:00 today
  (mortgage rate lock), civic obligation; confirm/postpone by tomorrow noon, travel
  reservation cancellation for next weekend, family event rescheduled Sat 12:00 → Fri 18:00,
  personal voicemail with hard 6pm-tonight deadline, M4.2 earthquake alert with imminent
  shaking instruction, 10-min ticket presale window opening with access code, reminder for
  tomorrow's vet appointment + prep needed (records, stool sample), proactive heads-up for
  mother's birthday tomorrow + history of forgetting.

  Banned keyword tuples (avoid reusing any tuple as a GT's keywords field):                  
  (flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, 
  cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert),      
  (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), 
  (hospital, mother), (security, unauthorized), (passport, expiring), (prescription, refill),
   (recall, airbag), (power, shutoff), (plumber, reschedule), (parking, meter, expires), 
  (standup, vacation), (gym, maintenance), (library, hold, expires), (protest, market
  street), (babysit, tonight), (strike, rail), (keynote, moved), (suspicious, charge), (tax,
  expires), (vet, surgery), (concert, swap), (elevator, "out of service"), (auction, ending),
   (wedding, rsvp), (sister, airport), (mortgage, "rate lock"), (jury, duty), (airbnb,
  cancelled), (wedding, rehearsal), (vet, luna), (earthquake, shaking), (mother, birthday),
  (presale, tickets), (photographer, engagement).

  Output: one Python function def test_trace_v11() -> Trace: in the style of the template,   
  followed by a single line adding "test_v11": test_trace_v11 to the get_trace registry.
  Return the code in a single fenced Python block. Do not explain.
````

### test_v12 (single attempt; PASS at attempt #1)

- **Raw SHA256 (as-pasted into fresh session):** `a626f6110d16d1f21fe611712ed6ed8252404c8cb79f2a3a5854712a50b84e4f`
- **Length (as-pasted):** 18719 chars
- **Whitespace-normalized SHA256:** `637151c6091d9bc9348f0a87f961e4461d87b876157e97ab50ce8e9759e01201` — used as the protocol-equivalence check between this prompt and the mechanically-generated C2 prompt SHA `39068ab7daa0db40ea773c814bdb1d2f9e4b1169033d8ff5cced36fe2eab228e` (12,449 chars). Normalization rule: collapse all whitespace runs (`\s+`) to single space, strip; mirrors how Opus 4.7 tokenizes whitespace.
- **Transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/da1af815-472f-4efe-97c5-2f39a3991611.jsonl`, first authoring user-message at message index 5, timestamp `2026-05-09T06:41:43.212Z` UTC (= 08:41 CEST)
- **Reproduction (raw-SHA):** `python3 -c "import json,hashlib,sys; d=[json.loads(l) for l in open(sys.argv[1])]; m=[x for x in d if x.get('type')=='user' and 'You are authoring' in str(x.get('message',{}).get('content',''))][0]; c=m['message']['content']; t=' '.join(x.get('text','') for x in c) if isinstance(c,list) else c; print(hashlib.sha256(t.encode()).hexdigest())" <transcript-path>` — yields the raw SHA above.

**Whitespace-only paste artifact (documented for transparency, not a content drift):** The expected mechanically-generated C2 prompt (SHA `39068ab7daa0db40ea773c814bdb1d2f9e4b1169033d8ff5cced36fe2eab228e`, 12,449 chars) was an extension of C1 with `test_v11` → `test_v12` substitution and the iterative-extension rule's 9 IDs / 5 themes / 5 tuples appended. The actual fresh-session prompt is byte-different (18,719 chars; 4-space indent vs C1's 2-space; extra blank lines) due to the user pasting from a markdown fenced code block, which the terminal re-rendered with doubled indentation. **Whitespace-normalized SHA matches exactly between actual-and-expected**, and structural markers (91 banned IDs with zero set diff; 51 banned tuples; identical test_v12 / banned-list-anchor-ID counts) verify content equivalence. Forward fix established for C3-C5: prompts will be supplied as a file path the user can `cat` to clipboard rather than pasting rendered markdown, eliminating the indent-doubling artifact.

````text
You are authoring one Python function that returns a `Trace` object. This is a held-out    
    evaluation trace for a project you have no other context about. Author it single-shot; do
                                                                                             
    not ask clarifying questions, do not iterate, do not explain your choices.
                                                                                             
                                                                                             
                                                                                             
    **Schema** (from `sandbox/event_trace.py`):                                              
                                                                                             
                  
                                                                                             
    ```python     

    from dataclasses import dataclass         
                                          
    from sandbox.world import Event
                                                                                             
                                              
                                                                                             
    @dataclass(frozen=True)
                                                                                             
    class GroundTruthEvent:                   
                                                                                             
        event: Event
                                                                                             
        proaction_window_s: float             
        keywords: tuple[str, ...]                                                            
                  
                                                                                             
    @dataclass(frozen=True)               
                                                                                             
    class Trace:                                                                             
        name: str
                                                                                             
        events: list[Event]                   
        ground_truth: list[GroundTruthEvent]
        briefing: str | None = None
                                                                                             
        intents: tuple[str, ...] = ()     
                                                                                             
                                                                                             
    Event has fields id: str, kind: str, sim_time: float, content: str.
                                                                                             
                                                                                             
                                          
    Syntactic template (one unrelated example for style only — do not reuse its ids, content,
                                                                                             
    or themes):
                                                                                             
                                              
                                          
    def dev_trace_v1() -> Trace:
        gts = [                                                                              
                                              
            _gt(                                                                             
                Event(id="flight_delay", kind="email", sim_time=10.0,
                                                                                             
                      content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours.
  New                                                                                        
     departure: 14:30."),                                                                    
                                                                                             
                window_s=300.0, keywords=("flight", "delay"),                                
            ),                                                                               
                                                                                             
            _gt(                                                                             
                Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,             
                                                                                             
                      content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),
                                          
                window_s=300.0, keywords=("meeting", "moved"),                               
                                                                                             
            ),                                                                               
                                                                                             
            _gt(  
                                                                                             
                Event(id="weather_alert", kind="world_event", sim_time=120.0,
                      content="Weather alert: heavy rain expected tomorrow morning; expect
                                              
    travel delays."),                                                                        
                                          
                window_s=300.0, keywords=("weather", "rain"),                                
                                                                                             
            ),                                                                               
                                                                                             
            _gt(                              
                Event(id="deadline", kind="email", sim_time=300.0,
                      content="Reminder: Quarterly Report deadline is in 24 hours."),
                                                                                             
                window_s=600.0, keywords=("deadline", "quarterly"),
                                                                                             
            ),                                                                               
                                          
            _gt(                                                                             
                                                                                             
                Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
                      content="Your dentist appointment today at 16:00 has been cancelled."),
                                              
                window_s=300.0, keywords=("dentist", "cancelled"),
                                          
            ),                                                                               
                                                                                             
        ]                                                                                    
                                                                                             
        return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)
                                          
                                              
    _gt is a local helper equivalent to GroundTruthEvent(event=event,                        
   
    proaction_window_s=window_s, keywords=keywords); you may use it or construct             
                                          
    GroundTruthEvent directly.                                                               
                                                                                             
                                              
    Structural requirements (hard constraints; violating any auto-rejects):                  
                  
                                                                                             
    - name = "test_v12".                  
                                                                                             
    - Exactly 5 GroundTruthEvents and exactly 4 distractor Events (mixed into events list,   
    sorted by sim_time).                  
                                                                                             
    - All sim_time values in [0, 1000]; for every GT, gt.event.sim_time +                    
  gt.proaction_window_s                   
     ≤ 1000.                                                                                 
                                                                                             
    - At least 3 distinct kind values across the 5 GTs. Allowed kinds: email,                
  calendar_update,                                                                           
    notification, alert, phone_message, world_event.
                                                                                             
    - At least one GT with proaction_window_s ≤ 30.
    - At least one GT with proaction_window_s ≥ 300.                                         
                                                                                             
    - Keyword/content alignment: for every GroundTruthEvent gt, every string kw in           
  gt.keywords                                                                                
    must satisfy kw.lower() in gt.event.content.lower(). Check is purely substring-based — if
                                                                                             
    the keyword's characters don't literally appear in the content, it fails.                
                                                                                             
    - Briefing: 2–4 first-person sentences describing the day's setting.                     
                                                                                             
    - Intents: tuple of exactly 5 short phrases.                                             
                                                                                             
    - Distractors are plausible routine / system noise a reasonable person would NOT want
    surfaced.                                                                                
                  
    - GTs are human-interpretable on content alone as warranting proaction.                  
                                          
                                                                                             
    Banned event ids (collision auto-rejects):                                               
    flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm,
                                                                                             
    news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival,
                                                                                             
    doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite,
  calendar_advert,                                                                           
     promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call,
                                                                                             
    security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry,
    prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule,              
  spotify_weekly,                                                                            
     app_version_note, distant_birthday, photo_likes, parking_meter_oak,                     
  cover_standup_request,                                                                     
     gym_class_cancelled, library_hold_expiring, protest_commute_route, linkedin_connections,
    github_repo_star, designgrid_renewal, calendar_feature_tip, babysitter_sick, rail_strike,
    keynote_slot, card_fraud, tax_extension, icloud_storage, ebook_receipt, bank_survey,     
    podcast_charge, vet_emergency, concert_swap, elevator_outage, auction_ending,
  wedding_rsvp,                                                                              
     reddit_digest, steam_sale, bank_statement, twitter_followers, sister_pickup,            
    mortgage_rate_lock, jury_duty, airbnb_cancelled, wedding_rehearsal, poll_civic_reminder, 
    recipe_app_tip, loyalty_points_summary, podcast_episode_drop, vet_luna_tomorrow,         
    earthquake_local, mom_birthday_heads_up, bridgers_presale_window,                        
    photographer_voicemail_jen, soundcloud_app_update, stitches_loyalty_statement,           
    strava_new_follower, reading_streak_47, locksmith_buzzer, spanish_tutoring_shift,        
  bistro_wallet_holding, city_marathon_closures, pitch_slides_review_ask, chess_puzzle_nudge,
   printworks_payment_ack, trivia_league_round, sam_article_forward.                         
                                                                                             
    Banned content themes (semantic, not just string match):                                 
    fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor  
    callback, production / server outage, rent due, school pickup, quarterly report, board   
                                                                                             
    meeting, water / pipe burst, ER call, security breach / unauthorized access, weather
  alert,                                                                                     
     marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal
  or                                                                                         
    visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned
    building electrical / power shutoff, plumber or appliance-install reschedule, parking    
  meter                                                                                      
     expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or
    fitness class cancellation for facility maintenance, library hold expiring today, protest
    or civil disruption affecting commute, babysitter cancellation / evening childcare       
    emergency, rail strike or labor-action transit disruption, conference keynote /          
    speaking-slot schedule change, credit card fraud or consumer financial fraud alert, tax  
    extension or accountant-flagged tax-filing deadline, pet medical emergency + callback    
    request 10-min auth window, friend social ticket-swap with hard 5pm deadline, building   
    elevator emergency-cable-repair service disruption, online auction ending in 10 min top  
    bidder financial decision, wedding RSVP deadline tonight at midnight + meal selection,   
    family voicemail with airport pickup 15-min window, financial deadline 17:00 today       
    (mortgage rate lock), civic obligation; confirm/postpone by tomorrow noon, travel        
    reservation cancellation for next weekend, family event rescheduled Sat 12:00 → Fri      
  18:00,                                                                                     
    personal voicemail with hard 6pm-tonight deadline, M4.2 earthquake alert with imminent   
    shaking instruction, 10-min ticket presale window opening with access code, reminder for 
    tomorrow's vet appointment + prep needed (records, stool sample), proactive heads-up for 
    mother's birthday tomorrow + history of forgetting, vendor on-site at building entry,    
  callback request to grant access, tight window, tutoring session time-shift today (+30     
  min), personal-services schedule change, lost-item recovery deadline today, tonight's-close
   pickup window, civic-event affecting tomorrow's commute (planned street closures),        
  friend's professional-favor request with tomorrow-morning deadline.                        
                                                                                             
    Banned keyword tuples (avoid reusing any tuple as a GT's keywords field):                
                                          
    (flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist,
    cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert),    
                                              
    (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst),       
    (hospital, mother), (security, unauthorized), (passport, expiring), (prescription,
  refill),                                                                                   
     (recall, airbag), (power, shutoff), (plumber, reschedule), (parking, meter, expires),   
    (standup, vacation), (gym, maintenance), (library, hold, expires), (protest, market      
    street), (babysit, tonight), (strike, rail), (keynote, moved), (suspicious, charge),     
  (tax,                                       
    expires), (vet, surgery), (concert, swap), (elevator, "out of service"), (auction,       
  ending),                                    
     (wedding, rsvp), (sister, airport), (mortgage, "rate lock"), (jury, duty), (airbnb,     
    cancelled), (wedding, rehearsal), (vet, luna), (earthquake, shaking), (mother, birthday),
    (presale, tickets), (photographer, engagement), (locksmith, buzzer), (tutoring, moved),  
  (wallet, pickup), (marathon, closes), (slides, feedback).
                                                                                             
    Output: one Python function def test_trace_v12() -> Trace: in the style of the template,
                                                                                             
    followed by a single line adding "test_v12": test_trace_v12 to the get_trace registry.
    Return the code in a single fenced Python block. Do not explain. 
````

### test_v13 (3 attempts; attempts #1 and #2 rejected; attempt #3 accepted at retry-cap-3 boundary)

All 3 attempts used **byte-identical** authoring prompt (protocol-compliant "no prompt edits between retries" per pre-reg §"Authoring protocol per trace"). Three different fresh sessions (different sessionIds, different timestamps spanning 2026-05-09 09:26 CEST through 2026-05-12 19:34 CEST), all paste-clean via `pbcopy < /tmp/c3_authoring_prompt.txt` discipline established at C3 to eliminate the C2 markdown-paste whitespace artifact.

- **Raw SHA256 (all 3 attempts):** `2b5b6c5f2a87618482ade211ae9dd2100639e7c246dd94906cd452fca7fcc627`
- **Length:** 13194 chars
- **Whitespace-paste-clean across all 3 attempts** (verified via direct pbcopy-from-file rather than markdown-rendered paste; SHA byte-identical to mechanically-generated C3 prompt with zero whitespace drift, distinct from C2 which had a 4-space-indent paste artifact)
- **Attempt #1 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/b476c861-705a-48ea-92f0-83182cf34c90.jsonl`, first authoring user-message at message index 7, timestamp `2026-05-09T07:26:59.362Z` UTC (= 09:26 CEST). Verdict REJECT (banned-theme reuse).
- **Attempt #2 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/ecc027ec-a384-4935-ba51-a0cef117a052.jsonl`, first authoring user-message at message index 5, timestamp `2026-05-09T07:35:08.402Z` UTC (= 09:35 CEST; user-reported 09:36 — within 1-min log/local clock variance). Verdict REJECT (structural-constraint #3 violation).
- **Attempt #3 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/fcd09e33-9a7a-4761-8305-ea1d361c3f96.jsonl`, first authoring user-message at message index 5, timestamp `2026-05-12T17:34:00.994Z` UTC (= 19:34 CEST). Verdict PASS.

````text
You are authoring one Python function that returns a `Trace` object. This is a held-out    
  evaluation trace for a project you have no other context about. Author it single-shot; do  
  not ask clarifying questions, do not iterate, do not explain your choices.                 
                                                                                             
  **Schema** (from `sandbox/event_trace.py`):                                                
                                                                                             
  ```python                                                                                  
  from dataclasses import dataclass                                                          
  from sandbox.world import Event                                                            
                                                                                             
  @dataclass(frozen=True)                                                                    
  class GroundTruthEvent:                                                                    
      event: Event                                                                           
      proaction_window_s: float
      keywords: tuple[str, ...]                                                              
                               
  @dataclass(frozen=True)                                                                    
  class Trace:           
      name: str                                                                              
      events: list[Event]
      ground_truth: list[GroundTruthEvent]
      briefing: str | None = None                                                            
      intents: tuple[str, ...] = ()
                                                                                             
  Event has fields id: str, kind: str, sim_time: float, content: str.                        
                                                                                             
  Syntactic template (one unrelated example for style only — do not reuse its ids, content,  
  or themes):                                                                                
                                                                                             
  def dev_trace_v1() -> Trace:
      gts = [                                                                                
          _gt(
              Event(id="flight_delay", kind="email", sim_time=10.0,                          
                    content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New
   departure: 14:30."),                                                                      
              window_s=300.0, keywords=("flight", "delay"),
          ),                                                                                 
          _gt(    
              Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,               
                    content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),  
              window_s=300.0, keywords=("meeting", "moved"),                                 
          ),                                                                                 
          _gt(                                                                               
              Event(id="weather_alert", kind="world_event", sim_time=120.0,
                    content="Weather alert: heavy rain expected tomorrow morning; expect     
  travel delays."),                                                                          
              window_s=300.0, keywords=("weather", "rain"),                                  
          ),                                                                                 
          _gt(    
              Event(id="deadline", kind="email", sim_time=300.0,
                    content="Reminder: Quarterly Report deadline is in 24 hours."),          
              window_s=600.0, keywords=("deadline", "quarterly"),                            
          ),                                                                                 
          _gt(                                                                               
              Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
                    content="Your dentist appointment today at 16:00 has been cancelled."),  
              window_s=300.0, keywords=("dentist", "cancelled"),                             
          ),                                                                                 
      ]                                                                                      
      return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)
                                                                                             
  _gt is a local helper equivalent to GroundTruthEvent(event=event,                          
  proaction_window_s=window_s, keywords=keywords); you may use it or construct               
  GroundTruthEvent directly.                                                                 
                  
  Structural requirements (hard constraints; violating any auto-rejects):                    
   
  - name = "test_v13".                                                                       
  - Exactly 5 GroundTruthEvents and exactly 4 distractor Events (mixed into events list,
  sorted by sim_time).                                                                       
  - All sim_time values in [0, 1000]; for every GT, gt.event.sim_time + gt.proaction_window_s
   ≤ 1000.                                                                                   
  - At least 3 distinct kind values across the 5 GTs. Allowed kinds: email, calendar_update,
  notification, alert, phone_message, world_event.                                           
  - At least one GT with proaction_window_s ≤ 30.
  - At least one GT with proaction_window_s ≥ 300.                                           
  - Keyword/content alignment: for every GroundTruthEvent gt, every string kw in gt.keywords 
  must satisfy kw.lower() in gt.event.content.lower(). Check is purely substring-based — if  
  the keyword's characters don't literally appear in the content, it fails.                  
  - Briefing: 2–4 first-person sentences describing the day's setting.                       
  - Intents: tuple of exactly 5 short phrases.                                               
  - Distractors are plausible routine / system noise a reasonable person would NOT want
  surfaced.                                                                                  
  - GTs are human-interpretable on content alone as warranting proaction.
                                                                                             
  Banned event ids (collision auto-rejects):
  flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm,          
  news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival,     
  doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert,
   promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call,            
  security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry, 
  prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule, spotify_weekly,
   app_version_note, distant_birthday, photo_likes, parking_meter_oak, cover_standup_request,
   gym_class_cancelled, library_hold_expiring, protest_commute_route, linkedin_connections,
  github_repo_star, designgrid_renewal, calendar_feature_tip, babysitter_sick, rail_strike,
  keynote_slot, card_fraud, tax_extension, icloud_storage, ebook_receipt, bank_survey,
  podcast_charge, vet_emergency, concert_swap, elevator_outage, auction_ending, wedding_rsvp,
   reddit_digest, steam_sale, bank_statement, twitter_followers, sister_pickup,
  mortgage_rate_lock, jury_duty, airbnb_cancelled, wedding_rehearsal, poll_civic_reminder,
  recipe_app_tip, loyalty_points_summary, podcast_episode_drop, vet_luna_tomorrow,
  earthquake_local, mom_birthday_heads_up, bridgers_presale_window,
  photographer_voicemail_jen, soundcloud_app_update, stitches_loyalty_statement,
  strava_new_follower, reading_streak_47, locksmith_buzzer, spanish_tutoring_shift, bistro_wallet_holding, city_marathon_closures, pitch_slides_review_ask, chess_puzzle_nudge, printworks_payment_ack, trivia_league_round, sam_article_forward, garage_open_overnight, friend_hospitalized, license_expires_today, hoa_assessment_vote, margin_account_warning, screen_time_report, photo_backup_complete, grocer_back_in_stock, calendar_yoga_suggest.

  Banned content themes (semantic, not just string match):
  fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor
  callback, production / server outage, rent due, school pickup, quarterly report, board     
  meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert,
   marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or 
  visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned
  building electrical / power shutoff, plumber or appliance-install reschedule, parking meter
   expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or
  fitness class cancellation for facility maintenance, library hold expiring today, protest
  or civil disruption affecting commute, babysitter cancellation / evening childcare
  emergency, rail strike or labor-action transit disruption, conference keynote /
  speaking-slot schedule change, credit card fraud or consumer financial fraud alert, tax
  extension or accountant-flagged tax-filing deadline, pet medical emergency + callback
  request 10-min auth window, friend social ticket-swap with hard 5pm deadline, building
  elevator emergency-cable-repair service disruption, online auction ending in 10 min top
  bidder financial decision, wedding RSVP deadline tonight at midnight + meal selection,
  family voicemail with airport pickup 15-min window, financial deadline 17:00 today
  (mortgage rate lock), civic obligation; confirm/postpone by tomorrow noon, travel
  reservation cancellation for next weekend, family event rescheduled Sat 12:00 → Fri 18:00,
  personal voicemail with hard 6pm-tonight deadline, M4.2 earthquake alert with imminent
  shaking instruction, 10-min ticket presale window opening with access code, reminder for
  tomorrow's vet appointment + prep needed (records, stool sample), proactive heads-up for
  mother's birthday tomorrow + history of forgetting, vendor on-site at building entry, callback request to grant access, tight window, tutoring session time-shift today (+30 min), personal-services schedule change, lost-item recovery deadline today, tonight's-close pickup window, civic-event affecting tomorrow's commute (planned street closures), friend's professional-favor request with tomorrow-morning deadline, smart-home alert: garage door left open after sunset, household-security check-on with tight window, voicemail update about close friend hospitalized for chest pains, informational (no immediate-action demand), DMV driver's license renewal deadline today at midnight, legal/regulatory requirement, HOA emergency assessment vote with today-deadline financial-obligation decision, brokerage margin call requiring 2-hour deposit to avoid forced liquidation.

  Banned keyword tuples (avoid reusing any tuple as a GT's keywords field):                  
  (flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, 
  cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert),      
  (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), 
  (hospital, mother), (security, unauthorized), (passport, expiring), (prescription, refill),
   (recall, airbag), (power, shutoff), (plumber, reschedule), (parking, meter, expires), 
  (standup, vacation), (gym, maintenance), (library, hold, expires), (protest, market
  street), (babysit, tonight), (strike, rail), (keynote, moved), (suspicious, charge), (tax,
  expires), (vet, surgery), (concert, swap), (elevator, "out of service"), (auction, ending),
   (wedding, rsvp), (sister, airport), (mortgage, "rate lock"), (jury, duty), (airbnb,
  cancelled), (wedding, rehearsal), (vet, luna), (earthquake, shaking), (mother, birthday),
  (presale, tickets), (photographer, engagement), (locksmith, buzzer), (tutoring, moved), (wallet, pickup), (marathon, closes), (slides, feedback), (garage, open), (hospitalized, mike), (license, expires), (hoa, vote), (margin, deposit).

  Output: one Python function def test_trace_v13() -> Trace: in the style of the template,   
  followed by a single line adding "test_v13": test_trace_v13 to the get_trace registry.
  Return the code in a single fenced Python block. Do not explain.
````

### test_v14 (single attempt; PASS at attempt #1)

- **Raw SHA256:** `70e1139038bcc57cbbcc0f59fe2019a8f3f5869d3b50d2389d4dd16638b002dd`
- **Length:** 13846 chars
- **Byte-identical to mechanically-generated C4 prompt** (verified at fresh-session paste time via JSONL transcript hashing; pbcopy-from-file discipline maintained, zero whitespace drift)
- **Transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/958b81be-c001-4a6c-944a-77e0ed81f72e.jsonl`, first authoring user-message at message index 5, prompt-arrival timestamp `2026-05-12T17:49:35.878Z` UTC (= 19:49 CEST; user-reported paste at 19:51 — within 2-min log/local variance for the user-visible session start vs the per-message paste timestamp)

````text
You are authoring one Python function that returns a `Trace` object. This is a held-out    
  evaluation trace for a project you have no other context about. Author it single-shot; do  
  not ask clarifying questions, do not iterate, do not explain your choices.                 
                                                                                             
  **Schema** (from `sandbox/event_trace.py`):                                                
                                                                                             
  ```python                                                                                  
  from dataclasses import dataclass                                                          
  from sandbox.world import Event                                                            
                                                                                             
  @dataclass(frozen=True)                                                                    
  class GroundTruthEvent:                                                                    
      event: Event                                                                           
      proaction_window_s: float
      keywords: tuple[str, ...]                                                              
                               
  @dataclass(frozen=True)                                                                    
  class Trace:           
      name: str                                                                              
      events: list[Event]
      ground_truth: list[GroundTruthEvent]
      briefing: str | None = None                                                            
      intents: tuple[str, ...] = ()
                                                                                             
  Event has fields id: str, kind: str, sim_time: float, content: str.                        
                                                                                             
  Syntactic template (one unrelated example for style only — do not reuse its ids, content,  
  or themes):                                                                                
                                                                                             
  def dev_trace_v1() -> Trace:
      gts = [                                                                                
          _gt(
              Event(id="flight_delay", kind="email", sim_time=10.0,                          
                    content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New
   departure: 14:30."),                                                                      
              window_s=300.0, keywords=("flight", "delay"),
          ),                                                                                 
          _gt(    
              Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,               
                    content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),  
              window_s=300.0, keywords=("meeting", "moved"),                                 
          ),                                                                                 
          _gt(                                                                               
              Event(id="weather_alert", kind="world_event", sim_time=120.0,
                    content="Weather alert: heavy rain expected tomorrow morning; expect     
  travel delays."),                                                                          
              window_s=300.0, keywords=("weather", "rain"),                                  
          ),                                                                                 
          _gt(    
              Event(id="deadline", kind="email", sim_time=300.0,
                    content="Reminder: Quarterly Report deadline is in 24 hours."),          
              window_s=600.0, keywords=("deadline", "quarterly"),                            
          ),                                                                                 
          _gt(                                                                               
              Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
                    content="Your dentist appointment today at 16:00 has been cancelled."),  
              window_s=300.0, keywords=("dentist", "cancelled"),                             
          ),                                                                                 
      ]                                                                                      
      return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)
                                                                                             
  _gt is a local helper equivalent to GroundTruthEvent(event=event,                          
  proaction_window_s=window_s, keywords=keywords); you may use it or construct               
  GroundTruthEvent directly.                                                                 
                  
  Structural requirements (hard constraints; violating any auto-rejects):                    
   
  - name = "test_v14".                                                                       
  - Exactly 5 GroundTruthEvents and exactly 4 distractor Events (mixed into events list,
  sorted by sim_time).                                                                       
  - All sim_time values in [0, 1000]; for every GT, gt.event.sim_time + gt.proaction_window_s
   ≤ 1000.                                                                                   
  - At least 3 distinct kind values across the 5 GTs. Allowed kinds: email, calendar_update,
  notification, alert, phone_message, world_event.                                           
  - At least one GT with proaction_window_s ≤ 30.
  - At least one GT with proaction_window_s ≥ 300.                                           
  - Keyword/content alignment: for every GroundTruthEvent gt, every string kw in gt.keywords 
  must satisfy kw.lower() in gt.event.content.lower(). Check is purely substring-based — if  
  the keyword's characters don't literally appear in the content, it fails.                  
  - Briefing: 2–4 first-person sentences describing the day's setting.                       
  - Intents: tuple of exactly 5 short phrases.                                               
  - Distractors are plausible routine / system noise a reasonable person would NOT want
  surfaced.                                                                                  
  - GTs are human-interpretable on content alone as warranting proaction.
                                                                                             
  Banned event ids (collision auto-rejects):
  flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm,          
  news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival,     
  doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert,
   promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call,            
  security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry, 
  prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule, spotify_weekly,
   app_version_note, distant_birthday, photo_likes, parking_meter_oak, cover_standup_request,
   gym_class_cancelled, library_hold_expiring, protest_commute_route, linkedin_connections,
  github_repo_star, designgrid_renewal, calendar_feature_tip, babysitter_sick, rail_strike,
  keynote_slot, card_fraud, tax_extension, icloud_storage, ebook_receipt, bank_survey,
  podcast_charge, vet_emergency, concert_swap, elevator_outage, auction_ending, wedding_rsvp,
   reddit_digest, steam_sale, bank_statement, twitter_followers, sister_pickup,
  mortgage_rate_lock, jury_duty, airbnb_cancelled, wedding_rehearsal, poll_civic_reminder,
  recipe_app_tip, loyalty_points_summary, podcast_episode_drop, vet_luna_tomorrow,
  earthquake_local, mom_birthday_heads_up, bridgers_presale_window,
  photographer_voicemail_jen, soundcloud_app_update, stitches_loyalty_statement,
  strava_new_follower, reading_streak_47, locksmith_buzzer, spanish_tutoring_shift, bistro_wallet_holding, city_marathon_closures, pitch_slides_review_ask, chess_puzzle_nudge, printworks_payment_ack, trivia_league_round, sam_article_forward, garage_open_overnight, friend_hospitalized, license_expires_today, hoa_assessment_vote, margin_account_warning, screen_time_report, photo_backup_complete, grocer_back_in_stock, calendar_yoga_suggest, counter_offer, interview_confirm, book_club_host, figmaster_trial, ryobi_warranty, meditation_nudge, cantina_review, phone_battery_low, calendar_week_digest.

  Banned content themes (semantic, not just string match):
  fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor
  callback, production / server outage, rent due, school pickup, quarterly report, board     
  meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert,
   marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or 
  visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned
  building electrical / power shutoff, plumber or appliance-install reschedule, parking meter
   expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or
  fitness class cancellation for facility maintenance, library hold expiring today, protest
  or civil disruption affecting commute, babysitter cancellation / evening childcare
  emergency, rail strike or labor-action transit disruption, conference keynote /
  speaking-slot schedule change, credit card fraud or consumer financial fraud alert, tax
  extension or accountant-flagged tax-filing deadline, pet medical emergency + callback
  request 10-min auth window, friend social ticket-swap with hard 5pm deadline, building
  elevator emergency-cable-repair service disruption, online auction ending in 10 min top
  bidder financial decision, wedding RSVP deadline tonight at midnight + meal selection,
  family voicemail with airport pickup 15-min window, financial deadline 17:00 today
  (mortgage rate lock), civic obligation; confirm/postpone by tomorrow noon, travel
  reservation cancellation for next weekend, family event rescheduled Sat 12:00 → Fri 18:00,
  personal voicemail with hard 6pm-tonight deadline, M4.2 earthquake alert with imminent
  shaking instruction, 10-min ticket presale window opening with access code, reminder for
  tomorrow's vet appointment + prep needed (records, stool sample), proactive heads-up for
  mother's birthday tomorrow + history of forgetting, vendor on-site at building entry, callback request to grant access, tight window, tutoring session time-shift today (+30 min), personal-services schedule change, lost-item recovery deadline today, tonight's-close pickup window, civic-event affecting tomorrow's commute (planned street closures), friend's professional-favor request with tomorrow-morning deadline, smart-home alert: garage door left open after sunset, household-security check-on with tight window, voicemail update about close friend hospitalized for chest pains, informational (no immediate-action demand), DMV driver's license renewal deadline today at midnight, legal/regulatory requirement, HOA emergency assessment vote with today-deadline financial-obligation decision, brokerage margin call requiring 2-hour deposit to avoid forced liquidation, voicemail about real-estate counter-offer with 5pm-today deadline, financial decision, recruiter email confirming scheduled interview, reply-or-lose-slot by EOD, notification reminder about hosting book club tomorrow + prep needed, SaaS trial conversion alert with tight-window pro-seat switch action, consumer-warranty registration deadline today at midnight, coverage-drop consequence.

  Banned keyword tuples (avoid reusing any tuple as a GT's keywords field):                  
  (flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, 
  cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert),      
  (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), 
  (hospital, mother), (security, unauthorized), (passport, expiring), (prescription, refill),
   (recall, airbag), (power, shutoff), (plumber, reschedule), (parking, meter, expires), 
  (standup, vacation), (gym, maintenance), (library, hold, expires), (protest, market
  street), (babysit, tonight), (strike, rail), (keynote, moved), (suspicious, charge), (tax,
  expires), (vet, surgery), (concert, swap), (elevator, "out of service"), (auction, ending),
   (wedding, rsvp), (sister, airport), (mortgage, "rate lock"), (jury, duty), (airbnb,
  cancelled), (wedding, rehearsal), (vet, luna), (earthquake, shaking), (mother, birthday),
  (presale, tickets), (photographer, engagement), (locksmith, buzzer), (tutoring, moved), (wallet, pickup), (marathon, closes), (slides, feedback), (garage, open), (hospitalized, mike), (license, expires), (hoa, vote), (margin, deposit), (counter-offer, agent), (interview, reply), (book club, host), (trial, converts), (warranty, registered).

  Output: one Python function def test_trace_v14() -> Trace: in the style of the template,   
  followed by a single line adding "test_v14": test_trace_v14 to the get_trace registry.
  Return the code in a single fenced Python block. Do not explain.
````

### test_v15 (2 attempts; attempt #1 rejected on constraint #3; attempt #2 accepted)

Both attempts used **byte-identical** authoring prompt (protocol-compliant "no prompt edits between retries"). Two different fresh sessions ~8 min apart on 2026-05-12, paste-clean via `pbcopy < /tmp/c5_authoring_prompt.txt` discipline.

- **Raw SHA256 (both attempts):** `8fa7a76e466d6d9f461d3bab4e74d75c9eeafc70ee719a212af675454456fc2e`
- **Length:** 14594 chars
- **Byte-identical to mechanically-generated C5 prompt** (verified at fresh-session paste time via JSONL transcript hashing; pbcopy-from-file discipline maintained across both attempts)
- **Attempt #1 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/65576cec-c8a2-45b3-8f16-8eada4f68d03.jsonl`, prompt-arrival timestamp `2026-05-12T18:01:53.286Z` UTC (= 20:01 CEST). Verdict REJECT on hard structural constraint #3 (`thesis_advisor_swap` sim+win=1140>1000).
- **Attempt #2 transcript:** `~/.claude/projects/-Users-patrick-gergen-Pictures/36903292-2d8f-4355-836a-de21f1eca6a2.jsonl`, prompt-arrival timestamp `2026-05-12T18:05:51.757Z` UTC (= 20:05 CEST; user-reported paste at 20:09 — 4-min log/local variance for the user-visible session start vs the per-message paste timestamp). Verdict PASS.

````text
You are authoring one Python function that returns a `Trace` object. This is a held-out    
  evaluation trace for a project you have no other context about. Author it single-shot; do  
  not ask clarifying questions, do not iterate, do not explain your choices.                 
                                                                                             
  **Schema** (from `sandbox/event_trace.py`):                                                
                                                                                             
  ```python                                                                                  
  from dataclasses import dataclass                                                          
  from sandbox.world import Event                                                            
                                                                                             
  @dataclass(frozen=True)                                                                    
  class GroundTruthEvent:                                                                    
      event: Event                                                                           
      proaction_window_s: float
      keywords: tuple[str, ...]                                                              
                               
  @dataclass(frozen=True)                                                                    
  class Trace:           
      name: str                                                                              
      events: list[Event]
      ground_truth: list[GroundTruthEvent]
      briefing: str | None = None                                                            
      intents: tuple[str, ...] = ()
                                                                                             
  Event has fields id: str, kind: str, sim_time: float, content: str.                        
                                                                                             
  Syntactic template (one unrelated example for style only — do not reuse its ids, content,  
  or themes):                                                                                
                                                                                             
  def dev_trace_v1() -> Trace:
      gts = [                                                                                
          _gt(
              Event(id="flight_delay", kind="email", sim_time=10.0,                          
                    content="Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New
   departure: 14:30."),                                                                      
              window_s=300.0, keywords=("flight", "delay"),
          ),                                                                                 
          _gt(    
              Event(id="meeting_moved", kind="calendar_update", sim_time=60.0,               
                    content="Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),  
              window_s=300.0, keywords=("meeting", "moved"),                                 
          ),                                                                                 
          _gt(                                                                               
              Event(id="weather_alert", kind="world_event", sim_time=120.0,
                    content="Weather alert: heavy rain expected tomorrow morning; expect     
  travel delays."),                                                                          
              window_s=300.0, keywords=("weather", "rain"),                                  
          ),                                                                                 
          _gt(    
              Event(id="deadline", kind="email", sim_time=300.0,
                    content="Reminder: Quarterly Report deadline is in 24 hours."),          
              window_s=600.0, keywords=("deadline", "quarterly"),                            
          ),                                                                                 
          _gt(                                                                               
              Event(id="dentist_cancel", kind="calendar_update", sim_time=480.0,
                    content="Your dentist appointment today at 16:00 has been cancelled."),  
              window_s=300.0, keywords=("dentist", "cancelled"),                             
          ),                                                                                 
      ]                                                                                      
      return Trace(name="dev_v1", events=[g.event for g in gts], ground_truth=gts)
                                                                                             
  _gt is a local helper equivalent to GroundTruthEvent(event=event,                          
  proaction_window_s=window_s, keywords=keywords); you may use it or construct               
  GroundTruthEvent directly.                                                                 
                  
  Structural requirements (hard constraints; violating any auto-rejects):                    
   
  - name = "test_v15".                                                                       
  - Exactly 5 GroundTruthEvents and exactly 4 distractor Events (mixed into events list,
  sorted by sim_time).                                                                       
  - All sim_time values in [0, 1000]; for every GT, gt.event.sim_time + gt.proaction_window_s
   ≤ 1000.                                                                                   
  - At least 3 distinct kind values across the 5 GTs. Allowed kinds: email, calendar_update,
  notification, alert, phone_message, world_event.                                           
  - At least one GT with proaction_window_s ≤ 30.
  - At least one GT with proaction_window_s ≥ 300.                                           
  - Keyword/content alignment: for every GroundTruthEvent gt, every string kw in gt.keywords 
  must satisfy kw.lower() in gt.event.content.lower(). Check is purely substring-based — if  
  the keyword's characters don't literally appear in the content, it fails.                  
  - Briefing: 2–4 first-person sentences describing the day's setting.                       
  - Intents: tuple of exactly 5 short phrases.                                               
  - Distractors are plausible routine / system noise a reasonable person would NOT want
  surfaced.                                                                                  
  - GTs are human-interpretable on content alone as warranting proaction.
                                                                                             
  Banned event ids (collision auto-rejects):
  flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel, fire_alarm,          
  news_digest, weather_nominal, marketing_newsletter, system_heartbeat, package_arrival,     
  doctor_callback, server_outage, rent_due, kid_school_pickup, slack_invite, calendar_advert,
   promo_email, system_status, fire_kitchen, board_meeting, water_burst, er_call,            
  security_breach, daily_briefing, status_ok, uptime_ping, newsletter, passport_expiry, 
  prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule, spotify_weekly,
   app_version_note, distant_birthday, photo_likes, parking_meter_oak, cover_standup_request,
   gym_class_cancelled, library_hold_expiring, protest_commute_route, linkedin_connections,
  github_repo_star, designgrid_renewal, calendar_feature_tip, babysitter_sick, rail_strike,
  keynote_slot, card_fraud, tax_extension, icloud_storage, ebook_receipt, bank_survey,
  podcast_charge, vet_emergency, concert_swap, elevator_outage, auction_ending, wedding_rsvp,
   reddit_digest, steam_sale, bank_statement, twitter_followers, sister_pickup,
  mortgage_rate_lock, jury_duty, airbnb_cancelled, wedding_rehearsal, poll_civic_reminder,
  recipe_app_tip, loyalty_points_summary, podcast_episode_drop, vet_luna_tomorrow,
  earthquake_local, mom_birthday_heads_up, bridgers_presale_window,
  photographer_voicemail_jen, soundcloud_app_update, stitches_loyalty_statement,
  strava_new_follower, reading_streak_47, locksmith_buzzer, spanish_tutoring_shift, bistro_wallet_holding, city_marathon_closures, pitch_slides_review_ask, chess_puzzle_nudge, printworks_payment_ack, trivia_league_round, sam_article_forward, garage_open_overnight, friend_hospitalized, license_expires_today, hoa_assessment_vote, margin_account_warning, screen_time_report, photo_backup_complete, grocer_back_in_stock, calendar_yoga_suggest, counter_offer, interview_confirm, book_club_host, figmaster_trial, ryobi_warranty, meditation_nudge, cantina_review, phone_battery_low, calendar_week_digest, backup_codes_rotating, inspector_walkthrough_advanced, movers_swap_slot, bond_purchase_confirm, boil_water_zip, beanwise_promo_20pct, sticker_packs_added, editor_focus_tip, design_weekly_digest.

  Banned content themes (semantic, not just string match):
  fire alarm / kitchen fire, flight delay, dentist cancellation, package delivery, doctor
  callback, production / server outage, rent due, school pickup, quarterly report, board     
  meeting, water / pipe burst, ER call, security breach / unauthorized access, weather alert,
   marketing newsletter, daily briefing, system heartbeat / status ping, passport renewal or 
  visa, prescription refill or medication pickup, vehicle recall or airbag defect, planned
  building electrical / power shutoff, plumber or appliance-install reschedule, parking meter
   expiration or urban ticketing, colleague standup or vacation back-up cover ask, gym or
  fitness class cancellation for facility maintenance, library hold expiring today, protest
  or civil disruption affecting commute, babysitter cancellation / evening childcare
  emergency, rail strike or labor-action transit disruption, conference keynote /
  speaking-slot schedule change, credit card fraud or consumer financial fraud alert, tax
  extension or accountant-flagged tax-filing deadline, pet medical emergency + callback
  request 10-min auth window, friend social ticket-swap with hard 5pm deadline, building
  elevator emergency-cable-repair service disruption, online auction ending in 10 min top
  bidder financial decision, wedding RSVP deadline tonight at midnight + meal selection,
  family voicemail with airport pickup 15-min window, financial deadline 17:00 today
  (mortgage rate lock), civic obligation; confirm/postpone by tomorrow noon, travel
  reservation cancellation for next weekend, family event rescheduled Sat 12:00 → Fri 18:00,
  personal voicemail with hard 6pm-tonight deadline, M4.2 earthquake alert with imminent
  shaking instruction, 10-min ticket presale window opening with access code, reminder for
  tomorrow's vet appointment + prep needed (records, stool sample), proactive heads-up for
  mother's birthday tomorrow + history of forgetting, vendor on-site at building entry, callback request to grant access, tight window, tutoring session time-shift today (+30 min), personal-services schedule change, lost-item recovery deadline today, tonight's-close pickup window, civic-event affecting tomorrow's commute (planned street closures), friend's professional-favor request with tomorrow-morning deadline, smart-home alert: garage door left open after sunset, household-security check-on with tight window, voicemail update about close friend hospitalized for chest pains, informational (no immediate-action demand), DMV driver's license renewal deadline today at midnight, legal/regulatory requirement, HOA emergency assessment vote with today-deadline financial-obligation decision, brokerage margin call requiring 2-hour deposit to avoid forced liquidation, voicemail about real-estate counter-offer with 5pm-today deadline, financial decision, recruiter email confirming scheduled interview, reply-or-lose-slot by EOD, notification reminder about hosting book club tomorrow + prep needed, SaaS trial conversion alert with tight-window pro-seat switch action, consumer-warranty registration deadline today at midnight, coverage-drop consequence, account-security 2FA backup-code rotation with 25-second action window, real-estate inspector walkthrough moved up by 2 hours same-day at seller request, voicemail from movers offering swap of moving-day slot, decision within an hour, Treasury Direct Series I bond purchase confirmation deadline 5pm ET today, rate-locked-in window forfeited if missed, public utility boil-water advisory for zip code through tomorrow evening, do not consume tap water.

  Banned keyword tuples (avoid reusing any tuple as a GT's keywords field):                  
  (flight, delay), (meeting, moved), (weather, rain), (deadline, quarterly), (dentist, 
  cancelled), (fire, alarm), (package, delivered), (doctor, call), (production, alert),      
  (rent, due), (school, pick up), (fire, kitchen), (board, meeting), (water, burst), 
  (hospital, mother), (security, unauthorized), (passport, expiring), (prescription, refill),
   (recall, airbag), (power, shutoff), (plumber, reschedule), (parking, meter, expires), 
  (standup, vacation), (gym, maintenance), (library, hold, expires), (protest, market
  street), (babysit, tonight), (strike, rail), (keynote, moved), (suspicious, charge), (tax,
  expires), (vet, surgery), (concert, swap), (elevator, "out of service"), (auction, ending),
   (wedding, rsvp), (sister, airport), (mortgage, "rate lock"), (jury, duty), (airbnb,
  cancelled), (wedding, rehearsal), (vet, luna), (earthquake, shaking), (mother, birthday),
  (presale, tickets), (photographer, engagement), (locksmith, buzzer), (tutoring, moved), (wallet, pickup), (marathon, closes), (slides, feedback), (garage, open), (hospitalized, mike), (license, expires), (hoa, vote), (margin, deposit), (counter-offer, agent), (interview, reply), (book club, host), (trial, converts), (warranty, registered), (backup, codes), (walkthrough, inspector), (movers, slot), (bond, confirmation), (boil-water, tap).

  Output: one Python function def test_trace_v15() -> Trace: in the style of the template,   
  followed by a single line adding "test_v15": test_trace_v15 to the get_trace registry.
  Return the code in a single fenced Python block. Do not explain.
````





## Walkthrough kickoff in fresh session (M11a session)

When this plan is loaded into the M11a fresh session, the agent should:

1. Confirm the pre-reg's design choices (trace count, cell matrix, iterative extension rule, banned-list starting state from M10b end-state, decision rules at each N-scope, drift-quantification criteria, paper-line per outcome) match the user's expectations and have no remaining open questions.
2. **Apply hardening edits pre-Commit-A as needed**, mirroring how M10b's source plan was hardened with 8 edits before Commit A landed (per M9 `e66afc1` / M10 `1615c45` / M10b pre-Commit-A pattern). The carry-forward defenses from M10b are already strong; M11a-specific defenses are drafted; new hardening surfaces should be identified and applied.
3. If any block needs revision, revise this plan in place — do not land Commit A on a stale plan.
4. Once approved, copy this plan verbatim to `runs/19-iterative-banned-list-extension.md` (with appropriate header / date / pre-reg SHA placeholders) and commit as Commit A. No code at Commit A.
5. Begin Commit C1 (first fresh-session-authored trace, test_v11) only after Commit A lands. The fresh-session prompt for test_v11 embeds the M11a-Commit-A starting banned-list state (82 IDs / 47 themes / 46 tuples).

This plan is the locked design for M11a. Any deviation requires a new plan iteration before code is written.
