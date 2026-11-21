import asyncio
import edge_tts
import os

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"

# Junior (Arjun) asking worried question
junior_line = "भैया, मेरा Oracle Cloud का फ्री सर्वर सात दिन में डिलीट होने वाला है! मेल आ गया! क्या करूँ?"

# Senior (Dr. Kabir) answering calmly
senior_line = "अर्जुन, टेंशन मत लो! ओरेकल का रूल है कि अगर सीपीयू 20% से कम रहा तो वो सर्वर बंद कर देते हैं। लेकिन इसको लाइफटाइम फ्री रखने के दो सॉलिड हैक हैं!"

async def test_dialogue():
    # Junior: Madhur (fast, pitch up)
    c_j = edge_tts.Communicate(junior_line, "hi-IN-MadhurNeural", rate="+14%", pitch="+3Hz")
    await c_j.save(os.path.join(out_dir, "test_dual_junior.mp3"))
    
    # Senior: Asad (mature, calm, authoritative)
    c_s = edge_tts.Communicate(senior_line, "ur-PK-AsadNeural", rate="+10%", pitch="-1Hz")
    await c_s.save(os.path.join(out_dir, "test_dual_senior.mp3"))
    
    # Also test Prabhat for senior
    c_s2 = edge_tts.Communicate(senior_line, "en-IN-PrabhatNeural", rate="+10%")
    await c_s2.save(os.path.join(out_dir, "test_dual_senior_prabhat.mp3"))
    
    print("Generated dual conversational dialogue samples!")

asyncio.run(test_dialogue())
