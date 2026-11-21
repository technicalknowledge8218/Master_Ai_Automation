# MASTER-AI Security & Compliance Policy

> **Security Posture**: Zero-Trust, Secret-Zero, Least-Privilege  
> **Source Directory**: `19_SECURITY_AND_COMPLIANCE/`  

---

## 1. Secret Management (Secret-Zero Policy)

1. **Absolute Ban on Code Secrets**: API keys, access tokens, database passwords, private keys, and certificates must NEVER appear in code, markdown, or commits.
2. **Environment Variable Injection**: All credentials must be loaded via `.env` files (excluded by `.gitignore`) or OS environment variables.
3. **Automated Secret Scanning**: Pre-commit hooks and security audits must scan for entropy patterns matching high-risk credentials.

---

## 2. Access Control & Sandboxing

1. **Filesystem Boundaries**: Tools and scripts must operate only within their assigned workspace directory.
2. **Tool Execution Whitelisting**: Arbitrary binary execution is strictly forbidden. Only approved development runtimes (Node, Python, Git) may be invoked.
3. **No Credential Bypassing**: Never attempt to circumvent access controls, Captchas, or firewall rules.

---

## 3. Vulnerability Management

- **OWASP Top 10 Defenses**: All web and API blueprints must implement parameter validation, SQL injection prevention, and CSP headers.
- **Dependency Auditing**: Run `npm audit` and `pip-audit` before incorporating third-party packages into `14_CODE_LIBRARY` or projects.

---

## 4. Multi-Agent Sandboxing & Human Approval Gatekeeper

1. **TaskSandbox Isolation**: Specialist agents must execute tasks within ephemeral sandboxes (`03_AI_AGENTS/sandbox/tasks/<task_id>/`). Direct in-place writes to root workspace during testing are prohibited.
2. **Centralized Agent Execution Authorization**:
   - Every agent request schema mandates a non-empty `auth_token`.
   - `BaseSpecialistAgent` enforces centralized authorization prior to any tool execution or work step.
   - Approval tokens are strictly task-bound (`AUTH-<task_id>-<token>`), cryptographically generated, and tracked in the approval ledger.
   - Direct agent instantiation or tool invocation without a valid, unexpired token issued for that exact task ID fails closed (`AUTHORIZATION_DENIED`).
   - Token TTL (default 3600 seconds) is enforced, rejecting stale tokens.
   - Agent self-approval is forbidden: actors matching `agent:*` cannot issue or approve tasks.
3. **Approval Ledger Concurrency & Integrity**:
   - The approval ledger (`03_AI_AGENTS/approval_engine/APPROVAL_LEDGER.json`) is protected by Windows-safe file locking (`msvcrt.locking` non-blocking with retry and timeout).
   - Atomic writes utilize unique temporary files (`.tmp.<pid>.<uuid>`) and atomic replacement (`os.replace`).
   - A rolling backup (`APPROVAL_LEDGER.json.bak`) is automatically maintained.
   - In case of unexpected process termination or corruption, the engine detects invalid JSON and auto-recovers from `.bak`.
4. **Subprocess Boundary Enforcement & Environment Sanitization**:
   - Commands are whitelisted exclusively to approved development runtimes (`python`, `node`, `git`).
   - Execution working directory is explicitly pinned to the task sandbox directory (`cwd=sandbox_dir`).
   - Environment sanitization: Sensitive host variables (`USERPROFILE`, `APPDATA`, credentials, tokens, passwords) are purged from child environments. Only safe system keys (`PATH`, `SYSTEMROOT`, `COMSPEC`, `TEMP`, `OS`) are whitelisted.
   - Command arguments are strictly validated against shell injection characters (`;`, `&&`, `||`, `|`, `&`, backticks, `$()`, `>`, `<`).
   - Mandatory timeouts (1 to 120s, default 15s) are enforced. Upon timeout, process tree termination is executed via `taskkill /F /T /PID <pid>` on Windows to prevent orphaned worker processes.
   - Every subprocess execution is permanently recorded in `03_AI_AGENTS/runs/SUBPROCESS_AUDIT.jsonl`.
5. **Deterministic Human Approval Gatekeeper**:
   - High-risk operations (global `.gemini` modifications, MCP configuration changes, paid APIs, external Git remotes, destructive operations) automatically place tasks into `REVIEW_REQUIRED`.
   - Execution is blocked until an explicit human authorization is granted.
6. **Zero-Secret AST Static Scanning**: Code produced by agents is scanned by `SecurityAuditor` for exposed credentials and dangerous functions (`eval`, `exec`, `os.system`) prior to acceptance.

---

## 5. Windows Process Isolation Architecture

MASTER-AI explicitly documents and operates under four distinct Windows execution isolation tiers:

| Isolation Tier | Mechanism | Workspace Applicability | Current Implementation Status |
| :--- | :--- | :--- | :--- |
| **Level A: Application-Level Path Validation & Environment Sanitization** | Strict cwd pinning, whitelisted binaries, argument validation, environment scrubbing, and `taskkill /F /T /PID` tree kill. | 100% portable, requires zero administrator privileges or host OS configuration. | **ACTIVE (Enforced in `sandbox_runner.py`)** |
| **Level B: Windows Job Objects** | Win32 Job Objects (`AssignProcessToJobObject`) with hard CPU, memory, and active process limits. | Highly portable on Windows, requires C/ctypes bindings, non-admin. | **DESIGNED (Documented in ADR-005; planned for future native extension)** |
| **Level C: Windows AppContainer Isolation** | Low-integrity capability-gated sandboxing (used by UWP and Chromium sandboxes). | Complex ACL manipulation, requires package SID creation, not zero-dependency. | **EVALUATED (Reserved for production enterprise deployment)** |
---

## 6. Secure Execution Boundary, Network Isolation & Trust Levels (Phase 4.3 Standard)

### 6.1 Filesystem Boundary Protections
1. **Unconditional Realpath Validation**: Both `os.path.abspath(target)` and `os.path.realpath(target)` must reside strictly inside `sandbox_dir`. This evaluation applies unconditionally, even when target files do not yet exist, permanently closing Windows directory junction (`mklink /J`) and symlink write-escapes.
2. **UNC Path Rejection**: Universal Naming Convention paths (`\\localhost\...`, `\\?\...`, `//...`) are strictly rejected.
3. **Alternate Data Stream (ADS) Blocking**: Colons in file paths outside the standard drive letter specifier (`C:\`) are rejected to prevent NTFS hidden stream exploitation.
4. **DOS Device Name Blocking**: Legacy Windows device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`) are blocked to prevent operating system deadlocks.
5. **Null Byte Rejection**: Paths containing `\0` are rejected immediately.

### 6.2 Subprocess Security & Binary Resolution
1. **Absolute Binary Resolution**: Executables are resolved strictly against system paths (`sys.executable` for Python; `shutil.which` against system `PATH` for Node and Git). Executing binaries from `cwd` (sandbox directory) is forbidden, preventing CWD binary hijacking.
2. **Windows Argument Sanitization**: Arguments containing carets (`^`), null bytes (`\0`), or unescaped trailing backslashes that escape closing quotes in `CreateProcess` are rejected.
3. **Execution Shell Banned**: `shell=False` is enforced unconditionally across all sandbox process spawning.

### 6.3 Network Isolation & Offline Enforcement
1. **Default Offline Policy**: By default (Trust Levels 0, 1, 2), all task sandboxes operate strictly offline without internet connectivity.
2. **Proxy Poisoning**: Environment variables `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and their lowercase equivalents are poisoned to a dead local port (`http://127.0.0.1:9`).
3. **Python Socket Interceptor**: Python processes load `03_AI_AGENTS/sandbox/guards/sitecustomize.py` via `PYTHONPATH`, intercepting `socket.socket.connect`. Any connection attempt to a non-loopback host raises `PermissionError`.
4. **Local Loopback Preserved**: Connections to `127.0.0.1`, `localhost`, and `::1` remain permitted for local service integration tests.
5. **Level 3 Gatekeeper**: Network access is only unlocked when a task is explicitly authorized at Trust Level 3 with human approval.

### 6.4 Git Command Restrictions
1. **Allowed Local Subcommands**: `status`, `diff`, `log`, `show`, `rev-parse`, `init`, `add`, `commit`, `checkout`, `branch`, `tag`, `describe`, `version`, `config`, `switch`.
2. **Forbidden Remote Subcommands**: `push`, `fetch`, `clone`, `pull`, `remote`, `ls-remote`, `submodule` are blocked under default offline policy.
3. **Forbidden Destructive Flags**: `--hard`, `-fdx`, `-f`, `-d`, `-D`, `--force` trigger immediate `SandboxSecurityViolation`.
4. **Forbidden Global Config**: `git config --global` and `git config --system` are blocked.

### 6.5 Formal 5-Tier Execution Trust Levels

| Trust Level | Classification | File Read | File Write | Code Exec | Network | Global Config | Authorization Required |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **LEVEL 0** | Read-Only Analysis | Workspace/Sandbox | None | None | None | None | Baseline |
| **LEVEL 1** | Workspace-Local File Ops | Workspace/Sandbox | Sandbox only | None | None | None | Baseline |
| **LEVEL 2** | Local Code Execution | Workspace/Sandbox | Sandbox only | Offline Sandbox | None | None | Task-Bound Token |
| **LEVEL 3** | Approved Network Operations | Workspace/Sandbox | Sandbox only | Approved Subprocesses | Whitelisted WAN | None | Explicit Human Approval |
| **LEVEL 4** | Host / Global System Config | Workspace/Sandbox | Sandbox + Global Staging | Full Runtimes | Approved | `.gemini` Allowed | Multi-Step Human Approval |

- **Anti-Self-Escalation**: No agent (`actor: agent:*`) can elevate its own trust level. Attempted self-escalation throws `TrustEscalationViolation`.
- **Untrusted Code Cap**: Untrusted or autonomously generated code is permanently restricted to Trust Level 2 or below and can never receive Level 4 permissions.

---

## 7. Phase 5 Full-Stack & LLM Security Invariants

### 7.1 Full-Stack Security Mandates
1. **Secret-Zero Invariants**: No API keys, credentials, JWT private secrets, or database connection strings may be stored in code, client-side bundles, or git tracking.
2. **Mandatory OWASP Top 10 Protections**:
   - Injection: Parameterized database queries and Zod/Pydantic input schema validation on all API endpoints.
   - Broken Access Control: Attribute-based access control (ABAC) verified per route.
   - Insecure Design: Rate limiting (token bucket) applied to authentication and sensitive paths.
   - Vulnerable Components: Continuous automated SCA scanning for CVEs in dependencies.
3. **Hardware Storage Security for Mobile**: Android Keystore and iOS Keychain must be used for sensitive tokens; `localStorage` and plaintext `SharedPreferences` are prohibited for secrets.

### 7.2 LLM Integration Security Invariants (LIRA)
1. **Zero Unapproved Paid API Invocations**: Financial expenditure cap defaults to \$0.00 USD. No billable model calls may occur without verified human authorization.
2. **Fail-Closed Offline Mocking**: All local development and testing executes against `OfflineMockProvider` with zero network sockets.
3. **Prompt & Log Sanitization**: All prompts and agent trajectory logs are scrubbed of secrets, tokens, and PII prior to persistence or transmission.
4. **Human Approval Gate for Destructive Actions**: Any action proposing host modification, remote push, deletion of production assets, or global configuration change requires multi-step interactive human confirmation.
