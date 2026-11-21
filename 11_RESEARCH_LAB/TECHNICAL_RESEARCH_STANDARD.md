# MASTER-AI Technical Research Standard & Methodology

> **Standard**: Anti-Hallucination, Empirical Verification & Strict Sourcing  
> **Source Directory**: `11_RESEARCH_LAB/`  

---

## 1. Information Source Priority Hierarchy

When investigating technologies, frameworks, APIs, or architectural options, all agents must adhere strictly to this priority hierarchy:

```
Tier 1: Official Vendor Documentation & API Reference (HIGHEST AUTHORITY)
   │
Tier 2: Official GitHub / GitLab Source Repositories & Release Notes
   │
Tier 3: Formal Standards, Specifications & RFCs (W3C, IETF, ECMA, OpenAPI)
   │
Tier 4: Reputable Engineering Publications & Peer-Reviewed Papers
   │
Tier 5: Practical Benchmarks & Empirical Experiments Conducted Locally
   │
Tier 6: Community Forums, Blog Posts & Unverified Articles (LOWEST - REQUIRES TESTING)
```

---

## 2. Mandatory Technical Distinctions

Every research report and technical evaluation must explicitly distinguish and document:

1. **Current Stable Version**: The actively maintained, production-tested version recommended for deployment today.
2. **Latest Release**: The most recent release tag, noting any bleeding-edge or pre-release qualifiers (RC, beta, alpha).
3. **Experimental Features**: Capabilities gated behind feature flags or marked experimental in official docs.
4. **Deprecated Features**: APIs or methods marked for removal in upcoming major versions.
5. **Compatibility Matrix**: Explicit language runtime, OS, and framework compatibility (e.g., Node 20+, Python 3.12+, Windows 11).
6. **Security & Vulnerability Profile**: Known CVEs, licensing terms (MIT, Apache 2.0, AGPL, proprietary), and data privacy implications.
7. **Practical Utility**: Objective assessment of whether the technology solves a real problem in MASTER-AI or introduces unnecessary complexity.
8. **Sources & Access Dates**: Full canonical URLs and exact ISO timestamps of when documentation was retrieved.

> [!WARNING]
> **Anti-Hallucination Mandate**: Never state that a library version is "latest" or "standard" based on training memory alone. The agent must verify release dates and version numbers against official registries (npm, PyPI, GitHub releases).
