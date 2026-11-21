---
name: api-engineering
description: >-
  Designs, specifies, documents, and validates resilient RESTful and event-driven APIs using OpenAPI 3.1.
  Enforces contract-first design, semantic HTTP status codes, rate limiting, versioning, and client SDK generation.
---

# API Engineering Skill

> **Status**: APPROVED (Workspace-Local)  
> **Version**: 1.0.0  
> **Domain**: DOM-07 (Software Development), DOM-09 (Backend & APIs)  
> **Reference Standard**: [backend_engineering.md](../../05_DEVELOPMENT/standards/backend_engineering.md)

---

## 1. Purpose & Scope
This skill governs the end-to-end lifecycle of Application Programming Interfaces (APIs). It standardizes contract-first specification authoring (OpenAPI 3.1), URI path conventions, idempotent HTTP verbs, semantic status codes, unified error responses, and automated client SDK generation.

## 2. When to Use This Skill
- Designing public or internal RESTful endpoints.
- Authoring and maintaining OpenAPI 3.1 / Swagger YAML/JSON specifications.
- Establishing API versioning strategies (URI path vs headers).
- Generating type-safe TypeScript or Python client SDKs from API contracts.
- Defining pagination, sorting, and field-filtering query parameters.
- Implementing webhook payloads and signature verification.

## 3. Required Inputs
- Domain resources and operations (CRUD operations, business actions).
- Authentication requirements (Bearer JWT, API Key, Mutual TLS).
- Expected request/response payload schemas.

## 4. Execution Workflow

### Step 1: Contract-First OpenAPI Specification
1. Author contract in OpenAPI 3.1 YAML/JSON before writing server implementation code.
2. Define standardized reusable components in `#/components/schemas`:
   - `ErrorResponse`: RFC 7807 Problem Details object.
   - `PaginationMeta`: `page`, `limit`, `total_items`, `total_pages`.
   - `StandardEnvelope`: Consistent wrapper if applicable.

### Step 2: RESTful URI & Verb Conventions
- **Collection Resource**: `GET /api/v1/projects` (List), `POST /api/v1/projects` (Create).
- **Individual Resource**: `GET /api/v1/projects/{id}` (Retrieve), `PUT /api/v1/projects/{id}` (Replace), `PATCH /api/v1/projects/{id}` (Partial Update), `DELETE /api/v1/projects/{id}` (Delete).
- **Sub-Resource**: `GET /api/v1/projects/{id}/tasks` (List tasks of project).
- **Action/Verb**: `POST /api/v1/projects/{id}/publish` (Specific business operation).

### Step 3: Semantic HTTP Status Codes
- `200 OK`: Successful read or update.
- `201 Created`: Successful creation (include `Location` header).
- `204 No Content`: Successful deletion (empty body).
- `400 Bad Request`: Payload validation failed.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Authenticated user lacks permission to access this resource.
- `404 Not Found`: Target resource does not exist.
- `409 Conflict`: Unique constraint violation or state transition conflict.
- `422 Unprocessable Content`: Semantically invalid business state.
- `429 Too Many Requests`: Rate limit exceeded (include `Retry-After` header).
- `500 Internal Server Error`: Unhandled server exception.

### Step 4: Pagination and Filtering Standards
1. Use cursor-based pagination for high-volume or dynamic streams (`?cursor=eyJpZCI6MTB9&limit=50`).
2. Use offset-based pagination for static dashboards (`?page=1&limit=25`).
3. Return pagination metadata in the response body alongside data items.

### Step 5: Client SDK Generation
1. Validate OpenAPI spec with spectral linter: `npx @stoplight/spectral lint openapi.yaml`.
2. Generate TypeScript client: `npx openapi-typescript openapi.yaml -o client/types.ts`.
3. Generate Python client via `openapi-python-client`.

## 5. Strict Rules & Constraints
- NEVER return HTTP 200 OK with an error payload inside the body (`{ status: "error" }`).
- NEVER use verbs in resource paths (use `POST /api/v1/documents`, not `/api/v1/createDocument`).
- NEVER break existing API contracts without incrementing major version (`/api/v2/`).
- NEVER transmit unencrypted API keys or tokens in URL query parameters.

## 6. Code Pattern Example (OpenAPI 3.1 Snippet)

```yaml
openapi: 3.1.0
info:
  title: Master AI Agent Gateway API
  version: 1.0.0
paths:
  /api/v1/tasks:
    get:
      summary: List tasks
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, running, completed, failed]
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: List of tasks retrieved successfully
          content:
            application/json:
              schema:
                type: object
                required: [items, pagination]
                properties:
                  items:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    $ref: '#/components/schemas/PaginationMeta'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
```

## 7. Quality Checklist
- [ ] OpenAPI 3.1 specification passes all Spectral linting rules with 0 errors.
- [ ] Every endpoint defines status codes for both success (2xx) and common failure (4xx, 5xx) cases.
- [ ] Rate limits are documented in headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`).
- [ ] All request payloads require strict JSON schema validation.
- [ ] Contract breaking changes are blocked in CI via schema diff comparison.
