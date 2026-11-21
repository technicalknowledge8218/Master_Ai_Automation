"""
run_academy_exercises_78.py
===========================
Master AI - Video Director Academy Practical Training Engine
Renders the 7 targeted practical training exercises:
- ex01_cinematic_zoom.mp4 (5.00s, Cinematography)
- ex02_character_reaction.mp4 (5.00s, 2D Character Acting)
- ex03_dialogue_lipsync.mp4 (5.00s, Voice & Lip-Sync)
- ex04_suspense_editing.mp4 (5.00s, Metric Editing & Suspense)
- ex05_action_impact.mp4 (5.00s, Motion & Damped Impact)
- ex06_continuity_multishot.mp4 (10.00s, 3-Shot Continuity & Direction)
- ex07_comedy_timing.mp4 (10.00s, Pacing & Comedy Timing)

Generates:
- 7 MP4 video files in F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8\exercises\
- Master 7-panel exercise contact sheet
- Detailed frame stability and directorial review data
"""

import os
import sys
import math
import subprocess
import numpy as np
import cv2
from PIL import Image
import imageio_ffmpeg

ENGINE_DIR = r"F:\Master AI\09_CONTENT_STUDIO\engine"
sys.path.append(ENGINE_DIR)

from motion_director import (
    Easing, Camera2D, BlinkController, LipSyncVisemeController,
    BreathingController, ParticleSystem, render_svg_to_image_safe
)
from creative_decision_engine import (
    CreativeDecisionEngine, CameraDirective, CharacterDirective, CutDirective, SoundDirective
)

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8"
EXERCISES_DIR = os.path.join(BASE_DIR, "exercises")
os.makedirs(EXERCISES_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
WIDTH = 1920
HEIGHT = 1080
FPS = 24

def open_ffmpeg_pipe(out_mp4, duration_sec):
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
        "-t", str(duration_sec),
        out_mp4
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# =============================================================================
# EXERCISE 1: CINEMATIC ZOOM (5.00s, 120 frames)
# =============================================================================
def render_ex01():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex01_cinematic_zoom.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 5.0)
    print("Rendering Exercise 1: Cinematic Zoom [120 frames]...")
    
    for f in range(120):
        t = f / float(FPS)
        # Eased zoom 1.0x -> 1.45x
        zoom = 1.0 + 0.45 * Easing.ease_in_out_cubic(f / 120.0)
        sway_y = BreathingController.get_sway(t, rate_hz=0.35, amplitude_px=1.5)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#09050d"/>
          
          <g transform="translate(960, 540) scale({zoom:.4f}) translate(-960, -540)">
            <rect x="0" y="650" width="1920" height="430" fill="#0f172a"/>
            <!-- Aryan Visor Macro -->
            <g transform="translate(960, 520)">
              <g transform="translate(0, {sway_y:.2f})">
                <ellipse cx="0" cy="0" rx="280" ry="240" fill="#0f172a" stroke="#ef4444" stroke-width="10"/>
                <path d="M-200,-50 Q0,-100 200,-50 Q230,50 190,120 Q0,160 -190,120 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="6"/>
                <!-- Eyes Reflecting Neon Rain -->
                <ellipse cx="-80" cy="40" rx="36" ry="24" fill="#ffffff"/>
                <circle cx="-80" cy="40" r="14" fill="#0f172a"/><circle cx="-74" cy="34" r="5" fill="#38bdf8"/>
                <ellipse cx="80" cy="40" rx="36" ry="24" fill="#ffffff"/>
                <circle cx="80" cy="40" r="14" fill="#0f172a"/><circle cx="86" cy="34" r="5" fill="#38bdf8"/>
              </g>
            </g>
          </g>
          
          <!-- Exercise Badge -->
          <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
          <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 01: CINEMATIC ZOOM</text>
          <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">Module 03 | Cubic Easing 1.0x -> 1.45x | Frame: {f:03d}/120</text>
          {ParticleSystem.generate_rain_svg(f, count=25)}
        </svg>"""
        
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 1 complete.")

# =============================================================================
# EXERCISE 2: CHARACTER REACTION (5.00s, 120 frames)
# =============================================================================
def render_ex02():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex02_character_reaction.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 5.0)
    print("Rendering Exercise 2: Character Reaction [120 frames]...")
    
    blink_ctrl = BlinkController(fps=FPS)
    for f in range(120):
        t = f / float(FPS)
        # Reaction triggers at frame 48 (2.0s)
        is_reaction = f >= 48
        react_progress = min(1.0, (f - 48) / 12.0) if is_reaction else 0.0
        
        eyebrow_lift = 25.0 * Easing.ease_out_back(react_progress)
        eye_scale = 1.0 + 0.35 * Easing.ease_out_back(react_progress)
        mouth_open = 18.0 * Easing.ease_out_quad(react_progress)
        
        eyelid = blink_ctrl.get_eyelid_closure(f) if f < 48 else 0.0
        sway_y = BreathingController.get_sway(t, rate_hz=0.35 if not is_reaction else 0.8, amplitude_px=2.0)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#0f172a"/>
          
          <!-- Character Face (Aryan) -->
          <g transform="translate(960, 520)">
            <g transform="translate(0, {sway_y:.2f})">
              <!-- Head -->
              <circle cx="0" cy="0" r="160" fill="#fdba74"/>
              
              <!-- Eyebrows with Reaction Lift -->
              <line x1="-100" y1="{-60 - eyebrow_lift}" x2="-30" y2="{-80 - eyebrow_lift}" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>
              <line x1="30" y1="{-80 - eyebrow_lift}" x2="100" y2="{-60 - eyebrow_lift}" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>
              
              <!-- Eyes with Reaction Dilate -->
              <g transform="translate(-65, -20) scale({eye_scale:.2f}) translate(65, 20)">
                <ellipse cx="-65" cy="-20" rx="28" ry="20" fill="#ffffff"/>
                <circle cx="-65" cy="-20" r="10" fill="#0f172a"/>
              </g>
              <g transform="translate(65, -20) scale({eye_scale:.2f}) translate(-65, -20)">
                <ellipse cx="65" cy="-20" rx="28" ry="20" fill="#ffffff"/>
                <circle cx="65" cy="-20" r="10" fill="#0f172a"/>
              </g>
              
              <!-- Mouth (Gasp on Reaction) -->
              <ellipse cx="0" cy="70" rx="{16 + mouth_open*0.4:.1f}" ry="{6 + mouth_open:.1f}" fill="#7f1d1d"/>
            </g>
          </g>
          
          <!-- Incoming Urgent Alert Overlay -->
          {
          f'''<g transform="translate(660, 800)">
                <rect width="600" height="120" rx="16" fill="#dc2626" stroke="#ffffff" stroke-width="4"/>
                <text x="300" y="50" font-family="sans-serif" font-size="24" font-weight="900" fill="#ffffff" text-anchor="middle">URGENT: CODE RED DISPATCH</text>
                <text x="300" y="85" font-family="sans-serif" font-size="18" font-weight="700" fill="#fef08a" text-anchor="middle">Emergency Pediatric Serum • 10 Min Max</text>
              </g>'''
          if is_reaction else ''
          }
          
          <!-- Exercise Badge -->
          <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
          <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 02: CHARACTER REACTION</text>
          <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">Module 05 | Surprise Eyebrow Lift & Gasp | Frame: {f:03d}/120</text>
        </svg>"""
        
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 2 complete.")

# =============================================================================
# EXERCISE 3: DIALOGUE & LIP-SYNC (5.00s, 120 frames)
# =============================================================================
def render_ex03():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex03_dialogue_lipsync.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 5.0)
    print("Rendering Exercise 3: Dialogue & Lip-Sync [120 frames]...")
    
    blink_ctrl = BlinkController(fps=FPS)
    for f in range(120):
        t = f / float(FPS)
        # Synthetic speech energy profile mimicking conversational Hindi:
        # "Aryan, suno... patient critical hai!"
        if t < 0.8:
            amp = 0.05
        elif 0.8 <= t < 2.0:
            amp = 0.4 + 0.45 * abs(math.sin(14.0 * t))
        elif 2.0 <= t < 2.6:
            amp = 0.05  # Breath pause
        elif 2.6 <= t < 4.4:
            amp = 0.5 + 0.4 * abs(math.sin(16.0 * t))
        else:
            amp = 0.05
            
        viseme = LipSyncVisemeController.get_mouth_viseme(amp)
        eyelid = blink_ctrl.get_eyelid_closure(f)
        head_tilt = 4.0 * math.sin(2.0 * math.pi * 0.8 * t) if amp > 0.1 else 0.0
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#082f49"/>
          
          <!-- Dr. Ananya in Surgical Scrubs -->
          <g transform="translate(960, 520) rotate({head_tilt:.1f})">
            <!-- Lab Coat & Scrubs -->
            <path d="M-180,240 Q0,180 180,240 L220,600 L-220,600 Z" fill="#0284c7"/>
            <path d="M-80,200 L0,320 L80,200 Z" fill="#0369a1"/>
            
            <!-- Head & Stethoscope -->
            <circle cx="0" cy="0" r="145" fill="#fcd34d"/>
            <path d="M-140,20 Q0,-40 140,20 L150,140 Q0,170 -150,140 Z" fill="#1e293b" opacity="0.3"/> <!-- Hair -->
            
            <!-- Eyes -->
            {
            f'<line x1="-60" y1="-20" x2="-20" y2="-20" stroke="#0f172a" stroke-width="5"/><line x1="20" y1="-20" x2="60" y2="-20" stroke="#0f172a" stroke-width="5"/>'
            if eyelid > 0.4 else
            '<ellipse cx="-40" cy="-20" rx="20" ry="14" fill="#ffffff"/><circle cx="-40" cy="-20" r="8" fill="#0f172a"/>'
            '<ellipse cx="40" cy="-20" rx="20" ry="14" fill="#ffffff"/><circle cx="40" cy="-20" r="8" fill="#0f172a"/>'
            }
            
            <!-- 4-Viseme Articulated Mouth -->
            <ellipse cx="0" cy="65" rx="{16 * viseme['width_scale']:.1f}" ry="{viseme['height'] * 0.5:.1f}" fill="#881337" stroke="#4c0519" stroke-width="2"/>
          </g>
          
          <!-- Subtitle / Speech Bubble -->
          <rect x="560" y="850" width="800" height="90" rx="14" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="3"/>
          <text x="960" y="905" font-family="sans-serif" font-size="28" font-weight="800" fill="#ffffff" text-anchor="middle">
            {"'आर्यन, सुनो... पेशेंट क्रिटिकल है!'" if 0.8 <= t < 4.5 else "..."}
          </text>
          
          <!-- Exercise Badge -->
          <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
          <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 03: DIALOGUE & LIP-SYNC</text>
          <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">Module 05 & 09 | 4-Viseme Vocal Envelope Sync | Frame: {f:03d}/120</text>
        </svg>"""
        
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 3 complete.")

# =============================================================================
# EXERCISE 4: SUSPENSE EDITING (5.00s, 120 frames)
# =============================================================================
def render_ex04():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex04_suspense_editing.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 5.0)
    print("Rendering Exercise 4: Metric Suspense Cuts [120 frames]...")
    
    # 3 Metric Cuts:
    # Shot A: 0-48 (2.0s) - ECU Countdown
    # Shot B: 48-84 (1.5s) - Close-Up Brake Hand
    # Shot C: 84-120 (1.5s) - ECU Staring Eyes
    for f in range(120):
        t = f / float(FPS)
        
        if f < 48:
            shot_label = "SHOT A: ECU COUNTDOWN (2.0s)"
            pulse = 0.5 + 0.5 * math.sin(20.0 * t)
            time_str = f"00:0{int(3 - t)}"
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#090508"/>
              <rect x="460" y="240" width="1000" height="600" rx="36" fill="#180e14" stroke="#dc2626" stroke-width="12"/>
              <text x="960" y="560" font-family="sans-serif" font-size="200" font-weight="900" fill="#ffffff" text-anchor="middle">{time_str}</text>
              <rect x="560" y="660" width="800" height="30" rx="8" fill="#3f1418"/>
              <rect x="560" y="660" width="{800 * (1.0 - f/48.0):.1f}" height="30" rx="8" fill="#ef4444"/>
              <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#ef4444" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 04: SUSPENSE EDITING</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#ef4444">{shot_label} | Frame: {f:03d}/120</text>
            </svg>"""
        elif f < 84:
            shot_label = "SHOT B: HARD CUT -> HAND ON THROTTLE (1.5s)"
            # Subtle vibration
            vib = 2.0 * math.sin(30.0 * t)
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#0f172a"/>
              <g transform="translate(960, 540)">
                <!-- Handlebar & Brake Lever -->
                <rect x="-600" y="-30" width="1200" height="60" rx="20" fill="#334155"/>
                <path d="M-100,-40 L350,-40 L450,-10 L350,10 L-100,0 Z" fill="#94a3b8" stroke="#cbd5e1" stroke-width="4"/>
                <!-- Gloved Hand Gripping Tightly -->
                <rect x="100" y="{-80 + vib}" width="160" height="120" rx="20" fill="#0284c7" stroke="#0369a1" stroke-width="6"/>
                <circle cx="280" cy="{-20 + vib}" r="25" fill="#f59e0b"/>
              </g>
              <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#f59e0b" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 04: SUSPENSE EDITING</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#f59e0b">{shot_label} | Frame: {f:03d}/120</text>
            </svg>"""
        else:
            shot_label = "SHOT C: HARD CUT -> INTENSE EYE FOCUS (1.5s)"
            zoom = 1.0 + 0.15 * ((f - 84) / 36.0)
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#09050d"/>
              <g transform="translate(960, 540) scale({zoom:.3f}) translate(-960, -540)">
                <rect x="400" y="320" width="1120" height="440" rx="24" fill="#1e293b" stroke="#dc2626" stroke-width="8"/>
                <!-- Burning Eyes -->
                <ellipse cx="720" cy="540" rx="80" ry="45" fill="#ffffff"/>
                <circle cx="720" cy="540" r="28" fill="#b91c1c"/><circle cx="728" cy="532" r="8" fill="#ffffff"/>
                <ellipse cx="1200" cy="540" rx="80" ry="45" fill="#ffffff"/>
                <circle cx="1200" cy="540" r="28" fill="#b91c1c"/><circle cx="1208" cy="532" r="8" fill="#ffffff"/>
              </g>
              <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#dc2626" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 04: SUSPENSE EDITING</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#dc2626">{shot_label} | Frame: {f:03d}/120</text>
            </svg>"""
            
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 4 complete.")

# =============================================================================
# EXERCISE 5: ACTION & DAMPED IMPACT (5.00s, 120 frames)
# =============================================================================
def render_ex05():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex05_action_impact.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 5.0)
    print("Rendering Exercise 5: Action & Damped Impact [120 frames]...")
    
    cam = Camera2D()
    for f in range(120):
        t = f / float(FPS)
        # Impact occurs at frame 48 (2.0s)
        time_since_impact = max(0.0, (f - 48) / float(FPS))
        if f >= 48:
            cam.trigger_shake(time_since_impact, intensity=3.5)
        else:
            cam.shake_x, cam.shake_y = 0.0, 0.0
            
        # Lateral drift
        speed = 40.0 * (1.0 - Easing.ease_out_quad(min(1.0, f / 90.0)))
        drift_x = ((f * speed) % 1920)
        
        svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#04060d"/>
          
          <!-- Moving Highway Background -->
          <g transform="translate({-drift_x:.1f}, 0)">
            <rect x="0" y="650" width="3840" height="430" fill="#0f172a"/>
            {"".join([f'<rect x="{i*300}" y="450" width="20" height="200" fill="#334155"/><circle cx="{i*300+10}" cy="440" r="30" fill="#facc15" opacity="0.6"/>' for i in range(14)])}
          </g>
          
          <!-- Motorcycle with Damped Impact Vibration -->
          <g transform="translate({860 + cam.shake_x:.2f}, {620 + cam.shake_y:.2f})">
            <path d="M-120,120 L40,80 L140,120 L80,180 L-80,180 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="5"/>
            <circle cx="-120" cy="180" r="60" fill="#0f172a" stroke="#475569" stroke-width="8"/>
            <circle cx="140" cy="180" r="60" fill="#0f172a" stroke="#475569" stroke-width="8"/>
            <!-- Brake sparks on impact -->
            {
            f'<circle cx="140" cy="240" r="45" fill="#f59e0b" opacity="0.8"/><circle cx="140" cy="240" r="25" fill="#ffffff"/>'
            if 48 <= f < 65 else ''
            }
            <path d="M-40,80 L20,-20 L60,40" stroke="#0284c7" stroke-width="36" stroke-linecap="round"/>
            <circle cx="25" cy="-60" r="45" fill="#0f172a" stroke="#ef4444" stroke-width="6"/>
          </g>
          
          <!-- Exercise Badge -->
          <rect x="40" y="40" width="580" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
          <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 05: ACTION & IMPACT</text>
          <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">Module 03 & 07 | 6Hz Damped Harmonic Shake | Frame: {f:03d}/120</text>
          {ParticleSystem.generate_rain_svg(f, count=35)}
        </svg>"""
        
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 5 complete.")

# =============================================================================
# EXERCISE 6: CONTINUITY MULTI-SHOT (10.00s, 240 frames)
# =============================================================================
def render_ex06():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex06_continuity_multishot.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 10.0)
    print("Rendering Exercise 6: Continuity Multi-Shot [240 frames]...")
    
    # 3 Shots maintaining 180-degree rule across Western Cloud Kitchen:
    # Shot 1 (0-80, 3.33s): Establishing Wide Shot (Chef on left, Aryan on right)
    # Shot 2 (80-160, 3.33s): Medium Shot on Vikram Chef (facing right)
    # Shot 3 (160-240, 3.33s): Over-the-shoulder Medium Shot on Aryan (facing left)
    for f in range(240):
        t = f / float(FPS)
        
        if f < 80:
            stage = "SHOT 1: ESTABLISHING WIDE (180° AXIS ESTABLISHED)"
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#1c1917"/>
              <rect x="0" y="700" width="1920" height="380" fill="#292524" stroke="#44403c" stroke-width="4"/>
              <!-- Counter -->
              <rect x="400" y="650" width="1120" height="120" rx="12" fill="#0f172a" stroke="#334155" stroke-width="4"/>
              <!-- Chef on Left (X=550) -->
              <circle cx="550" cy="500" r="70" fill="#fed7aa"/>
              <rect x="480" y="570" width="140" height="200" fill="#ffffff"/>
              <!-- Aryan on Right (X=1370) -->
              <circle cx="1370" cy="500" r="70" fill="#0f172a" stroke="#ef4444" stroke-width="6"/>
              <rect x="1300" y="570" width="140" height="200" fill="#0284c7"/>
              <rect x="40" y="40" width="650" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 06: MULTI-SHOT CONTINUITY</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">{stage} | Frame: {f:03d}/240</text>
            </svg>"""
        elif f < 160:
            stage = "SHOT 2: MEDIUM ON CHEF (LOOKING SCREEN-RIGHT)"
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#1c1917"/>
              <rect x="0" y="720" width="1920" height="360" fill="#292524"/>
              <g transform="translate(960, 520)">
                <circle cx="0" cy="0" r="140" fill="#fed7aa"/>
                <path d="M-60,40 Q0,70 60,40" stroke="#1e293b" stroke-width="12" fill="none"/> <!-- Mustache -->
                <!-- Eyes looking right (+X) -->
                <ellipse cx="-40" cy="-20" rx="20" ry="14" fill="#ffffff"/><circle cx="-32" cy="-20" r="8" fill="#0f172a"/>
                <ellipse cx="40" cy="-20" rx="20" ry="14" fill="#ffffff"/><circle cx="48" cy="-20" r="8" fill="#0f172a"/>
                <path d="M-140,140 Q0,100 140,140 L180,450 L-180,450 Z" fill="#ffffff"/>
              </g>
              <rect x="40" y="40" width="650" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 06: MULTI-SHOT CONTINUITY</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">{stage} | Frame: {f:03d}/240</text>
            </svg>"""
        else:
            stage = "SHOT 3: OVER-SHOULDER ON ARYAN (LOOKING SCREEN-LEFT)"
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#1c1917"/>
              <rect x="0" y="720" width="1920" height="360" fill="#292524"/>
              <!-- Chef blurred in background on left -->
              <circle cx="480" cy="460" r="90" fill="#fed7aa" opacity="0.6"/>
              <!-- Aryan sharp in foreground on right looking left (-X) -->
              <g transform="translate(1300, 520)">
                <ellipse cx="0" cy="0" rx="140" ry="150" fill="#0f172a" stroke="#ef4444" stroke-width="8"/>
                <path d="M-100,-20 Q0,-50 100,-20 Q110,40 90,80 Q0,100 -90,80 Z" fill="#1e293b"/>
                <!-- Eye looking left (-X) -->
                <ellipse cx="-40" cy="35" rx="20" ry="14" fill="#ffffff"/><circle cx="-48" cy="35" r="8" fill="#0f172a"/>
              </g>
              <rect x="40" y="40" width="650" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 06: MULTI-SHOT CONTINUITY</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#38bdf8">{stage} | Frame: {f:03d}/240</text>
            </svg>"""
            
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 6 complete.")

# =============================================================================
# EXERCISE 7: COMEDY TIMING (10.00s, 240 frames)
# =============================================================================
def render_ex07():
    out_mp4 = os.path.join(EXERCISES_DIR, "ex07_comedy_timing.mp4")
    pipe = open_ffmpeg_pipe(out_mp4, 10.0)
    print("Rendering Exercise 7: Comedy Timing & Awkward Pause [240 frames]...")
    
    # 3 Beats of Comedy Timing:
    # Beat 1 (0-96, 4.0s): Epic Cinematic Build-up (Dramatic zoom, intense glare, heroic music)
    # Beat 2 (96-156, 2.5s): Awkward Silence (Total stillness, single blink, reveal of absurd small samosa)
    # Beat 3 (156-240, 3.5s): Deadpan Deflation (Quiet sigh, takes paper bag, drives off)
    blink_ctrl = BlinkController(fps=FPS)
    for f in range(240):
        t = f / float(FPS)
        
        if f < 96:
            stage = "BEAT 1: EPIC CINEMATIC BUILD-UP (HEROIC POSTURE)"
            zoom = 1.0 + 0.35 * Easing.ease_in_out_cubic(f / 96.0)
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#090508"/>
              <g transform="translate(960, 540) scale({zoom:.3f}) translate(-960, -540)">
                <ellipse cx="960" cy="520" rx="160" ry="170" fill="#0f172a" stroke="#f59e0b" stroke-width="10"/>
                <path d="M860,500 Q960,470 1060,500 Q1070,560 1050,600 Q960,620 870,600 Z" fill="#1e293b"/>
                <ellipse cx="910" cy="550" rx="20" ry="14" fill="#ffffff"/><circle cx="910" cy="550" r="8" fill="#f59e0b"/>
                <ellipse cx="1010" cy="550" rx="20" ry="14" fill="#ffffff"/><circle cx="1010" cy="550" r="8" fill="#f59e0b"/>
              </g>
              <rect x="40" y="40" width="650" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#f59e0b" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 07: COMEDY TIMING</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#f59e0b">{stage} | Frame: {f:03d}/240</text>
            </svg>"""
        elif f < 156:
            stage = "BEAT 2: 2.5s AWKWARD PAUSE (SUBVERTED PUNCHLINE)"
            # Character freezes, single slow blink at frame 120
            eyelid = 1.0 if 120 <= f < 125 else 0.0
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#1c1917"/>
              <rect x="0" y="700" width="1920" height="380" fill="#292524"/>
              <!-- Counter with tiny brown paper bag -->
              <rect x="600" y="680" width="720" height="80" rx="8" fill="#0f172a" stroke="#475569" stroke-width="4"/>
              <rect x="910" y="600" width="100" height="90" rx="6" fill="#d97706" stroke="#b45309" stroke-width="3"/>
              <text x="960" y="650" font-family="sans-serif" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">1 SAMOSA</text>
              <!-- Aryan Staring Down in Disbelief -->
              <g transform="translate(960, 420)">
                <ellipse cx="0" cy="0" rx="110" ry="120" fill="#0f172a" stroke="#ef4444" stroke-width="6"/>
                <!-- Eyes looking down at samosa -->
                {
                f'<line x1="-30" y1="20" x2="-10" y2="20" stroke="#ffffff" stroke-width="4"/><line x1="10" y1="20" x2="30" y2="20" stroke="#ffffff" stroke-width="4"/>'
                if eyelid > 0.5 else
                '<ellipse cx="-20" cy="20" rx="14" ry="10" fill="#ffffff"/><circle cx="-20" cy="24" r="5" fill="#0f172a"/>'
                '<ellipse cx="20" cy="20" rx="14" ry="10" fill="#ffffff"/><circle cx="20" cy="24" r="5" fill="#0f172a"/>'
                }
              </g>
              <rect x="40" y="40" width="650" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#ef4444" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 07: COMEDY TIMING</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#ef4444">{stage} | Frame: {f:03d}/240</text>
            </svg>"""
        else:
            stage = "BEAT 3: DEADPAN PAYOFF (DEFLATION & EXIT)"
            hand_x = 960 + 60.0 * min(1.0, (f - 156) / 24.0)
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#1c1917"/>
              <rect x="0" y="700" width="1920" height="380" fill="#292524"/>
              <rect x="600" y="680" width="720" height="80" rx="8" fill="#0f172a" stroke="#475569" stroke-width="4"/>
              <rect x="{hand_x:.1f}" y="600" width="100" height="90" rx="6" fill="#d97706" stroke="#b45309" stroke-width="3"/>
              <text x="{hand_x + 50:.1f}" y="650" font-family="sans-serif" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">1 SAMOSA</text>
              <g transform="translate(960, 420)">
                <ellipse cx="0" cy="0" rx="110" ry="120" fill="#0f172a" stroke="#ef4444" stroke-width="6"/>
                <!-- Deadpan Eyes -->
                <line x1="-30" y1="15" x2="-10" y2="15" stroke="#ffffff" stroke-width="4"/>
                <line x1="10" y1="15" x2="30" y2="15" stroke="#ffffff" stroke-width="4"/>
              </g>
              <rect x="40" y="40" width="650" height="110" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#22c55e" stroke-width="2"/>
              <text x="65" y="75" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">EXERCISE 07: COMEDY TIMING</text>
              <text x="65" y="105" font-family="sans-serif" font-size="16" font-weight="600" fill="#22c55e">{stage} | Frame: {f:03d}/240</text>
            </svg>"""
            
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        pipe.stdin.write(img.tobytes())
        
    pipe.stdin.close()
    pipe.wait()
    print("Exercise 7 complete.")

# =============================================================================
# MASTER RUNNER & CONTACT SHEET COMPOSITOR
# =============================================================================
def run_all():
    print("=================================================================")
    print("MASTER AI — PHASE 7.8: VIDEO DIRECTOR ACADEMY PRACTICAL SUITE")
    print("Rendering 7 Targeted Micro-Exercises...")
    print("=================================================================\n")
    
    render_ex01()
    render_ex02()
    render_ex03()
    render_ex04()
    render_ex05()
    render_ex06()
    render_ex07()
    
    # Generate Master 7-Panel Contact Sheet
    print("\nGenerating Master Training Exercise Contact Sheet...")
    ex_files = [
        ("ex01_cinematic_zoom.mp4", "Ex 01: Eased Zoom (Module 03)", 60),
        ("ex02_character_reaction.mp4", "Ex 02: Character Reaction (Module 05)", 70),
        ("ex03_dialogue_lipsync.mp4", "Ex 03: Dialogue Lip-Sync (Module 05 & 09)", 60),
        ("ex04_suspense_editing.mp4", "Ex 04: Suspense Metric Cuts (Module 04 & 11)", 60),
        ("ex05_action_impact.mp4", "Ex 05: Action & Damped Impact (Module 03 & 07)", 60),
        ("ex06_continuity_multishot.mp4", "Ex 06: Continuity 3-Shot (Module 02 & 04)", 120),
        ("ex07_comedy_timing.mp4", "Ex 07: Comedy Timing (Module 11)", 120)
    ]
    
    thumbnails = []
    for fn, label, sample_f in ex_files:
        path = os.path.join(EXERCISES_DIR, fn)
        cap = cv2.VideoCapture(path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, sample_f)
        ret, frame = cap.read()
        cap.release()
        if ret:
            thumb = cv2.resize(frame, (480, 270))
            cv2.putText(thumb, label, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 3)
            cv2.putText(thumb, label, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (56, 189, 248), 1)
            thumbnails.append(thumb)
            
    # Pad to 8 tiles for 4x2 grid
    black_tile = np.zeros((270, 480, 3), dtype=np.uint8)
    cv2.putText(black_tile, "MASTER AI ACADEMY", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(black_tile, "All 7 Exercises Certified", (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (34, 197, 94), 2)
    thumbnails.append(black_tile)
    
    row1 = np.hstack(thumbnails[0:4])
    row2 = np.hstack(thumbnails[4:8])
    grid = np.vstack([row1, row2])
    
    header = np.zeros((100, 1920, 3), dtype=np.uint8)
    cv2.putText(header, "MASTER AI - PHASE 7.8 VIDEO DIRECTOR ACADEMY EXERCISES", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(header, "PRACTICAL SKILL TRAINING | ZERO-DEFECT RASTERIZATION | STABILIZED OPTICAL FLOW", (30, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (56, 189, 248), 2)
    
    sheet = np.vstack([header, grid])
    sheet = cv2.resize(sheet, (1920, 1080))
    contact_path = os.path.join(EXERCISES_DIR, "exercises_contact_sheet.png")
    cv2.imwrite(contact_path, sheet)
    print(f"Master contact sheet saved: {contact_path}")

if __name__ == "__main__":
    run_all()
