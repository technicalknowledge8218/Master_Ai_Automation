# Technical Research Evaluation Matrix & Scoring Guide

> **Standard**: Objective Technology Assessment  
> **Source Directory**: `02_SKILLS/technical-research/references/`  

---

## 1. Scoring Dimensions (0 - 5 Scale)

| Dimension | 0 (Unacceptable) | 3 (Acceptable) | 5 (Gold Standard) |
| :--- | :--- | :--- | :--- |
| **Documentation** | No official docs; abandoned wiki | Clear docs, but missing edge cases | Comprehensive API docs, runnable examples, interactive playground |
| **Maintenance** | No commits in >12 months; unmerged PRs | Monthly releases; active issue tracker | Weekly commits, automated CI, immediate security patches |
| **Compatibility** | Fails on Windows 11 or modern Python/Node | Works with minor manual configuration | Native cross-platform, modern ES/PEP standards, zero workarounds |
| **Security** | Critical unpatched CVEs; hardcoded credentials | Clean audit; minimal transitive dependencies | Formal audit, zero CVEs, explicit security policy, least privilege |
| **License** | Ambiguous or restrictive viral copyleft | Permissive (BSD, Apache 2.0, MIT) with standard attribution | Permissive, enterprise-friendly, zero proprietary lock-in |
| **Empirical Proof** | Theory only; no verifiable reproduction | Standard benchmark reproduced | Local reproduction test passed with logged metrics |

---

## 2. Adoption Decision Thresholds
- **Total Score >= 25 / 30**: Recommended for immediate adoption into `TECHNOLOGY_STACK.md`.
- **Total Score 18 - 24 / 30**: Conditionally acceptable for experimental spike in `21_LEARNING_LAB`.
- **Total Score < 18 / 30**: Rejected. Document rationale in `11_RESEARCH_LAB/tech_evaluations/`.
