"""
build_new_story_demos.py
Builds 2 brand-new, high-retention viral story demos with completely new characters and stories:
1. Story Demo 1: "Tech Hustle & AI Speed" (Neha & Arjun)
2. Story Demo 2: "Black Hole Time Dilation" (Billu Chibi & Dr. Kabir)

Both videos feature:
- 100% pure Google Gemini TTS dialogue (Puck, Kore, Charon)
- Active character bounce, scale, and emotional pose switching
- Alex Hormozi kinetic word-by-word bouncy neon subtitles
- Floating glassmorphism vector UI cards with real-time progress & metrics
- Multi-track audio: Voice + Ducked BGM + SFX (Whooshes, Pops, Chimes)
"""

import os
import sys
import math
import shutil
import subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG = r"F:\Master AI\.venv_py310\lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
BILLU_LIB = r"F:\Master AI\CHARACTER_LIBRARY\billu_chibi"
AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\story_audio"
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase"
ARTIFACT_DIR = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

SFX_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx"
BGM_WAV = os.path.join(SFX_DIR, "lofi_bg_track.wav")
WHOOSH_WAV = os.path.join(SFX_DIR, "whoosh.wav")
POP_WAV = os.path.join(SFX_DIR, "pop.wav")
DING_WAV = os.path.join(SFX_DIR, "ding.wav")

FPS = 24
WIDTH = 1080
HEIGHT = 1920

# Fonts
FONT_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 64)
FONT_SUB_ACTIVE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 72)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 38)
FONT_CARD_METRIC = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 68)

def load_rgba(path, max_h=850):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    ratio = max_h / h
    new_w = int(w * ratio)
    return im.resize((new_w, max_h), Image.Resampling.LANCZOS)

def draw_glass_card(draw_obj, rect, fill=(20, 24, 38, 220), border=(90, 160, 255, 230), radius=28, border_w=3):
    x0, y0, x1, y1 = rect
    draw_obj.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=border, width=border_w)

def mix_audio_track(voice_wavs_with_offsets, total_dur, sfx_events, bgm_path, out_wav):
    sr = 24000
    total_samples = int(total_dur * sr)
    master = np.zeros(total_samples, dtype=np.float32)

    # 1. Voice Track
    voice_mask = np.zeros(total_samples, dtype=np.float32)
    for wav_path, offset_sec in voice_wavs_with_offsets:
        data, file_sr = sf.read(wav_path)
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        if file_sr != sr:
            pass  # Gemini outputs 24000Hz
        start = int(offset_sec * sr)
        end = min(start + len(data), total_samples)
        chunk = data[:end - start]
        master[start:end] += chunk * 1.05
        voice_mask[start:end] = 1.0

    # 2. BGM with Ducking
    if os.path.exists(bgm_path):
        bgm, bgm_sr = sf.read(bgm_path)
        if len(bgm.shape) > 1:
            bgm = bgm.mean(axis=1)
        # Loop bgm
        repeats = int(np.ceil(total_samples / len(bgm)))
        bgm_long = np.tile(bgm, repeats)[:total_samples]
        
        # Smooth ducking curve: 0.12 when speaking, 0.28 during pauses
        # Simple moving average filter for smooth transitions
        window = int(sr * 0.25)
        kernel = np.ones(window) / window
        smoothed_mask = np.convolve(voice_mask, kernel, mode='same')
        gain = 0.28 - (smoothed_mask * 0.16)
        master += bgm_long * gain

    # 3. SFX Events (list of (sfx_wav, time_sec, volume))
    for sfx_path, t_sec, vol in sfx_events:
        if os.path.exists(sfx_path):
            sfx_data, sfx_sr = sf.read(sfx_path)
            if len(sfx_data.shape) > 1:
                sfx_data = sfx_data.mean(axis=1)
            start = int(t_sec * sr)
            end = min(start + len(sfx_data), total_samples)
            if end > start:
                master[start:end] += sfx_data[:end - start] * vol

    # Normalize
    peak = np.max(np.abs(master))
    if peak > 0.98:
        master = master * (0.95 / peak)

    sf.write(out_wav, master, sr)
    print(f"Mixed Audio: {out_wav} (Dur: {total_dur:.2f}s)")

def render_video_frames(frames_dir, num_frames, frame_generator):
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(num_frames):
        t = i / FPS
        im = frame_generator(i, t)
        im.save(os.path.join(frames_dir, f"frame_{i:05d}.jpg"), quality=93)
        if i % 60 == 0 or i == num_frames - 1:
            print(f"  Frame {i}/{num_frames} ({t:.1f}s)")

def encode_mp4(frames_dir, audio_wav, out_mp4):
    cmd = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", audio_wav,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Exported MP4: {out_mp4}")


# ==============================================================================
# STORY 1: TECH HUSTLE (Neha & Arjun)
# ==============================================================================
def build_story_1():
    print("\n=======================================================")
    print(">>> BUILDING STORY 1: TECH HUSTLE & AI SPEED (Neha & Arjun)")
    print("=======================================================")
    
    # 1. Audio durations
    a1_path = os.path.join(AUDIO_DIR, "s1_arjun_1.wav")
    a2_path = os.path.join(AUDIO_DIR, "s1_neha_2.wav")
    a3_path = os.path.join(AUDIO_DIR, "s1_arjun_3.wav")

    d1 = len(sf.read(a1_path)[0]) / 24000.0
    d2 = len(sf.read(a2_path)[0]) / 24000.0
    d3 = len(sf.read(a3_path)[0]) / 24000.0

    t_turn1 = 0.0
    t_turn2 = d1 + 0.35
    t_turn3 = t_turn2 + d2 + 0.35
    total_dur = t_turn3 + d3 + 0.6

    print(f"Timing: Turn 1: {t_turn1:.2f}s, Turn 2: {t_turn2:.2f}s, Turn 3: {t_turn3:.2f}s, Total: {total_dur:.2f}s")

    # SFX events
    sfx = [
        (WHOOSH_WAV, 0.05, 0.5),
        (POP_WAV, 1.2, 0.6),
        (WHOOSH_WAV, t_turn2, 0.6),
        (POP_WAV, t_turn2 + 1.0, 0.7),
        (DING_WAV, t_turn2 + 4.2, 0.8),
        (WHOOSH_WAV, t_turn3, 0.6),
        (POP_WAV, t_turn3 + 0.8, 0.7),
    ]

    master_wav = os.path.join(OUT_DIR, "story1_master_audio.wav")
    mix_audio_track(
        [(a1_path, t_turn1), (a2_path, t_turn2), (a3_path, t_turn3)],
        total_dur, sfx, BGM_WAV, master_wav
    )

    # Load character images
    arjun_stressed = load_rgba(os.path.join(CHAR_LIB, "arjun_shrug.png"), max_h=860)
    arjun_shocked = load_rgba(os.path.join(CHAR_LIB, "arjun_shocked.png"), max_h=860)
    arjun_happy = load_rgba(os.path.join(CHAR_LIB, "arjun_thumbsup.png"), max_h=860)

    neha_laptop = load_rgba(os.path.join(CHAR_LIB, "neha_laptop.png"), max_h=860)
    neha_point = load_rgba(os.path.join(CHAR_LIB, "neha_pointing.png"), max_h=860)
    neha_peace = load_rgba(os.path.join(CHAR_LIB, "neha_peace.png"), max_h=860)

    # Word subtitles per turn
    # Turn 1: "यार नेहा, आज रात भी जागना पड़ेगा! 500 लाइन का कोड लिखना है और क्लाइंट सुबह 8 बजे डिलीवरी मांग रहा है!"
    t1_words = [
        ("यार नेहा,", 0.0, 1.0),
        ("आज रात भी", 1.0, 2.2),
        ("जागना पड़ेगा!", 2.2, 3.4),
        ("500 लाइन का", 3.4, 4.4),
        ("कोड लिखना है", 4.4, 5.2),
        ("सुबह 8 बजे डिलीवरी!", 5.2, d1)
    ]
    # Turn 2: "अरे अर्जुन, तू 2020 में जी रहा है क्या? देख, Master AI ने 30 सेकंड में पूरा कोड टेस्ट करके लाइव भी कर दिया!"
    t2_words = [
        ("अरे अर्जुन,", 0.0, 1.1),
        ("2020 में जी रहा है?", 1.1, 2.6),
        ("देख Master AI ने", 2.6, 4.0),
        ("30 सेकंड में", 4.0, 5.2),
        ("पूरा कोड टेस्ट करके", 5.2, 6.5),
        ("लाइव भी कर दिया! 🚀", 6.5, d2)
    ]
    # Turn 3: "क्या बात कर रही है? सिर्फ 30 सेकंड में? मुझे भी सिखा दे भाई!"
    t3_words = [
        ("क्या बात कर रही है?", 0.0, 1.3),
        ("सिर्फ 30 सेकंड में?!", 1.3, 2.6),
        ("मुझे भी सिखा दे भाई! 🔥", 2.6, d3)
    ]

    total_frames = int(total_dur * FPS)
    frames_dir = os.path.join(OUT_DIR, "s1_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)

    def generate_s1_frame(i, t):
        # Background: Modern Tech Gradient with Grid
        img = Image.new("RGBA", (WIDTH, HEIGHT), (14, 18, 30, 255))
        draw = ImageDraw.Draw(img)

        # Subtle cyan-purple glow
        glow_center = (WIDTH // 2, 800)
        draw.ellipse([glow_center[0] - 500, glow_center[1] - 500, glow_center[0] + 500, glow_center[1] + 500], fill=(25, 45, 80, 140))

        # Top Header Badge
        draw.rounded_rectangle([WIDTH//2 - 240, 120, WIDTH//2 + 240, 190], radius=20, fill=(26, 34, 56, 230), outline=(0, 220, 255, 180), width=2)
        draw.text((WIDTH//2, 155), "⚡ MASTER AI TECH HUB ⚡", fill=(0, 240, 255), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30), anchor="mm")

        # Determine Active Speaker and State
        if t < t_turn2:
            # Turn 1: Arjun complaining
            speaker = "arjun"
            turn_rel_t = t - t_turn1
            sub_list = t1_words
            active_char = arjun_stressed
            inactive_char = neha_laptop
            
            # Card: Panic Deadline
            card_alpha = min(1.0, turn_rel_t / 0.5)
            card_y = 260 + int((1.0 - card_alpha) * 30)
            draw_glass_card(draw, [100, card_y, WIDTH - 100, card_y + 240], fill=(35, 20, 25, 230), border=(255, 60, 80, 220))
            draw.text((140, card_y + 45), "🚨 CRITICAL DEADLINE ALERT", fill=(255, 80, 90), font=FONT_CARD_TITLE)
            draw.text((140, card_y + 110), "Client delivery in 8 Hours ⏳", fill=(240, 240, 240), font=FONT_CARD_BODY)
            draw.text((140, card_y + 165), "500 Lines of Unfinished Code", fill=(255, 180, 180), font=FONT_CARD_BODY)

        elif t < t_turn3:
            # Turn 2: Neha schooling Arjun
            speaker = "neha"
            turn_rel_t = t - t_turn2
            sub_list = t2_words
            active_char = neha_point
            inactive_char = arjun_shocked

            # Card: Master AI Deployment
            progress = min(1.0, max(0.0, (turn_rel_t - 1.0) / 3.0))
            draw_glass_card(draw, [100, 260, WIDTH - 100, 530], fill=(18, 32, 45, 240), border=(0, 230, 160, 230))
            draw.text((140, 305), "⚡ MASTER AI AUTONOMOUS DEPLOY", fill=(0, 255, 180), font=FONT_CARD_TITLE)
            draw.text((140, 370), f"Status: Auto-coding & Testing... {int(progress * 100)}%", fill=(220, 240, 240), font=FONT_CARD_BODY)
            # Progress bar
            bar_w = WIDTH - 280
            draw.rounded_rectangle([140, 420, 140 + bar_w, 455], radius=16, fill=(30, 45, 60))
            draw.rounded_rectangle([140, 420, 140 + int(bar_w * progress), 455], radius=16, fill=(0, 240, 150))
            if progress >= 1.0:
                draw.text((140, 475), "✅ DEPLOYMENT COMPLETE (30s)", fill=(0, 255, 120), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34))

        else:
            # Turn 3: Arjun amazed
            speaker = "arjun"
            turn_rel_t = t - t_turn3
            sub_list = t3_words
            active_char = arjun_happy
            inactive_char = neha_peace

            # Card: Mind Blown Stat
            draw_glass_card(draw, [100, 260, WIDTH - 100, 500], fill=(28, 22, 50, 240), border=(220, 100, 255, 230))
            draw.text((140, 310), "🚀 PRODUCTIVITY MULTIPLIER", fill=(230, 120, 255), font=FONT_CARD_TITLE)
            draw.text((140, 380), "30s vs 5 Hours", fill=(255, 255, 255), font=FONT_CARD_METRIC)
            draw.text((140, 440), "Master AI Full-Stack Workflow ⚡", fill=(200, 220, 255), font=FONT_CARD_BODY)

        # Draw Characters (Left = Arjun, Right = Neha)
        # Active speaker bounces subtly and stays 100% opacity, inactive dims
        bounce = math.sin(t * 8.0) * 10 if speaker == "arjun" else 0
        arjun_pos = (60, 880 + int(bounce))
        arjun_img = active_char if speaker == "arjun" else inactive_char
        if speaker != "arjun":
            # Dim inactive
            dim = arjun_img.copy()
            dim.putalpha(Image.eval(dim.split()[-1], lambda a: int(a * 0.70)))
            img.alpha_composite(dim, arjun_pos)
        else:
            img.alpha_composite(arjun_img, arjun_pos)

        # Neha
        neha_bounce = math.sin(t * 8.0) * 10 if speaker == "neha" else 0
        neha_pos = (WIDTH - neha_point.size[0] - 60, 880 + int(neha_bounce))
        neha_img = active_char if speaker == "neha" else inactive_char
        if speaker != "neha":
            dim = neha_img.copy()
            dim.putalpha(Image.eval(dim.split()[-1], lambda a: int(a * 0.70)))
            img.alpha_composite(dim, neha_pos)
        else:
            img.alpha_composite(neha_img, neha_pos)

        # Draw Kinetic Subtitles
        # Find active subtitle phrase
        active_phrase = ""
        for phrase, p_start, p_end in sub_list:
            if p_start <= turn_rel_t <= p_end:
                active_phrase = phrase
                break
        if not active_phrase and sub_list:
            active_phrase = sub_list[-1][0]

        # Draw center punchy subtitle box
        sub_y = 750
        # Box background
        draw.rounded_rectangle([WIDTH//2 - 440, sub_y - 50, WIDTH//2 + 440, sub_y + 60], radius=24, fill=(10, 14, 24, 235), outline=(0, 230, 255, 200), width=3)
        # Glowing text
        draw.text((WIDTH//2, sub_y), active_phrase, fill=(255, 240, 0), font=FONT_SUB_ACTIVE, anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))

        return img.convert("RGB")

    render_video_frames(frames_dir, total_frames, generate_s1_frame)
    out_mp4 = os.path.join(OUT_DIR, "story_demo_1_tech_hustle.mp4")
    encode_mp4(frames_dir, master_wav, out_mp4)
    # Mirror to Artifact
    shutil.copy2(out_mp4, os.path.join(ARTIFACT_DIR, "story_demo_1_tech_hustle.mp4"))
    print(">>> Story 1 Finished & Mirrored!")


# ==============================================================================
# STORY 2: SPACE MYSTERY (Billu Chibi & Dr. Kabir)
# ==============================================================================
def build_story_2():
    print("\n=======================================================")
    print(">>> BUILDING STORY 2: SPACE MYSTERY (Billu & Dr. Kabir)")
    print("=======================================================")

    a1_path = os.path.join(AUDIO_DIR, "s2_billu_1.wav")
    a2_path = os.path.join(AUDIO_DIR, "s2_kabir_2.wav")
    a3_path = os.path.join(AUDIO_DIR, "s2_billu_3.wav")

    d1 = len(sf.read(a1_path)[0]) / 24000.0
    d2 = len(sf.read(a2_path)[0]) / 24000.0
    d3 = len(sf.read(a3_path)[0]) / 24000.0

    t_turn1 = 0.0
    t_turn2 = d1 + 0.35
    t_turn3 = t_turn2 + d2 + 0.35
    total_dur = t_turn3 + d3 + 0.6

    print(f"Timing: Turn 1: {t_turn1:.2f}s, Turn 2: {t_turn2:.2f}s, Turn 3: {t_turn3:.2f}s, Total: {total_dur:.2f}s")

    sfx = [
        (WHOOSH_WAV, 0.05, 0.6),
        (POP_WAV, 1.2, 0.6),
        (WHOOSH_WAV, t_turn2, 0.7),
        (POP_WAV, t_turn2 + 1.2, 0.7),
        (DING_WAV, t_turn2 + 4.5, 0.8),
        (WHOOSH_WAV, t_turn3, 0.6),
        (POP_WAV, t_turn3 + 0.7, 0.7),
    ]

    master_wav = os.path.join(OUT_DIR, "story2_master_audio.wav")
    mix_audio_track(
        [(a1_path, t_turn1), (a2_path, t_turn2), (a3_path, t_turn3)],
        total_dur, sfx, BGM_WAV, master_wav
    )

    # Load Billu & Scientist
    billu_ask = load_rgba(os.path.join(BILLU_LIB, "boy_handsup_clean.png"), max_h=860)
    billu_listen = load_rgba(os.path.join(BILLU_LIB, "boy_listen_clean.png"), max_h=860)
    billu_shocked = load_rgba(os.path.join(BILLU_LIB, "boy_shocked_clean.png"), max_h=860)

    sci_listen = load_rgba(os.path.join(BILLU_LIB, "sci_listen_clean.png"), max_h=860)
    sci_explain = load_rgba(os.path.join(BILLU_LIB, "sci_explain_clean.png"), max_h=860)
    sci_point = load_rgba(os.path.join(BILLU_LIB, "sci_point_clean.png"), max_h=860)

    # Subtitles
    # Turn 1: "प्रोफ़ेसर! क्या सच में अगर हम ब्लैक होल के पास 1 घंटा बिताएँ, तो पृथ्वी पर 7 साल बीत जाएंगे?!"
    t1_words = [
        ("प्रोफ़ेसर! क्या सच में", 0.0, 1.3),
        ("ब्लैक होल के पास 🕳️", 1.3, 2.7),
        ("1 घंटा बिताएँ...", 2.7, 3.8),
        ("तो पृथ्वी पर 7 साल?!", 3.8, d1)
    ]
    # Turn 2: "बिल्कुल बिल्लू! आइंस्टीन के अनुसार ग्रेविटी समय को धीमा कर देती है। तुम जवान रहोगे, पर पृथ्वी पर सब बूढ़े हो जाएंगे!"
    t2_words = [
        ("बिल्कुल बिल्लू!", 0.0, 1.2),
        ("ग्रेविटी समय को ⏳", 1.2, 2.8),
        ("धीमा कर देती है!", 2.8, 4.2),
        ("तुम जवान रहोगे,", 4.2, 5.7),
        ("पर सब बूढ़े हो जाएंगे! 👴", 5.7, d2)
    ]
    # Turn 3: "बाप रे! मतलब वहां 1 दिन की छुट्टी ली, तो धरती पर रिटायरमेंट हो जाएगा?!"
    t3_words = [
        ("बाप रे! 😱", 0.0, 1.2),
        ("1 दिन की छुट्टी ली...", 1.2, 2.6),
        ("तो धरती पर रिटायरमेंट?! 🏖️", 2.6, d3)
    ]

    total_frames = int(total_dur * FPS)
    frames_dir = os.path.join(OUT_DIR, "s2_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)

    def generate_s2_frame(i, t):
        # Cosmic Deep Space Background with Accretion Glow
        img = Image.new("RGBA", (WIDTH, HEIGHT), (6, 8, 20, 255))
        draw = ImageDraw.Draw(img)

        # Rotating Space Accretion Disk Simulation
        angle = t * 0.8
        glow_x = WIDTH // 2 + int(math.sin(angle) * 40)
        glow_y = 650 + int(math.cos(angle) * 20)
        draw.ellipse([glow_x - 420, glow_y - 200, glow_x + 420, glow_y + 200], fill=(220, 100, 20, 90))
        draw.ellipse([glow_x - 220, glow_y - 100, glow_x + 220, glow_y + 100], fill=(255, 200, 50, 140))
        draw.ellipse([glow_x - 120, glow_y - 60, glow_x + 120, glow_y + 60], fill=(0, 0, 0, 255))

        # Top Badge
        draw.rounded_rectangle([WIDTH//2 - 270, 120, WIDTH//2 + 270, 190], radius=20, fill=(16, 20, 40, 235), outline=(255, 170, 0, 200), width=2)
        draw.text((WIDTH//2, 155), "🌌 COSMIC MYSTERY LAB 🌌", fill=(255, 190, 50), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30), anchor="mm")

        # Speaker & Cards
        if t < t_turn2:
            speaker = "billu"
            turn_rel_t = t - t_turn1
            sub_list = t1_words
            active_char = billu_ask
            inactive_char = sci_listen

            # Card: Billu Question
            draw_glass_card(draw, [100, 240, WIDTH - 100, 480], fill=(20, 25, 45, 230), border=(100, 180, 255, 230))
            draw.text((140, 285), "❓ EVENT HORIZON PARADOX", fill=(100, 200, 255), font=FONT_CARD_TITLE)
            draw.text((140, 350), "1 Hour near Black Hole = ?", fill=(255, 255, 255), font=FONT_CARD_METRIC)
            draw.text((140, 420), "General Relativity Question ⏳", fill=(190, 220, 255), font=FONT_CARD_BODY)

        elif t < t_turn3:
            speaker = "kabir"
            turn_rel_t = t - t_turn2
            sub_list = t2_words
            active_char = sci_point
            inactive_char = billu_listen

            # Card: Time Dilation Fact
            draw_glass_card(draw, [100, 240, WIDTH - 100, 510], fill=(30, 20, 15, 240), border=(255, 140, 0, 240))
            draw.text((140, 285), "⏳ GRAVITATIONAL TIME DILATION", fill=(255, 160, 40), font=FONT_CARD_TITLE)
            draw.text((140, 355), "1 Hour = 7 Earth Years!", fill=(255, 240, 120), font=FONT_CARD_METRIC)
            draw.text((140, 435), "Time Dilation Factor: 61,320x Slower", fill=(240, 210, 180), font=FONT_CARD_BODY)

        else:
            speaker = "billu"
            turn_rel_t = t - t_turn3
            sub_list = t3_words
            active_char = billu_shocked
            inactive_char = sci_explain

            # Card: Vacation Paradox
            draw_glass_card(draw, [100, 240, WIDTH - 100, 480], fill=(40, 15, 30, 240), border=(255, 50, 100, 240))
            draw.text((140, 285), "🚨 THE VACATION CALCULATION", fill=(255, 80, 120), font=FONT_CARD_TITLE)
            draw.text((140, 350), "1 Day = 168 Earth Years!", fill=(255, 255, 255), font=FONT_CARD_METRIC)
            draw.text((140, 420), "Direct Retirement Guaranteed! 🏖️", fill=(255, 200, 210), font=FONT_CARD_BODY)

        # Characters
        # Left: Billu
        b_bounce = math.sin(t * 8.0) * 10 if speaker == "billu" else 0
        billu_pos = (50, 900 + int(b_bounce))
        b_img = active_char if speaker == "billu" else inactive_char
        if speaker != "billu":
            dim = b_img.copy()
            dim.putalpha(Image.eval(dim.split()[-1], lambda a: int(a * 0.70)))
            img.alpha_composite(dim, billu_pos)
        else:
            img.alpha_composite(b_img, billu_pos)

        # Right: Dr. Kabir
        k_bounce = math.sin(t * 8.0) * 8 if speaker == "kabir" else 0
        kabir_pos = (WIDTH - sci_point.size[0] - 40, 890 + int(k_bounce))
        k_img = active_char if speaker == "kabir" else inactive_char
        if speaker != "kabir":
            dim = k_img.copy()
            dim.putalpha(Image.eval(dim.split()[-1], lambda a: int(a * 0.70)))
            img.alpha_composite(dim, kabir_pos)
        else:
            img.alpha_composite(k_img, kabir_pos)

        # Subtitles
        active_phrase = ""
        for phrase, p_start, p_end in sub_list:
            if p_start <= turn_rel_t <= p_end:
                active_phrase = phrase
                break
        if not active_phrase and sub_list:
            active_phrase = sub_list[-1][0]

        sub_y = 750
        draw.rounded_rectangle([WIDTH//2 - 440, sub_y - 50, WIDTH//2 + 440, sub_y + 60], radius=24, fill=(10, 10, 25, 235), outline=(255, 190, 0, 210), width=3)
        draw.text((WIDTH//2, sub_y), active_phrase, fill=(0, 255, 230), font=FONT_SUB_ACTIVE, anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))

        return img.convert("RGB")

    render_video_frames(frames_dir, total_frames, generate_s2_frame)
    out_mp4 = os.path.join(OUT_DIR, "story_demo_2_space_mystery.mp4")
    encode_mp4(frames_dir, master_wav, out_mp4)
    shutil.copy2(out_mp4, os.path.join(ARTIFACT_DIR, "story_demo_2_space_mystery.mp4"))
    print(">>> Story 2 Finished & Mirrored!")

if __name__ == "__main__":
    build_story_1()
    build_story_2()
    print("\n>>> ALL NEW STORY DEMOS COMPLETE! <<<")
