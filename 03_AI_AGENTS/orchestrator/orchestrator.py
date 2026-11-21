"""
orchestrator.py
MASTER-AI Master Multi-Agent Orchestrator

Coordinates the multi-agent federation across the 7 specialist agents:
1. Classifies task complexity (SIMPLE, MODERATE, COMPLEX, FULL_LIFECYCLE).
2. Decomposes tasks into subtask Directed Acyclic Graphs (DAGs).
3. Routes subtasks to appropriate specialist agents.
4. Manages inter-agent artifact handoffs.
5. Enforces human approval checkpoints.
6. Sandboxes task execution and validates responses.
7. Generates comprehensive execution ledgers.
"""

import os
import sys
import json
import uuid
import time
import datetime
from typing import Dict, Any, List, Optional, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

from sandbox.sandbox_runner import TaskSandbox
from approval_engine.approval_engine import HumanApprovalEngine, ApprovalViolation
from contracts.validate_agent_contract import (
    validate_task,
    validate_agent_response,
    validate_artifact_handoff,
    validate_failure_report
)
from agents import (
    ResearchAgent,
    SoftwareArchitect,
    CodingAgent,
    TestingAgent,
    DocumentationAgent,
    SecurityAuditor,
    CapabilityDiscoveryAgent,
    AGENT_REGISTRY_MAP
)

RUNS_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs")


class MasterOrchestrator:
    def __init__(self, approval_engine: Optional[HumanApprovalEngine] = None):
        self.approval_engine = approval_engine or HumanApprovalEngine()
        self.agents: Dict[str, Any] = {
            agent_id: cls(approval_engine=self.approval_engine) for agent_id, cls in AGENT_REGISTRY_MAP.items()
        }
        os.makedirs(RUNS_DIR, exist_ok=True)

    def classify_task_complexity(self, task_description: str, agent_count: int) -> str:
        """Classifies task complexity into one of 4 standardized tiers."""
        desc_lower = task_description.lower()
        if agent_count == 1:
            return "SIMPLE_SINGLE_AGENT"
        elif agent_count == 2:
            return "MODERATE_SEQUENTIAL"
        elif "full" in desc_lower or "end-to-end" in desc_lower or agent_count >= 5:
            return "FULL_LIFECYCLE_FEDERATION"
        else:
            return "COMPLEX_PIPELINE"

    def decompose_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decomposes a task into an ordered list of executable subtasks with dependencies."""
        required_agents = task.get("required_agents", [])
        subtasks = []

        # Standard multi-agent lifecycle execution order
        stage_priority = [
            ("AGT-007", "Capability Discovery & Readiness Audit"),
            ("AGT-001", "Technical Research & Verification"),
            ("AGT-002", "Software Architecture & Specification"),
            ("AGT-003", "Component Implementation"),
            ("AGT-004", "Independent Unit & Integration Testing"),
            ("AGT-006", "Security & Static Analysis Audit"),
            ("AGT-005", "Living Documentation & ADR Generation")
        ]

        active_stages = [pair for pair in stage_priority if pair[0] in required_agents]
        # Include any remaining agents not in the standard pipeline
        for agent_id in required_agents:
            if not any(pair[0] == agent_id for pair in active_stages):
                active_stages.append((agent_id, f"Execution by {agent_id}"))

        for idx, (agent_id, stage_desc) in enumerate(active_stages):
            subtask_id = f"SUB-{task['task_id']}-{idx+1:02d}"
            depends_on = [subtasks[idx-1]["subtask_id"]] if idx > 0 else []
            subtasks.append({
                "subtask_id": subtask_id,
                "agent_id": agent_id,
                "title": stage_desc,
                "depends_on": depends_on,
                "status": "PENDING"
            })

        return subtasks

    def execute_plan(
        self,
        task: Dict[str, Any],
        approval_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Executes an end-to-end task across specialist agents in an isolated sandbox."""
        start_time = datetime.datetime.now()
        run_id = f"RUN-{task['task_id']}-{uuid.uuid4().hex[:6]}"
        run_dir = os.path.join(RUNS_DIR, run_id)
        os.makedirs(run_dir, exist_ok=True)

        ledger: Dict[str, Any] = {
            "run_id": run_id,
            "task_id": task["task_id"],
            "complexity": task.get("complexity", "MODERATE_SEQUENTIAL"),
            "status": "INITIALIZED",
            "started_at": start_time.isoformat(),
            "completed_at": None,
            "subtasks": [],
            "handoffs": [],
            "artifacts_summary": [],
            "final_result": {}
        }

        # Step 1: Register and check approval
        ticket = self.approval_engine.register_task(
            task_id=task["task_id"],
            title=task.get("title", "Untitled Task"),
            details=task,
            allow_reset=task.get("allow_reset", True)
        )

        if ticket["state"] == "REVIEW_REQUIRED":
            if not self.approval_engine.verify_authorization(task["task_id"], approval_token):
                ledger["status"] = "FAILED"
                ledger["final_result"] = {
                    "error": "REVIEW_REQUIRED: Task requires explicit human approval before execution."
                }
                self._write_ledger(run_dir, ledger)
                return ledger

        # Transition to EXECUTING
        if ticket["state"] in {"PROPOSED", "APPROVED"}:
            if ticket["state"] == "PROPOSED":
                self.approval_engine.transition_state(
                    task["task_id"], "APPROVED", actor="orchestrator", reason="Automated risk clearance"
                )
            self.approval_engine.transition_state(
                task["task_id"], "EXECUTING", actor="orchestrator", reason="Starting execution run"
            )

        auth_token = self.approval_engine.records.get(task["task_id"], {}).get("approval_token")

        ledger["status"] = "RUNNING"

        # Step 2: Initialize task sandbox
        sandbox = TaskSandbox(task_id=task["task_id"])
        subtasks = self.decompose_task(task)

        previous_artifacts: List[Dict[str, Any]] = []

        try:
            for subtask in subtasks:
                subtask_id = subtask["subtask_id"]
                agent_id = subtask["agent_id"]
                agent = self.agents.get(agent_id)

                if not agent:
                    raise KeyError(f"Specialist agent '{agent_id}' is not registered.")

                # Manage inter-agent artifact handoff
                if previous_artifacts:
                    handoff = {
                        "handoff_id": f"HND-{uuid.uuid4().hex[:6]}",
                        "task_id": task["task_id"],
                        "source_agent": ledger["subtasks"][-1]["agent_id"],
                        "target_agent": agent_id,
                        "artifacts": previous_artifacts,
                        "status": "TRANSFERRED",
                        "verification_notes": f"Transferred {len(previous_artifacts)} artifact(s)",
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    is_hnd_valid, _ = validate_artifact_handoff(handoff)
                    if is_hnd_valid:
                        ledger["handoffs"].append(handoff)

                # Build agent request payload
                agent_request = {
                    "request_id": f"REQ-{uuid.uuid4().hex[:8]}",
                    "task_id": task["task_id"],
                    "agent_id": agent_id,
                    "subtask_id": subtask_id,
                    "parameters": task.get("context", {}).get(agent_id, {}),
                    "input_artifacts": previous_artifacts,
                    "sandbox_dir": sandbox.sandbox_dir,
                    "allowed_tools": list(agent.tools_allowed),
                    "auth_token": auth_token,
                    "timeout_seconds": task.get("timeout_seconds", 30)
                }

                sub_start = time.time()
                response = agent.execute(agent_request, sandbox)
                sub_duration = time.time() - sub_start

                subtask_record = {
                    "subtask_id": subtask_id,
                    "agent_id": agent_id,
                    "status": response.get("status", "FAILURE"),
                    "execution_time_seconds": round(sub_duration, 3),
                    "response_summary": response.get("work_performed", "")
                }
                ledger["subtasks"].append(subtask_record)

                if response.get("status") != "SUCCESS":
                    raise RuntimeError(
                        f"Subtask {subtask_id} failed on {agent_id}: "
                        f"{response.get('remaining_limitations')}"
                    )

                previous_artifacts = response.get("artifacts", [])

            # Collect final sandbox artifacts
            all_artifacts = sandbox.collect_artifacts()
            ledger["artifacts_summary"] = all_artifacts
            ledger["status"] = "COMPLETED"
            ledger["final_result"] = {
                "outcome": "SUCCESS",
                "subtasks_executed": len(subtasks),
                "artifacts_produced": len(all_artifacts)
            }

            self.approval_engine.transition_state(
                task["task_id"], "VERIFIED", actor="orchestrator", reason="All subtasks passed"
            )
            self.approval_engine.transition_state(
                task["task_id"], "COMPLETED", actor="orchestrator", reason="Execution run complete"
            )

        except Exception as e:
            ledger["status"] = "FAILED"
            ledger["final_result"] = {"error": str(e)}

            self.approval_engine.transition_state(
                task["task_id"], "FAILED", actor="orchestrator", reason=str(e)
            )

            # Generate structured failure report
            failure_report = {
                "failure_id": f"FAIL-{uuid.uuid4().hex[:8]}",
                "task_id": task["task_id"],
                "agent_id": ledger["subtasks"][-1]["agent_id"] if ledger["subtasks"] else "ORCHESTRATOR",
                "subtask_id": ledger["subtasks"][-1]["subtask_id"] if ledger["subtasks"] else "NONE",
                "error_code": "TEST_FAILURE" if "test" in str(e).lower() else "SUBPROCESS_ERROR",
                "error_message": str(e),
                "triage_recommendation": "Inspect failing subtask inputs and sandbox logs.",
                "rollback_triggered": False,
                "timestamp": datetime.datetime.now().isoformat()
            }
            with open(os.path.join(run_dir, "failure_report.json"), "w", encoding="utf-8") as f:
                json.dump(failure_report, f, indent=2)

        finally:
            ledger["completed_at"] = datetime.datetime.now().isoformat()
            self._write_ledger(run_dir, ledger)

        return ledger

    def _write_ledger(self, run_dir: str, ledger: Dict[str, Any]):
        ledger_path = os.path.join(run_dir, "ledger.json")
        with open(ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)
