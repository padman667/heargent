"""M11b Commit D aggregate analysis.

Reads all D-phase JSONs + carry-forward references; computes per-trace
observations, per-tier failure-rate metrics with Clopper-Pearson + bootstrap
CIs (seed=42, 2000 resamples), Pareto-cost table, P1/P2/P3/P4 verdicts,
outcome-row + D7-branch identification, V3 attribution band, and drift
smoke Phase 2/Phase 3 bit-compare. Output is one Markdown document suitable
for direct paste into the runs/20-cross-model-sweep.md results appendix.

Run from repo root:
    uv run --with scipy python runs/data/.commit_d_analysis.py
"""
from __future__ import annotations
import json
import random
from pathlib import Path
from typing import Iterable

from scipy.stats import beta  # type: ignore

# ---------- Locked references (per pre-reg + correction commits) ----------

TRACES = ["test_v4", "test_v5", "test_v6", "test_v7", "test_v8",
          "test_v11", "test_v12", "test_v13", "test_v14", "test_v15"]
CO_DEV = ["dev_v2", "test_v1", "test_v2"]

# Carry-forward path map per scope
V23B_REF = {
    "test_v4":  "runs/data/15a-content-test_v4.json",
    "test_v5":  "runs/data/17d-content-3b-v2-test_v5.json",
    "test_v6":  "runs/data/18d-content-3b-v2-test_v6.json",
    "test_v7":  "runs/data/18d-content-3b-v2-test_v7.json",
    "test_v8":  "runs/data/18d-content-3b-v2-test_v8.json",
    **{f"test_v{i}": f"runs/data/19d-content-3b-v2-test_v{i}.json" for i in [11,12,13,14,15]},
}
V2OPUS_REF = {
    "test_v4":  "runs/data/17b-content-opus-v2-test_v4.json",
    "test_v5":  "runs/data/17d-content-opus-v2-test_v5.json",
    "test_v6":  "runs/data/18d-content-opus-v2-test_v6.json",
    "test_v7":  "runs/data/18d-content-opus-v2-test_v7.json",
    "test_v8":  "runs/data/18d-content-opus-v2-test_v8.json",
    **{f"test_v{i}": f"runs/data/19d-content-opus-v2-test_v{i}.json" for i in [11,12,13,14,15]},
}
POLLOPUS_REF = {
    "test_v4":  "runs/data/17b-poll-opus-test_v4.json",  # may not exist for test_v4
    "test_v5":  "runs/data/17d-poll-opus-test_v5.json",
    "test_v6":  "runs/data/18d-poll-opus-test_v6.json",
    "test_v7":  "runs/data/18d-poll-opus-test_v7.json",
    "test_v8":  "runs/data/18d-poll-opus-test_v8.json",
    **{f"test_v{i}": f"runs/data/19d-poll-opus-test_v{i}.json" for i in [11,12,13,14,15]},
}
V3OPUS_REF = {
    "test_v4":  "runs/data/17b-content-opus-v3-test_v4.json",
    "test_v5":  "runs/data/17d-content-opus-v3-test_v5.json",
}

# M11b new cells
V2SONNET = {tr: f"runs/data/20d-content-sonnet-v2-{tr}.json" for tr in TRACES}
V2HAIKU  = {tr: f"runs/data/20d-content-haiku-v2-{tr}.json" for tr in TRACES}
V3SONNET = {tr: f"runs/data/20d-content-sonnet-v3-{tr}.json" for tr in ["test_v4","test_v5"]}
V3HAIKU  = {tr: f"runs/data/20d-content-haiku-v3-{tr}.json" for tr in ["test_v4","test_v5"]}
POLLSONNET = {tr: f"runs/data/20d-poll-sonnet-{tr}.json" for tr in TRACES}
POLLHAIKU  = {tr: f"runs/data/20d-poll-haiku-{tr}.json" for tr in TRACES}

# ---------- Helpers ----------

def load(path: str) -> dict | None:
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else None

def joint_bar_fail(d: dict) -> bool:
    """Strict joint-bar definition per pre-reg line 224."""
    return d["hit_rate"] < 0.80 or d["false_initiation_rate_per_hour"] > 5.0

def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    lo = 0.0 if k == 0 else beta.ppf(alpha/2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha/2, k + 1, n - k)
    return float(lo), float(hi)

def bootstrap_ci(outcomes: list[int], n_resamples: int = 2000, seed: int = 42,
                 alpha: float = 0.05) -> tuple[float, float]:
    """2000-resample non-parametric bootstrap CI on per-trace failure rate."""
    rng = random.Random(seed)
    n = len(outcomes)
    rates = []
    for _ in range(n_resamples):
        sample = [outcomes[rng.randrange(n)] for _ in range(n)]
        rates.append(sum(sample) / n)
    rates.sort()
    lo = rates[int(n_resamples * alpha/2)]
    hi = rates[int(n_resamples * (1 - alpha/2)) - 1]
    return lo, hi

def fmt_pct(p: float) -> str:
    return f"{100*p:.1f}%"

def fmt_ci(lo: float, hi: float) -> str:
    return f"[{100*lo:.1f}%, {100*hi:.1f}%]"

# ---------- Per-trace observations ----------

def per_trace_table() -> str:
    lines = ["| Trace | V2-3B (h/false_h) | V2-Opus (h/false_h) | V2-Sonnet (h/false_h) | V2-Haiku (h/false_h) | poll-Sonnet (h) | poll-Haiku (h) | poll-Opus (h) | cron30s (h) | P1 V2-S matches V2-O? | P2 V2-H matches V2-O? |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for tr in TRACES:
        v23b = load(V23B_REF[tr])
        v2o = load(V2OPUS_REF[tr])
        v2s = load(V2SONNET[tr])
        v2h = load(V2HAIKU[tr])
        ps = load(POLLSONNET[tr])
        ph = load(POLLHAIKU[tr])
        po = load(POLLOPUS_REF[tr])
        # cron30s from belt re-run (same data as M11a/M10b/M10/M8b)
        cron = load(f"runs/data/20b-belt-cron30-{tr}.json")

        def fmt(d):
            if d is None: return "—"
            return f"{d['hit_rate']:.2f}/{d['false_initiation_rate_per_hour']:.2f}"
        def fmth(d):
            if d is None: return "—"
            return f"{d['hit_rate']:.2f}"

        # P1: |h(S)-h(O)|≤0.10 AND |false/h(S)-false/h(O)|≤2.5 per-trace
        if v2s and v2o:
            hp1 = abs(v2s['hit_rate'] - v2o['hit_rate']) <= 0.10
            fp1 = abs(v2s['false_initiation_rate_per_hour'] - v2o['false_initiation_rate_per_hour']) <= 2.5
            p1 = "Y" if (hp1 and fp1) else "N"
        else:
            p1 = "?"
        if v2h and v2o:
            hp2 = abs(v2h['hit_rate'] - v2o['hit_rate']) <= 0.10
            fp2 = abs(v2h['false_initiation_rate_per_hour'] - v2o['false_initiation_rate_per_hour']) <= 2.5
            p2 = "Y" if (hp2 and fp2) else "N"
        else:
            p2 = "?"

        lines.append(f"| {tr} | {fmt(v23b)} | {fmt(v2o)} | {fmt(v2s)} | {fmt(v2h)} | {fmth(ps)} | {fmth(ph)} | {fmth(po)} | {fmth(cron)} | {p1} | {p2} |")
    return "\n".join(lines)

# ---------- Per-tier failure rate ----------

def per_tier_failure_rates() -> tuple[str, dict]:
    counts = {}
    outcomes = {}
    for tier, path_map in [("V2-3B", V23B_REF), ("V2-Opus", V2OPUS_REF),
                           ("V2-Sonnet", V2SONNET), ("V2-Haiku", V2HAIKU)]:
        oc = []
        for tr in TRACES:
            d = load(path_map[tr])
            oc.append(1 if (d and joint_bar_fail(d)) else 0)
        counts[tier] = sum(oc)
        outcomes[tier] = oc

    lines = ["| Tier | Failures (joint bar: hit<0.80 OR false/h>5.0/h) | Failure rate | 95% CP CI | Bootstrap CI (n=2000, seed=42) | Δ vs V2-3B | Δ vs V2-Opus | CP-CI overlaps V2-3B? | CP-CI overlaps V2-Opus? |",
             "|---|---|---|---|---|---|---|---|---|"]
    cis = {}
    for tier in ["V2-3B", "V2-Opus", "V2-Sonnet", "V2-Haiku"]:
        k = counts[tier]; n = len(TRACES)
        lo, hi = clopper_pearson(k, n)
        blo, bhi = bootstrap_ci(outcomes[tier])
        cis[tier] = (k/n, lo, hi, blo, bhi)

    p_v23b = cis["V2-3B"][0]; lo_v23b, hi_v23b = cis["V2-3B"][1], cis["V2-3B"][2]
    p_v2o = cis["V2-Opus"][0]; lo_v2o, hi_v2o = cis["V2-Opus"][1], cis["V2-Opus"][2]
    for tier in ["V2-3B", "V2-Opus", "V2-Sonnet", "V2-Haiku"]:
        rate, lo, hi, blo, bhi = cis[tier]
        dv23b = (rate - p_v23b) * 100
        dv2o = (rate - p_v2o) * 100
        overlap_v23b = "—" if tier == "V2-3B" else ("YES" if (lo <= hi_v23b and hi >= lo_v23b) else "NO")
        overlap_v2o = "—" if tier == "V2-Opus" else ("YES" if (lo <= hi_v2o and hi >= lo_v2o) else "NO")
        lines.append(f"| {tier} | {counts[tier]}/10 | {fmt_pct(rate)} | {fmt_ci(lo, hi)} | {fmt_ci(blo, bhi)} | {dv23b:+.0f} pp | {dv2o:+.0f} pp | {overlap_v23b} | {overlap_v2o} |")
    return "\n".join(lines), {"counts": counts, "cis": cis, "outcomes": outcomes}

# ---------- Pareto cost ----------

def pareto_cost_table() -> tuple[str, dict]:
    """Mean $/cell + Mean $/hit by tier. Cross-tier and matched-arbiter ratios.

    Pre-reg §D5 P4: "denominator = # of hits in the cell; zero-hit cells reported
    but excluded from cost-per-hit aggregate."
    """
    tiers = [
        ("V2-3B",     V23B_REF),
        ("V2-Opus",   V2OPUS_REF),
        ("V2-Sonnet", V2SONNET),
        ("V2-Haiku",  V2HAIKU),
        ("poll-Opus", POLLOPUS_REF),
        ("poll-Sonnet", POLLSONNET),
        ("poll-Haiku",  POLLHAIKU),
        ("cron30s",  {tr: f"runs/data/20b-belt-cron30-{tr}.json" for tr in TRACES}),
    ]
    rows = []
    raw = {}
    for tier, pm in tiers:
        cell_costs = []
        per_hit = []
        for tr in TRACES:
            d = load(pm[tr])
            if d is None:
                cell_costs.append(None); per_hit.append(None); continue
            cost = d.get("cost_usd", 0.0)
            cell_costs.append(cost)
            hits = round(d["hit_rate"] * d["total_events"])
            if hits > 0:
                per_hit.append(cost / hits)
            else:
                per_hit.append(None)
        valid_costs = [c for c in cell_costs if c is not None]
        valid_perh = [c for c in per_hit if c is not None]
        mean_cell = sum(valid_costs) / len(valid_costs) if valid_costs else 0
        if valid_perh:
            mean_ph = sum(valid_perh) / len(valid_perh)
            min_ph = min(valid_perh); max_ph = max(valid_perh)
        else:
            mean_ph = min_ph = max_ph = 0
        rows.append((tier, mean_cell, mean_ph, min_ph, max_ph, len(valid_perh)))
        raw[tier] = {"cell_costs": cell_costs, "per_hit": per_hit, "mean_ph": mean_ph}

    lines = ["| Tier | Mean $/cell | Mean $/hit | Min $/hit | Max $/hit | n cells w/ hits |",
             "|---|---|---|---|---|---|"]
    for tier, mc, mp, mn, mx, nph in rows:
        lines.append(f"| {tier} | ${mc:.4f} | ${mp:.4f} | ${mn:.4f} | ${mx:.4f} | {nph}/10 |")

    # Matched-arbiter ratios + cross-tier
    def ratio(num, den):
        if den == 0: return "—"
        return f"{num/den:.1f}×"
    matched = [("V2-Sonnet vs poll-Sonnet", raw["poll-Sonnet"]["mean_ph"], raw["V2-Sonnet"]["mean_ph"]),
               ("V2-Haiku vs poll-Haiku",   raw["poll-Haiku"]["mean_ph"],  raw["V2-Haiku"]["mean_ph"]),
               ("V2-Opus vs poll-Opus",     raw["poll-Opus"]["mean_ph"],   raw["V2-Opus"]["mean_ph"])]
    cross = [("V2-Sonnet vs V2-Opus", raw["V2-Opus"]["mean_ph"], raw["V2-Sonnet"]["mean_ph"]),
             ("V2-Haiku vs V2-Opus",  raw["V2-Opus"]["mean_ph"], raw["V2-Haiku"]["mean_ph"])]
    out2 = ["", "**Matched-arbiter Pareto ratios (poll-X cost-per-hit ÷ V2-X cost-per-hit; higher = HeargentZA more cost-effective at matched arbiter):**", ""]
    for label, num, den in matched:
        out2.append(f"- {label}: {ratio(num, den)}")
    out2 += ["", "**Cross-tier Pareto ratios (V2-Opus cost-per-hit ÷ V2-X cost-per-hit; higher = X cheaper):**", ""]
    for label, num, den in cross:
        out2.append(f"- {label}: {ratio(num, den)}")
    return "\n".join(lines) + "\n" + "\n".join(out2), raw

# ---------- D7 mechanical identification ----------

def d7_diagnostic() -> str:
    """6-cell cross-product: {V2-Sonnet, V2-Haiku} × {trivia_league_round, grocer_back_in_stock, calendar_yoga_suggest}.

    Returns surface decision (YES if surfaced; NO if not).
    """
    targets = [
        ("test_v11", "trivia_league_round"),
        ("test_v12", "grocer_back_in_stock"),
        ("test_v12", "calendar_yoga_suggest"),
    ]
    lines = ["| Trace | event_id | V2-3B | V2-Opus | V2-Sonnet | V2-Haiku |",
             "|---|---|---|---|---|---|"]
    yes_count = {"V2-Sonnet": 0, "V2-Haiku": 0}
    for (tr, eid) in targets:
        row = [tr, eid]
        for tier, pm in [("V2-3B", V23B_REF), ("V2-Opus", V2OPUS_REF), ("V2-Sonnet", V2SONNET), ("V2-Haiku", V2HAIKU)]:
            d = load(pm[tr])
            if d is None:
                row.append("?"); continue
            sl = d.get("surprise_log", []) or []
            entries = [e for e in sl if e.get("event_id") == eid]
            if not entries:
                row.append("(absent)"); continue
            e = entries[0]
            surfaced = e.get("surfaced", False)
            row.append("YES" if surfaced else "NO")
            if surfaced and tier in yes_count:
                yes_count[tier] += 1
        lines.append("| " + " | ".join(row) + " |")
    total_yes = yes_count["V2-Sonnet"] + yes_count["V2-Haiku"]
    if total_yes == 6:
        branch = "D7-confirm"
    elif total_yes == 0:
        branch = "D7-falsify"
    else:
        branch = f"D7-partial ({total_yes} of 6 surfaced)"
    return "\n".join(lines) + f"\n\n**D7 branch identification:** {branch} (V2-Sonnet surfaces {yes_count['V2-Sonnet']}/3 of M11a-flagged event_ids; V2-Haiku surfaces {yes_count['V2-Haiku']}/3)"

# ---------- V3 attribution band ----------

def v3_attribution() -> str:
    lines = ["| Trace | V2-3B | V2-Opus | V3-Opus | V3-Sonnet | V3-Haiku |",
             "|---|---|---|---|---|---|"]
    def fmth(d):
        return f"{d['hit_rate']:.2f}/{d['false_initiation_rate_per_hour']:.2f}" if d else "—"
    for tr in ["test_v4", "test_v5"]:
        v23b = load(V23B_REF[tr])
        v2o = load(V2OPUS_REF[tr])
        v3o = load(V3OPUS_REF[tr])
        v3s = load(V3SONNET[tr])
        v3h = load(V3HAIKU[tr])
        lines.append(f"| {tr} | {fmth(v23b)} | {fmth(v2o)} | {fmth(v3o)} | {fmth(v3s)} | {fmth(v3h)} |")
    return "\n".join(lines)

# ---------- Drift smoke Phase 2 + Phase 3 ----------

LB_TOP = ["hit_rate", "false_initiation_rate_per_hour"]
LB_LLM = ["arbiter_calls", "arbiter_yes_rate", "arbiter_input_tokens", "arbiter_output_tokens", "arbiter_dispatched_model"]

def smoke_compare(a_path, b_path):
    a = load(a_path); b = load(b_path)
    if a is None or b is None:
        return "NO-DATA", []
    deltas = []
    for f in LB_TOP:
        if a.get(f) != b.get(f):
            deltas.append(f"{f}: {a.get(f)!r} → {b.get(f)!r}")
    a_llm = (a.get("llm_stats") or {}); b_llm = (b.get("llm_stats") or {})
    for f in LB_LLM:
        if a_llm.get(f) != b_llm.get(f):
            deltas.append(f"llm_stats.{f}: {a_llm.get(f)!r} → {b_llm.get(f)!r}")
    return ("PASS" if not deltas else "FAIL"), deltas

def drift_smoke_report() -> str:
    lines = ["| Phase compare | Model | Trace | Status | Deltas (if FAIL) |", "|---|---|---|---|---|"]
    for model in ["sonnet", "haiku"]:
        for trace in CO_DEV:
            base = f"runs/data/20b-baseline-content-{model}-v2-{trace}.json"
            p2 = f"runs/data/20d-smoke-preharness-content-{model}-v2-{trace}.json"
            p3 = f"runs/data/20d-smoke-postharness-content-{model}-v2-{trace}.json"
            for label, path_a, path_b in [("Phase2 vs Phase1", base, p2), ("Phase3 vs Phase1", base, p3), ("Phase3 vs Phase2", p2, p3)]:
                status, deltas = smoke_compare(path_a, path_b)
                lines.append(f"| {label} | {model} | {trace} | {status} | {'; '.join(deltas) if deltas else ''} |")
    return "\n".join(lines)

# ---------- Main ----------

def main():
    out = []
    out.append("# M11b Commit D Aggregate Analysis (auto-generated)\n")
    out.append(f"Generated at HEAD; reads N=10 sample {TRACES} + co-developed {CO_DEV}.\n")
    out.append("Joint bar definition (locked at M11a pre-reg line 224): `hit < 0.80 OR false/h > 5.0/h`.\n")
    out.append("V2-Opus combined-N=10 reference: corrected 3/10 = 30% per the M11a Commit D correction commit (was 2/10 = 20% in M11a Commit D `cceeddd`).\n\n")

    out.append("## Per-trace observations\n")
    out.append(per_trace_table())
    out.append("\n")

    out.append("## Per-tier failure-rate metrics at combined-N=10\n")
    s, m = per_tier_failure_rates()
    out.append(s)
    out.append("\n")

    out.append("## Pareto-cost table\n")
    s, _ = pareto_cost_table()
    out.append(s)
    out.append("\n")

    out.append("## D7 secondary outcome — bytewise-identical-false-init cross-product\n")
    out.append(d7_diagnostic())
    out.append("\n")

    out.append("## V3 attribution on failure subset {test_v4, test_v5}\n")
    out.append(v3_attribution())
    out.append("\n")

    out.append("## Sonnet + Haiku within-milestone drift smoke (Phase 2 + Phase 3 vs Phase 1)\n")
    out.append(drift_smoke_report())
    out.append("\n")

    # Outcome row identification (preview)
    v2s_count = m["counts"]["V2-Sonnet"]; v2h_count = m["counts"]["V2-Haiku"]
    v2o_count = m["counts"]["V2-Opus"]; v23b_count = m["counts"]["V2-3B"]
    out.append(f"\n## Primary outcome row identification (mechanical from P1/P2/P3 verdicts)\n")
    out.append(f"Preliminary: V2-Sonnet {v2s_count}/10, V2-Haiku {v2h_count}/10, V2-Opus {v2o_count}/10, V2-3B {v23b_count}/10\n")

    Path("/tmp/m11b_commit_d_report.md").write_text("\n".join(out))
    print("\n".join(out))
    print("\n\nWritten to /tmp/m11b_commit_d_report.md")

if __name__ == "__main__":
    main()
