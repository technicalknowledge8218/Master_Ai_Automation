"""
PERFECT CHIBI MASTER REEL - EXACT MATCH TO BILLU_DEVELOPER REEL
Zero fake mouths, zero seams, 100% authentic frames with cleared whiteboard.
Resolution: 720x1280 (9:16 vertical)
Duration: ~51s @ 30fps
"""
import os
import json
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf
import imageio_ffmpeg

WORK_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"
FRAMES_DIR = os.path.join(WORK_DIR, "ref_billu_frames")
DIALOGUE_DIR = os.path.join(WORK_DIR, "chibi_dialogue")
SNAPSHOTS_DIR = os.path.join(WORK_DIR, "snapshots_perfect_master")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

TEMP_VIDEO_TRACK = os.path.join(WORK_DIR, "temp_perfect_video.mp4")
TEMP_AUDIO_TRACK = os.path.join(WORK_DIR, "temp_perfect_audio.wav")
FINAL_OUTPUT = os.path.join(WORK_DIR, "chibi_oracle_master_reel.mp4")

# 1. Load Dialogue Metadata
with open(os.path.join(DIALOGUE_DIR, "dialogue_meta.json"), "r", encoding="utf-8") as f:
    tracks_meta = json.load(f)

# Frame mapping for each dialogue scene
FRAME_MAPPING = {
    "line1_boy": "frame_25.0s.jpg", # Boy arms out in shock, sci listening
    "line2_sci": "frame_20.0s.jpg", # Sci pointing directly up at whiteboard
    "line3_boy": "frame_15.0s.jpg", # Boy asking doubt, sci listening with hands clasped
    "line4_sci": "frame_30.0s.jpg", # Sci arms wide open explaining 2 hacks
    "line5_boy": "frame_3.0s.jpg",  # Boy hands up in celebration YES!
    "line6_sci": "frame_35.0s.jpg", # Sci waving / pointing outro CTA
}

# Pre-load base frames
BASE_FRAMES = {}
for tid, fname in FRAME_MAPPING.items():
    fp = os.path.join(FRAMES_DIR, fname)
    BASE_FRAMES[tid] = Image.open(fp).convert("RGB")

# 2. Build Timeline Schedule
fps = 30
target_sr = 44100
t_cursor = 0.5 # Start with brief pause
schedule = {}

for trk in tracks_meta:
    tid = trk["id"]
    dur = trk["dur"]
    schedule[tid] = {
        "start": t_cursor,
        "end": t_cursor + dur,
        "meta": trk
    }
    t_cursor += dur + 0.35 # Natural breathing gap between turns

total_dur = t_cursor + 0.8
total_frames = int(math.ceil(total_dur * fps))
print(f"Total Video Duration: {total_dur:.2f}s ({total_frames} frames)")

# 3. Compile Master Audio
BGM_SOURCE = os.path.join(WORK_DIR, "ambient_pulse.wav")
SFX_DIR = os.path.join(WORK_DIR, "sfx")

def compile_audio(total_seconds, sr):
    total_samples = int(total_seconds * sr)
    master = np.zeros(total_samples, dtype=np.float32)
    
    for tid, sinfo in schedule.items():
        wav_p = os.path.join(DIALOGUE_DIR, f"{tid}.wav")
        data, fs = sf.read(wav_p)
        if len(data.shape) > 1: data = data.mean(axis=1)
        s_idx = int(sinfo["start"] * sr)
        e_idx = min(total_samples, s_idx + len(data))
        master[s_idx:e_idx] += data[:e_idx - s_idx]
        
    sfx_cues = [
        (0.5, os.path.join(SFX_DIR, "alarm.wav")),
        (schedule["line2_sci"]["start"], os.path.join(SFX_DIR, "pop.wav")),
        (schedule["line4_sci"]["start"], os.path.join(SFX_DIR, "whoosh.wav")),
        (schedule["line5_boy"]["start"], os.path.join(SFX_DIR, "chime.wav")),
    ]
    for cue_t, sfx_p in sfx_cues:
        if os.path.exists(sfx_p):
            start_idx = int(cue_t * sr)
            sdata, ssr = sf.read(sfx_p)
            if len(sdata.shape) > 1: sdata = sdata.mean(axis=1)
            p_end = min(total_samples, start_idx + len(sdata))
            master[start_idx:p_end] += sdata[:p_end - start_idx] * 0.35
            
    if os.path.exists(BGM_SOURCE):
        bgm_data, bsr = sf.read(BGM_SOURCE)
        if len(bgm_data.shape) > 1: bgm_data = bgm_data.mean(axis=1)
        repeats = int(np.ceil(total_samples / len(bgm_data)))
        bgm_full = np.tile(bgm_data, repeats)[:total_samples]
        master += bgm_full * 0.085
        
    max_val = np.max(np.abs(master))
    if max_val > 0.95: master = master * (0.95 / max_val)
    sf.write(TEMP_AUDIO_TRACK, master, sr)
    print("Master Audio Ready:", TEMP_AUDIO_TRACK)

compile_audio(total_dur, target_sr)

# 4. Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_WB_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
FONT_WB_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 21)
FONT_WB_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 20)
FONT_SPEAKER_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)

# Safe Text Helper
def draw_safe_wrapped_text(draw, text, font, box, fill, line_spacing=6, max_lines=2):
    bx1, by1, bx2, by2 = box
    max_w = (bx2 - bx1)
    words = text.split()
    lines = []
    cur = []
    for w in words:
        test = " ".join(cur + [w])
        if (font.getbbox(test)[2] - font.getbbox(test)[0]) <= max_w:
            cur.append(w)
        else:
            if cur: lines.append(" ".join(cur))
            cur = [w]
    if cur: lines.append(" ".join(cur))
    lines = lines[:max_lines]
    
    total_h = len(lines) * (font.getbbox("Ay")[3] - font.getbbox("Ay")[1]) + (len(lines) - 1) * line_spacing
    y_start = by1 + (by2 - by1 - total_h) // 2
    for line in lines:
        tw = font.getbbox(line)[2] - font.getbbox(line)[0]
        x_start = bx1 + (max_w - tw) // 2
        draw.text((x_start, y_start), line, font=font, fill=fill)
        y_start += (font.getbbox("Ay")[3] - font.getbbox("Ay")[1]) + line_spacing

# 5. Dynamic Whiteboard Content Renderer
def draw_whiteboard_content(draw, active_tid, rel_t):
    # Whiteboard coordinates inside frame:
    # Top-left: (52, 105), Bottom-right: (668, 642)
    # Available area: w = 616, h = 537
    x0, y0 = 55, 110
    
    # Static Whiteboard Header Pill
    draw.text((x0 + 20, y0 + 15), "ORACLE CLOUD FREE TIER", font=FONT_TITLE, fill=(15, 23, 42))
    draw.line([x0 + 20, y0 + 52, x0 + 580, y0 + 52], fill=(226, 232, 240), width=2)
    
    content_y = y0 + 68
    
    if active_tid == "line1_boy":
        # Panic / Alarm State
        draw.rounded_rectangle([x0 + 20, content_y, x0 + 270, content_y + 36], radius=6, fill=(254, 226, 226), outline=(239, 68, 68), width=2)
        draw.text((x0 + 35, content_y + 8), "[CRITICAL ALERT]", font=FONT_WB_HEADER, fill=(185, 28, 28))
        
        draw.text((x0 + 20, content_y + 52), "OCI Free Instance:", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.text((x0 + 20, content_y + 80), "VM.Standard.A1.Flex (4 Core, 24GB)", font=FONT_WB_HEADER, fill=(15, 23, 42))
        
        # Red warning notification box
        draw.rounded_rectangle([x0 + 20, content_y + 125, x0 + 580, content_y + 215], radius=12, fill=(255, 241, 242), outline=(225, 29, 72), width=2)
        draw.text((x0 + 40, content_y + 140), "MAIL: 7 DAYS IDLE SHUTDOWN DETECTED!", font=FONT_WB_HEADER, fill=(190, 18, 60))
        draw.text((x0 + 40, content_y + 175), "Countdown: 48 Hours To Full VM Deletion!", font=FONT_WB_BODY, fill=(159, 18, 57))
        
        # Flashing deletion box
        flash = (int(rel_t * 4) % 2 == 0)
        del_fill = (225, 29, 72) if flash else (159, 18, 57)
        draw.rounded_rectangle([x0 + 20, content_y + 235, x0 + 400, content_y + 285], radius=8, fill=del_fill)
        draw.text((x0 + 35, content_y + 248), "ALL DATA WILL BE ERASED!", font=FONT_WB_HEADER, fill=(255, 255, 255))
        
    elif active_tid == "line2_sci":
        # Idle Rule Decoded
        draw.rounded_rectangle([x0 + 20, content_y, x0 + 310, content_y + 36], radius=6, fill=(219, 234, 254), outline=(37, 99, 235), width=2)
        draw.text((x0 + 35, content_y + 8), "[IDLE RULE DECODED]", font=FONT_WB_HEADER, fill=(29, 78, 216))
        
        draw.text((x0 + 20, content_y + 50), "Oracle Rule: 7 Days Consecutive CPU < 20%", font=FONT_WB_BODY, fill=(15, 23, 42))
        
        # CPU Gauge Bar
        gauge_y = content_y + 88
        draw.rounded_rectangle([x0 + 20, gauge_y, x0 + 580, gauge_y + 32], radius=10, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
        # Red bar for current CPU (~5.3%)
        fill_w = min(120, int(35 + (rel_t * 15)))
        draw.rounded_rectangle([x0 + 22, gauge_y + 2, x0 + 22 + fill_w, gauge_y + 30], radius=8, fill=(239, 68, 68))
        # 20% mark line
        mark_x = x0 + 20 + int(560 * 0.20)
        draw.line([mark_x, gauge_y - 6, mark_x, gauge_y + 38], fill=(234, 88, 12), width=3)
        draw.text((mark_x - 55, gauge_y + 44), "20% MIN LIMIT", font=FONT_WB_HEADER, fill=(194, 65, 12))
        
        # Reclaim box
        draw.rounded_rectangle([x0 + 20, content_y + 180, x0 + 580, content_y + 235], radius=10, fill=(254, 242, 242), outline=(248, 113, 113), width=2)
        draw.text((x0 + 35, content_y + 195), "Current CPU: 5.3% -> OCI IDLE RECLAIM TRIGGERED!", font=FONT_WB_BODY, fill=(185, 28, 28))
        
        # Solution tease
        draw.rounded_rectangle([x0 + 20, content_y + 255, x0 + 580, content_y + 310], radius=10, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
        draw.text((x0 + 35, content_y + 270), "SOLUTION: 2 Solid Hacks To Protect It Lifetime!", font=FONT_WB_HEADER, fill=(4, 120, 87))

    elif active_tid == "line3_boy":
        # Boy Asking Doubt
        draw.rounded_rectangle([x0 + 20, content_y, x0 + 310, content_y + 36], radius=6, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
        draw.text((x0 + 35, content_y + 8), "[STUDENT DOUBT ?]", font=FONT_WB_HEADER, fill=(180, 83, 9))
        
        draw.text((x0 + 20, content_y + 55), "Rohan's Question:", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.text((x0 + 20, content_y + 85), "\"Agar PAYG upgrade kiya to bill kitna aayega?\"", font=FONT_WB_HEADER, fill=(15, 23, 42))
        
        draw.rounded_rectangle([x0 + 20, content_y + 140, x0 + 580, content_y + 240], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=2)
        draw.text((x0 + 40, content_y + 160), "Common Fear: Credit card deduction?", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.text((x0 + 40, content_y + 195), "Real Reality: $0.00 ZERO CHARGE under Free Limits!", font=FONT_WB_HEADER, fill=(16, 185, 129))
        
    elif active_tid == "line4_sci":
        # The 2 Proven Hacks
        draw.rounded_rectangle([x0 + 20, content_y, x0 + 410, content_y + 36], radius=6, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
        draw.text((x0 + 35, content_y + 8), "[2 PROVEN PERMANENT HACKS]", font=FONT_WB_HEADER, fill=(4, 120, 87))
        
        # Hack 1: PAYG
        draw.rounded_rectangle([x0 + 20, content_y + 52, x0 + 580, content_y + 128], radius=10, fill=(240, 253, 250), outline=(20, 184, 166), width=2)
        draw.text((x0 + 35, content_y + 65), "HACK 1: Upgrade to PAYG (Pay-As-You-Go)", font=FONT_WB_HEADER, fill=(13, 148, 136))
        draw.text((x0 + 35, content_y + 95), "-> Free tier resources stay $0 forever (Never Reclaimed!)", font=FONT_WB_BODY, fill=(15, 118, 110))
        
        # Hack 2: lookbusy daemon
        draw.rounded_rectangle([x0 + 20, content_y + 145, x0 + 580, content_y + 275], radius=10, fill=(248, 250, 252), outline=(59, 130, 246), width=2)
        draw.text((x0 + 35, content_y + 158), "HACK 2: Run 'lookbusy' Background Daemon", font=FONT_WB_HEADER, fill=(29, 78, 216))
        draw.text((x0 + 35, content_y + 188), "Maintains 22% CPU lock automatically:", font=FONT_WB_BODY, fill=(71, 85, 105))
        
        # Terminal command box
        draw.rounded_rectangle([x0 + 35, content_y + 218, x0 + 560, content_y + 260], radius=6, fill=(15, 23, 42))
        cmd = "curl -sL https://git.io/lookbusy | bash -s 22"
        # Typing effect
        chars = min(len(cmd), int(rel_t * 12))
        draw.text((x0 + 50, content_y + 228), cmd[:chars] + " █", font=FONT_WB_MONO, fill=(74, 222, 128))
        
    elif active_tid == "line5_boy":
        # Celebration / Relief
        draw.rounded_rectangle([x0 + 20, content_y, x0 + 340, content_y + 36], radius=6, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
        draw.text((x0 + 35, content_y + 8), "[PROBLEM 100% SOLVED]", font=FONT_WB_HEADER, fill=(180, 83, 9))
        
        draw.text((x0 + 20, content_y + 55), "Oracle Free Tier Server Status:", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.text((x0 + 20, content_y + 85), "ACTIVE & LIFETIME PROTECTED!", font=FONT_WB_HEADER, fill=(16, 185, 129))
        
        # 3 Green checkmarks
        checklist = [
            "[OK] 4 Cores + 24GB RAM Active 24/7",
            "[OK] Zero Risk of 7-Day Auto Reclaim",
            "[OK] Zero Surprise Billing ($0.00)",
        ]
        chk_y = content_y + 130
        for item in checklist:
            draw.rounded_rectangle([x0 + 20, chk_y, x0 + 580, chk_y + 44], radius=8, fill=(240, 253, 244), outline=(134, 239, 172), width=1)
            draw.text((x0 + 40, chk_y + 10), item, font=FONT_WB_HEADER, fill=(22, 101, 52))
            chk_y += 54
            
    elif active_tid == "line6_sci":
        # Outro Call to Action
        draw.rounded_rectangle([x0 + 20, content_y, x0 + 440, content_y + 36], radius=6, fill=(243, 232, 255), outline=(168, 85, 247), width=2)
        draw.text((x0 + 35, content_y + 8), "[GET FULL AUTOMATION SCRIPT]", font=FONT_WB_HEADER, fill=(126, 34, 206))
        
        draw.text((x0 + 20, content_y + 55), "Full Setup Guide & One-Line Script:", font=FONT_WB_BODY, fill=(100, 116, 139))
        
        # CTA Box
        draw.rounded_rectangle([x0 + 20, content_y + 95, x0 + 580, content_y + 240], radius=14, fill=(250, 245, 255), outline=(192, 132, 252), width=2)
        draw.text((x0 + 40, content_y + 115), "1. SAVE this Reel for future reference", font=FONT_WB_HEADER, fill=(107, 33, 168))
        draw.text((x0 + 40, content_y + 155), "2. Comment 'ORACLE' below", font=FONT_WB_HEADER, fill=(147, 51, 234))
        draw.text((x0 + 40, content_y + 195), "3. Direct Script link inbox mein mil jayega!", font=FONT_WB_BODY, fill=(88, 28, 135))
        
        # Follow badge
        draw.rounded_rectangle([x0 + 20, content_y + 260, x0 + 380, content_y + 305], radius=8, fill=(147, 51, 234))
        draw.text((x0 + 45, content_y + 272), "+ FOLLOW For Cloud Hacks", font=FONT_WB_HEADER, fill=(255, 255, 255))

# 6. Master Frame Generator
def draw_frame(f_idx, fps, schedule, total_dur):
    t = f_idx / fps
    w, h = 720, 1280
    
    active_tid = "line1_boy"
    active_sinfo = schedule["line1_boy"]
    for tid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"] + 0.12:
            active_tid = tid
            active_sinfo = sinfo
            break
            
    meta = active_sinfo["meta"]
    scene_rel_t = t - active_sinfo["start"]
    speaker = meta["speaker"]
    is_boy_speaking = ("Boy" in speaker)
    
    # 1. Base Frame (Authentic Chibi Duo + Whiteboard Frame)
    base_im = BASE_FRAMES[active_tid].copy()
    draw = ImageDraw.Draw(base_im)
    
    # 2. Clear Whiteboard Inner Canvas (x=52..668, y=105..642)
    # Preserves outer frame, rounded corners, and marker tray with markers!
    draw.rounded_rectangle([52, 105, 668, 642], radius=12, fill=(253, 253, 250))
    
    # 3. Dynamic Whiteboard Content
    draw_whiteboard_content(draw, active_tid, scene_rel_t)
    
    # 4. Progress Bar at Very Top (y=0..6)
    progress_pct = min(1.0, t / total_dur)
    draw.rectangle([0, 0, w, 6], fill=(220, 225, 235))
    draw.rectangle([0, 0, int(w * progress_pct), 6], fill=(37, 99, 235))
    
    # 5. Subtitle Box & Speaker Badges (at bottom of screen)
    sub_x1, sub_y1, sub_x2, sub_y2 = 40, h - 145, w - 40, h - 35
    draw.rounded_rectangle([sub_x1, sub_y1, sub_x2, sub_y2], radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    
    # Speaker Pill Badge
    if is_boy_speaking:
        badge_w = 200
        draw.rounded_rectangle([sub_x1, sub_y1 - 34, sub_x1 + badge_w, sub_y1 - 6], radius=8, fill=(225, 29, 72))
        draw.text((sub_x1 + 18, sub_y1 - 28), "ROHAN (Junior Dev)", font=FONT_SPEAKER_BADGE, fill=(255, 255, 255))
        text_fill = (255, 235, 245)
    else:
        badge_w = 230
        draw.rounded_rectangle([sub_x1, sub_y1 - 34, sub_x1 + badge_w, sub_y1 - 6], radius=8, fill=(37, 99, 235))
        draw.text((sub_x1 + 18, sub_y1 - 28), "DR. BILLU (Cloud Mentor)", font=FONT_SPEAKER_BADGE, fill=(255, 255, 255))
        text_fill = (225, 245, 255)
        
    draw_safe_wrapped_text(draw, meta.get("sub", ""), FONT_SUBTITLE, (sub_x1 + 25, sub_y1 + 14, sub_x2 - 25, sub_y2 - 14), fill=text_fill, line_spacing=6, max_lines=2)
    
    # Verification Snapshots
    snap_map = {
        30: "snap_1_boy_panic_hook.jpg",
        350: "snap_2_billu_pointing_rule.jpg",
        760: "snap_3_boy_asking_doubt.jpg",
        950: "snap_4_billu_explaining_payg.jpg",
        1350: "snap_5_boy_celebrating_yes.jpg",
        1460: "snap_6_billu_outro_cta.jpg"
    }
    if f_idx in snap_map:
        sp = os.path.join(SNAPSHOTS_DIR, snap_map[f_idx])
        base_im.save(sp, quality=95)
        print(f"Saved snapshot {snap_map[f_idx]} at frame {f_idx}")
        
    return base_im

# 7. Render Video with FFmpeg Pipe
print(f"--- Rendering {total_frames} Frames @ {fps}fps ({total_dur:.2f}s) ---")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", "720x1280",
    "-pix_fmt", "rgb24",
    "-r", str(fps),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "veryfast",
    "-crf", "20",
    TEMP_VIDEO_TRACK
]

pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for f in range(total_frames):
    frame_img = draw_frame(f, fps, schedule, total_dur)
    pipe.stdin.write(frame_img.tobytes())
    if f % 250 == 0:
        print(f"Rendered Frame {f}/{total_frames} ({f/total_frames*100:.1f}%)")

pipe.stdin.close()
pipe.wait()
print("Video Rendered:", TEMP_VIDEO_TRACK)

# 8. Final Mux Audio & Video
print("--- Muxing Audio & Video Master ---")
mux_cmd = [
    ffmpeg_exe,
    "-y",
    "-i", TEMP_VIDEO_TRACK,
    "-i", TEMP_AUDIO_TRACK,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    FINAL_OUTPUT
]
subprocess.run(mux_cmd, check=True)
print(f"🎉 PERFECT CHIBI MASTER REEL READY: {FINAL_OUTPUT}")
