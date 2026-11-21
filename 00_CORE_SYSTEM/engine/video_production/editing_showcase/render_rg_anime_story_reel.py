"""
render_rg_anime_story_reel.py
Builds the Master Test Demo in 'Style C: RG Bucket List / Semi-Anime Comic Style':
- Story: "रात के 2 बजे का वो हॉस्टल कॉल" (The 2:00 AM Hostel Call)
- Character: 'Bunty' (Semi-Anime Style C with sharp jawline, textured hair, anime eyes)
- Audio RMS Viseme Lip-Sync (Neutral -> Speaking -> On Phone -> Terrified Shock)
- Atmospheric 2:00 AM Anime Room Background (Moonlight + Lamp + Clock)
- Dynamic Camera Angles (Wide -> Mid + Manga Call Panel -> Extreme Shock Punch-in -> Door Climax)
- Diegetic Sound Design (Ducked Moody Score + Phone Chime + Deep Bass Drop + 3 Realistic Door Knocks)
- Clean Netflix/Anime Style Bottom Subtitles
"""

import os
import math
import shutil
import subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG = r"F:\Master AI\.venv_py310\lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
BUNTY_LIB = r"F:\Master AI\CHARACTER_LIBRARY\rg_bunty"
BG_IMAGE_PATH = r"F:\Master AI\CHARACTER_LIBRARY\rg_anime_room_bg.jpg"
AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\rg_story"
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase"
ARTIFACT_DIR = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

SFX_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx"
BGM_WAV = os.path.join(SFX_DIR, "lofi_bg_track.wav")
WHOOSH_WAV = os.path.join(SFX_DIR, "whoosh.wav")
POP_WAV = os.path.join(SFX_DIR, "pop.wav")
KNOCKS_WAV = os.path.join(AUDIO_DIR, "knocks.wav")
BASS_DROP_WAV = os.path.join(AUDIO_DIR, "bass_drop.wav")

FPS = 24
WIDTH = 1080
HEIGHT = 1920

# Fonts
FONT_NETFLIX_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 46)
FONT_NETFLIX_SUB_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 48)
FONT_PANEL_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 36)
FONT_PANEL_TEXT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)

def load_sprite(path, target_h=1200):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    ratio = target_h / h
    return im.resize((int(w * ratio), target_h), Image.Resampling.LANCZOS)

def draw_netflix_subtitle(draw, text, y_pos=1680, is_highlight=False):
    # Calculate text width
    bbox = draw.textbbox((WIDTH // 2, y_pos), text, font=FONT_NETFLIX_SUB_BOLD if is_highlight else FONT_NETFLIX_SUB, anchor="mm")
    pad_x = 36
    pad_y = 16
    pill_rect = [bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y]
    # Subtle dark translucent backing
    draw.rounded_rectangle(pill_rect, radius=18, fill=(8, 10, 18, 210), outline=(255, 200, 50, 160) if is_highlight else (40, 50, 75, 120), width=2)
    # Text
    fill_color = (255, 230, 80) if is_highlight else (245, 245, 250)
    draw.text((WIDTH // 2, y_pos), text, fill=fill_color, font=FONT_NETFLIX_SUB_BOLD if is_highlight else FONT_NETFLIX_SUB, anchor="mm")

def draw_manga_phone_panel(draw, rect, rel_t):
    x0, y0, x1, y1 = rect
    # Manga Panel Outer Frame
    draw.rectangle([x0, y0, x1, y1], fill=(12, 16, 26, 240), outline=(220, 230, 255, 240), width=5)
    # Header
    draw.rectangle([x0, y0, x1, y0 + 50], fill=(240, 60, 70, 255))
    draw.text((x0 + (x1 - x0)//2, y0 + 25), "INCOMING CALL", fill=(255, 255, 255), font=FONT_PANEL_HEADER, anchor="mm")

    # Smartphone graphic inside panel
    phone_cx = x0 + (x1 - x0)//2
    phone_cy = y0 + 240
    # Vibration wobble
    vib = math.sin(rel_t * 30.0) * 4 if (rel_t % 1.5 < 0.8) else 0
    px0, py0, px1, py1 = phone_cx - 130 + vib, phone_cy - 160, phone_cx + 130 + vib, phone_cy + 160
    draw.rounded_rectangle([px0, py0, px1, py1], radius=24, fill=(20, 24, 35), outline=(0, 200, 255), width=3)
    # Caller avatar
    draw.ellipse([phone_cx - 45 + vib, phone_cy - 100, phone_cx + 45 + vib, phone_cy - 10], fill=(50, 75, 120), outline=(200, 220, 255), width=2)
    draw.text((phone_cx + vib, phone_cy - 55), "👤", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 36), anchor="mm")
    # Caller Name
    draw.text((phone_cx + vib, phone_cy + 25), "ROHIT (Roommate)", fill=(255, 255, 255), font=FONT_PANEL_TEXT, anchor="mm")
    draw.text((phone_cx + vib, phone_cy + 75), "📞 Calling...", fill=(0, 255, 180), font=ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26), anchor="mm")
    # Accept / Reject buttons
    draw.ellipse([phone_cx - 80 + vib, phone_cy + 115, phone_cx - 30 + vib, phone_cy + 165], fill=(220, 40, 40))
    draw.ellipse([phone_cx + 30 + vib, phone_cy + 115, phone_cx + 80 + vib, phone_cy + 165], fill=(35, 180, 50))

def draw_manga_door_panel(draw, rect, rel_t):
    x0, y0, x1, y1 = rect
    # Manga Panel Outer Frame
    draw.rectangle([x0, y0, x1, y1], fill=(10, 10, 18, 245), outline=(255, 60, 60, 240), width=5)
    # Header
    draw.rectangle([x0, y0, x1, y0 + 50], fill=(200, 30, 40, 255))
    draw.text((x0 + (x1 - x0)//2, y0 + 25), "ROOM DOOR (OUTSIDE)", fill=(255, 255, 255), font=FONT_PANEL_HEADER, anchor="mm")

    # Dark Wooden Door Silhouette
    dx0, dy0, dx1, dy1 = x0 + 40, y0 + 75, x1 - 40, y1 - 30
    draw.rectangle([dx0, dy0, dx1, dy1], fill=(30, 20, 18), outline=(60, 40, 35), width=4)
    # Door Handle
    draw.ellipse([dx1 - 35, dy0 + 190, dx1 - 15, dy0 + 210], fill=(180, 160, 80))

    # Shock waves / Knock impact circles
    # Knock times relative to this scene (Scene starts at 29.5s, knocks at 31.0, 32.2, 33.4 => rel_t: 1.5, 2.7, 3.9)
    for k_time in [1.5, 2.7, 3.9]:
        dt = rel_t - k_time
        if 0 <= dt <= 0.6:
            rad = int(dt * 120)
            alpha_k = int((1.0 - dt/0.6) * 220)
            k_im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            k_draw = ImageDraw.Draw(k_im)
            k_draw.ellipse([dx0 + 120 - rad, dy0 + 150 - rad, dx0 + 120 + rad, dy0 + 150 + rad], outline=(255, 80, 80, alpha_k), width=4)
            k_draw.text((dx0 + 120, dy0 + 150), "KNOCK!", fill=(255, 240, 100, alpha_k), font=FONT_PANEL_HEADER, anchor="mm")
            draw.bitmap((0, 0), k_im)

def mix_broadcast_audio(speech_wav, total_dur, sfx_events, bgm_path, out_wav):
    sr = 24000
    total_samples = int(total_dur * sr)
    master = np.zeros(total_samples, dtype=np.float32)

    # 1. Voice
    speech, _ = sf.read(speech_wav)
    if len(speech.shape) > 1:
        speech = speech.mean(axis=1)
    s_len = min(len(speech), total_samples)
    master[:s_len] += speech[:s_len] * 1.05

    # 2. Ducked BGM
    if os.path.exists(bgm_path):
        bgm, _ = sf.read(bgm_path)
        if len(bgm.shape) > 1:
            bgm = bgm.mean(axis=1)
        repeats = int(np.ceil(total_samples / len(bgm)))
        bgm_looped = np.tile(bgm, repeats)[:total_samples]
        
        # Smooth ducking
        v_mask = np.abs(speech[:s_len])
        win = int(sr * 0.25)
        smoothed = np.convolve(v_mask, np.ones(win)/win, mode='same')
        gain = np.where(smoothed > 0.02, 0.12, 0.26)
        master[:s_len] += bgm_looped[:s_len] * gain

    # 3. SFX Events
    for sfx_path, t_sec, vol in sfx_events:
        if os.path.exists(sfx_path):
            s_data, _ = sf.read(sfx_path)
            if len(s_data.shape) > 1:
                s_data = s_data.mean(axis=1)
            st = int(t_sec * sr)
            en = min(st + len(s_data), total_samples)
            if en > st:
                master[st:en] += s_data[:en - st] * vol

    # Normalize
    peak = np.max(np.abs(master))
    if peak > 0.98:
        master = master * (0.95 / peak)

    sf.write(out_wav, master, sr)
    print(f"Broadcast Master Audio Exported: {out_wav} (Dur: {total_dur:.2f}s)")

def main():
    print("\n==================================================================")
    print(">>> RENDERING MASTER 2D ANIME STORY REEL (RG BUCKET LIST STYLE) <<<")
    print("==================================================================")

    speech_wav = os.path.join(AUDIO_DIR, "rg_story_speech.wav")
    data, sr = sf.read(speech_wav)
    total_dur = len(data) / sr
    total_frames = int(total_dur * FPS)
    print(f"Total Audio Duration: {total_dur:.2f}s | Total Frames: {total_frames}")

    # Compute RMS per frame for speech lip-sync
    frame_samples = sr // FPS
    rms_per_frame = []
    for i in range(total_frames):
        st = i * frame_samples
        en = min(st + frame_samples, len(data))
        chunk = data[st:en]
        rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0.0
        rms_per_frame.append(rms)

    # SFX Event Timeline
    sfx = [
        (WHOOSH_WAV, 0.05, 0.5),        # Scene 1 open
        (POP_WAV, 4.8, 0.6),            # Phone screen lights up
        (WHOOSH_WAV, 7.5, 0.6),         # Scene 2 cut (Phone Call)
        (BASS_DROP_WAV, 16.5, 0.9),     # Dramatic Bass Drop at warning!
        (WHOOSH_WAV, 29.5, 0.6),        # Scene 4 cut to door
        (KNOCKS_WAV, 31.0, 1.0),        # 3 Door Knocks at 31s
    ]

    master_audio = os.path.join(OUT_DIR, "rg_story_master_audio.wav")
    mix_broadcast_audio(speech_wav, total_dur, sfx, BGM_WAV, master_audio)

    # Load Assets
    room_bg = Image.open(BG_IMAGE_PATH).convert("RGB")
    bunty_neutral = load_sprite(os.path.join(BUNTY_LIB, "bunty_neutral.png"), target_h=1180)
    bunty_speaking = load_sprite(os.path.join(BUNTY_LIB, "bunty_speaking.png"), target_h=1180)
    bunty_shocked = load_sprite(os.path.join(BUNTY_LIB, "bunty_shocked.png"), target_h=1180)
    bunty_phone = load_sprite(os.path.join(BUNTY_LIB, "bunty_phone.png"), target_h=1180)

    # Netflix-Style Subtitle Script Timeline
    subtitles = [
        # Scene 1: The Midnight Setup (0.0s - 7.5s)
        (0.0, 3.8, "ये बात पिछले महीने की है... रात के 2:00 बजे हॉस्टल का कमरा।", False),
        (3.8, 7.5, "तभी अचानक मेरे फोन की स्क्रीन जली... 📱", True),
        # Scene 2: The Call & Manga Panel (7.5s - 16.2s)
        (7.5, 11.2, "स्क्रीन पर नाम चमक रहा था—'रोहित' (रूममेट)।", False),
        (11.2, 13.8, "रोहित 10 मिनट पहले ही नीचे मैगी लेने गया था...", False),
        (13.8, 16.2, "मैंने फोन उठाया—'हाँ भाई, मैगी मिली क्या?'", False),
        # Scene 3: The Terrified Warning (16.2s - 29.5s)
        (16.2, 20.8, "लेकिन दूसरी तरफ से रोहित की कांपती आवाज़ आई...", True),
        (20.8, 25.2, "'बंटी! कमरे का दरवाज़ा तुरंत अंदर से बंद कर ले!' ⚠️", True),
        (25.2, 29.5, "'मैं अभी बाहर हूँ... पर कोई तेरे कमरे के बाहर खड़ा है!'", True),
        # Scene 4: The 3 Knocks (29.5s - 38.27s)
        (29.5, 33.5, "और तभी... कमरे के दरवाज़े पर धीरे से तीन बार दस्तक हुई—", True),
        (33.5, 36.2, "टक... टक... टक... 🚪", True),
        (36.2, total_dur, "पार्ट 2 के लिए फॉलो कर लो अभी! ✅", False)
    ]

    frames_dir = os.path.join(OUT_DIR, "rg_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)

    print(">>> Rendering RG Bucket List Semi-Anime Video Frames...")

    for i in range(total_frames):
        t = i / FPS
        rms = rms_per_frame[i]
        is_speaking = (rms > 0.022)

        # -------------------------------------------------------------
        # 1. Base Environment Setup
        # -------------------------------------------------------------
        frame = room_bg.copy()

        # Dynamic lighting shift:
        # In Scene 3 (16.2s - 29.5s), ambient shifts to dark crimson suspense
        if 16.2 <= t < 29.5:
            # Suspense vignette and red rim glow
            suspense_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (40, 5, 12, 110))
            frame.paste(Image.alpha_composite(frame.convert("RGBA"), suspense_overlay).convert("RGB"))

        draw = ImageDraw.Draw(frame)

        # -------------------------------------------------------------
        # 2. Camera Angles, Character Placement & Sprite Visemes
        # -------------------------------------------------------------
        breath = math.sin(t * 3.2) * 0.015
        sway = math.sin(t * 2.0) * 1.2

        if t < 7.5:
            # SCENE 1: WIDE SETUP SHOT
            # Bunty sitting/standing near desk on right side
            scale = 1.0
            chosen_sprite = bunty_speaking if is_speaking else bunty_neutral
            sw, sh = chosen_sprite.size
            sprite_res = chosen_sprite.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            sprite_rot = sprite_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            char_pos = (WIDTH - sprite_rot.size[0] - 60, 720)
            frame.convert("RGBA").paste(sprite_rot, char_pos, sprite_rot)
            # Reconvert to RGB
            frame.paste(sprite_rot, char_pos, sprite_rot)

            # Top Cinematic Title Card
            draw.text((WIDTH // 2, 90), "HOSTEL NIGHT FILES • EPISODE 1", fill=(140, 160, 200), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24), anchor="mm")

        elif t < 16.2:
            # SCENE 2: MID SHOT + MANGA PHONE PANEL
            scale = 1.12
            # On phone call
            chosen_sprite = bunty_phone
            sw, sh = chosen_sprite.size
            sprite_res = chosen_sprite.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            sprite_rot = sprite_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            # Bunty on Left
            char_pos = (40, 680)
            frame.paste(sprite_rot, char_pos, sprite_rot)

            # Manga Split Panel on Right
            rel_t = t - 7.5
            draw_manga_phone_panel(draw, [WIDTH - 440, 420, WIDTH - 40, 880], rel_t)

        elif t < 29.5:
            # SCENE 3: DRAMATIC EXTREME CLOSE-UP PUNCH-IN (SHOCK)
            scale = 1.40
            # Terrified shock reaction with trembling
            shiver_x = int(math.sin(t * 40.0) * 3)
            chosen_sprite = bunty_shocked
            sw, sh = chosen_sprite.size
            sprite_res = chosen_sprite.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            sprite_rot = sprite_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            # Centered close-up
            char_pos = ((WIDTH - sprite_rot.size[0]) // 2 + shiver_x, 620)
            frame.paste(sprite_rot, char_pos, sprite_rot)

            # Dramatic manga speed-lines / shock vignette on corners
            draw.text((WIDTH // 2, 120), "⚠️ CRITICAL WARNING", fill=(255, 60, 70), font=FONT_PANEL_HEADER, anchor="mm")

        else:
            # SCENE 4: CLIMAX & 3 KNOCKS ON THE DOOR
            scale = 1.15
            chosen_sprite = bunty_shocked
            sw, sh = chosen_sprite.size
            sprite_res = chosen_sprite.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            sprite_rot = sprite_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            # Bunty on Left, frozen
            char_pos = (30, 690)
            frame.paste(sprite_rot, char_pos, sprite_rot)

            # Manga Door Panel on Right
            rel_t = t - 29.5
            draw_manga_door_panel(draw, [WIDTH - 460, 380, WIDTH - 30, 920], rel_t)

            # Cliffhanger Outro Badge
            if t > 35.5:
                draw.rounded_rectangle([WIDTH//2 - 280, 110, WIDTH//2 + 280, 180], radius=16, fill=(15, 18, 30, 235), outline=(255, 200, 50, 220), width=2)
                draw.text((WIDTH // 2, 145), "🚪 PART 2 COMING SOON", fill=(255, 215, 0), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26), anchor="mm")

        # -------------------------------------------------------------
        # 3. Netflix / Anime Style Subtitles (Bottom Third)
        # -------------------------------------------------------------
        current_sub = ""
        is_highlight = False
        for s_start, s_end, text, hl in subtitles:
            if s_start <= t < s_end:
                current_sub = text
                is_highlight = hl
                break

        if current_sub:
            draw_netflix_subtitle(draw, current_sub, y_pos=1680, is_highlight=is_highlight)

        # Save Frame
        frame.save(os.path.join(frames_dir, f"frame_{i:05d}.jpg"), quality=93)
        if i % 100 == 0 or i == total_frames - 1:
            print(f"  Rendered Frame {i}/{total_frames} ({t:.1f}s) | Scene: {1 if t<7.5 else (2 if t<16.2 else (3 if t<29.5 else 4))}")

    # -------------------------------------------------------------
    # 4. Final Video Encoding via FFmpeg
    # -------------------------------------------------------------
    out_mp4 = os.path.join(OUT_DIR, "rg_bucket_list_master_demo.mp4")
    cmd = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", master_audio,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    print("\n>>> Encoding Final RG Bucket List Master MP4 via FFmpeg...")
    subprocess.run(cmd, check=True)
    print(f"Video Exported: {out_mp4}")

    # Mirror to Artifact
    artifact_mp4 = os.path.join(ARTIFACT_DIR, "rg_bucket_list_master_demo.mp4")
    shutil.copy2(out_mp4, artifact_mp4)
    print(f">>> Mirrored to Artifacts: {artifact_mp4}")
    print("\n>>> RG BUCKET LIST STYLE MASTER DEMO COMPLETE! <<<")

if __name__ == "__main__":
    main()
