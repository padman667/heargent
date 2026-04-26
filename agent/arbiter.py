from __future__ import annotations

import random
import re
from typing import TYPE_CHECKING

from agent.llm import OllamaClient

if TYPE_CHECKING:
    from anthropic import Anthropic


# Anthropic Opus 4.7 rates locked at runs/17-claude-arbiter.md SHA 68d42e3
# (M10 Commit A pre-reg). Used by ClaudeArbiter and baselines.react_poll_claude.
OPUS_INPUT_USD_PER_M = 15.0
OPUS_OUTPUT_USD_PER_M = 75.0

ARBITER_SYSTEM_PROMPT = (
    "You are a triage filter for a proactive assistant. Decide whether a\n"
    "single observed event warrants surfacing to the user right now.\n"
    "\n"
    "Surface (YES) if the event describes:\n"
    " - an urgent physical safety or security issue (fire, break-in, breach)\n"
    " - an unexpected interruption to the user's personal life (medical,\n"
    "   family emergency, home problem, childcare)\n"
    " - a financial or scheduling obligation with imminent action required\n"
    " - a production/on-call alert or outage\n"
    "\n"
    "Do NOT surface (NO) if the event is:\n"
    " - routine status, uptime, or heartbeat notifications\n"
    " - marketing, promotional, or newsletter content\n"
    " - generic \"all systems normal\" or daily briefing summaries\n"
    "\n"
    "Output exactly YES or NO, uppercase, on a single line. No explanation."
)


ARBITER_SYSTEM_PROMPT_V2 = (
    "You are a triage filter for a proactive assistant. Decide whether a\n"
    "single observed event warrants surfacing to the user right now.\n"
    "\n"
    "Surface (YES) if the event describes any of:\n"
    " - an urgent safety or security issue (fire, break-in, medical\n"
    "   emergency, security breach, unauthorized access)\n"
    " - a schedule change affecting the user personally (meeting moved,\n"
    "   meeting cancelled, flight delayed, appointment rescheduled,\n"
    "   appointment cancelled)\n"
    " - a financial or deadline obligation the user must act on within\n"
    "   the next few days (bill due, rent due, report deadline,\n"
    "   payment reminder)\n"
    " - a message or delivery directed personally to the user (package\n"
    "   delivered, callback requested, voicemail or phone message,\n"
    "   hospital calling about a family member)\n"
    " - a weather alert or external condition that would plausibly\n"
    "   change the user's planned day\n"
    " - a production/on-call alert or outage for a system the user owns\n"
    "\n"
    "Do NOT surface (NO) if the event is:\n"
    " - routine status, uptime, heartbeat, or \"all systems normal\" pings\n"
    " - marketing, promotional, or newsletter content\n"
    " - generic daily briefings that explicitly state no urgent items\n"
    " - feature announcements, app updates, or social/channel invites\n"
    "\n"
    "Output exactly YES or NO, uppercase, on a single line. No explanation."
)


# M9 / Commit B: principled AND-gate criterion attempted as a replacement
# for V2's closed YES enumeration. Frozen verbatim by runs/16-v3-prompt.md
# (Commit A SHA 3653880, defense hardening at e66afc1). Wire-up choice
# (a): the trailing `Content: {content}\n\nYES or NO:` block from the
# pre-reg text is dropped; content reaches the model via the chat
# template's user turn exactly as it does under V2
# (`client.chat(system=..., user=text)`), preserving V2's chat-template
# segmentation byte-for-byte. The system prompt body below is
# byte-identical to the pre-registered V3 text up through the
# token-contract sentence "Output exactly one token: YES or NO."
#
# OUTCOME (runs/16 §"Results — Commit B regression gate"): regression
# gate FAIL on round 0 across all three co-developed traces. Per
# scientifically-conservative path-C close, the pre-reg's redesign budget
# (up to 2 within-form rounds) was held in reserve; V3 reported as the
# 3B prompt-architecture ceiling under principled-criterion phrasing.
# ContentArbiter default reverted to V2 to preserve production behavior
# aligned with the M6a/M7/M8b published claims. V3 retained here as a
# named constant for paper reference and reproduction of M9's
# falsification result; pass `system_prompt=ARBITER_SYSTEM_PROMPT_V3`
# explicitly to reproduce.
ARBITER_SYSTEM_PROMPT_V3 = (
    "You judge whether a single notification warrants proactive surfacing to a user.\n"
    "\n"
    "Surface (YES) if the content meets BOTH of these conditions:\n"
    "1. Actionable — the content implies a decision, response, or adjustment the user could make.\n"
    "2. Time-bounded with regret — ignoring it for the next few hours could cost the user something they would notice (money, missed obligation, missed opportunity, safety).\n"
    "\n"
    "Do NOT surface (NO) if the content is routine status (service heartbeats, all-clear pings, uptime reports), social / ambient (app promotions, reaction notifications, friend activity, newsletters, subscription billing notices), or purely informational with nothing the user must decide or act on within hours.\n"
    "\n"
    "Output exactly one token: YES or NO."
)


_DECISION = re.compile(r"\b(YES|NO)\b")


class ContentArbiter:
    """Pure-content binary classifier for proactive surfacing.

    Ignores the predictor's output, the rolling history, any user briefing,
    and any intent list — only the event content text is fed in. This is the
    mechanism isolation from run 09: user-context injection hurt every cell
    it touched there, so the arbiter is deliberately context-free.
    """

    def __init__(
        self,
        client: OllamaClient,
        model: str = "qwen2.5:3b-instruct",
        *,
        temperature: float = 0.0,
        seed: int = 42,
        system_prompt: str = ARBITER_SYSTEM_PROMPT_V2,
    ) -> None:
        self.client = client
        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.system_prompt = system_prompt
        self.yes_count = 0
        self.no_count = 0

    @property
    def yes_rate(self) -> float:
        total = self.yes_count + self.no_count
        return self.yes_count / total if total else 0.0

    def classify(self, text: str) -> bool:
        raw = self.client.chat(
            system=self.system_prompt,
            user=text,
            model=self.model,
            max_tokens=5,
            temperature=self.temperature,
            seed=self.seed,
        )
        first_line = raw.strip().splitlines()[0] if raw.strip() else ""
        m = _DECISION.search(first_line.upper())
        decision = bool(m and m.group(1) == "YES")
        if decision:
            self.yes_count += 1
        else:
            self.no_count += 1
        return decision


class RandomArbiter:
    """Null-ablation arbiter: Bernoulli draw with pre-committed firing rate.

    Matches the M4 null-ablation role of run 05's random-gate. `p` is set to
    the empirical YES-rate of the content arbiter on dev_v2, so firing rate
    is controlled; only the content signal differs between this and the real
    arbiter.
    """

    def __init__(self, p: float, seed: int = 42) -> None:
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p must be in [0, 1]; got {p}")
        self.p = p
        self.seed = seed
        self._rng = random.Random(seed)
        self.yes_count = 0
        self.no_count = 0

    @property
    def yes_rate(self) -> float:
        total = self.yes_count + self.no_count
        return self.yes_count / total if total else 0.0

    def classify(self, text: str) -> bool:
        del text  # random arbiter ignores content by design
        decision = self._rng.random() < self.p
        if decision:
            self.yes_count += 1
        else:
            self.no_count += 1
        return decision


class ClaudeArbiter:
    """Pure-content binary classifier using Claude API (Opus 4.7).

    M10 model-scale lever (runs/17-claude-arbiter.md SHA 68d42e3). Same
    public surface as ContentArbiter (`classify`, `yes_count`, `no_count`,
    `yes_rate`) plus token + cost accounting for the dual-axis (tok/hit,
    usd/hit) Pareto. Wire-up choice (a) per runs/16-v3-prompt.md:51-53:
    `system = rules`, `user = event_content` — chat-template parity with
    V2/V3 at the 3B scale, so any V2-3B → V2-Opus delta attributes cleanly
    to the model lever rather than to a wire-up shape change.

    Default `system_prompt = ARBITER_SYSTEM_PROMPT_V2`. Pass
    `system_prompt=ARBITER_SYSTEM_PROMPT_V3` explicitly for V3-Opus
    attribution cells. Anthropic SDK is imported lazily so this module
    still imports cleanly when `anthropic` is not installed (e.g. during
    `--arbiter-mode content/random` runs).
    """

    def __init__(
        self,
        client: Anthropic | None = None,
        model: str = "claude-opus-4-7",
        *,
        max_tokens: int = 5,
        system_prompt: str = ARBITER_SYSTEM_PROMPT_V2,
    ) -> None:
        if client is None:
            from anthropic import Anthropic as _Anthropic
            client = _Anthropic()
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.yes_count = 0
        self.no_count = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.dispatched_model: str | None = None

    @property
    def yes_rate(self) -> float:
        total = self.yes_count + self.no_count
        return self.yes_count / total if total else 0.0

    @property
    def cost_usd(self) -> float:
        return (
            self.input_tokens * OPUS_INPUT_USD_PER_M
            + self.output_tokens * OPUS_OUTPUT_USD_PER_M
        ) / 1_000_000

    def classify(self, text: str) -> bool:
        # `temperature` parameter intentionally omitted: Opus 4.7 deprecates
        # it (anthropic.BadRequestError at request). Determinism verified
        # empirically at the connectivity smoke + doubled V2-vs-V3 probe;
        # see runs/17-claude-arbiter.md "Connectivity-smoke observations".
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": text}],
        )
        if self.dispatched_model is None:
            self.dispatched_model = resp.model
        self.input_tokens += resp.usage.input_tokens
        self.output_tokens += resp.usage.output_tokens
        raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        first_line = raw.splitlines()[0] if raw else ""
        m = _DECISION.search(first_line.upper())
        decision = bool(m and m.group(1) == "YES")
        if decision:
            self.yes_count += 1
        else:
            self.no_count += 1
        return decision
