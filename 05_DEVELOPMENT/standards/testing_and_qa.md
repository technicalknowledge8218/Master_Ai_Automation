# MASTER-AI Full-Stack Standards: Testing and QA

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Reviewer**: AGT-004 Testing Agent  

---

## 1. The 4-Tier Testing Pyramid

MASTER-AI full-stack engineering enforces a balanced **4-Tier Testing Pyramid** to ensure rapid feedback, high reliability, and zero-defect deployments:

```
        ▲
       / \
      / E2E \       Tier 4: End-to-End Tests (Playwright)
     /───────\      Critical user journeys, cross-browser, visual regression (10%)
    / Contract\     Tier 3: API Contract Tests (Pact / OpenAPI Spec Validation)
   /───────────\    Schema validation, request/response verification (15%)
  / Integration \   Tier 2: Integration Tests (Supertest / Testcontainers)
 /───────────────\  Database transactions, API endpoints, middleware chains (25%)
/   Unit Tests    \ Tier 1: Unit Tests (Vitest / PyTest)
─────────────────── Pure functions, domain entities, use case interactors (50%)
```

---

## 2. Test Coverage & Quality Gates

1. **Coverage Thresholds**:
   - **Domain / Business Logic**: Minimum **80% line and branch coverage**.
   - **Infrastructure / Adapters**: Minimum **70% coverage**.
   - **Presentational UI**: Component interaction and snapshot tests on key visual states.
2. **Deterministic Test Execution**:
   - Tests must execute deterministically without flaky dependencies.
   - External network access is strictly prohibited during test execution; all third-party APIs must be mocked using deterministic fixtures (MSW for web, responses for Python).
   - Use fixed seed values and frozen clock utilities (`vi.useFakeTimers()`, `time-machine`) when testing time-dependent logic.

---

## 3. Negative Testing & Boundary Assertions

Every test suite must test failure modes with equal rigor to the happy path:
- **Input Boundaries**: Empty strings, null bytes, maximum character limits, out-of-range numeric values.
- **Security Boundaries**: Unauthenticated access (401), unauthorized tenant cross-access (403), malicious SQL injection payloads, XSS strings.
- **Resilience Boundaries**: Database timeouts, third-party service 500 errors, network dropouts.
- **Rule**: Every API endpoint must have at least 3 negative test cases for every 1 positive test case.

---

## 4. End-to-End (E2E) Testing with Playwright

Playwright is the standard E2E testing framework for web and mobile web:
1. **User Journey Focus**: Test complete user workflows (Sign Up $\rightarrow$ Email Verification $\rightarrow$ Onboarding $\rightarrow$ Checkout).
2. **Resilient Selectors**: Select elements by user-facing accessibility roles (`getByRole('button', { name: 'Submit' })`) or test IDs (`data-testid`), never brittle CSS classes or deep XPath selectors.
3. **Automatic Retries & Tracing**: Capture video and execution traces on test failure in CI to facilitate rapid debugging.
