import asyncio
import edge_tts
import subprocess
import imageio_ffmpeg
import os
import soundfile as sf
from kokoro_onnx import Kokoro

FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\test_delivery"
os.makedirs(OUT_DIR, exist_ok=True)

# Test 1: Guy & Aria (Edge-TTS Viral US YouTuber style)
async def test_guy_aria():
    lines = [
        ("j_aria", "en-US-AriaNeural", "Wait! Should I cancel my twenty dollar ChatGPT subscription? DeepSeek R1 is literally free!"),
        ("s_guy", "en-US-GuyNeural", "Hold on! In coding, DeepSeek is an absolute beast, but before you cancel, you need to know these three brutal facts!")
    ]
    for sid, voice, text in lines:
        raw_p = os.path.join(OUT_DIR, f"{sid}_raw.mp3")
        wav_p = os.path.join(OUT_DIR, f"{sid}.wav")
        tts = edge_tts.Communicate(text, voice, rate="+12%")
        await tts.save(raw_p)
        cmd = [
            FF, "-y", "-i", raw_p,
            "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=3,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3,loudnorm=I=-14:LRA=7:tp=-1.0",
            wav_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Generated {sid} ({voice})")

# Test 2: Andrew Multilingual & Ava Multilingual (Modern tech slang / Hinglish capable)
async def test_andrew_ava():
    lines = [
        ("j_ava", "en-US-AvaMultilingualNeural", "Wait! Should I cancel my twenty dollar ChatGPT subscription? DeepSeek R1 is completely free!"),
        ("s_andrew", "en-US-AndrewMultilingualNeural", "Hold on bro! In coding, DeepSeek is an absolute beast, but before you cancel, you need to know these three brutal facts!")
    ]
    for sid, voice, text in lines:
        raw_p = os.path.join(OUT_DIR, f"{sid}_raw.mp3")
        wav_p = os.path.join(OUT_DIR, f"{sid}.wav")
        tts = edge_tts.Communicate(text, voice, rate="+10%")
        await tts.save(raw_p)
        cmd = [
            FF, "-y", "-i", raw_p,
            "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=3,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3,loudnorm=I=-14:LRA=7:tp=-1.0",
            wav_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Generated {sid} ({voice})")

# Test 3: Kokoro Adam & Bella (Human Studio delivery)
def test_kokoro():
    onnx_path = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\kokoro_model\kokoro-v0_19.onnx"
    voices_path = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\kokoro_model\voices.bin"
    kokoro = Kokoro(onnx_path, voices_path)
    
    lines = [
        ("j_bella", "af_bella", "Wait! Should I cancel my twenty dollar ChatGPT subscription? DeepSeek R1 is literally free!"),
        ("s_adam", "am_adam", "Hold on! In coding, DeepSeek is an absolute beast, but before you cancel, you need to know these three brutal facts!")
    ]
    for sid, voice, text in lines:
        samples, sr = kokoro.create(text, voice=voice, speed=1.18, lang="en-us")
        raw_p = os.path.join(OUT_DIR, f"{sid}_raw.wav")
        wav_p = os.path.join(OUT_DIR, f"{sid}.wav")
        sf.write(raw_p, samples, sr)
        cmd = [
            FF, "-y", "-i", raw_p,
            "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,highpass=f=80,loudnorm=I=-14:LRA=7:tp=-1.0",
            wav_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Generated {sid} ({voice})")

async def main():
    await test_guy_aria()
    await test_andrew_ava()
    test_kokoro()
    print("All delivery tests generated!")

if __name__ == "__main__":
    asyncio.run(main())
