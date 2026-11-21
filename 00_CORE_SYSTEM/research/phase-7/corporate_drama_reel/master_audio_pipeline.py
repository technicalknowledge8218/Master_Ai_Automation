import subprocess
import os
import json
import soundfile as sf
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\audio"

scenes_config = [
    {
        "id": "scene1_hook",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "sub": "Lala Company mein 2 saal din raat mehnat ke baad, appraisal day par cabin mein bulaya...",
        "topic": "LALA COMPANY APPRAISAL DAY",
        "in_wav": "scene1_fluent.wav",
        "out_wav": "scene1_mastered.wav",
        "is_sharma": False
    },
    {
        "id": "scene2_manager_gaslight",
        "speaker": "Mr. Sharma (Manager)",
        "char": "sharma",
        "sub": "Aryan, kaam theek hai par ownership missing hai! Market down hai, appraisal bhool jao!",
        "topic": "THE GASLIGHTING TRAP",
        "in_wav": "scene2_fluent.wav",
        "out_wav": "scene2_mastered.wav",
        "is_sharma": True
    },
    {
        "id": "scene3_employee_shock",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "sub": "Sir, 6 mahine se har weekend 14 ghante login kiya! Client ne khud appreciation mail bheja!",
        "topic": "THE BITTER TRUTH (PROOF)",
        "in_wav": "scene3_fluent.wav",
        "out_wav": "scene3_mastered.wav",
        "is_sharma": False
    },
    {
        "id": "scene4_manager_ultimatum",
        "speaker": "Mr. Sharma (Manager)",
        "char": "sharma",
        "sub": "Seedha faisla hai—ya 0% hike par 14 ghante kaam karo, ya resignation rakh do!",
        "topic": "THE TOXIC ULTIMATUM",
        "in_wav": "scene4_fluent.wav",
        "out_wav": "scene4_mastered.wav",
        "is_sharma": True
    },
    {
        "id": "scene5_cliffhanger",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "sub": "Ghar par Rs 45,000 EMI ka pressure tha, aur samne meri self-respect ki nilami ho rahi thi...",
        "topic": "THE MORAL DILEMMA",
        "in_wav": "scene5_fluent.wav",
        "out_wav": "scene5_mastered.wav",
        "is_sharma": False
    },
    {
        "id": "scene6_audience_question",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "sub": "Agar meri jagah aap hote toh kya karte? Comment karein, aur maine kya kiya... dekho Part 2 mein!",
        "topic": "WHAT WOULD YOU DO? (PART 2)",
        "in_wav": "scene6_fluent.wav",
        "out_wav": "scene6_mastered.wav",
        "is_sharma": False
    }
]

meta_list = []
for sc in scenes_config:
    in_p = os.path.join(AUDIO_DIR, sc["in_wav"])
    out_p = os.path.join(AUDIO_DIR, sc["out_wav"])
    if sc["is_sharma"]:
        # Deep authoritative warmth without pitch distortion
        af = "highpass=f=70,equalizer=f=135:t=q:w=1:g=4.5,equalizer=f=3000:t=q:w=1:g=1.5,volume=1.1"
    else:
        # Crisp youth clarity
        af = "highpass=f=80,equalizer=f=3200:t=q:w=1:g=2,volume=1.05"
        
    subprocess.run([ffmpeg_exe, "-y", "-i", in_p, "-af", af, out_p], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data, sr = sf.read(out_p)
    dur = round(len(data) / sr, 2)
    meta_list.append({
        "id": sc["id"],
        "speaker": sc["speaker"],
        "char": sc["char"],
        "sub": sc["sub"],
        "topic": sc["topic"],
        "wav": out_p,
        "dur": dur
    })
    print(f"{sc['id']}: {dur}s | {sc['speaker']}")

with open(os.path.join(AUDIO_DIR, "corporate_drama_meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta_list, f, ensure_ascii=False, indent=2)
print("Updated corporate_drama_meta.json successfully")
