import asyncio
import os
import json
import edge_tts
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\audio"
os.makedirs(out_dir, exist_ok=True)

script = [
    {
        "id": "scene1_hook",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+8%",
        "pitch": "+10Hz",
        "filter": "volume=1.05",
        "text": "लाला कंपनी में 2 साल जी-तोड़ मेहनत करने के बाद, आज अप्रेज़ल डे पर मैनेजर ने अचानक बंद केबिन में बुला लिया...",
        "sub": "Lala Company mein 2 saal ghisne ke baad, aaj appraisal day par Manager ne cabin mein bula liya...",
        "topic": "LALA COMPANY APPRAISAL DAY"
    },
    {
        "id": "scene2_manager_gaslight",
        "speaker": "Mr. Sharma (Toxic Manager)",
        "char": "sharma",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+3%",
        "pitch": "-26Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=6,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "आर्यन, काम तो ठीक है... लेकिन कंपनी के लिए ओनरशिप मिसिंग है! मार्केट डाउन है, क्लाइंट बजट काट रहे हैं... तो इस साल अप्रेज़ल तो भूल जाओ!",
        "sub": "Aryan, kaam toh theek hai... par Ownership missing hai! Market down hai, is saal appraisal bhool jao!",
        "topic": "THE GASLIGHTING TRAP"
    },
    {
        "id": "scene3_employee_shock",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+12%",
        "pitch": "+14Hz",
        "filter": "volume=1.08",
        "text": "सर, पिछले 6 महीने से हर वीकेंड 14 घंटे लॉगिन किया है! क्लाइंट ने खुद एप्रिसिएशन मेल भेजा था, और अब मार्केट डाउन का बहाना?!",
        "sub": "Sir, 6 mahine se har weekend 14 ghante login kiya! Client ne appreciation mail bheja, aur ab bahana?!",
        "topic": "THE BITTER TRUTH"
    },
    {
        "id": "scene4_manager_ultimatum",
        "speaker": "Mr. Sharma (Toxic Manager)",
        "char": "sharma",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-26Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=6,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "सुनो आर्यन, एप्रिसिएशन से कंपनी नहीं चलती! सीधा फैसला है—या तो बिना इंक्रीमेंट के 14 घंटे काम करो, या टेबल पर रेजिग्नेशन रख कर नोटिस पीरियड काउंट कर लो!",
        "sub": "Seedha faisla hai—ya toh bina hike ke 14 ghante kaam karo, ya resignation rakh do!",
        "topic": "THE TOXIC ULTIMATUM"
    },
    {
        "id": "scene5_cliffhanger",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+6%",
        "pitch": "+6Hz",
        "filter": "volume=1.05",
        "text": "घर पर ई-एम-आई का प्रेशर था, और सामने मेरी सेल्फ-रेस्पेक्ट की नीलामी हो रही थी...",
        "sub": "Ghar par EMI ka pressure tha, aur saamne meri self-respect ki auction lag rahi thi...",
        "topic": "THE MORAL DILEMMA"
    },
    {
        "id": "scene6_audience_question",
        "speaker": "Aryan (Employee)",
        "char": "aryan",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+9%",
        "pitch": "+12Hz",
        "filter": "volume=1.05",
        "text": "अगर मेरी जगह तुम होते, तो ई-एम-आई के डर से झुक जाते या रेजिग्नेशन देकर सेल्फ-रेस्पेक्ट चुनते? अपना जवाब कमेंट करो, और मैंने क्या किया... देखो पार्ट 2 में!",
        "sub": "Agar meri jagah tum hote toh kya karte? Comment your answer! Maine kya kiya... dekho Part 2 mein!",
        "topic": "WHAT WOULD YOU DO? (PART 2 TOMORROW)"
    }
]

async def gen():
    for item in script:
        raw_mp3 = os.path.join(out_dir, f"{item['id']}_raw.mp3")
        final_wav = os.path.join(out_dir, f"{item['id']}.wav")
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(raw_mp3)
        cmd = f'"{ffmpeg_exe}" -y -i "{raw_mp3}" -af "{item["filter"]}" -ar 44100 -ac 1 "{final_wav}"'
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        probe = subprocess.run(f'"{ffmpeg_exe}" -i "{final_wav}" 2>&1', shell=True, capture_output=True, text=True)
        dur = 0.0
        for line in probe.stdout.splitlines():
            if "Duration:" in line:
                part = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = part.split(":")
                dur = float(h)*3600 + float(m)*60 + float(s)
                break
        item["wav"] = final_wav
        item["dur"] = dur
        print(f"{item['id']}: {dur:.2f}s | {item['speaker']}")

    meta_path = os.path.join(out_dir, "corporate_drama_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    print(f"Corporate audio metadata saved to: {meta_path}")

if __name__ == "__main__":
    asyncio.run(gen())
