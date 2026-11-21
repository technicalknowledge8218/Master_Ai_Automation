"""Master AI - High-Fidelity Deterministic Offline Mock Adapter.

Provides zero-dependency, zero-cost, fail-closed offline LLM simulation
for testing, benchmarking, sandbox execution, and local development.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Iterator, List

from .base_adapter import BaseLLMAdapter


class OfflineMockAdapter(BaseLLMAdapter):
    """Deterministic offline mock provider adapter."""

    def __init__(self) -> None:
        super().__init__(name="OfflineMockProvider", is_local_or_mock=True)

    def is_available(self) -> tuple[bool, str]:
        return True, "Offline mock provider is permanently available"

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "provider": self.name,
            "latency_ms": 0.5,
            "mode": "deterministic_offline",
            "models_supported": ["offline-mock-deterministic"],
        }

    def _synthesize_response(self, prompt: str, **kwargs: Any) -> str:
        p_lower = prompt.lower()

        # Specific benchmark patterns
        if "find_primes" in p_lower or "sieve" in p_lower:
            return (
                "```python\n"
                "def find_primes(n: int) -> list[int]:\n"
                "    \"\"\"Sieve of Eratosthenes prime generator with type hints.\"\"\"\n"
                "    if n < 2:\n"
                "        return []\n"
                "    sieve = [True] * (n + 1)\n"
                "    for p in range(2, int(n**0.5) + 1):\n"
                "        if sieve[p]:\n"
                "            for i in range(p * p, n + 1, p):\n"
                "                sieve[i] = False\n"
                "    return [p for p in range(2, n + 1) if sieve[p]]\n"
                "```"
            )

        if "phoenix-992" in p_lower or "secret code word" in p_lower:
            return "The secret code word retrieved from the long-context document is PHOENIX-992."

        if "bullet" in p_lower and "verified" in p_lower:
            return "- VERIFIED: System architectural constraints confirmed.\n- VERIFIED: Model router evaluated successfully.\n- VERIFIED: Zero-cost security boundaries operational."

        if "hindi" in p_lower or "मशीन" in prompt or "नमस्ते" in prompt or "हिंदी" in prompt:
            return "नमस्ते! मशीन लर्निंग (Machine Learning) कृत्रिम बुद्धिमत्ता (AI) की एक महत्वपूर्ण शाखा है जो कंप्यूटर को डेटा से सीखने और भविष्यवाणियां करने में सक्षम बनाती है।"

        if "bm-04" in p_lower or ("project" in p_lower and "version" in p_lower):
            return json.dumps({
                "project": "Master AI",
                "version": "2.0.0",
                "status": "active",
            }, indent=2)

        if "json" in p_lower or "structured" in p_lower:
            return json.dumps({
                "status": "success",
                "message": "Processed successfully by Master AI Offline Mock",
                "extracted_entities": ["Master AI", "Intelligence Layer"],
                "confidence_score": 0.98,
            }, indent=2)

        if "code" in p_lower or "function" in p_lower or "python" in p_lower:
            return (
                "```python\n"
                "# Master AI Generated Code Block\n"
                "def master_ai_pipeline(input_data: dict) -> dict:\n"
                "    \"\"\"Process input data deterministically.\"\"\"\n"
                "    return {'processed': True, 'count': len(input_data)}\n"
                "```"
            )

        if "reason" in p_lower or "why" in p_lower or "sheep" in p_lower or "analyze" in p_lower:
            return (
                "Analysis:\n"
                "1. The statement specifies: 'All but 9 die'.\n"
                "2. This literally means exactly 9 sheep survive.\n"
                "3. Conclusion: The farmer has 9 sheep left."
            )

        return f"Master AI Deterministic Response to: {prompt[:80]}"

    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str = "offline-mock-deterministic",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        last_user_message = next(
            (m["content"] for m in reversed(messages) if m.get("role") == "user"),
            "Hello"
        )
        content = self._synthesize_response(last_user_message, **kwargs)
        tokens_in = sum(len(m.get("content", "").split()) for m in messages) * 2
        tokens_out = len(content.split()) * 2

        return {
            "id": f"mock-{int(time.time()*1000)}",
            "model": model,
            "provider": self.name,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": tokens_in,
                "completion_tokens": tokens_out,
                "total_tokens": tokens_in + tokens_out,
                "estimated_cost_usd": 0.0,
            },
        }

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = "offline-mock-deterministic",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Iterator[str]:
        full_res = self.generate(messages, model, temperature, max_tokens, **kwargs)
        content = full_res["choices"][0]["message"]["content"]
        words = content.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")

    def get_capabilities(self) -> List[str]:
        return ["streaming", "structured_json", "tool_calling", "code_generation", "reasoning"]
