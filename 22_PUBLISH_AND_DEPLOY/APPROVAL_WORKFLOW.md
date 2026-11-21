# MASTER-AI Global Deployment Approval Workflow

> **Standard**: 10-Step Deterministic Human Approval Gate  
> **Source Directory**: `22_PUBLISH_AND_DEPLOY/`  

---

## 1. The 10-Step Approval Sequence

Whenever an agent or developer proposes publishing a component to global Antigravity configuration, it must execute this exact 10-step sequence:

```
[1. Identify Source] ────> [2. Identify Dest]   ────> [3. Justify Global]
                                                            │
[6. Check Compat]    <──── [5. Conflict Check]  <──── [4. Show Full Diff]
       │
       v
[7. Security Audit]  ────> [8. Create Backup]   ────> [9. Generate Report]
                                                            │
                                                            v
                                            [10. STOP & WAIT FOR APPROVAL]
```

### Granular Step Instructions:
1. **Identify Source**: State the absolute path of the verified file inside `MASTER-AI` (e.g., `02_SKILLS/technical-research/SKILL.md`).
2. **Identify Destination**: State the exact destination path in `%USERPROFILE%\.gemini\config\`.
3. **Explain Global Value**: Articulate why this component belongs globally across all user projects rather than remaining isolated in MASTER-AI.
4. **Show Complete Proposed Changes**: Display the complete, exact content or file diff that will be written.
5. **Check for Naming Conflicts**: Inspect the destination directory to ensure no identically named file or directory exists.
6. **Check Dependencies & Compatibility**: Verify that any referenced scripts, runtimes, or models are available on the host.
7. **Check Security Implications**: Verify that zero API keys, personal credentials, or dangerous bash commands exist in the payload.
8. **Create Backup Plan**: Specify the exact snapshot folder in `22_PUBLISH_AND_DEPLOY/backups/` where the current destination state will be preserved.
9. **Generate Approval Report**: Populate the standard [GLOBAL_DEPLOYMENT_TEMPLATE.md](../17_TEMPLATES/projects/GLOBAL_DEPLOYMENT_TEMPLATE.md).
10. **STOP AND WAIT**: End turn immediately. Do not execute any tool calls or filesystem writes. Wait for the user to explicitly reply: `APPROVED`.

---

## 2. Rejection & Non-Consent Rules

- **Silence is NOT Approval**: If the user gives a generic instruction or changes the subject, the deployment remains blocked.
- **Specific Authorization Only**: The user must explicitly confirm the specific named component.
- **Immediate Cancellation**: If the user declines or raises concerns, the deployment ticket is canceled, and the reason is recorded in `22_PUBLISH_AND_DEPLOY/manifests/`.

---

## 3. Rollback & Disaster Recovery Protocol

If an approved global deployment introduces unexpected behavior or conflicts, or if a workspace rollback is required:
1. **List Verified Snapshots**:
   ```bash
   python 22_PUBLISH_AND_DEPLOY/scripts/rollback.py --list
   ```
2. **Execute Dry-Run Simulation**:
   ```bash
   python 22_PUBLISH_AND_DEPLOY/scripts/rollback.py --snapshot master_ai_backup_<TIMESTAMP>.zip
   ```
3. **Execute Live Rollback (Safety Guaranteed)**:
   ```bash
   python 22_PUBLISH_AND_DEPLOY/scripts/rollback.py --snapshot master_ai_backup_<TIMESTAMP>.zip --execute
   ```
   *Note*: The utility automatically generates a pre-rollback safety snapshot before extracting, verifies that no zip entry attempts path traversal (ZipSlip prevention), and rejects any target pointing to the global `.gemini` directory.
4. **Log Incident & Forensic Audit**:
   Every rollback operation is automatically appended to `23_CHANGELOG_AND_BACKUP/history/ROLLBACK_LOG.md` with timestamp, operator, source snapshot, pre-rollback safety archive, and file counts.
