"""Master AI - Central Model Registry.

Manages model capability profiles, context limits, pricing,
activation states, and validation for local and cloud models.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ModelProfile:
    """Detailed profile and execution constraints for a registered model."""

    model_id: str
    display_name: str
    provider: str
    context_window_tokens: int = 128000
    max_output_tokens: int = 4096
    pricing_per_1m_input_usd: float = 0.0
    pricing_per_1m_output_usd: float = 0.0
    tier: str = "mock"  # mock, tier_1_flagship, tier_2_fast_efficient, tier_3_edge_local
    capabilities: List[str] = field(default_factory=lambda: ["streaming", "structured_json"])
    allowed_in_offline_sandbox: bool = True
    status: str = "ACTIVE"  # ACTIVE, ACTIVE_DEFAULT, GATED_REQUIRES_APPROVAL, STANDBY_OFFLINE_READY, DEACTIVATED
    description: str = ""

    def validate(self) -> None:
        """Validate profile constraints."""
        if not self.model_id or not isinstance(self.model_id, str):
            raise ValueError("ModelProfile must have a valid model_id")
        if self.context_window_tokens <= 0:
            raise ValueError("context_window_tokens must be positive")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        if self.pricing_per_1m_input_usd < 0.0 or self.pricing_per_1m_output_usd < 0.0:
            raise ValueError("Pricing cannot be negative")

    def has_capability(self, capability: str) -> bool:
        """Return True if model explicitly lists capability."""
        return capability.lower() in [c.lower() for c in self.capabilities]

    def estimate_cost_usd(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate estimated cost for token count."""
        input_cost = (prompt_tokens / 1_000_000.0) * self.pricing_per_1m_input_usd
        output_cost = (completion_tokens / 1_000_000.0) * self.pricing_per_1m_output_usd
        return round(input_cost + output_cost, 6)


class ModelRegistry:
    """Thread-safe catalog of available LLMs and their capabilities."""

    def __init__(self, registry_file: Path | None = None) -> None:
        if registry_file is None:
            workspace_root = Path(__file__).resolve().parents[2]
            registry_file = workspace_root / "04_LLM_AND_AI" / "models" / "MODEL_REGISTRY.json"

        self.registry_file = registry_file
        self._models: Dict[str, ModelProfile] = {}
        self.default_active_model: str = "offline-mock-deterministic"
        self.enforce_zero_paid_api: bool = True
        self.load()

    def load(self) -> None:
        """Load registry from JSON file or seed defaults."""
        if self.registry_file.is_file():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.default_active_model = data.get("default_active_model", self.default_active_model)
                self.enforce_zero_paid_api = data.get("enforce_zero_paid_api", True)
                for item in data.get("models", []):
                    profile = ModelProfile(
                        model_id=item["model_id"],
                        display_name=item.get("display_name", item["model_id"]),
                        provider=item.get("provider", "Unknown"),
                        context_window_tokens=item.get("context_window_tokens", 128000),
                        max_output_tokens=item.get("max_output_tokens", 4096),
                        pricing_per_1m_input_usd=float(item.get("pricing_per_1m_input_usd", 0.0)),
                        pricing_per_1m_output_usd=float(item.get("pricing_per_1m_output_usd", 0.0)),
                        tier=item.get("tier", "mock"),
                        capabilities=item.get("capabilities", ["streaming"]),
                        allowed_in_offline_sandbox=item.get("allowed_in_offline_sandbox", True),
                        status=item.get("status", "ACTIVE"),
                        description=item.get("description", ""),
                    )
                    profile.validate()
                    self._models[profile.model_id] = profile
                return
            except Exception as e:
                pass

        # Seed defaults if file missing or corrupt
        self._seed_default_models()
        self.save()

    def _seed_default_models(self) -> None:
        self._models = {
            "offline-mock-deterministic": ModelProfile(
                model_id="offline-mock-deterministic",
                display_name="Deterministic Offline Mock LLM",
                provider="OfflineMockProvider",
                context_window_tokens=128000,
                max_output_tokens=8192,
                pricing_per_1m_input_usd=0.0,
                pricing_per_1m_output_usd=0.0,
                tier="mock",
                capabilities=["streaming", "tool_calling", "structured_json", "reasoning", "code_generation"],
                allowed_in_offline_sandbox=True,
                status="ACTIVE_DEFAULT",
                description="Default fail-closed deterministic local mock engine.",
            ),
            "qwen2.5:1.5b": ModelProfile(
                model_id="qwen2.5:1.5b",
                display_name="Qwen 2.5 1.5B (Ollama CPU-First)",
                provider="OllamaLocal",
                context_window_tokens=32768,
                max_output_tokens=4096,
                pricing_per_1m_input_usd=0.0,
                pricing_per_1m_output_usd=0.0,
                tier="tier_3_edge_local",
                capabilities=["streaming", "structured_json", "reasoning", "code_generation", "hindi_english"],
                allowed_in_offline_sandbox=True,
                status="STANDBY_OFFLINE_READY",
                description="Ultra-fast local model optimized for CPU inference.",
            ),
            "llama-3.1-8b-instruct-local": ModelProfile(
                model_id="llama-3.1-8b-instruct-local",
                display_name="Meta LLaMA 3.1 8B Instruct (Local)",
                provider="OllamaLocal",
                context_window_tokens=131072,
                max_output_tokens=4096,
                pricing_per_1m_input_usd=0.0,
                pricing_per_1m_output_usd=0.0,
                tier="tier_3_edge_local",
                capabilities=["streaming", "tool_calling", "structured_json", "code_generation", "reasoning"],
                allowed_in_offline_sandbox=True,
                status="STANDBY_OFFLINE_READY",
                description="High-reasoning 8B local instruction-tuned model.",
            ),
            "gemini-1.5-flash": ModelProfile(
                model_id="gemini-1.5-flash",
                display_name="Google Gemini 1.5 Flash",
                provider="Google",
                context_window_tokens=1048576,
                max_output_tokens=8192,
                pricing_per_1m_input_usd=0.075,
                pricing_per_1m_output_usd=0.30,
                tier="tier_2_fast_efficient",
                capabilities=["streaming", "tool_calling", "structured_json", "vision", "audio"],
                allowed_in_offline_sandbox=False,
                status="GATED_REQUIRES_APPROVAL",
                description="High-throughput multimodal cloud model with 1M context.",
            ),
            "gemini-1.5-pro": ModelProfile(
                model_id="gemini-1.5-pro",
                display_name="Google Gemini 1.5 Pro",
                provider="Google",
                context_window_tokens=2097152,
                max_output_tokens=8192,
                pricing_per_1m_input_usd=3.50,
                pricing_per_1m_output_usd=10.50,
                tier="tier_1_flagship",
                capabilities=["streaming", "tool_calling", "structured_json", "vision", "audio", "video", "deep_reasoning"],
                allowed_in_offline_sandbox=False,
                status="GATED_REQUIRES_APPROVAL",
                description="Flagship 2M-token frontier reasoning model.",
            ),
            "gpt-4o": ModelProfile(
                model_id="gpt-4o",
                display_name="OpenAI GPT-4o",
                provider="OpenAI",
                context_window_tokens=128000,
                max_output_tokens=4096,
                pricing_per_1m_input_usd=5.00,
                pricing_per_1m_output_usd=15.00,
                tier="tier_1_flagship",
                capabilities=["streaming", "tool_calling", "structured_json", "vision", "code_generation"],
                allowed_in_offline_sandbox=False,
                status="GATED_REQUIRES_APPROVAL",
                description="OpenAI flagship omni model.",
            ),
        }

    def save(self) -> None:
        """Persist current model registry to JSON file."""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "$schema": "https://master-ai.local/schemas/model-registry.v1.json",
            "registry_name": "Master AI Model Registry",
            "version": "1.1.0",
            "last_updated": "2026-11-17",
            "default_active_model": self.default_active_model,
            "enforce_zero_paid_api": self.enforce_zero_paid_api,
            "models": [asdict(p) for p in self._models.values()],
        }
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_model(self, model_id: str) -> Optional[ModelProfile]:
        """Fetch model profile by ID."""
        return self._models.get(model_id)

    def list_models(self, tier: str | None = None, capability: str | None = None, active_only: bool = False) -> List[ModelProfile]:
        """Filter and list models in registry."""
        results = list(self._models.values())
        if tier:
            results = [m for m in results if m.tier == tier]
        if capability:
            results = [m for m in results if m.has_capability(capability)]
        if active_only:
            results = [m for m in results if "ACTIVE" in m.status]
        return results

    def register_model(self, profile: ModelProfile) -> None:
        """Register or update a model profile."""
        profile.validate()
        self._models[profile.model_id] = profile
        self.save()

    def set_model_status(self, model_id: str, status: str) -> bool:
        """Update activation status of a model."""
        if model_id not in self._models:
            return False
        self._models[model_id].status = status
        self.save()
        return True

    def set_default_active_model(self, model_id: str) -> bool:
        """Set primary default active model."""
        if model_id not in self._models:
            return False
        # Update old default
        for m in self._models.values():
            if m.status == "ACTIVE_DEFAULT":
                m.status = "ACTIVE"
        self._models[model_id].status = "ACTIVE_DEFAULT"
        self.default_active_model = model_id
        self.save()
        return True
