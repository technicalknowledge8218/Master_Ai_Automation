import os
import sys
import time
import json
import wave
import numpy as np

# Automatically agree to Coqui XTTS TOS for headless / non-interactive generation
os.environ["COQUI_TOS_AGREED"] = "1"

# Force UTF-8 stdout
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print(">>> [OFFLINE_CLONER] Initializing Python 3.10 Offline XTTS-v2 Voice Cloner...")

try:
    import torch
    import torchaudio
    import soundfile as sf
    print(f">>> [OFFLINE_CLONER] PyTorch version: {torch.__version__}, Torchaudio: {torchaudio.__version__}")
    
    # Patch torch.load to set weights_only=False for PyTorch 2.6+ unpickling
    _orig_load = torch.load
    def _safe_load(*args, **kwargs):
        kwargs['weights_only'] = False
        return _orig_load(*args, **kwargs)
    torch.load = _safe_load

    # Patch torchaudio load and save with soundfile (bypasses missing torchcodec)
    def _sf_load(filepath, *args, **kwargs):
        data, sr = sf.read(filepath)
        if data.ndim == 1:
            tensor = torch.from_numpy(data).unsqueeze(0).float()
        else:
            tensor = torch.from_numpy(data.T).float()
        return tensor, sr
    torchaudio.load = _sf_load

    def _sf_save(filepath, src, sample_rate, *args, **kwargs):
        arr = src.detach().cpu().numpy()
        if arr.ndim == 2 and arr.shape[0] < arr.shape[1]:
            arr = arr.T
        sf.write(filepath, arr, sample_rate)
    torchaudio.save = _sf_save

except Exception as e:
    print(f"Error importing torch: {e}")
    sys.exit(1)

# Bypass pycrfsuite Windows AppLocker block (XTTS-v2 does not need pycrfsuite or gruut)
from unittest.mock import MagicMock
mock_gruut = MagicMock()
mock_gruut.name.return_value = 'gruut'
mock_gruut.supported_languages.return_value = ['en-us', 'de', 'es', 'fr', 'it']
sys.modules['pycrfsuite'] = MagicMock()
sys.modules['gruut'] = MagicMock()
sys.modules['TTS.tts.utils.text.phonemizers.gruut_wrapper'] = MagicMock(Gruut=mock_gruut)

try:
    from TTS.api import TTS
    print(">>> [OFFLINE_CLONER] Successfully imported TTS from Coqui!")
except Exception as e:
    print(f"Error importing TTS: {e}")
    sys.exit(1)

DNA_VAULT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\voice_dna"
OUTPUT_DIR = os.path.join(DNA_VAULT_DIR, "offline_cloned_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

ADAM_SEED = os.path.join(DNA_VAULT_DIR, "male_adam_dna.wav")
LALAJI_SEED = os.path.join(DNA_VAULT_DIR, "male_bill_boss_dna.wav")

print(f">>> [OFFLINE_CLONER] Reference Voice Seeds:")
print(f"    - Adam DNA: {ADAM_SEED} (Exists: {os.path.exists(ADAM_SEED)})")
print(f"    - Lala Ji DNA: {LALAJI_SEED} (Exists: {os.path.exists(LALAJI_SEED)})")

# Test Dialogue - YouTube Shorts vs Instagram Reels
dialogue_script = [
    {
        "id": "line_1_lalaji",
        "speaker": "Lala Ji (Bill)",
        "seed": LALAJI_SEED,
        "text": "अरे कबीर बाबू! इंस्टाग्राम पे तो मेरी रील पे दस लाख व्यूज आ गए! लाखों रुपये बरसेंगे अब तो!",
        "lang": "hi"
    },
    {
        "id": "line_2_kabir",
        "speaker": "Kabir (Adam)",
        "seed": ADAM_SEED,
        "text": "रोहन भाई, ज़रा अपना बैंक अकाउंट चेक करो। इंस्टाग्राम सिर्फ व्यूज के पैसे नहीं देता, असली कमाई स्पॉन्सरशिप से होती है।",
        "lang": "hi"
    },
    {
        "id": "line_3_lalaji",
        "speaker": "Lala Ji (Bill)",
        "seed": LALAJI_SEED,
        "text": "क्या बात कर रहे हो?! तो फिर यूट्यूब शॉर्ट्स पे अगर दस लाख व्यूज आ जाते तो क्या होता?",
        "lang": "hi"
    },
    {
        "id": "line_4_kabir",
        "speaker": "Kabir (Adam)",
        "seed": ADAM_SEED,
        "text": "यूट्यूब के ऐडसेंस रेवेन्यू शेयर से दस लाख व्यूज पर सीधे पंद्रह सौ से चार हज़ार रुपये खाते में आते हैं। लेकिन रुको... असली ट्विस्ट तो अभी बाकी है!",
        "lang": "hi"
    },
    {
        "id": "line_5_lalaji",
        "speaker": "Lala Ji (Bill)",
        "seed": LALAJI_SEED,
        "text": "असली ट्विस्ट? कैसा ट्विस्ट भाई?",
        "lang": "hi"
    },
    {
        "id": "line_6_kabir",
        "speaker": "Kabir (Adam)",
        "seed": ADAM_SEED,
        "text": "अगर तुम्हारे पास कोई डिजिटल प्रोडक्ट या एफिलिएट लिंक है, तो इंस्टाग्राम यूट्यूब से तीन गुना ज़्यादा सेल्स और कमाई कराता है! तो अब आप बताओ — आप ऐडसेंस पसंद करोगे या एफिलिएट मार्केटिंग? नीचे कमेंट करो!",
        "lang": "hi"
    }
]

print(">>> [OFFLINE_CLONER] Loading XTTS-v2 model onto CPU (100% offline)...")
# Automatically downloads xtts_v2 weights once, then caches forever locally in %APPDATA%/tts
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
print(">>> [OFFLINE_CLONER] Model loaded successfully!")

generated_files = []
for item in dialogue_script:
    out_wav = os.path.join(OUTPUT_DIR, f"{item['id']}.wav")
    print(f"\n>>> [CLONING] Speaker: {item['speaker']} -> File: {item['id']}.wav")
    print(f"    Text: {item['text']}")
    t0 = time.time()
    tts.tts_to_file(
        text=item["text"],
        speaker_wav=item["seed"],
        language=item["lang"],
        file_path=out_wav
    )
    elapsed = time.time() - t0
    print(f"    Done in {elapsed:.1f}s | Saved: {out_wav}")
    generated_files.append((item, out_wav))

print("\n>>> [OFFLINE_CLONER] All 6 dialogue segments generated locally via voice cloning!")

# Post-processing: Stitch segments and mix with BGM
import shutil
import subprocess

try:
    import soundfile as sf
    import scipy.signal

    print("\n>>> [POST-PROCESSING] Stitching dialogue and compressing pauses...")
    combined_audio = []
    sr = 24000

    pause_samples = int(0.12 * sr) # 120ms natural human pause
    silence_gap = np.zeros(pause_samples, dtype=np.float32)

    for item, wav_path in generated_files:
        data, file_sr = sf.read(wav_path)
        if file_sr != sr:
            # Resample to 24000 if needed
            num_samples = int(len(data) * sr / file_sr)
            data = scipy.signal.resample(data, num_samples)
        if data.ndim > 1:
            data = data.mean(axis=1)
        data = data.astype(np.float32)

        # Trim leading and trailing silences
        threshold = 0.01 * np.max(np.abs(data)) if np.max(np.abs(data)) > 0 else 0.01
        non_silent = np.where(np.abs(data) > threshold)[0]
        if len(non_silent) > 0:
            start_idx = max(0, non_silent[0] - int(0.02 * sr))
            end_idx = min(len(data), non_silent[-1] + int(0.04 * sr))
            data = data[start_idx:end_idx]

        combined_audio.append(data)
        combined_audio.append(silence_gap)

    full_dialogue = np.concatenate(combined_audio)
    # Peak normalization to -1.0 dB
    peak = np.max(np.abs(full_dialogue))
    if peak > 0:
        full_dialogue = full_dialogue / peak * 0.89

    dialogue_out = os.path.join(OUTPUT_DIR, "shorts_vs_reels_dialogue_offline_cloned.wav")
    sf.write(dialogue_out, full_dialogue, sr)
    print(f">>> [POST-PROCESSING] Dialogue master saved: {dialogue_out} ({len(full_dialogue)/sr:.2f}s)")

    # Mix BGM if available
    bgm_path = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\sfx\lofi_bg_track.wav"
    scene_master = os.path.join(OUTPUT_DIR, "shorts_vs_reels_master_offline_cloned.wav")

    if os.path.exists(bgm_path):
        bgm_data, bgm_sr = sf.read(bgm_path)
        if bgm_sr != sr:
            num_samples = int(len(bgm_data) * sr / bgm_sr)
            bgm_data = scipy.signal.resample(bgm_data, num_samples)
        if bgm_data.ndim > 1:
            bgm_data = bgm_data.mean(axis=1)

        # Loop or slice bgm to match dialogue length + 0.8s outro
        target_len = len(full_dialogue) + int(0.8 * sr)
        if len(bgm_data) < target_len:
            repeats = int(np.ceil(target_len / len(bgm_data)))
            bgm_data = np.tile(bgm_data, repeats)
        bgm_data = bgm_data[:target_len].astype(np.float32)

        # Lower BGM volume to -22 dB
        bgm_gain = 10 ** (-22.0 / 20.0)
        bgm_data = bgm_data * bgm_gain

        # Fade out BGM at the end
        fade_len = int(0.8 * sr)
        fade_curve = np.linspace(1.0, 0.0, fade_len)
        bgm_data[-fade_len:] *= fade_curve

        # Pad dialogue to target_len
        pad_dialogue = np.pad(full_dialogue, (0, target_len - len(full_dialogue)))
        final_mix = pad_dialogue + bgm_data

        final_peak = np.max(np.abs(final_mix))
        if final_peak > 0.95:
            final_mix = final_mix / final_peak * 0.95

        sf.write(scene_master, final_mix, sr)
        print(f">>> [POST-PROCESSING] Final Scene with BGM saved: {scene_master}")
    else:
        sf.write(scene_master, full_dialogue, sr)

    # Copy to Artifact directory
    artifact_dir = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"
    shutil.copy2(dialogue_out, os.path.join(artifact_dir, "shorts_vs_reels_dialogue_offline_cloned.wav"))
    shutil.copy2(scene_master, os.path.join(artifact_dir, "shorts_vs_reels_master_offline_cloned.wav"))
    print(">>> [POST-PROCESSING] Successfully mirrored to Artifacts directory!")

except Exception as e:
    print(f"Error during post-processing: {e}")

