"""
Master AI - Two-Character Whiteboard Explainer Reel Engine
Recreates the exact viral Instagram Reel format from ref_04 / ref_03:
- Top 60%: Interactive Whiteboard with dynamic point reveals, markers & strike-throughs
- Bottom 40%: Two animated talking 2D characters (Junior in Red Hoodie + Senior Mentor in Lab Coat)
- Real 2D puppet animation: Lip-sync mouth flap, eye blinking, pointing arm gestures, shocked head-grab
- Full sound design: Edge-TTS dialogue, marker scribble, pops, chimes, and lofi beat
"""

import os
import sys
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
WORK_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
OUTPUT_MP4 = os.path.join(WORK_DIR, "vibe_coding_explainer_master.mp4")

# Load dialogue durations
def get_dur(wav_file):
    cmd = [FFMPEG, "-i", wav_file]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            pts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(pts[0])*3600 + float(pts[1])*60 + float(pts[2])
    return 5.0

d1 = get_dur(os.path.join(AUDIO_DIR, "line1_junior.wav"))
d2 = get_dur(os.path.join(AUDIO_DIR, "line2_senior.wav"))
d3 = get_dur(os.path.join(AUDIO_DIR, "line3_senior.wav"))
d4 = get_dur(os.path.join(AUDIO_DIR, "line4_senior.wav"))
d5 = get_dur(os.path.join(AUDIO_DIR, "line5_junior.wav"))
d6 = get_dur(os.path.join(AUDIO_DIR, "line6_senior.wav"))

# Exact timeline schedule (with 0.15s gap between turns)
gap = 0.15
t_line1_start = 0.4
t_line1_end = t_line1_start + d1

t_line2_start = t_line1_end + gap
t_line2_end = t_line2_start + d2

t_line3_start = t_line2_end + gap
t_line3_end = t_line3_start + d3

t_line4_start = t_line3_end + gap
t_line4_end = t_line4_start + d4

t_line5_start = t_line4_end + gap
t_line5_end = t_line5_start + d5

t_line6_start = t_line5_end + gap
t_line6_end = t_line6_start + d6

total_duration = t_line6_end + 1.2
fps = 30
total_frames = int(total_duration * fps)

print(f"Timeline: Total Duration = {total_duration:.2f}s ({total_frames} frames @ 30fps)")

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 36)
FONT_CARD_DESC = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)

def draw_frame(frame_idx):
    t = frame_idx / fps
    w, h = 1080, 1920
    im = Image.new("RGBA", (w, h), (224, 242, 254, 255)) # Soft pastel sky background (#E0F2FE)
    draw = ImageDraw.Draw(im)
    
    # Subtle floor separator line at Y: 1840
    draw.rectangle([0, 1840, w, h], fill=(186, 230, 253, 255))
    draw.line([0, 1840, w, 1840], fill=(125, 211, 252, 255), width=3)
    
    # -------------------------------------------------------------
    # 1. TOP WHITEBOARD (Y: 90 to 1090)
    # -------------------------------------------------------------
    # Whiteboard Outer Shadow & Metallic Frame
    draw.rounded_rectangle([72, 92, 1008, 1078], radius=28, fill=(148, 163, 184, 180)) # shadow
    draw.rounded_rectangle([70, 90, 1010, 1070], radius=26, fill=(241, 245, 249, 255), outline=(30, 41, 59, 255), width=8) # frame
    # Inner White Surface
    draw.rounded_rectangle([86, 106, 994, 1030], radius=18, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=3)
    
    # Pen Tray at bottom of whiteboard
    draw.rounded_rectangle([250, 1056, 830, 1072], radius=6, fill=(71, 85, 105, 255), outline=(15, 23, 42, 255), width=2)
    # Red, Black, Blue Marker Caps in tray
    draw.rounded_rectangle([320, 1050, 360, 1062], radius=3, fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([380, 1050, 420, 1062], radius=3, fill=(15, 23, 42, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([440, 1050, 480, 1062], radius=3, fill=(2, 132, 199, 255), outline=(15, 23, 42, 255), width=1)
    
    # Whiteboard Header: Main Title
    # Card Pill for Header
    draw.rounded_rectangle([100, 125, 980, 210], radius=18, fill=(15, 23, 42, 255))
    draw.text((540, 168), "AI CODING KI 3 SABSE BADI GALATIYAN! ⚠️", font=FONT_TITLE, fill=(255, 255, 255, 255), anchor="mm")
    
    # Sub-header Hook Card (Initial Premise)
    draw.rounded_rectangle([120, 230, 960, 315], radius=16, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=3)
    draw.text((540, 272), "VIBE CODING: KYA AB DEV KI ZAROORAT NAHI? 🚀", font=FONT_SUB, fill=(30, 41, 59, 255), anchor="mm")
    
    # Animated Red Strike-Through over "KYA AB DEV KI ZAROORAT NAHI?"
    if t >= t_line2_start + 1.0:
        strike_progress = min(1.0, (t - (t_line2_start + 1.0)) / 0.8)
        start_x = 160
        end_x = start_x + int(strike_progress * 760)
        draw.line([start_x, 272, end_x, 272], fill=(239, 68, 68, 255), width=10)
        
        # Red Stamp [ NAHI! CRASH HOGA! ]
        if strike_progress >= 0.8:
            draw.rounded_rectangle([730, 236, 940, 308], radius=12, fill=(239, 68, 68, 255))
            draw.text((835, 272), "NAHI! ❌", font=FONT_SUB, fill=(255, 255, 255, 255), anchor="mm")
            
    # POINT 1 (Appears during Line 3)
    if t >= t_line3_start + 0.3:
        p1_anim = min(1.0, (t - (t_line3_start + 0.3)) / 0.5)
        y_pos = int(350 + (1.0 - p1_anim) * 15)
        # Background card
        draw.rounded_rectangle([110, y_pos, 970, y_pos + 130], radius=18, fill=(254, 242, 242, 255), outline=(239, 68, 68, 255), width=3)
        # Badge [1]
        draw.rounded_rectangle([135, y_pos + 25, 215, y_pos + 105], radius=16, fill=(239, 68, 68, 255))
        draw.text((175, y_pos + 65), "1", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        # Text
        draw.text((245, y_pos + 45), "HARDCODED API KEYS & SECRETS 🔑", font=FONT_CARD_TITLE, fill=(153, 27, 27, 255), anchor="lm")
        draw.text((245, y_pos + 92), "Code directly public GitHub pe leak ho jata hai!", font=FONT_CARD_DESC, fill=(185, 28, 28, 255), anchor="lm")
        
    # POINT 2 (Appears during Line 4)
    if t >= t_line4_start + 0.3:
        p2_anim = min(1.0, (t - (t_line4_start + 0.3)) / 0.5)
        y_pos = int(510 + (1.0 - p2_anim) * 15)
        draw.rounded_rectangle([110, y_pos, 970, y_pos + 130], radius=18, fill=(255, 247, 237, 255), outline=(249, 115, 22, 255), width=3)
        draw.rounded_rectangle([135, y_pos + 25, 215, y_pos + 105], radius=16, fill=(249, 115, 22, 255))
        draw.text((175, y_pos + 65), "2", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, y_pos + 45), "ZERO ERROR HANDLING & TRY-CATCH 🛑", font=FONT_CARD_TITLE, fill=(154, 52, 18, 255), anchor="lm")
        draw.text((245, y_pos + 92), "Ek network error aate hi screen blank ho jati hai!", font=FONT_CARD_DESC, fill=(194, 65, 12, 255), anchor="lm")

    # POINT 3 (Appears during Line 5)
    if t >= t_line5_start + 0.2:
        p3_anim = min(1.0, (t - (t_line5_start + 0.2)) / 0.5)
        y_pos = int(670 + (1.0 - p3_anim) * 15)
        draw.rounded_rectangle([110, y_pos, 970, y_pos + 130], radius=18, fill=(238, 242, 255, 255), outline=(79, 70, 229, 255), width=3)
        draw.rounded_rectangle([135, y_pos + 25, 215, y_pos + 105], radius=16, fill=(79, 70, 229, 255))
        draw.text((175, y_pos + 65), "3", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, y_pos + 45), "MISSING UNIT TESTS & EDGE CASES 🧪", font=FONT_CARD_TITLE, fill=(49, 46, 129, 255), anchor="lm")
        draw.text((245, y_pos + 92), "AI code likhega, par QA tester tum ho!", font=FONT_CARD_DESC, fill=(67, 56, 202, 255), anchor="lm")

    # FINAL TAKEAWAY CARD (Line 6)
    if t >= t_line6_start + 0.5:
        draw.rounded_rectangle([110, 830, 970, 1010], radius=22, fill=(6, 95, 70, 255), outline=(52, 211, 153, 255), width=4)
        draw.text((540, 880), "💡 GOLDEN RULE OF VIBE CODING:", font=FONT_SUB, fill=(167, 243, 208, 255), anchor="mm")
        draw.text((540, 950), "AI = JUNIOR CODER  |  TUM = SENIOR ARCHITECT! 🚀", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255), anchor="mm")

    # -------------------------------------------------------------
    # 2. DIALOGUE & SPEECH STATE CALCULATION
    # -------------------------------------------------------------
    # Determine who is speaking
    junior_speaking = (t_line1_start <= t <= t_line1_end) or (t_line5_start <= t <= t_line5_end)
    senior_speaking = (t_line2_start <= t <= t_line2_end) or (t_line3_start <= t <= t_line3_end) or \
                      (t_line4_start <= t <= t_line4_end) or (t_line6_start <= t <= t_line6_end)
                      
    # Eye blinking cycle (blink every 3.5 seconds for 0.15s)
    blink = (t % 3.5) < 0.16
    
    # Junior shocked state during Line 5
    junior_shocked = (t_line5_start <= t <= t_line5_end + 0.8)

    # -------------------------------------------------------------
    # 3. BOTTOM-LEFT CHARACTER: JUNIOR (ARYAN)
    # Staged around X: 140 to 460, Y: 1150 to 1840
    # -------------------------------------------------------------
    j_cx, j_cy = 300, 1420
    j_bob = int(math.sin(t * 5.0) * 3) if junior_speaking else int(math.sin(t * 2.0) * 1.5)
    
    # Red Hoodie Torso (#EF4444)
    draw.polygon([[j_cx - 130, 1560 + j_bob], [j_cx + 130, 1560 + j_bob], 
                  [j_cx + 150, 1840], [j_cx - 150, 1840]], fill=(239, 68, 68, 255), outline=(15, 23, 42, 255))
    # Hoodie Pocket
    draw.rounded_rectangle([j_cx - 70, 1720 + j_bob, j_cx + 70, 1820], radius=12, fill=(220, 38, 38, 255), outline=(15, 23, 42, 255), width=2)
    # White Drawstrings
    draw.line([j_cx - 20, 1550 + j_bob, j_cx - 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    draw.line([j_cx + 20, 1550 + j_bob, j_cx + 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    draw.ellipse([j_cx - 24, 1630 + j_bob, j_cx - 16, 1638 + j_bob], fill=(203, 213, 225, 255))
    draw.ellipse([j_cx + 16, 1630 + j_bob, j_cx + 24, 1638 + j_bob], fill=(203, 213, 225, 255))

    # Junior Arm Gestures:
    if junior_shocked:
        # Hands up clutching cheeks in shock!
        draw.line([j_cx - 120, 1580, j_cx - 80, 1460], fill=(239, 68, 68, 255), width=28)
        draw.line([j_cx + 120, 1580, j_cx + 80, 1460], fill=(239, 68, 68, 255), width=28)
        draw.ellipse([j_cx - 95, 1445, j_cx - 65, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 65, 1445, j_cx + 95, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    elif junior_speaking and (t_line1_start <= t <= t_line1_end):
        # Hand raised with raised thumb/palm questioning
        hand_lift = int(math.sin(t * 6.0) * 12)
        draw.line([j_cx + 120, 1600, j_cx + 160, 1430 + hand_lift], fill=(239, 68, 68, 255), width=28)
        draw.ellipse([j_cx + 145, 1410 + hand_lift, j_cx + 180, 1445 + hand_lift], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    else:
        # Resting hands in pockets
        draw.line([j_cx - 120, 1590, j_cx - 80, 1720], fill=(239, 68, 68, 255), width=26)
        draw.line([j_cx + 120, 1590, j_cx + 80, 1720], fill=(239, 68, 68, 255), width=26)
        
    # Junior Neck
    draw.rectangle([j_cx - 24, 1510 + j_bob, j_cx + 24, 1555 + j_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    
    # Junior Head (Circ: 110 radius)
    draw.ellipse([j_cx - 100, 1330 + j_bob, j_cx + 100, 1530 + j_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=4)
    # Hair: Modern voluminous dark mop (#0F172A)
    draw.polygon([[j_cx - 110, 1380 + j_bob], [j_cx - 120, 1320 + j_bob], [j_cx - 80, 1270 + j_bob],
                  [j_cx + 20, 1260 + j_bob], [j_cx + 90, 1290 + j_bob], [j_cx + 115, 1350 + j_bob],
                  [j_cx + 95, 1395 + j_bob], [j_cx + 60, 1340 + j_bob], [j_cx - 40, 1350 + j_bob]],
                 fill=(15, 23, 42, 255), outline=(15, 23, 42, 255))
                 
    # Junior Eyes:
    eye_y = 1420 + j_bob
    if blink:
        # Closed eye line
        draw.line([j_cx - 65, eye_y, j_cx - 35, eye_y], fill=(15, 23, 42, 255), width=4)
        draw.line([j_cx + 35, eye_y, j_cx + 65, eye_y], fill=(15, 23, 42, 255), width=4)
    else:
        # Big expressive round eyes looking up-right at whiteboard
        draw.ellipse([j_cx - 70, eye_y - 25, j_cx - 30, eye_y + 25], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 30, eye_y - 25, j_cx + 70, eye_y + 25], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        # Pupils looking up-right towards senior & whiteboard
        draw.ellipse([j_cx - 52, eye_y - 20, j_cx - 36, eye_y + 8], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx + 48, eye_y - 20, j_cx + 64, eye_y + 8], fill=(15, 23, 42, 255))
        # Eyebrows
        draw.line([j_cx - 68, eye_y - 36, j_cx - 32, eye_y - 42], fill=(15, 23, 42, 255), width=4)
        draw.line([j_cx + 32, eye_y - 42, j_cx + 68, eye_y - 36], fill=(15, 23, 42, 255), width=4)
        
    # Rosy Cheeks
    draw.ellipse([j_cx - 82, eye_y + 20, j_cx - 62, eye_y + 35], fill=(244, 114, 182, 140))
    draw.ellipse([j_cx + 62, eye_y + 20, j_cx + 82, eye_y + 35], fill=(244, 114, 182, 140))

    # Junior Mouth Animation (Lip-sync):
    m_y = 1485 + j_bob
    if junior_shocked:
        # Large shocked 'O' mouth
        draw.ellipse([j_cx - 18, m_y - 12, j_cx + 18, m_y + 22], fill=(153, 27, 27, 255), outline=(15, 23, 42, 255), width=3)
    elif junior_speaking:
        # Mouth flapping with audio sine
        mouth_open = int(abs(math.sin(t * 18.0)) * 14)
        if mouth_open > 3:
            draw.ellipse([j_cx - 20, m_y - mouth_open, j_cx + 20, m_y + mouth_open], fill=(185, 28, 28, 255), outline=(15, 23, 42, 255), width=3)
            # Teeth
            draw.rectangle([j_cx - 12, m_y - mouth_open, j_cx + 12, m_y - mouth_open + 5], fill=(255, 255, 255, 255))
        else:
            draw.line([j_cx - 18, m_y, j_cx + 18, m_y], fill=(15, 23, 42, 255), width=3)
    else:
        # Resting smile
        draw.arc([j_cx - 20, m_y - 10, j_cx + 20, m_y + 12], 10, 170, fill=(15, 23, 42, 255), width=3)

    # -------------------------------------------------------------
    # 4. BOTTOM-RIGHT CHARACTER: SENIOR MENTOR (VIKRAM)
    # Staged around X: 640 to 960, Y: 1150 to 1840
    # -------------------------------------------------------------
    s_cx, s_cy = 780, 1420
    s_bob = int(math.sin(t * 4.5) * 2.5) if senior_speaking else int(math.sin(t * 1.8) * 1.2)
    
    # Lab Coat / Doctor Coat (#F8FAFC) over Emerald Green Shirt (#047857)
    draw.polygon([[s_cx - 140, 1560 + s_bob], [s_cx + 140, 1560 + s_bob],
                  [s_cx + 160, 1840], [s_cx - 160, 1840]], fill=(248, 250, 252, 255), outline=(15, 23, 42, 255), width=3)
    # Emerald Inner Shirt V-neck
    draw.polygon([[s_cx - 40, 1560 + s_bob], [s_cx + 40, 1560 + s_bob],
                  [s_cx, 1660 + s_bob]], fill=(4, 120, 87, 255), outline=(15, 23, 42, 255), width=2)
    # Red Pocket Pen / Badge
    draw.rectangle([s_cx + 60, 1630 + s_bob, s_cx + 90, 1675 + s_bob], fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=2)
    
    # Senior Arm Gestures (Pointing up at Whiteboard):
    arm_point_y = int(math.sin(t * 4.0) * 8) if senior_speaking else 0
    # Left arm resting
    draw.line([s_cx + 130, 1580, s_cx + 150, 1740], fill=(248, 250, 252, 255), width=28)
    # Right arm raised pointing up towards whiteboard (X: 580, Y: 1100)
    draw.line([s_cx - 110, 1580, s_cx - 170, 1240 + arm_point_y], fill=(248, 250, 252, 255), width=30)
    # Pointing Hand with extended index finger
    draw.ellipse([s_cx - 185, 1215 + arm_point_y, s_cx - 155, 1250 + arm_point_y], fill=(217, 119, 6, 255), outline=(15, 23, 42, 255), width=3)
    draw.line([s_cx - 170, 1225 + arm_point_y, s_cx - 190, 1180 + arm_point_y], fill=(217, 119, 6, 255), width=10) # pointing finger!

    # Senior Neck
    draw.rectangle([s_cx - 26, 1505 + s_bob, s_cx + 26, 1555 + s_bob], fill=(245, 158, 11, 255), outline=(15, 23, 42, 255), width=3)

    # Senior Head
    draw.ellipse([s_cx - 100, 1320 + s_bob, s_cx + 100, 1525 + s_bob], fill=(245, 158, 11, 255), outline=(15, 23, 42, 255), width=4)
    # Dark Trimmed Beard (#1E293B)
    draw.polygon([[s_cx - 85, 1435 + s_bob], [s_cx - 95, 1495 + s_bob], [s_cx - 50, 1540 + s_bob],
                  [s_cx + 50, 1540 + s_bob], [s_cx + 95, 1495 + s_bob], [s_cx + 85, 1435 + s_bob],
                  [s_cx + 60, 1475 + s_bob], [s_cx - 60, 1475 + s_bob]],
                 fill=(30, 41, 59, 255), outline=(15, 23, 42, 255))
    # Hair: Short neat side-part with gray streak
    draw.polygon([[s_cx - 105, 1370 + s_bob], [s_cx - 110, 1300 + s_bob], [s_cx - 50, 1260 + s_bob],
                  [s_cx + 50, 1260 + s_bob], [s_cx + 110, 1300 + s_bob], [s_cx + 105, 1370 + s_bob],
                  [s_cx + 70, 1315 + s_bob], [s_cx - 60, 1315 + s_bob]],
                 fill=(30, 41, 59, 255), outline=(15, 23, 42, 255))
                 
    # Senior Rectangular Eyeglasses (#0F172A frames)
    s_eye_y = 1400 + s_bob
    draw.rounded_rectangle([s_cx - 80, s_eye_y - 20, s_cx - 15, s_eye_y + 20], radius=8, fill=(255, 255, 255, 200), outline=(15, 23, 42, 255), width=4)
    draw.rounded_rectangle([s_cx + 15, s_eye_y - 20, s_cx + 80, s_eye_y + 20], radius=8, fill=(255, 255, 255, 200), outline=(15, 23, 42, 255), width=4)
    draw.line([s_cx - 15, s_eye_y, s_cx + 15, s_eye_y], fill=(15, 23, 42, 255), width=4) # bridge
    
    # Senior Eyes inside glasses
    if blink:
        draw.line([s_cx - 65, s_eye_y, s_cx - 30, s_eye_y], fill=(15, 23, 42, 255), width=4)
        draw.line([s_cx + 30, s_eye_y, s_cx + 65, s_eye_y], fill=(15, 23, 42, 255), width=4)
    else:
        draw.ellipse([s_cx - 58, s_eye_y - 12, s_cx - 36, s_eye_y + 12], fill=(15, 23, 42, 255))
        draw.ellipse([s_cx + 36, s_eye_y - 12, s_cx + 58, s_eye_y + 12], fill=(15, 23, 42, 255))
        
    # Senior Mouth Animation (Lip-sync):
    sm_y = 1485 + s_bob
    if senior_speaking:
        s_mouth_open = int(abs(math.sin(t * 16.0)) * 12)
        if s_mouth_open > 3:
            draw.ellipse([s_cx - 20, sm_y - s_mouth_open, s_cx + 20, sm_y + s_mouth_open], fill=(153, 27, 27, 255), outline=(15, 23, 42, 255), width=3)
            draw.rectangle([s_cx - 14, sm_y - s_mouth_open, s_cx + 14, sm_y - s_mouth_open + 4], fill=(255, 255, 255, 255))
        else:
            draw.line([s_cx - 18, sm_y, s_cx + 18, sm_y], fill=(15, 23, 42, 255), width=3)
    else:
        draw.arc([s_cx - 20, sm_y - 8, s_cx + 20, sm_y + 10], 10, 170, fill=(15, 23, 42, 255), width=3)

    # -------------------------------------------------------------
    # 5. SUBTITLE SAFE ZONE (Y: 1780 to 1840)
    # -------------------------------------------------------------
    current_sub = ""
    if t_line1_start <= t <= t_line1_end:
        current_sub = "Junior: 'Bhaiya! Maine AI se 10 min mein app bana diya! Dev nahi chahiye!'"
    elif t_line2_start <= t <= t_line2_end:
        current_sub = "Senior: 'Ruko beta! AI code deta hai, par ye 3 galatiyan crash karwaengi!'"
    elif t_line3_start <= t <= t_line3_end:
        current_sub = "Senior: 'Pehli galati: Hardcoded API Keys! GitHub pe leak ho jati hain!'"
    elif t_line4_start <= t <= t_line4_end:
        current_sub = "Senior: 'Dusri: Zero Error Handling! Ek error pe screen poori blank!'"
    elif t_line5_start <= t <= t_line5_end:
        current_sub = "Junior: 'Arre baap re! Matlab testing humein hi karni padegi?'"
    elif t_line6_start <= t <= t_line6_end:
        current_sub = "Senior: 'AI tumhara junior coder hai... Senior Architect tum ho!'"

    if current_sub:
        draw.rounded_rectangle([60, 1765, 1020, 1845], radius=18, fill=(15, 23, 42, 230))
        draw.text((540, 1805), current_sub, font=FONT_CAPTION, fill=(255, 255, 255, 255), anchor="mm")
        
    return im.convert("RGB")

def render_and_stream_video():
    print(f"--- Starting Video Pipe Stream: {total_frames} frames ---")
    raw_video = os.path.join(WORK_DIR, "whiteboard_video_track.mp4")
    
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
    
    for f_idx in range(total_frames):
        im = draw_frame(f_idx)
        proc.stdin.write(im.tobytes())
        if f_idx % 90 == 0:
            print(f"Rendered frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)")
            
    proc.stdin.close()
    proc.wait()
    print("Video track compiled successfully:", raw_video)
    return raw_video

def assemble_master_audio():
    print("--- Assembling Master Audio Track with SFX & Background Music ---")
    # Generates exact audio tracks
    l1 = os.path.join(AUDIO_DIR, "line1_junior.wav")
    l2 = os.path.join(AUDIO_DIR, "line2_senior.wav")
    l3 = os.path.join(AUDIO_DIR, "line3_senior.wav")
    l4 = os.path.join(AUDIO_DIR, "line4_senior.wav")
    l5 = os.path.join(AUDIO_DIR, "line5_junior.wav")
    l6 = os.path.join(AUDIO_DIR, "line6_senior.wav")
    
    # Sound Effects:
    # 1. Pop chime on points (sine 880Hz -> 1320Hz)
    sfx_pop = os.path.join(WORK_DIR, "sfx_pop.wav")
    cmd_pop = [FFMPEG, "-y", "-f", "lavfi", "-i", "sine=f=1046:d=0.18,afade=t=out:st=0.04:d=0.14,volume=0.4", sfx_pop]
    subprocess.run(cmd_pop, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 2. Marker strike scratch sound
    sfx_scratch = os.path.join(WORK_DIR, "sfx_scratch.wav")
    cmd_scratch = [FFMPEG, "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.7:c=pink:r=44100,lowpass=f=1800,volume=0.35,afade=t=out:st=0.5:d=0.2", sfx_scratch]
    subprocess.run(cmd_scratch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 3. Ambient Lofi Background Beat (44s loop)
    bgm_path = os.path.join(WORK_DIR, "bgm_lofi.wav")
    cmd_bgm = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"sine=f=261.63:d={total_duration},volume=0.06",
        "-f", "lavfi",
        "-i", f"sine=f=329.63:d={total_duration},volume=0.04",
        "-f", "lavfi",
        "-i", f"sine=f=392.00:d={total_duration},volume=0.04",
        "-f", "lavfi",
        "-i", f"anoisesrc=d={total_duration}:c=brown:r=44100,lowpass=f=220,volume=0.1",
        "-filter_complex", f"[0:a][1:a][2:a][3:a]amix=inputs=4[m];[m]afade=t=out:st={total_duration-1.5:.2f}:d=1.5[out]",
        "-map", "[out]", bgm_path
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Assemble with adelay & amix
    d_l1 = int(t_line1_start * 1000)
    d_l2 = int(t_line2_start * 1000)
    d_l3 = int(t_line3_start * 1000)
    d_l4 = int(t_line4_start * 1000)
    d_l5 = int(t_line5_start * 1000)
    d_l6 = int(t_line6_start * 1000)
    d_scratch = int((t_line2_start + 1.0) * 1000)
    d_pop1 = int((t_line3_start + 0.3) * 1000)
    d_pop2 = int((t_line4_start + 0.3) * 1000)
    d_pop3 = int((t_line5_start + 0.2) * 1000)
    
    mix_filter = (
        f"[0:a]adelay={d_l1}|{d_l1},volume=1.4[a0];"
        f"[1:a]adelay={d_l2}|{d_l2},volume=1.5[a1];"
        f"[2:a]adelay={d_l3}|{d_l3},volume=1.5[a2];"
        f"[3:a]adelay={d_l4}|{d_l4},volume=1.5[a3];"
        f"[4:a]adelay={d_l5}|{d_l5},volume=1.4[a4];"
        f"[5:a]adelay={d_l6}|{d_l6},volume=1.5[a5];"
        f"[6:a]volume=0.3[a6];"
        f"[7:a]adelay={d_scratch}|{d_scratch},volume=0.5[a7];"
        f"[8:a]adelay={d_pop1}|{d_pop1},volume=0.6[a8];"
        f"[9:a]adelay={d_pop2}|{d_pop2},volume=0.6[a9];"
        f"[10:a]adelay={d_pop3}|{d_pop3},volume=0.6[a10];"
        f"[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10]amix=inputs=11:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1.0[final_audio]"
    )
    
    final_audio = os.path.join(WORK_DIR, "whiteboard_final_audio.wav")
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
        "-t", str(total_duration),
        final_audio
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("Master audio mix compiled:", final_audio)
    return final_audio

def compile_final_mp4(raw_video, final_audio):
    print("--- Compiling Final Master MP4 ---")
    cmd = [
        FFMPEG, "-y",
        "-i", raw_video,
        "-i", final_audio,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_duration),
        OUTPUT_MP4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n🎉 EXPLAINER REEL MASTER COMPLETED: {OUTPUT_MP4}")
    print(f"Duration: {total_duration:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")

if __name__ == "__main__":
    v_track = render_and_stream_video()
    a_track = assemble_master_audio()
    compile_final_mp4(v_track, a_track)
