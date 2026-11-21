import sys
sys.path.insert(0, 'F:/Master AI/03_AI_AGENTS/orchestrator')
from agent_registry import AgentRegistry

reg = AgentRegistry()
for ag_id in ['AGT-001', 'AGT-003', 'AGT-006', 'AGT-008', 'AGT-009', 'AGT-010', 'AGT-011', 'AGT-012', 'AGT-013', 'AGT-014', 'AGT-015']:
    ag = reg.get_agent(ag_id)
    if ag:
        print(f"{ag_id} ({ag['name']}): permitted_tools={ag.get('permitted_tools', [])}")
