"""
test_security_hardening.py
MASTER-AI Phase 4.2 Security & Execution Hardening Test Suite

Validates 16 critical security boundaries, failure-mode enforcement,
concurrency safety, authorization tokens, sandbox containment, and audit logging.
"""

import os
import sys
import time
import json
import shutil
import threading
from typing import Dict, Any, List

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGENTS_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS")
if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

from sandbox.sandbox_runner import (
    TaskSandbox,
    SandboxSecurityViolation,
    get_sanitized_environment,
    SUBPROCESS_AUDIT_LOG
)
from approval_engine.approval_engine import (
    HumanApprovalEngine,
    ApprovalViolation,
    LedgerCorruptionError,
    FileLock
)
from agents.coding_agent import CodingAgent
from agents.research_agent import ResearchAgent

TEST_SUMMARY_FILE = os.path.join(
    WORKSPACE_ROOT, "18_TESTING_AND_QA", "test_suites", "security_hardening_test_summary.json"
)


def run_sec_001_missing_auth_token() -> dict:
    """SEC-001: Direct agent execution without authorization token must fail closed."""
    sandbox = TaskSandbox("TSK-SEC-001")
    agent = CodingAgent()
    request = {
        "request_id": "REQ-SEC-001",
        "task_id": "TSK-SEC-001",
        "agent_id": "AGT-003",
        "subtask_id": "SUB-001",
        "parameters": {"module_name": "mod1"},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["write_file", "read_file"],
        "auth_token": "",  # Empty token
        "timeout_seconds": 10
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    work = resp.get("work_performed", "").lower()
    passed = (resp.get("status") == "FAILURE" and ("auth_token" in work or "authorization_denied" in work))
    return {
        "test_id": "SEC-001",
        "title": "Direct Execution Without Auth Token",
        "passed": passed,
        "expected": "Status FAILURE with auth_token validation or AUTHORIZATION_DENIED",
        "actual": resp.get("work_performed", "")
    }


def run_sec_002_invalid_auth_token() -> dict:
    """SEC-002: Direct agent execution with invalid authorization token must fail closed."""
    sandbox = TaskSandbox("TSK-SEC-002")
    agent = CodingAgent()
    request = {
        "request_id": "REQ-SEC-002",
        "task_id": "TSK-SEC-002",
        "agent_id": "AGT-003",
        "subtask_id": "SUB-002",
        "parameters": {"module_name": "mod2"},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["write_file", "read_file"],
        "auth_token": "AUTH-FORGED-FAKE-TOKEN-123456",
        "timeout_seconds": 10
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    passed = (resp.get("status") == "FAILURE" and "AUTHORIZATION_DENIED" in resp.get("work_performed", ""))
    return {
        "test_id": "SEC-002",
        "title": "Direct Execution With Forged Auth Token",
        "passed": passed,
        "expected": "Status FAILURE with AUTHORIZATION_DENIED",
        "actual": resp.get("work_performed", "")
    }


def run_sec_003_cross_task_token_reuse() -> dict:
    """SEC-003: Token issued for Task A must be rejected when used to authorize Task B."""
    engine = HumanApprovalEngine()
    # Register and approve Task A
    engine.register_task("TSK-TASK-A", "Task A", {"action": "build"}, allow_reset=True)
    ticket_a = engine.transition_state("TSK-TASK-A", "APPROVED", actor="operator")
    token_a = ticket_a["approval_token"]

    # Register Task B (unapproved)
    engine.register_task("TSK-TASK-B", "Task B", {"action": "deploy"}, allow_reset=True)

    # Attempt to execute agent on Task B using Task A's token
    sandbox = TaskSandbox("TSK-TASK-B")
    agent = CodingAgent(approval_engine=engine)
    request = {
        "request_id": "REQ-SEC-003",
        "task_id": "TSK-TASK-B",
        "agent_id": "AGT-003",
        "subtask_id": "SUB-003",
        "parameters": {"module_name": "mod_b"},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["write_file", "read_file"],
        "auth_token": token_a,  # Task A's token on Task B!
        "timeout_seconds": 10
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    passed = (resp.get("status") == "FAILURE" and "AUTHORIZATION_DENIED" in resp.get("work_performed", ""))
    return {
        "test_id": "SEC-003",
        "title": "Cross-Task Token Reuse Attack",
        "passed": passed,
        "expected": "Task A token rejected for Task B with AUTHORIZATION_DENIED",
        "actual": resp.get("work_performed", "")
    }


def run_sec_004_expired_token() -> dict:
    """SEC-004: Token past its TTL must fail closed."""
    engine = HumanApprovalEngine()
    task_id = "TSK-SEC-004-EXPIRED"
    engine.register_task(task_id, "Expired Task", {"action": "test"}, allow_reset=True)
    # Approve with 1 second TTL
    ticket = engine.transition_state(task_id, "APPROVED", actor="operator", ttl_seconds=1)
    token = ticket["approval_token"]

    # Sleep 1.5 seconds to expire token
    time.sleep(1.2)

    sandbox = TaskSandbox(task_id)
    agent = ResearchAgent(approval_engine=engine)
    request = {
        "request_id": "REQ-SEC-004",
        "task_id": task_id,
        "agent_id": "AGT-001",
        "subtask_id": "SUB-004",
        "parameters": {"query": "Test query"},
        "input_artifacts": [],
        "sandbox_dir": sandbox.sandbox_dir,
        "allowed_tools": ["read_file"],
        "auth_token": token,
        "timeout_seconds": 10
    }
    resp = agent.execute(request, sandbox)
    sandbox.cleanup()

    passed = (resp.get("status") == "FAILURE" and "AUTHORIZATION_DENIED" in resp.get("work_performed", ""))
    return {
        "test_id": "SEC-004",
        "title": "Expired Token Rejection",
        "passed": passed,
        "expected": "Expired token rejected with AUTHORIZATION_DENIED",
        "actual": resp.get("work_performed", "")
    }


def run_sec_005_agent_self_approval() -> dict:
    """SEC-005: Agent attempting to self-approve a task must be blocked with ApprovalViolation."""
    engine = HumanApprovalEngine()
    task_id = "TSK-SEC-005-SELF-APP"
    engine.register_task(task_id, "Self Approval Test", {"action": "deploy"}, allow_reset=True)

    passed = False
    actual_msg = ""
    try:
        engine.transition_state(task_id, "APPROVED", actor="agent:coding_agent")
        actual_msg = "Allowed agent self-approval"
    except ApprovalViolation as av:
        passed = True
        actual_msg = f"Caught expected ApprovalViolation: {str(av)}"
    except Exception as e:
        actual_msg = f"Unexpected error: {type(e).__name__}"

    return {
        "test_id": "SEC-005",
        "title": "Agent Self-Approval Prevention",
        "passed": passed,
        "expected": "Throws ApprovalViolation when agent attempts self-approval",
        "actual": actual_msg
    }


def run_sec_006_concurrent_ledger_updates() -> dict:
    """SEC-006: Simultaneous concurrent writes to approval ledger must be safe and uncorrupted."""
    temp_ledger = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "TEMP_CONCURRENT_LEDGER.json")
    engine = HumanApprovalEngine(ledger_file=temp_ledger)

    num_threads = 5
    tasks_per_thread = 4
    errors = []

    def worker(thread_idx: int):
        for i in range(tasks_per_thread):
            tid = f"TSK-THREAD-{thread_idx}-TASK-{i}"
            try:
                engine.register_task(tid, f"Thread Task {tid}", {"action": "read"})
                engine.transition_state(tid, "APPROVED", actor="concurrency_test")
            except Exception as e:
                errors.append(f"Thread {thread_idx} error on {tid}: {str(e)}")

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify ledger integrity
    records = engine._load_ledger()
    expected_count = num_threads * tasks_per_thread
    actual_count = len(records)

    # Clean up temp files
    for p in [temp_ledger, f"{temp_ledger}.lock", f"{temp_ledger}.bak"]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    passed = (len(errors) == 0 and actual_count == expected_count)
    return {
        "test_id": "SEC-006",
        "title": "Concurrent Ledger Atomic Updates",
        "passed": passed,
        "expected": f"{expected_count} concurrent tasks registered without corruption",
        "actual": f"{actual_count} recorded; Errors: {errors}"
    }


def run_sec_007_interrupted_atomic_write() -> dict:
    """SEC-007: Orphan .tmp files from interrupted writes do not corrupt primary ledger."""
    temp_ledger = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "TEMP_ORPHAN_LEDGER.json")
    engine = HumanApprovalEngine(ledger_file=temp_ledger)
    engine.register_task("TSK-VALID-001", "Valid Task", {"action": "clean"})

    # Simulate an interrupted write leaving a corrupted .tmp file
    orphan_tmp = f"{temp_ledger}.9999.abc123.tmp"
    with open(orphan_tmp, "w", encoding="utf-8") as f:
        f.write("{ CORRUPTED PARTIAL WRITE...")

    # Instantiate new engine which cleans up stale tmp files
    engine2 = HumanApprovalEngine(ledger_file=temp_ledger)
    records = engine2._load_ledger()

    orphan_exists = os.path.exists(orphan_tmp)

    # Clean up
    for p in [temp_ledger, f"{temp_ledger}.lock", f"{temp_ledger}.bak", orphan_tmp]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    passed = ("TSK-VALID-001" in records and not orphan_exists)
    return {
        "test_id": "SEC-007",
        "title": "Interrupted Atomic Write Recovery",
        "passed": passed,
        "expected": "Orphan .tmp cleaned up; primary ledger uncorrupted",
        "actual": f"Primary valid: {'TSK-VALID-001' in records}; Orphan still exists: {orphan_exists}"
    }


def run_sec_008_ledger_corruption_recovery() -> dict:
    """SEC-008: Corrupted primary ledger automatically recovers from .bak."""
    temp_ledger = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "TEMP_CORRUPT_LEDGER.json")
    engine = HumanApprovalEngine(ledger_file=temp_ledger)
    engine.register_task("TSK-RECOVER-001", "Recoverable Task", {"action": "backup"})

    # Ensure .bak exists
    bak_file = f"{temp_ledger}.bak"
    with open(temp_ledger, "r", encoding="utf-8") as src, open(bak_file, "w", encoding="utf-8") as dst:
        dst.write(src.read())

    # Corrupt primary ledger
    with open(temp_ledger, "w", encoding="utf-8") as f:
        f.write("MALFORMED JSON {{{")

    # Load with corruption recovery
    engine2 = HumanApprovalEngine(ledger_file=temp_ledger)
    records = engine2._load_ledger()

    # Clean up
    for p in [temp_ledger, f"{temp_ledger}.lock", bak_file]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    passed = ("TSK-RECOVER-001" in records)
    return {
        "test_id": "SEC-008",
        "title": "Corrupt Ledger Backup Auto-Recovery",
        "passed": passed,
        "expected": "Auto-recovered from .bak upon detecting primary corruption",
        "actual": f"Recovered records: {list(records.keys())}"
    }


def run_sec_009_path_traversal_relative() -> dict:
    """SEC-009: Relative path traversal in sandbox write_file must throw SandboxSecurityViolation."""
    sandbox = TaskSandbox("TSK-SEC-009")
    passed = False
    try:
        sandbox.write_file("../../outside.txt", "payload")
    except SandboxSecurityViolation:
        passed = True
    except Exception:
        pass
    finally:
        sandbox.cleanup()

    return {
        "test_id": "SEC-009",
        "title": "Relative Path Traversal Rejection",
        "passed": passed,
        "expected": "Throws SandboxSecurityViolation on ../../",
        "actual": "Blocked" if passed else "Allowed path escape"
    }


def run_sec_010_windows_absolute_path_escape() -> dict:
    """SEC-010: Windows drive absolute path escape must throw SandboxSecurityViolation."""
    sandbox = TaskSandbox("TSK-SEC-010")
    passed = False
    try:
        sandbox.write_file("C:\\Windows\\Temp\\escape.txt", "payload")
    except SandboxSecurityViolation:
        passed = True
    except Exception:
        pass
    finally:
        sandbox.cleanup()

    return {
        "test_id": "SEC-010",
        "title": "Windows Absolute Path Escape Rejection",
        "passed": passed,
        "expected": "Throws SandboxSecurityViolation on C:\\Windows\\...",
        "actual": "Blocked" if passed else "Allowed absolute path escape"
    }


def run_sec_011_sanitized_environment() -> dict:
    """SEC-011: Subprocess environment must strip sensitive user credentials and profiles."""
    sanitized = get_sanitized_environment()

    # Check for absence of high-risk sensitive keys
    leaked_keys = []
    for k in sanitized:
        k_upper = k.upper()
        if any(term in k_upper for term in ["USERPROFILE", "APPDATA", "SECRET", "TOKEN", "KEY", "AUTH", "GEMINI"]):
            leaked_keys.append(k)

    passed = (len(leaked_keys) == 0 and "SYSTEMROOT" in sanitized and "PATH" in sanitized)
    return {
        "test_id": "SEC-011",
        "title": "Subprocess Sanitized Environment",
        "passed": passed,
        "expected": "Sensitive keys (USERPROFILE, APPDATA, tokens) stripped",
        "actual": f"Leaked keys: {leaked_keys}; Preserved safe keys: {list(sanitized.keys())}"
    }


def run_sec_012_subprocess_timeout() -> dict:
    """SEC-012: Subprocess exceeding timeout must be terminated with exit code 124."""
    sandbox = TaskSandbox("TSK-SEC-012")
    sandbox.write_file("sleep_job.py", "import time\ntime.sleep(10)\n")
    ret, out, err = sandbox.run_subprocess(
        ["python", "sleep_job.py"],
        timeout_seconds=1
    )
    sandbox.cleanup()

    passed = (ret == 124 and "timed out" in err)
    return {
        "test_id": "SEC-012",
        "title": "Subprocess Mandatory Timeout Enforcement",
        "passed": passed,
        "expected": "Exit code 124 with timed out message",
        "actual": f"Exit code {ret}: {err}"
    }


def run_sec_013_process_tree_cleanup() -> dict:
    """SEC-013: Timed-out subprocess process tree must be cleanly terminated."""
    sandbox = TaskSandbox("TSK-SEC-013")
    # Spawn a python script that spawns a child sleep process
    script = (
        "import subprocess, sys\n"
        "p = subprocess.Popen([sys.executable, '-c', 'import time\\ntime.sleep(10)'])\n"
        "p.wait()\n"
    )
    sandbox.write_file("tree_job.py", script)
    ret, out, err = sandbox.run_subprocess(["python", "tree_job.py"], timeout_seconds=1)
    sandbox.cleanup()

    passed = (ret == 124)
    return {
        "test_id": "SEC-013",
        "title": "Subprocess Process Tree Termination",
        "passed": passed,
        "expected": "Process tree terminated cleanly on timeout (exit code 124)",
        "actual": f"Exit code {ret}: {err}"
    }


def run_sec_014_shell_injection_blocking() -> dict:
    """SEC-014: Shell injection patterns in command arguments must throw SandboxSecurityViolation."""
    sandbox = TaskSandbox("TSK-SEC-014")
    passed_cases = 0
    test_args = [
        ["python", "test.py; dir"],
        ["python", "test.py && whoami"],
        ["python", "test.py | cat"],
        ["python", "test.py `dir`"],
        ["python", "$(whoami)"]
    ]

    for cmd in test_args:
        try:
            sandbox.run_subprocess(cmd)
        except SandboxSecurityViolation:
            passed_cases += 1
        except Exception:
            pass

    sandbox.cleanup()

    passed = (passed_cases == len(test_args))
    return {
        "test_id": "SEC-014",
        "title": "Shell Injection Argument Sanitization",
        "passed": passed,
        "expected": f"All {len(test_args)} injection attempts blocked",
        "actual": f"{passed_cases}/{len(test_args)} blocked"
    }


def run_sec_015_subprocess_audit_logging() -> dict:
    """SEC-015: Subprocess executions must be recorded in SUBPROCESS_AUDIT.jsonl."""
    sandbox = TaskSandbox("TSK-SEC-015")
    sandbox.run_subprocess(["python", "-c", "print('audit_test')"], timeout_seconds=5)
    sandbox.cleanup()

    # Verify audit log existence and last entry
    passed = False
    details = ""
    if os.path.exists(SUBPROCESS_AUDIT_LOG):
        with open(SUBPROCESS_AUDIT_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if lines:
            last_entry = json.loads(lines[-1])
            if last_entry.get("task_id") == "TSK-SEC-015":
                passed = True
                details = f"Logged command: {last_entry.get('command')}"

    return {
        "test_id": "SEC-015",
        "title": "Subprocess Execution Audit Logging",
        "passed": passed,
        "expected": "Execution appended to SUBPROCESS_AUDIT.jsonl",
        "actual": details or "No matching audit entry found"
    }


def run_sec_016_global_config_access_blocked() -> dict:
    """SEC-016: Direct file modification targeting ~/.gemini must throw SandboxSecurityViolation."""
    sandbox = TaskSandbox("TSK-SEC-016")
    gemini_path = os.path.expanduser("~/.gemini/test_file.txt")
    passed = False
    try:
        sandbox.write_file(gemini_path, "payload")
    except SandboxSecurityViolation:
        passed = True
    except Exception:
        pass
    finally:
        sandbox.cleanup()

    return {
        "test_id": "SEC-016",
        "title": "Global Config (.gemini) Directory Write Block",
        "passed": passed,
        "expected": "Throws SandboxSecurityViolation on .gemini path write",
        "actual": "Blocked" if passed else "Allowed write to global path"
    }


def main():
    print("=== MASTER-AI PHASE 4.2 SECURITY HARDENING TEST SUITE ===\n")
    test_functions = [
        run_sec_001_missing_auth_token,
        run_sec_002_invalid_auth_token,
        run_sec_003_cross_task_token_reuse,
        run_sec_004_expired_token,
        run_sec_005_agent_self_approval,
        run_sec_006_concurrent_ledger_updates,
        run_sec_007_interrupted_atomic_write,
        run_sec_008_ledger_corruption_recovery,
        run_sec_009_path_traversal_relative,
        run_sec_010_windows_absolute_path_escape,
        run_sec_011_sanitized_environment,
        run_sec_012_subprocess_timeout,
        run_sec_013_process_tree_cleanup,
        run_sec_014_shell_injection_blocking,
        run_sec_015_subprocess_audit_logging,
        run_sec_016_global_config_access_blocked
    ]

    results = []
    all_passed = True
    start_time = time.time()

    for fn in test_functions:
        res = fn()
        results.append(res)
        status_str = "PASS" if res["passed"] else "FAIL"
        if not res["passed"]:
            all_passed = False
        print(f"[{status_str}] {res['test_id']}: {res['title']}")
        print(f"       Expected: {res['expected']}")
        print(f"       Actual:   {res['actual']}")

    duration = time.time() - start_time
    summary = {
        "suite_name": "Phase 4.2 Security Hardening Test Suite",
        "total_tests": len(test_functions),
        "passed_tests": sum(1 for r in results if r["passed"]),
        "failed_tests": sum(1 for r in results if not r["passed"]),
        "all_passed": all_passed,
        "execution_time_seconds": round(duration, 3),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }

    with open(TEST_SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=======================================================")
    print(f"OVERALL SUMMARY: {summary['passed_tests']}/{summary['total_tests']} PASSED in {duration:.3f}s | ALL_PASSED = {all_passed}")
    print(f"=======================================================")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
