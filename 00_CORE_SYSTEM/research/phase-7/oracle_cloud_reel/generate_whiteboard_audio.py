import asyncio
import os
import json
import edge_tts
import soundfile as sf
import subprocess

OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\whiteboard_test_audio"
os.makedirs(OUT_DIR, exist_ok=True)

FFMPEG = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
if not os.path.exists(FFMPEG):
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

lines = [
    {
        "id": "turn1_neha",
        "speaker": "Neha (Junior)",
        "char_type": "neha",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+15%",
        "pitch": "+2Hz",
        "text": "भैया! Oracle Cloud का मेरा फ्री सर्वर डिलीट हो जाएगा क्या?! मेल आया है कि सात दिन में बंद हो जाएगा!",
        "sub": "Neha: Bhaiya! Mera Free Server 7 din mein DELETE ho jayega?! Mail aaya hai!"
    },
    {
        "id": "turn2_kabir",
        "speaker": "Dr. Kabir (Senior)",
        "char_type": "kabir",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Neha chill karo! Ye Oracle ka idle rule hai—agar CPU 20 percent se kam raha toh reclaim hota hai. Par board par dekho, do solid hacks hain!",
        "sub": "Dr. Kabir: Chill karo! OCI ka 7-day idle rule hai. Board par dekho, 2 hacks hain!"
    },
    {
        "id": "turn3_neha",
        "speaker": "Neha (Junior)",
        "char_type": "neha",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+15%",
        "pitch": "+3Hz",
        "text": "कौनसे दो तरीके भैया? क्या कोई पैसे लगेंगे?!",
        "sub": "Neha: Kaunse do hacks bhaiya? Paise lagenge kya?!"
    },
    {
        "id": "turn4_kabir",
        "speaker": "Dr. Kabir (Senior)",
        "char_type": "kabir",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Ek rupya bhi nahi! Pehla tareeqa: PAYG mein upgrade karo, bill hamesha zero aayega. Doosra: terminal mein lookbusy daemon run karo—CPU hamesha 22 percent safe rahega!",
        "sub": "Dr. Kabir: Method 1: PAYG upgrade ($0 bill!) | Method 2: lookbusy 22% CPU lock!"
    }
]

async def gen_all():
    results = []
    for item in lines:
        tid = item["id"]
        mp3_p = os.path.join(OUT_DIR, f"{tid}.mp3")
        wav_p = os.path.join(OUT_DIR, f"{tid}.wav")
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(mp3_p)
        
        # Convert to WAV
        subprocess.run([FFMPEG, "-y", "-i", mp3_p, "-ar", "44100", "-ac", "1", wav_p], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        data, sr = sf.read(wav_p)
        dur = len(data) / sr
        print(f"Generated {tid}: {dur:.2f}s")
        item["wav"] = wav_p
        item["dur"] = dur
        results.append(item)
        
    meta_p = os.path.join(OUT_DIR, "whiteboard_meta.json")
    with open(meta_p, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Saved metadata:", meta_p)

if __name__ == "__main__":
    asyncio.run(gen_all())
