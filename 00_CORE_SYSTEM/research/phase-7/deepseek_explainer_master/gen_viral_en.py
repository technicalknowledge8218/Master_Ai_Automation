import asyncio
import os
import subprocess
import edge_tts
import imageio_ffmpeg
import soundfile as sf

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\viral_en_audio"
os.makedirs(OUT_DIR, exist_ok=True)

SCRIPTS = [
    {
        "id": "line1_j",
        "speaker": "junior",
        "voice": "en-US-AriaNeural",
        "rate": "+14%",
        "pitch": "+2Hz",
        "text": "Wait! Should I cancel my twenty dollar ChatGPT subscription? DeepSeek R1 is literally free!",
        "sub": "Junior: 'Should I cancel my $20 ChatGPT sub? DeepSeek is literally free!'"
    },
    {
        "id": "line2_s",
        "speaker": "senior",
        "voice": "en-US-GuyNeural",
        "rate": "+15%",
        "pitch": "+0Hz",
        "text": "Hold on! In coding, DeepSeek is an absolute beast, but before you cancel, you need to know these three brutal facts!",
        "sub": "Senior: 'Hold on! In coding, DeepSeek is a beast, but know these 3 facts first!'"
    },
    {
        "id": "line3_s",
        "speaker": "senior",
        "voice": "en-US-GuyNeural",
        "rate": "+14%",
        "pitch": "+0Hz",
        "text": "Fact number one: Reasoning power! In Python benchmarks and math, DeepSeek R1 literally destroys GPT-4o!",
        "sub": "Senior: '1. Reasoning Power: In Python & math, DeepSeek R1 destroys GPT-4o!'"
    },
    {
        "id": "line4_s",
        "speaker": "senior",
        "voice": "en-US-GuyNeural",
        "rate": "+14%",
        "pitch": "+0Hz",
        "text": "Fact number two: Privacy warning! Never put your company's proprietary code into the cloud! Run it locally instead!",
        "sub": "Senior: '2. Privacy Warning: Never put company code in cloud! Run locally!'"
    },
    {
        "id": "line5_j",
        "speaker": "junior",
        "voice": "en-US-AriaNeural",
        "rate": "+14%",
        "pitch": "+2Hz",
        "text": "Wait! You mean we can run the entire model on our own laptop without internet?",
        "sub": "Junior: 'Wait! We can run the entire model on our own laptop without internet?'"
    },
    {
        "id": "line6_s",
        "speaker": "senior",
        "voice": "en-US-GuyNeural",
        "rate": "+15%",
        "pitch": "+0Hz",
        "text": "Exactly! One hundred percent free, zero data leaks! Comment LOCAL and I will send you the complete setup guide!",
        "sub": "Senior: 'Exactly! 100% Free, zero leaks! Comment LOCAL for full setup guide!'"
    }
]

async def gen():
    for s in SCRIPTS:
        raw_p = os.path.join(OUT_DIR, f"{s['id']}_raw.mp3")
        clean_p = os.path.join(OUT_DIR, f"{s['id']}.wav")
        tts = edge_tts.Communicate(s["text"], s["voice"], rate=s["rate"], pitch=s["pitch"])
        await tts.save(raw_p)
        
        # Vocal chain: silenceremove + broadcast EQ + compand + loudnorm
        cmd = [
            FFMPEG, "-y", "-i", raw_p,
            "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=3.5,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3,loudnorm=I=-14:LRA=7:tp=-1.0",
            clean_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(raw_p):
            os.remove(raw_p)
        
        data, sr = sf.read(clean_p)
        print(f"Mastered {s['id']} ({s['voice']}): {len(data)/sr:.2f}s")

if __name__ == "__main__":
    asyncio.run(gen())
