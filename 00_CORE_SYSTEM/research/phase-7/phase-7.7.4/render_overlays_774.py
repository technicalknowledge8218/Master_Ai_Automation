"""
render_overlays_774.py
======================
Renders 1920x1080 transparent Devanagari text overlay badges and title card
using Google Chrome's HarfBuzz font shaping engine with Noto Sans Devanagari.
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\overlays_1080p"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

BADGES = [
    (
        "badge_scene_01.png",
        "आर्यन",
        "#0284c7",
        "दस मिनट... और पूरा शहर ट्रैफ़िक में डूबा है! पर ये ऑर्डर कैंसल नहीं होगा!"
    ),
    (
        "badge_scene_02.png",
        "विक्रम",
        "#f97316",
        "आर्यन, गरम है! संभल के ले जाना, किसी का ख़ास ऑर्डर है!"
    ),
    (
        "badge_scene_03.png",
        "आर्यन",
        "#0284c7",
        "चिंता मत करो शेफ़! घड़ी टिक रही है, और मैं उड़ रहा हूँ!"
    ),
    (
        "badge_scene_04.png",
        "आर्यन",
        "#0284c7",
        "सिर्फ़ तीन मिनट बचे हैं... रास्ता निकालना ही पड़ेगा!"
    ),
    (
        "badge_scene_06.png",
        "आर्यन",
        "#0284c7",
        "पहुंच गया! ठीक दो सेकंड पहले... अस्पताल का गेट!"
    ),
    (
        "badge_scene_07.png",
        "डॉ. अनन्या",
        "#059669",
        "माँ, तुम्हें याद था?! ड्यूटी के बाद... ये सबसे प्यारा सरप्राइज़ है!"
    ),
    (
        "badge_scene_08.png",
        "आर्यन",
        "#0284c7",
        "हैप्पी बर्थडे डॉक्टर साहिबा! आपकी मुस्कान ही जीत है!"
    ),
]

def render_badge(filename, speaker, color, text):
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Noto+Sans+Devanagari:wght@600;700;800&display=swap');
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 0;
    width: 1920px; height: 1080px; overflow: hidden;
    background: transparent;
    font-family: 'Noto Sans Devanagari', sans-serif;
    position: relative;
  }}
  .badge-container {{
    position: absolute;
    bottom: 55px;
    left: 120px;
    right: 120px;
    background: rgba(10, 15, 29, 0.92);
    border: 2px solid {color};
    border-radius: 18px;
    padding: 16px 36px;
    display: flex;
    align-items: center;
    gap: 28px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(8px);
  }}
  .speaker-pill {{
    background: {color};
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
    padding: 8px 24px;
    border-radius: 30px;
    letter-spacing: 0.5px;
    white-space: nowrap;
    text-shadow: 0 1px 2px rgba(0,0,0,0.4);
  }}
  .dialogue-text {{
    color: #f8fafc;
    font-size: 30px;
    font-weight: 700;
    line-height: 1.35;
    letter-spacing: 0.2px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
  }}
</style>
</head>
<body>
  <div class="badge-container">
    <div class="speaker-pill">{speaker}</div>
    <div class="dialogue-text">{text}</div>
  </div>
</body>
</html>"""

    out_path = os.path.join(OUTPUT_DIR, filename)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html)
        tmp = tf.name
    try:
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--default-background-color=00000000",
            "--window-size=1920,1080",
            f"--screenshot={out_path}",
            tmp
        ]
        subprocess.run(cmd, check=True)
        print(f"Rendered overlay: {filename}")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def render_outro_card():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Noto+Sans+Devanagari:wght@800;900&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 0;
    width: 1920px; height: 1080px; overflow: hidden;
    background: transparent;
    font-family: 'Montserrat', sans-serif;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
  }
  .card-box {
    background: rgba(10, 15, 29, 0.94);
    border: 3px solid #0284c7;
    border-radius: 28px;
    padding: 50px 80px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.85);
  }
  .title-hindi {
    font-family: 'Noto Sans Devanagari', sans-serif;
    font-size: 76px;
    font-weight: 900;
    color: #ffffff;
    margin: 0 0 10px 0;
    letter-spacing: 1px;
    text-shadow: 0 4px 16px rgba(2, 132, 199, 0.5);
  }
  .title-sub {
    font-size: 26px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 24px;
  }
  .credits {
    font-size: 18px;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 2px;
  }
</style>
</head>
<body>
  <div class="card-box">
    <div class="title-hindi">कोड रेड: डिलीवरी</div>
    <div class="title-sub">CODE RED: 10-MINUTE DELIVERY • A 60-SECOND INDIE FILM</div>
    <div class="credits">DIRECTED & EDITED BY MASTER AI • PHASE 7.7.4 ZERO BUDGET</div>
  </div>
</body>
</html>"""

    out_path = os.path.join(OUTPUT_DIR, "outro_title_card.png")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html)
        tmp = tf.name
    try:
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--default-background-color=00000000",
            "--window-size=1920,1080",
            f"--screenshot={out_path}",
            tmp
        ]
        subprocess.run(cmd, check=True)
        print("Rendered overlay: outro_title_card.png")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

if __name__ == "__main__":
    print("--- RENDERING 1080P DEVANAGARI TEXT OVERLAYS ---")
    for f, spk, col, txt in BADGES:
        render_badge(f, spk, col, txt)
    render_outro_card()
    print("All 1080p overlays rendered successfully!")
