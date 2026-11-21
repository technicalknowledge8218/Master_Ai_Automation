# MASTER-AI Formal Threat Model: Agent Execution & Host Boundaries

> **Document Type**: Formal Security Threat Model  
> **Standard**: STRIDE & Zero-Trust Defense-in-Depth  
> **Scope**: MASTER-AI Local Multi-Agent Ecosystem (`03_AI_AGENTS/`) & Windows Host Integration  
> **Status**: APPROVED & ACTIVE (Phase 4.3)  
> **Date**: 2026-11-17  

---

## 1. Threat Modeling Overview & Security Posture

MASTER-AI operates as a sovereign, multi-agent AI knowledge, research, and development workspace on Windows 11. As the system evolves from deterministic script simulation toward autonomous LLM-driven execution, the risk profile changes dramatically:
1. Agents may generate arbitrary Python, Node.js, and shell code.
2. Agents could be compromised via prompt injection, hallucinated dependencies, or malicious source repositories.
3. Agents operating on the Windows desktop must be rigorously prevented from accessing or corrupting user personal files, operating system configurations, credentials, or external networks without explicit human authorization.

---

## 2. Comprehensive 12-Threat Matrix

```
                      ┌────────────────────────────────────────┐
                      │        MASTER ORCHESTRATOR             │
                      │  (Enforces Trust Levels 0 - 4)        │
                      └──────────────────┬─────────────────────┘
                                         │ Task Request + Auth Token
                                         ▼
                      ┌────────────────────────────────────────┐
                      │      BASE SPECIALIST AGENT             │
                      │  (Fail-Closed Central Authorization)   │
                      └──────────────────┬─────────────────────┘
                                         │ Scoped Execution
                                         ▼
                      ┌────────────────────────────────────────┐
                      │           TASK SANDBOX                 │
                      │  ┌──────────────────────────────────┐  │
                      │  │ Filesystem Guard:                │  │
                      │  │  - Path Traversal Block          │  │
                      │  │  - Junction & Symlink Block      │  │
                      │  │  - UNC / Device / ADS Block      │  │
                      │  ├──────────────────────────────────┤  │
                      │  │ Subprocess Guard:                │  │
                      │  │  - Absolute Binary Resolution    │  │
                      │  │  - CWD Hijack Prevention         │  │
                      │  │  - Environment Sanitization      │  │
                      │  │  - Argument Sanitization         │  │
                      │  ├──────────────────────────────────┤  │
                      │  │ Network Guard:                   │  │
                      │  │  - Socket Connect Interception   │  │
                      │  │  - Proxy Poisoning (Dead Port)   │  │
                      │  │  - Level 3 Human Gatekeeper      │  │
                      │  ├──────────────────────────────────┤  │
                      │  │ Git Guard:                       │  │
                      │  │  - Remote Operations Block       │  │
                      │  │  - Destructive History Block     │  │
                      │  │  - Global Config Block           │  │
                      │  └──────────────────────────────────┘  │
                      └────────────────────────────────────────┘
```

---

### Threat 1: Malicious or Compromised Agent
- **Attack Scenario**: An agent receives a prompt containing an indirect injection or corrupted instruction directing it to ignore its role boundaries and execute unauthorized tools or arbitrary tasks.
- **Current Protection**: Role-based tool whitelisting (`ALLOWED_TOOLS` in agent specifications) and task-bound authorization tokens (`AUTH-<task_id>-<token>`).
- **Remaining Weakness**: An agent could attempt to forge an authorization token or reuse a token issued for another task.
- **Required Mitigation**: Centralized token verification in `BaseSpecialistAgent` with cryptographic task binding and actor rejection (`agent:*` cannot authorize).
- **Residual Risk**: Low. Any unauthorized tool call fails closed before execution.

---

### Threat 2: Malicious Generated Python Code
- **Attack Scenario**: CodingAgent generates Python code containing payload commands (`os.system("del ...")`, `import socket; ...`, `ctypes.windll...`, or infinite loops).
- **Current Protection**: SecurityAuditor performs static AST inspection for dangerous functions (`eval`, `exec`, `os.system`). Subprocesses enforce timeouts (15s).
- **Remaining Weakness**: Obfuscated code, dynamic imports (`__import__('os')`), or multi-stage payloads could evade static AST pattern matching.
- **Required Mitigation**: Pinned sandbox `cwd`, stripped environment variables, offline network socket interception via `sitecustomize.py`, and Windows process-tree termination via `taskkill /F /T /PID`.
- **Residual Risk**: Medium. In-memory exploits in the Python runtime could crash the child process, but cannot access host files or network.

---

### Threat 3: Malicious Generated Node.js Code
- **Attack Scenario**: Generated JavaScript/TypeScript code executes child processes (`child_process.exec`) or exfiltrates data via `fetch` / `http.get`.
- **Current Protection**: Strict binary whitelisting in `TaskSandbox` (`node` allowed, but `powershell`/`cmd` blocked).
- **Remaining Weakness**: Node.js has native filesystem and network access APIs (`fs`, `net`, `http`, `worker_threads`).
- **Required Mitigation**: Environment sanitization stripping credentials, proxy poisoning (`HTTP_PROXY=http://127.0.0.1:9`), explicit path validation on file read/write, and process-tree termination on timeout.
- **Residual Risk**: Low to Medium. Outbound network attempts time out against the dead loopback proxy.

---

### Threat 4: Filesystem Access Outside Task Workspace
- **Attack Scenario**: An agent attempts to read, write, or delete files in `C:\Windows`, `<USER_HOME>\Documents`, or the root MASTER-AI workspace via relative paths (`../../`) or absolute paths (`C:\...`).
- **Current Protection**: `TaskSandbox.is_safe_path()` checks `os.path.commonpath` against `sandbox_dir`.
- **Remaining Weakness**: Prior to Phase 4.3, non-existent target files skipped `os.path.realpath` evaluation, allowing directory junction write-escapes.
- **Required Mitigation**: Always resolve `os.path.realpath(target)` regardless of file existence; reject UNC paths (`\\...`), device names (`CON`, `NUL`), alternate data streams (`:stream`), and null bytes (`\0`).
- **Residual Risk**: Negligible. All file operations fail closed with `SandboxSecurityViolation`.

---

### Threat 5: Environment Variable Disclosure
- **Attack Scenario**: Generated code executes `os.environ` or `process.env` to read API tokens, cloud keys, user profile paths, and system secrets.
- **Current Protection**: `get_sanitized_environment()` filters environment variables to a strict safe allowlist (`PATH`, `SYSTEMROOT`, `COMSPEC`, `TEMP`, `OS`).
- **Remaining Weakness**: Safe allowlist variables could contain user names or system architecture details.
- **Required Mitigation**: `PATH` is scrubbed to remove user roaming/appdata directories. `TEMP` and `TMP` are redirected to an isolated sandbox temp folder.
- **Residual Risk**: Negligible. Zero credentials, tokens, or private user paths exist in the child environment.

---

### Threat 6: Credential Theft
- **Attack Scenario**: An agent attempts to search the host filesystem for `.env` files, SSH keys (`~/.ssh/id_rsa`), AWS credentials (`~/.aws/credentials`), or Git credentials.
- **Current Protection**: `USERPROFILE`, `HOME`, and `APPDATA` are purged from the child environment. Sandbox file operations cannot escape `sandbox_dir`.
- **Remaining Weakness**: Hardcoded path guesses in generated code (e.g., `open('<USER_HOME>/.ssh/id_rsa')`).
- **Required Mitigation**: Child processes run without administrative elevation. `TaskSandbox` file APIs reject all paths outside `sandbox_dir`.
- **Residual Risk**: Low. Windows file system permissions prevent standard unprivileged processes from accessing protected credentials outside the user session, while sandbox APIs prevent any escape.

---

### Threat 7: Network Exfiltration
- **Attack Scenario**: An agent or generated script attempts to transmit workspace files, source code, or telemetry to an external server via HTTP/HTTPS, DNS tunneling, or raw TCP/UDP sockets.
- **Current Protection**: High-risk operations require human approval.
- **Remaining Weakness**: Subprocesses previously inherited host network connectivity.
- **Required Mitigation**: Multi-tier defense:
  1. Proxy poisoning (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` set to `http://127.0.0.1:9`).
  2. Python `sitecustomize.py` preload blocking outbound sockets to non-loopback addresses with `PermissionError`.
  3. Git command wrapper blocking remote subcommands.
  4. Trust Level 3 human gatekeeping for any task requesting network connectivity.
- **Residual Risk**: Low. Without administrator-level Windows Firewall rules, an advanced binary could construct raw Winsock packets, but whitelisted binaries (`python`, `node`, `git`) are bounded by runtime hooks and proxy configuration.

---

### Threat 8: External Git Operations
- **Attack Scenario**: An agent executes `git push`, `git fetch`, `git clone`, `git remote add`, or modifies `--global` Git configurations, leaking repository history or altering global developer settings.
- **Current Protection**: Zero Git remotes exist; working tree is audited by quality gate.
- **Remaining Weakness**: `run_subprocess(["git", ...])` previously allowed any git subcommand.
- **Required Mitigation**: Dedicated `GitSecurityGatekeeper` enforcing an explicit whitelist of local safe commands (`status`, `diff`, `log`, `show`, `rev-parse`, `init`, `add`, `commit`, `checkout`, `branch`, `tag`). Remote commands (`push`, `fetch`, `clone`, `pull`, `remote`, `ls-remote`) and destructive operations (`reset --hard`, `clean -fdx`, `branch -D`) are blocked.
- **Residual Risk**: Zero. Git cannot communicate externally or rewrite history.

---

### Threat 9: Shell Command Injection
- **Attack Scenario**: Malicious input passed to `run_subprocess` contains command chaining characters (`;`, `&&`, `||`, `|`, `&`, backticks, `$()`, `>`, `<`), Windows carets (`^`), or trailing backslashes that escape command line quotes in `CreateProcess`.
- **Current Protection**: `shell=False` is enforced; prohibited characters trigger `SandboxSecurityViolation`.
- **Remaining Weakness**: Windows `subprocess.list2cmdline` has known edge cases where trailing backslashes escape trailing quotes (`"path\"` becomes `path\"`), corrupting the next argument.
- **Required Mitigation**: Comprehensive argument sanitization rejecting null bytes, control characters, carets, and unbalanced trailing backslashes before executing `Popen(shell=False)`.
- **Residual Risk**: Negligible. Shell interpreters (`cmd.exe`, `powershell.exe`) are never invoked directly.

---

### Threat 10: Symlink and Junction Escape
- **Attack Scenario**: An agent creates a Windows directory junction (`mklink /J link C:\`) or NTFS symlink inside the sandbox, and then performs reads or writes through the link to manipulate host files.
- **Current Protection**: `os.path.realpath` resolves symlinks.
- **Remaining Weakness**: Non-existent files were previously evaluated using `os.path.abspath` only, allowing write-escapes through junctions.
- **Required Mitigation**: Unconditionally compute `os.path.realpath(target)` for all read and write operations. If `os.path.commonpath([real_target, sandbox_dir]) != sandbox_dir`, reject immediately.
- **Residual Risk**: Zero. Junctions and symlinks pointing outside the sandbox are completely neutralized.

---

### Threat 11: Approval Engine Bypass
- **Attack Scenario**: An agent attempts to approve its own task by calling `HumanApprovalEngine.approve_task()` or directly writing to `APPROVAL_LEDGER.json`.
- **Current Protection**: State machine enforces `REVIEW_REQUIRED` on high-risk triggers; direct instantiation requires valid token.
- **Remaining Weakness**: An agent could pass `actor="human"` or invoke ledger methods if it gains Python execution context.
- **Required Mitigation**: Mandatory token validation in `BaseSpecialistAgent`; rejection of `agent:*` actors; atomic ledger updates protected by `msvcrt` file locks.
- **Residual Risk**: Low. Sandboxed subprocesses do not have access to the in-memory `HumanApprovalEngine` reference of the orchestrator.

---

### Threat 12: Agent-to-Agent Privilege Escalation
- **Attack Scenario**: A low-privilege agent (e.g. `ResearchAgent`, Level 0) attempts to invoke a higher-privilege agent (e.g. `CodingAgent`, Level 2) or steal its task-bound authorization token to execute arbitrary code.
- **Current Protection**: Agents do not directly instantiate peer agents; all delegation flows through `MasterOrchestrator`.
- **Remaining Weakness**: Shared memory or token disclosure in artifact handoffs.
- **Required Mitigation**: Cryptographically bound task tokens (`AUTH-<task_id>-<token>`). Tokens are single-task and rejected if used across tasks. `BaseSpecialistAgent` strictly verifies task ID match.
- **Residual Risk**: Zero. Cross-task token reuse is empirically blocked (verified by SEC-003).

---
*Threat Model Certified by MASTER-AI Security & Quality Gatekeeper.*
