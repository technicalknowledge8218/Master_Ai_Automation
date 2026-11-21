# ADR-004: Deterministic Human Approval Gatekeeper Engine

> **Status**: ACCEPTED  
> **Date**: 2026-11-17  
> **Deciders**: MASTER-AI Lead Architect, Security Auditor  

---

## 1. Context
Autonomous multi-agent systems risk executing unintended destructive or global actions (deploying global skills, modifying host configs, pushing to remote repositories, or executing paid APIs) without human knowledge or consent.

## 2. Decision
We implement a state machine-driven `HumanApprovalEngine`:
1. **Deterministic State Machine**:
   `PROPOSED` $\rightarrow$ `REVIEW_REQUIRED` $\rightarrow$ `APPROVED` $\rightarrow$ `EXECUTING` $\rightarrow$ `VERIFIED` $\rightarrow$ `COMPLETED`  
   with terminal states `REJECTED`, `FAILED`, and `ROLLED_BACK`.
2. **Automatic High-Risk Interception**: Any operation touching global paths (`.gemini`), MCP configurations, paid APIs, external Git remotes, or destructive commands automatically transitions to `REVIEW_REQUIRED`.
3. **Task-Bound Authorization Tokens**: Approval granted for task X generates a unique cryptographic token `AUTH-<task_id>-<uuid>` that cannot be reused for any other task.

## 3. Alternatives Considered
- Blanket user pre-approval: Rejected because broad pre-authorizations allow agents to escape boundaries on subsequent tasks.
- Prompt-only instruction ("Please don't modify global config"): Rejected because LLM prompt instructions can fail or be hallucinated; programmatic gatekeeping is mandatory.

## 4. Consequences
- **Positive**: Absolute protection against unauthorized global changes, data loss, and external publishing.
- **Negative**: High-risk tasks must pause and wait for explicit human review before execution.
