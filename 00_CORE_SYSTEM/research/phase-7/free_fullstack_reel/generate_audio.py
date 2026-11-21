import asyncio
import edge_tts
import os
import subprocess
import soundfile as sf
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

SCENES = [
    {
        "id": "scene1_hook",
        "text": "Agar tum abhi bhi Render ya Heroku par apna project host kar rahe ho, toh tumhara server 15 minute mein so jata hai aur portfolio kharab lagta hai! Aur AWS ya Vercel par surprise billing ka darr rehta hai."
    },
    {
        "id": "scene2_frontend",
        "text": "Toh ye hai 2026 ka zero rupee Lifetime Full-Stack Architecture! Frontend ke liye istemaal karo Cloudflare Pages. Jahan milti hai Unlimited Bandwidth, zero cold start, aur free custom domain!"
    },
    {
        "id": "scene3_backend",
        "text": "Database ke liye istemaal karo Supabase ya Neon DB, jahan milta hai free serverless PostgreSQL. Aur backend API ke liye Cloudflare Workers, jo daily 1 lakh requests bilkul free handle karta hai!"
    },
    {
        "id": "scene4_hack",
        "text": "Aur agar tumhe kisi bhi server ko 24 ghante jagaye rakhna hai, toh cron-job.org se ek free 10-minute automated ping laga do. Tumhara server kabhi nahi soyega aur har saal 20 hazaar rupaye bachenge!"
    },
    {
        "id": "scene5_cta",
        "text": "Is poore architecture ka ready GitHub starter template aur setup commands chahiye? Toh comment karo STACK, main direct tumhare DM mein bhej dunga! Aur follow karna mat bhoolna!"
    }
]

async def generate_scene_audio():
    total_dur = 0.0
    for sc in SCENES:
        mp3_path = os.path.join(AUDIO_DIR, f"{sc['id']}.mp3")
        wav_path = os.path.join(AUDIO_DIR, f"{sc['id']}.wav")
        comm = edge_tts.Communicate(sc['text'], "hi-IN-MadhurNeural", rate="+12%", pitch="+1Hz")
        await comm.save(mp3_path)
        
        # Convert to WAV with broadcast audio mastering: slight low-shelf warmth and clear high-presence
        cmd = [
            FFMPEG, "-y", "-i", mp3_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,bass=g=2:f=120,treble=g=2:f=3500",
            "-ar", "44100", "-ac", "2",
            wav_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        data, sr = sf.read(wav_path)
        dur = len(data) / sr
        total_dur += dur
        print(f"Generated {sc['id']}.wav - Duration: {dur:.2f}s")
    print(f"\nTotal Voiceover Duration: {total_dur:.2f}s")

if __name__ == "__main__":
    asyncio.run(generate_scene_audio())

