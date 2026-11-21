"""
render_validation_sample_710.py
================================
Master AI - Phase 7.10 Technical Integration Test & Validation Sample (Polished)
Demonstrates the Reference-Driven 2D Cinematic Architecture:
1. 4-Tier Visual Hierarchy (Progress bar, Topic badge pill, Centered focal card, Karaoke subtitles).
2. Explicit Notebook grid paper texture background.
3. Articulated 2D Vector Puppet Characters (Correct z-index, expressive face, hair, blinking, visemes).
4. Synchronized Karaoke Subtitles with animated yellow highlight box.
5. Multi-Track Audio: Neural conversational dialogue (< 0.40s gap), BGM, and spot Foley.

Runtime: Exactly 5.00 Seconds | 150 Frames @ 30.00 FPS CFR | 1080x1920 Full HD (9:16)
Output:
- F:\\Master AI\\00_CORE_SYSTEM\\research\\phase-7\\phase-7.10\\technical_validation_sample.mp4
"""

import os
import sys
import math
import wave
import struct
import subprocess
import numpy as np
from PIL import Image
import fitz
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.10"
OUT_MP4 = os.path.join(BASE_DIR, "technical_validation_sample.mp4")
AUDIO_WAV = os.path.join(BASE_DIR, "validation_audio.wav")

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
WIDTH = 1080
HEIGHT = 1920
FPS = 30
TOTAL_FRAMES = 150 # 5.00 seconds

KARAOKE_WORDS = [
    # Cue 1 (Karan)
    {"word": "यार,", "start": 0.50, "end": 0.85},
    {"word": "सिर्फ", "start": 0.85, "end": 1.20},
    {"word": "दस", "start": 1.20, "end": 1.50},
    {"word": "मिनट", "start": 1.50, "end": 1.85},
    {"word": "लेट", "start": 1.85, "end": 2.15},
    {"word": "हुआ!", "start": 2.15, "end": 2.45},
    # Gap: 2.45s to 2.85s (0.40s conversational hesitation beat)
    # Cue 2 (Meera)
    {"word": "तीन", "start": 2.85, "end": 3.15},
    {"word": "घंटे", "start": 3.15, "end": 3.45},
    {"word": "से", "start": 3.45, "end": 3.75},
    {"word": "लास्ट", "start": 3.75, "end": 4.10},
    {"word": "सीन", "start": 4.10, "end": 4.40},
    {"word": "दिखा?!", "start": 4.40, "end": 4.75},
]

# Pre-generate grid lines for notebook texture (avoiding SVG pattern bugs)
GRID_LINES = []
for gx in range(0, WIDTH + 40, 40):
    GRID_LINES.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{HEIGHT}" stroke="#e5dfd3" stroke-width="1.5"/>')
for gy in range(0, HEIGHT + 40, 40):
    GRID_LINES.append(f'<line x1="0" y1="{gy}" x2="{WIDTH}" y2="{gy}" stroke="#e5dfd3" stroke-width="1.5"/>')
GRID_SVG = "\n".join(GRID_LINES)

def get_karaoke_svg(current_time):
    if current_time < 2.6:
        cue_words = KARAOKE_WORDS[:6]
    else:
        cue_words = KARAOKE_WORDS[6:]
        
    parts = []
    start_x = 220
    word_gap = 110
    
    for idx, item in enumerate(cue_words):
        wx = start_x + idx * word_gap
        is_active = (item["start"] <= current_time <= item["end"])
        
        if is_active:
            parts.append(f"""
            <g transform="translate({wx}, 1620)">
              <rect x="-50" y="-42" width="100" height="58" rx="14" fill="#facc15" stroke="#000000" stroke-width="3.5"/>
              <text x="0" y="2" font-family="'Nirmala UI', 'Segoe UI', sans-serif" font-size="34" font-weight="900" fill="#000000" text-anchor="middle">{item['word']}</text>
            </g>
            """)
        else:
            parts.append(f"""
            <g transform="translate({wx}, 1620)">
              <text x="0" y="0" font-family="'Nirmala UI', 'Segoe UI', sans-serif" font-size="32" font-weight="800" fill="#1e293b" text-anchor="middle">{item['word']}</text>
            </g>
            """)
    return "".join(parts)

def render_validation_video():
    if not os.path.exists(AUDIO_WAV):
        raise FileNotFoundError("Audio mix missing")
        
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_WAV,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUT_MP4
    ]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Rendering 150 validation frames @ 30 FPS into FFmpeg pipe...")

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)
        progress = f / float(TOTAL_FRAMES)
        
        # 1. Retention Progress Bar
        bar_fill_w = int(progress * 760.0)
        
        # 2. Dynamic Topic Pill state & bounce
        if t < 2.6:
            topic_text = "REPLY LATE = NARAAZ"
            topic_bg = "#f97316" # Orange
            active_speaker = "karan"
        else:
            topic_text = "CALL CUT = GUSSA"
            topic_bg = "#ef4444" # Red
            active_speaker = "meera"
            
        # 3. Character kinematic parameters
        # Karan (waist up at x=340, y=880)
        karan_eyebrow = 16.0 if active_speaker == "karan" else -4.0
        karan_mouth_h = 16.0 * abs(math.sin(t * 14.0)) if active_speaker == "karan" else 3.0
        karan_blink = 1.0 if (30 <= f <= 33 or 90 <= f <= 93) else 0.0
        
        # Meera (waist up at x=740, y=880)
        meera_eyebrow = -18.0
        meera_mouth_h = 18.0 * abs(math.sin(t * 16.0)) if active_speaker == "meera" else 2.0
        meera_blink = 1.0 if (45 <= f <= 48 or 110 <= f <= 113) else 0.0
        meera_arm_angle = -35.0 + 8.0 * math.sin(t * 8.0) if active_speaker == "meera" else -15.0

        # Subtitles SVG
        sub_svg = get_karaoke_svg(t)
        
        svg = f"""<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#000000" flood-opacity="0.25"/>
            </filter>
          </defs>

          <!-- TIER 0: Explicit Notebook Grid Background -->
          <rect width="1080" height="1920" fill="#f6f2e9"/>
          {GRID_SVG}

          <!-- TIER 1: Top Retention Progress Bar & Channel Badge -->
          <g transform="translate(160, 100)">
            <!-- Progress Track -->
            <rect x="0" y="0" width="760" height="18" rx="9" fill="#ffffff" stroke="#000000" stroke-width="3"/>
            <rect x="0" y="0" width="{bar_fill_w}" height="18" rx="9" fill="#ef4444"/>
            <!-- Channel Series Pill -->
            <rect x="140" y="38" width="480" height="54" rx="27" fill="#facc15" stroke="#000000" stroke-width="4"/>
            <text x="380" y="74" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="900" fill="#000000" text-anchor="middle">MASTER AI • KARAN AUR MEERA</text>
          </g>

          <!-- TIER 2 & 3: Centered Focal Stage Card with Drop Shadow -->
          <g filter="url(#cardShadow)">
            <!-- Main Stage Card -->
            <rect x="70" y="270" width="940" height="1180" rx="42" fill="#fffdfa" stroke="#0c0a09" stroke-width="10"/>

            <!-- Clock Prop in Background -->
            <circle cx="540" cy="540" r="110" fill="#ffffff" stroke="#000000" stroke-width="6"/>
            <!-- Clock Ticks -->
            <line x1="540" y1="440" x2="540" y2="455" stroke="#000000" stroke-width="4"/>
            <line x1="540" y1="625" x2="540" y2="640" stroke="#000000" stroke-width="4"/>
            <line x1="440" y1="540" x2="455" y2="540" stroke="#000000" stroke-width="4"/>
            <line x1="625" y1="540" x2="640" y2="540" stroke="#000000" stroke-width="4"/>
            <!-- Clock Hands -->
            <line x1="540" y1="540" x2="540" y2="480" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
            <line x1="540" y1="540" x2="590" y2="520" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
            <circle cx="540" cy="540" r="8" fill="#000000"/>

            <!-- Floor Baseline -->
            <line x1="70" y1="1240" x2="1010" y2="1240" stroke="#000000" stroke-width="6"/>

            <!-- CHARACTER 1: KARAN (Waist-Up Rig with Correct Z-Index) -->
            <g transform="translate(340, 880)">
              <!-- Legs & Trousers -->
              <rect x="-42" y="200" width="36" height="160" rx="10" fill="#d6c7a1" stroke="#000000" stroke-width="5"/>
              <rect x="6" y="200" width="36" height="160" rx="10" fill="#d6c7a1" stroke="#000000" stroke-width="5"/>
              <ellipse cx="-24" cy="360" rx="25" ry="12" fill="#5c3a21" stroke="#000000" stroke-width="4"/>
              <ellipse cx="24" cy="360" rx="25" ry="12" fill="#5c3a21" stroke="#000000" stroke-width="4"/>

              <!-- Torso, Shirt & Blue Vest -->
              <rect x="-65" y="50" width="130" height="160" rx="16" fill="#ffffff" stroke="#000000" stroke-width="5"/>
              <path d="M -65 50 L -25 50 L -15 210 L -65 210 Z" fill="#1e3a8a" stroke="#000000" stroke-width="5"/>
              <path d="M 65 50 L 25 50 L 15 210 L 65 210 Z" fill="#1e3a8a" stroke="#000000" stroke-width="5"/>

              <!-- Left Arm holding blue phone -->
              <path d="M -65 70 Q -110 130 -80 180" fill="none" stroke="#ffffff" stroke-width="26" stroke-linecap="round"/>
              <rect x="-110" y="160" width="55" height="85" rx="8" fill="#1e293b" stroke="#000000" stroke-width="4"/>
              <rect x="-105" y="166" width="45" height="73" rx="4" fill="#38bdf8"/>

              <!-- Right Arm -->
              <path d="M 65 70 Q 110 140 80 190" fill="none" stroke="#ffffff" stroke-width="26" stroke-linecap="round"/>

              <!-- Head & Neck -->
              <rect x="-16" y="25" width="32" height="30" fill="#fde047" stroke="#000000" stroke-width="4"/>
              
              <!-- Back Hair -->
              <ellipse cx="0" cy="-45" rx="60" ry="60" fill="#451a03" stroke="#000000" stroke-width="5"/>
              
              <!-- Facial Base (Skin) -->
              <ellipse cx="0" cy="-35" rx="52" ry="58" fill="#fed7aa" stroke="#000000" stroke-width="5"/>
              
              <!-- Beard Contour -->
              <path d="M -48 -20 Q -50 25 0 28 Q 50 25 48 -20 Q 40 3 0 10 Q -40 3 -48 -20 Z" fill="#451a03"/>

              <!-- Front Top Hair Bangs -->
              <path d="M -52 -55 Q 0 -95 52 -55 Q 40 -35 0 -45 Q -40 -35 -52 -55 Z" fill="#451a03"/>

              <!-- Articulated Eyebrows -->
              <line x1="-38" y1="-50" x2="-14" y2="{-50 + karan_eyebrow * 0.4:.1f}" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
              <line x1="38" y1="-50" x2="14" y2="{-50 + karan_eyebrow * 0.4:.1f}" stroke="#000000" stroke-width="5" stroke-linecap="round"/>

              <!-- Eyes & Pupils -->
              <ellipse cx="-25" cy="-32" rx="12" ry="{max(1.0, 12.0 * (1.0 - karan_blink)):.1f}" fill="#ffffff" stroke="#000000" stroke-width="3"/>
              <ellipse cx="25" cy="-32" rx="12" ry="{max(1.0, 12.0 * (1.0 - karan_blink)):.1f}" fill="#ffffff" stroke="#000000" stroke-width="3"/>
              <circle cx="-25" cy="-32" r="5" fill="#000000"/>
              <circle cx="25" cy="-32" r="5" fill="#000000"/>

              <!-- Animated Mouth -->
              <ellipse cx="0" cy="5" rx="10" ry="{karan_mouth_h:.1f}" fill="#991b1b" stroke="#000000" stroke-width="2"/>
            </g>

            <!-- CHARACTER 2: MEERA (Waist-Up Rig) -->
            <g transform="translate(740, 880)">
              <!-- Charcoal Pants & Shoes -->
              <rect x="-35" y="200" width="30" height="160" rx="8" fill="#1f2937" stroke="#000000" stroke-width="5"/>
              <rect x="5" y="200" width="30" height="160" rx="8" fill="#1f2937" stroke="#000000" stroke-width="5"/>
              <ellipse cx="-20" cy="360" rx="22" ry="10" fill="#0c0a09"/>
              <ellipse cx="20" cy="360" rx="22" ry="10" fill="#0c0a09"/>

              <!-- Emerald Green Top -->
              <rect x="-55" y="55" width="110" height="155" rx="14" fill="#047857" stroke="#000000" stroke-width="5"/>

              <!-- Pointing Arm Gesture -->
              <g transform="rotate({meera_arm_angle:.1f}, -55, 75)">
                <path d="M -55 75 L -120 120" stroke="#047857" stroke-width="22" stroke-linecap="round"/>
                <circle cx="-120" cy="120" r="10" fill="#fed7aa"/>
                <line x1="-120" y1="120" x2="-155" y2="120" stroke="#fed7aa" stroke-width="10" stroke-linecap="round"/>
              </g>

              <!-- Head & Neck -->
              <rect x="-14" y="28" width="28" height="30" fill="#fed7aa" stroke="#000000" stroke-width="3"/>
              
              <!-- Hair Bun Top -->
              <circle cx="0" cy="-95" r="28" fill="#18181b" stroke="#000000" stroke-width="4"/>
              
              <!-- Back Hair -->
              <ellipse cx="0" cy="-40" rx="55" ry="55" fill="#18181b" stroke="#000000" stroke-width="5"/>

              <!-- Face Skin -->
              <ellipse cx="0" cy="-32" rx="48" ry="54" fill="#fed7aa" stroke="#000000" stroke-width="4"/>

              <!-- Front Hair Frame -->
              <path d="M -50 -45 Q 0 -85 50 -45 Q 45 -20 30 -30 Q 0 -40 -30 -30 Q -45 -20 -50 -45 Z" fill="#18181b"/>

              <!-- Red Bindi -->
              <circle cx="0" cy="-42" r="4" fill="#dc2626"/>

              <!-- Angry V Eyebrows -->
              <line x1="-35" y1="-42" x2="-12" y2="-52" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
              <line x1="35" y1="-42" x2="12" y2="-52" stroke="#000000" stroke-width="5" stroke-linecap="round"/>

              <!-- Eyes & Pupils -->
              <ellipse cx="-22" cy="-30" rx="11" ry="{max(1.0, 10.0 * (1.0 - meera_blink)):.1f}" fill="#ffffff" stroke="#000000" stroke-width="3"/>
              <ellipse cx="22" cy="-30" rx="11" ry="{max(1.0, 10.0 * (1.0 - meera_blink)):.1f}" fill="#ffffff" stroke="#000000" stroke-width="3"/>
              <circle cx="-20" cy="-30" r="5" fill="#000000"/>
              <circle cx="20" cy="-30" r="5" fill="#000000"/>

              <!-- Talking Mouth -->
              <ellipse cx="0" cy="10" rx="10" ry="{meera_mouth_h:.1f}" fill="#991b1b" stroke="#000000" stroke-width="2"/>
            </g>

            <!-- DYNAMIC TOPIC PILL (Overlapping Card Top) -->
            <g transform="translate(540, 260)">
              <rect x="-240" y="-34" width="480" height="68" rx="20" fill="{topic_bg}" stroke="#000000" stroke-width="6"/>
              <text x="0" y="10" font-family="'Segoe UI', sans-serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">{topic_text}</text>
            </g>
          </g>

          <!-- TIER 4: Dynamic Karaoke Subtitles (Lower Third) -->
          {sub_svg}
        </svg>"""

        doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")
        pix = doc[0].get_pixmap(dpi=72)
        pipe.stdin.write(pix.samples)

    pipe.stdin.close()
    pipe.wait()
    print(f"SUCCESS: Rendered Polished Technical Validation Video to: {OUT_MP4}")
    print(f"File size: {os.path.getsize(OUT_MP4):,} bytes")

if __name__ == "__main__":
    render_validation_video()
