# Master AI Technology Evaluations Index

This directory contains formal, evidence-based technical evaluations conducted under the [Technology Evaluation Framework](TECH_EVALUATION_FRAMEWORK.md).

All evaluations adhere to the 15 standardized criteria and scoring gates:
- **Score $\ge$ 80 / 100**: `APPROVED (ADOPT)`
- **Score 65 – 79 / 100**: `CONDITIONAL (TRIAL)`
- **Score 50 – 64 / 100**: `RESTRICTED (ASSESS)`
- **Score $<$ 50 / 100**: `REJECTED (AVOID)`

---

## Technology Evaluation Catalog

| ID | Technology | Version | Category | Score | Status | License | Link |
|---|---|---|---|---|---|---|---|
| **EVAL-001** | React | 19.x | Frontend UI Framework | **92.6 / 100** | `APPROVED (ADOPT)` | MIT | [TECH_EVAL_REACT.md](TECH_EVAL_REACT.md) |
| **EVAL-002** | Node.js & Express | v22+ LTS / Express 4/5 | Backend Runtime & HTTP | **91.2 / 100** | `APPROVED (ADOPT)` | MIT | [TECH_EVAL_NODE_EXPRESS.md](TECH_EVAL_NODE_EXPRESS.md) |
| **EVAL-003** | PostgreSQL | 16.x / 17.x / 18.x | Relational Database (RDBMS) | **96.4 / 100** | `APPROVED (ADOPT)` | PostgreSQL License | [TECH_EVAL_POSTGRESQL.md](TECH_EVAL_POSTGRESQL.md) |
| **EVAL-004** | MongoDB | 7.0 / 8.0 | Document NoSQL Database | **72.8 / 100** | `CONDITIONAL (TRIAL)` | SSPL v1 | [TECH_EVAL_MONGODB.md](TECH_EVAL_MONGODB.md) |
| **EVAL-005** | Capacitor | 6.x / 7.x / 8.x | Native Mobile Runtime | **87.4 / 100** | `APPROVED (ADOPT)` | MIT | [TECH_EVAL_CAPACITOR.md](TECH_EVAL_CAPACITOR.md) |
| **EVAL-006** | Tailwind CSS | v3.4 / v4.x | Utility-First CSS | **93.8 / 100** | `APPROVED (ADOPT)` | MIT | [TECH_EVAL_TAILWIND.md](TECH_EVAL_TAILWIND.md) |
| **EVAL-007** | Docker & Compose | Engine 26+, Compose v2 | Containerization & Dev Stacks | **94.2 / 100** | `APPROVED (ADOPT)` | Apache 2.0 | [TECH_EVAL_DOCKER.md](TECH_EVAL_DOCKER.md) |

---

## Summary of Decisions

1. **Adopted as Core Foundation**:
   - **PostgreSQL**: Primary transactional and hybrid JSONB/vector database.
   - **React 19 + Tailwind CSS**: Standard client-side presentation and styling tier.
   - **Node.js LTS + Express**: Primary API server and service orchestration tier.
   - **Capacitor**: Standard mobile bridge converting Web applications to Android and iOS.
   - **Docker & Compose**: Universal packaging, isolation, and deployment substrate.

2. **Approved for Conditional / Specialized Usage**:
   - **MongoDB**: Approved for high-throughput polymorphic document feeds; prohibited as primary financial or transactional system of record due to SSPL license constraints and ACID performance trade-offs.
