"""
Master AI - Fast Human-Energy Whiteboard Explainer Reel
Upgrades:
1. Snappy conversational Hindi (no bookish dragging)
2. Fast speech tempo (+25% rate, atempo 1.15, zero dead pauses)
3. Broadcast Studio Vocal Chain: High-pass 80Hz, presence EQ, radio compressor (compand)
4. Snappy 26-second total duration (Instagram Reel Sweet Spot)
"""

import os
import sys
import math
import asyncio
import subprocess
import imageio_ffmpeg
import edge_tts
from PIL import Image, ImageDraw, ImageFont

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
WORK_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test"
AUDIO_DIR = os.path.join(WORK_DIR, "fast_audio")
OUTPUT_MP4 = os.path.join(WORK_DIR, "vibe_coding_fast_human_master.mp4")

os.makedirs(AUDIO_DIR, exist_ok=True)

# Snappy natural conversational scripts
SCRIPTS = [
    {
        "id": "line1_j",
        "speaker": "junior",
        "text": "भैया! AI से 10 मिनट में पूरा ऐप बना दिया! अब डेवलपर की क्या ज़रूरत?",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+26%",
        "pitch": "+3Hz",
        "eq": "highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=4,equalizer=f=250:t=q:w=1.0:g=2,atempo=1.16,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3.5"
    },
    {
        "id": "line2_s",
        "speaker": "senior",
        "text": "अरे रुको भाई! AI कोड लिख तो देता है, पर प्रोडक्शन में ये 3 चीज़ें ऐप क्रैश करवा देंगी!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+22%",
        "pitch": "-3Hz",
        "eq": "highpass=f=80,equalizer=f=3500:t=q:w=1.2:g=4,equalizer=f=180:t=q:w=1.0:g=3,atempo=1.14,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3.5"
    },
    {
        "id": "line3_s",
        "speaker": "senior",
        "text": "पहली गलती: हार्डकोडेड API कीज़! जो सीधा गिटहब पे लीक हो जाती हैं!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+24%",
        "pitch": "-3Hz",
        "eq": "highpass=f=80,equalizer=f=3500:t=q:w=1.2:g=4,equalizer=f=180:t=q:w=1.0:g=3,atempo=1.14,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3.5"
    },
    {
        "id": "line4_s",
        "speaker": "senior",
        "text": "दूसरी: ज़ीरो एरर हैंडलिंग! हल्का सा नेटवर्क एरर आया और पूरी स्क्रीन ब्लैंक!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+24%",
        "pitch": "-3Hz",
        "eq": "highpass=f=80,equalizer=f=3500:t=q:w=1.2:g=4,equalizer=f=180:t=q:w=1.0:g=3,atempo=1.14,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3.5"
    },
    {
        "id": "line5_j",
        "speaker": "junior",
        "text": "अरे बाप रे! मतलब AI कोड लिखेगा, पर टेस्टिंग हमें ही करनी पड़ेगी?",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+26%",
        "pitch": "+3Hz",
        "eq": "highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=4,equalizer=f=250:t=q:w=1.0:g=2,atempo=1.16,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3.5"
    },
    {
        "id": "line6_s",
        "speaker": "senior",
        "text": "बिल्कुल! AI तुम्हारा जूनियर कोडर है, सीनियर आर्किटेक्ट तुम हो! फॉलो करो असली टेक टिप्स के लिए!",
        "voice": "hi-IN-MadhurNeural",
        "rate": "+24%",
        "pitch": "-3Hz",
        "eq": "highpass=f=80,equalizer=f=3500:t=q:w=1.2:g=4,equalizer=f=180:t=q:w=1.0:g=3,atempo=1.14,compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-3:gain=3.5"
    }
]

async def prepare_fast_audio():
    print("--- [1/4] Generating Fast Broadcast Neural Voiceovers ---")
    durations = {}
    for item in SCRIPTS:
        raw_p = os.path.join(AUDIO_DIR, f"{item['id']}_raw.mp3")
        clean_p = os.path.join(AUDIO_DIR, f"{item['id']}.wav")
        tts = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await tts.save(raw_p)
        
        # Apply vocal mastering chain
        cmd = [
            FFMPEG, "-y", "-i", raw_p,
            "-af", f"silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,{item['eq']}",
            clean_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Duration probe
        res = subprocess.run([FFMPEG, "-i", clean_p], stderr=subprocess.PIPE, text=True)
        dur = 3.0
        for l in res.stderr.splitlines():
            if "Duration:" in l:
                pts = l.split("Duration:")[1].split(",")[0].strip().split(":")
                dur = float(pts[0])*3600 + float(pts[1])*60 + float(pts[2])
                break
        durations[item["id"]] = dur
        print(f"Mastered {item['id']}: {dur:.2f}s")
        
    return durations

def build_timeline(durs):
    gap = 0.08 # Micro-pause (podcast level tight cuts)
    t = 0.3
    schedule = {}
    for item in SCRIPTS:
        sid = item["id"]
        d = durs[sid]
        schedule[sid] = {"start": t, "end": t + d, "dur": d, "speaker": item["speaker"]}
        t += d + gap
    total_dur = t + 0.8
    return schedule, total_dur

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 36)
FONT_CARD_DESC = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)

def draw_frame(f_idx, fps, schedule, total_duration):
    t = f_idx / fps
    w, h = 1080, 1920
    im = Image.new("RGBA", (w, h), (224, 242, 254, 255))
    draw = ImageDraw.Draw(im)
    
    # Subtle floor separator
    draw.rectangle([0, 1840, w, h], fill=(186, 230, 253, 255))
    draw.line([0, 1840, w, 1840], fill=(125, 211, 252, 255), width=3)
    
    # 1. WHITEBOARD
    draw.rounded_rectangle([72, 92, 1008, 1078], radius=28, fill=(148, 163, 184, 180))
    draw.rounded_rectangle([70, 90, 1010, 1070], radius=26, fill=(241, 245, 249, 255), outline=(30, 41, 59, 255), width=8)
    draw.rounded_rectangle([86, 106, 994, 1030], radius=18, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=3)
    
    # Tray & Markers
    draw.rounded_rectangle([250, 1056, 830, 1072], radius=6, fill=(71, 85, 105, 255), outline=(15, 23, 42, 255), width=2)
    draw.rounded_rectangle([320, 1050, 360, 1062], radius=3, fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([380, 1050, 420, 1062], radius=3, fill=(15, 23, 42, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([440, 1050, 480, 1062], radius=3, fill=(2, 132, 199, 255), outline=(15, 23, 42, 255), width=1)
    
    # Header Card
    draw.rounded_rectangle([100, 125, 980, 210], radius=18, fill=(15, 23, 42, 255))
    draw.text((540, 168), "AI CODING KI 3 SABSE BADI GALATIYAN! ⚠️", font=FONT_TITLE, fill=(255, 255, 255, 255), anchor="mm")
    
    # Hook Premise Card
    draw.rounded_rectangle([120, 230, 960, 315], radius=16, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=3)
    draw.text((540, 272), "VIBE CODING: KYA AB DEV KI ZAROORAT NAHI? 🚀", font=FONT_SUB, fill=(30, 41, 59, 255), anchor="mm")
    
    # Strike-through animation
    t_l2_start = schedule["line2_s"]["start"]
    if t >= t_l2_start + 0.6:
        strike_prog = min(1.0, (t - (t_l2_start + 0.6)) / 0.5)
        start_x = 160
        end_x = start_x + int(strike_prog * 760)
        draw.line([start_x, 272, end_x, 272], fill=(239, 68, 68, 255), width=10)
        if strike_prog >= 0.7:
            draw.rounded_rectangle([730, 236, 940, 308], radius=12, fill=(239, 68, 68, 255))
            draw.text((835, 272), "NAHI! ❌", font=FONT_SUB, fill=(255, 255, 255, 255), anchor="mm")
            
    # Points 1, 2, 3 reveals
    t_l3_start = schedule["line3_s"]["start"]
    if t >= t_l3_start + 0.2:
        draw.rounded_rectangle([110, 350, 970, 480], radius=18, fill=(254, 242, 242, 255), outline=(239, 68, 68, 255), width=3)
        draw.rounded_rectangle([135, 375, 215, 455], radius=16, fill=(239, 68, 68, 255))
        draw.text((175, 415), "1", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 395), "HARDCODED API KEYS & SECRETS 🔑", font=FONT_CARD_TITLE, fill=(153, 27, 27, 255), anchor="lm")
        draw.text((245, 442), "Code directly public GitHub pe leak ho jata hai!", font=FONT_CARD_DESC, fill=(185, 28, 28, 255), anchor="lm")
        
    t_l4_start = schedule["line4_s"]["start"]
    if t >= t_l4_start + 0.2:
        draw.rounded_rectangle([110, 510, 970, 640], radius=18, fill=(255, 247, 237, 255), outline=(249, 115, 22, 255), width=3)
        draw.rounded_rectangle([135, 535, 215, 615], radius=16, fill=(249, 115, 22, 255))
        draw.text((175, 575), "2", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 555), "ZERO ERROR HANDLING & TRY-CATCH 🛑", font=FONT_CARD_TITLE, fill=(154, 52, 18, 255), anchor="lm")
        draw.text((245, 602), "Ek network error aate hi screen blank ho jati hai!", font=FONT_CARD_DESC, fill=(194, 65, 12, 255), anchor="lm")

    t_l5_start = schedule["line5_j"]["start"]
    if t >= t_l5_start:
        draw.rounded_rectangle([110, 670, 970, 800], radius=18, fill=(238, 242, 255, 255), outline=(79, 70, 229, 255), width=3)
        draw.rounded_rectangle([135, 695, 215, 775], radius=16, fill=(79, 70, 229, 255))
        draw.text((175, 735), "3", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 715), "MISSING UNIT TESTS & EDGE CASES 🧪", font=FONT_CARD_TITLE, fill=(49, 46, 129, 255), anchor="lm")
        draw.text((245, 762), "AI code likhega, par QA tester tum ho!", font=FONT_CARD_DESC, fill=(67, 56, 202, 255), anchor="lm")

    t_l6_start = schedule["line6_s"]["start"]
    if t >= t_l6_start + 0.3:
        draw.rounded_rectangle([110, 830, 970, 1010], radius=22, fill=(6, 95, 70, 255), outline=(52, 211, 153, 255), width=4)
        draw.text((540, 880), "💡 GOLDEN RULE OF VIBE CODING:", font=FONT_SUB, fill=(167, 243, 208, 255), anchor="mm")
        draw.text((540, 950), "AI = JUNIOR CODER  |  TUM = SENIOR ARCHITECT! 🚀", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255), anchor="mm")

    # Speech state
    junior_speaking = False
    senior_speaking = False
    current_sub = ""
    for sid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"]:
            if sinfo["speaker"] == "junior":
                junior_speaking = True
            else:
                senior_speaking = True
            # Subtitle
            if sid == "line1_j": current_sub = "Junior: 'Bhaiya! AI se 10 min mein app bana diya! Dev kyu chahiye?'"
            elif sid == "line2_s": current_sub = "Senior: 'Ruko bhai! AI code dega, par 3 cheezein crash karwayengi!'"
            elif sid == "line3_s": current_sub = "Senior: 'Pehli galati: Hardcoded API Keys! GitHub pe leak hongi!'"
            elif sid == "line4_s": current_sub = "Senior: 'Dusri: Zero Error Handling! Network error pe screen blank!'"
            elif sid == "line5_j": current_sub = "Junior: 'Arre baap re! Matlab testing humein hi karni padegi?'"
            elif sid == "line6_s": current_sub = "Senior: 'AI tumhara junior coder hai... Senior Architect tum ho!'"
            break
            
    blink = (t % 3.2) < 0.15
    junior_shocked = (schedule["line5_j"]["start"] <= t <= schedule["line5_j"]["end"] + 0.5)

    # 2. JUNIOR CHARACTER
    j_cx, j_cy = 300, 1420
    j_bob = int(math.sin(t * 8.0) * 3) if junior_speaking else int(math.sin(t * 2.0) * 1.5)
    
    # Torso
    draw.polygon([[j_cx - 130, 1560 + j_bob], [j_cx + 130, 1560 + j_bob], [j_cx + 150, 1840], [j_cx - 150, 1840]], fill=(239, 68, 68, 255), outline=(15, 23, 42, 255))
    draw.rounded_rectangle([j_cx - 70, 1720 + j_bob, j_cx + 70, 1820], radius=12, fill=(220, 38, 38, 255), outline=(15, 23, 42, 255), width=2)
    # White strings
    draw.line([j_cx - 20, 1550 + j_bob, j_cx - 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    draw.line([j_cx + 20, 1550 + j_bob, j_cx + 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    
    # Arms
    if junior_shocked:
        draw.line([j_cx - 120, 1580, j_cx - 80, 1460], fill=(239, 68, 68, 255), width=28)
        draw.line([j_cx + 120, 1580, j_cx + 80, 1460], fill=(239, 68, 68, 255), width=28)
        draw.ellipse([j_cx - 95, 1445, j_cx - 65, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 65, 1445, j_cx + 95, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    elif junior_speaking and (schedule["line1_j"]["start"] <= t <= schedule["line1_j"]["end"]):
        hand_lift = int(math.sin(t * 8.0) * 12)
        draw.line([j_cx + 120, 1600, j_cx + 160, 1430 + hand_lift], fill=(239, 68, 68, 255), width=28)
        draw.ellipse([j_cx + 145, 1410 + hand_lift, j_cx + 180, 1445 + hand_lift], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    else:
        draw.line([j_cx - 120, 1590, j_cx - 80, 1720], fill=(239, 68, 68, 255), width=26)
        draw.line([j_cx + 120, 1590, j_cx + 80, 1720], fill=(239, 68, 68, 255), width=26)

    # Head
    draw.rectangle([j_cx - 24, 1510 + j_bob, j_cx + 24, 1555 + j_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    draw.ellipse([j_cx - 100, 1330 + j_bob, j_cx + 100, 1530 + j_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=4)
    # Hair
    draw.polygon([[j_cx - 110, 1380 + j_bob], [j_cx - 120, 1320 + j_bob], [j_cx - 80, 1270 + j_bob],
                  [j_cx + 20, 1260 + j_bob], [j_cx + 90, 1290 + j_bob], [j_cx + 115, 1350 + j_bob],
                  [j_cx + 95, 1395 + j_bob], [j_cx + 60, 1340 + j_bob], [j_cx - 40, 1350 + j_bob]],
                 fill=(15, 23, 42, 255), outline=(15, 23, 42, 255))
                 
    # Eyes
    eye_y = 1420 + j_bob
    if blink:
        draw.line([j_cx - 65, eye_y, j_cx - 35, eye_y], fill=(15, 23, 42, 255), width=4)
        draw.line([j_cx + 35, eye_y, j_cx + 65, eye_y], fill=(15, 23, 42, 255), width=4)
    else:
        draw.ellipse([j_cx - 70, eye_y - 25, j_cx - 30, eye_y + 25], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 30, eye_y - 25, j_cx + 70, eye_y + 25], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx - 52, eye_y - 20, j_cx - 36, eye_y + 8], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx + 48, eye_y - 20, j_cx + 64, eye_y + 8], fill=(15, 23, 42, 255))
        draw.line([j_cx - 68, eye_y - 36, j_cx - 32, eye_y - 42], fill=(15, 23, 42, 255), width=4)
        draw.line([j_cx + 32, eye_y - 42, j_cx + 68, eye_y - 36], fill=(15, 23, 42, 255), width=4)
        
    draw.ellipse([j_cx - 82, eye_y + 20, j_cx - 62, eye_y + 35], fill=(244, 114, 182, 140))
    draw.ellipse([j_cx + 62, eye_y + 20, j_cx + 82, eye_y + 35], fill=(244, 114, 182, 140))

    # Mouth
    m_y = 1485 + j_bob
    if junior_shocked:
        draw.ellipse([j_cx - 18, m_y - 12, j_cx + 18, m_y + 22], fill=(153, 27, 27, 255), outline=(15, 23, 42, 255), width=3)
    elif junior_speaking:
        mouth_open = int(abs(math.sin(t * 22.0)) * 14)
        if mouth_open > 3:
            draw.ellipse([j_cx - 20, m_y - mouth_open, j_cx + 20, m_y + mouth_open], fill=(185, 28, 28, 255), outline=(15, 23, 42, 255), width=3)
            draw.rectangle([j_cx - 12, m_y - mouth_open, j_cx + 12, m_y - mouth_open + 5], fill=(255, 255, 255, 255))
        else:
            draw.line([j_cx - 18, m_y, j_cx + 18, m_y], fill=(15, 23, 42, 255), width=3)
    else:
        draw.arc([j_cx - 20, m_y - 10, j_cx + 20, m_y + 12], 10, 170, fill=(15, 23, 42, 255), width=3)

    # 3. SENIOR CHARACTER
    s_cx, s_cy = 780, 1420
    s_bob = int(math.sin(t * 7.0) * 2.5) if senior_speaking else int(math.sin(t * 1.8) * 1.2)
    
    draw.polygon([[s_cx - 140, 1560 + s_bob], [s_cx + 140, 1560 + s_bob], [s_cx + 160, 1840], [s_cx - 160, 1840]], fill=(248, 250, 252, 255), outline=(15, 23, 42, 255), width=3)
    draw.polygon([[s_cx - 40, 1560 + s_bob], [s_cx + 40, 1560 + s_bob], [s_cx, 1660 + s_bob]], fill=(4, 120, 87, 255), outline=(15, 23, 42, 255), width=2)
    draw.rectangle([s_cx + 60, 1630 + s_bob, s_cx + 90, 1675 + s_bob], fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=2)
    
    # Arm pointing
    arm_point_y = int(math.sin(t * 6.0) * 8) if senior_speaking else 0
    draw.line([s_cx + 130, 1580, s_cx + 150, 1740], fill=(248, 250, 252, 255), width=28)
    draw.line([s_cx - 110, 1580, s_cx - 170, 1240 + arm_point_y], fill=(248, 250, 252, 255), width=30)
    draw.ellipse([s_cx - 185, 1215 + arm_point_y, s_cx - 155, 1250 + arm_point_y], fill=(217, 119, 6, 255), outline=(15, 23, 42, 255), width=3)
    draw.line([s_cx - 170, 1225 + arm_point_y, s_cx - 190, 1180 + arm_point_y], fill=(217, 119, 6, 255), width=10)

    # Head
    draw.rectangle([s_cx - 26, 1505 + s_bob, s_cx + 26, 1555 + s_bob], fill=(245, 158, 11, 255), outline=(15, 23, 42, 255), width=3)
    draw.ellipse([s_cx - 100, 1320 + s_bob, s_cx + 100, 1525 + s_bob], fill=(245, 158, 11, 255), outline=(15, 23, 42, 255), width=4)
    # Beard
    draw.polygon([[s_cx - 85, 1435 + s_bob], [s_cx - 95, 1495 + s_bob], [s_cx - 50, 1540 + s_bob],
                  [s_cx + 50, 1540 + s_bob], [s_cx + 95, 1495 + s_bob], [s_cx + 85, 1435 + s_bob],
                  [s_cx + 60, 1475 + s_bob], [s_cx - 60, 1475 + s_bob]],
                 fill=(30, 41, 59, 255), outline=(15, 23, 42, 255))
    # Hair
    draw.polygon([[s_cx - 105, 1370 + s_bob], [s_cx - 110, 1300 + s_bob], [s_cx - 50, 1260 + s_bob],
                  [s_cx + 50, 1260 + s_bob], [s_cx + 110, 1300 + s_bob], [s_cx + 105, 1370 + s_bob],
                  [s_cx + 70, 1315 + s_bob], [s_cx - 60, 1315 + s_bob]],
                 fill=(30, 41, 59, 255), outline=(15, 23, 42, 255))
                 
    # Glasses
    s_eye_y = 1400 + s_bob
    draw.rounded_rectangle([s_cx - 80, s_eye_y - 20, s_cx - 15, s_eye_y + 20], radius=8, fill=(255, 255, 255, 200), outline=(15, 23, 42, 255), width=4)
    draw.rounded_rectangle([s_cx + 15, s_eye_y - 20, s_cx + 80, s_eye_y + 20], radius=8, fill=(255, 255, 255, 200), outline=(15, 23, 42, 255), width=4)
    draw.line([s_cx - 15, s_eye_y, s_cx + 15, s_eye_y], fill=(15, 23, 42, 255), width=4)
    
    if blink:
        draw.line([s_cx - 65, s_eye_y, s_cx - 30, s_eye_y], fill=(15, 23, 42, 255), width=4)
        draw.line([s_cx + 30, s_eye_y, s_cx + 65, s_eye_y], fill=(15, 23, 42, 255), width=4)
    else:
        draw.ellipse([s_cx - 58, s_eye_y - 12, s_cx - 36, s_eye_y + 12], fill=(15, 23, 42, 255))
        draw.ellipse([s_cx + 36, s_eye_y - 12, s_cx + 58, s_eye_y + 12], fill=(15, 23, 42, 255))
        
    sm_y = 1485 + s_bob
    if senior_speaking:
        s_mouth_open = int(abs(math.sin(t * 20.0)) * 12)
        if s_mouth_open > 3:
            draw.ellipse([s_cx - 20, sm_y - s_mouth_open, s_cx + 20, sm_y + s_mouth_open], fill=(153, 27, 27, 255), outline=(15, 23, 42, 255), width=3)
            draw.rectangle([s_cx - 14, sm_y - s_mouth_open, s_cx + 14, sm_y - s_mouth_open + 4], fill=(255, 255, 255, 255))
        else:
            draw.line([s_cx - 18, sm_y, s_cx + 18, sm_y], fill=(15, 23, 42, 255), width=3)
    else:
        draw.arc([s_cx - 20, sm_y - 8, s_cx + 20, sm_y + 10], 10, 170, fill=(15, 23, 42, 255), width=3)

    # 4. SUBTITLES
    if current_sub:
        draw.rounded_rectangle([60, 1765, 1020, 1845], radius=18, fill=(15, 23, 42, 230))
        draw.text((540, 1805), current_sub, font=FONT_CAPTION, fill=(255, 255, 255, 255), anchor="mm")
        
    return im.convert("RGB")

def render_video_stream(schedule, total_dur):
    fps = 30
    total_f = int(total_dur * fps)
    print(f"--- [2/4] Streaming {total_f} Frames @ {fps}fps to FFmpeg ({total_dur:.2f}s) ---")
    raw_video = os.path.join(WORK_DIR, "fast_video_track.mp4")
    
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
        im = draw_frame(f_idx, fps, schedule, total_dur)
        proc.stdin.write(im.tobytes())
        if f_idx % 120 == 0:
            print(f"Frame {f_idx}/{total_f} ({f_idx/total_f*100:.1f}%)")
            
    proc.stdin.close()
    proc.wait()
    print("Fast video stream rendered successfully:", raw_video)
    return raw_video

def mix_fast_audio(schedule, total_dur):
    print("--- [3/4] Multi-Track Broadcast Audio Mixing ---")
    l1 = os.path.join(AUDIO_DIR, "line1_j.wav")
    l2 = os.path.join(AUDIO_DIR, "line2_s.wav")
    l3 = os.path.join(AUDIO_DIR, "line3_s.wav")
    l4 = os.path.join(AUDIO_DIR, "line4_s.wav")
    l5 = os.path.join(AUDIO_DIR, "line5_j.wav")
    l6 = os.path.join(AUDIO_DIR, "line6_s.wav")
    
    sfx_pop = os.path.join(WORK_DIR, "sfx_pop.wav")
    sfx_scratch = os.path.join(WORK_DIR, "sfx_scratch.wav")
    
    # Background lofi beat
    bgm_path = os.path.join(WORK_DIR, "bgm_fast_lofi.wav")
    cmd_bgm = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"sine=f=261.63:d={total_dur},volume=0.06",
        "-f", "lavfi",
        "-i", f"sine=f=329.63:d={total_dur},volume=0.04",
        "-f", "lavfi",
        "-i", f"sine=f=392.00:d={total_dur},volume=0.04",
        "-f", "lavfi",
        "-i", f"anoisesrc=d={total_dur}:c=brown:r=44100,lowpass=f=220,volume=0.1",
        "-filter_complex", f"[0:a][1:a][2:a][3:a]amix=inputs=4[m];[m]afade=t=out:st={total_dur-1.2:.2f}:d=1.2[out]",
        "-map", "[out]", bgm_path
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    d1 = int(schedule["line1_j"]["start"] * 1000)
    d2 = int(schedule["line2_s"]["start"] * 1000)
    d3 = int(schedule["line3_s"]["start"] * 1000)
    d4 = int(schedule["line4_s"]["start"] * 1000)
    d5 = int(schedule["line5_j"]["start"] * 1000)
    d6 = int(schedule["line6_s"]["start"] * 1000)
    
    d_scratch = int((schedule["line2_s"]["start"] + 0.6) * 1000)
    d_p1 = int((schedule["line3_s"]["start"] + 0.2) * 1000)
    d_p2 = int((schedule["line4_s"]["start"] + 0.2) * 1000)
    d_p3 = int((schedule["line5_j"]["start"]) * 1000)
    
    mix_filter = (
        f"[0:a]adelay={d1}|{d1},volume=1.5[a0];"
        f"[1:a]adelay={d2}|{d2},volume=1.5[a1];"
        f"[2:a]adelay={d3}|{d3},volume=1.5[a2];"
        f"[3:a]adelay={d4}|{d4},volume=1.5[a3];"
        f"[4:a]adelay={d5}|{d5},volume=1.5[a4];"
        f"[5:a]adelay={d6}|{d6},volume=1.5[a5];"
        f"[6:a]volume=0.25[a6];"
        f"[7:a]adelay={d_scratch}|{d_scratch},volume=0.45[a7];"
        f"[8:a]adelay={d_p1}|{d_p1},volume=0.55[a8];"
        f"[9:a]adelay={d_p2}|{d_p2},volume=0.55[a9];"
        f"[10:a]adelay={d_p3}|{d_p3},volume=0.55[a10];"
        f"[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10]amix=inputs=11:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1.0[final_audio]"
    )
    
    final_audio = os.path.join(WORK_DIR, "fast_final_audio.wav")
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

def compile_fast_mp4(v_track, a_track, total_dur):
    print("--- [4/4] Assembling Final High-Energy MP4 ---")
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
    print(f"\n🎉 FAST HUMAN-ENERGY REEL READY: {OUTPUT_MP4}")
    print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")

async def main():
    durs = await prepare_fast_audio()
    schedule, total_dur = build_timeline(durs)
    print(f"Total Video Planned Duration: {total_dur:.2f}s")
    v_track = render_video_stream(schedule, total_dur)
    a_track = mix_fast_audio(schedule, total_dur)
    compile_fast_mp4(v_track, a_track, total_dur)

if __name__ == "__main__":
    asyncio.run(main())
