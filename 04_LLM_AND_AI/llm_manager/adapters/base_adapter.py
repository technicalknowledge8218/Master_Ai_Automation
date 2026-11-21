"""Master AI - Base LLM Provider Adapter Protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List


class BaseLLMAdapter(ABC):
    """Abstract base class for all Master AI intelligence provider adapters."""

    def __init__(self, name: str, is_local_or_mock: bool = False) -> None:
        self.name = name
        self.is_local_or_mock = is_local_or_mock

    @abstractmethod
    def is_available(self) -> tuple[bool, str]:
        """Check if provider daemon or endpoint is reachable."""
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Return diagnostic health status."""
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Execute chat completion and return standardized response dictionary."""
        raise NotImplementedError

    @abstractmethod
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Iterator[str]:
        """Yield response tokens sequentially for streaming interfaces."""
        raise NotImplementedError

    def get_capabilities(self) -> List[str]:
        """Return supported capabilities (e.g. streaming, structured_json, tool_calling)."""
        return ["streaming", "structured_json"]
