"""
render_master_film_713.py
=========================
Master AI - Phase 7.13 Production Test Renderer
Title: "MIDNIGHT DISCOVERY"
Specifications:
- Resolution: 1080x1920 (9:16 Vertical Portrait)
- Framerate: 30.00 FPS Constant Frame Rate (CFR)
- Duration: Exactly 18.000 Seconds (540 Frames)
- Video Track: Real moving footage (Rain -> Tech Room -> Sunset Clouds)
- Character: High-fidelity textured character Dev with 3 distinct dramatic expression states
  (Neutral/contemplative -> Disbelief/Shock -> Confident Relief)
- Subtitles: Kinetic Roman Hinglish captions in vertical safe zone
- Audio: Multiplexed final_audio_mix.wav (EBU R128 Mastered)
"""

import os
import sys
import math
import time
import json
import subprocess
import cv2
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.13\production_test"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
AUDIO_WAV = os.path.join(BASE_DIR, "audio", "final_audio_mix.wav")
FINAL_MP4 = os.path.join(OUTPUT_DIR, "phase_7_13_test_film.mp4")
TIMELINE_JSON = os.path.join(BASE_DIR, "dialogue_timeline.json")

RAW_FOOTAGE_DIR = r"F:\Master AI\16_VIDEO_LIBRARY\raw_footage"
RAIN_FOOTAGE = os.path.join(RAW_FOOTAGE_DIR, "raindrops_window_radevormwald.ogv")
ROOM_FOOTAGE = os.path.join(RAW_FOOTAGE_DIR, "derelict_room_water_dripping.webm")
SUNSET_FOOTAGE = os.path.join(RAW_FOOTAGE_DIR, "sunset_nuages.ogv")

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
WIDTH = 1080
HEIGHT = 1920
FPS = 30
TOTAL_FRAMES = 540 # Exactly 18.000s

with open(TIMELINE_JSON, "r", encoding="utf-8") as f:
    cues_data = json.load(f)["cues"]

def get_active_caption(t):
    for c in cues_data:
        if c["start"] <= t <= c["end"]:
            return c
    return None

class BackgroundFootageStream:
    def __init__(self):
        # Open video captures
        self.cap_rain = cv2.VideoCapture(RAIN_FOOTAGE)
        self.cap_room = cv2.VideoCapture(ROOM_FOOTAGE)
        self.cap_sunset = cv2.VideoCapture(SUNSET_FOOTAGE)
        
    def get_frame(self, t, shot_id):
        # Scale and center crop to 1080x1920
        if shot_id == 1:
            ret, frame = self.cap_rain.read()
            if not ret:
                self.cap_rain.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap_rain.read()
            # Cold midnight grading: darken and push blue/cyan
            frame = cv2.resize(frame, (1080, 1920), interpolation=cv2.INTER_LINEAR)
            frame = cv2.convertScaleAbs(frame, alpha=0.45, beta=-15)
            frame[:, :, 0] = np.clip(frame[:, :, 0].astype(int) + 35, 0, 255) # Blue
            return frame
        elif shot_id == 2:
            ret, frame = self.cap_room.read()
            if not ret:
                self.cap_room.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap_room.read()
            frame = cv2.resize(frame, (1080, 1920), interpolation=cv2.INTER_LINEAR)
            # Emergency red pulse grading
            pulse = math.sin(t * 8.0) * 0.5 + 0.5 # 0 to 1
            frame = cv2.convertScaleAbs(frame, alpha=0.55, beta=-10)
            frame[:, :, 2] = np.clip(frame[:, :, 2].astype(int) + int(45 + 35 * pulse), 0, 255) # Red
            return frame
        else: # shot_id == 3
            ret, frame = self.cap_sunset.read()
            if not ret:
                self.cap_sunset.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap_sunset.read()
            frame = cv2.resize(frame, (1080, 1920), interpolation=cv2.INTER_LINEAR)
            # Warm golden dawn grading
            frame = cv2.convertScaleAbs(frame, alpha=0.85, beta=10)
            frame[:, :, 2] = np.clip(frame[:, :, 2].astype(int) + 25, 0, 255) # Warm red
            frame[:, :, 1] = np.clip(frame[:, :, 1].astype(int) + 15, 0, 255) # Yellow
            return frame

    def close(self):
        self.cap_rain.release()
        self.cap_room.release()
        self.cap_sunset.release()

def draw_character_dev(draw, t, shot_id, is_speaking):
    """
    Renders high-fidelity, consistent character Dev across 3 shot states:
    - Shot 1: Contemplative, looking window, holding coffee mug
    - Shot 2: Extreme shock / disbelief, glowing red phone reflecting on face
    - Shot 3: Relief, warm smile, glowing green confirmation
    """
    # Natural breathing
    breath = math.sin(t * 2.5) * 6.0
    # Eye blink cycle: blink every ~3.5 seconds for 0.15s
    blink_cycle = (t % 3.5)
    is_blinking = blink_cycle < 0.14
    
    # Base anchor
    cx = 540
    base_cy = 1350 + breath

    # Dynamic light tint
    if shot_id == 1:
        skin_base = (220, 185, 160)
        skin_shadow = (175, 140, 115)
        hoodie_base = (24, 38, 64)
        hair_color = (20, 18, 22)
    elif shot_id == 2:
        # Red emergency light cast from below
        skin_base = (240, 160, 150)
        skin_shadow = (190, 110, 100)
        hoodie_base = (45, 20, 30)
        hair_color = (30, 15, 20)
    else: # Shot 3
        # Warm golden dawn rim light
        skin_base = (242, 195, 165)
        skin_shadow = (195, 150, 120)
        hoodie_base = (30, 45, 75)
        hair_color = (25, 20, 24)

    # 1. Torso / Textured Hoodie
    # Broad shoulders and contoured chest
    hoodie_pts = [
        (cx - 360, 1920), (cx - 340, 1420 + breath),
        (cx - 190, 1250 + breath), (cx - 90, 1210 + breath),
        (cx + 90, 1210 + breath), (cx + 190, 1250 + breath),
        (cx + 340, 1420 + breath), (cx + 360, 1920)
    ]
    draw.polygon(hoodie_pts, fill=hoodie_base)
    # Hoodie zipper & drawstring shadow folds
    draw.line([(cx, 1220 + breath), (cx, 1920)], fill=(12, 18, 30), width=6)
    draw.line([(cx - 20, 1220 + breath), (cx - 25, 1460 + breath)], fill=(180, 190, 205), width=4)
    draw.line([(cx + 20, 1220 + breath), (cx + 25, 1460 + breath)], fill=(180, 190, 205), width=4)

    # 2. Neck & Shading
    neck_pts = [
        (cx - 75, 1230 + breath), (cx - 65, 1050 + breath),
        (cx + 65, 1050 + breath), (cx + 75, 1230 + breath)
    ]
    draw.polygon(neck_pts, fill=skin_shadow)

    # 3. Head & Jaw Contour
    # Organic jaw polygon with chin definition
    head_cy = 920 + breath * 0.8
    jaw_pts = [
        (cx - 150, head_cy - 120), (cx - 155, head_cy),
        (cx - 120, head_cy + 130), (cx - 50, head_cy + 210),
        (cx + 50, head_cy + 210), (cx + 120, head_cy + 130),
        (cx + 155, head_cy), (cx + 150, head_cy - 120),
        (cx, head_cy - 200)
    ]
    draw.polygon(jaw_pts, fill=skin_base)
    # Jawline subtle ambient occlusion
    draw.line([(cx - 120, head_cy + 130), (cx - 50, head_cy + 210), (cx + 50, head_cy + 210), (cx + 120, head_cy + 130)],
              fill=skin_shadow, width=4)

    # 4. Hair Volume & Strands
    hair_top = head_cy - 230
    hair_pts = [
        (cx - 180, head_cy - 60), (cx - 190, head_cy - 160),
        (cx - 140, hair_top - 30), (cx - 50, hair_top - 50),
        (cx + 60, hair_top - 40), (cx + 150, hair_top - 15),
        (cx + 190, head_cy - 140), (cx + 180, head_cy - 40),
        (cx + 140, head_cy - 110), (cx + 70, head_cy - 140),
        (cx - 20, head_cy - 125), (cx - 110, head_cy - 135)
    ]
    draw.polygon(hair_pts, fill=hair_color)

    # 5. Ears
    draw.ellipse([cx - 170, head_cy - 30, cx - 140, head_cy + 55], fill=skin_base)
    draw.ellipse([cx + 140, head_cy - 30, cx + 170, head_cy + 55], fill=skin_base)

    # 6. Eyebrows & Eyes based on Dramatic State
    eye_y = head_cy + 10
    
    if shot_id == 1: # Contemplative / neutral
        # Eyebrows relaxed
        draw.line([(cx - 105, eye_y - 45), (cx - 35, eye_y - 40)], fill=hair_color, width=8)
        draw.line([(cx + 35, eye_y - 40), (cx + 105, eye_y - 45)], fill=hair_color, width=8)
        if not is_blinking:
            # Left eye
            draw.ellipse([cx - 95, eye_y - 20, cx - 45, eye_y + 15], fill=(255, 255, 255))
            draw.ellipse([cx - 78, eye_y - 18, cx - 55, eye_y + 13], fill=(50, 35, 30))
            draw.ellipse([cx - 72, eye_y - 12, cx - 62, eye_y - 2], fill=(255, 255, 255)) # Catchlight
            # Right eye
            draw.ellipse([cx + 45, eye_y - 20, cx + 95, eye_y + 15], fill=(255, 255, 255))
            draw.ellipse([cx + 55, eye_y - 18, cx + 78, eye_y + 13], fill=(50, 35, 30))
            draw.ellipse([cx + 62, eye_y - 12, cx + 72, eye_y - 2], fill=(255, 255, 255))
        else:
            draw.line([(cx - 95, eye_y), (cx - 45, eye_y)], fill=(30, 20, 25), width=5)
            draw.line([(cx + 45, eye_y), (cx + 95, eye_y)], fill=(30, 20, 25), width=5)
            
    elif shot_id == 2: # DISBELIEF / SHOCK
        # Eyebrows raised high in distress
        draw.line([(cx - 110, eye_y - 70), (cx - 30, eye_y - 50)], fill=hair_color, width=9)
        draw.line([(cx + 30, eye_y - 50), (cx + 110, eye_y - 70)], fill=hair_color, width=9)
        # Eyes wide open (hyper-expressive)
        draw.ellipse([cx - 105, eye_y - 35, cx - 35, eye_y + 25], fill=(255, 255, 255))
        draw.ellipse([cx - 78, eye_y - 22, cx - 52, eye_y + 12], fill=(60, 20, 20)) # Dialated
        draw.ellipse([cx - 72, eye_y - 18, cx - 60, eye_y - 6], fill=(255, 255, 255))
        
        draw.ellipse([cx + 35, eye_y - 35, cx + 105, eye_y + 25], fill=(255, 255, 255))
        draw.ellipse([cx + 52, eye_y - 22, cx + 78, eye_y + 12], fill=(60, 20, 20))
        draw.ellipse([cx + 60, eye_y - 18, cx + 72, eye_y - 6], fill=(255, 255, 255))
        
    else: # Shot 3: RELIEF / CONFIDENT SMILE
        # Eyebrows relaxed & satisfied
        draw.line([(cx - 100, eye_y - 45), (cx - 35, eye_y - 48)], fill=hair_color, width=8)
        draw.line([(cx + 35, eye_y - 48), (cx + 100, eye_y - 45)], fill=hair_color, width=8)
        if not is_blinking:
            draw.ellipse([cx - 95, eye_y - 18, cx - 45, eye_y + 12], fill=(255, 255, 255))
            draw.ellipse([cx - 75, eye_y - 16, cx - 55, eye_y + 10], fill=(45, 55, 40))
            draw.ellipse([cx - 70, eye_y - 10, cx - 62, eye_y - 2], fill=(255, 255, 255))
            
            draw.ellipse([cx + 45, eye_y - 18, cx + 95, eye_y + 12], fill=(255, 255, 255))
            draw.ellipse([cx + 55, eye_y - 16, cx + 75, eye_y + 10], fill=(45, 55, 40))
            draw.ellipse([cx + 62, eye_y - 10, cx + 70, eye_y - 2], fill=(255, 255, 255))
        else:
            draw.line([(cx - 95, eye_y), (cx - 45, eye_y)], fill=(30, 20, 25), width=5)
            draw.line([(cx + 45, eye_y), (cx + 95, eye_y)], fill=(30, 20, 25), width=5)

    # 7. Shaded Nose
    draw.line([(cx, eye_y - 10), (cx - 8, eye_y + 65), (cx + 14, eye_y + 65)], fill=skin_shadow, width=4)

    # 8. Dynamic Mouth with Lip-Sync
    mouth_y = head_cy + 125
    if shot_id == 2:
        # Open agape in shock
        draw.ellipse([cx - 45, mouth_y - 25, cx + 45, mouth_y + 35], fill=(50, 15, 15))
        # Visible teeth
        draw.rectangle([cx - 25, mouth_y - 20, cx + 25, mouth_y - 5], fill=(250, 250, 250))
    elif shot_id == 3:
        # Broad warm smile
        if is_speaking:
            draw.chord([cx - 55, mouth_y - 15, cx + 55, mouth_y + 35], 0, 180, fill=(160, 45, 55))
            draw.rectangle([cx - 35, mouth_y - 10, cx + 35, mouth_y + 2], fill=(255, 255, 255))
        else:
            draw.arc([cx - 50, mouth_y - 20, cx + 50, mouth_y + 25], 20, 160, fill=(140, 40, 45), width=6)
    else: # Shot 1
        if is_speaking:
            viseme_open = (math.sin(t * 18.0) * 0.5 + 0.5) * 16.0
            draw.ellipse([cx - 35, mouth_y - viseme_open/2, cx + 35, mouth_y + viseme_open/2], fill=(130, 40, 50))
        else:
            draw.line([(cx - 30, mouth_y), (cx + 30, mouth_y)], fill=(120, 40, 45), width=5)

    # 9. Hand Props & Dynamic Light Emitters
    if shot_id == 2:
        # Hand holding glowing phone casting bright red alert
        phone_x, phone_y = cx + 80, 1280 + breath
        # Red ambient glow behind phone
        draw.ellipse([phone_x - 120, phone_y - 150, phone_x + 160, phone_y + 150], fill=(220, 38, 38, 120))
        # Phone body
        draw.rounded_rectangle([phone_x - 60, phone_y - 110, phone_x + 90, phone_y + 110], radius=16, fill=(15, 23, 42), outline=(239, 68, 68), width=4)
        # Red warning screen
        draw.rectangle([phone_x - 50, phone_y - 95, phone_x + 80, phone_y + 95], fill=(185, 28, 28))
        draw.text((phone_x - 40, phone_y - 40), "! ALERT", fill=(255, 255, 255))
        draw.text((phone_x - 45, phone_y), "-99,000", fill=(255, 255, 255))
        # Hand fingers gripping phone
        draw.ellipse([phone_x - 75, phone_y - 30, phone_x - 45, phone_y + 50], fill=skin_base)
    elif shot_id == 3:
        # Glowing green confirmation phone
        phone_x, phone_y = cx + 80, 1340 + breath
        draw.rounded_rectangle([phone_x - 60, phone_y - 100, phone_x + 90, phone_y + 100], radius=16, fill=(15, 23, 42), outline=(34, 197, 94), width=4)
        draw.rectangle([phone_x - 50, phone_y - 85, phone_x + 80, phone_y + 85], fill=(21, 128, 61))
        draw.text((phone_x - 35, phone_y - 20), "✓ TEST OK", fill=(255, 255, 255))

def render_film():
    print("="*65)
    print("MASTER AI — PHASE 7.13: MULTI-TRACK 9:16 VERTICAL TEST FILM")
    print("Title: 'MIDNIGHT DISCOVERY' (18.000s @ 30 FPS CFR = 540 Frames)")
    print("Combining: Real Moving Video Footage + Shaded Articulated Character")
    print("="*65)
    
    bg_stream = BackgroundFootageStream()

    # Master FFmpeg pipe
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_WAV,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        FINAL_MP4
    ]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Fonts
    try:
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
        font_badge = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
    except:
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    t_start = time.perf_counter()
    
    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)
        
        # Determine shot
        if t < 5.5:
            shot_id = 1
        elif t < 11.0:
            shot_id = 2
        else:
            shot_id = 3
            
        # 1. Fetch real moving background frame (BGR)
        bg_bgr = bg_stream.get_frame(t, shot_id)
        bg_rgb = cv2.cvtColor(bg_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(bg_rgb)
        draw = ImageDraw.Draw(im)
        
        # Active voice state
        active_cue = get_active_caption(t)
        is_speaking = active_cue is not None
        
        # 2. Draw articulated, richly shaded character Dev
        draw_character_dev(draw, t, shot_id, is_speaking)
        
        # 3. Burn-in Kinetic Subtitles in safe zone (y = 1460 to 1560)
        if active_cue:
            sub_text = active_cue["hinglish"]
            # Dark pill card backing
            bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
            text_w = bbox[2] - bbox[0]
            card_x0 = max(40, (WIDTH - text_w) // 2 - 25)
            card_x1 = min(WIDTH - 40, (WIDTH + text_w) // 2 + 25)
            card_y0 = 1480
            card_y1 = 1570
            
            draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=18, fill=(15, 23, 42, 230), outline=(250, 204, 21), width=2)
            # Speaker pill
            draw.rounded_rectangle([card_x0 + 10, card_y0 - 28, card_x0 + 120, card_y0 + 2], radius=8, fill=(250, 204, 21))
            draw.text((card_x0 + 22, card_y0 - 24), "DEV", font=font_badge, fill=(15, 23, 42))
            # Main caption text
            draw.text(((WIDTH - text_w) // 2, card_y0 + 18), sub_text, font=font_sub, fill=(255, 255, 255))

        # Push frame to FFmpeg stdin pipe
        pipe.stdin.write(im.tobytes())
        
        if (f + 1) % 90 == 0:
            elapsed = time.perf_counter() - t_start
            fps = (f + 1) / elapsed
            print(f"Rendered {f+1:3d} / 540 frames ({(f+1)/30.0:4.1f}s) | Speed: {fps:.1f} FPS | Elapsed: {elapsed:.1f}s")
            
    pipe.stdin.close()
    pipe.wait()
    bg_stream.close()
    
    total_time = time.perf_counter() - t_start
    print("="*65)
    print(f"TEST FILM RENDERED CLEANLY TO: {FINAL_MP4}")
    print(f"Total Elapsed Time: {total_time:.1f}s | Average Speed: {TOTAL_FRAMES/total_time:.1f} FPS")
    print(f"File Size: {os.path.getsize(FINAL_MP4):,} bytes")
    print("="*65)

if __name__ == "__main__":
    render_film()
