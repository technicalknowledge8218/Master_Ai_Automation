# Three-Tier Decoupled Architecture Reference

> **Reference**: `02_SKILLS/software-architecture/references/`  

---

## 1. Architectural Layers

```
+-------------------------------------------------------------+
| Presentation Layer (UI / CLI / View)                       |
| - React Components, CLI input handling, view templates      |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| Application / Domain Logic Layer                            |
| - Business rules, workflow orchestration, validation        |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| Infrastructure & Data Access Layer                          |
| - Database repositories (SQL/pgvector), external HTTP APIs |
+-------------------------------------------------------------+
```

## 2. Inviolable Dependency Inversion Rule
Dependencies must point **inward** toward the core domain logic:
- The domain layer defines repository interfaces.
- The infrastructure layer implements those interfaces.
- Changing from PostgreSQL to MongoDB or Redis should never require changing domain business logic.
