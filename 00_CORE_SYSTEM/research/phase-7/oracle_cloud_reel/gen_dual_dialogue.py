import asyncio
import edge_tts
import os
import json
import soundfile as sf
import numpy as np

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\dual_dialogue_v4"
os.makedirs(out_dir, exist_ok=True)

dialogue_script = [
    {
        "id": "turn1_junior_panic",
        "speaker": "Junior",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+3Hz",
        "text": "भैया! मेरा Oracle Cloud का फ्री सर्वर सात दिन में डिलीट होने वाला है! मेल आ गया! अब मेरा सारा डेटा चला जाएगा क्या?!",
        "subtitle": "Junior: भैया! मेरा Free Server 7 din mein DELETE ho jayega?!",
        "char": "arjun_shocked.png",
        "camera": "JUNIOR_CLOSEUP",
        "bg": (38, 16, 24, 255),
        "tag": "CRITICAL ALARM",
        "sfx": "alarm.wav"
    },
    {
        "id": "turn2_senior_explain_rule",
        "speaker": "Senior",
        "voice": "ur-PK-AsadNeural",
        "rate": "+10%",
        "pitch": "-1Hz",
        "text": "अरे अर्जुन, शांत हो जाओ! ये ओरेकल की आइडल रिक्लेमेशन पॉलिसी है। अगर सात दिन तक सीपीयू 20% से कम रहा, तो वो सर्वर बंद कर देते हैं। लेकिन इसको लाइफटाइम सेफ रखने के दो पक्के हैक हैं!",
        "subtitle": "Senior: OCI Rule: 7 din CPU < 20% raha toh delete! Par 2 hacks hain!",
        "char": "dr_kabir_warning.png",
        "camera": "SENIOR_EXPLAIN",
        "bg": (20, 24, 40, 255),
        "tag": "IDLE RULE EXPLAINED",
        "sfx": "pop.wav"
    },
    {
        "id": "turn3_junior_ask_payg",
        "speaker": "Junior",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+4Hz",
        "text": "कौनसा हैक भैया? कोई पैसे लगेंगे क्या? कोई सब्सक्रिप्शन लेना पड़ेगा?!",
        "subtitle": "Junior: Konsa hack bhaiya? Paise lagenge ya subscription?!",
        "char": "arjun_shrug.png",
        "camera": "JUNIOR_REACTION",
        "bg": (28, 20, 45, 255),
        "tag": "THE QUESTION",
        "sfx": "pop.wav"
    },
    {
        "id": "turn4_senior_payg_fix",
        "speaker": "Senior",
        "voice": "ur-PK-AsadNeural",
        "rate": "+10%",
        "pitch": "-1Hz",
        "text": "एक रुपया भी नहीं! पहला और बेस्ट तरीका: अपने अकाउंट को Pay As You Go में अपग्रेड कर दो। Always Free रिसोर्सेज़ पर ज़ीरो रुपया चार्ज लगता है, और PAYG सर्वर्स को ओरेकल कभी डिलीट नहीं करता!",
        "subtitle": "Senior: Method 1: Upgrade to PAYG ($0 Bill Forever & Lifetime Safe!)",
        "char": "dr_kabir_proud.png",
        "camera": "SENIOR_PAYG",
        "bg": (10, 35, 26, 255),
        "tag": "100% PERMANENT FIX",
        "sfx": "chime.wav"
    },
    {
        "id": "turn5_junior_ask_nocard",
        "speaker": "Junior",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+14%",
        "pitch": "+3Hz",
        "text": "और अगर किसी के पास क्रेडिट कार्ड ना हो, तब क्या करें?",
        "subtitle": "Junior: Aur agar credit card na lagana ho toh?",
        "char": "arjun_shrug.png",
        "camera": "JUNIOR_REACTION",
        "bg": (25, 20, 35, 255),
        "tag": "NO-CARD OPTION?",
        "sfx": "pop.wav"
    },
    {
        "id": "turn6_senior_terminal_fix",
        "speaker": "Senior",
        "voice": "ur-PK-AsadNeural",
        "rate": "+10%",
        "pitch": "-1Hz",
        "text": "तब सर्वर के टर्मिनल में लुकबिज़ी डेमन रन करो! ये सीपीयू को हमेशा 22% पर लॉक रखेगा ताकि ओरेकल को लगे सर्वर एक्टिव है!",
        "subtitle": "Senior: Method 2: Terminal mein 'lookbusy' daemon run karo (CPU 22% Safe Lock!)",
        "char": "dr_kabir_tablet.png",
        "camera": "TERMINAL_ANIMATED",
        "bg": (13, 17, 23, 255),
        "tag": "CLI AUTOMATION",
        "sfx": "typing.wav"
    },
    {
        "id": "turn7_outro_duo",
        "speaker": "Duo",
        "voice_j": "hi-IN-MadhurNeural",
        "voice_s": "ur-PK-AsadNeural",
        "rate_j": "+14%",
        "rate_s": "+10%",
        "text_j": "वाह भैया, मज़ा आ गया! अभी रील सेव करता हूँ!",
        "text_s": "और कमेंट में लिखो ORACLE, पूरी सेटअप कमांड्स डीएम कर देंगे!",
        "subtitle": "Save Reel & Comment 'ORACLE' for Full Setup Commands!",
        "char_j": "arjun_thumbsup.png",
        "char_s": "dr_kabir_explaining.png",
        "camera": "DUO_OUTRO",
        "bg": (15, 23, 42, 255),
        "tag": "SAVE & SHARE",
        "sfx": "chime.wav"
    }
]

async def generate_dialogue():
    meta = []
    total_dur = 0.0
    
    for item in dialogue_script:
        tid = item["id"]
        if tid != "turn7_outro_duo":
            comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
            f_mp3 = os.path.join(out_dir, f"{tid}.mp3")
            await comm.save(f_mp3)
            data, sr = sf.read(f_mp3)
            if len(data.shape) > 1: data = data.mean(axis=1)
            f_wav = os.path.join(out_dir, f"{tid}.wav")
            sf.write(f_wav, data, sr)
            dur = len(data) / sr
            total_dur += dur
            print(f"Generated {tid} ({item['speaker']}): {dur:.2f}s")
            meta.append({"id": tid, "speaker": item["speaker"], "dur": dur, "wav": f_wav, "config": item})
        else:
            # Outro has two quick lines: Junior then Senior
            comm_j = edge_tts.Communicate(item["text_j"], item["voice_j"], rate=item["rate_j"], pitch="+3Hz")
            comm_s = edge_tts.Communicate(item["text_s"], item["voice_s"], rate=item["rate_s"], pitch="-1Hz")
            f_j_mp3 = os.path.join(out_dir, "turn7_j.mp3")
            f_s_mp3 = os.path.join(out_dir, "turn7_s.mp3")
            await comm_j.save(f_j_mp3)
            await comm_s.save(f_s_mp3)
            
            dj, sr_j = sf.read(f_j_mp3)
            ds, sr_s = sf.read(f_s_mp3)
            if len(dj.shape) > 1: dj = dj.mean(axis=1)
            if len(ds.shape) > 1: ds = ds.mean(axis=1)
            
            # Combine with 0.15s gap
            gap = np.zeros(int(0.15 * sr_j), dtype=np.float32)
            comb = np.concatenate([dj, gap, ds])
            f_wav = os.path.join(out_dir, "turn7_outro_duo.wav")
            sf.write(f_wav, comb, sr_j)
            dur = len(comb) / sr_j
            total_dur += dur
            print(f"Generated turn7_outro_duo (Duo): {dur:.2f}s")
            meta.append({"id": tid, "speaker": "Duo", "dur": dur, "wav": f_wav, "config": item})
            
    with open(os.path.join(out_dir, "dialogue_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        
    print(f"\nALL CONVERSATIONAL TRACKS GENERATED! Total Audio Duration: {total_dur:.2f}s")

asyncio.run(generate_dialogue())
