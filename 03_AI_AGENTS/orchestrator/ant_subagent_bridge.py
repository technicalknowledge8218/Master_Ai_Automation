"""
ant_subagent_bridge.py
MASTER-AI Antigravity Native Subagent Bridge

Provides integration manifests and parameters to register the 7 specialist agents
into Antigravity's native `define_subagent` and `invoke_subagent` runtime system.
"""

import os
import json
from typing import Dict, Any, List

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFINITIONS_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "definitions")


def get_all_subagent_specs() -> List[Dict[str, Any]]:
    """Loads all 7 specialist agent definitions formatted for define_subagent."""
    specs = []
    for f in sorted(os.listdir(DEFINITIONS_DIR)):
        if f.endswith(".json"):
            path = os.path.join(DEFINITIONS_DIR, f)
            with open(path, "r", encoding="utf-8") as jf:
                data = json.load(jf)

            can_write = "write_file" in data.get("tools_allowed", [])
            spec = {
                "Name": data["slug"],
                "Description": f"{data['name']} ({data['id']}): {data['role']}. Primary Domain: {data['primary_domain']}.",
                "SystemPrompt": data["system_prompt"],
                "EnableWriteTools": can_write,
                "EnableMCPTools": False,
                "EnableSubagentTools": False
            }
            specs.append(spec)
    return specs


def generate_subagent_registration_script() -> str:
    """Generates Python snippet showing how define_subagent registers all 7 agents."""
    specs = get_all_subagent_specs()
    return json.dumps(specs, indent=2)


if __name__ == "__main__":
    print(generate_subagent_registration_script())
