---
name: capability-research
description: >-
  Discovers, benchmarks, and audits AI capabilities across the 30 master domains, identifies
  tool and skill gaps in the MASTER-AI ecosystem, and evaluates feasibility against hardware
  and API limits. Use when assessing missing capabilities or evaluating new AI modalities.
---

# Capability Research & Gap Analysis Skill

> **Status**: IMPLEMENTED & TESTED (Workspace)  
> **Version**: 1.0.0  
> **Domain**: DOM-30 (Emerging AI Technologies)  

---

## 1. Purpose & Scope
This skill provides an empirical framework to audit whether a proposed AI capability (e.g., video editing, voice cloning, local fine-tuning) is feasible within local hardware, API quotas, and security boundaries.

## 2. When to Use This Skill
- When an agent or user proposes expanding MASTER-AI into a new capability domain.
- When performing quarterly audits of capability readiness.
- When evaluating whether a task can be done locally or requires cloud infrastructure.

## 3. Required Inputs
- Target capability description.
- Hardware specifications (CPU, RAM, GPU VRAM, OS).
- API keys, quota constraints, and estimated monthly cost limits.

## 4. Execution Workflow

### Step 1: Evaluate Feasibility Criteria
Review [CAPABILITY_EVALUATION_CRITERIA.md](./references/CAPABILITY_EVALUATION_CRITERIA.md). Classify into:
- Fully Achievable (zero new external costs/tools).
- Achievable with External Tools (requires API or CLI tool).
- Partially Achievable (functional limits exist).
- Currently Infeasible (unsupported by current technology or hardware).

### Step 2: Automated Gap Evaluation
Run the gap evaluator script against the registry:
```powershell
python 02_SKILLS/capability-research/scripts/evaluate_capability_gap.py --domain "DOM-10"
```

### Step 3: Verification Checklist
- [ ] Hardware bottlenecks (VRAM/RAM) are documented.
- [ ] Third-party API pricing and quota constraints are calculated.
- [ ] Security and data privacy implications are assessed.
- [ ] Test reproduction steps are provided.
