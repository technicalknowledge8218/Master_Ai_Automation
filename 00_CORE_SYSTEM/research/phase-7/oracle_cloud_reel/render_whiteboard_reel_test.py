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
AUDIO_DIR = os.path.join(BASE_DIR, "whiteboard_test_audio")
SFX_DIR = os.path.join(BASE_DIR, "sfx")
CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
BGM_SOURCE = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\bgm_authentic_track.wav"
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots_whiteboard_test")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(BASE_DIR, "whiteboard_explainer_test_master.mp4")
TEMP_VIDEO_TRACK = os.path.join(BASE_DIR, "temp_wb_video.mp4")
TEMP_AUDIO_TRACK = os.path.join(BASE_DIR, "temp_wb_audio.wav")

with open(os.path.join(AUDIO_DIR, "whiteboard_meta.json"), "r", encoding="utf-8") as f:
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
        cur_t += dur + 0.15 # natural 150ms conversational gap
        
    total_dur = cur_t + 0.5
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
        
        # Pop SFX at start of each turn
        pop_p = os.path.join(SFX_DIR, "pop.wav")
        if os.path.exists(pop_p):
            pdata, psr = sf.read(pop_p)
            if len(pdata.shape) > 1: pdata = pdata.mean(axis=1)
            p_end = min(total_samples, start_idx + len(pdata))
            master[start_idx:p_end] += pdata[:p_end - start_idx] * 0.35
            
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

# 3. Load Character Sprites
SPRITES = {}
for name in ["neha_shocked.png", "neha_pointing.png", "neha_laptop.png", "neha_peace.png",
             "dr_kabir_warning.png", "dr_kabir_explaining.png", "dr_kabir_proud.png", "dr_kabir_tablet.png"]:
    p = os.path.join(CHAR_LIB, name)
    if os.path.exists(p):
        SPRITES[name] = Image.open(p).convert("RGBA")

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
FONT_WB_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)
FONT_WB_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 30)
FONT_WB_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 28)
FONT_SPEAKER_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)

# 4. Safe Text Helper
def draw_safe_wrapped_text(draw, text, font, box, fill, line_spacing=8, max_lines=2):
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

# 5. Draw Interactive Whiteboard Background (Reel 4 billu_developer Archetype)
def draw_whiteboard(draw, bx, by, bw, bh):
    # Outer Metal/Aluminum Frame
    draw.rounded_rectangle([bx - 12, by - 12, bx + bw + 12, by + bh + 12], radius=24, fill=(210, 215, 225, 255), outline=(160, 168, 180, 255), width=4)
    # Inner Whiteboard Gloss Surface
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=(253, 254, 255, 255), outline=(225, 230, 238, 255), width=2)
    
    # Bottom Marker Tray with Pens
    tray_h = 16
    draw.rounded_rectangle([bx + 40, by + bh + 4, bx + bw - 40, by + bh + 4 + tray_h], radius=6, fill=(180, 188, 200, 255), outline=(140, 148, 160, 255), width=2)
    # Black Marker Pen
    draw.rounded_rectangle([bx + 80, by + bh + 5, bx + 190, by + bh + 15], radius=4, fill=(25, 25, 30, 255))
    draw.rectangle([bx + 190, by + bh + 7, bx + 205, by + bh + 13], fill=(70, 70, 75, 255))
    # Blue Marker Pen
    draw.rounded_rectangle([bx + 230, by + bh + 5, bx + 340, by + bh + 15], radius=4, fill=(25, 95, 215, 255))
    draw.rectangle([bx + 340, by + bh + 7, bx + 355, by + bh + 13], fill=(60, 130, 240, 255))
    # Whiteboard Eraser
    draw.rounded_rectangle([bx + bw - 180, by + bh + 3, bx + bw - 80, by + bh + 17], radius=5, fill=(45, 55, 72, 255))

# 6. Content on Whiteboard per Scene
def draw_whiteboard_content(draw, bx, by, bw, bh, active_tid, scene_rel_t):
    # Header Banner on Whiteboard
    draw.text((bx + 50, by + 40), "ORACLE CLOUD FREE TIER", font=FONT_TITLE, fill=(15, 23, 42, 255))
    draw.line([(bx + 50, by + 105), (bx + bw - 50, by + 105)], fill=(203, 213, 225, 255), width=3)
    
    if active_tid == "turn1_neha":
        # Critical Termination Alert
        draw.rounded_rectangle([bx + 50, by + 130, bx + 360, by + 185], radius=12, fill=(254, 226, 226, 255), outline=(239, 68, 68, 255), width=2)
        draw.text((bx + 75, by + 142), "[CRITICAL ALERT]", font=FONT_WB_HEADER, fill=(220, 38, 38, 255))
        
        draw.text((bx + 50, by + 220), "OCI Free Instance:", font=FONT_WB_BODY, fill=(100, 116, 139, 255))
        draw.text((bx + 50, by + 265), "VM.Standard.A1.Flex (4 Core, 24GB)", font=FONT_WB_HEADER, fill=(15, 23, 42, 255))
        
        draw.rounded_rectangle([bx + 50, by + 340, bx + bw - 50, by + 470], radius=16, fill=(255, 241, 242, 255), outline=(225, 29, 72, 255), width=3)
        draw.text((bx + 80, by + 360), "MAIL DETECTED: 7 DAYS IDLE SHUTDOWN", font=FONT_WB_HEADER, fill=(225, 29, 72, 255))
        draw.text((bx + 80, by + 415), "Countdown: 48 Hours to Permanent Termination!", font=FONT_WB_BODY, fill=(159, 18, 57, 255))
        
        # Red Strike-through & Warning Stamp
        draw.rounded_rectangle([bx + 50, by + 510, bx + 420, by + 580], radius=12, fill=(239, 68, 68, 255))
        draw.text((bx + 70, by + 525), "ALL DATA WILL BE ERASED!", font=FONT_WB_BODY, fill=(255, 255, 255, 255))

    elif active_tid == "turn2_kabir":
        # Oracle Rule Decoded
        draw.rounded_rectangle([bx + 50, by + 130, bx + 420, by + 185], radius=12, fill=(224, 242, 254, 255), outline=(2, 132, 199, 255), width=2)
        draw.text((bx + 75, by + 142), "[IDLE RULE DECODED]", font=FONT_WB_HEADER, fill=(2, 132, 199, 255))
        
        # CPU Threshold Bar on Whiteboard
        draw.text((bx + 50, by + 215), "Oracle Rule: 7 Days Consecutive CPU < 20%", font=FONT_WB_BODY, fill=(15, 23, 42, 255))
        bar_x, bar_y, bar_w, bar_h = bx + 50, by + 270, bw - 100, 50
        draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=25, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=2)
        
        # 5% current CPU usage
        draw.rounded_rectangle([bar_x, bar_y, bar_x + int(bar_w * 0.08), bar_y + bar_h], radius=25, fill=(239, 68, 68, 255))
        # 20% limit marker line
        lim_x = bar_x + int(bar_w * 0.20)
        draw.line([(lim_x, bar_y - 10), (lim_x, bar_y + bar_h + 10)], fill=(234, 88, 12, 255), width=4)
        draw.text((lim_x - 70, bar_y + bar_h + 15), "20% MIN LIMIT", font=FONT_WB_BODY, fill=(234, 88, 12, 255))
        
        draw.rounded_rectangle([bx + 50, by + 400, bx + bw - 50, by + 490], radius=14, fill=(254, 242, 242, 255), outline=(239, 68, 68, 255), width=2)
        draw.text((bx + 75, by + 425), "Current CPU: 5.3% -> OCI IDLE RECLAIM TRIGGERED!", font=FONT_WB_BODY, fill=(220, 38, 38, 255))
        
        draw.rounded_rectangle([bx + 50, by + 520, bx + bw - 50, by + 600], radius=14, fill=(236, 253, 245, 255), outline=(16, 185, 129, 255), width=3)
        draw.text((bx + 75, by + 545), "SOLUTION: 2 Solid Hacks To Protect It Forever! 👇", font=FONT_WB_HEADER, fill=(5, 150, 105, 255))

    elif active_tid == "turn3_neha":
        # Question / Doubt Scene
        draw.rounded_rectangle([bx + 50, by + 130, bx + 420, by + 185], radius=12, fill=(254, 243, 199, 255), outline=(217, 119, 6, 255), width=2)
        draw.text((bx + 75, by + 142), "[DEVELOPER DOUBT]", font=FONT_WB_HEADER, fill=(180, 83, 9, 255))
        
        draw.text((bx + 50, by + 230), "Student Question:", font=FONT_WB_BODY, fill=(100, 116, 139, 255))
        draw.text((bx + 50, by + 280), "Kaunse do tareeqe bhaiya?", font=FONT_WB_HEADER, fill=(15, 23, 42, 255))
        draw.text((bx + 50, by + 340), "Kya koi paise lagenge? Koi subscription lena padega?", font=FONT_WB_HEADER, fill=(225, 29, 72, 255))
        
        draw.rounded_rectangle([bx + 50, by + 430, bx + 550, by + 520], radius=14, fill=(243, 244, 246, 255), outline=(156, 163, 175, 255), width=2)
        draw.text((bx + 80, by + 455), "Cost Doubt: Rs. 0 or Paid?! ❓", font=FONT_WB_HEADER, fill=(31, 41, 55, 255))

    elif active_tid == "turn4_kabir":
        # 2 Solutions on Whiteboard
        draw.rounded_rectangle([bx + 50, by + 130, bx + 440, by + 185], radius=12, fill=(236, 253, 245, 255), outline=(16, 185, 129, 255), width=2)
        draw.text((bx + 75, by + 142), "[2 LIFETIME FIXES]", font=FONT_WB_HEADER, fill=(5, 150, 105, 255))
        
        # Method 1
        draw.rounded_rectangle([bx + 50, by + 210, bx + bw - 50, by + 340], radius=14, fill=(240, 253, 244, 255), outline=(34, 197, 94, 255), width=3)
        draw.text((bx + 75, by + 230), "METHOD 1: Upgrade to Pay-As-You-Go (PAYG)", font=FONT_WB_HEADER, fill=(21, 128, 61, 255))
        draw.text((bx + 75, by + 280), "• Always Free Resources = Rs. 0 / Month (NEVER DELETED!)", font=FONT_WB_BODY, fill=(15, 23, 42, 255))
        
        # Method 2
        draw.rounded_rectangle([bx + 50, by + 370, bx + bw - 50, by + 510], radius=14, fill=(238, 242, 255, 255), outline=(99, 102, 241, 255), width=3)
        draw.text((bx + 75, by + 390), "METHOD 2: Terminal 'lookbusy' Daemon (No Card)", font=FONT_WB_HEADER, fill=(67, 56, 202, 255))
        draw.text((bx + 75, by + 440), "$ lookbusy -c 22 -m 128MB --quiet &", font=FONT_WB_MONO, fill=(30, 41, 59, 255))
        draw.text((bx + 75, by + 475), "• CPU locked at 22% -> OCI Idle Check 100% Bypassed!", font=FONT_WB_BODY, fill=(5, 150, 105, 255))
        
        # CTA Banner
        draw.rounded_rectangle([bx + 50, by + 535, bx + bw - 50, by + 610], radius=12, fill=(15, 23, 42, 255))
        draw.text((bx + 110, by + 555), "Save Reel & Comment 'ORACLE' For Setup Script!", font=FONT_WB_HEADER, fill=(250, 204, 21, 255))

# 7. Master Frame Generator with Turn-Taking Staging
def draw_frame(f_idx, fps, schedule, total_dur):
    t = f_idx / fps
    w, h = 1080, 1920
    
    # Active Turn Lookup
    active_tid = "turn1_neha"
    active_sinfo = schedule["turn1_neha"]
    for tid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"] + 0.15:
            active_tid = tid
            active_sinfo = sinfo
            break
            
    meta = active_sinfo["meta"]
    scene_rel_t = t - active_sinfo["start"]
    rms = get_speech_envelope(t, active_tid)
    is_speaking = (rms > 0.016)
    speaker = meta["speaker"] # "Neha (Junior)" or "Dr. Kabir (Senior)"
    
    # Background Wall Color Shifts (Reel 4 subtle subconscious color shift)
    wall_colors = {
        "turn1_neha": (248, 244, 236, 255),   # Warm Cream Ochre
        "turn2_kabir": (236, 245, 240, 255),  # Sage Soft Mint
        "turn3_neha": (245, 240, 250, 255),   # Soft Lavender
        "turn4_kabir": (235, 243, 250, 255)   # Soft Sky Slate
    }
    bg_color = wall_colors.get(active_tid, (245, 245, 245, 255))
    im = Image.new("RGBA", (w, h), bg_color)
    draw = ImageDraw.Draw(im)
    
    # Progress Bar at Top
    progress_pct = min(1.0, t / total_dur)
    draw.rectangle([0, 0, w, 8], fill=(220, 225, 235, 255))
    draw.rectangle([0, 0, int(w * progress_pct), 8], fill=(37, 99, 235, 255))
    
    # Whiteboard Position (Central Upper Stage)
    wb_x, wb_y, wb_w, wb_h = 70, 100, 940, 680
    draw_whiteboard(draw, wb_x, wb_y, wb_w, wb_h)
    draw_whiteboard_content(draw, wb_x, wb_y, wb_w, wb_h, active_tid, scene_rel_t)
    
    # Secondary Character Motion
    breath = math.sin(t * 3.2) * 4.0
    sway = math.sin(t * 1.8) * 3.0
    bob = math.sin(t * 12.0) * 3.5 if is_speaking else 0.0
    
    # --- TURN-TAKING CHARACTER STAGING (Both characters on screen in front of whiteboard) ---
    
    # LEFT CHARACTER: NEHA (Junior)
    neha_is_speaker = ("Neha" in speaker)
    if neha_is_speaker:
        if active_tid == "turn1_neha":
            neha_key = "neha_shocked.png" if is_speaking else "neha_pointing.png"
        else: # turn3_neha
            neha_key = "neha_pointing.png" if is_speaking else "neha_peace.png"
    else:
        # Listening mode: Neha stands attentive looking up toward board / Kabir
        neha_key = "neha_peace.png"
        
    neha_img = SPRITES.get(neha_key, SPRITES.get("neha_pointing.png"))
    if neha_img:
        ch_w, ch_h = neha_img.size
        target_h = 820
        target_w = int(ch_w * (target_h / ch_h))
        n_res = neha_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        # Position Neha on left side of stage
        nx = int(20 + sway)
        ny = int(h - target_h + 35 + breath + (bob if neha_is_speaker else 0.0))
        im.paste(n_res, (nx, ny), n_res)
        
    # RIGHT CHARACTER: DR. KABIR (Senior)
    kabir_is_speaker = ("Kabir" in speaker)
    if kabir_is_speaker:
        # When speaking, Kabir uses explaining sprite (pointing to board with open mouth on audio peaks)
        kabir_key = "dr_kabir_explaining.png" if is_speaking else "dr_kabir_warning.png"
    else:
        # Listening mode: Kabir stands attentive with hands folded/resting, mouth closed!
        kabir_key = "dr_kabir_warning.png"
        
    kabir_img = SPRITES.get(kabir_key, SPRITES.get("dr_kabir_warning.png"))
    if kabir_img:
        ch_w, ch_h = kabir_img.size
        target_h = 840
        target_w = int(ch_w * (target_h / ch_h))
        k_res = kabir_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        # Position Kabir on right side of stage pointing toward the whiteboard
        kx = int(w - target_w + 30 - sway)
        ky = int(h - target_h + 35 + breath + (bob if kabir_is_speaker else 0.0))
        im.paste(k_res, (kx, ky), k_res)
        
    # --- SUBTITLES & SPEAKER BADGES (Zero Overlap with Characters) ---
    sub_x1, sub_y1, sub_x2, sub_y2 = 60, h - 235, w - 60, h - 75
    draw.rounded_rectangle([sub_x1, sub_y1, sub_x2, sub_y2], radius=18, fill=(15, 23, 42, 245), outline=(51, 65, 85, 255), width=3)
    
    # Speaker Pill Badge
    if neha_is_speaker:
        badge_w = 260
        draw.rounded_rectangle([sub_x1, sub_y1 - 46, sub_x1 + badge_w, sub_y1 - 8], radius=10, fill=(236, 72, 153, 255))
        draw.text((sub_x1 + 22, sub_y1 - 38), "NEHA (Junior Dev)", font=FONT_SPEAKER_BADGE, fill=(255, 255, 255, 255))
        text_fill = (255, 235, 245, 255)
    else:
        badge_w = 340
        draw.rounded_rectangle([sub_x1, sub_y1 - 46, sub_x1 + badge_w, sub_y1 - 8], radius=10, fill=(37, 99, 235, 255))
        draw.text((sub_x1 + 22, sub_y1 - 38), "DR. KABIR (Senior Architect)", font=FONT_SPEAKER_BADGE, fill=(255, 255, 255, 255))
        text_fill = (225, 245, 255, 255)
        
    # Safe Subtitle Text Rendering
    draw_safe_wrapped_text(draw, meta.get("sub", ""), FONT_SUBTITLE, (sub_x1 + 30, sub_y1 + 18, sub_x2 - 30, sub_y2 - 18), fill=text_fill, line_spacing=8, max_lines=2)
    
    # Verification Snapshots
    snap_map = {
        30: "snap_1_neha_whiteboard_hook.jpg",
        320: "snap_2_kabir_explaining_board.jpg",
        640: "snap_3_neha_asking_doubt.jpg",
        850: "snap_4_kabir_payg_solution.jpg"
    }
    if f_idx in snap_map:
        sp = os.path.join(SNAPSHOTS_DIR, snap_map[f_idx])
        im.convert("RGB").save(sp, quality=95)
        print(f"Saved snapshot {snap_map[f_idx]} at frame {f_idx}")
        
    return im.convert("RGB")

# 8. High Performance Render Pipeline
def render_full():
    fps = 30
    total_frames = int(total_dur * fps)
    print(f"--- Rendering {total_frames} Frames @ {fps}fps ({total_dur:.2f}s) ---")
    
    cmd_video = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
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
    print(f"\n🎉 WHITEBOARD EXPLAINER TEST MASTER READY: {OUTPUT_VIDEO}\n")

if __name__ == "__main__":
    render_full()
