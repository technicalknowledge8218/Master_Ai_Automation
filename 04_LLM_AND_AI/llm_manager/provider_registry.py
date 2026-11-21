"""Master AI - Provider Registry & Adapter Manager.

Tracks available LLM providers, performs availability monitoring,
health checks, and handles adapter instantiation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .adapters.base_adapter import BaseLLMAdapter
from .adapters.litellm_adapter import LiteLLMAdapter
from .adapters.offline_mock_adapter import OfflineMockAdapter
from .adapters.ollama_adapter import OllamaAdapter
from .adapters.openai_adapter import OpenAICompatibleAdapter


class ProviderRegistry:
    """Manages active LLM provider adapters and monitors their status."""

    def __init__(self) -> None:
        self._adapters: Dict[str, BaseLLMAdapter] = {}
        self._register_default_adapters()

    def _register_default_adapters(self) -> None:
        self.register_adapter("OfflineMockProvider", OfflineMockAdapter())
        self.register_adapter("OllamaLocal", OllamaAdapter())
        self.register_adapter("LiteLLMGateway", LiteLLMAdapter())
        self.register_adapter("OpenAI", OpenAICompatibleAdapter(name="OpenAI"))
        self.register_adapter("Google", OpenAICompatibleAdapter(name="Google"))

    def register_adapter(self, provider_id: str, adapter: BaseLLMAdapter) -> None:
        """Register an adapter instance."""
        self._adapters[provider_id] = adapter

    def get_adapter(self, provider_id: str) -> Optional[BaseLLMAdapter]:
        """Fetch adapter by provider name."""
        return self._adapters.get(provider_id)

    def list_providers(self) -> List[Dict[str, Any]]:
        """List all providers and their availability status."""
        results = []
        for pid, adapter in self._adapters.items():
            avail, msg = adapter.is_available()
            results.append({
                "provider_id": pid,
                "name": adapter.name,
                "is_local_or_mock": adapter.is_local_or_mock,
                "is_available": avail,
                "status_message": msg,
                "capabilities": adapter.get_capabilities(),
            })
        return results

    def check_health_all(self) -> Dict[str, Any]:
        """Run diagnostic health check across all registered providers."""
        reports = {}
        for pid, adapter in self._adapters.items():
            reports[pid] = adapter.health_check()
        return reports
