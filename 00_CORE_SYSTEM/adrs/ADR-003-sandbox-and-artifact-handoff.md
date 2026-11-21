# ADR-003: Safe Subprocess Execution Sandbox and Artifact Handoff

> **Status**: ACCEPTED  
> **Date**: 2026-11-17  
> **Deciders**: MASTER-AI Lead Architect, Security Auditor  

---

## 1. Context
Executing code, running tests, and generating files directly in the main workspace presents serious risks of accidental overwrite, state corruption, and test pollution. An isolated runtime execution boundary is essential.

## 2. Decision
We implement a dedicated `TaskSandbox` subsystem:
1. **Isolated Task Root**: Every task executes in an ephemeral directory (`03_AI_AGENTS/sandbox/tasks/<task_id>/`).
2. **Path Traversal Guards**: Verifies all reads/writes stay within the task sandbox; forbids access targeting global configurations (`~/.gemini`).
3. **Subprocess Whitelisting**: Only whitelisted executables (`python`, `node`, `git`) are permitted with mandatory execution timeouts (15-30s).
4. **Artifact Handoff Integrity**: Computes SHA-256 digests for all generated artifacts and transfers them via typed handoff schemas.

## 3. Alternatives Considered
- Docker containerization: Rejected for local workspace execution on Windows 11 due to daemon startup latency and dependency on external Docker desktop.
- In-place workspace file modification: Rejected due to risk of untracked changes and difficult rollback.

## 4. Consequences
- **Positive**: Zero risk to root workspace; disposable workspaces; verified file hashes on handoff.
- **Negative**: Files must be explicitly collected or transferred between subtasks.
