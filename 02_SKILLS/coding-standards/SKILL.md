---
name: coding-standards
description: >-
  Enforces modern, strict programming standards across TypeScript, Python, and SQL, including
  type safety, zero hardcoded secrets, input sanitization, and clean code conventions.
  Use before committing code, during code reviews, or when setting up linters.
---

# Modern Coding Standards & Quality Enforcement Skill

> **Status**: IMPLEMENTED & TESTED (Workspace)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software and Web Development)  

---

## 1. Purpose & Scope
This skill provides automated and procedural rules for authoring clean, maintainable, and type-safe code. It forbids antipatterns like `any` in TypeScript, bare `except:` in Python, raw unparameterized SQL queries, and hardcoded API tokens.

## 2. When to Use This Skill
- Before writing or refactoring any code in MASTER-AI or downstream projects.
- During independent code reviews conducted by the Code Reviewer agent.
- When configuring project linters (ESLint, Prettier, Ruff, Black).

## 3. Required Standards
- **TypeScript**: `strict: true`, `noImplicitAny: true`, explicit return types on public functions.
- **Python**: PEP 8 style, strict type hints (`typing`), structured logging.
- **Security**: Zero secrets in source code, parameterized queries only.

## 4. Execution Workflow

### Step 1: Adhere to Language Specific Rules
Review [TYPESCRIPT_PYTHON_RULES.md](./references/TYPESCRIPT_PYTHON_RULES.md) for syntax standards.

### Step 2: Automated Code Hygiene Scan
Run the built-in static rule checker on target files:
```powershell
python 02_SKILLS/coding-standards/scripts/lint_rules_checker.py --target "path/to/source_file.py"
```

### Step 3: Verification Checklist
- [ ] No hardcoded secrets, passwords, or bearer tokens.
- [ ] TypeScript code compiles without `any` overrides.
- [ ] Python exceptions are typed and logged with context.
- [ ] All database queries use parameter binding to prevent SQL injection.
- [ ] Public functions include JSDoc or docstring documentation.
