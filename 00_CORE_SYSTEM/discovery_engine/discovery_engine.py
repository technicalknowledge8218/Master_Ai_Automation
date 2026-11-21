import os
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

def scan_workspace_skills(workspace_root):
    skills_dir = os.path.join(workspace_root, "02_SKILLS")
    discovered = []
    if not os.path.exists(skills_dir):
        return discovered
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path) and item not in ["references", "scripts", "templates", "core_skills", "domain_skills"]:
            skill_md = os.path.join(skill_path, "SKILL.md")
            if os.path.exists(skill_md):
                try:
                    with open(skill_md, "r", encoding="utf-8") as f:
                        content = f.read()
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        fm = yaml.safe_load(parts[1])
                        discovered.append({
                            "name": fm.get("name", item),
                            "description": fm.get("description", "").strip(),
                            "path": os.path.relpath(skill_md, workspace_root),
                            "has_references": os.path.exists(os.path.join(skill_path, "references")),
                            "has_scripts": os.path.exists(os.path.join(skill_path, "scripts")),
                            "has_examples": os.path.exists(os.path.join(skill_path, "examples")),
                            "valid_frontmatter": True
                        })
                    else:
                        discovered.append({
                            "name": item,
                            "path": os.path.relpath(skill_md, workspace_root),
                            "valid_frontmatter": False,
                            "error": "Missing frontmatter delimiters"
                        })
                except Exception as e:
                    discovered.append({
                        "name": item,
                        "path": os.path.relpath(skill_md, workspace_root),
                        "valid_frontmatter": False,
                        "error": str(e)
                    })
    return discovered

def scan_workspace_agents(workspace_root):
    agents_dir = os.path.join(workspace_root, "03_AI_AGENTS", "definitions")
    discovered = []
    if not os.path.exists(agents_dir):
        return discovered
    for item in os.listdir(agents_dir):
        if item.endswith(".json"):
            json_path = os.path.join(agents_dir, item)
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                discovered.append({
                    "id": data.get("id", item),
                    "name": data.get("name", item),
                    "role": data.get("role", ""),
                    "path": os.path.relpath(json_path, workspace_root),
                    "primary_domain": data.get("primary_domain", ""),
                    "tools_allowed": data.get("tools_allowed", []),
                    "tools_prohibited": data.get("tools_prohibited", []),
                    "valid_json": True
                })
            except Exception as e:
                discovered.append({
                    "id": item,
                    "path": os.path.relpath(json_path, workspace_root),
                    "valid_json": False,
                    "error": str(e)
                })
    return discovered

def scan_host_mcp():
    mcp_path = os.path.expanduser(r"~\.gemini\config\mcp_config.json")
    if os.path.exists(mcp_path):
        try:
            with open(mcp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("mcpServers", {})
        except Exception as e:
            return {"error": str(e)}
    return {}

def evaluate_domain_coverage(registry, discovered_skills, discovered_agents):
    """
    Evaluates domain readiness across the 30 domains, distinguishing
    COVERED_READY (has tested skill and agent), COVERED_PARTIAL (has skill or agent),
    and UNCOVERED_GAP (zero workspace coverage).
    """
    domains = registry.get("domains", [])
    registered_skills = registry.get("skills", [])
    registered_agents = registry.get("agents", [])

    discovered_skill_names = set(s["name"] for s in discovered_skills if s.get("valid_frontmatter"))
    discovered_agent_ids = set(a["id"] for a in discovered_agents if a.get("valid_json"))

    coverage_list = []
    ready_count = 0
    partial_count = 0
    gap_count = 0

    for dom in domains:
        dom_id = dom["id"]
        # Find matching skills from registry that are actually on disk
        covering_skills = [
            s for s in registered_skills 
            if s.get("domain_id") == dom_id and s.get("name") in discovered_skill_names
        ]
        # Find matching agents from registry that are actually on disk
        covering_agents = [
            a for a in registered_agents 
            if a.get("primary_domain") == dom_id and a.get("id") in discovered_agent_ids
        ]

        has_skills = len(covering_skills) > 0
        has_agents = len(covering_agents) > 0

        # Ready means both an active tested skill AND an agent specification exist
        if has_skills and has_agents:
            status = "COVERED_READY"
            ready_count += 1
        elif has_skills or has_agents:
            status = "COVERED_PARTIAL"
            partial_count += 1
        else:
            status = "UNCOVERED_GAP"
            gap_count += 1

        coverage_list.append({
            "domain_id": dom_id,
            "domain_name": dom["name"],
            "category": dom["category"],
            "coverage_status": status,
            "covering_skills": [s["name"] for s in covering_skills],
            "covering_agents": [a["name"] for a in covering_agents]
        })

    return {
        "total_domains": len(domains),
        "covered_ready": ready_count,
        "covered_partial": partial_count,
        "uncovered_gaps": gap_count,
        "domains_coverage": coverage_list
    }

def run_discovery():
    workspace = WORKSPACE_ROOT
    skills = scan_workspace_skills(workspace)
    agents = scan_workspace_agents(workspace)
    mcp = scan_host_mcp()

    # Read registry
    reg_path = os.path.join(workspace, "00_CORE_SYSTEM", "registry", "CAPABILITY_REGISTRY.json")
    registry = {}
    if os.path.exists(reg_path):
        with open(reg_path, "r", encoding="utf-8") as f:
            registry = json.load(f)

    coverage = evaluate_domain_coverage(registry, skills, agents)

    report = {
        "timestamp": os.environ.get("LOCAL_TIME", "2026-11-17"),
        "workspace_skills_count": len(skills),
        "workspace_skills": skills,
        "workspace_agents_count": len(agents),
        "workspace_agents": agents,
        "host_mcp_servers_count": len(mcp) if isinstance(mcp, dict) else 0,
        "host_mcp_servers": list(mcp.keys()) if isinstance(mcp, dict) else [],
        "domain_readiness_summary": {
            "total_domains": coverage["total_domains"],
            "covered_ready": coverage["covered_ready"],
            "covered_partial": coverage["covered_partial"],
            "uncovered_gaps": coverage["uncovered_gaps"]
        },
        "domain_coverage_details": coverage["domains_coverage"],
        "status": "DISCOVERY_AND_GAP_EVALUATION_COMPLETE"
    }

    out_json = os.path.join(workspace, "00_CORE_SYSTEM", "registry", "DISCOVERY_REPORT.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps({
        "workspace_skills_count": report["workspace_skills_count"],
        "workspace_agents_count": report["workspace_agents_count"],
        "host_mcp_servers_count": report["host_mcp_servers_count"],
        "domain_readiness_summary": report["domain_readiness_summary"],
        "status": report["status"]
    }, indent=2))
    return report

if __name__ == "__main__":
    run_discovery()
