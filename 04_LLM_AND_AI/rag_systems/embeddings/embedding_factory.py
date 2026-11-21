"""
Embedding Engine Factory for Master AI
=======================================
Instantiates appropriate embedding provider with automatic fallback.
"""

from typing import Optional
from .base_embedding import BaseEmbeddingEngine
from .offline_mock_embedding import OfflineMockEmbeddingEngine
from .ollama_embedding import OllamaEmbeddingEngine
from .cloud_embedding import CloudEmbeddingEngine


def get_embedding_engine(
    engine_type: str = "auto",
    dimension: int = 128,
    model_name: Optional[str] = None,
    **kwargs,
) -> BaseEmbeddingEngine:
    """
    Factory function for obtaining an embedding engine.

    Modes:
      - "auto": Checks Ollama availability; if loaded returns Ollama engine, else offline mock.
      - "mock": Deterministic pure-Python offline mock (default for testing/offline).
      - "ollama": Local Ollama embedding engine.
      - "cloud": Cloud provider gated by SecurityBoundary.
    """
    engine_type = engine_type.lower()

    if engine_type == "mock":
        name = model_name or f"offline-mock-embed-{dimension}"
        return OfflineMockEmbeddingEngine(dimension=dimension, model_name=name)

    if engine_type == "ollama":
        name = model_name or "nomic-embed-text"
        return OllamaEmbeddingEngine(model_name=name, dimension=dimension or 768, **kwargs)

    if engine_type == "cloud":
        name = model_name or "text-embedding-3-small"
        return CloudEmbeddingEngine(model_name=name, dimension=dimension or 1536, **kwargs)

    if engine_type == "auto":
        # Check Ollama first
        try:
            ollama = OllamaEmbeddingEngine(
                model_name=model_name or "nomic-embed-text",
                dimension=dimension or 768,
                **kwargs,
            )
            health = ollama.health_check()
            if health.get("status") == "healthy" and health.get("model_loaded"):
                return ollama
        except Exception:
            pass

        # Fallback to deterministic offline mock
        name = model_name or f"offline-mock-embed-{dimension}"
        return OfflineMockEmbeddingEngine(dimension=dimension, model_name=name)

    raise ValueError(f"Unknown embedding engine type: {engine_type}")
