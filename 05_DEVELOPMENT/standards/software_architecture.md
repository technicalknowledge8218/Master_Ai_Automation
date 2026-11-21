# MASTER-AI Full-Stack Standards: Software Architecture

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Reviewer**: AGT-002 Software Architect  

---

## 1. Architectural Philosophy: Three-Tier Decoupled System

MASTER-AI mandates a **Three-Tier Decoupled Clean Architecture** for all applications, whether targeting Web, Mobile, Desktop, or Cloud services:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PRESENTATION LAYER (UI & API Gateways)                   │
│    - React / Mobile / Desktop Components                    │
│    - HTTP Controllers, Route Handlers, Middleware           │
│    - Input Schema Parsing (Zod / Pydantic)                  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Calls Use Cases via Interfaces
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DOMAIN / APPLICATION LOGIC LAYER (Core Business Logic)    │
│    - Pure Business Entities & Aggregates                    │
│    - Application Services & Use Case Interactors            │
│    - Domain Events & Invariant Validation                   │
│    - Zero Dependency on Frameworks or Databases (POJO/Dataclasses)│
└──────────────────────────────▲──────────────────────────────┘
                               │ Implements Domain Interfaces
                               │ (Dependency Inversion)
┌──────────────────────────────┴──────────────────────────────┐
│ 3. INFRASTRUCTURE & DATA LAYER (Persistence & External)     │
│    - Database Adapters (PostgreSQL, MongoDB, SQLite)        │
│    - Repository Implementations & Cache Clients (Redis)     │
│    - External API Clients, Message Queues, File Stores      │
└─────────────────────────────────────────────────────────────┘
```

### Core Invariants:
1. **The Dependency Rule**: Source code dependencies must point strictly inward toward higher-level policies. The Domain layer must have zero dependencies on frameworks, databases, or UI libraries.
2. **Explicit Interfaces (Ports & Adapters)**: Any interaction between Domain and Infrastructure must flow across an abstract interface (Port) implemented by Infrastructure (Adapter).
3. **No Circular Dependencies**: Circular module references are strictly prohibited and enforced via linters and build gates.

---

## 2. Monolith vs. Microservices Decision Matrix

| Criterion | Modular Monolith (Recommended Default) | Microservices |
| :--- | :--- | :--- |
| **Team Size** | 1 – 15 developers | 20+ developers with dedicated platform teams |
| **Domain Maturity** | Evolving / Early to Mid-stage | Stable, well-understood bounded contexts |
| **Deployment Complexity** | Low (Single CI/CD pipeline, single artifact) | High (Kubernetes, service mesh, distributed tracing) |
| **Data Consistency** | ACID transactions across modules | Eventual consistency, Saga patterns, 2PC |
| **Operational Overhead** | Minimal monitoring requirements | High (OpenTelemetry, Prometheus, centralized logs) |
| **Recommendation** | **Start with Modular Monolith** | **Decompose only when bounded context scales independently** |

### Monolith-to-Microservices Decomposition Rules:
- Never begin a new project as distributed microservices.
- Ensure bounded contexts are decoupled within the monolith first.
- Only extract a service when it possesses distinct scaling needs (e.g., intensive GPU worker, separate billing security boundary) or separate team ownership.

---

## 3. Event-Driven & Layered Architecture

### Event-Driven Principles:
1. **Domain Events**: Dispatched when a significant state change occurs within an Aggregate (e.g., `UserRegisteredEvent`, `PaymentCapturedEvent`).
2. **At-Least-Once Delivery**: Consumers must be designed to be **idempotent**, using deduplication keys or idempotency tokens.
3. **Outbox Pattern**: When modifying database state and publishing an event, write the event to an `outbox` table in the same database transaction to guarantee event emission without distributed transaction overhead.

---

## 4. Architecture Decision Records (ADRs)

Every significant architectural decision (framework selection, database choice, concurrency model, breaking API change) must be recorded in an ADR under `12_DOCUMENTS/adr/` using the standard schema:
- **Title**: `ADR-XXX: Short Description`
- **Status**: `PROPOSED`, `ACCEPTED`, `SUPERSEDED`, or `DEPRECATED`
- **Context**: Problem statement, business drivers, and technical constraints.
- **Decision**: The selected architectural approach.
- **Consequences**: Positive benefits and negative trade-offs.
- **Alternatives Considered**: Evaluated technologies and rationale for rejection.
