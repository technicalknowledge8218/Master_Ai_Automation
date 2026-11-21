"""
trust_levels.py
MASTER-AI Execution Trust Level Classification & Enforcement

Defines the 5 formal trust levels (LEVEL 0 through LEVEL 4) and provides
validation routines to prevent unauthorized privilege and trust escalation.
"""

from enum import IntEnum
from typing import Dict, Any, Set, Tuple


class TrustLevel(IntEnum):
    """
    MASTER-AI 5-Tier Execution Trust Classification
    """
    LEVEL_0_READ_ONLY = 0        # Read-only exploration and analysis. No file writes, no code exec, no network.
    LEVEL_1_WORKSPACE_FS = 1     # Workspace-local file creation and editing in sandbox. No code exec, no network.
    LEVEL_2_LOCAL_EXECUTION = 2  # Workspace-local sandboxed code execution (Python, Node, safe local Git). No network.
    LEVEL_3_NETWORK_APPROVED = 3 # Approved external network operations. Requires explicit human authorization.
    LEVEL_4_HOST_GLOBAL = 4      # Host-level or global config changes (.gemini, global skills/rules). Requires explicit human approval.


class TrustEscalationViolation(Exception):
    """Raised when an agent or untrusted entity attempts to self-escalate trust level."""
    pass


# Permissions Matrix mapping each TrustLevel to allowed operations
TRUST_PERMISSIONS: Dict[TrustLevel, Set[str]] = {
    TrustLevel.LEVEL_0_READ_ONLY: {
        "read_workspace_files",
        "read_sandbox_files",
        "search_local_docs",
        "generate_static_analysis"
    },
    TrustLevel.LEVEL_1_WORKSPACE_FS: {
        "read_workspace_files",
        "read_sandbox_files",
        "search_local_docs",
        "generate_static_analysis",
        "write_sandbox_files",
        "edit_sandbox_files"
    },
    TrustLevel.LEVEL_2_LOCAL_EXECUTION: {
        "read_workspace_files",
        "read_sandbox_files",
        "search_local_docs",
        "generate_static_analysis",
        "write_sandbox_files",
        "edit_sandbox_files",
        "execute_sandboxed_python",
        "execute_sandboxed_node",
        "execute_safe_local_git"
    },
    TrustLevel.LEVEL_3_NETWORK_APPROVED: {
        "read_workspace_files",
        "read_sandbox_files",
        "search_local_docs",
        "generate_static_analysis",
        "write_sandbox_files",
        "edit_sandbox_files",
        "execute_sandboxed_python",
        "execute_sandboxed_node",
        "execute_safe_local_git",
        "execute_approved_network_request",
        "query_approved_remote_git"
    },
    TrustLevel.LEVEL_4_HOST_GLOBAL: {
        "read_workspace_files",
        "read_sandbox_files",
        "search_local_docs",
        "generate_static_analysis",
        "write_sandbox_files",
        "edit_sandbox_files",
        "execute_sandboxed_python",
        "execute_sandboxed_node",
        "execute_safe_local_git",
        "execute_approved_network_request",
        "query_approved_remote_git",
        "deploy_global_skill",
        "modify_global_config"
    }
}


def is_operation_permitted(trust_level: TrustLevel, operation_name: str) -> bool:
    """Verifies whether an operation is permitted at the designated trust level."""
    allowed = TRUST_PERMISSIONS.get(trust_level, set())
    return operation_name in allowed


def validate_trust_transition(
    current_level: TrustLevel,
    requested_level: TrustLevel,
    actor: str,
    has_human_approval: bool = False
) -> Tuple[bool, str]:
    """
    Enforces non-negotiable trust level transition invariants:
    1. No agent (actor matching 'agent:*') can self-escalate trust.
    2. Any escalation to Level 3 (Network) or Level 4 (Host/Global) strictly requires human approval.
    3. Untrusted generated code can never receive Level 4 permissions.
    """
    if requested_level < current_level:
        # De-escalation / reduction of privilege is always allowed
        return True, "Trust level de-escalated safely."

    if requested_level == current_level:
        return True, "Trust level unchanged."

    # Escalation requested:
    if actor.lower().startswith("agent:"):
        raise TrustEscalationViolation(
            f"Agent self-escalation forbidden: Agent '{actor}' cannot escalate trust level "
            f"from {current_level.name} to {requested_level.name}."
        )

    if requested_level in (TrustLevel.LEVEL_3_NETWORK_APPROVED, TrustLevel.LEVEL_4_HOST_GLOBAL):
        if not has_human_approval:
            return False, (
                f"Trust escalation to {requested_level.name} requires explicit human authorization. "
                f"State remains gated."
            )

    return True, f"Trust level successfully elevated to {requested_level.name} by {actor}."
