"""
test_execution_boundary.py
MASTER-AI Phase 4.3 Secure Execution Boundary & Network Isolation Test Suite

Validates all 24 security boundary controls:
- Filesystem boundaries (absolute, traversal, UNC, junction write, device names, ADS, null bytes)
- Network isolation (raw socket blocking, urllib proxy poisoning, loopback allowance, git remote blocking)
- Git restrictions (push, clone, destructive reset, branch deletion, global config, safe local git)
- Subprocess security (binary resolution, CWD hijacking prevention, carets, trailing backslashes)
- Trust level enforcement (Level 0-4 invariants, agent self-escalation prevention)
"""

import os
import sys
import time
import shutil
import subprocess
import tempfile
from typing import Dict, Any, List

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import importlib
sandbox_mod = importlib.import_module("03_AI_AGENTS.sandbox.sandbox_runner")
TaskSandbox = sandbox_mod.TaskSandbox
SandboxSecurityViolation = sandbox_mod.SandboxSecurityViolation

approval_mod = importlib.import_module("03_AI_AGENTS.approval_engine.approval_engine")
HumanApprovalEngine = approval_mod.HumanApprovalEngine
ApprovalViolation = approval_mod.ApprovalViolation

trust_mod = importlib.import_module("03_AI_AGENTS.approval_engine.trust_levels")
TrustLevel = trust_mod.TrustLevel
TrustEscalationViolation = trust_mod.TrustEscalationViolation
is_operation_permitted = trust_mod.is_operation_permitted
validate_trust_transition = trust_mod.validate_trust_transition

results = []

def record(test_id: str, name: str, passed: bool, expected: str, actual: str):
    results.append({
        "id": test_id,
        "name": name,
        "passed": passed,
        "expected": expected,
        "actual": actual
    })
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {test_id}: {name}")
    print(f"       Expected: {expected}")
    print(f"       Actual:   {actual}")


print("=== MASTER-AI PHASE 4.3 SECURE EXECUTION BOUNDARY TEST SUITE ===\n")

# -------------------------------------------------------------
# 1. FILESYSTEM BOUNDARY TESTS
# -------------------------------------------------------------

# BOUND-001: Absolute Windows Path Outside Sandbox
try:
    s = TaskSandbox("BOUND-001")
    s.write_file("C:\\Windows\\System32\\test.txt", "evil")
    record("BOUND-001", "Absolute Windows Path Outside Sandbox", False, "SandboxSecurityViolation", "Write succeeded")
except SandboxSecurityViolation:
    record("BOUND-001", "Absolute Windows Path Outside Sandbox", True, "SandboxSecurityViolation", "Blocked path escape")
finally:
    s.cleanup()

# BOUND-002: Relative Traversal Escape
try:
    s = TaskSandbox("BOUND-002")
    s.write_file("../../00_CORE_SYSTEM/pwn.txt", "evil")
    record("BOUND-002", "Relative Traversal Escape", False, "SandboxSecurityViolation", "Write succeeded")
except SandboxSecurityViolation:
    record("BOUND-002", "Relative Traversal Escape", True, "SandboxSecurityViolation", "Blocked traversal")
finally:
    s.cleanup()

# BOUND-003: UNC Path Rejection
try:
    s = TaskSandbox("BOUND-003")
    is_safe = s.is_safe_path("\\\\localhost\\c$\\Windows\\evil.txt")
    record("BOUND-003", "UNC Path Rejection", not is_safe, "is_safe_path returns False", f"is_safe_path = {is_safe}")
finally:
    s.cleanup()

# BOUND-004: Directory Junction Write-Escape Blocked (New File)
try:
    s = TaskSandbox("BOUND-004")
    junc_path = os.path.join(s.sandbox_dir, "junc_link")
    # Create directory junction pointing outside
    subprocess.run(["cmd", "/c", "mklink", "/J", junc_path, WORKSPACE_ROOT], capture_output=True, check=False)
    
    # Try writing a non-existent file through the junction
    caught = False
    try:
        s.write_file("junc_link/evil_escape.txt", "payload")
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-004", "Directory Junction Write-Escape Blocked", caught, "SandboxSecurityViolation on junction write", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-005: DOS Device Name Rejection
try:
    s = TaskSandbox("BOUND-005")
    caught = False
    try:
        s.write_file("CON.txt", "data")
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-005", "DOS Device Name Rejection", caught, "SandboxSecurityViolation on CON.txt", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-006: Alternate Data Stream (ADS) Rejection
try:
    s = TaskSandbox("BOUND-006")
    caught = False
    try:
        s.write_file("file.txt:hidden_stream", "payload")
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-006", "Alternate Data Stream (ADS) Rejection", caught, "SandboxSecurityViolation on ADS", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-007: Null Byte Path Rejection
try:
    s = TaskSandbox("BOUND-007")
    caught = False
    try:
        s.write_file("file.txt\0.py", "payload")
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-007", "Null Byte Path Rejection", caught, "SandboxSecurityViolation on null byte", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-008: Host Profile Root & .gemini Write Block
try:
    s = TaskSandbox("BOUND-008")
    gemini_path = os.path.expanduser("~/.gemini/test.txt")
    caught = False
    try:
        s.write_file(gemini_path, "payload")
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-008", "Host Profile Root & .gemini Write Block", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()


# -------------------------------------------------------------
# 2. NETWORK ISOLATION TESTS
# -------------------------------------------------------------

# BOUND-009: Python Raw Socket Connection Blocked
try:
    s = TaskSandbox("BOUND-009")
    s.write_file("test_raw_socket.py", """import socket
try:
    s = socket.create_connection(('1.1.1.1', 53), timeout=2)
    print('CONNECTED')
except PermissionError as e:
    print('PERMISSION_DENIED:', e)
except Exception as e:
    print('FAILED:', type(e).__name__, e)
""")
    code, stdout, stderr = s.run_subprocess(["python", "test_raw_socket.py"], network_allowed=False)
    blocked = "PERMISSION_DENIED" in stdout or "PermissionError" in stdout or code != 0
    record("BOUND-009", "Python Raw Socket Connection Blocked", blocked, "PermissionError / Network Block", stdout.strip())
finally:
    s.cleanup()

# BOUND-010: Python urllib Connection Fails / Proxied to Dead Port
try:
    s = TaskSandbox("BOUND-010")
    s.write_file("test_urllib.py", """import urllib.request
try:
    with urllib.request.urlopen('http://www.google.com', timeout=2) as resp:
        print('CONNECTED')
except Exception as e:
    print('URLLIB_BLOCKED:', type(e).__name__)
""")
    code, stdout, stderr = s.run_subprocess(["python", "test_urllib.py"], network_allowed=False)
    blocked = "URLLIB_BLOCKED" in stdout or "URLError" in stdout
    record("BOUND-010", "Python urllib Connection Fails via Proxy", blocked, "URLLIB_BLOCKED", stdout.strip())
finally:
    s.cleanup()

# BOUND-011: Local Loopback Allowed Under Offline Sandbox
try:
    s = TaskSandbox("BOUND-011")
    s.write_file("test_loopback.py", """import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 0))
port = s.getsockname()[1]
s.listen(1)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', port))
print('LOOPBACK_OK')
client.close()
s.close()
""")
    code, stdout, stderr = s.run_subprocess(["python", "test_loopback.py"], network_allowed=False)
    allowed = "LOOPBACK_OK" in stdout and code == 0
    record("BOUND-011", "Local Loopback Allowed Under Offline Sandbox", allowed, "LOOPBACK_OK", stdout.strip())
finally:
    s.cleanup()

# BOUND-012: Git Remote Operations Blocked Without Network Approval
try:
    s = TaskSandbox("BOUND-012")
    caught = False
    try:
        s.run_subprocess(["git", "ls-remote", "https://github.com/octocat/Hello-World.git"], network_allowed=False)
    except SandboxSecurityViolation as e:
        caught = True
        err_msg = str(e)
    record("BOUND-012", "Git Remote Operations Blocked Without Approval", caught, "SandboxSecurityViolation", err_msg if caught else "Executed")
finally:
    s.cleanup()

# BOUND-013: Network Allowed Flag Respected for Level 3 Approved Tasks
try:
    s = TaskSandbox("BOUND-013")
    s.write_file("test_net_flag.py", """import os
http_proxy = os.environ.get('HTTP_PROXY', '')
print('PROXY_PRESENT:', bool('127.0.0.1:9' in http_proxy))
""")
    code, stdout, stderr = s.run_subprocess(["python", "test_net_flag.py"], network_allowed=True)
    no_dead_proxy = "PROXY_PRESENT: False" in stdout
    record("BOUND-013", "Network Allowed Flag Disables Dead Proxy", no_dead_proxy, "PROXY_PRESENT: False", stdout.strip())
finally:
    s.cleanup()


# -------------------------------------------------------------
# 3. GIT COMMAND RESTRICTIONS
# -------------------------------------------------------------

# BOUND-014: Git Push Blocked
try:
    s = TaskSandbox("BOUND-014")
    caught = False
    try:
        s.run_subprocess(["git", "push", "origin", "master"])
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-014", "Git Push Blocked", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-015: Git Destructive Reset (--hard) Blocked
try:
    s = TaskSandbox("BOUND-015")
    caught = False
    try:
        s.run_subprocess(["git", "reset", "--hard", "HEAD~1"])
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-015", "Git Destructive Reset (--hard) Blocked", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-016: Git Branch Deletion (-D) Blocked
try:
    s = TaskSandbox("BOUND-016")
    caught = False
    try:
        s.run_subprocess(["git", "branch", "-D", "master"])
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-016", "Git Branch Deletion (-D) Blocked", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-017: Git Global Config Change Blocked
try:
    s = TaskSandbox("BOUND-017")
    caught = False
    try:
        s.run_subprocess(["git", "config", "--global", "user.name", "Attacker"])
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-017", "Git Global Config Change Blocked", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-018: Git Safe Local Commands Allowed
try:
    s = TaskSandbox("BOUND-018")
    code, stdout, stderr = s.run_subprocess(["git", "status"])
    passed = code == 0 or "On branch" in stdout or "fatal: not a git repository" in stderr
    record("BOUND-018", "Git Safe Local Commands Allowed", passed, "Executed without SecurityViolation", f"Exit: {code}")
finally:
    s.cleanup()


# -------------------------------------------------------------
# 4. SUBPROCESS SECURITY & PARSING EDGE CASES
# -------------------------------------------------------------

# BOUND-019: CWD Binary Hijacking Blocked
try:
    s = TaskSandbox("BOUND-019")
    # Place a fake binary in sandbox_dir
    fake_py = os.path.join(s.sandbox_dir, "python.exe")
    with open(fake_py, "w") as f:
        f.write("fake binary")

    s.write_file("check_sys_exec.py", "import sys\nprint(sys.executable)\n")
    # run_subprocess should resolve to sys.executable outside sandbox, NEVER fake_py
    code, stdout, stderr = s.run_subprocess(["python", "check_sys_exec.py"])
    used_system_python = sys.executable.lower() in stdout.lower()
    record("BOUND-019", "CWD Binary Hijacking Blocked", used_system_python, f"Used sys.executable ({sys.executable})", stdout.strip())
finally:
    s.cleanup()

# BOUND-020: Windows Command Argument Caret (^) Rejected
try:
    s = TaskSandbox("BOUND-020")
    caught = False
    try:
        s.run_subprocess(["python", "arg^test.py"])
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-020", "Windows Command Argument Caret (^) Rejected", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()

# BOUND-021: Windows Unescaped Trailing Backslash Rejected
try:
    s = TaskSandbox("BOUND-021")
    caught = False
    try:
        s.run_subprocess(["python", "some_script.py", "trailing\\"])
    except SandboxSecurityViolation:
        caught = True
    record("BOUND-021", "Windows Unescaped Trailing Backslash Rejected", caught, "SandboxSecurityViolation", f"Caught: {caught}")
finally:
    s.cleanup()


# -------------------------------------------------------------
# 5. TRUST LEVEL ENFORCEMENT & SELF-ESCALATION PREVENTION
# -------------------------------------------------------------

# BOUND-022: Trust Level Operation Permissions Check
l0_write_ok = is_operation_permitted(TrustLevel.LEVEL_0_READ_ONLY, "write_sandbox_files")
l1_write_ok = is_operation_permitted(TrustLevel.LEVEL_1_WORKSPACE_FS, "write_sandbox_files")
l1_exec_ok = is_operation_permitted(TrustLevel.LEVEL_1_WORKSPACE_FS, "execute_sandboxed_python")
l2_exec_ok = is_operation_permitted(TrustLevel.LEVEL_2_LOCAL_EXECUTION, "execute_sandboxed_python")
l2_net_ok = is_operation_permitted(TrustLevel.LEVEL_2_LOCAL_EXECUTION, "execute_approved_network_request")
l3_net_ok = is_operation_permitted(TrustLevel.LEVEL_3_NETWORK_APPROVED, "execute_approved_network_request")

perm_matrix_ok = (not l0_write_ok) and l1_write_ok and (not l1_exec_ok) and l2_exec_ok and (not l2_net_ok) and l3_net_ok
record("BOUND-022", "Trust Level Operation Permissions Check", perm_matrix_ok, "Level 0 < Level 1 < Level 2 < Level 3 enforced", f"Matrix Valid: {perm_matrix_ok}")

# BOUND-023: Agent Self-Escalation Attempt Blocked
try:
    validate_trust_transition(
        current_level=TrustLevel.LEVEL_2_LOCAL_EXECUTION,
        requested_level=TrustLevel.LEVEL_3_NETWORK_APPROVED,
        actor="agent:coding_agent"
    )
    record("BOUND-023", "Agent Self-Escalation Attempt Blocked", False, "TrustEscalationViolation", "Escalation allowed")
except TrustEscalationViolation:
    record("BOUND-023", "Agent Self-Escalation Attempt Blocked", True, "TrustEscalationViolation", "Caught self-escalation attempt")

# BOUND-024: Escalation to Level 3/4 Requires Human Approval in ApprovalEngine
try:
    engine = HumanApprovalEngine()
    engine.register_task("TSK-BOUND-024", "Network Task", {"trust_level": 2}, allow_reset=True)
    caught = False
    try:
        # Try elevating without human approval
        engine.elevate_trust_level("TSK-BOUND-024", requested_level=3, actor="human")
    except ApprovalViolation:
        caught = True
    record("BOUND-024", "Escalation to Level 3 Requires Human Approval", caught, "ApprovalViolation on non-approved task", f"Caught: {caught}")
except Exception as e:
    record("BOUND-024", "Escalation to Level 3 Requires Human Approval", False, "ApprovalViolation", f"Exception: {e}")


# -------------------------------------------------------------
# SUMMARY & ARTIFACT GENERATION
# -------------------------------------------------------------
total_tests = len(results)
passed_tests = sum(1 for r in results if r["passed"])
all_passed = (total_tests == passed_tests)

print("\n=======================================================")
print(f"OVERALL SUMMARY: {passed_tests}/{total_tests} PASSED | ALL_PASSED = {all_passed}")
print("=======================================================")

summary_file = os.path.join(os.path.dirname(__file__), "execution_boundary_test_summary.json")
with open(summary_file, "w", encoding="utf-8") as f:
    import json
    json.dump({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": total_tests,
        "passed": passed_tests,
        "all_passed": all_passed,
        "results": results
    }, f, indent=2)

if not all_passed:
    sys.exit(1)
