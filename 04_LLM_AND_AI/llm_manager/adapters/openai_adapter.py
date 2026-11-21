"""Master AI - OpenAI-Compatible Provider Adapter.

Supports local and remote OpenAI-standard endpoints (vLLM, LM Studio, OpenAI, LocalAI).
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, List

from .base_adapter import BaseLLMAdapter


class OpenAICompatibleAdapter(BaseLLMAdapter):
    """Adapter for endpoints implementing the OpenAI /v1/chat/completions standard."""

    def __init__(
        self,
        name: str = "OpenAICompatible",
        base_url: str | None = None,
        api_key: str | None = None,
        is_local_or_mock: bool = False,
    ) -> None:
        super().__init__(name=name, is_local_or_mock=is_local_or_mock)
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    def is_available(self) -> tuple[bool, str]:
        if not self.base_url:
            return False, "Base URL not configured"
        # If remote and no API key is provided, report unavailable without failing
        if not self.is_local_or_mock and not self.api_key:
            return False, "API key not configured"
        return True, "Endpoint configured"

    def health_check(self) -> Dict[str, Any]:
        available, msg = self.is_available()
        return {
            "status": "configured" if available else "disabled",
            "provider": self.name,
            "base_url": self.base_url,
            "has_api_key": bool(self.api_key),
            "message": msg,
        }

    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if not self.api_key and not self.is_local_or_mock:
            raise PermissionError(f"Cannot execute '{model}': Missing API key.")

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                data["provider"] = self.name
                return data
        except Exception as e:
            raise RuntimeError(f"OpenAI-compatible request to {self.base_url} failed: {e}") from e

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Iterator[str]:
        res = self.generate(messages, model, temperature, max_tokens, **kwargs)
        content = res.get("choices", [{}])[0].get("message", {}).get("content", "")
        for word in content.split(" "):
            yield word + " "

    def get_capabilities(self) -> List[str]:
        return ["streaming", "tool_calling", "structured_json", "vision"]
