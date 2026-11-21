# MASTER AI — LICENSE, INTELLECTUAL PROPERTY & SECURITY AUDIT

> **Research Phase**: Phase 6.4 Autonomous GitHub Ecosystem Discovery & Research  
> **Evaluation Date**: 2026-11-17  
> **Scope**: Commercial Viability, Licensing Compliance, and Security Boundaries for Master AI  

---

## 1. Executive Summary

This audit establishes strict legal, licensing, and security boundaries before any candidate repository or open-source model is integrated into Master AI.
A core tenet of Master AI is: **Open-source code does not automatically guarantee unrestricted commercial use.** Models, datasets, weights, and libraries each carry distinct legal terms that must be segregated architecturally to protect the core system.

---

## 2. Open-Source Software Licensing Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SOFTWARE LICENSING TIERS                           │
├────────────────────┬──────────────────────────────────┬─────────────────────┤
│ TIER 1: PERMISSIVE │ TIER 2: WEAK COPYLEFT / NOTICE   │ TIER 3: STRONG /    │
│ (Direct In-Process)│ (Subprocess / Dynamic Link)      │ NETWORK COPYLEFT    │
├────────────────────┼──────────────────────────────────┼─────────────────────┤
│ • MIT              │ • LGPL-2.1 / LGPL-3.0            │ • GPL-3.0           │
│ • Apache-2.0       │ • MPL-2.0 (Mozilla)              │ • AGPL-3.0          │
│ • BSD-2 / BSD-3    │ • EPL-2.0 (Eclipse)              │                     │
│ • Unlicense / CC0  │                                  │                     │
│                    │                                  │                     │
│ Action: Direct import│ Action: Isolated subpackage or │ Action: Out-of-     │
│ allowed in core.   │ dynamic library link.            │ process service only│
└────────────────────┴──────────────────────────────────┴─────────────────────┘
```

### 2.1 Permissive Licenses (Tier 1: Approved for Direct In-Process Python Import)
Repositories licensed under **MIT**, **Apache-2.0**, **BSD-2-Clause**, **BSD-3-Clause**, **ISC**, and **The Unlicense** can be directly imported into Master AI's Python virtual environment (`.venv`) and linked without legal friction:
- **faster-whisper** (MIT)
- **pyWikiCommons** (MIT)
- **pexels-api-python** (MIT)
- **yt-dlp** (The Unlicense)
- **sherpa-onnx** (Apache-2.0)
- **whisperX** (BSD-2-Clause)
- **PySceneDetect** (BSD-3-Clause)
- **openfilm** (MIT)
- **FireRed-OpenStoryline** (Apache-2.0)
- **langgraph** (MIT)
- **browser-use** (MIT)
- **Indic-TTS / IndicConformer** (MIT)

### 2.2 Strong Copyleft & Network Copyleft (Tier 3: Mandatory Process Isolation)
Strong copyleft licenses require any derivative work or statically combined software to be distributed under the same license.
- **AGPL-3.0 (Affero General Public License)**:
  - Examples: `gitroomhq/postiz-app`, `AUTOMATIC1111/stable-diffusion-webui`.
  - **Risk**: AGPL-3.0 extends copyleft obligations across network interactions if modified directly in the source tree.
  - **Architectural Isolation Mandate**: Master AI **MUST NOT** import or vendor AGPL code. AGPL tools must run as completely separate, independent processes (e.g. in a standalone Docker container) interacting with Master AI strictly over standardized HTTP REST APIs or Model Context Protocol (MCP) tool interfaces.
- **GPL-3.0 (General Public License)**:
  - Examples: `jianchang512/pyvideotrans`, `rany2/edge-tts`, `comfyanonymous/ComfyUI`, `WyattBlue/auto-editor`.
  - **Risk**: Direct in-memory linking could legally obligate Master AI to release proprietary extensions under GPL-3.0.
  - **Architectural Isolation Mandate**: Must be invoked via subprocess CLI commands (e.g. `subprocess.run(["auto-editor", ...])`) or via standalone WebSocket/HTTP API daemons (e.g. ComfyUI API).

---

## 3. Code License vs. Model Weights License Discrepancy

A critical vulnerability in modern AI projects is assuming that because a GitHub repository is MIT or Apache-2.0, its model weights are also free for commercial use. The following distinctions are enforced:

| Model / Framework | GitHub Code License | Pretrained Weights License | Commercial YouTube Use Permitted? |
| :--- | :---: | :---: | :---: |
| **Meta AudioCraft (MusicGen)** | MIT | **CC-BY-NC 4.0** (Non-Commercial) | ❌ **PROHIBITED** without custom license |
| **Stability AI SDXL-Turbo** | MIT | **Stability Research License** | ❌ **PROHIBITED** (Research only) |
| **Stability AI Stable Audio Open** | MIT | **CC-BY-NC-SA 4.0** | ❌ **PROHIBITED** for commercial monetization |
| **Coqui XTTS v2** | MPL-2.0 | **Coqui Public Model License** | ⚠️ Non-commercial clause applies |
| **Alibaba Wan2.1 (1.3B & 14B)** | Apache-2.0 | **Apache-2.0** | ✅ **PERMITTED** |
| **Lightricks LTX-Video** | Apache-2.0 | **Apache-2.0** | ✅ **PERMITTED** |
| **Black Forest Labs FLUX.1-schnell** | Apache-2.0 | **Apache-2.0** | ✅ **PERMITTED** (schnell variant only) |
| **Black Forest Labs FLUX.1-dev** | Apache-2.0 | **FLUX.1-dev Non-Commercial** | ❌ **PROHIBITED** for commercial monetization |
| **THUDM CogVideoX-2B / 5B** | Apache-2.0 | **Apache-2.0** | ✅ **PERMITTED** |
| **AI4Bharat Indic-TTS & IndicConformer**| MIT | **MIT** | ✅ **PERMITTED** |
| **SYSTRAN faster-whisper** | MIT | **MIT** (OpenAI Whisper weights) | ✅ **PERMITTED** |

> [!WARNING]
> **Enforcement Rule**: Master AI's `MediaQualityAssuranceAuditor` and `ProductionPackager` must audit the exact weight checkpoint used. Generating background music with AudioCraft/MusicGen and publishing it to a monetized YouTube channel violates CC-BY-NC 4.0. Master AI must utilize procedural synthesis, CC-0 archives (FreeMusicArchive), or genuinely permissive commercial models.

---

## 4. Stock Media & Footage Licensing Governance

| Media Provider | License Type | Commercial Rights | Attribution Requirements |
| :--- | :--- | :--- | :--- |
| **Wikimedia Commons (CC-0)** | Creative Commons Zero 1.0 Universal | Unrestricted | None legally required (best practice to credit) |
| **Wikimedia Commons (Public Domain)**| Expired Copyright / US Gov Work | Unrestricted | None legally required |
| **Wikimedia Commons (CC-BY 4.0)** | Creative Commons Attribution 4.0 | Allowed | **Mandatory on-screen or description credit** |
| **Wikimedia Commons (CC-BY-SA 4.0)**| ShareAlike 4.0 | Restricted | **Copyleft**: Derivative video must also be CC-BY-SA! |
| **Pexels** | Pexels License | Allowed on YouTube & Social | No attribution required (giving credit is encouraged) |
| **Pixabay** | Pixabay Content License | Allowed | No attribution required |
| **Internet Archive (Pre-1929)** | Public Domain | Unrestricted | None |

> [!IMPORTANT]
> **Audit Rule**: Phase 6.3 revealed that code-generated graphics were falsely labeled as Wikimedia Commons CC-0. Any media asset ingested must record:
> 1. Exact source download URL.
> 2. Specific license identifier (e.g. `CC0-1.0`, `Pexels-License`, `CC-BY-4.0`).
> 3. Author name and source page link.
> 4. Automated verification ensuring no `CC-BY-SA` or `CC-BY-NC` footage enters a commercial documentary bundle.

---

## 5. Security & Isolation Controls

### 5.1 Credential & Secret Hygiene
- **Social Media OAuth Tokens**: Tokens for YouTube, TikTok, X, and Instagram must be stored in encrypted local files or Windows Credential Manager. Plaintext storage in Git or logs is strictly prohibited.
- **API Keys**: All external API keys (Pexels, Hugging Face, fal.ai, Replicate) reside strictly in `.env.local` which is ignored in `.gitignore`.
- **ApprovalCenter Enforcement**: Zero network API calls that incur billing or upload public content may execute without a signed approval ticket containing a valid cryptographic `auth_token`.

### 5.2 Arbitrary Code Execution & Deserialization Defense
- **ComfyUI Custom Nodes**: Community custom nodes for ComfyUI execute arbitrary Python code. If ComfyUI is integrated, it must run inside an isolated Docker container with network restrictions.
- **Model Checkpoints**: No `.ckpt` or `.bin` files using Python's `pickle` module may be loaded directly. All models must be loaded strictly as `.safetensors` or `.onnx` to eliminate remote code execution vulnerabilities.
- **Browser Automation Sandboxing**: `browser-use` must be constrained with allowed domain whitelists and run in headless non-privileged browser profiles to prevent CSRF, cookie harvesting, or unintended navigation.
