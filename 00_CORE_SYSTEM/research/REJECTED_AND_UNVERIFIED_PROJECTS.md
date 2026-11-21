# MASTER AI — REJECTED, RESTRICTED & UNVERIFIED PROJECTS AUDIT

> **Research Phase**: Phase 6.4 Autonomous GitHub Ecosystem Discovery & Research  
> **Evaluation Date**: 2026-11-17  
> **Objective**: Transparent documentation of disqualified tools, legal risks, and technical dead ends  

---

## 1. Executive Summary

A critical principle of Master AI architecture is: **Knowing what NOT to build or integrate is just as important as selecting top tools.**
During Phase 6.4, dozens of widely discussed open-source repositories and models were investigated and rejected due to license restrictions, abandonment, security vulnerabilities, or severe architectural incompatibilities with Master AI's Windows 11 Enterprise (Intel Iris Xe CPU) host.

---

## 2. Table of Disqualified & Restricted Candidates

| Project Name | Repository URL | Primary Disqualification Reason | Risk Category | Final Verdict |
| :--- | :--- | :--- | :--- | :---: |
| **ShortGPT** | `RayVentura/ShortGPT` | Abandoned maintenance; tightly coupled to legacy moviepy 1.0; brittle prompts. | Technical Obsolescence | **REJECTED** |
| **Stable Diffusion WebUI** | `AUTOMATIC1111/stable-diffusion-webui` | Monolithic GUI; heavy AGPL-3.0 copyleft risk; poor programmatic agent API. | License & Architecture | **REJECTED** |
| **Remotion** | `remotion-dev/remotion` | Proprietary commercial license required for organizations $>3$ employees. | Commercial Licensing | **REJECTED** (Prefer openfilm) |
| **Coqui TTS** | `coqui-ai/TTS` | Company dissolved; repository unmaintained; fragile C++ build on Windows. | Abandonment | **REJECTED** |
| **Wav2Lip** | `Rudrabha/Wav2Lip` | Restrictive custom research-only license; incompatible with commercial media. | Legal & Licensing | **REJECTED** |
| **Meta AudioCraft (MusicGen)**| `facebookresearch/audiocraft` | Pretrained weights licensed under CC-BY-NC 4.0; commercial use prohibited. | Legal & Licensing | **RESTRICTED** |
| **Stable Video Diffusion** | `Stability-AI/generative-models` | Superseded by Wan2.1/LTX; high VRAM footprint; complex commercial gating. | Technical & License | **REJECTED** |
| **Instagram Private API** | `ping/instagram_private_api` | Reverse-engineered private API; high risk of immediate account bans. | Security & Terms of Service | **REJECTED** |
| **TikTok Unofficial Uploader** | `wkaisertexas/tiktok-uploader` | Headless browser uploader vulnerable to bot detection and account suspension. | Operational Fragility | **REJECTED** |
| **ChatDev** | `OpenBMB/ChatDev` | Heavy simulation overhead; token-wasteful roleplay; poor deterministic output. | Architectural Waste | **REJECTED** |

---

## 3. In-Depth Rejection Rationale

### 3.1 RayVentura/ShortGPT
- **Why Rejected**: ShortGPT gained early popularity in 2023 for automated short video generation. However, inspecting the repository reveals no significant maintenance in recent months, hardcoded dependencies on deprecated `moviepy 1.0`, and unmaintained Gradio interfaces. Master AI's existing modular FFmpeg pipeline is faster, cleaner, and fully maintained.
- **Alternative Adopted**: `openfilm` + Master AI Native `VideoEditingEngine`.

### 3.2 AUTOMATIC1111/stable-diffusion-webui
- **Why Rejected**: While popular among hobbyists, the codebase is a monolithic 145k-star script with hundreds of community extensions that execute unvetted Python code. It is licensed under AGPL-3.0, posing a severe copyleft risk if imported or bundled. Furthermore, its API mode is secondary to its browser UI.
- **Alternative Adopted**: `comfyanonymous/ComfyUI` (isolated via REST API) for node-based graph diffusion workflows.

### 3.3 remotion-dev/remotion
- **Why Rejected**: Remotion is technically impressive for React-based video generation. However, its license is **not standard open-source**: while free for individuals and companies with $\le 3$ employees, larger organizations or enterprise commercial use requires purchasing a recurring commercial license. Adopting Remotion creates an external licensing bottleneck for Master AI commercial publishing.
- **Alternative Adopted**: `openfilm/openfilm` (100% permissive MIT license, zero commercial restrictions, uses standard HTML/CSS/Canvas/WebGL).

### 3.4 facebookresearch/audiocraft (MusicGen)
- **Why Restricted**: MusicGen produces impressive orchestral and cinematic background music. However, while Meta released the code under MIT, the **pretrained model weights are licensed under CC-BY-NC 4.0 (Non-Commercial)**. Publishing a documentary video with MusicGen audio to a monetized YouTube channel or commercial client violates this license.
- **Alternative Adopted**: Procedural FFmpeg audio synthesis (`anoisesrc`, `lowpass`, `flanger`) and verified CC-0 public domain music archives (e.g. FreeMusicArchive / Musopen).

### 3.5 Reverse-Engineered Social Media Uploaders
- **Why Rejected**: Several community projects (such as `instagram_private_api` or unofficial TikTok uploaders) simulate mobile app requests or use brittle Playwright script hacks. Meta and ByteDance actively detect and permanently ban accounts utilizing unofficial API endpoints.
- **Alternative Adopted**: Official platform APIs via `socialdrop` and `postiz-app` using registered developer OAuth applications with user consent.
