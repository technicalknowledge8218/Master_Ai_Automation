import sys
sys.path.insert(0, 'F:/Master AI/03_AI_AGENTS/orchestrator')
from agent_registry import AgentRegistry

reg = AgentRegistry()
agents = reg.list_agents()
for ag in sorted(agents, key=lambda x: x.get('id', '')):
    print(f"{ag.get('id')}: {ag.get('name')} | role={ag.get('role')} | tier={ag.get('permission_tier')}")

