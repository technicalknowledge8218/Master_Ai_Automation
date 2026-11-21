import asyncio
import edge_tts
import os
import soundfile as sf

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"

# 100% Fluid, Continuous, High-Energy Tech Creator Speech (Zero stutter, Zero dead gaps)
# Uses natural punctuation (commas, exclamation marks) for human cadence
# Uses 'इस्तेमाल' to avoid 'use' confusion, 'उसे' (usey), and 'सब्सक्रिप्शन' (subscription)

scripts = {
    "scene1_hook": (
        "अगर आप Oracle Cloud का फ्री टियर वीएम इस्तेमाल कर रहे हो, तो ध्यान से सुनना! "
        "सिर्फ सात दिन के अंदर आपका सर्वर ऑटोमैटिक डिलीट हो सकता है!"
    ),
    "scene2_problem": (
        "क्योंकि Oracle की एक स्ट्रिक्ट आइडल पॉलिसी है! "
        "अगर सात दिन तक आपका सीपीयू यूसेज 20% से कम रहा, तो Oracle उसे आइडल समझकर इंस्टेंस टर्मिनेट कर देता है, "
        "और आपका सारा डेटा गायब!"
    ),
    "scene3_fix1_payg": (
        "लेकिन टेंशन मत लो! कोई पेड सब्सक्रिप्शन नहीं लेना पड़ेगा! "
        "पहला और बेस्ट तरीका: अपने अकाउंट को Pay As You Go में अपग्रेड कर दो! "
        "ऑलवेज फ्री रिसोर्सेज़ पर ज़ीरो रुपया चार्ज लगता है, और PAYG सर्वर्स को Oracle कभी डिलीट नहीं करता!"
    ),
    "scene4_fix2_script": (
        "और दूसरा तरीका: अगर कार्ड नहीं लगाना, तो सर्वर के टर्मिनल में रन करो लुकबिज़ी टूल! "
        "ये सीपीयू को हमेशा 22% पर मेंटेन रखेगा, ताकि सिस्टम कभी आइडल डिटेक्ट ही ना हो!"
    ),
    "scene5_cta": (
        "इस रील को अभी सेव कर लो ताकि आपका सर्वर सेफ रहे, "
        "और कमेंट करो ORACLE, डायरेक्ट सेटअप कमांड डीएम कर दूंगा!"
    )
}

async def gen_fluid():
    for sid, text in scripts.items():
        # High-energy, fluid human pace: rate=+14%, pitch=+2Hz
        comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+14%", pitch="+2Hz")
        out_p = os.path.join(out_dir, f"fluid_{sid}.wav")
        # Save as mp3 first then read
        mp3_p = os.path.join(out_dir, f"fluid_{sid}.mp3")
        await comm.save(mp3_p)
        data, sr = sf.read(mp3_p)
        sf.write(out_p, data, sr)
        dur = len(data) / sr
        print(f"Generated {sid}: {dur:.2f}s (FLUID, ZERO STUTTER)")

asyncio.run(gen_fluid())
