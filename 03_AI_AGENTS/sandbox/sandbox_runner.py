"""
sandbox_runner.py
MASTER-AI Safe Execution Sandbox Manager (Hardened)

Manages isolated task workspaces, enforces command timeouts, path boundaries,
subprocess restrictions, environment sanitization, process-tree termination,
audit logging, and artifact SHA-256 hashing.
"""

import os
import sys
import shutil
import subprocess
import hashlib
import time
import json
import datetime
from typing import Dict, Any, List, Optional, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SANDBOX_TASKS_ROOT = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "sandbox", "tasks")
ROLLBACK_SCRIPT = os.path.join(WORKSPACE_ROOT, "22_PUBLISH_AND_DEPLOY", "scripts", "rollback.py")
GLOBAL_CONFIG_PATTERN = os.path.expanduser(os.path.join("~", ".gemini"))
SUBPROCESS_AUDIT_LOG = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "SUBPROCESS_AUDIT.jsonl")

ALLOWED_EXECUTABLES = {"python", "node", "git"}

# Permitted local Git commands; remote or destructive operations require Trust Level 3/4
ALLOWED_LOCAL_GIT_COMMANDS = {
    "status", "diff", "log", "show", "rev-parse",
    "init", "add", "commit", "checkout", "branch",
    "tag", "describe", "version", "config", "switch"
}
FORBIDDEN_REMOTE_GIT_COMMANDS = {
    "push", "fetch", "clone", "pull", "remote",
    "ls-remote", "submodule"
}
DESTRUCTIVE_GIT_FLAGS = {
    "--hard", "-fdx", "-f", "-d", "-D", "--force"
}

DOS_DEVICE_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
}

# Dangerous shell injection characters and command patterns
DISALLOWED_ARG_CHARS = [";", "&&", "||", "|", "&", "`", "$(", ">", "<", "\n", "\r", "\0"]
DISALLOWED_COMMAND_PATTERNS = [
    "powershell -enc",
    "powershell -encodedcommand",
    "rm -rf /",
    "rmdir /s /q c:\\",
    "format",
    "del /f /s /q c:\\",
    "shutdown",
    "curl http",
    "wget http",
    ".gemini"
]

SAFE_ENV_ALLOWLIST = {
    "SYSTEMROOT",
    "COMSPEC",
    "PATH",
    "PATHEXT",
    "TEMP",
    "TMP",
    "NUMBER_OF_PROCESSORS",
    "OS",
    "PROCESSOR_ARCHITECTURE"
}

SENSITIVE_VAR_PATTERNS = [
    "KEY", "TOKEN", "SECRET", "PASS", "AUTH", "GEMINI", "API", "CREDENTIAL"
]


class SandboxSecurityViolation(Exception):
    """Raised when an agent attempts an unauthorized or dangerous operation in the sandbox."""
    pass


def get_sanitized_environment(
    base_env: Optional[Dict[str, str]] = None,
    extra_env: Optional[Dict[str, str]] = None,
    allow_git: bool = True
) -> Dict[str, str]:
    """Builds a minimal, sanitized environment stripping credentials and user profile roots."""
    source_env = base_env or os.environ
    sanitized: Dict[str, str] = {}

    for k, v in source_env.items():
        k_upper = k.upper()
        # Keep only explicitly whitelisted safe environment variables
        if k_upper in SAFE_ENV_ALLOWLIST:
            # Strip sensitive patterns even in whitelisted names
            if not any(pattern in k_upper for pattern in SENSITIVE_VAR_PATTERNS):
                sanitized[k] = v

    # Filter PATH to retain only system and runtime directories (strip user script and roaming dirs)
    if "PATH" in sanitized:
        paths = sanitized["PATH"].split(os.pathsep)
        clean_paths = []
        allowed_terms = ["python", "nodejs", "node", "system32"]
        if allow_git:
            allowed_terms.append("git")
        for p in paths:
            p_lower = p.lower()
            if any(term in p_lower for term in allowed_terms):
                if not any(term in p_lower for term in ["appdata", "roaming", ".gemini"]):
                    clean_paths.append(p)
        sanitized["PATH"] = os.pathsep.join(clean_paths)

    # Force isolated temp directory
    sanitized["TEMP"] = os.path.join(SANDBOX_TASKS_ROOT, ".temp")
    sanitized["TMP"] = sanitized["TEMP"]
    os.makedirs(sanitized["TEMP"], exist_ok=True)

    if extra_env:
        for ek, ev in extra_env.items():
            ek_upper = ek.upper()
            if not any(p in ek_upper for p in SENSITIVE_VAR_PATTERNS):
                sanitized[ek] = ev

    return sanitized


class TaskSandbox:
    def __init__(self, task_id: str, seed_files: Optional[List[str]] = None):
        self.task_id = task_id
        safe_task_id = "".join(c for c in task_id if c.isalnum() or c in ("-", "_"))
        self.sandbox_dir = os.path.abspath(os.path.join(SANDBOX_TASKS_ROOT, safe_task_id))
        self.seed_files = seed_files or []
        self._initialize_sandbox()

    def _initialize_sandbox(self):
        """Creates an empty, isolated sandbox directory for the task."""
        if os.path.exists(self.sandbox_dir):
            shutil.rmtree(self.sandbox_dir, ignore_errors=True)
        os.makedirs(self.sandbox_dir, exist_ok=True)

        for rel_path in self.seed_files:
            src = os.path.join(WORKSPACE_ROOT, rel_path)
            dst = os.path.join(self.sandbox_dir, rel_path)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

    def is_safe_path(self, target_path: str) -> bool:
        """
        Verifies target path resides strictly inside sandbox_dir, is not a symlink/junction escape,
        does not target UNC shares, device names, or Alternate Data Streams, and never targets global config.
        """
        if not target_path or not isinstance(target_path, str):
            return False

        # 1. Null byte check
        if "\0" in target_path:
            return False

        # 2. Reject UNC paths (\\... or //...)
        norm_path = target_path.replace("/", "\\")
        if norm_path.startswith("\\\\"):
            return False

        # 3. Reject Alternate Data Streams (colon in path other than drive specifier like C:\)
        parts_after_drive = norm_path[2:] if (len(norm_path) >= 2 and norm_path[1] == ":") else norm_path
        if ":" in parts_after_drive:
            return False

        # 4. Reject DOS device names (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
        base_leaf = os.path.basename(norm_path).split(".")[0].upper()
        if base_leaf in DOS_DEVICE_NAMES:
            return False

        # 5. Normalize relative paths against sandbox_dir if not absolute
        if not os.path.isabs(target_path):
            target_path = os.path.join(self.sandbox_dir, target_path)

        abs_target = os.path.abspath(target_path)
        real_target = os.path.realpath(target_path)
        abs_sandbox = os.path.abspath(self.sandbox_dir)
        abs_global = os.path.abspath(GLOBAL_CONFIG_PATTERN)
        user_profile = os.path.abspath(os.path.expanduser("~"))

        # Check for global config (.gemini) or host profile root targeting
        try:
            if os.path.commonpath([abs_target, abs_global]) == abs_global:
                return False
            if os.path.commonpath([real_target, abs_global]) == abs_global:
                return False
            if abs_target == user_profile or real_target == user_profile:
                return False
        except ValueError:
            pass

        # Check path stays within sandbox (both abspath AND realpath)
        # CRITICAL: Always check realpath regardless of whether file exists yet to block junction/symlink write escapes.
        try:
            in_sandbox_abs = (os.path.commonpath([abs_target, abs_sandbox]) == abs_sandbox)
            in_sandbox_real = (os.path.commonpath([real_target, abs_sandbox]) == abs_sandbox)
            return in_sandbox_abs and in_sandbox_real
        except ValueError:
            return False

    def write_file(self, rel_path: str, content: str) -> str:
        """Writes a file inside the sandbox. Throws SandboxSecurityViolation if path escapes."""
        target_path = os.path.join(self.sandbox_dir, rel_path)
        if not self.is_safe_path(target_path):
            raise SandboxSecurityViolation(
                f"Path traversal detected: {rel_path} escapes sandbox {self.sandbox_dir}"
            )
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return target_path

    def read_file(self, rel_path: str) -> str:
        """Reads a file from within the sandbox."""
        target_path = os.path.join(self.sandbox_dir, rel_path)
        if not self.is_safe_path(target_path):
            raise SandboxSecurityViolation(
                f"Path traversal detected: {rel_path} escapes sandbox {self.sandbox_dir}"
            )
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"File not found in sandbox: {rel_path}")
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()

    def _validate_git_command(self, command_list: List[str], network_allowed: bool):
        """Enforces safe local-only Git operations, blocking remote and destructive actions."""
        if len(command_list) < 2:
            return

        subcmd = command_list[1].lower()
        if subcmd.startswith("-"):
            # Flags before subcommand, e.g. git -C ... or git --version
            if any(arg.lower() in ("--version", "-v") for arg in command_list):
                return
            # Find first non-flag argument
            for a in command_list[1:]:
                if not a.startswith("-"):
                    subcmd = a.lower()
                    break

        if subcmd in FORBIDDEN_REMOTE_GIT_COMMANDS and not network_allowed:
            raise SandboxSecurityViolation(
                f"Git remote operation '{subcmd}' is blocked. External network access is prohibited without Trust Level 3 approval."
            )

        if subcmd not in ALLOWED_LOCAL_GIT_COMMANDS and subcmd not in FORBIDDEN_REMOTE_GIT_COMMANDS:
            raise SandboxSecurityViolation(
                f"Git subcommand '{subcmd}' is not in allowed local git list: {ALLOWED_LOCAL_GIT_COMMANDS}"
            )

        # Destructive flags check
        for arg in command_list[1:]:
            arg_lower = arg.lower()
            if arg_lower in DESTRUCTIVE_GIT_FLAGS:
                raise SandboxSecurityViolation(
                    f"Destructive Git flag '{arg}' is strictly prohibited in sandbox."
                )

        # Global or system configuration modification check
        if subcmd == "config":
            for arg in command_list[2:]:
                if arg.lower() in ("--global", "--system"):
                    raise SandboxSecurityViolation(
                        f"Git configuration change '{arg}' outside local workspace is strictly prohibited."
                    )

    def run_subprocess(
        self,
        command_list: List[str],
        timeout_seconds: int = 15,
        env_vars: Optional[Dict[str, str]] = None,
        network_allowed: bool = False
    ) -> Tuple[int, str, str]:
        """
        Executes a strictly restricted, sanitized command inside the sandbox with absolute
        binary resolution, argument sanitization, process-tree termination, and offline network gating.
        """
        start_time = time.time()
        if not command_list:
            raise SandboxSecurityViolation("Empty command supplied.")

        raw_exec = os.path.basename(command_list[0]).lower()
        if raw_exec.endswith(".exe"):
            raw_exec = raw_exec[:-4]

        if raw_exec not in ALLOWED_EXECUTABLES:
            raise SandboxSecurityViolation(
                f"Executable '{raw_exec}' is not in allowed sandbox list: {ALLOWED_EXECUTABLES}"
            )

        # Node.js offline isolation policy: core Node.js runtimes do not enforce socket-level sandbox
        if raw_exec == "node" and not network_allowed:
            raise SandboxSecurityViolation(
                "Untrusted Node.js execution is disabled by default in offline sandbox because Node.js "
                "core runtimes do not enforce socket-level isolation without system firewall rules. "
                "Explicit Trust Level 3 human authorization is required to execute Node.js."
            )

        # 1. Absolute Executable Resolution (CWD binary hijacking prevention)
        if raw_exec == "python":
            resolved_exec = sys.executable
        elif raw_exec == "node":
            resolved_exec = shutil.which("node", path=os.environ.get("PATH"))
            if not resolved_exec:
                raise SandboxSecurityViolation("Node executable not found in system PATH.")
        elif raw_exec == "git":
            resolved_exec = shutil.which("git", path=os.environ.get("PATH"))
            if not resolved_exec:
                raise SandboxSecurityViolation("Git executable not found in system PATH.")
        else:
            resolved_exec = command_list[0]

        # Ensure resolved executable does not reside inside sandbox_dir (cannot execute binaries placed by agent in sandbox)
        abs_resolved = os.path.abspath(resolved_exec)
        abs_sandbox = os.path.abspath(self.sandbox_dir)
        try:
            if os.path.commonpath([abs_resolved, abs_sandbox]) == abs_sandbox:
                raise SandboxSecurityViolation(
                    f"CWD executable hijacking blocked: Cannot execute binaries residing inside sandbox: {resolved_exec}"
                )
        except ValueError:
            pass

        # 2. Argument validation & Windows edge case sanitization
        cmd_str = " ".join(command_list)
        for arg in command_list[1:]:
            for ch in DISALLOWED_ARG_CHARS:
                if ch in arg:
                    raise SandboxSecurityViolation(
                        f"Command argument '{arg}' contains prohibited shell control characters: '{ch}'"
                    )
            if "^" in arg:
                raise SandboxSecurityViolation(
                    f"Command argument '{arg}' contains prohibited Windows escape character '^'"
                )
            if arg.endswith("\\") and not arg.endswith("\\\\"):
                raise SandboxSecurityViolation(
                    f"Command argument '{arg}' has unescaped trailing backslash which corrupts Windows argument parsing."
                )

        for pattern in DISALLOWED_COMMAND_PATTERNS:
            if pattern.lower() in cmd_str.lower():
                raise SandboxSecurityViolation(
                    f"Command contains forbidden pattern '{pattern}': {cmd_str}"
                )

        # 3. Git-specific validation
        if raw_exec == "git":
            self._validate_git_command(command_list, network_allowed=network_allowed)

        # 4. Sanitized Environment & Network Interception
        sanitized_env = get_sanitized_environment(extra_env=env_vars, allow_git=network_allowed)

        if not network_allowed:
            # Poison proxy variables to dead local port
            for pk in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]:
                sanitized_env[pk] = "http://127.0.0.1:9"

            # Inject Python offline socket interceptor via PYTHONPATH
            guard_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "guards"))
            if "PYTHONPATH" in sanitized_env and sanitized_env["PYTHONPATH"]:
                sanitized_env["PYTHONPATH"] = f"{guard_dir}{os.pathsep}{sanitized_env['PYTHONPATH']}"
            else:
                sanitized_env["PYTHONPATH"] = guard_dir

        cmd_to_run = [resolved_exec] + command_list[1:]
        timeout_val = max(1, min(timeout_seconds, 120))

        exit_code = 1
        stdout_str = ""
        stderr_str = ""
        status = "COMPLETED"

        proc = None
        try:
            proc = subprocess.Popen(
                cmd_to_run,
                cwd=self.sandbox_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=sanitized_env,
                shell=False
            )
            stdout_str, stderr_str = proc.communicate(timeout=timeout_val)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            status = "TIMEOUT"
            exit_code = 124
            stderr_str = f"Command timed out after {timeout_val} seconds."
            if proc:
                self._terminate_process_tree(proc.pid)
        except Exception as e:
            status = "ERROR"
            exit_code = 1
            stderr_str = str(e)
            if proc:
                self._terminate_process_tree(proc.pid)
        finally:
            duration = time.time() - start_time
            self._record_subprocess_audit(
                command_list=command_list,
                timeout=timeout_val,
                duration=duration,
                exit_code=exit_code,
                status=status
            )

        return exit_code, stdout_str, stderr_str

    def _terminate_process_tree(self, pid: int):
        """Kills entire process tree on Windows or POSIX to prevent orphan processes."""
        try:
            if sys.platform.startswith("win"):
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(pid)],
                    capture_output=True,
                    check=False
                )
            else:
                os.kill(pid, 9)
        except Exception:
            pass

    def _record_subprocess_audit(
        self,
        command_list: List[str],
        timeout: int,
        duration: float,
        exit_code: int,
        status: str
    ):
        """Appends audit log entry for subprocess invocation."""
        os.makedirs(os.path.dirname(SUBPROCESS_AUDIT_LOG), exist_ok=True)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "task_id": self.task_id,
            "executable": os.path.basename(command_list[0]),
            "command": command_list,
            "cwd": self.sandbox_dir,
            "timeout_seconds": timeout,
            "duration_seconds": round(duration, 3),
            "exit_code": exit_code,
            "status": status
        }
        try:
            with open(SUBPROCESS_AUDIT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def compute_file_sha256(self, rel_path: str) -> str:
        """Computes SHA-256 for a file inside the sandbox."""
        full_path = os.path.join(self.sandbox_dir, rel_path)
        if not os.path.exists(full_path):
            return ""
        hasher = hashlib.sha256()
        with open(full_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def collect_artifacts(self) -> List[Dict[str, Any]]:
        """Collects all generated files in sandbox with metadata and SHA-256."""
        artifacts = []
        for root, _, files in os.walk(self.sandbox_dir):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, self.sandbox_dir)
                sha = self.compute_file_sha256(rel_path)
                artifacts.append({
                    "artifact_id": f"ART-{len(artifacts)+1:03d}",
                    "artifact_type": os.path.splitext(file_name)[1].lstrip(".") or "text",
                    "path": rel_path,
                    "sha256": sha,
                    "size_bytes": os.path.getsize(full_path)
                })
        return artifacts

    def cleanup(self):
        """Removes the task sandbox workspace."""
        if os.path.exists(self.sandbox_dir):
            shutil.rmtree(self.sandbox_dir, ignore_errors=True)
