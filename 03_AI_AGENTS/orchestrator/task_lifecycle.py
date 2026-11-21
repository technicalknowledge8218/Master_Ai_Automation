"""task_lifecycle.py
MASTER-AI Persistent Task Lifecycle & Checkpoint Manager

Enforces deterministic 13-state workflow lifecycle:
CREATED -> PLANNED -> APPROVED -> QUEUED -> RUNNING -> VALIDATING -> COMPLETED
with edge states: FAILED, BLOCKED, WAITING_FOR_APPROVAL, PAUSED, CANCELLED, RETRYING.

Provides atomic JSON persistence, restart recovery, and subtask checkpointing.
"""

import os
import sys
import json
import time
import uuid
import datetime
from typing import Dict, Any, List, Optional, Set, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORKFLOWS_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "workflows")
INDEX_PATH = os.path.join(WORKFLOWS_DIR, "WORKFLOW_INDEX.json")


VALID_LIFECYCLE_STATES = {
    "CREATED",
    "PLANNED",
    "APPROVED",
    "QUEUED",
    "RUNNING",
    "VALIDATING",
    "COMPLETED",
    "FAILED",
    "BLOCKED",
    "WAITING_FOR_APPROVAL",
    "PAUSED",
    "CANCELLED",
    "RETRYING"
}

ALLOWED_TRANSITIONS = {
    "CREATED": {"PLANNED", "CANCELLED"},
    "PLANNED": {"APPROVED", "WAITING_FOR_APPROVAL", "CANCELLED"},
    "WAITING_FOR_APPROVAL": {"APPROVED", "BLOCKED", "CANCELLED"},
    "APPROVED": {"QUEUED", "CANCELLED"},
    "QUEUED": {"RUNNING", "PAUSED", "CANCELLED"},
    "RUNNING": {"VALIDATING", "RETRYING", "FAILED", "PAUSED", "CANCELLED", "BLOCKED"},
    "VALIDATING": {"COMPLETED", "RETRYING", "FAILED"},
    "RETRYING": {"RUNNING", "FAILED", "CANCELLED"},
    "PAUSED": {"QUEUED", "RUNNING", "CANCELLED"},
    "BLOCKED": {"QUEUED", "CANCELLED", "FAILED"},
    "COMPLETED": set(),
    "FAILED": set(),
    "CANCELLED": set()
}


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class TaskLifecycleManager:
    """Manages workflow persistence, state transitions, and restart checkpoints."""

    def __init__(self, workflows_dir: Optional[str] = None):
        self.workflows_dir = workflows_dir or WORKFLOWS_DIR
        self.index_path = os.path.join(self.workflows_dir, "WORKFLOW_INDEX.json")
        os.makedirs(self.workflows_dir, exist_ok=True)
        self._ensure_index()

    def _ensure_index(self):
        if not os.path.exists(self.index_path):
            self._write_json(self.index_path, {"workflows": {}})

    def _write_json(self, path: str, data: Dict[str, Any]):
        """Atomic write using temporary file and replacement."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        tmp = path + f".{uuid.uuid4().hex[:6]}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)

    def _read_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_workflow(self, plan: Dict[str, Any]) -> str:
        """Initializes and persists a new workflow instance from an execution plan."""
        wf_id = f"WF-{uuid.uuid4().hex[:8]}"
        now = datetime.datetime.now().isoformat()

        # Build subtask status map
        subtasks_state = {}
        for st in plan.get("subtasks", []):
            st_id = st["subtask_id"]
            subtasks_state[st_id] = {
                "subtask_id": st_id,
                "title": st.get("title", ""),
                "description": st.get("description", ""),
                "assigned_agent": st.get("assigned_agent", "AGT-001"),
                "priority": st.get("priority", "MEDIUM"),
                "status": "QUEUED",
                "depends_on": st.get("depends_on", []),
                "inputs": st.get("inputs", {}),
                "expected_outputs": st.get("expected_outputs", []),
                "outputs": {},
                "artifacts": [],
                "error": None,
                "retry_count": 0,
                "max_retries": st.get("retry_budget", 2),
                "started_at": None,
                "completed_at": None,
                "duration_seconds": 0.0
            }

        initial_status = "WAITING_FOR_APPROVAL" if plan.get("requires_human_approval") else "PLANNED"

        workflow_data = {
            "workflow_id": wf_id,
            "plan_id": plan.get("plan_id", "UNKNOWN"),
            "goal": plan.get("goal", ""),
            "complexity": plan.get("complexity", "MODERATE_SEQUENTIAL"),
            "status": initial_status,
            "created_at": now,
            "started_at": None,
            "completed_at": None,
            "current_wave_index": 0,
            "waves": plan.get("waves", []),
            "subtasks": subtasks_state,
            "artifacts": [],
            "checkpoint_history": [
                {"timestamp": now, "status": initial_status, "tag": "WORKFLOW_INITIALIZED"}
            ],
            "final_deliverable": None
        }

        wf_path = os.path.join(self.workflows_dir, f"{wf_id}.json")
        self._write_json(wf_path, workflow_data)

        # Update index
        index_data = self._read_json(self.index_path)
        index_data.setdefault("workflows", {})[wf_id] = {
            "workflow_id": wf_id,
            "goal": plan.get("goal", "")[:80],
            "status": initial_status,
            "created_at": now,
            "subtask_count": len(subtasks_state),
            "completed_count": 0
        }
        self._write_json(self.index_path, index_data)

        return wf_id

    def load_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Loads a workflow from disk."""
        path = os.path.join(self.workflows_dir, f"{workflow_id}.json")
        if not os.path.exists(path):
            return None
        return self._read_json(path)

    def transition_workflow_status(
        self,
        workflow_id: str,
        new_status: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transitions workflow status with validation and checkpoint recording."""
        if new_status not in VALID_LIFECYCLE_STATES:
            raise ValueError(f"Invalid lifecycle state: '{new_status}'")

        wf = self.load_workflow(workflow_id)
        if not wf:
            raise KeyError(f"Workflow '{workflow_id}' not found.")

        current_status = wf.get("status", "CREATED")
        allowed = ALLOWED_TRANSITIONS.get(current_status, set())
        if new_status not in allowed and current_status != new_status:
            raise InvalidStateTransitionError(
                f"Cannot transition workflow '{workflow_id}' from '{current_status}' to '{new_status}'."
            )

        now = datetime.datetime.now().isoformat()
        wf["status"] = new_status
        if new_status == "RUNNING" and not wf.get("started_at"):
            wf["started_at"] = now
        elif new_status in {"COMPLETED", "FAILED", "CANCELLED"}:
            wf["completed_at"] = now

        wf.setdefault("checkpoint_history", []).append({
            "timestamp": now,
            "status": new_status,
            "tag": reason or f"TRANSITION_TO_{new_status}"
        })

        wf_path = os.path.join(self.workflows_dir, f"{workflow_id}.json")
        self._write_json(wf_path, wf)

        # Update index
        index_data = self._read_json(self.index_path)
        if workflow_id in index_data.get("workflows", {}):
            index_data["workflows"][workflow_id]["status"] = new_status
            completed = sum(1 for st in wf.get("subtasks", {}).values() if st.get("status") == "COMPLETED")
            index_data["workflows"][workflow_id]["completed_count"] = completed
            self._write_json(self.index_path, index_data)

        return wf

    def update_subtask_status(
        self,
        workflow_id: str,
        subtask_id: str,
        status: str,
        outputs: Optional[Dict[str, Any]] = None,
        artifacts: Optional[List[str]] = None,
        error: Optional[str] = None,
        duration_seconds: float = 0.0
    ) -> Dict[str, Any]:
        """Updates an individual subtask's execution state and saves a checkpoint."""
        wf = self.load_workflow(workflow_id)
        if not wf:
            raise KeyError(f"Workflow '{workflow_id}' not found.")

        if subtask_id not in wf.get("subtasks", {}):
            raise KeyError(f"Subtask '{subtask_id}' not found in workflow '{workflow_id}'.")

        now = datetime.datetime.now().isoformat()
        st = wf["subtasks"][subtask_id]
        st["status"] = status
        if status == "RUNNING" and not st.get("started_at"):
            st["started_at"] = now
        elif status in {"COMPLETED", "FAILED"}:
            st["completed_at"] = now
            st["duration_seconds"] = round(duration_seconds, 3)

        if outputs is not None:
            st["outputs"] = outputs
        if artifacts is not None:
            st["artifacts"] = artifacts
            wf.setdefault("artifacts", []).extend(artifacts)
        if error is not None:
            st["error"] = error
        if status == "RETRYING":
            st["retry_count"] = st.get("retry_count", 0) + 1

        wf_path = os.path.join(self.workflows_dir, f"{workflow_id}.json")
        self._write_json(wf_path, wf)

        # Update index
        index_data = self._read_json(self.index_path)
        if workflow_id in index_data.get("workflows", {}):
            completed = sum(1 for s in wf["subtasks"].values() if s.get("status") == "COMPLETED")
            index_data["workflows"][workflow_id]["completed_count"] = completed
            self._write_json(self.index_path, index_data)

        return wf

    def list_workflows(self) -> List[Dict[str, Any]]:
        """Returns indexed overview of all persisted workflows."""
        index_data = self._read_json(self.index_path)
        return list(index_data.get("workflows", {}).values())

    def recover_incomplete_workflows(self) -> List[Dict[str, Any]]:
        """Finds all workflows interrupted mid-execution (RUNNING, QUEUED, PAUSED, RETRYING)."""
        incomplete = []
        for summary in self.list_workflows():
            if summary.get("status") in {"RUNNING", "QUEUED", "PAUSED", "RETRYING"}:
                wf = self.load_workflow(summary["workflow_id"])
                if wf:
                    incomplete.append(wf)
        return incomplete
