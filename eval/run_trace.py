from __future__ import annotations

import argparse
import importlib
import json
import sys
from typing import Protocol

from sandbox.event_trace import Trace, get_trace
from sandbox.world import Event, World


class Agent(Protocol):
    name: str

    def tick(self, observations: list[Event], world: World, sim_time: float) -> None: ...

    def cost_usd(self) -> float: ...


def _matches_keywords(text: str, keywords: tuple[str, ...]) -> bool:
    lo = text.lower()
    return all(kw.lower() in lo for kw in keywords)


def score(world: World, trace: Trace) -> dict:
    hits: list[dict] = []
    misses: list[str] = []
    matched_notification_indexes: set[int] = set()

    for gt in trace.ground_truth:
        window_start = gt.event.sim_time
        window_end = gt.event.sim_time + gt.proaction_window_s
        found = False
        for idx, note in enumerate(world.notifications):
            if idx in matched_notification_indexes:
                continue
            if not (window_start <= note.sim_time <= window_end):
                continue
            if not _matches_keywords(note.content, gt.keywords):
                continue
            hits.append(
                {
                    "event_id": gt.event.id,
                    "notification_sim_time": note.sim_time,
                    "time_to_notice_s": note.sim_time - gt.event.sim_time,
                }
            )
            matched_notification_indexes.add(idx)
            found = True
            break
        if not found:
            misses.append(gt.event.id)

    false_initiations = len(world.notifications) - len(matched_notification_indexes)
    duration = trace.duration_s
    hours = duration / 3600.0 if duration > 0 else 1.0

    ttns = sorted(h["time_to_notice_s"] for h in hits)
    median_ttn = ttns[len(ttns) // 2] if ttns else None

    return {
        "hit_rate": len(hits) / len(trace.ground_truth) if trace.ground_truth else 0.0,
        "false_initiation_rate_per_hour": false_initiations / hours,
        "median_time_to_notice_s": median_ttn,
        "total_notifications": len(world.notifications),
        "total_events": len(trace.ground_truth),
        "total_distractors": len(trace.events) - len(trace.ground_truth),
        "hits": hits,
        "misses": misses,
    }


def run(agent: Agent, trace: Trace, tick_dt_s: float = 5.0) -> dict:
    world = World()
    world.load_trace(trace.events)
    duration = trace.duration_s

    while world.sim_time < duration:
        world.advance(tick_dt_s)
        observations = world.observe()
        agent.tick(observations, world, world.sim_time)

    metrics = score(world, trace)
    metrics["agent_name"] = agent.name
    metrics["cost_usd"] = agent.cost_usd()
    metrics["tick_dt_s"] = tick_dt_s
    metrics["trace_duration_s"] = duration
    if hasattr(agent, "llm_stats"):
        metrics["llm_stats"] = agent.llm_stats()
    return metrics


def _load_agent(
    spec: str,
    trace: Trace | None = None,
    *,
    intent_mode: str | None = None,
    with_briefing: bool = False,
    arbiter_mode: str | None = None,
    arbiter_random_p: float | None = None,
    arbiter_random_seed: int | None = None,
    arbiter_system_prompt: str = "v2",
) -> Agent:
    module_name, _, cls_name = spec.rpartition(":")
    if not module_name:
        raise ValueError(f"Expected spec like 'baselines.react_reactive:ReactiveAgent', got {spec!r}")
    module = importlib.import_module(module_name)
    cls = getattr(module, cls_name)
    if intent_mode is not None:
        if not hasattr(cls, "from_trace"):
            raise ValueError(f"{spec} does not support --intent-mode (no from_trace classmethod)")
        return cls.from_trace(trace, mode=intent_mode)
    if with_briefing:
        if not hasattr(cls, "from_trace"):
            raise ValueError(f"{spec} does not support --with-briefing (no from_trace classmethod)")
        return cls.from_trace(trace, with_briefing=True)
    if arbiter_mode == "claude":
        # M10 (runs/17 SHA 68d42e3) — Claude-API arbiter dispatched here
        # rather than via HeargentZA.from_trace so agent/loop.py stays
        # untouched per the pre-reg's "Critical files" list.
        from agent.arbiter import (
            ARBITER_SYSTEM_PROMPT_V2,
            ARBITER_SYSTEM_PROMPT_V3,
            ClaudeArbiter,
        )
        prompt = (
            ARBITER_SYSTEM_PROMPT_V3
            if arbiter_system_prompt == "v3"
            else ARBITER_SYSTEM_PROMPT_V2
        )
        arbiter = ClaudeArbiter(system_prompt=prompt)
        return cls(arbiter=arbiter)
    if arbiter_mode is not None:
        if not hasattr(cls, "from_trace"):
            raise ValueError(f"{spec} does not support --arbiter-mode (no from_trace classmethod)")
        kwargs: dict = {"mode": arbiter_mode, "random_p": arbiter_random_p}
        if arbiter_random_seed is not None:
            kwargs["random_seed"] = arbiter_random_seed
        return cls.from_trace(trace, **kwargs)
    return cls()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True, help="Module:Class of the agent to run")
    parser.add_argument("--trace", default="dev_v1", help="Trace name (dev_v1, dev_v2, test_v1, test_v2)")
    parser.add_argument("--tick-dt", type=float, default=5.0)
    parser.add_argument("--out", default=None, help="Write metrics JSON here; default stdout")
    parser.add_argument(
        "--intent-mode",
        choices=["oracle", "briefing", "placebo"],
        default=None,
        help="Intent source for HeargentZIntent (calls agent.from_trace)",
    )
    parser.add_argument(
        "--with-briefing",
        action="store_true",
        help="Pass trace.briefing to the agent (calls agent.from_trace(trace, with_briefing=True))",
    )
    parser.add_argument(
        "--arbiter-mode",
        choices=["content", "random", "claude"],
        default=None,
        help="Arbiter source for HeargentZA. content/random call agent.from_trace; claude (M10) constructs ClaudeArbiter directly.",
    )
    parser.add_argument(
        "--arbiter-random-p",
        type=float,
        default=None,
        help="Bernoulli p for --arbiter-mode=random (pre-committed YES-rate from content run on dev_v2)",
    )
    parser.add_argument(
        "--arbiter-random-seed",
        type=int,
        default=None,
        help="RandomArbiter RNG seed for --arbiter-mode=random (default 42 when omitted)",
    )
    parser.add_argument(
        "--arbiter-system-prompt",
        choices=["v2", "v3"],
        default="v2",
        help="System prompt for --arbiter-mode=claude (V2 closed enumeration or V3 principled criterion). Ignored for content/random.",
    )
    args = parser.parse_args()

    trace = get_trace(args.trace)
    agent = _load_agent(
        args.agent,
        trace,
        intent_mode=args.intent_mode,
        with_briefing=args.with_briefing,
        arbiter_mode=args.arbiter_mode,
        arbiter_random_p=args.arbiter_random_p,
        arbiter_random_seed=args.arbiter_random_seed,
        arbiter_system_prompt=args.arbiter_system_prompt,
    )
    metrics = run(agent, trace, tick_dt_s=args.tick_dt)
    metrics["trace_name"] = trace.name
    metrics["intent_mode"] = args.intent_mode
    metrics["with_briefing"] = args.with_briefing
    metrics["arbiter_mode"] = args.arbiter_mode
    metrics["arbiter_random_p"] = args.arbiter_random_p
    metrics["arbiter_random_seed"] = args.arbiter_random_seed
    metrics["arbiter_system_prompt"] = args.arbiter_system_prompt
    if args.arbiter_mode == "claude":
        # Augment llm_stats with Claude arbiter token counts and override
        # cost_usd (HeargentZA.cost_usd returns 0.0 by default since the
        # 3B path is local). M10 (runs/17 SHA 68d42e3).
        arb = agent.arbiter
        metrics.setdefault("llm_stats", {})
        metrics["llm_stats"]["arbiter_input_tokens"] = arb.input_tokens
        metrics["llm_stats"]["arbiter_output_tokens"] = arb.output_tokens
        metrics["llm_stats"]["arbiter_dispatched_model"] = arb.dispatched_model
        metrics["cost_usd"] = arb.cost_usd
    if hasattr(agent, "intents"):
        metrics["intents"] = list(agent.intents)
    if hasattr(agent, "surprise_log"):
        metrics["surprise_log"] = agent.surprise_log
    payload = json.dumps(metrics, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(payload)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
