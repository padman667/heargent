# heargent — Progress Index

Central place to review outcomes. Every work session produces a numbered markdown in this folder (`01-…`, `02-…`, …) documenting what was built, the exact commands used, raw JSON results, and interpretation. Raw metric JSONs are under `runs/data/`.

- **Plan**: [`../heargent-plan.md`](../heargent-plan.md) — project thesis, v1 architecture, evaluation strategy, risks, milestones.
- **Reference**: [`../hearbeat-agent.pdf`](../hearbeat-agent.pdf) — Hong Su's original paper.

---

## Current status (as of 2026-04-19)

**Milestone:** M4 — surprise + lightweight-content arbiter pre-registered, executed, **partially validated**. Criterion 1 (primary test_v2 recovery) passes strongly and criterion 3 (random-arbiter ablation) confirms the content signal is load-bearing; criterion 2 (no-regression on regime-aligned traces) fails cleanly.
**Next:** M5 — regime-robust arbiter prompt. The pre-registered prompt's reading of "imminent action required" is too strict on within-24-hour scheduling phrasings, regressing dev_v2 / test_v1 while winning test_v2 outright. M5 re-pre-registers a broader prompt and re-runs the three-trace matrix with a fresh random ablation.
**Tooling:** ollama 0.21 + `qwen2.5:3b-instruct` (predictor + arbiter, temp=0/seed=42, deterministic) + `nomic-embed-text` (surprise).

### Headline Pareto (frozen hyperparameters, no per-trace tuning)

| Agent | dev_v2 (hit / false-h / TTN / tok/hit) | test_v1 (hit / false-h / TTN / tok/hit) | test_v2 (hit / false-h / TTN / tok/hit) |
|---|---|---|---|
| cron 30 s | 0.80 / 17.48 / 0 / 0 | 0.80 / 18.37 / 10 / 0 | 0.80 / 18.75 / 0 / 0 |
| HeargentZ z_thr=0.0 inverted (frozen on dev_v2) | 1.00 / 0.00 / 0 / 444 | 0.80 / 7.35 / 0 / 260 | 0.40 / 7.50 / 0 / 1039 |
| **HeargentZA (content arbiter, M4)** | 0.60 / 0.00 / 0 / 984 | 0.40 / 3.67 / 0 / 1674 | **0.80 / 0.00 / 0 / 770** |
| react_poll_local (strong baseline) | 1.00 / 0.00 / 0 / 7711 | 1.00 / 0.00 / 0 / 7575 | 1.00 / 0.00 / 0 / 7629 |

- **On test_v2 (adversarial trace), HeargentZA strictly Pareto-dominates plain HeargentZ**: hit 0.40 → 0.80 (cron-matching), false/h 7.50 → 0.00 (poll-matching), tok/hit 1039 → 770. Against poll on the same trace: 0.80 hit vs 1.00 at **10.0× lower token cost per correct proaction**. The random-arbiter null ablation with matched YES-rate p = 0.25 scores 0.60 / 3.75 on test_v2 — the content signal is load-bearing, not a firing-rate trick.
- **On dev_v2 and test_v1 (regime-aligned traces), HeargentZA regresses** because the bootstrap-phase arbiter reads within-24-hour scheduling phrasings ("flight delayed tomorrow", "meeting moved to 14:00", "rent due in 2 days") as non-urgent and skips them. Isolation probe before eval confirmed 0/5 dev-trace GTs classified YES vs 5/5 test_v2 GTs; the matrix was still run unchanged, per frozen-config discipline.
- **Regime-selective result.** The same arbiter prompt that delivers the cleanest test_v2 number to date regresses the two traces where plain HeargentZ was already working. No single-config frozen prompt under this design wins all three; the trade-off surface is the arbiter's YES-policy wording.
- **Honest paper framing:** *Content-arbitered surprise gating recovers adversarial-regime performance (poll-matching quality at 10× lower cost) at a pre-registered cost to regime-aligned traces; the arbiter's decision boundary between "right-now urgency" and "24-hour scheduling" is a documented trade-off surface, and addressing it is an M5-pre-registered scope item.*

---

## Runs

| # | Date | Focus | Key finding |
|---|---|---|---|
| [01](01-reactive-baseline-sanity.md) | 2026-04-18 | First end-to-end pipeline run. Reactive floor baseline on `dev_trace_v1`. | Pipeline works; reactive agent correctly scores zero. Pipeline validated for misses only. |
| [02](02-cron-keyword-sweep.md) | 2026-04-18 | Non-LLM cron baseline at 30 s and 300 s on `dev_trace_v1`. | True-positive path validated (all hits). **But trace was too easy** — both intervals hit 100 %. Triggered decision to harden trace. |
| [03](03-cron-v2-sweep.md) | 2026-04-18 | `dev_trace_v2` introduced (tight windows + distractors). Cron sweep re-run. | First real Pareto shape. False-initiation path now non-zero. Cron 300 s dominated. `fire_alarm` is the discriminative case. |
| [04](04-heargent-v1.md) | 2026-04-18 | heargent v1 end-to-end (qwen2.5:3b predictor + nomic-embed surprise gate) on dev_v2. | **hit_rate=1.0, fire_alarm TTN=0.** Pareto-dominates all cron baselines. But θ=0.30 surfaces all distractors too — surprise alone doesn't separate signal from noise on this trace. |
| [05](05-sweep-ablation.md) | 2026-04-18 | Determinism check, θ sweep, random-gate ablation, polarity flip on dev_v2. | **Forward gate falsified** (random matches/beats it). **But inverted gate at θ=0.43 hits 1.00 / 0.00 false / TTN=0** — strict Pareto optimum across all agents. Polarity opposite of FEP-naïve reading. Needs held-out trace to confirm. |
| [06](06-test_v1-generalization.md) | 2026-04-18 | New held-out `test_v1` trace; full battery rerun. Server_outage event constructed to be unwinnable for cron 30s. | **Polarity sign generalizes** (GT mean surprise < distractor mean on both traces). **Magnitude does not** (test_v1 has interleaved distributions, no perfect classifier). Inverted heargent θ=0.58 strictly Pareto-dominates cron 30s on hit/false/TTN. Inverted θ=0.50 dominates matched random-gate on both axes — surprise signal is load-bearing. dev-best θ does not transfer; need a θ-selection rule. |
| [07](07-frozen-transfer-and-poll.md) | 2026-04-18 | HeargentZ (rolling-window z-score gate) for transfer; `react_poll_local` strong baseline; first cost-per-correct-proaction numbers. | **Pre-registered frozen z_thr=0.0 transfers to test_v1 at hit=0.80** (abs-θ collapsed to 0.40). **Poll is quality ceiling (1.00/0.00 on both traces) but at 17–29× more tokens per hit than frozen HeargentZ.** Paper-shaped v1 story: selective initiation at near-ceiling quality, ≈20× cheaper. |
| [08](08-test_v2-adversarial.md) | 2026-04-18 | Adversarial `test_v2`: distractors = calm routine, GT = abrupt interruptions. Polarity-flip stress test. | **Polarity-flip falsified.** Frozen inverted z_thr=0.0 collapses to hit=0.40. Forward gate gets 0.60 (catches different GT subset). Polarity-agnostic \|z\| hits 1.00 but matches random p=1.0 — no signal. Mechanism: predictor latches on dominant surface narrative, per-event polarity becomes unstable. Poll is the only agent that wins this trace (1.00/0.00/0 at 7629 tok/hit). v1 thesis confirmed in regime-aligned traces, falsified on adversarial split — intent-conditioned prediction is now the next required step. |
| [09](09-intent-conditioned-prediction.md) | 2026-04-19 | Pre-registered M3 intent-conditioned predictor (oracle A, briefing-extracted B, placebo) × 3 traces + poll+briefing × 3. 12 new cells, frozen config. | **M3 falsified.** Intent-B on test_v2 hit=0.40 (unchanged from run-08 baseline); primary criterion fails. **Placebo hit=0.60 > briefing hit=0.40** on test_v2 — criterion 5 placebo-null fails hard, intent content is not load-bearing. Per-event logs show all three intent cells latch on "FIRE…" after fire_kitchen regardless of intent list (oracle / briefing / gardening). Pre-registered option-4 exit fires: pivot to surprise + lightweight-content arbiter for M4. Post-hoc: poll+briefing degrades plain poll on dev_v2 / test_v1 (hit 1.00→0.80, false/h 0.00→17.48 on dev_v2). |
| [10](10-surprise-content-arbiter.md) | 2026-04-19 | Pre-registered M4 HeargentZ + content arbiter (three-way gate: `z < −0.5` auto-surf, `z > +1.0` auto-skip, otherwise + bootstrap → 3B YES/NO classifier on event content only). 3 content cells + 3 matched-firing-rate random-arbiter ablation cells, frozen config. | **M4 partially validated.** Primary (test_v2 hit ≥ 0.80 AND tok/hit < poll's 7629): **PASS** — HeargentZA test_v2 = 0.80 / 0.00 / 770, strictly Pareto-dominant over plain HeargentZ (0.40 / 7.50 / 1039) and 10× cheaper than poll at matching quality. Arbiter-content load-bearing vs random: **PASS** (Δhit = 0.20). **No-regression: FAIL** on both dev_v2 (1.00 → 0.60) and test_v1 (0.80 → 0.40) — the arbiter's narrow reading of "imminent action required" skips "tomorrow" and "in-24-hours" scheduling phrasings. Regime-selective win; next session re-pre-registers a broader-prompt variant. |

---

## Folder layout

```
heargent/
├── heargent-plan.md              ← the plan (read this first)
├── hearbeat-agent.pdf            ← reference paper
├── sandbox/
│   ├── world.py                  ← World/Event/Notification + observe/advance/surface
│   └── event_trace.py            ← Trace type, dev_trace_v1, dev_trace_v2
├── eval/
│   └── run_trace.py              ← harness + scoring + CLI (--agent, --trace, --out)
├── baselines/
│   ├── react_reactive.py         ← floor
│   └── react_cron_keyword.py     ← structural cron (no LLM)
├── agent/
│   ├── llm.py                    ← OllamaClient (stdlib HTTP) + LLMStats
│   ├── predictor.py              ← qwen2.5:3b-instruct one-sentence predictions
│   ├── surprise.py               ← nomic-embed-text cosine-distance surprise
│   ├── intent_extractor.py       ← briefing → intent list (M3, qwen2.5:3b)
│   ├── arbiter.py                ← ContentArbiter + RandomArbiter (M4)
│   └── loop.py                   ← HeargentAgent / HeargentZ / HeargentZIntent / HeargentZA
├── runs/
│   ├── README.md                 ← this file
│   ├── 01-reactive-baseline-sanity.md
│   ├── 02-cron-keyword-sweep.md
│   ├── 03-cron-v2-sweep.md
│   ├── 04-heargent-v1.md
│   ├── 05-sweep-ablation.md
│   ├── 06-test_v1-generalization.md
│   ├── 07-frozen-transfer-and-poll.md
│   ├── 08-test_v2-adversarial.md
│   └── data/                     ← raw metrics JSON per run
└── pyproject.toml
```

---

## How to read a run doc

Each numbered run follows the same sections so you can scan them quickly:

1. **Goal** — why this session was run.
2. **Commands** — exact shell commands (copy-paste reproducible).
3. **Results** — summary table and raw JSON verbatim.
4. **What this validates** — what the pipeline is now known to do correctly.
5. **Still untested / what this surfaces** — open problems and decisions.
6. **Next session** — concrete follow-ups.

If you want to verify a result yourself, the raw JSON is in `runs/data/` and every run doc shows the exact `uv run python -m eval.run_trace …` command that produced it.

---

## Reproducing everything from scratch

```sh
# fresh checkout
uv sync                                    # creates .venv, installs deps

# regenerate all published runs
uv run python -m eval.run_trace --agent baselines.react_reactive:ReactiveAgent       --trace dev_v1 --out runs/data/01-reactive-v1.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s  --trace dev_v1 --out runs/data/02a-cron-30s.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword300s --trace dev_v1 --out runs/data/02b-cron-300s.json
uv run python -m eval.run_trace --agent baselines.react_reactive:ReactiveAgent       --trace dev_v2 --out runs/data/03a-reactive-v2.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword30s  --trace dev_v2 --out runs/data/03b-cron30-v2.json
uv run python -m eval.run_trace --agent baselines.react_cron_keyword:CronKeyword300s --trace dev_v2 --out runs/data/03c-cron300-v2.json
uv run python -m eval.run_trace --agent agent.loop:HeargentV1                        --trace dev_v2 --out runs/data/04-heargent-v1-dev_v2.json
```

**Note:** run 04 depends on ollama 0.21 running locally with `qwen2.5:3b-instruct` and `nomic-embed-text` pulled. It is **not** bit-deterministic because the predictor runs at temperature 0.4 — re-runs will produce similar but not identical surprise values. Temperature-0 deterministic re-run is on the list for the next session.

All runs are deterministic (no RNG, no LLM yet), so re-running should produce bit-identical JSON.
