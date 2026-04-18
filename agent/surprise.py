from __future__ import annotations

import math

from agent.llm import OllamaClient


class SurpriseScorer:
    """Independent embedding-based surprise scorer.

    Deliberately uses a different model (nomic-embed-text by default) from the
    predictor. This mitigates Risk 1 from the plan: if we scored surprise from
    the predictor model's own logprobs, it would just be perplexity dressed up.
    By using an independent embedder, the surprise signal reflects semantic
    divergence in a shared vector space neither the predictor nor the agent
    has direct influence over.

    score() returns cosine distance in [0, 2]; typical "reasonable prediction"
    distances cluster around 0.2-0.4, clearly unrelated sentences around 0.8+.
    """

    def __init__(self, client: OllamaClient, model: str = "nomic-embed-text") -> None:
        self.client = client
        self.model = model

    def _embed(self, text: str) -> list[float]:
        return self.client.embed(text, model=self.model)

    def score(self, prediction: str, observation: str) -> float:
        a = self._embed(prediction)
        b = self._embed(observation)
        return _cosine_distance(a, b)


def _cosine_distance(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"embedding dim mismatch: {len(a)} vs {len(b)}")
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    denom = math.sqrt(na) * math.sqrt(nb)
    if denom == 0.0:
        return 1.0
    return 1.0 - (dot / denom)
