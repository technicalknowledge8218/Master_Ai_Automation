#!/usr/bin/env python3
"""
MASTER-AI Architecture Decision Record (ADR) Structure Validator
Validates ADR markdown documents for required sections, valid status, unique identifier,
considered alternatives, and relative link integrity.
"""

import argparse
import json
import os
import re
import sys

VALID_STATUSES = ["PROPOSED", "ACCEPTED", "SUPERSEDED", "DEPRECATED"]

def validate_adr(adr_path):
    if not os.path.exists(adr_path):
        return {"passed": False, "errors": [f"File does not exist: {adr_path}"]}

    try:
        with open(adr_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"passed": False, "errors": [f"File read error: {str(e)}"]}

    errors = []
    # 1. Identifier check
    title_match = re.search(r"#\s*(ADR-\d+):\s*(.+)", content)
    if not title_match:
        errors.append("Missing valid title format: '# ADR-NNN: Title'")
        adr_id = "UNKNOWN"
        adr_title = "UNKNOWN"
    else:
        adr_id = title_match.group(1)
        adr_title = title_match.group(2).strip()

    # 2. Status check
    status_match = re.search(r"\*\*Status\*\*:\s*([A-Za-z]+)", content)
    if not status_match:
        errors.append("Missing '**Status**:' field in metadata header.")
        status = "UNKNOWN"
    else:
        status = status_match.group(1).upper()
        if status not in VALID_STATUSES:
            errors.append(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}.")

    # 3. Required sections
    req_sections = [
        (r"##\s*1\.\s*Context", "Context section ('## 1. Context')"),
        (r"##\s*2\.\s*Decision", "Decision section ('## 2. Decision')"),
        (r"##\s*3\.\s*Alternatives Considered", "Alternatives section ('## 3. Alternatives Considered')"),
        (r"##\s*4\.\s*Consequences", "Consequences section ('## 4. Consequences')")
    ]
    for pattern, name in req_sections:
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Missing required section: {name}")

    # 4. Check relative links inside ADR
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    broken_links = []
    base_dir = os.path.dirname(os.path.abspath(adr_path))
    for match in link_pattern.finditer(content):
        _, target = match.groups()
        if target.startswith(("http://", "https://", "#", "mailto:", "file:")):
            continue
        clean_target = target.split("#")[0]
        if not clean_target:
            continue
        resolved = os.path.normpath(os.path.join(base_dir, clean_target))
        if not os.path.exists(resolved):
            broken_links.append(f"{target} -> unresolved: {resolved}")

    if broken_links:
        errors.extend([f"Broken relative link: {b}" for b in broken_links])

    return {
        "file": adr_path,
        "adr_id": adr_id,
        "title": adr_title,
        "status": status,
        "errors": errors,
        "passed": len(errors) == 0
    }

def main():
    parser = argparse.ArgumentParser(description="Validate Architecture Decision Record (ADR)")
    parser.add_argument("--adr", required=True, help="Path to ADR markdown file")
    args = parser.parse_args()

    result = validate_adr(args.adr)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)

if __name__ == "__main__":
    main()
