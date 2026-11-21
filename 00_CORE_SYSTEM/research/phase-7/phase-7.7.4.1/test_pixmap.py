import fitz
import os, sys, math

ENGINE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\engine"
sys.path.append(ENGINE_DIR)
from motion_director import Easing, Camera2D, ParticleSystem

cam = Camera2D()
for f in range(10):
    t = f / 24.0
    zoom = 1.0 + 0.18 * Easing.ease_out_quad(f / 180.0)
    cam.trigger_shake(t if t < 1.5 else (t % 0.8), intensity=4.0)
    screen_pulse = 0.5 + 0.5 * math.sin(2.0 * math.pi * 3.0 * t)
    glow_alpha = 0.2 + 0.25 * screen_pulse
    
    svg = f"""<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
      <rect width="1920" height="1080" fill="#090508"/>
      <g transform="translate(960, 540) scale({zoom}) translate(-960, -540)">
        <rect x="0" y="700" width="1920" height="380" fill="#0f172a"/>
        <line x1="200" y1="740" x2="1720" y2="740" stroke="#334155" stroke-width="28" stroke-linecap="round"/>
        <rect x="880" y="650" width="160" height="120" rx="16" fill="#1e293b" stroke="#475569" stroke-width="4"/>
        <g transform="translate({cam.shake_x}, {cam.shake_y})">
          <rect x="660" y="160" width="600" height="660" rx="36" fill="#0c070c" stroke="#dc2626" stroke-width="8"/>
          <rect x="680" y="180" width="560" height="620" rx="28" fill="rgba(239, 68, 68, {glow_alpha:.2f})"/>
          <rect x="710" y="210" width="500" height="65" rx="14" fill="#1e1014"/>
          <circle cx="750" cy="242" r="14" fill="#ef4444"/>
          <text x="780" y="250" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff">URGENT DELIVERY</text>
        </g>
      </g>
      {ParticleSystem.generate_rain_svg(f, count=25)}
    </svg>"""
    
    doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")
    page = doc[0]
    pix = page.get_pixmap(dpi=96)
    print(f"Frame {f}: rect={page.rect}, pix=({pix.width}, {pix.height}), origin=({pix.x}, {pix.y}), samples_len={len(pix.samples)}")
