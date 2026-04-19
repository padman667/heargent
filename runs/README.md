# heargent — Progress Index

Central place to review outcomes. Every work session produces a numbered markdown in this folder (`01-…`, `02-…`, …) documenting what was built, the exact commands used, raw JSON results, and interpretation. Raw metric JSONs are under `runs/data/`.

- **Plan**: [`../heargent-plan.md`](../heargent-plan.md) — project thesis, v1 architecture, evaluation strategy, risks, milestones.
- **Reference**: [`../hearbeat-agent.pdf`](../hearbeat-agent.pdf) — Hong Su's original paper.

---

## Current status (as of 2026-04-19)

**Milestone:** M3 — intent-conditioned predictor pre-registered, executed, **falsified** on the primary test_v2 hypothesis. Pre-reg success criteria 1 (primary), 4 (A-vs-B ceiling), and 5 (placebo-null) all fail; the pre-registered option-4 exit fires.
**Next:** surprise + lightweight-content arbiter on test_v2 (M4). Intent-conditioning via system-prompt anchor is off the table — placebo intents (gardening / Premier League) beat briefing-extracted intents on test_v2, so intent content is not load-bearing; the 3B predictor latches on recent observations regardless of what the intent list says.
**Tooling:** ollama 0.21 + `qwen2.5:3b-instruct` (predictor + poll + intent extractor, temp=0/seed=42, deterministic) + `nomic-embed-text` (surprise).

### Headline Pareto (frozen hyperparameters, no per-trace tuning)

| Agent | dev_v2 (hit / false-h / TTN / tok/hit) | test_v1 (hit / false-h / TTN / tok/hit) | test_v2 (hit / false-h / TTN / tok/hit) |
|---|---|---|---|
| cron 30 s | 0.80 / 17.48 / 0 / 0 | 0.80 / 18.37 / 10 / 0 | 0.80 / 18.75 / 0 / 0 |
| **HeargentZ z_thr=0.0 inverted (frozen on dev_v2)** | **1.00 / 0.00 / 0 / 444** | **0.80 / 7.35 / 0 / 260** | **0.40 / 7.50 / 0 / 1039** |
| react_poll_local (strong baseline) | 1.00 / 0.00 / 0 / 7711 | 1.00 / 0.00 / 0 / 7575 | 1.00 / 0.00 / 0 / 7629 |

- **Two traces (dev_v2, test_v1)** — both with "human-relevant GT vs system-noise distractors" structure: HeargentZ matches poll quality at 17–29× lower cost. Clean v1 story.
- **One trace (test_v2)** — adversarial: distractors are mundane routine, GT events are abrupt interruptions of varying semantic distance to the rolling prediction. **Frozen inverted gate collapses to hit=0.40.** Forward gate hits 0.60. Polarity-agnostic |z| gate hits 1.00 but matches random p=1.0 (no signal). Cron 30 s outperforms heargent on hit rate.
- **Polarity flip is regime-dependent**, not universal: it holds where GT and distractors occupy structurally distinct semantic spaces; it falsifies when they overlap. Predictor latching (the predictor anchors on whatever surface narrative dominates the last few observations) is the underlying failure mechanism.
- **Poll remains the only quality-ceiling agent across all three traces.** v1 surprise gate is dominated by poll on test_v2; the cost-efficiency story only holds on the regime-aligned traces.
- **Honest paper framing**: *HeargentZ is selective-initiation at ~20× lower cost than polling on traces with a structurally consistent GT/distractor split; on traces with mixed semantics, single-step embedding surprise is not a sufficient gate signal and intent-conditioned prediction is needed.*

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
│   └── loop.py                   ← HeargentAgent (v1 prediction-error gate)
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
