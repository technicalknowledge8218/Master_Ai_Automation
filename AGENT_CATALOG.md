# MASTER-AI Specialized Agent Catalog

> **Orchestration Model**: Multi-Agent Federation & Scoped Delegation  
> **Source Location**: `03_AI_AGENTS/`  

---

## 1. Federation Principles

1. **Role Specialization**: Each agent possesses an explicit mandate, restricted toolset, and strict operational boundaries.
2. **Deterministic Delegation**: The Master Architect delegates tasks to specialized agents rather than executing every domain single-handedly.
3. **Least Privilege**: Agents are granted only the tools and read/write scopes required for their specialization.
4. **Dual-Check Quality**: High-risk deliverables must be reviewed by the Code Reviewer or Security Auditor before landing.

---

## 2. Specialized Roster (18 Personas)

| # | Agent Designation | Category | Primary Mandate & Scope |
| :--- | :--- | :--- | :--- |
| 1 | **Master Architect** | Orchestration | Global system architecture, cross-agent coordination, and roadmap oversight |
| 2 | **Technical Researcher** | Intelligence | Fact verification, official doc exploration, academic papers, and benchmarking |
| 3 | **AI Engineer** | Core AI | Model evaluations, fine-tuning, context optimization, and computer vision |
| 4 | **Agent Engineer** | Multi-Agent | Designing agent swarms, subagents, prompt chains, and delegation protocols |
| 5 | **Frontend Engineer** | Engineering | React, TypeScript, client-side performance, CSS, and modern web applications |
| 6 | **Backend Engineer** | Engineering | APIs, server architecture, databases, microservices, and distributed caching |
| 7 | **UI/UX Designer** | Creative | Visual design systems, atomic components, micro-interactions, and accessibility |
| 8 | **Mobile Engineer** | Engineering | Android, Jetpack Compose, Capacitor cross-platform apps, and mobile SDKs |
| 9 | **Database Architect** | Data | Relational schemas, query optimization, migrations, and vector index tuning |
| 10 | **Security Auditor** | Governance | Static analysis, OWASP scanning, secret audits, and compliance verification |
| 11 | **QA Engineer** | Quality | Test strategy, unit/integration/E2E test authoring, and regression suites |
| 12 | **DevOps Engineer** | Operations | CI/CD pipelines, Docker containerization, cloud deployment, and infrastructure |
| 13 | **Automation Engineer** | Workflows | n8n orchestration, webhooks, cron schedulers, and API integrations |
| 14 | **Content Director** | Media | Long-form documentary storytelling, narrative structure, and scriptwriting |
| 15 | **Video Production Specialist** | Media | Video editing protocols, B-roll curation, pacing, and audio mastering |
| 16 | **Social Media Manager** | Growth | Multi-platform distribution, channel analytics, and publishing schedule |
| 17 | **Documentation Engineer** | Knowledge | Architecture Decision Records (ADRs), guides, API references, and cataloging |
| 18 | **Code Reviewer** | Quality | Independent code review, adherence to coding standards, and refactoring |

---

## 3. Invocation & Collaboration Models
- **Single Agent Mode**: Direct execution for isolated, bounded tasks.
- **Hierarchical Delegation**: Master Architect assigns discrete sub-tasks to specialized subagents.
- **Swarm Mode**: Parallel execution across isolated workspaces with shared message-board synthesis.

---

## 4. Agent Capability Tiers & Runtime Status

| Tier | Status | Meaning & Criteria | Current Count |
| :---: | :---: | :--- | :---: |
| **Tier A** | Documented | Persona and scope documented in catalog | 18 |
| **Tier B** | Configured | Typed JSON schema in `03_AI_AGENTS/definitions/` | 7 |
| **Tier C** | Runtime-Executable | Python runner in `03_AI_AGENTS/agents/` + `define_subagent` registration | 7 |
| **Tier D** | Tested on Real Tasks | Empirically verified across 9 isolated sandbox test scenarios | 7 |

### Active Tier D Operational Agents:
1. `AGT-001` **Research Agent**: Empirical research, package validation, citations.
2. `AGT-002` **Software Architect**: Modular architecture, three-tier decoupling, system spec.
3. `AGT-003` **Coding Agent**: Type-safe Python/TypeScript, PEP 8, zero secrets.
4. `AGT-004` **Testing Agent**: Unit and integration test suites, assertions, coverage.
5. `AGT-005` **Documentation Agent**: Architecture Decision Records (ADRs), markdown manifests.
6. `AGT-006` **Security Auditor**: Zero-secret audit, AST safety scan (`eval`, `exec`), boundary audit.
7. `AGT-007` **Capability Discovery Agent**: 30-domain horizon scanning and gap assessment.

Execution Dashboard: [AGENT_DASHBOARD.md](file:///c:/Users/Sangam/Desktop/Master%20AI/03_AI_AGENTS/dashboard/AGENT_DASHBOARD.md)  
Execution Standard: [AGENT_EXECUTION_STANDARD.md](file:///c:/Users/Sangam/Desktop/Master%20AI/AGENT_EXECUTION_STANDARD.md)
