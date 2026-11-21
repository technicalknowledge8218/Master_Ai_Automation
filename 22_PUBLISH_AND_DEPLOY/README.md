# 22_PUBLISH_AND_DEPLOY — Antigravity Deployment & Publishing Engine

## 1. Executive Purpose
Automated, safe deployment pipeline to package, validate, and publish Master AI skills, rules, and tools to global Antigravity config.

This domain serves as an integral pillar of the **MASTER-AI Ecosystem**, providing structured knowledge, standardized workflows, and verified engineering assets.

## 2. Directory Architecture
```text
22_PUBLISH_AND_DEPLOY/
├── README.md
├── antigravity_global/
├── scripts/
├── backups/
├── manifests/
```

### Subfolder Breakdown:
- `/antigravity_global`: Dedicated subfolder for antigravity global.
- `/scripts`: Dedicated subfolder for scripts.
- `/backups`: Dedicated subfolder for backups.
- `/manifests`: Dedicated subfolder for manifests.

## 3. Operational Protocols & Usage
- **Scope & Context**: Includes backup verification, namespace collision detection, dry-run validation, and instant rollback capability.
- **Rollback Utility**: Automated CLI in `22_PUBLISH_AND_DEPLOY/scripts/rollback.py`:
  - List available snapshots: `python 22_PUBLISH_AND_DEPLOY/scripts/rollback.py --list`
  - Dry-run validation (default): `python 22_PUBLISH_AND_DEPLOY/scripts/rollback.py --snapshot <archive_name>`
  - Live execution (requires `--execute`): `python 22_PUBLISH_AND_DEPLOY/scripts/rollback.py --snapshot <archive_name> --execute`
  - Safety guarantees: ZipSlip path traversal prevention, global directory extraction rejection, and mandatory pre-rollback safety snapshot generation before any live restoration.
- **Verification Rule**: All implementations, files, and updates placed in this directory must adhere to the Master Rulebook in `01_GLOBAL_RULES` and have verified references.
- **Progressive Learning**: Whenever new patterns or operational standards are developed in this domain, record learnings in `21_LEARNING_LAB` and update the relevant skills in `02_SKILLS`.

## 4. Antigravity Ecosystem Linkage
When an AI agent operates within this domain, it must cross-reference:
- Master Architecture: `[MASTER_AI_ARCHITECTURE.md](../MASTER_AI_ARCHITECTURE.md)`
- Global Rulebook: `[MASTER_AI_RULEBOOK.md](../MASTER_AI_RULEBOOK.md)`
- System Registry: `[00_CORE_SYSTEM/registry/](../00_CORE_SYSTEM/registry/)`
