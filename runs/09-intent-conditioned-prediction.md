# Run 09 — Intent-Conditioned Prediction (M3)

**Date:** 2026-04-18
**Milestone:** M3 — intent-conditioned predictor to fix predictor-latching failure identified in run 08.
**Status:** pre-registered; eval runs pending.

## Goal

Test whether giving the predictor a stable anchor in "what the user cares about" fixes the test_v2 predictor-latching failure (hit=0.40 with frozen inverted gate) *without regressing* the dev_v2 / test_v1 wins (hit=1.00 / 0.80). The mechanism under test: an intent list, prepended into the predictor's system prompt on every tick, keeps the baseline prediction anchored in user-life-relevant semantic space instead of drifting with whatever surface narrative dominated the last few observations.

## Design reasoning (why B+A+placebo, not alternatives)

The key M3 design decision was how intents enter the system. Three candidates:

1. **A — pre-seeded per trace (oracle):** trace author hand-writes intents. Simple, deterministic, zero extra LLM calls. But the trace author has hindsight knowledge of GT events, so A as a standalone result invites the "you cherry-picked intents" objection.
2. **B — LLM-extracted from a t=0 user briefing event (realistic):** one natural-language briefing per trace, extracted once into an intent list by qwen2.5:3b at temp=0. Models the realistic information channel (users brief assistants). The briefing text is a new knob — must be written without GT-event-specific keywords to avoid leakage.
3. **C — maintained via Act/Reflect (dynamic):** intent stack updated during the trace by a Reflect step. Matches the original heargent-plan.md architecture. Adds two unvalidated subsystems (intent-conditioning + reflection) simultaneously.

**Chosen: B as primary, A as oracle ceiling, C deferred to M4+.**

Rationale:
- A alone is too easy to attack ("oracle"). B alone leaves a gap ("what if extraction is the bottleneck?"). The B-minus-plain-HeargentZ delta attributes the effect to intent-conditioning; the A-minus-B delta attributes the gap to extraction quality. Cleaner scientific story than either alone.
- C now would confound two changes in one run. The failure mode from run 08 (predictor latching within ~750s) is answerable with a *static* intent list; dynamic maintenance is an extension, not a prerequisite.

**Plus one placebo-intent ablation.** Same pipeline as B, but fed a briefing about irrelevant topics (gardening, Premier League, Italian cookbook). If the placebo agent matches B on hit rate, the predictor is just responding to "having any anchor text," not user-relevant anchoring — and the intent-conditioning story collapses. This is directly analogous to run 05's random-gate ablation that established surprise was load-bearing.

**Local-only for M3.** qwen2.5:3b-instruct handles both prediction and briefing extraction; nomic-embed-text handles surprise. No Claude API yet — Claude enters at M4 for Act/Reflect escalation and LLM-judge false-initiation scoring, both deferred. Keeping M3 local also preserves the "cheap local stack is sufficient" paper story — mixing Claude into extraction would muddy the cost ledger.

## Pre-registered artifacts (frozen before any eval run)

Everything in this section is written, committed, and not changed after eval begins. Any post-hoc modification is a protocol deviation and will be called out explicitly.

### Briefings per trace (option B input)

Each briefing is a single natural-language message the user would plausibly say at t=0. Briefings describe **user life context at the abstraction level a friend would use** — they must not contain GT-event-specific keywords (e.g. no "fire", "alarm", "delay", "cancelled", "outage", "500 errors", "burst", "ER", "breach"). Thematic overlap (e.g. "travel", "on-call", "family") is intentional and is what the intent-conditioning is meant to exploit.

**dev_v2 briefing:**
> "Normal workday at the office. I've got a trip to Berlin later this week for some design review prep, the quarterly report is hanging over me, and I've got a couple of personal medical appointments squeezed into the calendar. Flag anything that actually needs my attention."

*Thematic coverage vs GT:* office presence (fire_alarm), travel (flight_delay), work reviews (meeting_moved), work deliverable (deadline), personal medical (dentist_cancel).

**test_v1 briefing:**
> "On-call for the production rotation today. Waiting on some health follow-ups, got home-logistics stuff in progress, my son is at school for the usual day, and the monthly household bills are coming due soon."

*Thematic coverage vs GT:* on-call / production (server_outage), health (doctor_callback), home logistics (package_arrival), kid at school (kid_school_pickup), bills (rent_due).

**test_v2 briefing:**
> "Working from home today. There's a quarterly board session on the calendar, my mother has some ongoing medical stuff I'm keeping tabs on, and there's been some flaky login behavior on my accounts. Flag urgent."

*Thematic coverage vs GT:* home presence (fire_kitchen, water_burst), work meetings (board_meeting), family health (er_call), account security (security_breach).

### Placebo briefing (same across all three traces)

> "I'm trying to keep up with my vegetable garden this spring, following the Premier League title race, and I've been cooking my way through an Italian regional cookbook on weekends. Flag anything relevant."

No thematic overlap with any GT event on any of the three traces. Used to control for the "any anchor text helps" null.

### Extraction system prompt

```
You extract a small set of the user's active concerns from a brief personal
statement. Output a numbered list of 3 to 6 short phrases (max 10 words each),
each describing one thematic concern the user would want a proactive assistant
to monitor on their behalf. Keep phrases abstract (themes, not specific events).
No invented details not present in the briefing. Output only the numbered list,
one concern per line, nothing else.
```

Extraction user message (template):
```
User briefing:
{briefing_text}

Themes to monitor:
```

Model: qwen2.5:3b-instruct. temperature=0.0, seed=42, max_tokens=200. Parsed by stripping numbering and whitespace; any line containing no alphanumeric content is dropped. Resulting intents are frozen for the remainder of the trace.

### Intent-conditioned prediction system prompt

```
You are a prediction module for a proactive assistant.

The user's active concerns today are:
{intents_as_bulleted_list}

Given recent observations, output EXACTLY ONE SHORT SENTENCE (under 20 words)
describing the next notable event you expect that would be relevant to any of
those concerns. If nothing notable is expected, reply exactly: "No notable
events expected in the next minute."

No preamble, no reasoning, no lists, no quotes. Output only the sentence.
```

User message: unchanged from the current `Predictor.predict` (recent observations block + current sim_time + "One-sentence prediction of the next notable event:").

Model: qwen2.5:3b-instruct. temperature=0.0, seed=42, max_tokens=50. Exactly matches the current predictor except for the system prompt.

### Option A intents (oracle ceiling)

Hand-written by trace author *at the same abstraction level as option B extracts* (themes, not event keywords). Written here before any eval run, so A's intent lists are frozen.

**dev_v2 (A):**
1. physical safety while at the office
2. upcoming international travel plans
3. work meetings and design reviews
4. quarterly work deliverables and deadlines
5. personal medical appointments

**test_v1 (A):**
1. production on-call responsibilities
2. personal health follow-ups
3. household deliveries and logistics
4. child's school day
5. monthly household bills

**test_v2 (A):**
1. physical safety at home
2. scheduled work meetings and board sessions
3. family member health
4. account and login security
5. urgent household incidents

### Frozen agent config

All six new agent cells use:
- **Gate:** inverted z-score, `z_threshold=0.0`, rolling window size 16, min_window 4. Identical to `HeargentZ` in run 08 except for the predictor's system prompt.
- **Predictor:** qwen2.5:3b-instruct, temperature=0.0, seed=42.
- **Surprise scorer:** nomic-embed-text (unchanged).
- **No per-trace tuning.** One config, three traces.

### Pre-registered success criteria

1. **Primary (test_v2):** HeargentZ+intent-B hit rate ≥ 0.80 **and** false/h ≤ 18.75 (cron 30 s). This is the failure mode we're trying to fix. Meeting this makes M3 a success headline.
2. **No regression (dev_v2, test_v1):** HeargentZ+intent-B hit rate ≥ HeargentZ hit rate − 0.20 on each. Intent-conditioning must not break the traces where the plain gate already works.
3. **Signal over polling cost:** HeargentZ+intent-B tok/hit on test_v2 < react_poll_local+briefing tok/hit. The paper premise is "cheaper than polling"; losing that on test_v2 kills the story even if hit rate recovers.
4. **Ceiling check (A vs B):** if A succeeds and B fails on test_v2 → the bottleneck is extraction, not the mechanism; next step is a better extractor or richer briefing. If both fail → intent-conditioning is not the answer; pivot to the surprise+content arbiter flagged at the end of run 08.
5. **Placebo-null:** placebo agent hit rate on test_v2 strictly less than B's hit rate by ≥ 0.20. If placebo matches or beats B, the intent content is not load-bearing and we cannot claim intent-conditioning as the mechanism.

Any headline claim from this run must cite which of these criteria it passed or failed, verbatim.

## Evaluation matrix

Frozen config on every cell. Each cell = one run, one JSON output in `runs/data/09-*.json`.

| Agent | dev_v2 | test_v1 | test_v2 |
|---|---|---|---|
| cron 30 s | (existing, run 02/03/08) | (existing, run 06) | (existing, run 08) |
| HeargentZ (no intents, frozen) | (existing, run 07) | (existing, run 07) | (existing, run 08) |
| react_poll_local (no briefing) | (existing, run 07) | (existing, run 07) | (existing, run 08) |
| **HeargentZ+intent-A (oracle)** | new | new | new |
| **HeargentZ+intent-B (briefing)** | new | new | new |
| **HeargentZ+intent-placebo** | new | new | new |
| **react_poll_local+briefing** | new | new | new |

12 new runs. Existing runs re-cited, not re-executed.

Each new JSON includes: git commit SHA (pre-registration commit), ollama version, model digests for `qwen2.5:3b-instruct` and `nomic-embed-text`, per-event `(prediction, observation, surprise, z, surfaced)` dumps identical in schema to run-08.

## Architecture changes (additive only)

1. `sandbox/event_trace.py` — optional `intents: tuple[str, ...]` field on `Trace`. Default `()` preserves existing trace signatures.
2. `agent/predictor.py` — `Predictor.predict(history, sim_time, intents=())`. When intents non-empty, the intent-conditioned system prompt above is used; otherwise the existing system prompt. One code path, one extra conditional.
3. `agent/intent_extractor.py` (new file) — `extract_intents(client, briefing_text) -> tuple[str, ...]` implementing the extraction prompt above. One-shot call, no retry, deterministic.
4. `agent/loop.py` — `HeargentZIntent(intent_source)` class. `intent_source` is either a static `tuple[str, ...]` (option A / placebo) or a callable that extracts from a briefing (option B). Gate logic, window, z-threshold all identical to `HeargentZ`.
5. `eval/run_trace.py` — thread the intent source through to agent init. No changes to scoring or world harness.

No changes to baselines, cron, `HeargentZ` (no-intent), or the gate logic itself. If run 09 falsifies the approach, reverting is a one-class delete.

## Results

*(To be filled in after the 12 evaluation cells run. Results section will include: full results table, per-event prediction/surprise dumps for the six intent-conditioned cells, pass/fail against each pre-registered success criterion, headline interpretation, and any post-hoc observations clearly marked as post-hoc.)*

## Reproduce

*(Exact `uv run python -m eval.run_trace ...` commands will be listed here after the runs complete.)*

## Artifacts

*(`runs/data/09-*.json` paths listed after runs complete.)*
