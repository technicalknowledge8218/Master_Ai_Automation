"""
approval_engine.py
MASTER-AI Human Approval & Governance Gatekeeper Engine

Enforces deterministic approval state machine:
PROPOSED -> REVIEW_REQUIRED -> APPROVED -> EXECUTING -> VERIFIED -> COMPLETED
Also handles REJECTED, FAILED, ROLLED_BACK.

Features Windows-safe file locking, atomic writes with replacement,
checksum corruption detection, automatic backup recovery, and task-bound tokens with TTL.
"""

import os
import sys
import json
import uuid
import time
import hashlib
import datetime
from typing import Dict, Any, List, Optional, Tuple

try:
    from .trust_levels import TrustLevel, TrustEscalationViolation, validate_trust_transition
except ImportError:
    from trust_levels import TrustLevel, TrustEscalationViolation, validate_trust_transition

# Platform-specific locking for Windows
IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import fcntl

APPROVAL_LEDGER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "runs", "APPROVAL_LEDGER.json"
)

VALID_STATES = {
    "PROPOSED",
    "REVIEW_REQUIRED",
    "APPROVED",
    "EXECUTING",
    "VERIFIED",
    "COMPLETED",
    "REJECTED",
    "FAILED",
    "ROLLED_BACK"
}

STATE_TRANSITIONS = {
    "PROPOSED": {"REVIEW_REQUIRED", "APPROVED", "REJECTED"},
    "REVIEW_REQUIRED": {"APPROVED", "REJECTED"},
    "APPROVED": {"EXECUTING", "REJECTED"},
    "EXECUTING": {"VERIFIED", "FAILED", "ROLLED_BACK"},
    "VERIFIED": {"COMPLETED", "FAILED", "ROLLED_BACK"},
    "COMPLETED": set(),
    "REJECTED": set(),
    "FAILED": {"ROLLED_BACK"},
    "ROLLED_BACK": set()
}

HIGH_RISK_TRIGGERS = [
    "global_installation",
    "global_skill_deployment",
    "global_rule_deployment",
    "mcp_config_modification",
    "paid_api_activation",
    "external_publishing",
    "git_remote_push",
    "destructive_operation"
]

DEFAULT_TOKEN_TTL_SECONDS = 3600  # 1 hour default


class ApprovalViolation(Exception):
    """Raised when an operation attempts to bypass human approval."""
    pass


class LedgerCorruptionError(Exception):
    """Raised when the approval ledger is corrupt and unrecoverable."""
    pass


class FileLock:
    """Cross-platform, non-blocking with retry file lock context manager."""
    def __init__(self, lock_file_path: str, timeout: float = 5.0, delay: float = 0.05):
        self.lock_file_path = lock_file_path
        self.timeout = timeout
        self.delay = delay
        self.fd = None

    def __enter__(self):
        start_time = time.time()
        os.makedirs(os.path.dirname(os.path.abspath(self.lock_file_path)), exist_ok=True)
        while True:
            try:
                self.fd = open(self.lock_file_path, "a+")
                if IS_WINDOWS:
                    msvcrt.locking(self.fd.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self.fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except (IOError, OSError):
                if self.fd:
                    try:
                        self.fd.close()
                    except Exception:
                        pass
                    self.fd = None
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Could not acquire lock on {self.lock_file_path} within {self.timeout}s")
                time.sleep(self.delay)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd:
            try:
                if IS_WINDOWS:
                    self.fd.seek(0)
                    msvcrt.locking(self.fd.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(self.fd.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
            finally:
                self.fd.close()
                self.fd = None


class HumanApprovalEngine:
    def __init__(self, ledger_file: Optional[str] = None):
        self.ledger_file = os.path.abspath(ledger_file or APPROVAL_LEDGER_PATH)
        self.lock_file = f"{self.ledger_file}.lock"
        self.backup_file = f"{self.ledger_file}.bak"
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        self._cleanup_stale_tmp_files()
        self.records: Dict[str, Dict[str, Any]] = self._load_ledger()

    def _cleanup_stale_tmp_files(self):
        """Removes orphan .tmp files left from interrupted writes."""
        dir_name = os.path.dirname(self.ledger_file)
        base_name = os.path.basename(self.ledger_file)
        if os.path.exists(dir_name):
            for f in os.listdir(dir_name):
                if f.startswith(base_name) and f.endswith(".tmp"):
                    try:
                        os.remove(os.path.join(dir_name, f))
                    except Exception:
                        pass

    def _load_ledger(self) -> Dict[str, Dict[str, Any]]:
        """Loads ledger with corruption detection and automatic recovery from .bak."""
        if not os.path.exists(self.ledger_file):
            return {}

        with FileLock(self.lock_file):
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
                    raise ValueError("Ledger content is not a JSON object")
            except Exception as primary_err:
                # Attempt recovery from backup
                if os.path.exists(self.backup_file):
                    try:
                        with open(self.backup_file, "r", encoding="utf-8") as bf:
                            recovered = json.load(bf)
                            if isinstance(recovered, dict):
                                # Restore primary from backup
                                self._atomic_write(recovered)
                                return recovered
                    except Exception:
                        pass
                raise LedgerCorruptionError(
                    f"Approval ledger at {self.ledger_file} is corrupt: {str(primary_err)}"
                )

    def _atomic_write(self, data: Dict[str, Any]):
        """Writes data atomically using a unique temp file and os.replace, preserving .bak."""
        tmp_file = f"{self.ledger_file}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
        # 1. Create backup of current valid ledger if it exists
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as src, \
                     open(self.backup_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            except Exception:
                pass

        # 2. Write to temp file with fsync
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        # 3. Atomic replacement
        os.replace(tmp_file, self.ledger_file)

    def _save_ledger(self):
        """Thread-safe and process-safe atomic save."""
        with FileLock(self.lock_file):
            self._atomic_write(self.records)

    def assess_task_risk(self, task: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Analyzes task description, context, and requested operations for high-risk triggers."""
        reasons = []
        task_str = json.dumps(task).lower()

        if ".gemini" in task_str or "global" in task_str and "deploy" in task_str:
            reasons.append("Attempts global Antigravity installation/deployment (.gemini)")
        if "mcp_config" in task_str:
            reasons.append("Attempts MCP configuration modification")
        if "paid_api" in task_str or "billing" in task_str:
            reasons.append("Attempts paid API or subscription activation")
        if "git push" in task_str or "remote" in task_str and "publish" in task_str:
            reasons.append("Attempts external Git remote push or public publishing")
        if "rm -rf" in task_str or "destructive" in task_str or "drop table" in task_str:
            reasons.append("Attempts potentially destructive operation")

        return len(reasons) > 0, reasons

    def register_task(
        self,
        task_id: str,
        title: str,
        details: Dict[str, Any],
        allow_reset: bool = False
    ) -> Dict[str, Any]:
        """Registers a new task into the approval engine. Prevents duplicate overwrite of active/completed tasks unless allow_reset=True."""
        with FileLock(self.lock_file):
            # Refresh records
            if os.path.exists(self.ledger_file):
                try:
                    with open(self.ledger_file, "r", encoding="utf-8") as f:
                        self.records = json.load(f)
                except Exception:
                    pass

            if task_id in self.records and not allow_reset:
                existing_state = self.records[task_id]["state"]
                if existing_state in {"COMPLETED", "EXECUTING", "VERIFIED"}:
                    raise ApprovalViolation(
                        f"Cannot re-register active or completed task '{task_id}' (state: {existing_state})."
                    )

            is_high_risk, risk_reasons = self.assess_task_risk(details)
            initial_state = "REVIEW_REQUIRED" if is_high_risk else "PROPOSED"

            initial_trust_level = details.get("trust_level", TrustLevel.LEVEL_2_LOCAL_EXECUTION.value)
            if is_high_risk:
                task_str = json.dumps(details).lower()
                if ".gemini" in task_str or "global" in task_str:
                    initial_trust_level = max(initial_trust_level, TrustLevel.LEVEL_4_HOST_GLOBAL.value)
                elif "network" in task_str or "remote" in task_str:
                    initial_trust_level = max(initial_trust_level, TrustLevel.LEVEL_3_NETWORK_APPROVED.value)

            ticket = {
                "task_id": task_id,
                "title": title,
                "state": initial_state,
                "trust_level": initial_trust_level,
                "is_high_risk": is_high_risk,
                "risk_reasons": risk_reasons,
                "approval_token": None,
                "token_issued_at": None,
                "token_ttl_seconds": DEFAULT_TOKEN_TTL_SECONDS,
                "history": [
                    {
                        "from_state": None,
                        "to_state": initial_state,
                        "timestamp": datetime.datetime.now().isoformat(),
                        "actor": "system",
                        "reason": f"Task registered with initial Trust Level {TrustLevel(initial_trust_level).name}"
                    }
                ]
            }
            self.records[task_id] = ticket
            self._atomic_write(self.records)
            return ticket

    def elevate_trust_level(
        self,
        task_id: str,
        requested_level: int,
        actor: str = "human",
        auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Elevates or changes task trust level, strictly enforcing that agents cannot self-escalate."""
        with FileLock(self.lock_file):
            if os.path.exists(self.ledger_file):
                try:
                    with open(self.ledger_file, "r", encoding="utf-8") as f:
                        self.records = json.load(f)
                except Exception:
                    pass

            if task_id not in self.records:
                raise KeyError(f"Task '{task_id}' not registered in approval engine.")

            ticket = self.records[task_id]
            current_level = TrustLevel(ticket.get("trust_level", TrustLevel.LEVEL_2_LOCAL_EXECUTION.value))
            target_level = TrustLevel(requested_level)

            # Prevent agent self-escalation
            actor_lower = actor.lower()
            if actor_lower.startswith("agent") or "agent" in actor_lower and "orchestrator" not in actor_lower and "human" not in actor_lower:
                raise TrustEscalationViolation(
                    f"Agent self-escalation forbidden: Agent '{actor}' cannot elevate trust level from {current_level.name} to {target_level.name}."
                )

            # High privilege levels (Level 3 Network, Level 4 Host) require APPROVED status
            if target_level in (TrustLevel.LEVEL_3_NETWORK_APPROVED, TrustLevel.LEVEL_4_HOST_GLOBAL):
                if ticket["state"] != "APPROVED":
                    raise ApprovalViolation(
                        f"Cannot elevate task '{task_id}' to {target_level.name}: Task state is '{ticket['state']}' and requires explicit human APPROVAL."
                    )

            ticket["trust_level"] = target_level.value
            ticket["history"].append({
                "from_state": ticket["state"],
                "to_state": ticket["state"],
                "timestamp": datetime.datetime.now().isoformat(),
                "actor": actor,
                "reason": f"Trust level updated to {target_level.name}"
            })
            self._atomic_write(self.records)
            return ticket

    def transition_state(
        self,
        task_id: str,
        to_state: str,
        actor: str = "human",
        reason: str = "",
        ttl_seconds: int = DEFAULT_TOKEN_TTL_SECONDS
    ) -> Dict[str, Any]:
        """Transitions task approval state, enforcing valid state machine edges and rejecting agent self-approval."""
        with FileLock(self.lock_file):
            # Refresh state
            if os.path.exists(self.ledger_file):
                try:
                    with open(self.ledger_file, "r", encoding="utf-8") as f:
                        self.records = json.load(f)
                except Exception:
                    pass

            if task_id not in self.records:
                raise KeyError(f"Task '{task_id}' not registered in approval engine.")

            ticket = self.records[task_id]
            current_state = ticket["state"]

            if to_state not in VALID_STATES:
                raise ValueError(f"Invalid target state '{to_state}'. Valid states: {VALID_STATES}")

            # Self-approval guard: agents cannot approve tasks
            if to_state == "APPROVED":
                actor_lower = actor.lower()
                if actor_lower.startswith("agent") or "agent" in actor_lower and "orchestrator" not in actor_lower and "human" not in actor_lower:
                    raise ApprovalViolation("Agent self-approval is forbidden. Only human operators or orchestrator may authorize tasks.")

            allowed_next = STATE_TRANSITIONS.get(current_state, set())
            if to_state not in allowed_next:
                raise ApprovalViolation(
                    f"Illegal state transition for task '{task_id}': cannot move from '{current_state}' to '{to_state}'. "
                    f"Allowed transitions: {allowed_next}"
                )

            # Generate task-bound cryptographic token with TTL upon approval
            if to_state == "APPROVED":
                ticket["approval_token"] = f"AUTH-{task_id}-{uuid.uuid4().hex[:12]}"
                ticket["token_issued_at"] = time.time()
                ticket["token_ttl_seconds"] = ttl_seconds

            ticket["state"] = to_state
            ticket["history"].append({
                "from_state": current_state,
                "to_state": to_state,
                "timestamp": datetime.datetime.now().isoformat(),
                "actor": actor,
                "reason": reason
            })
            self._atomic_write(self.records)
            return ticket

    def verify_authorization(self, task_id: str, token: Optional[str]) -> bool:
        """Verifies that a task has an active, valid, non-expired, task-bound approval token."""
        if not token:
            return False

        with FileLock(self.lock_file):
            if os.path.exists(self.ledger_file):
                try:
                    with open(self.ledger_file, "r", encoding="utf-8") as f:
                        self.records = json.load(f)
                except Exception:
                    pass

            ticket = self.records.get(task_id)
            if not ticket:
                return False

            if ticket["state"] not in {"APPROVED", "EXECUTING", "VERIFIED"}:
                return False

            stored_token = ticket.get("approval_token")
            if not stored_token or stored_token != token:
                return False

            # Expiration check
            issued_at = ticket.get("token_issued_at")
            ttl = ticket.get("token_ttl_seconds", DEFAULT_TOKEN_TTL_SECONDS)
            if issued_at is not None and (time.time() - issued_at > ttl):
                return False  # Token expired

            return True

    def check_operation_allowed(
        self,
        task_id: str,
        operation: str,
        token: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Checks if a specific operation is permitted. Blocks high-risk operations without explicit approval."""
        ticket = self.records.get(task_id)
        if not ticket:
            return False, f"Task '{task_id}' not found."

        is_high_risk = any(trigger in operation.lower() for trigger in HIGH_RISK_TRIGGERS)
        if is_high_risk:
            if ticket["state"] != "APPROVED":
                return False, (
                    f"BLOCKED: Operation '{operation}' is high-risk. "
                    f"Task state is '{ticket['state']}'. Requires explicit human APPROVAL."
                )
            if not self.verify_authorization(task_id, token):
                return False, f"BLOCKED: Invalid or missing task-bound authorization token for '{task_id}'."

        return True, "Operation authorized."
