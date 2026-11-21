"""test_phase5_orchestration.py
MASTER-AI Phase 5 Automated Test Suite: Autonomous Multi-Agent Orchestration & Task Execution

Covers:
1. Goal interpretation and DAG task decomposition.
2. Topological wave dependency scheduling.
3. Central agent registry queries, capabilities, and dynamic registration.
4. Tool permission enforcement and fail-closed zero-paid violation rejection.
5. Centralized approval center ticketing, authorization tokens, and expiration.
6. Execution tracing, observability metrics, and automatic secret scrubbing.
7. Anti-loop guards and duplicate subtask execution prevention.
8. Persistent lifecycle state transitions, checkpoints, and atomic file writes.
9. Process crash/restart recovery from intermediate checkpoints.
10. Retry budget and failure triage for failing subtasks.
11. Pause, resume, and cancellation lifecycle controls.
12. LangGraph evaluation reporting under Windows 11 / Python 3.14.5.
13. End-to-end acceptance test: "Research lions and prepare a Hindi documentary production plan".
14. REST API endpoint responses via FastAPI test client.
"""

import os
import sys
import json
import time
import unittest
from pathlib import Path

# Ensure workspace root is in sys.path
_current_dir = Path(__file__).resolve().parent
import importlib

_workspace_root = _current_dir.parents[1]
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

_orch_pkg = importlib.import_module("03_AI_AGENTS.orchestrator")
MasterOrchestrationCore = _orch_pkg.MasterOrchestrationCore
AgentRegistry = _orch_pkg.AgentRegistry
GoalDecomposer = _orch_pkg.GoalDecomposer
TaskLifecycleManager = _orch_pkg.TaskLifecycleManager
WorkflowBlackboard = _orch_pkg.WorkflowBlackboard
ToolExecutionGateway = _orch_pkg.ToolExecutionGateway
ExecutionTracer = _orch_pkg.ExecutionTracer
scrub_secrets = _orch_pkg.scrub_secrets
InvalidStateTransitionError = _orch_pkg.InvalidStateTransitionError
AgentLoopViolationError = _orch_pkg.AgentLoopViolationError
DuplicateTaskExecutionError = _orch_pkg.DuplicateTaskExecutionError
ToolPermissionViolationError = _orch_pkg.ToolPermissionViolationError
ZeroPaidPolicyViolationError = _orch_pkg.ZeroPaidPolicyViolationError

_appr_pkg = importlib.import_module("03_AI_AGENTS.approval_engine.approval_center")
ApprovalCenter = _appr_pkg.ApprovalCenter

_sand_pkg = importlib.import_module("03_AI_AGENTS.sandbox.sandbox_runner")
TaskSandbox = _sand_pkg.TaskSandbox


class TestPhase5Orchestration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = AgentRegistry()
        cls.core = MasterOrchestrationCore(registry=cls.registry)

    def test_01_goal_interpretation_and_decomposition(self):
        """Verify natural language goal is parsed and decomposed into a DAG with dependencies."""
        decomposer = GoalDecomposer(self.registry)
        goal = "Research lions and create a professional 5-minute documentary in Hindi"
        plan = decomposer.create_execution_plan(goal)

        self.assertIn("plan_id", plan)
        self.assertEqual(plan["analysis"]["intent"], "CONTENT_CREATION")
        self.assertEqual(plan["analysis"]["target_language"], "Hindi")
        self.assertEqual(plan["complexity"], "FULL_LIFECYCLE_FEDERATION")
        self.assertGreaterEqual(len(plan["subtasks"]), 5)

        # Check DAG dependencies
        st_ids = {st["subtask_id"] for st in plan["subtasks"]}
        for st in plan["subtasks"]:
            for dep in st.get("depends_on", []):
                self.assertIn(dep, st_ids, f"Dependency {dep} must exist in subtask set")

    def test_02_dependency_wave_scheduling(self):
        """Verify subtasks are partitioned into ordered execution waves."""
        decomposer = GoalDecomposer(self.registry)
        plan = decomposer.create_execution_plan("Research lions and prepare a Hindi documentary production plan")
        waves = plan["waves"]

        self.assertGreaterEqual(len(waves), 3, "Must have at least 3 distinct execution waves")
        # First wave must have zero dependencies
        first_wave_id = waves[0][0]
        first_st = next(s for s in plan["subtasks"] if s["subtask_id"] == first_wave_id)
        self.assertEqual(len(first_st["depends_on"]), 0, "First wave tasks must have no dependencies")

    def test_03_agent_registry_and_dynamic_registration(self):
        """Verify canonical 7 agents exist and future agents can register dynamically."""
        agents = self.registry.list_agents()
        self.assertGreaterEqual(len(agents), 7)

        # Verify AGT-001 through AGT-007 exist
        agent_ids = {a["id"] for a in agents}
        for expected in ["AGT-001", "AGT-002", "AGT-003", "AGT-004", "AGT-005", "AGT-006", "AGT-007"]:
            self.assertIn(expected, agent_ids)

        # Test dynamic agent registration
        dyn_agent = {
            "id": "AGT-DYN-01",
            "name": "Dynamic Media Agent",
            "slug": "dynamic_media_agent",
            "role": "Media Rendering Specialist",
            "capabilities": ["video_splicing", "audio_mixing"],
            "task_eligibility": ["MEDIA_RENDER", "AUDIO_MIX"]
        }
        res = self.registry.register_agent(dyn_agent)
        self.assertTrue(res)
        retrieved = self.registry.get_agent("AGT-DYN-01")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Dynamic Media Agent")

    def test_04_tool_permissions_and_zero_paid_enforcement(self):
        """Verify prohibited tools are blocked and paid tools require authorization."""
        gateway = ToolExecutionGateway(self.registry)

        # AGT-001 is prohibited from execute_subprocess and activate_paid_api
        with self.assertRaises(ToolPermissionViolationError):
            gateway.execute_tool(
                agent_id="AGT-001",
                tool_name="execute_subprocess",
                parameters={"cmd": "whoami"}
            )

        # Paid API invocation without token must trigger ZeroPaidPolicyViolationError
        with self.assertRaises(ZeroPaidPolicyViolationError):
            gateway.execute_tool(
                agent_id="AGT-003",
                tool_name="sandbox_eval",
                parameters={"use_paid_provider": True}
            )

    def test_05_centralized_approval_center(self):
        """Verify approval ticket lifecycle: request -> pending -> approve/reject/revoke."""
        appr = ApprovalCenter()
        ticket = appr.request_approval(
            category="PAID_API_CALL",
            title="External Model Execution Request",
            description="Agent requested external API for high-resolution rendering",
            requesting_agent="AGT-003",
            target_resource="cloud_render_service"
        )
        tkt_id = ticket["ticket_id"]
        self.assertEqual(ticket["status"], "PENDING")

        # Approve ticket
        approved = appr.approve_ticket(tkt_id, actor="admin_operator", reason="Approved for testing")
        self.assertEqual(approved["status"], "APPROVED")
        token = approved["auth_token"]
        self.assertIsNotNone(token)
        self.assertTrue(token.startswith("AUTH-"))

        # Verify token validity
        self.assertTrue(appr.verify_token(tkt_id, token))
        self.assertFalse(appr.verify_token(tkt_id, "AUTH-INVALID"))

    def test_06_observability_and_secret_scrubbing(self):
        """Verify execution tracer records events and scrubs confidential credentials."""
        raw_text = "Connecting to service with api_key: 'AIzaSyD-TEST-FAKE-KEY-123456789' and password: 'SecretPassword99'"
        scrubbed = scrub_secrets(raw_text)
        self.assertNotIn("AIzaSyD-TEST-FAKE-KEY-123456789", scrubbed)
        self.assertNotIn("SecretPassword99", scrubbed)
        self.assertIn("[REDACTED_SECRET]", scrubbed)

        tracer = ExecutionTracer("WF-OBSERVABILITY-TEST")
        tracer.record_event("API_CALL", raw_text)
        trace = tracer.get_trace()
        self.assertEqual(trace["metrics"]["total_events"], 1)
        self.assertNotIn("SecretPassword99", str(trace))

    def test_07_anti_loop_and_idempotency_guards(self):
        """Verify blackboard prevents duplicate subtask runs and rejects excessive handoff loops."""
        bb = WorkflowBlackboard("WF-LOOP-TEST")

        # Idempotency
        self.assertTrue(bb.verify_and_claim_subtask("ST-01"))
        with self.assertRaises(DuplicateTaskExecutionError):
            bb.verify_and_claim_subtask("ST-01")

        # Anti-loop hops (limit 10)
        for i in range(10):
            bb.post_message("AGT-001", "AGT-002", "TASK_HANDOFF", {"subtask_id": "ST-BOUNCE"})

        with self.assertRaises(AgentLoopViolationError):
            bb.post_message("AGT-001", "AGT-002", "TASK_HANDOFF", {"subtask_id": "ST-BOUNCE"})

    def test_08_lifecycle_persistence_and_restart_recovery(self):
        """Verify workflow state is persisted to disk and can resume from checkpoints."""
        lifecycle = TaskLifecycleManager()
        plan = self.core.submit_goal("General task lifecycle test")
        wf_id = lifecycle.create_workflow(plan)

        # Verify persisted on disk
        loaded = lifecycle.load_workflow(wf_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["status"], "PLANNED")

        # Update subtask and transition
        lifecycle.transition_workflow_status(wf_id, "APPROVED")
        lifecycle.transition_workflow_status(wf_id, "QUEUED")
        lifecycle.transition_workflow_status(wf_id, "RUNNING")

        st_id = plan["subtasks"][0]["subtask_id"]
        lifecycle.update_subtask_status(wf_id, st_id, "COMPLETED", outputs={"res": "OK"})

        # Reload after simulated process restart
        reloaded = lifecycle.load_workflow(wf_id)
        self.assertEqual(reloaded["status"], "RUNNING")
        self.assertEqual(reloaded["subtasks"][st_id]["status"], "COMPLETED")
        self.assertGreaterEqual(len(reloaded["checkpoint_history"]), 3)

    def test_09_pause_resume_and_cancellation(self):
        """Verify workflow pause, resume, and cancellation mechanics."""
        plan = self.core.submit_goal("Cancellation and pause test")
        wf = self.core.approve_plan(plan["plan_id"])
        wf_id = wf["workflow_id"]

        paused = self.core.pause_workflow(wf_id)
        self.assertEqual(paused["status"], "PAUSED")

        cancelled = self.core.cancel_workflow(wf_id, reason="User test cancellation")
        self.assertEqual(cancelled["status"], "CANCELLED")

        # Invalid transition from CANCELLED must raise error
        with self.assertRaises(InvalidStateTransitionError):
            self.core.lifecycle.transition_workflow_status(wf_id, "RUNNING")

    def test_10_langgraph_compatibility_evaluation(self):
        """Verify LangGraph evaluation report produces valid metrics under Windows 11."""
        report = self.core.evaluate_langgraph_integration()
        self.assertIn("framework", report)
        self.assertEqual(report["framework"], "LangGraph")
        self.assertTrue(report["compatible"])
        self.assertEqual(report["os"], "Windows 11")

    def test_11_end_to_end_hindi_documentary_workflow(self):
        """End-to-End Acceptance: 'Research lions and prepare a Hindi documentary production plan'.
        Executes across Research Agent -> Architect -> Testing Agent -> Security Auditor -> Documentation Agent.
        """
        goal = "Research lions and prepare a Hindi documentary production plan."
        plan = self.core.submit_goal(goal)
        self.assertEqual(plan["analysis"]["intent"], "CONTENT_CREATION")
        self.assertEqual(plan["analysis"]["target_language"], "Hindi")

        # Approve and initialize workflow
        wf = self.core.approve_plan(plan["plan_id"])
        wf_id = wf["workflow_id"]

        # Execute all waves
        completed_wf = self.core.execute_workflow(wf_id)

        self.assertEqual(completed_wf["status"], "COMPLETED")
        self.assertEqual(completed_wf["current_wave_index"], len(completed_wf["waves"]))

        # Verify all subtasks are COMPLETED
        for st_id, st in completed_wf["subtasks"].items():
            self.assertEqual(st["status"], "COMPLETED", f"Subtask {st_id} should be COMPLETED")

        # Verify final deliverable
        deliverable = completed_wf.get("final_deliverable", {})
        self.assertEqual(deliverable["status"], "SUCCESS")
        self.assertIn("documentary_production_plan_hindi.md", deliverable["artifacts_produced"])
        self.assertIn("research_dossier.json", deliverable["artifacts_produced"])
        self.assertIn("documentary_storyboard.json", deliverable["artifacts_produced"])
        self.assertIn("timing_validation_report.json", deliverable["artifacts_produced"])
        self.assertIn("content_risk_audit.json", deliverable["artifacts_produced"])

        # Check script contents
        sandbox_path = deliverable["sandbox_path"]
        script_file = os.path.join(sandbox_path, "documentary_production_plan_hindi.md")
        self.assertTrue(os.path.exists(script_file))
        with open(script_file, "r", encoding="utf-8") as f:
            script_text = f.read()
        self.assertIn("सवाना का सम्राट", script_text)
        self.assertIn("प्राइड", script_text)
        self.assertIn("Act I: Dawn on the Savannah", script_text)

        # Check trace
        trace = self.core.get_execution_trace(wf_id)
        self.assertEqual(trace["status"], "COMPLETED")
        self.assertEqual(trace["estimated_cost_usd"], 0.00)
        self.assertGreater(trace["metrics"]["total_events"], 5)

    def test_12_fastapi_orchestrator_endpoints(self):
        """Verify REST API endpoints respond with 200 and expected schemas."""
        from fastapi.testclient import TestClient
        import importlib

        main_mod = importlib.import_module("00_CORE_SYSTEM.api.main")
        client = TestClient(main_mod.app)

        # 1. Health check
        res = client.get("/health")
        self.assertEqual(res.status_code, 200)

        # 2. List agents
        res = client.get("/api/v1/orchestrator/agents")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(res.json()["count"], 7)

        # 3. Create goal
        res = client.post("/api/v1/orchestrator/goals", json={"goal": "Build an API in Python"})
        self.assertEqual(res.status_code, 200)
        plan_id = res.json()["plan"]["plan_id"]

        # 4. Get plan
        res = client.get(f"/api/v1/orchestrator/plans/{plan_id}")
        self.assertEqual(res.status_code, 200)

        # 5. Approve plan
        res = client.post(f"/api/v1/orchestrator/plans/{plan_id}/approve", json={})
        self.assertEqual(res.status_code, 200)
        wf_id = res.json()["workflow"]["workflow_id"]

        # 6. Get status
        res = client.get(f"/api/v1/orchestrator/workflows/{wf_id}/status")
        self.assertEqual(res.status_code, 200)

        # 7. List approvals
        res = client.get("/api/v1/orchestrator/approvals")
        self.assertEqual(res.status_code, 200)

        # 8. LangGraph evaluation
        res = client.get("/api/v1/orchestrator/evaluation/langgraph")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["compatible"])


if __name__ == "__main__":
    unittest.main()
