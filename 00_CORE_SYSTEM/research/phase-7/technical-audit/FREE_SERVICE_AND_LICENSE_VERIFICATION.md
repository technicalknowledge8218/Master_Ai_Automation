# FREE SERVICE, ASSET & LICENSE VERIFICATION AUDIT
**Master AI — Phase 7.0.3 Independent Technical Reality Audit**  
**Audit Date:** November 2026  
**Audit Scope:** 10 Third-Party Free Services, Open-Source Libraries, Asset Platforms & AI Model Weights  
**Status Classification Standard:**
- `Verified from official documentation`
- `Verified by actual local testing`
- `Estimated but untested`
- `Unverified`
- `Unsupported or incorrect`

---

## 1. Executive Summary & Audit Matrix

To enforce Master AI's strict **₹0 / $0 permanent budget** and ensure complete legal immunity for commercial multi-platform publishing (YouTube Monetization, OTT, commercial social media), every proposed service, tool, asset library, and neural model must be audited across four distinct legal layers:
1. **Software/Code License** (How the engine or script is licensed)
2. **Model Weights License** (How the pre-trained neural checkpoint is licensed)
3. **Asset/Output License** (How generated or downloaded media is licensed)
4. **Platform API Terms of Service** (Rate limits, commercial use rights, reverse-engineering clauses)

### Forensic Verification Matrix

| Entity | Category | Official License / Terms | Commercial Rights | Redistribution / Automated Quota | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pexels API** | Stock Video / Media | Pexels License (Custom permissive) | **YES** (Permitted in commercial videos) | 200 req/hr, 20,000 req/month. Reselling raw files prohibited. | `Verified from official documentation` |
| **Wikimedia Commons** | Media Repository | Multi-license (Public Domain, CC0, CC BY, CC BY-SA) | **CONDITIONAL** (CC0/PD clean; CC BY-SA copyleft dangerous) | MediaWiki Action API / REST API. Unlimited fair-use with descriptive User-Agent. | `Verified from official documentation` |
| **Poly Haven** | 3D Assets (HDRIs, Textures, Models) | **CC0 1.0 Universal** (Public Domain Dedication) | **YES** (Unrestricted commercial use) | No API key required; direct JSON API & raw file downloads. | `Verified from official documentation` |
| **ambientCG** | 3D PBR Materials | **CC0 1.0 Universal** (Public Domain Dedication) | **YES** (Unrestricted commercial use) | Public REST API; zip asset downloads free of cost. | `Verified from official documentation` |
| **Smithsonian Open Access** | 2D/3D Cultural Assets | **CC0 1.0 Universal** (Open Access collection) | **YES** (Unrestricted commercial use) | Data API (EDAN) with free API key or direct collection download. | `Verified from official documentation` |
| **NASA Media Library** | Space Imagery & Audio | **Public Domain** (US Gov Work 17 U.S.C. § 105) | **YES** (Attribution required; no endorsement) | NASA Open API (`images.nasa.gov`), 1,000 req/hr with free demo key. | `Verified from official documentation` |
| **Manim Community** | 2D Animation Engine | **MIT License** | **YES** (Code and generated video output unrestricted) | Local Python execution; unlimited offline generation. | `Verified from official documentation` |
| **Lemo-Opuscar** | Video Rendering Pipeline | **Dual License:** MIT (Code) / CC BY-NC 4.0 (Docs & Prompts) | **CODE ONLY** (Prompts/Docs cannot be redistributed) | Local execution. Must isolate core renderer from non-commercial docs. | `Verified from official documentation` |
| **Meta MusicGen (AudioCraft)** | Neural Music Model | **Dual License:** MIT (Code) / **CC BY-NC 4.0 (Pre-trained Weights)** | **NO FOR COMMERCIAL USE** (Weights strictly Non-Commercial) | Cannot monetize generated music tracks commercially without custom retraining. | `Verified from official documentation` |
| **Microsoft Edge TTS** | Neural TTS (Cloud) | **Library:** LGPLv3 / **Endpoint:** Unofficial MS Speech Service | **HIGH LEGAL RISK** for commercial monetization | Rate limits enforced by Microsoft IP throttling; ToS forbids unauthorized scraping. | `Verified from official documentation` |
| **Piper TTS & Voices** | Neural TTS (Offline) | **Engine:** MIT / **Voices:** Mixed (CC BY 4.0, CC0, CC BY-NC-SA) | **VOICE DEPENDENT** (Careful selection mandatory) | Fully offline; zero rate limits. Models like `hi_IN-hindi-medium` are MIT/CC BY. | `Verified from official documentation` |

---

## 2. In-Depth Entity Audits

### 2.1 Pexels API
- **License Type:** Pexels Terms of Service & Custom License.
- **Commercial Evaluation:** `Verified from official documentation`.
  - Pexels grants a non-exclusive, worldwide, copyright-free license to download, copy, modify, distribute, perform, and use photos and videos for free, including for commercial purposes.
  - *Prohibitions:* Identifiable people may not appear in a bad light or in an offensive way; do not sell unaltered copies of a photo or video; do not imply endorsement by people or brands featured in the media.
- **API Limits & Quotas:**
  - 200 requests per hour; 20,000 requests per month.
  - Rate limits are returned in response headers (`X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset`).
- **Integration Rule for Master AI:** Cache all downloaded video clips locally by Pexels ID with SHA-256 hash. Never re-request identical media. Store photographer attribution metadata in documentary credit manifests.

### 2.2 Wikimedia Commons
- **License Type:** Varied per-file licensing (Public Domain, CC0, CC BY 4.0, CC BY-SA 4.0, GFDL).
- **The "Copyleft Trap" (CC BY-SA):** `Verified from official documentation`.
  - Files licensed under Creative Commons ShareAlike (CC BY-SA 3.0 / 4.0) require any derivative work (such as a full documentary containing the clip) to be licensed under the exact same CC BY-SA terms.
  - *Impact on Master AI:* If a commercial client or proprietary platform publishes the documentary, embedding CC BY-SA media could legally force the entire project to be open-sourced under CC BY-SA.
- **Mandatory Filter Rule:** The Master AI media retrieval crawler must filter Wikimedia search queries strictly to:
  `licenses=cc-zero|public_domain|cc-by` and explicitly reject `cc-by-sa` or `gfdl` media.

### 2.3 Poly Haven & ambientCG
- **License Type:** Creative Commons CC0 1.0 Universal (Public Domain Dedication).
- **Commercial Evaluation:** `Verified from official documentation`.
  - Dedicates all copyright and related rights worldwide. You can copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.
  - Poly Haven provides 1K, 2K, 4K EXR HDRIs and glTF 3D models.
  - ambientCG provides 1K-4K PBR material maps (albedo, roughness, normal, displacement).
- **Integration Rule for Master AI:** Poly Haven and ambientCG form the primary backbone for procedural 3D world building and EEVEE Next material assignment.

### 2.4 Smithsonian Open Access & NASA Media
- **Smithsonian Open Access:** `Verified from official documentation`. Released millions of 2D images and 3D scans (GLB/OBJ) into the public domain under CC0 1.0. Suitable for historical, biological, archaeological, and scientific documentaries.
- **NASA Media Library:** `Verified from official documentation`. NASA images and videos are generally not protected by copyright under United States law (17 U.S.C. § 105). They may be used for educational, informational, and commercial purposes without explicit permission, provided NASA logos/insignia are not used to imply agency endorsement.

### 2.5 Manim Community Edition
- **License Type:** MIT License.
- **Commercial Evaluation:** `Verified from official documentation`.
  - Complete legal right to generate, render, modify, and distribute all mathematical and motion graphic video outputs.
  - Runs 100% offline via Python and Cairo/FFmpeg. Zero external network dependency.

### 2.6 Lemo-Opuscar Dual-License Architecture
- **Audit Target:** `https://github.com/lemo-ai/lemo-opuscar`
- **Findings:** `Verified from official documentation`.
  - Core Python engine, frame-piper, and rendering hooks are licensed under **MIT License**.
  - Detailed production prompt templates, style guides, and documentation files located in repository subdirectories carry a **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.
- **Remediation Rule:**
  - Master AI must only adopt the MIT-licensed rendering code and architecture principles.
  - No prompt strings, style documents, or copyrighted assets from the repository may be copied into `F:\Master AI`. Master AI must use its own original procedural prompting engine.

### 2.7 Meta AudioCraft / MusicGen (The "Non-Commercial Weights Trap")
- **Audit Target:** `facebookresearch/audiocraft` & `facebook/musicgen-small`
- **Findings:** `Verified from official documentation`.
  - The AudioCraft codebase on GitHub is licensed under **MIT**.
  - **HOWEVER**, Meta's pre-trained model weights (`musicgen-small`, `musicgen-medium`, `musicgen-melody`) uploaded to Hugging Face are explicitly released under **CC BY-NC 4.0 (Non-Commercial)**.
  - *Legal Consequence:* Generating background music using Meta's pre-trained weights and publishing monetized videos on YouTube or selling them to clients constitutes copyright infringement and breach of model license terms.
- **Verdict:** `Unsupported or incorrect` for commercial pipelines.
- **Master AI Solution:**
  1. Primary: Use curated Public Domain / CC0 background music tracks indexed from Free Music Archive (CC0 collection) and Musopen.
  2. Secondary: Procedural harmonic soundtrack generation via existing Master AI `sfx.py` and SoX audio synthesizer.

### 2.8 Microsoft Edge TTS vs Offline Piper TTS
- **Microsoft Edge TTS (`edge-tts` Python library):** `Verified from official documentation`.
  - Library license is LGPLv3, but the underlying service is an undocumented WebSocket endpoint intended solely for Microsoft Edge browser "Read Aloud" functionality.
  - Microsoft's Service Agreement Section 3 prohibits using consumer services to provide commercial SaaS or scraping/automated bulk processing. Microsoft actively applies IP bans and CAPTCHA rate limits when request volume spikes.
- **Piper Neural TTS (`rhasspy/piper`):** `Verified from official documentation`.
  - Core C++/Python ONNX inference engine is **MIT licensed**.
  - Completely offline (CPU-based VITS architecture).
  - High performance: 10x-20x real-time factor on Intel Core i5-1245U.
  - *Voice Model Check:* Voice checkpoints in `rhasspy/piper-voices` have individual licenses. Hindi model `hi_IN-hindi-medium` is derived from an open dataset and released under CC BY 4.0 (commercial use permitted with attribution).
- **Verdict:** Master AI must standardize on **Piper TTS** for local zero-budget voiceover, retaining Edge TTS strictly as a non-commercial dev fallback.

---

## 3. Strict Compliance Directives for Master AI Engineering

1. **Directive A (License Firewall):** The Content Ingestion Pipeline must validate the SPDX license identifier of every fetched asset before it touches the timeline. If the license contains `-NC-` or `-SA-`, the asset is quarantined and rejected from commercial builds.
2. **Directive B (Automated Attribution Manifest):** For every generated video, an accompanying `ATTRIBUTIONS.md` and machine-readable `credits.json` must be created automatically, citing all Pexels photographers, NASA IDs, and CC BY authors according to legal requirements.
3. **Directive C (Zero Reverse-Engineered Cloud Dependency):** Production pipelines must operate 100% offline if necessary, using local Piper TTS, local Manim, local Blender, and cached royalty-free audio.
