# MASTER-AI Sovereign Rulebook & Operating Laws

> **Authority**: Inviolable System Laws  
> **Enforcement**: Mandatory for all AI agents, subagents, and human contributors  

---

## Law 1: Research Before Implementation (The Anti-Hallucination Law)

1. **Verify Before Coding**: Never invent API endpoints, library functions, class names, or package versions.
2. **Official Documentation First**: Prioritize current official documentation, vendor specifications, and RFC standards over general assumptions.
3. **Check Version & Release Date**: Before recommending or utilizing a technology, check its active version, release date, and breaking changes.
4. **Distinguish Epistemic States**: Clearly distinguish between:
   - **Verified Facts**: Backed by official docs or successful test execution.
   - **Hypotheses / Assumptions**: Explicitly labeled as requiring empirical testing.
   - **Experimental Findings**: Recorded with reproduction steps and logs.
5. **Citations Required**: When introducing external patterns or tools, record the source URL, access date, and evaluated limitations.

---

## Law 2: Modern Coding & Architecture Standards

1. **Clean & Scalable Code**: Write clean, modular, self-documenting code adhering strictly to modern language standards (e.g., TypeScript strict mode, Python PEP 8 / type hints).
2. **No Overengineering**: Solve the concrete problem with the simplest robust architecture. Avoid premature microservice decomposition or excessive abstractions.
3. **Preservation of Working Code**: Never silently rewrite, overwrite, or delete working code without:
   - Inspecting existing functionality.
   - Creating an explicit rollback / recovery point.
   - Explaining the technical rationale for modification.
4. **Zero-Defect Quality Gates**: All code must include appropriate unit tests, input validation, error handling, and structured logging.
5. **Separation of Concerns**: Strictly isolate UI, business logic, data access, and external integrations.

---

## Law 3: Secret-Zero & Security Mandates

1. **No Hardcoded Secrets**: Under no circumstances may API keys, passwords, bearer tokens, or private certificates be written into code or committed to Git.
2. **Environment Isolation**: All credentials must be ingested via environment variables or secret vaults.
3. **Principle of Least Privilege**: Agents and tools must only receive the permissions necessary for their immediate task.
4. **OWASP Top 10 Compliance**: Defend by default against injection, broken access control, cross-site scripting, and insecure deserialization.
5. **Dependency Hygiene**: Regularly scan dependencies for known CVEs. Never install unmaintained, unvetted packages.

---

## Law 4: Systematic Learning & Continuous Improvement

1. **Knowledge Persistence**: When a new technology, design pattern, or solution is discovered:
   - Understand the mechanism.
   - Verify it via empirical trial or authoritative reference.
   - Record findings in `21_LEARNING_LAB`.
   - Distill actionable instructions into `02_SKILLS`.
   - Update `LEARNING_PROGRESS.md`.
2. **No False Mastery Claims**: An agent must never claim to have learned something permanently unless the asset has been written to disk in MASTER-AI.
3. **No Redundancy**: Before creating any new skill or documentation, inspect `SKILL_CATALOG.md` to prevent duplication.

---

## Law 5: Human Sovereignty & Permission Gates

The following actions **ALWAYS require explicit human approval**:
- Publishing content to public social media channels.
- Deleting or modifying global Antigravity configurations (`~/.gemini/config/`).
- Deleting production databases, cloud resources, or git repository history.
- Executing destructive or irreversible filesystem commands.
- Installing untrusted third-party binaries or network listeners.
