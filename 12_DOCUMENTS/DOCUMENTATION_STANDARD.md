# MASTER-AI Documentation Standard

> **Document Version:** 1.0.0  
> **Status:** Active / Sovereign Standard  
> **Applies To:** All 24 Domains & Full-Stack Engineering Operations  

---

## 1. Overview & Core Philosophy

Within the MASTER-AI ecosystem, documentation is a first-class citizen. Code without documentation is incomplete, and outdated documentation is technical debt. All documentation must strictly adhere to **GitHub-Flavored Markdown (GFM)** standards, maintain verified relative links, and reside within its designated domain directory or root registry.

### Guiding Principles
- **Living Documentation:** Every architectural change, API update, or skill integration must be accompanied by corresponding doc updates.
- **Truth-First Verification:** All code references, schema definitions, and path structures must be verified against actual implementation before publishing.
- **Predictable Hierarchy:** Every domain, module, and sub-system follows a structured manifest pattern.

---

## 2. README Hierarchy & Manifest Standards

The MASTER-AI repository enforces a strict top-down README hierarchy to ensure rapid discoverability across all 24 operational domains.

### Hierarchy Tiers
1. **Root Manifest (`README.md`):** Serves as the global entry point, outlining ecosystem architecture, domain index, and quick-start protocols.
2. **Domain Manifest (`<DOMAIN_ID>/README.md`):** Every domain folder (e.g., `00_CORE_SYSTEM`, `12_DOCUMENTS`, `19_SECURITY_AND_COMPLIANCE`) must contain a dedicated README detailing its scope, key artifacts, sub-modules, and maintainer protocols.
3. **Component Readmes:** Sub-directories containing complex modules must include brief local README files explaining module-specific setup and execution.

### Domain README Template
```markdown
# [Domain Name / Number] - Domain Title

> **Scope:** Brief summary of the domain's purpose within MASTER-AI.  
> **Status:** Active / Stabilizing  

## Directory Structure
- `subfolder/` - Purpose and contents.
- `artifact.md` - Key documentation artifact.

## Key Guidelines & Operational Rules
1. Rule one...
2. Rule two...
```

---

## 3. OpenAPI 3.1 API Specifications

All backend services, REST endpoints, and MCP tool interfaces exposed within MASTER-AI must maintain rigorous OpenAPI 3.1 specifications.

### Specification Structure & Requirements
- **Format:** YAML (`.yaml`) or JSON (`.json`) stored alongside the service code or in `12_DOCUMENTS/api/`.
- **Version Header:** Must specify `openapi: 3.1.0`.
- **Info Object:** Must include `title`, `version`, `description`, and `contact` metadata.
- **Components Section:** Reusable schemas, security schemes, and error responses must be centralized under `components/`.

### Example OpenAPI 3.1 Template
```yaml
openapi: 3.1.0
info:
  title: MASTER-AI Core Engine API
  version: 1.0.0
  description: Sovereign API specification for MASTER-AI full-stack operations.
servers:
  - url: http://localhost:8080/api/v1
    description: Local development server
paths:
  /health:
    get:
      summary: Health check endpoint
      operationId: getHealthStatus
      responses:
        '200':
          description: System operational
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: healthy
                  timestamp:
                    type: string
                    format: date-time
components:
  schemas:
    ErrorResponse:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: integer
          example: 400
        message:
          type: string
          example: Invalid request payload
```

---

## 4. Architecture Decision Records (ADRs)

Architecture Decision Records capture significant architectural, structural, or technological choices made within the MASTER-AI ecosystem.

### ADR Location & Naming
- **Path:** `12_DOCUMENTS/adr/` (or within the relevant domain folder).
- **Naming Convention:** `ADR-YYYYMMDD-Short-Title.md` (e.g., `ADR-20261117-open-api-standard.md`).

### ADR Template
```markdown
# ADR-[YYYYMMDD]-[Short Title]

- **Status:** Proposed / Accepted / Deprecated / Superseded
- **Date:** YYYY-MM-DD
- **Author:** [Agent / Engineer ID]
- **Deciders:** MASTER-AI Core Architecture Committee

## Context
Describe the forces at play, including technological, business, operational, or constraints context. Why is a decision necessary now?

## Decision
State the explicit choice made. Use clear, imperative language ("We will use...", "We choose...").

## Consequences
### Positive
- Benefit 1
- Benefit 2

### Negative / Trade-offs
- Risk 1 (and mitigation strategy)
- Technical debt accepted

## Alternatives Considered
- **Alternative A:** Why it was rejected.
- **Alternative B:** Why it was rejected.
```

---

## 5. Link Validation & Relative Path Protocols

Broken links undermine system integrity. All documentation must comply with strict link validation rules.

### Rules for Linking
1. **Relative Paths Only:** Use relative paths for internal repository files (e.g., `[Security Policy](../SECURITY_POLICY.md)`). Never use absolute local file paths (like `C:\Users\...`) unless referencing system artifacts outside the workspace.
2. **File Scheme Links:** When linking files in agent responses or interactive contexts, follow the `file:///` absolute path format as required by workspace rules.
3. **Anchor Verification:** Heading links and table-of-contents anchor tags must be slugified and verified against actual heading text.
4. **No Dead Links:** All internal links are subject to automated verification checks during documentation builds.

---

## 6. Documentation Maintenance & Review Lifecycle

1. **Authoring:** Created during feature or architecture development.
2. **Review:** Verified against codebase implementation and cross-domain standards.
3. **Publishing:** Committed to the master branch and referenced in `CHANGELOG.md`.
4. **Auditing:** Periodic review during system updates to prune obsolete specs.
