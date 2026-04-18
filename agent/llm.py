from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_HOST = "http://localhost:11434"


@dataclass
class LLMStats:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_duration_ns: int = 0
    by_model: dict[str, int] = field(default_factory=dict)

    def record_generate(self, model: str, payload: dict) -> None:
        self.calls += 1
        self.prompt_tokens += payload.get("prompt_eval_count", 0) or 0
        self.completion_tokens += payload.get("eval_count", 0) or 0
        self.total_duration_ns += payload.get("total_duration", 0) or 0
        self.by_model[model] = self.by_model.get(model, 0) + 1


class OllamaClient:
    def __init__(self, host: str = DEFAULT_HOST, timeout_s: float = 60.0) -> None:
        self.host = host.rstrip("/")
        self.timeout_s = timeout_s
        self.stats = LLMStats()

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise RuntimeError(f"ollama request to {path} failed: {e}") from e

    def generate(
        self,
        prompt: str,
        model: str = "qwen3:4b",
        *,
        think: bool = False,
        max_tokens: int = 80,
        temperature: float = 0.7,
    ) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": think,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }
        resp = self._post("/api/generate", payload)
        self.stats.record_generate(model, resp)
        return (resp.get("response") or "").strip()

    def chat(
        self,
        system: str,
        user: str,
        model: str = "qwen3:4b",
        *,
        think: bool = False,
        max_tokens: int = 80,
        temperature: float = 0.7,
        seed: int | None = None,
    ) -> str:
        options: dict[str, Any] = {
            "num_predict": max_tokens,
            "temperature": temperature,
        }
        if seed is not None:
            options["seed"] = seed
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "think": think,
            "options": options,
        }
        resp = self._post("/api/chat", payload)
        self.stats.record_generate(model, resp)
        msg = resp.get("message") or {}
        return (msg.get("content") or "").strip()

    def embed(self, text: str, model: str = "nomic-embed-text") -> list[float]:
        resp = self._post("/api/embeddings", {"model": model, "prompt": text})
        emb = resp.get("embedding")
        if not emb:
            raise RuntimeError(f"empty embedding from {model}")
        return emb
