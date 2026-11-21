"""
render_1080p_text_overlays.py
=============================
Renders 100% typographically correct, HarfBuzz-shaped Devanagari text overlays
at native 1920x1080 Full HD resolution for Master AI Phase 7.7.1.
Uses Chromium (Google Chrome / Blink / HarfBuzz / Skia).
"""

import os
import sys
import tempfile
import subprocess

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.1"
OVERLAYS_DIR = os.path.join(OUTPUT_DIR, "overlays_1080p")
os.makedirs(OVERLAYS_DIR, exist_ok=True)

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png_1080p(html_content: str, output_png: str):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_content)
        temp_html = tf.name

    try:
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1920,1080",
            "--default-background-color=00000000",
            f"--screenshot={output_png}",
            temp_html
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not os.path.isfile(output_png):
            raise RuntimeError(f"Chrome screenshot failed: {res.stderr}")
        print(f"Rendered: {output_png}")
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

# 1. Lower Third Badges (1920x1080)
badges = [
    {
        "id": "badge_scene_01",
        "part": "दृश्य १",
        "title": "खामोश धुन — उदास बारिश और उलझन",
        "color": "#38bdf8"
    },
    {
        "id": "badge_scene_02",
        "part": "दृश्य २",
        "title": "लियो का साथ — बेज़ुबान दोस्त का हौसला",
        "color": "#f59e0b"
    },
    {
        "id": "badge_scene_03",
        "part": "दृश्य ३",
        "title": "पहला सुर — खामोशी को चीरती एक नई धुन",
        "color": "#10b981"
    },
    {
        "id": "badge_scene_04",
        "part": "दृश्य ४",
        "title": "नई सुबह — बादलों के पार सूरज की रोशनी",
        "color": "#fbbf24"
    }
]

for b in badges:
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  body {{
    margin: 0;
    padding: 0;
    background: transparent;
    width: 1920px;
    height: 1080px;
    position: relative;
    font-family: 'Noto Sans Devanagari', 'Nirmala UI', sans-serif;
  }}
  .badge {{
    position: absolute;
    bottom: 80px;
    left: 90px;
    display: inline-flex;
    align-items: center;
    background: rgba(15, 23, 42, 0.90);
    border: 2px solid {b['color']};
    border-left: 8px solid {b['color']};
    border-radius: 8px;
    padding: 14px 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  }}
  .part {{
    font-size: 24px;
    font-weight: 700;
    color: {b['color']};
    margin-right: 18px;
    letter-spacing: 0.5px;
  }}
  .divider {{
    width: 2px;
    height: 28px;
    background: rgba(255, 255, 255, 0.2);
    margin-right: 18px;
  }}
  .text {{
    font-size: 26px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.3px;
  }}
</style>
</head>
<body>
  <div class="badge">
    <div class="part">{b['part']}</div>
    <div class="divider"></div>
    <div class="text">{b['title']}</div>
  </div>
</body>
</html>"""
    out_path = os.path.join(OVERLAYS_DIR, f"{b['id']}.png")
    render_html_to_png_1080p(html, out_path)

# 2. Outro Title Card (1920x1080)
outro_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700;800&display=swap');
  body {
    margin: 0;
    padding: 0;
    background: transparent;
    width: 1920px;
    height: 1080px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: 'Noto Sans Devanagari', 'Nirmala UI', sans-serif;
  }
  .card {
    text-align: center;
    background: rgba(15, 23, 42, 0.85);
    border: 2px solid rgba(245, 158, 11, 0.5);
    border-radius: 16px;
    padding: 40px 70px;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.7);
  }
  .sub {
    font-size: 22px;
    font-weight: 600;
    color: #fbbf24;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  .title {
    font-size: 64px;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
    margin-bottom: 16px;
  }
  .tagline {
    font-size: 24px;
    font-weight: 400;
    color: #94a3b8;
    max-width: 700px;
    line-height: 1.5;
  }
</style>
</head>
<body>
  <div class="card">
    <div class="sub">मास्टर एआई स्टूडियो</div>
    <div class="title">पहली धुन</div>
    <div class="tagline">जब सपने रुकने लगें, तो एक सच्चा दोस्त ही जीने की धुन वापस लाता है।</div>
  </div>
</body>
</html>"""
outro_path = os.path.join(OVERLAYS_DIR, "outro_title_card.png")
render_html_to_png_1080p(outro_html, outro_path)
print("All 1080p HarfBuzz Devanagari Overlays Rendered Successfully!")
