"""
render_calibration_7741.py
===========================
Master AI - Phase 7.7.4.1 Calibration Test Renderer
Renders a 10.000s (240 frames @ 24fps CFR, 1920x1080) visual calibration film.

Test Blocks:
- Block 1 (0.0 - 2.5s): Static Camera & Micro-Motion (zero camera drift, eyelid blink, breathing)
- Block 2 (2.5 - 5.0s): Smooth Cinematic Zoom (ease_in_out_cubic 1.0x -> 1.35x, lip-sync visemes)
- Block 3 (5.0 - 7.5s): Multi-Plane Parallax Pan (4 depth layers moving horizontally, zero vertical drift)
- Block 4 (7.5 - 10.0s): Stabilized Vehicular Ride (smooth 6Hz damped harmonic road vibration)

Strictly uses render_svg_to_image_safe with exact 1920x1080x3 byte verification.
"""

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image
import imageio_ffmpeg

ENGINE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4.1\engine"
sys.path.append(ENGINE_DIR)
from motion_director import Easing, Camera2D, BlinkController, LipSyncVisemeController, BreathingController, ParticleSystem, render_svg_to_image_safe

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4.1"
OUTPUT_MP4 = os.path.join(BASE_DIR, "calibration_video.mp4")
TEMP_VIDEO = os.path.join(BASE_DIR, "temp_calibration_raw.mp4")
AUDIO_SRC = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\audio\final_mix.wav"

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
WIDTH = 1920
HEIGHT = 1080
FPS = 24
TOTAL_FRAMES = 240  # Exactly 10.000 seconds

def open_ffmpeg_pipe(out_mp4):
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        out_mp4
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_calibration():
    print("=================================================================")
    print("MASTER AI — PHASE 7.7.4.1: RENDERING CALIBRATION TEST VIDEO")
    print(f"Target: 10.000s | {TOTAL_FRAMES} Frames | 1920x1080 @ 24fps CFR")
    print("=================================================================")

    pipe = open_ffmpeg_pipe(TEMP_VIDEO)
    blink_ctrl = BlinkController(fps=FPS)
    cam = Camera2D()

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)
        
        # -------------------------------------------------------------
        # BLOCK 1: Static Camera Calibration (Frames 0 to 59, 0.0s - 2.5s)
        # -------------------------------------------------------------
        if f < 60:
            stage_name = "BLOCK 1: STATIC CAMERA (ZERO JITTER BASELINE)"
            # Breathing sway (subtle organic chest motion)
            sway_y = BreathingController.get_sway(t, rate_hz=0.35, amplitude_px=2.0)
            eyelid = blink_ctrl.get_eyelid_closure(f)
            
            # Static camera: exact center, zoom 1.0, zero shake
            cam.set_position(0.0, 0.0, zoom=1.0)
            
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#09050d"/>
              
              <!-- Calibration Grid (Reference grid to verify zero scanline wobble) -->
              <g stroke="#1e293b" stroke-width="1" opacity="0.4">
                {"".join([f'<line x1="{x}" y1="0" x2="{x}" y2="1080"/>' for x in range(0, 1921, 120)])}
                {"".join([f'<line x1="0" y1="{y}" x2="1920" y2="{y}"/>' for y in range(0, 1081, 120)])}
              </g>
              
              <!-- Dark Street Background -->
              <rect x="0" y="680" width="1920" height="400" fill="#0f172a"/>
              <line x1="0" y1="680" x2="1920" y2="680" stroke="#38bdf8" stroke-width="4"/>
              
              <!-- Character: Aryan (Centered Medium Shot) -->
              <g transform="translate(960, 480)">
                <!-- Torso with Breathing Sway -->
                <g transform="translate(0, {sway_y:.2f})">
                  <path d="M-140,240 Q0,180 140,240 L180,600 L-180,600 Z" fill="#0284c7" stroke="#0369a1" stroke-width="6"/> <!-- Delivery Jacket -->
                  <rect x="-40" y="280" width="80" height="220" fill="#f59e0b"/> <!-- Reflective Hi-Viz Stripe -->
                  <text x="0" y="380" font-family="sans-serif" font-size="20" font-weight="900" fill="#0f172a" text-anchor="middle">EXPRESS</text>
                  
                  <!-- Neck & Helmet -->
                  <rect x="-35" y="140" width="70" height="60" fill="#fdba74"/>
                  <!-- Black Modular Helmet -->
                  <ellipse cx="0" cy="50" rx="130" ry="140" fill="#0f172a" stroke="#ef4444" stroke-width="8"/>
                  <path d="M-90,-10 Q0,-40 90,-10 Q110,40 90,80 Q0,100 -90,80 Z" fill="#1e293b"/> <!-- Visor Opening -->
                  
                  <!-- Eyes Inside Helmet -->
                  {
                  f'<line x1="-55" y1="35" x2="-20" y2="35" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/><line x1="20" y1="35" x2="55" y2="35" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>'
                  if eyelid > 0.4 else
                  '<ellipse cx="-38" cy="35" rx="18" ry="12" fill="#ffffff"/><circle cx="-38" cy="35" r="7" fill="#0f172a"/><circle cx="-35" cy="32" r="2.5" fill="#ffffff"/>'
                  '<ellipse cx="38" cy="35" rx="18" ry="12" fill="#ffffff"/><circle cx="38" cy="35" r="7" fill="#0f172a"/><circle cx="41" cy="32" r="2.5" fill="#ffffff"/>'
                  }
                </g>
              </g>
              
              <!-- Calibration Telemetry Badge -->
              <rect x="50" y="50" width="620" height="130" rx="12" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="80" cy="85" r="8" fill="#22c55e"/>
              <text x="105" y="92" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">PHASE 7.7.4.1 CALIBRATION SUITE</text>
              <text x="75" y="125" font-family="sans-serif" font-size="16" font-weight="700" fill="#38bdf8">{stage_name}</text>
              <text x="75" y="155" font-family="sans-serif" font-size="14" font-weight="600" fill="#94a3b8">Frame: {f:03d}/240 | Time: {t:4.2f}s | Camera Jitter: 0.00 px</text>
              
              <!-- Atmospheric Rain -->
              {ParticleSystem.generate_rain_svg(f, count=25)}
            </svg>"""

        # -------------------------------------------------------------
        # BLOCK 2: Smooth Cinematic Zoom (Frames 60 to 119, 2.5s - 5.0s)
        # -------------------------------------------------------------
        elif f < 120:
            stage_name = "BLOCK 2: SMOOTH CINEMATIC ZOOM (EASING CUBIC)"
            progress = (f - 60) / 60.0
            zoom = 1.0 + 0.35 * Easing.ease_in_out_cubic(progress)
            
            # Lip sync articulation
            mouth_amp = 0.4 + 0.35 * abs(math.sin(10.0 * t))
            mouth = LipSyncVisemeController.get_mouth_viseme(mouth_amp)
            eyelid = blink_ctrl.get_eyelid_closure(f)
            
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#09050d"/>
              
              <!-- Centered Zoom Transform -->
              <g transform="translate(960, 540) scale({zoom:.4f}) translate(-960, -540)">
                <!-- Background Streets -->
                <rect x="0" y="680" width="1920" height="400" fill="#0f172a"/>
                <line x1="0" y1="680" x2="1920" y2="680" stroke="#38bdf8" stroke-width="4"/>
                
                <!-- Character & Delivery Console -->
                <g transform="translate(960, 480)">
                  <path d="M-140,240 Q0,180 140,240 L180,600 L-180,600 Z" fill="#0284c7" stroke="#0369a1" stroke-width="6"/>
                  <rect x="-40" y="280" width="80" height="220" fill="#f59e0b"/>
                  
                  <!-- Helmet -->
                  <rect x="-35" y="140" width="70" height="60" fill="#fdba74"/>
                  <ellipse cx="0" cy="50" rx="130" ry="140" fill="#0f172a" stroke="#ef4444" stroke-width="8"/>
                  <path d="M-90,-10 Q0,-40 90,-10 Q110,40 90,80 Q0,100 -90,80 Z" fill="#1e293b"/>
                  
                  <!-- Eyes -->
                  {
                  f'<line x1="-55" y1="35" x2="-20" y2="35" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/><line x1="20" y1="35" x2="55" y2="35" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>'
                  if eyelid > 0.4 else
                  '<ellipse cx="-38" cy="35" rx="18" ry="12" fill="#ffffff"/><circle cx="-38" cy="35" r="7" fill="#0f172a"/>'
                  '<ellipse cx="38" cy="35" rx="18" ry="12" fill="#ffffff"/><circle cx="38" cy="35" r="7" fill="#0f172a"/>'
                  }
                  
                  <!-- Lip Sync Viseme Mouth -->
                  <ellipse cx="0" cy="72" rx="{14 * mouth['width_scale']:.1f}" ry="{mouth['height'] * 0.45:.1f}" fill="#7f1d1d"/>
                </g>
                
                <!-- Smartphone Console Mounted on Handlebars -->
                <g transform="translate(680, 720)">
                  <rect x="0" y="0" width="560" height="340" rx="24" fill="#0c070c" stroke="#dc2626" stroke-width="6"/>
                  <text x="280" y="60" font-family="sans-serif" font-size="24" font-weight="900" fill="#ef4444" text-anchor="middle">ST. MARTHA'S ICU DELIVERY</text>
                  <text x="280" y="150" font-family="sans-serif" font-size="64" font-weight="900" fill="#ffffff" text-anchor="middle">07:42</text>
                  <text x="280" y="195" font-family="sans-serif" font-size="18" font-weight="700" fill="#38bdf8" text-anchor="middle">SPEED: 72 KM/H • ETA 4 MIN</text>
                </g>
              </g>
              
              <!-- Calibration Telemetry Badge -->
              <rect x="50" y="50" width="620" height="130" rx="12" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="80" cy="85" r="8" fill="#38bdf8"/>
              <text x="105" y="92" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">PHASE 7.7.4.1 CALIBRATION SUITE</text>
              <text x="75" y="125" font-family="sans-serif" font-size="16" font-weight="700" fill="#38bdf8">{stage_name}</text>
              <text x="75" y="155" font-family="sans-serif" font-size="14" font-weight="600" fill="#94a3b8">Frame: {f:03d}/240 | Zoom: {zoom:.3f}x | Monotonic & Continuous</text>
              
              {ParticleSystem.generate_rain_svg(f, count=30)}
            </svg>"""

        # -------------------------------------------------------------
        # BLOCK 3: Multi-Plane Optical Parallax (Frames 120 to 179, 5.0s - 7.5s)
        # -------------------------------------------------------------
        elif f < 180:
            stage_name = "BLOCK 3: MULTI-PLANE OPTICAL PARALLAX PAN"
            progress = (f - 120) / 60.0
            pan_speed = 32.0  # px per frame
            
            # Continuous parallax offsets (strictly horizontal, zero vertical drift)
            bg_x = ((f - 120) * pan_speed * 0.20) % 1920
            mid_x = ((f - 120) * pan_speed * 0.55) % 1920
            fore_x = ((f - 120) * pan_speed * 1.10) % 1920
            
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#04060d"/>
              
              <!-- Layer 1: Distant Sky & Moon (Parallax 0.20) -->
              <g transform="translate({-bg_x:.2f}, 0)">
                <circle cx="1600" cy="200" r="80" fill="#f8fafc" opacity="0.3"/>
                <circle cx="3520" cy="200" r="80" fill="#f8fafc" opacity="0.3"/>
                <!-- Distant Mumbai Skyline Silhouette -->
                <path d="M0,580 L200,580 L200,420 L320,420 L320,580 L500,580 L500,380 L620,380 L620,580 L900,580 L900,460 L1020,460 L1020,580 L1400,580 L1400,340 L1550,340 L1550,580 L1920,580 L1920,1080 L0,1080 Z" fill="#090d16"/>
                <path d="M1920,580 L2120,580 L2120,420 L2240,420 L2240,580 L2420,580 L2420,380 L2540,380 L2540,580 L2820,580 L2820,460 L2940,460 L2940,580 L3320,580 L3320,340 L3470,340 L3470,580 L3840,580 L3840,1080 L1920,1080 Z" fill="#090d16"/>
              </g>
              
              <!-- Layer 2: Midground Highway Architecture & Streetlights (Parallax 0.55) -->
              <g transform="translate({-mid_x:.2f}, 0)">
                <rect x="0" y="650" width="3840" height="430" fill="#0f172a"/>
                {"".join([f'<rect x="{i*300}" y="420" width="16" height="230" fill="#334155"/><circle cx="{i*300+8}" cy="410" r="24" fill="#facc15" opacity="0.6"/>' for i in range(14)])}
              </g>
              
              <!-- Layer 3: Foreground Subject (Aryan on Electric Bike, Parallax 1.0) -->
              <g transform="translate(820, 620)">
                <!-- Electric Bike Chassis -->
                <path d="M-120,120 L40,80 L140,120 L80,180 L-80,180 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="5"/>
                <!-- Wheels -->
                <circle cx="-120" cy="180" r="60" fill="#0f172a" stroke="#475569" stroke-width="8"/>
                <circle cx="140" cy="180" r="60" fill="#0f172a" stroke="#475569" stroke-width="8"/>
                <!-- Rider Aryan in Dynamic Forward Lean -->
                <path d="M-40,80 L20,-20 L60,40" stroke="#0284c7" stroke-width="36" stroke-linecap="round"/>
                <!-- Helmet -->
                <circle cx="25" cy="-60" r="45" fill="#0f172a" stroke="#ef4444" stroke-width="6"/>
                <path d="M20,-60 L55,-55" stroke="#38bdf8" stroke-width="12" stroke-linecap="round"/>
                <!-- Insulated Medical Box on Back Rack -->
                <rect x="-110" y="0" width="80" height="90" rx="8" fill="#dc2626" stroke="#fca5a5" stroke-width="4"/>
                <text x="-70" y="52" font-family="sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">+</text>
              </g>
              
              <!-- Layer 4: Foreground Road Puddles & Splash (Parallax 1.10) -->
              <g transform="translate({-fore_x:.2f}, 0)">
                {"".join([f'<ellipse cx="{i*450+150}" cy="960" rx="140" ry="24" fill="#0284c7" opacity="0.4"/>' for i in range(10)])}
              </g>
              
              <!-- Calibration Telemetry Badge -->
              <rect x="50" y="50" width="620" height="130" rx="12" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="80" cy="85" r="8" fill="#f59e0b"/>
              <text x="105" y="92" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">PHASE 7.7.4.1 CALIBRATION SUITE</text>
              <text x="75" y="125" font-family="sans-serif" font-size="16" font-weight="700" fill="#38bdf8">{stage_name}</text>
              <text x="75" y="155" font-family="sans-serif" font-size="14" font-weight="600" fill="#94a3b8">Frame: {f:03d}/240 | 4 Layers | Delta Y: 0.00 px (Locked)</text>
              
              {ParticleSystem.generate_rain_svg(f, count=40)}
            </svg>"""

        # -------------------------------------------------------------
        # BLOCK 4: Stabilized Ride & Harmonic Road Vibration (Frames 180 to 239, 7.5s - 10.0s)
        # -------------------------------------------------------------
        else:
            stage_name = "BLOCK 4: NYQUIST-SAFE ROAD VIBRATION & BRAKING"
            progress = (f - 180) / 60.0
            
            # Smooth 6.0 Hz road vibration damped to zero at braking
            vibe_t = (f - 180) / float(FPS)
            damping = 1.0 - Easing.ease_in_out_cubic(progress)
            cam.trigger_shake(vibe_t, intensity=3.5 * damping)
            
            # Decelerating parallax
            cur_speed = 36.0 * (1.0 - 0.7 * progress)
            fore_x = ((f - 180) * cur_speed) % 1920
            
            svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
              <rect width="1920" height="1080" fill="#04060d"/>
              
              <!-- Hospital Emergency Gate Ahead -->
              <g transform="translate(1300, 380)">
                <rect x="0" y="0" width="500" height="400" rx="16" fill="#0f172a" stroke="#38bdf8" stroke-width="6"/>
                <rect x="50" y="50" width="400" height="70" rx="10" fill="#b91c1c"/>
                <text x="250" y="95" font-family="sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">ICU EMERGENCY ENTRY</text>
                <circle cx="250" cy="220" r="45" fill="#ffffff"/>
                <path d="M250,195 L250,245 M225,220 L275,220" stroke="#dc2626" stroke-width="12" stroke-linecap="round"/>
              </g>
              
              <!-- Road Surface with Safe Camera Vibration -->
              <rect x="0" y="700" width="1920" height="380" fill="#090d16"/>
              
              <!-- Aryan & Bike with Damped Harmonic Vibration -->
              <g transform="translate({650 + cam.shake_x:.2f}, {640 + cam.shake_y:.2f})">
                <path d="M-120,120 L40,80 L140,120 L80,180 L-80,180 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="5"/>
                <circle cx="-120" cy="180" r="60" fill="#0f172a" stroke="#475569" stroke-width="8"/>
                <circle cx="140" cy="180" r="60" fill="#0f172a" stroke="#475569" stroke-width="8"/>
                <path d="M-40,80 L20,-20 L60,40" stroke="#0284c7" stroke-width="36" stroke-linecap="round"/>
                <circle cx="25" cy="-60" r="45" fill="#0f172a" stroke="#ef4444" stroke-width="6"/>
                <path d="M20,-60 L55,-55" stroke="#38bdf8" stroke-width="12" stroke-linecap="round"/>
                <rect x="-110" y="0" width="80" height="90" rx="8" fill="#dc2626" stroke="#fca5a5" stroke-width="4"/>
                <text x="-70" y="52" font-family="sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">+</text>
              </g>
              
              <!-- Calibration Telemetry Badge -->
              <rect x="50" y="50" width="620" height="130" rx="12" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="80" cy="85" r="8" fill="#a855f7"/>
              <text x="105" y="92" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">PHASE 7.7.4.1 CALIBRATION SUITE</text>
              <text x="75" y="125" font-family="sans-serif" font-size="16" font-weight="700" fill="#38bdf8">{stage_name}</text>
              <text x="75" y="155" font-family="sans-serif" font-size="14" font-weight="600" fill="#94a3b8">Frame: {f:03d}/240 | Safe 6Hz Shake: dx={cam.shake_x:.2f}, dy={cam.shake_y:.2f}</text>
              
              {ParticleSystem.generate_rain_svg(f, count=30)}
            </svg>"""

        # Strict safe rasterization with exact stride enforcement
        img = render_svg_to_image_safe(svg, WIDTH, HEIGHT)
        raw_bytes = img.tobytes()
        assert len(raw_bytes) == WIDTH * HEIGHT * 3, f"Buffer size mismatch: {len(raw_bytes)}"
        pipe.stdin.write(raw_bytes)
        
        if f % 30 == 0:
            print(f"Rendered frame {f:03d} / {TOTAL_FRAMES} ({t:.2f}s)")

    pipe.stdin.close()
    pipe.wait()
    print("Video stream rendering complete.")

    # Multiplex first 10.0s of final_mix.wav audio
    print("\nMultiplexing audio into calibration_video.mp4...")
    cmd_audio = [
        FFMPEG_BIN, "-y",
        "-i", TEMP_VIDEO,
        "-i", AUDIO_SRC,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-t", "10.000",
        "-movflags", "+faststart",
        OUTPUT_MP4
    ]
    subprocess.run(cmd_audio, check=True)
    if os.path.exists(TEMP_VIDEO):
        os.remove(TEMP_VIDEO)
        
    print(f"\nCALIBRATION VIDEO CREATED: {OUTPUT_MP4}")
    print(f"File size: {os.path.getsize(OUTPUT_MP4):,} bytes")

if __name__ == "__main__":
    render_calibration()
