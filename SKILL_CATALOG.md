# MASTER-AI Modular Skill Catalog & Governance Matrix

> **Format Standard**: Antigravity `SKILL.md` Specification  
> **Source Directory**: `02_SKILLS/`  
> **Governance Standard**: `02_SKILLS/SKILL_DEVELOPMENT_STANDARD.md`  

---

## 1. Skill Maturity Lifecycle & Scopes

Skills advance through a 6-stage maturity pipeline:
```
DISCOVERED ──> RESEARCHED ──> IMPLEMENTED ──> TESTED ──> APPROVED ──> PUBLISHED
```

### Stage Definitions & Evidence Requirements:
- **DISCOVERED**: Identified as a capability requirement in `CAPABILITY_REGISTRY.json`.
- **RESEARCHED**: Official vendor documentation, APIs, and edge cases verified.
- **IMPLEMENTED**: `SKILL.md`, references, and examples physically authored.
- **TESTED**: Validated via automated scripts and negative test suites in `18_TESTING_AND_QA/`.
- **APPROVED**: Formally reviewed and signed off against the Master AI Quality Gate.
- **PUBLISHED**: Deployed to designated runtime scope (Workspace or Global).

---

## 2. Prioritized 5-Level Skill Roadmap

### Level 1: Foundational Intelligence & Engineering (Core Prerequisites)
| Skill Identifier | Category | Maturity Status | Workspace Scope | Global Scope | Scope & Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `technical-research` | Research | **APPROVED** | **PUBLISHED** | Unapproved | Anti-hallucination tech evaluation & official API verification |
| `prompt-engineering` | AI/Prompt | **TESTED** | **PUBLISHED** | Unapproved | Structured output, few-shot conditioning & system prompts |
| `software-architecture` | Architecture | **TESTED** | **PUBLISHED** | Unapproved | System boundaries, domain separation & architectural patterns |
| `coding-standards` | Quality | **TESTED** | **PUBLISHED** | Unapproved | Modern TypeScript/Python strict style & zero-secret rules |
| `documentation-engineering`| Knowledge | **TESTED** | **PUBLISHED** | Unapproved | Architecture Decision Records (ADRs), guides & catalogs |
| `capability-research` | Intelligence | **TESTED** | **PUBLISHED** | Unapproved | Capability discovery, readiness scoring & gap analysis |

### Level 2: AI, LLM & Tool Integrations
| Skill Identifier | Category | Maturity Status | Workspace Scope | Global Scope | Scope & Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ai-engineering` | Core AI | DRAFT | Unassigned | Unassigned | Machine learning workflows, model benchmarking & inference |
| `llm-engineering` | Core AI | DRAFT | Unassigned | Unassigned | Token optimization, context window management & structured outputs |
| `rag-engineering` | RAG/Data | DRAFT | Unassigned | Unassigned | Hybrid dense/sparse search, chunking & reranking pipelines |
| `agent-development` | Agents | DRAFT | Unassigned | Unassigned | Autonomous agent lifecycles, memory & tool execution |
| `mcp-development` | Protocols | DRAFT | Unassigned | Unassigned | Model Context Protocol servers, stdio schemas & security |

### Level 3: Full-Stack Engineering, UI/UX & Mobile
| Skill Identifier | Category | Maturity Status | Workspace Scope | Global Scope | Scope & Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `frontend-engineering` | Development | DRAFT | Unassigned | Unassigned | React 19, TypeScript strict mode, state & web performance |
| `backend-engineering` | Development | DRAFT | Unassigned | Unassigned | Fastify, FastAPI, REST/GraphQL microservices & caching |
| `database-engineering` | Data | DRAFT | Unassigned | Unassigned | PostgreSQL, pgvector, Redis caching & relational modeling |
| `ui-ux-design` | Design | DRAFT | Unassigned | Unassigned | Modern design tokens, WCAG 2.2 AAA accessibility & CSS |
| `mobile-development` | Mobile | DRAFT | Unassigned | Unassigned | Android native (Compose), Capacitor & cross-platform apps |

### Level 4: Multi-Agent Systems, Automation & Security
| Skill Identifier | Category | Maturity Status | Workspace Scope | Global Scope | Scope & Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `multi-agent-orchestration`| Swarms | DRAFT | Unassigned | Unassigned | Swarms, coordinator-worker topologies & subagent briefs |
| `automation-engineering` | Automation | DRAFT | Unassigned | Unassigned | n8n workflow construction, webhooks & background cron jobs |
| `security-engineering` | Security | DRAFT | Unassigned | Unassigned | OWASP Top 10, secret-zero audits & threat modeling |
| `testing-and-qa` | Quality | DRAFT | Unassigned | Unassigned | Vitest, PyTest, Playwright E2E & automated quality gates |
| `devops-engineering` | Operations | DRAFT | Unassigned | Unassigned | Docker, GitHub Actions CI/CD & cloud infrastructure |

### Level 5: Media Production & Social Media Growth
| Skill Identifier | Category | Maturity Status | Workspace Scope | Global Scope | Scope & Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `documentary-production` | Media | DRAFT | Unassigned | Unassigned | Narrative structuring, research scripting & storyboarding |
| `ai-video-generation` | Media | DRAFT | Unassigned | Unassigned | Text-to-video generation, image reference & motion synthesis |
| `social-media-automation`| Distribution | DRAFT | Unassigned | Unassigned | Multi-channel publishing queues & post analytics |
| `multi-platform-publishing`| Distribution | DRAFT | Unassigned | Unassigned | YouTube, Instagram, Telegram & X API publishing connectors |

---

## 3. Skill Development Rules
1. Before authoring any skill, check this catalog to prevent duplicate work.
2. Follow the standard template in `17_TEMPLATES/skills/SKILL_TEMPLATE.md`.
3. Test every script inside `scripts/` before advancing to `APPROVED`.
4. Global deployment requires an explicit user approval report following `22_PUBLISH_AND_DEPLOY/APPROVAL_WORKFLOW.md`.
