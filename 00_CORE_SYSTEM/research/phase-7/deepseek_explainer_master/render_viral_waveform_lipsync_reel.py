import os
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf
import numpy as np

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
PROJ_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master"
AUDIO_DIR = os.path.join(PROJ_DIR, "viral_en_audio")
SNAP_DIR = os.path.join(PROJ_DIR, "snapshots_viral")
os.makedirs(SNAP_DIR, exist_ok=True)
OUTPUT_MP4 = os.path.join(PROJ_DIR, "deepseek_viral_waveform_lipsync_master.mp4")

TRACKS = [
    {
        "id": "line1_j",
        "file": "line1_j.wav",
        "speaker": "junior",
        "sub": "Junior: 'Wait! Should I cancel my $20 ChatGPT sub? DeepSeek is literally free!'",
        "action": "junior_excited"
    },
    {
        "id": "line2_s",
        "file": "line2_s.wav",
        "speaker": "senior",
        "sub": "Senior: 'Hold on! In coding, DeepSeek is a beast, but know these 3 facts first!'",
        "action": "senior_warn"
    },
    {
        "id": "line3_s",
        "file": "line3_s.wav",
        "speaker": "senior",
        "sub": "Senior: '1. Reasoning Power: In Python & math, DeepSeek R1 destroys GPT-4o!'",
        "action": "point1"
    },
    {
        "id": "line4_s",
        "file": "line4_s.wav",
        "speaker": "senior",
        "sub": "Senior: '2. Privacy Warning: Never put company code in cloud! Run locally!'",
        "action": "point2"
    },
    {
        "id": "line5_j",
        "file": "line5_j.wav",
        "speaker": "junior",
        "sub": "Junior: 'Wait! We can run the entire model on our own laptop without internet?'",
        "action": "junior_shocked"
    },
    {
        "id": "line6_s",
        "file": "line6_s.wav",
        "speaker": "senior",
        "sub": "Senior: 'Exactly! 100% Free, zero leaks! Comment LOCAL for full setup guide!'",
        "action": "cta"
    }
]

# 1. Load Audio Data and calculate exact timing
def load_audio_data():
    audio_data = {}
    gap = 0.08  # Snappy micro-pause
    cur_t = 0.3
    schedule = {}
    
    for t in TRACKS:
        fp = os.path.join(AUDIO_DIR, t["file"])
        data, sr = sf.read(fp)
        if len(data.shape) > 1:
            data = data.mean(axis=1) # Mono
        dur = len(data) / sr
        
        audio_data[t["id"]] = {"data": data, "sr": sr, "dur": dur}
        schedule[t["id"]] = {
            "start": cur_t,
            "end": cur_t + dur,
            "dur": dur,
            "speaker": t["speaker"],
            "sub": t["sub"],
            "action": t["action"],
            "file": t["file"]
        }
        print(f"Loaded {t['file']}: {dur:.2f}s (SR={sr})")
        cur_t += dur + gap
        
    total_dur = cur_t + 0.8
    return audio_data, schedule, total_dur

# Calculate exact RMS amplitude at time t for a speaker
def get_speech_envelope(t, sid, schedule, audio_data):
    sinfo = schedule[sid]
    if not (sinfo["start"] <= t <= sinfo["end"]):
        return 0.0
    
    offset_s = t - sinfo["start"]
    data = audio_data[sid]["data"]
    sr = audio_data[sid]["sr"]
    center_idx = int(offset_s * sr)
    
    # 40ms window
    win = int(0.040 * sr)
    start_idx = max(0, center_idx - win // 2)
    end_idx = min(len(data), center_idx + win // 2)
    
    if start_idx >= end_idx:
        return 0.0
    
    chunk = data[start_idx:end_idx]
    rms = np.sqrt(np.mean(chunk**2))
    return float(rms)

# Fonts
FONT_MAIN_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
FONT_SUB_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
FONT_CARD_DESC = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 30)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)

def draw_frame(f_idx, fps, schedule, total_duration, audio_data):
    t = f_idx / fps
    w, h = 1080, 1920
    
    # Clean Studio Light Background
    im = Image.new("RGBA", (w, h), (241, 245, 249, 255))
    draw = ImageDraw.Draw(im)
    
    # Background subtle technical grid dots
    for gx in range(40, w, 60):
        for gy in range(40, h, 60):
            draw.ellipse([gx, gy, gx + 2, gy + 2], fill=(203, 213, 225, 120))
            
    # Bottom Studio Floor
    draw.rectangle([0, 1830, w, h], fill=(226, 232, 240, 255))
    draw.line([0, 1830, w, 1830], fill=(148, 163, 184, 255), width=3)
    
    # ==========================================
    # 1. TOP WHITEBOARD COMPONENT (Y: 90 - 1070)
    # ==========================================
    draw.rounded_rectangle([72, 94, 1008, 1074], radius=28, fill=(148, 163, 184, 160))
    draw.rounded_rectangle([70, 90, 1010, 1070], radius=26, fill=(255, 255, 255, 255), outline=(30, 41, 59, 255), width=8)
    draw.rounded_rectangle([86, 106, 994, 1030], radius=18, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    
    # Marker Tray & Pens
    draw.rounded_rectangle([250, 1056, 830, 1072], radius=6, fill=(71, 85, 105, 255), outline=(15, 23, 42, 255), width=2)
    draw.rounded_rectangle([320, 1050, 360, 1062], radius=3, fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([380, 1050, 420, 1062], radius=3, fill=(15, 23, 42, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([440, 1050, 480, 1062], radius=3, fill=(37, 99, 235, 255), outline=(15, 23, 42, 255), width=1)
    
    # Header Card
    draw.rounded_rectangle([100, 125, 980, 210], radius=18, fill=(15, 23, 42, 255))
    draw.text((540, 168), "DEEPSEEK R1 VS CHATGPT-4o ⚡", font=FONT_MAIN_TITLE, fill=(255, 255, 255, 255), anchor="mm")
    
    # Hook Card
    draw.rounded_rectangle([120, 230, 960, 315], radius=16, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255), width=3)
    draw.text((540, 272), "CHATGPT PLUS: $20/MONTH SUBSCRIPTION 💸", font=FONT_SUB_HEADER, fill=(30, 41, 59, 255), anchor="mm")
    
    # Strikethrough Animation on Hook Card
    t_l2_start = schedule["line2_s"]["start"]
    if t >= t_l2_start + 0.5:
        strike_prog = min(1.0, (t - (t_l2_start + 0.5)) / 0.45)
        start_x = 160
        end_x = start_x + int(strike_prog * 760)
        draw.line([start_x, 272, end_x, 272], fill=(239, 68, 68, 255), width=10)
        if strike_prog >= 0.7:
            draw.rounded_rectangle([740, 236, 940, 308], radius=12, fill=(239, 68, 68, 255))
            draw.text((840, 272), "CANCEL? ❌", font=FONT_SUB_HEADER, fill=(255, 255, 255, 255), anchor="mm")

    # Point 1: Reasoning Power
    t_l3_start = schedule["line3_s"]["start"]
    if t >= t_l3_start + 0.2:
        draw.rounded_rectangle([110, 350, 970, 480], radius=18, fill=(238, 242, 255, 255), outline=(79, 70, 229, 255), width=3)
        draw.rounded_rectangle([135, 375, 215, 455], radius=16, fill=(79, 70, 229, 255))
        draw.text((175, 415), "1", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 395), "REASONING & COMPLEX CODE 🧠", font=FONT_CARD_TITLE, fill=(49, 46, 129, 255), anchor="lm")
        draw.text((245, 442), "DeepSeek R1 destroys GPT-4o in Python & Math! (100% Free)", font=FONT_CARD_DESC, fill=(67, 56, 202, 255), anchor="lm")
        draw.rounded_rectangle([780, 380, 945, 415], radius=8, fill=(30, 27, 75, 255))
        draw.text((862, 398), "BENCHMARK 🏆", font=FONT_TAG, fill=(165, 180, 252, 255), anchor="mm")
        
    # Point 2: Privacy Warning
    t_l4_start = schedule["line4_s"]["start"]
    if t >= t_l4_start + 0.2:
        draw.rounded_rectangle([110, 510, 970, 640], radius=18, fill=(254, 242, 242, 255), outline=(239, 68, 68, 255), width=3)
        draw.rounded_rectangle([135, 535, 215, 615], radius=16, fill=(239, 68, 68, 255))
        draw.text((175, 575), "2", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 555), "PRIVACY & DATA LEAK WARNING ⚠️", font=FONT_CARD_TITLE, fill=(153, 27, 27, 255), anchor="lm")
        draw.text((245, 602), "Never put company code in cloud! Run offline on laptop!", font=FONT_CARD_DESC, fill=(185, 28, 28, 255), anchor="lm")
        draw.rounded_rectangle([780, 540, 945, 575], radius=8, fill=(153, 27, 27, 255))
        draw.text((862, 558), "CLOUD = RISKY", font=FONT_TAG, fill=(254, 202, 202, 255), anchor="mm")

    # Point 3: 100% Offline Local Model
    t_l5_start = schedule["line5_j"]["start"]
    if t >= t_l5_start:
        draw.rounded_rectangle([110, 670, 970, 800], radius=18, fill=(240, 253, 244, 255), outline=(34, 197, 94, 255), width=3)
        draw.rounded_rectangle([135, 695, 215, 775], radius=16, fill=(34, 197, 94, 255))
        draw.text((175, 735), "3", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 715), "100% OFFLINE LAPTOP RUN 💻", font=FONT_CARD_TITLE, fill=(20, 83, 45, 255), anchor="lm")
        draw.text((245, 762), "Terminal command: 'ollama run deepseek-r1:7b'", font=FONT_CARD_DESC, fill=(22, 101, 52, 255), anchor="lm")
        draw.rounded_rectangle([780, 700, 945, 735], radius=8, fill=(20, 83, 45, 255))
        draw.text((862, 718), "₹0 FOREVER ✅", font=FONT_TAG, fill=(187, 247, 208, 255), anchor="mm")

    # Call-to-Action Card
    t_l6_start = schedule["line6_s"]["start"]
    if t >= t_l6_start + 0.3:
        draw.rounded_rectangle([110, 830, 970, 1010], radius=22, fill=(15, 23, 42, 255), outline=(56, 189, 248, 255), width=4)
        draw.text((540, 880), "🚀 WANT TO RUN DEEPSEEK ON YOUR LAPTOP?", font=FONT_SUB_HEADER, fill=(56, 189, 248, 255), anchor="mm")
        draw.text((540, 950), "COMMENT 'LOCAL' FOR FULL STEP-BY-STEP SETUP! 📩", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255), anchor="mm")

    # Speech state & Real Waveform Envelope
    active_sid = None
    junior_speaking = False
    senior_speaking = False
    current_sub = ""
    junior_rms = 0.0
    senior_rms = 0.0
    
    for sid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"]:
            active_sid = sid
            current_sub = sinfo["sub"]
            if sinfo["speaker"] == "junior":
                junior_speaking = True
                junior_rms = get_speech_envelope(t, sid, schedule, audio_data)
            else:
                senior_speaking = True
                senior_rms = get_speech_envelope(t, sid, schedule, audio_data)
            break
            
    blink = (t % 3.4) < 0.15
    junior_shocked = (schedule["line5_j"]["start"] <= t <= schedule["line5_j"]["end"] + 0.5)

    # ==========================================
    # 2. JUNIOR CHARACTER (Left: CX=300)
    # ==========================================
    j_cx, j_cy = 300, 1420
    # Dynamic head bob tied directly to vocal energy
    j_bob = int(junior_rms * 25) if junior_speaking else int(math.sin(t * 2.0) * 1.5)
    
    # Torso (Purple / Indigo Modern Hoodie)
    draw.polygon([[j_cx - 130, 1560 + j_bob], [j_cx + 130, 1560 + j_bob], [j_cx + 150, 1840], [j_cx - 150, 1840]], fill=(124, 58, 237, 255), outline=(15, 23, 42, 255))
    draw.rounded_rectangle([j_cx - 70, 1720 + j_bob, j_cx + 70, 1820], radius=12, fill=(109, 40, 217, 255), outline=(15, 23, 42, 255), width=2)
    draw.line([j_cx - 20, 1550 + j_bob, j_cx - 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    draw.line([j_cx + 20, 1550 + j_bob, j_cx + 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    
    # Dynamic Arms
    if junior_shocked:
        draw.line([j_cx - 120, 1580, j_cx - 80, 1460], fill=(124, 58, 237, 255), width=28)
        draw.line([j_cx + 120, 1580, j_cx + 80, 1460], fill=(124, 58, 237, 255), width=28)
        draw.ellipse([j_cx - 95, 1445, j_cx - 65, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 65, 1445, j_cx + 95, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    elif junior_speaking and (schedule["line1_j"]["start"] <= t <= schedule["line1_j"]["end"]):
        hand_lift = int(junior_rms * 60)
        draw.line([j_cx + 120, 1600, j_cx + 160, 1430 - hand_lift], fill=(124, 58, 237, 255), width=28)
        draw.ellipse([j_cx + 145, 1410 - hand_lift, j_cx + 180, 1445 - hand_lift], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        draw.line([j_cx - 120, 1590, j_cx - 80, 1720], fill=(124, 58, 237, 255), width=26)
    else:
        draw.line([j_cx - 120, 1590, j_cx - 80, 1720], fill=(124, 58, 237, 255), width=26)
        draw.line([j_cx + 120, 1590, j_cx + 80, 1720], fill=(124, 58, 237, 255), width=26)
        
    # Head & Hair
    draw.ellipse([j_cx - 135, j_cy - 120 + j_bob, j_cx - 75, j_cy + 20 + j_bob], fill=(30, 27, 75, 255))
    draw.ellipse([j_cx - 95, j_cy - 110 + j_bob, j_cx + 95, j_cy + 110 + j_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=4)
    draw.chord([j_cx - 100, j_cy - 120 + j_bob, j_cx + 100, j_cy + 30 + j_bob], 180, 360, fill=(30, 27, 75, 255))
    
    # Expressive Eyes
    if blink:
        draw.line([j_cx - 50, j_cy - 15 + j_bob, j_cx - 10, j_cy - 15 + j_bob], fill=(15, 23, 42, 255), width=4)
        draw.line([j_cx + 10, j_cy - 15 + j_bob, j_cx + 50, j_cy - 15 + j_bob], fill=(15, 23, 42, 255), width=4)
    elif junior_shocked:
        draw.ellipse([j_cx - 55, j_cy - 35 + j_bob, j_cx - 15, j_cy + 5 + j_bob], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 15, j_cy - 35 + j_bob, j_cx + 55, j_cy + 5 + j_bob], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx - 38, j_cy - 18 + j_bob, j_cx - 32, j_cy - 12 + j_bob], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx + 32, j_cy - 18 + j_bob, j_cx + 38, j_cy - 12 + j_bob], fill=(15, 23, 42, 255))
    else:
        draw.ellipse([j_cx - 45, j_cy - 25 + j_bob, j_cx - 15, j_cy + 5 + j_bob], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx + 15, j_cy - 25 + j_bob, j_cx + 45, j_cy + 5 + j_bob], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx - 32, j_cy - 22 + j_bob, j_cx - 24, j_cy - 14 + j_bob], fill=(255, 255, 255, 255))
        draw.ellipse([j_cx + 28, j_cy - 22 + j_bob, j_cx + 36, j_cy - 14 + j_bob], fill=(255, 255, 255, 255))

    # ==========================================
    # TRUE WAVEFORM ENVELOPE LIP-SYNC (JUNIOR)
    # ==========================================
    jm_y = j_cy + 42 + j_bob
    if junior_speaking and junior_rms >= 0.018:
        # Mouth open height scales proportionally to acoustic energy
        open_h = min(22, int((junior_rms - 0.018) * 160) + 4)
        draw.ellipse([j_cx - 22, jm_y - open_h, j_cx + 22, jm_y + open_h], fill=(15, 23, 42, 255))
        if open_h > 8:
            # White upper teeth row
            draw.chord([j_cx - 16, jm_y - open_h + 2, j_cx + 16, jm_y - 2], 180, 360, fill=(255, 255, 255, 255))
            # Pink tongue
            draw.chord([j_cx - 14, jm_y + 2, j_cx + 14, jm_y + open_h - 2], 0, 180, fill=(244, 114, 182, 255))
    elif junior_shocked:
        draw.ellipse([j_cx - 16, jm_y - 12, j_cx + 16, jm_y + 16], fill=(15, 23, 42, 255))
    else:
        # Closed smiling mouth
        draw.arc([j_cx - 22, jm_y - 8, j_cx + 22, jm_y + 12], 10, 170, fill=(15, 23, 42, 255), width=3)

    # ==========================================
    # 3. SENIOR CHARACTER (Right: CX=780)
    # ==========================================
    s_cx, s_cy = 780, 1380
    s_bob = int(senior_rms * 25) if senior_speaking else int(math.sin(t * 2.0) * 1.5)
    
    # Body (Navy Jacket + White shirt + Amber Tie)
    draw.polygon([[s_cx - 140, 1540 + s_bob], [s_cx + 140, 1540 + s_bob], [s_cx + 160, 1840], [s_cx - 160, 1840]], fill=(30, 41, 59, 255), outline=(15, 23, 42, 255))
    draw.polygon([[s_cx - 45, 1540 + s_bob], [s_cx + 45, 1540 + s_bob], [s_cx, 1660 + s_bob]], fill=(255, 255, 255, 255), outline=(203, 213, 225, 255))
    draw.polygon([[s_cx - 10, 1550 + s_bob], [s_cx + 10, 1550 + s_bob], [s_cx + 14, 1690 + s_bob], [s_cx, 1720 + s_bob], [s_cx - 14, 1690 + s_bob]], fill=(245, 158, 11, 255))
    
    # Dynamic Laser Pointer Arm
    is_pointing = senior_speaking and (schedule["line2_s"]["start"] <= t <= schedule["line4_s"]["end"] + 0.3)
    if is_pointing:
        if t >= schedule["line4_s"]["start"]:
            target_y = 575 # Point 2
        elif t >= schedule["line3_s"]["start"]:
            target_y = 415 # Point 1
        else:
            target_y = 272 # Hook card
            
        draw.line([s_cx - 130, 1570, s_cx - 240, 1180], fill=(30, 41, 59, 255), width=30)
        draw.ellipse([s_cx - 255, 1165, s_cx - 225, 1195], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        draw.line([s_cx - 240, 1180, s_cx - 360, target_y], fill=(239, 68, 68, 255), width=5)
        draw.ellipse([s_cx - 370, target_y - 10, s_cx - 350, target_y + 10], fill=(239, 68, 68, 255))
        draw.ellipse([s_cx - 378, target_y - 18, s_cx - 342, target_y + 18], fill=(239, 68, 68, 80))
    else:
        draw.line([s_cx - 130, 1570, s_cx - 90, 1730], fill=(30, 41, 59, 255), width=26)
    draw.line([s_cx + 130, 1570, s_cx + 90, 1730], fill=(30, 41, 59, 255), width=26)

    # Head & Hair
    draw.ellipse([s_cx - 95, s_cy - 110 + s_bob, s_cx + 95, s_cy + 110 + s_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=4)
    draw.chord([s_cx - 100, s_cy - 130 + s_bob, s_cx + 100, s_cy + 10 + s_bob], 180, 360, fill=(51, 65, 85, 255))
    draw.polygon([[s_cx - 70, s_cy - 120 + s_bob], [s_cx + 30, s_cy - 145 + s_bob], [s_cx + 80, s_cy - 115 + s_bob]], fill=(51, 65, 85, 255))
    
    # Glasses
    draw.rounded_rectangle([s_cx - 70, s_cy - 30 + s_bob, s_cx - 15, s_cy + 15 + s_bob], radius=10, fill=(255, 255, 255, 120), outline=(15, 23, 42, 255), width=4)
    draw.rounded_rectangle([s_cx + 15, s_cy - 30 + s_bob, s_cx + 70, s_cy + 15 + s_bob], radius=10, fill=(255, 255, 255, 120), outline=(15, 23, 42, 255), width=4)
    draw.line([s_cx - 15, s_cy - 10 + s_bob, s_cx + 15, s_cy - 10 + s_bob], fill=(15, 23, 42, 255), width=4)
    
    # Eyes
    if blink:
        draw.line([s_cx - 55, s_cy - 10 + s_bob, s_cx - 30, s_cy - 10 + s_bob], fill=(15, 23, 42, 255), width=3)
        draw.line([s_cx + 30, s_cy - 10 + s_bob, s_cx + 55, s_cy - 10 + s_bob], fill=(15, 23, 42, 255), width=3)
    else:
        draw.ellipse([s_cx - 50, s_cy - 18 + s_bob, s_cx - 35, s_cy - 3 + s_bob], fill=(15, 23, 42, 255))
        draw.ellipse([s_cx + 35, s_cy - 18 + s_bob, s_cx + 50, s_cy - 3 + s_bob], fill=(15, 23, 42, 255))

    # ==========================================
    # TRUE WAVEFORM ENVELOPE LIP-SYNC (SENIOR)
    # ==========================================
    sm_y = s_cy + 45 + s_bob
    if senior_speaking and senior_rms >= 0.018:
        open_h = min(22, int((senior_rms - 0.018) * 160) + 4)
        draw.ellipse([s_cx - 20, sm_y - open_h, s_cx + 20, sm_y + open_h], fill=(15, 23, 42, 255))
        if open_h > 8:
            draw.chord([s_cx - 14, sm_y - open_h + 2, s_cx + 14, sm_y - 2], 180, 360, fill=(255, 255, 255, 255))
            draw.chord([s_cx - 12, sm_y + 2, s_cx + 12, sm_y + open_h - 2], 0, 180, fill=(244, 114, 182, 255))
        else:
            draw.line([s_cx - 18, sm_y, s_cx + 18, sm_y], fill=(15, 23, 42, 255), width=3)
    else:
        draw.arc([s_cx - 20, sm_y - 8, s_cx + 20, sm_y + 10], 10, 170, fill=(15, 23, 42, 255), width=3)

    # 4. SUBTITLES
    if current_sub:
        draw.rounded_rectangle([60, 1765, 1020, 1845], radius=18, fill=(15, 23, 42, 235))
        draw.text((540, 1805), current_sub, font=FONT_CAPTION, fill=(255, 255, 255, 255), anchor="mm")
        
    return im.convert("RGB")

def render_video_stream(schedule, total_dur, audio_data):
    fps = 30
    total_f = int(total_dur * fps)
    print(f"--- [1/3] Streaming {total_f} Frames @ {fps}fps to FFmpeg ({total_dur:.2f}s) ---")
    raw_video = os.path.join(PROJ_DIR, "viral_video_track.mp4")
    
    # Save Keyframe Snapshots
    test_frames = [
        (int(2.0 * fps), "snap_1_hook.jpg"),
        (int(schedule["line3_s"]["start"] * fps + 30), "snap_2_point1.jpg"),
        (int(schedule["line4_s"]["start"] * fps + 30), "snap_3_point2.jpg"),
        (int(schedule["line6_s"]["start"] * fps + 30), "snap_4_cta.jpg")
    ]
    for fi, sname in test_frames:
        if fi < total_f:
            sim = draw_frame(fi, fps, schedule, total_dur, audio_data)
            sim.save(os.path.join(SNAP_DIR, sname), quality=92)
            print(f"Saved snapshot {sname} at frame {fi}")
    
    cmd_ffmpeg = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "22",
        raw_video
    ]
    
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f_idx in range(total_f):
        im = draw_frame(f_idx, fps, schedule, total_dur, audio_data)
        proc.stdin.write(im.tobytes())
        if f_idx % 200 == 0:
            print(f"Rendered Frame {f_idx}/{total_f} ({f_idx/total_f*100:.1f}%)")
            
    proc.stdin.close()
    proc.wait()
    print("Video stream rendered successfully:", raw_video)
    return raw_video

def mix_audio(schedule, total_dur):
    print("--- [2/3] Multi-Track Broadcast Audio Mixing ---")
    l1 = os.path.join(AUDIO_DIR, "line1_j.wav")
    l2 = os.path.join(AUDIO_DIR, "line2_s.wav")
    l3 = os.path.join(AUDIO_DIR, "line3_s.wav")
    l4 = os.path.join(AUDIO_DIR, "line4_s.wav")
    l5 = os.path.join(AUDIO_DIR, "line5_j.wav")
    l6 = os.path.join(AUDIO_DIR, "line6_s.wav")
    
    sfx_pop = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\sfx_pop.wav"
    sfx_scratch = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\sfx_scratch.wav"
    
    bgm_path = os.path.join(PROJ_DIR, "bgm_viral_track.wav")
    cmd_bgm = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"sine=f=220.00:d={total_dur},volume=0.05",
        "-f", "lavfi",
        "-i", f"sine=f=277.18:d={total_dur},volume=0.035",
        "-f", "lavfi",
        "-i", f"sine=f=329.63:d={total_dur},volume=0.035",
        "-f", "lavfi",
        "-i", f"anoisesrc=d={total_dur}:c=brown:r=44100,lowpass=f=200,volume=0.08",
        "-filter_complex", f"[0:a][1:a][2:a][3:a]amix=inputs=4[m];[m]afade=t=out:st={total_dur-1.5:.2f}:d=1.5[out]",
        "-map", "[out]", bgm_path
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    d1 = int(schedule["line1_j"]["start"] * 1000)
    d2 = int(schedule["line2_s"]["start"] * 1000)
    d3 = int(schedule["line3_s"]["start"] * 1000)
    d4 = int(schedule["line4_s"]["start"] * 1000)
    d5 = int(schedule["line5_j"]["start"] * 1000)
    d6 = int(schedule["line6_s"]["start"] * 1000)
    
    d_scratch = int((schedule["line2_s"]["start"] + 0.5) * 1000)
    d_p1 = int((schedule["line3_s"]["start"] + 0.2) * 1000)
    d_p2 = int((schedule["line4_s"]["start"] + 0.2) * 1000)
    d_p3 = int((schedule["line5_j"]["start"]) * 1000)
    
    mix_filter = (
        f"[0:a]adelay={d1}|{d1},volume=1.4[a0];"
        f"[1:a]adelay={d2}|{d2},volume=1.4[a1];"
        f"[2:a]adelay={d3}|{d3},volume=1.4[a2];"
        f"[3:a]adelay={d4}|{d4},volume=1.4[a3];"
        f"[4:a]adelay={d5}|{d5},volume=1.4[a4];"
        f"[5:a]adelay={d6}|{d6},volume=1.4[a5];"
        f"[6:a]volume=0.20[a6];"
        f"[7:a]adelay={d_scratch}|{d_scratch},volume=0.45[a7];"
        f"[8:a]adelay={d_p1}|{d_p1},volume=0.55[a8];"
        f"[9:a]adelay={d_p2}|{d_p2},volume=0.55[a9];"
        f"[10:a]adelay={d_p3}|{d_p3},volume=0.55[a10];"
        f"[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10]amix=inputs=11:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1.0[final_audio]"
    )
    
    final_audio = os.path.join(PROJ_DIR, "viral_final_audio.wav")
    cmd_mix = [
        FFMPEG, "-y",
        "-i", l1,
        "-i", l2,
        "-i", l3,
        "-i", l4,
        "-i", l5,
        "-i", l6,
        "-i", bgm_path,
        "-i", sfx_scratch,
        "-i", sfx_pop,
        "-i", sfx_pop,
        "-i", sfx_pop,
        "-filter_complex", mix_filter,
        "-map", "[final_audio]",
        "-t", str(total_dur),
        final_audio
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("Master audio mix compiled:", final_audio)
    return final_audio

def compile_final_mp4(v_track, a_track, total_dur):
    print("--- [3/3] Assembling Final MP4 ---")
    cmd = [
        FFMPEG, "-y",
        "-i", v_track,
        "-i", a_track,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_dur),
        OUTPUT_MP4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n🎉 MASTER REEL READY WITH REAL WAVEFORM LIP-SYNC: {OUTPUT_MP4}")
    print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")

def main():
    audio_data, schedule, total_dur = load_audio_data()
    print(f"Total Video Planned Duration: {total_dur:.2f}s")
    v_track = render_video_stream(schedule, total_dur, audio_data)
    a_track = mix_audio(schedule, total_dur)
    compile_final_mp4(v_track, a_track, total_dur)

if __name__ == "__main__":
    main()
