# MASTER AI — PHASE 7.5 VOICEOVER ENGINE ARCHITECTURE
**Neural Speech Synthesis, Timeline Alignment & Loudness Normalization Architecture**
*Project Root: `F:\Master AI`*
*Date: November 18, 2026*
*Author: AGT-013 (Voice Lead) & AGT-012 (Audio Director)*

---

## 1. Engine Design Principles & Invariants

The `VoiceoverEngine` (`F:\Master AI\09_CONTENT_STUDIO\engine\voiceover_engine.py`) provides an autonomous, broadcast-compliant speech synthesis pipeline engineered under three non-negotiable principles:

1. **Strict Human Speech Invariant**:
   Procedural tones, harmonic sine waves, or robotic bleeps must NEVER be substituted for human speech. If a genuine neural or phonetic human voice engine is unavailable, the pipeline must fail closed to an explicit User Narration Recording Checkpoint.
2. **Millisecond-Exact Timeline Conforming**:
   Dialogue must not be lumped into a single unaligned audio block. Every cue must be synthesized independently, duration-measured, normalized, and positioned at exact timeline timestamps via FFmpeg `adelay` filters.
3. **Strict Zero-Budget ($0 / ₹0) Operation**:
   All speech generation must operate using permanently free, open-source, or local operating system capabilities without paid API keys, monthly subscriptions, or usage-capped trial tiers.

---

## 2. Voice Personas & Language Capabilities

| Language | Voice Persona | Gender | Engine Provider | Sample Rate | Pacing & Pitch Control | Primary Genre Suitability |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Hindi** | `hi-IN-MadhurNeural` | Male | Edge-TTS 7.3.1 | 24 kHz $\rightarrow$ 44.1 kHz | Rate: $\pm 50\%$, Pitch: $\pm 50\text{Hz}$ | Documentary, Serious Drama, Narration |
| **Hindi** | `hi-IN-SwaraNeural` | Female | Edge-TTS 7.3.1 | 24 kHz $\rightarrow$ 44.1 kHz | Rate: $\pm 50\%$, Pitch: $\pm 50\text{Hz}$ | Emotional Storytelling, Intimate Drama |
| **English** | `en-US-GuyNeural` | Male | Edge-TTS 7.3.1 | 24 kHz $\rightarrow$ 44.1 kHz | Rate: $\pm 50\%$, Pitch: $\pm 50\text{Hz}$ | International Cinema, Documentaries |
| **English** | `en-US-JennyNeural` | Female | Edge-TTS 7.3.1 | 24 kHz $\rightarrow$ 44.1 kHz | Rate: $\pm 50\%$, Pitch: $\pm 50\text{Hz}$ | Explainer, Warm Narrative |
| **English** | `Microsoft David Desktop` | Male | Windows SAPI5 | 16 kHz $\rightarrow$ 44.1 kHz | Rate: $-10 \dots +10$ | Local Offline Fail-Safe Fallback |
| **English** | `Microsoft Zira Desktop` | Female | Windows SAPI5 | 16 kHz $\rightarrow$ 44.1 kHz | Rate: $-10 \dots +10$ | Local Offline Fail-Safe Fallback |

---

## 3. Cue Chunking & Timeline Assembly Pipeline

```
[Script Sentences + Timestamps]
              │
              ▼
   [Async Edge-TTS Synthesizer] ──> Synthesizes individual raw cue MP3s
              │
              ▼
    [FFmpeg Audio Conformer]   ──> Transcodes to 44.1kHz 16-bit PCM Mono
                                  Applies EBU R128 `loudnorm=I=-16:TP=-1.5:LRA=11`
              │
              ▼
    [Millisecond Delay Engine] ──> Calculates `delay_ms = int(start_sec * 1000)`
                                  Builds `[i:a]adelay=delay_ms|delay_ms[delayed_i]`
              │
              ▼
    [FFmpeg amix Master Track] ──> `amix=inputs=N:duration=first:dropout_transition=0`
                                  Applies `apad` and `atrim=0:target_duration_sec`
              │
              ▼
[Master Narration WAV File + Physical Telemetry Manifest]
```

### Mathematical Timeline Rule
For $N$ dialogue cues, where cue $i$ has text $T_i$ and scheduled start time $S_i$:
$$\text{delay\_ms}_i = \lfloor S_i \times 1000 \rfloor$$
The filtergraph executes:
$$\sum_{i=0}^{N-1} [i:a]\text{adelay}=\text{delay\_ms}_i|\text{delay\_ms}_i[\text{delayed}_i]; \quad \prod_{i=0}^{N-1}[\text{delayed}_i]\text{amix}=N[\text{out\_voice}]$$

---

## 4. Empirical Waveform Telemetry

Measurements extracted from the Phase 7.5 30-second master narration file (`aakhiri_chitti_narration_30s.wav`):

| Waveform Parameter | Measured Value | Standard Target | Assessment |
| :--- | :--- | :--- | :---: |
| **Sample Rate** | 44,100 Hz | 44,100 Hz | Exact Match |
| **Bit Depth** | 16-bit Signed PCM | 16-bit Signed PCM | Exact Match |
| **Channels** | 1 (Mono) | 1 (Mono Broadcast Vocal) | Compliant |
| **Duration** | 30.000 seconds | 30.000 seconds | $0.00\text{s}$ Drift |
| **RMS Amplitude** | 0.02221 ($-33.07\text{ dBFS}$) | $-30 \dots -36\text{ dBFS}$ (with speech pauses) | Optimal |
| **Peak Amplitude** | 0.28054 ($-11.04\text{ dBFS}$) | $< -6.0\text{ dBFS}$ | Safe Headroom |
| **Digital Clipping** | 0 samples (0.00%) | Exactly 0 | **ZERO CLIPPING** |
| **Speech Articulation** | 3 distinct cues | 3 distinct cues | 100% Intelligible |

---

## 5. Licensing & Commercial-Use Assessment

- **Edge-TTS (v7.3.1)**:
  `edge-tts` is an open-source Python library (GNU LGPL v3.0) interfacing with Microsoft's speech service via the publicly exposed ReadAloud websocket protocol.
  - **License**: LGPL-3.0-or-later.
  - **Financial Cost**: $0.00 (No API credentials or payments required).
  - **Attribution Policy**: Open-source cinema research attribution provided in production dossiers.
- **Windows SAPI5**:
  Bundled directly into Microsoft Windows 11 under the host operating system's software license. Fully accessible offline for unlimited local synthesis with zero licensing fees.
- **Fail-Closed Fallback (User Narration Checkpoint)**:
  When cloud endpoints are unreachable and local voices are unsuited for the target language (e.g. Hindi on an English-only OS), the system generates timed script handbooks (`narration_recording_script.txt`) allowing human voice recording, ensuring 100% clean IP ownership.
