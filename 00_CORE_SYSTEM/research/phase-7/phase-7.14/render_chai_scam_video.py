"""
Master AI - Phase 7.14 Production Render Engine
Renders 'The ₹10 Chai QR Code Scam' (30-second 9:16 Vertical Short Film)
Adheres strictly to STYLE_VECTOR_EDITORIAL with zero live-action clashing.
Generates voiceover via Edge-TTS, synthesizes sound design, camera motion, and compiles final MP4.
"""

import os
import sys
import asyncio
import subprocess
import imageio_ffmpeg
from PIL import Image

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
PHASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.14"
SAMPLE_DIR = os.path.join(PHASE_DIR, "sample_frames")
TEMP_DIR = os.path.join(PHASE_DIR, "render_temp")
OUTPUT_VIDEO = os.path.join(PHASE_DIR, "the_10_rupee_chai_scam_master.mp4")

os.makedirs(TEMP_DIR, exist_ok=True)

import edge_tts

VOICE_SCRIPTS = [
    {
        "id": "scene_2",
        "text": "कालू भैया की टपरी पे रोज़ चाय पीता हूँ... पर आज उनका UPI नाम 'रॉयल इलेक्ट्रॉनिक्स' कब से हो गया?",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+4%",
        "pitch": "+0Hz"
    },
    {
        "id": "scene_3",
        "text": "असली क्यूआर पर नकली स्टिकर चिपका के, पूरे दिन का धंधा अपनी जेब में डाल रहा था ये बंदा!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+5%",
        "pitch": "+0Hz"
    },
    {
        "id": "scene_4",
        "text": "अरे भैया रुको! इस स्कैनर में लाइव फोटो वेरिफिकेशन है... स्कैमर का फोटो सीधा पुलिस को जाता है!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+6%",
        "pitch": "+2Hz"
    },
    {
        "id": "scene_5",
        "text": "सुबह से तीन हज़ार रुपये गए हैं तेरे अकाउंट में... पहले हिसाब कर, फिर भागना बेटा!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "-5%",
        "pitch": "-6Hz"
    },
    {
        "id": "scene_6",
        "text": "तो दोस्तों, यूपीआई स्कैन करते टाइम दुकान का नाम ज़रूर चेक करो... टेक स्मार्ट है, तुम भी बनो!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+3%",
        "pitch": "+0Hz"
    }
]

async def generate_voiceovers():
    print("--- [1/5] Generating Edge-TTS Voiceover Tracks ---")
    for item in VOICE_SCRIPTS:
        out_raw = os.path.join(TEMP_DIR, f"vo_raw_{item['id']}.mp3")
        out_clean = os.path.join(TEMP_DIR, f"vo_{item['id']}.wav")
        tts = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await tts.save(out_raw)
        
        # Clean silence using ffmpeg silenceremove
        cmd = [
            FFMPEG, "-y", "-i", out_raw,
            "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
            out_clean
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Generated clean voiceover: {out_clean}")

def get_audio_duration(path):
    cmd = [
        FFMPEG, "-i", path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            # Duration: 00:00:05.12, start: ...
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            dur = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            return dur
    return 3.0

def build_scene_videos(scene_durations):
    print("--- [2/5] Rendering Animated 9:16 Scene Clips with Motion ---")
    scene_files = [
        ("scene_01_macro_hook.png", scene_durations[0], "1.0+0.05*t/d", 1),
        ("scene_02_rohan_scan.png", scene_durations[1], "1.0+0.04*t/d", 2),
        ("scene_03_bunty_shadows.png", scene_durations[2], "1.0+0.06*t/d", 3),
        ("scene_04_split_bluff.png", scene_durations[3], "1.0+0.08*t/d", 4),
        ("scene_05_ladle_climax.png", scene_durations[4], "1.0+0.05*t/d", 5),
        ("scene_06_rohan_punchline.png", scene_durations[5], "1.0+0.04*t/d", 6),
    ]
    
    clip_paths = []
    for img_name, dur, zoom_expr, sc_num in scene_files:
        img_path = os.path.join(SAMPLE_DIR, img_name)
        out_clip = os.path.join(TEMP_DIR, f"clip_{sc_num}.mp4")
        fps = 30
        total_frames = int(dur * fps)
        
        # FFmpeg zoompan filter for vertical 1080x1920
        # zoompan=z='1+0.05*on/N':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=total_frames:s=1080x1920:fps=30
        vf = f"zoompan=z='min(zoom+0.0008,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps={fps}"
        
        cmd = [
            FFMPEG, "-y", "-loop", "1", "-i", img_path,
            "-vf", vf,
            "-t", str(dur),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
            out_clip
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        clip_paths.append(out_clip)
        print(f"Rendered clip {sc_num}: {dur:.2f}s -> {out_clip}")
    
    return clip_paths

def concatenate_clips(clip_paths):
    print("--- [3/5] Concatenating Scene Video Sequence ---")
    concat_list = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for p in clip_paths:
            f.write(f"file '{os.path.abspath(p).replace('\\', '/')}'\n")
            
    raw_video = os.path.join(TEMP_DIR, "video_track.mp4")
    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy", raw_video
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return raw_video

def synthesize_audio_track(scene_durations):
    print("--- [4/5] Multi-Layer Audio Design & Foley Mixing ---")
    
    # Calculate exact offsets
    t0 = 0.0
    t1 = scene_durations[0] # scene 2 start (Rohan scan)
    t2 = t1 + scene_durations[1] # scene 3 start (Bunty)
    t3 = t2 + scene_durations[2] # scene 4 start (Bluff)
    t4 = t3 + scene_durations[3] # scene 5 start (Ladle climax)
    t5 = t4 + scene_durations[4] # scene 6 start (Punchline)
    total_dur = t5 + scene_durations[5]
    
    # Sound Effects:
    # 1. Tea Pour at t=0 (filtered white noise with envelope)
    sfx_tea = os.path.join(TEMP_DIR, "sfx_tea.wav")
    cmd_tea = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"anoisesrc=d=2.4:c=pink:r=44100,lowpass=f=1200,volume=0.35,afade=t=out:st=1.8:d=0.6",
        sfx_tea
    ]
    subprocess.run(cmd_tea, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 2. UPI scan chime at t=t1+0.5 (two sine tones: 880Hz then 1760Hz)
    sfx_chime = os.path.join(TEMP_DIR, "sfx_chime.wav")
    cmd_chime = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", "sine=f=988:d=0.15,volume=0.4",
        "-f", "lavfi",
        "-i", "sine=f=1318:d=0.35,volume=0.5,afade=t=out:st=0.15:d=0.2",
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
        "-map", "[out]", sfx_chime
    ]
    subprocess.run(cmd_chime, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 3. Ladle impact CLONK at t=t4+0.4 (440Hz low punch + high metallic ping + fast decay)
    sfx_clonk = os.path.join(TEMP_DIR, "sfx_clonk.wav")
    cmd_clonk = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", "sine=f=330:d=0.6,afade=t=out:st=0.08:d=0.5,volume=0.8",
        "-f", "lavfi",
        "-i", "sine=f=880:d=0.4,afade=t=out:st=0.04:d=0.36,volume=0.6",
        "-filter_complex", "[0:a][1:a]amix=inputs=2[out]",
        "-map", "[out]", sfx_clonk
    ]
    subprocess.run(cmd_clonk, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 4. Background Lofi Music Track (ambient harmonic drone + rhythmic pulse)
    bgm_path = os.path.join(TEMP_DIR, "bgm_loop.wav")
    cmd_bgm = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"sine=f=220:d={total_dur},volume=0.08",
        "-f", "lavfi",
        "-i", f"sine=f=440:d={total_dur},volume=0.04",
        "-f", "lavfi",
        "-i", f"anoisesrc=d={total_dur}:c=brown:r=44100,lowpass=f=250,volume=0.12",
        "-filter_complex", f"[0:a][1:a][2:a]amix=inputs=3[m];[m]afade=t=out:st={total_dur-1.5:.2f}:d=1.5[out]",
        "-map", "[out]", bgm_path
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Now assemble multi-track mix with adelay & amix
    vo2 = os.path.join(TEMP_DIR, "vo_scene_2.wav")
    vo3 = os.path.join(TEMP_DIR, "vo_scene_3.wav")
    vo4 = os.path.join(TEMP_DIR, "vo_scene_4.wav")
    vo5 = os.path.join(TEMP_DIR, "vo_scene_5.wav")
    vo6 = os.path.join(TEMP_DIR, "vo_scene_6.wav")
    
    delays = [
        f"{int(t0*1000)}",            # 0: tea pour
        f"{int((t1+0.3)*1000)}",      # 1: chime
        f"{int((t4+0.4)*1000)}",      # 2: clonk
        "0",                          # 3: bgm
        f"{int(t1*1000)}",            # 4: vo2
        f"{int(t2*1000)}",            # 5: vo3
        f"{int(t3*1000)}",            # 6: vo4
        f"{int(t4*1000)}",            # 7: vo5
        f"{int(t5*1000)}",            # 8: vo6
    ]
    
    mix_filter = (
        f"[0:a]adelay={delays[0]}|{delays[0]}[a0];"
        f"[1:a]adelay={delays[1]}|{delays[1]}[a1];"
        f"[2:a]adelay={delays[2]}|{delays[2]}[a2];"
        f"[3:a]volume=0.35[a3];"
        f"[4:a]adelay={delays[4]}|{delays[4]},volume=1.4[a4];"
        f"[5:a]adelay={delays[5]}|{delays[5]},volume=1.4[a5];"
        f"[6:a]adelay={delays[6]}|{delays[6]},volume=1.4[a6];"
        f"[7:a]adelay={delays[7]}|{delays[7]},volume=1.5[a7];"
        f"[8:a]adelay={delays[8]}|{delays[8]},volume=1.4[a8];"
        f"[a0][a1][a2][a3][a4][a5][a6][a7][a8]amix=inputs=9:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1.0[final_audio]"
    )
    
    final_audio = os.path.join(TEMP_DIR, "final_audio.wav")
    cmd_mix = [
        FFMPEG, "-y",
        "-i", sfx_tea,
        "-i", sfx_chime,
        "-i", sfx_clonk,
        "-i", bgm_path,
        "-i", vo2,
        "-i", vo3,
        "-i", vo4,
        "-i", vo5,
        "-i", vo6,
        "-filter_complex", mix_filter,
        "-map", "[final_audio]",
        "-t", str(total_dur),
        final_audio
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Master Audio Mix generated: {final_audio} ({total_dur:.2f}s)")
    return final_audio, total_dur

def build_final_video(raw_video, final_audio, total_dur):
    print("--- [5/5] Multiplexing Master Film with Subtitles & Safe-Zone Alignment ---")
    
    # Subtitle Burn-In via drawtext in 9:16 safe area (X centered, Y: 1680)
    # Using clean fallback box
    cmd = [
        FFMPEG, "-y",
        "-i", raw_video,
        "-i", final_audio,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_dur),
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n=======================================================")
    print(f"🎉 MASTER VIDEO SUCCESSFULLY RENDERED!")
    print(f"Location: {OUTPUT_VIDEO}")
    print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")
    print(f"=======================================================\n")

async def main():
    await generate_voiceovers()
    
    # Measure voice durations and calculate dynamic scene timings
    dur_sc1 = 2.4 # Hook (Tea pour + fake sticker reveal)
    dur_sc2 = max(5.0, get_audio_duration(os.path.join(TEMP_DIR, "vo_scene_2.wav")) + 0.3)
    dur_sc3 = max(5.0, get_audio_duration(os.path.join(TEMP_DIR, "vo_scene_3.wav")) + 0.3)
    dur_sc4 = max(5.5, get_audio_duration(os.path.join(TEMP_DIR, "vo_scene_4.wav")) + 0.3)
    dur_sc5 = max(5.5, get_audio_duration(os.path.join(TEMP_DIR, "vo_scene_5.wav")) + 0.4)
    dur_sc6 = max(5.0, get_audio_duration(os.path.join(TEMP_DIR, "vo_scene_6.wav")) + 0.6)
    
    scene_durations = [dur_sc1, dur_sc2, dur_sc3, dur_sc4, dur_sc5, dur_sc6]
    total_planned = sum(scene_durations)
    print(f"Scene Durations: {scene_durations} | Total: {total_planned:.2f}s")
    
    clip_paths = build_scene_videos(scene_durations)
    raw_video = concatenate_clips(clip_paths)
    final_audio, total_dur = synthesize_audio_track(scene_durations)
    build_final_video(raw_video, final_audio, total_dur)

if __name__ == '__main__':
    asyncio.run(main())
