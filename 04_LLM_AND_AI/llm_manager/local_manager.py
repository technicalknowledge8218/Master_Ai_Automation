"""Master AI - Local Model Manager (Ollama Native Integration).

Provides safe discovery, metadata inspection, storage-bounded pull management,
resource profile estimation, and guarded deletion requiring explicit human approval.
"""

from __future__ import annotations

import json
import os
import shutil
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .adapters.ollama_adapter import OllamaAdapter


@dataclass
class LocalModelProfile:
    """Metadata and resource profile for a local model."""

    name: str
    size_bytes: int
    size_gb: float
    modified_at: str
    digest: str
    parameter_size: str = "Unknown"
    quantization_level: str = "Unknown"
    estimated_ram_gb: float = 0.0
    status: str = "INSTALLED"


class LocalModelManager:
    """Manages local model lifecycle on Ollama daemon with strict safety bounds."""

    def __init__(self, ollama_adapter: OllamaAdapter | None = None) -> None:
        self.adapter = ollama_adapter or OllamaAdapter()
        self.base_url = self.adapter.base_url
        self.max_model_size_gb = float(os.getenv("MAX_LOCAL_MODEL_SIZE_GB", "2.73"))

    def check_daemon(self) -> tuple[bool, str]:
        """Check if local Ollama daemon is reachable."""
        return self.adapter.is_available()

    def list_installed_models(self) -> List[LocalModelProfile]:
        """Discover and profile all locally cached Ollama models."""
        raw_models = self.adapter.list_installed_models()
        profiles: List[LocalModelProfile] = []

        for m in raw_models:
            size_b = m.get("size", 0)
            size_gb = round(size_b / (1024**3), 2)
            details = m.get("details", {})
            param_size = details.get("parameter_size", "Unknown")
            quant = details.get("quantization_level", "Unknown")

            # Estimate required RAM: ~1.2x file size on disk for Q4 inference + KV cache
            ram_estimate = round(size_gb * 1.25, 2)

            profiles.append(
                LocalModelProfile(
                    name=m.get("name", "unknown"),
                    size_bytes=size_b,
                    size_gb=size_gb,
                    modified_at=m.get("modified_at", ""),
                    digest=m.get("digest", "")[:12],
                    parameter_size=param_size,
                    quantization_level=quant,
                    estimated_ram_gb=ram_estimate,
                )
            )
        return profiles

    def get_model_details(self, model_name: str) -> Dict[str, Any]:
        """Fetch full parameter details, license, and template of an installed model."""
        return self.adapter.get_model_info(model_name)

    def estimate_model_resource_needs(self, param_billions: float, quant: str = "Q4") -> Dict[str, Any]:
        """Estimate required disk and RAM before downloading a model."""
        # Baseline Q4 footprint: ~0.6 GB per billion parameters
        multiplier = 0.6 if "4" in quant else (0.8 if "5" in quant else 1.0)
        disk_gb = round(param_billions * multiplier, 2)
        ram_gb = round(disk_gb * 1.3, 2)  # includes 2-4K context KV cache
        within_budget = disk_gb <= self.max_model_size_gb

        return {
            "parameter_billions": param_billions,
            "quantization": quant,
            "estimated_disk_gb": disk_gb,
            "estimated_ram_gb": ram_gb,
            "max_allowed_size_gb": self.max_model_size_gb,
            "allowed_for_automatic_pull": within_budget,
            "safety_verdict": "APPROVED_WITHIN_BUDGET" if within_budget else "EXCEEDS_STORAGE_BUDGET",
        }

    def pull_model(self, model_name: str, estimated_size_gb: float = 0.0) -> Dict[str, Any]:
        """Safely pull a model from Ollama library, enforcing storage limits."""
        if estimated_size_gb > self.max_model_size_gb:
            return {
                "success": False,
                "error": f"Pull rejected: Model size ({estimated_size_gb:.2f} GB) exceeds safe maximum ({self.max_model_size_gb:.2f} GB).",
            }

        available, msg = self.check_daemon()
        if not available:
            return {"success": False, "error": f"Ollama daemon unreachable: {msg}"}

        payload = {"name": model_name, "stream": False}
        req = urllib.request.Request(
            f"{self.base_url}/api/pull",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "result": data, "model": model_name}
        except Exception as e:
            return {"success": False, "error": f"Pull operation failed: {e}", "model": model_name}

    def delete_model(self, model_name: str, explicit_user_approval: bool = False) -> Dict[str, Any]:
        """Delete an installed model ONLY after explicit user confirmation."""
        if not explicit_user_approval:
            return {
                "success": False,
                "error": "Model deletion rejected: explicit_user_approval=True is strictly required to prevent data loss.",
            }

        payload = {"name": model_name}
        req = urllib.request.Request(
            f"{self.base_url}/api/delete",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="DELETE",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {
                    "success": True,
                    "message": f"Model '{model_name}' deleted successfully with explicit user approval.",
                }
        except Exception as e:
            return {"success": False, "error": f"Delete request failed: {e}"}
