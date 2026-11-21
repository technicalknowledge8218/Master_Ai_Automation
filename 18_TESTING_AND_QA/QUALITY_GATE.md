# MASTER-AI Quality Gate & Verification Standard

> **Standard**: Zero-Defect Quality Assurance  
> **Source Directory**: `18_TESTING_AND_QA/`  

---

## 1. The Master AI Quality Gate Checklist

Before any skill, code snippet, agent persona, or technical document is marked `APPROVED`, it must pass all 9 verification gates:

| Gate | Focus Area | Verification Criteria | Pass/Fail |
| :--- | :--- | :--- | :--- |
| **G1** | **Folder Consistency** | Adheres to standardized folder architecture; no rogue empty folders | [ ] |
| **G2** | **Documentation Completeness**| All required sections, examples, edge cases, and references present | [ ] |
| **G3** | **Skill Metadata** | Valid YAML frontmatter, unique kebab-case name, concise trigger description | [ ] |
| **G4** | **Source Quality** | Sourced from Tier 1/2 official documentation with URLs and access dates | [ ] |
| **G5** | **Zero Redundancy** | Verified against `SKILL_CATALOG.md` and `KNOWLEDGE_INDEX.md` | [ ] |
| **G6** | **Security & Privacy** | Zero hardcoded secrets, no credential exposure, OWASP compliance | [ ] |
| **G7** | **Link Integrity** | All markdown relative links resolve correctly without dead paths | [ ] |
| **G8** | **Version Compatibility** | Validated against active host environment (Windows 11, Node LTS, Python 3.12+) | [ ] |
| **G9** | **Deployment Safety** | Global deployment requires explicit approval report and backup plan | [ ] |
| **G10**| **Negative Test Suite** | Negative failure-mode tests (syntax, budget, ZipSlip) pass 100% | [ ] |

---

## 2. Skill Maturity Pipeline
Every skill advances through 6 discrete maturity states:
```
DISCOVERED ──> RESEARCHED ──> IMPLEMENTED ──> TESTED ──> APPROVED ──> PUBLISHED
```
- **DISCOVERED**: Registered in capability tracking matrix.
- **RESEARCHED**: Official vendor APIs, specifications, and edge cases verified.
- **IMPLEMENTED**: `SKILL.md`, references, and examples physically authored.
- **TESTED**: Positive and negative automated test scripts pass with 100% success.
- **APPROVED**: Signed off against all 10 Quality Gates.
- **PUBLISHED**: Deployed to designated runtime scope.

---

## 3. Publication Tracking

Publication must be explicitly tracked across two separate scopes:

- **Workspace Publication**: The skill is active within `MASTER-AI/02_SKILLS/` and available for workspace tasks.
- **Global Publication**: The skill has passed global approval and is deployed to `%USERPROFILE%\.gemini\config\skills\`.

An asset may be `PUBLISHED (Workspace)` while remaining `UNPUBLISHED (Global)`.
