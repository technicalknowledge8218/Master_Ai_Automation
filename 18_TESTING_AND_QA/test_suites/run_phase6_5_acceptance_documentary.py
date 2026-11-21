#!/usr/bin/env python3
"""run_phase6_5_acceptance_documentary.py
MASTER-AI Phase 6.5 Final Acceptance Documentary Generation & Audit
Executes end-to-end 300.0-second Hindi wildlife documentary with:
- FireRed-OpenStoryline AI directing plan
- Wikimedia Commons & Pexels verified wildlife media acquisition
- Ground-truth .provenance.json licensing records
- Edge TTS hi-IN-MadhurNeural Hindi speech synthesis
- faster-whisper CPU INT8 speech intelligibility & ASR verification
- OpenFilm HTML5 dynamic title sequence
- Socialdrop multi-platform staged distribution (dry-run, ApprovalCenter gated)
- 14-Point strict fail-closed Media QA Audit
"""

import os
import sys
import json
import time
from pathlib import Path

WORKSPACE_ROOT = Path("F:/Master AI").resolve()
sys.path.insert(0, str(WORKSPACE_ROOT))

from importlib import import_module
cs_mod = import_module("09_CONTENT_STUDIO.engine.content_studio_orchestrator")
ContentStudioOrchestrator = getattr(cs_mod, "ContentStudioOrchestrator")


def run_acceptance_documentary():
    print("=" * 70)
    print("MASTER-AI PHASE 6.5: FINAL ACCEPTANCE DOCUMENTARY RUN")
    print("=" * 70)

    orchestrator = ContentStudioOrchestrator()
    prompt = "Create a 5-minute Hindi documentary about lions for YouTube."
    print(f"Goal: '{prompt}'")
    print("Target Duration: 300.0 seconds | Resolution: 1920x1080 | Language: Hindi")
    print("-" * 70)

    t0 = time.time()
    summary = orchestrator.produce_documentary(
        request_prompt=prompt,
        target_duration_sec=300.0,
        language="Hindi",
        resolution=(1920, 1080),
        fps=30
    )
    elapsed = round(time.time() - t0, 2)

    print("\n" + "=" * 70)
    print(f"PRODUCTION COMPLETE in {elapsed}s")
    print(f"Project ID: {summary.get('project_id')}")
    print(f"QA Status: {summary.get('qa_status')} (Passed: {summary.get('qa_passed')})")
    print(f"Actual Duration: {summary.get('actual_duration_sec')}s (Target: {summary.get('target_duration_sec')}s)")
    print(f"Video File: {summary.get('video_path')} ({summary.get('video_size_bytes'):,} bytes)")
    print(f"Thumbnail: {summary.get('thumbnail_path')}")
    print(f"Subtitles (SRT): {summary.get('subtitles_srt')}")
    print(f"Soundtrack: {summary.get('soundtrack_path')}")
    print(f"Approval Ticket: {summary.get('approval_ticket_id')}")
    print("=" * 70)

    # Inspect QA Report
    proj_dir = Path(summary.get("video_path")).parent
    qa_file = proj_dir / "qa_report.json"
    if qa_file.exists():
        with open(qa_file, "r", encoding="utf-8") as f:
            qa = json.load(f)
        print(f"\nMEDIA QA AUDIT RESULTS ({qa.get('checks_run')} CHECKS RUN):")
        for c in qa.get("checks", []):
            status = "PASS" if c.get("passed") else "FAIL"
            print(f"  [{status}] {c.get('name')}: {c.get('details')}")

    # Inspect Provenance Files
    assets_dir = proj_dir / "assets"
    prov_files = list(assets_dir.glob("*.provenance.json"))
    print(f"\nVERIFIED PROVENANCE MANIFESTS ({len(prov_files)} records):")
    for pf in prov_files:
        with open(pf, "r", encoding="utf-8") as f:
            p_data = json.load(f)
        print(f"  - {pf.name}: Source={p_data.get('source', p_data.get('source_type'))}, License={p_data.get('license')}")

    # Inspect OpenFilm Title Bundle
    openfilm_dir = proj_dir / "openfilm_titles"
    print(f"\nOPENFILM TITLE BUNDLE: {openfilm_dir} (exists: {openfilm_dir.exists()})")

    # Inspect Socialdrop Staged Manifest
    social_file = proj_dir / "socialdrop_staged_manifest.json"
    print(f"SOCIALDROP STAGED MANIFEST: {social_file} (exists: {social_file.exists()})")

    # Return summary dict
    return summary


if __name__ == "__main__":
    res = run_acceptance_documentary()
    if not res.get("qa_passed"):
        print("\nERROR: Acceptance documentary failed QA audit!")
        sys.exit(1)
    else:
        print("\nSUCCESS: Acceptance documentary passed all quality gates!")
        sys.exit(0)
