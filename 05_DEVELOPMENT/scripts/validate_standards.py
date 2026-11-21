#!/usr/bin/env python3
"""
validate_standards.py - Master AI Full-Stack Standards Validator
Validates STANDARDS_REGISTRY.json and checks that all listed standards files exist,
are non-empty, and contain required structural sections.
"""

import os
import sys
import json
from pathlib import Path

def validate_standards():
    workspace_root = Path(__file__).resolve().parent.parent.parent
    standards_dir = workspace_root / "05_DEVELOPMENT" / "standards"
    registry_path = standards_dir / "STANDARDS_REGISTRY.json"

    errors = []
    print(f"[+] Validating Engineering Standards in: {standards_dir}")

    if not registry_path.exists():
        print(f"[!] Registry file missing: {registry_path}")
        return False

    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        print(f"[!] JSON parsing error in registry: {e}")
        return False

    standards_list = registry.get("standards", [])
    if len(standards_list) < 8:
        errors.append(f"Expected at least 8 standards, found {len(standards_list)}")

    for std in standards_list:
        std_id = std.get("id")
        title = std.get("title")
        rel_path = std.get("path") or std.get("file")

        if not std_id or not title or not rel_path:
            errors.append(f"Incomplete entry in registry: {std}")
            continue

        target_file = workspace_root / rel_path if not Path(rel_path).is_absolute() else Path(rel_path)
        if not target_file.exists():
            # Try within standards_dir
            target_file = standards_dir / Path(rel_path).name
        if not target_file.exists():
            errors.append(f"Standard file does not exist on disk: {target_file}")
            continue

        content = target_file.read_text(encoding="utf-8")
        if len(content.strip()) < 200:
            errors.append(f"Standard file '{rel_path}' appears too short ({len(content)} chars)")

        # Verify key markdown elements
        if not content.startswith("#"):
            errors.append(f"Standard file '{rel_path}' does not start with a markdown header")

        print(f"  [✓] Standard {std_id}: '{title}' ({target_file.name}) verified")

    if errors:
        print("[!] Standards validation FAILED:")
        for err in errors:
            print(f"    - {err}")
        return False

    print(f"[✓] ALL {len(standards_list)} STANDARDS PASSED VALIDATION.")
    return True

if __name__ == "__main__":
    success = validate_standards()
    sys.exit(0 if success else 1)
