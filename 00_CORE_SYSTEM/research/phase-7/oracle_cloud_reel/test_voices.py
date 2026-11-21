import asyncio
import edge_tts
import os

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"

sample_text = (
    "Agar aap Oracle Cloud ka Free Tier VM use kar rahe ho, toh dhyan se sunna! "
    "7 din baad aapka server automatic DELETE ho sakta hai! "
    "Isko 100% lifetime free kaise bachayein? Chaliye dekhte hain."
)

async def generate():
    # 1. Madhur (Hindi/Hinglish male, high energy)
    comm_m = edge_tts.Communicate(sample_text, "hi-IN-MadhurNeural", rate="+12%", pitch="+2Hz")
    await comm_m.save(os.path.join(out_dir, "test_madhur_hinglish.mp3"))
    
    # 2. Prabhat (Indian English/Hinglish male, confident tech vibe)
    comm_p = edge_tts.Communicate(sample_text, "en-IN-PrabhatNeural", rate="+10%")
    await comm_p.save(os.path.join(out_dir, "test_prabhat_hinglish.mp3"))
    
    print("Generated both samples successfully!")

asyncio.run(generate())
