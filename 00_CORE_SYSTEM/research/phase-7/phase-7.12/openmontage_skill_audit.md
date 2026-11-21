# OPENMONTAGE SKILLS & PIPELINE INVESTIGATION AUDIT
**Target Output**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.12\openmontage_skill_audit.md`  
**Repository Inspected**: `OpenMontageInc/OpenMontage` (Commit `main` @ 2026-11)  
**Date**: 2026-11-18  

---

## 1. Architectural Architecture & Discovery Hierarchy

OpenMontage operates on a three-tier skill architecture that decouples agent intelligence from tool execution:

```
[Layer 1: Pipeline Manifests] (pipeline_defs/<pipeline>.yaml)
      │
      ▼
[Layer 2: Stage Director Skills] (skills/pipelines/<pipeline>/<stage>-director.md)
      │
      ▼
[Layer 3: Tool & Provider Skills] (.agents/skills/<provider>/<tool>.md)
      │
      ▼
[Python BaseTool Execution Engine] (tools/tool_registry.py -> FFmpeg / Remotion / API)
```

### The Seven Core Concepts Master AI Must Adopt

1. **Pipeline Manifests as Contracts (`pipeline_defs/`)**:
   - Rather than letting an agent guess what steps to run, a YAML manifest defines:
     - `stages`: ordered list (e.g. `research`, `scripting`, `storyboard`, `asset_generation`, `voiceover`, `music`, `composition`, `qa`).
     - `tools`: exact tools registered for each stage.
     - `quality_gates`: mandatory validation criteria before advancing to the next stage.

2. **Stage Director Skills (`skills/pipelines/...`)**:
   - For every single stage, the agent reads a dedicated markdown guide that tells it how a human film professional (e.g. Art Director, Cinematographer, Editor) thinks, decides, and formats output.

3. **Preflight Capability Discovery**:
   - Before accepting a user prompt or writing scripts, the agent queries its tool registry to build a `support_envelope()`. It determines what local tools, API keys, and model backends are actually available, avoiding unfulfillable promises.

4. **Reference-Driven Production Entry Point (`video-reference-analyst`)**:
   - Treats reference video input as a first-class workflow: downloads/inspects the video, extracts transcript, detects scenes, samples keyframes, analyzes pacing, and extracts the structural grammar before writing a single line of script.

5. **Living Storyboard & Approval Gates (`Backlot`)**:
   - Renders a multi-take contact sheet at the storyboard stage. The production pauses and requests human sign-off *before* spending compute or time rendering the full film.

6. **Layer 3 Knowledge Injection**:
   - Provider-specific prompting rules (e.g. camera lens tags, lighting modifiers, negative prompts, aspect ratio flags) are encapsulated in dedicated markdown skill files read immediately before calling the tool.

7. **Multi-Point Self-Review (Pre-Release QA)**:
   - Evaluates:
     - ffprobe stream validation (CFR, resolution, audio sample rate).
     - Visual frame sampling (checking for visual artifacts, cut-off text, or frozen holds).
     - Audio level compliance (True Peak, Integrated RMS loudness).
     - Subtitle synchronization and safe-zone adherence.

---

## 2. OpenMontage Production Pipelines Overview

| Pipeline ID | Focus / Genre | Primary Visual Engine | Audio / Music Strategy | Typical Cost |
| :--- | :--- | :--- | :--- | :--- |
| `animated-explainer` | Tech/Educational 2D/3D | Remotion + Vector / Stills | TTS Narration + Royalty-Free BGM | $0.00 – $1.50 |
| `cinematic-trailer` | Sci-Fi / Drama / Action | Veo / Kling AI Motion Clips | Epic Orchestral BGM + Sound FX | $3.00 – $8.00 |
| `documentary-montage`| History / Nature / Culture | Real Stock Footage (Pexels) | Deep Narration + Acoustic Score | $0.00 (Free Stock)|
| `talking-head` | Interviews / Commentary | Live Video / Avatar Lip-Sync| Direct Mic Audio + Subtitles | $0.00 – $2.00 |
| `product-showcase` | Commercials / Ads | Image-to-Video Pinning | Upbeat Synth Pop + Sound FX | $2.00 – $5.00 |
| `objects-in-overdrive`| 3D Kinetic Physics | Blender Eevee/Cycles + FFmpeg| Phonk / Electronic Beats | $0.00 (Local 3D) |

---

## 3. Translation to Master AI

Because of OpenMontage's AGPL-3.0 license, Master AI will not copy its code directly. Instead, Master AI implements an equivalent, independent Python architecture:
- `F:\Master AI\00_CORE_SYSTEM\orchestrator\pipeline_registry.py` (Clean-room manifest executor).
- `F:\Master AI\00_CORE_SYSTEM\skills\video-production\` (Dedicated Master AI skills for every stage).
- `F:\Master AI\00_CORE_SYSTEM\tools\` (Native tool discovery and capability envelope).
