"""
Base Embedding Protocol for Master AI RAG System
=================================================
Defines the standard interface for embedding engines.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseEmbeddingEngine(ABC):
    """Abstract base class for all embedding providers."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Vector dimensionality produced by this engine."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Name or identifier of the embedding model."""
        pass

    @property
    @abstractmethod
    def is_mock(self) -> bool:
        """True if this engine produces deterministic offline test embeddings."""
        pass

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate a normalized embedding vector for a single string."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate normalized embedding vectors for a list of strings."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Return connectivity and readiness status."""
        pass
