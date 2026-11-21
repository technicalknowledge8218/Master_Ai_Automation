#!/usr/bin/env python3
"""
MASTER-AI Safe Workspace Rollback Utility
Enforces safe snapshot verification, ZipSlip rejection, dry-run simulation, and pre-rollback snapshotting.
"""

import argparse
import datetime
import json
import os
import sys
import zipfile
import importlib
from pathlib import Path

# Resolve workspace root dynamically via centralized path configuration
_current_dir = Path(__file__).resolve().parent
_workspace_candidate = _current_dir.parents[1]
if str(_workspace_candidate) not in sys.path:
    sys.path.insert(0, str(_workspace_candidate))

try:
    _path_config = importlib.import_module("00_CORE_SYSTEM.config.path_config")
    WORKSPACE_ROOT = str(_path_config.WORKSPACE_ROOT)
    SNAPSHOTS_DIR = str(_path_config.SNAPSHOTS_DIR)
    ROLLBACK_LOG_PATH = str(_path_config.ROLLBACK_LOG_DIR / "ROLLBACK_LOG.md")
except Exception:
    WORKSPACE_ROOT = os.getenv("MASTER_AI_ROOT", str(_workspace_candidate))
    SNAPSHOTS_DIR = os.path.join(WORKSPACE_ROOT, "23_CHANGELOG_AND_BACKUP", "snapshots")
    ROLLBACK_LOG_PATH = os.path.join(WORKSPACE_ROOT, "23_CHANGELOG_AND_BACKUP", "history", "ROLLBACK_LOG.md")

def is_safe_extraction_path(target_dir, member_path):
    """
    Guards against ZipSlip path traversal attacks.
    Ensures that extracting member_path stays strictly inside target_dir.
    """
    target_abs = os.path.abspath(target_dir)
    # Check for drive letter or root path in member_path
    if os.path.isabs(member_path) or member_path.startswith("/") or member_path.startswith("\\"):
        return False
    resolved = os.path.abspath(os.path.join(target_abs, member_path))
    return resolved.startswith(target_abs + os.sep) or resolved == target_abs

def list_snapshots(snapshots_dir=SNAPSHOTS_DIR):
    if not os.path.exists(snapshots_dir):
        return []
    snapshots = []
    for f in sorted(os.listdir(snapshots_dir), reverse=True):
        if f.endswith(".zip"):
            fp = os.path.join(snapshots_dir, f)
            size_kb = os.path.getsize(fp) / 1024.0
            snapshots.append({
                "filename": f,
                "path": fp,
                "size_kb": round(size_kb, 2),
                "created": datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime("%Y-%m-%d %H:%M:%S")
            })
    return snapshots

def validate_archive(zip_path, target_dir):
    """
    Validates zip integrity and guarantees zero ZipSlip path traversals.
    """
    if not os.path.exists(zip_path):
        return False, f"Snapshot archive not found: {zip_path}"

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            corrupted = zf.testzip()
            if corrupted:
                return False, f"Corrupted file in archive: {corrupted}"

            for info in zf.infolist():
                if not is_safe_extraction_path(target_dir, info.filename):
                    return False, f"SECURITY ALERT: Unsafe path detected in archive: '{info.filename}' (ZipSlip attempt rejected)"
        return True, "Archive validation passed successfully"
    except Exception as e:
        return False, f"Archive read error: {str(e)}"

def log_rollback_action(operation, snapshot_id, status, target_dir, details):
    os.makedirs(os.path.dirname(ROLLBACK_LOG_PATH), exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
### Rollback Event: `{snapshot_id}`
- **Timestamp**: `{timestamp}`
- **Operation**: `{operation}`
- **Status**: `{status}`
- **Target Directory**: `{target_dir}`
- **Details**: {details}
---
"""
    with open(ROLLBACK_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

def execute_rollback(snapshot_path, target_dir=WORKSPACE_ROOT, dry_run=True):
    # Security check on target_dir: NEVER allow global configuration path
    target_abs = os.path.abspath(target_dir)
    user_home = os.path.expanduser("~")
    gemini_global = os.path.abspath(os.path.join(user_home, ".gemini"))
    if target_abs.startswith(gemini_global):
        log_rollback_action("ABORTED", os.path.basename(snapshot_path), "FAILED", target_dir, "Targeting global config is strictly prohibited.")
        return False, "SECURITY ERROR: Rollback utility cannot target global configuration directory."

    valid, msg = validate_archive(snapshot_path, target_dir)
    if not valid:
        log_rollback_action("VALIDATION_FAILED", os.path.basename(snapshot_path), "FAILED", target_dir, msg)
        return False, msg

    with zipfile.ZipFile(snapshot_path, "r") as zf:
        members = zf.infolist()
        total_files = len(members)

        if dry_run:
            preview = [m.filename for m in members[:10]]
            log_rollback_action("DRY_RUN", os.path.basename(snapshot_path), "SUCCESS", target_dir, f"Simulated restoration of {total_files} files.")
            return True, f"DRY-RUN SUCCESS: Archive valid. {total_files} files would be restored. Preview: {preview}"

        # If --execute is specified: Create fresh safety snapshot before extracting
        pre_rollback_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pre_rollback_zip = os.path.join(SNAPSHOTS_DIR, f"pre_rollback_safety_{pre_rollback_ts}.zip")
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

        with zipfile.ZipFile(pre_rollback_zip, "w", zipfile.ZIP_DEFLATED) as pre_zf:
            for dirpath, dirnames, filenames in os.walk(target_dir):
                if "snapshots" in dirpath or ".git" in dirpath:
                    continue
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    rel = os.path.relpath(fp, target_dir)
                    pre_zf.write(fp, rel)

        # Extract archive safely
        for member in members:
            zf.extract(member, target_dir)

        log_rollback_action("RESTORE_EXECUTED", os.path.basename(snapshot_path), "SUCCESS", target_dir, f"Restored {total_files} files. Pre-rollback safety backup saved at {pre_rollback_zip}")
        return True, f"RESTORE COMPLETE: {total_files} files restored. Safety backup created at {pre_rollback_zip}"

def main():
    parser = argparse.ArgumentParser(description="Safe Workspace Rollback Utility")
    parser.add_argument("--list", action="store_true", help="List available verified backup snapshots")
    parser.add_argument("--snapshot", help="Filename or path of snapshot archive to restore")
    parser.add_argument("--target-dir", default=WORKSPACE_ROOT, help="Target extraction directory (default: workspace root)")
    parser.add_argument("--execute", action="store_true", help="Execute actual restoration (default is dry-run)")
    args = parser.parse_args()

    if args.list:
        snaps = list_snapshots()
        print(json.dumps(snaps, indent=2))
        sys.exit(0)

    if not args.snapshot:
        print("ERROR: --snapshot <filename_or_path> is required when not listing snapshots.", file=sys.stderr)
        sys.exit(1)

    snap_path = args.snapshot
    if not os.path.isabs(snap_path) and not os.path.exists(snap_path):
        snap_path = os.path.join(SNAPSHOTS_DIR, args.snapshot)

    dry_run = not args.execute
    success, message = execute_rollback(snap_path, target_dir=args.target_dir, dry_run=dry_run)

    result = {
        "snapshot": os.path.basename(snap_path),
        "target_directory": args.target_dir,
        "mode": "DRY_RUN (Simulation)" if dry_run else "EXECUTE (Live Restoration)",
        "success": success,
        "message": message
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
