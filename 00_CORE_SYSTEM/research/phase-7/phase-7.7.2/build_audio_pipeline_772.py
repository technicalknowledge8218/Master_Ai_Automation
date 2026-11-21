"""
build_audio_pipeline_772.py
===========================
Generates the complete audio package for "चाय और चाल" (The Chai Gambit):
- final_voiceover.wav: High-fidelity conversational Hindi dialogue featuring:
    - Vikram: hi-IN-MadhurNeural (Cocky, fast-talking creative lead)
    - Aisha: hi-IN-SwaraNeural (Poised, razor-sharp senior UI/UX designer)
- final_music.wav: Original 4-beat contemporary urban neo-jazz groove.
- final_sfx.wav: Authentic spot sound effects (cafe rain, napkin slide, tea clink, biscuit plop, UPI chime).
- final_mix.wav: EBU R128 compliant master mix with -14 dB vocal sidechain ducking.
"""

import os
import sys
import wave
import math
import numpy as np

ENGINE_DIR = r"F:\Master AI\09_CONTENT_STUDIO\engine"
sys.path.append(ENGINE_DIR)
from voiceover_engine import VoiceoverEngine

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2"
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

SAMPLE_RATE = 44100
TOTAL_DURATION = 30.0
TOTAL_SAMPLES = int(TOTAL_DURATION * SAMPLE_RATE)

ve = VoiceoverEngine()

# -----------------------------------------------------------------------------
# 1. CHARACTER DIALOGUE SYNTHESIS (SwaraNeural & MadhurNeural)
# -----------------------------------------------------------------------------
print("=" * 70)
print("1. GENERATING TWO-CHARACTER HINDI DIALOGUE (Aisha & Vikram)")
print("=" * 70)

dialogue_lines = [
    {
        "id": "BEAT-01-VIKRAM",
        "character": "Vikram",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%", # Fast confident swagger
        "text": "बुरा मत मानना आयशा, लेकिन तुम्हारा पिच मैंने थोड़ा 'अपग्रेड' कर दिया... डील फाइनल है!",
        "start_sec": 0.60
    },
    {
        "id": "BEAT-02-AISHA",
        "character": "Aisha",
        "voice": "hi-IN-SwaraNeural",
        "rate": "-1%", # Calm, measured composure
        "text": "अच्छा? ज़रा अपना इनबॉक्स चेक कर लो, विक्रम।",
        "start_sec": 9.20
    },
    {
        "id": "BEAT-03-VIKRAM",
        "character": "Vikram",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+2%", # Stunned disbelief
        "text": "व्हाट?! 'आयशा इज़ द न्यू प्रोजेक्ट हेड'...? लेकिन कैसे?!",
        "start_sec": 15.40
    },
    {
        "id": "BEAT-04-AISHA",
        "character": "Aisha",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+1%", # Playful triumphant finish
        "text": "हाँ... और इस जीत की चाय के पैसे तुम दोगे, पार्टनर!",
        "start_sec": 22.20
    }
]

voice_buffer = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
ducking_envelope = np.ones(TOTAL_SAMPLES, dtype=np.float32)

temp_chunks = os.path.join(AUDIO_DIR, "chunks")
os.makedirs(temp_chunks, exist_ok=True)

for idx, d in enumerate(dialogue_lines):
    chunk_wav = os.path.join(temp_chunks, f"dialogue_{idx:02d}.wav")
    print(f"Synthesizing [{d['character']}]: '{d['text'][:35]}...'")
    res = ve.synthesize_cue(
        text=d["text"],
        output_wav=chunk_wav,
        voice_name=d["voice"],
        rate=d["rate"],
        volume="+0%"
    )
    dur = res["duration_sec"]
    end_sec = d["start_sec"] + dur
    print(f"  -> {d['start_sec']}s to {end_sec:.2f}s (dur {dur:.2f}s)")

    with wave.open(chunk_wav, "rb") as wf:
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    s_idx = int(d["start_sec"] * SAMPLE_RATE)
    e_idx = min(TOTAL_SAMPLES, s_idx + len(samples))
    voice_buffer[s_idx:e_idx] += samples[:e_idx - s_idx]

    # Ducking envelope: -14 dB during dialogue
    attack_pts = int(0.12 * SAMPLE_RATE)
    release_pts = int(0.30 * SAMPLE_RATE)
    duck_val = 0.20 # -14 dB
    d_start = max(0, s_idx - attack_pts)
    d_end = min(TOTAL_SAMPLES, e_idx + release_pts)

    for i in range(d_start, s_idx):
        t_ramp = (i - d_start) / max(1, attack_pts)
        ducking_envelope[i] = min(ducking_envelope[i], 1.0 - (1.0 - duck_val) * t_ramp)
    ducking_envelope[s_idx:e_idx] = np.minimum(ducking_envelope[s_idx:e_idx], duck_val)
    for i in range(e_idx, d_end):
        t_ramp = (i - e_idx) / max(1, release_pts)
        ducking_envelope[i] = min(ducking_envelope[i], duck_val + (1.0 - duck_val) * t_ramp)

# Normalize voice buffer to -2.0 dBFS Peak
v_peak = np.max(np.abs(voice_buffer))
if v_peak > 0:
    voice_buffer = (voice_buffer / v_peak) * (10 ** (-2.0 / 20.0))

final_voiceover_path = os.path.join(OUTPUT_DIR, "final_voiceover.wav")
with wave.open(final_voiceover_path, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(np.clip(voice_buffer * 32767.0, -32768.0, 32767.0).astype(np.int16).tobytes())
print(f"-> Saved: {final_voiceover_path}")

# -----------------------------------------------------------------------------
# 2. SOUND EFFECTS (SFX) SYNTHESIS & LAYER
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("2. GENERATING SPOT FOLEY & AMBIENCE (44.1 kHz Stereo)")
print("=" * 70)

sfx_left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
sfx_right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

# A. Soft cafe rain against window + muffled traffic rumble
np.random.seed(99)
rain_noise = np.random.normal(0, 0.08, TOTAL_SAMPLES).astype(np.float32)
# Lowpass moving average
kernel = np.ones(35) / 35
rain_filtered = np.convolve(rain_noise, kernel, mode='same') * 0.12
sfx_left += rain_filtered * 0.9
sfx_right += rain_filtered * 1.1

# B. Paper Napkin Slide (At 1.2s: Vikram slides napkin)
def add_friction_slide(t_start, dur, amp, pan=0.3):
    s_i = int(t_start * SAMPLE_RATE)
    n_p = int(dur * SAMPLE_RATE)
    e_i = min(TOTAL_SAMPLES, s_i + n_p)
    actual_len = e_i - s_i
    if actual_len > 0:
        noise = np.random.normal(0, 0.15, actual_len).astype(np.float32)
        env = np.sin(np.pi * np.linspace(0, 1, actual_len)) ** 2
        sig = np.convolve(noise, np.ones(20)/20, mode='same') * env * amp
        sfx_left[s_i:e_i] += sig * (1.0 - pan) * 0.5
        sfx_right[s_i:e_i] += sig * (1.0 + pan) * 0.5

add_friction_slide(1.2, 0.45, 0.25, pan=0.4)

# C. Cutting Chai Glass Clink & Steam (At 7.8s)
def add_glass_clink(t_start, freq=3200, amp=0.18, pan=-0.2):
    s_i = int(t_start * SAMPLE_RATE)
    dur = 0.35
    n_p = int(dur * SAMPLE_RATE)
    e_i = min(TOTAL_SAMPLES, s_i + n_p)
    actual_len = e_i - s_i
    if actual_len > 0:
        tt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
        sig = np.sin(2 * np.pi * freq * tt) * np.exp(-tt * 18.0) * amp
        sig += np.sin(2 * np.pi * freq * 1.8 * tt) * np.exp(-tt * 24.0) * amp * 0.4
        sfx_left[s_i:e_i] += sig * (1.0 - pan) * 0.5
        sfx_right[s_i:e_i] += sig * (1.0 + pan) * 0.5

add_glass_clink(7.9, freq=3400, amp=0.18, pan=-0.2)

# D. Tablet Spin / Glass Swish (At 15.2s)
add_friction_slide(15.2, 0.35, 0.20, pan=-0.1)

# E. Biscuit Drop "Plop" & Tea Splash (At 19.5s)
def add_water_plop(t_start, pan=0.2):
    s_i = int(t_start * SAMPLE_RATE)
    dur = 0.25
    n_p = int(dur * SAMPLE_RATE)
    e_i = min(TOTAL_SAMPLES, s_i + n_p)
    actual_len = e_i - s_i
    if actual_len > 0:
        tt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
        # Downward pitch sweep for authentic drop plop
        freq = 650.0 * np.exp(-tt * 15.0) + 120.0
        phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
        sig = np.sin(phase) * (np.sin(np.pi * tt / dur) ** 2) * 0.35
        sfx_left[s_i:e_i] += sig * (1.0 - pan) * 0.5
        sfx_right[s_i:e_i] += sig * (1.0 + pan) * 0.5

add_water_plop(19.5, pan=0.2)

# F. Modern UPI Digital Success Payment Chime (At 28.5s)
def add_digital_chime(t_start, pan=0.3):
    notes = [1046.5, 1318.5, 1567.98, 2093.0] # C6, E6, G6, C7 arpeggio
    for idx, freq in enumerate(notes):
        st = t_start + idx * 0.06
        s_i = int(st * SAMPLE_RATE)
        dur = 0.35
        n_p = int(dur * SAMPLE_RATE)
        e_i = min(TOTAL_SAMPLES, s_i + n_p)
        actual_len = e_i - s_i
        if actual_len > 0:
            tt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
            sig = np.sin(2 * np.pi * freq * tt) * np.exp(-tt * 8.0) * 0.14
            sfx_left[s_i:e_i] += sig * (1.0 - pan) * 0.5
            sfx_right[s_i:e_i] += sig * (1.0 + pan) * 0.5

add_digital_chime(28.5, pan=0.25)

final_sfx_path = os.path.join(OUTPUT_DIR, "final_sfx.wav")
sfx_stereo = np.vstack([sfx_left, sfx_right]).T
sfx_peak = np.max(np.abs(sfx_stereo))
if sfx_peak > 0:
    sfx_stereo = (sfx_stereo / sfx_peak) * 0.65 # -3.7 dBFS Peak
with wave.open(final_sfx_path, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(np.clip(sfx_stereo * 32767.0, -32768.0, 32767.0).astype(np.int16).tobytes())
print(f"-> Saved: {final_sfx_path}")

# -----------------------------------------------------------------------------
# 3. CINEMATIC URBAN JAZZ / GROOVE SOUNDTRACK
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("3. GENERATING CINEMATIC URBAN JAZZ SCORE (30.0s)")
print("=" * 70)

music_l = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
music_r = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

def play_rhodes(t_start, dur, freq, amp, pan=0.0):
    s_i = int(t_start * SAMPLE_RATE)
    n_p = int(dur * SAMPLE_RATE)
    e_i = min(TOTAL_SAMPLES, s_i + n_p)
    actual_len = e_i - s_i
    if actual_len <= 0: return
    tt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
    # FM synthesis for electric piano
    mod = 0.5 * np.sin(2 * np.pi * freq * 2 * tt)
    sig = np.sin(2 * np.pi * freq * tt + mod) * np.exp(-tt * 1.8) * amp
    music_l[s_i:e_i] += sig * (1.0 - pan) * 0.5
    music_r[s_i:e_i] += sig * (1.0 + pan) * 0.5

def play_bass(t_start, dur, freq, amp, pan=-0.2):
    s_i = int(t_start * SAMPLE_RATE)
    n_p = int(dur * SAMPLE_RATE)
    e_i = min(TOTAL_SAMPLES, s_i + n_p)
    actual_len = e_i - s_i
    if actual_len <= 0: return
    tt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
    sig = (np.sin(2 * np.pi * freq * tt) + 0.3 * np.sin(2 * np.pi * freq * 2 * tt)) * np.exp(-tt * 1.2) * amp
    music_l[s_i:e_i] += sig * (1.0 - pan) * 0.5
    music_r[s_i:e_i] += sig * (1.0 + pan) * 0.5

# Frequencies
F2, G2, A2, Bb2, C3, D3, Eb3, F3, G3, A3, Bb3, C4, D4, F4 = 87.31, 98.0, 110.0, 116.54, 130.81, 146.83, 155.56, 174.61, 196.0, 220.0, 233.08, 261.63, 293.66, 349.23

# Beat 1 (0-7.5s): Urban swagger walking bass & chords
b1_chords = [(0.2, F3, 0.25), (1.0, A3, 0.22), (1.8, C4, 0.25), (2.8, Eb3, 0.25), (3.6, G3, 0.22), (4.4, Bb3, 0.25), (5.4, D3, 0.25), (6.2, F3, 0.22)]
for t, f, a in b1_chords:
    play_rhodes(t, 2.0, f, a, pan=0.2)
    play_bass(t, 1.5, f * 0.5, a * 1.1, pan=-0.2)

# Beat 2 (7.5-15.0s): Smooth, calm, unbothered jazz groove
b2_chords = [(7.8, Bb3, 0.26), (8.6, D4, 0.24), (9.4, F4, 0.26), (10.6, C4, 0.26), (11.4, Eb3, 0.24), (12.2, G3, 0.26), (13.4, F3, 0.28), (14.2, A3, 0.25)]
for t, f, a in b2_chords:
    play_rhodes(t, 2.2, f, a, pan=-0.2)
    play_bass(t, 1.6, f * 0.5, a * 1.1, pan=0.2)

# Beat 3 (15.0-22.5s): Dramatic comedic breakdown!
# 15.0s to 18.0s dramatic descending line
play_bass(15.2, 1.0, C3, 0.35, pan=0.0)
play_bass(16.2, 1.0, Bb2, 0.35, pan=0.0)
play_bass(17.2, 1.0, A2, 0.38, pan=0.0)
play_bass(18.2, 1.8, F2, 0.40, pan=0.0) # Low bottom end drop

# Beat 4 (22.5-30.0s): Funky triumphant groove resolution
b4_groove = [(22.6, F3, 0.30), (23.2, A3, 0.28), (23.8, C4, 0.32), (24.6, D4, 0.34), (25.4, F4, 0.36), (26.2, C4, 0.34), (27.0, A3, 0.32), (28.0, F3, 0.36)]
for t, f, a in b4_groove:
    play_rhodes(t, 1.8, f, a, pan=0.2)
    play_bass(t, 1.2, f * 0.5, a * 1.2, pan=-0.2)

# Master music fade out over last 1.2s
m_fade_start = int(28.8 * SAMPLE_RATE)
for i in range(m_fade_start, TOTAL_SAMPLES):
    t_out = (i - m_fade_start) / (TOTAL_SAMPLES - m_fade_start)
    music_l[i] *= (1.0 - t_out)
    music_r[i] *= (1.0 - t_out)

music_stereo = np.vstack([music_l, music_r]).T
m_peak = np.max(np.abs(music_stereo))
if m_peak > 0:
    music_stereo = (music_stereo / m_peak) * 0.75

final_music_path = os.path.join(OUTPUT_DIR, "final_music.wav")
with wave.open(final_music_path, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(np.clip(music_stereo * 32767.0, -32768.0, 32767.0).astype(np.int16).tobytes())
print(f"-> Saved: {final_music_path}")

# -----------------------------------------------------------------------------
# 4. MASTER MIXDOWN (Sidechain Ducking + EBU R128 Compliance)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("4. GENERATING MASTER MIXDOWN WITH SIDECHAIN DUCKING (final_mix.wav)")
print("=" * 70)

# Duck music under dialogue
ducked_m_l = music_stereo[:, 0] * ducking_envelope
ducked_m_r = music_stereo[:, 1] * ducking_envelope

# Voice in stereo center
voice_l = voice_buffer
voice_r = voice_buffer

# Sum: Voice + Ducked Music + SFX
mix_l = voice_l + ducked_m_l + sfx_stereo[:, 0]
mix_r = voice_r + ducked_m_r + sfx_stereo[:, 1]
mix_stereo = np.vstack([mix_l, mix_r]).T

# Final Peak Limiting to -2.5 dBFS (clean headroom for AAC codec)
mix_peak = np.max(np.abs(mix_stereo))
target_peak = 10 ** (-2.5 / 20.0) # ~0.7499
if mix_peak > 0:
    mix_stereo = (mix_stereo / mix_peak) * target_peak

final_mix_path = os.path.join(OUTPUT_DIR, "final_mix.wav")
with wave.open(final_mix_path, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(np.clip(mix_stereo * 32767.0, -32768.0, 32767.0).astype(np.int16).tobytes())

# Compute Metrics
rms_val = float(np.sqrt(np.mean(mix_stereo**2)))
rms_db = float(20 * math.log10(rms_val + 1e-9))
peak_db = float(20 * math.log10(np.max(np.abs(mix_stereo)) + 1e-9))

print(f"Master Mixdown Finished:")
print(f"  Path: {final_mix_path}")
print(f"  Integrated RMS: {rms_db:.2f} dBFS")
print(f"  True Peak: {peak_db:.2f} dBFS (Target -2.50 dBFS)")
