---
name: technical-research
description: >-
  Researches, benchmarks, and validates software technologies, libraries, and APIs against
  official documentation and specifications before implementation. Use whenever investigating
  a new technology, evaluating library versions, or verifying API capabilities.
---

# Technical Research Standard Skill

> **Status**: APPROVED (Workspace)  
> **Version**: 1.0.0  
> **Last Verified**: 2026-11-16  

---

## 1. Purpose & Scope
This skill governs the systematic, anti-hallucination research protocol for any software library, framework, AI model, or API proposed for the MASTER-AI ecosystem. It guarantees that no technology is adopted based on unverified assumptions or stale model training data.

## 2. When to Use This Skill
- When considering adding a new dependency or library to any project.
- When verifying the latest stable release and breaking changes of a framework.
- When an AI agent needs to confirm method signatures or API endpoints.
- When comparing competing technologies (e.g., pgvector vs Qdrant, Vite vs Next.js).
- **Do NOT use for**: Writing production application business logic (use domain-specific skills).

## 3. Required Inputs & Research Checklist
Before formulating any recommendation, collect:
1. Target technology name and package ecosystem (npm, PyPI, Crates, etc.).
2. The exact current stable version and release date from official sources.
3. The official documentation URL and source repository.
4. Active license (MIT, Apache 2.0, BSD, GPL, etc.).

## 4. Step-by-Step Execution Workflow

### Step 1: Query Official Documentation First
Always inspect Tier 1 sources before consulting community articles.
- Official API documentation.
- Official GitHub repository releases and tags.
- Official migration guides for major version upgrades.

### Step 2: Validate Version Metadata
Run the metadata verification helper script:
```powershell
python 02_SKILLS/technical-research/scripts/verify_tech_metadata.py --package "<package_name>" --ecosystem "<pypi|npm>"
```

### Step 3: Evaluate Against the 8 Research Criteria
Cross-reference your findings against [RESEARCH_EVALUATION_MATRIX.md](./references/RESEARCH_EVALUATION_MATRIX.md):
1. Current stable version vs latest pre-release.
2. Experimental features vs production-ready APIs.
3. Deprecated methods and migration paths.
4. Language and OS compatibility (Node LTS, Python 3.12+, Windows 11).
5. Dependency weight and vulnerability history (CVE scan).
6. License compatibility with Master AI principles.
7. Active maintainer cadence and commit velocity.
8. Concrete reproduction or benchmark script.

### Step 4: Record Findings in Master Knowledge Engine
1. Formulate a structured research report using [KNOWLEDGE_TEMPLATE.md](../../17_TEMPLATES/docs/KNOWLEDGE_TEMPLATE.md).
2. Save the report in `11_RESEARCH_LAB/tech_evaluations/` or `21_LEARNING_LAB/notes/`.
3. Register the new knowledge ID in `00_CORE_SYSTEM/registry/KNOWLEDGE_INDEX.md`.

## 5. Verification Checklist
- [ ] Official documentation URL is recorded and functional.
- [ ] Current stable version number verified from official package registry.
- [ ] Tested compatibility on Windows 11 / target platform.
- [ ] Checked for security alerts and open CVEs.
- [ ] Output documented and indexed in MASTER-AI.

## 6. Common Pitfalls & Antipatterns
- **Stale Memory Trap**: Recommending an API or version from training data without checking current docs.
- **Marketing vs Reality**: Treating vendor marketing claims or benchmark graphs as verified truth without running an empirical trial.
- **Ignoring License Restrictions**: Adopting AGPL or non-commercial licensed code without user consent.
