"""
Generate 100% Pure Conversational Devanagari Hindi Audio with distinct Boy and Mentor personas.
"""
import asyncio
import os
import json
import subprocess
import edge_tts
import imageio_ffmpeg

WORK_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"
AUDIO_DIR = os.path.join(WORK_DIR, "animated_audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# Exact dialogue lines crafted with 100% Devanagari phonetics for natural Indian cadence
SCRIPT_LINES = [
    {
        "id": "line1_boy",
        "speaker": "Rohan (Junior Dev)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+12%",
        "pitch": "+22Hz",
        "filter": "volume=1.05",
        "text": "भैया! ऑरेकल क्लाउड से मेल आया है कि मेरा फ्री सर्वर 7 दिन में बंद हो जाएगा! सच में सारा डेटा उड़ जाएगा क्या?!",
        "sub": "Bhaiya! OCI Free Server 7 din mein band ho jayega?! Saara data udd jayega?!"
    },
    {
        "id": "line2_sci",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-22Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "अरे चिल करो! कोई डेटा नहीं उड़ेगा। ऑरेकल का रूल है कि अगर 7 दिन तक सीपीयू 20 परसेंट से कम रहा, तो वो सर्वर को आइडल मानकर रिक्लेम कर लेते हैं। लेकिन बोर्ड पर देख, इसके 2 सॉलिड हैक्स हैं!",
        "sub": "Chill karo! 7-day idle rule hai (CPU < 20%). Board par dekho, 2 solid hacks hain!"
    },
    {
        "id": "line3_boy",
        "speaker": "Rohan (Junior Dev)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+10%",
        "pitch": "+20Hz",
        "filter": "volume=1.05",
        "text": "कौनसे दो हैक्स भैया? क्या कोई पैसे लगेंगे?!",
        "sub": "Kaunse do hacks bhaiya? Paise lagenge kya?!"
    },
    {
        "id": "line4_sci",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-22Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "अरे 1 रुपया भी नहीं लगेगा! पहला हैक—अकाउंट को पे-ऐज़-यू-गो में अपग्रेड कर लो, ऑलवेज़-फ्री रिसोर्सेज़ पर बिल हमेशा ₹0 आएगा। और दूसरा—टर्मिनल में लुक-बिज़ी डेमन रन कर दो, सीपीयू हमेशा 22 परसेंट पर लॉक रहेगा!",
        "sub": "Re 1 bhi nahi! 1: PAYG upgrade ($0 bill!) | 2: lookbusy daemon (22% CPU lock!)"
    },
    {
        "id": "line5_boy",
        "speaker": "Rohan (Junior Dev)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+12%",
        "pitch": "+22Hz",
        "filter": "volume=1.05",
        "text": "वाह भैया! अभी रील सेव करता हूँ!",
        "sub": "Woah bhaiya! Abhi reel save karta hoon!"
    },
    {
        "id": "line6_sci",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-22Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "और कमेंट में लिखो ऑरेकल, पूरी सेटअप कमांड्स और स्क्रिप्ट इनबॉक्स में तुरंत मिल जाएगी!",
        "sub": "Save Reel & Comment 'ORACLE' for Full Setup Commands!"
    }
]

async def generate_all():
    dialogue_meta = []
    for line in SCRIPT_LINES:
        raw_wav = os.path.join(AUDIO_DIR, f"raw_{line['id']}.wav")
        proc_wav = os.path.join(AUDIO_DIR, f"{line['id']}.wav")
        
        # 1. Edge-TTS Generation
        comm = edge_tts.Communicate(line["text"], line["voice"], rate=line["rate"], pitch=line["pitch"])
        await comm.save(raw_wav)
        
        # 2. FFmpeg audio post-processing (persona equalization & warmth)
        cmd = [
            ffmpeg_exe, "-y",
            "-i", raw_wav,
            "-af", line["filter"],
            "-ar", "44100",
            "-ac", "1",
            proc_wav
        ]
        subprocess.run(cmd, check=True)
        
        # 3. Get exact duration
        dur_cmd = [
            ffmpeg_exe, "-i", proc_wav
        ]
        res = subprocess.run(dur_cmd, stderr=subprocess.PIPE, text=True)
        dur = 0.0
        for l in res.stderr.splitlines():
            if "Duration:" in l:
                t_str = l.split("Duration:")[1].split(",")[0].strip()
                h, m, s = t_str.split(":")
                dur = float(h)*3600 + float(m)*60 + float(s)
                break
                
        line_copy = dict(line)
        line_copy["wav"] = proc_wav
        line_copy["dur"] = round(dur, 2)
        dialogue_meta.append(line_copy)
        print(f"Generated {line['id']}: {dur:.2f}s ({line['speaker']})")
        
    meta_path = os.path.join(AUDIO_DIR, "animated_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(dialogue_meta, f, indent=2, ensure_ascii=False)
    print("Metadata Saved:", meta_path)

if __name__ == "__main__":
    asyncio.run(generate_all())
