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
        "text": "ज़िंदगी में कभी-कभी अपने ही सपने अजनबी लगने लगते हैं... महीनों से मेरा गिटार खामोश था।",
        "start_sec": 0.8
    },
    {
        "id": "CUE-02",
        "text": "तभी मेरे वफ़ादार कुत्ते लियो ने आकर मुझे देखा, मानो कह रहा हो—रुकना मत दोस्त!",
        "start_sec": 9.8
    },
    {
        "id": "CUE-03",
        "text": "मैंने गिटार उठाया, और उस एक सुर ने पूरी खामोशी तोड़ दी।",
        "start_sec": 17.0
    },
    {
        "id": "CUE-04",
        "text": "बादलों के पीछे से सूरज निकल आया... और मुझे मेरी आवाज़ मिल गई।",
        "start_sec": 23.0
    }
]

temp_dir = os.path.join(OUTPUT_DIR, "voice_chunks")
os.makedirs(temp_dir, exist_ok=True)

sr = 44100
total_dur = 30.0
total_samples = int(total_dur * sr)
master_buffer = np.zeros(total_samples, dtype=np.float32)

print("Synthesizing 4 calibrated cues with hi-IN-MadhurNeural...")
for idx, c in enumerate(cues):
    wav_path = os.path.join(temp_dir, f"calibrated_cue_{idx:02d}.wav")
    res = ve.synthesize_cue(
        text=c["text"],
        output_wav=wav_path,
        voice_name="hi-IN-MadhurNeural",
        rate="-2%",
        volume="+0%"
    )
    dur = res["duration_sec"]
    end_sec = c["start_sec"] + dur
    print(f"Cue {idx+1} ({c['id']}): Start={c['start_sec']}s, Dur={dur:.2f}s, End={end_sec:.2f}s | Text: {c['text'][:30]}...")

    with wave.open(wav_path, "rb") as wf:
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    s_idx = int(c["start_sec"] * sr)
    e_idx = min(total_samples, s_idx + len(samples))
    master_buffer[s_idx:e_idx] += samples[:e_idx - s_idx]

# Check for overlap between cues
for i in range(len(cues) - 1):
    c1 = cues[i]
    c2 = cues[i+1]
    # We will verify end time of cue i vs start time of cue i+1
