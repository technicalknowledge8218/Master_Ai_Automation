import asyncio
import edge_tts
import os

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"

# Comparison:
# 1. Ambiguous Roman Hinglish (what went wrong):
bad_text = "agar aap ise use kar rahe ho aur use delete hone se bachana hai to koi subscription nahi chahiye"

# 2. Devanagari Script (100% Phonetically Unambiguous):
devanagari_text = (
    "अगर आप इसे इस्तेमाल कर रहे हो, "
    "और उसे डिलीट होने से बचाना है, "
    "तो कोई सब्सक्रिप्शन नहीं चाहिए!"
)

# 3. Romanized Phonetic with unambiguous spelling:
# 'usey' for उसे, 'istemaal' for use, 'subscription' explicitly
phonetic_roman = (
    "Agar aap isey istemaal kar rahe ho, "
    "aur usey delete hone se bachana hai, "
    "toh koi subscription nahi chahiye!"
)

async def run_tests():
    # Test Devanagari with Madhur
    c1 = edge_tts.Communicate(devanagari_text, "hi-IN-MadhurNeural", rate="+10%")
    await c1.save(os.path.join(out_dir, "pronounce_devanagari.mp3"))
    print("Saved pronounce_devanagari.mp3")
    
    # Test Phonetic Roman with Madhur
    c2 = edge_tts.Communicate(phonetic_roman, "hi-IN-MadhurNeural", rate="+10%")
    await c2.save(os.path.join(out_dir, "pronounce_phonetic_roman.mp3"))
    print("Saved pronounce_phonetic_roman.mp3")

asyncio.run(run_tests())
