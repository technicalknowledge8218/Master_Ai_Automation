"""
render_scenes_774.py
====================
Master AI - Phase 7.7.4 High-Fidelity 1080p Scene Renderer
Uses MotionDirector (Easing, Parallax Camera, BlinkController,
VisemeLipSync, ParticleSystems) and Chrome Devanagari text overlays.

Outputs:
- scenes_1080p/scene_01.mp4 to scene_08.mp4 (180 frames each, 7.50s @ 24fps)
"""

import os
import sys
import math
import subprocess
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
import imageio_ffmpeg

ENGINE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\engine"
sys.path.append(ENGINE_DIR)

from motion_director import Easing, Camera2D, BlinkController, LipSyncVisemeController, BreathingController, ParticleSystem

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4"
SCENES_DIR = os.path.join(BASE_DIR, "scenes_1080p")
OVERLAYS_DIR = os.path.join(BASE_DIR, "overlays_1080p")
os.makedirs(SCENES_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
WIDTH = 1920
HEIGHT = 1080
FPS = 24
SCENE_FRAMES = 180  # 7.50s per scene

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
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def load_overlay(filename):
    path = os.path.join(OVERLAYS_DIR, filename)
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    return None

def apply_overlay(base_img, overlay, current_frame, start_frame=12, end_frame=165):
    if overlay and start_frame <= current_frame <= end_frame:
        alpha_mult = 1.0
        if current_frame < start_frame + 12:
            alpha_mult = (current_frame - start_frame) / 12.0
        elif current_frame > end_frame - 12:
            alpha_mult = (end_frame - current_frame) / 12.0
        ov_copy = overlay.copy()
        if alpha_mult < 1.0:
            r, g, b, a = ov_copy.split()
            a = a.point(lambda p: int(p * alpha_mult))
            ov_copy.putalpha(a)
        base_img.paste(ov_copy, (0, 0), ov_copy)

# =============================================================================
# SCENE 1: THE COUNTDOWN [EXTREME CLOSE-UP] (180 frames, 7.5s)
# =============================================================================
def render_scene_01():
    out_mp4 = os.path.join(SCENES_DIR, "scene_01.mp4")
    overlay = load_overlay("badge_scene_01.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 1: The 10-Minute Countdown [180 frames]...")

    cam = Camera2D()
    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Camera Dolly-In with Ease-Out
        zoom = 1.0 + 0.18 * Easing.ease_out_quad(f / float(SCENE_FRAMES))
        # Vibration on phone mount
        cam.trigger_shake(t if t < 1.5 else (t % 0.8), intensity=4.0)
        
        # Phone screen pulse
        screen_pulse = 0.5 + 0.5 * math.sin(2.0 * math.pi * 3.0 * t)
        glow_alpha = 0.2 + 0.25 * screen_pulse
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#090508"/>
          
          <g transform="translate(960, 540) scale({zoom}) translate(-960, -540)">
            <!-- Scooter Handlebar Mount & Background Night Street Blur -->
            <rect x="0" y="700" width="1920" height="380" fill="#0f172a"/>
            <line x1="200" y1="740" x2="1720" y2="740" stroke="#334155" stroke-width="28" stroke-linecap="round"/>
            <rect x="880" y="650" width="160" height="120" rx="16" fill="#1e293b" stroke="#475569" stroke-width="4"/>
            
            <!-- Vibration offsets -->
            <g transform="translate({cam.shake_x}, {cam.shake_y})">
              <!-- Smartphone Body -->
              <rect x="660" y="160" width="600" height="660" rx="36" fill="#0c070c" stroke="#dc2626" stroke-width="8"/>
              <!-- Screen Pulsing Glow -->
              <rect x="680" y="180" width="560" height="620" rx="28" fill="rgba(239, 68, 68, {glow_alpha:.2f})"/>
              
              <!-- App Interface Header -->
              <rect x="710" y="210" width="500" height="65" rx="14" fill="#1e1014"/>
              <circle cx="750" cy="242" r="14" fill="#ef4444"/>
              <text x="780" y="250" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">URGENT DELIVERY • ORDER #402</text>
              
              <!-- Giant Countdown Display -->
              <text x="960" y="440" font-family="sans-serif" font-size="120" font-weight="900" fill="#ffffff" text-anchor="middle">09:59</text>
              <text x="960" y="520" font-family="sans-serif" font-size="26" font-weight="800" fill="#fca5a5" text-anchor="middle">REMAINING BEFORE AUTOMATIC CANCELLATION</text>
              
              <!-- Destination Card -->
              <rect x="710" y="570" width="500" height="180" rx="20" fill="#180e14" stroke="#7f1d1d" stroke-width="3"/>
              <text x="740" y="620" font-family="sans-serif" font-size="22" font-weight="800" fill="#38bdf8">DROP: ST. MARTHA'S HOSPITAL</text>
              <text x="740" y="660" font-family="sans-serif" font-size="18" font-weight="600" fill="#cbd5e1">Emergency ICU Ward • 4.2 km in Heavy Rain</text>
              <rect x="740" y="685" width="220" height="40" rx="8" fill="#ef4444"/>
              <text x="850" y="712" font-family="sans-serif" font-size="16" font-weight="900" fill="#ffffff" text-anchor="middle">ACCEPT & RIDE</text>
            </g>
          </g>
          
          <!-- Raindrops streaking across phone glass -->
          {ParticleSystem.generate_rain_svg(f, count=25)}
        </svg>"""

        base_img = render_svg_to_image(svg)
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=165)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 1 rendered successfully!")

# =============================================================================
# SCENE 2: THE CHAOTIC CLOUD KITCHEN [MEDIUM SHOT] (180 frames, 7.5s)
# =============================================================================
def render_scene_02():
    out_mp4 = os.path.join(SCENES_DIR, "scene_02.mp4")
    overlay = load_overlay("badge_scene_02.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 2: The Chaotic Cloud Kitchen [180 frames]...")

    blink_ctrl = BlinkController()
    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Camera Pan Right
        cam_x = -120.0 * Easing.ease_in_out_cubic(f / float(SCENE_FRAMES))
        
        # Wok toss harmonic oscillation
        wok_toss = 25.0 * math.sin(2.0 * math.pi * 1.5 * t)
        
        # Chef blinking & speech mouth
        eyelid = blink_ctrl.get_eyelid_closure(f)
        mouth_amp = 0.5 + 0.4 * abs(math.sin(12.0 * t))
        mouth = LipSyncVisemeController.get_mouth_viseme(mouth_amp)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Steamy Kitchen Interior -->
          <rect width="1920" height="1080" fill="#1c0e08"/>
          
          <g transform="translate({cam_x}, 0)">
            <!-- Kitchen Stainless Steel Shelves & Heat Lamps -->
            <rect x="100" y="80" width="1800" height="24" fill="#475569"/>
            <rect x="200" y="104" width="200" height="40" fill="#f97316" opacity="0.6"/>
            <rect x="600" y="104" width="200" height="40" fill="#f97316" opacity="0.6"/>
            <rect x="1100" y="104" width="200" height="40" fill="#f97316" opacity="0.6"/>
            
            <!-- Kitchen Countertop in foreground -->
            <rect x="0" y="740" width="2100" height="340" fill="#0f172a" stroke="#334155" stroke-width="6"/>
            
            <!-- Vikram Chef on Left Behind Counter -->
            <path d="M520,740 Q660,670 800,740 L770,1080 L550,1080 Z" fill="#ffffff"/> <!-- White apron -->
            <rect x="580" y="780" width="160" height="140" fill="#b91c1c" opacity="0.8"/> <!-- Sauce stain -->
            <circle cx="660" cy="500" r="105" fill="#fed7aa"/>
            
            <!-- Chef Mustache -->
            <path d="M600,540 Q660,565 720,540 Q660,530 600,540 Z" fill="#1e293b"/>
            
            <!-- Eyelids with Blink Controller -->
            {
            f'''<line x1="615" y1="485" x2="645" y2="485" stroke="#1e293b" stroke-width="5"/>
                <line x1="675" y1="485" x2="705" y2="485" stroke="#1e293b" stroke-width="5"/>'''
            if eyelid > 0.4 else
            '''<ellipse cx="630" cy="485" rx="16" ry="12" fill="#ffffff"/><circle cx="630" cy="485" r="6" fill="#1e293b"/>
               <ellipse cx="690" cy="485" rx="16" ry="12" fill="#ffffff"/><circle cx="690" cy="485" r="6" fill="#1e293b"/>'''
            }
            
            <!-- Lip-Sync Mouth -->
            <ellipse cx="660" cy="570" rx="{18 * mouth['width_scale']:.1f}" ry="{mouth['height'] * 0.6:.1f}" fill="#7f1d1d"/>
            
            <!-- Flaming Wok with Tossing Noodles -->
            <g transform="translate(0, {wok_toss})">
              <!-- Wok Body -->
              <ellipse cx="980" cy="720" rx="140" ry="65" fill="#090d16" stroke="#475569" stroke-width="6"/>
              <!-- Roaring Wok Fire -->
              <path d="M870,710 Q980,560 1090,710 Q1040,640 980,620 Q920,640 870,710 Z" fill="#f97316"/>
              <path d="M910,700 Q980,600 1050,700 Z" fill="#facc15"/>
            </g>
            
            <!-- Embers Particles Rising -->
            {ParticleSystem.generate_embers_svg(f, origin_x=980, origin_y=680, count=28)}
            
            <!-- Insulated Delivery Box on Counter -->
            <rect x="1250" y="600" width="220" height="150" rx="14" fill="#0284c7" stroke="#38bdf8" stroke-width="5"/>
            <rect x="1270" y="640" width="180" height="30" rx="6" fill="#f59e0b"/>
            <text x="1360" y="662" font-family="sans-serif" font-size="16" font-weight="900" fill="#0f172a" text-anchor="middle">HOT INSULATED</text>
            
            <!-- Aryan's Arm Grabbing the Box -->
            <path d="M1650,850 L1460,670" stroke="#0284c7" stroke-width="32" stroke-linecap="round"/>
            <circle cx="1460" cy="670" r="20" fill="#fdba74"/>
          </g>
        </svg>"""

        base_img = render_svg_to_image(svg)
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=165)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 2 rendered successfully!")

# =============================================================================
# SCENE 3: KINETIC LAUNCH [LOW-ANGLE TRACKING] (180 frames, 7.5s)
# =============================================================================
def render_scene_03():
    out_mp4 = os.path.join(SCENES_DIR, "scene_03.mp4")
    overlay = load_overlay("badge_scene_03.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 3: Kinetic Launch [180 frames]...")

    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Multi-plane Parallax Velocity
        speed = 28.0  # px per frame
        bg_offset = (f * speed * 0.25) % 1920
        mid_offset = (f * speed * 0.60) % 1920
        puddle_offset = (f * speed * 1.30) % 1920
        
        # Wheel rotation
        wheel_rot = (f * 35) % 360
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Rainy Night Sky -->
          <rect width="1920" height="1080" fill="#060c18"/>
          
          <!-- Background Layer (Parallax 0.25x): Neon Storefronts & Skyline -->
          <g transform="translate({-bg_offset}, 0)">
            <rect x="200" y="320" width="300" height="380" fill="#0f172a"/>
            <rect x="240" y="360" width="180" height="40" rx="8" fill="#f43f5e" opacity="0.8"/>
            <text x="330" y="388" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff" text-anchor="middle">PHARMACY</text>
            
            <rect x="800" y="240" width="400" height="460" fill="#111827"/>
            <rect x="840" y="280" width="220" height="40" rx="8" fill="#06b6d4" opacity="0.8"/>
            <text x="950" y="308" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff" text-anchor="middle">METRO STATION</text>
            
            <rect x="1500" y="300" width="350" height="400" fill="#0f172a"/>
            <!-- Duplicate for infinite wrap -->
            <rect x="2120" y="320" width="300" height="380" fill="#0f172a"/>
            <rect x="2720" y="240" width="400" height="460" fill="#111827"/>
          </g>
          
          <!-- Wet Asphalt Road Surface -->
          <rect x="0" y="700" width="1920" height="380" fill="#0a0f1d"/>
          
          <!-- Midground Layer (Parallax 0.60x): Street Curb & Neon Reflection -->
          <g transform="translate({-mid_offset}, 0)">
            <line x1="0" y1="710" x2="3840" y2="710" stroke="#f59e0b" stroke-width="8" stroke-dasharray="80,50"/>
            <!-- Puddle Reflections -->
            <ellipse cx="600" cy="850" rx="280" ry="40" fill="rgba(56, 189, 248, 0.25)"/>
            <ellipse cx="1600" cy="880" rx="340" ry="45" fill="rgba(244, 63, 94, 0.25)"/>
            <ellipse cx="2520" cy="850" rx="280" ry="40" fill="rgba(56, 189, 248, 0.25)"/>
          </g>
          
          <!-- Low-Angle Electric Scooter Wheel in Subject Focus Plane -->
          <g transform="translate(860, 680)">
            <!-- Front Fork & Teal Chassis -->
            <path d="M120,-180 L80,80" stroke="#0284c7" stroke-width="28" stroke-linecap="round"/>
            <path d="M140,-160 L240,-40" stroke="#f59e0b" stroke-width="22" stroke-linecap="round"/>
            
            <!-- Wheel Rim & Tyre -->
            <circle cx="80" cy="80" r="130" fill="#090d16" stroke="#475569" stroke-width="28"/>
            <circle cx="80" cy="80" r="75" fill="#1e293b" stroke="#38bdf8" stroke-width="8"/>
            <!-- Spinning Spokes -->
            <g transform="rotate({wheel_rot} 80 80)">
              <line x1="80" y1="15" x2="80" y2="145" stroke="#94a3b8" stroke-width="6"/>
              <line x1="15" y1="80" x2="145" y2="80" stroke="#94a3b8" stroke-width="6"/>
            </g>
            
            <!-- High Speed Water Spray Jets Shooting Back -->
            <path d="M-20,110 Q-160,80 -320,160" stroke="#bae6fd" stroke-width="12" fill="none" opacity="0.85"/>
            <path d="M-40,90 Q-200,50 -400,120" stroke="#7dd3fc" stroke-width="8" fill="none" opacity="0.75"/>
          </g>
          
          <!-- Diagonal Falling Rain Streaks -->
          {ParticleSystem.generate_rain_svg(f, count=45)}
        </svg>"""

        base_img = render_svg_to_image(svg)
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=165)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 3 rendered successfully!")

# =============================================================================
# SCENE 4: THE TRAFFIC GRIDLOCK [POV / CLOSE-UP] (180 frames, 7.5s)
# =============================================================================
def render_scene_04():
    out_mp4 = os.path.join(SCENES_DIR, "scene_04.mp4")
    overlay = load_overlay("badge_scene_04.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 4: The Traffic Gridlock [180 frames]...")

    blink_ctrl = BlinkController()
    cam = Camera2D()
    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Camera Shake as scooter swerves between traffic
        cam.trigger_shake(t % 0.6, intensity=8.0)
        
        # Eyes tracking left and right
        gaze_x = 12.0 * math.sin(2.0 * math.pi * 0.8 * t)
        eyelid = blink_ctrl.get_eyelid_closure(f)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Dark Night Street with glowing red tail lights of stopped cars -->
          <rect width="1920" height="1080" fill="#070a12"/>
          
          <!-- Distant Blurred Red Brake Lights (Gridlock) -->
          <g transform="translate({cam.shake_x}, {cam.shake_y})">
            <circle cx="380" cy="480" r="75" fill="#ef4444" opacity="0.75"/>
            <circle cx="580" cy="480" r="75" fill="#ef4444" opacity="0.75"/>
            
            <circle cx="980" cy="440" r="95" fill="#dc2626" opacity="0.85"/>
            <circle cx="1220" cy="440" r="95" fill="#dc2626" opacity="0.85"/>
            
            <circle cx="1560" cy="500" r="70" fill="#ef4444" opacity="0.75"/>
            <circle cx="1740" cy="500" r="70" fill="#ef4444" opacity="0.75"/>
            
            <!-- Neon Amber Auto-Rickshaw Stripes in Traffic -->
            <rect x="740" y="520" width="160" height="60" fill="#f59e0b" opacity="0.8"/>
          </g>
          
          <!-- Helmet Visor Edge Framing the POV Shot -->
          <path d="M0,0 L1920,0 L1920,240 Q960,160 0,240 Z" fill="#0f172a"/>
          <path d="M0,840 Q960,920 1920,840 L1920,1080 L0,1080 Z" fill="#0f172a"/>
          <path d="M0,0 L180,0 L140,1080 L0,1080 Z" fill="#0f172a"/>
          <path d="M1740,0 L1920,0 L1920,1080 L1780,1080 Z" fill="#0f172a"/>
          <rect x="140" y="220" width="1640" height="640" fill="none" stroke="#0284c7" stroke-width="14" rx="40"/>
          
          <!-- Aryan's Focused Eyes in Visor Mirror Reflection -->
          <g transform="translate({gaze_x}, 0)">
            <!-- Left Eye -->
            {
            '<line x1="680" y1="360" x2="780" y2="360" stroke="#0f172a" stroke-width="8"/>'
            if eyelid > 0.4 else
            f'''<ellipse cx="730" cy="360" rx="55" ry="34" fill="#ffffff"/>
                <circle cx="{735 + gaze_x}" cy="360" r="20" fill="#78350f"/>
                <circle cx="{738 + gaze_x}" cy="355" r="7" fill="#ffffff"/>'''
            }
            <!-- Right Eye -->
            {
            '<line x1="1140" y1="360" x2="1240" y2="360" stroke="#0f172a" stroke-width="8"/>'
            if eyelid > 0.4 else
            f'''<ellipse cx="1190" cy="360" rx="55" ry="34" fill="#ffffff"/>
                <circle cx="{1195 + gaze_x}" cy="360" r="20" fill="#78350f"/>
                <circle cx="{1198 + gaze_x}" cy="355" r="7" fill="#ffffff"/>'''
            }
            <!-- Furrowed Determined Eyebrows -->
            <path d="M660,310 Q730,290 800,320" stroke="#0f172a" stroke-width="12" fill="none" stroke-linecap="round"/>
            <path d="M1120,320 Q1190,290 1260,310" stroke="#0f172a" stroke-width="12" fill="none" stroke-linecap="round"/>
          </g>
          
          <!-- Raindrops Beading on Visor Surface -->
          {ParticleSystem.generate_rain_svg(f, count=35)}
        </svg>"""

        base_img = render_svg_to_image(svg)
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=165)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 4 rendered successfully!")

# =============================================================================
# SCENE 5: THE FINAL SECONDS [INSERT / DOLLY-ZOOM] (180 frames, 7.5s)
# =============================================================================
def render_scene_05():
    out_mp4 = os.path.join(SCENES_DIR, "scene_05.mp4")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 5: The Final Seconds [180 frames]...")

    cam = Camera2D()
    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Vertigo / Dolly-Zoom effect: zoom in while background scales
        zoom = 1.0 + 0.35 * Easing.ease_in_out_cubic(f / float(SCENE_FRAMES))
        cam.trigger_shake(t, intensity=10.0 * (f / float(SCENE_FRAMES)))
        
        # Countdown time calculation
        # Starts at 00:30 and races down to 00:03
        secs_left = max(2, int(30 - (f / float(SCENE_FRAMES)) * 28))
        
        # Leaning angle on corner turn
        tilt_angle = -12.0 * math.sin(f / float(SCENE_FRAMES) * math.pi)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#180406"/>
          
          <g transform="translate(960, 540) rotate({tilt_angle}) scale({zoom}) translate(-960, -540)">
            <!-- Wet Asphalt & Yellow Corner Line -->
            <rect x="0" y="0" width="1920" height="1080" fill="#0d0408"/>
            <path d="M0,800 Q960,400 1920,800" stroke="#f59e0b" stroke-width="36" fill="none"/>
            
            <!-- Handlebar Display with Shake -->
            <g transform="translate({cam.shake_x}, {cam.shake_y})">
              <rect x="460" y="240" width="1000" height="600" rx="40" fill="#090d16" stroke="#ef4444" stroke-width="12"/>
              <rect x="490" y="270" width="940" height="540" rx="30" fill="#180606"/>
              
              <!-- Warning Banner -->
              <text x="960" y="380" font-family="sans-serif" font-size="44" font-weight="900" fill="#ef4444" text-anchor="middle">CRITICAL DEADLINE APPROACHING</text>
              
              <!-- Giant Pulsing Countdown -->
              <text x="960" y="580" font-family="sans-serif" font-size="180" font-weight="900" fill="#ffffff" text-anchor="middle">00:{secs_left:02d}</text>
              
              <rect x="680" y="660" width="560" height="65" rx="32" fill="#ef4444"/>
              <text x="960" y="704" font-family="sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">REACH DESTINATION NOW</text>
            </g>
          </g>
          
          <!-- Raindrops flying horizontally from speed -->
          {ParticleSystem.generate_rain_svg(f, count=40)}
        </svg>"""

        base_img = render_svg_to_image(svg)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 5 rendered successfully!")

# =============================================================================
# SCENE 6: ARRIVAL AT ST. MARTHA'S [WIDE ESTABLISHING] (180 frames, 7.5s)
# =============================================================================
def render_scene_06():
    out_mp4 = os.path.join(SCENES_DIR, "scene_06.mp4")
    overlay = load_overlay("badge_scene_06.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 6: Arrival at St. Martha's [180 frames]...")

    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Scooter deceleration stop: moves from x=200 to x=900 with Ease-Out
        scooter_x = 200 + 700 * Easing.ease_out_quad(min(1.0, f / 90.0))
        
        # Steam rising from scooter battery / motor after stop
        steam_y = 780 - 40.0 * ((f % 45) / 45.0)
        steam_alpha = 0.8 * (1.0 - (f % 45) / 45.0) if f > 90 else 0.0
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Hospital Exterior in Gentle Night Rain -->
          <rect width="1920" height="1080" fill="#06121e"/>
          
          <!-- Warm Street Lamppost Halo on Left -->
          <ellipse cx="400" cy="300" rx="350" ry="250" fill="rgba(250, 204, 21, 0.12)"/>
          <line x1="400" y1="200" x2="400" y2="820" stroke="#334155" stroke-width="16"/>
          <circle cx="400" cy="200" r="30" fill="#facc15"/>
          
          <!-- Hospital Entrance Architecture -->
          <rect x="760" y="160" width="1160" height="660" rx="20" fill="#0d1b2a" stroke="#1e293b" stroke-width="6"/>
          <!-- Glowing Emergency Cross Sign -->
          <rect x="860" y="240" width="90" height="30" rx="6" fill="#ef4444"/>
          <rect x="890" y="210" width="30" height="90" rx="6" fill="#ef4444"/>
          <text x="1000" y="270" font-family="sans-serif" font-size="38" font-weight="900" fill="#ffffff">ST. MARTHA'S HOSPITAL</text>
          <text x="1000" y="320" font-family="sans-serif" font-size="22" font-weight="700" fill="#38bdf8">24/7 EMERGENCY & INTENSIVE CARE</text>
          
          <!-- Automatic Glass Sliding Doors -->
          <rect x="1150" y="440" width="480" height="380" rx="10" fill="#132438" stroke="#38bdf8" stroke-width="4"/>
          <line x1="1390" y1="440" x2="1390" y2="820" stroke="#38bdf8" stroke-width="4"/>
          
          <!-- Pavement Ground -->
          <rect x="0" y="820" width="1920" height="260" fill="#090d16" stroke="#1e293b" stroke-width="4"/>
          
          <!-- Electric Scooter & Aryan Coming to Stop -->
          <g transform="translate({scooter_x}, 580)">
            <!-- Scooter Body -->
            <rect x="40" y="180" width="160" height="45" rx="10" fill="#0284c7"/>
            <circle cx="30" cy="220" r="35" fill="#0f172a" stroke="#475569" stroke-width="8"/>
            <circle cx="210" cy="220" r="35" fill="#0f172a" stroke="#475569" stroke-width="8"/>
            <!-- Aryan Seated, Visor Raised -->
            <rect x="80" y="40" width="80" height="140" rx="16" fill="#0284c7"/>
            <circle cx="120" cy="-10" r="45" fill="#0f172a" stroke="#0284c7" stroke-width="4"/>
            <!-- Raised Visor -->
            <path d="M90,-35 L150,-35" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
            <ellipse cx="120" cy="-5" rx="8" ry="6" fill="#fdba74"/>
          </g>
          
          <!-- Motor Steam Puff -->
          <circle cx="{scooter_x + 100}" cy="{steam_y}" r="25" fill="rgba(248, 250, 252, {steam_alpha:.2f})"/>
          
          <!-- Soft Rain falling in Lamplight -->
          {ParticleSystem.generate_rain_svg(f, count=30)}
        </svg>"""

        base_img = render_svg_to_image(svg)
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=165)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 6 rendered successfully!")

# =============================================================================
# SCENE 7: THE BIRTHDAY SURPRISE [MEDIUM CLOSE-UP] (180 frames, 7.5s)
# =============================================================================
def render_scene_07():
    out_mp4 = os.path.join(SCENES_DIR, "scene_07.mp4")
    overlay = load_overlay("badge_scene_07.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 7: The Birthday Surprise [180 frames]...")

    blink_ctrl = BlinkController()
    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Camera Slow Push-In with Cubic Easing
        zoom = 1.0 + 0.12 * Easing.ease_in_out_cubic(f / float(SCENE_FRAMES))
        
        # Ananya breathing & tear shimmer
        eyelid = blink_ctrl.get_eyelid_closure(f)
        candle_flicker = 0.85 + 0.15 * math.sin(2.0 * math.pi * 5.0 * t)
        
        # Mouth Viseme for Ananya speaking
        mouth_amp = 0.4 + 0.3 * abs(math.sin(10.0 * t))
        mouth = LipSyncVisemeController.get_mouth_viseme(mouth_amp)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Hospital Entrance Warm Interior Backlight -->
          <rect width="1920" height="1080" fill="#091316"/>
          
          <g transform="translate(960, 540) scale({zoom}) translate(-960, -540)">
            <!-- Glass Automatic Doors open behind -->
            <rect x="200" y="100" width="1520" height="720" rx="16" fill="#0a1a1f" stroke="#134e4a" stroke-width="4"/>
            
            <!-- Dr. Ananya in Surgical Scrubs on Left -->
            <!-- Scrub Top & Stethoscope -->
            <path d="M480,820 Q660,740 840,820 L810,1080 L510,1080 Z" fill="#059669"/>
            <path d="M580,820 Q660,950 740,820" stroke="#cbd5e1" stroke-width="6" fill="none"/>
            <circle cx="660" cy="940" r="14" fill="#94a3b8"/>
            
            <!-- Ananya Head & Scrub Cap -->
            <circle cx="660" cy="480" r="120" fill="#fed7aa"/>
            <path d="M540,460 Q660,320 780,460 Z" fill="#065f46"/> <!-- Dark Green Scrub Cap -->
            
            <!-- Eyes with Blink Controller -->
            {
            '<line x1="610" y1="465" x2="650" y2="465" stroke="#1e293b" stroke-width="5"/>'
            if eyelid > 0.4 else
            '''<ellipse cx="630" cy="465" rx="18" ry="14" fill="#ffffff"/><circle cx="630" cy="465" r="7" fill="#1e293b"/>
               <path d="M605,485 Q630,495 655,485" stroke="#94a3b8" stroke-width="2" fill="none"/>'''
            }
            {
            '<line x1="670" y1="465" x2="710" y2="465" stroke="#1e293b" stroke-width="5"/>'
            if eyelid > 0.4 else
            '''<ellipse cx="690" cy="465" rx="18" ry="14" fill="#ffffff"/><circle cx="690" cy="465" r="7" fill="#1e293b"/>
               <path d="M665,485 Q690,495 715,485" stroke="#94a3b8" stroke-width="2" fill="none"/>
               <!-- Joyful tear droplet -->
               <ellipse cx="715" cy="495" rx="4" ry="7" fill="#38bdf8"/>'''
            }
            
            <!-- Gentle Emotional Smile & Lip-Sync -->
            <path d="M635,550 Q660,575 685,550" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <ellipse cx="660" cy="555" rx="{14 * mouth['width_scale']:.1f}" ry="{mouth['height'] * 0.4:.1f}" fill="#7f1d1d"/>
            
            <!-- Open Delivery Box in Ananya's Hands -->
            <rect x="960" y="520" width="460" height="300" rx="20" fill="#fef08a" stroke="#ca8a04" stroke-width="6"/>
            
            <!-- Strawberry Birthday Pastry inside -->
            <rect x="1050" y="600" width="280" height="140" rx="16" fill="#fda4af" stroke="#e11d48" stroke-width="4"/>
            <!-- Whipped Cream & Strawberries -->
            <circle cx="1120" cy="600" r="16" fill="#ffffff"/>
            <circle cx="1190" cy="600" r="16" fill="#ffffff"/>
            <circle cx="1260" cy="600" r="16" fill="#ffffff"/>
            
            <!-- Tiny Lit Birthday Candle -->
            <line x1="1190" y1="600" x2="1190" y2="520" stroke="#ffffff" stroke-width="8" stroke-linecap="round"/>
            <!-- Candle Flame & Warm Radial Glow -->
            <circle cx="1190" cy="500" r="{35 * candle_flicker:.1f}" fill="rgba(250, 204, 21, 0.25)"/>
            <ellipse cx="1190" cy="505" rx="10" ry="16" fill="#facc15"/>
            <ellipse cx="1190" cy="508" rx="5" ry="9" fill="#ef4444"/>
            
            <!-- Handwritten Mom Note Card -->
            <rect x="1080" y="720" width="220" height="75" rx="8" fill="#ffffff" stroke="#94a3b8" stroke-width="2" transform="rotate(-6 1190 750)"/>
            <text x="1190" y="750" font-family="sans-serif" font-size="14" font-weight="900" fill="#991b1b" text-anchor="middle" transform="rotate(-6 1190 750)">HAPPY BIRTHDAY BETA!</text>
            <text x="1190" y="775" font-family="sans-serif" font-size="12" font-weight="700" fill="#334155" text-anchor="middle" transform="rotate(-6 1190 750)">Love always, Mom ❤️</text>
          </g>
        </svg>"""

        base_img = render_svg_to_image(svg)
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=165)
        pipe.stdin.write(base_img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print("Scene 7 rendered successfully!")

# =============================================================================
# SCENE 8: TRIUMPH & SMILE [MEDIUM SHOT] (180 frames, 7.5s)
# =============================================================================
def render_scene_08():
    out_mp4 = os.path.join(SCENES_DIR, "scene_08.mp4")
    overlay = load_overlay("badge_scene_08.png")
    outro_card = load_overlay("outro_title_card.png")
    pipe = open_ffmpeg_pipe(out_mp4)
    print("Rendering Scene 8: Triumph & Smile [180 frames]...")

    for f in range(SCENE_FRAMES):
        t = f / FPS
        # Camera Pull Back Ease-Out
        zoom = 1.05 - 0.05 * Easing.ease_out_quad(f / float(SCENE_FRAMES))
        
        # Aryan Salute Arm Motion
        salute_angle = 15.0 * math.sin(min(math.pi, f / 40.0 * math.pi))
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <!-- Glistening Rain Scene Outside Hospital -->
          <rect width="1920" height="1080" fill="#070a12"/>
          
          <g transform="translate(960, 540) scale({zoom}) translate(-960, -540)">
            <!-- Warm Hospital Entrance Backlight -->
            <rect x="300" y="160" width="1320" height="660" rx="20" fill="#0f172a" stroke="#1e293b" stroke-width="4"/>
            
            <!-- Ground with Glistening Reflections -->
            <rect x="0" y="800" width="1920" height="280" fill="#090d16"/>
            <ellipse cx="600" cy="920" rx="280" ry="30" fill="rgba(56, 189, 248, 0.2)"/>
            <ellipse cx="1300" cy="920" rx="280" ry="30" fill="rgba(250, 204, 21, 0.2)"/>
            
            <!-- Aryan on Left: Giving Warm Salute -->
            <path d="M440,820 Q600,760 760,820 L730,1080 L470,1080 Z" fill="#0284c7"/>
            <circle cx="600" cy="500" r="115" fill="#0f172a" stroke="#0284c7" stroke-width="5"/> <!-- Helmet -->
            <!-- Open Visor with Genuine Warm Grin -->
            <path d="M540,460 L660,460" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
            <circle cx="600" cy="510" r="45" fill="#fdba74"/>
            <!-- Happy Smiling Eyes & Smile -->
            <path d="M575,495 Q590,480 605,495" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M580,535 Q600,555 620,535" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            
            <!-- Saluting Right Arm -->
            <path d="M720,820 L840,{580 - salute_angle} L880,{460 - salute_angle}" stroke="#0284c7" stroke-width="32" stroke-linecap="round"/>
            <circle cx="880" cy="{460 - salute_angle}" r="22" fill="#fdba74"/> <!-- Two-finger salute hand -->
            
            <!-- Dr. Ananya on Right: Deeply Moved, Smiling with Pastry -->
            <path d="M1160,820 Q1320,760 1480,820 L1460,1080 L1180,1080 Z" fill="#059669"/>
            <circle cx="1320" cy="500" r="110" fill="#fed7aa"/>
            <path d="M1210,480 Q1320,350 1430,480 Z" fill="#065f46"/>
            <!-- Happy Tearful Eyes & Broad Smile -->
            <path d="M1270,490 Q1290,475 1310,490" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M1330,490 Q1350,475 1370,490" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M1290,535 Q1320,565 1350,535 Z" fill="#7f1d1d"/>
            
            <!-- Holding Pastry in Hands -->
            <rect x="1230" y="660" width="180" height="90" rx="12" fill="#fda4af" stroke="#e11d48" stroke-width="4"/>
          </g>
          
          <!-- Soft Glistening Rain -->
          {ParticleSystem.generate_rain_svg(f, count=25)}
        </svg>"""

        base_img = render_svg_to_image(svg)
        
        # Dialogue overlay up to frame 125
        apply_overlay(base_img, overlay, f, start_frame=12, end_frame=125)
        
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
# MAIN RENDERER ENTRYPOINT
# =============================================================================
if __name__ == "__main__":
    import time
    t0 = time.time()
    print("=================================================================")
    print("MASTER AI — PHASE 7.7.4: HIGH-FIDELITY 1080P SCENE RENDERER")
    print("Scenes: 8 | Frames per Scene: 180 | FPS: 24.0 CFR | Res: 1920x1080")
    print("=================================================================")
    
    render_scene_01()
    render_scene_02()
    render_scene_03()
    render_scene_04()
    render_scene_05()
    render_scene_06()
    render_scene_07()
    render_scene_08()
    
    dt = time.time() - t0
    print(f"\nAll 8 scenes rendered in {dt:.2f}s (~{dt/1440*1000:.1f}ms/frame)!")
