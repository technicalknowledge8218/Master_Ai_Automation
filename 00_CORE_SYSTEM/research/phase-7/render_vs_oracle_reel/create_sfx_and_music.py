import os
import math
import numpy as np
import soundfile as sf

sfx_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\render_vs_oracle_reel\sfx"
os.makedirs(sfx_dir, exist_ok=True)
sr = 44100

# 1. Pop Sound (for bullet points / cards popping in)
t_pop = np.linspace(0, 0.08, int(sr * 0.08), endpoint=False)
freq_pop = np.linspace(600, 1400, len(t_pop))
phase_pop = 2 * np.pi * np.cumsum(freq_pop) / sr
env_pop = np.exp(-t_pop * 45)
pop = np.sin(phase_pop) * env_pop * 0.7
sf.write(os.path.join(sfx_dir, "pop.wav"), pop.astype(np.float32), sr)

# 2. Ding / Success Chime (for Oracle 24GB monster specs)
t_ding = np.linspace(0, 0.6, int(sr * 0.6), endpoint=False)
env_ding = np.exp(-t_ding * 6)
ding = (0.6 * np.sin(2 * np.pi * 1046.5 * t_ding) + 0.4 * np.sin(2 * np.pi * 2093.0 * t_ding)) * env_ding * 0.6
sf.write(os.path.join(sfx_dir, "ding.wav"), ding.astype(np.float32), sr)

# 3. Whoosh Sound (for scene transitions)
t_whoosh = np.linspace(0, 0.25, int(sr * 0.25), endpoint=False)
noise = np.random.uniform(-1, 1, len(t_whoosh))
env_whoosh = np.sin(np.pi * t_whoosh / 0.25) ** 2
# Simple low-pass filter by moving average
whoosh = np.convolve(noise, np.ones(25)/25, mode='same') * env_whoosh * 0.5
sf.write(os.path.join(sfx_dir, "whoosh.wav"), whoosh.astype(np.float32), sr)

# 4. Error Buzz (for 15-min sleep / cold start trap)
t_buzz = np.linspace(0, 0.22, int(sr * 0.22), endpoint=False)
buzz = (0.5 * np.sign(np.sin(2 * np.pi * 140 * t_buzz)) + 0.3 * np.sign(np.sin(2 * np.pi * 210 * t_buzz))) * np.exp(-t_buzz * 4) * 0.4
sf.write(os.path.join(sfx_dir, "buzz.wav"), buzz.astype(np.float32), sr)

# 5. Upbeat Lo-fi Background Beat (82 BPM, subtle Rhodes + kick/snare groove)
duration_bg = 60.0
total_samples = int(sr * duration_bg)
t_total = np.linspace(0, duration_bg, total_samples, endpoint=False)
bpm = 85
beat_interval = 60.0 / bpm # ~0.705s

bg_track = np.zeros(total_samples, dtype=np.float32)

# Generate repeating kick, snare, and warm chord swell
for beat in range(int(duration_bg / beat_interval)):
    beat_t = beat * beat_interval
    sample_idx = int(beat_t * sr)
    if sample_idx >= total_samples:
        break
    
    # Kick on beats 0, 2 (sample_idx)
    if beat % 2 == 0:
        k_len = int(sr * 0.15)
        if sample_idx + k_len < total_samples:
            tk = np.linspace(0, 0.15, k_len, endpoint=False)
            freq_k = np.linspace(130, 45, k_len)
            kick = np.sin(2 * np.pi * np.cumsum(freq_k) / sr) * np.exp(-tk * 20) * 0.35
            bg_track[sample_idx:sample_idx+k_len] += kick
            
    # Soft snare / clap on beats 1, 3
    else:
        s_len = int(sr * 0.12)
        if sample_idx + s_len < total_samples:
            ts = np.linspace(0, 0.12, s_len, endpoint=False)
            snare_noise = np.random.uniform(-0.15, 0.15, s_len) * np.exp(-ts * 25)
            snare_tone = np.sin(2 * np.pi * 220 * ts) * np.exp(-ts * 30) * 0.15
            bg_track[sample_idx:sample_idx+s_len] += (snare_noise + snare_tone)

# Add warm lofi chord pad (Cmaj7 -> Am7)
f_c = 261.63 # C4
f_e = 329.63 # E4
f_g = 392.00 # G4
f_b = 493.88 # B4
pad = 0.04 * (np.sin(2 * np.pi * f_c * t_total) + 
              np.sin(2 * np.pi * f_e * t_total) + 
              np.sin(2 * np.pi * f_g * t_total) + 
              np.sin(2 * np.pi * f_b * t_total))
bg_track += pad

# Normalize bg music to pleasant background level (-22dB)
bg_max = np.max(np.abs(bg_track))
if bg_max > 0:
    bg_track = (bg_track / bg_max) * 0.12 # low background level

sf.write(os.path.join(sfx_dir, "lofi_bg_track.wav"), bg_track.astype(np.float32), sr)
print("Synthesized SFX (pop, ding, whoosh, buzz) and Lo-fi Background Track!")
