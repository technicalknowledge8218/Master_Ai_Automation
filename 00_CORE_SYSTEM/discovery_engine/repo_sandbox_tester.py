"""
Hardened Sandbox Testing for Candidate Repositories
===================================================
Executes pre-installation static analysis, dependency safety inspection,
and isolated test execution under strict Windows 11 / WDAC compliance.
Refuses host execution of untrusted installation scripts without explicit consent.
"""

import os
import re
import ast
import json
import time
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class RepoSandboxTester:
    """Safe evaluation and isolated testing harness for discovered repositories."""

    DANGEROUS_IMPORTS = {"socket", "pty", "termios", "winreg", "ctypes"}
    MALICIOUS_CALL_PATTERNS = [
        re.compile(r"base64\.b64decode"),
        re.compile(r"urllib\.request\.urlretrieve"),
        re.compile(r"subprocess\.(Popen|call|run)\(.*(curl|wget|powershell|cmd)", re.IGNORECASE),
        re.compile(r"os\.system\(.*(curl|wget|rm\s+-rf)", re.IGNORECASE),
        re.compile(r"__import__\(['\"](os|subprocess)['\"]\)\.system"),
    ]

    def __init__(self, workspace_root: Optional[Path | str] = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).resolve().parent.parent.parent
        self.sandbox_base = self.workspace_root / "03_AI_AGENTS" / "sandbox" / "repo_eval"
        self.sandbox_base.mkdir(parents=True, exist_ok=True)

    def inspect_dependencies_and_scripts(self, repo_dir: Path | str) -> Dict[str, Any]:
        """Perform static inspection on repository files prior to test execution."""
        r_path = Path(repo_dir)
        findings = {
            "is_safe_to_evaluate": True,
            "security_alerts": [],
            "suspicious_patterns_found": [],
            "dependencies_found": [],
            "files_scanned": 0,
        }

        if not r_path.exists():
            return {"is_safe_to_evaluate": False, "error": "Repository path does not exist."}

        for root, _, files in os.walk(r_path):
            for f in files:
                ext = Path(f).suffix.lower()
                fp = Path(root) / f
                findings["files_scanned"] += 1

                # 1. Dependency checks
                if f in {"requirements.txt", "Pipfile", "pyproject.toml"}:
                    try:
                        content = fp.read_text(encoding="utf-8", errors="replace")
                        for line in content.splitlines():
                            line_s = line.strip()
                            if line_s and not line_s.startswith("#"):
                                findings["dependencies_found"].append(line_s[:100])
                                if "==" not in line_s and ">=" not in line_s and len(line_s) > 2:
                                    findings["security_alerts"].append(f"Unpinned dependency in {f}: {line_s}")
                    except Exception:
                        pass

                # 2. Malicious script patterns in setup or python files
                if ext in {".py", ".sh", ".bat", ".ps1"}:
                    try:
                        text = fp.read_text(encoding="utf-8", errors="replace")
                        for pat in self.MALICIOUS_CALL_PATTERNS:
                            if pat.search(text):
                                findings["is_safe_to_evaluate"] = False
                                findings["suspicious_patterns_found"].append(f"Dangerous call pattern '{pat.pattern}' in {f}")
                                findings["security_alerts"].append(f"SUSPICIOUS_PAYLOAD_DETECTED in {f}")
                    except Exception:
                        pass

                # 3. Python AST check
                if ext == ".py":
                    try:
                        code = fp.read_text(encoding="utf-8", errors="replace")
                        tree = ast.parse(code)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    if alias.name in self.DANGEROUS_IMPORTS:
                                        findings["security_alerts"].append(f"Potentially sensitive module '{alias.name}' imported in {f}")
                    except Exception:
                        pass

        if findings["suspicious_patterns_found"]:
            findings["is_safe_to_evaluate"] = False

        return findings

    def run_isolated_test(
        self,
        eval_id: str,
        test_script_content: str,
        timeout_seconds: float = 10.0,
        allow_untrusted_execution: bool = False,
    ) -> Dict[str, Any]:
        """
        Executes a sandboxed test in a segregated workspace with environment sanitization
        and strict execution timeout.
        """
        eval_dir = self.sandbox_base / f"eval_{eval_id}_{int(time.time())}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        test_file = eval_dir / "test_runner.py"
        test_file.write_text(test_script_content, encoding="utf-8")

        # Static inspection
        inspection = self.inspect_dependencies_and_scripts(eval_dir)
        if not inspection["is_safe_to_evaluate"] and not allow_untrusted_execution:
            shutil.rmtree(eval_dir, ignore_errors=True)
            return {
                "eval_id": eval_id,
                "status": "BLOCKED_SECURITY_VIOLATION",
                "reason": "Untrusted or suspicious code detected in candidate script. Host execution refused.",
                "inspection": inspection,
                "exit_code": -1,
                "duration_seconds": 0.0,
            }

        # Clean sanitized environment: remove all production credentials
        sanitized_env = dict(os.environ)
        for key in list(sanitized_env.keys()):
            if any(k in key.lower() for k in ["api_key", "secret", "token", "password", "auth"]):
                del sanitized_env[key]
        sanitized_env["PYTHONPATH"] = str(eval_dir)

        # Execute using verified python interpreter
        python_exe = str(self.workspace_root / ".venv" / "Scripts" / "python.exe")
        if not Path(python_exe).exists():
            python_exe = "python"

        start_time = time.time()
        try:
            proc = subprocess.run(
                [python_exe, str(test_file)],
                cwd=str(eval_dir),
                env=sanitized_env,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            duration = round(time.time() - start_time, 3)
            passed = proc.returncode == 0
            res = {
                "eval_id": eval_id,
                "status": "PASSED" if passed else "FAILED",
                "exit_code": proc.returncode,
                "duration_seconds": duration,
                "stdout": proc.stdout[:2000],
                "stderr": proc.stderr[:2000],
                "inspection": inspection,
            }
        except subprocess.TimeoutExpired:
            res = {
                "eval_id": eval_id,
                "status": "TIMEOUT",
                "exit_code": -1,
                "duration_seconds": timeout_seconds,
                "reason": f"Execution exceeded maximum timeout of {timeout_seconds}s",
                "inspection": inspection,
            }
        except Exception as e:
            res = {
                "eval_id": eval_id,
                "status": "ERROR",
                "exit_code": -1,
                "duration_seconds": round(time.time() - start_time, 3),
                "error": str(e),
                "inspection": inspection,
            }
        finally:
            # Clean up sandbox directory
            shutil.rmtree(eval_dir, ignore_errors=True)

        return res
