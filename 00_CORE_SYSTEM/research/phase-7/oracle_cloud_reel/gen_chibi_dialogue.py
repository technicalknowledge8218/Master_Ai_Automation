import asyncio
import os
import json
import edge_tts
import soundfile as sf
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\chibi_dialogue"
os.makedirs(OUT_DIR, exist_ok=True)

dialogue = [
    {
        "id": "line1_boy",
        "speaker": "Boy (Junior)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+18%",
        "pitch": "+6Hz",
        "text": "भैया! Oracle Cloud से मेल आया है कि मेरा फ्री सर्वर सात दिन में बंद हो जाएगा! मेरा सारा डेटा चला जाएगा क्या?!",
        "sub": "Bhaiya! OCI Free Server 7 din mein band ho jayega?! Saara data udd jayega?!"
    },
    {
        "id": "line2_sci",
        "speaker": "Scientist (Mentor)",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Arrey chill karo! Ye Oracle ki 7-day idle policy hai. Agar CPU 20 percent se kam raha toh server delete hota hai. Par board par dekho, do solid tareeqe hain!",
        "sub": "Chill karo! 7-day idle policy hai (CPU < 20%). Board par dekho, 2 hacks hain!"
    },
    {
        "id": "line3_boy",
        "speaker": "Boy (Junior)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+18%",
        "pitch": "+6Hz",
        "text": "कौनसे दो तरीके भैया? क्या कोई पैसे लगेंगे?!",
        "sub": "Kaunse do hacks bhaiya? Paise lagenge kya?!"
    },
    {
        "id": "line4_sci",
        "speaker": "Scientist (Mentor)",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Ek rupya bhi nahi! Pehla tareeqa: PAYG mein upgrade karo, Always Free par hamesha zero bill aayega! Aur doosra: terminal mein lookbusy daemon run karo taaki CPU 22 percent safe rahe!",
        "sub": "Re 1 bhi nahi! 1: PAYG upgrade ($0 bill!) | 2: lookbusy daemon (22% CPU lock!)"
    },
    {
        "id": "line5_boy",
        "speaker": "Boy (Junior)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+18%",
        "pitch": "+6Hz",
        "text": "वाह भैया! अभी रील सेव करता हूँ!",
        "sub": "Woah bhaiya! Abhi reel save karta hoon!"
    },
    {
        "id": "line6_sci",
        "speaker": "Scientist (Mentor)",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Aur comment mein likho ORACLE, poori setup commands turant bhej denge!",
        "sub": "Save Reel & Comment 'ORACLE' for Full Setup Commands!"
    }
]

async def gen_all():
    results = []
    for item in dialogue:
        tid = item["id"]
        mp3_p = os.path.join(OUT_DIR, f"{tid}.mp3")
        wav_p = os.path.join(OUT_DIR, f"{tid}.wav")
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(mp3_p)
        subprocess.run([FFMPEG, "-y", "-i", mp3_p, "-ar", "44100", "-ac", "1", wav_p], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        data, sr = sf.read(wav_p)
        dur = len(data) / sr
        print(f"Generated {tid}: {dur:.2f}s")
        item["wav"] = wav_p
        item["dur"] = dur
        results.append(item)
        
    meta_p = os.path.join(OUT_DIR, "dialogue_meta.json")
    with open(meta_p, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Saved metadata:", meta_p)

if __name__ == "__main__":
    asyncio.run(gen_all())
