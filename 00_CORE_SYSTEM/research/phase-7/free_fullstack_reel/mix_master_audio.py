import os
import numpy as np
import soundfile as sf
import imageio_ffmpeg
import subprocess

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
SFX_DIR = os.path.join(BASE_DIR, "sfx")
BGM_PATH = os.path.join(SFX_DIR, "lofi_bg_track.wav")
OUTPUT_AUDIO = os.path.join(AUDIO_DIR, "master_audio_track.wav")

SCENE_FILES = [
    "scene1_hook.wav",
    "scene2_frontend.wav",
    "scene3_backend.wav",
    "scene4_hack.wav",
    "scene5_cta.wav"
]

def load_wav(path, target_sr=44100):
    data, sr = sf.read(path)
    if data.ndim == 1:
        data = np.column_stack([data, data])
    elif data.shape[1] > 2:
        data = data[:, :2]
    # Simple resample if needed
    if sr != target_sr:
        num_samples = int(len(data) * target_sr / sr)
        indices = np.linspace(0, len(data) - 1, num_samples)
        data = np.column_stack([
            np.interp(indices, np.arange(len(data)), data[:, 0]),
            np.interp(indices, np.arange(len(data)), data[:, 1])
        ])
    return data

def main():
    sr = 44100
    scene_audios = []
    scene_durations = []
    scene_start_times = []
    
    current_time = 0.0
    for sf_name in SCENE_FILES:
        path = os.path.join(AUDIO_DIR, sf_name)
        audio = load_wav(path, sr)
        dur = len(audio) / sr
        scene_start_times.append(current_time)
        scene_durations.append(dur)
        scene_audios.append(audio)
        current_time += dur
    
    total_duration = current_time
    total_samples = int(total_duration * sr)
    print(f"Total Reel Duration: {total_duration:.2f}s ({total_samples} samples)")
    for i, (st, dur) in enumerate(zip(scene_start_times, scene_durations)):
        print(f"Scene {i+1}: Start = {st:.2f}s, Dur = {dur:.2f}s")
    
    # 1. Master Voice Track
    voice_track = np.zeros((total_samples, 2), dtype=np.float32)
    pos = 0
    for audio in scene_audios:
        l = len(audio)
        end = min(pos + l, total_samples)
        voice_track[pos:end] += audio[:end-pos]
        pos += l
        
    # 2. Master SFX Track
    sfx_track = np.zeros((total_samples, 2), dtype=np.float32)
    
    def add_sfx(sfx_name, start_t, volume=0.7):
        p = os.path.join(SFX_DIR, sfx_name)
        if not os.path.exists(p):
            print(f"SFX not found: {sfx_name}")
            return
        snd = load_wav(p, sr) * volume
        s_idx = int(start_t * sr)
        e_idx = min(s_idx + len(snd), total_samples)
        if s_idx < total_samples:
            sfx_track[s_idx:e_idx] += snd[:e_idx - s_idx]
            print(f"Added SFX {sfx_name} at t={start_t:.2f}s")

    # Add transition whooshes at scene boundaries
    for st in scene_start_times:
        add_sfx("whoosh.wav", st, volume=0.55)
        
    # Add scene-specific SFX
    add_sfx("alarm.wav", 1.2, volume=0.45)           # Scene 1 cold start warning
    add_sfx("ding.wav", scene_start_times[1] + 1.2, volume=0.5)     # Scene 2 Cloudflare Pages reveal
    # Scene 3: Terminal typing bursts
    t3 = scene_start_times[2]
    for click_t in [t3 + 2.0, t3 + 3.2, t3 + 4.5, t3 + 6.0, t3 + 7.5]:
        add_sfx("typing.wav", click_t, volume=0.5)
    add_sfx("pop.wav", t3 + 8.5, volume=0.5)         # Deploy success pop
    
    # Scene 4: Cost comparison chime
    t4 = scene_start_times[3]
    add_sfx("chime.wav", t4 + 3.0, volume=0.6)       # $0 Lifetime chime
    
    # Scene 5: CTA pop
    t5 = scene_start_times[4]
    add_sfx("pop.wav", t5 + 2.0, volume=0.6)         # Comment STACK pop

    # 3. Master BGM Track with Side-chain ducking (-18dB during voiceover)
    bgm_track = np.zeros((total_samples, 2), dtype=np.float32)
    if os.path.exists(BGM_PATH):
        raw_bgm = load_wav(BGM_PATH, sr)
        # Loop BGM to cover total duration
        loops = int(np.ceil(total_samples / len(raw_bgm)))
        tiled_bgm = np.tile(raw_bgm, (loops, 1))[:total_samples]
        
        # Calculate voice envelope for sidechain ducking
        voice_mono = np.abs(voice_track).mean(axis=1)
        # Smooth window: 0.15s
        win = int(0.15 * sr)
        envelope = np.convolve(voice_mono, np.ones(win)/win, mode='same')
        
        # Ducking multiplier: when voice is present, BGM is at 0.12 (-18dB), when silent, BGM is at 0.35
        duck_factor = np.where(envelope > 0.02, 0.12, 0.35)
        bgm_track = tiled_bgm * duck_factor[:, np.newaxis]
        print("BGM loaded and ducked successfully.")
        
    # 4. Final Master Mix
    final_mix = voice_track * 1.0 + sfx_track * 0.9 + bgm_track * 0.8
    # Peak normalize to -1.0 dB
    peak = np.max(np.abs(final_mix))
    if peak > 0:
        final_mix = final_mix / peak * 0.90
        
    sf.write(OUTPUT_AUDIO, final_mix, sr)
    print(f"Master audio track exported: {OUTPUT_AUDIO}")
    
    # Save timing metadata for video renderer
    metadata = {
        "total_duration": total_duration,
        "scene_starts": scene_start_times,
        "scene_durations": scene_durations
    }
    import json
    with open(os.path.join(BASE_DIR, "timing_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved timing_metadata.json")

if __name__ == "__main__":
    main()
