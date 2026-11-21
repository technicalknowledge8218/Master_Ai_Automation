---
name: software-architecture
description: >-
  Designs modular, decoupled, and scalable software systems following clean architecture,
  domain-driven design, and strict separation of concerns. Use when architecting new projects,
  evaluating microservice vs monolith trade-offs, or defining module interfaces.
---

# Software Architecture & System Design Skill

> **Status**: IMPLEMENTED & TESTED (Workspace)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software and Web Development)  

---

## 1. Purpose & Scope
This skill provides architectural patterns, boundary definition rules, and system decomposition principles across frontend, backend, and database tiers. It prevents tight coupling, circular dependencies, and premature complexity.

## 2. When to Use This Skill
- When designing the folder structure and module boundaries for a new project.
- When choosing between a Modular Monolith, Serverless functions, or Microservices.
- When defining API contracts and domain models between frontend and backend.
- When restructuring legacy code to adhere to Clean Architecture.

## 3. Required Inputs
- Functional requirements and scalability goals (expected users, read/write ratios).
- Target tech stack (e.g., React 19 + Fastify + PostgreSQL).
- Environmental constraints (cloud hosting, edge execution, offline mobile).

## 4. Execution Workflow

### Step 1: Establish Tier Separation
Adhere strictly to the Three-Tier Decoupled Architecture:
- Review [THREE_TIER_ARCHITECTURE.md](./references/THREE_TIER_ARCHITECTURE.md).
- Keep domain entities isolated from database ORM and HTTP transport logic.

### Step 2: Formulate System Topology
- Detail data flow: Client $\rightarrow$ API Gateway / Controller $\rightarrow$ Domain Service $\rightarrow$ Data Repository.
- Model state transitions and event emissions.
- Inspect sample blueprint: [modular_system_spec.json](./examples/modular_system_spec.json).

### Step 3: Architecture Quality Checklist
- [ ] No circular imports between modules.
- [ ] Business logic contains zero framework-specific HTTP request/response objects.
- [ ] Database queries are abstracted behind repository interfaces.
- [ ] Error handling uses strongly-typed domain error classes.
- [ ] Configuration is injected via environment variables.
