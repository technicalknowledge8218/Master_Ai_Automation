import asyncio
import edge_tts
import os
import subprocess
import soundfile as sf
import numpy as np
import imageio_ffmpeg
import json

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\remotion_tech_reel"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_dialogue")
os.makedirs(AUDIO_DIR, exist_ok=True)
SFX_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\sfx"

DIALOGUE = [
    {
        "id": "turn1_arjun",
        "speaker": "ARJUN",
        "role": "JUNIOR DEV",
        "char_img": "arjun_shocked.png",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+3Hz",
        "text": "Bhai, mere AWS account mein 40 dollar ka surprise bill aa gaya! Student project ke liye itna paisa kahan se laun?",
        "subtitle": "Bhai, mere AWS account mein $40 ka surprise bill aa gaya! Student project ke liye itna paisa kahan se laun?",
        "badge_color": "#00E599",
        "sfx": "alarm.wav"
    },
    {
        "id": "turn2_kabir",
        "speaker": "KABIR",
        "role": "SENIOR ARCHITECT",
        "char_img": "dr_kabir_explaining.png",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+11%",
        "pitch": "-2Hz",
        "text": "Arre tension mat le! Junior dev ho kar AWS use karna band kar. 2026 mein sab Cloudflare Pages aur Supabase use karte hain — zero cold start aur lifetime zero rupee bill!",
        "subtitle": "Tension mat le! Junior dev ho kar AWS chhod! 2026 mein sab Cloudflare Pages aur Supabase use karte hain — $0 bill!",
        "badge_color": "#FFD21E",
        "sfx": "ding.wav"
    },
    {
        "id": "turn3_arjun",
        "speaker": "ARJUN",
        "role": "JUNIOR DEV",
        "char_img": "arjun_pointing.png",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+3Hz",
        "text": "Lekin backend API aur database 24 ghante kaise chalega bina soye?",
        "subtitle": "Lekin backend API aur database 24 ghante kaise chalega bina soye?",
        "badge_color": "#00E599",
        "sfx": "whoosh.wav"
    },
    {
        "id": "turn4_kabir",
        "speaker": "KABIR",
        "role": "SENIOR ARCHITECT",
        "char_img": "dr_kabir_proud.png",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+11%",
        "pitch": "-2Hz",
        "text": "Cron-job.org se ek free 10-minute automated ping laga de, server kabhi nahi soyega! Starter GitHub template ke liye comment karo STACK, direct DM bhej raha hoon!",
        "subtitle": "Cron-job.org se 10-minute automated ping laga de, server kabhi nahi soyega! Repo ke liye comment karo 'STACK'!",
        "badge_color": "#FFD21E",
        "sfx": "pop.wav"
    }
]

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
    turn_audios = []
    turn_durs = []
    turn_starts = []
    
    current_time = 0.5 # Start after 0.5s pause
    
    for item in DIALOGUE:
        mp3_p = os.path.join(AUDIO_DIR, f"{item['id']}.mp3")
        wav_p = os.path.join(AUDIO_DIR, f"{item['id']}.wav")
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(mp3_p)
        
        # Audio mastering
        cmd = [
            FFMPEG, "-y", "-i", mp3_p,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,bass=g=2:f=120,treble=g=2:f=3500",
            "-ar", str(sr), "-ac", "2",
            wav_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(mp3_p):
            os.remove(mp3_p)
            
        data = load_wav(wav_p, sr)
        dur = len(data) / sr
        turn_starts.append(current_time)
        turn_durs.append(dur)
        turn_audios.append(data)
        current_time += dur + 0.35 # Natural 0.35s conversational reaction gap
        print(f"Generated {item['id']} ({item['speaker']}) - Duration: {dur:.2f}s")
        
    total_dur = current_time + 1.0 # 1s tail
    total_samples = int(total_dur * sr)
    print(f"\nTotal Dialogue Reel Duration: {total_dur:.2f}s")
    
    # Mix Tracks
    voice_track = np.zeros((total_samples, 2), dtype=np.float32)
    sfx_track = np.zeros((total_samples, 2), dtype=np.float32)
    
    def add_sfx(name, t_sec, vol=0.55):
        p = os.path.join(SFX_DIR, name)
        if os.path.exists(p):
            snd = load_wav(p, sr) * vol
            idx = int(t_sec * sr)
            end = min(idx + len(snd), total_samples)
            if idx < total_samples:
                sfx_track[idx:end] += snd[:end - idx]
                
    for i, item in enumerate(DIALOGUE):
        st = turn_starts[i]
        audio = turn_audios[i]
        s_idx = int(st * sr)
        e_idx = min(s_idx + len(audio), total_samples)
        voice_track[s_idx:e_idx] += audio[:e_idx - s_idx]
        
        # Add SFX on speaker transition
        add_sfx("whoosh.wav", max(0.0, st - 0.2), vol=0.4)
        if item.get("sfx"):
            add_sfx(item["sfx"], st + 0.5, vol=0.5)

    # BGM Track with Side-chain ducking
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
        
    master_mix = voice_track * 1.0 + sfx_track * 0.9 + bgm_track * 0.75
    peak = np.max(np.abs(master_mix))
    if peak > 0:
        master_mix = master_mix / peak * 0.92
        
    master_audio_p = os.path.join(AUDIO_DIR, "dialogue_master_audio.wav")
    sf.write(master_audio_p, master_mix, sr)
    print(f"Master dialogue audio written: {master_audio_p}")
    
    # Save metadata for Remotion
    metadata = {
        "total_duration": total_dur,
        "turns": [
            {
                "id": DIALOGUE[i]["id"],
                "speaker": DIALOGUE[i]["speaker"],
                "role": DIALOGUE[i]["role"],
                "char_img": DIALOGUE[i]["char_img"],
                "start": turn_starts[i],
                "duration": turn_durs[i],
                "end": turn_starts[i] + turn_durs[i],
                "subtitle": DIALOGUE[i]["subtitle"],
                "badge_color": DIALOGUE[i]["badge_color"],
            }
            for i in range(len(DIALOGUE))
        ]
    }
    
    meta_p = os.path.join(BASE_DIR, "src", "dialogue_metadata.json")
    with open(meta_p, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Dialogue metadata saved: {meta_p}")

if __name__ == "__main__":
    asyncio.run(main())
