"""
render_scenes_773.py
====================
Renders the 8 high-fidelity 1080p 2D animated scenes for:
"लास्ट बग" (The Last Bug) - 60.00s Animated Short

Resolution: 1920x1080
Frame Rate: 24.0 FPS Constant Frame Rate
Total Frames: 1524 (Scenes 1-7: 192 frames each, Scene 8: 180 frames)
Alpha compositing of HarfBuzz Devanagari overlays.
"""

import os
import sys
import time
import math
import subprocess
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3"
SCENES_DIR = os.path.join(BASE_DIR, "scenes_1080p")
OVERLAYS_DIR = os.path.join(BASE_DIR, "overlays_1080p")
os.makedirs(SCENES_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
WIDTH = 1920
HEIGHT = 1080
FPS = 24

def open_ffmpeg_pipe(out_mp4):
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        out_mp4
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_svg_to_image(svg_str):
    doc = fitz.open(stream=svg_str.encode("utf-8"), filetype="svg")
    pix = doc[0].get_pixmap(dpi=96)
    # Convert pixmap samples to PIL Image (RGB)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def load_overlay(filename):
    path = os.path.join(OVERLAYS_DIR, filename)
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    return None

# =============================================================================
# SCENE 1: THE 3:00 AM RED ALERT (192 frames, 8.0s)
# =============================================================================
def render_scene_01():
    out_mp4 = os.path.join(SCENES_DIR, "scene_01.mp4")
    overlay = load_overlay("badge_scene_01.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 1 (The 3:00 AM Red Alert) [192 frames]...")

    for f in range(192):
        t = f / FPS
        # Red pulsing emergency screen glow
        alarm_pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 2.5 * t)
        glow_color = f"rgba(239, 68, 68, {0.15 + 0.25 * alarm_pulse:.2f})"
        
        # Kabir head shaking in panic
        shake_x = 960 + 8.0 * math.sin(18.0 * t)
        shake_y = 620 + 4.0 * math.cos(14.0 * t)
        mouth_open = 28 + 14 * abs(math.sin(10.0 * t))
        
        # Scenery SVG
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Dark Dev Studio at 3:00 AM -->
          <rect width="1920" height="1080" fill="#090d16"/>
          <!-- Window blinds with night shadows -->
          <line x1="200" y1="100" x2="600" y2="100" stroke="#1e293b" stroke-width="8"/>
          <line x1="200" y1="180" x2="600" y2="180" stroke="#1e293b" stroke-width="8"/>
          <line x1="200" y1="260" x2="600" y2="260" stroke="#1e293b" stroke-width="8"/>
          <!-- Clock on wall showing 3:02 AM -->
          <circle cx="1600" cy="180" r="45" fill="#1e293b" stroke="#475569" stroke-width="4"/>
          <line x1="1600" y1="180" x2="1600" y2="155" stroke="#ef4444" stroke-width="4"/>
          <line x1="1600" y1="180" x2="1625" y2="180" stroke="#ffffff" stroke-width="4"/>
          <text x="1600" y="245" font-family="sans-serif" font-size="14" font-weight="700" fill="#ef4444" text-anchor="middle">3:02 AM</text>
          
          <!-- Giant Fatal Crash Monitor -->
          <rect x="460" y="160" width="1000" height="520" rx="18" fill="#180606" stroke="#ef4444" stroke-width="6"/>
          <rect x="460" y="160" width="1000" height="520" rx="18" fill="{glow_color}"/>
          <text x="960" y="260" font-family="sans-serif" font-size="42" font-weight="800" fill="#ef4444" text-anchor="middle">FATAL PRODUCTION CRASH</text>
          <text x="960" y="320" font-family="sans-serif" font-size="22" font-weight="600" fill="#fca5a5" text-anchor="middle">THREAD 0x8F94: UNRESPONSIVE DEADLOCK • 504 GATEWAY TIMEOUT</text>
          
          <!-- Scrolling Crash Hex Logs -->
          <text x="520" y="400" font-family="monospace" font-size="16" fill="#f87171">[ERR] 03:02:11 Kernel panic: System execution halted by recursive trap</text>
          <text x="520" y="435" font-family="monospace" font-size="16" fill="#f87171">[ERR] 03:02:12 Fatal key queue overflow: 104,857 events queued</text>
          <text x="520" y="470" font-family="monospace" font-size="16" fill="#f87171">[CRIT] Database auto-rollback failed. Retrying dump...</text>
          
          <!-- Studio Desk -->
          <rect x="200" y="780" width="1520" height="300" fill="#111827" stroke="#1f2937" stroke-width="6"/>
          
          <!-- Kabir Clutching Hair in Panic -->
          <!-- Torso in Coral Hoodie -->
          <path d="M780,820 Q960,740 1140,820 L1110,1080 L810,1080 Z" fill="#f97316"/>
          <path d="M960,780 L960,940" stroke="#ea580c" stroke-width="5"/>
          <!-- Head -->
          <circle cx="{shake_x}" cy="{shake_y}" r="110" fill="#fdba74"/>
          <!-- Backwards Cap & Dark Slate Curly Hair -->
          <path d="M{shake_x - 110},{shake_y - 30} Q{shake_x},{shake_y - 120} {shake_x + 110},{shake_y - 30} Q{shake_x},{shake_y - 160} {shake_x - 110},{shake_y - 30} Z" fill="#334155"/>
          <path d="M{shake_x - 80},{shake_y - 80} Q{shake_x + 80},{shake_y - 90} {shake_x + 130},{shake_y - 70}" stroke="#475569" stroke-width="12" fill="none" stroke-linecap="round"/>
          <!-- Wide Panic Eyes -->
          <ellipse cx="{shake_x - 45}" cy="{shake_y - 10}" rx="20" ry="17" fill="#ffffff"/>
          <circle cx="{shake_x - 45}" cy="{shake_y - 10}" r="8" fill="#78350f"/>
          <ellipse cx="{shake_x + 45}" cy="{shake_y - 10}" rx="20" ry="17" fill="#ffffff"/>
          <circle cx="{shake_x + 45}" cy="{shake_y - 10}" r="8" fill="#78350f"/>
          <!-- Wide Open Agonized Mouth -->
          <ellipse cx="{shake_x}" cy="{shake_y + 55}" rx="30" ry="{mouth_open}" fill="#7f1d1d"/>
          <!-- Flailing Arms Clutching Hair -->
          <path d="M780,850 Q750,680 {shake_x - 90},{shake_y - 20}" stroke="#f97316" stroke-width="32" fill="none" stroke-linecap="round"/>
          <path d="M1140,850 Q1170,680 {shake_x + 90},{shake_y - 20}" stroke="#f97316" stroke-width="32" fill="none" stroke-linecap="round"/>
          <circle cx="{shake_x - 90}" cy="{shake_y - 20}" r="22" fill="#fdba74"/>
          <circle cx="{shake_x + 90}" cy="{shake_y - 20}" r="22" fill="#fdba74"/>
        </svg>"""

        base_img = render_svg_to_image(svg)
        
        # Dialogue overlay from frame 15 to 175
        if overlay and 15 <= f <= 175:
            # Subtle smooth fade in/out
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 1 rendered successfully!")

# =============================================================================
# SCENE 2: THE CONSPIRACY & COFFEE (192 frames, 8.0s)
# =============================================================================
def render_scene_02():
    out_mp4 = os.path.join(SCENES_DIR, "scene_02.mp4")
    overlay = load_overlay("badge_scene_02.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 2 (The Conspiracy & Coffee) [192 frames]...")

    for f in range(192):
        t = f / FPS
        # Meera walking in from right: x moves from 1580 to 1320
        walk_progress = min(1.0, f / 60.0)
        meera_x = 1580 - (1580 - 1320) * (1.0 - math.cos(walk_progress * math.pi * 0.5))
        meera_bob = 6.0 * abs(math.sin(walk_progress * math.pi * 4.0)) if walk_progress < 1.0 else 0
        
        # Steam rising from coffee mug
        steam_y = 600 - 30.0 * ((f % 40) / 40.0)
        steam_alpha = 1.0 - ((f % 40) / 40.0)
        
        # Kabir waving hands nervously
        kabir_arm_angle = 15.0 * math.sin(12.0 * t)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Studio Interior with glass divider -->
          <rect width="1920" height="1080" fill="#0c1322"/>
          <line x1="960" y1="0" x2="960" y2="800" stroke="#1e293b" stroke-width="8"/>
          <!-- Bengaluru City lights through window -->
          <rect x="100" y="100" width="760" height="500" fill="#070c18" stroke="#1e293b" stroke-width="4"/>
          <rect x="200" y="320" width="40" height="280" fill="#1e293b"/>
          <rect x="280" y="240" width="60" height="360" fill="#172554"/>
          <rect x="380" y="280" width="50" height="320" fill="#1e293b"/>
          <!-- Tiny glowing yellow building windows -->
          <circle cx="215" cy="360" r="3" fill="#facc15"/><circle cx="215" cy="400" r="3" fill="#facc15"/>
          <circle cx="300" cy="280" r="3" fill="#facc15"/><circle cx="320" cy="320" r="3" fill="#facc15"/>
          
          <!-- Desk in foreground -->
          <rect x="0" y="780" width="1920" height="300" fill="#0f172a" stroke="#1e293b" stroke-width="4"/>
          
          <!-- Kabir Pacing / Gesticulating on Left -->
          <path d="M420,830 Q560,760 700,830 L670,1080 L450,1080 Z" fill="#f97316"/>
          <circle cx="560" cy="560" r="95" fill="#fdba74"/>
          <!-- Backwards cap -->
          <path d="M465,530 Q560,460 655,530 Q560,420 465,530 Z" fill="#334155"/>
          <path d="M490,490 Q620,480 670,500" stroke="#475569" stroke-width="10" fill="none" stroke-linecap="round"/>
          <ellipse cx="530" cy="550" rx="16" ry="14" fill="#ffffff"/><circle cx="530" cy="550" r="7" fill="#78350f"/>
          <ellipse cx="590" cy="550" rx="16" ry="14" fill="#ffffff"/><circle cx="590" cy="550" r="7" fill="#78350f"/>
          <path d="M535,605 Q560,585 585,605" stroke="#78350f" stroke-width="6" fill="none" stroke-linecap="round"/>
          <!-- Kabir gesturing arm -->
          <path d="M680,830 L{780 + kabir_arm_angle},{700 - kabir_arm_angle}" stroke="#f97316" stroke-width="28" stroke-linecap="round"/>
          
          <!-- Meera Walking In Calmly on Right -->
          <!-- Denim Jacket -->
          <path d="M{meera_x - 140},{840 - meera_bob} Q{meera_x},{770 - meera_bob} {meera_x + 140},{840 - meera_bob} L{meera_x + 120},1080 L{meera_x - 120},1080 Z" fill="#2563eb"/>
          <circle cx="{meera_x}" cy="{540 - meera_bob}" r="90" fill="#fed7aa"/>
          <!-- High Bun Hair with Lavender Streak -->
          <circle cx="{meera_x + 20}" cy="{420 - meera_bob}" r="45" fill="#1e293b"/>
          <path d="M{meera_x - 90},{520 - meera_bob} Q{meera_x},{430 - meera_bob} {meera_x + 90},{520 - meera_bob} Z" fill="#1e293b"/>
          <path d="M{meera_x - 40},{460 - meera_bob} Q{meera_x},{450 - meera_bob} {meera_x + 60},{480 - meera_bob}" stroke="#c084fc" stroke-width="12" fill="none" stroke-linecap="round"/>
          <!-- Glasses -->
          <circle cx="{meera_x - 38}" cy="{540 - meera_bob}" r="28" fill="none" stroke="#38bdf8" stroke-width="5"/>
          <circle cx="{meera_x + 38}" cy="{540 - meera_bob}" r="28" fill="none" stroke="#38bdf8" stroke-width="5"/>
          <line x1="{meera_x - 10}" y1="{540 - meera_bob}" x2="{meera_x + 10}" y2="{540 - meera_bob}" stroke="#38bdf8" stroke-width="4"/>
          <circle cx="{meera_x - 38}" cy="{540 - meera_bob}" r="7" fill="#1e293b"/>
          <circle cx="{meera_x + 38}" cy="{540 - meera_bob}" r="7" fill="#1e293b"/>
          <!-- Gentle Calm Smirk -->
          <path d="M{meera_x - 20},{595 - meera_bob} Q{meera_x},{610 - meera_bob} {meera_x + 25},{595 - meera_bob}" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
          
          <!-- Steaming Coffee Mug in Meera's Hand -->
          <rect x="{meera_x - 120}" y="{670 - meera_bob}" width="50" height="68" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="4"/>
          <path d="M{meera_x - 125},{685 - meera_bob} Q{meera_x - 145},{700 - meera_bob} {meera_x - 125},{720 - meera_bob}" stroke="#cbd5e1" stroke-width="5" fill="none"/>
          <path d="M{meera_x - 95},{steam_y} Q{meera_x - 85},{steam_y - 20} {meera_x - 95},{steam_y - 40}" stroke="rgba(248, 250, 252, {steam_alpha:.2f})" stroke-width="4" fill="none"/>
        </svg>"""

        base_img = render_svg_to_image(svg)
        if overlay and 15 <= f <= 175:
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 2 rendered successfully!")

# =============================================================================
# SCENE 3: THE DESPERATE ESCALATION (192 frames, 8.0s)
# =============================================================================
def render_scene_03():
    out_mp4 = os.path.join(SCENES_DIR, "scene_03.mp4")
    overlay = load_overlay("badge_scene_03.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 3 (The Desperate Escalation) [192 frames]...")

    for f in range(192):
        t = f / FPS
        # Camera slow zoom into giant format button
        zoom = 1.0 + 0.15 * (f / 192.0)
        # Trembling hand hovering with mouse
        tremble_x = 520 + 8.0 * math.sin(28.0 * t)
        tremble_y = 560 + 6.0 * math.cos(32.0 * t)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#1a0b16"/>
          
          <g transform="translate(960, 540) scale({zoom}) translate(-960, -540)">
            <!-- Terminal Dialog Box -->
            <rect x="360" y="200" width="1200" height="600" rx="24" fill="#0d0811" stroke="#dc2626" stroke-width="8"/>
            <rect x="360" y="200" width="1200" height="70" rx="24" fill="#7f1d1d"/>
            <text x="420" y="245" font-family="sans-serif" font-size="24" font-weight="800" fill="#ffffff">SYSTEM DISASTER RECOVERY PROTOCOL</text>
            <circle cx="1500" cy="235" r="12" fill="#ef4444"/>
            
            <!-- Warning Sign -->
            <polygon points="960,300 910,390 1010,390" fill="#eab308" stroke="#ca8a04" stroke-width="4"/>
            <text x="960" y="375" font-family="sans-serif" font-size="34" font-weight="900" fill="#78350f" text-anchor="middle">!</text>
            <text x="960" y="440" font-family="sans-serif" font-size="28" font-weight="700" fill="#fee2e2" text-anchor="middle">DATABASE CORRUPTION DETECTED</text>
            
            <!-- GIANT RED FORMAT BUTTON -->
            <rect x="460" y="480" width="1000" height="240" rx="28" fill="#dc2626" stroke="#f87171" stroke-width="8"/>
            <rect x="480" y="495" width="960" height="100" rx="20" fill="rgba(255,255,255,0.15)"/>
            <text x="960" y="585" font-family="sans-serif" font-size="52" font-weight="900" fill="#ffffff" text-anchor="middle">FORMAT & PURGE DATABASE</text>
            <text x="960" y="660" font-family="sans-serif" font-size="24" font-weight="700" fill="#fecaca" text-anchor="middle">WARNING: THIS OPERATION IS COMPLETE AND IRREVERSIBLE</text>
          </g>
          
          <!-- Kabir's Trembling Arm & Mouse Cursor in Foreground -->
          <path d="M200,900 L{tremble_x},{tremble_y}" stroke="#f97316" stroke-width="46" stroke-linecap="round"/>
          <!-- Hand & Ergonomic Mouse -->
          <ellipse cx="{tremble_x}" cy="{tremble_y}" rx="45" ry="32" fill="#fdba74"/>
          <rect x="{tremble_x - 20}" y="{tremble_y - 28}" width="40" height="55" rx="16" fill="#1e293b" stroke="#38bdf8" stroke-width="4"/>
          <line x1="{tremble_x}" y1="{tremble_y - 28}" x2="{tremble_x}" y2="{tremble_y}" stroke="#38bdf8" stroke-width="3"/>
          <!-- Sweating beads flying off -->
          <ellipse cx="{tremble_x + 50}" cy="{tremble_y - 40}" rx="6" ry="10" fill="#38bdf8" transform="rotate(30 {tremble_x + 50} {tremble_y - 40})"/>
        </svg>"""

        base_img = render_svg_to_image(svg)
        if overlay and 15 <= f <= 175:
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 3 rendered successfully!")

# =============================================================================
# SCENE 4: INVESTIGATION & DISCOVERY (192 frames, 8.0s)
# =============================================================================
def render_scene_04():
    out_mp4 = os.path.join(SCENES_DIR, "scene_04.mp4")
    overlay = load_overlay("badge_scene_04.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 4 (Investigation & Discovery) [192 frames]...")

    for f in range(192):
        t = f / FPS
        # Meera adjusts glasses with knuckle
        glasses_lift = 5.0 * math.sin(min(math.pi, f / 40.0 * math.pi))
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#051324"/>
          
          <!-- Meera Medium Close-up peering intently -->
          <circle cx="960" cy="{420 - glasses_lift}" r="140" fill="#fed7aa"/>
          <!-- High Bun & Lavender Streak -->
          <circle cx="980" cy="{260 - glasses_lift}" r="55" fill="#1e293b"/>
          <path d="M820,{380 - glasses_lift} Q960,{280 - glasses_lift} 1100,{380 - glasses_lift} Z" fill="#1e293b"/>
          <path d="M880,{330 - glasses_lift} Q960,{310 - glasses_lift} 1030,{340 - glasses_lift}" stroke="#c084fc" stroke-width="16" fill="none" stroke-linecap="round"/>
          
          <!-- Circular Blue Wire-rim Glasses with Screen Reflections -->
          <circle cx="895" cy="{420 - glasses_lift}" r="42" fill="none" stroke="#38bdf8" stroke-width="8"/>
          <circle cx="1025" cy="{420 - glasses_lift}" r="42" fill="none" stroke="#38bdf8" stroke-width="8"/>
          <line x1="937" y1="{420 - glasses_lift}" x2="983" y2="{420 - glasses_lift}" stroke="#38bdf8" stroke-width="6"/>
          
          <!-- Pupils looking down at debug console -->
          <ellipse cx="895" cy="{425 - glasses_lift}" rx="14" ry="12" fill="#1e293b"/>
          <ellipse cx="1025" cy="{425 - glasses_lift}" rx="14" ry="12" fill="#1e293b"/>
          <circle cx="890" cy="{420 - glasses_lift}" r="4" fill="#ffffff"/>
          <circle cx="1020" cy="{420 - glasses_lift}" r="4" fill="#ffffff"/>
          
          <!-- Inquisitive Eyebrow arch -->
          <path d="M860,{360 - glasses_lift} Q895,{340 - glasses_lift} 930,{365 - glasses_lift}" stroke="#78350f" stroke-width="6" fill="none" stroke-linecap="round"/>
          <path d="M990,{365 - glasses_lift} Q1025,{350 - glasses_lift} 1060,{360 - glasses_lift}" stroke="#78350f" stroke-width="6" fill="none" stroke-linecap="round"/>
          
          <!-- Debug Event Monitor in Foreground -->
          <rect x="360" y="620" width="1200" height="340" rx="16" fill="#080f1a" stroke="#0284c7" stroke-width="5"/>
          <rect x="360" y="620" width="1200" height="50" rx="16" fill="#0369a1"/>
          <text x="400" y="655" font-family="sans-serif" font-size="20" font-weight="700" fill="#ffffff">HARDWARE INPUT EVENT STREAM & KEYLOGGER</text>
          
          <text x="420" y="730" font-family="monospace" font-size="26" font-weight="800" fill="#f59e0b">[EVENT 0x011B] KEY_DOWN: KEY_ESCAPE (DURATION: 10,480,210 ms - STUCK!)</text>
          <text x="420" y="790" font-family="monospace" font-size="26" font-weight="800" fill="#f59e0b">[EVENT 0x0074] KEY_DOWN: KEY_F5     (DURATION: 10,480,210 ms - STUCK!)</text>
          <text x="420" y="850" font-family="monospace" font-size="22" font-weight="700" fill="#ef4444">[ALERT] 50,000 recursive page reloads queued. Host CPU throttled at 99.8%</text>
          <text x="420" y="900" font-family="monospace" font-size="22" font-weight="700" fill="#38bdf8">[STATUS] Physical keyboard switch held depressed continuously.</text>
        </svg>"""

        base_img = render_svg_to_image(svg)
        if overlay and 15 <= f <= 175:
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 4 rendered successfully!")

# =============================================================================
# SCENE 5: THE PHYSICAL CLUE (192 frames, 8.0s)
# =============================================================================
def render_scene_05():
    out_mp4 = os.path.join(SCENES_DIR, "scene_05.mp4")
    overlay = load_overlay("badge_scene_05.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 5 (The Physical Clue) [192 frames]...")

    for f in range(192):
        t = f / FPS
        # Camera panning down along glowing keyboard cable
        pan_y = 60.0 * (f / 192.0)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Top-down Birds Eye View of Desk -->
          <rect width="1920" height="1080" fill="#0f172a"/>
          <!-- Wood grain desk mat -->
          <rect x="200" y="140" width="1520" height="820" rx="24" fill="#1e293b" stroke="#334155" stroke-width="6"/>
          
          <!-- Braided Blue USB Keyboard Cable -->
          <path d="M960,140 Q940,{320 + pan_y} 780,{420 + pan_y}" stroke="#38bdf8" stroke-width="12" fill="none" stroke-linecap="round"/>
          
          <!-- Mechanical Keyboard Chassis -->
          <rect x="360" y="{340 + pan_y}" width="1200" height="420" rx="20" fill="#090d16" stroke="#64748b" stroke-width="6"/>
          
          <!-- Keycap Grid -->
          <!-- Top Function Row (ESC, F1-F12) -->
          <rect x="400" y="{370 + pan_y}" width="65" height="45" rx="6" fill="#ef4444"/> <!-- ESC pressed down -->
          <text x="432" y="{400 + pan_y}" font-family="sans-serif" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">ESC</text>
          
          <rect x="480" y="{370 + pan_y}" width="55" height="45" rx="6" fill="#334155"/><text x="507" y="{400 + pan_y}" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">F1</text>
          <rect x="545" y="{370 + pan_y}" width="55" height="45" rx="6" fill="#334155"/><text x="572" y="{400 + pan_y}" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">F2</text>
          <rect x="610" y="{370 + pan_y}" width="55" height="45" rx="6" fill="#334155"/><text x="637" y="{400 + pan_y}" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">F3</text>
          <rect x="675" y="{370 + pan_y}" width="55" height="45" rx="6" fill="#334155"/><text x="702" y="{400 + pan_y}" font-family="sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">F4</text>
          
          <rect x="745" y="{370 + pan_y}" width="65" height="45" rx="6" fill="#ef4444"/> <!-- F5 pressed down -->
          <text x="777" y="{400 + pan_y}" font-family="sans-serif" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">F5</text>
          
          <!-- Number Row & Spacebar -->
          <rect x="400" y="{430 + pan_y}" width="1120" height="240" rx="10" fill="#1e293b"/>
          <rect x="680" y="{685 + pan_y}" width="400" height="50" rx="8" fill="#475569"/>
          
          <!-- Heavy Steel Insulated Thermos resting on ESC -->
          <rect x="380" y="{260 + pan_y}" width="140" height="220" rx="30" fill="#cbd5e1" stroke="#475569" stroke-width="6"/>
          <ellipse cx="450" cy="{280 + pan_y}" rx="60" ry="24" fill="#94a3b8"/>
          <line x1="450" y1="{310 + pan_y}" x2="450" y2="{440 + pan_y}" stroke="#64748b" stroke-width="4"/>
          
          <!-- GIANT CRUMPLED PACKET OF HALDIRAM'S BHUJIA RESTING ON F5 -->
          <polygon points="680,{300 + pan_y} 980,{250 + pan_y} 1010,{490 + pan_y} 710,{540 + pan_y}" fill="#eab308" stroke="#ca8a04" stroke-width="6"/>
          <!-- Brand Badge -->
          <rect x="740" y="{340 + pan_y}" width="200" height="90" rx="12" fill="#b91c1c" stroke="#fef08a" stroke-width="4" transform="rotate(-8 840 {385 + pan_y})"/>
          <text x="840" y="{375 + pan_y}" font-family="sans-serif" font-size="20" font-weight="900" fill="#fef08a" text-anchor="middle" transform="rotate(-8 840 {385 + pan_y})">HALDIRAM'S</text>
          <text x="840" y="{410 + pan_y}" font-family="sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle" transform="rotate(-8 840 {385 + pan_y})">BHUJIA</text>
          
          <!-- Yellow strands of bhujia scattered on keys -->
          <line x1="730" y1="{440 + pan_y}" x2="750" y2="{430 + pan_y}" stroke="#facc15" stroke-width="4" stroke-linecap="round"/>
          <line x1="810" y1="{470 + pan_y}" x2="825" y2="{485 + pan_y}" stroke="#facc15" stroke-width="4" stroke-linecap="round"/>
          <line x1="690" y1="{490 + pan_y}" x2="715" y2="{485 + pan_y}" stroke="#facc15" stroke-width="4" stroke-linecap="round"/>
        </svg>"""

        base_img = render_svg_to_image(svg)
        if overlay and 15 <= f <= 175:
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 5 rendered successfully!")

# =============================================================================
# SCENE 6: THE LIFT & CLACK (192 frames, 8.0s)
# =============================================================================
def render_scene_06():
    out_mp4 = os.path.join(SCENES_DIR, "scene_06.mp4")
    overlay = load_overlay("badge_scene_06.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 6 (The Lift & Clack) [192 frames]...")

    # The Clack happens at frame 36 (1.5s into scene 6, which is 37.5 + 1.5 = 39.0s)
    # Actually mechanical clack SFX is at 37.8s (0.3s into scene 6 = frame 7!)
    LIFT_FRAME = 8

    for f in range(192):
        t = f / FPS
        is_lifted = f >= LIFT_FRAME
        
        # Lift animation
        lift_y = 0.0
        if is_lifted:
            lift_progress = min(1.0, (f - LIFT_FRAME) / 24.0)
            lift_y = -260.0 * (1.0 - math.cos(lift_progress * math.pi * 0.5))
            
        # Screen color transition
        screen_bg = "#064e3b" if is_lifted else "#180606"
        screen_border = "#10b981" if is_lifted else "#ef4444"
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Studio Desk & Terminal Screen -->
          <rect width="1920" height="1080" fill="#042f2e" />
          
          <!-- Big Monitor Background -->
          <rect x="360" y="80" width="1200" height="520" rx="20" fill="{screen_bg}" stroke="{screen_border}" stroke-width="8"/>
          
          {"<!-- GREEN SUCCESS TERMINAL -->" if is_lifted else "<!-- RED STUCK ERROR -->"}
          {
          f'''
          <text x="960" y="240" font-family="sans-serif" font-size="46" font-weight="900" fill="#34d399" text-anchor="middle">BUILD SUCCESSFUL • 248 TESTS PASSED</text>
          <text x="960" y="320" font-family="sans-serif" font-size="58" font-weight="900" fill="#ffffff" text-anchor="middle">READY TO DEPLOY • PRODUCTION V1.0</text>
          <rect x="660" y="380" width="600" height="60" rx="30" fill="#10b981"/>
          <text x="960" y="420" font-family="sans-serif" font-size="28" font-weight="800" fill="#064e3b" text-anchor="middle">ALL SENSORS & KEYS RELEASED</text>
          '''
          if is_lifted else
          '''
          <text x="960" y="280" font-family="sans-serif" font-size="48" font-weight="900" fill="#ef4444" text-anchor="middle">KEYBOARD BUFFER OVERFLOW</text>
          <text x="960" y="360" font-family="sans-serif" font-size="32" font-weight="700" fill="#fca5a5" text-anchor="middle">RELEASING SWITCHES REQUIRED TO RESUME</text>
          '''
          }
          
          <!-- Desk in foreground -->
          <rect x="100" y="660" width="1720" height="420" fill="#0f172a" stroke="#1e293b" stroke-width="6"/>
          
          <!-- Keyboard keys popping up -->
          <rect x="760" y="740" width="100" height="70" rx="8" fill="{'#38bdf8' if is_lifted else '#ef4444'}"/>
          <text x="810" y="785" font-family="sans-serif" font-size="22" font-weight="800" fill="#ffffff" text-anchor="middle">F5</text>
          {
          f'''
          <!-- Spring release sparks -->
          <line x1="810" y1="730" x2="810" y2="700" stroke="#facc15" stroke-width="4"/>
          <line x1="780" y1="735" x2="760" y2="710" stroke="#facc15" stroke-width="4"/>
          <line x1="840" y1="735" x2="860" y2="710" stroke="#facc15" stroke-width="4"/>
          <text x="810" y="680" font-family="sans-serif" font-size="28" font-weight="900" fill="#facc15" text-anchor="middle">*CLACK!*</text>
          ''' if (LIFT_FRAME <= f <= LIFT_FRAME + 20) else ''
          }
          
          <!-- Meera's Hand Lifting the Bhujia Packet -->
          <g transform="translate(0, {lift_y})">
            <!-- Bhujia Packet -->
            <polygon points="740,680 1060,630 1090,880 770,930" fill="#eab308" stroke="#ca8a04" stroke-width="6"/>
            <rect x="800" y="720" width="200" height="85" rx="12" fill="#b91c1c" stroke="#fef08a" stroke-width="4" transform="rotate(-8 900 760)"/>
            <text x="900" y="755" font-family="sans-serif" font-size="18" font-weight="900" fill="#fef08a" text-anchor="middle" transform="rotate(-8 900 760)">HALDIRAM'S</text>
            <text x="900" y="788" font-family="sans-serif" font-size="26" font-weight="900" fill="#ffffff" text-anchor="middle" transform="rotate(-8 900 760)">BHUJIA</text>
            
            <!-- Meera's Slender Arm & Fingers Grasping Corner -->
            <path d="M1180,480 L920,650" stroke="#fed7aa" stroke-width="26" stroke-linecap="round"/>
            <ellipse cx="910" cy="655" rx="18" ry="14" fill="#fed7aa"/>
          </g>
        </svg>"""

        base_img = render_svg_to_image(svg)
        if overlay and 15 <= f <= 175:
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 6 rendered successfully!")

# =============================================================================
# SCENE 7: STUNNED SLACK-JAW (192 frames, 8.0s)
# =============================================================================
def render_scene_07():
    out_mp4 = os.path.join(SCENES_DIR, "scene_07.mp4")
    overlay = load_overlay("badge_scene_07.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 7 (Stunned Slack-Jaw) [192 frames]...")

    for f in range(192):
        t = f / FPS
        # Kabir's jaw dropping in comic disbelief
        jaw_drop = min(50.0, 50.0 * (f / 30.0))
        # Meera taking slow coffee sip
        meera_mug_y = 580 - 15.0 * math.sin(f / 40.0 * math.pi)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#0b1324"/>
          
          <!-- Background Studio Shelves with awards & game boxes -->
          <rect x="200" y="160" width="1520" height="20" fill="#1e293b"/>
          <rect x="260" y="80" width="80" height="80" rx="8" fill="#3b82f6"/>
          <rect x="360" y="60" width="60" height="100" rx="8" fill="#10b981"/>
          
          <!-- Desk in foreground -->
          <rect x="0" y="800" width="1920" height="280" fill="#0f172a" stroke="#1e293b" stroke-width="4"/>
          
          <!-- Kabir Stunned Comic Face on Left -->
          <path d="M400,840 Q580,780 760,840 L730,1080 L430,1080 Z" fill="#f97316"/>
          <circle cx="580" cy="500" r="130" fill="#fdba74"/>
          <!-- Backwards cap -->
          <path d="M460,460 Q580,360 700,460 Q580,310 460,460 Z" fill="#334155"/>
          <path d="M490,410 Q650,400 720,430" stroke="#475569" stroke-width="12" fill="none" stroke-linecap="round"/>
          
          <!-- Huge Wide Disbelief Eyes -->
          <ellipse cx="530" cy="480" rx="26" ry="24" fill="#ffffff"/><circle cx="530" cy="480" r="8" fill="#78350f"/>
          <ellipse cx="630" cy="480" rx="26" ry="24" fill="#ffffff"/><circle cx="630" cy="480" r="8" fill="#78350f"/>
          
          <!-- Comic Dropping Slack-Jaw Mouth -->
          <ellipse cx="580" cy="{580 + jaw_drop * 0.5}" rx="32" ry="{24 + jaw_drop * 0.6}" fill="#451a03"/>
          <path d="M560,{560 + jaw_drop * 0.5} Q580,{570 + jaw_drop * 0.5} 600,{560 + jaw_drop * 0.5}" stroke="#ffffff" stroke-width="6" fill="none"/>
          
          <!-- Question Marks pop above Kabir -->
          <text x="500" y="320" font-family="sans-serif" font-size="54" font-weight="900" fill="#facc15">?</text>
          <text x="640" y="300" font-family="sans-serif" font-size="64" font-weight="900" fill="#facc15">?!</text>
          
          <!-- Meera on Right Holding Bhujia Packet & Sipping Coffee -->
          <path d="M1200,830 Q1360,770 1520,830 L1500,1080 L1220,1080 Z" fill="#2563eb"/>
          <circle cx="1360" cy="480" r="120" fill="#fed7aa"/>
          <circle cx="1380" cy="340" r="50" fill="#1e293b"/>
          <path d="M1240,450 Q1360,370 1480,450 Z" fill="#1e293b"/>
          <path d="M1280,390 Q1360,380 1440,410" stroke="#c084fc" stroke-width="14" fill="none" stroke-linecap="round"/>
          
          <!-- Glasses -->
          <circle cx="1305" cy="480" r="34" fill="none" stroke="#38bdf8" stroke-width="6"/>
          <circle cx="1415" cy="480" r="34" fill="none" stroke="#38bdf8" stroke-width="6"/>
          <line x1="1339" y1="480" x2="1381" y2="480" stroke="#38bdf8" stroke-width="5"/>
          <!-- Amused Side-Glance Eyes -->
          <ellipse cx="1295" cy="480" rx="10" ry="8" fill="#1e293b"/>
          <ellipse cx="1405" cy="480" rx="10" ry="8" fill="#1e293b"/>
          
          <!-- Meera Holding Bhujia Packet upright -->
          <polygon points="1520,480 1700,440 1720,640 1540,680" fill="#eab308" stroke="#ca8a04" stroke-width="5"/>
          <text x="1620" y="560" font-family="sans-serif" font-size="22" font-weight="900" fill="#991b1b" text-anchor="middle" transform="rotate(-12 1620 560)">BHUJIA</text>
          
          <!-- Coffee Mug brought up to lips -->
          <rect x="1335" y="{meera_mug_y}" width="50" height="65" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="4"/>
          <path d="M1330,{meera_mug_y + 15} Q1310,{meera_mug_y + 30} 1330,{meera_mug_y + 50}" stroke="#cbd5e1" stroke-width="5" fill="none"/>
        </svg>"""

        base_img = render_svg_to_image(svg)
        if overlay and 15 <= f <= 175:
            alpha_mult = 1.0
            if f < 30: alpha_mult = (f - 15) / 15.0
            elif f > 160: alpha_mult = (175 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 7 rendered successfully!")

# =============================================================================
# SCENE 8: PUNCHLINE & VICTORY (180 frames, 7.5s)
# =============================================================================
def render_scene_08():
    out_mp4 = os.path.join(SCENES_DIR, "scene_08.mp4")
    overlay = load_overlay("badge_scene_08.png")
    outro_card = load_overlay("outro_title_card.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 8 (Punchline & Victory) [180 frames]...")

    for f in range(180):
        t = f / FPS
        # Kabir triumphant fist pump
        fist_y = 420 + 20.0 * math.sin(10.0 * t)
        
        # Floating confetti drifting down
        confetti_svg = ""
        for i in range(16):
            cx = (i * 125 + f * 12) % 1920
            cy = (i * 70 + f * 9) % 1080
            col = ["#f97316", "#38bdf8", "#10b981", "#facc15", "#c084fc"][i % 5]
            confetti_svg += f'<rect x="{cx}" y="{cy}" width="14" height="8" rx="2" fill="{col}" transform="rotate({(f*5 + i*20)%360} {cx+7} {cy+4})"/>\n'
            
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#090d16"/>
          
          <!-- Victory Confetti -->
          {confetti_svg}
          
          <!-- Big Success Banner at top -->
          <rect x="460" y="80" width="1000" height="100" rx="20" fill="#1e293b" stroke="#f97316" stroke-width="4"/>
          <text x="960" y="145" font-family="sans-serif" font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">APP SUBMISSION COMPLETE • V1.0 LIVE!</text>
          
          <!-- Desk in foreground -->
          <rect x="0" y="800" width="1920" height="280" fill="#0f172a" stroke="#1e293b" stroke-width="4"/>
          
          <!-- Kabir Laughing & Pumping Fist on Left -->
          <path d="M420,840 Q600,780 780,840 L750,1080 L450,1080 Z" fill="#f97316"/>
          <circle cx="600" cy="520" r="120" fill="#fdba74"/>
          <path d="M490,470 Q600,380 710,470 Q600,330 490,470 Z" fill="#334155"/>
          <!-- Joyful Squinting Eyes -->
          <path d="M530,500 Q555,480 580,500" stroke="#78350f" stroke-width="6" fill="none" stroke-linecap="round"/>
          <path d="M620,500 Q645,480 670,500" stroke="#78350f" stroke-width="6" fill="none" stroke-linecap="round"/>
          <!-- Huge Happy Grin -->
          <path d="M545,550 Q600,610 655,550 Z" fill="#7f1d1d"/>
          
          <!-- Fist Pump Arm -->
          <path d="M720,830 L820,{fist_y + 100} L860,{fist_y}" stroke="#f97316" stroke-width="36" fill="none" stroke-linecap="round"/>
          <circle cx="860" cy="{fist_y}" r="26" fill="#fdba74"/>
          
          <!-- Meera Holding Bhujia High like a Trophy -->
          <path d="M1180,830 Q1340,770 1500,830 L1480,1080 L1200,1080 Z" fill="#2563eb"/>
          <circle cx="1340" cy="510" r="115" fill="#fed7aa"/>
          <circle cx="1360" cy="375" r="48" fill="#1e293b"/>
          <path d="M1225,480 Q1340,400 1455,480 Z" fill="#1e293b"/>
          <path d="M1260,420 Q1340,410 1420,440" stroke="#c084fc" stroke-width="14" fill="none" stroke-linecap="round"/>
          
          <!-- Glasses & Grin -->
          <circle cx="1285" cy="510" r="32" fill="none" stroke="#38bdf8" stroke-width="6"/>
          <circle cx="1395" cy="510" r="32" fill="none" stroke="#38bdf8" stroke-width="6"/>
          <line x1="1317" y1="510" x2="1363" y2="510" stroke="#38bdf8" stroke-width="5"/>
          <ellipse cx="1285" cy="510" rx="10" ry="8" fill="#1e293b"/>
          <ellipse cx="1395" cy="510" rx="10" ry="8" fill="#1e293b"/>
          <path d="M1310,570 Q1340,600 1370,570" stroke="#78350f" stroke-width="6" fill="none" stroke-linecap="round"/>
          
          <!-- Bhujia Packet Held High in Right Arm -->
          <path d="M1440,830 L1580,560" stroke="#fed7aa" stroke-width="30" stroke-linecap="round"/>
          <polygon points="1520,380 1720,340 1740,560 1540,600" fill="#eab308" stroke="#ca8a04" stroke-width="6"/>
          <rect x="1560" y="420" width="160" height="70" rx="10" fill="#b91c1c" stroke="#fef08a" stroke-width="4" transform="rotate(-12 1640 455)"/>
          <text x="1640" y="450" font-family="sans-serif" font-size="16" font-weight="900" fill="#fef08a" text-anchor="middle" transform="rotate(-12 1640 455)">HALDIRAM'S</text>
          <text x="1640" y="478" font-family="sans-serif" font-size="22" font-weight="900" fill="#ffffff" text-anchor="middle" transform="rotate(-12 1640 455)">BHUJIA</text>
        </svg>"""

        base_img = render_svg_to_image(svg)
        
        # Dialogue overlay up to frame 125
        if overlay and 10 <= f <= 125:
            alpha_mult = 1.0
            if f < 25: alpha_mult = (f - 10) / 15.0
            elif f > 110: alpha_mult = (125 - f) / 15.0
            ov_copy = overlay.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        # Outro Title Card Fading in from frame 130 to 180
        if outro_card and f >= 130:
            alpha_mult = min(1.0, (f - 130) / 20.0)
            ov_copy = outro_card.copy()
            if alpha_mult < 1.0:
                r, g, b, a = ov_copy.split()
                a = a.point(lambda p: int(p * alpha_mult))
                ov_copy.putalpha(a)
            base_img.paste(ov_copy, (0, 0), ov_copy)
            
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 8 rendered successfully!")

# =============================================================================
# MAIN ORCHESTRATOR FOR ALL 8 SCENES
# =============================================================================
if __name__ == "__main__":
    t_start = time.time()
    print("=================================================================")
    print("MASTER AI — PHASE 7.7.3: HIGH-FIDELITY 1080P SCENE RENDERER")
    print("Total Frames: 1524 | FPS: 24.0 CFR | Resolution: 1920x1080")
    print("=================================================================")
    
    render_scene_01()
    render_scene_02()
    render_scene_03()
    render_scene_04()
    render_scene_05()
    render_scene_06()
    render_scene_07()
    render_scene_08()
    
    total_time = time.time() - t_start
    print(f"\nAll 8 scenes rendered in {total_time:.2f}s (~{total_time/1524*1000:.1f}ms/frame)!")
