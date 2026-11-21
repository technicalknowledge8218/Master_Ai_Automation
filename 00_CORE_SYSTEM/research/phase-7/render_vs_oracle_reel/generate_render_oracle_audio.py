import asyncio
import os
import json
import edge_tts
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\render_vs_oracle_reel\audio"
os.makedirs(out_dir, exist_ok=True)

dialogues = [
    {
        "id": "line1_boy",
        "speaker": "Rohan (Junior Dev)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+12%",
        "pitch": "+24Hz",
        "filter": "volume=1.05",
        "text": "भैया! अपनी फुल-स्टैक बैकएंड ऐप डिप्लॉय करनी है! रेंडर पर डालूँ या ऑरेकल क्लाउड पर? किसमें जीरो बिल आएगा?!",
        "sub": "Bhaiya! Fullstack App Render pe host karun ya Oracle Cloud pe?!",
        "base_frame": "frame_1.0s.jpg",
        "speaking": "boy"
    },
    {
        "id": "line2_sci",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-24Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "अरे ध्यान से सुन! रेंडर पर डिप्लॉय करना आसान है, वन-क्लिक में हो जाता है। लेकिन फ्री टियर में सिर्फ 512 एमबी रैम मिलती है, और 15 मिनट बाद सर्वर सो जाता है—यानी पूरे 50 सेकंड का कोल्ड स्टार्ट!",
        "sub": "Render pe 1-click deploy hai, par 512MB RAM aur 15 min baad server so jata hai!",
        "base_frame": "frame_20.0s.jpg",
        "speaking": "sci"
    },
    {
        "id": "line3_boy",
        "speaker": "Rohan (Junior Dev)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+12%",
        "pitch": "+24Hz",
        "filter": "volume=1.05",
        "text": "अरे बाप रे! मतलब डिस्कॉर्ड बॉट या डेटाबेस डाला तो बार-बार बंद हो जाएगा?! तो फिर ऑरेकल क्लाउड में क्या मिलता है?!",
        "sub": "Matlab Discord bot ya DB band ho jayega?! Aur Oracle mein kya milta hai?!",
        "base_frame": "frame_12.0s.jpg",
        "speaking": "boy"
    },
    {
        "id": "line4_sci",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-24Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "ऑरेकल क्लाउड एक असली मॉन्स्टर है! इसमें फ्री टियर में 4 ओ-सी-पी-यू, 24 जीबी रैम और 200 जीबी एसएसडी मिलती है! और सर्वर कभी सोता नहीं, 24 घंटे ऑलवेज़-ऑन चालू रहता है!",
        "sub": "Oracle ek monster hai! 4 OCPU, 24GB RAM, 200GB SSD aur 24/7 Always-ON!",
        "base_frame": "frame_25.0s.jpg",
        "speaking": "sci"
    },
    {
        "id": "line5_sci",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-24Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "तो सीधा रूल—क्विक पोर्टफोलियो या हॉबी प्रोजेक्ट के लिए रेंडर बेस्ट है। लेकिन सीरियस 24 घंटे चलने वाले बैकएंड, बॉट्स और डेटाबेस के लिए ऑरेकल क्लाउड फ्री टियर चुनो!",
        "sub": "Quick hobby project -> Render | 24/7 Backend & DB -> Oracle Cloud Free Tier!",
        "base_frame": "frame_35.0s.jpg",
        "speaking": "sci"
    },
    {
        "id": "line6_duo",
        "speaker": "Dr. Billu (Cloud Mentor)",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "-24Hz",
        "filter": "equalizer=f=120:width_type=o:w=1:g=5,equalizer=f=3200:width_type=o:w=1:g=2,volume=1.15",
        "text": "इस रील को अभी सेव करो और कमेंट में लिखो COMPARE, दोनों का फुल सेटअप गाइड तुम्हारे इनबॉक्स में तुरंत मिल जाएगा!",
        "sub": "Save Reel & Comment 'COMPARE' for Step-by-Step Setup Guide!",
        "base_frame": "frame_30.0s.jpg",
        "speaking": "sci"
    }
]

async def gen():
    for item in dialogues:
        raw_mp3 = os.path.join(out_dir, f"{item['id']}_raw.mp3")
        final_wav = os.path.join(out_dir, f"{item['id']}.wav")
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(raw_mp3)
        cmd = f'"{ffmpeg_exe}" -y -i "{raw_mp3}" -af "{item["filter"]}" -ar 44100 -ac 1 "{final_wav}"'
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        probe = subprocess.run(f'"{ffmpeg_exe}" -i "{final_wav}" 2>&1', shell=True, capture_output=True, text=True)
        # Parse duration from ffmpeg output
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

    meta_path = os.path.join(out_dir, "render_vs_oracle_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(dialogues, f, indent=2, ensure_ascii=False)
    print(f"Metadata written to {meta_path}")

if __name__ == "__main__":
    asyncio.run(gen())
