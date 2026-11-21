# MASTER-AI Global Configuration Deployment Policy (Windows 11)

> **Policy Level**: MANDATORY GOVERNANCE  
> **Target Environment**: Windows 11 / Antigravity Standalone IDE  
> **Core Principle**: MANUAL USER APPROVAL REQUIRED FOR ALL GLOBAL ACTIONS  

---

## 1. Scope & System Boundaries

MASTER-AI operates on the principle that the **Master repository is the single sovereign source of truth**, completely separate from deployed runtime environments.

Deploying customizations globally modifies the behavior of the Antigravity IDE across **every project on the user's workstation**. Therefore, global deployments are treated with the highest level of security scrutiny.

---

## 2. Official Windows 11 Antigravity Target Locations

All global deployments must target only the officially recognized Antigravity configuration paths:

| Component Type | Official Windows 11 Target Location | Scope |
| :--- | :--- | :--- |
| **Global Skills** | `%USERPROFILE%\.gemini\config\skills\<skill_name>\` | Machine-wide: Accessible across all projects |
| **Global Rules** | `%USERPROFILE%\.gemini\AGENTS.md` | Machine-wide: Primary root rule loaded everywhere |
| **Modular Global Rules** | `%USERPROFILE%\.gemini\config\rules\*.md` | Machine-wide: Categorized rule modules |
| **Global MCP Config** | `%USERPROFILE%\.gemini\config\mcp_config.json` | Machine-wide: External tool server integrations |
| **Workspace Skills** | `<ProjectRoot>\.agents\skills\<skill_name>\` | Project-specific: Isolated to current repository |
| **Workspace Rules** | `<ProjectRoot>\.agents\rules\*.md` | Project-specific: Local directory constraints |

---

## 3. The 5 Inviolable Deployment Rules

1. **Decoupled Source of Truth**: Files never live solely in `%USERPROFILE%\.gemini\`. They must be authored, tested, and versioned inside `MASTER-AI` first.
2. **No Automatic Installations**: Autonomous agents are strictly prohibited from copying, linking, or writing to `%USERPROFILE%\.gemini\` without explicit user sign-off.
3. **Single-Target Approval**: Approval granted for one skill or rule does NOT authorize deployment of any other item.
4. **Mandatory Snapshot Backup**: An automated backup of `%USERPROFILE%\.gemini\config\` must be recorded in `22_PUBLISH_AND_DEPLOY/backups/` before any file write.
5. **Instant Rollback Guarantee**: Every deployment must be accompanied by an automated, verified reversal mechanism.
