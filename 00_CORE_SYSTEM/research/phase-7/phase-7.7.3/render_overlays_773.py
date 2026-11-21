"""
render_overlays_773.py
======================
Renders 1920x1080 transparent Devanagari text overlay badges and title card
using Google Chrome's HarfBuzz font shaping engine with Noto Sans Devanagari.

Outputs:
- badge_scene_01.png to badge_scene_08.png
- outro_title_card.png
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3\overlays_1080p"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

BADGES = [
    (
        "badge_scene_01.png",
        "कबीर",
        "#f97316",
        "अरे यार! सुबह के तीन बज रहे हैं और ये सर्वर फिर क्रैश हो गया?!"
    ),
    (
        "badge_scene_02.png",
        "मीरा",
        "#0284c7",
        "कबीर, सांस ले। कोई हैकर नहीं है। कॉफ़ी पी और शांत हो।"
    ),
    (
        "badge_scene_03.png",
        "कबीर",
        "#f97316",
        "नहीं मीरा! ये पक्का डीडीओएस अटैक है! मैं डेटाबेस फ़ॉर्मेट कर रहा हूँ!"
    ),
    (
        "badge_scene_04.png",
        "मीरा",
        "#0284c7",
        "हाथ हटा वहां से! रुक, ये क्या है? F5 और ESC की कंटीन्यूअस प्रेस?"
    ),
    (
        "badge_scene_05.png",
        "कबीर",
        "#f97316",
        "क्या मतलब?! मैंने तो कीबोर्ड छुआ भी नहीं!"
    ),
    (
        "badge_scene_06.png",
        "मीरा",
        "#0284c7",
        "तूने नहीं छुआ, लेकिन इस पर कुछ भारी रखा ज़रूर है!"
    ),
    (
        "badge_scene_07.png",
        "कबीर",
        "#f97316",
        "ये... ये भुजिया थी?! पूरा दिन भुजिया की वजह से बर्बाद हुआ?!"
    ),
    (
        "badge_scene_08.png",
        "मीरा",
        "#0284c7",
        "हाँ! तो हमारे सबसे बड़े इंटरनेशनल हैकर का नाम था... हल्दीराम की स्पेशल भुजिया!"
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
    border: 3px solid #f97316;
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
    text-shadow: 0 4px 16px rgba(249, 115, 22, 0.4);
  }
  .title-sub {
    font-size: 26px;
    font-weight: 800;
    color: #f97316;
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
    <div class="title-hindi">लास्ट बग</div>
    <div class="title-sub">THE LAST BUG • A 60-SECOND 2D ANIMATED SHORT</div>
    <div class="credits">MASTER AI AUTONOMOUS PRODUCTION ENGINE • PHASE 7.7.3</div>
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
