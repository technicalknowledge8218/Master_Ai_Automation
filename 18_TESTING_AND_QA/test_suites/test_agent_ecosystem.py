"""
test_agent_ecosystem.py
MASTER-AI Phase 4 Multi-Agent Ecosystem End-to-End Test Suite

Executes the 9 mandatory agent test scenarios:
1. Research Agent empirical research & evidence.
2. Architect Agent structured system spec design.
3. Coding Agent type-safe component implementation.
4. Testing Agent independent test suite execution.
5. Security Auditor static analysis & secret audit.
6. Documentation Agent ADR creation & structure check.
7. Master Orchestrator end-to-end multi-agent pipeline synthesis.
8. Safe failure handling on intentionally failing task.
9. Unauthorized global action block by Human Approval Engine.
"""

import os
import sys
import json
import time
import shutil

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGENTS_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS")

if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

from sandbox.sandbox_runner import TaskSandbox
from approval_engine.approval_engine import HumanApprovalEngine, ApprovalViolation
from contracts.validate_agent_contract import (
    validate_agent_response,
    validate_task,
    validate_failure_report
)
from agents import (
    ResearchAgent,
    SoftwareArchitect,
    CodingAgent,
    TestingAgent,
    DocumentationAgent,
    SecurityAuditor,
    CapabilityDiscoveryAgent
)
from orchestrator.orchestrator import MasterOrchestrator

TEST_SUMMARY_FILE = os.path.join(
    WORKSPACE_ROOT, "18_TESTING_AND_QA", "test_suites", "agent_ecosystem_test_summary.json"
)


def run_scenario_1_research() -> dict:
    """Scenario 1: Research Agent researches local technical question and returns evidence."""
    task_id = "TSK-TEST-SCENARIO-1"
    engine = HumanApprovalEngine()
    engine.register_task(task_id, "Scenario 1", {"action": "research"}, allow_reset=True)
    ticket = engine.transition_state(task_id, "APPROVED", actor="test_runner")
    token = ticket["approval_token"]

    sandbox = TaskSandbox(task_id)
    agent = ResearchAgent(approval_engine=engine)
    request = {
        "request_id": "REQ-TEST-001",
        "task_id": task_id,
        "agent_id": "AGT-001",
        "subtask_id": "SUB-001",
        "parameters": {
            "query": "Three-Tier Architecture in Python",
            "ecosystem": "Python",
            "target_version": "3.12"
        },
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "search_web", "view_file"],
        "auth_token": token,
        "timeout_seconds": 15
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    is_valid, errs = validate_agent_response(resp)
    passed = is_valid and resp.get("status") == "SUCCESS" and len(resp.get("artifacts", [])) > 0
    return {
        "scenario": "Scenario 1: Research Agent Empirical Research",
        "agent": "AGT-001 (Research Agent)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": resp.get("work_performed", ""),
        "errors": errs
    }


def run_scenario_2_architect() -> dict:
    """Scenario 2: Architect Agent produces structured design from requirement."""
    task_id = "TSK-TEST-SCENARIO-2"
    engine = HumanApprovalEngine()
    engine.register_task(task_id, "Scenario 2", {"action": "architecture"}, allow_reset=True)
    ticket = engine.transition_state(task_id, "APPROVED", actor="test_runner")
    token = ticket["approval_token"]

    sandbox = TaskSandbox(task_id)
    agent = SoftwareArchitect(approval_engine=engine)
    request = {
        "request_id": "REQ-TEST-002",
        "task_id": task_id,
        "agent_id": "AGT-002",
        "subtask_id": "SUB-002",
        "parameters": {
            "system_name": "TestMathService",
            "pattern": "three-tier-decoupled"
        },
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "write_file", "edit_file", "run_command"],
        "auth_token": token,
        "timeout_seconds": 15
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    is_valid, errs = validate_agent_response(resp)
    passed = is_valid and resp.get("status") == "SUCCESS" and "system_architecture_spec.json" in resp.get("files_changed", [])
    return {
        "scenario": "Scenario 2: Software Architect System Design",
        "agent": "AGT-002 (Software Architect)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": resp.get("work_performed", ""),
        "errors": errs
    }


def run_scenario_3_coding() -> dict:
    """Scenario 3: Coding Agent implements small disposable test project."""
    task_id = "TSK-TEST-SCENARIO-3"
    engine = HumanApprovalEngine()
    engine.register_task(task_id, "Scenario 3", {"action": "coding"}, allow_reset=True)
    ticket = engine.transition_state(task_id, "APPROVED", actor="test_runner")
    token = ticket["approval_token"]

    sandbox = TaskSandbox(task_id)
    agent = CodingAgent(approval_engine=engine)
    request = {
        "request_id": "REQ-TEST-003",
        "task_id": task_id,
        "agent_id": "AGT-003",
        "subtask_id": "SUB-003",
        "parameters": {
            "module_name": "calc_module",
            "code_type": "calculator_module"
        },
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "write_file", "edit_file", "run_command"],
        "auth_token": token,
        "timeout_seconds": 15
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    is_valid, errs = validate_agent_response(resp)
    passed = is_valid and resp.get("status") == "SUCCESS" and "calc_module.py" in resp.get("files_changed", [])
    return {
        "scenario": "Scenario 3: Coding Agent Type-Safe Implementation",
        "agent": "AGT-003 (Coding Agent)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": resp.get("work_performed", ""),
        "errors": errs
    }


def run_scenario_4_testing() -> dict:
    """Scenario 4: Testing Agent independently tests that project."""
    task_id = "TSK-TEST-SCENARIO-4"
    engine = HumanApprovalEngine()
    engine.register_task(task_id, "Scenario 4", {"action": "testing"}, allow_reset=True)
    ticket = engine.transition_state(task_id, "APPROVED", actor="test_runner")
    token = ticket["approval_token"]

    sandbox = TaskSandbox(task_id)
    # First seed the coding agent module into sandbox
    coding_agent = CodingAgent(approval_engine=engine)
    coding_agent.execute({
        "request_id": "REQ-SEED-004",
        "task_id": task_id,
        "agent_id": "AGT-003",
        "subtask_id": "SUB-SEED",
        "parameters": {"module_name": "sample_service", "code_type": "calculator_module"},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "write_file", "edit_file", "run_command"],
        "auth_token": token,
        "timeout_seconds": 15
    }, sandbox)

    # Now execute testing agent
    agent = TestingAgent(approval_engine=engine)
    request = {
        "request_id": "REQ-TEST-004",
        "task_id": task_id,
        "agent_id": "AGT-004",
        "subtask_id": "SUB-004",
        "parameters": {"target_module": "sample_service"},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "write_file", "edit_file", "run_command"],
        "auth_token": token,
        "timeout_seconds": 15
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    is_valid, errs = validate_agent_response(resp)
    passed = is_valid and resp.get("status") == "SUCCESS" and len(resp.get("tests_executed", [])) > 0
    return {
        "scenario": "Scenario 4: Testing Agent Independent QA",
        "agent": "AGT-004 (Testing Agent)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": resp.get("work_performed", ""),
        "errors": errs
    }


def run_scenario_5_security() -> dict:
    """Scenario 5: Security Auditor inspects the test project."""
    task_id = "TSK-TEST-SCENARIO-5"
    engine = HumanApprovalEngine()
    engine.register_task(task_id, "Scenario 5", {"action": "security"}, allow_reset=True)
    ticket = engine.transition_state(task_id, "APPROVED", actor="test_runner")
    token = ticket["approval_token"]

    sandbox = TaskSandbox(task_id)
    # Seed a clean file
    sandbox.write_file("clean_app.py", "def greet(name: str) -> str:\n    return f'Hello {name}'\n")

    agent = SecurityAuditor(approval_engine=engine)
    request = {
        "request_id": "REQ-TEST-005",
        "task_id": task_id,
        "agent_id": "AGT-006",
        "subtask_id": "SUB-005",
        "parameters": {},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "view_file"],
        "auth_token": token,
        "timeout_seconds": 15
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    is_valid, errs = validate_agent_response(resp)
    passed = is_valid and resp.get("status") == "SUCCESS" and resp.get("evidence", {}).get("verdict") == "PASS"
    return {
        "scenario": "Scenario 5: Security Auditor Zero-Trust Audit",
        "agent": "AGT-006 (Security Auditor)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": resp.get("work_performed", ""),
        "errors": errs
    }


def run_scenario_6_documentation() -> dict:
    """Scenario 6: Documentation Agent creates a test report & ADR."""
    task_id = "TSK-TEST-SCENARIO-6"
    engine = HumanApprovalEngine()
    engine.register_task(task_id, "Scenario 6", {"action": "documentation"}, allow_reset=True)
    ticket = engine.transition_state(task_id, "APPROVED", actor="test_runner")
    token = ticket["approval_token"]

    sandbox = TaskSandbox(task_id)
    agent = DocumentationAgent(approval_engine=engine)
    request = {
        "request_id": "REQ-TEST-006",
        "task_id": task_id,
        "agent_id": "AGT-005",
        "subtask_id": "SUB-006",
        "parameters": {
            "adr_id": "006",
            "title": "Automated Multi-Agent Service Implementation",
            "status": "ACCEPTED"
        },
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file", "write_file", "edit_file", "run_command"],
        "auth_token": token,
        "timeout_seconds": 15
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    is_valid, errs = validate_agent_response(resp)
    passed = is_valid and resp.get("status") == "SUCCESS" and "ADR-006.md" in resp.get("files_changed", [])
    return {
        "scenario": "Scenario 6: Documentation Agent ADR Generation",
        "agent": "AGT-005 (Documentation Agent)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": resp.get("work_performed", ""),
        "errors": errs
    }


def run_scenario_7_orchestration() -> dict:
    """Scenario 7: Master Orchestrator combines all outputs into one final result."""
    orchestrator = MasterOrchestrator()
    task = {
        "task_id": "TSK-E2E-FULL-PIPELINE",
        "title": "Full Multi-Agent Engineering Federation Pipeline",
        "description": "Execute end-to-end engineering pipeline from research to documentation",
        "complexity": "FULL_LIFECYCLE_FEDERATION",
        "required_agents": [
            "AGT-001",
            "AGT-002",
            "AGT-003",
            "AGT-004",
            "AGT-006",
            "AGT-005"
        ],
        "approval_state": "PROPOSED",
        "created_at": "2026-11-17T01:00:00",
        "context": {
            "AGT-001": {"query": "Clean Architecture in Python", "ecosystem": "Python"},
            "AGT-002": {"system_name": "PipelineService", "pattern": "three-tier-decoupled"},
            "AGT-003": {"module_name": "sample_service", "code_type": "calculator_module"},
            "AGT-004": {"target_module": "sample_service"},
            "AGT-005": {"adr_id": "007", "title": "Pipeline Integration ADR", "status": "ACCEPTED"},
            "AGT-006": {}
        },
        "timeout_seconds": 30
    }

    ledger = orchestrator.execute_plan(task)
    passed = (
        ledger.get("status") == "COMPLETED" and
        len(ledger.get("subtasks", [])) == 6 and
        all(s["status"] == "SUCCESS" for s in ledger.get("subtasks", [])) and
        len(ledger.get("handoffs", [])) >= 5
    )

    return {
        "scenario": "Scenario 7: Master Orchestrator Full-Lifecycle Federation",
        "agent": "Master Orchestrator (Orchestrating 6 Specialist Agents)",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": f"Executed {len(ledger.get('subtasks', []))} subtasks with {len(ledger.get('handoffs', []))} artifact handoffs.",
        "errors": [] if passed else [ledger.get("final_result", {}).get("error", "Orchestration failed")]
    }


def run_scenario_8_failure_handling() -> dict:
    """Scenario 8: Intentionally failing task triggers safe failure handling."""
    orchestrator = MasterOrchestrator()
    # Task requesting an invalid agent that will raise an error
    task = {
        "task_id": "TSK-FAIL-SAFE-TEST",
        "title": "Intentionally Failing Task",
        "description": "Trigger safe failure handling",
        "complexity": "SIMPLE_SINGLE_AGENT",
        "required_agents": ["AGT-NONEXISTENT"],
        "approval_state": "PROPOSED",
        "created_at": "2026-11-17T01:00:00",
        "context": {},
        "timeout_seconds": 10
    }

    ledger = orchestrator.execute_plan(task)
    passed = ledger.get("status") == "FAILED" and "error" in ledger.get("final_result", {})

    return {
        "scenario": "Scenario 8: Intentionally Failing Task Safe Handling",
        "agent": "Master Orchestrator / Failure Subsystem",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": "Safe failure triggered, ledger recorded FAILED status, failure report generated.",
        "errors": []
    }


def run_scenario_9_unauthorized_global_blocked() -> dict:
    """Scenario 9: Unauthorized global action is blocked by Human Approval Engine."""
    approval_engine = HumanApprovalEngine()
    # High risk task attempting global deployment without approval
    high_risk_task = {
        "task_id": "TSK-UNAUTH-GLOBAL-TEST",
        "title": "Unauthorized Global Deployment",
        "description": "Attempting to deploy skill to ~/.gemini global config without authorization",
        "action": "global_skill_deployment",
        "target": "<USER_HOME>/.gemini/config"
    }

    ticket = approval_engine.register_task(
        task_id=high_risk_task["task_id"],
        title=high_risk_task["title"],
        details=high_risk_task,
        allow_reset=True
    )

    # Must be placed in REVIEW_REQUIRED immediately
    initial_review_required = (ticket["state"] == "REVIEW_REQUIRED")

    # Attempting operation check without token must be blocked
    allowed, reason = approval_engine.check_operation_allowed(
        task_id=high_risk_task["task_id"],
        operation="global_skill_deployment",
        token=None
    )
    operation_blocked = (allowed is False and "BLOCKED" in reason)

    passed = initial_review_required and operation_blocked

    return {
        "scenario": "Scenario 9: Unauthorized Global Action Blocked",
        "agent": "Human Approval Engine",
        "passed": passed,
        "mode": "REAL_AGENT_EXECUTION",
        "details": f"High-risk action intercepted: {reason}",
        "errors": []
    }


def main():
    print("=== MASTER-AI PHASE 4 AGENT ECOSYSTEM TEST RUNNER ===\n")
    scenarios = [
        run_scenario_1_research,
        run_scenario_2_architect,
        run_scenario_3_coding,
        run_scenario_4_testing,
        run_scenario_5_security,
        run_scenario_6_documentation,
        run_scenario_7_orchestration,
        run_scenario_8_failure_handling,
        run_scenario_9_unauthorized_global_blocked
    ]

    results = []
    all_passed = True
    start_time = time.time()

    for idx, sc_fn in enumerate(scenarios, 1):
        res = sc_fn()
        results.append(res)
        status_str = "PASS" if res["passed"] else "FAIL"
        if not res["passed"]:
            all_passed = False
        print(f"[{status_str}] {res['scenario']} ({res['mode']})")
        print(f"       Details: {res['details']}")
        if res.get("errors"):
            print(f"       Errors: {res['errors']}")

    duration = time.time() - start_time
    summary = {
        "suite_name": "Phase 4 Multi-Agent Ecosystem End-to-End Suite",
        "total_scenarios": len(scenarios),
        "passed_scenarios": sum(1 for r in results if r["passed"]),
        "failed_scenarios": sum(1 for r in results if not r["passed"]),
        "all_passed": all_passed,
        "execution_time_seconds": round(duration, 3),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }

    with open(TEST_SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=======================================================")
    print(f"OVERALL SUMMARY: {summary['passed_scenarios']}/{summary['total_scenarios']} PASSED in {duration:.3f}s | ALL_PASSED = {all_passed}")
    print(f"=======================================================")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
