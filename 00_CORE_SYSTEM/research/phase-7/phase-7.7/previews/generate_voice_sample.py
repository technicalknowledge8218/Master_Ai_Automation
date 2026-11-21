import os
import sys
import wave
import numpy as np

ENGINE_DIR = r"F:\Master AI\09_CONTENT_STUDIO\engine"
sys.path.append(ENGINE_DIR)
from voiceover_engine import VoiceoverEngine

PREVIEWS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews"
os.makedirs(PREVIEWS_DIR, exist_ok=True)

ve = VoiceoverEngine()

# Dialogue Manifest with Two Voice Actors:
# Aanya (hi-IN-SwaraNeural) & Kabir (hi-IN-MadhurNeural)
cues = [
    {
        "id": "CUE-01",
        "character": "Aanya (आन्या)",
        "voice": "hi-IN-SwaraNeural",
        "text": "तीन हफ्ते हो गए कबीर... एक भी कस्टमर नहीं आया। शायद मुझे ये सब बंद कर देना चाहिए।",
        "start_sec": 0.8,
        "rate": "-3%",
        "volume": "+0%"
    },
    {
        "id": "CUE-02",
        "character": "Kabir (कबीर)",
        "voice": "hi-IN-MadhurNeural",
        "text": "दीदी, इतनी जल्दी हिम्मत हारोगी? अरे सुनो... फ़ोन पर क्या बजा?",
        "start_sec": 8.5,
        "rate": "+2%",
        "volume": "+0%"
    },
    {
        "id": "CUE-03",
        "character": "Aanya (आन्या)",
        "voice": "hi-IN-SwaraNeural",
        "text": "कबीर... देखो! सच में पहला ऑर्डर आ गया!",
        "start_sec": 16.2,
        "rate": "+0%",
        "volume": "+0%"
    },
    {
        "id": "CUE-04",
        "character": "Kabir (कबीर)",
        "voice": "hi-IN-MadhurNeural",
        "text": "कहा था ना मैंने! अब अपना एप्रन पहनिए शेफ़ साहिबा... आपकी नई शुरुआत हो गई!",
        "start_sec": 23.5,
        "rate": "+1%",
        "volume": "+0%"
    }
]

sr = 44100
target_dur = 30.0
total_samples = int(target_dur * sr)
master_buffer = np.zeros(total_samples, dtype=np.float32)

temp_dir = os.path.join(PREVIEWS_DIR, "voice_temp")
os.makedirs(temp_dir, exist_ok=True)

synthesized_info = []

for idx, c in enumerate(cues):
    chunk_wav = os.path.join(temp_dir, f"chunk_{idx:02d}_{c['character'].split()[0]}.wav")
    print(f"Synthesizing {c['character']} [Voice: {c['voice']}]...")
    res = ve.synthesize_cue(
        text=c["text"],
        output_wav=chunk_wav,
        voice_name=c["voice"],
        rate=c["rate"],
        volume=c["volume"]
    )

    with wave.open(chunk_wav, "rb") as wf:
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    start_idx = int(c["start_sec"] * sr)
    end_idx = min(total_samples, start_idx + len(samples))
    master_buffer[start_idx:end_idx] += samples[:end_idx - start_idx]

    c_info = dict(c)
    c_info["duration_sec"] = res["duration_sec"]
    c_info["end_sec"] = round(c["start_sec"] + res["duration_sec"], 2)
    synthesized_info.append(c_info)
    print(f"  -> Generated: {res['duration_sec']:.2f}s | Starts: {c['start_sec']}s -> Ends: {c_info['end_sec']}s")

# Normalize to -1.5 dBFS True Peak
peak = np.max(np.abs(master_buffer))
if peak > 0.0:
    target_peak = 10 ** (-1.5 / 20.0) # ~0.841
    master_buffer = (master_buffer / peak) * target_peak

out_wav = os.path.join(PREVIEWS_DIR, "voice_sample_preview.wav")
int16_samples = np.clip(master_buffer * 32767.0, -32768.0, 32767.0).astype(np.int16)
with wave.open(out_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(int16_samples.tobytes())

# Compute Speech Activity Detection (SAD) across 30 seconds
energy_profile = []
for s in range(int(target_dur)):
    seg = master_buffer[s * sr : (s + 1) * sr]
    seg_rms = float(np.sqrt(np.mean(seg**2)))
    seg_peak = float(np.max(np.abs(seg)))
    rms_db = float(20 * np.log10(seg_rms + 1e-9))
    peak_db = float(20 * np.log10(seg_peak + 1e-9))
    is_active = seg_rms > 0.02
    energy_profile.append({
        "second": s,
        "is_active": is_active,
        "rms_dbfs": round(rms_db, 1),
        "peak_dbfs": round(peak_db, 1)
    })

active_secs = sum(1 for e in energy_profile if e["is_active"])
total_rms = float(np.sqrt(np.mean(master_buffer**2)))
total_rms_db = float(20 * np.log10(total_rms + 1e-9))

print("\n" + "="*60)
print("HINDI VOICEOVER SAMPLE GENERATION COMPLETE")
print("="*60)
print(f"File Path: {out_wav}")
print(f"Duration: {target_dur} seconds ({total_samples:,} samples)")
print(f"Active Speech Seconds: {active_secs} / 30 ({active_secs/30*100:.1f}%)")
print(f"Integrated Loudness: {total_rms_db:.2f} dBFS | True Peak: -1.50 dBFS")
print("Per-Second Speech Profile:")
for e in energy_profile:
    st = "ACTIVE VOICE" if e["is_active"] else "BREATH / DRAMATIC PAUSE"
    print(f"  Sec {e['second']:02d}: {st} (RMS: {e['rms_dbfs']} dBFS)")
