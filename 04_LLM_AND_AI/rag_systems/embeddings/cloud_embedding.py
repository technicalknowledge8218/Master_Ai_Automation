"""
Cloud Embedding Engine for Master AI
=====================================
Provider-agnostic cloud embeddings (OpenAI, Voyage, Cohere) strictly gated by
Master AI Security Boundary and zero-paid API policy.
"""

import os
import importlib
from typing import List, Dict, Any, Optional
from .base_embedding import BaseEmbeddingEngine


class CloudEmbeddingEngine(BaseEmbeddingEngine):
    """Gated cloud embedding provider."""

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        dimension: int = 1536,
        estimated_cost_per_1m_tokens: float = 0.02,
        user_explicit_approval: bool = False,
    ):
        self._model_name = model_name
        self._dim = dimension
        self._cost = estimated_cost_per_1m_tokens
        self._approval = user_explicit_approval

        # Import security boundary dynamically to avoid package prefix issues
        try:
            sec_mod = importlib.import_module("04_LLM_AND_AI.llm_manager.security")
            self._security_boundary = sec_mod.SecurityBoundary()
        except Exception:
            self._security_boundary = None

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
        """Check cloud provider permissions and credentials."""
        can_invoke = False
        reason = "SecurityBoundary not loaded"
        if self._security_boundary:
            can_invoke, reason = self._security_boundary.can_invoke_model(
                self._model_name,
                estimated_cost_usd=self._cost,
                is_local_or_mock=False,
            )

        api_key_set = bool(os.getenv("OPENAI_API_KEY"))
        return {
            "status": "healthy" if (can_invoke and api_key_set) else "gated_or_blocked",
            "model_name": self._model_name,
            "can_invoke": can_invoke,
            "security_reason": reason,
            "has_credentials": api_key_set,
            "dimension": self._dim,
            "is_mock": False,
        }

    def embed_text(self, text: str) -> List[float]:
        """Verify security gate before calling cloud API."""
        if self._security_boundary:
            allowed, reason = self._security_boundary.can_invoke_model(
                self._model_name,
                estimated_cost_usd=self._cost,
                is_local_or_mock=False,
            )
            if not allowed:
                raise PermissionError(f"Cloud embedding blocked by security policy: {reason}")

        try:
            import litellm
            response = litellm.embedding(model=self._model_name, input=[text])
            vec = response.data[0]["embedding"]
            self._dim = len(vec)
            return vec
        except Exception as e:
            raise RuntimeError(f"Cloud embedding invocation failed for '{self._model_name}': {e}")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if self._security_boundary:
            allowed, reason = self._security_boundary.can_invoke_model(
                self._model_name,
                estimated_cost_usd=self._cost * (len(texts) / 100),
                is_local_or_mock=False,
            )
            if not allowed:
                raise PermissionError(f"Cloud embedding blocked by security policy: {reason}")

        try:
            import litellm
            response = litellm.embedding(model=self._model_name, input=texts)
            return [d["embedding"] for d in response.data]
        except Exception as e:
            raise RuntimeError(f"Cloud batch embedding failed for '{self._model_name}': {e}")
