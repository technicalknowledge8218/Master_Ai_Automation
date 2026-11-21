"""Master AI - Agent Model Assignment Manager.

Allows configuring preferred models, backup models, task overrides,
and generation hyperparameters per agent without modifying agent source code.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class AgentModelConfig:
    """Model assignment and hyperparameter settings for a specific agent."""

    agent_slug: str
    preferred_model_id: str = "offline-mock-deterministic"
    backup_model_id: str = "offline-mock-deterministic"
    temperature: float = 0.5
    top_p: float = 0.95
    max_output_tokens: int = 2048
    capability_requirements: List[str] = field(default_factory=list)
    task_specific_overrides: Dict[str, str] = field(default_factory=dict)
    notes: str = ""


class AgentModelAssignmentManager:
    """Manages external agent model assignments and configuration persistence."""

    def __init__(self, config_file: Path | None = None) -> None:
        if config_file is None:
            workspace_root = Path(__file__).resolve().parents[2]
            config_file = workspace_root / "04_LLM_AND_AI" / "models" / "AGENT_MODEL_ASSIGNMENTS.json"

        self.config_file = config_file
        self._assignments: Dict[str, AgentModelConfig] = {}
        self.load()

    def _seed_defaults(self) -> None:
        defaults = [
            AgentModelConfig(
                agent_slug="coding_agent",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="qwen2.5:1.5b",
                temperature=0.2,
                max_output_tokens=4096,
                capability_requirements=["code_generation", "streaming"],
                task_specific_overrides={"refactoring": "offline-mock-deterministic", "bugfix": "offline-mock-deterministic"},
                notes="Strict low temperature for reproducible code output.",
            ),
            AgentModelConfig(
                agent_slug="research_agent",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="qwen2.5:1.5b",
                temperature=0.5,
                max_output_tokens=3072,
                capability_requirements=["reasoning", "streaming"],
                task_specific_overrides={"literature_survey": "offline-mock-deterministic"},
                notes="Balanced temperature for comprehensive synthesis.",
            ),
            AgentModelConfig(
                agent_slug="software_architect",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="llama-3.1-8b-instruct-local",
                temperature=0.3,
                max_output_tokens=4096,
                capability_requirements=["structured_json", "reasoning"],
                task_specific_overrides={"adr_design": "offline-mock-deterministic"},
                notes="High precision for architectural schemas and ADR generation.",
            ),
            AgentModelConfig(
                agent_slug="testing_agent",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="qwen2.5:1.5b",
                temperature=0.2,
                max_output_tokens=2048,
                capability_requirements=["code_generation"],
                task_specific_overrides={"negative_testing": "offline-mock-deterministic"},
                notes="Low temperature for test assertions and coverage.",
            ),
            AgentModelConfig(
                agent_slug="documentation_agent",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="qwen2.5:1.5b",
                temperature=0.6,
                max_output_tokens=3072,
                capability_requirements=["streaming"],
                notes="Clarity and readability formatting.",
            ),
            AgentModelConfig(
                agent_slug="security_auditor",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="llama-3.1-8b-instruct-local",
                temperature=0.1,
                max_output_tokens=2048,
                capability_requirements=["reasoning", "structured_json"],
                notes="Ultra-low temperature for adversarial compliance checking.",
            ),
            AgentModelConfig(
                agent_slug="capability_discovery_agent",
                preferred_model_id="offline-mock-deterministic",
                backup_model_id="qwen2.5:1.5b",
                temperature=0.4,
                max_output_tokens=2048,
                capability_requirements=["structured_json"],
                notes="Catalog inspection and capability classification.",
            ),
        ]
        self._assignments = {cfg.agent_slug: cfg for cfg in defaults}

    def load(self) -> None:
        """Load assignments from disk or seed defaults."""
        if self.config_file.is_file():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data.get("assignments", []):
                    cfg = AgentModelConfig(**item)
                    self._assignments[cfg.agent_slug] = cfg
                return
            except Exception:
                pass

        self._seed_defaults()
        self.save()

    def save(self) -> None:
        """Persist current assignments to disk."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0.0",
            "last_updated": "2026-11-17",
            "assignments": [asdict(c) for c in self._assignments.values()],
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def get_assignment(self, agent_slug: str) -> AgentModelConfig:
        """Fetch assignment for agent or fallback to safe defaults."""
        if agent_slug in self._assignments:
            return self._assignments[agent_slug]
        return AgentModelConfig(agent_slug=agent_slug)

    def update_assignment(
        self,
        agent_slug: str,
        preferred_model_id: str | None = None,
        backup_model_id: str | None = None,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
        task_specific_overrides: Dict[str, str] | None = None,
    ) -> AgentModelConfig:
        """Update settings for an agent and save."""
        cfg = self.get_assignment(agent_slug)
        if preferred_model_id is not None:
            cfg.preferred_model_id = preferred_model_id
        if backup_model_id is not None:
            cfg.backup_model_id = backup_model_id
        if temperature is not None:
            cfg.temperature = max(0.0, min(2.0, temperature))
        if max_output_tokens is not None:
            cfg.max_output_tokens = max(128, max_output_tokens)
        if task_specific_overrides is not None:
            cfg.task_specific_overrides.update(task_specific_overrides)

        self._assignments[agent_slug] = cfg
        self.save()
        return cfg

    def resolve_model_for_task(self, agent_slug: str, task_name: str | None = None) -> tuple[str, str]:
        """Return (preferred_model_id, backup_model_id) considering task overrides."""
        cfg = self.get_assignment(agent_slug)
        preferred = cfg.preferred_model_id
        if task_name and task_name in cfg.task_specific_overrides:
            preferred = cfg.task_specific_overrides[task_name]
        return preferred, cfg.backup_model_id

    def list_assignments(self) -> List[Dict[str, Any]]:
        """Return all agent model assignments."""
        return [asdict(c) for c in self._assignments.values()]
