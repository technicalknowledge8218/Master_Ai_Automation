# UNIFIED EDITING AND 16-POINT QUALITY GATES
## UnifiedTimelineEngine, VisualQualityEvaluator, AssetLicenseVerifier & Comprehensive QA Protocol

**Document Version:** 1.0.0-unified-production  
**Project Root:** `F:\Master AI`  
**Target Path:** `00_CORE_SYSTEM\research\phase-7\unified-visual-production\UNIFIED_EDITING_AND_QUALITY_GATES.md`  
**Classification:** Quality Engineering, Audio-Visual Verification & License Governance  
**Status:** Approved Quality Specification  

---

## 1. THE UNIFIED TIMELINE ENGINE (`UnifiedTimelineEngine.py`)

Regardless of whether a scene was produced via 2D vector animation, 3D Blender CGI, or authentic stock video, all streams flow into the **`UnifiedTimelineEngine`**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        UNIFIED TIMELINE ENGINE                         │
├────────────────────────────────────────────────────────────────────────┤
│ • Input Normalizer: Transcodes all source clips to uniform             │
│   1920x1080, 30.0 FPS, yuv420p color matrix.                           │
│ • Transition Orchestrator: Calculates xfade offsets dynamically based  │
│   on FireRed directing plan pacing metadata.                           │
│ • Harmonization Filtergraph: Chains 3D LUTs, film grain, and subtitles │
│   in a single, hardware-accelerated FFmpeg pass.                       │
│ • Audio Bus Mixer: Combines voice, music, and foley stems into a       │
│   continuous master soundtrack with dynamic sidechain ducking.         │
│ • Multi-Ratio Exporter: Transcodes 16:9 Landscape, 9:16 Vertical, and  │
│   1:1 Square outputs concurrently.                                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. THE 16-POINT MEDIA QUALITY GATE

Before any production can be submitted to the `ApprovalCenter`, it must pass all 16 automated, fail-closed quality checks in `VisualQualityEvaluator`:

| Check # | Check Name | Evaluation Methodology | Passing Criteria | Action on Failure |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Video Duration Check** | FFprobe container inspection | Duration == `target_duration_sec ± 0.5s` | **FAIL-CLOSED** (Re-render) |
| **02** | **Resolution & FPS Check** | Stream metadata analysis | `1920x1080` (or `1080x1920`), `30.0 FPS` | **FAIL-CLOSED** (Transcode) |
| **03** | **Bitstream Decode Audit** | Full decode via `ffmpeg -f null -` | **Zero unreadable packets or decode errors** | **FAIL-CLOSED** (Re-encode) |
| **04** | **Frozen / Black Frame Audit**| Frame pixel standard deviation | Zero frozen segments >1.5s; zero black frames | **FAIL-CLOSED** (Scene repair) |
| **05** | **2D Vector Quality Check** | Edge detection & anti-aliasing scan | Clean vector contours; zero pixelation artifacts | **WARNING** (Review) |
| **06** | **3D CGI Depth Verification** | Optical flow & parallax delta test | Verifiable spatial parallax ($\Delta x_{\text{fg}} > \Delta x_{\text{bg}}$) | **FAIL-CLOSED** (Reject fake 3D) |
| **07** | **Real Footage Provenance** | SHA-256 hash match against `.provenance`| Exact checksum match; verified public domain/Pexels | **FAIL-CLOSED** (Block unverified) |
| **08** | **Audio Duration Check** | WAV header sample count inspection | Audio duration == Video duration ± 0.1s | **FAIL-CLOSED** (Pad / Trim) |
| **09** | **EBU R128 Loudness Audit** | Two-pass `ebur128` filter measurement| Integrated loudness == **`-14.0 LUFS ± 1.0`** | **FAIL-CLOSED** (Re-master) |
| **10** | **True Peak Ceiling Check** | Peak amplitude measurement | True peak <= **`-1.0 dBTP`** (Zero digital clipping) | **FAIL-CLOSED** (Limiter pass) |
| **11** | **Vocal Ducking Verification** | Audio amplitude comparison during voice | Music attenuated by **`-14 dB to -18 dB`** during speech | **FAIL-CLOSED** (Adjust ducking) |
| **12** | **Silent Audio Gap Audit** | Silence detect filter (`silencedetect`) | Zero silent sections >6.0s outside ambient beds | **WARNING** (Check breathers) |
| **13** | **ASR Speech Intelligibility** | `faster-whisper` CPU INT8 transcription | Levenshtein similarity >= **85%**; zero hallucinations | **FAIL-CLOSED** (Re-synthesize) |
| **14** | **Subtitle Synchronization** | Timestamp overlap vs audio chunks | Subtitle starts within ±0.2s of speech start | **FAIL-CLOSED** (Re-timecode) |
| **15** | **Asset License Verifier** | License manifest audit | 100% commercial exploitation permitted; zero NC | **FAIL-CLOSED** (Reject asset) |
| **16** | **Zero-Budget Spend Gate** | Billing ledger & token counter audit | Total project expenditure == **`₹0.00 / $0.00`** | **FAIL-CLOSED** (Block dispatch) |

---

## 3. ASSET LICENSE VERIFIER (`AssetLicenseVerifier.py`)

The `AssetLicenseVerifier` audits every file referenced in the project manifest before final release:
1. **Permitted Licenses:**
   - Code: MIT, BSD, Apache 2.0, GNU GPL v3.
   - Media & Stock: Pexels License, Creative Commons CC0-1.0 Universal, US Government Public Domain.
   - Fonts: SIL Open Font License (OFL).
2. **Strictly Blacklisted Terms:**
   - Creative Commons NonCommercial (`CC BY-NC`, `CC BY-NC-SA`).
   - Proprietary "Editorial Use Only" or "Personal Use Only" tags.
   - Unlicensed scraped web images or watermarked stock samples.
3. **Execution Invariant:** Any asset failing verification is automatically purged from the project directory, and the orchestrator is instructed to acquire a verified CC0 alternative.
