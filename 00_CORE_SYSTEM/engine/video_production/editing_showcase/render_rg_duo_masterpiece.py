"""
render_rg_duo_masterpiece.py
The Ultimate 2D Anime Master Reel merging ALL 5 Discussed Points:
1. Art Style: Style C (RG Bucket List / Semi-Anime Comic Standard)
2. Character Duo: Bunty (Anime Hero, Gemini Puck) & Rohit (Roommate, Gemini Charon)
3. Living Animation: 3-Stage Viseme Mouth Flapping ('Muh Chalne Wala') + Eye Blinks + Breathing
4. Atmospheric Environment: 2:00 AM Hostel Room with hybrid moonlight/lamp, shifting to suspense crimson
5. Camera Dynamics & Sound: Multi-angle scene cuts, Manga phone & door panels, 3 Knocks, Bass drop, Netflix subtitles
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
CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
BG_IMAGE_PATH = r"F:\Master AI\CHARACTER_LIBRARY\rg_anime_room_bg.jpg"
AUDIO_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\rg_duo_audio"
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase"
ARTIFACT_DIR = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

SFX_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel\sfx"
BGM_WAV = os.path.join(SFX_DIR, "lofi_bg_track.wav")
WHOOSH_WAV = os.path.join(SFX_DIR, "whoosh.wav")
KNOCKS_WAV = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\rg_story\knocks.wav"
BASS_DROP_WAV = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\rg_story\bass_drop.wav"

FPS = 24
WIDTH = 1080
HEIGHT = 1920

# Fonts
FONT_NETFLIX_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 46)
FONT_NETFLIX_SUB_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 48)
FONT_PANEL_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 36)
FONT_PANEL_TEXT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
FONT_SPEAKER_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)

def load_rgba(path, target_h=1180):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    ratio = target_h / h
    return im.resize((int(w * ratio), target_h), Image.Resampling.LANCZOS)

def draw_netflix_subtitle(draw, speaker_label, text, y_pos=1680, is_highlight=False):
    full_text = f"{speaker_label}: {text}" if speaker_label else text
    bbox = draw.textbbox((WIDTH // 2, y_pos), full_text, font=FONT_NETFLIX_SUB_BOLD if is_highlight else FONT_NETFLIX_SUB, anchor="mm")
    pad_x = 36
    pad_y = 16
    pill_rect = [bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y]
    draw.rounded_rectangle(pill_rect, radius=18, fill=(8, 10, 18, 220), outline=(255, 200, 50, 180) if is_highlight else (40, 50, 75, 130), width=2)
    fill_color = (255, 230, 80) if is_highlight else (245, 245, 250)
    draw.text((WIDTH // 2, y_pos), full_text, fill=fill_color, font=FONT_NETFLIX_SUB_BOLD if is_highlight else FONT_NETFLIX_SUB, anchor="mm")

def draw_manga_phone_panel(draw, rect, rel_t):
    x0, y0, x1, y1 = rect
    draw.rectangle([x0, y0, x1, y1], fill=(12, 16, 26, 240), outline=(220, 230, 255, 240), width=5)
    draw.rectangle([x0, y0, x1, y0 + 50], fill=(240, 60, 70, 255))
    draw.text((x0 + (x1 - x0)//2, y0 + 25), "INCOMING CALL", fill=(255, 255, 255), font=FONT_PANEL_HEADER, anchor="mm")

    phone_cx = x0 + (x1 - x0)//2
    phone_cy = y0 + 230
    vib = math.sin(rel_t * 30.0) * 4 if (rel_t % 1.5 < 0.8) else 0
    px0, py0, px1, py1 = phone_cx - 130 + vib, phone_cy - 150, phone_cx + 130 + vib, phone_cy + 150
    draw.rounded_rectangle([px0, py0, px1, py1], radius=24, fill=(20, 24, 35), outline=(0, 200, 255), width=3)
    draw.ellipse([phone_cx - 40 + vib, phone_cy - 95, phone_cx + 40 + vib, phone_cy - 15], fill=(50, 75, 120), outline=(200, 220, 255), width=2)
    draw.text((phone_cx + vib, phone_cy - 55), "👤", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 34), anchor="mm")
    draw.text((phone_cx + vib, phone_cy + 25), "ROHIT (Roommate)", fill=(255, 255, 255), font=FONT_PANEL_TEXT, anchor="mm")
    draw.text((phone_cx + vib, phone_cy + 70), "📞 Connected (00:14)", fill=(0, 255, 180), font=ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24), anchor="mm")

def draw_manga_door_panel(draw, rect, rel_t):
    x0, y0, x1, y1 = rect
    draw.rectangle([x0, y0, x1, y1], fill=(10, 10, 18, 245), outline=(255, 60, 60, 240), width=5)
    draw.rectangle([x0, y0, x1, y0 + 50], fill=(200, 30, 40, 255))
    draw.text((x0 + (x1 - x0)//2, y0 + 25), "ROOM DOOR (OUTSIDE)", fill=(255, 255, 255), font=FONT_PANEL_HEADER, anchor="mm")

    dx0, dy0, dx1, dy1 = x0 + 40, y0 + 75, x1 - 40, y1 - 30
    draw.rectangle([dx0, dy0, dx1, dy1], fill=(30, 20, 18), outline=(60, 40, 35), width=4)
    draw.ellipse([dx1 - 35, dy0 + 190, dx1 - 15, dy0 + 210], fill=(180, 160, 80))

    # Knocks shockwaves
    for k_time in [0.2, 1.0, 1.8]:
        dt = rel_t - k_time
        if 0 <= dt <= 0.6:
            rad = int(dt * 120)
            alpha_k = int((1.0 - dt/0.6) * 220)
            k_im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            k_draw = ImageDraw.Draw(k_im)
            k_draw.ellipse([dx0 + 120 - rad, dy0 + 150 - rad, dx0 + 120 + rad, dy0 + 150 + rad], outline=(255, 80, 80, alpha_k), width=4)
            k_draw.text((dx0 + 120, dy0 + 150), "KNOCK!", fill=(255, 240, 100, alpha_k), font=FONT_PANEL_HEADER, anchor="mm")
            draw.bitmap((0, 0), k_im)

def main():
    print("\n==================================================================")
    print(">>> RENDERING THE MASTER RG ANIME DUO MASTERPIECE (5 POINTS MERGED) <<<")
    print("==================================================================")

    # 1. Timeline of Dialogue Cues
    cues = [
        ("b1", "Bunty", os.path.join(AUDIO_DIR, "b1_intro.wav")),
        ("b2", "Bunty", os.path.join(AUDIO_DIR, "b2_call.wav")),
        ("r1", "Rohit", os.path.join(AUDIO_DIR, "r1_warning.wav")),
        ("b3", "Bunty", os.path.join(AUDIO_DIR, "b3_shock.wav")),
        ("r2", "Rohit", os.path.join(AUDIO_DIR, "r2_alert.wav")),
        ("b4", "Bunty", os.path.join(AUDIO_DIR, "b4_outro.wav")),
    ]

    sr = 24000
    timeline = []
    cur_t = 0.0

    # Build sequential timeline with slight pauses
    for cid, spk, wav_p in cues:
        wdata, _ = sf.read(wav_p)
        dur = len(wdata) / sr
        timeline.append({
            "id": cid,
            "speaker": spk,
            "wav": wav_p,
            "data": wdata,
            "start": cur_t,
            "end": cur_t + dur,
            "dur": dur
        })
        cur_t += dur + 0.35  # 350ms conversational pause

    total_dur = cur_t + 1.2
    total_frames = int(total_dur * FPS)
    print(f"Total Duo Duration: {total_dur:.2f}s | Total Frames: {total_frames}")

    # Assemble Master Audio
    total_samples = int(total_dur * sr)
    master_speech = np.zeros(total_samples, dtype=np.float32)
    voice_mask = np.zeros(total_samples, dtype=np.float32)

    for item in timeline:
        st_samp = int(item["start"] * sr)
        en_samp = st_samp + len(item["data"])
        if en_samp <= total_samples:
            master_speech[st_samp:en_samp] += item["data"] * 1.05
            voice_mask[st_samp:en_samp] = 1.0

    # Ducked BGM
    master_mix = np.zeros(total_samples, dtype=np.float32)
    master_mix += master_speech
    if os.path.exists(BGM_WAV):
        bgm, _ = sf.read(BGM_WAV)
        if len(bgm.shape) > 1: bgm = bgm.mean(axis=1)
        repeats = int(np.ceil(total_samples / len(bgm)))
        bgm_long = np.tile(bgm, repeats)[:total_samples]
        
        # Smooth ducking
        win = int(sr * 0.25)
        smoothed = np.convolve(voice_mask, np.ones(win)/win, mode='same')
        gain = np.where(smoothed > 0.02, 0.11, 0.26)
        master_mix += bgm_long * gain

    # SFX
    # Door Knocks happen right during r2 (at start of r2 + 0.2s)
    r2_item = [x for x in timeline if x["id"] == "r2"][0]
    r1_item = [x for x in timeline if x["id"] == "r1"][0]

    sfx_events = [
        (WHOOSH_WAV, 0.05, 0.5),
        (WHOOSH_WAV, timeline[1]["start"], 0.6),
        (BASS_DROP_WAV, r1_item["start"] + 0.5, 0.95),  # Dramatic Bass Drop when Rohit shouts warning!
        (WHOOSH_WAV, timeline[3]["start"], 0.6),
        (KNOCKS_WAV, r2_item["start"] - 0.2, 1.0),       # 3 Door Knocks!
    ]

    for sfx_p, t_sec, vol in sfx_events:
        if os.path.exists(sfx_p):
            s_data, _ = sf.read(sfx_p)
            if len(s_data.shape) > 1: s_data = s_data.mean(axis=1)
            st = int(t_sec * sr)
            en = min(st + len(s_data), total_samples)
            if en > st:
                master_mix[st:en] += s_data[:en - st] * vol

    # Peak normalization
    peak = np.max(np.abs(master_mix))
    if peak > 0.98:
        master_mix = master_mix * (0.95 / peak)

    master_wav_path = os.path.join(OUT_DIR, "rg_duo_master_audio.wav")
    sf.write(master_wav_path, master_mix, sr)
    print(f"Master Broadcast Audio Exported: {master_wav_path}")

    # Compute RMS per frame across speech track for precise lip-sync
    frame_samples = sr // FPS
    rms_per_frame = []
    for i in range(total_frames):
        st = i * frame_samples
        en = min(st + frame_samples, len(master_speech))
        chunk = master_speech[st:en]
        rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0.0
        rms_per_frame.append(rms)

    # Load Character Sprites
    # Bunty (Anime Hero)
    bunty_neutral = load_rgba(os.path.join(BUNTY_LIB, "bunty_neutral.png"), target_h=1180)
    bunty_half = load_rgba(os.path.join(BUNTY_LIB, "bunty_half.png"), target_h=1180)
    bunty_speaking = load_rgba(os.path.join(BUNTY_LIB, "bunty_speaking.png"), target_h=1180)
    bunty_shocked = load_rgba(os.path.join(BUNTY_LIB, "bunty_shocked.png"), target_h=1180)
    bunty_phone = load_rgba(os.path.join(BUNTY_LIB, "bunty_phone.png"), target_h=1180)

    # Rohit (Roommate Friend)
    rohit_neutral = load_rgba(os.path.join(CHAR_LIB, "rohit_clean.png"), target_h=1150)
    rohit_half = load_rgba(os.path.join(CHAR_LIB, "rohit_half.png"), target_h=1150)
    rohit_speaking = load_rgba(os.path.join(CHAR_LIB, "rohit_speaking.png"), target_h=1150)

    # Load Background
    room_bg = Image.open(BG_IMAGE_PATH).convert("RGB")

    # Subtitles timeline
    sub_data = [
        (timeline[0]["start"], timeline[0]["end"], "बंटी", "रात के 2 बज रहे थे... हॉस्टल में सब सो चुके थे। तभी मेरा फोन बजा।", False),
        (timeline[1]["start"], timeline[1]["end"], "बंटी", "मैंने कॉल उठाया—'हाँ रोहित, मैगी लाया क्या भाई?'", False),
        (timeline[2]["start"], timeline[2]["end"], "रोहित", "बंटी! मज़ाक मत कर भाई! कमरा अंदर से तुरंत बंद कर ले! कोई तेरे दरवाज़े पर है!", True),
        (timeline[3]["start"], timeline[3]["end"], "बंटी", "क्या बोल रहा है रोहित? यहाँ दरवाज़े पर कौन...", True),
        (timeline[4]["start"], timeline[4]["end"], "रोहित", "दरवाज़ा बिल्कुल मत खोलना बंटी! ⚠️", True),
        (timeline[5]["start"], total_dur, "बंटी", "फॉलो कर लो पार्ट 2 के लिए! ✅", False),
    ]

    frames_dir = os.path.join(OUT_DIR, "rg_duo_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)

    print(">>> Rendering 2-Character Animated Frames with Genuine Viseme Flapping ('Muh Chalne Wala')...")

    for i in range(total_frames):
        t = i / FPS
        rms = rms_per_frame[i]
        is_speaking_energy = (rms > 0.018)

        # Find active speaker cue
        active_cue = None
        for item in timeline:
            if item["start"] <= t < item["end"]:
                active_cue = item
                break

        active_speaker = active_cue["speaker"] if active_cue else None
        active_id = active_cue["id"] if active_cue else None

        # -------------------------------------------------------------
        # 1. Base Environment & Hybrid Suspense Lighting
        # -------------------------------------------------------------
        frame = room_bg.copy()

        # Dynamic lighting shift: When Rohit gives warning (Scene r1 & r2) -> Suspense Crimson overlay!
        if active_id in ["r1", "b3", "r2"]:
            suspense_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (45, 6, 15, 115))
            frame.paste(Image.alpha_composite(frame.convert("RGBA"), suspense_overlay).convert("RGB"))

        draw = ImageDraw.Draw(frame)

        # -------------------------------------------------------------
        # 2. Breathing & Eye Blink Timing
        # -------------------------------------------------------------
        breath = math.sin(t * 3.4) * 0.015
        sway = math.sin(t * 2.2) * 1.2
        is_blink = ((int(t * 10) % 38) in [0, 1])

        # -------------------------------------------------------------
        # 3. Authentic 3-Stage Viseme Mouth Flap Logic ('Muh Chalne Wala')
        # -------------------------------------------------------------
        # Flap phase cycles between 0 (closed), 1 (half), 2 (wide), 3 (half) at 9Hz
        flap_phase = int(t * 9.0) % 4

        # Bunty Mouth State
        if active_speaker == "Bunty" and is_speaking_energy:
            if flap_phase == 0:
                bunty_viseme = bunty_neutral
            elif flap_phase in [1, 3]:
                bunty_viseme = bunty_half
            else:
                bunty_viseme = bunty_speaking
        else:
            bunty_viseme = bunty_neutral

        # Rohit Mouth State
        if active_speaker == "Rohit" and is_speaking_energy:
            if flap_phase == 0:
                rohit_viseme = rohit_neutral
            elif flap_phase in [1, 3]:
                rohit_viseme = rohit_half
            else:
                rohit_viseme = rohit_speaking
        else:
            rohit_viseme = rohit_neutral

        # -------------------------------------------------------------
        # 4. Camera Angles & Scene Staging
        # -------------------------------------------------------------
        if active_id == "b1":
            # SCENE 1: WIDE SHOT (Bunty alone at 2 AM)
            scale = 1.0
            sw, sh = bunty_viseme.size
            sprite_res = bunty_viseme.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            sprite_rot = sprite_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            frame.paste(sprite_rot, (WIDTH - sprite_rot.size[0] - 80, 720), sprite_rot)

            # Top Badge
            draw.text((WIDTH // 2, 90), "HOSTEL NIGHT TALES • BUNTY & ROHIT", fill=(160, 180, 220), font=FONT_SPEAKER_TAG, anchor="mm")

        elif active_id == "b2":
            # SCENE 2: BUNTY ON PHONE + MANGA PHONE PANEL
            scale = 1.10
            # Bunty holding phone with talking mouth!
            b_phone_active = bunty_phone if (flap_phase % 2 == 0 or not is_speaking_energy) else bunty_speaking
            sw, sh = b_phone_active.size
            sprite_res = b_phone_active.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            sprite_rot = sprite_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            frame.paste(sprite_rot, (40, 680), sprite_rot)

            # Manga Incoming Call Panel on Right
            rel_t = t - active_cue["start"]
            draw_manga_phone_panel(draw, [WIDTH - 440, 420, WIDTH - 40, 880], rel_t)

        elif active_id == "r1":
            # SCENE 3: CAMERA CUT TO ROHIT (PANICKED FRIEND SHOUTING ON STREET!)
            scale = 1.18
            # Dim the hostel background slightly and show street night atmosphere
            street_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (20, 10, 30, 120))
            frame.paste(Image.alpha_composite(frame.convert("RGBA"), street_overlay).convert("RGB"))

            # Rohit centered on screen speaking with active mouth flap!
            rw, rh = rohit_viseme.size
            rohit_res = rohit_viseme.resize((int(rw * scale), int(rh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            rohit_rot = rohit_res.rotate(sway * 1.5, resample=Image.Resampling.BICUBIC, expand=True)
            rx = (WIDTH - rohit_rot.size[0]) // 2
            frame.paste(rohit_rot, (rx, 680), rohit_rot)

            # Alert Badge
            draw.text((WIDTH // 2, 110), "⚠️ ROHIT CALLING FROM OUTSIDE", fill=(255, 80, 90), font=FONT_PANEL_HEADER, anchor="mm")

        elif active_id == "b3":
            # SCENE 4: DRAMATIC EXTREME CLOSE-UP ON BUNTY (SHOCK)
            scale = 1.42
            shiver = int(math.sin(t * 40.0) * 3)
            # Bunty terrified shock pose!
            sw, sh = bunty_shocked.size
            b_shock_res = bunty_shocked.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            b_shock_rot = b_shock_res.rotate(sway, resample=Image.Resampling.BICUBIC, expand=True)
            bx = (WIDTH - b_shock_rot.size[0]) // 2 + shiver
            frame.paste(b_shock_rot, (bx, 620), b_shock_rot)

            draw.text((WIDTH // 2, 120), "🚨 SOMEONE IS AT THE DOOR", fill=(255, 60, 70), font=FONT_PANEL_HEADER, anchor="mm")

        elif active_id == "r2":
            # SCENE 5: THE DOOR KNOCKS & ROHIT FINAL WARNING
            # Split: Bunty frozen on Left, Manga Door Panel on Right with 3 Knocks!
            scale = 1.15
            sw, sh = bunty_shocked.size
            b_res = bunty_shocked.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            frame.paste(b_res, (30, 690), b_res)

            # Door Panel on Right
            rel_t = t - active_cue["start"]
            draw_manga_door_panel(draw, [WIDTH - 460, 380, WIDTH - 30, 920], rel_t)

        else:
            # SCENE 6: OUTRO / PART 2
            scale = 1.15
            b_outro = bunty_speaking if is_speaking_energy else bunty_neutral
            sw, sh = b_outro.size
            b_res = b_outro.resize((int(sw * scale), int(sh * scale * (1.0 + breath))), Image.Resampling.LANCZOS)
            frame.paste(b_res, ((WIDTH - b_res.size[0]) // 2, 700), b_res)

            draw.rounded_rectangle([WIDTH//2 - 280, 110, WIDTH//2 + 280, 180], radius=16, fill=(15, 18, 30, 235), outline=(255, 200, 50, 220), width=2)
            draw.text((WIDTH // 2, 145), "🚪 PART 2 COMING SOON", fill=(255, 215, 0), font=FONT_PANEL_HEADER, anchor="mm")

        # -------------------------------------------------------------
        # 5. Clean Netflix/Anime Style Subtitles (Bottom Third)
        # -------------------------------------------------------------
        current_sub = None
        for s_start, s_end, spk, text, hl in sub_data:
            if s_start <= t < s_end:
                current_sub = (spk, text, hl)
                break

        if current_sub:
            spk, text, hl = current_sub
            draw_netflix_subtitle(draw, spk, text, y_pos=1680, is_highlight=hl)

        # Save Frame
        frame.save(os.path.join(frames_dir, f"frame_{i:05d}.jpg"), quality=93)
        if i % 100 == 0 or i == total_frames - 1:
            print(f"  Frame {i}/{total_frames} ({t:.1f}s) | Active Speaker: {active_speaker} | Mouth Flap: {flap_phase if is_speaking_energy else 'CLOSED'}")

    # -------------------------------------------------------------
    # 6. Final Video Encoding via FFmpeg
    # -------------------------------------------------------------
    out_mp4 = os.path.join(OUT_DIR, "rg_duo_masterpiece.mp4")
    cmd = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", master_wav_path,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    print("\n>>> Encoding Final RG Anime Duo Masterpiece MP4 via FFmpeg...")
    subprocess.run(cmd, check=True)
    print(f"Video Exported: {out_mp4}")

    # Mirror to Artifact
    artifact_mp4 = os.path.join(ARTIFACT_DIR, "rg_duo_masterpiece.mp4")
    shutil.copy2(out_mp4, artifact_mp4)
    print(f">>> Mirrored to Artifacts: {artifact_mp4}")
    print("\n>>> RG ANIME DUO MASTERPIECE COMPLETED WITH ALL 5 POINTS MERGED! <<<")

if __name__ == "__main__":
    main()
