"""
render_text_overlays_772.py
===========================
Renders HarfBuzz-shaped Devanagari 1080p subtitle cards and chapter badges
for "चाय और चाल" (The Chai Gambit) using Chromium (Blink/HarfBuzz/Skia).
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2\overlays_1080p"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content: str, output_png: str):
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

badges = [
    {
        "id": "badge_beat_01",
        "speaker": "विक्रम",
        "role": "आर्ट डायरेक्टर",
        "dialogue": "बुरा मत मानना आयशा, लेकिन तुम्हारा पिच मैंने थोड़ा 'अपग्रेड' कर दिया... डील फाइनल है!",
        "accent": "#047857",
        "speaker_color": "#10b981"
    },
    {
        "id": "badge_beat_02",
        "speaker": "आयशा",
        "role": "सीनियर यूआई/यूएक्स डिज़ाइनर",
        "dialogue": "अच्छा? ज़रा अपना इनबॉक्स चेक कर लो, विक्रम।",
        "accent": "#ca8a04",
        "speaker_color": "#facc15"
    },
    {
        "id": "badge_beat_03",
        "speaker": "विक्रम",
        "role": "स्तब्ध",
        "dialogue": "व्हाट?! 'आयशा इज़ द न्यू प्रोजेक्ट हेड'...? लेकिन कैसे?!",
        "accent": "#ef4444",
        "speaker_color": "#f87171"
    },
    {
        "id": "badge_beat_04",
        "speaker": "आयशा",
        "role": "प्रोजेक्ट हेड",
        "dialogue": "हाँ... और इस जीत की चाय के पैसे तुम दोगे, पार्टनर!",
        "accent": "#f59e0b",
        "speaker_color": "#fbbf24"
    }
]

for b in badges:
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  body {{
    margin: 0; padding: 0; background: transparent;
    width: 1920px; height: 1080px; position: relative;
    font-family: 'Noto Sans Devanagari', 'Montserrat', sans-serif;
  }}
  .card {{
    position: absolute; bottom: 75px; left: 80px;
    display: inline-flex; align-items: center;
    background: rgba(15, 20, 32, 0.92);
    border: 2px solid {b['accent']};
    border-left: 10px solid {b['accent']};
    border-radius: 10px;
    padding: 16px 32px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.65);
    max-width: 1400px;
  }}
  .speaker-box {{
    display: flex; flex-direction: column; margin-right: 24px;
    border-right: 2px solid rgba(255, 255, 255, 0.18);
    padding-right: 24px; min-width: 130px;
  }}
  .name {{
    font-size: 24px; font-weight: 700; color: {b['speaker_color']};
  }}
  .role {{
    font-size: 13px; font-weight: 600; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px;
  }}
  .dialogue {{
    font-size: 26px; font-weight: 600; color: #ffffff;
    line-height: 1.4;
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="speaker-box">
      <div class="name">{b['speaker']}</div>
      <div class="role">{b['role']}</div>
    </div>
    <div class="dialogue">"{b['dialogue']}"</div>
  </div>
</body>
</html>"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, f"{b['id']}.png"))

# Outro Title Card (1920x1080)
outro_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&family=Noto+Sans+Devanagari:wght@400;700;800&display=swap');
  body {
    margin: 0; padding: 0; background: transparent;
    width: 1920px; height: 1080px;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    font-family: 'Noto Sans Devanagari', 'Montserrat', sans-serif;
  }
  .card {
    text-align: center;
    background: rgba(15, 20, 32, 0.90);
    border: 2px solid rgba(245, 158, 11, 0.6);
    border-radius: 18px;
    padding: 45px 80px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75);
  }
  .sub {
    font-size: 20px; font-weight: 700; color: #f59e0b;
    letter-spacing: 4px; text-transform: uppercase; margin-bottom: 12px;
  }
  .title {
    font-size: 72px; font-weight: 800; color: #ffffff;
    text-shadow: 0 4px 25px rgba(245, 158, 11, 0.5);
    margin-bottom: 15px;
  }
  .tagline {
    font-size: 24px; font-weight: 600; color: #cbd5e1;
    max-width: 750px; line-height: 1.5;
  }
</style>
</head>
<body>
  <div class="card">
    <div class="sub">मास्टर एआई स्टूडियो प्रस्तुत करता है</div>
    <div class="title">चाय और चाल</div>
    <div class="tagline">"काम की चोरी कभी जीत नहीं दिलाती... चाय के पैसे तो देने ही पड़ते हैं!"</div>
  </div>
</body>
</html>"""
render_html_to_png(outro_html, os.path.join(OUTPUT_DIR, "outro_title_card.png"))
print("All 1080p Overlays Rendered Successfully!")
