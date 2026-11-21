"""
Offline Mock Embedding Engine for Master AI
============================================
Provides deterministic, normalized, zero-dependency embeddings for testing,
development, and offline execution without downloading large neural weights.
"""

import math
import re
import hashlib
from typing import List, Dict, Any
from .base_embedding import BaseEmbeddingEngine


class OfflineMockEmbeddingEngine(BaseEmbeddingEngine):
    """
    Deterministic pseudo-semantic embedding engine.
    Produces reproducible unit vectors using hashed token projections.
    """

    def __init__(self, dimension: int = 128, model_name: str = "offline-mock-embed-128"):
        self._dim = dimension
        self._model_name = model_name

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def is_mock(self) -> bool:
        return True

    def _token_to_vector(self, token: str) -> List[float]:
        """Project a single token deterministically into R^dim."""
        vec = [0.0] * self._dim
        h = hashlib.sha256(token.encode("utf-8")).digest()
        # Use 4-byte chunks from sha256 to seed coordinates
        for i in range(self._dim):
            byte_idx = (i * 2) % len(h)
            val = (h[byte_idx] << 8) | h[(byte_idx + 1) % len(h)]
            # Map [0, 65535] to [-1.0, 1.0]
            norm_val = (val / 32767.5) - 1.0
            vec[i] = norm_val
        return vec

    def embed_text(self, text: str) -> List[float]:
        """Generate a deterministic normalized embedding for text."""
        if not text or not text.strip():
            # Return unit vector pointing along first dimension for empty input
            vec = [0.0] * self._dim
            vec[0] = 1.0
            return vec

        cleaned = text.lower()
        tokens = re.findall(r"\w+", cleaned)
        if not tokens:
            tokens = [cleaned.strip()]

        accum = [0.0] * self._dim
        for token in tokens:
            t_vec = self._token_to_vector(token)
            for i in range(self._dim):
                accum[i] += t_vec[i]

        # Add whole-document hash to capture global phrasing
        doc_hash_vec = self._token_to_vector(f"__DOC__{cleaned}")
        for i in range(self._dim):
            accum[i] += doc_hash_vec[i] * 0.5

        # Normalize to L2 unit length
        norm_sq = sum(x * x for x in accum)
        if norm_sq < 1e-12:
            norm = 1.0
        else:
            norm = math.sqrt(norm_sq)

        return [x / norm for x in accum]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        return [self.embed_text(t) for t in texts]

    def health_check(self) -> Dict[str, Any]:
        """Return health status."""
        return {
            "status": "healthy",
            "mode": "deterministic_offline",
            "model_name": self._model_name,
            "dimension": self._dim,
            "is_mock": True,
            "paid_cost": 0.0,
        }
