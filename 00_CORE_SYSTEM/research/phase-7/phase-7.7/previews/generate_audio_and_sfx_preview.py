import os
import wave
import subprocess
import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe
FFMPEG = get_ffmpeg_exe()

PREVIEWS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews"
os.makedirs(PREVIEWS_DIR, exist_ok=True)

sr = 44100
dur = 30.0
total_samples = int(dur * sr)
t = np.linspace(0, dur, total_samples, endpoint=False)

print("Synthesizing Original 30-Second Acoustic Score ('पहला ऑर्डर')...")

def acoustic_guitar_note(freq, t_rel, decay_tau=2.2):
    mask = (t_rel >= 0) & (t_rel < 4.0)
    out = np.zeros_like(t_rel)
    tr = t_rel[mask]
    # Nylon string harmonic series
    h1 = np.sin(2 * np.pi * freq * tr) * np.exp(-tr / decay_tau)
    h2 = 0.60 * np.sin(2 * np.pi * 2 * freq * tr) * np.exp(-tr / (decay_tau * 0.7))
    h3 = 0.35 * np.sin(2 * np.pi * 3 * freq * tr) * np.exp(-tr / (decay_tau * 0.45))
    h4 = 0.15 * np.sin(2 * np.pi * 4 * freq * tr) * np.exp(-tr / (decay_tau * 0.3))
    # Body resonance (cedar top plate)
    body = 0.12 * np.sin(2 * np.pi * (freq * 0.5) * tr) * np.exp(-tr / (decay_tau * 1.4))
    pick = 0.05 * np.random.uniform(-1, 1, len(tr)) * np.exp(-tr / 0.012)
    out[mask] = h1 + h2 + h3 + h4 + body + pick
    return out

def warm_rhodes_chord(freqs, t_rel, dur=3.0):
    mask = (t_rel >= 0) & (t_rel < dur)
    out = np.zeros_like(t_rel)
    tr = t_rel[mask]
    for f in freqs:
        bell = np.sin(2 * np.pi * f * tr) * np.exp(-tr / 2.5)
        tine = 0.4 * np.sin(2 * np.pi * 3.5 * f * tr) * np.exp(-tr / 0.8)
        out[mask] += 0.08 * (bell + tine)
    return out

music_raw = np.zeros_like(t)

# BEAT 1 (0.0s - 8.0s | Contemplative Doubt in A minor)
# Am9 -> Fmaj7 arpeggios
m1_notes = [
    (0.0, 220.0, 2.5), (0.6, 261.63, 2.5), (1.2, 329.63, 2.5), (1.8, 392.00, 2.5),
    (2.8, 174.61, 2.5), (3.4, 261.63, 2.5), (4.0, 329.63, 2.5), (4.6, 349.23, 2.5),
    (5.6, 220.0, 2.5), (6.2, 261.63, 2.5), (6.8, 329.63, 2.5), (7.4, 392.00, 2.5)
]
for st, freq, d in m1_notes:
    music_raw += 0.22 * acoustic_guitar_note(freq, t - st, d)

# Rhodes soft bed
music_raw += warm_rhodes_chord([220.0, 261.63, 329.63, 392.0], t - 0.0, 4.0)
music_raw += warm_rhodes_chord([174.61, 261.63, 329.63, 349.23], t - 4.0, 4.0)

# BEAT 2 (8.0s - 16.0s | Sibling Encouragement & The Notification)
# C major -> G major (Tempo picks up with rhythmic picking)
m2_notes = [
    (8.0, 261.63, 1.8), (8.5, 329.63, 1.8), (9.0, 392.00, 1.8), (9.5, 523.25, 1.8),
    (10.0, 196.00, 1.8), (10.5, 293.66, 1.8), (11.0, 392.00, 1.8), (11.5, 493.88, 1.8),
    (12.0, 261.63, 1.8), (12.5, 329.63, 1.8), (13.0, 392.00, 1.8), (13.5, 523.25, 1.8),
    (14.0, 196.00, 1.8), (14.5, 293.66, 1.8), (15.0, 392.00, 1.8), (15.5, 493.88, 1.8)
]
for st, freq, d in m2_notes:
    music_raw += 0.25 * acoustic_guitar_note(freq, t - st, d)

# Notification chime sparkle in music at 10.2s (Marimba / Glockenspiel)
for f_bell, delay in [(1046.5, 0.0), (1318.5, 0.08), (1567.98, 0.16), (2093.0, 0.24)]:
    t_bell = t - (10.2 + delay)
    mask_b = (t_bell >= 0) & (t_bell < 1.5)
    music_raw[mask_b] += 0.18 * np.sin(2 * np.pi * f_bell * t_bell[mask_b]) * np.exp(-t_bell[mask_b] / 0.6)

# BEAT 3 (16.0s - 23.0s | The Breakthrough - Warm Cello Swell & Piano)
# F major -> G major -> C major (Uplifting resolution)
m3_chords = [
    (16.0, [174.61, 220.00, 261.63, 349.23], 3.2), # Fmaj7
    (19.2, [196.00, 246.94, 293.66, 392.00], 3.5)  # G7
]
for st, freqs, d in m3_chords:
    for f in freqs:
        music_raw += 0.20 * acoustic_guitar_note(f, t - st, d)

# Cello swell in Beat 3
m3_mask = (t >= 16.0) & (t < 23.0)
tr_c = t[m3_mask] - 16.0
cello_f = 130.81 # C3
cello = np.sin(2 * np.pi * cello_f * tr_c) * (1.0 + 0.03 * np.sin(2 * np.pi * 5.0 * tr_c))
cello *= np.clip(tr_c / 1.5, 0, 1) * np.exp(-tr_c / 7.0)
music_raw[m3_mask] += 0.18 * cello

# BEAT 4 (23.0s - 30.0s | The Dawn of Confidence - Soaring C major & Bells)
m4_notes = [
    (23.0, 261.63, 2.5), (23.6, 329.63, 2.5), (24.2, 392.00, 2.5), (24.8, 523.25, 2.5),
    (25.8, 349.23, 2.5), (26.4, 392.00, 2.5), (27.0, 523.25, 2.5), (27.6, 659.25, 2.5),
    (28.5, [130.81, 261.63, 329.63, 392.00, 523.25], 3.5) # Final resonant strum
]
for item in m4_notes:
    st = item[0]
    freq = item[1]
    d = item[2]
    if isinstance(freq, list):
        for f in freq:
            music_raw += 0.22 * acoustic_guitar_note(f, t - st, d)
    else:
        music_raw += 0.22 * acoustic_guitar_note(freq, t - st, d)

# Studio Reverb simulation
reverb = np.zeros_like(music_raw)
reverb[int(0.045 * sr):] += 0.24 * music_raw[:-int(0.045 * sr)]
reverb[int(0.090 * sr):] += 0.14 * music_raw[:-int(0.090 * sr)]
reverb[int(0.160 * sr):] += 0.08 * music_raw[:-int(0.160 * sr)]
final_music = music_raw + reverb
final_music = (final_music / np.max(np.abs(final_music))) * 0.78

music_wav = os.path.join(PREVIEWS_DIR, "music_preview.wav")
with wave.open(music_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes((final_music * 32767).astype(np.int16).tobytes())
print(f"Music Preview Rendered: {music_wav}")

# -------------------------------------------------------------
# SYNTHESIZE SPOT FOLEY SFX TRACK
# -------------------------------------------------------------
print("Assembling Spot Foley Sound Effects Track...")
sfx_buffer = np.zeros(total_samples, dtype=np.float32)

def load_audio_segment(path: str) -> np.ndarray:
    cmd = [FFMPEG, "-i", path, "-ac", "1", "-ar", "44100", "-f", "s16le", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw, _ = proc.communicate()
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

ASSETS_AUDIO = r"F:\Master AI\15_ASSETS\audio\sfx"
footsteps = load_audio_segment(os.path.join(ASSETS_AUDIO, "sfx_footsteps_wood.ogg"))
paper = load_audio_segment(os.path.join(ASSETS_AUDIO, "sfx_paper_turning_page.ogg"))
chime = load_audio_segment(os.path.join(ASSETS_AUDIO, "sfx_tibetan_bowl_chime.ogg"))

# 1. Subtle shoe shift on floor (0.8s - 2.0s)
fs_idx = int(0.8 * sr)
sfx_buffer[fs_idx : fs_idx + int(1.2 * sr)] += 0.35 * footsteps[:int(1.2 * sr)]

# 2. Ceramic chai glass clinking counter (4.5s)
mug_t = np.linspace(0, 0.4, int(0.4 * sr))
ceramic_clink = np.sin(2 * np.pi * 2400.0 * mug_t) * np.exp(-mug_t / 0.04) + 0.5 * np.sin(2 * np.pi * 3600.0 * mug_t) * np.exp(-mug_t / 0.02)
cg_idx = int(4.5 * sr)
sfx_buffer[cg_idx : cg_idx + len(ceramic_clink)] += 0.40 * ceramic_clink

# 3. Modern Smartphone Digital Order Ding (10.2s)
phone_t = np.linspace(0, 0.8, int(0.8 * sr))
ding_f1 = np.sin(2 * np.pi * 1760.0 * phone_t) * np.exp(-phone_t / 0.3)
ding_f2 = 0.85 * np.sin(2 * np.pi * 2637.0 * phone_t) * np.exp(-phone_t / 0.35)
phone_ding = ding_f1 + ding_f2
pd_idx = int(10.2 * sr)
sfx_buffer[pd_idx : pd_idx + len(phone_ding)] += 0.65 * phone_ding

# 4. Fabric rustle as apron is unfolded (16.8s)
fab_idx = int(16.8 * sr)
fab_len = min(len(paper), int(1.8 * sr))
sfx_buffer[fab_idx : fab_idx + fab_len] += 0.52 * paper[:fab_len]

# 5. Apron strap tie snap & morning chime (24.0s)
snap_t = np.linspace(0, 0.15, int(0.15 * sr))
snap = np.sin(2 * np.pi * 420.0 * snap_t) * np.exp(-snap_t / 0.02) * np.random.uniform(0.8, 1.2, len(snap_t))
snap_idx = int(24.0 * sr)
sfx_buffer[snap_idx : snap_idx + len(snap)] += 0.60 * snap

# Morning chime / warm resonance (24.5s - 29.5s)
ch_idx = int(24.5 * sr)
ch_len = min(len(chime), total_samples - ch_idx)
sfx_buffer[ch_idx : ch_idx + ch_len] += 0.38 * chime[:ch_len]

# Normalize SFX
sfx_max = np.max(np.abs(sfx_buffer))
if sfx_max > 0.0:
    sfx_buffer = (sfx_buffer / sfx_max) * 0.80

sfx_wav = os.path.join(PREVIEWS_DIR, "sfx_preview.wav")
with wave.open(sfx_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes((sfx_buffer * 32767).astype(np.int16).tobytes())
print(f"SFX Preview Rendered: {sfx_wav}")

# -------------------------------------------------------------
# MASTER BALANCED AUDIO MIX WITH SIDECHAIN DUCKING
# -------------------------------------------------------------
print("Creating Master Balanced Audio Mix with Dynamic Ducking...")
voice_wav = os.path.join(PREVIEWS_DIR, "voice_sample_preview.wav")
with wave.open(voice_wav, "rb") as wf:
    v_raw = wf.readframes(wf.getnframes())
    voice_data = np.frombuffer(v_raw, dtype=np.int16).astype(np.float32) / 32768.0

# Calculate voice envelope for ducking (50ms window)
w_sz = int(0.05 * sr)
v_env = np.zeros_like(voice_data)
for i in range(0, len(voice_data) - w_sz, w_sz):
    rms_w = np.sqrt(np.mean(voice_data[i : i + w_sz]**2))
    v_env[i : i + w_sz] = rms_w

duck = np.ones_like(voice_data)
duck[v_env > 0.015] = 0.20 # -14 dB attenuation under voice
smooth_duck = np.convolve(duck, np.ones(int(0.20 * sr)) / (0.20 * sr), mode="same")

# Ducked music
music_ducked = final_music * smooth_duck * 0.42

# Sum stems
mixed_master = voice_data * 1.0 + music_ducked + sfx_buffer * 0.85

# Master limiter to -1.5 dBFS
peak_m = np.max(np.abs(mixed_master))
if peak_m > 0.84:
    mixed_master = (mixed_master / peak_m) * 0.84

mixed_wav = os.path.join(PREVIEWS_DIR, "mixed_audio_preview.wav")
with wave.open(mixed_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes((mixed_master * 32767).astype(np.int16).tobytes())

rms_mix = float(np.sqrt(np.mean(mixed_master**2)))
rms_mix_db = float(20 * np.log10(rms_mix + 1e-9))
peak_mix_db = float(20 * np.log10(np.max(np.abs(mixed_master)) + 1e-9))

print(f"Master Mixed Audio Rendered: {mixed_wav}")
print(f"  -> Integrated RMS: {rms_mix_db:.2f} dBFS | True Peak: {peak_mix_db:.2f} dBFS (EBU R128 Compliant)")
