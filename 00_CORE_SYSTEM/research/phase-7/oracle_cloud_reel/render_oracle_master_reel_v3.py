import os
import sys
import math
import subprocess
import numpy as np
import soundfile as sf
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"
AUDIO_DIR = BASE_DIR
SFX_DIR = os.path.join(BASE_DIR, "sfx")
CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
BGM_SOURCE = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\bgm_authentic_track.wav"
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots_v3")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(BASE_DIR, "oracle_cloud_master_reel_v3.mp4")
TEMP_VIDEO_TRACK = os.path.join(BASE_DIR, "temp_video_v3.mp4")
TEMP_AUDIO_TRACK = os.path.join(BASE_DIR, "temp_audio_v3.wav")

# High-Energy Fluid Audio Tracks (Zero Stutter)
SCENES = [
    {
        "id": "scene1_hook",
        "audio_file": "fluid_scene1_hook.wav",
        "bg_color": (15, 23, 42, 255),      # Slate 900
        "tag": "CRITICAL WARNING",
        "card_type": "WARNING",
        "char": "arjun_shocked.png",
        "char_side": "right",
        "bubble_title": "⚠️ CRITICAL WARNING:",
        "bubble_text": "Don't let your free VM die!",
        "subtitle": "Oracle Cloud Free Server 7 Din Mein DELETE Ho Jayega?!",
        "sfx": "alarm.wav"
    },
    {
        "id": "scene2_problem",
        "audio_file": "fluid_scene2_problem.wav",
        "bg_color": (38, 16, 24, 255),      # Dark Crimson
        "tag": "IDLE RECLAMATION POLICY",
        "card_type": "GAUGE",
        "char": "dr_kabir_warning.png",
        "char_side": "left",
        "bubble_title": "📊 OCI THRESHOLD:",
        "bubble_text": "CPU < 20% = INSTANCE TERMINATED!",
        "subtitle": "Oracle Rule: CPU < 20% = Server Terminated & Data Lost!",
        "sfx": "pop.wav"
    },
    {
        "id": "scene3_fix1_payg",
        "audio_file": "fluid_scene3_fix1_payg.wav",
        "bg_color": (10, 35, 26, 255),      # Deep Emerald
        "tag": "100% PERMANENT FIX",
        "card_type": "PAYG",
        "char": "arjun_pointing.png",
        "char_side": "right",
        "bubble_title": "💡 OFFICIAL FIX:",
        "bubble_text": "Upgrade to PAYG (Rs. 0 Bill Forever)",
        "subtitle": "Method 1: Upgrade to PAYG ($0 Bill Forever & Lifetime Safe)",
        "sfx": "chime.wav"
    },
    {
        "id": "scene4_fix2_script",
        "audio_file": "fluid_scene4_fix2_script.wav",
        "bg_color": (16, 24, 40, 255),      # Tech Slate
        "tag": "CLI AUTOMATION FIX",
        "card_type": "TERMINAL_ANIMATED",
        "char": "dr_kabir_tablet.png",
        "char_side": "left",
        "bubble_title": "⚡ AUTOMATION FIX:",
        "bubble_text": "Run 'lookbusy' daemon (Keep CPU at 22%)",
        "subtitle": "Method 2: Run 'lookbusy' Tool (Keep CPU at 22%)",
        "sfx": "pop.wav"
    },
    {
        "id": "scene5_cta",
        "audio_file": "fluid_scene5_cta.wav",
        "bg_color": (28, 20, 50, 255),      # Modern Indigo
        "tag": "SAVE & SHARE REEL",
        "card_type": "CTA",
        "char": "arjun_thumbsup.png",
        "char_side": "right",
        "bubble_title": "📩 GET COMMANDS:",
        "bubble_text": "Comment 'ORACLE' for 1-click script!",
        "subtitle": "Save Reel & Comment 'ORACLE' for Full Setup Commands!",
        "sfx": "chime.wav"
    }
]

# 1. Timeline Build
def build_timeline():
    cur_t = 0.0
    schedule = {}
    audio_data = {}
    target_sr = 44100
    
    for s in SCENES:
        p = os.path.join(AUDIO_DIR, s["audio_file"])
        data, sr = sf.read(p)
        if len(data.shape) > 1: data = data.mean(axis=1)
        dur = len(data) / sr
        
        schedule[s["id"]] = {
            "start": cur_t,
            "end": cur_t + dur,
            "dur": dur,
            "config": s
        }
        audio_data[s["id"]] = {"data": data, "sr": sr}
        cur_t += dur + 0.12 # tight 0.12s gap
        
    total_dur = cur_t + 0.4
    return schedule, audio_data, total_dur, target_sr

schedule, audio_data, total_dur, target_sr = build_timeline()
print(f"Total Video Planned Duration: {total_dur:.2f}s")

# 2. Multi-Track Audio Master (Voice + Typing SFX + BGM + Cues)
def compile_audio(total_dur, target_sr):
    total_samples = int(total_dur * target_sr)
    master = np.zeros(total_samples, dtype=np.float32)
    
    for sid, sinfo in schedule.items():
        data = audio_data[sid]["data"]
        sr = audio_data[sid]["sr"]
        if sr != target_sr:
            indices = np.round(np.arange(0, len(data), sr / target_sr)).astype(int)
            indices = indices[indices < len(data)]
            data = data[indices]
            
        start_idx = int(sinfo["start"] * target_sr)
        end_idx = min(total_samples, start_idx + len(data))
        seg_len = end_idx - start_idx
        master[start_idx:end_idx] += data[:seg_len] * 1.15
        
        # Primary SFX
        sfx_name = sinfo["config"]["sfx"]
        sfx_path = os.path.join(SFX_DIR, sfx_name)
        if os.path.exists(sfx_path):
            sdata, ssr = sf.read(sfx_path)
            if len(sdata.shape) > 1: sdata = sdata.mean(axis=1)
            s_end = min(total_samples, start_idx + len(sdata))
            master[start_idx:s_end] += sdata[:s_end - start_idx] * 0.45
            
        # Specific Typing SFX for Scene 4
        if sid == "scene4_fix2_script":
            typing_p = os.path.join(SFX_DIR, "typing.wav")
            if os.path.exists(typing_p):
                tdata, tsr = sf.read(typing_p)
                if len(tdata.shape) > 1: tdata = tdata.mean(axis=1)
                t_start = start_idx + int(0.8 * target_sr)
                t_end = min(total_samples, t_start + len(tdata))
                master[t_start:t_end] += tdata[:t_end - t_start] * 0.35
                
    # Background Music
    if os.path.exists(BGM_SOURCE):
        bgm_data, bsr = sf.read(BGM_SOURCE)
        if len(bgm_data.shape) > 1: bgm_data = bgm_data.mean(axis=1)
        repeats = int(np.ceil(total_samples / len(bgm_data)))
        bgm_full = np.tile(bgm_data, repeats)[:total_samples]
        master += bgm_full * 0.10 # clean ducked groove
        
    max_val = np.max(np.abs(master))
    if max_val > 0.95:
        master = master * (0.95 / max_val)
        
    sf.write(TEMP_AUDIO_TRACK, master, target_sr)
    print("Master Audio Compiled:", TEMP_AUDIO_TRACK)

compile_audio(total_dur, target_sr)

# 3. Load Characters from CHARACTER_LIBRARY
CHARACTERS = {}
for name in ["arjun_shocked.png", "arjun_pointing.png", "arjun_thumbsup.png", "dr_kabir_warning.png", "dr_kabir_tablet.png"]:
    p = os.path.join(CHAR_LIB, name)
    if os.path.exists(p):
        CHARACTERS[name] = Image.open(p).convert("RGBA")

# Fonts (Standard Windows clean typography)
FONT_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
FONT_CARD_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
FONT_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 26)
FONT_MONO_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 28)
FONT_BUBBLE_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
FONT_BUBBLE_TEXT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)

# 4. Helper: Dynamic Wrapped Text with Zero Overflow
def draw_safe_wrapped_text(draw, text, font, box, fill, line_spacing=8, max_lines=4):
    bx1, by1, bx2, by2 = box
    max_w = (bx2 - bx1)
    words = text.split()
    lines = []
    cur_line = []
    
    for word in words:
        test_line = " ".join(cur_line + [word])
        # Measure
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_w:
            cur_line.append(word)
        else:
            if cur_line:
                lines.append(" ".join(cur_line))
            cur_line = [word]
    if cur_line:
        lines.append(" ".join(cur_line))
        
    lines = lines[:max_lines]
    # Draw lines vertically centered in box
    total_h = sum([font.getbbox(l)[3] - font.getbbox(l)[1] for l in lines]) + (len(lines)-1)*line_spacing
    cur_y = by1 + max(0, (by2 - by1 - total_h) // 2)
    
    for line in lines:
        l_bbox = font.getbbox(line)
        lw = l_bbox[2] - l_bbox[0]
        lh = l_bbox[3] - l_bbox[1]
        draw.text((bx1, cur_y), line, font=font, fill=fill)
        cur_y += lh + line_spacing

# 5. Dynamic Procedural Cards (Ensuring Zero Overflow & Animated Terminal)
def draw_warning_card(draw, cx, cy, cw=940, ch=520):
    # Outer container
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(239, 68, 68, 255), width=4)
    # Header bar
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=24, fill=(55, 20, 25, 255))
    draw.text((cx + 40, cy + 24), "⚠️  ORACLE CLOUD COMPUTE ALERT", font=FONT_CARD_TITLE, fill=(239, 68, 68, 255))
    
    # Details
    draw.text((cx + 40, cy + 115), "Instance: instance-2026-arm-free", font=FONT_CARD_BOLD, fill=(255, 255, 255, 255))
    draw.text((cx + 40, cy + 155), "Shape: 4 OCPU, 24 GB RAM (Always Free)", font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
    
    # Inner Warning Alert
    ax1, ay1, ax2, ay2 = cx + 40, cy + 210, cx + cw - 40, cy + 360
    draw.rounded_rectangle([ax1, ay1, ax2, ay2], radius=16, fill=(45, 18, 22, 255), outline=(239, 68, 68, 255), width=2)
    draw.text((ax1 + 25, ay1 + 20), "IDLE RECLAMATION TRIGGERED!", font=FONT_CARD_TITLE, fill=(239, 68, 68, 255))
    draw.text((ax1 + 25, ay1 + 68), "Condition: 7 Consecutive Days CPU < 20%", font=FONT_CARD_BODY, fill=(255, 255, 255, 255))
    draw.text((ax1 + 25, ay1 + 105), "Action: VM will be STOPPED / DELETED!", font=FONT_CARD_BOLD, fill=(245, 158, 11, 255))
    
    # Bottom Note
    draw.rounded_rectangle([cx + 40, cy + 390, cx + cw - 40, cy + 475], radius=14, fill=(20, 30, 45, 255))
    draw.text((cx + 60, cy + 418), "Risk: Permanent Boot Volume Deletion", font=FONT_CARD_BOLD, fill=(255, 255, 255, 255))

def draw_gauge_card(draw, cx, cy, cw=940, ch=460, t_rel=0.0):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(51, 65, 85, 255), width=3)
    draw.text((cx + 40, cy + 30), "📊 OCI METRIC: 7-DAY CPU UTILIZATION", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255))
    
    # Animated CPU Bar
    bar_x, bar_y, bar_w, bar_h = cx + 40, cy + 120, cw - 80, 60
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=30, fill=(45, 55, 72, 255))
    
    # 20% limit line
    t_x = bar_x + int(bar_w * 0.20)
    
    # Oscillate in danger zone 6% to 12%
    cpu_val = 8.0 + 3.0 * math.sin(t_rel * 4.0)
    fill_w = int(bar_w * (cpu_val / 100.0))
    draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=30, fill=(239, 68, 68, 255))
    
    draw.line([(t_x, bar_y - 12), (t_x, bar_y + bar_h + 12)], fill=(245, 158, 11, 255), width=4)
    draw.text((t_x - 70, bar_y + bar_h + 20), "20% MIN LIMIT", font=FONT_TAG, fill=(245, 158, 11, 255))
    
    # Text Metrics
    draw.text((cx + 40, cy + 250), f"Current Usage: {cpu_val:.1f}%", font=FONT_HEADER, fill=(239, 68, 68, 255))
    draw.text((cx + 40, cy + 325), "Status: CRITICAL DANGER (IDLE DETECTED)", font=FONT_CARD_TITLE, fill=(239, 68, 68, 255))
    draw.text((cx + 40, cy + 380), "Oracle Policy: Must stay ABOVE 20% to prevent termination", font=FONT_CARD_BODY, fill=(148, 163, 184, 255))

def draw_payg_card(draw, cx, cy, cw=940, ch=540):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(16, 185, 129, 255), width=4)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=24, fill=(16, 50, 35, 255))
    draw.text((cx + 40, cy + 24), "✅ METHOD 1: UPGRADE TO PAY-AS-YOU-GO", font=FONT_CARD_TITLE, fill=(16, 185, 129, 255))
    
    benefits = [
        ("💰 Cost For Always Free:", "Rs. 0 / Month ($0.00 Forever)"),
        ("⚡ Idle Instance Reclaim:", "100% IMMUNE (Never Terminated)"),
        ("🛡️ Account Tier:", "Paid Tier (Enterprise Priority)"),
        ("🚀 4 ARM Cores + 24GB RAM:", "Keeps Running Lifetime 24/7!")
    ]
    
    y = cy + 115
    for label, val in benefits:
        draw.rounded_rectangle([cx + 35, y, cx + cw - 35, y + 80], radius=14, fill=(20, 30, 45, 255), outline=(40, 60, 85, 255), width=2)
        draw.text((cx + 55, y + 14), label, font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
        draw.text((cx + 55, y + 42), val, font=FONT_CARD_BOLD, fill=(16, 185, 129, 255) if "0" in val or "IMMUNE" in val else (255, 255, 255, 255))
        y += 98

def draw_animated_terminal(draw, cx, cy, cw=940, ch=560, t_rel=0.0):
    # Terminal Window Body
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill=(13, 17, 23, 255), outline=(48, 54, 61, 255), width=3)
    
    # Title Bar
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 55], radius=20, fill=(22, 27, 34, 255))
    draw.ellipse([cx + 25, cy + 18, cx + 43, cy + 36], fill=(255, 95, 86, 255))
    draw.ellipse([cx + 55, cy + 18, cx + 73, cy + 36], fill=(255, 189, 46, 255))
    draw.ellipse([cx + 85, cy + 18, cx + 103, cy + 36], fill=(39, 201, 63, 255))
    draw.text((cx + 300, cy + 16), "bash — ubuntu@oci-arm-vps:~ (ssh)", font=FONT_TAG, fill=(139, 148, 158, 255))
    
    # Cursor blink
    cursor = "█" if int(t_rel * 3.0) % 2 == 0 else ""
    
    # Command 1 Typing Animation (from t=0.8s to t=3.2s)
    cmd1_full = "sudo apt update && sudo apt install -y lookbusy"
    cmd1_progress = min(1.0, max(0.0, (t_rel - 0.8) / 2.4))
    cmd1_typed = cmd1_full[:int(len(cmd1_full) * cmd1_progress)]
    
    y = cy + 80
    draw.text((cx + 35, y), "ubuntu@oci-vps:~$ ", font=FONT_MONO_BOLD, fill=(126, 231, 135, 255))
    prompt_w = FONT_MONO_BOLD.getbbox("ubuntu@oci-vps:~$ ")[2]
    c1_disp = cmd1_typed + (cursor if t_rel < 3.4 else "")
    draw.text((cx + 35 + prompt_w, y), c1_disp, font=FONT_MONO, fill=(255, 255, 255, 255))
    
    # Output 1 (at t > 3.4s)
    if t_rel >= 3.4:
        y += 48
        draw.text((cx + 35, y), "[OK] Reading package lists... Done", font=FONT_MONO, fill=(139, 148, 158, 255))
        y += 40
        draw.text((cx + 35, y), "[OK] Setting up lookbusy (1.4-1) ... Done", font=FONT_MONO, fill=(126, 231, 135, 255))
        
    # Command 2 Typing Animation (from t=4.8s to t=7.2s)
    if t_rel >= 4.6:
        y += 55
        cmd2_full = "lookbusy -c 22 -m 128MB --quiet &"
        cmd2_progress = min(1.0, max(0.0, (t_rel - 4.8) / 2.4))
        cmd2_typed = cmd2_full[:int(len(cmd2_full) * cmd2_progress)]
        draw.text((cx + 35, y), "ubuntu@oci-vps:~$ ", font=FONT_MONO_BOLD, fill=(126, 231, 135, 255))
        c2_disp = cmd2_typed + (cursor if t_rel < 7.4 else "")
        draw.text((cx + 35 + prompt_w, y), c2_disp, font=FONT_MONO, fill=(250, 204, 21, 255))
        
    # Final Success Output (at t > 7.4s)
    if t_rel >= 7.4:
        y += 55
        draw.rounded_rectangle([cx + 35, y, cx + cw - 35, y + 80], radius=10, fill=(16, 45, 30, 255), outline=(46, 160, 67, 255), width=2)
        draw.text((cx + 50, y + 16), "[✓] Worker Active: CPU Locked At 22%", font=FONT_MONO_BOLD, fill=(126, 231, 135, 255))
        draw.text((cx + 50, y + 46), "[✓] OCI Idle Status: 100% PROTECTED", font=FONT_MONO_BOLD, fill=(56, 189, 248, 255))

def draw_cta_card(draw, cx, cy, cw=940, ch=520):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(6, 182, 212, 255), width=4)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=24, fill=(15, 35, 55, 255))
    draw.text((cx + 40, cy + 24), "🚀 LIFETIME FREE VM CHECKLIST", font=FONT_CARD_TITLE, fill=(6, 182, 212, 255))
    
    items = [
        ("✅ 4 ARM Cores & 24GB RAM:", "100% Free Forever"),
        ("✅ Method 1 (Official):", "Upgrade to PAYG ($0 Bill)"),
        ("✅ Method 2 (No Card):", "Run 'lookbusy' Idle Script"),
        ("📩 Setup Commands:", "Comment 'ORACLE' Below!")
    ]
    
    y = cy + 115
    for label, val in items:
        draw.rounded_rectangle([cx + 35, y, cx + cw - 35, y + 78], radius=14, fill=(20, 30, 45, 255))
        draw.text((cx + 55, y + 22), label, font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
        draw.text((cx + 450, y + 22), val, font=FONT_CARD_BOLD, fill=(245, 158, 11, 255) if "ORACLE" in val else (255, 255, 255, 255))
        y += 92

# 6. Master Frame Drawing with Character Momentum
def draw_frame(f_idx, fps, schedule, total_dur):
    t = f_idx / fps
    w, h = 1080, 1920
    
    # Active Scene
    active_sid = "scene1_hook"
    active_sinfo = schedule["scene1_hook"]
    for sid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"] + 0.12:
            active_sid = sid
            active_sinfo = sinfo
            break
            
    cfg = active_sinfo["config"]
    scene_rel_t = t - active_sinfo["start"]
    
    im = Image.new("RGBA", (w, h), cfg["bg_color"])
    draw = ImageDraw.Draw(im)
    
    # A. Top Progress Bar
    progress_pct = min(1.0, t / total_dur)
    draw.rectangle([0, 0, w, 8], fill=(30, 41, 59, 255))
    draw.rectangle([0, 0, int(w * progress_pct), 8], fill=(6, 182, 212, 255))
    
    # B. Header Tag Banner
    draw.rounded_rectangle([60, 80, w - 60, 160], radius=16, fill=(15, 23, 42, 235), outline=(51, 65, 85, 255), width=2)
    draw.text((90, 103), f"🔥 TECH LIFE HACK  |  {cfg['tag']}", font=FONT_TAG, fill=(6, 182, 212, 255))
    
    # C. Main Category Title
    draw.text((60, 195), "ORACLE CLOUD FREE TIER", font=FONT_HEADER, fill=(255, 255, 255, 255))
    
    # D. Card with Spring Slide-in
    cw = 940
    cx = (w - cw) // 2
    target_cy = 295
    slide_progress = min(1.0, scene_rel_t / 0.35)
    # ease_out_back overshoot
    c1 = 1.70158
    c3 = c1 + 1
    p = slide_progress - 1.0
    ease = 1.0 + c3 * (p**3) + c1 * (p**2) if slide_progress < 1.0 else 1.0
    cur_cy = int(target_cy - (1.0 - ease) * 120)
    
    ctype = cfg["card_type"]
    if ctype == "WARNING":
        draw_warning_card(draw, cx, cur_cy, cw=cw)
    elif ctype == "GAUGE":
        draw_gauge_card(draw, cx, cur_cy, cw=cw, t_rel=scene_rel_t)
    elif ctype == "PAYG":
        draw_payg_card(draw, cx, cur_cy, cw=cw)
    elif ctype == "TERMINAL_ANIMATED":
        draw_animated_terminal(draw, cx, cur_cy, cw=cw, t_rel=scene_rel_t)
    elif ctype == "CTA":
        draw_cta_card(draw, cx, cur_cy, cw=cw)
        
    # E. Character with Momentum (Breathing, Sway, Spring Entry)
    char_img = CHARACTERS.get(cfg["char"])
    if char_img:
        ch_w, ch_h = char_img.size
        target_h = 820
        target_w = int(ch_w * (target_h / ch_h))
        
        # Breathing & body sway
        breath = math.sin(t * 3.5) * 6.0
        sway = math.sin(t * 2.2) * 4.0
        
        # Spring Entry from bottom
        char_slide = min(1.0, scene_rel_t / 0.40)
        p_c = char_slide - 1.0
        char_ease = 1.0 + c3 * (p_c**3) + c1 * (p_c**2) if char_slide < 1.0 else 1.0
        entry_offset_y = int((1.0 - char_ease) * 150)
        
        char_resized = char_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        if cfg["char_side"] == "right":
            char_x = int(w - target_w + 35 + sway)
            char_y = int(h - target_h + 30 + breath + entry_offset_y)
        else:
            char_x = int(-35 + sway)
            char_y = int(h - target_h + 30 + breath + entry_offset_y)
            
        im.paste(char_resized, (char_x, char_y), char_resized)
        
    # F. Speech Callout Bubble (with proper padding & clean wrap)
    bubble_w, bubble_h = 620, 140
    bx = 50 if cfg["char_side"] == "right" else w - 50 - bubble_w
    by = h - 650
    draw.rounded_rectangle([bx, by, bx + bubble_w, by + bubble_h], radius=20, fill=(15, 23, 42, 245), outline=(6, 182, 212, 255), width=3)
    draw.text((bx + 30, by + 20), cfg["bubble_title"], font=FONT_BUBBLE_TITLE, fill=(245, 158, 11, 255))
    draw.text((bx + 30, by + 65), cfg["bubble_text"], font=FONT_BUBBLE_TEXT, fill=(255, 255, 255, 255))
    
    # G. Bottom Kinetic Subtitle Box (Zero Overflow Guarantee)
    sub_box_y = h - 220
    draw.rounded_rectangle([50, sub_box_y, w - 50, sub_box_y + 140], radius=18, fill=(10, 15, 26, 245), outline=(30, 41, 59, 255), width=2)
    
    # Use our safe wrap function
    draw_safe_wrapped_text(draw, cfg["subtitle"], FONT_SUBTITLE, (80, sub_box_y + 15, w - 80, sub_box_y + 125), (250, 204, 21, 255), line_spacing=10, max_lines=2)
    
    return im.convert("RGB")

# 7. Render Stream to FFmpeg
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
    int(schedule["scene4_fix2_script"]["start"] * fps) + 50: "snap_4_terminal_typing.jpg",
    int(schedule["scene4_fix2_script"]["start"] * fps) + 120: "snap_4_terminal_done.jpg",
    int(schedule["scene5_cta"]["start"] * fps) + 25: "snap_5_cta.jpg"
}

for f in range(total_frames):
    frame_img = draw_frame(f, fps, schedule, total_dur)
    
    if f in snapshot_targets:
        sname = snapshot_targets[f]
        sp = os.path.join(SNAPSHOTS_DIR, sname)
        frame_img.save(sp, quality=95)
        print(f"Saved snapshot {sname} at frame {f}")
        
    proc.stdin.write(frame_img.tobytes())
    if f % 300 == 0 or f == total_frames - 1:
        pct = (f / total_frames) * 100
        print(f"Rendered Frame {f}/{total_frames} ({pct:.1f}%)")

proc.stdin.close()
proc.wait()
print("Video Stream Complete:", TEMP_VIDEO_TRACK)

# 8. Mux Final Video + Audio
print("--- Assembling Final Master MP4 ---")
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

print(f"\n🎉 MASTER REEL V3 PASSED: {OUTPUT_VIDEO}")
print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")
