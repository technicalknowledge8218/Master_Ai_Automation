#!/usr/bin/env python3
"""
Static Lint & Secret Hygiene Checker
Scans source files for common security flaws and code quality antipatterns.
"""

import argparse
import re
import sys
import json
import os

SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|secret|password|token|bearer)\s*=\s*['\"][A-Za-z0-9_\-\.]{12,}['\"]", "Possible hardcoded API key or secret"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI Secret Key"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key")
]

ANTIPATTERNS = [
    (r"except:\s*$", "Bare except clause (Python antipattern)"),
    (r"\beval\(", "Insecure eval() call"),
    (r"\bexec\(", "Insecure exec() call"),
    (r":\s*any\b", "Forbidden 'any' type annotation in TypeScript")
]

def scan_file(file_path):
    issues = []
    if not os.path.exists(file_path):
        return {"file": file_path, "error": "File does not exist", "passed": False}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        for pat, desc in SECRET_PATTERNS:
            if re.search(pat, line):
                issues.append({"line": idx, "type": "SECRET_LEAK", "message": desc})
        for pat, desc in ANTIPATTERNS:
            if re.search(pat, line):
                issues.append({"line": idx, "type": "ANTIPATTERN", "message": desc})

    return {
        "file": file_path,
        "scanned_lines": len(lines),
        "issues_count": len(issues),
        "issues": issues,
        "passed": len(issues) == 0
    }

def main():
    parser = argparse.ArgumentParser(description="Check source file for secrets and antipatterns")
    parser.add_argument("--target", required=True, help="File path to scan")
    args = parser.parse_args()

    result = scan_file(args.target)
    print(json.dumps(result, indent=2))
    if not result.get("passed"):
        sys.exit(1)

if __name__ == "__main__":
    main()
