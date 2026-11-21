"""execution_tracer.py
MASTER-AI Live Execution Tracer & Observability Subsystem

Captures timeline events, agent assignments, subtask transitions, tool invocations,
model selections, approval checks, retries, and errors, with automatic secret scrubbing.
"""

import os
import sys
import json
import re
import time
import uuid
import datetime
from typing import Dict, Any, List, Optional, Set

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRACES_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "traces")

# Secret scrubbing regex patterns
_KV_SECRET_PATTERN = re.compile(r"(?i)((?:api[_-]?key|secret|token|password|bearer|auth[_-]?token)\s*[:=]\s*['\"]?)[a-zA-Z0-9_\-\.]{8,}['\"]?")
_STANDALONE_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{36,}"),
    re.compile(r"AIza[0-9A-Za-z-_]{35}")
]


def scrub_secrets(obj: Any) -> Any:
    """Recursively redacts API keys, passwords, and tokens from dictionaries, lists, and strings."""
    if isinstance(obj, str):
        cleaned = _KV_SECRET_PATTERN.sub(r"\1[REDACTED_SECRET]", obj)
        for pat in _STANDALONE_PATTERNS:
            cleaned = pat.sub("[REDACTED_SECRET]", cleaned)
        return cleaned
    elif isinstance(obj, dict):
        cleaned_dict = {}
        for k, v in obj.items():
            if any(s in k.lower() for s in ["key", "token", "secret", "password", "auth", "credential"]):
                cleaned_dict[k] = "[REDACTED_SECRET]"
            else:
                cleaned_dict[k] = scrub_secrets(v)
        return cleaned_dict
    elif isinstance(obj, list):
        return [scrub_secrets(item) for item in obj]
    return obj


class ExecutionTracer:
    """Observability tracer tracking live workflow execution timeline."""

    def __init__(self, workflow_id: str, traces_dir: Optional[str] = None):
        self.workflow_id = workflow_id
        self.traces_dir = traces_dir or TRACES_DIR
        self.trace_file = os.path.join(self.traces_dir, f"TRACE_{workflow_id}.json")
        os.makedirs(self.traces_dir, exist_ok=True)

        self._start_time = time.time()
        self._trace_data: Dict[str, Any] = {
            "workflow_id": workflow_id,
            "goal": "",
            "started_at": datetime.datetime.now().isoformat(),
            "completed_at": None,
            "duration_seconds": 0.0,
            "estimated_cost_usd": 0.00,  # Sovereign local execution
            "active_subtask": None,
            "timeline": [],
            "metrics": {
                "total_events": 0,
                "tool_calls": 0,
                "model_calls": 0,
                "retries": 0,
                "errors": 0,
                "approvals_requested": 0
            }
        }
        self._save_trace()

    def set_goal(self, goal: str):
        """Sets the user goal being executed."""
        self._trace_data["goal"] = scrub_secrets(goal)
        self._save_trace()

    def record_event(
        self,
        event_type: str,
        message: str,
        agent_id: Optional[str] = None,
        subtask_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Appends an event to the trace timeline with secret scrubbing."""
        now = datetime.datetime.now().isoformat()
        elapsed = round(time.time() - self._start_time, 3)

        event = {
            "event_id": f"EVT-{uuid.uuid4().hex[:6]}",
            "timestamp": now,
            "elapsed_seconds": elapsed,
            "event_type": event_type,
            "message": scrub_secrets(message),
            "agent_id": agent_id,
            "subtask_id": subtask_id,
            "details": scrub_secrets(details or {})
        }

        self._trace_data["timeline"].append(event)
        self._trace_data["metrics"]["total_events"] += 1

        if subtask_id:
            self._trace_data["active_subtask"] = subtask_id

        # Update specific metrics
        if "TOOL" in event_type.upper():
            self._trace_data["metrics"]["tool_calls"] += 1
        elif "MODEL" in event_type.upper():
            self._trace_data["metrics"]["model_calls"] += 1
        elif "RETRY" in event_type.upper():
            self._trace_data["metrics"]["retries"] += 1
        elif "ERROR" in event_type.upper() or "FAIL" in event_type.upper():
            self._trace_data["metrics"]["errors"] += 1
        elif "APPROVAL" in event_type.upper():
            self._trace_data["metrics"]["approvals_requested"] += 1

        self._trace_data["duration_seconds"] = elapsed
        self._save_trace()
        return event

    def complete_trace(self, status: str = "COMPLETED"):
        """Marks the execution trace as completed."""
        self._trace_data["completed_at"] = datetime.datetime.now().isoformat()
        self._trace_data["duration_seconds"] = round(time.time() - self._start_time, 3)
        self._trace_data["status"] = status
        self.record_event(
            event_type=f"WORKFLOW_{status.upper()}",
            message=f"Workflow trace marked as {status}."
        )
        self._save_trace()

    def get_trace(self) -> Dict[str, Any]:
        """Returns the scrubbed trace."""
        return dict(self._trace_data)

    def _save_trace(self):
        """Atomic persistence of trace data."""
        try:
            tmp = self.trace_file + f".{uuid.uuid4().hex[:6]}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._trace_data, f, indent=2)
            os.replace(tmp, self.trace_file)
        except Exception:
            pass
