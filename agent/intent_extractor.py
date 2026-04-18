from __future__ import annotations

import re

from agent.llm import OllamaClient

PLACEBO_BRIEFING = (
    "I'm trying to keep up with my vegetable garden this spring, following "
    "the Premier League title race, and I've been cooking my way through an "
    "Italian regional cookbook on weekends. Flag anything relevant."
)

EXTRACTION_SYSTEM_PROMPT = (
    "You extract a small set of the user's active concerns from a brief "
    "personal statement. Output a numbered list of 3 to 6 short phrases "
    "(max 10 words each), each describing one thematic concern the user "
    "would want a proactive assistant to monitor on their behalf. Keep "
    "phrases abstract (themes, not specific events). No invented details "
    "not present in the briefing. Output only the numbered list, one "
    "concern per line, nothing else."
)

_LIST_PREFIX_RE = re.compile(r"^[\s\d\.\)\-\*]+")


def _parse_intents(raw: str, max_items: int = 6) -> tuple[str, ...]:
    out: list[str] = []
    for line in raw.splitlines():
        cleaned = _LIST_PREFIX_RE.sub("", line).strip()
        cleaned = cleaned.strip("-*•").strip()
        if cleaned and any(c.isalnum() for c in cleaned):
            out.append(cleaned)
        if len(out) >= max_items:
            break
    return tuple(out)


def extract_intents(
    client: OllamaClient,
    briefing_text: str,
    *,
    model: str = "qwen2.5:3b-instruct",
    max_items: int = 6,
) -> tuple[str, ...]:
    user_msg = f"User briefing:\n{briefing_text}\n\nThemes to monitor:"
    response = client.chat(
        system=EXTRACTION_SYSTEM_PROMPT,
        user=user_msg,
        model=model,
        max_tokens=200,
        temperature=0.0,
        seed=42,
    )
    return _parse_intents(response, max_items=max_items)
