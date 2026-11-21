"""
build_audio_713.py
==================
Synthesizes and masters audio for Phase 7.13 18.0-Second Short Film
Title: "MIDNIGHT DISCOVERY"
"""

import os
import sys
import wave
import json
import asyncio
import subprocess
import numpy as np
import edge_tts
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.13\production_test"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
ASSETS_DIR = r"F:\Master AI\15_ASSETS\audio"

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
SAMPLE_RATE = 44100
TOTAL_DURATION = 18.0
TOTAL_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

VOICE_CUES = [
    {
        "id": "cue_01",
        "text": "बाहर तूफ़ान था, और मेरे सर्वर पर शांति... मुझे लगा सब कंट्रोल में है।",
        "hinglish": "Bahir toofan tha, aur mere server par shaanti... mujhe laga sab control mein hai.",
        "start": 0.5,
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-1Hz"
    },
    {
        "id": "cue_02",
        "text": "तभी स्क्रीन पर रेड अलर्ट चमका—अननोन ट्रांजेक्शन निन्यानवे हज़ार रुपये?!",
        "hinglish": "Tabhi screen par red alert chamka—unknown transaction ₹99,000?!",
        "start": 5.6,
        "voice": "hi-IN-MadhurNeural",
        "rate": "+8%",
        "pitch": "+2Hz"
    },
    {
        "id": "cue_03",
        "text": "मैंने गौर से देखा... अरे, ये तो कंपनी का टेस्ट क्रेडिट था! बच गया भाई।",
        "hinglish": "Maine gaur se dekha... arrey, ye to company ka test credit tha! Bach gaya bhai.",
        "start": 11.6,
        "voice": "hi-IN-MadhurNeural",
        "rate": "+5%",
        "pitch": "+0Hz"
    }
]

async def generate_speech_cues():
    print("Synthesizing neural Hindi dialogue cues with Edge-TTS...")
    rendered_cues = []
    for c in VOICE_CUES:
        mp3_path = os.path.join(AUDIO_DIR, f"{c['id']}.mp3")
        wav_path = os.path.join(AUDIO_DIR, f"{c['id']}.wav")
        communicate = edge_tts.Communicate(c["text"], c["voice"], rate=c["rate"], pitch=c["pitch"])
        await communicate.save(mp3_path)
        
        # Convert to 44.1kHz mono WAV and trim only leading and trailing silence
        cmd = [
            FFMPEG_BIN, "-y", "-i", mp3_path,
            "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
            "-ar", str(SAMPLE_RATE), "-ac", "1", wav_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        with wave.open(wav_path, "rb") as wf:
            dur = wf.getnframes() / wf.getframerate()
        print(f"  {c['id']} rendered: duration = {dur:.2f}s (start = {c['start']:.2f}s, end = {c['start']+dur:.2f}s)")
        rendered_cues.append({**c, "wav": wav_path, "duration": dur, "end": c["start"] + dur})
        
    return rendered_cues

def load_wav_samples(wav_path):
    with wave.open(wav_path, "rb") as wf:
        n = wf.getnframes()
        raw = wf.readframes(n)
        sr = wf.getframerate()
        ch = wf.getnchannels()
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if ch == 2:
            samples = samples.reshape(-1, 2)
        else:
            samples = np.column_stack([samples, samples])
    return samples, sr

def synth_sfx_ding(freq=1200, duration=0.6):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Sine with exponential decay
    decay = np.exp(-t * 6.0)
    sig = 0.5 * np.sin(2 * np.pi * freq * t) * decay
    return np.column_stack([sig, sig])

def synth_tension_thud(duration=0.8):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    decay = np.exp(-t * 5.0)
    sig = 0.6 * np.sin(2 * np.pi * 65.0 * t) * decay
    return np.column_stack([sig, sig])

def build_master_soundtrack(cues):
    print("Mastering multi-movement audio mix with sidechain ducking...")
    master_mix = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    voice_track = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    music_track = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    sfx_track = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)

    # 1. Place dialogue cues
    speech_envelope = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    for c in cues:
        samps, _ = load_wav_samples(c["wav"])
        idx_start = int(c["start"] * SAMPLE_RATE)
        idx_end = min(TOTAL_SAMPLES, idx_start + len(samps))
        voice_track[idx_start:idx_end] += samps[:idx_end - idx_start]
        # Mark speech envelope with 0.15s padding for smooth ducking
        pad = int(0.15 * SAMPLE_RATE)
        p_start = max(0, idx_start - pad)
        p_end = min(TOTAL_SAMPLES, idx_end + pad)
        speech_envelope[p_start:p_end] = 1.0

    # 2. Smooth speech envelope (running average 100ms)
    kernel_size = int(0.1 * SAMPLE_RATE)
    kernel = np.ones(kernel_size) / kernel_size
    smoothed_ducking = np.convolve(speech_envelope, kernel, mode="same")
    smoothed_ducking = np.clip(smoothed_ducking, 0.0, 1.0)

    # 3. Load & loop Chopin piano music
    bgm_path = os.path.join(ASSETS_DIR, "music", "bgm_chopin_nocturne_op37_no1.ogg")
    bgm_wav = os.path.join(AUDIO_DIR, "bgm_temp.wav")
    subprocess.run([FFMPEG_BIN, "-y", "-i", bgm_path, "-t", str(TOTAL_DURATION), "-ar", str(SAMPLE_RATE), "-ac", "2", bgm_wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    bgm_samps, _ = load_wav_samples(bgm_wav)
    n_bgm = min(TOTAL_SAMPLES, len(bgm_samps))
    music_track[:n_bgm] = bgm_samps[:n_bgm]

    # Dynamic sidechain ducking: -14 dBFS during speech (gain 0.20), normal 0.70
    music_gain = 0.70 * (1.0 - smoothed_ducking * 0.72)
    music_track[:, 0] *= music_gain
    music_track[:, 1] *= music_gain

    # 4. Spot Foley SFX
    # Rain ambience continuously in background (gain 0.18)
    rain_path = os.path.join(ASSETS_DIR, "sfx", "sfx_rain_against_window.ogg")
    rain_wav = os.path.join(AUDIO_DIR, "rain_temp.wav")
    subprocess.run([FFMPEG_BIN, "-y", "-i", rain_path, "-t", str(TOTAL_DURATION), "-ar", str(SAMPLE_RATE), "-ac", "2", rain_wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rain_samps, _ = load_wav_samples(rain_wav)
    n_rain = min(TOTAL_SAMPLES, len(rain_samps))
    sfx_track[:n_rain] += rain_samps[:n_rain] * 0.22

    # Spot SFX 1: J-Cut Notification Alert at 5.35s (0.25s before Shot 2!)
    ding = synth_sfx_ding(freq=1450, duration=0.7) * 0.75
    idx_ding = int(5.35 * SAMPLE_RATE)
    sfx_track[idx_ding:idx_ding+len(ding)] += ding

    # Spot SFX 2: Heartbeat tension thud at 6.2s
    thud = synth_tension_thud(duration=0.8) * 0.8
    idx_thud = int(6.2 * SAMPLE_RATE)
    sfx_track[idx_thud:idx_thud+len(thud)] += thud

    # Spot SFX 3: Success chime at 16.2s
    success_chime = synth_sfx_ding(freq=980, duration=1.2) * 0.6
    idx_succ = int(16.2 * SAMPLE_RATE)
    sfx_track[idx_succ:idx_succ+len(success_chime)] += success_chime

    # 5. Master Summing
    master_mix = (voice_track * 1.15) + music_track + sfx_track

    # Normalize to EBU R128 peak compliant target (-2.8 dBFS)
    max_val = np.max(np.abs(master_mix))
    target_peak = 10.0 ** (-2.8 / 20.0) # ~0.724
    if max_val > 0:
        master_mix = master_mix * (target_peak / max_val)

    # Export 16-bit stereo WAV
    out_wav = os.path.join(AUDIO_DIR, "final_audio_mix.wav")
    int_samples = (master_mix * 32767.0).astype(np.int16)
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(int_samples.tobytes())

    # Measure final metrics
    peak_db = 20 * np.log10(np.max(np.abs(master_mix)))
    rms_db = 20 * np.log10(np.sqrt(np.mean(master_mix**2)))
    print(f"Master soundtrack written to: {out_wav}")
    print(f"  Duration: {TOTAL_DURATION:.2f}s | True Peak: {peak_db:.2f} dBFS | RMS: {rms_db:.2f} dBFS")

    # Export dialogue timeline JSON
    timeline_path = os.path.join(BASE_DIR, "dialogue_timeline.json")
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump({"total_duration": TOTAL_DURATION, "cues": cues}, f, indent=2)

if __name__ == "__main__":
    cues = asyncio.run(generate_speech_cues())
    build_master_soundtrack(cues)
