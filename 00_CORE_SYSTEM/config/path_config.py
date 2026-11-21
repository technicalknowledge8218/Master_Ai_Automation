"""Master AI - Centralized Path Configuration Module.

Resolves workspace root dynamically with MASTER_AI_ROOT environment override.
Validates the presence of expected core architectural directories and provides
consistent, canonical Path accessors across the entire ecosystem.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Sequence

# Required directories used to validate that a path is a genuine Master AI root
EXPECTED_CORE_DIRECTORIES: Sequence[str] = (
    "00_CORE_SYSTEM",
    "01_GLOBAL_RULES",
    "02_SKILLS",
    "03_AI_AGENTS",
    "04_LLM_AND_AI",
    "18_TESTING_AND_QA",
    "23_CHANGELOG_AND_BACKUP",
)


def _detect_workspace_root() -> Path:
    """Detect and validate the Master AI workspace root directory.

    Priority:
    1. MASTER_AI_ROOT environment variable (if set and valid).
    2. Dynamic resolution relative to this file's location (parents[2]).
    3. Current working directory or parent traversal fallback.
    """
    env_root = os.getenv("MASTER_AI_ROOT")
    if env_root:
        candidate = Path(env_root).resolve()
        if candidate.is_dir() and _is_valid_workspace_root(candidate):
            return candidate

    # Relative to: 00_CORE_SYSTEM/config/path_config.py -> parents[2] is workspace root
    candidate = Path(__file__).resolve().parents[2]
    if candidate.is_dir() and _is_valid_workspace_root(candidate):
        return candidate

    # Fallback to traversing upwards from current working directory
    cwd = Path.cwd().resolve()
    curr = cwd
    for _ in range(5):
        if _is_valid_workspace_root(curr):
            return curr
        if curr.parent == curr:
            break
        curr = curr.parent

    # Default to candidate if validation fails, but warn
    return candidate


def _is_valid_workspace_root(path: Path) -> bool:
    """Check if the given directory contains required Master AI components."""
    if not path.is_dir():
        return False
    # At least 4 of the key directories must exist
    matches = sum(1 for d in EXPECTED_CORE_DIRECTORIES if (path / d).is_dir())
    return matches >= 4


# Canonical workspace root
WORKSPACE_ROOT: Path = _detect_workspace_root()


def get_workspace_root() -> Path:
    """Return the resolved workspace root as a Path object."""
    return WORKSPACE_ROOT


def resolve_path(*subpaths: str) -> Path:
    """Resolve a path relative to the workspace root."""
    return WORKSPACE_ROOT.joinpath(*subpaths)


def validate_workspace(root: Path | None = None) -> bool:
    """Validate that the workspace root contains the complete project architecture."""
    target = root or WORKSPACE_ROOT
    return _is_valid_workspace_root(target)


def ensure_directory(path: Path) -> Path:
    """Create directory if it does not exist and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


# --- Centralized Subdirectory Definitions ---
CORE_SYSTEM_DIR: Path = WORKSPACE_ROOT / "00_CORE_SYSTEM"
GLOBAL_RULES_DIR: Path = WORKSPACE_ROOT / "01_GLOBAL_RULES"
SKILLS_DIR: Path = WORKSPACE_ROOT / "02_SKILLS"
AGENTS_DIR: Path = WORKSPACE_ROOT / "03_AI_AGENTS"
LLM_DIR: Path = WORKSPACE_ROOT / "04_LLM_AND_AI"
DEVELOPMENT_DIR: Path = WORKSPACE_ROOT / "05_DEVELOPMENT"
UI_UX_DIR: Path = WORKSPACE_ROOT / "06_UI_UX_DESIGN"
MCP_AND_TOOLS_DIR: Path = WORKSPACE_ROOT / "07_MCP_AND_TOOLS"
AUTOMATION_DIR: Path = WORKSPACE_ROOT / "08_AUTOMATION"
CONTENT_STUDIO_DIR: Path = WORKSPACE_ROOT / "09_CONTENT_STUDIO"
SOCIAL_MEDIA_DIR: Path = WORKSPACE_ROOT / "10_SOCIAL_MEDIA"
RESEARCH_LAB_DIR: Path = WORKSPACE_ROOT / "11_RESEARCH_LAB"
DOCUMENTS_DIR: Path = WORKSPACE_ROOT / "12_DOCUMENTS"
MARKDOWN_DIR: Path = WORKSPACE_ROOT / "13_MARKDOWN"
CODE_LIBRARY_DIR: Path = WORKSPACE_ROOT / "14_CODE_LIBRARY"
ASSETS_DIR: Path = WORKSPACE_ROOT / "15_ASSETS"
VIDEO_DIR: Path = WORKSPACE_ROOT / "16_VIDEO_LIBRARY"
TEMPLATES_DIR: Path = WORKSPACE_ROOT / "17_TEMPLATES"
TESTING_DIR: Path = WORKSPACE_ROOT / "18_TESTING_AND_QA"
SECURITY_DIR: Path = WORKSPACE_ROOT / "19_SECURITY_AND_COMPLIANCE"
PROJECTS_DIR: Path = WORKSPACE_ROOT / "20_PROJECTS"
LEARNING_LAB_DIR: Path = WORKSPACE_ROOT / "21_LEARNING_LAB"
DEPLOY_DIR: Path = WORKSPACE_ROOT / "22_PUBLISH_AND_DEPLOY"
BACKUP_DIR: Path = WORKSPACE_ROOT / "23_CHANGELOG_AND_BACKUP"

# Specialized Operational Directories
VENV_DIR: Path = WORKSPACE_ROOT / ".venv"
REGISTRY_DIR: Path = CORE_SYSTEM_DIR / "registry"
DASHBOARD_DIR: Path = CORE_SYSTEM_DIR / "dashboard"
SNAPSHOTS_DIR: Path = BACKUP_DIR / "snapshots"
ROLLBACK_LOG_DIR: Path = BACKUP_DIR / "history"
QDRANT_DIR: Path = LLM_DIR / "rag_systems" / "qdrant_db"


if __name__ == "__main__":
    print(f"Workspace Root: {WORKSPACE_ROOT}")
    print(f"Valid Master AI Root: {validate_workspace()}")
    print(f"Skills Dir: {SKILLS_DIR} (exists: {SKILLS_DIR.is_dir()})")
    print(f"Agents Dir: {AGENTS_DIR} (exists: {AGENTS_DIR.is_dir()})")
    print(f"Testing Dir: {TESTING_DIR} (exists: {TESTING_DIR.is_dir()})")
