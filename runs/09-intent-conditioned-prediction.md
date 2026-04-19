# Run 09 — Intent-Conditioned Prediction (M3)

**Date:** 2026-04-18 (pre-registration); 2026-04-19 (evaluation and writeup).
**Milestone:** M3 — intent-conditioned predictor to fix predictor-latching failure identified in run 08.
**Status:** complete; pre-registered hypothesis **falsified**.
**Pre-registration SHA:** `ff063cc`. **Implementation SHA:** `547636e`. 12 evaluation cells executed from the same tree.
**Environment:** ollama 0.21.0; `qwen2.5:3b-instruct` digest `357c53fb659c5076`, `nomic-embed-text:latest` digest `0a109f422b47e3a3`. temp=0, seed=42, deterministic.

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

### Full 12-cell matrix (new runs only; existing baselines cited for context)

`tok/hit = (prompt+completion)/n_hits`. Baseline rows are carried over verbatim from runs 07 / 08 for comparison.

| Agent | dev_v2 (hit / false-h / TTN / tok/hit) | test_v1 (hit / false-h / TTN / tok/hit) | test_v2 (hit / false-h / TTN / tok/hit) |
|---|---|---|---|
| *(baseline)* HeargentZ (no intents) | 1.00 / 0.00 / 0 / 444 | 0.80 / 7.35 / 0 / 260 | **0.40** / 7.50 / 0 / 1039 |
| *(baseline)* react_poll_local (no briefing) | 1.00 / 0.00 / 0 / 7711 | 1.00 / 0.00 / 0 / 7575 | 1.00 / 0.00 / 0 / 7629 |
| **HeargentZ+intent-A (oracle)** | **1.00** / 3.50 / 0 / 530 | 0.60 / 7.35 / 0 / 829 | 0.60 / 11.25 / 0 / 812 |
| **HeargentZ+intent-B (briefing)** | 0.80 / 3.50 / 0 / 703 | **0.80** / 3.67 / 0 / 636 | **0.40** / 11.25 / 0 / 1315 |
| **HeargentZ+intent-placebo** | 0.80 / 3.50 / 0 / 693 | 0.80 / 7.35 / 0 / 665 | 0.60 / 11.25 / 0 / 875 |
| **react_poll_local+briefing** | 0.80 / 17.48 / 5 / 12084 | 0.80 / 11.02 / 15 / 10629 | 1.00 / 0.00 / 0 / 9586 |

n_hits on test_v2 for intent-B: 2/5 (fire_kitchen, water_burst). For intent-A and intent-placebo: 3/5 (A adds board_meeting; placebo adds board_meeting). Misses on test_v2 across all six new cells: er_call and security_breach are missed by every intent cell; every non-poll cell also misses either fire_kitchen (no) or the two late GTs. Poll+briefing catches all five on test_v2.

### Per-event prediction / surprise — test_v2 (the pre-registered primary)

Three intent cells on the same adversarial trace. Column `pred` is the predictor's output *at the prior tick* — i.e., the anchor against which the current observation's surprise is scored.

| t | id | role | A (oracle) | B (briefing) | placebo |
|---|---|---|---|---|---|
| 10 | daily_briefing | dist | boot 0.376 **SURF** "No notable events…" | boot 0.376 **SURF** "No notable…" | boot 0.376 **SURF** "No notable…" |
| 60 | status_ok | dist | boot 0.478 **SURF** "No notable…" | boot 0.478 **SURF** "No notable…" | boot 0.478 **SURF** "No notable…" |
| 85 | uptime_ping | dist | boot 0.467 **SURF** "No notable…" | boot 0.467 **SURF** "No notable…" | boot 0.467 **SURF** "No notable…" |
| **95** | **fire_kitchen** | **GT** | boot 0.482 **SURF** "No notable…" | boot 0.482 **SURF** "No notable…" | boot 0.482 **SURF** "No notable…" |
| **250** | **board_meeting** | **GT** | z=−1.51 0.385 **SURF** "FIRE detected in kitchen; occupants should evacuate now." | z=+0.17 0.458 "FIRE detected: evacuation order issued for household." | z=−0.89 0.412 **SURF** "FIRE detected in kitchen; evacuation order issued." |
| 350 | newsletter | dist | z=+1.23 0.495 "FIRE … evacuation order remains in effect." | z=+0.58 0.475 "FIRE detected in kitchen; evacuation ongoing." | z=+0.83 0.478 "FIRE detected in kitchen; evacuation order expected." |
| **400** | **water_burst** | **GT** | z=−1.92 0.355 **SURF** "FIRE detected in kitchen; evacuate immediately." | z=−2.76 0.355 **SURF** "FIRE detected in your kitchen; evacuate immediately." | z=−2.32 0.355 **SURF** "FIRE detected in kitchen; evacuate immediately." |
| **550** | **er_call** | **GT** | z=+1.22 0.501 "Emergency: main water line burst continues to flood…" | z=+0.80 0.481 "Emergency response team dispatched for apartment 3B flooding." | z=+1.66 0.518 "Flooded hallway cleanup scheduled for later today." |
| **750** | **security_breach** | **GT** | z=+0.31 0.460 "Emergency: main water line burst in apartment 3B…" | z=+0.85 0.487 "Emergency response team dispatched due to main water line burst." | z=+0.26 0.460 "Emergency: main water line burst in apartment 3B…" |

Three things are visible in this table:

1. **All three cells surface the same bootstrap window (t=10, 60, 85, 95).** The min_window=4 bootstrap fires before any intent-conditioned prediction has been emitted, so the first four events are surfaced regardless of intent content. One of those is a GT (fire_kitchen), three are distractors.
2. **All three cells latch on "FIRE" after fire_kitchen lands at t=95.** The intent-conditioned system prompt is effectively overridden by the recent-observation context. The predictor continues to roll forward a fire / emergency narrative whether its intent list is `[physical safety at home, board meeting, family health, account security, urgent household incidents]` (oracle), an extraction of the user's briefing (briefing), or `[garden maintenance, vegetable growth, weather conditions, cooking techniques, regional cuisine]` (placebo).
3. **Hits after bootstrap are driven by inverted-z accidents of semantic similarity to the latched prediction, not by intent relevance.** `water_burst` hits across all three cells because its content is close to the latched fire/emergency narrative and scores a strongly negative z. `board_meeting` hits under oracle and placebo but not briefing, and the reason is purely mechanical — the predictor output happens to mention "evacuate now" (oracle) or "evacuation order issued" (placebo), which is close enough to the abstract shape of an urgent interrupt to score a mild negative z; the briefing cell's anchor "evacuation order issued for household" scores marginally *higher* cosine distance from the board-meeting string and fails the gate. Neither the oracle intent "scheduled work meetings and board sessions" nor any other concept in any intent list is doing work here. `er_call` and `security_breach` miss in every intent cell because by t=550 / t=750 the predictor has latched on water-burst language, and neither ER-call nor account-breach content aligns.

The mechanism from run 08 — **per-event polarity flipping driven by predictor latching on recent observations** — is untouched by intent-conditioning.

### Pre-registered success criteria

Each criterion is evaluated verbatim against the rule frozen before any eval run. Post-hoc rationalisation is not permitted at this step.

**Criterion 1 — Primary (test_v2): Intent-B hit ≥ 0.80 AND false/h ≤ 18.75.**
Result: **FAIL.** Intent-B on test_v2 scored hit=0.40, false/h=11.25. Hit rate is exactly the same as the plain HeargentZ baseline from run 08 (0.40). The failure mode we set out to fix is unchanged.

**Criterion 2 — No regression (dev_v2, test_v1): Intent-B hit ≥ HeargentZ hit − 0.20 on each.**
Result: **PASS** (both). Intent-B dev_v2=0.80 vs HeargentZ 1.00 → Δ = −0.20, exactly at the tolerance boundary. Intent-B test_v1=0.80 vs HeargentZ 0.80 → Δ = 0. Intent-conditioning did not break the two traces where the plain gate already worked, but on dev_v2 it sits at the edge of the tolerance and the single missed event is `dentist_cancel` (z=+0.02; the extractor's "Medical appointments" intent did not prevent latching on the flight-delay narrative — see Design reasoning below for why this is a weaker signal than it looks).

**Criterion 3 — Signal over polling cost: Intent-B tok/hit on test_v2 < react_poll_local+briefing tok/hit on test_v2.**
Result: **PASS (vacuously).** Intent-B = 1315 tok/hit < poll+briefing = 9586 tok/hit. But this comparison is moot: poll+briefing hits 1.00 on test_v2, intent-B hits 0.40. Beating a 2.5×-stronger baseline on cost-per-correct-proaction when you catch 40% vs 100% is not a meaningful cost win. Reported as PASS because that is what the criterion literally says; flagged here as not interpretively load-bearing.

**Criterion 4 — Ceiling check (A vs B on test_v2).** The pre-reg rule: *"If A succeeds and B fails → bottleneck is extraction. If both fail → intent-conditioning is not the answer; pivot to the surprise+content arbiter flagged at run 08."*
Result: **Both fail.** Intent-A on test_v2 = 0.60, Intent-B on test_v2 = 0.40. Neither reaches the 0.80 success bar. Per the pre-registered decision rule, **the pivot signal fires: intent-conditioning is not the mechanism, and the next step is the surprise + lightweight-content arbiter, not a better extractor or richer briefing.**

**Criterion 5 — Placebo-null: placebo hit on test_v2 strictly less than B's by ≥ 0.20.**
Result: **FAIL, in the opposite direction.** Placebo test_v2 = 0.60, B test_v2 = 0.40. **Placebo is 0.20 higher than B, not 0.20 lower.** The pre-reg rule for this outcome was: *"If placebo matches or beats B, the intent content is not load-bearing and we cannot claim intent-conditioning as the mechanism."* That rule fires. Intent content is not load-bearing; the agent does roughly the same thing whether its anchor text is user-relevant or about vegetable gardens.

**Summary: criteria 1, 4, 5 fail; 2, 3 pass; 4's pre-registered decision rule says pivot.** Three of five fail — including the primary and the placebo-null — which is a cleanly falsified pre-registration. The plan's option-4 exit path activates: surprise + lightweight-content arbiter, not intent-conditioned prediction, is the next architectural bet.

### Headline findings

1. **M3 is falsified on the primary test_v2 hypothesis.** The adversarial trace's 0.40 hit rate from run 08 is unchanged under intent-conditioning with a realistic briefing. The mechanism we pre-registered as the fix does not fix it.

2. **The placebo-null fails in the opposite direction.** Off-topic intents (gardening / Premier League / Italian cookbook) produce a *higher* hit rate on test_v2 than the user-relevant briefing extraction (0.60 vs 0.40). Intent content is not load-bearing; the predictor is not using the intents as a stable anchor, it is mostly ignoring them and conditioning on the last few observations.

3. **The mechanism: intent-conditioning does not prevent latching.** Per-event logs on test_v2 show all three intent cells produce the same post-fire predictions ("FIRE detected in kitchen; evacuate…"). The system-prompt intent list is overridden by recent-observation context inside the 3B predictor. The same failure mode identified in run 08 (predictor latching → per-event polarity instability) is present unchanged in all six new intent-conditioned cells.

4. **Where intent content *does* seem to help, the effect is confounded with "the predictor refuses to latch."** The placebo predictor on dev_v2 and test_v1 outputs `"No notable events expected in the next minute."` on every tick, because no observation matches the garden/cooking intents strongly enough to force a specific prediction. That stable null baseline produces a cleaner surprise distribution than a latched hallucination. So the placebo-matches-oracle result is not "garden intents are secretly useful" — it's "refusing to latch is better than latching on the wrong thing", which is a finding about the predictor, not about intents.

5. **Intent-A (oracle) hits 1.00 on dev_v2 but at worse false/h than plain HeargentZ.** Oracle dev_v2: 1.00 / 3.50 / 530 vs plain HeargentZ dev_v2: 1.00 / 0.00 / 444. Oracle adds one false initiation without gaining any GT coverage, and is 1.2× more expensive per hit. There is no dev_v2 configuration where any intent cell Pareto-dominates plain HeargentZ.

### Post-hoc finding (not pre-registered) — briefing degrades the poll baseline

A surprise in the opposite direction: the `react_poll_local+briefing` cells do *worse* than plain `react_poll_local`:

| Trace | poll (no briefing, run 07/08) | poll+briefing (new) |
|---|---|---|
| dev_v2 | 1.00 / 0.00 / 0 / 7711 | 0.80 / 17.48 / 5 / 12084 |
| test_v1 | 1.00 / 0.00 / 0 / 7575 | 0.80 / 11.02 / 15 / 10629 |
| test_v2 | 1.00 / 0.00 / 0 / 7629 | 1.00 / 0.00 / 0 / 9586 |

On dev_v2 and test_v1 the briefing causes the 3B poller to both miss one previously-caught GT and manufacture new false initiations, while also spending ≈40–60 % more tokens per hit. On test_v2 the briefing is null (the adversarial GTs are strong enough that the poller surfaces them regardless). **This is a real anti-result for the "give the agent user context" narrative that motivated M3**, and it cuts at both ends of the proposed design space: the local-LLM poller does not benefit from a plain-text briefing in the prompt any more than HeargentZ benefits from an extracted intent list.

This is marked post-hoc because it was not a pre-registered test — the poll+briefing cells were included in the matrix specifically to prevent an unfair "heargent has the briefing, poll doesn't" comparison, not to test whether briefings help poll. The result is consistent with criterion 5's finding that briefing content is not helping anywhere.

### What this means for M3 and what comes next

The pre-reg option-4 exit fires. The next step is **not** a better extractor, richer briefing, larger predictor, or Reflect-based dynamic intent maintenance (C). The data says the gate itself — single-step embedding surprise against a latching 3B predictor — is the bottleneck, and anchoring the predictor in a persistent intent list does not unlock it. The M3 hypothesis is falsified in the clean pre-registered sense.

The remaining candidates, in descending priority:

1. **Surprise + lightweight content arbiter.** Use HeargentZ's |z| signal as a cheap first stage; when |z| is borderline (say |z| ∈ [0.5, 1.5]), call a second 3B model with a short "is this worth surfacing?" classifier prompt that sees the event content directly. Cost is bounded: poll pays for one call per tick; the arbiter pays for one call per *borderline* event, of which there are few per trace. Poll's 7.6 k tok/hit is probably beatable by ~3×. This is the next session's primary bet.

2. **Larger predictor (7–13 B).** A larger local model might resist latching more robustly and produce a predictor that honors intent-conditioning. Useful as a sanity check that the falsification isn't purely a 3B property, but expensive enough that it should only run if the arbiter approach also underperforms.

3. **Reflect-based dynamic intents (option C, from the plan).** Still on the table but lower priority: if static intents didn't help, dynamic ones on top of the same latching predictor are unlikely to save it. Defer until the arbiter is scored.

`heargent-plan.md` milestone language: M3 closes as falsified; M4 becomes "surprise + content arbiter vs poll Pareto on test_v2".

## Reproduce

Ollama 0.21.0 must be running locally with `qwen2.5:3b-instruct` and `nomic-embed-text` pulled. All runs are deterministic (temp=0, seed=42).

```sh
# Intent-A (oracle) × 3 traces
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace dev_v2  --intent-mode oracle   --out runs/data/09a-intent-oracle-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace test_v1 --intent-mode oracle   --out runs/data/09e-intent-oracle-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace test_v2 --intent-mode oracle   --out runs/data/09i-intent-oracle-test_v2.json

# Intent-B (briefing) × 3 traces
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace dev_v2  --intent-mode briefing --out runs/data/09b-intent-briefing-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace test_v1 --intent-mode briefing --out runs/data/09f-intent-briefing-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace test_v2 --intent-mode briefing --out runs/data/09j-intent-briefing-test_v2.json

# Intent-placebo × 3 traces
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace dev_v2  --intent-mode placebo  --out runs/data/09c-intent-placebo-dev_v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace test_v1 --intent-mode placebo  --out runs/data/09g-intent-placebo-test_v1.json
uv run python -m eval.run_trace --agent agent.loop:HeargentZIntent --trace test_v2 --intent-mode placebo  --out runs/data/09k-intent-placebo-test_v2.json

# react_poll_local + briefing × 3 traces
uv run python -m eval.run_trace --agent baselines.react_poll_local:ReactPollLocal --trace dev_v2  --with-briefing --out runs/data/09d-poll-briefing-dev_v2.json
uv run python -m eval.run_trace --agent baselines.react_poll_local:ReactPollLocal --trace test_v1 --with-briefing --out runs/data/09h-poll-briefing-test_v1.json
uv run python -m eval.run_trace --agent baselines.react_poll_local:ReactPollLocal --trace test_v2 --with-briefing --out runs/data/09l-poll-briefing-test_v2.json
```

## Artifacts

- `runs/data/09a-intent-oracle-dev_v2.json` … `09l-poll-briefing-test_v2.json` — full 12-cell matrix.
- Every JSON contains `intents` (extracted or oracle list, where applicable), `surprise_log` (per-event prediction/observation/surprise/z/surfaced tuples), `llm_stats` (calls / prompt_tokens / completion_tokens), and standard eval scoring (hit_rate / false_initiation_rate_per_hour / median_time_to_notice_s / hits / misses).
- Baselines cited for comparison: `runs/data/07c-heargent-comparison.json`, `runs/data/08f-heargent-z-sweep-test_v2.json` (HeargentZ rows), `runs/data/07a-poll-dev_v2.json`, `runs/data/07b-poll-test_v1.json`, `runs/data/08d-poll-test_v2.json` (plain poll rows).
- Code: `agent/loop.py::HeargentZIntent`, `agent/intent_extractor.py`, `agent/predictor.py::Predictor.predict(..., intents=())`, `sandbox/event_trace.py::Trace.briefing` + `Trace.intents`, `baselines/react_poll_local.py::ReactPollLocal.from_trace(..., with_briefing=True)`. All committed at `547636e`; no code changes between pre-registration and eval.
