import os
import sys
import math
import json
import subprocess
import numpy as np
import soundfile as sf
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"
AUDIO_DIR = os.path.join(BASE_DIR, "chibi_dialogue")
SFX_DIR = os.path.join(BASE_DIR, "sfx")
FRAMES_DIR = os.path.join(BASE_DIR, "ref_billu_frames")
BGM_SOURCE = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\bgm_authentic_track.wav"
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots_chibi_master")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(BASE_DIR, "chibi_oracle_master_reel.mp4")
TEMP_VIDEO_TRACK = os.path.join(BASE_DIR, "temp_chibi_video.mp4")
TEMP_AUDIO_TRACK = os.path.join(BASE_DIR, "temp_chibi_audio.wav")

with open(os.path.join(AUDIO_DIR, "dialogue_meta.json"), "r", encoding="utf-8") as f:
    dialogue_meta = json.load(f)

# 1. Timeline & RMS Envelope
def build_timeline():
    cur_t = 0.0
    schedule = {}
    audio_tracks = {}
    target_sr = 44100
    
    for item in dialogue_meta:
        tid = item["id"]
        p = item["wav"]
        data, sr = sf.read(p)
        if len(data.shape) > 1: data = data.mean(axis=1)
        dur = len(data) / sr
        
        schedule[tid] = {
            "start": cur_t,
            "end": cur_t + dur,
            "dur": dur,
            "meta": item
        }
        audio_tracks[tid] = {"data": data, "sr": sr}
        cur_t += dur + 0.12 # natural 120ms conversational gap
        
    total_dur = cur_t + 0.4
    return schedule, audio_tracks, total_dur, target_sr

schedule, audio_tracks, total_dur, target_sr = build_timeline()
print(f"Total Video Duration: {total_dur:.2f}s")

# Speech RMS Envelope
def get_speech_envelope(t, sid):
    sinfo = schedule[sid]
    if not (sinfo["start"] <= t <= sinfo["end"]):
        return 0.0
    offset_s = t - sinfo["start"]
    data = audio_tracks[sid]["data"]
    sr = audio_tracks[sid]["sr"]
    center_idx = int(offset_s * sr)
    win = int(0.040 * sr)
    start_idx = max(0, center_idx - win // 2)
    end_idx = min(len(data), center_idx + win // 2)
    if start_idx >= end_idx: return 0.0
    chunk = data[start_idx:end_idx]
    return float(np.sqrt(np.mean(chunk**2)))

# 2. Compile Audio Master
def compile_audio(total_dur, target_sr):
    total_samples = int(total_dur * target_sr)
    master = np.zeros(total_samples, dtype=np.float32)
    
    for tid, sinfo in schedule.items():
        data = audio_tracks[tid]["data"]
        sr = audio_tracks[tid]["sr"]
        if sr != target_sr:
            indices = np.round(np.arange(0, len(data), sr / target_sr)).astype(int)
            indices = indices[indices < len(data)]
            data = data[indices]
            
        start_idx = int(sinfo["start"] * target_sr)
        end_idx = min(total_samples, start_idx + len(data))
        seg_len = end_idx - start_idx
        master[start_idx:end_idx] += data[:seg_len] * 1.15
        
        # Sound Effects
        if tid == "line1_boy":
            sfx_p = os.path.join(SFX_DIR, "alarm.wav")
        elif tid in ["line2_sci", "line3_boy"]:
            sfx_p = os.path.join(SFX_DIR, "pop.wav")
        else:
            sfx_p = os.path.join(SFX_DIR, "chime.wav")
            
        if os.path.exists(sfx_p):
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
    sf.write(TEMP_AUDIO_TRACK, master, target_sr)
    print("Master Audio Ready:", TEMP_AUDIO_TRACK)

compile_audio(total_dur, target_sr)

# 3. Load Character Stage Crops (720x630 Bottom Area from ref_billu_frames)
SCENE_BOTTOMS = {
    "line1_boy": Image.open(os.path.join(FRAMES_DIR, "frame_12.0s.jpg")).crop((0, 650, 720, 1280)), # Shocked boy, sci pointing
    "line2_sci": Image.open(os.path.join(FRAMES_DIR, "frame_20.0s.jpg")).crop((0, 650, 720, 1280)), # Sci pointing board, boy listening
    "line3_boy": Image.open(os.path.join(FRAMES_DIR, "frame_10.0s.jpg")).crop((0, 650, 720, 1280)), # Boy asking, sci hands out
    "line4_sci": Image.open(os.path.join(FRAMES_DIR, "frame_30.0s.jpg")).crop((0, 650, 720, 1280)), # Sci explaining, boy listening
    "line5_boy": Image.open(os.path.join(FRAMES_DIR, "frame_3.0s.jpg")).crop((0, 650, 720, 1280)),  # Boy hands up YES!
    "line6_sci": Image.open(os.path.join(FRAMES_DIR, "frame_35.0s.jpg")).crop((0, 650, 720, 1280)), # Sci pointing CTA, boy happy
}

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_WB_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 23)
FONT_WB_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
FONT_WB_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 19)
FONT_SPEAKER_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)

# 4. Safe Text Helper
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
    
    total_h = sum([font.getbbox(l)[3] - font.getbbox(l)[1] for l in lines]) + (len(lines)-1)*line_spacing
    cur_y = by1 + max(0, (by2 - by1 - total_h) // 2)
    for l in lines:
        lh = font.getbbox(l)[3] - font.getbbox(l)[1]
        draw.text((bx1, cur_y), l, font=font, fill=fill)
        cur_y += lh + line_spacing

# 5. Draw Whiteboard
def draw_whiteboard(draw, bx, by, bw, bh):
    # Outer Metal Double Rim
    draw.rounded_rectangle([bx - 10, by - 10, bx + bw + 10, by + bh + 10], radius=18, fill=(215, 222, 230), outline=(30, 35, 45), width=3)
    # Surface
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=14, fill=(253, 254, 255), outline=(180, 185, 195), width=2)
    # Marker Tray
    tray_h = 14
    draw.rounded_rectangle([bx + 80, by + bh + 3, bx + bw - 80, by + bh + 3 + tray_h], radius=4, fill=(185, 192, 202), outline=(30, 35, 45), width=2)
    # Markers (Red, Black, Blue) & Eraser
    draw.rounded_rectangle([bx + 120, by + bh + 4, bx + 180, by + bh + 12], radius=3, fill=(225, 45, 45))
    draw.rounded_rectangle([bx + 200, by + bh + 4, bx + 260, by + bh + 12], radius=3, fill=(25, 25, 30))
    draw.rounded_rectangle([bx + 280, by + bh + 4, bx + 340, by + bh + 12], radius=3, fill=(35, 95, 225))
    draw.rounded_rectangle([bx + bw - 160, by + bh + 3, bx + bw - 100, by + bh + 13], radius=4, fill=(45, 55, 72))

# 6. Dynamic Whiteboard Content per Scene
def draw_whiteboard_content(draw, bx, by, bw, bh, active_tid, scene_rel_t):
    # Board Title
    draw.text((bx + 35, by + 25), "ORACLE CLOUD FREE TIER", font=FONT_TITLE, fill=(15, 23, 42))
    draw.line([(bx + 35, by + 68), (bx + bw - 35, by + 68)], fill=(203, 213, 225), width=2)
    
    if active_tid == "line1_boy":
        # Critical Termination Alert
        draw.rounded_rectangle([bx + 35, by + 85, bx + 280, by + 125], radius=8, fill=(254, 226, 226), outline=(239, 68, 68), width=2)
        draw.text((bx + 50, by + 94), "[CRITICAL ALERT]", font=FONT_WB_HEADER, fill=(220, 38, 38))
        
        draw.text((bx + 35, by + 145), "OCI Free Instance:", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.text((bx + 35, by + 175), "VM.Standard.A1.Flex (4 Core, 24GB)", font=FONT_WB_HEADER, fill=(15, 23, 42))
        
        draw.rounded_rectangle([bx + 35, by + 225, bx + bw - 35, by + 320], radius=12, fill=(255, 241, 242), outline=(225, 29, 72), width=2)
        draw.text((bx + 55, by + 240), "MAIL: 7 DAYS IDLE SHUTDOWN DETECTED!", font=FONT_WB_HEADER, fill=(225, 29, 72))
        draw.text((bx + 55, by + 278), "Countdown: 48 Hours To Full VM Deletion!", font=FONT_WB_BODY, fill=(159, 18, 57))
        
        draw.rounded_rectangle([bx + 35, by + 345, bx + 360, by + 395], radius=10, fill=(239, 68, 68))
        draw.text((bx + 55, by + 356), "ALL DATA WILL BE ERASED! ❌", font=FONT_WB_BODY, fill=(255, 255, 255))

    elif active_tid == "line2_sci":
        # Idle Rule Decoded with CPU Gauge
        draw.rounded_rectangle([bx + 35, by + 85, bx + 320, by + 125], radius=8, fill=(224, 242, 254), outline=(2, 132, 199), width=2)
        draw.text((bx + 50, by + 94), "[IDLE RULE DECODED]", font=FONT_WB_HEADER, fill=(2, 132, 199))
        
        draw.text((bx + 35, by + 145), "Oracle Rule: 7 Days Consecutive CPU < 20%", font=FONT_WB_BODY, fill=(15, 23, 42))
        bar_x, bar_y, bar_w, bar_h = bx + 35, by + 185, bw - 70, 42
        draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=20, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
        
        # 5% current CPU usage
        draw.rounded_rectangle([bar_x, bar_y, bar_x + int(bar_w * 0.08), bar_y + bar_h], radius=20, fill=(239, 68, 68))
        # 20% limit marker
        lim_x = bar_x + int(bar_w * 0.20)
        draw.line([(lim_x, bar_y - 8), (lim_x, bar_y + bar_h + 8)], fill=(234, 88, 12), width=3)
        draw.text((lim_x - 55, bar_y + bar_h + 10), "20% MIN LIMIT", font=FONT_WB_BODY, fill=(234, 88, 12))
        
        draw.rounded_rectangle([bx + 35, by + 285, bx + bw - 35, by + 350], radius=12, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
        draw.text((bx + 50, by + 305), "Current CPU: 5.3% -> OCI IDLE RECLAIM TRIGGERED!", font=FONT_WB_BODY, fill=(220, 38, 38))
        
        draw.rounded_rectangle([bx + 35, by + 370, bx + bw - 35, by + 430], radius=12, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
        draw.text((bx + 50, by + 388), "SOLUTION: 2 Solid Hacks To Protect It Lifetime! 👇", font=FONT_WB_HEADER, fill=(5, 150, 105))

    elif active_tid == "line3_boy":
        # Question Scene
        draw.rounded_rectangle([bx + 35, by + 85, bx + 320, by + 125], radius=8, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
        draw.text((bx + 50, by + 94), "[DEVELOPER DOUBT]", font=FONT_WB_HEADER, fill=(180, 83, 9))
        
        draw.text((bx + 35, by + 150), "Student Question:", font=FONT_WB_BODY, fill=(100, 116, 139))
        draw.text((bx + 35, by + 185), "Kaunse do tareeqe bhaiya?", font=FONT_WB_HEADER, fill=(15, 23, 42))
        draw.text((bx + 35, by + 230), "Kya koi paise lagenge? Koi subscription lena padega?", font=FONT_WB_HEADER, fill=(225, 29, 72))
        
        draw.rounded_rectangle([bx + 35, by + 300, bx + 420, by + 370], radius=12, fill=(243, 244, 246), outline=(156, 163, 175), width=2)
        draw.text((bx + 55, by + 322), "Cost Doubt: Rs. 0 or Paid?! ❓", font=FONT_WB_HEADER, fill=(31, 41, 55))

    elif active_tid == "line4_sci":
        # 2 Solutions
        draw.rounded_rectangle([bx + 35, by + 85, bx + 320, by + 125], radius=8, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
        draw.text((bx + 50, by + 94), "[2 LIFETIME FIXES]", font=FONT_WB_HEADER, fill=(5, 150, 105))
        
        # Method 1
        draw.rounded_rectangle([bx + 35, by + 145, bx + bw - 35, by + 250], radius=12, fill=(240, 253, 244), outline=(34, 197, 94), width=2)
        draw.text((bx + 50, by + 160), "METHOD 1: Upgrade to Pay-As-You-Go (PAYG)", font=FONT_WB_HEADER, fill=(21, 128, 61))
        draw.text((bx + 50, by + 200), "• Always Free Resources = Rs. 0 / Month (IMMUNE! ✅)", font=FONT_WB_BODY, fill=(15, 23, 42))
        
        # Method 2
        draw.rounded_rectangle([bx + 35, by + 270, bx + bw - 35, by + 390], radius=12, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((bx + 50, by + 285), "METHOD 2: Terminal 'lookbusy' Daemon (No Card)", font=FONT_WB_HEADER, fill=(67, 56, 202))
        draw.text((bx + 50, by + 322), "$ lookbusy -c 22 -m 128MB --quiet &", font=FONT_WB_MONO, fill=(30, 41, 59))
        draw.text((bx + 50, by + 352), "• CPU locked at 22% -> OCI Idle Check 100% Bypassed! ✅", font=FONT_WB_BODY, fill=(5, 150, 105))

    elif active_tid in ["line5_boy", "line6_sci"]:
        # Outro & Checklist
        draw.rounded_rectangle([bx + 35, by + 85, bx + 340, by + 125], radius=8, fill=(254, 249, 195), outline=(202, 138, 4), width=2)
        draw.text((bx + 50, by + 94), "[LIFETIME VM SUMMARY]", font=FONT_WB_HEADER, fill=(161, 98, 7))
        
        draw.rounded_rectangle([bx + 35, by + 145, bx + bw - 35, by + 310], radius=12, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
        draw.text((bx + 50, by + 165), "✅ 4 ARM Cores & 24GB RAM 100% Free Forever", font=FONT_WB_BODY, fill=(15, 23, 42))
        draw.text((bx + 50, by + 210), "✅ Method 1: Upgrade to PAYG ($0 Bill Forever)", font=FONT_WB_BODY, fill=(15, 23, 42))
        draw.text((bx + 50, by + 255), "✅ Method 2: lookbusy Idle Script (No Card Needed)", font=FONT_WB_BODY, fill=(15, 23, 42))
        
        draw.rounded_rectangle([bx + 35, by + 335, bx + bw - 35, by + 400], radius=10, fill=(15, 23, 42))
        draw.text((bx + 60, by + 352), "Save Reel & Comment 'ORACLE' For Setup Script! 🚀", font=FONT_WB_HEADER, fill=(250, 204, 21))

# 7. Master Frame Generator
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
    rms = get_speech_envelope(t, active_tid)
    is_speaking = (rms > 0.016)
    speaker = meta["speaker"]
    is_boy_speaking = ("Boy" in speaker)
    
    # Background Wall Color matching the scene
    wall_colors = {
        "line1_boy": (130, 194, 229), # Blue wall (frame 12s)
        "line2_sci": (152, 228, 176), # Mint Green wall (frame 20s)
        "line3_boy": (130, 194, 229), # Blue wall (frame 10s)
        "line4_sci": (152, 228, 176), # Mint Green wall (frame 30s)
        "line5_boy": (246, 201, 76),  # Warm Yellow (frame 3s)
        "line6_sci": (197, 180, 227)  # Lavender Lilac (frame 35s)
    }
    bg_color = wall_colors.get(active_tid, (130, 194, 229))
    im = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(im)
    
    # Progress Bar at Top
    progress_pct = min(1.0, t / total_dur)
    draw.rectangle([0, 0, w, 6], fill=(220, 225, 235))
    draw.rectangle([0, 0, int(w * progress_pct), 6], fill=(37, 99, 235))
    
    # Upper Whiteboard Canvas (y = 80 to 580)
    wb_x, wb_y, wb_w, wb_h = 30, 80, 660, 470
    draw_whiteboard(draw, wb_x, wb_y, wb_w, wb_h)
    draw_whiteboard_content(draw, wb_x, wb_y, wb_w, wb_h, active_tid, scene_rel_t)
    
    # Bottom Character Layer from SCENE_BOTTOMS (720x630 from ref_billu_frames)
    bottom_crop = SCENE_BOTTOMS.get(active_tid, SCENE_BOTTOMS["line1_boy"]).copy()
    
    # Subtle character breathing / speech bounce
    breath_y = int(math.sin(t * 3.5) * 3.0)
    im.paste(bottom_crop, (0, 650 + breath_y))
    
    # Subtitle Box & Speaker Badges (at bottom of screen)
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
        720: "snap_3_boy_asking_doubt.jpg",
        950: "snap_4_billu_explaining_payg.jpg",
        1350: "snap_5_boy_celebrating_yes.jpg",
        1460: "snap_6_billu_outro_cta.jpg"
    }
    if f_idx in snap_map:
        sp = os.path.join(SNAPSHOTS_DIR, snap_map[f_idx])
        im.save(sp, quality=95)
        print(f"Saved snapshot {snap_map[f_idx]} at frame {f_idx}")
        
    return im

# 8. High Performance Render Pipeline
def render_full():
    fps = 30
    total_frames = int(total_dur * fps)
    print(f"--- Rendering {total_frames} Frames @ {fps}fps ({total_dur:.2f}s) ---")
    
    cmd_video = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "720x1280",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        TEMP_VIDEO_TRACK
    ]
    
    proc = subprocess.Popen(cmd_video, stdin=subprocess.PIPE)
    for f in range(total_frames):
        frame_img = draw_frame(f, fps, schedule, total_dur)
        proc.stdin.write(frame_img.tobytes())
        if f % 250 == 0 or f == total_frames - 1:
            print(f"Rendered Frame {f}/{total_frames} ({(f/total_frames)*100:.1f}%)")
            
    proc.stdin.close()
    proc.wait()
    print("Video Rendered:", TEMP_VIDEO_TRACK)
    
    print("--- Muxing Audio & Video Master ---")
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
    print(f"\n🎉 CHIBI ORACLE MASTER REEL READY: {OUTPUT_VIDEO}\n")

if __name__ == "__main__":
    render_full()
