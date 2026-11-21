import asyncio
import os
import json
import soundfile as sf
import subprocess
import imageio_ffmpeg
import edge_tts

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\test_lalaji_reel\audio"

scenes = [
    {
        "id": "scene1_hook",
        "speaker": "Chintu",
        "char": "chintu",
        "badge": "CHINTU",
        "text": "सर पूरे एक साल बिना किसी छुट्टी के काम करने के बाद मुझे सिर्फ तीन दिन की सिक लीव चाहिए।",
        "sub": "Sir, 1 saal non-stop kaam ke baad mujhe sirf 3 din ki sick leave chahiye!",
        "topic": "UNLIMITED LEAVE SCAM",
        "hud_pill": "// 01 · HR PROMISE",
        "rate": "+6%",
        "is_lalaji": False
    },
    {
        "id": "scene2_lalaji",
        "speaker": "Lala Ji (Boss)",
        "char": "lalaji",
        "badge": "LALA JI",
        "text": "अरे चिंटू सिक लीव? अपनी कंपनी में तो अनलिमिटेड लीव पॉलिसी है फिर भी तुम गिड़गिड़ा रहे हो?",
        "sub": "Chintu, apni company mein Unlimited Leave Policy hai, phir bhi gidgida rahe ho?",
        "topic": "THE LALA LOGIC",
        "hud_pill": "// 02 · LALA LOGIC",
        "rate": "-1%",
        "is_lalaji": True
    },
    {
        "id": "scene3_shock",
        "speaker": "Chintu",
        "char": "chintu",
        "badge": "CHINTU",
        "text": "लेकिन सर जब भी पोर्टल पर अप्लाई करता हूं मैनेजर तुरंत रिजेक्ट का बटन दबा देता है।",
        "sub": "Lekin sir, portal par apply karte hi Manager turant REJECT daba deta hai!",
        "topic": "PORTAL REALITY",
        "hud_pill": "// 03 · THE TRAP",
        "rate": "+6%",
        "is_lalaji": False
    },
    {
        "id": "scene4_punchline",
        "speaker": "Lala Ji (Boss)",
        "char": "lalaji",
        "badge": "LALA JI",
        "text": "अरे नादान अनलिमिटेड का मतलब छुट्टी लेना नहीं होता बल्कि कंपनी कभी भी छुट्टी कैंसिल कर सकती है यह होता है। मंडे को ऑफिस आओ वरना परमानेंट छुट्टी पर चले जाओ।",
        "sub": "Unlimited ka matlab chutti lena nahi, company kabhi bhi cancel kar sakti hai ye hota hai! Monday ko aao ya resign karo!",
        "topic": "THE PUNCHLINE",
        "hud_pill": "// 04 · ULTIMATUM",
        "rate": "+0%",
        "is_lalaji": True
    },
    {
        "id": "scene5_cta",
        "speaker": "Chintu",
        "char": "chintu",
        "badge": "CHINTU",
        "text": "क्या आपकी कंपनी में भी ऐसा ही लाला कल्चर चलता है? अपना दर्द नीचे कमेंट में शेयर करो।",
        "sub": "Kya aapki company mein bhi aisa Lala Culture hai? Comment karke apna dard share karo!",
        "topic": "AUDIENCE VOTE",
        "hud_pill": "// 05 · VOTE NOW",
        "rate": "+6%",
        "is_lalaji": False
    }
]

async def generate_speech():
    meta = []
    for sc in scenes:
        raw_mp3 = os.path.join(AUDIO_DIR, f"{sc['id']}_raw.mp3")
        raw_wav = os.path.join(AUDIO_DIR, f"{sc['id']}_raw.wav")
        out_wav = os.path.join(AUDIO_DIR, f"{sc['id']}_mastered.wav")

        comm = edge_tts.Communicate(sc["text"], "hi-IN-MadhurNeural", rate=sc["rate"])
        await comm.save(raw_mp3)

        # Convert to WAV
        subprocess.run([ffmpeg_exe, "-y", "-i", raw_mp3, "-ac", "1", "-ar", "44100", raw_wav], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Broadcast Vocal Mastering
        if sc["is_lalaji"]:
            # Lalaji: authoritative low-end warmth + power
            af = "highpass=f=70,equalizer=f=135:t=q:w=1:g=5,equalizer=f=3000:t=q:w=1:g=2,volume=1.12"
        else:
            # Chintu: crisp clarity
            af = "highpass=f=80,equalizer=f=3200:t=q:w=1:g=2.2,volume=1.06"

        subprocess.run([ffmpeg_exe, "-y", "-i", raw_wav, "-af", af, out_wav], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        data, sr = sf.read(out_wav)
        dur = round(len(data) / sr, 2)
        sc_data = dict(sc)
        sc_data["wav"] = out_wav
        sc_data["dur"] = dur
        meta.append(sc_data)
        print(f"Generated {sc['id']}: {dur}s | {sc['speaker']}")

    with open(os.path.join(AUDIO_DIR, "reel_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("All audio tracks mastered & metadata saved.")

if __name__ == "__main__":
    asyncio.run(generate_speech())
