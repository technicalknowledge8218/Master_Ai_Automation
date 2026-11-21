import asyncio
import edge_tts
import os
import json
import soundfile as sf
import numpy as np

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\dialogue_neha_kabir"
os.makedirs(out_dir, exist_ok=True)

# Junior: Neha (Young Indian Female Developer, energetic & worried): hi-IN-SwaraNeural
# Senior: Dr. Kabir (Senior Indian Male Architect, calm & authoritative): en-IN-PrabhatNeural

dialogue_script = [
    {
        "id": "turn1_neha_panic",
        "speaker": "Neha (Junior)",
        "char_type": "neha",
        "char_sprite": "neha_shocked.png",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+15%",
        "pitch": "+2Hz",
        "text": "भैया! मेरा Oracle Cloud का फ्री सर्वर सात दिन में डिलीट होने वाला है! मेल आ गया! अब मेरा सारा डेटा चला जाएगा क्या?!",
        "subtitle": "Neha: भैया! मेरा Free Server 7 din mein DELETE ho jayega?!",
        "camera": "NEHA_SPOTLIGHT",
        "bg": (38, 16, 24, 255),
        "tag": "CRITICAL EMERGENCY",
        "sfx": "alarm.wav"
    },
    {
        "id": "turn2_kabir_explain",
        "speaker": "Dr. Kabir (Senior)",
        "char_type": "kabir",
        "char_sprite": "dr_kabir_warning.png",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Neha, chill karo! Ye Oracle ki idle reclamation policy hai. Agar 7 din CPU 20 percent se kam raha, toh server terminate ho jata hai. Lekin isko lifetime safe rakhne ke do solid hacks hain!",
        "subtitle": "Dr. Kabir: OCI Rule: 7 din CPU < 20% raha toh delete! Par 2 hacks hain!",
        "camera": "KABIR_EXPLAIN",
        "bg": (20, 24, 40, 255),
        "tag": "IDLE RULE EXPLAINED",
        "sfx": "pop.wav"
    },
    {
        "id": "turn3_neha_question",
        "speaker": "Neha (Junior)",
        "char_type": "neha",
        "char_sprite": "neha_pointing.png",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+15%",
        "pitch": "+3Hz",
        "text": "कौनसा हैक भैया? कोई पैसे लगेंगे क्या? कोई सब्सक्रिप्शन लेना पड़ेगा?!",
        "subtitle": "Neha: Konsa hack bhaiya? Paise lagenge ya subscription?!",
        "camera": "NEHA_QUESTION",
        "bg": (28, 20, 45, 255),
        "tag": "THE BIG QUESTION",
        "sfx": "pop.wav"
    },
    {
        "id": "turn4_kabir_payg",
        "speaker": "Dr. Kabir (Senior)",
        "char_type": "kabir",
        "char_sprite": "dr_kabir_proud.png",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Ek rupya bhi nahi! Pehla aur best tareeqa: Apne account ko Pay As You Go mein upgrade kar do. Always Free resources par zero rupee charge lagta hai, aur PAYG servers ko Oracle kabhi delete nahi karta!",
        "subtitle": "Dr. Kabir: Method 1: Upgrade to PAYG ($0 Bill Forever & Lifetime Safe!)",
        "camera": "KABIR_PAYG",
        "bg": (10, 35, 26, 255),
        "tag": "100% PERMANENT FIX",
        "sfx": "chime.wav"
    },
    {
        "id": "turn5_neha_nocard",
        "speaker": "Neha (Junior)",
        "char_type": "neha",
        "char_sprite": "neha_laptop.png",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+15%",
        "pitch": "+2Hz",
        "text": "और अगर किसी के पास क्रेडिट कार्ड ना हो, तब क्या करें?",
        "subtitle": "Neha: Aur agar credit card na lagana ho toh?",
        "camera": "NEHA_QUESTION",
        "bg": (25, 20, 35, 255),
        "tag": "NO-CARD OPTION?",
        "sfx": "pop.wav"
    },
    {
        "id": "turn6_kabir_terminal",
        "speaker": "Dr. Kabir (Senior)",
        "char_type": "kabir",
        "char_sprite": "dr_kabir_tablet.png",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+12%",
        "pitch": "-2Hz",
        "text": "Tab server ke terminal mein lookbusy daemon run karo! Ye CPU ko hamesha 22 percent par lock rakhega taaki Oracle ko lage server active hai!",
        "subtitle": "Dr. Kabir: Method 2: Terminal mein 'lookbusy' daemon run karo (CPU 22% Safe Lock!)",
        "camera": "TERMINAL_ANIMATED",
        "bg": (13, 17, 23, 255),
        "tag": "CLI AUTOMATION",
        "sfx": "typing.wav"
    },
    {
        "id": "turn7_duo_outro",
        "speaker": "Duo",
        "voice_n": "hi-IN-SwaraNeural",
        "voice_k": "en-IN-PrabhatNeural",
        "rate_n": "+15%",
        "rate_k": "+12%",
        "text_n": "वाह भैया, मज़ा आ गया! अभी रील सेव करती हूँ!",
        "text_k": "Aur comment mein likho ORACLE, poori setup commands DM kar denge!",
        "subtitle": "Save Reel & Comment 'ORACLE' for Full Setup Commands!",
        "char_n": "neha_peace.png",
        "char_k": "dr_kabir_explaining.png",
        "camera": "DUO_OUTRO",
        "bg": (15, 23, 42, 255),
        "tag": "SAVE & SHARE",
        "sfx": "chime.wav"
    }
]

async def gen_all():
    meta = []
    total_dur = 0.0
    for item in dialogue_script:
        tid = item["id"]
        if tid != "turn7_duo_outro":
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
            comm_n = edge_tts.Communicate(item["text_n"], item["voice_n"], rate=item["rate_n"], pitch="+2Hz")
            comm_k = edge_tts.Communicate(item["text_k"], item["voice_k"], rate=item["rate_k"], pitch="-2Hz")
            f_n_mp3 = os.path.join(out_dir, "turn7_n.mp3")
            f_k_mp3 = os.path.join(out_dir, "turn7_k.mp3")
            await comm_n.save(f_n_mp3)
            await comm_k.save(f_k_mp3)
            dn, sr_n = sf.read(f_n_mp3)
            dk, sr_k = sf.read(f_k_mp3)
            if len(dn.shape) > 1: dn = dn.mean(axis=1)
            if len(dk.shape) > 1: dk = dk.mean(axis=1)
            
            gap = np.zeros(int(0.12 * sr_n), dtype=np.float32)
            comb = np.concatenate([dn, gap, dk])
            f_wav = os.path.join(out_dir, "turn7_duo_outro.wav")
            sf.write(f_wav, comb, sr_n)
            dur = len(comb) / sr_n
            total_dur += dur
            print(f"Generated turn7_duo_outro (Duo): {dur:.2f}s")
            meta.append({"id": tid, "speaker": "Duo", "dur": dur, "wav": f_wav, "config": item})
            
    with open(os.path.join(out_dir, "dialogue_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        
    print(f"\nALL 7 DIALOGUE TRACKS GENERATED! Total Audio Duration: {total_dur:.2f}s")

asyncio.run(gen_all())
