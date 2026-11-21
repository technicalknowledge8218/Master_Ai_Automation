import asyncio
import edge_tts
import os

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\voice_tests"
os.makedirs(out_dir, exist_ok=True)

# Test lines
j_line = "भैया! मेरा Oracle Cloud का फ्री सर्वर सात दिन में डिलीट होने वाला है! मेल आ गया! अब क्या करूँ?!"
s_line = "टेंशन मत लो! ओरेकल का रूल है कि अगर 7 दिन तक सीपीयू 20% से कम रहा तो वो सर्वर बंद कर देते हैं। लेकिन इसको लाइफटाइम सेफ रखने के दो पक्के हैक हैं!"

async def test_pairs():
    # Pair A: Male + Female (Neha + Dr. Kabir) -> 100% unmistakably different!
    # Neha (Female developer, high energy):
    c_neha = edge_tts.Communicate(j_line, "hi-IN-SwaraNeural", rate="+15%", pitch="+2Hz")
    await c_neha.save(os.path.join(out_dir, "test_pairA_junior_neha_female.mp3"))
    
    # Dr. Kabir (Male architect, deep authoritative):
    c_kabir = edge_tts.Communicate(s_line, "en-IN-PrabhatNeural", rate="+10%", pitch="-2Hz")
    await c_kabir.save(os.path.join(out_dir, "test_pairA_senior_kabir_male.mp3"))
    
    # Pair B: Young Boyish (Madhur +5Hz) + Deep Mature Male (Asad or Madhur -8Hz deep)
    c_madhur_boy = edge_tts.Communicate(j_line, "hi-IN-MadhurNeural", rate="+18%", pitch="+5Hz")
    await c_madhur_boy.save(os.path.join(out_dir, "test_pairB_junior_boyish.mp3"))
    
    c_deep_man = edge_tts.Communicate(s_line, "hi-IN-MadhurNeural", rate="+5%", pitch="-8Hz")
    await c_deep_man.save(os.path.join(out_dir, "test_pairB_senior_deep_male.mp3"))
    
    print("Voice test pairs generated!")

asyncio.run(test_pairs())
