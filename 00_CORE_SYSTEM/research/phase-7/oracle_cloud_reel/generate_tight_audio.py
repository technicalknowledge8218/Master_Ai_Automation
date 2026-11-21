import asyncio
import edge_tts
import os
import json

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\audio"
os.makedirs(out_dir, exist_ok=True)

# High-Energy, Fast-Paced Viral Tech Reel Script (Sweet spot: ~38s)
dialogue_script = [
    {
        "id": "scene1_hook",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+18%",
        "pitch": "+2Hz",
        "text": "Agar aap Oracle Cloud ka Free Tier VM use kar rahe ho, toh sunno! Saat din baad aapka server automatic DELETE ho sakta hai!",
        "subtitle": "Oracle Cloud Free Server 7 Din Mein DELETE Ho Jayega?!",
        "tag": "CRITICAL ALERT",
        "visual_type": "ALERT_HOOK"
    },
    {
        "id": "scene2_problem",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+18%",
        "pitch": "+1Hz",
        "text": "Kyunki Oracle ki strict idle policy hai: agar aapka CPU usage 20% se kam raha, toh instance terminate ho jayega aur sara data khatam!",
        "subtitle": "Oracle Rule: CPU < 20% = Server Terminated & Data Lost!",
        "tag": "IDLE RECLAMATION RULE",
        "visual_type": "CPU_METER_ALERT"
    },
    {
        "id": "scene3_fix1_payg",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+1Hz",
        "text": "Isko bachane ka pehla aur official tarika: Account ko Pay As You Go mein upgrade kar do! Always Free resources par zero rupee charge lagta hai, aur PAYG servers ko Oracle kabhi delete nahi karta!",
        "subtitle": "Method 1: Upgrade to PAYG ($0 Bill Forever & Lifetime Safe)",
        "tag": "100% PERMANENT FIX",
        "visual_type": "PAYG_SOLUTION"
    },
    {
        "id": "scene4_fix2_script",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+18%",
        "pitch": "+1Hz",
        "text": "Doosra tarika: agar card nahi lagana, toh terminal mein run karo lookbusy tool! Ye CPU usage ko 22% par maintain rakhega taaki Oracle kabhi idle detect na kare!",
        "subtitle": "Method 2: Run 'lookbusy' Tool (Keep CPU at 22%)",
        "tag": "CLI AUTOMATION FIX",
        "visual_type": "TERMINAL_CODE"
    },
    {
        "id": "scene5_cta",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+2Hz",
        "text": "Is reel ko abhi save kar lo taaki aapka free server safe rahe, aur comment karo ORACLE, direct setup command bhej dunga!",
        "subtitle": "Save Reel & Comment 'ORACLE' for Full Setup Commands!",
        "tag": "SAVE & SHARE",
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
            "tag": item["tag"],
            "visual_type": item["visual_type"]
        })
    
    with open(os.path.join(out_dir, "script_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Punchy audio generated successfully!")

asyncio.run(gen_all())
