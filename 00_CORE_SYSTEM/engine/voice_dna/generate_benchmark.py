import os
import sys
import json
import urllib.request
import urllib.error
import soundfile as sf
import numpy as np
import scipy.signal

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_KEY = "sk_94905d8358b110922eb9a9304a5d011d3e778a06333e143a"
ADAM_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
GEORGE_LALAJI_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" # George / Bill Boss

OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\voice_dna\offline_cloned_output"
os.makedirs(OUT_DIR, exist_ok=True)
ARTIFACT_DIR = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

dialogue = [
    {
        "id": "line_1_lalaji",
        "voice_id": GEORGE_LALAJI_VOICE_ID,
        "speaker": "Lala Ji",
        "text": "अरे कबीर बाबू! इंस्टाग्राम पे तो मेरी रील पे दस लाख व्यूज आ गए! लाखों रुपये बरसेंगे अब तो!",
        "stability": 0.45,
        "similarity": 0.85
    },
    {
        "id": "line_2_kabir",
        "voice_id": ADAM_VOICE_ID,
        "speaker": "Kabir",
        "text": "रोहन भाई, ज़रा अपना बैंक अकाउंट चेक करो। इंस्टाग्राम सिर्फ व्यूज के पैसे नहीं देता, असली कमाई स्पॉन्सरशिप से होती है।",
        "stability": 0.50,
        "similarity": 0.85
    },
    {
        "id": "line_3_lalaji",
        "voice_id": GEORGE_LALAJI_VOICE_ID,
        "speaker": "Lala Ji",
        "text": "क्या बात कर रहे हो?! तो फिर यूट्यूब शॉर्ट्स पे अगर दस लाख व्यूज आ जाते तो क्या होता?",
        "stability": 0.40,
        "similarity": 0.85
    },
    {
        "id": "line_4_kabir",
        "voice_id": ADAM_VOICE_ID,
        "speaker": "Kabir",
        "text": "यूट्यूब के ऐडसेंस रेवेन्यू शेयर से दस लाख व्यूज पर सीधे पंद्रह सौ से चार हज़ार रुपये खाते में आते हैं। लेकिन रुको... असली ट्विस्ट तो अभी बाकी है!",
        "stability": 0.50,
        "similarity": 0.85
    },
    {
        "id": "line_5_lalaji",
        "voice_id": GEORGE_LALAJI_VOICE_ID,
        "speaker": "Lala Ji",
        "text": "असली ट्विस्ट? कैसा ट्विस्ट भाई?",
        "stability": 0.40,
        "similarity": 0.85
    },
    {
        "id": "line_6_kabir",
        "voice_id": ADAM_VOICE_ID,
        "speaker": "Kabir",
        "text": "अगर तुम्हारे पास कोई डिजिटल प्रोडक्ट या एफिलिएट लिंक है, तो इंस्टाग्राम यूट्यूब से तीन गुना ज़्यादा सेल्स कराता है! तो अब आप बताओ — आप ऐडसेंस पसंद करोगे या एफिलिएट मार्केटिंग? नीचे कमेंट करो!",
        "stability": 0.50,
        "similarity": 0.85
    }
]

print(">>> [BENCHMARK] Generating Studio-Grade ElevenLabs Multilingual v2 Master...")
generated_files = []
sr = 44100

for item in dialogue:
    out_mp3 = os.path.join(OUT_DIR, f"eleven_{item['id']}.mp3")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{item['voice_id']}"
    payload = {
        "text": item["text"],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": item["stability"],
            "similarity_boost": item["similarity"],
            "style": 0.4,
            "use_speaker_boost": True
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as resp:
        with open(out_mp3, "wb") as f:
            f.write(resp.read())
    print(f"    - Generated {item['speaker']} -> {out_mp3}")
    generated_files.append(out_mp3)

# Stitch with soundfile and 120ms pauses
import shutil
import subprocess

combined = []
pause = np.zeros(int(0.12 * 44100), dtype=np.float32)

for fpath in generated_files:
    wav_temp = fpath.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-y", "-i", fpath, "-ar", "44100", "-ac", "1", wav_temp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data, file_sr = sf.read(wav_temp)
    # Trim silence
    threshold = 0.01 * np.max(np.abs(data)) if np.max(np.abs(data)) > 0 else 0.01
    non_silent = np.where(np.abs(data) > threshold)[0]
    if len(non_silent) > 0:
        data = data[max(0, non_silent[0]-int(0.02*44100)):min(len(data), non_silent[-1]+int(0.03*44100))]
    combined.append(data)
    combined.append(pause)

full_dialogue = np.concatenate(combined)
peak = np.max(np.abs(full_dialogue))
if peak > 0:
    full_dialogue = full_dialogue / peak * 0.90

diag_master = os.path.join(OUT_DIR, "shorts_vs_reels_elevenlabs_dialogue.wav")
sf.write(diag_master, full_dialogue, 44100)

# Mix Lo-Fi BGM
bgm_path = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\sfx\lofi_bg_track.wav"
scene_master = os.path.join(OUT_DIR, "shorts_vs_reels_elevenlabs_studio_master.wav")

if os.path.exists(bgm_path):
    bgm_data, bgm_sr = sf.read(bgm_path)
    if bgm_sr != 44100:
        num_samples = int(len(bgm_data) * 44100 / bgm_sr)
        bgm_data = scipy.signal.resample(bgm_data, num_samples)
    if bgm_data.ndim > 1:
        bgm_data = bgm_data.mean(axis=1)

    target_len = len(full_dialogue) + int(0.8 * 44100)
    if len(bgm_data) < target_len:
        repeats = int(np.ceil(target_len / len(bgm_data)))
        bgm_data = np.tile(bgm_data, repeats)
    bgm_data = bgm_data[:target_len].astype(np.float32)

    bgm_gain = 10 ** (-22.0 / 20.0)
    bgm_data = bgm_data * bgm_gain

    fade_len = int(0.8 * 44100)
    bgm_data[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

    pad_diag = np.pad(full_dialogue, (0, target_len - len(full_dialogue)))
    final_mix = pad_diag + bgm_data
    final_peak = np.max(np.abs(final_mix))
    if final_peak > 0.95:
        final_mix = final_mix / final_peak * 0.95
    sf.write(scene_master, final_mix, 44100)
else:
    sf.write(scene_master, full_dialogue, 44100)

shutil.copy2(diag_master, os.path.join(ARTIFACT_DIR, "shorts_vs_reels_elevenlabs_dialogue.wav"))
shutil.copy2(scene_master, os.path.join(ARTIFACT_DIR, "shorts_vs_reels_elevenlabs_studio_master.wav"))
print(f">>> [BENCHMARK] Complete! Master saved: {scene_master} ({len(full_dialogue)/44100:.2f}s)")
