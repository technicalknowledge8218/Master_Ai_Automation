import asyncio
import os
import subprocess
import edge_tts
import imageio_ffmpeg
import soundfile as sf

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
PROJ_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master"
AUDIO_DIR = os.path.join(PROJ_DIR, "audio")

SCRIPTS = [
    {
        "id": "line1_j",
        "speaker": "junior",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+22%",
        "pitch": "+2Hz",
        "text": "भैया! क्या ChatGPT का ₹2000 का सब्सक्रिप्शन कैंसिल कर दूं? DeepSeek R1 तो बिल्कुल FREE है!",
        "sub": "Junior: 'Bhaiya! ChatGPT ka ₹2000 subscription cancel kar du? DeepSeek FREE hai!'"
    },
    {
        "id": "line2_s",
        "speaker": "senior",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+16%",
        "pitch": "+0Hz",
        "text": "Wait bro! Coding aur maths mein to DeepSeek baap hai, par ye teen sach jaane bina switch mat karna!",
        "sub": "Senior: 'Wait bro! Coding me DeepSeek baap hai, par ye 3 sach jaan lo pehle!'"
    },
    {
        "id": "line3_s",
        "speaker": "senior",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+16%",
        "pitch": "+0Hz",
        "text": "Pehla sach: Reasoning Power! Coding aur complex logic mein DeepSeek R1 beats GPT-4o easily!",
        "sub": "Senior: '1. Reasoning Power: Coding aur complex logic me R1 beats GPT-4o!'"
    },
    {
        "id": "line4_s",
        "speaker": "senior",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+16%",
        "pitch": "+0Hz",
        "text": "Doosra: Privacy Warning! Agar office ka confidential code daal rahe ho, to cloud app nahi, local run karo!",
        "sub": "Senior: '2. Privacy Alert: Confidential code ke liye cloud nahi, Local Ollama run karo!'"
    },
    {
        "id": "line5_j",
        "speaker": "junior",
        "voice": "hi-IN-SwaraNeural",
        "rate": "+22%",
        "pitch": "+2Hz",
        "text": "अरे वाह! मतलब बिना इंटरनेट हम पूरा DeepSeek अपने लैपटॉप पे चला सकते हैं?",
        "sub": "Junior: 'Arre wah! Matlab bina internet pura DeepSeek apne laptop pe chalega?'"
    },
    {
        "id": "line6_s",
        "speaker": "senior",
        "voice": "en-IN-PrabhatNeural",
        "rate": "+16%",
        "pitch": "+0Hz",
        "text": "Bilkul! 100% Free, zero data leak! Comment karo LOCAL aur poora step-by-step setup guide mil jayega!",
        "sub": "Senior: 'Bilkul! Zero data leak! Comment karo LOCAL for full free setup guide!'"
    }
]

async def gen_audio():
    print("--- [1/2] Generating Voiceovers ---")
    for s in SCRIPTS:
        raw_p = os.path.join(AUDIO_DIR, f"{s['id']}_raw.mp3")
        clean_p = os.path.join(AUDIO_DIR, f"{s['id']}.wav")
        tts = edge_tts.Communicate(s["text"], s["voice"], rate=s["rate"], pitch=s["pitch"])
        await tts.save(raw_p)
        
        # High quality broadcast mastering
        cmd = [
            FFMPEG, "-y", "-i", raw_p,
            "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=3.5,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3,loudnorm=I=-14:LRA=7:tp=-1.0",
            clean_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(raw_p):
            os.remove(raw_p)
            
        data, sr = sf.read(clean_p)
        dur = len(data) / sr
        print(f"Mastered {s['id']} ({s['voice']}): {dur:.2f}s")

if __name__ == "__main__":
    asyncio.run(gen_audio())
