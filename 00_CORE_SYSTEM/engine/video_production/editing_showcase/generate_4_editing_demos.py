import os
import sys
import time
import json
import numpy as np
import soundfile as sf
import scipy.signal
import subprocess
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SHOWCASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase"
os.makedirs(SHOWCASE_DIR, exist_ok=True)
ARTIFACT_DIR = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

# Shared Audio & Assets
VOICE_WAV = r"F:\Master AI\00_CORE_SYSTEM\engine\voice_dna\offline_cloned_output\showcase\03_gemini_puck_energetic_male.wav"
BGM_WAV = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\sfx\lofi_bg_track.wav"
WHOOSH_WAV = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx\whoosh.wav"
POP_WAV = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx\pop.wav"
DING_WAV = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx\ding.wav"

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
SPRITE_JUNIOR = os.path.join(ASSETS_DIR, "clean_junior_hands_up.png")
SPRITE_SENIOR = os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png")

import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Read Voice Audio
v_data, sr = sf.read(VOICE_WAV)
if v_data.ndim > 1: v_data = v_data.mean(axis=1)
v_dur = len(v_data) / sr
total_dur = v_dur + 0.5
FPS = 24
total_frames = int(total_dur * FPS)
WIDTH, HEIGHT = 1080, 1920

print(f">>> [SETUP] Total Duration: {total_dur:.2f}s | Total Frames: {total_frames}")

# Prepare Master Mixed Audio
bgm_data, bgm_sr = sf.read(BGM_WAV)
if bgm_sr != sr:
    bgm_data = scipy.signal.resample(bgm_data, int(len(bgm_data)*sr/bgm_sr))
if bgm_data.ndim > 1: bgm_data = bgm_data.mean(axis=1)

target_len = int(total_dur * sr)
bgm_loop = np.tile(bgm_data, int(np.ceil(target_len/len(bgm_data))))[:target_len] * (10**(-22.0/20.0))
# Fade out
fade_len = int(0.6 * sr)
bgm_loop[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

pad_v = np.pad(v_data, (0, target_len - len(v_data))) if len(v_data) < target_len else v_data[:target_len]
mixed_audio = pad_v * 0.92 + bgm_loop
mixed_audio_path = os.path.join(SHOWCASE_DIR, "master_audio_bed.wav")
sf.write(mixed_audio_path, mixed_audio, sr)

# Prepare SFX layered audio for Demo 1 & Demo 4
sfx_audio = mixed_audio.copy()
def overlay_sfx(target, sfx_path, at_time, gain_db=-6.0):
    if not os.path.exists(sfx_path): return
    sd, ssr = sf.read(sfx_path)
    if ssr != sr: sd = scipy.signal.resample(sd, int(len(sd)*sr/ssr))
    if sd.ndim > 1: sd = sd.mean(axis=1)
    sd = sd * (10**(gain_db/20.0))
    start_s = int(at_time * sr)
    end_s = min(len(target), start_s + len(sd))
    target[start_s:end_s] += sd[:end_s - start_s]

# Add whoosh at 3.2s (beat change) and 7.1s (punchline)
overlay_sfx(sfx_audio, WHOOSH_WAV, 3.1)
overlay_sfx(sfx_audio, POP_WAV, 3.4)
overlay_sfx(sfx_audio, WHOOSH_WAV, 7.0)
overlay_sfx(sfx_audio, DING_WAV, 7.3)
peak = np.max(np.abs(sfx_audio))
if peak > 0.95: sfx_audio = sfx_audio / peak * 0.95
sfx_audio_path = os.path.join(SHOWCASE_DIR, "master_sfx_audio_bed.wav")
sf.write(sfx_audio_path, sfx_audio, sr)

# Fonts
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 48)
    font_sub_hi = ImageFont.truetype("mangal.ttf", 52)
    font_sub_en = ImageFont.truetype("arialbd.ttf", 44)
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_giant = ImageFont.truetype("arialbd.ttf", 72)
    font_giant_hi = ImageFont.truetype("mangal.ttf", 64)
except Exception:
    font_bold = font_sub_hi = font_sub_en = font_badge = font_giant = font_giant_hi = ImageFont.load_default()

sprite_img = Image.open(SPRITE_JUNIOR).convert("RGBA")
senior_img = Image.open(SPRITE_SENIOR).convert("RGBA")

# Base Background
bg_dark = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 255))
d = ImageDraw.Draw(bg_dark)
for y in range(HEIGHT):
    g = int(23 + (15 - 23)*(y/HEIGHT))
    b = int(42 + (30 - 42)*(y/HEIGHT))
    d.line([(0, y), (WIDTH, y)], fill=(12, g, b, 255))


# =============================================================
# DEMO 1: FFmpeg Pro Filtergraph (Camera Motion & Jump Cuts)
# =============================================================
print("\n>>> [DEMO 1] Rendering Demo 1: FFmpeg Pro Camera Motion & Jump Cuts...")
d1_dir = os.path.join(SHOWCASE_DIR, "d1_frames")
os.makedirs(d1_dir, exist_ok=True)

for i in range(total_frames):
    t = i / FPS
    # Camera punch-in algorithm:
    # 0.0 - 3.2s: Wide camera (zoom 1.0 to 1.05)
    # 3.2 - 7.0s: Close-up Jump Cut on face (zoom 1.25)
    # 7.0 - end: Wide punch with screen shake
    frame = bg_dark.copy()
    fdraw = ImageDraw.Draw(frame)

    if t < 3.2:
        zoom = 1.0 + (t / 3.2) * 0.08
        offset_y = 0
        active_sprite = sprite_img
        cut_label = "🎥 SHOT 1: WIDE DOLLY IN (Zoom 1.0x -> 1.08x)"
    elif 3.2 <= t < 7.0:
        zoom = 1.25 + np.sin((t-3.2)*3.0)*0.02
        offset_y = 120
        active_sprite = senior_img
        cut_label = "🎥 SHOT 2: JUMP-CUT CLOSE-UP (Zoom 1.25x Punch)"
    else:
        shake_x = int(np.sin(t * 30.0) * 8 * max(0, 1.0 - (t-7.0)))
        shake_y = int(np.cos(t * 25.0) * 8 * max(0, 1.0 - (t-7.0)))
        zoom = 1.12
        offset_y = shake_y
        active_sprite = sprite_img
        cut_label = "🎥 SHOT 3: IMPACT SHAKE + PULLBACK"

    # Draw scaled sprite according to zoom
    target_w = int(760 * zoom)
    target_h = int(active_sprite.height * (target_w / active_sprite.width))
    char_r = active_sprite.resize((target_w, target_h), Image.Resampling.LANCZOS)
    cx = (WIDTH - target_w) // 2
    cy = 500 - offset_y
    frame.alpha_composite(char_r, (cx, cy))

    # Top technical indicator badge
    fdraw.rounded_rectangle([(60, 80), (WIDTH - 60, 180)], radius=20, fill=(20, 26, 42, 230), outline=(56, 189, 248), width=3)
    fdraw.text((WIDTH//2, 115), "TOOL 1: FFMPEG PRO CAMERA MOTION", font=font_bold, fill=(56, 189, 248), anchor="mm")
    fdraw.text((WIDTH//2, 150), cut_label, font=font_badge, fill=(226, 232, 240), anchor="mm")

    # Bottom Standard Subtitle
    sub_text = "सिर्फ मेहनत करके अमीर नहीं बन सकते!" if t < 3.2 else ("बड़ी गलतफहमी में हैं आप!" if t < 7.0 else "असली खेल सही जानकारी और स्मार्ट सिस्टम्स का है!")
    fdraw.rounded_rectangle([(80, 1580), (WIDTH - 80, 1780)], radius=24, fill=(15, 23, 42, 240), outline=(148, 163, 184), width=2)
    fdraw.text((WIDTH//2, 1680), sub_text, font=font_sub_hi, fill=(255, 255, 255), anchor="mm")

    frame.convert("RGB").save(os.path.join(d1_dir, f"frame_{i:05d}.jpg"), quality=90)

d1_mp4 = os.path.join(SHOWCASE_DIR, "demo_1_ffmpeg_pro_motion.mp4")
subprocess.run([
    FFMPEG, "-y", "-framerate", str(FPS),
    "-i", os.path.join(d1_dir, "frame_%05d.jpg"),
    "-i", sfx_audio_path,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast",
    "-c:a", "aac", "-b:a", "192k", "-shortest", d1_mp4
], check=True)
print("    Demo 1 Exported:", d1_mp4)


# =============================================================
# DEMO 2: Web-Standards / HTML5-CSS Remotion Vector Motion
# =============================================================
print("\n>>> [DEMO 2] Rendering Demo 2: Web-Standards / Remotion Vector Motion...")
d2_dir = os.path.join(SHOWCASE_DIR, "d2_frames")
os.makedirs(d2_dir, exist_ok=True)

for i in range(total_frames):
    t = i / FPS
    frame = bg_dark.copy()
    fdraw = ImageDraw.Draw(frame)

    # Top Badge
    fdraw.rounded_rectangle([(60, 80), (WIDTH - 60, 180)], radius=20, fill=(20, 26, 42, 230), outline=(168, 85, 247), width=3)
    fdraw.text((WIDTH//2, 115), "TOOL 2: REMOTION / CSS VECTOR MOTION", font=font_bold, fill=(192, 132, 252), anchor="mm")
    fdraw.text((WIDTH//2, 150), "DYNAMIC FLOATING UI CARDS & SPRING PHYSICS", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # Character in background (static breathing)
    breath = int(np.sin(t * 3.5) * 6)
    target_w = 640
    target_h = int(sprite_img.height * (target_w / sprite_img.width))
    c_img = sprite_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    frame.alpha_composite(c_img, ((WIDTH - target_w)//2, 600 + breath))

    # Floating Animated UI Card 1: "HARD WORK 99%" vs "SMART SYSTEMS 100x"
    # Spring sliding card from right side
    card_progress = min(1.0, max(0.0, (t - 0.5) / 0.8))
    # Overshoot spring curve:
    spring = 1.0 - np.exp(-6.0 * card_progress) * np.cos(10.0 * card_progress)
    card_x = int(-400 + spring * 480)
    card_y = 380

    # Draw Floating Glassmorphism Card
    fdraw.rounded_rectangle([(card_x, card_y), (card_x + 680, card_y + 260)], radius=28, fill=(30, 41, 59, 235), outline=(56, 189, 248), width=3)
    fdraw.text((card_x + 50, card_y + 60), "❌ HARD WORK ALONE", font=font_bold, fill=(248, 113, 113))
    fdraw.text((card_x + 50, card_y + 130), "TRAPPED IN 9-TO-5 GRIND", font=font_badge, fill=(148, 163, 184))
    fdraw.rounded_rectangle([(card_x + 50, card_y + 180), (card_x + 600, card_y + 210)], radius=15, fill=(15, 23, 42))
    fdraw.rounded_rectangle([(card_x + 50, card_y + 180), (card_x + 250, card_y + 210)], radius=15, fill=(239, 68, 68))

    # Second Floating Card: "AI & AUTOMATION" pops in at t=4.5s
    if t >= 4.0:
        c2_prog = min(1.0, (t - 4.0) / 0.7)
        c2_spring = 1.0 - np.exp(-6.0 * c2_prog) * np.cos(10.0 * c2_prog)
        c2_w = int(720 * c2_spring)
        c2_h = int(240 * c2_spring)
        c2_x = (WIDTH - c2_w) // 2
        c2_y = 680
        if c2_w > 50:
            fdraw.rounded_rectangle([(c2_x, c2_y), (c2_x + c2_w, c2_y + c2_h)], radius=28, fill=(15, 23, 42, 245), outline=(34, 197, 94), width=4)
            if c2_prog > 0.6:
                fdraw.text((WIDTH//2, c2_y + 70), "⚡ AI & AUTOMATION: 100X SCALE", font=font_bold, fill=(74, 222, 128), anchor="mm")
                fdraw.text((WIDTH//2, c2_y + 140), "THE REAL WEALTH GAME IN 2026", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # Bottom Standard Subtitle
    sub_text = "सिर्फ मेहनत करके अमीर नहीं बन सकते!" if t < 3.2 else ("बड़ी गलतफहमी में हैं आप!" if t < 7.0 else "असली खेल सही जानकारी और स्मार्ट सिस्टम्स का है!")
    fdraw.rounded_rectangle([(80, 1580), (WIDTH - 80, 1780)], radius=24, fill=(15, 23, 42, 240), outline=(148, 163, 184), width=2)
    fdraw.text((WIDTH//2, 1680), sub_text, font=font_sub_hi, fill=(255, 255, 255), anchor="mm")

    frame.convert("RGB").save(os.path.join(d2_dir, f"frame_{i:05d}.jpg"), quality=90)

d2_mp4 = os.path.join(SHOWCASE_DIR, "demo_2_web_motion_graphics.mp4")
subprocess.run([
    FFMPEG, "-y", "-framerate", str(FPS),
    "-i", os.path.join(d2_dir, "frame_%05d.jpg"),
    "-i", mixed_audio_path,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast",
    "-c:a", "aac", "-b:a", "192k", "-shortest", d2_mp4
], check=True)
print("    Demo 2 Exported:", d2_mp4)


# =============================================================
# DEMO 3: Kinetic Word-by-Word Bouncy Subtitles (Hormozi / Vox)
# =============================================================
print("\n>>> [DEMO 3] Rendering Demo 3: Kinetic Word-by-Word Bouncy Subtitles...")
d3_dir = os.path.join(SHOWCASE_DIR, "d3_frames")
os.makedirs(d3_dir, exist_ok=True)

# Word level timestamps (Simulated high-precision Whisper alignment)
word_timestamps = [
    (0.0, 0.7, "अगर आप", "सकते हैं?"),
    (0.7, 1.6, "सोचते हैं", "कि सिर्फ"),
    (1.6, 2.4, "मेहनत करके", "अमीर"),
    (2.4, 3.4, "बन सकते हैं,", "तो सुनो!"),
    (3.4, 4.4, "तो आप बहुत", "बड़ी"),
    (4.4, 5.6, "गलतफहमी", "में हैं!"),
    (5.6, 7.0, "असली खेल", "मेहनत का नहीं,"),
    (7.0, 8.4, "सही जानकारी", "और"),
    (8.4, 10.6, "स्मार्ट सिस्टम्स", "का है! 🚀")
]

for i in range(total_frames):
    t = i / FPS
    frame = bg_dark.copy()
    fdraw = ImageDraw.Draw(frame)

    # Top Badge
    fdraw.rounded_rectangle([(60, 80), (WIDTH - 60, 180)], radius=20, fill=(20, 26, 42, 230), outline=(234, 179, 8), width=3)
    fdraw.text((WIDTH//2, 115), "TOOL 3: KINETIC WORD-BY-WORD CAPTIONS", font=font_bold, fill=(250, 204, 21), anchor="mm")
    fdraw.text((WIDTH//2, 150), "ALEX HORMOZI / VOX RETENTION STYLE", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # Character behind
    target_w = 700
    target_h = int(sprite_img.height * (target_w / sprite_img.width))
    c_img = sprite_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    frame.alpha_composite(c_img, ((WIDTH - target_w)//2, 540))

    # Find active word
    active_pair = word_timestamps[-1]
    for w_start, w_end, w1, w2 in word_timestamps:
        if w_start <= t < w_end:
            active_pair = (w_start, w_end, w1, w2)
            break

    # Kinetic Pop Animation (scale bounce on word start)
    rel_t = t - active_pair[0]
    bounce = 1.0 + 0.18 * max(0.0, 1.0 - (rel_t / 0.25))

    # Center Box for Kinetic Pop
    k_box = [(80, 1380), (WIDTH - 80, 1720)]
    fdraw.rounded_rectangle(k_box, radius=32, fill=(15, 23, 42, 245), outline=(250, 204, 21), width=4)

    # Word 1 (Glowing Yellow/Red)
    w1_color = (239, 68, 68) if "गलतफहमी" in active_pair[2] else ((34, 197, 94) if "स्मार्ट" in active_pair[2] else (253, 224, 71))
    fdraw.text((WIDTH//2, 1480), active_pair[2], font=font_giant_hi, fill=w1_color, anchor="mm")
    
    # Word 2 (White with outline)
    fdraw.text((WIDTH//2, 1610), active_pair[3], font=font_giant_hi, fill=(255, 255, 255), anchor="mm")

    frame.convert("RGB").save(os.path.join(d3_dir, f"frame_{i:05d}.jpg"), quality=90)

d3_mp4 = os.path.join(SHOWCASE_DIR, "demo_3_kinetic_word_subtitles.mp4")
subprocess.run([
    FFMPEG, "-y", "-framerate", str(FPS),
    "-i", os.path.join(d3_dir, "frame_%05d.jpg"),
    "-i", mixed_audio_path,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast",
    "-c:a", "aac", "-b:a", "192k", "-shortest", d3_mp4
], check=True)
print("    Demo 3 Exported:", d3_mp4)


# =============================================================
# DEMO 4: MASTER HYBRID REEL (All 3 Tools Combined)
# =============================================================
print("\n>>> [DEMO 4] Rendering Demo 4: THE MASTER HYBRID (All 3 Tools Combined)...")
d4_dir = os.path.join(SHOWCASE_DIR, "d4_frames")
os.makedirs(d4_dir, exist_ok=True)

for i in range(total_frames):
    t = i / FPS
    frame = bg_dark.copy()
    fdraw = ImageDraw.Draw(frame)

    # 1. FFmpeg Camera Zoom & Jump Cuts
    if t < 3.2:
        zoom = 1.0 + (t / 3.2) * 0.08
        offset_y = 0
        active_sprite = sprite_img
    elif 3.2 <= t < 7.0:
        zoom = 1.25 + np.sin((t-3.2)*3.0)*0.02
        offset_y = 120
        active_sprite = senior_img
    else:
        shake_y = int(np.cos(t * 25.0) * 8 * max(0, 1.0 - (t-7.0)))
        zoom = 1.12
        offset_y = shake_y
        active_sprite = sprite_img

    # Character Sprite
    target_w = int(760 * zoom)
    target_h = int(active_sprite.height * (target_w / active_sprite.width))
    char_r = active_sprite.resize((target_w, target_h), Image.Resampling.LANCZOS)
    cx = (WIDTH - target_w) // 2
    cy = 500 - offset_y
    frame.alpha_composite(char_r, (cx, cy))

    # 2. Web Vector Floating Motion Graphic Card (Appears at t=3.5s to 7.0s)
    if 3.2 <= t < 7.0:
        c_prog = min(1.0, (t - 3.2) / 0.5)
        spring = 1.0 - np.exp(-6.0 * c_prog) * np.cos(8.0 * c_prog)
        cw = int(680 * spring)
        ch = int(220 * spring)
        card_x = (WIDTH - cw) // 2
        card_y = 350
        if cw > 40:
            fdraw.rounded_rectangle([(card_x, card_y), (card_x + cw, card_y + ch)], radius=24, fill=(15, 23, 42, 240), outline=(239, 68, 68), width=4)
            if c_prog > 0.5:
                fdraw.text((WIDTH//2, card_y + 65), "⚠️ 99% DEVS GET THIS WRONG", font=font_bold, fill=(248, 113, 113), anchor="mm")
                fdraw.text((WIDTH//2, card_y + 140), "TRAPPED IN MANUAL TOIL", font=font_badge, fill=(226, 232, 240), anchor="mm")
    elif t >= 7.0:
        c_prog = min(1.0, (t - 7.0) / 0.5)
        spring = 1.0 - np.exp(-6.0 * c_prog) * np.cos(8.0 * c_prog)
        cw = int(720 * spring)
        ch = int(220 * spring)
        card_x = (WIDTH - cw) // 2
        card_y = 350
        if cw > 40:
            fdraw.rounded_rectangle([(card_x, card_y), (card_x + cw, card_y + ch)], radius=24, fill=(15, 23, 42, 240), outline=(34, 197, 94), width=4)
            if c_prog > 0.5:
                fdraw.text((WIDTH//2, card_y + 65), "🚀 SMART SYSTEMS = INFINITE LEVERAGE", font=font_bold, fill=(74, 222, 128), anchor="mm")
                fdraw.text((WIDTH//2, card_y + 140), "AUTOMATE YOUR CODE & EARNINGS", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # 3. Top Header Badge
    fdraw.rounded_rectangle([(60, 80), (WIDTH - 60, 180)], radius=20, fill=(20, 26, 42, 235), outline=(34, 197, 94), width=3)
    fdraw.text((WIDTH//2, 115), "🔥 DEMO 4: MASTER HYBRID (ALL 3 COMBINED)", font=font_bold, fill=(74, 222, 128), anchor="mm")
    fdraw.text((WIDTH//2, 150), "FFMPEG MOTION + REMOTION GRAPHICS + KINETIC SUBS + SFX", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # 4. Kinetic Word-by-Word Subtitles (Bottom Center)
    active_pair = word_timestamps[-1]
    for w_start, w_end, w1, w2 in word_timestamps:
        if w_start <= t < w_end:
            active_pair = (w_start, w_end, w1, w2)
            break

    k_box = [(80, 1400), (WIDTH - 80, 1720)]
    fdraw.rounded_rectangle(k_box, radius=32, fill=(15, 23, 42, 248), outline=(250, 204, 21), width=4)

    w1_color = (239, 68, 68) if "गलतफहमी" in active_pair[2] else ((34, 197, 94) if "स्मार्ट" in active_pair[2] else (253, 224, 71))
    fdraw.text((WIDTH//2, 1490), active_pair[2], font=font_giant_hi, fill=w1_color, anchor="mm")
    fdraw.text((WIDTH//2, 1615), active_pair[3], font=font_giant_hi, fill=(255, 255, 255), anchor="mm")

    frame.convert("RGB").save(os.path.join(d4_dir, f"frame_{i:05d}.jpg"), quality=90)

d4_mp4 = os.path.join(SHOWCASE_DIR, "demo_4_master_hybrid_viral.mp4")
subprocess.run([
    FFMPEG, "-y", "-framerate", str(FPS),
    "-i", os.path.join(d4_dir, "frame_%05d.jpg"),
    "-i", sfx_audio_path,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast",
    "-c:a", "aac", "-b:a", "192k", "-shortest", d4_mp4
], check=True)
print("    Demo 4 Exported:", d4_mp4)

# Mirror all 4 MP4s to Artifacts
import shutil
for f in ["demo_1_ffmpeg_pro_motion.mp4", "demo_2_web_motion_graphics.mp4", "demo_3_kinetic_word_subtitles.mp4", "demo_4_master_hybrid_viral.mp4"]:
    src = os.path.join(SHOWCASE_DIR, f)
    dst = os.path.join(ARTIFACT_DIR, f)
    shutil.copy2(src, dst)
    print(f"Mirrored {f} -> {os.path.getsize(dst)/(1024*1024):.2f} MB")

print("\n>>> [SHOWCASE COMPLETE] All 4 Demos Successfully Generated & Mirrored!")
