# Run 18 — N-trace External Authoring (Empirical Coverage Variance, M10b)

**Date:** 2026-05-07 (pre-registration). Results sections (Commit C1-C5 audit logs + per-session attestations; Commit D 20-cell harness eval + paper-line per outcome row) appended post-eval.
**Milestone:** M10b — empirical hardening of M10's H2 (model-scale) claim. Five fresh externally-authored traces (test_v6 through test_v10) under the M8b/M10 protocol, evaluated on V2-3B vs V2-Opus to characterize coverage variance. Zero new architectural levers; zero code changes (sandbox + harness + arbiters all unchanged from M10 close `6f86c8d`); mirrors M8b/M10 protocol verbatim with pre-data hardening (8 edits made to the source plan before Commit A; mirrors M9 `e66afc1` / M10 `1615c45` pattern of defenses-hardening on top of an original pre-reg, but performed pre-Commit-A here since hardening was identified at the pre-reg walkthrough rather than after the original commit).
**Pre-registration SHA:** Commit A landed at SHA `1fd1c95` (this file's first commit; backfilled into the file body at the immediately-following SHA-backfill commit per no-amend discipline). Plan source: `~/.claude/plans/m10b-n-trace-external.md`. The 8 pre-data hardening edits (V2-Opus false/h ceiling, GT-regime classification independence, fresh-session model lock, 1-session-per-trace discipline, Row 4 split into 4a/4b, fair-trace-subset rule, N=5 CI-aware Row 1 wording, expanded drift smoke + GT-regime observation table) are documented in this plan and were landed in the source before any cell ran. None change the 0.80 hit threshold or the 0% / 20% / ≥40% failure-rate buckets; all are stricter, clarifying, or honest-weakening — audit-table-verified zero goalpost-moving risk.
**Predecessors:** M10 close SHA `6f86c8d` (positive close at row 1, H2 confirmed at n=1 external trace); M8b results SHA `ad70d67` (test_v4 falsification at V2-3B); M9 close SHA `aaa6232` (V3 path-C close at 3B, reframed at M10 as model-capability-bound).
**Environment:** Identical to M10. ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3` (predictor + surprise scorer + V2-3B baseline cell). Claude API: `anthropic` SDK, `ANTHROPIC_API_KEY` env var, `claude-opus-4-7` alias (M10b arbiter; per-call dispatch ID echoed `claude-opus-4-7` at M10 close, recorded per-cell at M10b run). Anthropic rates carry forward from M10's pre-reg lock: Opus 4.7 = $15 / M input tokens, $75 / M output tokens (no rate change observed between M10 close 2026-04-27 and M10b pre-reg 2026-05-07; verified at one-shot probe immediately before this commit).

## Context

M10 (`runs/17-claude-arbiter.md`, commit `6f86c8d`) closed at row 1 of the pre-registered paper-line table:
- In-distribution regression PASS on dev_v2 / test_v1 / test_v2 (V2-Opus matches M6a + recovers `package_arrival` on test_v1: hit 0.80→1.00).
- `test_v4` H1/H2 attribution: V2-Opus = 0.80, V3-Opus = 0.80 (vs M8b V2-3B = 0.40) → **H2 confirmed; V3 also viable at Opus scale.**
- `test_v5` (M10's fresh externally-authored trace): V2-Opus = V3-Opus = V2-3B = poll-Opus = cron = **1.00**. Fresh-session author chose GTs falling within V2's enumeration; doesn't differentiate H1/H2 by itself.
- Pareto: V2-Opus on test_v5 = $0.0088/hit vs poll-Opus = $0.2057/hit → **23.3× cheaper** at matched arbiter capability (P2 floor 3× exceeded by 7.8×).
- Aggregate M10 spend: $4.23 of $3-5 pre-reg budget.

**The single most predictable reviewer attack on the M10 close** (per the user's M10-close discussion): *"Your H2 claim ('model scale closes the M8b coverage gap') rests on n=1 trace. test_v4 V2-3B=0.40 → V2-Opus=0.80 is one data point. test_v5 doesn't differentiate H1/H2 because everyone hits 1.00. So your model-scale lever is supported by a single external trace's spread."*

M10b is **empirical hardening of the existing H2 claim**. No new architectural lever. No new prompt, no new model, no new code (sandbox + harness + arbiters all unchanged). The contribution is statistical: convert H2 from n=1 (test_v4) to n=5+ externally-authored traces, characterize the V2-3B-vs-V2-Opus coverage variance distribution empirically, and report it honestly regardless of pattern.

This pass is intentionally narrower than M10. M10 introduced the model-scale lever. M10b just exercises that lever N more times under the same M8b/M10 protocol.

## Thesis

> Under the M8b external-authoring protocol (fresh Claude Code session, non-project cwd, verbatim runs/16 authoring prompt, no carried context), V2-3B coverage on externally-authored traces is empirically below V2-Opus coverage; the M8b/test_v4 failure mode is a consistent property of out-of-V2-enumeration content rather than a one-off artifact.

The thesis is testable in three branches per the pre-registered analysis below. Each branch is publishable; the experiment is not designed to find a particular outcome.

## Frozen design choices (locked at this commit)

### Trace count: 5 new externally-authored traces

`test_v6` through `test_v10`. Hard cap N=5; no extension after eval. Pre-registered before any cell runs. Trace-count chosen as the smallest N that converts "single data point" into "binomial-style distribution with 5 trials" — large enough to support statements like "V2-3B fails on X of 5" but small enough to fit the same-day API budget at ~$1-2/trace.

### Cell matrix per trace: 4 cells × 5 traces = 20 cells

| cell | agent | arbiter | per-cell cost |
|---|---|---|---|
| V2-3B content | HeargentZAWide | ContentArbiter (V2 prompt, qwen2.5:3b-instruct) | $0 (local) |
| V2-Opus content | HeargentZAWide | ClaudeArbiter (V2 prompt, claude-opus-4-7) | ~$0.05 |
| poll-Opus | react_poll_claude | (Opus poll on every tick) | ~$1 |
| cron30s | CronKeyword30s | — | $0 |

**Skipped on purpose:**
- **V3-Opus**: M10's test_v4 attribution + test_v5 cells already established that V3-Opus tracks V2-Opus event-for-event at Opus scale. The V3 question is closed; running V3-Opus on each new trace would just duplicate the V2-Opus column at no information gain. (If the user wants V3 reconfirmed across N=5, that's an additional 5 cells × ~$0.05 = $0.25 — call out as optional; default skip.)
- **Random ablation**: M7's N=20 seed-variance + M10's test_v5 random cell already characterize random's behavior. M10b's question is V2-3B-vs-V2-Opus coverage variance, not random ablation. Skipping saves wall time.
- **V2-3B vs V2-Opus on co-developed traces**: not the M10b question; already pinned by M10 Commit B regression.

### Authoring protocol per trace (mirrors M8b/M10 Commit C verbatim)

1. **Fresh Claude Code session — pre-registered constraints (locked at this commit):**
   - **Model**: Opus 4.7 (`claude-opus-4-7` alias) for the authoring session. If the alias is rotated by Anthropic during the M10b run window, use the strongest available 4.x model at run date and record the substitution in the §"Authoring sessions" log per-trace. Rationale: M8b's `test_v4` and M10's `test_v5` were authored by the strongest Claude available at their respective run dates; M10b carries that protocol forward verbatim.
   - **Discipline**: **1 fresh Claude Code session per trace, hard rule.** Five traces ⇒ five separate sessions. Batched-with-/clear is **not permitted** under M10b protocol — the prompt-caching infrastructure could carry session-level state across `/clear` boundaries, and M8b/M10 both used 1-session-per-trace. Pre-registering the stricter discipline here closes the cross-session-leakage attack.
   - **Cwd / context isolation**: non-project cwd (e.g., `/tmp` or `~/Pictures`); no project CLAUDE.md, no auto-memory, no file-tree visibility on the project. `/clear` at session start to confirm empty history (defense-in-depth alongside the fresh-session rule).
   - **Per-session attestation**: record per-trace in runs/18 §"Authoring sessions": fresh-session timestamp, cwd, dispatched `response.model` from a one-shot probe, /clear confirmation. Mirrors M10's per-call dispatch ID logging.
2. Paste runs/16 §"Authoring prompt" verbatim as first user message. **One substitution:** `name = "test_vN"` where N ∈ {6, 7, 8, 9, 10}, and `def test_trace_vN()` accordingly. The substitution is mechanical and pre-registered; it does not change semantic content of the prompt.
3. Fresh session emits a single Python code block + registry line.
4. M10b working session audits against the 11 hard structural constraints + 3 banned lists (lists extended below to include test_v5's contributions; see "Banned lists for M10b").
5. If audit passes: paste verbatim into `sandbox/event_trace.py`, add to `get_trace` registry. Permitted edits per pre-reg: import ordering, parsing-blocker typo fixes, registry line. No content/keyword/structural modifications.
6. If audit fails: log rejection in runs/18 §"Rejections log" (fresh-session timestamp + first violated constraint + one-sentence violation description). Open **another fresh session** (new session, not /clear-on-existing) for the same trace number; no prompt edits. **Retry cap: 3 audit attempts per trace.** If the third fresh session also fails audit, halt M10b and document — likely indicates a banned-list-pressure systematic-drift signal (per defense #7) and the protocol itself needs M11+ revision.
7. Commit each authored trace as `M10b: externally-authored test_vN (fresh session <model-id>, <timestamp>)`.

### Banned lists for M10b (extends test_v5 contributions)

Each new trace's authoring prompt receives the M10b-extended banned lists. Extensions add test_v5's 9 IDs / 5 themes / 5 keyword tuples to runs/16's already-extended lists.

**Banned event IDs (55 = 46 from runs/16 + 9 from test_v5):**
```
flight_delay, meeting_moved, weather_alert, deadline, dentist_cancel,
fire_alarm, news_digest, weather_nominal, marketing_newsletter, system_heartbeat,
package_arrival, doctor_callback, server_outage, rent_due, kid_school_pickup,
slack_invite, calendar_advert, promo_email, system_status,
fire_kitchen, board_meeting, water_burst, er_call, security_breach,
daily_briefing, status_ok, uptime_ping, newsletter,
passport_expiry, prescription_urgent, car_recall, power_shutoff_planned, plumber_reschedule,
spotify_weekly, app_version_note, distant_birthday, photo_likes,
parking_meter_oak, cover_standup_request, gym_class_cancelled, library_hold_expiring, protest_commute_route,
linkedin_connections, github_repo_star, designgrid_renewal, calendar_feature_tip,
babysitter_sick, rail_strike, keynote_slot, card_fraud, tax_extension,
icloud_storage, ebook_receipt, bank_survey, podcast_charge
```

**Banned content themes (32 = 27 from runs/16 + 5 from test_v5):**

(runs/16's 27 themes verbatim) +
- babysitter cancellation / evening childcare emergency
- rail strike or labor-action transit disruption
- conference keynote / speaking-slot schedule change
- credit card fraud or consumer financial fraud alert
- tax extension or accountant-flagged tax-filing deadline

**Banned keyword tuples (31 = 26 from runs/16 + 5 from test_v5):**

(runs/16's 26 tuples verbatim) +
`(babysit, tonight), (strike, rail), (keynote, moved), (suspicious, charge), (tax, expires)`

### Code changes

**Zero**. M10b reuses every component of M10 unchanged:
- `agent/arbiter.py` ClaudeArbiter — unchanged
- `baselines/react_poll_claude.py` — unchanged
- `eval/run_trace.py` CLI — unchanged
- All baselines, predictor, surprise scorer, sandbox/world.py — unchanged
- `sandbox/event_trace.py` — only appends `test_trace_v6` … `test_trace_v10` and registry entries; no edits to existing trace functions

This is the simplest possible follow-up to M10. M10b is empirical iteration on the existing protocol, not engineering.

## Five-commit protocol

| Commit | Content | Gates |
|---|---|---|
| **A** | This pre-reg → `runs/18-n-trace-external.md` (frozen design choices + banned-list extensions + cell matrix + decision rules + paper-line per outcome). No code. | — |
| **C1-C5** | Five externally-authored traces (one commit per trace). Each via fresh session, audit, paste verbatim into `sandbox/event_trace.py`, register, commit. | Audit gate per trace; reject + log on any constraint violation, retry with new fresh session, no prompt edits. |
| **D** | 20-cell harness matrix run after all 5 traces lands; results table + per-trace verdict + aggregate analysis appended to runs/18. | Verbatim evaluation against frozen P1 / P2 rules. |

(Note the absence of a "Commit B": M10b adds no code. The Commit B equivalent is implicit in M10's `f28689e` — that's the code state M10b runs on.)

## Pre-registered analysis

### Per-trace observations table (filled at Commit D)

| trace | V2-3B hit | V2-3B false/h | V2-Opus hit | V2-Opus false/h | poll-Opus hit | cron30s hit | GT-regime in V2's YES enumeration? (independent inspection) | V2-Opus closes? |
|---|---|---|---|---|---|---|---|---|

Each row is one of test_v6 … test_v10.

**"GT-regime in V2's YES enumeration?" classification rule (pre-registered).** Filled per trace by inspecting the GT events' regime (e.g., transit / weather / health / financial / civic / childcare / professional / urban-warning) against V2's literal YES list in `ARBITER_SYSTEM_PROMPT_V2` (`agent/arbiter.py`). **Performed before reading V2-3B's hit_rate on that trace** — independent classification, not derived from V2-3B's pass/fail (which would be tautological). Recorded as a paper-readability annotation; the aggregate failure-rate metric (P1) is fully objective and does not use this column.

### Aggregate metrics (filled at Commit D)

- **V2-3B failure rate**: # of fair-trace-subset traces (per P3) with `hit_rate(V2-3B) < 0.80`
- **V2-3B mean hit rate**: average across the fair-trace subset
- **V2-Opus failure rate**: # of fair-trace-subset traces with `hit_rate(V2-Opus) < 0.80` OR `false_initiation_rate_per_hour(V2-Opus) > 5.0` (expected: 0). The false/h ceiling is the YES-bias / permissiveness check — mirrors M10's +5/h tolerance defense (M10 §"Reviewer-vulnerable surfaces" #8). If V2-Opus reaches hit ≥ 0.80 by becoming permissive on borderline content, it counts as a failure, not a pass.
- **V2-Opus mean hit rate**: average across the fair-trace subset
- **V2-Opus mean false/h**: average across the fair-trace subset (sanity report alongside the failure-rate count)
- **Δhit (V2-Opus − V2-3B) per-trace and aggregate**: positive on traces where V2-3B fails; ~0 on traces where V2-3B already hits 1.00
- **V2-Opus closes V2-3B failures**: count of (trace where V2-3B<0.80 AND V2-Opus passes both bars)
- **Cost variance**: per-trace V2-Opus and poll-Opus $/hit; should track Commit B / D in-distribution + test_v5 numbers
- **Trace fairness**: poll-Opus hit_rate per trace (P3 sanity); cron30s hit_rate per trace
- **GT-regime distribution**: per-trace GT regimes tagged from the independent-classification column; aggregate compared against the dev_v2 / test_v1 / test_v2 / test_v4 / test_v5 regime distribution to detect banned-list-pressure systematic drift (per defense #7).

### Pre-registered decision rules (frozen; no post-hoc redefinition)

**P-numbering note (cross-milestone).** M10's P-numbering was P1 (primary hit), P2 (Pareto cost), P3 (C3 random), P4 (poll-Opus sanity). M10b's question is different (coverage variance, not Pareto / C3), so the numbering renumbers: P1 (V2-3B failure-rate buckets), P2 (V2-Opus failure rate including false/h ceiling), P3 (poll-Opus trace-fairness sanity, the M10-P4 analog). No analog of M10's P2 (Pareto cost) or P3 (C3 random) — those are not M10b's question; cost is reported as observation, random ablation is closed by M7's 20-seed sweep + M10's test_v5 random cell.

**P3 — Trace-fairness sanity (evaluated FIRST; gates the fair-trace subset for P1/P2).** poll-Opus hit ≥ 0.80 on each new trace (mirror M8b/M10 P4). The **fair-trace subset** = {trace ∈ test_v6..test_v10 : hit_rate(poll-Opus on trace) ≥ 0.80}. Traces failing this gate are reported as "ambiguous to all agents," kept as artifacts (per M8b's `test_v3` discipline), and **excluded from P1/P2 failure-rate computations**. Sensitivity analysis reports both included-all-5 and fair-subset-only variants for full transparency, but the headline P1/P2 verdicts are read off the fair-subset numbers. This rule is symmetric — fairness is not derived from V2-3B or V2-Opus performance — and is pre-registered before any cell runs.

**P1 — V2-3B failure rate ≥ 40%** (≥2 of N_fair traces with V2-3B hit < 0.80, where N_fair = |fair-trace subset|, expected N_fair = 5): **H2 confirmed at point estimate; CI-aware framing required.**
> Paper line: *"Across N=N_fair fresh externally-authored traces under the M8b protocol (fair-trace subset; see Methods), V2-3B coverage failed (hit < 0.80) on X / N_fair (point estimate; 95% binomial CI on the underlying failure rate is [L%, H%], wide due to small N). V2-Opus closed every failure (hit ≥ 0.80 AND false/h ≤ 5.0/h on X / X of those traces). Combined with M10's test_v4 attribution, the H2 (model-scale) claim rests on (X + 1) externally-authored failure cases plus 1 V2-3B success case (test_v5). The M8b/test_v4 failure mode is replicable in N=5 external authoring; tighter rate estimates require N=20+ future work (M11+)."*

**P1 — V2-3B failure rate = 20%** (1 of N_fair traces with V2-3B hit < 0.80): **H2 modestly confirmed at point estimate.**
> Paper line: *"Across N=N_fair fresh externally-authored traces (fair-trace subset), V2-3B coverage failed on 1 / N_fair (plus 1 / 1 on test_v4 from M8b → 2 / (N_fair+1) aggregate ≈ Y% point estimate; 95% binomial CI [L%, H%]). V2-Opus closed both failures (hit ≥ 0.80 AND false/h ≤ 5.0/h). At point estimate, the M8b failure mode appears at ~Y% rate in external authoring; V2-Opus is load-bearing when out-of-enumeration content surfaces, but in-enumeration draws are the more common case. CI is wide; M11+ N=20 would tighten."*

**P1 — V2-3B failure rate = 0%** (0 of N_fair traces with V2-3B < 0.80): **H2 weakly confirmed at point estimate; reframe Opus as insurance.**
> Paper line: *"Across N=N_fair fresh externally-authored traces (fair-trace subset), V2-3B coverage held at hit ≥ 0.80 on every trace. M8b's test_v4 failure (1 / (N_fair+1) point estimate; 95% binomial CI [L%, H%]) is a rare failure mode at the 3B scale rather than a consistent property of external authoring. V2-Opus serves as insurance against rare out-of-enumeration content (closing test_v4 on 1 / 6) rather than a uniform requirement; the in-distribution and Pareto headlines (M10) hold without modification, but H2 weakens to 'rare-failure-mode rescue' rather than 'consistent gap closure.' The methodological contribution remains M8b's external-authoring protocol; the empirical finding is that the protocol's failure rate at 3B is lower than test_v4 alone suggested. CI is wide; M11+ N=20 would tighten."*

**P2 — V2-Opus failure rate > 0%** (V2-Opus hit < 0.80 OR false/h > 5.0/h on any fair-subset trace): **New finding requiring mechanism diagnosis.**
> Paper line (conditional): *"On X / N_fair new traces, V2-Opus failed the joint bar (hit < 0.80 or false/h > 5.0/h) — extending M10's coverage scope. Per-failure mechanism: [tags, including whether hit-failure or false/h-permissiveness-failure]. The H2 claim updates from 'V2-Opus closes M8b's gap' to 'V2-Opus closes M8b's gap on most external-authored content but exhibits residual gaps on [classified failure modes]'. Future work (M11+) addresses these via [routing / V4 prompt / model-family upgrade]."*

The +5/h false/h ceiling is the YES-bias / permissiveness check (mirrors M10's +5/h symmetric tolerance defense on the in-distribution regression bars). Without it, V2-Opus could pass P2 by becoming permissive enough to surface every event (high hit, high false/h), which would be a regression from M10's bias-aware framing. Pre-registering the joint bar at this commit closes that loophole before any cell fires.

### Outcome interpretation lookup table (5 rows; locked at Commit A)

All counts are over the fair-trace subset (N_fair, expected = 5). "V2-Opus failures" = traces where V2-Opus fails the joint bar (hit < 0.80 OR false/h > 5.0/h). "V2-3B failures" = traces where V2-3B hit < 0.80. Every (V2-3B-failure-count, V2-Opus-failure-count) integer cell maps to exactly one row; Rows 4a/4b together cover all V2-Opus-failure cases.

| V2-3B failure rate | V2-Opus failure count | Row | Paper headline |
|---|---|---|---|
| ≥ 40% (≥2 / N_fair) | 0 | **Row 1** | H2 confirmed at point estimate across N_fair + test_v4. Model-scale load-bearing on the M8b out-of-V2-enum failure mode in this sample; CI on the underlying rate is wide and tighter estimates are M11+ future work. |
| = 20% (1 / N_fair) | 0 | **Row 2** | H2 modestly confirmed at point estimate; M8b failure mode at ~Y% aggregate rate (1+1 over N_fair+1). |
| = 0% (0 / N_fair) | 0 | **Row 3** | H2 weakened to rare-failure-rescue at point estimate; M8b/test_v4 was atypical. M10 in-dist + Pareto stand. |
| any | > 0 AND ≤ V2-3B failure count | **Row 4a** | **Partial-closure with residuals.** V2-Opus closes some of V2-3B's failures but has its own residual joint-bar failures on [tag] traces. Model-scale upgrade is *load-bearing-but-not-sufficient*; aggregate Δ(failure_count) = V2-3B − V2-Opus > 0 (improvement) or = 0 (no improvement). M11+ scope: routing / V4 prompt / model-family upgrade. |
| any | > V2-3B failure count | **Row 4b** | **Model-scale upgrade insufficient or harmful.** V2-Opus introduces *more* joint-bar failures than V2-3B (e.g., V2-Opus permissive on borderline content driving false/h spikes, or V2-Opus over-NO on regimes V2-3B happened to pass). Surface as the headline finding; H2 falsified in this direction. M11+ scope: prompt re-elicitation across model scales, or a different lever entirely. |

## Cost framework

Per-trace expected spend:
- V2-3B content: $0 (local)
- V2-Opus content: ~$0.05 (5-10 arbiter calls × ~$0.005 each)
- poll-Opus: ~$1 (200 ticks × ~$0.005/call)
- cron30s: $0 (local)
- **Per trace total: ~$1.05**

5 traces × $1.05 = **~$5-6 total**. Consistent with "M10b is cheap insurance" framing in the M10-close discussion.

If user opts for V3-Opus also (optional add-on): + 5 cells × $0.05 = $0.25 more (negligible).

If user opts for poll-Opus skip on some traces (cost reduction): minus $1 per trace skipped. Floor at ~$2-3 total if poll-Opus is run on only 2 of 5 (P3 sanity sample).

Default plan: poll-Opus on every trace ($5-6 total). The cost story for the paper benefits from full N=5 cost-denominator coverage.

## Critical files

- `~/.claude/plans/m10b-n-trace-external.md` — this plan; walkthrough at fresh-session kickoff before Commit A.
- `runs/18-n-trace-external.md` — Commit A pre-reg lands as a copy of this plan with appropriate header / date / pre-reg SHA.
- `sandbox/event_trace.py` — appends `test_trace_v6` … `test_trace_v10` + registry entries. Existing trace functions not touched.
- `runs/data/18*.json` — 20 cell results.
- `runs/README.md` — row 18 added; status block updated; paper framing updated to row 1/2/3/4 of M10b's outcome table.
- `agent/`, `baselines/`, `eval/`, `pyproject.toml`, `uv.lock` — **not touched** at any M10b commit.

## Verification

### Pre-Commit-D bit-identical smoke (drift detector across M10 close → M10b)

Run on **all three co-developed traces** (not just dev_v2) to fully cover the V2-Opus-arbiter-call surface that M10 in-distribution-regression-tested. ~$0.03 marginal vs dev_v2-only; closes "drift smoke only checked one trace's arbiter-call pattern" reviewer attack.

```sh
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace dev_v2 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out /tmp/smoke-pre-M10b-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v1 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out /tmp/smoke-pre-M10b-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
  --trace test_v2 --arbiter-mode claude --arbiter-system-prompt v2 \
  --out /tmp/smoke-pre-M10b-test_v2.json
# Compare each against runs/data/17b-content-opus-v2-{dev_v2,test_v1,test_v2}.json.
# Must be bit-identical on all three (no API drift between M10 close 2026-04-27 and M10b run date).
# Compare: hit_rate, false_initiation_rate_per_hour, total_notifications, misses,
#          llm_stats.arbiter_calls, llm_stats.arbiter_yes_rate, cost_usd.
```

If any of the three fails: halt, document drift (which trace, which field diverged, and the recorded `response.model` from a one-shot probe at smoke time), do not proceed. M10b's evaluation is conditional on the same Opus 4.7 dispatching to the same model version M10 used. If only the bit-level token counts shift but pass/fail decisions are unchanged, document as "soft drift" and decide whether to proceed (pre-reg note: a soft-drift M10b is still publishable as long as the discrepancy is documented and not load-bearing on P1/P2).

### Per-trace structural audit (mirrors M10 Commit C audit)

Per trace authored:
1. Schema check via `uv run python -c "from sandbox.event_trace import get_trace; t = get_trace('test_vN'); print(...)"`.
2. Keyword/content alignment audit (`all(kw.lower() in event.content.lower() for kw in keywords)` per GT, per M8b's hard constraint).
3. Banned-ID, banned-keyword-tuple, banned-theme manual review against the M10b-extended banned lists.
4. **Independent GT-regime classification** for the per-trace observations table: tag each GT's regime (e.g., transit / weather / health / financial / civic / childcare / professional / urban-warning) and check against V2's literal YES list. **Performed before any harness cell on this trace runs**, so the classification is independent of V2-3B's pass/fail. Recorded in runs/18 §"GT-regime classification" per-trace.
5. Reject + log + retry on any violation. No prompt edits. Retry cap: 3 audit attempts per trace (per Authoring protocol step 6).

### Commit D harness execution

```sh
# Per trace: 4 cells (V2-3B, V2-Opus, poll-Opus, cron30s)
for trace in test_v6 test_v7 test_v8 test_v9 test_v10; do
  uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
    --trace $trace --arbiter-mode content \
    --out runs/data/18d-content-3b-v2-${trace}.json
  uv run python -m eval.run_trace --agent agent.loop:HeargentZAWide \
    --trace $trace --arbiter-mode claude --arbiter-system-prompt v2 \
    --out runs/data/18d-content-opus-v2-${trace}.json
  uv run python -m eval.run_trace --agent baselines.react_poll_claude:ReactPollClaude \
    --trace $trace --out runs/data/18d-poll-opus-${trace}.json
  uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s \
    --trace $trace --out runs/data/18d-cron30-${trace}.json
done
```

Aggregate: read 20 cell JSONs, compute per-trace verdict, populate observations table, identify outcome row.

## Reviewer-vulnerable surfaces and pre-registered defenses

Mirroring M10's defense pattern.

1. **"Five external traces is still small N for variance characterization."** Defense: pre-registered hard cap before any cell ran. The choice of N=5 is documented as the smallest credible test_v6+ scope; adding more traces post-hoc would be cherry-picking. Future work (M11+) can scale to N=20+ if reviewers push.

2. **"You ran the fresh sessions yourself; how do we know you didn't subtly steer them?"** Defense: each session is opened in a non-project cwd (`/tmp` or `~/Pictures`), `/clear` first, single user message = the runs/16 authoring prompt verbatim. The fresh session has no project CLAUDE.md, no auto-memory, no file-tree visibility. M10b pre-registers **1 fresh Claude Code session per trace** (no batched-with-/clear) and **Opus 4.7 as the authoring model** — both stricter than the M8b/M10 verbal protocol, and both enforced via the per-session attestation recorded in runs/18 (timestamp + cwd + dispatched `response.model` + /clear confirmation per trace).

3. **"You only swap V2-3B vs V2-Opus; what about V3?"** Defense: M10's test_v4 attribution + test_v5 cells already established that V3-Opus tracks V2-Opus event-for-event at Opus scale. The V3 question is closed for the headline. Optional V3-Opus add-on (5 cells, $0.25) is named in §"Cost framework" as available; default skip preserves M10b focus.

4. **"Why didn't you also run cross-model (Sonnet, Haiku)?"** Defense: M10b is empirical hardening of M10's H2 claim, not a cost-curve milestone. Cross-model sweep is M11a (separate pre-reg, separate run number). M10b's question is "does V2-3B's failure repeat across N traces" — that question is answered with V2-3B + V2-Opus alone.

5. **"Pre-registered outcome table covers the field; what if results land between thresholds?"** Defense: P1 thresholds are at 0% / 20% / ≥40% (= 0/N_fair, 1/N_fair, 2/N_fair+) on the fair-trace subset; V2-Opus failure count splits Row 4 into 4a (V2-Opus failures > V2-3B failures) vs 4b (V2-Opus failures ≤ V2-3B failures, both > 0). With integer trace failures, every (V2-3B-failure-count, V2-Opus-failure-count) cell maps to exactly one of Rows 1/2/3/4a/4b. Edge cases (e.g., 1.5/5) cannot occur. P1 thresholds are on the fair-trace subset (N_fair, expected 5; smaller if any trace fails P3 fairness); the choice to compute on the fair subset rather than all 5 is symmetric (fairness criterion is poll-Opus ≥ 0.80, independent of V2-3B / V2-Opus performance) and pre-registered before any cell runs.

6. **"V2-3B failure mode tagging is a manual judgment call."** Defense: per-trace mechanism tagging (the "GT-regime in V2's YES enumeration?" column) is reported as observation, not as gate. The aggregate metric (V2-3B failure rate) is fully objective (count of traces with hit < 0.80). The classification is performed before reading V2-3B's hit_rate on each trace (per the per-trace structural audit step 4) — independent of V2-3B's pass/fail rather than tautologically derived from it. Pre-registered as a paper-readability annotation only.

7. **"What if test_v6+ traces are systematically harder than test_v4 / test_v5 because the banned lists keep growing?"** Defense: banned lists prohibit *recycling* prior themes/IDs/tuples; they don't reduce the space of authorable content. The fresh-session author can still pick from any out-of-enumeration regime not yet seen. M10b *does* test for this via the per-trace independent GT-regime classification + aggregate regime-distribution comparison against the dev_v2 / test_v1 / test_v2 / test_v4 / test_v5 baseline (per the aggregate-metrics §"GT-regime distribution" entry). If M10b's regimes concentrate in spaces none of the prior 5 traces touch, that itself is a publishable finding and is documented in §"Mechanism notes." A retry-cap-3 hard halt at the audit gate (per Authoring protocol step 6) further bounds the systematic-drift surface: if 3 fresh sessions can't author a non-violating trace, the protocol itself is flagged as needing M11+ revision.

8. **"You have a positive M10 close already; why do M10b at all?"** Defense: M10's H2 claim rests on n=1 external trace (test_v4). M10b converts that to n=6 aggregate (test_v4 + test_v6-10). The single most predictable reviewer attack on M10 is the "n=1 H2" reading; M10b directly addresses it for ~$5-6 and ~1-2 hours of user time. Cost-benefit overwhelmingly favors doing it before paper submission.

## Non-goals

- **No new architectural lever**. M10b reuses M10's code state verbatim (zero code changes).
- **No prompt redesign**. V2 and V3 stay frozen.
- **No cross-model sweep**. M11a scope.
- **No hierarchical routing**. M11b scope.
- **No coverage-variance estimate at scale (N=20+)**. M10b is N=5; future work scales up if reviewers push.
- **No re-running test_v3 / test_v4 / test_v5**. They stay as artifacts.
- **No edits to V2 / V3 prompts in response to M10b results**. Held-out external traces are held out; protocol converges, agent does not chase trace-specific residuals (per M10's "Protocol-failure rule").

## Authoring sessions

(Populated during Commits C1-C5. One row per fresh session.)

| trace | fresh-session timestamp | cwd | one-shot-probe response.model | /clear confirmation | audit attempt # |
|---|---|---|---|---|---|

## Rejections log

(Populated during Commits C1-C5 if any audit fails. Each rejection notes: fresh-session timestamp, first violated constraint, one-sentence description of the violation. A rejected generation is not merged; the generator code is not kept.)

## GT-regime classification

(Populated during Commits C1-C5 per the per-trace structural audit step 4. Independent classification of each GT's regime against V2's literal YES list, performed before any harness cell on that trace runs.)

| trace | GT id | content one-liner | classified regime | in V2's YES list? |
|---|---|---|---|---|

## Mechanism notes

(Populated at Commit D. Per-failure mechanism tags + aggregate GT-regime distribution comparison against dev_v2 / test_v1 / test_v2 / test_v4 / test_v5 baseline + any systematic-drift signal.)

## Results

(Populated at Commit D. Per-trace observations table + aggregate metrics + outcome-row identification + paper-line per outcome.)
