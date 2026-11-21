#!/usr/bin/env python3
"""
MASTER-AI Automated Quality Gate Framework
Validates skills, agents, registry, link integrity, security rules, and approval requirements.
"""

import os
import re
import json
import yaml
import sys
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
except Exception:
    WORKSPACE_ROOT = os.getenv("MASTER_AI_ROOT", str(_workspace_candidate))

# Standard excluded directories for scanners (pruned during os.walk)
EXCLUDED_SCAN_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    "23_CHANGELOG_AND_BACKUP",
    "snapshots",
}

SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|secret|password|token)\s*=\s*['\"][A-Za-z0-9_\-\.]{14,}['\"]", "Possible hardcoded secret"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI Secret Key")
]

def check_skills():
    skills_dir = os.path.join(WORKSPACE_ROOT, "02_SKILLS")
    results = {"total": 0, "passed": 0, "failures": []}
    if not os.path.exists(skills_dir):
        return results

    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path) and item not in ["references", "scripts", "templates", "core_skills", "domain_skills"]:
            skill_md = os.path.join(skill_path, "SKILL.md")
            results["total"] += 1
            if not os.path.exists(skill_md):
                results["failures"].append(f"{item}: Missing SKILL.md")
                continue
            try:
                with open(skill_md, "r", encoding="utf-8") as f:
                    content = f.read()
                if not content.startswith("---"):
                    results["failures"].append(f"{item}: Missing frontmatter delimiters")
                    continue
                parts = content.split("---", 2)
                fm = yaml.safe_load(parts[1])
                if not fm or "name" not in fm or "description" not in fm:
                    results["failures"].append(f"{item}: Missing name or description in YAML frontmatter")
                    continue
                if not re.match(r"^[a-z0-9-]+$", fm["name"]):
                    results["failures"].append(f"{item}: Name '{fm['name']}' is not valid lowercase-kebab-case")
                    continue
                results["passed"] += 1
            except Exception as e:
                results["failures"].append(f"{item}: YAML parse error: {e}")
    return results

def check_agents():
    agents_dir = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "definitions")
    results = {"total": 0, "passed": 0, "failures": []}
    if not os.path.exists(agents_dir):
        return results

    for item in os.listdir(agents_dir):
        if item.endswith(".json"):
            results["total"] += 1
            p = os.path.join(agents_dir, item)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                req_fields = ["id", "name", "role", "system_prompt", "tools_allowed", "tools_prohibited"]
                missing = [rf for rf in req_fields if rf not in data]
                if missing:
                    results["failures"].append(f"{item}: Missing required fields {missing}")
                else:
                    results["passed"] += 1
            except Exception as e:
                results["failures"].append(f"{item}: Invalid JSON: {e}")
    return results

def check_registry_integrity():
    reg_path = os.path.join(WORKSPACE_ROOT, "00_CORE_SYSTEM", "registry", "CAPABILITY_REGISTRY.json")
    results = {"passed": False, "failures": []}
    if not os.path.exists(reg_path):
        results["failures"].append("CAPABILITY_REGISTRY.json not found")
        return results

    try:
        with open(reg_path, "r", encoding="utf-8") as f:
            reg = json.load(f)

        # Check skills existence
        for s in reg.get("skills", []):
            sp = os.path.join(WORKSPACE_ROOT, s.get("path", ""))
            if not os.path.exists(sp):
                results["failures"].append(f"Registered skill path missing: {s.get('path')}")

        # Check agents existence
        for a in reg.get("agents", []):
            ap = os.path.join(WORKSPACE_ROOT, a.get("definition_file", ""))
            if not os.path.exists(ap):
                results["failures"].append(f"Registered agent definition missing: {a.get('definition_file')}")

        # Check duplicate IDs
        all_ids = [d["id"] for d in reg.get("domains", [])] + [s["id"] for s in reg.get("skills", [])] + [a["id"] for a in reg.get("agents", [])]
        duplicates = [x for x in all_ids if all_ids.count(x) > 1]
        if duplicates:
            results["failures"].append(f"Duplicate IDs detected: {set(duplicates)}")

        results["passed"] = len(results["failures"]) == 0
    except Exception as e:
        results["failures"].append(f"Registry parse error: {e}")
    return results

def check_security():
    results = {"scanned_files": 0, "secret_leaks": [], "passed": True}
    for dirpath, dirnames, filenames in os.walk(WORKSPACE_ROOT):
        # Prune excluded directories in-place to prevent traversing dependencies/build/cache
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_SCAN_DIRS]
        for f in filenames:
            if f.endswith((".py", ".json", ".md", ".sh", ".yaml", ".yml")):
                results["scanned_files"] += 1
                fp = os.path.join(dirpath, f)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                        lines = fh.readlines()
                    for idx, line in enumerate(lines, 1):
                        for pat, desc in SECRET_PATTERNS:
                            if re.search(pat, line):
                                results["secret_leaks"].append({
                                    "file": os.path.relpath(fp, WORKSPACE_ROOT),
                                    "line": idx,
                                    "desc": desc
                                })
                except Exception:
                    pass
    results["passed"] = len(results["secret_leaks"]) == 0
    return results

def check_links():
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    results = {"scanned_docs": 0, "broken_links": [], "passed": True}
    for dirpath, dirnames, filenames in os.walk(WORKSPACE_ROOT):
        # Prune excluded directories and template directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_SCAN_DIRS and d != "17_TEMPLATES"]
        for f in filenames:
            if f.endswith(".md"):
                results["scanned_docs"] += 1
                fp = os.path.join(dirpath, f)
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                for match in link_pattern.finditer(content):
                    _, target = match.groups()
                    if target.startswith(("http://", "https://", "#", "mailto:", "file:")):
                        continue
                    clean_target = target.split("#")[0]
                    if not clean_target:
                        continue
                    resolved = os.path.normpath(os.path.join(dirpath, clean_target))
                    if not os.path.exists(resolved):
                        results["broken_links"].append({
                            "source": os.path.relpath(fp, WORKSPACE_ROOT),
                            "target": target,
                            "resolved": os.path.relpath(resolved, WORKSPACE_ROOT)
                        })
    results["passed"] = len(results["broken_links"]) == 0
    return results

def run_all_gates():
    skills_res = check_skills()
    agents_res = check_agents()
    reg_res = check_registry_integrity()
    sec_res = check_security()
    links_res = check_links()

    overall_passed = (
        len(skills_res["failures"]) == 0 and
        len(agents_res["failures"]) == 0 and
        reg_res["passed"] and
        sec_res["passed"] and
        links_res["passed"]
    )

    report = {
        "status": "ALL_GATES_PASSED" if overall_passed else "QUALITY_GATE_FAILED",
        "skills_audit": skills_res,
        "agents_audit": agents_res,
        "registry_integrity": reg_res,
        "security_audit": sec_res,
        "link_integrity": links_res
    }

    out_file = os.path.join(WORKSPACE_ROOT, "18_TESTING_AND_QA", "test_suites", "quality_gate_results.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    return overall_passed

if __name__ == "__main__":
    passed = run_all_gates()
    sys.exit(0 if passed else 1)
