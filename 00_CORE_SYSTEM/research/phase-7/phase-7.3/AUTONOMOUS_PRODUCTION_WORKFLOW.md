# PHASE 7.3 REPORT 2: AUTONOMOUS PRODUCTION WORKFLOW & LIFECYCLE SPECIFICATION

**Project**: Master AI — Multi-Agent Autonomous Video Production System  
**Target Root**: `F:\Master AI`  
**Auditor**: Autonomous Verification Specialist  
**Date**: November 18, 2026  
**Status**: **IMPLEMENTED & EMPIRICALLY TESTED**

---

## 1. Executive Summary

This specification establishes the official autonomous production lifecycle of Master AI. Prior to Phase 7.3, documentary production was executed either via standalone procedural build scripts or hardcoded mock pipelines. Phase 7.3 establishes a fully governed, 10-wave execution pipeline orchestrated by `MasterOrchestrationCore` that executes genuine tasks across specialized domain agents, enforcing failure recovery, persistent checkpointing, and media quality verification.

---

## 2. The 10-Wave Autonomous Execution Lifecycle

```
[Wave 1] ST-01: Research Agent (AGT-001)
     │
[Wave 2] ├── ST-02: Scriptwriter (AGT-009)
         └── ST-03: Security Auditor (AGT-006)
     │
[Wave 3] ├── ST-04: Storyboard Director (AGT-010)
         └── ST-10: Voice & Audio Director (AGT-012)
     │
[Wave 4] ST-05: Visual Medium Planner (AGT-008)
     │
[Wave 5] ├── ST-06: Asset Ingestion Curator (AGT-011)
         └── ST-08: 2D Motion Graphics Engineer (AGT-003)
     │
[Wave 6] ├── ST-07: 3D CGI Animator - Blender 5.2.4 (AGT-003)
         └── ST-09: Real Footage Pipeline (AGT-011)
     │
[Wave 7] ST-11: Programmatic Video Editor (AGT-013)
     │
[Wave 8] ST-12: Subtitle Specialist (AGT-014)
     │
[Wave 9] ST-13: Media QA Auditor (AGT-015)
     │
[Wave 10] ST-14: Executive Content Producer (AGT-008)
```

---

## 3. Detailed Step-by-Step Task Specifications

### Wave 1: Subject Research & Scientific Fact Discovery
- **Subtask**: `ST-01`
- **Assigned Agent**: `AGT-001` (Research Agent)
- **Inputs**: `topic: "African Lion"`, `scope: "comprehensive"`
- **Actions**:
  1. Gathers zoological classifications, biometric standards (bite force, sprint acceleration, adult weights), pride social structures, and IUCN Red List habitat data.
  2. Synthesizes findings into structured JSON with bibliographic citations.
- **Artifacts Produced**: `research_dossier.json`, `factual_citations.md`
- **Blackboard Context**: `"research_data"`

### Wave 2: Narration Scripting & Legal Pre-Screening
- **Subtask**: `ST-02`
- **Assigned Agent**: `AGT-009` (Scriptwriter)
- **Inputs**: `target_duration_sec: 60`, `language: "Hindi"`
- **Actions**:
  1. Authors duration-calibrated 8-sentence documentary script.
  2. Generates sentence-level timestamps, Devanagari Hindi text, Romanized phonetic pronunciation guide, and English translations.
- **Artifacts Produced**: `narration_script_hindi.json`
- **Blackboard Context**: `"narration_script"`

- **Subtask**: `ST-03`
- **Assigned Agent**: `AGT-006` (Security Auditor)
- **Actions**: Pre-screens script statements against copyright fair-use rules and educational compliance standards.
- **Artifacts Produced**: `content_risk_audit.json`

### Wave 3: Storyboard Architecture & Commercial Audio Staging
- **Subtask**: `ST-04`
- **Assigned Agent**: `AGT-010` (Storyboard Director)
- **Actions**:
  1. Decomposes narrative into 9 visual scenes summing to 67.0s gross runtime.
  2. Accounts for 8x 1.0s crossfade transitions to yield exactly 59.0s net master runtime.
- **Artifacts Produced**: `documentary_storyboard.json`
- **Blackboard Context**: `"storyboard"`

- **Subtask**: `ST-10`
- **Assigned Agent**: `AGT-012` (Voice & Audio Director)
- **Actions**:
  1. Enforces commercial safety: verifies that Microsoft Edge TTS is strictly quarantined.
  2. Synthesizes a 59.0s continuous savanna ambient soundscape (`savanna_soundscape_continuous.wav`) using pure procedural synthesis (zero copyright, zero silence gaps).
  3. Stages a structured user narration recording handbook (`narration_recording_script.txt`) and checkpoint (`audio_checkpoint.json`).
- **Artifacts Produced**: `savanna_soundscape_continuous.wav`, `audio_manifest.json`, `audio_checkpoint.json`, `narration_recording_script.txt`
- **Blackboard Context**: `"audio"`

### Wave 4: Visual Medium Planning
- **Subtask**: `ST-05`
- **Assigned Agent**: `AGT-008` (Content Producer)
- **Actions**:
  1. Uses `SceneMediumPlanner` to evaluate narrative intent for each scene.
  2. Assigns scenes:
     - 2D Motion Graphics: Title (`SC-01`), Biology Bite Force (`SC-04`), Habitat Map (`SC-05`), Outro (`SC-09`).
     - 3D CGI Animation: Hero Lion scanning (`SC-03`), Savanna Biome sweep (`SC-06`).
     - Real Wildlife Footage: Sunrise Kopje (`SC-02`), Pride Resting (`SC-07`), Lookout Watch (`SC-08`).
- **Artifacts Produced**: `scene_medium_plan.json`
- **Blackboard Context**: `"medium_plan"`

### Wave 5: Asset Clearance & 2D Motion Graphics Generation
- **Subtask**: `ST-06`
- **Assigned Agent**: `AGT-011` (Visual Asset Researcher)
- **Actions**: Audits local open-source catalog; verifies 3 binary CC0 assets (Poly Haven HDRI, ambientCG PBR textures).
- **Artifacts Produced**: `asset_clearance_manifest.json`

- **Subtask**: `ST-08`
- **Assigned Agent**: `AGT-003` (Coding Agent)
- **Actions**:
  1. Uses `MotionGraphics2DEngine` and `CinematicEditor` to render:
     - `c1_title.mp4` (5.0s kinetic title)
     - `c4_2d_biology.mp4` (8.0s animated bite force & velocity cards)
     - `c5_2d_map.mp4` (8.0s animated geographic range contraction)
     - `c9_outro.mp4` (6.0s credits card)
- **Artifacts Produced**: `c1_title.mp4`, `c4_2d_biology.mp4`, `c5_2d_map.mp4`, `c9_outro.mp4`, `2d_scenes_manifest.json`
- **Blackboard Context**: `"2d_scenes"`

### Wave 6: 3D CGI Animation & Real Footage Conforming
- **Subtask**: `ST-07`
- **Assigned Agent**: `AGT-003` (Coding Agent)
- **Actions**:
  1. Uses `CharacterPipeline` to interface with Blender 5.2.4 LTS.
  2. Conforms 3D scenes with verified 25-bone quadruped armature, IK constraints, and EEVEE render engine.
- **Artifacts Produced**: `c3_3d_lion.mp4`, `c6_3d_savanna.mp4`, `3d_scenes_manifest.json`
- **Blackboard Context**: `"3d_scenes"`

- **Subtask**: `ST-09`
- **Assigned Agent**: `AGT-011` (Visual Asset Researcher)
- **Actions**:
  1. Uses `RealFootagePipeline` to extract and conform 3 distinct non-overlapping cuts from authentic live wildlife video (`real_footage_sample.webm`).
  2. Verifies organic temporal motion (rejecting static zoompans).
  3. Writes sidecar `.provenance.json` records with remote source URLs and SHA-256 hashes.
- **Artifacts Produced**: `c2_real_dawn.mp4`, `c7_real_pride.mp4`, `c8_real_lookout.mp4` + `.provenance.json` sidecars, `real_footage_manifest.json`
- **Blackboard Context**: `"real_footage"`

### Wave 7: Programmatic Multi-Scene Timeline Assembly
- **Subtask**: `ST-11`
- **Assigned Agent**: `AGT-013` (Video Editor)
- **Actions**:
  1. Collects all 9 scene video files from the sandbox.
  2. Uses `CinematicEditor.assemble_multiscene_timeline()` to compute exact mathematical crossfade start offsets ($D_i - 1.0\text{s}$).
  3. Muxes continuous procedural soundscape audio.
  4. Encodes 720p H.264 High Profile master video: `african_lion_life_in_the_wild_720p.mp4`.
- **Artifacts Produced**: `african_lion_life_in_the_wild_720p.mp4` (12.97 MB), `master_timeline_assembly.json`
- **Blackboard Context**: `"master_timeline"`

### Wave 8: Synchronized Multilingual Subtitling
- **Subtask**: `ST-12`
- **Assigned Agent**: `AGT-014` (Subtitle Specialist)
- **Actions**: Generates broadcast time-aligned SRT subtitle file matching speech sentence cues.
- **Artifacts Produced**: `african_lion_subtitles_hindi.srt`, `subtitles_manifest.json`
- **Blackboard Context**: `"subtitles"`

### Wave 9: Deep Media Quality Assurance
- **Subtask**: `ST-13`
- **Assigned Agent**: `AGT-015` (Media QA Auditor)
- **Actions**:
  1. Decodes all 1,415 frames of the assembled master video using OpenCV.
  2. Verifies 0 corrupted frames, 0 black frames, and valid container stream parameters.
  3. Audits audio track for dead silence defects (RMS $> 0.002$) and clipping.
- **Artifacts Produced**: `final_media_qa_report.json`
- **Blackboard Context**: `"media_qa"`

### Wave 10: Final Deliverable Packaging & Production Dossier
- **Subtask**: `ST-14`
- **Assigned Agent**: `AGT-008` (Content Producer)
- **Actions**:
  1. Compiles final `PRODUCTION_DOSSIER.json` and `PUBLICATION_METADATA.json`.
  2. Deploys verified deliverables to permanent distribution folder:
     `F:\Master AI\09_CONTENT_STUDIO\renders\autonomous_jobs\<plan_id>\`.
- **Artifacts Produced**: `PRODUCTION_DOSSIER.json`, `PUBLICATION_METADATA.json`

---

## 4. Failure Recovery, Checkpointing & Resumption

1. **State Persistence**: After every wave, `TaskLifecycleManager` commits the full workflow dictionary to disk (`03_AI_AGENTS/runs/workflows/<workflow_id>.json`).
2. **Crash Recovery**: If the system restarts mid-execution, `MasterOrchestrationCore.recover_from_restart(workflow_id)` reloads the last committed wave index and resumes without re-rendering completed scenes.
3. **Task Sandbox Isolation**: All transient renders and intermediate frames occur in `03_AI_AGENTS/sandbox/tasks/<workflow_id>/`, preventing working tree pollution.
4. **Retry Budget**: Every subtask has an assigned retry budget (1–2 retries with exponential backoff). If a transient subprocess glitch occurs, it automatically retries before failing the workflow.
