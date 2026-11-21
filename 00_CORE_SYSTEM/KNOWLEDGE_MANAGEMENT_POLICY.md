# MASTER-AI Knowledge Management Policy & Engine

> **Standard**: Rigorous Knowledge Lifecycle & Epistemic Classification  
> **Source Directory**: `00_CORE_SYSTEM/` & `21_LEARNING_LAB/`  

---

## 1. The 8-Stage Knowledge Lifecycle

Every concept, architectural pattern, library evaluation, and operational insight in MASTER-AI moves through a deterministic 8-stage lifecycle:

```
[1. DISCOVER] ──> [2. RESEARCH] ──> [3. VERIFY] ──> [4. DOCUMENT]
       │
       v
[5. CLASSIFY] ──> [6. REVIEW]   ──> [7. APPROVE] ──> [8. PUBLISH]
```

### Stage Definitions:
1. **DISCOVER**: Identify an emerging technology, novel design pattern, recurring bug solution, or workflow optimization.
2. **RESEARCH**: Investigate official vendor documentation, specification RFCs, source repositories, and release changelogs.
3. **VERIFY**: Execute an empirical sandbox test, code reproduction, or benchmark confirming that the behavior matches official documentation.
4. **DOCUMENT**: Structure the verified findings using the standard [KNOWLEDGE_TEMPLATE.md](../17_TEMPLATES/docs/KNOWLEDGE_TEMPLATE.md).
5. **CLASSIFY**: Assign the entry to an authoritative epistemic category and define its domain boundaries.
6. **REVIEW**: Perform peer or agent verification checking for duplicate concepts in `SKILL_CATALOG.md` and `KNOWLEDGE_INDEX.md`.
7. **APPROVE**: Final review confirming code safety, absence of hardcoded secrets, and clarity.
8. **PUBLISH**: Graduate the record to the Master Repository (`13_MARKDOWN/`, `14_CODE_LIBRARY/`, or `02_SKILLS/`).

---

## 2. Knowledge Categories

Every recorded knowledge artifact must be assigned to exactly one of the following 6 epistemic categories:

| Category | Definition | Verification Requirement | Storage Path |
| :--- | :--- | :--- | :--- |
| **Verified Knowledge** | Fully validated facts, syntax, and behaviors backed by current official docs or passing tests | 100% test pass or official specification citation | `13_MARKDOWN/guides/` or `02_SKILLS/` |
| **Experimental Knowledge** | Novel approaches, alpha/beta framework features, or performance optimizations under evaluation | Empirical test script output logged in `21_LEARNING_LAB` | `21_LEARNING_LAB/experiments/` |
| **Research Notes** | Synthesized findings, architecture trade-offs, and literature summaries | Primary sources cited with access dates | `11_RESEARCH_LAB/tech_evaluations/` |
| **Deprecated Knowledge** | Superseded APIs, obsolete patterns, or security-vulnerable libraries | Breaking change notes and migration guide linked | `13_MARKDOWN/summaries/deprecated/` |
| **Unverified Claims** | Marketing claims, theoretical benchmarks, or community forum suggestions pending validation | Explicitly labeled as UNVERIFIED | `21_LEARNING_LAB/notes/` |
| **Reusable Engineering Patterns**| Battle-tested code architectures, microservice boilerplates, and design token setups | Code passes linting, type-checking, and unit tests | `14_CODE_LIBRARY/` |

---

## 3. Mandatory Knowledge Record Schema

Every formal knowledge document must provide the following structured metadata fields:

```yaml
---
id: KNOW-YYYY-NNN               # Unique sequential ID (e.g., KNOW-2026-001)
topic: "Clear Descriptive Title"
category: "Verified Knowledge"   # One of the 6 categories above
technology: "Technology Name"
technology_version: "X.Y.Z"
verification_status: "VERIFIED" # VERIFIED | EXPERIMENTAL | DEPRECATED | UNVERIFIED
source_urls:
  - "https://official-docs.example.com/api"
source_access_date: "YYYY-MM-DD"
last_reviewed_date: "YYYY-MM-DD"
related_skills:
  - "technical-research"
limitations:
  - "Specific constraint or environment boundary"
---
```

---

## 4. Anti-Redundancy & Maintenance Rules

1. **Query Before Creating**: Before drafting a knowledge document, query `00_CORE_SYSTEM/registry/KNOWLEDGE_INDEX.md`. If a record exists, update it rather than creating a duplicate.
2. **Quarterly Stale-Check**: Knowledge records older than 180 days must be flagged for re-verification against latest release notes.
3. **Deprecation over Deletion**: Do not delete superseded knowledge. Reclassify it as `Deprecated Knowledge` and provide an explicit pointer to the replacement standard to prevent recurring regressions.
