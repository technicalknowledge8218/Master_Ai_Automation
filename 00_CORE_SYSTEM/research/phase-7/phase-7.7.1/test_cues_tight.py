import os
import sys
import wave
import numpy as np

ENGINE_DIR = r"F:\Master AI\09_CONTENT_STUDIO\engine"
sys.path.append(ENGINE_DIR)
from voiceover_engine import VoiceoverEngine

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.1"
ve = VoiceoverEngine()

cues = [
    {
        "id": "CUE-01",
        "text": "कभी-कभी अपने ही सपने अजनबी लगने लगते हैं... महीनों से मेरा गिटार खामोश था।",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+0%"
    },
    {
        "id": "CUE-02",
        "text": "तभी मेरे वफ़ादार कुत्ते लियो ने मुझे देखा, मानो कह रहा हो—रुकना मत दोस्त!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+0%"
    },
    {
        "id": "CUE-03",
        "text": "मैंने गिटार उठाया, और उस एक सुर ने पूरी खामोशी तोड़ दी।",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+0%"
    },
    {
        "id": "CUE-04",
        "text": "बादलों के पीछे से सूरज निकल आया... और मुझे मेरी आवाज़ मिल गई।",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+0%"
    }
]

temp_dir = os.path.join(OUTPUT_DIR, "voice_chunks")
os.makedirs(temp_dir, exist_ok=True)

results = []
for idx, c in enumerate(cues):
    wav_path = os.path.join(temp_dir, f"timed_cue_{idx:02d}.wav")
    res = ve.synthesize_cue(
        text=c["text"],
        output_wav=wav_path,
        voice_name=c["voice"],
        rate=c["rate"],
        volume="+0%"
    )
    dur = res["duration_sec"]
    results.append((c["id"], dur, c["text"]))
    print(f"{c['id']}: Dur = {dur:.2f}s | {c['text']}")

print("\nTotal spoken duration:", sum(r[1] for r in results))
