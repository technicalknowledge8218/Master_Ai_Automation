import os
import sys
import json
import base64
import wave
import asyncio
import urllib.request
import urllib.error
import edge_tts
import soundfile as sf
import numpy as np

# Force UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\voice_dna\offline_cloned_output\showcase"
os.makedirs(OUT_DIR, exist_ok=True)
ARTIFACT_DIR = r"<ARTIFACT_DIR>"

# The Universal Test Line in Hindi
HINDI_SCRIPT = "अगर आप सोचते हैं कि सिर्फ मेहनत करके आप अमीर बन सकते हैं, तो आप बहुत बड़ी गलतफहमी में हैं। असली खेल मेहनत का नहीं, सही जानकारी और स्मार्ट सिस्टम्स का है!"

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash-preview-tts"

print(">>> [SHOWCASE] Starting Complete Voice Audition Pack Generation in Hindi...")

# 1. Generate Google Gemini TTS Voices
gemini_voices = [
    ("Charon", "01_gemini_charon_deep_male.wav", "Deep / Serious Male Narrator"),
    ("Fenrir", "02_gemini_fenrir_dramatic_male.wav", "Dramatic / Aggressive Cinematic Male"),
    ("Puck", "03_gemini_puck_energetic_male.wav", "Energetic / Youth Tech Male"),
    ("Kore", "04_gemini_kore_confident_female.wav", "Professional / Calm Corporate Female"),
    ("Aoede", "05_gemini_aoede_storyteller_female.wav", "Melodic / Expressive Female Storyteller")
]

for vname, fname, desc in gemini_voices:
    out_path = os.path.join(OUT_DIR, fname)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": HINDI_SCRIPT}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": vname
                    }
                }
            }
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            parts = res.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for p in parts:
                if "inlineData" in p:
                    raw_pcm = base64.b64decode(p["inlineData"]["data"])
                    with wave.open(out_path, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(24000)
                        wf.writeframes(raw_pcm)
                    print(f"    [OK] Gemini -> {fname} ({desc})")
    except Exception as e:
        print(f"    [ERR] Gemini {vname}: {e}")

# 2. Generate Microsoft Edge Neural TTS Voices
edge_voices = [
    ("hi-IN-MadhurNeural", "06_edge_madhur_hindi_male.wav", "Crisp Native Indian Hindi Male", "+0%", "-2Hz"),
    ("hi-IN-SwaraNeural", "07_edge_swara_hindi_female.wav", "Warm Native Indian Hindi Female", "+0%", "+0Hz")
]

async def gen_edge():
    for vname, fname, desc, rate, pitch in edge_voices:
        out_path = os.path.join(OUT_DIR, fname)
        temp_mp3 = out_path.replace(".wav", ".mp3")
        try:
            comm = edge_tts.Communicate(HINDI_SCRIPT, vname, rate=rate, pitch=pitch)
            await comm.save(temp_mp3)
            data, sr = sf.read(temp_mp3)
            sf.write(out_path, data, sr)
            if os.path.exists(temp_mp3): os.remove(temp_mp3)
            print(f"    [OK] Edge-TTS -> {fname} ({desc})")
        except Exception as e:
            print(f"    [ERR] Edge-TTS {vname}: {e}")

asyncio.run(gen_edge())

# 3. Mirror all generated files to Artifact directory
import shutil
for f in os.listdir(OUT_DIR):
    if f.endswith(".wav"):
        src = os.path.join(OUT_DIR, f)
        dst = os.path.join(ARTIFACT_DIR, f)
        shutil.copy2(src, dst)

print("\n>>> [SHOWCASE] All voices generated and mirrored successfully to Artifacts!")
