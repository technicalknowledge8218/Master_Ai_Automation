---
name: backend-engineering
description: >-
  Architects secure, scalable, and resilient backend services and APIs using Node.js/Express or Python/FastAPI.
  Covers middleware pipelines, authentication flows, structured JSON logging, input validation, and transactional integrity.
---

# Backend Engineering Skill

> **Status**: APPROVED (Workspace-Local)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software Development), DOM-09 (Backend Engineering)  
> **Reference Standard**: [backend_engineering.md](../../05_DEVELOPMENT/standards/backend_engineering.md)

---

## 1. Purpose & Scope
This skill provides production standards for engineering server-side applications, microservices, and asynchronous task workers. It enforces defensive coding, uniform error envelopes (RFC 7807), secure authentication mechanisms, and structured observability.

## 2. When to Use This Skill
- Designing RESTful or GraphQL server architectures.
- Implementing authentication middleware (JWT, secure session cookies, OAuth2).
- Structuring request validation and sanitization pipelines.
- Configuring structured JSON logging (Pino/structlog) and OpenTelemetry tracing.
- Setting up rate limiting, CORS, and security HTTP headers.
- Implementing background job processing (BullMQ / Celery).

## 3. Required Inputs
- API specification or requirements (endpoints, verbs, payloads).
- Data models and database schemas.
- Non-functional requirements (throughput targets, latency SLAs, auth providers).

## 4. Execution Workflow

### Step 1: Middleware Chain Setup
Assemble the request lifecycle in deterministic order:
1. `Correlation ID`: Inject `X-Correlation-ID` header into request context and logger.
2. `Security Headers`: Apply `helmet` (CSP, HSTS, X-Content-Type-Options).
3. `CORS`: Restrict origins strictly to authorized domains (never `*` in production).
4. `Rate Limiting`: Apply IP/user token bucket rate limiters (e.g., 100 req/min per IP).
5. `Body Parsing`: Parse JSON payloads with strict byte limits (e.g., max 1MB).

### Step 2: Request Validation & Controller Logic
1. Validate incoming query parameters, headers, and request bodies using Zod or Pydantic.
2. Reject invalid payloads immediately with HTTP 400 Bad Request before touching business logic.
3. Keep controllers thin: extract inputs $\rightarrow$ delegate to Domain Service $\rightarrow$ return HTTP response.

### Step 3: Domain Service & Data Access
1. Execute domain rules inside services isolated from transport concerns (no `req`/`res` objects).
2. Use repository patterns or parameterized query interfaces; never concatenate raw SQL.
3. Manage database transactions explicitly with rollback on any failure.

### Step 4: Centralized Error Handling
1. Catch all unhandled exceptions in a terminal error-handling middleware.
2. Format errors according to RFC 7807 Problem Details:
   ```json
   {
     "type": "https://api.master-ai.local/errors/invalid-credentials",
     "title": "Invalid Credentials",
     "status": 401,
     "detail": "The provided username or password is incorrect.",
     "instance": "/api/v1/auth/login",
     "correlation_id": "req-98f7-41ab"
   }
   ```
3. Never leak stack traces, database table names, or internal environment paths to clients.

## 5. Strict Rules & Constraints
- NEVER store plain text passwords; hash with Argon2id or bcrypt (cost >= 12).
- NEVER log sensitive fields (passwords, tokens, credit card numbers, PII) in structured logs.
- NEVER permit unvalidated input to reach database queries or shell command execution.
- NEVER block the event loop with synchronous file I/O (`fs.readFileSync`) in production request handlers.

## 6. Code Pattern Example

```typescript
import express, { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import pino from 'pino';

const logger = pino({ level: process.env.LOG_LEVEL || 'info' });
const app = express();

const CreateProjectSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().max(500).optional(),
});

app.post('/api/v1/projects', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const validatedData = CreateProjectSchema.parse(req.body);
    // Delegate to Domain Service
    const project = await projectService.create(validatedData, req.user.id);
    
    logger.info({ projectId: project.id, userId: req.user.id }, "Project created successfully");
    res.status(201).json({ status: "success", data: project });
  } catch (error) {
    next(error);
  }
});
```

## 7. Quality Checklist
- [ ] All endpoints validate inputs using declarative schemas before execution.
- [ ] Structured JSON logging includes correlation IDs on all entries.
- [ ] Authentication and authorization checks are enforced on protected routes.
- [ ] Sensitive secrets are accessed exclusively through environment variables.
- [ ] Automated integration tests verify HTTP 200, 400, 401, and 500 status codes.
