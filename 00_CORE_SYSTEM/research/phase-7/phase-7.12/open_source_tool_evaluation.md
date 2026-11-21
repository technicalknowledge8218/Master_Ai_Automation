# COMPREHENSIVE OPEN-SOURCE REPOSITORY & TOOL EVALUATION
**Target Output**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.12\open_source_tool_evaluation.md`  
**Date**: 2026-11-18  
**Scope**: Rigorous code and documentation audit of five candidate repositories for Master AI autonomous production.

---

## 1. Evaluation Matrix

| Criteria | A. OpenMontage | B. OpenDirector | C. ComfyUI | D. OpenBone | E. OpenToonz |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Repository** | `OpenMontageInc/OpenMontage` | `seme-org/open-director` | `Comfy-Org/ComfyUI` | `UXCentury/open-bone` | `opentoonz/opentoonz` |
| **Community / Stars** | 81,471 ⭐ | 133 ⭐ | 147,462 ⭐ | 5 ⭐ (Emerging) | 8,286 ⭐ |
| **License** | **AGPL-3.0** | **LGPL-3.0** | **GPL-3.0** | **MIT (Permissive)** | **Modified BSD** |
| **Primary Language** | Python + TypeScript | TypeScript / React | Python | C++ / TypeScript / Rust | C++ / Qt |
| **Active Maintenance** | High (Daily commits) | Moderate | Very High | Active (Pre-1.0) | Stable / Slow |
| **Windows Support** | Yes (Python + Node.js) | Yes (via Docker/Node) | Yes (Standalone & pip)| Yes (Multi-platform) | Yes (Windows native) |
| **Hardware Reqs** | Low (CPU for pipelines) | Low (Web UI client) | High (NVIDIA GPU 12GB+)| Low (CPU/WebGL/Native)| Low/Moderate |
| **Agent / CLI Support** | Native Agentic Design | Web UI focused | REST & WebSocket API | Native Agent MCP Server| GUI Desktop Only |
| **Commercial Use** | Strong copyleft risk | Moderate copyleft risk| GPL viral risk | Commercial Friendly | Commercial Friendly |
| **Verdict for Master AI**| **Adopt Architecture & Concepts (Clean-Room)** | **Reject (GUI dependent)** | **API adapter only (No local models)** | **Primary Candidate for 2D Rigging** | **Reject (Headless incompatible)** |

---

## 2. In-Depth Project Breakdowns

### A. OpenMontage (`OpenMontageInc/OpenMontage`)
- **Core Functionality**: The first agentic video production system designed to turn coding assistants (Claude Code, Cursor, Copilot, Antigravity) into a full studio. It features 12 production pipelines, 100+ tools, and 700+ agent skill markdown files.
- **Architecture**:
  - Python manages tools, CLI, and project state.
  - Remotion (Node.js/React) serves as the programmatic composition timeline.
  - The AI Agent acts as Executive Director, reading YAML pipeline manifests and markdown stage director skills.
- **Strengths**: Built specifically for autonomous agents; treats production as a sequence of stage-gated decisions; includes preflight discovery and reference video analysis.
- **Weaknesses**: Relies on external paid APIs (Kling, Veo, Fal.ai, Suno) for high-end video/music generation unless using stock footage pipelines.
- **License Constraint**: **AGPL-3.0**. Copying its source code directly into Master AI would impose AGPL network copyleft obligations. Therefore, Master AI must implement clean-room skills and native Python adapters modeled after its best design patterns.

---

### B. OpenDirector (`seme-org/open-director`)
- **Core Functionality**: Web-based visual storyboard editor and directing interface designed to orchestrate generative video prompts.
- **Architecture**: Next.js, Node.js frontend, Docker-compose setup.
- **Assessment**: OpenDirector is built primarily for human creative directors sitting in front of a browser clicking timeline blocks. It does not provide headless CLI agent integration or autonomous pipeline execution.
- **Verdict**: Not suitable for Master AI autonomous agent execution.

---

### C. ComfyUI (`Comfy-Org/ComfyUI`)
- **Core Functionality**: Node-based visual graph execution engine for Stable Diffusion, FLUX, Wan 2.1, LTX-Video, and other generative models.
- **Architecture**: Python backend exposing REST endpoints and WebSocket channels for queueing prompt graphs.
- **Assessment**:
  - ComfyUI is the global benchmark for generative AI image and video pipelines.
  - However, local execution on this workstation is constrained: the system has Intel Iris Xe Graphics (no NVIDIA GPU, no CUDA) and only 10.86 GB free on `C:\`. Video diffusion models require 15–30 GB disk space and 12–24 GB VRAM.
- **Verdict**: Retain ComfyUI as an optional remote/API adapter for users with dedicated GPU rigs, but do not rely on local ComfyUI video inference on the current host.

---

### D. OpenBone (`UXCentury/open-bone`)
- **Core Functionality**: Open-source 2D skeletal animation engine designed to rig characters like Spine and make them interactive like Rive.
- **Key Breakthrough**: Includes a native **MCP server** specifically designed so AI agents can rig characters, adjust bone hierarchies, generate lip-sync from audio waveforms, and trigger skeletal animations programmatically!
- **License**: **MIT License** (fully permissive, commercial-friendly).
- **Runtimes**: C++, WebGL/Canvas, Flutter, C#, Java, Swift.
- **Assessment**: OpenBone directly solves Master AI's Phase 7.11 character animation weakness. Instead of primitive sinusoidal SVG coordinates, characters can be defined with bone hierarchies, skin textures, mesh weights, and automated lip-sync visemes.
- **Verdict**: **Adopt as Master AI's primary 2D character rigging and animation standard.**

---

### E. OpenToonz (`opentoonz/opentoonz`)
- **Core Functionality**: Professional traditional 2D animation suite originally developed by Digital Video S.p.A. and customized by Studio Ghibli.
- **Architecture**: Heavy C++ desktop GUI application using Qt5/Qt6.
- **Assessment**: OpenToonz is designed for human animators using drawing tablets and desktop UI. It has very limited headless scripting capability, lacks a CLI automation pipeline, and cannot be driven smoothly by an autonomous agent via JSON/REST/MCP.
- **Verdict**: Reject for autonomous agent production.
