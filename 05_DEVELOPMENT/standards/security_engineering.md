# MASTER-AI Full-Stack Standards: Security Engineering

> **Domain**: `05_DEVELOPMENT/standards/`  
> **Status**: APPROVED & ACTIVE (Phase 5)  
> **Reviewer**: AGT-006 Security Auditor  
> **Security Posture**: Zero-Trust, Secret-Zero, Fail-Closed, Least-Privilege  

---

## 1. OWASP Top 10 Defense-in-Depth

| Vulnerability Category | Root Cause | Mandatory Defensive Requirement |
| :--- | :--- | :--- |
| **A01: Broken Access Control** | Missing authorization checks on endpoints or record IDs | Enforce explicit deny-by-default on every route. Verify resource ownership (`WHERE user_id = current_user.id`) on all mutations. |
| **A02: Cryptographic Failures** | Weak ciphers, plain secrets, unencrypted transmission | Mandate TLS 1.3 in transit and AES-256-GCM at rest. Prohibit hardcoded keys. |
| **A03: Injection (SQL/NoSQL/OS)** | Concatenating untrusted user input into interpreters | Use parameterized queries and prepared statements exclusively. Validate all inputs against strict schemas (Zod/Pydantic). |
| **A04: Insecure Design** | Absence of threat modeling during architecture | Conduct STRIDE threat modeling before writing code for any new service. |
| **A05: Security Misconfiguration** | Verbose errors, default accounts, exposed debug ports | Disable debug modes, hide detailed stack traces from clients, enforce hardened headers via `Helmet`. |
| **A06: Vulnerable Components** | Outdated libraries with known CVEs | Enforce automated SCA scanning (`npm audit`, `pip-audit`, Dependabot) in CI quality gates. |
| **A07: Identification Failures** | Weak passwords, brute-force vulnerabilities, insecure sessions | Enforce multi-factor authentication (MFA), argon2id password hashing, and IP/user rate limiting. |
| **A08: Software Integrity Failures** | Tampered dependencies or unverified build pipelines | Verify cryptographic checksums for dependencies and package releases. |
| **A09: Logging & Monitoring Failures** | Missing audit trails or logging sensitive data | Centralize structured JSON logs. Never log passwords, tokens, or PII. |
| **A10: SSRF** | Unsanitized server-side fetches of user-provided URLs | Validate URLs against strict allowlists. Block requests to loopback and private CIDR ranges (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.169.254`). |

---

## 2. The Secret-Zero Mandate

1. **Zero Hardcoded Secrets**: Under no circumstances may API keys, passwords, database credentials, private certificates, or bearer tokens appear in source code, markdown, or Git history.
2. **Environment Variable Injection**: All credentials must be ingested via environment variables or managed secret vaults (Google Cloud Secret Manager, AWS Secrets Manager, HashiCorp Vault).
3. **Automated Static Scanning**: Pre-commit hooks and CI gates must execute automated secret scanning (`gitleaks`, entropy detectors) to block commits containing sensitive patterns.

---

## 3. JWT & Session Management

- **Short-Lived Access Tokens**: JWTs must have a maximum validity of 15 minutes.
- **Asymmetric Signing**: Sign tokens using RS256 or ES256 with managed private keys. Never accept the `none` algorithm.
- **Secure Cookie Transport**: Refresh tokens must reside exclusively in cookies configured with:
  `HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth/refresh`
- **Immediate Invalidation**: Maintain a revocation list (Redis TTL) for revoking refresh tokens upon logout or account compromise.

---

## 4. Secure File Upload Protocols

When handling user file uploads (images, documents, videos):
1. **Never Trust File Extensions**: Inspect magic byte signatures at the file header (e.g., using `file-type`) to verify actual MIME type.
2. **Randomize Filenames**: Generate a cryptographic UUID for the filename on storage (e.g., `upload_f47ac10b.png`). Never use the client-supplied original filename on disk.
3. **Storage Isolation**: Store uploads in isolated object storage buckets (S3, GCS) with public access blocked. Serve files via signed URLs or a dedicated CDN with sanitized content headers (`Content-Disposition: attachment` for executable/untrusted types).
4. **Size Caps**: Enforce strict size limits at the reverse proxy (e.g., max 5MB for images, 50MB for video).
