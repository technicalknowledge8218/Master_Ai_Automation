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
AUDIO_DIR = os.path.join(BASE_DIR, "dual_dialogue_v5")
SFX_DIR = os.path.join(BASE_DIR, "sfx")
CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
BGM_SOURCE = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\bgm_authentic_track.wav"
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots_v4_conversational")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(BASE_DIR, "oracle_cloud_conversational_master.mp4")
TEMP_VIDEO_TRACK = os.path.join(BASE_DIR, "temp_video_v4.mp4")
TEMP_AUDIO_TRACK = os.path.join(BASE_DIR, "temp_audio_v4.wav")

# Load Dialogue Metadata
with open(os.path.join(AUDIO_DIR, "dialogue_meta.json"), "r", encoding="utf-8") as f:
    dialogue_meta = json.load(f)

# 1. Build Timeline Schedule with Smooth Transitions
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
            "config": item["config"]
        }
        audio_tracks[tid] = {"data": data, "sr": sr}
        cur_t += dur + 0.12 # tight 0.12s natural conversational gap
        
    total_dur = cur_t + 0.4
    return schedule, audio_tracks, total_dur, target_sr

schedule, audio_tracks, total_dur, target_sr = build_timeline()
print(f"Total Master Video Planned Duration: {total_dur:.2f}s")

# 2. Multi-Track Audio Master (Junior + Senior + Typing SFX + BGM + Cues)
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
        
        # Cues / SFX
        sfx_name = sinfo["config"].get("sfx", "")
        if sfx_name and sfx_name != "typing.wav":
            sfx_p = os.path.join(SFX_DIR, sfx_name)
            if os.path.exists(sfx_p):
                sdata, ssr = sf.read(sfx_p)
                if len(sdata.shape) > 1: sdata = sdata.mean(axis=1)
                s_end = min(total_samples, start_idx + len(sdata))
                master[start_idx:s_end] += sdata[:s_end - start_idx] * 0.40
                
        # Terminal typing SFX for Turn 6
        if tid == "turn6_senior_terminal_fix":
            typ_p = os.path.join(SFX_DIR, "typing.wav")
            if os.path.exists(typ_p):
                tdata, tsr = sf.read(typ_p)
                if len(tdata.shape) > 1: tdata = tdata.mean(axis=1)
                t_start = start_idx + int(0.6 * target_sr)
                t_end = min(total_samples, t_start + len(tdata))
                master[t_start:t_end] += tdata[:t_end - t_start] * 0.35
                
    # Background Music at clean -18dB side-chain ducking
    if os.path.exists(BGM_SOURCE):
        bgm_data, bsr = sf.read(BGM_SOURCE)
        if len(bgm_data.shape) > 1: bgm_data = bgm_data.mean(axis=1)
        repeats = int(np.ceil(total_samples / len(bgm_data)))
        bgm_full = np.tile(bgm_data, repeats)[:total_samples]
        master += bgm_full * 0.095
        
    max_val = np.max(np.abs(master))
    if max_val > 0.95:
        master = master * (0.95 / max_val)
        
    sf.write(TEMP_AUDIO_TRACK, master, target_sr)
    print("Master Conversational Audio Compiled:", TEMP_AUDIO_TRACK)

compile_audio(total_dur, target_sr)

# 3. Load Character Sprites
CHARACTERS = {}
for name in ["arjun_shocked.png", "arjun_shrug.png", "arjun_pointing.png", "arjun_thumbsup.png",
             "dr_kabir_warning.png", "dr_kabir_proud.png", "dr_kabir_tablet.png", "dr_kabir_explaining.png"]:
    p = os.path.join(CHAR_LIB, name)
    if os.path.exists(p):
        CHARACTERS[name] = Image.open(p).convert("RGBA")

# Fonts
FONT_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
FONT_CARD_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
FONT_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 26)
FONT_MONO_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 28)
FONT_SPEAKER_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)

# 4. Zero-Overflow Text Helper
def draw_safe_wrapped_text(draw, text, font, box, fill, line_spacing=8, max_lines=3):
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

# 5. Dynamic Graphic Cards
def draw_turn1_alert_card(draw, cx, cy, cw=940, ch=500):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(239, 68, 68, 255), width=4)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=24, fill=(55, 20, 25, 255))
    draw.text((cx + 40, cy + 24), "🚨 OCI INSTANCE TERMINATION ALERT", font=FONT_CARD_TITLE, fill=(239, 68, 68, 255))
    
    draw.text((cx + 40, cy + 115), "Instance: oci-free-dev-vm (VM.Standard.A1.Flex)", font=FONT_CARD_BOLD, fill=(255, 255, 255, 255))
    draw.text((cx + 40, cy + 155), "Specs: 4 OCPU, 24 GB RAM | 7 Days Idle Detected", font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
    
    ax1, ay1, ax2, ay2 = cx + 40, cy + 210, cx + cw - 40, cy + 355
    draw.rounded_rectangle([ax1, ay1, ax2, ay2], radius=16, fill=(48, 16, 22, 255), outline=(239, 68, 68, 255), width=2)
    draw.text((ax1 + 25, ay1 + 20), "STATUS: RECLAMATION ACTIVE!", font=FONT_CARD_TITLE, fill=(239, 68, 68, 255))
    draw.text((ax1 + 25, ay1 + 68), "Trigger: 7 Consecutive Days CPU < 20%", font=FONT_CARD_BODY, fill=(255, 255, 255, 255))
    draw.text((ax1 + 25, ay1 + 105), "Countdown: 48 Hours To Full VM Termination!", font=FONT_CARD_BOLD, fill=(245, 158, 11, 255))
    
    draw.rounded_rectangle([cx + 40, cy + 380, cx + cw - 40, cy + 465], radius=14, fill=(20, 30, 45, 255))
    draw.text((cx + 60, cy + 408), "Data Loss Threat: ALL Boot Storage Will Be Erased", font=FONT_CARD_BOLD, fill=(255, 255, 255, 255))

def draw_turn2_gauge_card(draw, cx, cy, cw=940, ch=460, t_rel=0.0):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(51, 65, 85, 255), width=3)
    draw.text((cx + 40, cy + 30), "📊 ORACLE RULE: 7-DAY CPU THRESHOLD", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255))
    
    bar_x, bar_y, bar_w, bar_h = cx + 40, cy + 120, cw - 80, 60
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=30, fill=(45, 55, 72, 255))
    
    t_x = bar_x + int(bar_w * 0.20)
    cpu_val = 7.5 + 2.5 * math.sin(t_rel * 4.0)
    fill_w = int(bar_w * (cpu_val / 100.0))
    draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=30, fill=(239, 68, 68, 255))
    
    draw.line([(t_x, bar_y - 12), (t_x, bar_y + bar_h + 12)], fill=(245, 158, 11, 255), width=4)
    draw.text((t_x - 70, bar_y + bar_h + 20), "20% MIN LIMIT", font=FONT_TAG, fill=(245, 158, 11, 255))
    
    draw.text((cx + 40, cy + 250), f"Current Usage: {cpu_val:.1f}%", font=FONT_HEADER, fill=(239, 68, 68, 255))
    draw.text((cx + 40, cy + 325), "Oracle Status: IDLE DETECTED (Under 20%)", font=FONT_CARD_TITLE, fill=(239, 68, 68, 255))
    draw.text((cx + 40, cy + 380), "Solution: Must keep CPU > 20% or upgrade tier", font=FONT_CARD_BODY, fill=(148, 163, 184, 255))

def draw_turn4_payg_card(draw, cx, cy, cw=940, ch=540):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(16, 185, 129, 255), width=4)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=24, fill=(16, 50, 35, 255))
    draw.text((cx + 40, cy + 24), "✅ HACK 1: UPGRADE TO PAY-AS-YOU-GO", font=FONT_CARD_TITLE, fill=(16, 185, 129, 255))
    
    benefits = [
        ("💰 Cost For Always Free:", "Rs. 0 / Month ($0.00 Forever)"),
        ("⚡ Idle Instance Reclaim:", "100% IMMUNE (Never Terminated)"),
        ("🛡️ Account Status:", "Paid Tier (Enterprise Exemption)"),
        ("🚀 4 ARM Cores + 24GB RAM:", "Keeps Running 24/7 Without Shutdown!")
    ]
    
    y = cy + 115
    for label, val in benefits:
        draw.rounded_rectangle([cx + 35, y, cx + cw - 35, y + 80], radius=14, fill=(20, 30, 45, 255), outline=(40, 60, 85, 255), width=2)
        draw.text((cx + 55, y + 14), label, font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
        draw.text((cx + 55, y + 42), val, font=FONT_CARD_BOLD, fill=(16, 185, 129, 255) if "0" in val or "IMMUNE" in val else (255, 255, 255, 255))
        y += 98

def draw_turn6_animated_terminal(draw, cx, cy, cw=940, ch=540, t_rel=0.0):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill=(13, 17, 23, 255), outline=(48, 54, 61, 255), width=3)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 55], radius=20, fill=(22, 27, 34, 255))
    draw.ellipse([cx + 25, cy + 18, cx + 43, cy + 36], fill=(255, 95, 86, 255))
    draw.ellipse([cx + 55, cy + 18, cx + 73, cy + 36], fill=(255, 189, 46, 255))
    draw.ellipse([cx + 85, cy + 18, cx + 103, cy + 36], fill=(39, 201, 63, 255))
    draw.text((cx + 280, cy + 16), "bash — ubuntu@oci-free-vps:~ (ssh)", font=FONT_TAG, fill=(139, 148, 158, 255))
    
    cursor = "█" if int(t_rel * 3.0) % 2 == 0 else ""
    cmd_full = "lookbusy -c 22 -m 128MB --quiet &"
    cmd_progress = min(1.0, max(0.0, (t_rel - 0.8) / 2.8))
    cmd_typed = cmd_full[:int(len(cmd_full) * cmd_progress)]
    
    y = cy + 90
    draw.text((cx + 35, y), "ubuntu@oci-vps:~$ ", font=FONT_MONO_BOLD, fill=(126, 231, 135, 255))
    prompt_w = FONT_MONO_BOLD.getbbox("ubuntu@oci-vps:~$ ")[2]
    c_disp = cmd_typed + (cursor if t_rel < 4.0 else "")
    draw.text((cx + 35 + prompt_w, y), c_disp, font=FONT_MONO, fill=(250, 204, 21, 255))
    
    if t_rel >= 4.0:
        y += 65
        draw.text((cx + 35, y), "[OK] Process lookbusy started in background (PID 4821)", font=FONT_MONO, fill=(139, 148, 158, 255))
        y += 45
        draw.text((cx + 35, y), "[OK] CPU Utilization locked at 22.4% (Threshold: 20%)", font=FONT_MONO, fill=(126, 231, 135, 255))
        y += 60
        draw.rounded_rectangle([cx + 35, y, cx + cw - 35, y + 80], radius=12, fill=(16, 45, 30, 255), outline=(46, 160, 67, 255), width=2)
        draw.text((cx + 50, y + 16), "[✓] WORKER ACTIVE: 22% CPU SAFE LOCK", font=FONT_MONO_BOLD, fill=(126, 231, 135, 255))
        draw.text((cx + 50, y + 46), "[✓] OCI IDLE DETECTION: 100% BYPASSED", font=FONT_MONO_BOLD, fill=(56, 189, 248, 255))

def draw_turn7_outro_card(draw, cx, cy, cw=940, ch=500):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 255), outline=(6, 182, 212, 255), width=4)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 85], radius=24, fill=(15, 35, 55, 255))
    draw.text((cx + 40, cy + 24), "🚀 LIFETIME FREE VM CHECKLIST", font=FONT_CARD_TITLE, fill=(6, 182, 212, 255))
    
    items = [
        ("✅ 4 ARM Cores & 24GB RAM:", "100% Free Forever"),
        ("✅ Method 1 (Official):", "Upgrade to PAYG ($0 Bill)"),
        ("✅ Method 2 (No Card):", "Run 'lookbusy' Idle Script"),
        ("📩 Setup Guide & Script:", "Comment 'ORACLE' Below!")
    ]
    
    y = cy + 115
    for label, val in items:
        draw.rounded_rectangle([cx + 35, y, cx + cw - 35, y + 75], radius=14, fill=(20, 30, 45, 255))
        draw.text((cx + 55, y + 20), label, font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
        draw.text((cx + 460, y + 20), val, font=FONT_CARD_BOLD, fill=(245, 158, 11, 255) if "ORACLE" in val else (255, 255, 255, 255))
        y += 88

# 6. Master Conversational Scene Renderer
def draw_frame(f_idx, fps, schedule, total_dur):
    t = f_idx / fps
    w, h = 1080, 1920
    
    # Active Turn
    active_tid = "turn1_junior_panic"
    active_sinfo = schedule["turn1_junior_panic"]
    for tid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"] + 0.12:
            active_tid = tid
            active_sinfo = sinfo
            break
            
    cfg = active_sinfo["config"]
    scene_rel_t = t - active_sinfo["start"]
    cam = cfg["camera"]
    
    bg_color = tuple(cfg["bg"]) if isinstance(cfg["bg"], list) else cfg["bg"]
    im = Image.new("RGBA", (w, h), bg_color)
    draw = ImageDraw.Draw(im)
    
    # Progress Scrub Bar
    progress_pct = min(1.0, t / total_dur)
    draw.rectangle([0, 0, w, 8], fill=(30, 41, 59, 255))
    draw.rectangle([0, 0, int(w * progress_pct), 8], fill=(6, 182, 212, 255))
    
    # Top Category Header
    draw.rounded_rectangle([60, 75, w - 60, 150], radius=16, fill=(15, 23, 42, 235), outline=(51, 65, 85, 255), width=2)
    draw.text((90, 97), f"🔥 TECH CONVERSATION  |  {cfg['tag']}", font=FONT_TAG, fill=(6, 182, 212, 255))
    
    # Category Title
    draw.text((60, 185), "ORACLE CLOUD FREE TIER", font=FONT_HEADER, fill=(255, 255, 255, 255))
    
    # Card with Spring Easing
    cw = 940
    cx = (w - cw) // 2
    target_cy = 280
    slide_progress = min(1.0, scene_rel_t / 0.35)
    c1 = 1.70158
    c3 = c1 + 1
    p = slide_progress - 1.0
    ease = 1.0 + c3 * (p**3) + c1 * (p**2) if slide_progress < 1.0 else 1.0
    cur_cy = int(target_cy - (1.0 - ease) * 120)
    
    # Draw Specific Center Visual
    if active_tid == "turn1_junior_panic":
        draw_turn1_alert_card(draw, cx, cur_cy, cw=cw)
    elif active_tid == "turn2_senior_explain_rule":
        draw_turn2_gauge_card(draw, cx, cur_cy, cw=cw, t_rel=scene_rel_t)
    elif active_tid in ["turn3_junior_ask_payg", "turn5_junior_ask_nocard"]:
        # Question card
        draw.rounded_rectangle([cx, cur_cy, cx + cw, cur_cy + 420], radius=24, fill=(30, 41, 59, 255), outline=(245, 158, 11, 255), width=4)
        draw.rounded_rectangle([cx, cur_cy, cx + cw, cur_cy + 85], radius=24, fill=(45, 30, 15, 255))
        draw.text((cx + 40, cur_cy + 24), "❓ JUNIOR DEVELOPER QUESTION", font=FONT_CARD_TITLE, fill=(245, 158, 11, 255))
        draw.text((cx + 40, cur_cy + 130), "Issue: Always Free VM Idle Reclamation", font=FONT_CARD_BOLD, fill=(255, 255, 255, 255))
        draw.text((cx + 40, cur_cy + 180), "Question: Any cost, credit card or subscription needed?", font=FONT_CARD_BODY, fill=(148, 163, 184, 255))
        draw.rounded_rectangle([cx + 40, cur_cy + 250, cx + cw - 40, cur_cy + 360], radius=16, fill=(20, 25, 40, 255))
        draw.text((cx + 60, cur_cy + 285), "Goal: 100% Free Lifetime Without Paying ₹1", font=FONT_CARD_BOLD, fill=(6, 182, 212, 255))
    elif active_tid == "turn4_senior_payg_fix":
        draw_turn4_payg_card(draw, cx, cur_cy, cw=cw)
    elif active_tid == "turn6_senior_terminal_fix":
        draw_turn6_animated_terminal(draw, cx, cur_cy, cw=cw, t_rel=scene_rel_t)
    elif active_tid == "turn7_outro_duo":
        draw_turn7_outro_card(draw, cx, cur_cy, cw=cw)
        
    # CHARACTER ANIMATION BASED ON CAMERA CUT
    breath = math.sin(t * 3.5) * 6.0
    sway = math.sin(t * 2.2) * 4.0
    char_slide = min(1.0, scene_rel_t / 0.40)
    p_c = char_slide - 1.0
    char_ease = 1.0 + c3 * (p_c**3) + c1 * (p_c**2) if char_slide < 1.0 else 1.0
    entry_offset_y = int((1.0 - char_ease) * 160)
    
    if cam == "JUNIOR_CLOSEUP" or cam == "JUNIOR_REACTION":
        # Junior in focus (Right side, large expressive presence)
        char_img = CHARACTERS.get(cfg["char"])
        if char_img:
            ch_w, ch_h = char_img.size
            target_h = 860
            target_w = int(ch_w * (target_h / ch_h))
            char_resized = char_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            char_x = int(w - target_w + 40 + sway)
            char_y = int(h - target_h + 30 + breath + entry_offset_y)
            im.paste(char_resized, (char_x, char_y), char_resized)
            
            # Speaker Badge
            draw.rounded_rectangle([char_x - 40, char_y + 120, char_x + 160, char_y + 175], radius=12, fill=(249, 115, 22, 255))
            draw.text((char_x - 20, char_y + 132), "JUNIOR (Arjun)", font=FONT_SPEAKER_BADGE, fill=(255, 255, 255, 255))
            
    elif cam in ["SENIOR_EXPLAIN", "SENIOR_PAYG", "TERMINAL_ANIMATED"]:
        # Senior in focus (Left side, authoritative presence)
        char_img = CHARACTERS.get(cfg["char"])
        if char_img:
            ch_w, ch_h = char_img.size
            target_h = 860
            target_w = int(ch_w * (target_h / ch_h))
            char_resized = char_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            char_x = int(-40 + sway)
            char_y = int(h - target_h + 30 + breath + entry_offset_y)
            im.paste(char_resized, (char_x, char_y), char_resized)
            
            # Speaker Badge
            draw.rounded_rectangle([char_x + target_w - 140, char_y + 120, char_x + target_w + 90, char_y + 175], radius=12, fill=(37, 99, 235, 255))
            draw.text((char_x + target_w - 120, char_y + 132), "SENIOR (Dr. Kabir)", font=FONT_SPEAKER_BADGE, fill=(255, 255, 255, 255))
            
    elif cam == "DUO_OUTRO":
        # Both characters together!
        # Left: Dr. Kabir
        kabir_img = CHARACTERS.get(cfg["char_s"])
        if kabir_img:
            ch_w, ch_h = kabir_img.size
            target_h = 780
            target_w = int(ch_w * (target_h / ch_h))
            k_res = kabir_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            im.paste(k_res, (int(-30 + sway), int(h - target_h + 30 + breath)), k_res)
            
        # Right: Arjun
        arjun_img = CHARACTERS.get(cfg["char_j"])
        if arjun_img:
            ch_w, ch_h = arjun_img.size
            target_h = 780
            target_w = int(ch_w * (target_h / ch_h))
            a_res = arjun_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            im.paste(a_res, (int(w - target_w + 30 - sway), int(h - target_h + 30 + breath)), a_res)
            
    # Bottom Subtitle Box with Safe Wrapped Text
    sub_box_y = h - 215
    draw.rounded_rectangle([50, sub_box_y, w - 50, sub_box_y + 140], radius=18, fill=(10, 15, 26, 248), outline=(30, 41, 59, 255), width=2)
    
    # Speaker indicator color
    sub_color = (249, 115, 22, 255) if "Junior" in cfg["subtitle"] else ((56, 189, 248, 255) if "Senior" in cfg["subtitle"] else (250, 204, 21, 255))
    draw_safe_wrapped_text(draw, cfg["subtitle"], FONT_SUBTITLE, (80, sub_box_y + 15, w - 80, sub_box_y + 125), sub_color, line_spacing=8, max_lines=2)
    
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
    int(schedule["turn1_junior_panic"]["start"] * fps) + 30: "snap_1_junior_panic.jpg",
    int(schedule["turn2_senior_explain_rule"]["start"] * fps) + 40: "snap_2_senior_gauge.jpg",
    int(schedule["turn3_junior_ask_payg"]["start"] * fps) + 30: "snap_3_junior_question.jpg",
    int(schedule["turn4_senior_payg_fix"]["start"] * fps) + 40: "snap_4_senior_payg.jpg",
    int(schedule["turn6_senior_terminal_fix"]["start"] * fps) + 50: "snap_5_senior_terminal.jpg",
    int(schedule["turn7_outro_duo"]["start"] * fps) + 35: "snap_6_duo_outro.jpg"
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

# 8. Mux Final Audio & Video
print("--- Assembling Final Master Conversational MP4 ---")
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

print(f"\n🎉 CONVERSATIONAL MASTER REEL READY: {OUTPUT_VIDEO}")
print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")
