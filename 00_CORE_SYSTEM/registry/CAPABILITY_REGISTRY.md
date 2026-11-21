# MASTER-AI Sovereign Capability Registry

> **Registry Version**: `1.0.0`  
> **Last Synchronized**: `2026-11-17`  
> **Source File**: `00_CORE_SYSTEM/registry/CAPABILITY_REGISTRY.json`  

---

## 1. Registry Summary Metrics

- **Total Capability Domains**: 30
- **Total Tracked Skills**: 12
- **Total Specialized Agents**: 7
- **Total Host MCP Servers**: 8
- **Curated GitHub Repositories**: 20

---

## 2. Capability Domains Matrix (30 Master Domains)

| Domain ID | Domain Designation | Category | Status |
| :--- | :--- | :--- | :--- |
| `DOM-01` | **LLMs and Foundation Models** | Core AI | `active` |
| `DOM-02` | **Prompt Engineering and Context Engineering** | Core AI | `active` |
| `DOM-03` | **RAG and Knowledge Systems** | AI Systems | `active` |
| `DOM-04` | **AI Agents and Multi-Agent Systems** | Autonomous Systems | `active` |
| `DOM-05` | **Skills and Agent Frameworks** | Frameworks | `active` |
| `DOM-06` | **MCP and Tool Calling** | Integration | `active` |
| `DOM-07` | **Software and Web Development** | Engineering | `active` |
| `DOM-08` | **Android and Cross-Platform Apps** | Engineering | `active` |
| `DOM-09` | **UI/UX and Graphic Design** | Design | `active` |
| `DOM-10` | **Video Creation and Editing** | Media | `active` |
| `DOM-11` | **Documentary and Reels Production** | Media | `active` |
| `DOM-12` | **Image Generation and Editing** | Media | `active` |
| `DOM-13` | **Voice, Audio and Music Production** | Media | `active` |
| `DOM-14` | **Social Media Management** | Growth | `active` |
| `DOM-15` | **YouTube Automation** | Growth | `active` |
| `DOM-16` | **Instagram and Facebook Automation** | Growth | `active` |
| `DOM-17` | **Telegram, X and Other Platform Integrations** | Growth | `active` |
| `DOM-18` | **Multi-Platform Publishing** | Automation | `active` |
| `DOM-19` | **Browser Automation and Computer Use** | Automation | `active` |
| `DOM-20` | **Business Process Automation** | Automation | `active` |
| `DOM-21` | **Research and Data Analysis** | Intelligence | `active` |
| `DOM-22` | **Cybersecurity and Privacy** | Security | `active` |
| `DOM-23` | **Software Testing and Quality Assurance** | Quality | `active` |
| `DOM-24` | **DevOps and Cloud Infrastructure** | Operations | `active` |
| `DOM-25` | **Marketing, SEO and Analytics** | Growth | `active` |
| `DOM-26` | **Business Operations and Customer Support** | Operations | `active` |
| `DOM-27` | **Document and Presentation Creation** | Productivity | `active` |
| `DOM-28` | **Learning and Educational Systems** | Education | `active` |
| `DOM-29` | **Robotics and IoT** | Emerging Tech | `active` |
| `DOM-30` | **Emerging AI Technologies** | Emerging Tech | `active` |

---

## 3. Skills Registry

| Skill ID | Skill Name | Path | Category | Maturity | Scope | Approval |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SKILL-001` | **technical-research** | `02_SKILLS/technical-research/SKILL.md` | Intelligence | `APPROVED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-002` | **prompt-engineering** | `02_SKILLS/prompt-engineering/SKILL.md` | Core AI | `TESTED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-003` | **software-architecture** | `02_SKILLS/software-architecture/SKILL.md` | Engineering | `TESTED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-004` | **coding-standards** | `02_SKILLS/coding-standards/SKILL.md` | Quality | `TESTED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-005` | **documentation-engineering** | `02_SKILLS/documentation-engineering/SKILL.md` | Productivity | `TESTED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-006` | **capability-research** | `02_SKILLS/capability-research/SKILL.md` | Intelligence | `TESTED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-007` | **frontend-engineering** | `02_SKILLS/frontend-engineering/SKILL.md` | Development | `APPROVED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-008` | **backend-engineering** | `02_SKILLS/backend-engineering/SKILL.md` | Development | `APPROVED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-009` | **database-engineering** | `02_SKILLS/database-engineering/SKILL.md` | Development | `APPROVED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-010` | **mobile-engineering** | `02_SKILLS/mobile-engineering/SKILL.md` | Development | `APPROVED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-011` | **api-engineering** | `02_SKILLS/api-engineering/SKILL.md` | Development | `APPROVED` | `workspace` | `APPROVED_LOCAL` |
| `SKILL-012` | **ui-ux-design** | `02_SKILLS/ui-ux-design/SKILL.md` | Design | `APPROVED` | `workspace` | `APPROVED_LOCAL` |

---

## 4. Specialized Agents Registry

| Agent ID | Agent Designation | Definition JSON | Spec Document | Category | Mode | Runtime Tier | Approval |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `AGT-001` | **Research Agent** | `03_AI_AGENTS/definitions/research_agent.json` | `03_AI_AGENTS/specialists/RESEARCH_AGENT.md` | Intelligence | `inherit` | `Tier D` | `APPROVED_LOCAL` |
| `AGT-002` | **Software Architect** | `03_AI_AGENTS/definitions/software_architect.json` | `03_AI_AGENTS/architect/SOFTWARE_ARCHITECT.md` | Architecture | `inherit` | `Tier D` | `APPROVED_LOCAL` |
| `AGT-003` | **Coding Agent** | `03_AI_AGENTS/definitions/coding_agent.json` | `03_AI_AGENTS/engineers/CODING_AGENT.md` | Engineering | `branch` | `Tier D` | `APPROVED_LOCAL` |
| `AGT-004` | **Testing Agent** | `03_AI_AGENTS/definitions/testing_agent.json` | `03_AI_AGENTS/engineers/TESTING_AGENT.md` | Quality | `inherit` | `Tier D` | `APPROVED_LOCAL` |
| `AGT-005` | **Documentation Agent** | `03_AI_AGENTS/definitions/documentation_agent.json` | `03_AI_AGENTS/specialists/DOCUMENTATION_AGENT.md` | Productivity | `inherit` | `Tier D` | `APPROVED_LOCAL` |
| `AGT-006` | **Security Auditor** | `03_AI_AGENTS/definitions/security_auditor.json` | `03_AI_AGENTS/specialists/SECURITY_AUDITOR.md` | Security | `inherit` | `Tier D` | `APPROVED_LOCAL` |
| `AGT-007` | **Capability Discovery Agent** | `03_AI_AGENTS/definitions/capability_discovery_agent.json` | `03_AI_AGENTS/specialists/CAPABILITY_DISCOVERY_AGENT.md` | Intelligence | `inherit` | `Tier D` | `APPROVED_LOCAL` |

---

## 5. Host MCP Servers Registry

| MCP ID | Server Identifier | Transport | Command / Endpoint | Host Status | Verified |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MCP-01` | **chrome-devtools-mcp** | `stdio` | `npx -y chrome-devtools-mcp@latest` | `CONFIGURED_HOST` | `True` |
| `MCP-02` | **cloudrun** | `stdio` | `npx -y @google-cloud/cloud-run-mcp` | `CONFIGURED_HOST` | `True` |
| `MCP-03` | **genkit-mcp-server** | `stdio` | `npx -y genkit-cli@^1.28.0 mcp` | `CONFIGURED_HOST` | `True` |
| `MCP-04` | **gmp-code-assist** | `sse` | `https://mapscodeassist.googleapis.com/mcp` | `CONFIGURED_HOST` | `True` |
| `MCP-05` | **google-home-developer** | `sse` | `https://homedevelopers.googleapis.com/mcp` | `CONFIGURED_HOST` | `True` |
| `MCP-06` | **playwright** | `stdio` | `npx -y @playwright/mcp@latest` | `CONFIGURED_HOST` | `True` |
| `MCP-07` | **get-shit-done** | `stdio` | `npx -y @gsd-build/mcp-server` | `CONFIGURED_HOST` | `True` |
| `MCP-08` | **gsd-task-manager** | `stdio` | `npx -y gsd-mcp-server` | `CONFIGURED_HOST` | `True` |

---

## 6. High-Priority GitHub Repositories Registry

| Repository | Category | Primary Domain | Stars (approx) | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| `langchain-ai/langgraph` | Agent Frameworks | `DOM-04` | ~18k | **REFERENCE** |
| `crewAIInc/crewAI` | Agent Frameworks | `DOM-04` | ~26k | **REFERENCE** |
| `microsoft/autogen` | Agent Frameworks | `DOM-04` | ~38k | **REFERENCE** |
| `All-Hands-AI/OpenHands` | Coding Agents | `DOM-04` | ~45k | **REFERENCE** |
| `Aider-AI/aider` | Coding Agents | `DOM-07` | ~28k | **REFERENCE** |
| `modelcontextprotocol/servers` | MCP | `DOM-06` | ~15k | **USE** |
| `modelcontextprotocol/python-sdk` | MCP | `DOM-06` | ~5k | **USE** |
| `qdrant/qdrant` | Vector DB | `DOM-03` | ~22k | **USE** |
| `pgvector/pgvector` | Vector DB | `DOM-03` | ~14k | **USE** |
| `vllm-project/vllm` | Local LLM | `DOM-01` | ~35k | **REFERENCE** |
| `ollama/ollama` | Local LLM | `DOM-01` | ~115k | **USE** |
| `n8n-io/n8n` | Automation | `DOM-20` | ~62k | **USE** |
| `microsoft/playwright` | Browser Automation | `DOM-19` | ~68k | **USE** |
| `shadcn-ui/ui` | UI/UX | `DOM-09` | ~75k | **USE** |
| `Remotion-dev/remotion` | Video Synthesis | `DOM-10` | ~22k | **TEST** |
| `openai/whisper` | Voice/Audio | `DOM-13` | ~72k | **USE** |
| `vitest-dev/vitest` | Testing | `DOM-23` | ~14k | **USE** |
| `trufflesecurity/trufflehog` | Security | `DOM-22` | ~17k | **USE** |
| `fastify/fastify` | Web Dev | `DOM-07` | ~33k | **USE** |
| `tiangolo/fastapi` | Web Dev | `DOM-07` | ~78k | **USE** |
