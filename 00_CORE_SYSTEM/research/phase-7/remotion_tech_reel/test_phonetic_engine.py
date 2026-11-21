import asyncio
import edge_tts
import os
import subprocess
import imageio_ffmpeg
import soundfile as sf

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\remotion_tech_reel\phonetic_tests"
os.makedirs(OUT_DIR, exist_ok=True)

TEST_CASES = [
    {
        "name": "01_subscription_fix",
        "desc": "Subscription pronunciation fix via SSML and Devanagari phonetics",
        "text": """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
            <voice name="hi-IN-MadhurNeural">
                <prosody rate="+12%" pitch="+1Hz">
                    Agar tum cloud <lang xml:lang="en-US">subscription</lang> le rahe ho, toh pehle uski terms padho!
                    सब-स्क्रिप्ट-शन का खर्च हर महीने बढ़ता है।
                </prosody>
            </voice>
        </speak>"""
    },
    {
        "name": "02_use_vs_usey_fix",
        "desc": "Disambiguating English 'use' (utilize) vs Hindi 'उसे' (him/her)",
        "text": """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
            <voice name="hi-IN-MadhurNeural">
                <prosody rate="+12%" pitch="+1Hz">
                    उसे बताओ कि इस टूल का सही इस्तेमाल कैसे करना है, और इसका <lang xml:lang="en-US">use case</lang> क्या है।
                </prosody>
            </voice>
        </speak>"""
    },
    {
        "name": "03_tech_acronyms_fix",
        "desc": "Disambiguating AWS, API, SQL, EC2, PostgreSQL",
        "text": """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
            <voice name="hi-IN-MadhurNeural">
                <prosody rate="+12%" pitch="+1Hz">
                    <say-as interpret-as="characters">AWS</say-as> और <say-as interpret-as="characters">API</say-as> पर <break time="100ms"/> 
                    पोस्टग्रेस <say-as interpret-as="characters">SQL</say-as> डेटाबेस कैसे डिप्लॉय करें?
                </prosody>
            </voice>
        </speak>"""
    },
    {
        "name": "04_conversational_flow",
        "desc": "Fluid sentence momentum without robotic stuttering",
        "text": """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
            <voice name="hi-IN-MadhurNeural">
                <prosody rate="+14%" pitch="+1Hz">
                    अरे भाई, टेंशन मत ले! <break time="150ms"/> 
                    2026 में कोई भी जूनियर डेवलपर <say-as interpret-as="characters">AWS</say-as> का महंगा सर्वर नहीं खरीदता।
                    सीधा क्लाउडफ्लेयर पेजेस और सुपाबेस चलाओ, <break time="100ms"/>
                    और लाइफटाइम जीरो रुपया बिल पाओ!
                </prosody>
            </voice>
        </speak>"""
    }
]

async def run_tests():
    print("=== Testing Neural Speech Phonetics & SSML Engine ===")
    for tc in TEST_CASES:
        mp3_path = os.path.join(OUT_DIR, f"{tc['name']}.mp3")
        wav_path = os.path.join(OUT_DIR, f"{tc['name']}.wav")
        comm = edge_tts.Communicate(tc["text"], "hi-IN-MadhurNeural")
        await comm.save(mp3_path)
        
        # Master WAV
        cmd = [
            FFMPEG, "-y", "-i", mp3_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,bass=g=2:f=120,treble=g=2:f=3500",
            "-ar", "44100", "-ac", "2",
            wav_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        data, sr = sf.read(wav_path)
        dur = len(data) / sr
        print(f"[✓] {tc['name']}: {tc['desc']} -> Duration: {dur:.2f}s")
    print("\nAll phonetic test audios generated successfully.")

if __name__ == "__main__":
    asyncio.run(run_tests())
