"""
render_scenes_772.py
====================
Renders the 4 high-fidelity 2D animated scenes for "चाय और चाल" (The Chai Gambit)
at native 1920x1080 resolution @ 24.0 FPS CFR:
- Scene 1: 8.0s (192 frames) - The Confrontation & Napkin Slide
- Scene 2: 8.0s (192 frames) - The Unflinching Chai Sip (Close-Up Aisha)
- Scene 3: 8.0s (192 frames) - The iPad Screen Reveal & Jaw Drop (Vikram Shock)
- Scene 4: 7.5s (180 frames) - The Playful Wink & UPI Surrender

Uses PyMuPDF (MuPDF vector rasterizer) for anti-aliased 1080p SVG frame rendering,
compositing 1080p HarfBuzz Devanagari typography, and piping directly into FFmpeg H.264.
"""

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image
import pymupdf
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2"
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
        "-crf", "17",
        "-preset", "fast",
        output_mp4
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

# =============================================================================
# SCENE 1: THE CONFRONTATION & NAPKIN SLIDE (8.0s = 192 frames)
# =============================================================================
def render_scene_1(output_mp4):
    print("Rendering Scene 1: The Confrontation & Napkin Slide (1920x1080, 192 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 192
    overlay = load_overlay("badge_beat_01.png")

    for f in range(total_frames):
        t = f / FPS
        # Dynamic subtle cafe neon glow pulsation
        neon_pulse = 0.5 + 0.5 * math.sin(t * 3.0)
        
        # Vikram mouth phonemes for speech: "बुरा मत मानना आयशा..."
        is_speaking = (0.6 <= t <= 7.8)
        mouth_open = int(abs(math.sin(t * 14.0)) * 14) if is_speaking else 0
        brow_cock = int(math.sin(t * 2.5) * 6)
        
        # Napkin slide animation: moves forward from x=1100 to rest at x=880 between f=24 and f=72
        slide_prog = min(1.0, max(0.0, (f - 24) / 48.0))
        # Ease-out cubic
        slide_prog = 1.0 - (1.0 - slide_prog)**3
        napkin_x = 1120 - slide_prog * 240
        napkin_y = 780 + slide_prog * 40
        arm_reach = slide_prog * 60

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
          <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#090d1a"/>
              <stop offset="60%" stop-color="#141c2e"/>
              <stop offset="100%" stop-color="#1e293b"/>
            </linearGradient>
            <linearGradient id="woodTable" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3e2723"/>
              <stop offset="25%" stop-color="#2d1d18"/>
              <stop offset="100%" stop-color="#1a110e"/>
            </linearGradient>
            <linearGradient id="bomberVikram" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#059669"/>
              <stop offset="100%" stop-color="#064e3b"/>
            </linearGradient>
            <linearGradient id="coatAisha" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#eab308"/>
              <stop offset="100%" stop-color="#a16207"/>
            </linearGradient>
          </defs>

          <!-- Cafe Interior Background -->
          <rect width="{W}" height="{H}" fill="url(#bg)"/>

          <!-- Rain Streaked Glass Window with City Lights Bokeh -->
          <rect x="180" y="80" width="1560" height="700" fill="#0d1527" stroke="#334155" stroke-width="8" rx="8"/>
          <!-- Window Mullions -->
          <line x1="960" y1="80" x2="960" y2="780" stroke="#1e293b" stroke-width="8"/>
          <line x1="180" y1="430" x2="1740" y2="430" stroke="#1e293b" stroke-width="6"/>

          <!-- Glowing Cafe Neon Signs Bokeh Outside -->
          <circle cx="450" cy="260" r="130" fill="#f43f5e" opacity="{0.20 + 0.08 * neon_pulse}"/>
          <circle cx="820" cy="220" r="95" fill="#38bdf8" opacity="0.18"/>
          <circle cx="1200" cy="300" r="110" fill="#f59e0b" opacity="0.22"/>
          <circle cx="1480" cy="240" r="85" fill="#10b981" opacity="0.16"/>

          <!-- Warm cafe neon script sign -->
          <text x="320" y="180" font-family="'Montserrat', sans-serif" font-size="56" font-weight="800" fill="#f59e0b" opacity="0.45" letter-spacing="6">CHAI &amp; CO. • MUMBAI</text>

          <!-- Diagonal Rain Streaks across Window -->
          {' '.join([f'<line x1="{180 + (i*75 + int(f*12))%1560}" y1="{80 + (i*95 + int(f*18))%700}" x2="{160 + (i*75 + int(f*12))%1560}" y2="{120 + (i*95 + int(f*18))%700}" stroke="#64748b" stroke-width="2.5" opacity="0.4"/>' for i in range(28)])}

          <!-- Cafe Table (Perspective Foreground) -->
          <polygon points="0,800 1920,800 1920,1080 0,1080" fill="url(#woodTable)"/>
          <line x1="0" y1="800" x2="1920" y2="800" stroke="#5d4037" stroke-width="6"/>
          <!-- Table woodgrain reflections -->
          <ellipse cx="960" cy="840" rx="480" ry="20" fill="#f59e0b" opacity="0.08"/>

          <!-- AISHA (Foreground Left, 3/4 Back/Profile, Composed Poise) -->
          <g transform="translate(180, 360)">
            <!-- Trench Coat Torso & Shoulder -->
            <path d="M120 280 C180 200, 320 220, 360 380 L320 540 L80 540 Z" fill="url(#coatAisha)"/>
            <!-- Black Turtleneck Collar -->
            <path d="M210 180 L280 180 L270 240 L215 240 Z" fill="#18181b"/>
            <!-- Elegant Neck & Jawline -->
            <path d="M220 120 Q260 110 270 170 Q230 190 220 120 Z" fill="#fed7aa"/>
            <!-- Sleek Asymmetrical Bob Cut Hair -->
            <path d="M180 120 C170 30, 320 30, 305 120 C320 190, 310 270, 260 290 C250 200, 235 150, 220 130 C190 120, 180 150, 180 120 Z" fill="#1e1b4b"/>
            <path d="M210 65 Q255 50 290 70" stroke="#818cf8" stroke-width="4" fill="none" opacity="0.6"/>
            <!-- Silver Ear Cuff glint -->
            <circle cx="218" cy="138" r="4.5" fill="#f8fafc"/>
          </g>

          <!-- VIKRAM (Midground Right, Leaning Forward with Smug Swagger) -->
          <g transform="translate(1120, 280)">
            <!-- Bomber Jacket Torso -->
            <path d="M160 340 L80 560 L480 560 L420 340 Z" fill="url(#bomberVikram)"/>
            <!-- Ribbed Collar -->
            <path d="M220 320 Q290 350 360 320 L365 345 Q290 375 215 345 Z" fill="#1f2937"/>
            <path d="M245 340 L290 410 L335 340 Z" fill="#4b5563"/>

            <!-- Neck & Strong Athletic Jaw -->
            <path d="M255 240 L325 240 L320 320 L260 320 Z" fill="#fcd34d"/>
            <path d="M210 140 Q290 100 370 140 Q380 230 290 275 Q200 230 210 140 Z" fill="#fcd34d"/>
            <!-- 5 O'Clock Shadow -->
            <path d="M225 210 Q290 275 355 210 L345 235 Q290 268 235 235 Z" fill="#78350f" opacity="0.25"/>

            <!-- Styled Quiff Fade Hair -->
            <path d="M205 140 C200 60, 375 60, 370 140 C375 160, 365 190, 355 200 C345 140, 330 100, 290 92 C250 100, 230 140, 220 200 Z" fill="#18181b"/>
            <path d="M240 85 Q290 68 340 88" stroke="#52525b" stroke-width="4" fill="none"/>

            <!-- Tortoiseshell Glasses -->
            <rect x="230" y="160" width="55" height="40" rx="6" fill="none" stroke="#78350f" stroke-width="5.5"/>
            <rect x="300" y="160" width="55" height="40" rx="6" fill="none" stroke="#78350f" stroke-width="5.5"/>
            <line x1="285" y1="178" x2="300" y2="178" stroke="#78350f" stroke-width="6"/>

            <!-- Eyes behind Glasses (Looking cockily at Aisha) -->
            <ellipse cx="258" cy="180" rx="8" ry="7" fill="#ffffff"/>
            <circle cx="255" cy="180" r="5" fill="#1e1b4b"/>
            <circle cx="253" cy="178" r="1.8" fill="#ffffff"/>
            <ellipse cx="328" cy="180" rx="8" ry="7" fill="#ffffff"/>
            <circle cx="325" cy="180" r="5" fill="#1e1b4b"/>
            <circle cx="323" cy="178" r="1.8" fill="#ffffff"/>

            <!-- Eyebrows (Left steady, Right cocked high) -->
            <path d="M225 152 L275 150" stroke="#18181b" stroke-width="6" stroke-linecap="round"/>
            <path d="M300 142 L355 {148 - brow_cock}" stroke="#18181b" stroke-width="7" stroke-linecap="round"/>

            <!-- Nose -->
            <path d="M285 185 L292 215 L280 218" stroke="#b45309" stroke-width="3.5" stroke-linecap="round" fill="none"/>

            <!-- Cocky Mouth (Animated speaking) -->
            <path d="M245 242 Q290 {248 + mouth_open} 335 238" stroke="#78350f" stroke-width="6" stroke-linecap="round" fill="{ '#451a03' if mouth_open > 4 else 'none' }"/>

            <!-- Left Arm leaning forward sliding napkin -->
            <path d="M180 380 L{80 - arm_reach} 500 L{140 - arm_reach} 520 L230 420 Z" fill="#047857"/>
            <ellipse cx="{75 - arm_reach}" cy="505" rx="22" ry="16" fill="#fcd34d"/>
          </g>

          <!-- Paper Napkin Sliding Across Table -->
          <g transform="translate({napkin_x}, {napkin_y}) rotate(-6)">
            <polygon points="0,0 160,-15 175,90 15,105" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2.5"/>
            <!-- Napkin Creases & Red Pen Sketch -->
            <line x1="25" y1="20" x2="145" y2="10" stroke="#e2e8f0" stroke-width="2"/>
            <circle cx="85" cy="45" r="24" fill="none" stroke="#ef4444" stroke-width="4"/>
            <path d="M72 45 L98 45 M85 32 L85 58" stroke="#ef4444" stroke-width="3"/>
          </g>

          <!-- Two Steaming Cutting Chai Glasses on Table -->
          <g transform="translate(680, 770)">
            <!-- Glass holder wire frame -->
            <rect x="0" y="30" width="90" height="90" fill="none" stroke="#94a3b8" stroke-width="3" rx="4"/>
            <polygon points="12,30 78,30 70,110 20,110" fill="#f59e0b" stroke="#ffffff" stroke-width="3.5"/>
            <!-- Steam wisps -->
            <path d="M40 20 Q48 5 38 -8 Q46 -22 40 -35" stroke="#ffffff" stroke-width="3" fill="none" opacity="{0.5 + 0.3*math.sin(t*4.0)}"/>
          </g>
        </svg>"""

        doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
        pix = doc[0].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Composite HarfBuzz Lower-Third Badge
        if overlay is not None:
            alpha = 1.0
            if f < 24:
                alpha = max(0.0, f / 24.0)
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
    print(f"Scene 1 Complete: {output_mp4}")

# =============================================================================
# SCENE 2: THE UNFLINCHING CHAI SIP (CLOSE-UP AISHA) (8.0s = 192 frames)
# =============================================================================
def render_scene_2(output_mp4):
    print("Rendering Scene 2: The Unflinching Chai Sip (1920x1080, 192 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 192
    overlay = load_overlay("badge_beat_02.png")

    for f in range(total_frames):
        t = f / FPS
        # Chai sip movement: glass raises from y=750 to lips at y=560 during f=0..60, holds f=60..100, lowers f=100..140
        if f < 60:
            prog = (f / 60.0)**2
            sip_y = 750 - prog * 180
        elif f < 100:
            sip_y = 570
        elif f < 140:
            prog = ((f - 100) / 40.0)
            sip_y = 570 + prog * 160
        else:
            sip_y = 730

        # Speaking phonemes: Aisha speaks from t=1.7s (f=40) to t=7.3s (f=175)
        is_speaking = (f >= 105 and f <= 175)
        mouth_open = int(abs(math.sin(t * 15.0)) * 12) if is_speaking else 0
        blink = (f % 96 > 88 and (f < 105 or f > 175)) # periodic natural blink

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
          <defs>
            <linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0c1222"/>
              <stop offset="50%" stop-color="#162238"/>
              <stop offset="100%" stop-color="#241b2f"/>
            </linearGradient>
            <linearGradient id="aishaHair2" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#2e1065"/>
              <stop offset="50%" stop-color="#1e1b4b"/>
              <stop offset="100%" stop-color="#09090b"/>
            </linearGradient>
            <linearGradient id="coatGrad2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#facc15"/>
              <stop offset="50%" stop-color="#ca8a04"/>
              <stop offset="100%" stop-color="#854d0e"/>
            </linearGradient>
          </defs>

          <!-- Rich Cinematic Bokeh Cafe Background -->
          <rect width="{W}" height="{H}" fill="url(#bg2)"/>
          <circle cx="350" cy="380" r="220" fill="#f59e0b" opacity="0.16"/>
          <circle cx="1550" cy="320" r="250" fill="#10b981" opacity="0.14"/>
          <circle cx="960" cy="180" r="180" fill="#38bdf8" opacity="0.12"/>

          <!-- AISHA (Center Close-Up Hero Shot) -->
          <g transform="translate(960, 480)">
            <!-- Trench Coat Lapels & Shoulders -->
            <path d="M-440 380 L-220 220 L0 320 L220 220 L440 380 L480 600 L-480 600 Z" fill="url(#coatGrad2)"/>
            <!-- Black Turtleneck Collar -->
            <path d="M-140 180 L140 180 L110 320 L-110 320 Z" fill="#18181b"/>
            <!-- Sculpted Neck & Shadow -->
            <path d="M-90 100 L90 100 L80 200 L-80 200 Z" fill="#fed7aa"/>
            <path d="M-60 140 Q0 180 60 140 L50 200 L-50 200 Z" fill="#ea580c" opacity="0.18"/>

            <!-- Delicate Silver Geometric Pendant -->
            <line x1="0" y1="180" x2="0" y2="235" stroke="#cbd5e1" stroke-width="2.5"/>
            <polygon points="-8,235 8,235 0,250" fill="#f8fafc"/>

            <!-- Sculpted Head & Jawline -->
            <path d="M-210 -180 Q0 -320 210 -180 Q250 140 0 280 Q-250 140 -210 -180 Z" fill="#fed7aa"/>
            <path d="M-180 60 Q0 280 180 60 L140 160 Q0 260 -140 160 Z" fill="#f97316" opacity="0.15"/>

            <!-- Silver Ear Cuff on right ear -->
            <circle cx="-218" cy="-30" r="10" fill="#f8fafc"/>
            <circle cx="-214" cy="-10" r="8" fill="#e2e8f0"/>

            <!-- Expressive Almond Eyes & Cat-Eye Winged Eyeliner -->
            {'<line x1="-140" y1="-50" x2="-60" y2="-50" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/> <line x1="60" y1="-50" x2="140" y2="-50" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/>' if blink else f'''
            <!-- Left Eye -->
            <ellipse cx="-100" cy="-45" rx="38" ry="18" fill="#ffffff"/>
            <circle cx="-96" cy="-45" r="15" fill="#451a03"/>
            <circle cx="-96" cy="-45" r="8" fill="#1c1917"/>
            <circle cx="-100" cy="-50" r="4.5" fill="#ffffff"/>
            <path d="M-145 -55 Q-100 -78 -55 -55 L-45 -65" stroke="#0f172a" stroke-width="8" stroke-linecap="round" fill="none"/>
            <!-- Right Eye -->
            <ellipse cx="100" cy="-45" rx="38" ry="18" fill="#ffffff"/>
            <circle cx="96" cy="-45" r="15" fill="#451a03"/>
            <circle cx="96" cy="-45" r="8" fill="#1c1917"/>
            <circle cx="92" cy="-50" r="4.5" fill="#ffffff"/>
            <path d="M55 -55 Q100 -78 145 -55 L155 -65" stroke="#0f172a" stroke-width="8" stroke-linecap="round" fill="none"/>
            '''}

            <!-- Delicate Arched Eyebrows -->
            <path d="M-145 -85 Q-100 -105 -55 -85" stroke="#0f172a" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M55 -85 Q100 -105 145 -85" stroke="#0f172a" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Refined Nose Bridge -->
            <path d="M-10 -30 L10 40 L-20 48" stroke="#ea580c" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Berry Red Lips (Animated with Smirk) -->
            <path d="M-70 125 Q0 {132 + mouth_open} 70 120" stroke="#be123c" stroke-width="10" stroke-linecap="round" fill="{ '#4c0519' if mouth_open > 3 else 'none' }"/>
            <path d="M-55 125 Q0 110 55 125" stroke="#9f1239" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Sleek Jet-Black Asymmetrical Bob Hair with Violet Highlights -->
            <path d="M-240 -180 C-220 -380, 240 -380, 220 -180 C270 90, 270 290, 150 360 C120 180, 80 20, 80 -40 C-30 -100, -170 0, -220 90 Z" fill="url(#aishaHair2)"/>
            <!-- Flowing hair specular sheen -->
            <path d="M-160 -260 Q0 -300 160 -260" stroke="#a5b4fc" stroke-width="6" fill="none" opacity="0.6"/>
            <path d="M-180 -180 Q-210 20 -140 180" stroke="#818cf8" stroke-width="5" fill="none" opacity="0.45"/>
          </g>

          <!-- Cutting Chai Glass in Aisha's Hand (Raising to lips / taking sip) -->
          <g transform="translate(960, {sip_y})">
            <!-- Glass Shadow -->
            <ellipse cx="0" cy="115" rx="50" ry="12" fill="#000000" opacity="0.4"/>
            <!-- Glass Body with Chai Liquid & Glass Reflections -->
            <polygon points="-42,0 42,0 34,110 -34,110" fill="#f59e0b" stroke="#ffffff" stroke-width="6"/>
            <polygon points="-36,15 36,15 30,105 -30,105" fill="#d97706"/>
            <!-- Glass Rim Highlight -->
            <ellipse cx="0" cy="0" rx="42" ry="10" fill="none" stroke="#ffffff" stroke-width="4"/>
            <!-- Elegant Fingers holding glass -->
            <path d="M-55 35 Q-40 45 -42 60" stroke="#fed7aa" stroke-width="14" stroke-linecap="round" fill="none"/>
            <path d="M-52 65 Q-38 75 -40 90" stroke="#fed7aa" stroke-width="13" stroke-linecap="round" fill="none"/>
            <!-- Steam Wisps -->
            <path d="M-10 -15 Q0 -45 -15 -75 Q0 -105 -10 -135" stroke="#ffffff" stroke-width="4.5" fill="none" opacity="{0.55 + 0.3*math.sin(t*5.0)}"/>
            <path d="M15 -10 Q25 -40 10 -70 Q25 -100 15 -130" stroke="#ffffff" stroke-width="3.5" fill="none" opacity="{0.45 + 0.25*math.cos(t*4.0)}"/>
          </g>
        </svg>"""

        doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
        pix = doc[0].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if overlay is not None:
            alpha = 1.0
            if f < 24:
                alpha = max(0.0, f / 24.0)
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
    print(f"Scene 2 Complete: {output_mp4}")

# =============================================================================
# SCENE 3: THE IPAD REVEAL & JAW DROP (VIKRAM SHOCK) (8.0s = 192 frames)
# =============================================================================
def render_scene_3(output_mp4):
    print("Rendering Scene 3: The iPad Reveal & Jaw Drop (1920x1080, 192 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 192
    overlay = load_overlay("badge_beat_03.png")

    for f in range(total_frames):
        t = f / FPS
        # Shock progression: starts cocky f=0..20, shock hits f=25, jaw drops f=30..60, biscuit slips f=50..95
        shock_prog = min(1.0, max(0.0, (f - 24) / 36.0))
        jaw_drop = int(shock_prog * 36)
        pupil_dilate = shock_prog * 8
        sweat_drop_y = int(min(60, (f - 30) * 1.5)) if f > 30 else 0

        # Biscuit falling physics
        if f > 45:
            biscuit_t = (f - 45) / 40.0
            biscuit_y = min(180, int(0.5 * 980 * (biscuit_t**2)))
            splash = max(0, int((f - 80) * 1.5)) if f > 75 else 0
        else:
            biscuit_y = 0
            splash = 0

        # Vikram speaking: "व्हाट?! 'आयशा इज़ द न्यू प्रोजेक्ट हेड'..."
        is_speaking = (f >= 30 and f <= 170)
        speech_jaw = int(abs(math.sin(t * 16.0)) * 14) if is_speaking else 0

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
          <defs>
            <linearGradient id="bg3" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#090d16"/>
              <stop offset="60%" stop-color="#141a29"/>
              <stop offset="100%" stop-color="#1e2433"/>
            </linearGradient>
            <linearGradient id="ipadScreen" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0369a1"/>
              <stop offset="40%" stop-color="#0284c7"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
          </defs>

          <!-- Cafe Background with Dutch Angle Energy -->
          <rect width="{W}" height="{H}" fill="url(#bg3)"/>
          <polygon points="0,780 1920,780 1920,1080 0,1080" fill="#241711"/>
          <line x1="0" y1="780" x2="1920" y2="780" stroke="#451a03" stroke-width="6"/>

          <!-- iPad Spun Forward Towards Vikram (Left/Center) -->
          <g transform="translate(380, 260) rotate(-2)">
            <!-- Aluminum Chassis with Screen Glow Aura -->
            <rect x="-15" y="-15" width="670" height="470" rx="28" fill="#38bdf8" opacity="0.3"/>
            <rect x="0" y="0" width="640" height="440" rx="22" fill="#1e293b" stroke="#38bdf8" stroke-width="6"/>
            <!-- Glowing Retina Display -->
            <rect x="25" y="25" width="590" height="390" rx="14" fill="url(#ipadScreen)"/>

            <!-- Email Interface Content -->
            <text x="50" y="80" font-family="'Montserrat', sans-serif" font-size="20" font-weight="800" fill="#38bdf8" letter-spacing="2">APEX GLOBAL • EXECUTIVE VERDICT</text>
            <line x1="50" y1="100" x2="590" y2="100" stroke="#38bdf8" stroke-width="2" opacity="0.5"/>
            <text x="50" y="155" font-family="'Montserrat', sans-serif" font-size="36" font-weight="800" fill="#ffffff">"LOVED AISHA'S PITCH!"</text>
            <text x="50" y="215" font-family="'Montserrat', sans-serif" font-size="24" font-weight="600" fill="#f8fafc">Aisha appointed as Lead Director</text>
            <text x="50" y="265" font-family="'Montserrat', sans-serif" font-size="22" font-weight="600" fill="#f59e0b">Vikram: Assigned as Junior Assistant</text>

            <!-- Verified Stamp Badge -->
            <g transform="translate(460, 310)">
              <circle cx="45" cy="45" r="40" fill="#10b981"/>
              <path d="M28 45 L40 58 L64 32" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            </g>
          </g>

          <!-- VIKRAM (Right: Jaw Drop Disbelief) -->
          <g transform="translate(1380, 380)">
            <!-- Quilted Bomber Jacket -->
            <path d="M-180 240 L-100 440 L340 440 L280 240 Z" fill="#047857"/>

            <!-- Head & Shocked Dropped Jaw -->
            <path d="M-90 -120 Q0 -240 140 -120 Q160 80 0 160 Q-120 80 -90 -120 Z" fill="#fcd34d"/>
            <path d="M-60 60 Q0 180 80 60 L60 100 Q0 160 -40 100 Z" fill="#78350f" opacity="0.25"/>

            <!-- Giant Shocked Eyes behind Askew Tortoiseshell Glasses -->
            <rect x="-80" y="-70" width="{65 + pupil_dilate}" height="{50 + pupil_dilate}" rx="8" fill="none" stroke="#78350f" stroke-width="6"/>
            <rect x="25" y="-70" width="{65 + pupil_dilate}" height="{50 + pupil_dilate}" rx="8" fill="none" stroke="#78350f" stroke-width="6"/>
            <line x1="-15" y1="-45" x2="25" y2="-45" stroke="#78350f" stroke-width="6"/>

            <!-- Dilated Shocked Pupils -->
            <ellipse cx="-45" cy="-45" rx="{10 + pupil_dilate}" ry="{12 + pupil_dilate}" fill="#ffffff"/>
            <circle cx="-45" cy="-45" r="{7 + pupil_dilate*0.6}" fill="#1e1b4b"/>
            <circle cx="-48" cy="-48" r="3" fill="#ffffff"/>
            <ellipse cx="60" cy="-45" rx="{10 + pupil_dilate}" ry="{12 + pupil_dilate}" fill="#ffffff"/>
            <circle cx="60" cy="-45" r="{7 + pupil_dilate*0.6}" fill="#1e1b4b"/>
            <circle cx="57" cy="-48" r="3" fill="#ffffff"/>

            <!-- High Shocked Eyebrows -->
            <path d="M-85 {-105 - shock_prog*18} Q-45 {-130 - shock_prog*18} -5 {-105 - shock_prog*18}" stroke="#18181b" stroke-width="7" stroke-linecap="round" fill="none"/>
            <path d="M20 {-105 - shock_prog*18} Q60 {-130 - shock_prog*18} 100 {-105 - shock_prog*18}" stroke="#18181b" stroke-width="7" stroke-linecap="round" fill="none"/>

            <!-- Dropped 'O' Jaw Mouth (Animated) -->
            <ellipse cx="10" cy="{80 + jaw_drop*0.5}" rx="{24 + speech_jaw*0.6}" ry="{32 + jaw_drop + speech_jaw}" fill="#451a03"/>
            <ellipse cx="10" cy="{70 + jaw_drop*0.5}" rx="16" ry="10" fill="#dc2626"/>

            <!-- Cold Sweat Droplet running down temple -->
            <path d="M95 {-80 + sweat_drop_y} Q105 {-65 + sweat_drop_y} 95 {-55 + sweat_drop_y} Q85 {-65 + sweat_drop_y} 95 {-80 + sweat_drop_y} Z" fill="#38bdf8"/>

            <!-- Quiff Hair -->
            <path d="M-95 -120 C-90 -250, 140 -250, 135 -120 C140 -90, 130 -60, 120 -50 C110 -110, 85 -160, 20 -165 C-45 -160, -70 -110, -85 -50 Z" fill="#18181b"/>
          </g>

          <!-- Parle-G Biscuit Dropping & Splashing into Cutting Chai Glass -->
          <g transform="translate(1120, 750)">
            <!-- Chai Glass -->
            <polygon points="-35,0 35,0 28,100 -28,100" fill="#f59e0b" stroke="#ffffff" stroke-width="5"/>
            <!-- Biscuit (Falling trajectory) -->
            <g transform="translate(0, {biscuit_y}) rotate(18)">
              <rect x="-30" y="-16" width="60" height="32" rx="4" fill="#d97706" stroke="#b45309" stroke-width="2"/>
              <text x="0" y="5" font-family="'Montserrat'" font-size="12" font-weight="800" fill="#78350f" text-anchor="middle">PARLE</text>
            </g>
            <!-- Splash droplets when biscuit hits chai -->
            {' '.join([f'<circle cx="{i*14 - 28}" cy="{-splash - abs(i)*4}" r="{max(1, 6 - abs(i))}" fill="#f59e0b"/>' for i in range(-2, 3)]) if splash > 0 else ''}
          </g>
        </svg>"""

        doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
        pix = doc[0].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if overlay is not None:
            alpha = 1.0
            if f < 24:
                alpha = max(0.0, f / 24.0)
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
    print(f"Scene 3 Complete: {output_mp4}")

# =============================================================================
# SCENE 4: THE PLAYFUL WINK & UPI SURRENDER (7.5s = 180 frames)
# =============================================================================
def render_scene_4(output_mp4):
    print("Rendering Scene 4: The Playful Wink & UPI Surrender (1920x1080, 180 frames)...")
    proc = start_ffmpeg_pipe(output_mp4)
    total_frames = 180
    badge_overlay = load_overlay("badge_beat_04.png")
    outro_overlay = load_overlay("outro_title_card.png")

    for f in range(total_frames):
        t = f / FPS
        # Aisha Speaking & Toast Wink:
        # Dialogue: "हाँ... और इस जीत की चाय के पैसे तुम दोगे, पार्टनर!"
        is_speaking = (f >= 0 and f <= 135)
        mouth_open = int(abs(math.sin(t * 15.0)) * 12) if is_speaking else 0
        
        # Wink timing: winks on "पार्टनर" between f=75 and f=140!
        is_winking = (f >= 72 and f <= 140)

        # Vikram pulling out phone & tapping UPI payment: f=40..160
        phone_y = min(120, max(0, int((f - 40) * 2.5)))

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
          <defs>
            <linearGradient id="bg4" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0a1020"/>
              <stop offset="50%" stop-color="#182035"/>
              <stop offset="100%" stop-color="#2a182c"/>
            </linearGradient>
            <linearGradient id="wetStreet" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#261c24"/>
              <stop offset="100%" stop-color="#0f0c12"/>
            </linearGradient>
          </defs>

          <!-- Cafe Atmosphere Background -->
          <rect width="{W}" height="{H}" fill="url(#bg4)"/>

          <!-- Rain-Washed Wet Pavement Reflections Outside -->
          <polygon points="0,820 1920,820 1920,1080 0,1080" fill="url(#wetStreet)"/>
          <line x1="0" y1="820" x2="1920" y2="820" stroke="#4a3b47" stroke-width="5"/>
          <!-- Neon puddle ripples -->
          <ellipse cx="500" cy="940" rx="280" ry="25" fill="#f43f5e" opacity="0.22"/>
          <ellipse cx="1400" cy="950" rx="320" ry="25" fill="#38bdf8" opacity="0.25"/>

          <!-- AISHA (Left Hero Position, Raising Toast with Playful Wink) -->
          <g transform="translate(560, 440)">
            <!-- Mustard Coat & Turtleneck -->
            <path d="M-280 260 L-140 140 L0 220 L140 140 L280 260 L320 460 L-320 460 Z" fill="#ca8a04"/>
            <path d="M-90 120 L90 120 L70 220 L-70 220 Z" fill="#18181b"/>
            <!-- Head & Face -->
            <path d="M-150 -100 Q0 -220 150 -100 Q180 120 0 220 Q-180 120 -150 -100 Z" fill="#fed7aa"/>

            <!-- Eyes: Left Eye Open Sparkling Joyfully -->
            <ellipse cx="-70" cy="-20" rx="26" ry="14" fill="#ffffff"/>
            <circle cx="-68" cy="-20" r="11" fill="#451a03"/>
            <circle cx="-68" cy="-20" r="6" fill="#1c1917"/>
            <circle cx="-72" cy="-24" r="3.5" fill="#ffffff"/>
            <path d="M-105 -28 Q-70 -45 -35 -28" stroke="#0f172a" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Right Eye: ELEGANT WINK when is_winking! -->
            {'''
            <path d="M35 -20 Q70 -5 105 -20" stroke="#0f172a" stroke-width="7" stroke-linecap="round" fill="none"/>
            <path d="M102 -22 L115 -30" stroke="#0f172a" stroke-width="5" stroke-linecap="round"/>
            <path d="M35 -45 Q70 -62 105 -45" stroke="#0f172a" stroke-width="5" stroke-linecap="round" fill="none"/>
            ''' if is_winking else '''
            <ellipse cx="70" cy="-20" rx="26" ry="14" fill="#ffffff"/>
            <circle cx="68" cy="-20" r="11" fill="#451a03"/>
            <circle cx="64" cy="-24" r="3.5" fill="#ffffff"/>
            <path d="M35 -28 Q70 -45 105 -28" stroke="#0f172a" stroke-width="6" stroke-linecap="round" fill="none"/>
            '''}

            <!-- Nose -->
            <path d="M-8 -5 L8 35 L-12 42" stroke="#ea580c" stroke-width="4.5" stroke-linecap="round" fill="none"/>

            <!-- Triumphant Smiling Berry Lips (Showing Teeth) -->
            <path d="M-55 85 Q0 {110 + mouth_open} 55 85 Z" fill="#be123c"/>
            <path d="M-45 88 Q0 102 45 88 Z" fill="#ffffff"/>

            <!-- Asymmetrical Bob Cut Hair -->
            <path d="M-170 -100 C-150 -250, 170 -250, 160 -100 C190 90, 190 230, 110 280 C80 140, 50 20, 50 -20 C-20 -70, -120 0, -150 70 Z" fill="#1e1b4b"/>
            <!-- Ear Cuff -->
            <circle cx="-155" cy="5" r="7" fill="#f8fafc"/>

            <!-- Hand Raising Cutting Chai Glass in Toast (Right Arm) -->
            <path d="M160 160 L280 20 L240 -10 L120 120 Z" fill="#ca8a04"/>
            <!-- Raised Cutting Glass -->
            <polygon points="260,-40 330,-40 318,50 272,50" fill="#f59e0b" stroke="#ffffff" stroke-width="5"/>
            <!-- Toast Clink Sparkle Stars! -->
            <polygon points="295,-60 298,-48 310,-48 300,-40 304,-28 295,-34 286,-28 290,-40 280,-48 292,-48" fill="#fcd34d"/>
          </g>

          <!-- VIKRAM (Right: Sheepish Smile & UPI Payment Surrender) -->
          <g transform="translate(1380, 480)">
            <path d="M-160 220 L-90 420 L300 420 L240 220 Z" fill="#047857"/>

            <!-- Head & Glasses -->
            <path d="M-70 -80 Q0 -180 120 -80 Q140 80 0 140 Q-90 80 -70 -80 Z" fill="#fcd34d"/>
            <rect x="-60" y="-40" width="50" height="38" rx="6" fill="none" stroke="#78350f" stroke-width="5"/>
            <rect x="20" y="-40" width="50" height="38" rx="6" fill="none" stroke="#78350f" stroke-width="5"/>

            <!-- Sheepish Squinting Eyes -->
            <path d="M-48 -22 Q-35 -12 -22 -22" stroke="#18181b" stroke-width="5" fill="none"/>
            <path d="M32 -22 Q45 -12 58 -22" stroke="#18181b" stroke-width="5" fill="none"/>

            <!-- Sheepish Amused Grin -->
            <path d="M-35 60 Q10 78 55 52" stroke="#78350f" stroke-width="6" stroke-linecap="round" fill="none"/>

            <!-- Quiff Hair -->
            <path d="M-75 -80 C-70 -180, 120 -180, 115 -80 C120 -50, 110 -20, 100 -10 C90 -60, 70 -110, 20 -115 C-35 -110, -50 -60, -65 -10 Z" fill="#18181b"/>

            <!-- Smartphone in Hand (Tapping UPI Payment) -->
            <g transform="translate(-120, {260 - phone_y})">
              <!-- Smartphone Body -->
              <rect x="0" y="0" width="95" height="160" rx="14" fill="#0f172a" stroke="#10b981" stroke-width="5"/>
              <rect x="10" y="15" width="75" height="130" rx="8" fill="#1e293b"/>
              <!-- Green UPI Payment Success / QR Icon -->
              <circle cx="47" cy="70" r="24" fill="#10b981"/>
              <path d="M37 70 L44 77 L57 63" stroke="#ffffff" stroke-width="5" stroke-linecap="round" fill="none"/>
              <text x="47" y="115" font-family="'Montserrat'" font-size="11" font-weight="800" fill="#10b981" text-anchor="middle">PAID ₹40</text>
            </g>
          </g>
        </svg>"""

        doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
        pix = doc[0].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Composite HarfBuzz Lower-Third Badge (First half f=0..90)
        if f < 96 and badge_overlay is not None:
            alpha = 1.0
            if f < 20:
                alpha = max(0.0, f / 20.0)
            elif f > 75:
                alpha = max(0.0, (96 - f) / 21.0)
            if alpha > 0.0:
                cur_overlay = badge_overlay.copy()
                if alpha < 1.0:
                    r, g, b, a = cur_overlay.split()
                    a = a.point(lambda p: int(p * alpha))
                    cur_overlay.putalpha(a)
                img.paste(cur_overlay, (0, 0), cur_overlay)

        # Composite Outro Title Card (Second half f=100..180)
        if f >= 100 and outro_overlay is not None:
            outro_alpha = min(1.0, (f - 100) / 24.0)
            cur_outro = outro_overlay.copy()
            if outro_alpha < 1.0:
                r, g, b, a = cur_outro.split()
                a = a.point(lambda p: int(p * outro_alpha))
                cur_outro.putalpha(a)
            img.paste(cur_outro, (0, 0), cur_outro)

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"Scene 4 Complete: {output_mp4}")

if __name__ == "__main__":
    s1 = os.path.join(SCENES_DIR, "scene_01.mp4")
    s2 = os.path.join(SCENES_DIR, "scene_02.mp4")
    s3 = os.path.join(SCENES_DIR, "scene_03.mp4")
    s4 = os.path.join(SCENES_DIR, "scene_04.mp4")

    render_scene_1(s1)
    render_scene_2(s2)
    render_scene_3(s3)
    render_scene_4(s4)
    print("\nALL 4 SCENES RENDERED IN BROADCAST-GRADE 1080p!")
