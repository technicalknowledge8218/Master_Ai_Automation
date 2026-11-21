import os
import sys
import json
import math
import subprocess
import numpy as np
import soundfile as sf
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SFX_DIR = os.path.join(BASE_DIR, "sfx")
REF_ASSETS = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
BGM_SOURCE = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\bgm_authentic_track.wav"
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(BASE_DIR, "oracle_cloud_master_reel.mp4")
TEMP_VIDEO_TRACK = os.path.join(BASE_DIR, "temp_video.mp4")
TEMP_AUDIO_TRACK = os.path.join(BASE_DIR, "temp_audio.wav")

# 1. Load Audio and Calculate Timeline Schedule
SCENES = [
    {
        "id": "scene1_hook",
        "file": "scene1_hook.mp3",
        "bg_color": (15, 23, 42, 255),      # Slate 900
        "tag": "CRITICAL ALERT",
        "card": "card_warning.png",
        "char": "clean_junior_shrug.png",
        "char_side": "right",
        "bubble_title": "⚠️ WARNING:",
        "bubble_text": "Don't let your free VM die!",
        "subtitle": "Oracle Cloud Free Server 7 Din Mein DELETE Ho Jayega?!",
        "sfx": "alarm.wav"
    },
    {
        "id": "scene2_problem",
        "file": "scene2_problem.mp3",
        "bg_color": (38, 16, 24, 255),      # Dark Crimson
        "tag": "IDLE RECLAMATION POLICY",
        "card": "gauge_cpu_6.png",
        "char": "clean_senior_pointing_up.png",
        "char_side": "left",
        "bubble_title": "📊 OCI THRESHOLD:",
        "bubble_text": "CPU < 20% = INSTANCE TERMINATED!",
        "subtitle": "Oracle Rule: CPU < 20% = Server Terminated & Data Lost!",
        "sfx": "pop.wav"
    },
    {
        "id": "scene3_fix1_payg",
        "file": "scene3_fix1_payg.mp3",
        "bg_color": (10, 35, 26, 255),      # Deep Emerald
        "tag": "100% PERMANENT FIX",
        "card": "card_payg.png",
        "char": "clean_junior_pointing.png",
        "char_side": "right",
        "bubble_title": "💡 OFFICIAL FIX:",
        "bubble_text": "Upgrade to PAYG (Rs. 0 Bill Forever)",
        "subtitle": "Method 1: Upgrade to PAYG ($0 Bill Forever & Lifetime Safe)",
        "sfx": "chime.wav"
    },
    {
        "id": "scene4_fix2_script",
        "file": "scene4_fix2_script.mp3",
        "bg_color": (16, 24, 40, 255),      # Tech Slate
        "tag": "CLI AUTOMATION FIX",
        "card": "card_terminal.png",
        "char": "clean_senior_pointing_up.png",
        "char_side": "left",
        "bubble_title": "⚡ AUTOMATION FIX:",
        "bubble_text": "Run 'lookbusy' daemon (Keep CPU at 22%)",
        "subtitle": "Method 2: Run 'lookbusy' Tool (Keep CPU at 22%)",
        "sfx": "pop.wav"
    },
    {
        "id": "scene5_cta",
        "file": "scene5_cta.mp3",
        "bg_color": (28, 20, 50, 255),      # Modern Indigo
        "tag": "SAVE & SHARE REEL",
        "card": "card_cta.png",
        "char": "clean_junior_pointing.png",
        "char_side": "right",
        "bubble_title": "📩 GET COMMANDS:",
        "bubble_text": "Comment 'ORACLE' for 1-click script!",
        "subtitle": "Save Reel & Comment 'ORACLE' for Full Setup Commands!",
        "sfx": "chime.wav"
    }
]

def build_timeline():
    cur_t = 0.0
    schedule = {}
    audio_data = {}
    target_sr = 44100
    
    for s in SCENES:
        p = os.path.join(AUDIO_DIR, s["file"])
        data, sr = sf.read(p)
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        dur = len(data) / sr
        
        schedule[s["id"]] = {
            "start": cur_t,
            "end": cur_t + dur,
            "dur": dur,
            "config": s
        }
        audio_data[s["id"]] = {"data": data, "sr": sr}
        cur_t += dur + 0.15  # tight 0.15s gap between scenes
        
    total_dur = cur_t + 0.5
    return schedule, audio_data, total_dur, target_sr

schedule, audio_data, total_dur, target_sr = build_timeline()
print(f"Total Video Planned Duration: {total_dur:.2f}s")

# 2. Build Multi-Track Audio Master (Voice + SFX + BGM)
def compile_audio(total_dur, target_sr):
    total_samples = int(total_dur * target_sr)
    master = np.zeros(total_samples, dtype=np.float32)
    
    # A. Place Speech Tracks
    for sid, sinfo in schedule.items():
        data = audio_data[sid]["data"]
        sr = audio_data[sid]["sr"]
        # Resample to target_sr if needed
        if sr != target_sr:
            indices = np.round(np.arange(0, len(data), sr / target_sr)).astype(int)
            indices = indices[indices < len(data)]
            data = data[indices]
            
        start_idx = int(sinfo["start"] * target_sr)
        end_idx = min(total_samples, start_idx + len(data))
        seg_len = end_idx - start_idx
        master[start_idx:end_idx] += data[:seg_len] * 1.15
        
        # B. Place SFX at scene start
        sfx_name = sinfo["config"]["sfx"]
        sfx_path = os.path.join(SFX_DIR, sfx_name)
        if os.path.exists(sfx_path):
            sdata, ssr = sf.read(sfx_path)
            if len(sdata.shape) > 1: sdata = sdata.mean(axis=1)
            s_end = min(total_samples, start_idx + len(sdata))
            master[start_idx:s_end] += sdata[:s_end - start_idx] * 0.4
            
    # C. Loop Background Music at -18dB ducking
    if os.path.exists(BGM_SOURCE):
        bgm_data, bsr = sf.read(BGM_SOURCE)
        if len(bgm_data.shape) > 1: bgm_data = bgm_data.mean(axis=1)
        # Repeat BGM to fill duration
        repeats = int(np.ceil(total_samples / len(bgm_data)))
        bgm_full = np.tile(bgm_data, repeats)[:total_samples]
        master += bgm_full * 0.12 # clean lo-fi ducking
        
    # Master Limiter
    max_val = np.max(np.abs(master))
    if max_val > 0.95:
        master = master * (0.95 / max_val)
        
    sf.write(TEMP_AUDIO_TRACK, master, target_sr)
    print("Master Audio Compiled:", TEMP_AUDIO_TRACK)

compile_audio(total_dur, target_sr)

# 3. Load Visual Resources
CARDS = {}
for name in ["card_warning.png", "gauge_cpu_6.png", "gauge_cpu_24.png", "card_payg.png", "card_terminal.png", "card_cta.png"]:
    p = os.path.join(ASSETS_DIR, name)
    if os.path.exists(p):
        CARDS[name] = Image.open(p).convert("RGBA")

SPRITES = {
    "clean_junior_pointing.png": Image.open(os.path.join(REF_ASSETS, "clean_junior_pointing.png")).convert("RGBA"),
    "clean_junior_shrug.png": Image.open(os.path.join(REF_ASSETS, "clean_junior_shrug.png")).convert("RGBA"),
    "clean_senior_pointing_up.png": Image.open(os.path.join(REF_ASSETS, "clean_senior_pointing_up.png")).convert("RGBA")
}

FONT_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_BUBBLE_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
FONT_BUBBLE_TEXT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)

# 4. Draw Single Frame
def draw_frame(f_idx, fps, schedule, total_dur):
    t = f_idx / fps
    w, h = 1080, 1920
    
    # Find active scene
    active_sid = "scene1_hook"
    active_sinfo = schedule["scene1_hook"]
    for sid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"] + 0.15:
            active_sid = sid
            active_sinfo = sinfo
            break
            
    cfg = active_sinfo["config"]
    scene_rel_t = t - active_sinfo["start"]
    
    # Canvas
    im = Image.new("RGBA", (w, h), cfg["bg_color"])
    draw = ImageDraw.Draw(im)
    
    # A. Top Progress Bar (Reel Scrub indicator)
    progress_pct = min(1.0, t / total_dur)
    draw.rectangle([0, 0, w, 8], fill=(30, 41, 59, 255))
    draw.rectangle([0, 0, int(w * progress_pct), 8], fill=(6, 182, 212, 255))
    
    # B. Header Tag Banner
    draw.rounded_rectangle([60, 85, w - 60, 165], radius=16, fill=(15, 23, 42, 235), outline=(51, 65, 85, 255), width=2)
    draw.text((90, 107), f"🔥 TECH LIFE HACK  |  {cfg['tag']}", font=FONT_TAG, fill=(6, 182, 212, 255))
    
    # C. Main Category Title
    draw.text((60, 205), "ORACLE CLOUD FREE TIER", font=FONT_HEADER, fill=(255, 255, 255, 255))
    
    # D. Card Slide-in Animation (Spring easing)
    card_img = CARDS.get(cfg["card"])
    if card_img:
        cw, ch = card_img.size
        # Slide in from top (0s to 0.35s)
        slide_progress = min(1.0, scene_rel_t / 0.35)
        # overshoot spring
        ease = 1.0 + 0.12 * math.sin(slide_progress * math.pi) if slide_progress < 1.0 else 1.0
        
        target_cy = 310
        cur_cy = int(target_cy - (1.0 - slide_progress) * 180)
        cx = (w - cw) // 2
        
        im.paste(card_img, (cx, cur_cy), card_img)
        
    # E. Character Presentation (Lower Section)
    char_img = SPRITES.get(cfg["char"])
    if char_img:
        ch_w, ch_h = char_img.size
        target_h = 820
        target_w = int(ch_w * (target_h / ch_h))
        
        # Subtle speaking bounce (scale 1.0 -> 1.015)
        bob = math.sin(t * 12.0) * 6.0
        
        char_resized = char_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        if cfg["char_side"] == "right":
            char_x = w - target_w + 35
            char_y = int(h - target_h + 30 + bob)
        else:
            char_x = -35
            char_y = int(h - target_h + 30 + bob)
            
        im.paste(char_resized, (char_x, char_y), char_resized)
        
    # F. Speech Callout Bubble
    bubble_w, bubble_h = 600, 140
    bx = 60 if cfg["char_side"] == "right" else w - 60 - bubble_w
    by = h - 660
    draw.rounded_rectangle([bx, by, bx + bubble_w, by + bubble_h], radius=20, fill=(15, 23, 42, 240), outline=(6, 182, 212, 255), width=3)
    draw.text((bx + 30, by + 22), cfg["bubble_title"], font=FONT_BUBBLE_TITLE, fill=(245, 158, 11, 255))
    draw.text((bx + 30, by + 65), cfg["bubble_text"], font=FONT_BUBBLE_TEXT, fill=(255, 255, 255, 255))
    
    # G. Bottom Kinetic Subtitle Box
    sub_box_y = h - 220
    draw.rounded_rectangle([50, sub_box_y, w - 50, sub_box_y + 140], radius=18, fill=(10, 15, 26, 245), outline=(30, 41, 59, 255), width=2)
    
    sub_words = cfg["subtitle"].split()
    half = len(sub_words) // 2 + 1
    line1 = " ".join(sub_words[:half])
    line2 = " ".join(sub_words[half:])
    
    draw.text((80, sub_box_y + 25), line1, font=FONT_SUBTITLE, fill=(255, 255, 255, 255))
    draw.text((80, sub_box_y + 75), line2, font=FONT_SUBTITLE, fill=(250, 204, 21, 255))
    
    return im.convert("RGB")

# 5. Render Video Frames & Stream Directly to FFmpeg
fps = 30
total_frames = int(total_dur * fps)
print(f"--- Streaming {total_frames} Frames @ {fps}fps to FFmpeg ({total_dur:.2f}s) ---")

cmd_video = [
    FFMPEG, "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", "1080x1920",
    "-pix_fmt", "rgb24",
    "-r", str(fps),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-crf", "20",
    TEMP_VIDEO_TRACK
]

proc = subprocess.Popen(cmd_video, stdin=subprocess.PIPE)

snapshot_targets = {
    int(schedule["scene1_hook"]["start"] * fps) + 35: "snap_1_hook.jpg",
    int(schedule["scene2_problem"]["start"] * fps) + 35: "snap_2_problem.jpg",
    int(schedule["scene3_fix1_payg"]["start"] * fps) + 35: "snap_3_payg.jpg",
    int(schedule["scene4_fix2_script"]["start"] * fps) + 35: "snap_4_script.jpg",
    int(schedule["scene5_cta"]["start"] * fps) + 25: "snap_5_cta.jpg"
}

for f in range(total_frames):
    frame_img = draw_frame(f, fps, schedule, total_dur)
    
    # Save Keyframe Snapshots
    if f in snapshot_targets:
        sname = snapshot_targets[f]
        sp = os.path.join(SNAPSHOTS_DIR, sname)
        frame_img.save(sp, quality=95)
        print(f"Saved snapshot {sname} at frame {f}")
        
    proc.stdin.write(frame_img.tobytes())
    if f % 250 == 0 or f == total_frames - 1:
        pct = (f / total_frames) * 100
        print(f"Rendered Frame {f}/{total_frames} ({pct:.1f}%)")

proc.stdin.close()
proc.wait()
print("Video Stream Complete:", TEMP_VIDEO_TRACK)

# 6. Mux Final Broadcast MP4 with AAC Audio
print("--- Assembling Final Broadcast Master MP4 ---")
cmd_mux = [
    FFMPEG, "-y",
    "-i", TEMP_VIDEO_TRACK,
    "-i", TEMP_AUDIO_TRACK,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_VIDEO
]
subprocess.run(cmd_mux, check=True)

print(f"\n🎉 MASTER REEL COMPLETED: {OUTPUT_VIDEO}")
print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")
