"""Off-harness V2-vs-V3 Opus probe (M10 Commit B pre-flight).

Mirrors the runs/16-v3-prompt.md:454 diagnostic that surfaced V3's 3B
NO-bias. Iterates 8 representative events × 2 prompts (V2 closed
enumeration, V3 principled criterion) through claude-opus-4-7 directly
and prints a markdown table. Output is captured verbatim into
runs/17-claude-arbiter.md under the "V2-vs-V3 Opus probe" sub-section
before any harness cell fires.

Confirms before Commit B cells:
  (a) parser handles Opus's actual output shape (must be YES/NO per
      agent.arbiter._DECISION regex);
  (b) Opus reads V2 closer to YES than 3B reads V2 on these
      representative cases (sanity);
  (c) V3 at Opus does NOT exhibit the 3B's pattern-matching-on-regret-
      list-words mode observed in M9 (sanity check before V3-Opus
      harness cells).

Usage: ANTHROPIC_API_KEY=... uv run python -m eval.probes.probe_v2_v3_opus
"""

from __future__ import annotations

from agent.arbiter import (
    ARBITER_SYSTEM_PROMPT_V2,
    ARBITER_SYSTEM_PROMPT_V3,
    ClaudeArbiter,
)


PROBE_EVENTS: list[tuple[str, str]] = [
    ("fire_alarm", "Fire alarm in building A triggered; evacuation in progress."),
    ("flight_delay", "Flight UA123 to Berlin tomorrow has been delayed by 3 hours. New departure: 14:30."),
    ("meeting_moved", "Meeting 'Design Review' tomorrow moved from 10:00 to 14:00."),
    ("news_digest", "Daily news digest updated."),
    ("rent_due", "Reminder: rent payment of $1450 is due tomorrow."),
    ("package_arrival", "Your package has been delivered to your door."),
    # test_v4 GTs that V2-3B missed (M8b coverage gap) and V3-3B did not rescue (M9 off-harness probe):
    ("parking_meter_oak", "Parking meter at 1247 Oak Street expires in 12 minutes; ticket likely if not extended."),
    ("cover_standup_request", "Hey, can you cover my 9am standup tomorrow? I'm taking a half-day for a doctor visit."),
]


def main() -> int:
    v2 = ClaudeArbiter(system_prompt=ARBITER_SYSTEM_PROMPT_V2)
    v3 = ClaudeArbiter(system_prompt=ARBITER_SYSTEM_PROMPT_V3)

    rows = []
    for event_id, content in PROBE_EVENTS:
        v2_decision = v2.classify(content)
        v3_decision = v3.classify(content)
        rows.append((event_id, content, v2_decision, v3_decision))

    print("| event | content | V2 | V3 |")
    print("|---|---|:---:|:---:|")
    for event_id, content, v2d, v3d in rows:
        v2_str = "YES" if v2d else "NO"
        v3_str = "YES" if v3d else "NO"
        # Truncate content for table readability; full content is reproducible
        # from PROBE_EVENTS in this file.
        c = content if len(content) <= 60 else content[:57] + "..."
        print(f"| `{event_id}` | {c} | {v2_str} | {v3_str} |")

    print()
    print(f"V2 dispatched model: {v2.dispatched_model}")
    print(f"V3 dispatched model: {v3.dispatched_model}")
    print(f"V2 input/output tokens: {v2.input_tokens}/{v2.output_tokens}")
    print(f"V3 input/output tokens: {v3.input_tokens}/{v3.output_tokens}")
    print(f"V2 cost: ${v2.cost_usd:.6f}")
    print(f"V3 cost: ${v3.cost_usd:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
