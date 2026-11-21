# MASTER-AI Architecture Specification

> **Document Version**: `1.0.0`  
> **Status**: APPROVED  
> **Last Updated**: 2026-11-16  

---

## 1. Architectural Philosophy

The MASTER-AI ecosystem is built upon the **Three-Tier Decoupled Architecture**:

```
+---------------------------------------------------------------------------------+
|                       TIER 1: MASTER REPOSITORY (SOURCE OF TRUTH)               |
|  - 24 Modular Knowledge & Engineering Domains                                   |
|  - Skill Catalog, Agent Profiles, Verified Codebase, Research Papers            |
|  - Immutable Version History & Test Verification                                |
+---------------------------------------+-----------------------------------------+
                                        |
                   [Staging, Validation & Safe Publishing]
                                        v
+---------------------------------------------------------------------------------+
|                       TIER 2: RUNTIME ANTIGRAVITY ENGINE                        |
|  - Local Workspace Environment (.agents/ or local rules)                        |
|  - Progressive Disclosure Engine (SKILL.md metadata vs full body)               |
|  - Agent Subagent / Swarm Orchestration Engine                                  |
|  - Tool Context Protocol (MCP Clients & Local Execution Tools)                  |
+---------------------------------------+-----------------------------------------+
                                        |
                 [Validated Export via 22_PUBLISH_AND_DEPLOY]
                                        v
+---------------------------------------------------------------------------------+
|                       TIER 3: GLOBAL RUNTIME INTEGRATION                        |
|  - Antigravity Global Customizations: ~/.gemini/config/                         |
|  - Global Skills, Global Rules (AGENTS.md), Global MCP Servers                  |
|  - Reused seamlessly across ALL other independent workspaces and projects      |
+---------------------------------------------------------------------------------+
```

### Key Architectural Tenets:
1. **Decoupling from Model Runtimes**: MASTER-AI does not modify foundational model weights. It builds a persistent, verifiable context, reasoning, and tool layer that elevates model performance deterministically.
2. **Sovereignty of Workspace**: MASTER-AI is the permanent source of truth. Changes do not originate in volatile global configs; they originate in MASTER-AI, undergo automated validation, and are published outbound.
3. **Progressive Disclosure**: To preserve the agent's context budget, complex skills and deep references are never loaded indiscriminately. Only metadata is exposed initially; procedural runbooks are hydrated on-demand.
4. **Hierarchical Rule Precedence**:
   - Level 1: Inviolable Security & Safety Policies (`01_GLOBAL_RULES/security_rules/`).
   - Level 2: Engineering & Code Quality Standards (`01_GLOBAL_RULES/coding_standards/`).
   - Level 3: Task-Specific Skill Instructions (`02_SKILLS/`).
   - Level 4: Runtime Model Decisions.

---

## 2. Directory & Domain Topology

The ecosystem maintains 24 strictly bounded domains:

1. **`00_CORE_SYSTEM`**: Master orchestration, registry of active components, environment configuration, and execution metadata.
2. **`01_GLOBAL_RULES`**: Absolute constraints for code, documentation, agent autonomy, and security.
3. **`02_SKILLS`**: Production-ready, modular skills following Antigravity's `SKILL.md` specification.
4. **`03_AI_AGENTS`**: Persona, capability, and boundary manifests for 18 specialized AI agents.
5. **`04_LLM_AND_AI`**: LLM architectures, RAG pipelines, fine-tuning setups, prompt engineering, and evaluation benchmarks.
6. **`05_DEVELOPMENT`**: Enterprise full-stack engineering guides, frontend (React/TypeScript), backend (Node.js/Python), mobile (Android/Capacitor), and databases.
7. **`06_UI_UX_DESIGN`**: Modern design systems, atomic components, accessibility (WCAG 2.2 AAA), and design-to-code pipelines.
8. **`07_MCP_AND_TOOLS`**: Model Context Protocol servers, transport schemas (stdio/SSE), and sandboxed execution bridges.
9. **`08_AUTOMATION`**: n8n workflows, event webhooks, cron schedulers, and fault-tolerant background pipelines.
10. **`09_CONTENT_STUDIO`**: Documentary scripting, viral short-form frameworks, AI voice/video synthesis, and cue sheets.
11. **`10_SOCIAL_MEDIA`**: Multi-platform publishing engine (YouTube, Instagram, Telegram, X) with human verification gates.
12. **`11_RESEARCH_LAB`**: Empirical investigations, emerging tech evaluations, and peer-reviewed whitepapers.
13. **`12_DOCUMENTS`**: Formal non-markdown documents, executive summaries, and architecture diagrams.
14. **`13_MARKDOWN`**: Fast-access markdown cheatsheets, syntax guides, and distilled conceptual summaries.
15. **`14_CODE_LIBRARY`**: Curated, verified, and unit-tested code algorithms and boilerplate utilities.
16. **`15_ASSETS`**: Brand identity assets, logos, icons, vector graphics, and standard audio beds.
17. **`16_VIDEO_LIBRARY`**: Asset manifests, raw footage references, B-roll catalogs, and rendering presets.
18. **`17_TEMPLATES`**: Project starters, skill templates, agent templates, and RFC document scaffolds.
19. **`18_TESTING_AND_QA`**: Quality gates, unit/integration/E2E testing suites, and performance audit tools.
20. **`19_SECURITY_AND_COMPLIANCE`**: Threat modeling, OWASP verification, secret scanning, and regulatory compliance.
21. **`20_PROJECTS`**: Active, archived, and conceptual project directories consuming MASTER-AI capabilities.
22. **`21_LEARNING_LAB`**: Active learning tracking, technology experiment sandboxes, and verified learning logs.
23. **`22_PUBLISH_AND_DEPLOY`**: Staging, conflict detection, backup generation, and publishing engine for global configs.
24. **`23_CHANGELOG_AND_BACKUP`**: Semantic version tracking, system snapshots, and disaster recovery images.

---

## 3. Skill & Agent Architecture

### Skill Specification (`SKILL.md`)
Every skill within `02_SKILLS` must comply with the official Antigravity specification:
- **YAML Frontmatter**: Exactly `name` (lowercase-kebab-case) and `description` (third-person trigger specification).
- **Concise Body**: Quick execution procedure in the root `SKILL.md`.
- **Progressive Depth**: In-depth specifications placed in `./references/`, automation tools in `./scripts/`, and examples in `./examples/`.

### Agent Federation & Runtime Execution Engine
Agents operate under the principle of **least privilege and explicit delegation**:
- **Master Orchestrator (`03_AI_AGENTS/orchestrator/`)**: Decomposes complex tasks into subtask DAGs, selects agents, manages artifact handoffs, and writes verified run ledgers.
- **Task Sandbox (`03_AI_AGENTS/sandbox/`)**: Executes code, commands, and tests in ephemeral task worktrees (`03_AI_AGENTS/sandbox/tasks/<task_id>/`). Prevents path traversal via unconditional `realpath` checks (blocking directory junction and symlink write-escapes), rejects UNC paths, Alternate Data Streams, and DOS device names. Resolves binaries absolutely to prevent CWD binary hijacking. Scrubs sensitive environment variables (passwords, tokens, `USERPROFILE`, `APPDATA`), enforces mandatory timeouts with Windows process-tree kill (`taskkill /F /T /PID`), enforces default offline network isolation (proxy poisoning and Python socket connect interception), restricts Git commands to safe local operations, and logs all subprocess actions to `SUBPROCESS_AUDIT.jsonl`.
- **Human Approval Engine & Trust Classification (`03_AI_AGENTS/approval_engine/`)**: Enforces state machine transitions (`PROPOSED` $\rightarrow$ `REVIEW_REQUIRED` $\rightarrow$ `APPROVED` $\rightarrow$ `EXECUTING` $\rightarrow$ `VERIFIED` $\rightarrow$ `COMPLETED`) and a formal 5-Tier Execution Trust Level model (LEVEL 0 Read-Only to LEVEL 4 Host/Global). Issues task-bound approval tokens (`AUTH-<task_id>-<token>`) with TTL enforcement. Blocks high-risk triggers (global `.gemini` paths, MCP configs, paid APIs, external Git remotes), prevents agent self-approval and self-escalation, and secures ledger concurrency with Windows `msvcrt` file locking, atomic writes, and auto-backup/recovery.
- **Base Specialist Agent Hardening (`03_AI_AGENTS/agents/base_agent.py`)**: Centralizes authorization checking before tool execution; fails closed (`AUTHORIZATION_DENIED`) on missing, expired, or cross-task tokens.
- **Antigravity Native Subagent Bridge (`ant_subagent_bridge.py`)**: Exports subagent definitions for Antigravity's native `define_subagent` and `invoke_subagent` session delegation, enabling empirically verified Dual-Mode execution (IDE Interactive vs Headless Pipeline).
- **4 Capability Tiers**: Tier A (Documented) $\rightarrow$ Tier B (Configured) $\rightarrow$ Tier C (Runtime-Executable) $\rightarrow$ Tier D (Tested on Real Tasks in Sandbox).
- Subagents are spawned with targeted prompts, restricted toolsets, and scoped workspaces (`inherit`, `branch`, or `share`).

---

## 4. Antigravity Global Publishing Architecture

The publishing mechanism inside `22_PUBLISH_AND_DEPLOY` enforces a 6-step deployment lifecycle:

```
[Master AI Asset] 
       │
       ▼
1. Source Validation (Schema, Lint, Frontmatter check)
       │
       ▼
2. Conflict Detection (Inspect ~/.gemini/config/ for name collisions)
       │
       ▼
3. Automated Backup (Snapshot existing ~/.gemini/config/ state into 22_PUBLISH_AND_DEPLOY/backups/)
       │
       ▼
4. Human Approval Gate (Explicit user confirmation required)
       │
       ▼
5. Atomic Deployment (Copy approved artifacts into ~/.gemini/config/)
       │
       ▼
6. Health Verification & Rollback Protection
```

---

## 5. Full-Stack Engineering Standards Layer

Phase 5 establishes a modular standards library in `05_DEVELOPMENT/standards/` governed by `STANDARDS_REGISTRY.json`:
- **STD-001 Software Architecture**: Three-Tier Decoupled, Domain-Driven Design, Monolith vs Microservices criteria, ADRs.
- **STD-002 Frontend Engineering**: React 19, TypeScript strict mode (zero any), state management tiers, WCAG 2.2 AAA accessibility.
- **STD-003 Backend Engineering**: Node.js LTS, Express, RESTful OpenAPI 3.1, structured JSON logging (Pino), RFC 7807 error envelopes.
- **STD-004 Database Engineering**: PostgreSQL primary, MongoDB secondary, ACID transactions, B-Tree/GIN indexing, expand/contract zero-downtime migrations.
- **STD-005 Mobile Engineering**: Capacitor cross-platform webview bridge, native Android Jetpack Compose, Keystore/Keychain secure storage, offline-first sync.
- **STD-006 Security Engineering**: OWASP Top 10 defenses, Secret-Zero rules, JWT/session handling, CSRF/CSP headers, automated SCA vulnerability scanning.
- **STD-007 Testing and QA**: 4-Tier testing pyramid, 80% coverage threshold on business logic, deterministic mocks, boundary assertions.
- **STD-008 DevOps & Deployment**: Trunk-based Git workflow, multi-stage Docker builds, non-root users, blue-green / canary rollouts.

---

## 6. Universal UI/UX Design System

Consists of token-driven styling and accessible component specifications in `06_UI_UX_DESIGN/`:
- **Token Taxonomy** (`tokens/DESIGN_TOKENS.json`): 8 categories (colors, typography, spacing, breakpoints, radii, shadows, motion, z-indices).
- **Universal Specification** (`design_systems/UNIVERSAL_DESIGN_SYSTEM.md`): WCAG 2.2 AAA standards, 44x44px touch targets, 7-state component modeling (`idle`, `hover`, `focus-visible`, `active`, `loading`, `disabled`, `error`), and responsive mobile-first grids.
- **Component Registry** (`design_systems/DESIGN_SYSTEM_REGISTRY.json`): Machine-readable inventory of Buttons, Inputs, Cards, Modals, Toasts, Tables, and Navigation headers.

---

## 7. LLM Integration Readiness Architecture (LIRA)

Defines vendor-independent model abstractions in `04_LLM_AND_AI/`:
- **Unified LLM Gateway**: Standard `BaseLLMClient` protocol decoupling agents from proprietary cloud SDKs.
- **Model Registry** (`models/MODEL_REGISTRY.json`): Catalogs model metadata, context window budgets, token pricing, and offline capability flags.
- **Prompt Catalog** (`prompts/PROMPT_CATALOG.json`): Version-controlled system prompts for all 7 specialist agents.
- **Zero Paid API Invariant**: Hard financial spending limit default of \$0.00 USD with a fail-closed offline mock (`OfflineMockProvider`).
