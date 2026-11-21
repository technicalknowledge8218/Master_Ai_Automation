#!/usr/bin/env python3
"""
Capability Gap & Domain Readiness Evaluator
Reads the Capability Registry to determine whether active skills, agents, or tools cover a target domain.
"""

import argparse
import json
import os
import sys
import importlib
from pathlib import Path

# Resolve workspace root dynamically via centralized path configuration
_current_dir = Path(__file__).resolve().parent
_workspace_candidate = _current_dir.parents[2]
if str(_workspace_candidate) not in sys.path:
    sys.path.insert(0, str(_workspace_candidate))

try:
    _path_config = importlib.import_module("00_CORE_SYSTEM.config.path_config")
    WORKSPACE_ROOT = str(_path_config.WORKSPACE_ROOT)
except Exception:
    WORKSPACE_ROOT = os.getenv("MASTER_AI_ROOT", str(_workspace_candidate))

def evaluate_domain_gap(domain_id):
    reg_path = os.path.join(WORKSPACE_ROOT, "00_CORE_SYSTEM", "registry", "CAPABILITY_REGISTRY.json")
    if not os.path.exists(reg_path):
        return {"error": "Registry not found", "passed": False}

    with open(reg_path, "r", encoding="utf-8") as f:
        reg = json.load(f)

    target_domain = None
    for d in reg.get("domains", []):
        if d.get("id") == domain_id or d.get("name").lower() == domain_id.lower():
            target_domain = d
            break

    if not target_domain:
        return {"error": f"Domain '{domain_id}' not found in registry", "passed": False}

    matched_skills = [s for s in reg.get("skills", []) if s.get("domain_id") == target_domain["id"]]
    matched_agents = [a for a in reg.get("agents", []) if a.get("primary_domain") == target_domain["id"]]
    matched_repos = [g for g in reg.get("github_repositories", []) if g.get("domain_id") == target_domain["id"]]

    has_coverage = len(matched_skills) > 0 or len(matched_agents) > 0
    readiness = "READY" if (len(matched_skills) > 0 and len(matched_agents) > 0) else ("PARTIAL" if has_coverage else "GAP")

    return {
        "domain_id": target_domain["id"],
        "domain_name": target_domain["name"],
        "category": target_domain["category"],
        "readiness_status": readiness,
        "covering_skills": [s["name"] for s in matched_skills],
        "covering_agents": [a["name"] for a in matched_agents],
        "curated_github_repos": [g["repo"] for g in matched_repos],
        "passed": True
    }

def main():
    parser = argparse.ArgumentParser(description="Evaluate domain readiness and capability gap")
    parser.add_argument("--domain", required=True, help="Domain ID (e.g., DOM-02) or name")
    args = parser.parse_args()

    result = evaluate_domain_gap(args.domain)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
