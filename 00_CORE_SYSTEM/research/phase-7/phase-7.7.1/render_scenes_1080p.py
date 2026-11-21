"""
render_scenes_1080p.py
======================
Renders the 4 high-fidelity 2D animated scenes for "पहली धुन" (The First Melody)
at native 1920x1080 resolution @ 24.0 FPS CFR:
- Scene 1: 8.0s (192 frames) - The Block & Rain (Studio Dawn, Rain Streaks, Slumped Musician)
- Scene 2: 8.0s (192 frames) - Leo's Gaze (Golden Retriever Enters, Tail Wag, Knee Nuzzle, Warm Smile)
- Scene 3: 8.0s (192 frames) - The Strum & Bloom (Vibrating Guitar Strings, Visualizer Spectrum Explosion)
- Scene 4: 7.5s (180 frames) - Golden Sunbeams & Triumph (Sunlight Shafts, Singing, Outro Card)

Total raw frames: 756 frames (31.5s gross).
Composited via 3x 0.5s xfade transitions into exactly 30.00s (720 frames).
"""

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.1"
SCENES_DIR = os.path.join(OUTPUT_DIR, "scenes_1080p")
OVERLAYS_DIR = os.path.join(OUTPUT_DIR, "overlays_1080p")
os.makedirs(SCENES_DIR, exist_ok=True)

W, H = 1920, 1080
FPS = 24

def load_overlay(badge_filename):
    p = os.path.join(OVERLAYS_DIR, badge_filename)
    if os.path.exists(p):
        return Image.open(p).convert("RGBA")
    return None

def start_ffmpeg_pipe(output_mp4):
    cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        output_mp4
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

# =============================================================================
# SCENE 1: THE BLOCK & RAIN (8.0s = 192 frames)
# =============================================================================
def render_scene_1(output_mp4):
    print("Rendering Scene 1: The Block & Rain (1920x1080, 192 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 192
    overlay = load_overlay("badge_scene_01.png")

    np.random.seed(101)
    num_drops = 75
    drop_x = np.random.uniform(200, 1000, num_drops)
    drop_y = np.random.uniform(0, 750, num_drops)
    drop_len = np.random.uniform(25, 55, num_drops)
    drop_speed = np.random.uniform(16, 28, num_drops)

    for f in range(total_frames):
        t = f / FPS
        # Background gradient: Cold misty indigo predawn sky
        img = Image.new("RGB", (W, H), (15, 20, 32))
        draw = ImageDraw.Draw(img)

        # Distant rainy city silhouettes through window (Window left=150, top=100, right=1050, bottom=780)
        draw.rectangle([150, 100, 1050, 780], fill=(22, 28, 45), outline=(50, 60, 85), width=8)
        # Window pane cross mullions
        draw.line([600, 100, 600, 780], fill=(45, 55, 78), width=6)
        draw.line([150, 440, 1050, 440], fill=(45, 55, 78), width=6)

        # Distant skyscrapers through rain
        city_buildings = [(180, 320, 260), (280, 240, 380), (400, 360, 520), (540, 200, 680), (700, 280, 820), (840, 350, 980)]
        for bx1, by1, bx2 in city_buildings:
            draw.rectangle([bx1, by1, bx2, 780], fill=(16, 21, 35))
            # Blinking city tower beacon
            if f % 48 < 24 and bx1 == 540:
                draw.ellipse([610, 195, 616, 201], fill=(239, 68, 68))

        # Rain streaks on window glass
        drop_y = (drop_y + drop_speed) % 680
        for i in range(num_drops):
            dx = drop_x[i]
            dy = 100 + drop_y[i]
            draw.line([dx, dy, dx - 4, dy + drop_len[i]], fill=(70, 90, 130), width=2)
            # Water droplet head
            draw.ellipse([dx - 5, dy + drop_len[i] - 2, dx - 2, dy + drop_len[i] + 2], fill=(100, 130, 180))

        # Studio Wall Acoustic Foam Panels (Right wall)
        for row in range(5):
            for col in range(4):
                px = 1150 + col * 180
                py = 80 + row * 160
                draw.rectangle([px, py, px + 160, py + 140], fill=(26, 32, 48), outline=(38, 48, 70), width=3)
                # 3D foam bevel lines
                draw.line([px, py, px + 80, py + 70], fill=(32, 40, 60), width=2)
                draw.line([px + 160, py, px + 80, py + 70], fill=(20, 25, 38), width=2)

        # Studio Desk (Foreground/Midground)
        draw.polygon([(0, 820), (1920, 820), (1920, 1080), (0, 1080)], fill=(18, 22, 33))
        draw.line([0, 820, 1920, 820], fill=(40, 50, 72), width=5)

        # Studio Monitor Speakers
        draw.rectangle([1100, 580, 1260, 820], fill=(12, 14, 22), outline=(30, 36, 52), width=3)
        draw.ellipse([1135, 610, 1225, 700], fill=(25, 30, 42), outline=(50, 60, 85), width=2) # Tweeter
        draw.ellipse([1130, 710, 1230, 810], fill=(20, 24, 35), outline=(40, 50, 70), width=3) # Woofer

        # Audio Interface with glowing red status LED (indicating silence / no signal)
        draw.rectangle([1320, 750, 1500, 820], fill=(20, 25, 38), outline=(45, 55, 78), width=2)
        draw.ellipse([1340, 775, 1352, 787], fill=(239, 68, 68) if f % 24 < 16 else (100, 20, 20)) # Flashing red LED
        draw.rectangle([1370, 770, 1480, 800], fill=(10, 14, 20))
        # Flatlined audio waveform on interface LCD
        draw.line([1375, 785, 1475, 785], fill=(70, 120, 150), width=2)

        # Silent Acoustic Guitar resting on stand in background
        # Guitar body
        draw.ellipse([1620, 560, 1780, 740], fill=(95, 45, 20), outline=(60, 28, 12), width=4)
        draw.ellipse([1645, 470, 1755, 590], fill=(95, 45, 20), outline=(60, 28, 12), width=4)
        draw.ellipse([1680, 550, 1720, 590], fill=(20, 15, 10)) # Sound hole
        # Guitar neck and headstock
        draw.rectangle([1692, 280, 1708, 480], fill=(120, 65, 30), outline=(80, 40, 18), width=2)
        draw.polygon([(1688, 240), (1712, 240), (1708, 280), (1692, 280)], fill=(90, 45, 20))

        # Musician Rohan (Slumped at desk, head supported by hand, tapping pencil)
        # Subtle breathing torso movement
        breathe = math.sin(t * 1.5) * 4
        # Torso (Dark navy hoodie)
        draw.polygon([(460, 760 - breathe), (640, 760 - breathe), (690, 890), (420, 890)], fill=(28, 38, 58))
        # Rohan's Head (Tilted down in exhaustion)
        head_tilt = math.sin(t * 1.2) * 2
        draw.ellipse([510 + head_tilt, 600 - breathe, 590 + head_tilt, 690 - breathe], fill=(210, 160, 125)) # Face skin
        # Hair (Messy modern dark curls)
        draw.ellipse([505 + head_tilt, 580 - breathe, 595 + head_tilt, 645 - breathe], fill=(24, 22, 28))
        # Left Arm resting on desk holding head
        draw.line([465, 780 - breathe, 490, 820, 515, 680], fill=(28, 38, 58), width=22)
        # Right Arm on desk holding pencil
        pencil_tap = math.sin(t * 8.0) * 8 if (f % 48 < 24) else 0 # Periodic tapping
        draw.line([630, 790 - breathe, 720, 830, 800, 820 + pencil_tap], fill=(28, 38, 58), width=20)
        # Pencil and blank music sheet
        draw.rectangle([740, 820, 920, 850], fill=(230, 230, 220), outline=(180, 180, 170), width=1) # Music paper
        draw.line([795, 810 + pencil_tap, 835, 825 + pencil_tap], fill=(245, 158, 11), width=4) # Yellow pencil

        # Composite HarfBuzz Lower-Third Badge (Fade in f=12..36, Fade out f=168..188)
        if overlay is not None:
            alpha = 1.0
            if f < 36:
                alpha = max(0.0, (f - 12) / 24.0)
            elif f > 168:
                alpha = max(0.0, (192 - f) / 24.0)
            if alpha > 0.0:
                cur_overlay = overlay.copy()
                if alpha < 1.0:
                    r, g, b, a = cur_overlay.split()
                    a = a.point(lambda p: int(p * alpha))
                    cur_overlay.putalpha(a)
                img.paste(cur_overlay, (0, 0), cur_overlay)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"Scene 1 Render Complete: {output_mp4}")

# =============================================================================
# SCENE 2: LEO'S GAZE & COMPANIONSHIP (8.0s = 192 frames)
# =============================================================================
def render_scene_2(output_mp4):
    print("Rendering Scene 2: Leo's Gaze & Companionship (1920x1080, 192 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 192
    overlay = load_overlay("badge_scene_02.png")

    for f in range(total_frames):
        t = f / FPS
        # Warm ambient lighting begins infusing the room
        warmth = min(1.0, f / 96.0)
        bg_r = int(22 + warmth * 18)
        bg_g = int(24 + warmth * 12)
        bg_b = int(36 - warmth * 6)
        img = Image.new("RGB", (W, H), (bg_r, bg_g, bg_b))
        draw = ImageDraw.Draw(img)

        # Soft atmospheric warm glow lamp on the left table
        lamp_intensity = 0.5 + 0.5 * warmth
        lamp_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(lamp_glow)
        for r_ring in range(250, 0, -15):
            alpha_ring = int((1.0 - r_ring / 250.0) * 80 * lamp_intensity)
            g_draw.ellipse([300 - r_ring, 400 - r_ring, 300 + r_ring, 400 + r_ring], fill=(251, 191, 36, alpha_ring))
        img.paste(lamp_glow, (0, 0), lamp_glow)

        # Studio Wall & Framed Indie Album Posters
        draw.rectangle([200, 150, 420, 420], fill=(28, 32, 45), outline=(60, 65, 80), width=4)
        draw.ellipse([270, 220, 350, 300], fill=(245, 158, 11)) # Vinyl record circle in poster
        draw.rectangle([500, 120, 760, 440], fill=(32, 38, 52), outline=(70, 75, 90), width=4)

        # Floor (Warm dark parquet wood)
        draw.polygon([(0, 680), (1920, 680), (1920, 1080), (0, 1080)], fill=(45, 32, 24))
        for line_y in range(710, 1080, 50):
            draw.line([0, line_y, 1920, line_y], fill=(35, 24, 18), width=3)

        # Rohan (Left midground, sitting on studio chair, knee visible)
        # Studio chair
        draw.rectangle([340, 520, 460, 780], fill=(20, 22, 28), outline=(40, 44, 55), width=4)
        # Rohan's Jeans/Knee (Left leg extended towards center)
        draw.polygon([(420, 650), (620, 670), (660, 750), (450, 760)], fill=(40, 55, 80)) # Thigh & Knee
        draw.line([660, 750, 680, 950], fill=(35, 48, 72), width=45) # Shin

        # Rohan's Torso & Head turning down towards Leo
        # As Leo enters, Rohan's posture shifts from slumped to attentive
        rohan_turn = min(1.0, f / 72.0)
        head_x = 480 + rohan_turn * 20
        head_y = 480 + rohan_turn * 15
        draw.polygon([(380, 570), (520, 560), (550, 680), (370, 690)], fill=(32, 44, 68)) # Hoodie
        # Head & Face
        draw.ellipse([head_x, head_y, head_x + 95, head_y + 115], fill=(218, 168, 132))
        draw.ellipse([head_x - 5, head_y - 10, head_x + 100, head_y + 55], fill=(24, 22, 28)) # Hair
        # Eye looking down affectionately at Leo
        draw.ellipse([head_x + 60, head_y + 48, head_x + 68, head_y + 56], fill=(40, 25, 18))
        # Gentle smile curving (from straight to curved as warmth increases)
        smile_dip = rohan_turn * 5
        draw.arc([head_x + 55, head_y + 68, head_x + 78, head_y + 78 + smile_dip], start=10, end=170, fill=(160, 70, 60), width=3)

        # Rohan's Arm reaching down to stroke Leo behind ears
        hand_x = 680 + math.sin(t * 3.0) * 12 * rohan_turn
        hand_y = 660 + math.cos(t * 3.0) * 6 * rohan_turn
        draw.line([500, 600, 590, 650, hand_x, hand_y], fill=(32, 44, 68), width=28)
        draw.ellipse([hand_x - 15, hand_y - 12, hand_x + 18, hand_y + 15], fill=(218, 168, 132)) # Hand

        # Leo the Golden Retriever (Steps in from right, rests chin on Rohan's knee)
        # Entry movement: Leo moves from x=1100 to rest position x=740
        leo_entry = min(1.0, f / 60.0)
        leo_root_x = 1100 - leo_entry * 360
        leo_y = 700

        # Tail wagging! Smooth harmonic wagging increasing in joy
        tail_angle = math.sin(t * 7.0) * 28 # Energetic joyful tail
        tail_rad = math.radians(tail_angle - 30)
        tail_end_x = leo_root_x + 360 + math.cos(tail_rad) * 140
        tail_end_y = leo_y + 40 + math.sin(tail_rad) * 140
        # Bushy golden tail
        draw.line([leo_root_x + 320, leo_y + 40, tail_end_x, tail_end_y], fill=(225, 170, 75), width=34)
        draw.ellipse([tail_end_x - 20, tail_end_y - 20, tail_end_x + 20, tail_end_y + 20], fill=(235, 180, 85))

        # Leo Body (Golden fur curves)
        draw.ellipse([leo_root_x + 120, leo_y - 40, leo_root_x + 350, leo_y + 140], fill=(215, 155, 60)) # Hindquarters
        draw.ellipse([leo_root_x, leo_y - 80, leo_root_x + 240, leo_y + 120], fill=(228, 168, 70)) # Chest & shoulders
        # Front Paws
        draw.line([leo_root_x + 80, leo_y + 80, leo_root_x + 60, leo_y + 220], fill=(215, 155, 60), width=32)
        draw.ellipse([leo_root_x + 40, leo_y + 200, leo_root_x + 85, leo_y + 230], fill=(235, 175, 75)) # Left paw
        draw.line([leo_root_x + 140, leo_y + 80, leo_root_x + 130, leo_y + 220], fill=(205, 145, 55), width=28)
        draw.ellipse([leo_root_x + 115, leo_y + 205, leo_root_x + 155, leo_y + 230], fill=(225, 165, 65)) # Right paw

        # Leo Neck & Blue Collar with Brass Bell Tag
        draw.polygon([(leo_root_x + 20, leo_y - 50), (leo_root_x + 90, leo_y - 40), (leo_root_x + 70, leo_y + 20), (leo_root_x - 10, leo_y)], fill=(228, 168, 70))
        # Blue collar
        draw.line([leo_root_x + 10, leo_y - 20, leo_root_x + 75, leo_y - 5], fill=(30, 64, 175), width=12)
        # Shiny brass tag (jingles with breathing)
        tag_jingle = math.sin(t * 8.0) * 3
        draw.ellipse([leo_root_x + 38 + tag_jingle, leo_y - 6, leo_root_x + 52 + tag_jingle, leo_y + 10], fill=(251, 191, 36))

        # Leo Head resting directly on Rohan's knee (x ~ 660, y ~ 660)
        head_resting_x = leo_root_x - 45
        head_resting_y = leo_y - 95 + math.sin(t * 2.0) * 3 # Soft breathing rise/fall
        # Floppy ears
        ear_flutter = math.sin(t * 3.0) * 4
        draw.ellipse([head_resting_x + 50, head_resting_y - 20, head_resting_x + 110, head_resting_y + 65 + ear_flutter], fill=(195, 135, 48))
        # Muzzle & skull
        draw.ellipse([head_resting_x - 30, head_resting_y, head_resting_x + 85, head_resting_y + 85], fill=(235, 175, 75))
        draw.ellipse([head_resting_x - 65, head_resting_y + 25, head_resting_x + 10, head_resting_y + 85], fill=(245, 195, 105)) # Muzzle
        # Dark moist nose
        draw.ellipse([head_resting_x - 72, head_resting_y + 35, head_resting_x - 52, head_resting_y + 55], fill=(25, 20, 20))
        # Big expressive dog eye (Amber/Hazel, looking up devotedly at Rohan)
        blink = (f % 96 > 90) # Periodic gentle blink
        if not blink:
            draw.ellipse([head_resting_x + 5, head_resting_y + 22, head_resting_x + 28, head_resting_y + 44], fill=(90, 50, 20)) # Iris
            draw.ellipse([head_resting_x + 10, head_resting_y + 26, head_resting_x + 24, head_resting_y + 40], fill=(20, 12, 8)) # Pupil
            draw.ellipse([head_resting_x + 12, head_resting_y + 27, head_resting_x + 18, head_resting_y + 33], fill=(255, 255, 255)) # Sparkle highlight!
        else:
            draw.line([head_resting_x + 5, head_resting_y + 34, head_resting_x + 28, head_resting_y + 34], fill=(40, 25, 15), width=3)

        # Composite HarfBuzz Lower-Third Badge
        if overlay is not None:
            alpha = 1.0
            if f < 30:
                alpha = max(0.0, (f - 10) / 20.0)
            elif f > 168:
                alpha = max(0.0, (192 - f) / 24.0)
            if alpha > 0.0:
                cur_overlay = overlay.copy()
                if alpha < 1.0:
                    r, g, b, a = cur_overlay.split()
                    a = a.point(lambda p: int(p * alpha))
                    cur_overlay.putalpha(a)
                img.paste(cur_overlay, (0, 0), cur_overlay)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"Scene 2 Render Complete: {output_mp4}")

# =============================================================================
# SCENE 3: THE STRUM & VISUALIZER BLOOM (8.0s = 192 frames)
# =============================================================================
def render_scene_3(output_mp4):
    print("Rendering Scene 3: The Strum & Visualizer Bloom (1920x1080, 192 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 192
    overlay = load_overlay("badge_scene_03.png")

    for f in range(total_frames):
        t = f / FPS
        # Dynamic energy background: Deep studio slate with pulsating colorful aura
        strum_power = min(1.0, f / 36.0) # Chord struck at beginning and sustains
        img = Image.new("RGB", (W, H), (16, 20, 32))
        draw = ImageDraw.Draw(img)

        # Large studio computer monitor in center background (Width 1100, Height 550)
        mon_x1, mon_y1, mon_x2, mon_y2 = 410, 80, 1510, 630
        draw.rectangle([mon_x1, mon_y1, mon_x2, mon_y2], fill=(8, 10, 16), outline=(45, 55, 75), width=6)
        # Monitor stand
        draw.polygon([(920, 630), (1000, 630), (1020, 720), (900, 720)], fill=(30, 36, 48))
        draw.rectangle([840, 720, 1080, 740], fill=(24, 28, 38))

        # Dynamic Audio Visualizer on Screen!
        # Multi-band frequency spectrum dancing vigorously with vibrant gradient bars
        num_bars = 48
        bar_w = 18
        bar_gap = 4
        start_bx = mon_x1 + 35
        base_by = mon_y2 - 30

        for b_idx in range(num_bars):
            bx = start_bx + b_idx * (bar_w + bar_gap)
            # Harmonic height modulation
            freq_mult = 1.0 + (b_idx % 8) * 0.5
            osc1 = math.sin(t * 14.0 + b_idx * 0.4)
            osc2 = math.cos(t * 22.0 - b_idx * 0.3)
            b_height = int((0.3 + 0.7 * (abs(osc1 * 0.6 + osc2 * 0.4))) * 380 * strum_power) + 20
            
            # Color gradient: Cyan (bass) -> Emerald (mids) -> Gold/Amber (highs) -> Magenta
            col_t = b_idx / num_bars
            if col_t < 0.33:
                r_c, g_c, b_c = 14, int(165 + col_t * 200), 233 # Cyan
            elif col_t < 0.66:
                r_c, g_c, b_c = int(16 + (col_t-0.33)*400), 220, 100 # Emerald to Gold
            else:
                r_c, g_c, b_c = 245, int(158 - (col_t-0.66)*200), int(50 + (col_t-0.66)*400) # Gold to Magenta

            draw.rectangle([bx, base_by - b_height, bx + bar_w, base_by], fill=(r_c, g_c, b_c))
            # Peak cap LED
            draw.rectangle([bx, base_by - b_height - 6, bx + bar_w, base_by - b_height - 2], fill=(255, 255, 255))

        # Glowing waveform oscilloscope line crossing monitor
        wave_pts = []
        for wx in range(mon_x1 + 20, mon_x2 - 20, 10):
            norm_wx = (wx - mon_x1) / (mon_x2 - mon_x1)
            wy = (mon_y1 + mon_y2) // 2 + int(math.sin(norm_wx * 18.0 + t * 24.0) * math.exp(-abs(norm_wx - 0.5)*2) * 90 * strum_power)
            wave_pts.append((wx, wy))
        if len(wave_pts) > 1:
            draw.line(wave_pts, fill=(251, 191, 36), width=3)

        # Foreground: Rohan holding Acoustic Guitar in Playing Position
        # Golden acoustic guitar body angled dynamically across lower screen
        g_center_x, g_center_y = 960, 840
        # Lower bout & upper bout
        draw.ellipse([g_center_x - 380, g_center_y - 120, g_center_x + 160, g_center_y + 240], fill=(160, 82, 35), outline=(100, 45, 18), width=8) # Warm mahogany
        draw.ellipse([g_center_x - 260, g_center_y - 200, g_center_x + 60, g_center_y + 40], fill=(185, 95, 42), outline=(100, 45, 18), width=6)
        # Sound hole with concentric rosette inlays
        draw.ellipse([g_center_x - 140, g_center_y - 110, g_center_x + 10, g_center_y + 40], fill=(24, 16, 12), outline=(245, 158, 11), width=5)
        draw.ellipse([g_center_x - 150, g_center_y - 120, g_center_x + 20, g_center_y + 50], outline=(255, 255, 255), width=2)

        # Guitar Fretboard & Headstock extending to upper left
        draw.polygon([(g_center_x - 100, g_center_y - 90), (g_center_x - 70, g_center_y - 40), (120, 220), (80, 180)], fill=(45, 30, 22), outline=(75, 50, 35), width=3)
        # Frets (Silver nickel lines)
        for fret_i in range(1, 12):
            frac = fret_i / 13.0
            fx1 = int((g_center_x - 100) * frac + 80 * (1.0 - frac))
            fy1 = int((g_center_y - 90) * frac + 180 * (1.0 - frac))
            fx2 = int((g_center_x - 70) * frac + 120 * (1.0 - frac))
            fy2 = int((g_center_y - 40) * frac + 220 * (1.0 - frac))
            draw.line([fx1, fy1, fx2, fy2], fill=(180, 190, 200), width=3)

        # 6 Vibrating Acoustic Guitar Strings!
        # When strummed, strings oscillate in standing wave harmonics!
        string_colors = [(245, 210, 130), (240, 200, 120), (220, 185, 110), (200, 200, 200), (210, 210, 210), (220, 220, 220)]
        for s_idx in range(6):
            s_frac = s_idx / 5.0
            sx_start = int(95 * (1.0 - s_frac) + 115 * s_frac)
            sy_start = int(185 * (1.0 - s_frac) + 215 * s_frac)
            sx_end = int((g_center_x - 80) * (1.0 - s_frac) + (g_center_x - 55) * s_frac) + 150
            sy_end = int((g_center_y - 75) * (1.0 - s_frac) + (g_center_y - 25) * s_frac) + 20
            
            # String vibration displacement (standing wave)
            str_pts = []
            for step in range(25):
                st_frac = step / 24.0
                curr_x = sx_start * (1.0 - st_frac) + sx_end * st_frac
                curr_y = sy_start * (1.0 - st_frac) + sy_end * st_frac
                # Standing wave oscillation
                vib = math.sin(st_frac * math.pi) * math.sin(t * (40.0 + s_idx * 15.0)) * 6.0 * strum_power
                str_pts.append((curr_x, curr_y + vib))
            draw.line(str_pts, fill=string_colors[s_idx], width=2 if s_idx > 2 else 3)

        # Rohan's Right Hand Strumming across strings (Holding tortoiseshell pick)
        pick_stroke = math.sin(t * 12.0) * 25 * strum_power
        hand_px = g_center_x - 60
        hand_py = g_center_y - 20 + pick_stroke
        # Forearm
        draw.line([hand_px + 280, hand_py + 220, hand_px + 50, hand_py + 20], fill=(32, 44, 68), width=48)
        # Hand & fingers curled
        draw.ellipse([hand_px - 20, hand_py - 15, hand_px + 45, hand_py + 35], fill=(225, 172, 138))
        # Tortoise pick striking string
        draw.polygon([(hand_px - 25, hand_py + 5), (hand_px - 10, hand_py + 28), (hand_px - 5, hand_py + 5)], fill=(245, 158, 11))

        # Luminous acoustic burst rings radiating from sound hole!
        burst_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(burst_glow)
        for ring_i in range(3):
            ring_rad = int(((f * 8 + ring_i * 90) % 360))
            ring_alpha = max(0, int((1.0 - ring_rad / 360.0) * 120 * strum_power))
            if ring_alpha > 0:
                b_draw.ellipse([g_center_x - 65 - ring_rad, g_center_y - 35 - ring_rad, g_center_x - 65 + ring_rad, g_center_y - 35 + ring_rad], outline=(251, 191, 36, ring_alpha), width=4)
        img.paste(burst_glow, (0, 0), burst_glow)

        # Composite HarfBuzz Lower-Third Badge
        if overlay is not None:
            alpha = 1.0
            if f < 30:
                alpha = max(0.0, (f - 10) / 20.0)
            elif f > 168:
                alpha = max(0.0, (192 - f) / 24.0)
            if alpha > 0.0:
                cur_overlay = overlay.copy()
                if alpha < 1.0:
                    r, g, b, a = cur_overlay.split()
                    a = a.point(lambda p: int(p * alpha))
                    cur_overlay.putalpha(a)
                img.paste(cur_overlay, (0, 0), cur_overlay)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"Scene 3 Render Complete: {output_mp4}")

# =============================================================================
# SCENE 4: GOLDEN SUNBEAMS & TRIUMPH (7.5s = 180 frames)
# =============================================================================
def render_scene_4(output_mp4):
    print("Rendering Scene 4: Golden Sunbeams & Triumph (1920x1080, 180 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 180
    badge_overlay = load_overlay("badge_scene_04.png")
    outro_overlay = load_overlay("outro_title_card.png")

    for f in range(total_frames):
        t = f / FPS
        # Rich sunrise sky: Radiant amber and gold morning light floods the room
        img = Image.new("RGB", (W, H), (42, 30, 24))
        draw = ImageDraw.Draw(img)

        # Sunbeam shafts angled through window from top right (Window x: 1200..1850, y: 50..650)
        # Window with clear golden morning sky outside
        draw.rectangle([1200, 50, 1850, 650], fill=(255, 230, 160), outline=(210, 170, 90), width=10)
        # Window mullions
        draw.line([1525, 50, 1525, 650], fill=(180, 140, 70), width=8)
        draw.line([1200, 350, 1850, 350], fill=(180, 140, 70), width=8)
        # Rising Golden Sun outside window
        draw.ellipse([1450, 120, 1600, 270], fill=(255, 248, 200))

        # Golden Volumetric Sunbeams piercing into the studio interior!
        sunbeams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(sunbeams)
        beam_polys = [
            [(1525, 200), (1850, 650), (1300, 1080), (700, 1080)],
            [(1350, 150), (1600, 500), (950, 1080), (450, 1080)],
            [(1200, 250), (1450, 600), (600, 1080), (150, 1080)]
        ]
        beam_alpha = int(45 + math.sin(t * 1.5) * 8)
        for poly in beam_polys:
            s_draw.polygon(poly, fill=(254, 240, 138, beam_alpha))
        img.paste(sunbeams, (0, 0), sunbeams)

        # Floor (Golden morning floor reflections)
        draw.polygon([(0, 720), (1920, 720), (1920, 1080), (0, 1080)], fill=(75, 48, 28))
        draw.line([0, 720, 1920, 720], fill=(120, 80, 45), width=4)

        # Rohan Standing in Full View, Singing Joyfully with Headphones and Guitar!
        # Headphone band across hair
        rohan_x = 750
        rohan_y = 350
        # Studio Condenser Microphone on boom stand in front of Rohan
        mic_x, mic_y = rohan_x - 120, rohan_y + 80
        draw.line([mic_x, mic_y + 40, mic_x, 880], fill=(160, 165, 175), width=8) # Mic stand
        draw.rectangle([mic_x - 22, mic_y - 45, mic_x + 22, mic_y + 35], fill=(45, 50, 60), outline=(200, 205, 215), width=3) # Mic body
        draw.ellipse([mic_x - 18, mic_y - 75, mic_x + 18, mic_y - 40], fill=(30, 35, 45), outline=(245, 158, 11), width=3) # Gold grille

        # Rohan Body (Slim, standing tall and confident)
        sing_sway = math.sin(t * 3.5) * 8
        draw.polygon([(rohan_x - 70, rohan_y + 140), (rohan_x + 90, rohan_y + 140), (rohan_x + 110, rohan_y + 420), (rohan_x - 80, rohan_y + 420)], fill=(38, 54, 84)) # Navy jacket
        # Trousers
        draw.line([rohan_x - 30, rohan_y + 420, rohan_x - 40, 850], fill=(28, 35, 48), width=38)
        draw.line([rohan_x + 50, rohan_y + 420, rohan_x + 60, 850], fill=(28, 35, 48), width=38)

        # Rohan Head (Singing with chin raised towards microphone, blissful expression)
        draw.ellipse([rohan_x - 45 + sing_sway, rohan_y - 20, rohan_x + 55 + sing_sway, rohan_y + 105], fill=(225, 175, 140)) # Face
        draw.ellipse([rohan_x - 55 + sing_sway, rohan_y - 35, rohan_x + 60 + sing_sway, rohan_y + 40], fill=(25, 22, 28)) # Dark hair
        # Professional studio headphones
        draw.arc([rohan_x - 58 + sing_sway, rohan_y - 45, rohan_x + 62 + sing_sway, rohan_y + 50], start=180, end=0, fill=(20, 20, 25), width=8) # Headband
        draw.ellipse([rohan_x + 40 + sing_sway, rohan_y + 20, rohan_x + 68 + sing_sway, rohan_y + 70], fill=(245, 158, 11), outline=(30, 30, 30), width=3) # Amber ear cup
        # Closed eyes in emotional singing ecstasy
        draw.arc([rohan_x - 22 + sing_sway, rohan_y + 35, rohan_x - 6 + sing_sway, rohan_y + 48], start=0, end=180, fill=(45, 28, 20), width=3)
        draw.arc([rohan_x + 6 + sing_sway, rohan_y + 35, rohan_x + 22 + sing_sway, rohan_y + 48], start=0, end=180, fill=(45, 28, 20), width=3)
        # Open singing mouth!
        draw.ellipse([rohan_x - 12 + sing_sway, rohan_y + 60, rohan_x + 8 + sing_sway, rohan_y + 82], fill=(130, 35, 30), outline=(225, 175, 140), width=2)

        # Acoustic Guitar hanging from strap across Rohan's shoulder
        draw.line([rohan_x - 60, rohan_y + 140, rohan_x + 70, rohan_y + 290], fill=(20, 20, 20), width=10) # Black woven strap
        draw.ellipse([rohan_x - 90, rohan_y + 220, rohan_x + 130, rohan_y + 380], fill=(175, 92, 42), outline=(110, 50, 20), width=6) # Guitar body
        draw.ellipse([rohan_x - 10, rohan_y + 270, rohan_x + 50, rohan_y + 330], fill=(25, 18, 12)) # Sound hole
        # Strumming hand
        draw.line([rohan_x + 80, rohan_y + 190, rohan_x + 60, rohan_y + 280], fill=(38, 54, 84), width=24)
        draw.ellipse([rohan_x + 45, rohan_y + 270, rohan_x + 75, rohan_y + 300], fill=(225, 175, 140))

        # Leo the Golden Dog sitting proudly beside Rohan on the right
        leo_x = rohan_x + 240
        leo_y = 660
        # Leo sitting posture with upright chest and wagging tail
        draw.ellipse([leo_x - 30, leo_y + 20, leo_x + 110, leo_y + 180], fill=(215, 155, 60)) # Body
        draw.ellipse([leo_x - 20, leo_y - 60, leo_x + 80, leo_y + 50], fill=(230, 170, 72)) # Chest & neck
        draw.line([leo_x + 80, leo_y + 100, leo_x + 180, leo_y + 80 + math.sin(t * 8.0) * 20], fill=(225, 165, 65), width=28) # Wagging tail
        # Leo Head held high, smiling happily with tongue out!
        draw.ellipse([leo_x - 10, leo_y - 100, leo_x + 70, leo_y - 30], fill=(235, 175, 75)) # Head
        draw.ellipse([leo_x - 35, leo_y - 75, leo_x + 20, leo_y - 35], fill=(245, 190, 95)) # Muzzle
        draw.ellipse([leo_x - 40, leo_y - 70, leo_x - 24, leo_y - 54], fill=(25, 20, 20)) # Nose
        # Happy panting pink tongue
        draw.ellipse([leo_x - 28, leo_y - 42, leo_x - 10, leo_y - 22], fill=(244, 114, 182))
        # Happy squinting eye
        draw.arc([leo_x + 10, leo_y - 78, leo_x + 28, leo_y - 62], start=180, end=0, fill=(45, 28, 15), width=3)
        # Floppy golden ear
        draw.ellipse([leo_x + 35, leo_y - 95, leo_x + 75, leo_y - 30], fill=(200, 140, 50))

        # Floating golden dust motes sparkling in the morning sunbeams
        np.random.seed(42)
        mote_xs = (np.random.uniform(200, 1800, 35) + t * 15) % 1800
        mote_ys = (np.random.uniform(100, 900, 35) + math.sin(t) * 20) % 900
        for mx, my in zip(mote_xs, mote_ys):
            draw.ellipse([mx, my, mx + 4, my + 4], fill=(255, 255, 230))

        # Composite HarfBuzz Lower-Third Badge (First half: f=0..84)
        if f < 90 and badge_overlay is not None:
            alpha = 1.0
            if f < 20:
                alpha = max(0.0, f / 20.0)
            elif f > 70:
                alpha = max(0.0, (90 - f) / 20.0)
            if alpha > 0.0:
                cur_overlay = badge_overlay.copy()
                if alpha < 1.0:
                    r, g, b, a = cur_overlay.split()
                    a = a.point(lambda p: int(p * alpha))
                    cur_overlay.putalpha(a)
                img.paste(cur_overlay, (0, 0), cur_overlay)

        # Composite Outro Title Card (Second half: f=96..180)
        if f >= 96 and outro_overlay is not None:
            outro_alpha = min(1.0, (f - 96) / 24.0)
            cur_outro = outro_overlay.copy()
            if outro_alpha < 1.0:
                r, g, b, a = cur_outro.split()
                a = a.point(lambda p: int(p * outro_alpha))
                cur_outro.putalpha(a)
            img.paste(cur_outro, (0, 0), cur_outro)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"Scene 4 Render Complete: {output_mp4}")

if __name__ == "__main__":
    s1_mp4 = os.path.join(SCENES_DIR, "scene_01.mp4")
    s2_mp4 = os.path.join(SCENES_DIR, "scene_02.mp4")
    s3_mp4 = os.path.join(SCENES_DIR, "scene_03.mp4")
    s4_mp4 = os.path.join(SCENES_DIR, "scene_04.mp4")

    render_scene_1(s1_mp4)
    render_scene_2(s2_mp4)
    render_scene_3(s3_mp4)
    render_scene_4(s4_mp4)
    print("\nALL 4 SCENES RENDERED IN 1080p FULL HD!")
