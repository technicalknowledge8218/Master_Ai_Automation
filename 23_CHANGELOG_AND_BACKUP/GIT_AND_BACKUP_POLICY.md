# MASTER-AI Git Governance, Versioning & Backup Policy

> **Objective**: Absolute Source Control Integrity & Zero Data Loss  
> **Source Directory**: `23_CHANGELOG_AND_BACKUP/`  

---

## 1. Git Repository Governance

1. **Private Repository Policy**: MASTER-AI must always reside in a private, encrypted Git repository. Under no circumstances may this knowledge base be initialized or pushed to a public remote repository without explicit user authorization.
2. **Human Permission Gate**: Agents are strictly forbidden from initializing remotes, creating remote tracking branches, or executing `git push` without prior explicit approval.

---

## 2. Branching & Commit Standards

### Branch Topology:
- `main`: The immutable, production-grade release branch. Only verified, tested knowledge and skills reside here.
- `develop`: The active integration branch where newly authored skills and modules are consolidated.
- `feature/<name>`: Dedicated feature branches for authoring major domain components.
- `spike/<name>`: Isolated branches for research experiments in `21_LEARNING_LAB`.

### Conventional Commit Conventions:
Every commit message must follow the Conventional Commits specification:
```text
<type>(<scope>): <concise description in present tense>

[optional body explaining motivation and architectural trade-offs]

[optional footer with issue or task reference]
```
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `gov` (governance).
- Example: `gov(constitution): ratify master ai operating constitution and laws`

---

## 3. Large Media & Secrets Exclusion

- **Zero Secrets Committed**: Enforced by pre-commit hooks and [.gitignore](../.gitignore). Files matching `.env*`, `*.pem`, `*.key` are permanently excluded.
- **Large Asset Management**: High-resolution video, raw footage, and large audio stems in `16_VIDEO_LIBRARY/` are excluded from standard Git commits. They must be managed via Git-LFS or tracked via cloud storage manifest references.

---

## 4. Multi-Tier Backup & Recovery Protocol

1. **Tier 1 (Local Snapshots)**: Automated filesystem snapshots generated before structural modifications, stored in `23_CHANGELOG_AND_BACKUP/snapshots/`.
2. **Tier 2 (Staging Backups)**: Pre-deployment snapshots of `%USERPROFILE%\.gemini\config\` stored in `22_PUBLISH_AND_DEPLOY/backups/`.
3. **Tier 3 (Git Archive)**: Periodic encrypted archive bundles (`git bundle create`) stored on secure secondary physical or private cloud storage.
