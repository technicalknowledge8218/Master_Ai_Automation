"""
render_pro_character_viral_reel.py
Builds a true commercial-grade 2D character viral reel featuring:
- Brand new character 'Dev' (Modern AI Creator in matte black streetwear bomber & cyan tee)
- Real Audio RMS-driven Viseme Lip-Sync (mouth opens on speech energy, closes on pauses)
- Spring Physics Entry (ease_out_back) & Natural Breathing/Body Sway
- Dynamic Camera Punch-Ins (Wide -> Punch-in -> Reaction -> Heroic CTA)
- Authentic macOS Terminal Window with Live Character Typing & Blinking Cursor
- Kinetic Alex Hormozi Neon Word Subtitles
- Multi-track Broadcast Audio with ducked BGM + SFX Whooshes, Pops, Chimes
"""

import os
import math
import shutil
import subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG = r"F:\Master AI\.venv_py310\lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
DEV_LIB = r"F:\Master AI\CHARACTER_LIBRARY\dev_creator"
AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\dev_story"
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase"
ARTIFACT_DIR = r"<ARTIFACT_DIR>"

SFX_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx"
BGM_WAV = os.path.join(SFX_DIR, "lofi_bg_track.wav")
WHOOSH_WAV = os.path.join(SFX_DIR, "whoosh.wav")
POP_WAV = os.path.join(SFX_DIR, "pop.wav")
DING_WAV = os.path.join(SFX_DIR, "ding.wav")

FPS = 24
WIDTH = 1080
HEIGHT = 1920

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 66)
FONT_BODY = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 36)
FONT_CODE = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 32)
FONT_METRIC = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 74)

def ease_out_back(x):
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * math.pow(x - 1.0, 3) + c1 * math.pow(x - 1.0, 2)

def load_sprite(path, target_h=1100):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    ratio = target_h / h
    return im.resize((int(w * ratio), target_h), Image.Resampling.LANCZOS)

def draw_glass_card(draw, rect, fill=(18, 22, 36, 230), border=(0, 220, 255, 200), radius=26, border_w=3):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=border, width=border_w)

def draw_macos_terminal(draw, rect, cmd_text, output_lines, cursor_on=True):
    x0, y0, x1, y1 = rect
    # Terminal Window
    draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(12, 14, 22, 245), outline=(60, 75, 110, 200), width=2)
    # Title bar
    draw.rounded_rectangle([x0, y0, x1, y0 + 55], radius=20, fill=(22, 26, 38, 255))
    draw.rectangle([x0, y0 + 35, x1, y0 + 55], fill=(22, 26, 38, 255))
    # Traffic lights
    draw.ellipse([x0 + 20, y0 + 18, x0 + 38, y0 + 36], fill=(255, 95, 86))
    draw.ellipse([x0 + 48, y0 + 18, x0 + 66, y0 + 36], fill=(255, 189, 46))
    draw.ellipse([x0 + 76, y0 + 18, x0 + 94, y0 + 36], fill=(39, 201, 63))
    # Terminal title
    draw.text((x0 + (x1 - x0)//2, y0 + 27), "master-ai — bash — 1080x1920", fill=(140, 155, 180), font=ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22), anchor="mm")

    # Command line
    curr_y = y0 + 85
    draw.text((x0 + 25, curr_y), "$ " + cmd_text + (" █" if cursor_on else ""), fill=(0, 255, 200), font=FONT_CODE)
    curr_y += 50

    # Outputs
    for line, color in output_lines:
        if curr_y + 40 > y1:
            break
        draw.text((x0 + 25, curr_y), line, fill=color, font=FONT_CODE)
        curr_y += 45

def build_master_audio(speech_wav, total_dur, sfx_list, bgm_path, out_wav):
    sr = 24000
    total_samples = int(total_dur * sr)
    master = np.zeros(total_samples, dtype=np.float32)

    # 1. Voice
    speech, s_sr = sf.read(speech_wav)
    if len(speech.shape) > 1:
        speech = speech.mean(axis=1)
    s_len = min(len(speech), total_samples)
    master[:s_len] += speech[:s_len] * 1.05

    # Voice mask for ducking
    v_mask = np.zeros(total_samples, dtype=np.float32)
    v_mask[:s_len] = np.abs(speech[:s_len])
    window = int(sr * 0.3)
    smoothed = np.convolve(v_mask, np.ones(window)/window, mode='same')
    duck_gain = np.where(smoothed > 0.02, 0.12, 0.28)

    # 2. BGM
    if os.path.exists(bgm_path):
        bgm, _ = sf.read(bgm_path)
        if len(bgm.shape) > 1:
            bgm = bgm.mean(axis=1)
        repeats = int(np.ceil(total_samples / len(bgm)))
        bgm_looped = np.tile(bgm, repeats)[:total_samples]
        master += bgm_looped * duck_gain

    # 3. SFX
    for sfx_p, t_sec, vol in sfx_list:
        if os.path.exists(sfx_p):
            s_data, _ = sf.read(sfx_p)
            if len(s_data.shape) > 1:
                s_data = s_data.mean(axis=1)
            st = int(t_sec * sr)
            en = min(st + len(s_data), total_samples)
            if en > st:
                master[st:en] += s_data[:en - st] * vol

    # Peak normalization
    peak = np.max(np.abs(master))
    if peak > 0.98:
        master = master * (0.95 / peak)

    sf.write(out_wav, master, sr)
    print(f"Master Broadcast Audio Exported: {out_wav}")

def main():
    print("\n==================================================================")
    print(">>> RENDERING PRO 2D CHARACTER VIRAL REEL (DEV CREATOR EDITION) <<<")
    print("==================================================================")

    speech_wav = os.path.join(AUDIO_DIR, "dev_full_speech.wav")
    data, sr = sf.read(speech_wav)
    total_dur = len(data) / sr
    total_frames = int(total_dur * FPS)
    print(f"Total Speech Duration: {total_dur:.2f}s | Total Frames: {total_frames}")

    # Compute RMS per frame for speech lip-sync
    frame_samples = sr // FPS
    rms_per_frame = []
    for i in range(total_frames):
        st = i * frame_samples
        en = min(st + frame_samples, len(data))
        chunk = data[st:en]
        rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0.0
        rms_per_frame.append(rms)

    # SFX events across the 31 seconds
    sfx = [
        (WHOOSH_WAV, 0.05, 0.6),    # Intro spring slide whoosh
        (POP_WAV, 2.2, 0.6),        # 90% Stat reveal pop
        (WHOOSH_WAV, 7.8, 0.7),     # Scene 2 jump cut to Terminal
        (POP_WAV, 10.5, 0.6),       # Terminal 60s execution
        (DING_WAV, 13.8, 0.8),      # Terminal deployment success chime
        (WHOOSH_WAV, 15.6, 0.7),    # Scene 3 transition to Master AI Solution
        (POP_WAV, 18.2, 0.6),       # Solution card reveal
        (WHOOSH_WAV, 24.8, 0.7),    # Scene 4 Climax cut
        (DING_WAV, 28.5, 0.9),      # Climax CTA bell
    ]

    master_audio = os.path.join(OUT_DIR, "dev_viral_master_audio.wav")
    build_master_audio(speech_wav, total_dur, sfx, BGM_WAV, master_audio)

    # Load Dev Character Sprites
    dev_resting = load_sprite(os.path.join(DEV_LIB, "dev_resting.png"), target_h=1120)
    dev_speaking = load_sprite(os.path.join(DEV_LIB, "dev_speaking.png"), target_h=1120)
    dev_shocked = load_sprite(os.path.join(DEV_LIB, "dev_shocked.png"), target_h=1120)
    dev_thumbsup = load_sprite(os.path.join(DEV_LIB, "dev_thumbsup.png"), target_h=1120)

    # Subtitles timeline (Alex Hormozi style)
    subtitles = [
        # Scene 1: Hook (0s - 7.8s)
        (0.0, 1.4, "अगर आप 2026 में"),
        (1.4, 2.8, "सिर्फ नॉर्मल कोडिंग सीख रहे हैं,"),
        (2.8, 4.2, "तो सावधान हो जाइए! ⚠️"),
        (4.2, 5.8, "90% कंपनियाँ अब"),
        (5.8, 7.8, "AI एजेंट्स को हायर कर रही हैं! 🤖"),
        # Scene 2: Problem (7.8s - 15.6s)
        (7.8, 9.8, "क्योंकि जो काम 3 डेवलपर्स"),
        (9.8, 11.6, "1 पूरे हफ़्ते में करते थे... ⏳"),
        (11.6, 13.6, "वही काम एक अकेला AI एजेंट"),
        (13.6, 15.6, "सिर्फ 60 सेकंड में लाइव कर देता है! ⚡"),
        # Scene 3: Solution (15.6s - 24.8s)
        (15.6, 17.6, "तो क्या कोडिंग छोड़ दें?"),
        (17.6, 19.4, "बिल्कुल नहीं! ❌"),
        (19.4, 21.8, "आपको सिर्फ कोड लिखने वाला नहीं,"),
        (21.8, 24.8, "Master AI आर्किटेक्ट बनना होगा! 🚀"),
        # Scene 4: Climax & CTA (24.8s - 31.3s)
        (24.8, 27.2, "क्योंकि भविष्य कोडर्स का नहीं,"),
        (27.2, 29.4, "AI को कंट्रोल करने वालों का है! 🔥"),
        (29.4, total_dur, "फॉलो कर लो अभी! ✅")
    ]

    frames_dir = os.path.join(OUT_DIR, "dev_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)

    print(">>> Rendering 24fps Video Frames with Audio-Driven Visemes & Spring Physics...")

    for i in range(total_frames):
        t = i / FPS
        rms = rms_per_frame[i]

        # ------------------------------------------------------------------
        # 1. Background Setup (Cyber-Tech Dark Space with Subtle Gradient)
        # ------------------------------------------------------------------
        img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 14, 24, 255))
        draw = ImageDraw.Draw(img)

        # Dynamic ambient backlight pulsing with speech energy
        glow_alpha = int(80 + rms * 250)
        glow_rad = int(450 + rms * 150)
        cx, cy = WIDTH // 2, 850
        draw.ellipse([cx - glow_rad, cy - glow_rad, cx + glow_rad, cy + glow_rad], fill=(20, 50, 95, min(200, glow_alpha)))

        # Header Badge
        draw.rounded_rectangle([WIDTH//2 - 260, 110, WIDTH//2 + 260, 180], radius=18, fill=(20, 26, 42, 230), outline=(0, 240, 255, 180), width=2)
        draw.text((WIDTH//2, 145), "⚡ MASTER AI FUTURE TECH ⚡", fill=(0, 240, 255), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28), anchor="mm")

        # ------------------------------------------------------------------
        # 2. Scene-Specific UI Elements & Visual B-Roll
        # ------------------------------------------------------------------
        if t < 7.8:
            # SCENE 1: THE HOOK
            # Floating Alert Card
            draw_glass_card(draw, [90, 230, WIDTH - 90, 480], fill=(30, 20, 30, 235), border=(255, 70, 90, 220))
            draw.text((130, 275), "🚨 2026 INDUSTRY REPORT", fill=(255, 90, 110), font=FONT_TITLE)
            draw.text((130, 345), "90% Shift to Autonomous AI", fill=(255, 255, 255), font=FONT_METRIC)
            draw.text((130, 420), "Junior Developer Hiring Disruption", fill=(240, 200, 210), font=FONT_BODY)

            # Character Camera Framing: Medium shot sliding in with spring physics
            entry_p = min(1.0, t / 0.55)
            eased_y = ease_out_back(entry_p)
            char_base_y = int(HEIGHT - 100 - (1050 * eased_y))
            char_scale = 1.0

        elif t < 15.6:
            # SCENE 2: TERMINAL LIVE TYPING & COMPARISON
            # Live typing macOS terminal
            rel_t = t - 7.8
            full_cmd = "npx master-ai build --agent=autonomous"
            chars = int(min(len(full_cmd), len(full_cmd) * (rel_t / 2.5)))
            shown_cmd = full_cmd[:chars]

            terminal_outputs = []
            if rel_t > 2.2:
                terminal_outputs.append(("[*] Analyzing repository schema...", (120, 170, 255)))
            if rel_t > 3.8:
                terminal_outputs.append(("[✓] 2,400 LOC generated in 12s", (0, 255, 180)))
            if rel_t > 5.2:
                terminal_outputs.append(("[✓] All 48 unit tests PASSED", (0, 255, 120)))
            if rel_t > 6.5:
                terminal_outputs.append(("[🚀] DEPLOYED TO CLUSTER (Total: 60s)", (255, 220, 0)))

            draw_macos_terminal(draw, [80, 220, WIDTH - 80, 570], shown_cmd, terminal_outputs, cursor_on=((int(t * 4) % 2) == 0))

            # Character Camera Framing: Camera punch-in (1.18x) on the right side
            char_base_y = 780
            char_scale = 1.15

        elif t < 24.8:
            # SCENE 3: THE MASTER ARCHITECT SOLUTION
            draw_glass_card(draw, [90, 230, WIDTH - 90, 500], fill=(16, 28, 48, 240), border=(0, 230, 180, 230))
            draw.text((130, 275), "⚡ THE NEW PARADIGM", fill=(0, 255, 180), font=FONT_TITLE)
            draw.text((130, 345), "Master AI Architect", fill=(255, 255, 255), font=FONT_METRIC)
            draw.text((130, 425), "Command Systems • Orchestrate Swarms 🚀", fill=(190, 230, 255), font=FONT_BODY)

            char_base_y = 820
            char_scale = 1.05

        else:
            # SCENE 4: CLIMAX & CTA
            draw_glass_card(draw, [90, 230, WIDTH - 90, 480], fill=(32, 22, 54, 240), border=(230, 100, 255, 230))
            draw.text((130, 275), "🔥 OWN THE FUTURE", fill=(230, 120, 255), font=FONT_TITLE)
            draw.text((130, 345), "Master AI Ecosystem", fill=(255, 255, 255), font=FONT_METRIC)
            draw.text((130, 420), "Tap Follow For Daily AI Superpowers ⚡", fill=(230, 220, 255), font=FONT_BODY)

            char_base_y = 760
            char_scale = 1.25

        # ------------------------------------------------------------------
        # 3. Dynamic Character Sprite Selection with Real Audio Visemes
        # ------------------------------------------------------------------
        # Select active sprite based on speech RMS energy & scene context
        is_speaking = (rms > 0.024)

        if t >= 27.5:
            # Climax triumph
            chosen_sprite = dev_thumbsup
        elif (10.0 <= t <= 12.5) or (2.8 <= t <= 4.2):
            # Shock moments (1 week vs 60s, or warning hook)
            chosen_sprite = dev_shocked
        else:
            # Normal speech: Viseme switching!
            chosen_sprite = dev_speaking if is_speaking else dev_resting

        # ------------------------------------------------------------------
        # 4. Secondary Motion: Natural Breathing & Body Sway
        # ------------------------------------------------------------------
        breath = math.sin(t * 3.5) * 0.015
        sway_deg = math.sin(t * 2.2) * 1.5

        sw, sh = chosen_sprite.size
        render_w = int(sw * char_scale)
        render_h = int(sh * char_scale * (1.0 + breath))

        sprite_scaled = chosen_sprite.resize((render_w, render_h), Image.Resampling.LANCZOS)
        sprite_rotated = sprite_scaled.rotate(sway_deg, resample=Image.Resampling.BICUBIC, expand=True)

        # Place character (Center-bottom or slightly offset)
        char_x = (WIDTH - sprite_rotated.size[0]) // 2
        char_y = char_base_y
        img.alpha_composite(sprite_rotated, (char_x, char_y))

        # ------------------------------------------------------------------
        # 5. Kinetic Alex Hormozi Subtitles (Word Bursts + Neon Glow)
        # ------------------------------------------------------------------
        current_sub = ""
        for s_start, s_end, text in subtitles:
            if s_start <= t < s_end:
                current_sub = text
                break

        if current_sub:
            sub_y = 710
            # Rounded caption pill
            draw.rounded_rectangle([WIDTH//2 - 450, sub_y - 50, WIDTH//2 + 450, sub_y + 55], radius=24, fill=(8, 10, 18, 240), outline=(0, 240, 255, 210), width=3)
            # Glowing high-contrast neon text with shadow
            draw.text((WIDTH//2, sub_y), current_sub, fill=(255, 240, 0), font=FONT_SUB, anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))

        # Save frame
        rgb_frame = img.convert("RGB")
        rgb_frame.save(os.path.join(frames_dir, f"frame_{i:05d}.jpg"), quality=93)

        if i % 100 == 0 or i == total_frames - 1:
            print(f"  Rendered Frame {i}/{total_frames} ({t:.1f}s) | Viseme: {'SPEAK' if is_speaking else 'REST'} | RMS: {rms:.3f}")

    # ------------------------------------------------------------------
    # 6. Encode Final MP4 via FFmpeg
    # ------------------------------------------------------------------
    out_mp4 = os.path.join(OUT_DIR, "pro_dev_viral_reel.mp4")
    cmd = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", master_audio,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    print("\n>>> Encoding Final Pro Viral MP4 via FFmpeg...")
    subprocess.run(cmd, check=True)
    print(f"Video Exported: {out_mp4}")

    # Mirror to Artifact
    artifact_mp4 = os.path.join(ARTIFACT_DIR, "pro_dev_viral_reel.mp4")
    shutil.copy2(out_mp4, artifact_mp4)
    print(f">>> Mirrored to Artifacts: {artifact_mp4}")
    print("\n>>> PRO 2D CHARACTER VIRAL REEL PRODUCTION COMPLETE! <<<")

if __name__ == "__main__":
    main()
