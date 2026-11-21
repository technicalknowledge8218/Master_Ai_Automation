# LICENSE AUDIT CORRECTIONS & FORENSIC INVESTIGATION
**Master AI — Phase 7.0.4 Technical Reality Audit**  
**Audit Target:** Commercial Legality, Model Cards, Datasets, and Copyleft Jurisprudence  
**Execution Environment:** Windows 11, Python 3.14  
**Date:** November 2026  
**Auditor:** Independent Licensing & Architecture Verification Agent  

---

## 1. Executive Summary & Critical Corrections

Phase 7.0.3 highlighted general licensing categories but made two critical assumptions that required empirical correction:
1. **Piper TTS Repository Assumption (Corrected):** Assuming that because the `rhasspy/piper` repository engine is MIT licensed, its pre-trained voice checkpoints are automatically permitted for commercial exploitation.
2. **Wikimedia Commons CC BY-SA Generalization (Corrected):** Treating all CC BY-SA assets as an infectious copyleft contamination across all forms of media compilation without distinguishing between **Adaptations (Derivative Works)** and **Collections (Compilations)** under Creative Commons legal definitions.

This forensic audit conducted direct network queries of the official Piper model cards on Hugging Face, verified underlying dataset terms, and established clear legal distinctions for documentary production.

---

## 2. Piper Hindi Voice Model Forensic Audit

Forensic inspection was executed directly against the raw Hugging Face model cards under `rhasspy/piper-voices`:

```
Direct Endpoint: https://huggingface.co/rhasspy/piper-voices/raw/main/hi/hi_IN/<voice>/medium/MODEL_CARD
```

### 2.1 Model: `pratham` (`hi_IN-pratham-medium`)
- **Direct Source URL:** `https://huggingface.co/rhasspy/piper-voices/raw/main/hi/hi_IN/pratham/medium/MODEL_CARD`
- **Quality / Architecture:** Medium, 22,050 Hz, 1 Speaker, VITS ONNX.
- **Training Source:** `https://github.com/AI4Bharat/indicnlp_corpus` (Trained by PravalX).
- **Dataset License:** `http://creativecommons.org/licenses/by-nc-sa/4.0/` (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International).
- **Legal Analysis:**
  - The underlying training corpus is licensed under **CC BY-NC-SA 4.0**.
  - Under Section 2(a)(1) of the CC BY-NC-SA 4.0 license, the license explicitly denies rights for commercial purposes: *"NonCommercial means not primarily intended for or directed towards commercial advantage or monetary compensation."*
  - The model weights are a direct derivative of this corpus. Training a neural voice model on non-commercial audio data creates a derivative model bound by the non-commercial covenant.
  - Furthermore, the **ShareAlike (SA)** clause mandates that any derivative model or synthesized content claiming to redistribute or adapt the corpus must be shared under the exact same terms.
- **Commercial Status:** **STRICTLY NON-COMMERCIAL. COMMERCIAL MONETIZATION PROHIBITED.**
- **Verdict:** **REJECTED & QUARANTINED.**

### 2.2 Model: `priyamvada` (`hi_IN-priyamvada-medium`)
- **Direct Source URL:** `https://huggingface.co/rhasspy/piper-voices/raw/main/hi/hi_IN/priyamvada/medium/MODEL_CARD`
- **Quality / Architecture:** Medium, 22,050 Hz, 1 Speaker, VITS ONNX.
- **Training Source:** `https://github.com/AI4Bharat/indicnlp_corpus` (Trained by PravalX).
- **Dataset License:** `http://creativecommons.org/licenses/by-nc-sa/4.0/` (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International).
- **Legal Analysis:**
  - Identical dataset lineage and trainer to `pratham`.
  - Governed by CC BY-NC-SA 4.0. Commercial exploitation on monetized YouTube channels, client deliverables, or commercial streaming platforms constitutes copyright infringement and breach of license.
- **Commercial Status:** **STRICTLY NON-COMMERCIAL. COMMERCIAL MONETIZATION PROHIBITED.**
- **Verdict:** **REJECTED & QUARANTINED.**

### 2.3 Model: `rohan` (`hi_IN-rohan-medium`)
- **Direct Source URL:** `https://huggingface.co/rhasspy/piper-voices/raw/main/hi/hi_IN/rohan/medium/MODEL_CARD`
- **Quality / Architecture:** Medium, 22,050 Hz, 1 Speaker, VITS ONNX (fine-tuned from US English `lessac`).
- **Dataset Provider:** IIT Madras DonLab IndicTTS (`https://www.iitm.ac.in/donlab/indictts`).
- **Database Name:** "Hindi Mono Male".
- **Dataset License URL:** `https://www.iitm.ac.in/donlab/indictts/downloads/license.pdf`.
- **Legal Analysis:**
  - The dataset was created by the Speech Technology Consortium funded by TDIL, Ministry of Electronics and Information Technology (MeitY), Government of India.
  - The DonLab download license URL (`/downloads/license.pdf`) is currently unreachable / timing out on network requests.
  - Historical Speech Consortium documentation indicates that early releases were restricted to academic and research evaluation, while later iterations under Bhashini/AI4Bharat migrated to open models.
  - Because the exact text of `license.pdf` cannot be retrieved and verified to contain an explicit, unconditional commercial use grant, commercial rights cannot be legally certified.
- **Commercial Status:** **UNVERIFIED / UNCERTAIN RIGHTS.**
- **Verdict:** **QUARANTINED.** Do not approve for commercial production until explicit written terms or an unencumbered permissive voice model is established.

### 2.4 Summary of Piper Voice Models

| Voice Model | Language | Dataset Origin | Dataset License | Commercial Production Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **`hi_IN-pratham-medium`** | Hindi (India) | AI4Bharat indicnlp_corpus | CC BY-NC-SA 4.0 | **FAIL (Quarantined - Non-Commercial)** |
| **`hi_IN-priyamvada-medium`**| Hindi (India) | AI4Bharat indicnlp_corpus | CC BY-NC-SA 4.0 | **FAIL (Quarantined - Non-Commercial)** |
| **`hi_IN-rohan-medium`** | Hindi (India) | IIT Madras IndicTTS | Undetermined (license.pdf unreachable) | **QUARANTINED (Unverified Commercial Rights)** |

*Rule:* Master AI must **NOT** use `pratham`, `priyamvada`, or `rohan` for commercial documentary projects.

---

## 3. Wikimedia Commons CC BY-SA Legal Correction

In previous research (Phase 7.0.3), the audit warned of "copyleft contamination" whenever a Creative Commons Attribution-ShareAlike (`CC BY-SA 3.0 / 4.0`) asset is used. This requires rigorous legal refinement.

### 3.1 Creative Commons Legal Taxonomy: Adaptations vs Collections

Under **Creative Commons 4.0 Legal Code (Section 1 and Section 3)**:

1. **What is a "Collection" (Collective Work / Compilation)?**
   - A **Collection** is a compilation of separate, independent works, assembled together (e.g., an anthology of poems, an encyclopedia, or a directory of standalone video files).
   - *Legal Effect:* Merely including an unmodified CC BY-SA work in a collection does **not** require the collection as a whole or the other independent works in it to be licensed under CC BY-SA. The CC BY-SA asset retains its own license, and the other assets retain theirs.
2. **What is an "Adapted Material" (Derivative Work)?**
   - An **Adapted Material** is work derived from or based upon the licensed material, where the material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring copyright permission.
   - *Legal Effect:* The adapter's license **must** be CC BY-SA or a compatible license. The derivative output is bound by ShareAlike.

### 3.2 The Specific Reality of Video & Audio Synchronization
Why does CC BY-SA remain dangerous for commercial video editing despite the "Collection" exception?

- **Synchronization ("Synch Rights"):** Under US copyright law (and international Berne Convention jurisprudence), synchronizing audio (voiceover, music) with moving images creates a **Derivative Work** (an adaptation), not merely a collection.
- **Timeline Editing & Compositing:** When an editor cuts a clip, applies crossfades (`xfade`), overlays lower-thirds or color grading, and mixes it into a master audio/video stream, the resulting composite scene is legally categorized as an **Adapted Material**.
- **Commercial Distribution Risk:** If an adaptation contains a CC BY-SA element, the ShareAlike clause mandates that the adapted scene (or potentially the entire integrated video master) be made available under CC BY-SA. This prevents the producer from granting exclusive licenses, selling proprietary rights, or enforcing standard copyright protection on commercial platforms.

### 3.3 Final Operational Policy for Master AI
- **Public Domain & CC0 Assets:** **APPROVED.** Completely safe for commercial production without attribution or copyleft risk.
- **CC BY Assets:** **APPROVED WITH ATTRIBUTION.** Permitted for commercial use, provided the author, title, source URL, and license are explicitly recorded in `credits.json` and `ATTRIBUTIONS.md`.
- **CC BY-SA Assets:** **QUARANTINED FOR COMMERCIAL MASTERS.** Because video synchronization and transitions constitute derivative adaptations that risk ShareAlike copyleft contamination, CC BY-SA media must not be composited into proprietary commercial documentaries.

---

## 4. Quarantined Asset Register

The following assets are permanently registered in the Master AI Quarantine Ledger:

| Asset Name | Provider / Repo | Detected License | Reason for Quarantine |
| :--- | :--- | :--- | :--- |
| **Meta MusicGen Weights** | Hugging Face (`facebook/musicgen-*`) | CC BY-NC 4.0 | Non-commercial model weights trap. |
| **Piper Pratham Voice** | Hugging Face (`rhasspy/piper-voices`) | CC BY-NC-SA 4.0 | Non-commercial and ShareAlike dataset license. |
| **Piper Priyamvada Voice**| Hugging Face (`rhasspy/piper-voices`) | CC BY-NC-SA 4.0 | Non-commercial and ShareAlike dataset license. |
| **Piper Rohan Voice** | Hugging Face (`rhasspy/piper-voices`) | Unverified TDIL/Consortium | `license.pdf` unreachable; commercial grant unproven. |
| **Wikimedia CC BY-SA Media**| Wikimedia Commons | CC BY-SA 3.0 / 4.0 | Synchronization/derivative copyleft contamination risk. |
| **Microsoft Edge TTS** | Unofficial Python `edge-tts` | LGPLv3 / MS Consumer Terms | Violates MS Service Agreement Section 3 (scraping/commercial SaaS). |
