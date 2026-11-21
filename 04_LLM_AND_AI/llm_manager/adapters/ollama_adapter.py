"""Master AI - Native Ollama Provider Adapter.

Interfaces with the native local Ollama daemon on Windows (http://127.0.0.1:11434)
for CPU-first and hardware-accelerated local inference.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, List

from .base_adapter import BaseLLMAdapter


class OllamaAdapter(BaseLLMAdapter):
    """Adapter for local Ollama daemon."""

    def __init__(self, base_url: str | None = None) -> None:
        super().__init__(name="OllamaLocal", is_local_or_mock=True)
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")

    def is_available(self) -> tuple[bool, str]:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "MasterAI/2.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    return True, "Ollama daemon is reachable"
                return False, f"Ollama returned HTTP {resp.status}"
        except Exception as e:
            return False, f"Ollama connection error: {e}"

    def health_check(self) -> Dict[str, Any]:
        t0 = time.time()
        available, msg = self.is_available()
        latency_ms = round((time.time() - t0) * 1000, 2)
        installed = self.list_installed_models() if available else []
        return {
            "status": "healthy" if available else "unreachable",
            "provider": self.name,
            "base_url": self.base_url,
            "latency_ms": latency_ms,
            "message": msg,
            "installed_models_count": len(installed),
            "installed_models": [m.get("name") for m in installed],
        }

    def list_installed_models(self) -> List[Dict[str, Any]]:
        """Fetch list of models currently cached in Ollama."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("models", [])
        except Exception:
            return []

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Fetch detailed parameters, license, and template of an installed model."""
        try:
            req = urllib.request.Request(
                f"{self.base_url}/api/show",
                data=json.dumps({"name": model_name}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e), "model": model_name}

    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str = "qwen2.5:1.5b",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                msg = data.get("message", {})
                prompt_eval_count = data.get("prompt_eval_count", 0)
                eval_count = data.get("eval_count", 0)
                return {
                    "id": f"ollama-{int(time.time()*1000)}",
                    "model": model,
                    "provider": self.name,
                    "choices": [
                        {
                            "index": 0,
                            "message": msg,
                            "finish_reason": "stop" if data.get("done") else "length",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": prompt_eval_count,
                        "completion_tokens": eval_count,
                        "total_tokens": prompt_eval_count + eval_count,
                        "estimated_cost_usd": 0.0,
                    },
                }
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed for model '{model}': {e}") from e

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = "qwen2.5:1.5b",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Iterator[str]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                for line in resp:
                    if line:
                        chunk = json.loads(line.decode("utf-8"))
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield content
        except Exception as e:
            raise RuntimeError(f"Ollama streaming failed: {e}") from e

    def get_capabilities(self) -> List[str]:
        return ["streaming", "structured_json", "local_cpu", "offline_ready"]
