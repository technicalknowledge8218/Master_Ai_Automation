"""
render_master_organic_anime_reel.py
MASTER REEL: Organic 2D Mesh Deformation Lipsync & Anime Story Reel
Eliminates 100% of the flat cardboard/sticker feel:
- Continuous Organic 2D Mesh Deformation (cv2.remap bicubic warp) on jaw, chin, and lips
- Dynamic mouth cavity (teeth, tongue) scaling with voice RMS
- Upper eyelid blinking (smooth roll-down/up)
- Voice-cadence head nodding & breathing sway
- 5 Rhythmic Dynamic Camera Cuts & Manga Speed Lines
- Diagonal Comic Split-Screen (Both characters live reacting)
- Diegetic 3 Door Knocks, Sub-Bass Drop, Whooshes, and Clean Netflix Subtitles
"""

import os
import math
import shutil
import cv2
import numpy as np
import soundfile as sf
import subprocess

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

def warp_character_face(base_rgba, char_type="bunty", openness=0.0, blink=0.0):
    """
    Organic 2D Mesh Deformation for Bunty & Rohit:
    - deforms the jawline, chin, and lips continuously with bicubic cv2.remap
    - smoothly opens oral cavity (teeth, tongue)
    - blinks upper eyelids
    """
    h, w = base_rgba.shape[:2]
    grid_y, grid_x = np.indices((h, w), dtype=np.float32)
    
    if char_type == "bunty":
        mx, my = 190.0, 285.0
        sigma_x, sigma_y = 38.0, 48.0
        jaw_drop = 22.0
        eyes = [(165.0, 215.0), (215.0, 215.0)]
        eye_sigma = (18.0, 16.0)
    else:  # rohit
        mx, my = 230.0, 226.0
        sigma_x, sigma_y = 36.0, 44.0
        jaw_drop = 20.0
        eyes = [(205.0, 175.0), (250.0, 175.0)]
        eye_sigma = (16.0, 14.0)
        
    dist_sq = ((grid_x - mx)**2) / (2 * sigma_x**2) + ((grid_y - (my + 8))**2) / (2 * sigma_y**2)
    mouth_weight = np.exp(-dist_sq)
    
    pull_y = openness * jaw_drop * mouth_weight
    pull_x = openness * 3.0 * (grid_x - mx) / sigma_x * mouth_weight
    
    eye_weight = np.zeros_like(grid_x)
    for ex, ey in eyes:
        e_dist = ((grid_x - ex)**2) / (2 * eye_sigma[0]**2) + ((grid_y - ey)**2) / (2 * eye_sigma[1]**2)
        eye_weight += np.exp(-e_dist)
    pull_y += blink * 13.0 * eye_weight
    
    map_x = (grid_x - pull_x).astype(np.float32)
    map_y = (grid_y - pull_y).astype(np.float32)
    warped = cv2.remap(base_rgba, map_x, map_y, cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    
    if openness > 0.04:
        open_h = int(openness * 18)
        open_w = int(22 + openness * 8)
        cav_cx = int(mx)
        cav_cy = int(my + openness * 6)
        
        overlay = warped.copy()
        cv2.ellipse(overlay, (cav_cx, cav_cy), (open_w // 2, open_h // 2), 0, 0, 360, (25, 20, 60, 255), -1)
        t_h = max(2, int(open_h * 0.30))
        cv2.rectangle(overlay, (cav_cx - open_w // 3, cav_cy - open_h // 2), (cav_cx + open_w // 3, cav_cy - open_h // 2 + t_h), (245, 245, 250, 255), -1)
        tongue_h = max(2, int(open_h * 0.38))
        cv2.ellipse(overlay, (cav_cx, cav_cy + open_h // 4), (open_w // 3, tongue_h), 0, 0, 180, (90, 80, 210, 255), -1)
        cv2.ellipse(overlay, (cav_cx, cav_cy), (open_w // 2, open_h // 2), 0, 0, 360, (22, 18, 28, 255), 2)
        warped = overlay
        
    return warped

def paste_character_safe(frame, sprite_rgba, x, y):
    """Safely alpha-blends sprite onto frame handling boundary clipping."""
    sh, sw = sprite_rgba.shape[:2]
    fh, fw = frame.shape[:2]
    
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(fw, x + sw), min(fh, y + sh)
    
    sx0, sy0 = x0 - x, y0 - y
    sx1, sy1 = sx0 + (x1 - x0), sy0 + (y1 - y0)
    
    if x1 > x0 and y1 > y0:
        crop_sp = sprite_rgba[sy0:sy1, sx0:sx1]
        alpha = crop_sp[:, :, 3] / 255.0
        for c in range(3):
            frame[y0:y1, x0:x1, c] = (1.0 - alpha) * frame[y0:y1, x0:x1, c] + alpha * crop_sp[:, :, c]

def create_manga_speedlines(cx, cy, intensity=0.85, t=0.0):
    im = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    num_spokes = 84
    max_r = 1600
    min_r = 300
    np.random.seed(int(t * 14) % 1000)
    for i in range(num_spokes):
        base_angle = (2 * math.pi / num_spokes) * i + np.random.uniform(-0.02, 0.02)
        half_w = np.random.uniform(0.012, 0.038)
        r0 = min_r + np.random.uniform(0, 140)
        r1 = max_r
        
        p0 = (int(cx + r0 * math.cos(base_angle)), int(cy + r0 * math.sin(base_angle)))
        p1 = (int(cx + r1 * math.cos(base_angle - half_w)), int(cy + r1 * math.sin(base_angle - half_w)))
        p2 = (int(cx + r1 * math.cos(base_angle + half_w)), int(cy + r1 * math.sin(base_angle + half_w)))
        
        alpha = int(240 * intensity * np.random.uniform(0.65, 1.0))
        pts = np.array([p0, p1, p2], np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(im, [pts], (15, 12, 22, alpha))
    return im

def draw_sweat_drop_cv(frame, x, y, scale=1.0, progress=0.0):
    slide_y = int(y + progress * 60)
    w = int(22 * scale)
    h = int(38 * scale)
    cv2.ellipse(frame, (x, slide_y), (w//2, h//2), 0, 0, 360, (255, 210, 130), -1)
    pts = np.array([[x - w//2, slide_y], [x, slide_y - h//2], [x + w//2, slide_y]], np.int32)
    cv2.fillPoly(frame, [pts], (255, 210, 130))
    cv2.circle(frame, (x - w//6, slide_y - h//6), max(2, int(3*scale)), (255, 255, 255), -1)

def draw_subtitles_cv(frame, speaker, text, is_alert=False):
    y_pos = 1680
    full_str = f"{speaker}: {text}"
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.95
    thickness = 2
    (tw, th), baseline = cv2.getTextSize(full_str, font, font_scale, thickness)
    
    pad_x, pad_y = 36, 18
    x0 = (WIDTH - tw) // 2 - pad_x
    y0 = y_pos - th - pad_y
    x1 = (WIDTH + tw) // 2 + pad_x
    y1 = y_pos + baseline + pad_y
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (x0, y0), (x1, y1), (12, 14, 24), -1)
    border_color = (60, 60, 255) if is_alert else (80, 215, 255)
    cv2.rectangle(overlay, (x0, y0), (x1, y1), border_color, 3)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    
    txt_col = (80, 235, 255) if is_alert else (255, 255, 255)
    cv2.putText(frame, full_str, ((WIDTH - tw) // 2, y_pos), font, font_scale, (10, 10, 10), 5, cv2.LINE_AA)
    cv2.putText(frame, full_str, ((WIDTH - tw) // 2, y_pos), font, font_scale, txt_col, thickness, cv2.LINE_AA)

def main():
    print("\n==================================================================")
    print(">>> RENDERING MASTER ORGANIC 2D ANIME REEL (DEFORMATION LIPSYNC) <<<")
    print("==================================================================")
    
    sr = 24000
    
    b2_wav, _ = sf.read(os.path.join(AUDIO_DIR, "b2_call.wav"))
    r1_full, _ = sf.read(os.path.join(AUDIO_DIR, "r1_warning.wav"))
    r1_clip = r1_full[:int(4.5 * sr)]
    knocks_raw, _ = sf.read(KNOCKS_WAV)
    r2_clip, _ = sf.read(os.path.join(AUDIO_DIR, "r2_alert.wav"))
    b3_clip, _ = sf.read(os.path.join(AUDIO_DIR, "b3_shock.wav"))
    
    t1_st = 0.0
    t1_dur = len(b2_wav) / sr
    t2_st = t1_dur + 0.15
    t2_dur = len(r1_clip) / sr
    t3_st = t2_st + t2_dur + 0.10
    t3_dur = 2.40
    t4_st = t3_st + t3_dur + 0.05
    t4_dur = len(r2_clip) / sr
    t5_st = t4_st + t4_dur + 0.05
    t5_dur = len(b3_clip) / sr
    
    total_dur = t5_st + t5_dur + 0.8
    total_frames = int(total_dur * FPS)
    print(f"Total Video Duration: {total_dur:.2f}s ({total_frames} frames)")
    
    total_samples = int(total_dur * sr)
    master_mix = np.zeros(total_samples, dtype=np.float32)
    voice_track = np.zeros(total_samples, dtype=np.float32)
    
    def add_clip(clip, st_sec, vol=1.0, is_voice=True):
        st = int(st_sec * sr)
        en = min(st + len(clip), total_samples)
        if en > st:
            master_mix[st:en] += clip[:en-st] * vol
            if is_voice:
                voice_track[st:en] += clip[:en-st]
                
    add_clip(b2_wav, t1_st, 1.1)
    add_clip(r1_clip, t2_st, 1.15)
    add_clip(knocks_raw, t3_st + 0.1, 1.35, is_voice=False)
    add_clip(r2_clip, t4_st, 1.1)
    add_clip(b3_clip, t5_st, 1.05)
    
    if os.path.exists(BASS_DROP_WAV):
        bd_data, _ = sf.read(BASS_DROP_WAV)
        add_clip(bd_data, t2_st + 0.2, 0.9, is_voice=False)
        add_clip(bd_data, t3_st + 0.1, 1.2, is_voice=False)
        add_clip(bd_data, t5_st + 0.2, 1.1, is_voice=False)
        
    if os.path.exists(WHOOSH_WAV):
        wh_data, _ = sf.read(WHOOSH_WAV)
        add_clip(wh_data, 0.05, 0.6, is_voice=False)
        add_clip(wh_data, t2_st - 0.1, 0.8, is_voice=False)
        add_clip(wh_data, t3_st - 0.1, 0.8, is_voice=False)
        add_clip(wh_data, t5_st - 0.1, 0.7, is_voice=False)
        
    if os.path.exists(BGM_WAV):
        bgm_raw, _ = sf.read(BGM_WAV)
        if len(bgm_raw.shape) > 1: bgm_raw = bgm_raw.mean(axis=1)
        reps = int(np.ceil(total_samples / len(bgm_raw)))
        bgm_tile = np.tile(bgm_raw, reps)[:total_samples]
        master_mix += bgm_tile * 0.14
        
    pk = np.max(np.abs(master_mix))
    if pk > 0.98: master_mix = master_mix * (0.95 / pk)
    
    master_audio_p = os.path.join(OUT_DIR, "master_organic_audio.wav")
    sf.write(master_audio_p, master_mix, sr)
    
    f_samples = sr // FPS
    rms_list = []
    for f in range(total_frames):
        st = f * f_samples
        en = min(st + f_samples, len(voice_track))
        chunk = voice_track[st:en]
        rms = np.sqrt(np.mean(chunk**2)) if len(chunk) > 0 else 0.0
        rms_list.append(rms)
        
    max_rms = max(rms_list) if max(rms_list) > 0 else 1.0
    normalized_rms = [min(1.0, r / (max_rms * 0.75)) for r in rms_list]
    smoothed_rms = np.convolve(normalized_rms, np.ones(3)/3.0, mode='same')
    
    bunty_neutral = cv2.imread(os.path.join(BUNTY_LIB, "bunty_neutral.png"), cv2.IMREAD_UNCHANGED)
    bunty_shocked = cv2.imread(os.path.join(BUNTY_LIB, "bunty_shocked.png"), cv2.IMREAD_UNCHANGED)
    rohit_clean = cv2.imread(os.path.join(CHAR_LIB, "rohit_clean.png"), cv2.IMREAD_UNCHANGED)
    bg_raw = cv2.imread(BG_IMAGE_PATH)
    bg_resized = cv2.resize(bg_raw, (WIDTH, HEIGHT))
    
    out_mp4 = os.path.join(OUT_DIR, "rg_master_organic_reel.mp4")
    artifact_mp4 = os.path.join(ARTIFACT_DIR, "rg_master_organic_reel.mp4")
    
    cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(FPS),
        "-i", "-",
        "-i", master_audio_p,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-shortest",
        out_mp4
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    print(f">>> Processing {total_frames} Organic Deformed Frames...")
    
    for i in range(total_frames):
        t = i / FPS
        raw_val = smoothed_rms[i]
        syllable_mod = 0.5 + 0.5 * math.sin(t * 22.0)
        openness = raw_val * syllable_mod if raw_val > 0.12 else 0.0
        
        cycle_t = t % 3.0
        blink = math.sin((cycle_t / 0.15) * math.pi) if 0.0 <= cycle_t < 0.15 else 0.0
        
        frame = bg_resized.copy()
        sub_spk = None
        sub_txt = None
        sub_alert = False
        shake_x = 0
        shake_y = 0
        
        # -------------------------------------------------------------
        # SHOT 1: BUNTY INTRO WITH ORGANIC MESH LIPSYNC (0.0s -> t2_st)
        # -------------------------------------------------------------
        if t < t2_st:
            warped_b = warp_character_face(bunty_neutral, "bunty", openness, blink)
            nod_angle = math.sin(t * 7.5) * 1.5 if raw_val > 0.15 else 0.0
            breath_y = math.sin(t * 3.0) * 4.0
            
            bh, bw = warped_b.shape[:2]
            target_h = 1180
            target_w = int(bw * (target_h / bh))
            sc_b = cv2.resize(warped_b, (target_w, target_h), interpolation=cv2.INTER_CUBIC)
            
            M = cv2.getRotationMatrix2D((target_w // 2, target_h // 2), nod_angle, 1.0)
            rot_b = cv2.warpAffine(sc_b, M, (target_w, target_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
            
            paste_character_safe(frame, rot_b, 220, int(680 + breath_y))
            sub_spk = "बंटी"
            sub_txt = "हाँ रोहित, मैगी लाया क्या भाई?"
            sub_alert = False
            
        # -------------------------------------------------------------
        # SHOT 2: FLASH CUT TO ROHIT (ORGANIC MESH LIPSYNC + MANGA SPEEDLINES) (t2_st -> t3_st)
        # -------------------------------------------------------------
        elif t < t3_st:
            rel_t = t - t2_st
            if rel_t < (1.0 / FPS):
                frame = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)
            else:
                dark_tint = np.full((HEIGHT, WIDTH, 3), (25, 12, 40), dtype=np.uint8)
                cv2.addWeighted(dark_tint, 0.45, frame, 0.55, 0, frame)
                
                sl = create_manga_speedlines(WIDTH // 2, 750, intensity=0.85, t=rel_t)
                sl_alpha = sl[:, :, 3] / 255.0
                for c in range(3):
                    frame[:, :, c] = (1.0 - sl_alpha) * frame[:, :, c] + sl_alpha * sl[:, :, c]
                    
                decay = max(0.0, 1.0 - rel_t / 1.5)
                shake_x = int(math.sin(t * 48.0) * 16 * decay)
                shake_y = int(math.cos(t * 42.0) * 12 * decay)
                
                warped_r = warp_character_face(rohit_clean, "rohit", openness, blink)
                rh, rw = warped_r.shape[:2]
                target_h = 1200
                target_w = int(rw * (target_h / rh))
                sc_r = cv2.resize(warped_r, (target_w, target_h), interpolation=cv2.INTER_CUBIC)
                
                rx = (WIDTH - target_w) // 2 + shake_x
                ry = 640 + shake_y
                paste_character_safe(frame, sc_r, rx, ry)
                
            sub_spk = "रोहित"
            sub_txt = "बंटी! मज़ाक मत कर भाई! कमरा तुरंत बंद कर ले!"
            sub_alert = True
            
        # -------------------------------------------------------------
        # SHOT 3: DIAGONAL COMIC SPLIT SCREEN + 3 DOOR KNOCKS (t3_st -> t4_st)
        # -------------------------------------------------------------
        elif t < t4_st:
            rel_t = t - t3_st
            
            knock_times = [0.1, 0.9, 1.7]
            is_knock = False
            for kt in knock_times:
                dt = rel_t - kt
                if 0 <= dt < 0.25:
                    is_knock = True
                    decay = 1.0 - dt / 0.25
                    shake_x = int(math.sin(dt * 65.0) * 22 * decay)
                    shake_y = int(math.cos(dt * 55.0) * 18 * decay)
                    break
                    
            canvas = bg_resized.copy()
            
            mask = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
            poly_left = np.array([[0, 0], [640, 0], [440, HEIGHT], [0, HEIGHT]], np.int32)
            cv2.fillPoly(mask, [poly_left], 255)
            
            scene_l = np.full((HEIGHT, WIDTH, 3), (25, 10, 35), dtype=np.uint8)
            warped_r = warp_character_face(rohit_clean, "rohit", openness, blink)
            rh, rw = warped_r.shape[:2]
            sc_r = cv2.resize(warped_r, (int(rw * 1150 / rh), 1150), interpolation=cv2.INTER_CUBIC)
            paste_character_safe(scene_l, sc_r, 20, 680)
            
            scene_r = np.full((HEIGHT, WIDTH, 3), (12, 16, 28), dtype=np.uint8)
            warped_b = warp_character_face(bunty_shocked, "bunty", openness * 0.4, blink)
            bh, bw = warped_b.shape[:2]
            sc_b = cv2.resize(warped_b, (int(bw * 1150 / bh), 1150), interpolation=cv2.INTER_CUBIC)
            bx_pos = WIDTH - sc_b.shape[1] - 20
            paste_character_safe(scene_r, sc_b, bx_pos, 660)
            
            draw_sweat_drop_cv(scene_r, WIDTH - 260, 720, scale=1.3, progress=(rel_t % 0.8) / 0.8)
            
            mask_3c = mask[:, :, None] / 255.0
            canvas = (mask_3c * scene_l + (1.0 - mask_3c) * scene_r).astype(np.uint8)
            
            cv2.line(canvas, (640, 0), (440, HEIGHT), (0, 0, 0), 16)
            cv2.line(canvas, (640, 0), (440, HEIGHT), (255, 255, 255), 8)
            
            if is_knock:
                red_flash = np.full((HEIGHT, WIDTH, 3), (30, 30, 220), dtype=np.uint8)
                cv2.addWeighted(red_flash, 0.4, canvas, 0.6, 0, canvas)
                cv2.putText(canvas, "THUD!!", (WIDTH//2 - 140 + shake_x, 360 + shake_y), cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 240, 255), 6, cv2.LINE_AA)
                
            frame = canvas
            sub_spk = "दरवाज़ा"
            sub_txt = "* * ज़ोरदार आवाज़: खट... खट... खट! * *"
            sub_alert = True
            
        # -------------------------------------------------------------
        # SHOT 4: ROHIT FINAL WARNING (t4_st -> t5_st)
        # -------------------------------------------------------------
        elif t < t5_st:
            rel_t = t - t4_st
            crimson = np.full((HEIGHT, WIDTH, 3), (20, 15, 60), dtype=np.uint8)
            cv2.addWeighted(crimson, 0.45, frame, 0.55, 0, frame)
            
            sl = create_manga_speedlines(WIDTH // 2, 720, intensity=0.9, t=rel_t)
            sl_alpha = sl[:, :, 3] / 255.0
            for c in range(3):
                frame[:, :, c] = (1.0 - sl_alpha) * frame[:, :, c] + sl_alpha * sl[:, :, c]
                
            warped_r = warp_character_face(rohit_clean, "rohit", openness, blink)
            rh, rw = warped_r.shape[:2]
            target_h = 1250
            target_w = int(rw * (target_h / rh))
            sc_r = cv2.resize(warped_r, (target_w, target_h), interpolation=cv2.INTER_CUBIC)
            rx = (WIDTH - target_w) // 2
            ry = 630
            paste_character_safe(frame, sc_r, rx, ry)
                
            sub_spk = "रोहित"
            sub_txt = "दरवाज़ा बिल्कुल मत खोलना बंटी!!"
            sub_alert = True
            
        # -------------------------------------------------------------
        # SHOT 5: DRAMATIC SUSPENSE CLIFFHANGER (t5_st -> end)
        # -------------------------------------------------------------
        else:
            rel_t = t - t5_st
            vignette = np.full((HEIGHT, WIDTH, 3), (20, 10, 70), dtype=np.uint8)
            vig_alpha = min(0.65, 0.35 + rel_t * 0.12)
            cv2.addWeighted(vignette, vig_alpha, frame, 1.0 - vig_alpha, 0, frame)
            
            warped_b = warp_character_face(bunty_shocked, "bunty", openness * 0.5, blink)
            bh, bw = warped_b.shape[:2]
            target_h = int(1350 + min(150, rel_t * 60))
            target_w = int(bw * (target_h / bh))
            sc_b = cv2.resize(warped_b, (target_w, target_h), interpolation=cv2.INTER_CUBIC)
            shiver = int(math.sin(t * 50.0) * 4)
            bx = (WIDTH - target_w) // 2 + shiver
            by = 560
            paste_character_safe(frame, sc_b, bx, by)
                
            draw_sweat_drop_cv(frame, bx + 220, by + 180, scale=1.5, progress=(rel_t % 0.6) / 0.6)
            
            cv2.rectangle(frame, (WIDTH//2 - 320, 140), (WIDTH//2 + 320, 230), (12, 14, 24), -1)
            cv2.rectangle(frame, (WIDTH//2 - 320, 140), (WIDTH//2 + 320, 230), (60, 60, 255), 4)
            cv2.putText(frame, "TO BE CONTINUED . PART 2", (WIDTH//2 - 275, 200), cv2.FONT_HERSHEY_DUPLEX, 1.1, (80, 235, 255), 2, cv2.LINE_AA)
            
            sub_spk = "बंटी"
            sub_txt = "यहाँ दरवाज़े पर कौन है...? 😨"
            sub_alert = True
            
        if sub_spk and sub_txt:
            draw_subtitles_cv(frame, sub_spk, sub_txt, is_alert=sub_alert)
            
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    shutil.copyfile(out_mp4, artifact_mp4)
    print("\n=======================================================")
    print(">>> MASTER ORGANIC REEL EXPORTED SUCCESSFULLY! <<<")
    print(f"File: {out_mp4}")
    print(f"Artifact: {artifact_mp4}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
