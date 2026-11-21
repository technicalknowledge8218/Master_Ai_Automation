import asyncio
import edge_tts
import os
import json
import soundfile as sf
import numpy as np

audio_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\audio_v2"
os.makedirs(audio_dir, exist_ok=True)

# 100% Phonetically Unambiguous Script
# In Devanagari, 'इस्तेमाल' removes 'use' confusion, 'उसे' is never read as English 'use',
# and 'सब्सक्रिप्शन' has 100% pure pronunciation!
scenes_script = [
    {
        "id": "scene1_hook",
        "char": "arjun_shocked.png",
        "char_side": "right",
        "bg_color": (15, 23, 42, 255),
        "tag": "CRITICAL WARNING",
        "card": "card_warning.png",
        "sfx": "alarm.wav",
        "bubble_title": "⚠️ WARNING:",
        "bubble_text": "Don't let your free VM die!",
        "subtitle": "Oracle Cloud Free Server 7 Din Mein DELETE Ho Jayega?!",
        # Phrased bursts with pitch and micro-pauses
        "bursts": [
            ("अगर आप Oracle Cloud का फ्री टियर वीएम इस्तेमाल कर रहे हो?", "+14%", "+2Hz", 0.22),
            ("तो ध्यान से सुनना!", "+16%", "+4Hz", 0.28),
            ("सिर्फ सात दिन के अंदर...", "+10%", "+1Hz", 0.18),
            ("आपका सर्वर ऑटोमैटिक डिलीट हो जाएगा!", "+16%", "+3Hz", 0.35)
        ]
    },
    {
        "id": "scene2_problem",
        "char": "dr_kabir_warning.png",
        "char_side": "left",
        "bg_color": (38, 16, 24, 255),
        "tag": "IDLE RECLAMATION POLICY",
        "card": "gauge_cpu_6.png",
        "sfx": "pop.wav",
        "bubble_title": "📊 OCI THRESHOLD:",
        "bubble_text": "CPU < 20% = INSTANCE TERMINATED!",
        "subtitle": "Oracle Rule: CPU < 20% = Server Terminated & Data Lost!",
        "bursts": [
            ("क्योंकि Oracle की एक स्ट्रिक्ट आइडल पॉलिसी है:", "+12%", "+1Hz", 0.20),
            ("अगर सात दिन तक आपका सीपीयू यूसेज 20% से कम रहा,", "+14%", "+1Hz", 0.22),
            ("तो Oracle उसे आइडल समझकर इंस्टेंस टर्मिनेट कर देता है,", "+12%", "+2Hz", 0.25),
            ("और आपका सारा डेटा गायब!", "+18%", "+3Hz", 0.35)
        ]
    },
    {
        "id": "scene3_fix1_payg",
        "char": "arjun_pointing.png",
        "char_side": "right",
        "bg_color": (10, 35, 26, 255),
        "tag": "100% PERMANENT FIX",
        "card": "card_payg.png",
        "sfx": "chime.wav",
        "bubble_title": "💡 OFFICIAL FIX:",
        "bubble_text": "Upgrade to PAYG (Rs. 0 Bill Forever)",
        "subtitle": "Method 1: Upgrade to PAYG ($0 Bill Forever & Lifetime Safe)",
        "bursts": [
            ("लेकिन डरने की ज़रूरत नहीं! कोई पेड सब्सक्रिप्शन नहीं लेना पड़ेगा!", "+14%", "+2Hz", 0.25),
            ("पहला और ऑफिशियल तरीका:", "+12%", "+2Hz", 0.18),
            ("अपने अकाउंट को Pay As You Go में अपग्रेड कर दो!", "+14%", "+2Hz", 0.22),
            ("ऑलवेज फ्री रिसोर्सेज़ पर ज़ीरो रुपया चार्ज लगता है,", "+12%", "+1Hz", 0.20),
            ("और PAYG सर्वर्स को Oracle कभी डिलीट नहीं करता!", "+14%", "+3Hz", 0.35)
        ]
    },
    {
        "id": "scene4_fix2_script",
        "char": "dr_kabir_tablet.png",
        "char_side": "left",
        "bg_color": (16, 24, 40, 255),
        "tag": "CLI AUTOMATION FIX",
        "card": "card_terminal.png",
        "sfx": "pop.wav",
        "bubble_title": "⚡ AUTOMATION FIX:",
        "bubble_text": "Run 'lookbusy' daemon (Keep CPU at 22%)",
        "subtitle": "Method 2: Run 'lookbusy' Tool (Keep CPU at 22%)",
        "bursts": [
            ("और दूसरा तरीका: अगर कार्ड नहीं लगाना,", "+12%", "+1Hz", 0.20),
            ("तो टर्मिनल में रन करो लुकबिज़ी टूल!", "+16%", "+2Hz", 0.25),
            ("ये सीपीयू को हमेशा 22% पर मेंटेन रखेगा,", "+14%", "+1Hz", 0.20),
            ("ताकि सिस्टम कभी आइडल डिटेक्ट ना हो!", "+14%", "+3Hz", 0.35)
        ]
    },
    {
        "id": "scene5_cta",
        "char": "arjun_thumbsup.png",
        "char_side": "right",
        "bg_color": (28, 20, 50, 255),
        "tag": "SAVE & SHARE REEL",
        "card": "card_cta.png",
        "sfx": "chime.wav",
        "bubble_title": "📩 GET COMMANDS:",
        "bubble_text": "Comment 'ORACLE' for 1-click script!",
        "subtitle": "Save Reel & Comment 'ORACLE' for Full Setup Commands!",
        "bursts": [
            ("इस रील को अभी सेव कर लो ताकि आपका सर्वर सेफ रहे,", "+12%", "+2Hz", 0.22),
            ("और कमेंट करो ORACLE,", "+16%", "+3Hz", 0.20),
            ("डायरेक्ट सेटअप कमांड डीएम कर दूंगा!", "+14%", "+3Hz", 0.40)
        ]
    }
]

async def generate_scene_audio():
    total_sec = 0.0
    for scene in scenes_script:
        sid = scene["id"]
        stitched = []
        target_sr = 24000
        
        for b_idx, (text, rate, pitch, pause_s) in enumerate(scene["bursts"]):
            comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate=rate, pitch=pitch)
            b_path = os.path.join(audio_dir, f"{sid}_burst_{b_idx}.mp3")
            await comm.save(b_path)
            
            data, sr = sf.read(b_path)
            if len(data.shape) > 1: data = data.mean(axis=1)
            target_sr = sr
            stitched.append(data)
            
            # Add breathing pause
            pause_len = int(pause_s * sr)
            stitched.append(np.zeros(pause_len, dtype=np.float32))
            
        full_scene_audio = np.concatenate(stitched)
        final_scene_path = os.path.join(audio_dir, f"{sid}.wav")
        sf.write(final_scene_path, full_scene_audio, target_sr)
        
        dur = len(full_scene_audio) / target_sr
        total_sec += dur
        print(f"Generated {sid}.wav: {dur:.2f}s")
        
    print(f"\nAll scenes audio generated! Total Duration: {total_sec:.2f}s")

asyncio.run(generate_scene_audio())
