"""Master AI - Intelligent Model Router.

Selects the optimal model and provider adapter based on task requirements,
intelligence level, cost constraints, capabilities, and availability.
Enforces automatic fallback, retries, and strict zero-paid-model safeguards.
"""

from __future__ import annotations

import datetime
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .model_registry import ModelProfile, ModelRegistry
from .provider_registry import ProviderRegistry
from .security import SecurityBoundary

logger = logging.getLogger("master_ai.router")


@dataclass
class RoutingRequest:
    """Request specification passed to IntelligentModelRouter."""

    task_type: str = "general"  # coding, reasoning, research, fast_chat, creative, structured_json, multimodal
    intelligence_level: str = "medium"  # low, medium, high, frontier
    required_capabilities: List[str] = field(default_factory=list)
    min_context_tokens: int = 4096
    preferred_model_id: Optional[str] = None
    backup_model_id: Optional[str] = None
    allow_paid_models: bool = False
    max_retries: int = 2
    timeout_seconds: float = 30.0


@dataclass
class FallbackRecord:
    """Logged record of a routing execution or fallback."""

    timestamp: str
    task_type: str
    primary_model: str
    primary_error: Optional[str]
    resolved_model: str
    success: bool
    latency_ms: float
    retries_attempted: int


class IntelligentModelRouter:
    """Core routing engine orchestrating LLM execution and fallbacks."""

    def __init__(
        self,
        model_registry: ModelRegistry | None = None,
        provider_registry: ProviderRegistry | None = None,
        security_boundary: SecurityBoundary | None = None,
    ) -> None:
        self.model_registry = model_registry or ModelRegistry()
        self.provider_registry = provider_registry or ProviderRegistry()
        self.security = security_boundary or SecurityBoundary()
        self.fallback_history: List[FallbackRecord] = []

    def select_model(self, req: RoutingRequest) -> tuple[ModelProfile, List[ModelProfile]]:
        """Select optimal primary model and fallback candidate list.

        Guarantees:
        - NEVER returns a paid model if req.allow_paid_models is False or policy forbids.
        - Matches required capabilities and context window.
        """
        # If user explicitly preferred an active model
        if req.preferred_model_id:
            profile = self.model_registry.get_model(req.preferred_model_id)
            if profile and "ACTIVE" in profile.status:
                can_run, _ = self.security.can_invoke_model(
                    profile.model_id,
                    profile.pricing_per_1m_input_usd,
                    is_local_or_mock=(profile.pricing_per_1m_input_usd == 0.0),
                )
                if can_run:
                    backups = self._resolve_backups(req, exclude=[profile.model_id])
                    return profile, backups

        # Task-based matching
        candidates = self.model_registry.list_models()

        def score_model(m: ModelProfile) -> float:
            score = 0.0
            # Offline/Free bonus when paid models are forbidden
            if m.pricing_per_1m_input_usd == 0.0:
                score += 50.0
            elif not req.allow_paid_models or self.model_registry.enforce_zero_paid_api:
                return -999.0  # Disqualified

            # Intelligence level matching
            tier_scores = {
                "mock": 10.0 if req.intelligence_level == "low" else 5.0,
                "tier_3_edge_local": 25.0 if req.intelligence_level in ("low", "medium") else 15.0,
                "tier_2_fast_efficient": 30.0 if req.intelligence_level in ("medium", "high") else 20.0,
                "tier_1_flagship": 40.0 if req.intelligence_level in ("high", "frontier") else 10.0,
            }
            score += tier_scores.get(m.tier, 10.0)

            # Capability matches
            for cap in req.required_capabilities:
                if m.has_capability(cap):
                    score += 15.0
                else:
                    score -= 20.0

            # Task type specialization
            if req.task_type == "coding" and m.has_capability("code_generation"):
                score += 20.0
            elif req.task_type == "reasoning" and (m.has_capability("reasoning") or m.has_capability("deep_reasoning")):
                score += 20.0
            elif req.task_type == "structured_json" and m.has_capability("structured_json"):
                score += 15.0

            # Context size fit
            if m.context_window_tokens >= req.min_context_tokens:
                score += 10.0
            else:
                score -= 50.0

            # Availability check of underlying provider
            adapter = self.provider_registry.get_adapter(m.provider)
            if adapter:
                avail, _ = adapter.is_available()
                if avail:
                    score += 15.0
                else:
                    score -= 40.0
            else:
                score -= 30.0

            return score

        scored = sorted(candidates, key=score_model, reverse=True)
        # Filter out disqualified models
        eligible = [m for m in scored if score_model(m) > 0.0]

        if not eligible:
            # Absolute fallback to offline mock model
            mock_profile = self.model_registry.get_model("offline-mock-deterministic")
            return mock_profile, []

        primary = eligible[0]
        backups = eligible[1:4]
        return primary, backups

    def _resolve_backups(self, req: RoutingRequest, exclude: List[str]) -> List[ModelProfile]:
        """Find secondary fallback candidates."""
        models = self.model_registry.list_models()
        valid = []
        for m in models:
            if m.model_id in exclude:
                continue
            if not req.allow_paid_models and m.pricing_per_1m_input_usd > 0.0:
                continue
            valid.append(m)
        return valid[:3]

    def execute_completion(
        self,
        messages: List[Dict[str, str]],
        routing_request: RoutingRequest | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Execute chat completion with automatic retry, fallback, and audit logging."""
        req = routing_request or RoutingRequest()
        primary_model, fallbacks = self.select_model(req)
        chain = [primary_model] + fallbacks

        last_error: Optional[str] = None
        t0 = time.time()
        retries = 0

        for idx, model in enumerate(chain):
            adapter = self.provider_registry.get_adapter(model.provider)
            if not adapter:
                last_error = f"No provider adapter registered for '{model.provider}'"
                continue

            # Verify security permissions
            can_run, reason = self.security.can_invoke_model(
                model.model_id,
                model.pricing_per_1m_input_usd,
                is_local_or_mock=adapter.is_local_or_mock,
            )
            if not can_run:
                last_error = f"Security block on '{model.model_id}': {reason}"
                continue

            # Try execution with configured retries
            for attempt in range(req.max_retries + 1):
                try:
                    res = adapter.generate(
                        messages=messages,
                        model=model.model_id,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **kwargs,
                    )
                    # Successful completion
                    latency_ms = round((time.time() - t0) * 1000, 2)
                    record = FallbackRecord(
                        timestamp=datetime.datetime.now().isoformat(),
                        task_type=req.task_type,
                        primary_model=primary_model.model_id,
                        primary_error=last_error if idx > 0 else None,
                        resolved_model=model.model_id,
                        success=True,
                        latency_ms=latency_ms,
                        retries_attempted=retries,
                    )
                    self.fallback_history.append(record)
                    res["routing_metadata"] = {
                        "resolved_model": model.model_id,
                        "provider": model.provider,
                        "fallback_triggered": idx > 0,
                        "latency_ms": latency_ms,
                    }
                    return res
                except Exception as e:
                    retries += 1
                    last_error = str(e)
                    time.sleep(0.05 * (2**attempt))

        # If all candidates in chain failed, fallback to offline mock engine
        mock_adapter = self.provider_registry.get_adapter("OfflineMockProvider")
        if mock_adapter:
            res = mock_adapter.generate(
                messages=messages,
                model="offline-mock-deterministic",
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
            latency_ms = round((time.time() - t0) * 1000, 2)
            self.fallback_history.append(
                FallbackRecord(
                    timestamp=datetime.datetime.now().isoformat(),
                    task_type=req.task_type,
                    primary_model=primary_model.model_id,
                    primary_error=last_error,
                    resolved_model="offline-mock-deterministic",
                    success=True,
                    latency_ms=latency_ms,
                    retries_attempted=retries,
                )
            )
            res["routing_metadata"] = {
                "resolved_model": "offline-mock-deterministic",
                "provider": "OfflineMockProvider",
                "fallback_triggered": True,
                "latency_ms": latency_ms,
                "exhausted_chain_error": last_error,
            }
            return res

        raise RuntimeError(f"All LLM routing options failed. Last error: {last_error}")

    def execute_stream(
        self,
        messages: List[Dict[str, str]],
        routing_request: RoutingRequest | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> Iterator[str]:
        """Stream completion tokens using resolved model."""
        req = routing_request or RoutingRequest()
        primary_model, _ = self.select_model(req)
        adapter = self.provider_registry.get_adapter(primary_model.provider) or self.provider_registry.get_adapter("OfflineMockProvider")
        yield from adapter.generate_stream(
            messages=messages,
            model=primary_model.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    def get_fallback_history(self) -> List[Dict[str, Any]]:
        """Return history of all fallback occurrences."""
        return [
            {
                "timestamp": r.timestamp,
                "task_type": r.task_type,
                "primary_model": r.primary_model,
                "primary_error": r.primary_error,
                "resolved_model": r.resolved_model,
                "success": r.success,
                "latency_ms": r.latency_ms,
                "retries": r.retries_attempted,
            }
            for r in self.fallback_history
        ]
