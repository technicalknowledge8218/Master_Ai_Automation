---
name: documentation-engineering
description: >-
  Structures, authors, and maintains high-yield technical documentation, Architecture Decision
  Records (ADRs), API specifications, and README manifests. Use whenever documenting system
  architecture, recording major technical decisions, or generating documentation sets.
---

# Documentation Engineering & ADR Methodology Skill

> **Status**: IMPLEMENTED & TESTED (Workspace)  
> **Version**: 1.0.0  
> **Domain**: DOM-27 (Document and Presentation Creation)  

---

## 1. Purpose & Scope
This skill provides standards for producing living, accurate, and navigable documentation. It mandates that every major architectural fork is documented via an Architecture Decision Record (ADR), and that all documentation adheres to GitHub-flavored markdown standards.

## 2. When to Use This Skill
- When making a substantial architectural decision that affects multiple modules.
- When creating README files for new domains or repositories.
- When drafting API reference documentation or integration guides.
- When reviewing documentation for freshness and link integrity.

## 3. Required Inputs
- Title of architectural decision or system component.
- Context and problem statement.
- Evaluated options with trade-offs.
- Final decision and consequences (positive and negative).

## 4. Execution Workflow

### Step 1: Follow the ADR Methodology
Review [ADR_METHODOLOGY.md](./references/ADR_METHODOLOGY.md) and inspect the canonical [ADR_SAMPLE.md](./examples/ADR_SAMPLE.md).

### Step 2: Document Structure Standard
- Include YAML or metadata header.
- Provide clear visual topology (Mermaid diagram or ASCII flow).
- Provide copy-paste runnable commands and code snippets.
- Document edge cases, failure states, and troubleshooting tips.

### Step 3: Verification Checklist
- [ ] Document title is clear and specific.
- [ ] Context explains "WHY" the decision was made, not just "WHAT".
- [ ] Trade-offs and downsides are explicitly acknowledged.
- [ ] Internal markdown links use valid relative paths.
- [ ] No hardcoded private credentials or environment paths.
