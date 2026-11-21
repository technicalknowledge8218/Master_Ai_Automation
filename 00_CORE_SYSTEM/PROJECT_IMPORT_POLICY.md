# MASTER-AI Project Knowledge Import Policy

> **Objective**: Safe, Sanitized Knowledge Ingestion from External Projects  
> **Source Directory**: `00_CORE_SYSTEM/` & `20_PROJECTS/`  

---

## 1. Ingestion Philosophy

Future external projects (web applications, mobile apps, automation pipelines) will discover novel, high-value patterns. MASTER-AI must harvest these insights without polluting the central repository with project-specific debris, customer secrets, or brittle assumptions.

> [!CAUTION]
> **Never Import Entire Repositories Blindly.**  
> Blindly copying an entire project codebase into MASTER-AI degrades repository quality, introduces untracked dependencies, and risks leaking sensitive data.

---

## 2. The 7-Step Import Workflow

When an AI agent operating in any project discovers a reusable pattern, it must follow this 7-step protocol:

```
[1. Identify Pattern] ──> [2. Redundancy Check] ──> [3. Sanitize Secrets]
                                                            │
[6. Local Approval]   <── [5. Propose Skill/Doc] <── [4. Create Knowledge]
       │
       v
[7. Separate Global Approval (If applicable)]
```

### Step Breakdown:
1. **Identify Reusable Pattern**: Pinpoint the generic, reusable core (e.g., an advanced TanStack Query caching pattern, a resilient WebSocket reconnect strategy).
2. **Redundancy Check**: Search `00_CORE_SYSTEM/registry/KNOWLEDGE_INDEX.md` and `SKILL_CATALOG.md`. If the concept already exists, determine whether this is an incremental update or an edge-case note.
3. **Sanitize Secrets & Project Specifics**:
   - Strip all client identifiers, company names, and internal URLs.
   - Replace project-specific variables with generic parameters.
   - Run entropy checks to guarantee zero leaked tokens or keys.
4. **Create Reusable Knowledge Entry**: Draft a standardized entry in `21_LEARNING_LAB/notes/` using [KNOWLEDGE_TEMPLATE.md](../17_TEMPLATES/docs/KNOWLEDGE_TEMPLATE.md).
5. **Propose Skill or Boilerplate Update**:
   - If procedural: Propose a new or updated skill in `02_SKILLS/`.
   - If algorithmic: Propose adding the sanitized utility to `14_CODE_LIBRARY/`.
6. **Request Workspace Approval**: Ask the user for confirmation before committing the new asset to MASTER-AI.
7. **Separate Global Evaluation**: If the knowledge represents a universal skill candidate, submit it to the separate [Approval Workflow](../22_PUBLISH_AND_DEPLOY/APPROVAL_WORKFLOW.md). Never bundle local and global approvals into one request.
