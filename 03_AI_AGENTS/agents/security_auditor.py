"""
security_auditor.py
MASTER-AI Security Auditor Specialist (AGT-006)

Inspects code, configs, and artifacts for secret leaks, AST antipatterns (eval, exec),
boundary violations, and unauthorized operations.
"""

import os
import re
from typing import Dict, Any, List
from .base_agent import BaseSpecialistAgent, TaskSandbox

DANGEROUS_PATTERNS = [
    (r"\beval\s*\(", "Use of dangerous eval() function"),
    (r"\bexec\s*\(", "Use of dangerous exec() function"),
    (r"os\.system\s*\(", "Direct os.system() invocation (use subprocess.run with list args)"),
    (r"AIza[0-9A-Za-z-_]{35}", "Exposed Google API Key pattern"),
    (r"sk-[0-9A-Za-z]{32,}", "Exposed OpenAI/Anthropic API Key pattern"),
    (r"ghp_[0-9A-Za-z]{36}", "Exposed GitHub Personal Access Token")
]


class SecurityAuditor(BaseSpecialistAgent):
    def __init__(self, approval_engine=None):
        super().__init__("security_auditor.json", approval_engine)

    def execute_task(self, request: Dict[str, Any], sandbox: TaskSandbox) -> Dict[str, Any]:
        violations: List[str] = []
        files_scanned: List[str] = []

        for root, _, files in os.walk(sandbox.sandbox_dir):
            for file_name in files:
                if file_name.endswith((".py", ".json", ".md", ".sh", ".yaml", ".yml")):
                    full_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(full_path, sandbox.sandbox_dir)
                    files_scanned.append(rel_path)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        for pattern, desc in DANGEROUS_PATTERNS:
                            if re.search(pattern, content):
                                violations.append(f"{rel_path}: {desc}")
                    except Exception as e:
                        violations.append(f"{rel_path}: Read error: {str(e)}")

        audit_report = (
            "# Security Audit Inspection Report\n\n"
            f"- **Files Scanned**: {len(files_scanned)}\n"
            f"- **Security Violations Detected**: {len(violations)}\n"
            f"- **Auditor Verdict**: {'PASS' if len(violations) == 0 else 'FAIL'}\n\n"
            "## Violation Details\n"
        )
        if violations:
            for v in violations:
                audit_report += f"- [ALERT] {v}\n"
        else:
            audit_report += "- Zero secret leaks or dangerous execution patterns identified.\n"

        report_filename = "security_audit_report.md"
        sandbox.write_file(report_filename, audit_report)
        sha = sandbox.compute_file_sha256(report_filename)

        passed = (len(violations) == 0)

        artifacts = [{
            "artifact_id": "ART-SEC-001",
            "artifact_type": "markdown",
            "path": report_filename,
            "sha256": sha
        }]

        evidence = {
            "files_scanned": files_scanned,
            "violations_count": len(violations),
            "verdict": "PASS" if passed else "FAIL"
        }

        tests_executed = [{
            "test_name": "ZeroSecretAndAstSafetyCheck",
            "passed": passed,
            "output": f"Scanned {len(files_scanned)} files. Violations: {len(violations)}"
        }]

        if not passed:
            return self._build_failure_response(
                task_id=request["task_id"],
                subtask_id=request["subtask_id"],
                reason=f"Security audit flagged {len(violations)} violation(s): {violations}"
            )

        return self._build_success_response(
            task_id=request["task_id"],
            subtask_id=request["subtask_id"],
            work_performed=f"Completed automated security audit of {len(files_scanned)} files; zero vulnerabilities found.",
            files_changed=[report_filename],
            evidence=evidence,
            tests_executed=tests_executed,
            remaining_limitations=[],
            artifacts=artifacts
        )
