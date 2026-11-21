# LEMO-OPUSCAR LICENSE AND SECURITY AUDIT
## Multi-Tier Licensing Analysis & Security Review for Master AI Integration

**Audit Date:** 2026-11-17  
**Repository Audited:** `https://github.com/lemomo-ai/lemo-opuscar`  
**Cloned Location:** `F:\Master AI\00_CORE_SYSTEM\research\external_repos\lemo-opuscar`  
**License Files Inspected:** `LICENSE`, `REUSE.toml`, `LICENSES/MIT.txt`, `LICENSES/CC-BY-NC-4.0.txt`, `LICENSES/CC-BY-4.0.txt`  
**Auditor:** Master AI Legal & Security Compliance Engine  

---

## 1. EXECUTIVE SUMMARY & COMPLIANCE FINDINGS

Lemo-Opuscar does **not** possess a single uniform open-source license. Instead, it utilizes a sophisticated multi-tier licensing structure governed by `LICENSE` and codified machine-readably in `REUSE.toml`.

### Compliance Matrix

| Artifact Category | License | Commercial Film Production | Redistribution Inside Master AI Product |
| :--- | :--- | :--- | :--- |
| **Rendering Code (`core/`, `tools/`, `plugin/`)** | **MIT License** | **PERMITTED** (Royalty-free) | **PERMITTED** (Must include MIT copyright notice) |
| **Documentation & Guides (`*.md`)** | **CC BY-NC 4.0** | **PERMITTED** (Under grant exception) | **PROHIBITED** without commercial license |
| **Image Generation Prompts** | **CC BY-NC 4.0** | **PERMITTED** (Under grant exception) | **PROHIBITED** without commercial license |
| **Demo Posters & Stills (`styles/*/poster.jpg`)** | **CC BY 4.0** | **PERMITTED** with attribution | **PERMITTED** with proper attribution |
| **Anthropic "Clawd" Mascot (`LicenseRef-Clawd`)** | **PROPRIETARY (Anthropic)** | **PROHIBITED** | **STRICTLY FORBIDDEN** |
| **Third-Party Trademarks & UI Redraws** | **PROPRIETARY (Owners)** | **PROHIBITED** | **STRICTLY FORBIDDEN** |
| **Edge TTS / Doubao Voice Demos** | **EXCLUDED FROM LICENSE** | **PROHIBITED** (Cannot extract) | **STRICTLY FORBIDDEN** |

---

## 2. DETAILED FILE-LEVEL LICENSING BREAKDOWN

### 2.1 Rule 4: The MIT Code Tier (Legally Safe for Master AI Codebase)
Under Rule 4 of `LICENSE` and Section 1 of `REUSE.toml`:
- **Files Covered:** All JavaScript, Python, Shell, and configuration files in `core/`, `tools/`, `styleboard/`, `plugin/`, and the individual demo `index.html` and script files.
- **License Terms:** Standard MIT License (`LICENSES/MIT.txt`).
- **Permissions:** Full right to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software.
- **Obligation:** The copyright notice (`Copyright (c) 2026 Lemomo (LemoLab)`) and the MIT permission notice must be included in substantial portions of the software.

### 2.2 Rule 2: The CC BY-NC 4.0 Documentation & Prompt Tier (Restricted)
Under Rule 2 of `LICENSE` and Section 2 of `REUSE.toml`:
- **Files Covered:**
  - Every Markdown file (`*.md`): including `AGENTS.md`, `DIRECTOR.md`, `TECHNIQUE.md`, and all 101 `styles/*/STYLE.md` and `DEMO.md` files.
  - All prompt files: `styles/*/demo/prompts/**`.
  - Style suffixes: `styles/manga-panels/demo/tools/style_suffix.txt` and `styles/comic-history/demo/tools/sheets.json`.
- **License Terms:** Creative Commons Attribution-NonCommercial 4.0 International.
- **Commercial Film Production Exception:**
  Lemomo grants an explicit worldwide, royalty-free, non-exclusive permission to read, follow, copy, and adapt the docs to make films (including commercial client films).
- **Product Redistribution Prohibition:**
  The grant explicitly states:
  > *"This permission does not cover sharing the docs or adapted versions with others beyond those people and those project files, or selling them: CC BY-NC 4.0 and the commercial licence below govern those. Any commercial use of the docs beyond the permission above (for example selling them, or putting them, whole, in part or adapted, into a product or service run for commercial advantage, paid or not) needs a commercial licence."*
- **Impact on Master AI:**
  Master AI cannot copy, bundle, or redistribute Lemo-Opuscar's Markdown guides or prompt collections into its public distribution without purchasing a commercial license from Lemomo Studio (`lemomo.studio@gmail.com`).

### 2.3 Excluded & Third-Party Proprietary Assets
1. **Anthropic Clawd Character (`LicenseRef-Clawd`):**
   Appears in `styles/mascot-screencast/`, `OPUSCAR 98`, and thank-you demo files. This character is the proprietary trademark and design of Anthropic. **Must never be copied or bundled into Master AI.**
2. **Third-Party Trademarks & UIs (`LicenseRef-ThirdPartyMarks`):**
   Includes redraws of the Anthropic Claude interface, Apple macOS desktop UI, OpenAI GPT interfaces, etc. Not licensed for commercial redistribution.
3. **Six Specific Narration Tracks:**
   The audio tracks in the demo films of *Chalkboard*, *Circuit Board*, *Tabletop App Flythrough*, *Isometric People Scene*, *Scratchboard Long Take*, and *Broadcast News Package* are explicitly excluded from any license. They must not be extracted or reused.

---

## 3. SECURITY & CODE EXECUTION AUDIT

A thorough static security analysis of Lemo-Opuscar's source code was conducted to identify potential execution risks, network vulnerabilities, and sandbox boundaries:

### 3.1 Subprocess Execution Risks
- **`core/render/video.mjs`:** Spawns `ffmpeg` with user-specified resolution, FPS, and segment directories. Arguments are strictly sanitized and piped via IPC. No raw shell string interpolation (`exec` is avoided in favor of `spawn` with array arguments).
- **`core/render/mux.sh`:** Bash script that executes FFmpeg loudnorm and limiter filters. While standard, running arbitrary shell scripts on Windows poses path parsing and terminal injection risks.
- **`core/image/gen_image.py`:** Executes `codex exec` via subprocess. If invoked without credentials or inside an unauthorized environment, it could attempt unapproved external API requests.

### 3.2 Network Behavior & Data Exfiltration
- **Headless Local Server (`core/render/serve.mjs`):** Binds strictly to `127.0.0.1` (localhost) to serve static demo files to Playwright. It does not open external public ports.
- **Asset Fetching (`tools/fetch.sh` & `sampler.py`):** When `LEMO_FETCH=1`, the scripts download sample soundfonts and models from GitHub releases and Hugging Face.
- **Recommendation:** In Master AI, enforce `LEMO_FETCH=0` to block untrusted background downloads and maintain our zero-paid / zero-external invariant.

### 3.3 File System & Concurrency Safety
- **Lock Files (`.lock`):** `video.mjs` prevents race conditions by creating `<out>.lock`. It handles stale locks by verifying process PID liveness (`process.kill(pid, 0)`).
- **Segment Cleanup:** Temporary segment files (`.<base>_segs-<id>/`) are deleted automatically on process exit, `SIGINT`, or error.

---

## 4. COMPLIANCE & GOVERNANCE MANDATE FOR MASTER AI

To safely utilize Lemo-Opuscar capabilities within Master AI without legal liability or security compromise, the following governance rules are established:

1. **Clean-Room Code Adaptation (Rule 4 Only):**
   Master AI may adapt the MIT-licensed rendering mechanisms (`video.mjs`, `page.mjs`, `lib.js`) into its native Python/Node visual adapters.
2. **Strict Exclusion of CC BY-NC 4.0 Text & Prompts:**
   Do **not** copy or vendor the `styles/*/demo/prompts/` directory or Markdown style guides into Master AI's repository. Master AI specialist agents must generate their own original system prompts and scene descriptions.
3. **Exclusion of Proprietary Assets:**
   Blacklist and delete all references to `LicenseRef-Clawd`, third-party trademark redraws, and demo voice tracks.
4. **Offline Isolation:**
   All rendering must operate against local static templates with zero external internet dependencies during frame generation.
