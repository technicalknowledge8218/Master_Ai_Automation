# MASTER AI — ZERO-BUDGET MASTER ARCHITECTURE (₹0 / $0)
## Complete Autonomous Cinematic Production House Under Absolute Zero-Cost Constraint

**Document Version:** 1.0.0-zero-budget  
**Project Root:** `F:\Master AI`  
**Target Path:** `00_CORE_SYSTEM\research\phase-7\zero-budget\ZERO_BUDGET_MASTER_ARCHITECTURE.md`  
**Classification:** Core System Architecture & Financial Policy  
**Status:** Approved Architectural Specification  

---

## 1. THE PERMANENT BUSINESS INVARIANT (₹0 / $0)

Master AI is engineered under a non-negotiable architectural invariant: **The total operating budget of this platform is permanently fixed at ₹0 / $0.**

This is not a default setting, an introductory mode, or an interim development phase. It is an immutable constitutional constraint:
1. **Zero Paid APIs:** No OpenAI, Anthropic, ElevenLabs, Google Cloud Vertex AI, Kling, Runway, or Midjourney paid endpoints.
2. **Zero Paid Cloud Compute:** No paid GPU instances (AWS EC2, RunPod paid, Modal paid, Lambda Labs).
3. **Zero Paid Subscriptions:** No monthly SaaS memberships, freemium unlock tiers, or token top-ups.
4. **Zero Paid Licenses:** No proprietary software licenses, commercial plugin fees, or paid asset marketplaces.
5. **Trial Elimination:** Any service that functions only as a temporary free trial, promotional credit voucher, or expires into a paywall is classified as **NOT SUITABLE** and excluded from production architecture.

If a task cannot be performed at ₹0, Master AI does not fail open or request payment details. It either routes to a verified free alternative or halts that specific operation with an honest technical limitation report.

---

## 2. MODULAR ZERO-BUDGET SUBSYSTEMS ARCHITECTURE

Master AI partitions its production pipeline into seven modular subsystems, each powered strictly by local open-source software or legitimate, permanently free services:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MASTER AI ZERO-BUDGET ARCHITECTURE (₹0)                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  ┌───────────────────────┐   ┌───────────────────────────┐   ┌──────────────────────┐  │
│  │  1. CREATIVE & RAG    │   │  2. VISUAL PRODUCTION     │   │ 3. VOICE & SOUND     │  │
│  │     ORCHESTRATION     │   │     DUAL ZERO-COST CORE   │   │    SYNTHESIS         │  │
│  ├───────────────────────┤   ├───────────────────────────┤   ├──────────────────────┤  │
│  │ • Local Ollama Engine │   │ [Tier A: 3D CGI & Motion] │   │ • Microsoft Edge TTS │  │
│  │   (Llama 3.2 3B GGUF) │   │ • Blender 4.x (bpy CPU)   │   │   (hi-IN / en-US)    │  │
│  │ • Groq Free Tier      │   │ • Lemo-Opuscar MIT Canvas │   │ • Piper TTS (Local)  │  │
│  │   (Llama 3.3 70B)     │   │ [Tier B: Real Stock]      │   │ • FreeSound CC0      │  │
│  │ • Google AI Studio    │   │ • Pexels API (Commercial) │   │ • Lemo sfx.py Foley  │  │
│  │   (Gemini 2.0 Free)   │   │ • Wikimedia CC0 Archive   │   │ • Meta MusicGen CPU  │  │
│  │ • Wikipedia/ArXiv RAG │   │ [Tier C: Free Cloud GPU]  │   │ • faster-whisper     │  │
│  │ • Scriptwriter Agent  │   │ • Kaggle (30h/wk T4 GPU)  │   │   (CPU INT8 ASR)     │  │
│  └───────────┬───────────┘   └─────────────┬─────────────┘   └──────────┬───────────┘  │
│              │                             │                            │              │
│              └─────────────────────────────┼────────────────────────────┘              │
│                                            ▼                                           │
│                              ┌───────────────────────────┐                             │
│                              │  4. EDITING & COMPOSITING │                             │
│                              │     100% LOCAL & FREE     │                             │
│                              ├───────────────────────────┤                             │
│                              │ • FFmpeg 7.1 Complex Graph│                             │
│                              │ • Lemo-Opuscar MIT Pipes  │                             │
│                              │ • Free CC0 3D LUT Presets │                             │
│                              │ • EBU R128 loudnorm (-14) │                             │
│                              │ • Styled ASS Subtitles    │                             │
│                              └─────────────┬─────────────┘                             │
│                                            ▼                                           │
│                              ┌───────────────────────────┐                             │
│                              │  5. 16-POINT MEDIA QA     │                             │
│                              │     VERIFICATION ENGINE   │                             │
│                              ├───────────────────────────┤                             │
│                              │ • Local Whisper ASR Gate  │                             │
│                              │ • True Provenance Verifier│                             │
│                              │ • Bitstream Decode Audit  │                             │
│                              │ • Reading-Speed Checker   │                             │
│                              └─────────────┬─────────────┘                             │
│                                            ▼                                           │
│                              ┌───────────────────────────┐                             │
│                              │  6. MULTI-RATIO EXPORTER  │                             │
│                              │     & PACKAGING STUDIO    │                             │
│                              ├───────────────────────────┤                             │
│                              │ • 16:9 Landscape (YouTube)│                             │
│                              │ • 9:16 Vertical (Shorts)  │                             │
│                              │ • 1:1 Square (Instagram)  │                             │
│                              │ • Local PIL Thumbnails    │                             │
│                              └─────────────┬─────────────┘                             │
│                                            ▼                                           │
│                              ┌───────────────────────────┐                             │
│                              │  7. ZERO-COST PUBLISHING  │                             │
│                              │     & APPROVAL GOVERNANCE │                             │
│                              ├───────────────────────────┤                             │
│                              │ • ApprovalCenter Tickets  │                             │
│                              │ • YouTube API (10k units) │                             │
│                              │ • Meta Graph API (Free)   │                             │
│                              │ • socialdrop Staging Gating                             │
│                              └───────────────────────────┘                             │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. COMPONENT SELECTION ACROSS THE 13 PRODUCTION DOMAINS

| # | Production Domain | Primary Zero-Cost Component | Fallback Zero-Cost Component | Licensing & Cost |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **LLM Orchestration** | Local Ollama (`llama3.2:3b` GGUF) | Groq Cloud Free Tier (`llama-3.3-70b`) | Open Weights / Free Tier |
| **2** | **Script & Research** | Europe PMC, ArXiv, Wikipedia APIs | Gemini 2.0 Flash (AI Studio Free) | Public APIs (₹0) |
| **3** | **Image Generation** | OpenVINO SD 1.5 (Local Intel Iris Xe) | Pollinations.ai / HF Free Spaces | Apache 2.0 / Free API (₹0) |
| **4** | **AI Video Gen** | Kaggle Remote T4 (Wan 2.1 1.3B) | Pexels Verified HD Wildlife Video | Apache 2.0 / Pexels License |
| **5** | **Image-to-Video** | Kaggle Remote T4 (Wan 2.1 I2V) | Local 3D Blender camera animation | Open Source (₹0) |
| **6** | **3D CGI Animation** | Blender 4.x Headless (`bpy` CPU Cycles) | Blender EEVEE Next (Direct3D 11) | GNU GPL v3 (₹0) |
| **7** | **Character Consistency** | Rigged 3D Meshes (glTF / Poly Haven) | InsightFace CPU face re-projection | CC0 / MIT (₹0) |
| **8** | **Voice Narration** | Microsoft Edge TTS (`hi-IN-MadhurNeural`)| Piper TTS (Local CPU C++ ONNX) | Free WebSocket / MIT |
| **9** | **Music & SFX** | Lemo-Opuscar `sfx.py` + CC0 Orchestral | Meta MusicGen-small (Local CPU) | MIT / Free CC0 (₹0) |
| **10**| **Video Editing** | FFmpeg 7.1 Complex Filtergraph | Lemo-Opuscar MIT frame-piper | LGPL / MIT (₹0) |
| **11**| **ASR & Subtitles** | `faster-whisper` (CPU INT8) | SubtitleEngine (.ASS / .SRT) | MIT (Local ₹0) |
| **12**| **Thumbnail Studio** | PIL + Google Fonts (Noto / Montserrat) | Lemo-Opuscar `still.mjs` | OFL / Apache 2.0 (₹0) |
| **13**| **Social Publishing** | YouTube Data API v3 (10k units/day) | Meta Graph API (50 posts/day) | Official Free Tiers (₹0) |

---

## 4. ADAPTER-FIRST DESIGN & SOVEREIGN ORCHESTRATION

To ensure that the platform never becomes dependent on any single free provider, Master AI enforces the **Universal Adapter Contract**:

1. **Central Orchestrator Supremacy:** The central Python orchestrator (`content_studio_orchestrator.py`) retains absolute authority over pipeline logic, task state, error handling, and artifact registries.
2. **Hot-Swappable Providers:** All external models and free services implement standardized abstract base classes:
   - `BaseLLMAdapter`
   - `BaseVideoAdapter`
   - `BaseVoiceAdapter`
   - `BaseCGIAdapter`
   - `BasePublishingAdapter`
3. **Automated Zero-Cost Failover:**
   If a free cloud provider (such as Groq or Kaggle) encounters rate limits or temporary downtime, the adapter instantly catches the exception and routes to the local offline fallback (e.g. from Groq to local Ollama; from cloud video to genuine CC0 stock) in under 5 seconds.
4. **Hard Coded Zero-Spend Guardrail:**
   Every adapter contains a pre-execution verification check:
   ```python
   if getattr(config, "spend_usd", 0.0) > 0.0:
       raise PermissionError("Zero-Budget Violation: Master AI prohibits any operation with spend > $0.00.")
   ```
