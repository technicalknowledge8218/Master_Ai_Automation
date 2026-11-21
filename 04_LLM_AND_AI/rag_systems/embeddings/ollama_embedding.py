"""
Ollama Local Embedding Engine for Master AI
============================================
Communicates with local Ollama daemon for neural embeddings.
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
from .base_embedding import BaseEmbeddingEngine


class OllamaEmbeddingEngine(BaseEmbeddingEngine):
    """Embeddings via local Ollama daemon (e.g. nomic-embed-text, all-minilm)."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model_name: str = "nomic-embed-text",
        dimension: int = 768,
        timeout_seconds: float = 10.0,
    ):
        self._base_url = base_url.rstrip("/")
        self._model_name = model_name
        self._dim = dimension
        self._timeout = timeout_seconds

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def is_mock(self) -> bool:
        return False

    def health_check(self) -> Dict[str, Any]:
        """Check if Ollama is running and has the model loaded."""
        try:
            req = urllib.request.Request(f"{self._base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                model_loaded = any(self._model_name in m for m in models)
                return {
                    "status": "healthy" if model_loaded else "standby_no_weights",
                    "ollama_reachable": True,
                    "model_name": self._model_name,
                    "model_loaded": model_loaded,
                    "available_models": models,
                    "dimension": self._dim,
                    "is_mock": False,
                }
        except Exception as e:
            return {
                "status": "unreachable",
                "ollama_reachable": False,
                "model_name": self._model_name,
                "model_loaded": False,
                "error": str(e),
                "dimension": self._dim,
                "is_mock": False,
            }

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding vector using Ollama's /api/embeddings or /api/embed."""
        url = f"{self._base_url}/api/embeddings"
        payload = json.dumps({"model": self._model_name, "prompt": text}).encode("utf-8")
        req = urllib.request.Request(
            url, data=payload, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                vec = data.get("embedding", [])
                if not vec:
                    raise RuntimeError("Ollama returned empty embedding vector")
                self._dim = len(vec)
                return vec
        except Exception as e:
            raise RuntimeError(f"Ollama embedding failed for model '{self._model_name}': {e}")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch embedding via individual or combined calls."""
        return [self.embed_text(t) for t in texts]
