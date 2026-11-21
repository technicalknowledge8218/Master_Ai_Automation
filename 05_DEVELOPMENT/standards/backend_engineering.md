# MASTER-AI Full-Stack Standards: Backend Engineering

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Runtimes**: Node.js (LTS) & Python (FastAPI)  

---

## 1. API Architecture & Standards

MASTER-AI backend services must adhere to RESTful principles and modern contract-first engineering:

### Core API Rules:
1. **Contract-First Design**: API schemas must be defined in **OpenAPI 3.1** before or alongside implementation.
2. **Explicit URI Versioning**: All public endpoints must include the major version in the URI path: `/api/v1/resources`.
3. **HTTP Verb Semantics**:
   - `GET`: Safe, idempotent read operations. Never mutates server state.
   - `POST`: Create a new resource or execute non-idempotent processing.
   - `PUT`: Complete resource replacement (idempotent).
   - `PATCH`: Partial resource update (idempotent).
   - `DELETE`: Remove a resource (idempotent).
4. **Consistent Status Codes**:
   - `200 OK`: Successful read or update.
   - `201 Created`: Resource successfully created (with `Location` header).
   - `204 No Content`: Successful operation with empty response body.
   - `400 Bad Request`: Input schema validation failure.
   - `401 Unauthorized`: Missing or invalid authentication token.
   - `403 Forbidden`: Authenticated user lacks permission for the resource.
   - `404 Not Found`: Resource does not exist.
   - `429 Too Many Requests`: Rate limit exceeded.
   - `500 Internal Server Error`: Unhandled server exception.

---

## 2. Authentication, Authorization & Security Middleware

### Authentication:
- **Stateless Tokens**: Short-lived JSON Web Tokens (15 min TTL) signed with RS256/ES256.
- **Refresh Flow**: Long-lived, rotatable refresh tokens stored in secure, `HttpOnly`, `SameSite=Strict` cookies.
- **Revocation**: Refresh token IDs stored in Redis or database for instant revocation on logout or password change.

### Mandatory Middleware Pipeline:
```
[Incoming Request]
        │
        ├──> 1. Request ID Middleware (Inject unique X-Request-ID)
        ├──> 2. Security Headers (Helmet: HSTS, CSP, X-Frame-Options)
        ├──> 3. CORS Middleware (Strict origin allowlist; no wildcard '*' with credentials)
        ├──> 4. Rate Limiter (IP/User token bucket via Redis)
        ├──> 5. Body Parser & Size Limiter (Max 1MB for JSON payloads)
        ├──> 6. Authentication Middleware (Verify JWT signature & expiration)
        ├──> 7. Schema Validation Middleware (Zod / Pydantic parse)
        ├──> 8. Controller Handler (Business logic invocation)
        └──> 9. Centralized Error Handler (RFC 7807 Problem Details)
```

---

## 3. Structured Logging & Error Handling

### Structured Logging (JSON):
All logs must output structured JSON (using **Pino** in Node.js or **structlog** in Python):
```json
{
  "timestamp": "2026-11-17T02:00:00.000Z",
  "level": "info",
  "request_id": "req-98f21a4e",
  "method": "POST",
  "path": "/api/v1/orders",
  "status": 201,
  "duration_ms": 34.2,
  "user_id": "usr-10293"
}
```
**Forbidden in Logs**: Passwords, API tokens, full credit card numbers, PII, session secrets.

### Error Handling Standard (RFC 7807):
Errors returned to API clients must follow RFC 7807 Problem Details:
```json
{
  "type": "https://api.masterai.local/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "Field 'email' must be a valid email address.",
  "instance": "/api/v1/users",
  "request_id": "req-98f21a4e",
  "invalid_params": [
    {"name": "email", "reason": "invalid_email_format"}
  ]
}
```

---

## 4. Background Jobs & Real-Time Communication

1. **Asynchronous Processing**: Long-running tasks (> 200ms, such as video rendering, AI generation, email dispatch) must be offloaded to worker queues (**BullMQ** with Redis or **Celery** with RabbitMQ/Redis).
2. **Real-Time Communication**:
   - **Server-Sent Events (SSE)**: Preferred for unidirectional server-to-client streaming (e.g., LLM generation tokens, progress bars, notifications).
   - **WebSockets**: Reserved for bidirectional interactive systems (collaborative editing, chat, multi-player games). Must authenticate connection handshakes via JWT.
