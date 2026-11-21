# MASTER-AI Agent Execution & Federation Standard

> **Standard Version**: 1.0.0  
> **Status**: APPROVED & ACTIVE  
> **Source Directory**: `03_AI_AGENTS/`  

---

## 1. Operational Overview & Identity

The MASTER-AI Agent Ecosystem is a modular federation of specialist agents coordinated by a centralized, boundary-enforcing Master Orchestrator. 

Agents are classified across four progressive capability tiers:
- **Tier A (Documented)**: Persona and operational mandate established in markdown catalogs.
- **Tier B (Configured)**: Formal JSON specification authored with strict input/output schemas, allowed tools, and prohibited actions in `03_AI_AGENTS/definitions/`.
- **Tier C (Runtime-Executable)**: Executable Python runner instantiated in `03_AI_AGENTS/agents/` and registered natively via Antigravity `define_subagent`.
- **Tier D (Tested on Real Tasks)**: Empirically verified on isolated sandbox tasks with validated artifact handoffs and passing test assertions.

---

## 2. Core Federation Principles

1. **Least Privilege & Scoped Tooling**: Agents are granted only the tools essential for their specialization. Destructive or global tools are strictly prohibited.
2. **Mandatory Sandboxing**: All code generation, script execution, and test runs MUST occur within an ephemeral `TaskSandbox` (`03_AI_AGENTS/sandbox/tasks/<task_id>/`). Never execute untested code on the workspace root.
3. **Strict Schema Contracts**: Every agent request and response must validate against standard JSON schemas (`agent_request_schema.json`, `agent_response_schema.json`).
4. **Transparent Artifact Handoffs**: Data passed between agents is tracked via cryptographic SHA-256 digests and recorded in the execution ledger.
5. **Deterministic Human Approval**: Any operation attempting global deployment, configuration modification, remote Git push, or destructive file changes is blocked by the `HumanApprovalEngine`.

---

## 3. Specialist Agent Execution Contracts

| Agent ID | Agent Slug | Primary Mandate | Allowed Tools | Prohibited Actions |
| :--- | :--- | :--- | :--- | :--- |
| `AGT-001` | `research_agent` | Literature and empirical research | `search_web, read_file, run_command, view_file` | `write_file_outside_sandbox, install_global_packages, modify_system_configs` |
| `AGT-002` | `software_architect` | System architecture & spec design | `read_file, write_file, edit_file, view_file` | `write_file_outside_sandbox, bypass_architecture_rules` |
| `AGT-003` | `coding_agent` | Type-safe modular implementation | `read_file, write_file, edit_file, run_command` | `git_push_remote, bypass_lint_rules, store_credentials` |
| `AGT-004` | `testing_agent` | QA & test automation suites | `read_file, write_file, run_command, view_file` | `modify_source_code, bypass_failures, deploy_packages` |
| `AGT-005` | `documentation_agent`| ADRs and living documentation | `read_file, write_file, edit_file, view_file` | `modify_source_code, delete_historical_adrs` |
| `AGT-006` | `security_auditor` | Static analysis & zero-secret audit | `read_file, run_command, view_file` | `write_code, bypass_security_alerts` |
| `AGT-007` | `capability_discovery_agent` | Capability domain horizon scanning | `read_file, run_command, view_file` | `write_code, modify_global_configs` |

---

## 4. Subtask Execution & Handoff Lifecycle

```
[Master Orchestrator] ───> Decomposes Task into Subtask DAG
          │
          ├──> AGT-007 (Capability Discovery): Validates system readiness
          ├──> AGT-001 (Research): Researches patterns & cites sources
          │       │  [Handoff: Research Report + SHA-256]
          ├──> AGT-002 (Architecture): Generates validated system spec
          │       │  [Handoff: Architecture Spec + SHA-256]
          ├──> AGT-003 (Coding): Implements type-safe code in Sandbox
          │       │  [Handoff: Source Code + SHA-256]
          ├──> AGT-004 (Testing): Executes isolated unit/integration tests
          │       │  [Handoff: Test Summary + SHA-256]
          ├──> AGT-006 (Security): Audits sandbox code for secrets & AST safety
          │       │  [Handoff: Security Audit Report + SHA-256]
          └──> AGT-005 (Documentation): Generates validated ADR & documentation
                  │
[Consolidated Ledger] <─── Records all subtasks, handoffs, and final result
```

---

## 5. Human Approval Engine & Authorization Token Protocol

### State Machine
$$\text{PROPOSED} \longrightarrow \text{REVIEW\_REQUIRED} \longrightarrow \text{APPROVED} \longrightarrow \text{EXECUTING} \longrightarrow \text{VERIFIED} \longrightarrow \text{COMPLETED}$$

Any high-risk trigger (touching `.gemini`, modifying MCP configs, external Git remotes, or paid APIs) immediately transitions the task to `REVIEW_REQUIRED` and pauses execution until explicit human authorization is recorded.

### Authorization Token Protocol (Phase 4.2 Standard)
1. **Mandatory Token Injection**: All agent task requests must supply a valid `auth_token` matching the task schema.
2. **Centralized Verification**: `BaseSpecialistAgent` independently verifies the token against `HumanApprovalEngine` before invoking any agent execution or tool. Direct execution without a token fails closed (`AUTHORIZATION_DENIED`).
3. **Task-Bound Enforcement**: A token generated for `TASK-A` is cryptographically bound (`AUTH-TASK-A-<random>`) and immediately rejected if presented for `TASK-B`.
4. **Token TTL Expiration**: Tokens carry an explicit issue timestamp and time-to-live (TTL, default 3600s). Expired tokens are rejected.
5. **Agent Self-Approval Prohibition**: Actors matching the pattern `agent:*` are rejected by the approval engine. Only human operators or system orchestrators may authorize or transition tasks.
6. **Concurrent Ledger Protection**: The approval ledger is protected by Windows `msvcrt` file locking and atomic replacement (`.tmp` + `os.replace`), with automatic backup and recovery from `.bak`.

---

## 6. Process Execution Hardening & Secure Boundary Enforcement (Phase 4.3 Standard)

Specialist agent tools that spawn subprocesses must execute within `TaskSandbox` which enforces:
- **Absolute Binary Resolution**: System runtimes (`sys.executable` for Python; system `PATH` resolution for Node and Git) are resolved absolutely. Executing binaries located inside the sandbox `cwd` is blocked to prevent binary hijacking.
- **Unconditional Path Boundary**: Both `abspath` and `realpath` must reside inside `sandbox_dir`. This is checked unconditionally for existing and non-existent paths, blocking directory junction (`mklink /J`) and symlink write-escapes.
- **UNC & Device Name Filtering**: UNC paths (`\\...`), Alternate Data Streams (`:stream`), and DOS device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`) are rejected.
- **Sanitized Environment**: Child processes do not inherit host credentials, tokens, passwords, `USERPROFILE`, or `APPDATA`. Only a minimal whitelist of system paths and OS variables is provided.
- **Offline Network Isolation (Default)**: Task sandboxes operate offline by default. Outbound HTTP/HTTPS is neutralized via dead-port proxy poisoning (`http://127.0.0.1:9`), and Python raw sockets are intercepted via `03_AI_AGENTS/sandbox/guards/sitecustomize.py`, raising `PermissionError` on external connections while allowing local loopback (`127.0.0.1`).
- **Git Command Restrictions**: Only safe local Git commands (`status`, `diff`, `log`, `show`, `rev-parse`, `init`, `add`, `commit`, `checkout`, `branch`, `tag`) are allowed. Remote commands (`push`, `fetch`, `clone`) and destructive commands (`reset --hard`, `clean -fdx`, `branch -D`) are blocked.
- **Argument Sanitization**: Shell command chaining characters (`;`, `&&`, `||`, `|`, `&`, backticks, `$()`, `>`, `<`), Windows carets (`^`), null bytes (`\0`), and unescaped trailing backslashes are rejected.
- **Process Tree Kill on Timeout**: Windows child process trees are terminated using `taskkill /F /T /PID <pid>` upon timeout (15s default), preventing orphan or background runaway processes.
- **Audit Logging**: Every subprocess invocation is permanently recorded in `03_AI_AGENTS/runs/SUBPROCESS_AUDIT.jsonl`.

---

## 7. Formal 5-Tier Execution Trust Levels

| Trust Level | Designation | Allowed Capabilities | Gating Mechanism |
| :--- | :--- | :--- | :--- |
| **LEVEL 0** | Read-Only Analysis | File reading within workspace/sandbox, doc search, static AST analysis. | Baseline role assignment. |
| **LEVEL 1** | Workspace-Local File Ops | File creation, editing, and staging strictly inside task sandbox. | Baseline role assignment. |
| **LEVEL 2** | Local Code Execution | Sandboxed execution of Python, Node, and safe local Git (offline). | Task-bound authorization token. |
| **LEVEL 3** | Approved Network Operations | Scoped external network queries or authorized remote Git access. | Explicit human approval required. |
| **LEVEL 4** | Host / Global System Config | Modification of global `.gemini` settings, skills, or rules. | Multi-step human approval required. |

- **Invariants**:
  1. No agent (`actor: agent:*`) can elevate its own trust level.
  2. Untrusted autonomously generated code is permanently capped at Trust Level 2 and can never receive Level 4 permissions.

---

## 8. Dual-Mode Antigravity Subagent Execution Architecture & Native Verification

The multi-agent ecosystem supports two distinct operational modes:

1. **IDE Interactive Mode**:
   - `03_AI_AGENTS/orchestrator/ant_subagent_bridge.py` prepares agent specifications conforming to Antigravity's `define_subagent` interface.
   - When running inside the Antigravity IDE, agents are registered dynamically in the IDE session, and hierarchical delegation is handled via `invoke_subagent`.
2. **Local Autonomous Pipeline Mode**:
   - Programmatic execution via `python 03_AI_AGENTS/orchestrator/orchestrator.py` provides standalone execution for CI/CD, local test runners, and automated scripts without requiring active IDE UI session interaction.
   - Both modes share the exact same underlying specialist agent implementations, contracts, approval engine, and security sandbox.

### Empirical Native Subagent Verification (Phase 4.3 Evidence)
Native Antigravity subagent invocation was empirically verified on 2026-11-17:
- **Subagent Type**: `research`
- **Assigned Role**: `Codebase Researcher`
- **Assigned Model**: `flash_lite`
- **Conversation ID**: `420e6d97-df7e-47a2-a6c4-83c6953c3ee5`
- **Log Absolute URI**: `file:///C:/Users/Sangam/.gemini/antigravity/brain/420e6d97-df7e-47a2-a6c4-83c6953c3ee5/.system_generated/logs/transcript.jsonl`
- **Reported Result**: Subagent inspected `00_CORE_SYSTEM`, listed its 11 items (`adrs`, `config`, `dashboard`, `discovery_engine`, `learning_engine`, `protocols`, `registry`, `KNOWLEDGE_MANAGEMENT_POLICY.md`, `MASTER_AI_CONSTITUTION.md`, `PROJECT_IMPORT_POLICY.md`, `README.md`, `SYSTEM_INSTRUCTIONS.md`), verified read-only exploration constraints, and delivered a high-priority notification to the parent session.
- **Verification**: Proven operational without simulation or mock wrappers.

### Phase 5 Full Specialist Team Live Verification (2026-11-17 Evidence)
All 7 native Antigravity specialist subagents were invoked and completed genuine technical assignments in Phase 5:
1. **AGT-001 `research_agent`** (ID: `2f390876-b54e-4cb8-a646-4360415ad9ba`): Verified official documentation URLs, versions, and licenses for React 19, PostgreSQL, Node.js, and Capacitor.
2. **AGT-002 `software_architect`** (ID: `1ea37359-a192-45ea-bd55-73acc5d2f9dd`): Formulated Three-Tier Clean Architecture, dependency inversion, DAG module boundaries, monolith vs microservices criteria, and ADR guidelines.
3. **AGT-003 `coding_agent`** (ID: `c44248e6-ba1b-40ce-ab44-a9ce476a6775`): Defined TypeScript strict mode (zero-any, discriminated unions, tsconfig) and Python standards (PEP 8, type hints, Pydantic v2).
4. **AGT-004 `testing_agent`** (ID: `dd0ae579-9d0a-418d-807b-5aa7118714e1`): Formulated 4-tier testing pyramid (unit, integration, contract, E2E), 80% coverage threshold, deterministic mocks, and boundary assertions.
5. **AGT-005 `documentation_agent`** (ID: `cfc7c9ac-cba8-4565-ae88-0b99da065327`): Authored `12_DOCUMENTS/DOCUMENTATION_STANDARD.md` covering GFM living documentation, README hierarchy, OpenAPI 3.1 specifications, ADR templates, and relative link protocols.
6. **AGT-006 `security_auditor`** (ID: `1419d1a9-72a0-4de9-af8a-8e90271d89dc`): Defined full-stack security standards (OWASP Top 10 mitigations, Secret-Zero rules, JWT/session handling, CSRF/CSP defense, and SCA scanning).
7. **AGT-007 `capability_discovery_agent`** (ID: `0c115d7c-5a34-4887-aecd-30272c584aca`): Performed capability gap audit across 30 domains, mapping coverage and identifying priority capabilities for Phase 5.
