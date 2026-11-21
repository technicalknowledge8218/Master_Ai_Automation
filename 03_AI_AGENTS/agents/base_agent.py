"""
base_agent.py
MASTER-AI Base Specialist Agent Runtime

Abstract execution base class for all 7 specialist agents.
Enforces centralized authorization tokens, tool boundaries, sandbox isolation,
schema validation, and evidence tracking.
"""

import os
import sys
import json
import uuid
import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFINITIONS_DIR = os.path.join(AGENTS_DIR, "definitions")

if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

from sandbox.sandbox_runner import TaskSandbox, SandboxSecurityViolation
from approval_engine.approval_engine import HumanApprovalEngine, ApprovalViolation
from contracts.validate_agent_contract import (
    validate_agent_request,
    validate_agent_response
)


class BaseSpecialistAgent(ABC):
    def __init__(self, definition_filename: str, approval_engine: Optional[HumanApprovalEngine] = None):
        self.definition_path = os.path.join(DEFINITIONS_DIR, definition_filename)
        self.definition = self._load_definition()
        self.agent_id = self.definition["id"]
        self.name = self.definition["name"]
        self.slug = self.definition["slug"]
        self.role = self.definition["role"]
        self.tools_allowed = set(self.definition.get("tools_allowed", []))
        self.tools_prohibited = set(self.definition.get("tools_prohibited", []))
        self.system_prompt = self.definition.get("system_prompt", "")
        self.approval_engine = approval_engine

    def _load_definition(self) -> Dict[str, Any]:
        if not os.path.exists(self.definition_path):
            raise FileNotFoundError(f"Agent definition missing at {self.definition_path}")
        with open(self.definition_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def execute(self, request: Dict[str, Any], sandbox: TaskSandbox) -> Dict[str, Any]:
        """Main execution envelope: validates request, enforces token authorization, checks tools, calls execute_task, validates response."""
        is_req_valid, req_errors = validate_agent_request(request)
        if not is_req_valid:
            return self._build_failure_response(
                task_id=request.get("task_id", "UNKNOWN"),
                subtask_id=request.get("subtask_id", "UNKNOWN"),
                reason=f"Agent request validation failed: {req_errors}"
            )

        # Centralized Task-Bound Authorization Check
        engine = self.approval_engine or HumanApprovalEngine()
        auth_token = request.get("auth_token")
        if not engine.verify_authorization(request["task_id"], auth_token):
            return self._build_failure_response(
                task_id=request["task_id"],
                subtask_id=request.get("subtask_id", "UNKNOWN"),
                reason=(
                    f"AUTHORIZATION_DENIED: Execution rejected. Task-bound approval token missing, "
                    f"invalid, expired, or mismatched for '{request['task_id']}'."
                )
            )

        # Check requested tools against prohibited
        requested_tools = set(request.get("allowed_tools", []))
        prohibited_conflict = requested_tools.intersection(self.tools_prohibited)
        if prohibited_conflict:
            return self._build_failure_response(
                task_id=request["task_id"],
                subtask_id=request["subtask_id"],
                reason=f"Security violation: Agent attempted prohibited tools: {prohibited_conflict}"
            )

        try:
            # Delegate to specialized subclass implementation
            response_payload = self.execute_task(request, sandbox)
            is_resp_valid, resp_errors = validate_agent_response(response_payload)
            if not is_resp_valid:
                return self._build_failure_response(
                    task_id=request["task_id"],
                    subtask_id=request["subtask_id"],
                    reason=f"Agent response schema validation failed: {resp_errors}"
                )
            return response_payload
        except Exception as e:
            return self._build_failure_response(
                task_id=request["task_id"],
                subtask_id=request["subtask_id"],
                reason=f"Unhandled agent exception: {str(e)}"
            )

    @abstractmethod
    def execute_task(self, request: Dict[str, Any], sandbox: TaskSandbox) -> Dict[str, Any]:
        """Specialist logic implemented by individual agent."""
        pass

    def _build_failure_response(self, task_id: str, subtask_id: str, reason: str) -> Dict[str, Any]:
        return {
            "response_id": f"RESP-{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "agent_id": self.agent_id,
            "subtask_id": subtask_id,
            "status": "FAILURE",
            "work_performed": f"Agent {self.name} encountered an error: {reason}",
            "files_changed": [],
            "evidence": {"error": reason},
            "tests_executed": [{"test_name": "ExecutionCheck", "passed": False, "output": reason}],
            "remaining_limitations": [reason],
            "artifacts": [],
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _build_success_response(
        self,
        task_id: str,
        subtask_id: str,
        work_performed: str,
        files_changed: List[str],
        evidence: Dict[str, Any],
        tests_executed: List[Dict[str, Any]],
        remaining_limitations: List[str],
        artifacts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            "response_id": f"RESP-{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "agent_id": self.agent_id,
            "subtask_id": subtask_id,
            "status": "SUCCESS",
            "work_performed": work_performed,
            "files_changed": files_changed,
            "evidence": evidence,
            "tests_executed": tests_executed,
            "remaining_limitations": remaining_limitations,
            "artifacts": artifacts,
            "timestamp": datetime.datetime.now().isoformat()
        }
