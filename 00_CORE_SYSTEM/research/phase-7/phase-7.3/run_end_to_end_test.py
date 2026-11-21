"""
Master AI - Phase 7.3 End-to-End Autonomous Acceptance Test
Executes the target goal through the Central Multi-Agent Orchestrator:
'Create a 60-second cinematic African lion documentary in Hindi for YouTube.'
"""

import os
import sys
import json
import time

sys.path.insert(0, r"F:\Master AI")
sys.path.insert(0, r"F:\Master AI\03_AI_AGENTS")
sys.path.insert(0, r"F:\Master AI\03_AI_AGENTS\orchestrator")
from orchestration_core import MasterOrchestrationCore

def main():
    print("=" * 80)
    print("MASTER AI — PHASE 7.3 AUTONOMOUS CINEMATIC ACCEPTANCE TEST")
    print("Goal: 'Create a 60-second cinematic African lion documentary in Hindi for YouTube.'")
    print("=" * 80)

    orchestrator = MasterOrchestrationCore()

    # Step 1: Goal Submission & DAG Decomposition
    print("\n[STEP 1] Submitting Goal to Central Orchestrator...")
    goal_text = "Create a 60-second cinematic African lion documentary in Hindi for YouTube."
    plan = orchestrator.submit_goal(goal_text)

    plan_id = plan["plan_id"]
    print(f"Plan ID: {plan_id}")
    print(f"Goal Intent: {plan['analysis']['intent']}")
    print(f"Is Cinematic Production: {plan['analysis']['is_cinematic']}")
    print(f"Target Duration: {plan['analysis']['target_duration_sec']}s")
    print(f"Target Language: {plan['analysis']['target_language']}")
    print(f"Subtask Count: {plan['subtask_count']}")
    print(f"Waves Count: {len(plan['waves'])}")

    for i, wave in enumerate(plan["waves"]):
        print(f"  Wave {i+1}: {wave}")

    # Step 2: Human Approval Gate & Workflow Initialization
    print("\n[STEP 2] Approving Execution Plan & Initializing Workflow...")
    wf = orchestrator.approve_plan(plan_id)
    wf_id = wf["workflow_id"]
    print(f"Workflow ID: {wf_id}")
    print(f"Workflow Status: {wf['status']}")

    # Step 3: Central Multi-Agent Workflow Execution
    print("\n[STEP 3] Executing Workflow through Central Orchestrator...")
    t0 = time.time()
    result = orchestrator.execute_workflow(wf_id)
    t1 = time.time()

    print(f"\nExecution Finished in {t1 - t0:.2f} seconds!")
    print(f"Workflow Status: {result.get('status')}")

    # Step 4: Inspect Final Deliverable & Production Dossier
    print("\n[STEP 4] Inspecting Final Deliverables...")
    fd = result.get("final_deliverable", {})
    master_video = fd.get("master_video_path")
    artifacts = fd.get("artifacts_produced", [])
    dossier = fd.get("production_dossier", {})

    print(f"Master Video Path: {master_video}")
    print(f"Artifacts Produced ({len(artifacts)}):")
    for a in artifacts:
        print(f"  - {a}")

    print("\nProduction Dossier Highlights:")
    print(f"  Title: {dossier.get('title')}")
    print(f"  Runtime: {dossier.get('runtime_seconds')}s")
    print(f"  Resolution: {dossier.get('resolution')}")
    print(f"  FPS: {dossier.get('fps')}")
    print(f"  Commercial Clearance: {dossier.get('commercial_clearance_status')}")
    print(f"  QA Verdict: {dossier.get('quality_assurance_verdict')}")
    print(f"  Total Cost: ${dossier.get('cost_usd', 0.0):.2f}")

    # Save summary report for audit
    report_path = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.3\acceptance_test_result.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved Acceptance Test Result to: {report_path}")

if __name__ == "__main__":
    main()
