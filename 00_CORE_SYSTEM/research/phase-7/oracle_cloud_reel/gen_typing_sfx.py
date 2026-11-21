import numpy as np
import soundfile as sf
import os

sfx_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\sfx"
os.makedirs(sfx_dir, exist_ok=True)
sr = 44100

def gen_typing_loop(fname, duration_s=4.0):
    total_samples = int(duration_s * sr)
    audio = np.zeros(total_samples, dtype=np.float32)
    
    # Generate random key click bursts (roughly 8-10 clicks per second)
    num_clicks = int(duration_s * 9)
    click_times = np.sort(np.random.uniform(0.1, duration_s - 0.2, num_clicks))
    
    for ct in click_times:
        start_idx = int(ct * sr)
        click_len = int(0.025 * sr) # 25ms click
        t = np.linspace(0, 0.025, click_len, False)
        # Click sound: damped high frequency burst + low thud
        freq = np.random.uniform(2500, 4500)
        env = np.exp(-t * 250)
        click = (np.sin(2 * np.pi * freq * t) * 0.4 + np.sin(2 * np.pi * 300 * t) * 0.6) * env * 0.25
        end_idx = min(total_samples, start_idx + click_len)
        audio[start_idx:end_idx] += click[:end_idx - start_idx]
        
    sf.write(os.path.join(sfx_dir, fname), audio, sr)
    print("Saved typing.wav SFX")

gen_typing_loop("typing.wav", duration_s=5.0)
