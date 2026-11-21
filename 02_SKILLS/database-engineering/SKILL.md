---
name: database-engineering
description: >-
  Designs performant, normalized relational and document schemas, writes efficient queries and indexes,
  executes zero-downtime database migrations, and enforces ACID transactional integrity across PostgreSQL, MongoDB, and Redis.
---

# Database Engineering Skill

> **Status**: APPROVED (Workspace-Local)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software Development), DOM-10 (Database Engineering)  
> **Reference Standard**: [database_engineering.md](../../05_DEVELOPMENT/standards/database_engineering.md)

---

## 1. Purpose & Scope
This skill provides rigorous data modeling standards, query optimization techniques, index selection heuristics, and migration protocols. It ensures maximum read/write performance, prevents deadlocks, and guarantees zero data loss during schema evolution.

## 2. When to Use This Skill
- Choosing between Relational (Postgres), Document (MongoDB), Key-Value (Redis), or Embedded (SQLite).
- Designing normalized schemas, foreign keys, constraints, and audit columns.
- Writing complex SQL queries, CTEs, window functions, or JSONB queries.
- Designing zero-downtime schema migrations (Expand and Contract pattern).
- Diagnosing slow queries using `EXPLAIN ANALYZE` and creating appropriate indexes.
- Configuring connection pools, timeouts, and transaction isolation levels.

## 3. Required Inputs
- Entity-relationship diagrams or domain entities.
- Query access patterns (read-heavy vs write-heavy, point lookups vs range scans).
- Volume projections (row count, growth rate per month).

## 4. Execution Workflow

### Step 1: Database Selection & Schema Design
1. Follow the selection matrix:
   - Primary structured transactional data $\rightarrow$ PostgreSQL.
   - High-throughput unstructured feeds $\rightarrow$ MongoDB.
   - Cache, pub/sub, rate-limiting tokens $\rightarrow$ Redis.
   - Local CLI tool or single-user desktop client $\rightarrow$ SQLite.
2. Standard columns for all relational entities:
   - `id`: UUIDv7 primary key (time-ordered, index-friendly).
   - `created_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW().
   - `updated_at`: TIMESTAMPTZ NOT NULL DEFAULT NOW().
   - `version`: INTEGER NOT NULL DEFAULT 1 (for optimistic concurrency).

### Step 2: Indexing Strategy
1. Add B-Tree indexes on all foreign keys (`user_id`, `tenant_id`) and search filters.
2. Create compound indexes ordering by equality columns first, then range columns (`status, created_at`).
3. Use partial indexes for soft-deleted or sparse tables (`WHERE deleted_at IS NULL`).
4. Avoid over-indexing: each index degrades write and insert throughput.

### Step 3: Zero-Downtime Migrations (Expand/Contract)
Never execute breaking schema changes in a single step:
- **Phase 1 (Expand)**: Add new column as nullable; dual-write from application code.
- **Phase 2 (Backfill)**: Run asynchronous background migration in batches.
- **Phase 3 (Switch)**: Update read queries to use new column; make column NOT NULL.
- **Phase 4 (Contract)**: Drop old column in a subsequent release.

### Step 4: Performance Verification
1. Run `EXPLAIN (ANALYZE, BUFFERS)` on all high-frequency queries.
2. Verify that query execution avoids sequential scans (`Seq Scan`) on large tables.
3. Confirm that locks are held for minimal duration inside transactions.

## 5. Strict Rules & Constraints
- NEVER run `ALTER TABLE ... ADD COLUMN ... DEFAULT ...` on huge tables without verifying PostgreSQL version non-locking defaults.
- NEVER execute destructive `DROP TABLE` or `DROP COLUMN` without prior verified backup and multi-phase contract approval.
- NEVER permit unbounded queries (`SELECT * FROM table` without `LIMIT`).
- NEVER store raw sensitive credentials in database tables.

## 6. Code Pattern Example (PostgreSQL Migration)

```sql
-- Migration: 20261117_create_tenants_and_projects.sql
BEGIN;

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Compound index for fast tenant project filtering
CREATE INDEX IF NOT EXISTS idx_projects_tenant_status 
ON projects (tenant_id, status);

-- GIN index for JSONB metadata querying
CREATE INDEX IF NOT EXISTS idx_projects_metadata_gin 
ON projects USING GIN (metadata);

COMMIT;
```

## 7. Quality Checklist
- [ ] Primary keys use UUIDv7 or auto-incrementing bigserial with indexing.
- [ ] Foreign key constraints enforce referential integrity (`ON DELETE RESTRICT/CASCADE`).
- [ ] `EXPLAIN ANALYZE` confirms index scans on critical query paths.
- [ ] Down migrations (`down.sql`) are authored and tested for rollback safety.
- [ ] Connection pool limits are calibrated against database server memory and max connections.
