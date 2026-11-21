# MASTER-AI Skill Development Standard & Lifecycle

> **Specification**: Antigravity-Compatible Skill Architecture  
> **Source Directory**: `02_SKILLS/`  

---

## 1. Skill Directory Anatomy

Every skill inside `02_SKILLS/` must adhere strictly to the following physical layout:

```text
skills/<skill-name>/
├── SKILL.md              # Mandatory: YAML frontmatter + concise operational procedure
├── references/           # Optional: In-depth technical guides, API specs, checklists
├── scripts/              # Optional: Executable Python, Node.js, or PowerShell scripts
└── assets/               # Optional: Static schemas, templates, and sample inputs
```

> [!IMPORTANT]
> **No Empty Folders**: Create only the subdirectories actually required by that specific skill. If a skill does not require scripts or assets, omit those directories.

---

## 2. The `SKILL.md` Specification

The main `SKILL.md` file is subject to strict constraints to preserve the agent's context budget:

```markdown
---
name: lowercase-kebab-name
description: >-
  Actionable 3rd-person description stating WHAT the skill does and EXACTLY WHEN to use it.
  Example: "Researches software libraries and verifies API specifications against official documentation."
---

# Skill Title

Short overview of the skill's purpose and guaranteed outcomes.

## When to Use This Skill
- Concrete trigger condition 1.
- Concrete trigger condition 2.

## Required Inputs
- Expected parameter or context item.

## Execution Workflow
1. Step one with exact commands or subroutines.
2. Step two with references to `spec.md` in the `references/` directory.

## Verification & Quality Checklist
- [ ] Output verification criterion 1.
- [ ] Output verification criterion 2.

## Common Mistakes & Traps
- Antipattern to avoid.
```

### Frontmatter Rules:
- `name`: Must be lowercase letters, numbers, and hyphens (`^[a-z0-9-]+$`).
- `description`: Must be concise (under 1,000 characters). Must be written in the third person. Must clearly express the **activation trigger** so the LLM knows when to load the skill on demand.

---

## 3. Skill Lifecycle & Maturity Pipeline

Every skill passes through 6 progressive maturity states:

```
[DRAFT] ──> [RESEARCHED] ──> [IMPLEMENTED] ──> [TESTED] ──> [APPROVED] ──> [PUBLISHED]
```

1. **DRAFT**: Skill entry cataloged with defined name and scope in `SKILL_CATALOG.md`.
2. **RESEARCHED**: Official vendor documentation, edge cases, and APIs verified and recorded.
3. **IMPLEMENTED**: `SKILL.md`, `references/`, and `scripts/` fully authored.
4. **TESTED**: Executed in a realistic test project or sandbox with zero failures.
5. **APPROVED**: Validated against the Master AI Quality Gate by human or lead agent.
6. **PUBLISHED**: Deployed to its target scope.
   - **Workspace Publication**: Loaded in `MASTER-AI/.agents/skills/`.
   - **Global Publication**: Approved and deployed to `%USERPROFILE%\.gemini\config\skills\` via the approval pipeline.

---

## 4. Skill Testing & Duplicate Prevention Process

### Duplicate Detection
Before any new skill is authored:
1. Search `SKILL_CATALOG.md` for existing keywords and intent matches.
2. If an existing skill covers >60% of the capability, **extend the existing skill** using modular reference files rather than creating a competing skill.

### Skill Testing Protocol
Every skill containing executable scripts or procedural instructions must be validated:
1. **Syntax Check**: YAML frontmatter must parse cleanly as valid YAML.
2. **Link Integrity**: All relative links to `references/` or `scripts/` must resolve without 404s.
3. **Dry-Run Test**: Any script in `scripts/` must execute successfully in a clean virtual environment or sandbox.
4. **Execution Test**: An agent must follow the instructions on a sample problem and reach the expected verification state.

---

## 5. Deprecation & Versioning

- **Semantic Versioning**: Skills track versions in their changelog or metadata comments (`v1.0.0`).
- **Deprecation Warning**: When an underlying API changes, the skill's `SKILL.md` must display a `> [!WARNING]` alert and link to the replacement skill. Deprecated skills are preserved in `02_SKILLS/deprecated/` for backwards compatibility.
