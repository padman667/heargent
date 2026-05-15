"""M11a-extension §D4 self-restate pre-flight gate (locked at D14-H7).

Emits the structural-constraint self-restate prompt with the iteratively-
extended banned list inlined. Fresh-session authoring sessions read the
emitted text, restate constraints (a)-(d) in their own words BEFORE
authoring, and persist the restate response as a Commit C audit artifact
alongside the authored trace per ~/.claude/plans/m11a-extension-v4-prompt-
n20.md §D4 + runs/21-v4-prompt-n20-extension.md §D4. Targets the M11a
structural-parsing-failure rate of 3/9 = 33% (test_v11 #1 walrus syntax;
test_v13 #2 + test_v15 #1 arithmetic in event_ids) surfaced at runs/19.

Module entry point: ``python -m eval.author_trace --banned-list <path>``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SELF_RESTATE_PROMPT = (
    "You will author one EventTrace for the heargent harness. Per M11a "
    "iterative-extension protocol, your trace must (a) use only Python "
    "expressions parseable by sandbox/event_trace.py; (b) not use walrus "
    "operator; (c) not use arithmetic in event_id strings; (d) avoid "
    "reusing event_ids from the iteratively-extended banned list (provided "
    "below). Restate (a)-(d) in your own words before authoring."
)


def render(banned_list_path: Path) -> str:
    return f"{SELF_RESTATE_PROMPT}\n\nBanned list:\n{banned_list_path.read_text()}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="M11a-extension §D4 self-restate pre-flight gate"
    )
    parser.add_argument(
        "--banned-list",
        required=True,
        type=Path,
        help="Path to the iteratively-extended banned-list file (event_ids + themes + tuples per M11a protocol)",
    )
    args = parser.parse_args()
    print(render(args.banned_list))
    return 0


if __name__ == "__main__":
    sys.exit(main())
