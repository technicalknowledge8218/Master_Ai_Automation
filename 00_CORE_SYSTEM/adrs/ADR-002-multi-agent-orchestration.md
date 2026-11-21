# ADR-002: Multi-Agent Federation & Scoped Runtime Orchestration

> **Status**: ACCEPTED  
> **Date**: 2026-11-17  
> **Deciders**: MASTER-AI Lead Architect, Security Auditor  

---

## 1. Context
To scale beyond single-turn prompt interactions, MASTER-AI requires a multi-agent federation where specialized agents (Research, Architecture, Coding, Testing, Documentation, Security, Capability Discovery) execute discrete tasks within defined boundaries, exchange typed artifacts, and report back to an overarching orchestrator.

## 2. Decision
We implement a hybrid orchestration model:
1. **Workspace-Local Orchestrator (`MasterOrchestrator`)**: Coordinates execution through DAG subtask decomposition, sandbox isolation, and structured ledger recording.
2. **Antigravity Native Subagent Bridge (`ant_subagent_bridge.py`)**: Exports subagent definitions into Antigravity's native `define_subagent` and `invoke_subagent` runtime system.
3. **Structured Communication**: Enforces strict JSON contracts for task requests, responses, and inter-agent handoffs without relying on third-party dependencies.

## 3. Alternatives Considered
- Monolithic Single-Agent Execution: Rejected because complex multi-domain tasks suffer from context drift and lack independent security/test verification.
- Direct Unsandboxed Tool Execution: Rejected due to risk of unauthorized filesystem modifications and secret leaks.

## 4. Consequences
- **Positive**: Clear separation of concerns; deterministic task routing; verifiable audit logs in execution ledgers.
- **Negative**: Subprocess spawning introduces slight execution overhead (~0.9s per 6-agent lifecycle run).
