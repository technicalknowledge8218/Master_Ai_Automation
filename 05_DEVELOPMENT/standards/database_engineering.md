# MASTER-AI Full-Stack Standards: Database Engineering

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Primary Databases**: PostgreSQL (Relational) & MongoDB (Document)  

---

## 1. Database Selection Matrix

| Engine | Primary Use Case | Strengths | Constraints |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | Core business data, transactional systems, relational graphs, hybrid JSONB. | ACID compliance, strict constraints, rich extensions (`pgvector`, `PostGIS`). | Vertical scaling for writes; requires connection pooling (`PgBouncer`). |
| **MongoDB** | Unstructured catalogs, dynamic content feeds, rapid schema prototyping. | Flexible document schema, native sharding, high ingest throughput. | No cross-collection joins; eventual consistency requires careful modeling. |
| **Redis** | In-memory cache, session store, rate-limiting, job queue backing. | Sub-millisecond latency, pub/sub, atomic data structures. | Volatile memory footprint; persistence requires RDB/AOF configuration. |
| **SQLite** | Embedded local storage, desktop apps, mobile devices, local testing. | Zero-configuration single file, serverless, fast local reads. | Concurrency write lock; unsuitable for multi-tier concurrent web backends. |

---

## 2. PostgreSQL Relational Standards

### Schema Design & Data Integrity:
1. **Naming Conventions**: `snake_case` for all table names (plural: `users`, `orders`), column names (`user_id`, `created_at`), and indexes (`idx_users_email`).
2. **Primary Keys**: Use UUIDv7 (time-ordered UUID) or BigInt identity for primary keys. UUIDv7 prevents B-Tree fragmentation while ensuring distributed uniqueness.
3. **Foreign Keys**: Always define explicit `FOREIGN KEY` constraints with appropriate `ON DELETE` semantics (`RESTRICT`, `CASCADE`, `SET NULL`).
4. **Audit Columns**: Every table must include:
   - `created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL`
   - `updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL`

### Indexing Guidelines:
- **Index Foreign Keys**: Always index foreign key columns to avoid full table scans on joins.
- **Index Types**:
  - `B-Tree` (default): Equality and range queries (`=`, `<`, `>`, `BETWEEN`).
  - `GIN`: For `JSONB` columns, array types, and full-text search.
  - `BRIN`: For append-only, chronologically ordered massive log/timeseries tables.
- **Partial Indexes**: Use partial indexes (`WHERE is_active = true`) to index small subsets of data efficiently.
- **Rule**: Never create speculative indexes without query profiling via `EXPLAIN (ANALYZE, BUFFERS)`.

---

## 3. Database Transactions & Concurrency

1. **Isolation Levels**: Default to `READ COMMITTED`. Use `REPEATABLE READ` or `SERIALIZABLE` only when financial or concurrent inventory transactions require strict isolation.
2. **Short-Lived Transactions**: Keep transactions as brief as possible. Never perform external network calls, file I/O, or heavy CPU operations inside an active database transaction.
3. **Pessimistic vs. Optimistic Locking**:
   - Use **Optimistic Locking** (with a `version` column) for web applications where conflicts are rare.
   - Use **Pessimistic Locking** (`SELECT ... FOR UPDATE`) only when high contention demands strict queueing (e.g., ticket booking, seat reservation).

---

## 4. Migration Strategies & Zero-Downtime Deployments

All database schema changes must be version-controlled using migration tools (**Prisma Migrate**, **Flyway**, or **Alembic**).

### Zero-Downtime "Expand and Contract" Pattern:
Never execute breaking schema modifications (renaming a column, dropping a column) in a single deployment:
1. **Expand**: Add the new column or table alongside the old one. Deploy backend code that writes to both old and new columns, reading from the old one.
2. **Backfill**: Migrate historical records from the old column to the new column via background job.
3. **Switch**: Deploy backend code that reads and writes exclusively to the new column.
4. **Contract**: In a subsequent release, safely remove the old column and clean up legacy database triggers.
