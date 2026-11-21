import os
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# --- Configuration & Paths ---
PROJECT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\render_vs_oracle_reel"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
REF_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\ref_billu_frames"
OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "render_vs_oracle_master_reel.mp4")
TEMP_VIDEO = os.path.join(PROJECT_DIR, "temp_video.mp4")
TEMP_AUDIO = os.path.join(PROJECT_DIR, "temp_audio.wav")
SNAPSHOT_DIR = os.path.join(PROJECT_DIR, "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Load metadata
with open(os.path.join(AUDIO_DIR, "render_vs_oracle_meta.json"), "r", encoding="utf-8") as f:
    dialogue_cues = json.load(f)

# Load base frames
base_images = {
    "line1_boy": Image.open(os.path.join(REF_DIR, "frame_1.0s.jpg")).convert("RGB"),
    "line2_sci": Image.open(os.path.join(REF_DIR, "frame_20.0s.jpg")).convert("RGB"),
    "line3_boy": Image.open(os.path.join(REF_DIR, "frame_12.0s.jpg")).convert("RGB"),
    "line4_sci": Image.open(os.path.join(REF_DIR, "frame_25.0s.jpg")).convert("RGB"),
    "line5_sci": Image.open(os.path.join(REF_DIR, "frame_35.0s.jpg")).convert("RGB"),
    "line6_duo": Image.open(os.path.join(REF_DIR, "frame_30.0s.jpg")).convert("RGB"),
}

# Fix line1_boy: paste open alert eyes so he is awake
boy_eyes_open = base_images["line2_sci"].crop((140, 770, 270, 860))
base_images["line1_boy"].paste(boy_eyes_open, (140, 770))

# Load fonts
FONT_WB_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_WB_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
FONT_WB_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
FONT_WB_CODE = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 19)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 21)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)

# --- Audio Master Assembly ---
# Stitch WAVs sequentially
wav_list_txt = os.path.join(PROJECT_DIR, "audio_concat.txt")
total_duration = sum(c["dur"] for c in dialogue_cues)
timeline = []
cur_time = 0.0

with open(wav_list_txt, "w", encoding="utf-8") as f:
    for c in dialogue_cues:
        p = c["wav"].replace("\\", "/")
        f.write(f"file '{p}'\n")
        timeline.append({
            "id": c["id"],
            "speaker": c["speaker"],
            "speaking": c["speaking"],
            "sub": c["sub"],
            "start": cur_time,
            "end": cur_time + c["dur"],
            "dur": c["dur"]
        })
        cur_time += c["dur"]

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
cmd_concat = f'"{ffmpeg_exe}" -y -f concat -safe 0 -i "{wav_list_txt}" -c copy "{TEMP_AUDIO}"'
subprocess.run(cmd_concat, shell=True, check=True, capture_output=True)
print(f"Total Video Duration: {cur_time:.2f}s ({int(cur_time * 30)} frames)")

# --- Whiteboard Content Renderer ---
def draw_whiteboard(draw, scene_id, rel_t):
    # Canvas area: x=52..668, y=105..642 (width=616, height=537)
    x0, y0 = 65, 115

    if scene_id == "line1_boy":
        # Scene 1: Clash Hook
        draw.text((x0, y0), "RENDER  vs  ORACLE CLOUD", font=FONT_WB_TITLE, fill=(15, 23, 42))
        draw.rectangle([x0, y0 + 38, x0 + 290, y0 + 68], fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((x0 + 10, y0 + 42), "[FREE TIER CLASH: PaaS vs IaaS]", font=FONT_WB_TAG, fill=(67, 56, 202))

        draw.text((x0, y0 + 85), "Sawaal: Full-Stack App Kahan Host Karein?", font=FONT_WB_BODY, fill=(100, 116, 139))

        # Contender 1: Render
        draw.rectangle([x0, y0 + 120, x0 + 580, y0 + 205], fill=(245, 243, 255), outline=(147, 51, 234), width=2)
        draw.text((x0 + 15, y0 + 130), "🟣 RENDER.COM (PaaS - Web Service)", font=FONT_WB_TITLE, fill=(126, 34, 206))
        draw.text((x0 + 15, y0 + 165), "1-Click GitHub Deploy • Free • 512MB RAM Limit", font=FONT_WB_BODY, fill=(88, 28, 135))

        # Contender 2: Oracle
        draw.rectangle([x0, y0 + 220, x0 + 580, y0 + 305], fill=(254, 242, 242), outline=(239, 68, 68), width=2)
        draw.text((x0 + 15, y0 + 230), "🔴 ORACLE CLOUD (IaaS - ARM VPS)", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.text((x0 + 15, y0 + 265), "4 OCPU • 24GB RAM • 200GB SSD • Always Free", font=FONT_WB_BODY, fill=(153, 27, 27))

        # Bottom punchline
        draw.rectangle([x0, y0 + 325, x0 + 580, y0 + 395], fill=(254, 249, 195), outline=(202, 138, 4), width=2)
        draw.text((x0 + 25, y0 + 345), "Kismein Hoga $0 Bill & Best Performance?", font=FONT_WB_TITLE, fill=(133, 77, 14))

    elif scene_id == "line2_sci":
        # Scene 2: Render Cold Start Trap
        draw.text((x0, y0), "OPTION 1: RENDER.COM (PaaS)", font=FONT_WB_TITLE, fill=(126, 34, 206))
        draw.rectangle([x0, y0 + 38, x0 + 260, y0 + 68], fill=(245, 243, 255), outline=(147, 51, 234), width=2)
        draw.text((x0 + 10, y0 + 42), "[THE FREE TIER LIMITS]", font=FONT_WB_TAG, fill=(126, 34, 206))

        draw.text((x0 + 10, y0 + 85), "[✓] Super Easy 1-Click Git Deploy", font=FONT_WB_BODY, fill=(22, 101, 52))
        draw.text((x0 + 10, y0 + 115), "[!] Memory: Sirf 512MB RAM & 0.1 vCPU", font=FONT_WB_BODY, fill=(180, 83, 9))

        # Critical Trap Box
        draw.rectangle([x0, y0 + 150, x0 + 580, y0 + 270], fill=(254, 242, 242), outline=(220, 38, 38), width=2)
        draw.text((x0 + 15, y0 + 160), "⚠️ CRITICAL TRAP: 15-Min Inactivity Sleep!", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.text((x0 + 15, y0 + 195), "Agar 15 minute koi traffic nahi aaya, server SO JATA HAI!", font=FONT_WB_BODY, fill=(153, 27, 27))
        draw.text((x0 + 15, y0 + 225), "Agla user aane par: 50+ SECONDS COLD START!", font=FONT_WB_TITLE, fill=(185, 28, 28))

        # Delay Visualizer
        draw.text((x0 + 10, y0 + 290), "User Loading Experience:", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.rectangle([x0 + 10, y0 + 320, x0 + 570, y0 + 348], fill=(241, 245, 249), outline=(203, 213, 225), width=2)
        delay_w = int(550 * min(1.0, rel_t / 12.0))
        draw.rectangle([x0 + 12, y0 + 322, x0 + 12 + delay_w, y0 + 346], fill=(239, 68, 68))
        draw.text((x0 + 20, y0 + 360), f"Spin-Down Wait: ~50 Seconds (User swipes away!)", font=FONT_WB_BODY, fill=(220, 38, 38))

    elif scene_id == "line3_boy":
        # Scene 3: Cold Start Nightmare
        draw.text((x0, y0), "THE COLD START NIGHTMARE", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.rectangle([x0, y0 + 38, x0 + 280, y0 + 68], fill=(254, 242, 242), outline=(239, 68, 68), width=2)
        draw.text((x0 + 10, y0 + 42), "[WHAT BREAKS ON RENDER]", font=FONT_WB_TAG, fill=(185, 28, 28))

        draw.rectangle([x0, y0 + 85, x0 + 580, y0 + 165], fill=(255, 247, 237), outline=(234, 88, 12), width=2)
        draw.text((x0 + 15, y0 + 95), "1. Discord / Telegram Bots -> DIE!", font=FONT_WB_TITLE, fill=(194, 65, 12))
        draw.text((x0 + 15, y0 + 130), "WebSocket connection breaks jab server so jata hai!", font=FONT_WB_BODY, fill=(154, 52, 18))

        draw.rectangle([x0, y0 + 180, x0 + 580, y0 + 260], fill=(255, 247, 237), outline=(234, 88, 12), width=2)
        draw.text((x0 + 15, y0 + 190), "2. Cron Jobs & Webhooks -> MISSED!", font=FONT_WB_TITLE, fill=(194, 65, 12))
        draw.text((x0 + 15, y0 + 225), "Scheduled tasks execute nahi hote jab container idle hai!", font=FONT_WB_BODY, fill=(154, 52, 18))

        draw.rectangle([x0, y0 + 275, x0 + 580, y0 + 355], fill=(254, 242, 242), outline=(220, 38, 38), width=2)
        draw.text((x0 + 15, y0 + 285), "3. Free PostgreSQL -> Deleted in 90 Days!", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.text((x0 + 15, y0 + 320), "Render ka free database 90 din baad expire ho jata hai!", font=FONT_WB_BODY, fill=(153, 27, 27))

        draw.text((x0 + 20, y0 + 375), "Toh 24/7 Always-On Free Solution Kahan Hai?!", font=FONT_WB_TITLE, fill=(15, 23, 42))

    elif scene_id == "line4_sci":
        # Scene 4: Oracle Cloud Monster Specs
        draw.text((x0, y0), "OPTION 2: ORACLE CLOUD (IaaS)", font=FONT_WB_TITLE, fill=(185, 28, 28))
        draw.rectangle([x0, y0 + 38, x0 + 290, y0 + 68], fill=(254, 242, 242), outline=(239, 68, 68), width=2)
        draw.text((x0 + 10, y0 + 42), "[THE UNBEATABLE FREE BEAST]", font=FONT_WB_TAG, fill=(185, 28, 28))

        specs = [
            ("🔥 CPU:", "4 Ampere ARM OCPU (High Performance)"),
            ("⚡ RAM:", "24GB DDR4 Memory (Full Server Power!)"),
            ("💾 STORAGE:", "200GB NVMe SSD Block Volume Free!"),
            ("⏱️ UPTIME:", "24/7 Always ON — ZERO Spin-Down!"),
        ]

        sy = y0 + 85
        for icon_lbl, desc in specs:
            draw.rectangle([x0, sy, x0 + 580, sy + 58], fill=(240, 253, 244), outline=(34, 197, 94), width=2)
            draw.text((x0 + 15, sy + 6), icon_lbl, font=FONT_WB_TITLE, fill=(21, 128, 61))
            draw.text((x0 + 15, sy + 32), desc, font=FONT_WB_BODY, fill=(22, 101, 52))
            sy += 68

        draw.rectangle([x0, sy, x0 + 580, sy + 55], fill=(254, 249, 195), outline=(202, 138, 4), width=2)
        draw.text((x0 + 15, sy + 15), "Catch: Linux VPS Setup (SSH, Nginx, Docker)", font=FONT_WB_BODY, fill=(133, 77, 14))

    elif scene_id == "line5_sci":
        # Scene 5: Decision Matrix
        draw.text((x0, y0), "DIRECT COMPARISON: KISE CHUNEIN?", font=FONT_WB_TITLE, fill=(15, 23, 42))
        draw.rectangle([x0, y0 + 38, x0 + 280, y0 + 68], fill=(241, 245, 249), outline=(100, 116, 139), width=2)
        draw.text((x0 + 10, y0 + 42), "[CLEAR DECISION MATRIX]", font=FONT_WB_TAG, fill=(51, 65, 85))

        # Render Use-Case
        draw.rectangle([x0, y0 + 85, x0 + 580, y0 + 200], fill=(245, 243, 255), outline=(147, 51, 234), width=2)
        draw.text((x0 + 15, y0 + 95), "🟣 CHOOSE RENDER AGAR:", font=FONT_WB_TITLE, fill=(126, 34, 206))
        draw.text((x0 + 15, y0 + 130), "• Quick Portfolio / College Hackathon Demos", font=FONT_WB_BODY, fill=(88, 28, 135))
        draw.text((x0 + 15, y0 + 160), "• Sirf 1-Click mein deploy chahiye (Zero Linux)", font=FONT_WB_BODY, fill=(88, 28, 135))

        # Oracle Use-Case
        draw.rectangle([x0, y0 + 215, x0 + 580, y0 + 330], fill=(240, 253, 244), outline=(34, 197, 94), width=2)
        draw.text((x0 + 15, y0 + 225), "🔴 CHOOSE ORACLE CLOUD AGAR:", font=FONT_WB_TITLE, fill=(21, 128, 61))
        draw.text((x0 + 15, y0 + 260), "• 24/7 Always-ON Backend, Discord/Telegram Bots", font=FONT_WB_BODY, fill=(22, 101, 52))
        draw.text((x0 + 15, y0 + 290), "• Heavy PostgreSQL/Redis Database & Docker Apps", font=FONT_WB_BODY, fill=(22, 101, 52))

        # Pro Tip
        draw.rectangle([x0, y0 + 345, x0 + 580, y0 + 395], fill=(254, 249, 195), outline=(202, 138, 4), width=2)
        draw.text((x0 + 15, y0 + 358), "Pro Tip: PAYG upgrade karlo to lifetime $0 bill!", font=FONT_WB_BODY, fill=(133, 77, 14))

    elif scene_id == "line6_duo":
        # Scene 6: Outro & Call to Action
        draw.text((x0, y0), "GET CLOUD SETUP CHEATSHEET", font=FONT_WB_TITLE, fill=(15, 23, 42))
        draw.rectangle([x0, y0 + 38, x0 + 270, y0 + 68], fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((x0 + 10, y0 + 42), "[STEP-BY-STEP DEPLOY GUIDE]", font=FONT_WB_TAG, fill=(67, 56, 202))

        draw.rectangle([x0, y0 + 85, x0 + 580, y0 + 165], fill=(254, 249, 195), outline=(234, 179, 8), width=2)
        draw.text((x0 + 20, y0 + 100), "1. SAVE THIS REEL for your next project", font=FONT_WB_TITLE, fill=(133, 77, 14))
        draw.text((x0 + 20, y0 + 130), "Kyunki deploy karte waqt ye details kaam aayengi!", font=FONT_WB_BODY, fill=(161, 98, 7))

        draw.rectangle([x0, y0 + 180, x0 + 580, y0 + 265], fill=(240, 253, 244), outline=(34, 197, 94), width=2)
        draw.text((x0 + 20, y0 + 195), "2. COMMENT 'COMPARE' BELOW!", font=FONT_WB_TITLE, fill=(21, 128, 61))
        draw.text((x0 + 20, y0 + 230), "Auto-DM: Full Oracle 24GB VPS & Docker Script!", font=FONT_WB_BODY, fill=(22, 101, 52))

        draw.rectangle([x0, y0 + 285, x0 + 580, y0 + 365], fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((x0 + 20, y0 + 300), "3. Share with your Developer Friends!", font=FONT_WB_TITLE, fill=(67, 56, 202))
        draw.text((x0 + 20, y0 + 330), "Save money & avoid 50-second cold starts!", font=FONT_WB_BODY, fill=(79, 70, 229))

# --- Main Video Render Pipeline ---
FPS = 30
TOTAL_FRAMES = int(total_duration * FPS)

ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", "720x1280",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "faster",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    TEMP_VIDEO
]

print(f"--- Starting Render: {TOTAL_FRAMES} frames ({total_duration:.2f}s) ---")
pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS

    # Find active cue
    active_cue = timeline[-1]
    for c in timeline:
        if c["start"] <= t < c["end"]:
            active_cue = c
            break

    scene_id = active_cue["id"]
    rel_t = t - active_cue["start"]
    speaker = active_cue["speaking"] # 'boy' or 'sci'

    # Clone base image for this scene
    frame = base_images[scene_id].copy()
    draw = ImageDraw.Draw(frame)

    # 1. Clear whiteboard inner canvas (x=52..668, y=105..642)
    draw.rectangle([52, 105, 668, 642], fill=(255, 255, 255))

    # 2. Draw dynamic whiteboard content
    draw_whiteboard(draw, scene_id, rel_t)

    # 3. Dynamic Lip Sync & Head Bounce
    # Boy mouth: x=180..225, y=885..910 (in f12: x=180..225, y=885..910; in f1/f20: x=175..225, y=885..910)
    # Dr Billu mouth: x=500..546, y=896..923
    is_open = (int(rel_t * 6.5) % 2 == 1)
    is_blinking = (math.sin(t * 1.95) > 0.95)

    if speaker == "boy":
        # Boy is speaking
        if is_open:
            # Mouth open
            if scene_id != "line3_boy":
                # Draw red open cavity with pink tongue
                draw.rectangle([180, 888, 222, 908], fill=(142, 38, 63))
                draw.ellipse([188, 898, 214, 907], fill=(225, 95, 125))
        else:
            # Mouth closed
            draw.rectangle([178, 886, 224, 910], fill=(242, 179, 149)) # Skin fill
            draw.line([184, 897, 218, 897], fill=(80, 40, 30), width=3) # Smile line

        # Dr Billu is listening: keep mouth closed
        draw.rectangle([500, 896, 546, 923], fill=(50, 32, 39))

    else:
        # Dr Billu is speaking
        if is_open:
            # Mouth open: red cavity with pink tongue
            draw.rectangle([500, 896, 546, 923], fill=(145, 37, 63))
            draw.ellipse([508, 908, 538, 922], fill=(230, 90, 120))
        else:
            # Mouth closed: fill cavity with beard color
            draw.rectangle([500, 896, 546, 923], fill=(50, 32, 39))

        # Boy is listening: keep mouth closed
        draw.rectangle([178, 886, 224, 910], fill=(242, 179, 149))
        draw.line([184, 897, 218, 897], fill=(80, 40, 30), width=3)

    # 4. Top Progress Bar
    pct = t / total_duration
    draw.rectangle([0, 0, 720, 6], fill=(226, 232, 240))
    draw.rectangle([0, 0, int(720 * pct), 6], fill=(99, 102, 241))

    # 5. Character Speaker Tag
    tag_text = active_cue["speaker"]
    tag_bg = (239, 68, 68) if speaker == "boy" else (37, 99, 235)
    draw.rectangle([40, 1090, 245, 1118], fill=tag_bg)
    draw.text((48, 1094), tag_text, font=FONT_TAG, fill=(255, 255, 255))

    # 6. Bottom Subtitle Card
    sub_text = active_cue["sub"]
    draw.rectangle([40, 1125, 680, 1215], fill=(15, 23, 42))
    draw.rectangle([40, 1125, 680, 1215], outline=(99, 102, 241), width=2)
    # Centered subtitle
    bbox = draw.textbbox((0, 0), sub_text, font=FONT_SUB)
    sub_w = bbox[2] - bbox[0]
    sub_x = max(50, (720 - sub_w) // 2)
    draw.text((sub_x, 1152), sub_text, font=FONT_SUB, fill=(255, 255, 255))

    # Pipe frame
    pipe.stdin.write(frame.tobytes())

    # Save periodic snapshots
    if f_idx in [60, 400, 900, 1400, 1800, 2200]:
        snap_path = os.path.join(SNAPSHOT_DIR, f"snap_frame_{f_idx}.jpg")
        frame.save(snap_path)
        print(f"Saved snapshot {snap_path} at frame {f_idx}")

    if f_idx % 250 == 0:
        print(f"Rendered Frame {f_idx}/{TOTAL_FRAMES} ({f_idx*100/TOTAL_FRAMES:.1f}%)")

pipe.stdin.close()
pipe.wait()
print(f"Video Stream Rendered: {TEMP_VIDEO}")

# --- Mux Audio & Video ---
print("--- Muxing Audio & Video Master ---")
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
print(f"🎉 MASTER REEL READY: {OUTPUT_VIDEO}")
