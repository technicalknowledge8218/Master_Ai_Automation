"""Master AI Configuration Package."""

from .path_config import (
    WORKSPACE_ROOT,
    get_workspace_root,
    resolve_path,
    validate_workspace,
    CORE_SYSTEM_DIR,
    SKILLS_DIR,
    AGENTS_DIR,
    LLM_DIR,
    TESTING_DIR,
    VIDEO_DIR,
    BACKUP_DIR,
    REGISTRY_DIR,
    SNAPSHOTS_DIR,
    QDRANT_DIR,
)

__all__ = [
    "WORKSPACE_ROOT",
    "get_workspace_root",
    "resolve_path",
    "validate_workspace",
    "CORE_SYSTEM_DIR",
    "SKILLS_DIR",
    "AGENTS_DIR",
    "LLM_DIR",
    "TESTING_DIR",
    "VIDEO_DIR",
    "BACKUP_DIR",
    "REGISTRY_DIR",
    "SNAPSHOTS_DIR",
    "QDRANT_DIR",
]
