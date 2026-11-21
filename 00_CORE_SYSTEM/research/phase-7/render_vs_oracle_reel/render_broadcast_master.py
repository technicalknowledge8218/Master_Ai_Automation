import os
import json
import math
import subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# --- Directory Paths ---
PROJECT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\render_vs_oracle_reel"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
SFX_DIR = os.path.join(PROJECT_DIR, "sfx")
REF_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\ref_billu_frames"
OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "render_vs_oracle_broadcast_master.mp4")
TEMP_VIDEO = os.path.join(PROJECT_DIR, "temp_broadcast_video.mp4")
TEMP_AUDIO = os.path.join(PROJECT_DIR, "temp_broadcast_audio.wav")
SNAPSHOT_DIR = os.path.join(PROJECT_DIR, "snapshots_broadcast")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# --- Load Audio Cues & Assembly ---
with open(os.path.join(AUDIO_DIR, "render_vs_oracle_meta.json"), "r", encoding="utf-8") as f:
    dialogue_cues = json.load(f)

# Total video duration & cue timeline
sr = 44100
timeline = []
cur_time = 0.0

for c in dialogue_cues:
    timeline.append({
        "id": c["id"],
        "speaker": c["speaker"],
        "speaking": c["speaking"],
        "sub": c["sub"],
        "start": cur_time,
        "end": cur_time + c["dur"],
        "dur": c["dur"],
        "wav": c["wav"]
    })
    cur_time += c["dur"]

total_duration = cur_time
total_samples = int(total_duration * sr)
master_audio = np.zeros(total_samples, dtype=np.float32)

# 1. Mix Dialogue
for c in timeline:
    data, r = sf.read(c["wav"])
    if r != sr:
        # Resample if needed
        pass
    start_s = int(c["start"] * sr)
    end_s = start_s + len(data)
    if end_s > total_samples:
        data = data[:total_samples - start_s]
        end_s = total_samples
    master_audio[start_s:end_s] += data * 0.95

# 2. Mix Lo-fi Background Music (-22dB)
bg_path = os.path.join(SFX_DIR, "lofi_bg_track.wav")
if os.path.exists(bg_path):
    bg_data, _ = sf.read(bg_path)
    # Loop bg track to match total_duration
    repeats = int(math.ceil(total_samples / len(bg_data)))
    bg_full = np.tile(bg_data, repeats)[:total_samples]
    master_audio += bg_full * 0.40

# 3. Mix Spot SFX at Precise Narrative Timestamps
def add_sfx(sfx_name, t_sec, vol=0.5):
    p = os.path.join(SFX_DIR, sfx_name)
    if os.path.exists(p):
        sfx_data, _ = sf.read(p)
        st = int(t_sec * sr)
        en = min(total_samples, st + len(sfx_data))
        master_audio[st:en] += sfx_data[:en - st] * vol

# Add whooshes at scene cuts
for c in timeline:
    if c["start"] > 0:
        add_sfx("whoosh.wav", c["start"] - 0.12, vol=0.35)

# Add pops and dings
add_sfx("pop.wav", timeline[1]["start"] + 1.2, vol=0.45) # Render 1-click
add_sfx("buzz.wav", timeline[1]["start"] + 6.5, vol=0.45) # 15-min sleep trap
add_sfx("buzz.wav", timeline[2]["start"] + 2.0, vol=0.40) # Discord bot dies
add_sfx("ding.wav", timeline[3]["start"] + 2.5, vol=0.50) # Oracle 4 OCPU
add_sfx("ding.wav", timeline[3]["start"] + 6.0, vol=0.55) # Oracle 24GB RAM
add_sfx("ding.wav", timeline[3]["start"] + 9.5, vol=0.55) # Oracle 200GB SSD
add_sfx("pop.wav", timeline[4]["start"] + 2.0, vol=0.45) # Decision matrix
add_sfx("ding.wav", timeline[5]["start"] + 1.0, vol=0.50) # Outro CTA

# Normalize master audio to -1dB peak
peak = np.max(np.abs(master_audio))
if peak > 0:
    master_audio = master_audio / peak * 0.92

sf.write(TEMP_AUDIO, master_audio, sr)
print(f"Master Mixed Audio Ready: {TEMP_AUDIO} ({total_duration:.2f}s)")

# --- Base Frames Setup (Scaled to 1080x1920) ---
W, H = 1080, 1920
scale_x = W / 720.0
scale_y = H / 1280.0

raw_frames = {
    "line1_boy": Image.open(os.path.join(REF_DIR, "frame_1.0s.jpg")).convert("RGB"),
    "line2_sci": Image.open(os.path.join(REF_DIR, "frame_20.0s.jpg")).convert("RGB"),
    "line3_boy": Image.open(os.path.join(REF_DIR, "frame_12.0s.jpg")).convert("RGB"),
    "line4_sci": Image.open(os.path.join(REF_DIR, "frame_25.0s.jpg")).convert("RGB"),
    "line5_sci": Image.open(os.path.join(REF_DIR, "frame_35.0s.jpg")).convert("RGB"),
    "line6_duo": Image.open(os.path.join(REF_DIR, "frame_30.0s.jpg")).convert("RGB"),
}

# Paste open eyes on line1_boy
boy_eyes_open = raw_frames["line2_sci"].crop((140, 770, 270, 860))
raw_frames["line1_boy"].paste(boy_eyes_open, (140, 770))

base_images = {}
for k, img in raw_frames.items():
    base_images[k] = img.resize((W, H), Image.Resampling.LANCZOS)

# Fonts (1080p scaled)
FONT_WB_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
FONT_WB_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28)
FONT_WB_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 30)
FONT_WB_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)

# Whiteboard coordinates in 1080x1920:
# 720x1280: x=52..668, y=105..642
# 1080x1920: x=78..1002, y=158..963
WB_X0, WB_Y0, WB_X1, WB_Y1 = 78, 158, 1002, 963

# --- Dynamic Kinetic Whiteboard Renderer ---
def draw_kinetic_whiteboard(draw, scene_id, rel_t):
    # Base clear white canvas
    draw.rectangle([WB_X0, WB_Y0, WB_X1, WB_Y1], fill=(255, 255, 255))
    
    x0 = WB_X0 + 25
    y0 = WB_Y0 + 25
    
    if scene_id == "line1_boy":
        # Scene 1: Clash Hook
        draw.text((x0, y0), "RENDER  vs  ORACLE CLOUD", font=FONT_WB_TITLE, fill=(15, 23, 42))
        draw.rectangle([x0, y0 + 55, x0 + 440, y0 + 100], fill=(238, 242, 255), outline=(99, 102, 241), width=3)
        draw.text((x0 + 15, y0 + 62), "[FREE TIER CLASH: PaaS vs IaaS]", font=FONT_WB_TAG, fill=(67, 56, 202))
        
        draw.text((x0, y0 + 125), "Sawaal: Full-Stack App Kahan Host Karein?", font=FONT_WB_BODY, fill=(100, 116, 139))
        
        # Render Box pops at rel_t >= 0.5s
        if rel_t >= 0.5:
            draw.rectangle([x0, y0 + 175, x0 + 870, y0 + 300], fill=(245, 243, 255), outline=(147, 51, 234), width=3)
            draw.text((x0 + 25, y0 + 190), "🟣 RENDER.COM (PaaS - Web Service)", font=FONT_WB_BOLD, fill=(126, 34, 206))
            draw.text((x0 + 25, y0 + 245), "1-Click Git Deploy • Free • 512MB RAM Limit", font=FONT_WB_BODY, fill=(88, 28, 135))
            
        # Oracle Box pops at rel_t >= 2.5s
        if rel_t >= 2.5:
            draw.rectangle([x0, y0 + 325, x0 + 870, y0 + 450], fill=(254, 242, 242), outline=(239, 68, 68), width=3)
            draw.text((x0 + 25, y0 + 340), "🔴 ORACLE CLOUD (IaaS - ARM VPS)", font=FONT_WB_BOLD, fill=(185, 28, 28))
            draw.text((x0 + 25, y0 + 395), "4 OCPU • 24GB RAM • 200GB SSD • Always Free", font=FONT_WB_BODY, fill=(153, 27, 27))
            
        # Bottom Question
        if rel_t >= 4.5:
            draw.rectangle([x0, y0 + 480, x0 + 870, y0 + 580], fill=(254, 249, 195), outline=(202, 138, 4), width=3)
            draw.text((x0 + 35, y0 + 510), "Kismein Hoga $0 Bill & Best Performance?", font=FONT_WB_TITLE, fill=(133, 77, 14))

    elif scene_id == "line2_sci":
        # Scene 2: Render Cold Start Trap
        draw.text((x0, y0), "OPTION 1: RENDER.COM (PaaS)", font=FONT_WB_TITLE, fill=(126, 34, 206))
        draw.rectangle([x0, y0 + 55, x0 + 380, y0 + 100], fill=(245, 243, 255), outline=(147, 51, 234), width=3)
        draw.text((x0 + 15, y0 + 62), "[THE FREE TIER LIMITS]", font=FONT_WB_TAG, fill=(126, 34, 206))

        draw.text((x0 + 15, y0 + 125), "[PASS] Super Easy 1-Click Git Deploy", font=FONT_WB_BODY, fill=(22, 101, 52))
        draw.text((x0 + 15, y0 + 175), "[WARN] Memory: Sirf 512MB RAM & 0.1 vCPU", font=FONT_WB_BODY, fill=(180, 83, 9))

        # Critical Trap Box pops at rel_t >= 4.0s
        if rel_t >= 4.0:
            draw.rectangle([x0, y0 + 230, x0 + 870, y0 + 410], fill=(254, 242, 242), outline=(220, 38, 38), width=3)
            draw.text((x0 + 25, y0 + 245), "[!] CRITICAL TRAP: 15-Min Inactivity Sleep!", font=FONT_WB_BOLD, fill=(185, 28, 28))
            draw.text((x0 + 25, y0 + 300), "15 minute traffic na aane par server SO JATA HAI!", font=FONT_WB_BODY, fill=(153, 27, 27))
            draw.text((x0 + 25, y0 + 345), "Agla user aane par: 50+ SECONDS COLD START!", font=FONT_WB_BOLD, fill=(185, 28, 28))

        # Animated Delay Bar
        if rel_t >= 7.0:
            draw.text((x0 + 15, y0 + 435), "User Loading Experience (50s Delay):", font=FONT_WB_BODY, fill=(100, 116, 139))
            draw.rectangle([x0 + 15, y0 + 480, x0 + 855, y0 + 520], fill=(241, 245, 249), outline=(203, 213, 225), width=2)
            progress = min(1.0, (rel_t - 7.0) / 7.0)
            fill_w = int(836 * progress)
            draw.rectangle([x0 + 17, y0 + 482, x0 + 17 + fill_w, y0 + 518], fill=(239, 68, 68))
            draw.text((x0 + 25, y0 + 540), "Spin-Down Wait: ~50 Seconds (User swipes away!)", font=FONT_WB_BODY, fill=(220, 38, 38))

    elif scene_id == "line3_boy":
        # Scene 3: Cold Start Nightmare
        draw.text((x0, y0), "THE COLD START NIGHTMARE", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.rectangle([x0, y0 + 55, x0 + 410, y0 + 100], fill=(254, 242, 242), outline=(239, 68, 68), width=3)
        draw.text((x0 + 15, y0 + 62), "[WHAT BREAKS ON RENDER]", font=FONT_WB_TAG, fill=(185, 28, 28))

        if rel_t >= 1.0:
            draw.rectangle([x0, y0 + 125, x0 + 870, y0 + 235], fill=(255, 247, 237), outline=(234, 88, 12), width=3)
            draw.text((x0 + 25, y0 + 140), "1. Discord / Telegram Bots -> DIE!", font=FONT_WB_BOLD, fill=(194, 65, 12))
            draw.text((x0 + 25, y0 + 185), "WebSocket disconnect ho jata hai jab server so jata hai!", font=FONT_WB_BODY, fill=(154, 52, 18))

        if rel_t >= 3.5:
            draw.rectangle([x0, y0 + 255, x0 + 870, y0 + 365], fill=(255, 247, 237), outline=(234, 88, 12), width=3)
            draw.text((x0 + 25, y0 + 270), "2. Cron Jobs & Webhooks -> MISSED!", font=FONT_WB_BOLD, fill=(194, 65, 12))
            draw.text((x0 + 25, y0 + 315), "Scheduled tasks trigger nahi hote jab container idle hai!", font=FONT_WB_BODY, fill=(154, 52, 18))

        if rel_t >= 6.0:
            draw.rectangle([x0, y0 + 385, x0 + 870, y0 + 495], fill=(254, 242, 242), outline=(220, 38, 38), width=3)
            draw.text((x0 + 25, y0 + 400), "3. Free PostgreSQL -> Deleted in 90 Days!", font=FONT_WB_BOLD, fill=(185, 28, 28))
            draw.text((x0 + 25, y0 + 445), "Render ka free database 90 din baad delete ho jata hai!", font=FONT_WB_BODY, fill=(153, 27, 27))

        if rel_t >= 8.0:
            draw.text((x0 + 30, y0 + 525), "Toh 24/7 Always-On Free Solution Kahan Hai?!", font=FONT_WB_TITLE, fill=(15, 23, 42))

    elif scene_id == "line4_sci":
        # Scene 4: Oracle Cloud Monster Specs
        draw.text((x0, y0), "OPTION 2: ORACLE CLOUD (IaaS)", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.rectangle([x0, y0 + 55, x0 + 430, y0 + 100], fill=(254, 242, 242), outline=(239, 68, 68), width=3)
        draw.text((x0 + 15, y0 + 62), "[THE UNBEATABLE FREE BEAST]", font=FONT_WB_TAG, fill=(185, 28, 28))

        specs = [
            ("CPU:", "4 Ampere ARM OCPU (High Performance)", 1.0),
            ("RAM:", "24GB DDR4 Memory (Full Server Power!)", 4.0),
            ("STORAGE:", "200GB NVMe SSD Block Volume Free!", 7.5),
            ("UPTIME:", "24/7 Always ON — ZERO Spin-Down!", 11.0),
        ]

        sy = y0 + 125
        for lbl, desc, trigger_t in specs:
            if rel_t >= trigger_t:
                draw.rectangle([x0, sy, x0 + 870, sy + 80], fill=(240, 253, 244), outline=(34, 197, 94), width=3)
                draw.text((x0 + 25, sy + 10), lbl, font=FONT_WB_BOLD, fill=(21, 128, 61))
                draw.text((x0 + 25, sy + 44), desc, font=FONT_WB_BODY, fill=(22, 101, 52))
            sy += 95

        if rel_t >= 14.0:
            draw.rectangle([x0, sy, x0 + 870, sy + 75], fill=(254, 249, 195), outline=(202, 138, 4), width=2)
            draw.text((x0 + 25, sy + 20), "Catch: Linux VPS Setup (SSH, Nginx, Docker)", font=FONT_WB_BODY, fill=(133, 77, 14))

    elif scene_id == "line5_sci":
        # Scene 5: Decision Matrix
        draw.text((x0, y0), "DIRECT COMPARISON: KISE CHUNEIN?", font=FONT_WB_TITLE, fill=(15, 23, 42))
        draw.rectangle([x0, y0 + 55, x0 + 420, y0 + 100], fill=(241, 245, 249), outline=(100, 116, 139), width=3)
        draw.text((x0 + 15, y0 + 62), "[CLEAR DECISION MATRIX]", font=FONT_WB_TAG, fill=(51, 65, 85))

        if rel_t >= 0.8:
            draw.rectangle([x0, y0 + 125, x0 + 870, y0 + 285], fill=(245, 243, 255), outline=(147, 51, 234), width=3)
            draw.text((x0 + 25, y0 + 140), "🟣 CHOOSE RENDER AGAR:", font=FONT_WB_BOLD, fill=(126, 34, 206))
            draw.text((x0 + 25, y0 + 190), "• Quick Portfolio / College Hackathon Demos", font=FONT_WB_BODY, fill=(88, 28, 135))
            draw.text((x0 + 25, y0 + 235), "• Sirf 1-Click mein deploy chahiye (Zero Linux)", font=FONT_WB_BODY, fill=(88, 28, 135))

        if rel_t >= 4.5:
            draw.rectangle([x0, y0 + 310, x0 + 870, y0 + 470], fill=(240, 253, 244), outline=(34, 197, 94), width=3)
            draw.text((x0 + 25, y0 + 325), "🔴 CHOOSE ORACLE CLOUD AGAR:", font=FONT_WB_BOLD, fill=(21, 128, 61))
            draw.text((x0 + 25, y0 + 375), "• 24/7 Always-ON Backend, Discord/Telegram Bots", font=FONT_WB_BODY, fill=(22, 101, 52))
            draw.text((x0 + 25, y0 + 420), "• Heavy PostgreSQL/Redis Database & Docker Apps", font=FONT_WB_BODY, fill=(22, 101, 52))

        if rel_t >= 9.0:
            draw.rectangle([x0, y0 + 495, x0 + 870, y0 + 565], fill=(254, 249, 195), outline=(202, 138, 4), width=2)
            draw.text((x0 + 25, y0 + 515), "Pro Tip: PAYG upgrade karlo to lifetime $0 bill!", font=FONT_WB_BODY, fill=(133, 77, 14))

    elif scene_id == "line6_duo":
        # Scene 6: Outro & Call to Action
        draw.text((x0, y0), "GET CLOUD SETUP CHEATSHEET", font=FONT_WB_TITLE, fill=(15, 23, 42))
        draw.rectangle([x0, y0 + 55, x0 + 400, y0 + 100], fill=(238, 242, 255), outline=(99, 102, 241), width=3)
        draw.text((x0 + 15, y0 + 62), "[STEP-BY-STEP DEPLOY GUIDE]", font=FONT_WB_TAG, fill=(67, 56, 202))

        steps = [
            ("1. SAVE THIS REEL for your next project", "Kyunki deploy karte waqt ye details kaam aayengi!", (254, 249, 195), (133, 77, 14), 0.5),
            ("2. COMMENT 'COMPARE' BELOW!", "Auto-DM: Full Oracle 24GB VPS & Docker Script!", (240, 253, 244), (21, 128, 61), 2.5),
            ("3. Share with your Developer Friends!", "Save money & avoid 50-second cold starts!", (238, 242, 255), (67, 56, 202), 5.0),
        ]

        sy = y0 + 125
        for title_s, desc_s, bg_c, txt_c, trig_t in steps:
            if rel_t >= trig_t:
                draw.rectangle([x0, sy, x0 + 870, sy + 110], fill=bg_c, outline=txt_c, width=3)
                draw.text((x0 + 30, sy + 15), title_s, font=FONT_WB_BOLD, fill=txt_c)
                draw.text((x0 + 30, sy + 62), desc_s, font=FONT_WB_BODY, fill=txt_c)
            sy += 135

# --- Main Render Loop (1080x1920 @ 30 FPS) ---
FPS = 30
TOTAL_FRAMES = int(total_duration * FPS)

ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "faster",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    TEMP_VIDEO
]

print(f"--- Starting 1080p Broadcast Render: {TOTAL_FRAMES} frames ({total_duration:.2f}s) ---")
pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS

    # Active cue
    active_cue = timeline[-1]
    for c in timeline:
        if c["start"] <= t < c["end"]:
            active_cue = c
            break

    scene_id = active_cue["id"]
    rel_t = t - active_cue["start"]
    speaker = active_cue["speaking"]

    # Base image for scene
    frame = base_images[scene_id].copy()
    draw = ImageDraw.Draw(frame)

    # 1. Kinetic Whiteboard
    draw_kinetic_whiteboard(draw, scene_id, rel_t)

    # 2. Dynamic 4-Viseme Lip Sync & Speech Bobbing
    # In 1080x1920:
    # Boy mouth: x ~ 270..335, y ~ 1325..1365
    # Dr Billu mouth: x ~ 750..820, y ~ 1344..1385
    viseme_cycle = int(rel_t * 7.0) % 4
    is_blinking = (math.sin(t * 1.95) > 0.96)
    bob_y = int(3.0 * math.sin(rel_t * 12.0)) if rel_t > 0.2 else 0

    bx0, by0, bx1, by1 = int(180 * scale_x), int(885 * scale_y) + bob_y, int(225 * scale_x), int(910 * scale_y) + bob_y
    sx0, sy0, sx1, sy1 = int(500 * scale_x), int(896 * scale_y) + bob_y, int(546 * scale_x), int(923 * scale_y) + bob_y

    if speaker == "boy":
        # Boy is speaking (Cycle 4 visemes)
        if viseme_cycle == 0:
            # REST
            draw.rectangle([bx0, by0, bx1, by1], fill=(242, 179, 149))
            draw.line([bx0 + 8, by0 + 15, bx1 - 8, by0 + 15], fill=(80, 40, 30), width=4)
        elif viseme_cycle == 1:
            # AH (Open Vowel)
            draw.rectangle([bx0, by0, bx1, by1], fill=(242, 179, 149))
            draw.ellipse([bx0 + 6, by0 + 2, bx1 - 6, by1 - 2], fill=(25, 12, 16))
            draw.ellipse([bx0 + 9, by0 + 5, bx1 - 9, by1 - 5], fill=(142, 38, 63))
            draw.rectangle([bx0 + 18, by0 + 5, bx1 - 18, by0 + 12], fill=(245, 245, 250))
            draw.ellipse([bx0 + 15, by0 + 18, bx1 - 15, by1 - 5], fill=(225, 95, 125))
        elif viseme_cycle == 2:
            # OH (Round Vowel)
            draw.rectangle([bx0, by0, bx1, by1], fill=(242, 179, 149))
            draw.ellipse([bx0 + 14, by0 + 2, bx1 - 14, by1 - 2], fill=(25, 12, 16))
            draw.ellipse([bx0 + 17, by0 + 5, bx1 - 17, by1 - 5], fill=(138, 35, 60))
            draw.ellipse([bx0 + 22, by0 + 18, bx1 - 22, by1 - 5], fill=(225, 95, 125))
        else:
            # EE (Wide Smile)
            draw.rectangle([bx0, by0, bx1, by1], fill=(242, 179, 149))
            draw.ellipse([bx0 + 4, by0 + 8, bx1 - 4, by1 - 8], fill=(25, 12, 16))
            draw.ellipse([bx0 + 7, by0 + 10, bx1 - 7, by1 - 10], fill=(142, 38, 63))
            draw.rectangle([bx0 + 14, by0 + 10, bx1 - 14, by0 + 16], fill=(245, 245, 250))

        # Dr. Billu is listening: closed mouth
        draw.rectangle([sx0, sy0, sx1, sy1], fill=(50, 32, 39))
    else:
        # Dr. Billu is speaking (Cycle 4 visemes)
        if viseme_cycle == 0:
            # REST
            draw.rectangle([sx0, sy0, sx1, sy1], fill=(50, 32, 39))
            draw.line([sx0 + 8, sy0 + 15, sx1 - 8, sy0 + 15], fill=(28, 16, 20), width=3)
        elif viseme_cycle == 1:
            # AH (Open Vowel)
            draw.rectangle([sx0, sy0, sx1, sy1], fill=(50, 32, 39))
            draw.ellipse([sx0 + 4, sy0 + 2, sx1 - 4, sy1 - 2], fill=(25, 12, 16))
            draw.ellipse([sx0 + 7, sy0 + 5, sx1 - 7, sy1 - 5], fill=(130, 28, 48))
            draw.rectangle([sx0 + 16, sy0 + 5, sx1 - 16, sy0 + 14], fill=(245, 245, 250))
            draw.ellipse([sx0 + 14, sy0 + 20, sx1 - 14, sy1 - 5], fill=(225, 85, 115))
        elif viseme_cycle == 2:
            # OH (Round Vowel)
            draw.rectangle([sx0, sy0, sx1, sy1], fill=(50, 32, 39))
            draw.ellipse([sx0 + 15, sy0 + 2, sx1 - 15, sy1 - 2], fill=(25, 12, 16))
            draw.ellipse([sx0 + 18, sy0 + 5, sx1 - 18, sy1 - 5], fill=(125, 26, 45))
            draw.ellipse([sx0 + 23, sy0 + 20, sx1 - 23, sy1 - 5], fill=(220, 80, 110))
        else:
            # EE (Wide Smile)
            draw.rectangle([sx0, sy0, sx1, sy1], fill=(50, 32, 39))
            draw.ellipse([sx0 + 3, sy0 + 8, sx1 - 3, sy1 - 8], fill=(25, 12, 16))
            draw.ellipse([sx0 + 6, sy0 + 10, sx1 - 6, sy1 - 10], fill=(130, 28, 48))
            draw.rectangle([sx0 + 12, sy0 + 10, sx1 - 12, sy0 + 16], fill=(245, 245, 250))

        # Boy is listening: closed mouth
        draw.rectangle([bx0, by0, bx1, by1], fill=(242, 179, 149))
        draw.line([bx0 + 8, by0 + 15, bx1 - 8, by0 + 15], fill=(80, 40, 30), width=4)

    # 3. Top Progress Bar
    pct = t / total_duration
    draw.rectangle([0, 0, W, 8], fill=(226, 232, 240))
    draw.rectangle([0, 0, int(W * pct), 8], fill=(99, 102, 241))

    # 4. Speaker Tag
    tag_text = active_cue["speaker"]
    tag_bg = (239, 68, 68) if speaker == "boy" else (37, 99, 235)
    draw.rectangle([60, 1630, 360, 1675], fill=tag_bg)
    draw.text((75, 1637), tag_text, font=FONT_TAG, fill=(255, 255, 255))

    # 5. Centered Modern Subtitle Pill with Word Highlight (Karaoke style)
    sub_text = active_cue["sub"]
    draw.rectangle([60, 1685, W - 60, 1820], fill=(15, 23, 42))
    draw.rectangle([60, 1685, W - 60, 1820], outline=(99, 102, 241), width=3)
    
    # Render subtitle centered
    bbox = draw.textbbox((0, 0), sub_text, font=FONT_SUB)
    sub_w = bbox[2] - bbox[0]
    sub_x = max(75, (W - sub_w) // 2)
    draw.text((sub_x, 1730), sub_text, font=FONT_SUB, fill=(255, 255, 255))

    # Pipe to FFmpeg
    pipe.stdin.write(frame.tobytes())

    # Save representative snapshots
    if f_idx in [60, 450, 950, 1450, 1850, 2200]:
        snap_p = os.path.join(SNAPSHOT_DIR, f"broadcast_snap_{f_idx}.jpg")
        frame.save(snap_p)
        print(f"Saved snapshot {snap_p} at frame {f_idx}")

    if f_idx % 300 == 0:
        print(f"Rendered {f_idx}/{TOTAL_FRAMES} frames ({f_idx*100/TOTAL_FRAMES:.1f}%)")

pipe.stdin.close()
pipe.wait()
print(f"Video stream rendered: {TEMP_VIDEO}")

# --- Mux Audio & Video Master ---
print("--- Muxing Broadcast Master ---")
cmd_mux = [
    ffmpeg_exe,
    "-y",
    "-i", TEMP_VIDEO,
    "-i", TEMP_AUDIO,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    OUTPUT_VIDEO
]
subprocess.run(cmd_mux, check=True)
print(f"🎉 BROADCAST MASTER REEL READY: {OUTPUT_VIDEO}")
