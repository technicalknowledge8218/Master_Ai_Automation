import asyncio
import edge_tts
import os
import json

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\audio"
os.makedirs(out_dir, exist_ok=True)

# Full Script for the Reel (Conversational Hinglish Tech Creator Style)
dialogue_script = [
    {
        "id": "scene1_hook",
        "speaker": "Host",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+10%",
        "pitch": "+2Hz",
        "text": "Agar aap Oracle Cloud ka Free Tier VM use kar rahe ho, toh dhyan se sunna! Saat din ke andar aapka server automatic DELETE ho sakta hai!",
        "subtitle": "Oracle Cloud Free Tier VM DELETE ho jayega?!",
        "visual_type": "ALERT_HOOK"
    },
    {
        "id": "scene2_problem",
        "speaker": "Host",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+10%",
        "pitch": "+1Hz",
        "text": "Kyunki Oracle ki ek strict policy hai: agar aapka CPU usage satatar din tak 20% se kam raha, toh Oracle use IDLE samajhkar instance terminate kar deta hai aur aapka sara data gaya!",
        "subtitle": "Oracle Idle Reclamation: CPU < 20% = INSTANCE TERMINATED!",
        "visual_type": "CPU_METER_ALERT"
    },
    {
        "id": "scene3_fix1_payg",
        "speaker": "Host",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+8%",
        "pitch": "+1Hz",
        "text": "Lekin tension mat lo! Isko bachane ka pehla aur official tarika hai: Apne account ko Pay As You Go mein upgrade kar do. Darro mat, Always Free resources par zero rupee charge lagta hai, lekin PAYG accounts ko Oracle kabhi reclaim nahi karta!",
        "subtitle": "Official Fix: Upgrade to Pay As You Go (Rs. 0 Bill Forever)",
        "visual_type": "PAYG_SOLUTION"
    },
    {
        "id": "scene4_fix2_script",
        "speaker": "Host",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+10%",
        "pitch": "+1Hz",
        "text": "Aur doosra tarika: agar card nahi lagana, toh server ke terminal mein run karo lookbusy daemon! Ye CPU ko automatically 22% par maintain rakhega taaki Oracle kabhi idle detect na kare!",
        "subtitle": "Script Fix: Run 'lookbusy' daemon (Keep CPU at 22%)",
        "visual_type": "TERMINAL_CODE"
    },
    {
        "id": "scene5_cta",
        "speaker": "Host",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+8%",
        "pitch": "+2Hz",
        "text": "Is reel ko abhi save kar lo taaki aapka free server kabhi band na ho, aur comment mein likho ORACLE, direct setup guide bhej dunga!",
        "subtitle": "Save Reel & Comment 'ORACLE' for 1-click script!",
        "visual_type": "CTA_OUTRO"
    }
]

async def gen_all():
    results = []
    for item in dialogue_script:
        fname = f"{item['id']}.mp3"
        fpath = os.path.join(out_dir, fname)
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(fpath)
        print(f"Generated {fname}")
        results.append({
            "id": item["id"],
            "path": fpath,
            "text": item["text"],
            "subtitle": item["subtitle"],
            "visual_type": item["visual_type"]
        })
    
    with open(os.path.join(out_dir, "script_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("All audio generated & metadata saved!")

asyncio.run(gen_all())
