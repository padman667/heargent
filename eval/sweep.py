from __future__ import annotations

import argparse
import json
from statistics import mean, stdev

from agent.loop import HeargentAgent
from baselines.random_gate import RandomGateAgent
from eval.run_trace import run
from sandbox.event_trace import get_trace


def heargent_at(theta: float, trace_name: str) -> dict:
    agent = HeargentAgent(theta=theta)
    trace = get_trace(trace_name)
    metrics = run(agent, trace, tick_dt_s=5.0)
    metrics["theta"] = theta
    metrics["surprise_log"] = agent.surprise_log
    return metrics


def random_gate_at(p: float, trace_name: str, seeds: list[int]) -> dict:
    trace = get_trace(trace_name)
    runs = []
    for s in seeds:
        agent = RandomGateAgent(p=p, seed=s)
        runs.append(run(agent, trace, tick_dt_s=5.0))
    hit_rates = [r["hit_rate"] for r in runs]
    false_rates = [r["false_initiation_rate_per_hour"] for r in runs]
    return {
        "p": p,
        "seeds": seeds,
        "hit_rate_mean": mean(hit_rates),
        "hit_rate_stdev": stdev(hit_rates) if len(hit_rates) > 1 else 0.0,
        "false_rate_mean": mean(false_rates),
        "false_rate_stdev": stdev(false_rates) if len(false_rates) > 1 else 0.0,
        "per_seed": [
            {
                "seed": s,
                "hit_rate": r["hit_rate"],
                "false_initiation_rate_per_hour": r["false_initiation_rate_per_hour"],
                "notifications": r["total_notifications"],
            }
            for s, r in zip(seeds, runs)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", default="dev_v2")
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--thetas",
        nargs="+",
        type=float,
        default=[0.30, 0.35, 0.40, 0.43, 0.45, 0.50],
    )
    parser.add_argument("--random-seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    args = parser.parse_args()

    trace = get_trace(args.trace)
    total_obs = len(trace.events)

    theta_results = []
    for theta in args.thetas:
        m = heargent_at(theta, args.trace)
        theta_results.append(m)
        n_fire = m["total_notifications"]
        rate = n_fire / total_obs
        print(
            f"heargent θ={theta:.2f}: hit={m['hit_rate']:.2f} "
            f"false/h={m['false_initiation_rate_per_hour']:.2f} "
            f"notifs={n_fire}/{total_obs} (rate={rate:.2f})"
        )

    random_results = []
    seen_p = set()
    for m in theta_results:
        p = m["total_notifications"] / total_obs
        p_key = round(p, 3)
        if p_key in seen_p:
            continue
        seen_p.add(p_key)
        r = random_gate_at(p=p_key, trace_name=args.trace, seeds=args.random_seeds)
        random_results.append(r)
        print(
            f"random_gate p={p_key:.2f}: hit_mean={r['hit_rate_mean']:.2f}±{r['hit_rate_stdev']:.2f} "
            f"false_mean={r['false_rate_mean']:.2f}±{r['false_rate_stdev']:.2f}"
        )

    out = {
        "trace": args.trace,
        "total_observations": total_obs,
        "ground_truth_count": len(trace.ground_truth),
        "distractor_count": total_obs - len(trace.ground_truth),
        "heargent_thetas": theta_results,
        "random_gate": random_results,
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
