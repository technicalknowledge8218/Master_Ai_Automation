import asyncio
import edge_tts
import os
import subprocess
import soundfile as sf
import numpy as np
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\remotion_tech_reel"
SFX_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\sfx"
RAW_VIDEO = os.path.join(BASE_DIR, "out_remotion_demo.mp4")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "remotion_master_tech_reel.mp4")

VOICE_PATH = os.path.join(BASE_DIR, "remotion_voice.wav")
AUDIO_MIX_PATH = os.path.join(BASE_DIR, "remotion_audio_mix.wav")

SCRIPT_TEXT = "Frontend ke liye istemaal karo Cloudflare Pages! Jahan milti hai Unlimited Bandwidth, zero cold start delay, aur lifetime zero rupee bill!"

def load_wav(path, target_sr=44100):
    data, sr = sf.read(path)
    if data.ndim == 1:
        data = np.column_stack([data, data])
    elif data.shape[1] > 2:
        data = data[:, :2]
    if sr != target_sr:
        num_samples = int(len(data) * target_sr / sr)
        indices = np.linspace(0, len(data) - 1, num_samples)
        data = np.column_stack([
            np.interp(indices, np.arange(len(data)), data[:, 0]),
            np.interp(indices, np.arange(len(data)), data[:, 1])
        ])
    return data

async def main():
    sr = 44100
    total_dur = 10.0 # 300 frames @ 30fps
    total_samples = int(total_dur * sr)
    
    # 1. Generate Voiceover
    print("Generating Edge-TTS voiceover...")
    mp3_tmp = os.path.join(BASE_DIR, "temp_voice.mp3")
    comm = edge_tts.Communicate(SCRIPT_TEXT, "hi-IN-MadhurNeural", rate="+14%", pitch="+1Hz")
    await comm.save(mp3_tmp)
    
    # Master voice with FFmpeg
    cmd_voice = [
        FFMPEG, "-y", "-i", mp3_tmp,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,bass=g=3:f=120,treble=g=3:f=3500",
        "-ar", str(sr), "-ac", "2",
        VOICE_PATH
    ]
    subprocess.run(cmd_voice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(mp3_tmp):
        os.remove(mp3_tmp)
        
    voice_raw = load_wav(VOICE_PATH, sr)
    voice_track = np.zeros((total_samples, 2), dtype=np.float32)
    # Start voice at t=0.6s
    s_idx = int(0.6 * sr)
    e_idx = min(s_idx + len(voice_raw), total_samples)
    voice_track[s_idx:e_idx] = voice_raw[:e_idx - s_idx] * 1.05
    
    # 2. SFX Track
    sfx_track = np.zeros((total_samples, 2), dtype=np.float32)
    
    def add_sfx(name, t_sec, vol=0.6):
        p = os.path.join(SFX_DIR, name)
        if os.path.exists(p):
            snd = load_wav(p, sr) * vol
            idx = int(t_sec * sr)
            end = min(idx + len(snd), total_samples)
            if idx < total_samples:
                sfx_track[idx:end] += snd[:end - idx]
                
    add_sfx("whoosh.wav", 0.0, vol=0.5)
    # Terminal typing clicks between t=1.0s and t=3.0s, and t=3.5s to 5.0s
    for t_click in [1.0, 1.4, 1.8, 2.2, 2.6, 3.6, 4.0, 4.4, 4.8]:
        add_sfx("typing.wav", t_click, vol=0.45)
    add_sfx("pop.wav", 5.4, vol=0.55) # Status reveal pop
    add_sfx("chime.wav", 8.0, vol=0.5) # $0 Lifetime chime
    
    # 3. BGM Track with Side-chain ducking
    bgm_track = np.zeros((total_samples, 2), dtype=np.float32)
    bgm_path = os.path.join(SFX_DIR, "lofi_bg_track.wav")
    if os.path.exists(bgm_path):
        raw_bgm = load_wav(bgm_path, sr)
        loops = int(np.ceil(total_samples / len(raw_bgm)))
        tiled_bgm = np.tile(raw_bgm, (loops, 1))[:total_samples]
        
        voice_mono = np.abs(voice_track).mean(axis=1)
        win = int(0.15 * sr)
        envelope = np.convolve(voice_mono, np.ones(win)/win, mode='same')
        duck = np.where(envelope > 0.02, 0.12, 0.35)
        bgm_track = tiled_bgm * duck[:, np.newaxis]
        
    # 4. Master Mix
    master_mix = voice_track * 1.0 + sfx_track * 0.9 + bgm_track * 0.75
    peak = np.max(np.abs(master_mix))
    if peak > 0:
        master_mix = master_mix / peak * 0.92
        
    sf.write(AUDIO_MIX_PATH, master_mix, sr)
    print("Master audio mixed successfully.")
    
    # 5. Mux with Remotion video
    print("Muxing final video with audio track...")
    mux_cmd = [
        FFMPEG, "-y",
        "-i", RAW_VIDEO,
        "-i", AUDIO_MIX_PATH,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"\nREMOTION MASTER VIDEO READY:")
    print(f"Path: {OUTPUT_VIDEO}")
    print(f"Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    asyncio.run(main())
