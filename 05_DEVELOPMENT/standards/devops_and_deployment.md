# MASTER-AI Full-Stack Standards: DevOps & Deployment

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Deployment Paradigms**: Containerized Microservices & Serverless Containers (Cloud Run)  

---

## 1. Git Workflow & Branching Strategy

MASTER-AI adopts **Trunk-Based Development** with short-lived feature branches:
1. **Branch Naming**:
   - `feat/<feature-slug>`: New features and capability expansions.
   - `fix/<bug-slug>`: Bug fixes and defect resolutions.
   - `chore/<maintenance-slug>`: Dependencies, refactoring, and tooling updates.
2. **Commit Message Standard (Conventional Commits)**:
   - Format: `<type>(<scope>): <short imperative description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
3. **Pull Request Quality Gates**:
   - Every PR must pass automated CI checks: linting, type-checking, unit tests, security scans, and link integrity.
   - No direct pushes to the main production branch (`master` / `main`).

---

## 2. Containerization Standards (Docker)

All backend services must be packaged using **multi-stage Docker builds**:
```dockerfile
# Stage 1: Build & Dependencies
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Stage 2: Minimal Production Image
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Run as unprivileged non-root user
USER node
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Container Security Invariants:
1. **Non-Root Execution**: Containers must never run as `root`. Always specify an unprivileged user (`USER node` or `USER 10001`).
2. **Minimal Base Images**: Use minimal base images (`alpine`, `distroless`, or `slim`) to reduce the attack surface and image size (< 150 MB).
3. **No Secrets in Images**: Never copy `.env` files or hardcode credentials into Dockerfiles. Pass configuration at runtime via environment variables.

---

## 3. Deployment Strategies & Zero-Downtime Rollbacks

1. **Blue-Green Deployments**: Maintain two identical production environments. Deploy and verify the new release on Green, then switch routing at the load balancer. If errors spike, route traffic back to Blue instantly.
2. **Canary Releases**: Route a small percentage of user traffic (e.g., 5%) to the new release while monitoring error rates, CPU usage, and latency. Gradually scale to 100% upon automated validation.
3. **Automated Health Checks**:
   - **Liveness Probe**: `/healthz/live` verifies that the process is responsive.
   - **Readiness Probe**: `/healthz/ready` verifies that database connections and external dependencies are initialized before receiving traffic.
4. **Disaster Recovery (DR) Objectives**:
   - **Recovery Point Objective (RPO)**: Maximum acceptable data loss window ($\le 15$ minutes via continuous WAL archiving).
   - **Recovery Time Objective (RTO)**: Maximum acceptable system recovery duration ($\le 30$ minutes via automated container orchestration).
