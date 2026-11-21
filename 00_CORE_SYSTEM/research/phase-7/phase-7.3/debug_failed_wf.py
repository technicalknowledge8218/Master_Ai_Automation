import json

with open(r"F:\Master AI\03_AI_AGENTS\runs\workflows\WF-f33ee5ae.json", "r", encoding="utf-8") as f:
    wf = json.load(f)

print("Status:", wf.get("status"))
print("Current wave:", wf.get("current_wave_index"))
for st_id, st in wf.get("subtasks", {}).items():
    print(f"{st_id} ({st.get('assigned_agent')} - {st.get('title')}): status={st.get('status')} err={st.get('error')}")
