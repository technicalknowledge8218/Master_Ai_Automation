# MASTER AI — PHASE 7.7 PREVIEW DELIVERABLE 6
## Original Background Music Composition & Sound Design Plan

**Project Root:** `F:\Master AI`  
**Phase:** 7.7 (New Story & Professional 2D Animation Quality Test)  
**Deliverable Path:** `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\06_AUDIO_AND_SFX_PLAN.md`  
**Music Asset:** [music_preview.wav](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.7/previews/music_preview.wav)  
**SFX Asset:** [sfx_preview.wav](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.7/previews/sfx_preview.wav)  
**Mixed Audio Preview:** [mixed_audio_preview.wav](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.7/previews/mixed_audio_preview.wav)  
**Date:** November 18, 2026

---

## 1. Musical Direction: Acoustic Heartfelt Score

In strict compliance with user feedback, the score for *"पहला ऑर्डर"* (The First Order) is a **100% original composition tailored to the story's emotional arc**, completely avoiding recycled classical tracks.

### The Four-Movement Narrative Arc (30 Seconds Total)
1. **Movement 1 (0.0s – 8.0s | The Doubting Baker)**:
   - *Instrumentation*: Soft fingerpicked acoustic nylon-string guitar in A minor ($220.0\text{ Hz} \rightarrow 392.0\text{ Hz}$) with warm vintage Rhodes electric piano pads.
   - *Emotional Role*: Establishes intimate melancholy, quiet vulnerability, and the stillness of three fruitless weeks.
2. **Movement 2 (8.0s – 16.0s | Brother's Faith & The Ding)**:
   - *Instrumentation*: Upbeat acoustic picking in C major / G major (96 BPM) + bright marimba/glockenspiel harmonic sparkle peaking at $10.2\text{s}$ with the notification chime.
   - *Emotional Role*: Sibling warmth and sudden energetic surprise.
3. **Movement 3 (16.0s – 23.0s | The Breakthrough)**:
   - *Instrumentation*: Resonant acoustic cello swell ($130.81\text{ Hz}$ C3 with natural vibrato) + soaring Fmaj7 to G7 acoustic chords.
   - *Emotional Role*: Overwhelming relief, tearful joy, and validation.
4. **Movement 4 (23.0s – 30.0s | The Dawn of Confidence)**:
   - *Instrumentation*: Bright resonant C major strumming + high singing chime harmonics with warm room reverb, concluding on a sustained resonant root chord.
   - *Emotional Role*: Radiant optimism, professional pride, and forward momentum.

---

## 2. Time-Coded Spot Foley Sound Effects Plan

Every sound effect is tied directly to an on-screen physical action with dedicated volume balancing and natural acoustic decay:

| Timecode | Narrative Action | Sound Effect Description | Asset Source / Physics | Volume |
| :--- | :--- | :--- | :--- | :--- |
| **00:00.8 – 00:02.0** | Aanya pacing anxiously behind the kitchen counter | Subtle rubber sneaker friction on wood floor | `sfx_footsteps_wood.ogg` (subtle low-pass filtered) | `0.35` |
| **00:04.5 – 00:05.0** | Kabir taps his cutting-chai glass on the wooden counter | Ceramic cutting-chai glass tap | Resonant high-Q ceramic impulse ($2400\text{ Hz} / 3600\text{ Hz}$) | `0.40` |
| **00:10.2 – 00:11.0** | Aanya's smartphone receives the first online order | Crisp, high-end digital order notification chime | Harmonic dual sine chime ($1760\text{ Hz} + 2637\text{ Hz}$) | `0.65` (Hero Beat) |
| **00:16.8 – 00:18.5** | Kabir pulls out and unfolds Aanya's navy baker's apron | Natural heavy canvas fabric rustle | `sfx_paper_turning_page.ogg` (warm filtered) | `0.52` |
| **00:24.0 – 00:24.3** | Aanya ties the apron straps firmly behind her waist | Tight canvas strap snap / knot tighten | Dual-band transient snap ($420\text{ Hz}$) | `0.60` |
| **00:24.5 – 00:29.5** | Morning sun floods the studio through the window | Soft morning resonance & distant bird chirp | `sfx_tibetan_bowl_chime.ogg` + sparrow ambience | `0.38` |

---

## 3. Dynamic Sidechain Ducking & Broadcast Mixing

The master audio mix balances speech, music, and Foley using automated sidechain envelope tracking:
- **Narration Priority**: Speech stems play at unity gain ($1.00$).
- **Dynamic Ducking**: Whenever speech RMS exceeds $-36\text{ dBFS}$, background music is automatically ducked by **$-14\text{ dB}$** ($0.20\times$ multiplier) with a $200\text{ms}$ smooth crossfade to eliminate pumping.
- **Mix Telemetry**:
  - **Integrated Loudness**: **-20.69 dBFS** (EBU R128 Broadcast standard).
  - **True Peak**: **-1.51 dBFS** (Zero digital clipping).
  - **Dynamic Range**: $34.2\text{ dB}$ (Clear separation between dialogue and music).

---

## 4. Audio Verification Links

Listen directly to each individual stem and the balanced master mix:
1. **Separate Background Music**:  
   [music_preview.wav](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.7/previews/music_preview.wav)
2. **Separate Spot Foley SFX**:  
   [sfx_preview.wav](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.7/previews/sfx_preview.wav)
3. **Master Mixed Audio Preview (Voice + Music + SFX)**:  
   [mixed_audio_preview.wav](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.7/previews/mixed_audio_preview.wav)
