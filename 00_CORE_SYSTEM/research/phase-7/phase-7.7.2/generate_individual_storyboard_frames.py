"""
generate_individual_storyboard_frames.py
========================================
Generates the 4 individual 1920x1080 Storyboard Keyframes for:
- frame_01.png: Beat 1 - The Confrontation & Napkin Slide
- frame_02.png: Beat 2 - The Unflinching Chai Sip
- frame_03.png: Beat 3 - The iPad Screen Reveal & Jaw Drop
- frame_04.png: Beat 4 - The Playful Wink & UPI Surrender
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2\storyboard"
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
            f"--screenshot={output_png}",
            temp_html
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not os.path.isfile(output_png):
            raise RuntimeError(f"Chrome screenshot failed: {res.stderr}")
        print(f"Generated: {output_png}")
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

# Frame 1
f1_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Noto+Sans+Devanagari:wght@700&display=swap');
  body { margin:0; background:#0b1329; width:1920px; height:1080px; overflow:hidden; font-family:'Montserrat',sans-serif; }
</style>
</head>
<body>
<svg width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a1128"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#bgGrad)"/>
  <!-- Mumbai rain window with colorful neon cafe bokeh -->
  <circle cx="350" cy="280" r="140" fill="#f43f5e" opacity="0.25"/>
  <circle cx="680" cy="220" r="100" fill="#38bdf8" opacity="0.2"/>
  <circle cx="950" cy="310" r="120" fill="#f59e0b" opacity="0.2"/>
  <text x="180" y="160" font-family="'Montserrat'" font-size="64" font-weight="800" fill="#f59e0b" opacity="0.5" letter-spacing="8">CHAI & CO. • MUMBAI</text>
  <!-- Modern Cafe Table -->
  <polygon points="0,820 1920,820 1920,1080 0,1080" fill="#292019"/>
  <line x1="0" y1="820" x2="1920" y2="820" stroke="#451a03" stroke-width="8"/>
  <!-- Vikram (Right) Leaning in with Cocky Smirk -->
  <path d="M1250 420 Q1450 360 1560 480 Q1580 620 1440 700 Q1220 640 1250 420 Z" fill="#fcd34d"/>
  <path d="M1270 540 Q1440 680 1540 540 L1520 600 Q1440 670 1290 600 Z" fill="#78350f" opacity="0.25"/>
  <!-- Glasses -->
  <rect x="1320" y="470" width="70" height="50" rx="8" fill="none" stroke="#78350f" stroke-width="7"/>
  <rect x="1410" y="470" width="70" height="50" rx="8" fill="none" stroke="#78350f" stroke-width="7"/>
  <line x1="1390" y1="495" x2="1410" y2="495" stroke="#78350f" stroke-width="7"/>
  <circle cx="1355" cy="495" r="8" fill="#1e1b4b"/>
  <circle cx="1445" cy="495" r="8" fill="#1e1b4b"/>
  <!-- Raised eyebrow & Smug grin -->
  <path d="M1315 445 L1385 440" stroke="#18181b" stroke-width="8" stroke-linecap="round"/>
  <path d="M1410 430 L1480 440" stroke="#18181b" stroke-width="9" stroke-linecap="round"/>
  <path d="M1340 610 Q1420 640 1500 595" stroke="#78350f" stroke-width="8" stroke-linecap="round" fill="none"/>
  <!-- Quiff hair -->
  <path d="M1230 430 C1210 280, 1550 270, 1530 430 C1550 470, 1530 520, 1500 550 C1460 380, 1380 320, 1260 360 Z" fill="#18181b"/>
  <!-- Bomber Jacket Arm sliding napkin forward -->
  <path d="M1180 580 L1020 740 L1220 780 Z" fill="#047857"/>
  <!-- Napkin with concept sketch sliding across table -->
  <polygon points="900,760 1060,740 1110,810 950,830" fill="#f8fafc" stroke="#94a3b8" stroke-width="3"/>
  <path d="M940,780 L1030,765" stroke="#ef4444" stroke-width="5"/>
  <!-- Aisha seated opposite, listening coolly -->
  <path d="M420 540 Q540 480 620 580 Q580 720 440 720 Z" fill="#eab308"/>
  <path d="M460 460 Q560 410 620 500 Q580 610 460 610 Z" fill="#1e1b4b"/>
  <!-- Title Badge -->
  <rect x="80" y="930" width="700" height="80" rx="10" fill="rgba(15,23,42,0.92)" stroke="#f59e0b" stroke-width="3"/>
  <text x="120" y="980" font-family="'Noto Sans Devanagari'" font-size="28" font-weight="700" fill="#ffffff">विक्रम: "बुरा मत मानना, लेकिन डील फाइनल है!"</text>
</svg>
</body>
</html>"""
render_html_to_png(f1_html, os.path.join(OUTPUT_DIR, "frame_01.png"))

# Frame 2
f2_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Noto+Sans+Devanagari:wght@700&display=swap');
  body { margin:0; background:#101826; width:1920px; height:1080px; overflow:hidden; font-family:'Montserrat',sans-serif; }
</style>
</head>
<body>
<svg width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#101826"/>
  <!-- Warm cafe lighting & ambient neon bokeh -->
  <circle cx="1500" cy="300" r="180" fill="#f59e0b" opacity="0.22"/>
  <circle cx="400" cy="350" r="140" fill="#10b981" opacity="0.18"/>
  <!-- Aisha Close-Up -->
  <path d="M720 280 Q960 180 1180 290 Q1220 540 960 680 Q700 540 720 280 Z" fill="#fed7aa"/>
  <!-- Almond Eyes, cat-eye wings, cool confident gaze -->
  <ellipse cx="860" cy="410" rx="36" ry="18" fill="#ffffff"/>
  <circle cx="865" cy="410" r="14" fill="#451a03"/>
  <circle cx="860" cy="405" r="4.5" fill="#ffffff"/>
  <ellipse cx="1060" cy="410" rx="36" ry="18" fill="#ffffff"/>
  <circle cx="1055" cy="410" r="14" fill="#451a03"/>
  <circle cx="1050" cy="405" r="4.5" fill="#ffffff"/>
  <!-- Winged eyeliner -->
  <path d="M825 400 Q865 380 905 400 L915 390" stroke="#0f172a" stroke-width="8" stroke-linecap="round" fill="none"/>
  <path d="M1020 400 Q1060 380 1100 400 L1110 390" stroke="#0f172a" stroke-width="8" stroke-linecap="round" fill="none"/>
  <!-- Nose bridge -->
  <path d="M950 430 L965 480 L940 488" stroke="#ea580c" stroke-width="6" stroke-linecap="round" fill="none"/>
  <!-- Knowing smirk taking a sip of cutting chai -->
  <path d="M890 560 Q960 580 1025 545" stroke="#be123c" stroke-width="10" stroke-linecap="round" fill="none"/>
  <!-- Cutting Chai Glass held by hand at lips -->
  <path d="M920 530 L1020 530 L1000 680 L940 680 Z" fill="#f59e0b" stroke="#ffffff" stroke-width="6"/>
  <!-- Delicate steam curling up -->
  <path d="M960 510 Q980 460 950 410 Q980 360 960 310" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.8"/>
  <!-- Hair: Glossy asymmetrical modern bob with violet sheen -->
  <path d="M680 290 C660 120, 1200 120, 1180 290 C1220 500, 1220 680, 1080 750 C1060 550, 1010 390, 1010 340 C910 290, 770 380, 720 470 Z" fill="#1e1b4b"/>
  <!-- Silver Ear Cuff -->
  <circle cx="690" cy="420" r="12" fill="#e2e8f0"/>
  <!-- Trench Coat & Turtleneck -->
  <path d="M580 780 L760 700 L960 780 L1160 700 L1340 780 L1400 1080 L520 1080 Z" fill="#eab308"/>
  <path d="M820 680 L960 840 L1100 680 Z" fill="#18181b"/>
  <!-- Title Badge -->
  <rect x="80" y="930" width="700" height="80" rx="10" fill="rgba(15,23,42,0.92)" stroke="#10b981" stroke-width="3"/>
  <text x="120" y="980" font-family="'Noto Sans Devanagari'" font-size="28" font-weight="700" fill="#ffffff">आयशा: "अच्छा? ज़रा इनबॉक्स चेक कर लो, विक्रम।"</text>
</svg>
</body>
</html>"""
render_html_to_png(f2_html, os.path.join(OUTPUT_DIR, "frame_02.png"))

# Frame 3
f3_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Noto+Sans+Devanagari:wght@700&display=swap');
  body { margin:0; background:#0d1422; width:1920px; height:1080px; overflow:hidden; font-family:'Montserrat',sans-serif; }
</style>
</head>
<body>
<svg width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#0d1422"/>
  <polygon points="0,780 1920,780 1920,1080 0,1080" fill="#292019"/>
  <!-- Glowing iPad Screen spun towards Vikram -->
  <rect x="420" y="280" width="580" height="420" rx="20" fill="#1e293b" stroke="#38bdf8" stroke-width="8"/>
  <rect x="450" y="310" width="520" height="360" rx="12" fill="#0f172a"/>
  <text x="480" y="375" font-family="'Montserrat'" font-size="26" font-weight="800" fill="#38bdf8">APEX CORP • DESIGN APPROVAL</text>
  <text x="480" y="440" font-family="'Montserrat'" font-size="34" font-weight="800" fill="#ffffff">"LOVED AISHA'S PITCH!"</text>
  <text x="480" y="500" font-family="'Montserrat'" font-size="24" font-weight="600" fill="#94a3b8">Appointed as Project Lead & Director</text>
  <text x="480" y="555" font-family="'Montserrat'" font-size="22" font-weight="600" fill="#f59e0b">Vikram: Assigned to assist as Junior Lead</text>
  <circle cx="910" cy="610" r="22" fill="#10b981"/>
  <!-- Vikram Jaw-Drop Shock (Right) -->
  <path d="M1280 260 Q1480 190 1590 310 Q1600 520 1460 620 Q1240 550 1280 260 Z" fill="#fcd34d"/>
  <!-- Huge Shocked Eyes behind askew glasses -->
  <rect x="1330" y="320" width="75" height="60" rx="8" fill="none" stroke="#78350f" stroke-width="7"/>
  <rect x="1440" y="320" width="75" height="60" rx="8" fill="none" stroke="#78350f" stroke-width="7"/>
  <circle cx="1368" cy="350" r="15" fill="#1e1b4b"/>
  <circle cx="1478" cy="350" r="15" fill="#1e1b4b"/>
  <circle cx="1360" cy="342" r="5" fill="#ffffff"/>
  <circle cx="1470" cy="342" r="5" fill="#ffffff"/>
  <!-- Shocked High Eyebrows -->
  <path d="M1320 280 Q1368 250 1416 280" stroke="#18181b" stroke-width="7" fill="none"/>
  <path d="M1430 280 Q1478 250 1526 280" stroke="#18181b" stroke-width="7" fill="none"/>
  <!-- Open 'O' Dropped Jaw Mouth -->
  <ellipse cx="1430" cy="510" rx="35" ry="50" fill="#451a03"/>
  <!-- Giant cold sweat drop on brow -->
  <path d="M1520 280 Q1540 310 1520 330 Q1500 310 1520 280 Z" fill="#38bdf8"/>
  <!-- Parle-G Biscuit falling into cutting tea glass with splash! -->
  <ellipse cx="1180" cy="740" rx="35" ry="18" fill="#d97706"/>
  <circle cx="1150" cy="710" r="8" fill="#f59e0b"/>
  <circle cx="1200" cy="700" r="6" fill="#f59e0b"/>
  <!-- Title Badge -->
  <rect x="80" y="930" width="750" height="80" rx="10" fill="rgba(15,23,42,0.92)" stroke="#ef4444" stroke-width="3"/>
  <text x="120" y="980" font-family="'Noto Sans Devanagari'" font-size="28" font-weight="700" fill="#ffffff">विक्रम: "व्हाट?! 'आयशा इज़ द न्यू प्रोजेक्ट हेड'...?!"</text>
</svg>
</body>
</html>"""
render_html_to_png(f3_html, os.path.join(OUTPUT_DIR, "frame_03.png"))

# Frame 4
f4_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Noto+Sans+Devanagari:wght@700&display=swap');
  body { margin:0; background:#0a0f1d; width:1920px; height:1080px; overflow:hidden; font-family:'Montserrat',sans-serif; }
</style>
</head>
<body>
<svg width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#0a0f1d"/>
  <!-- Wet city pavement outside with vibrant pink and cyan neon puddles -->
  <polygon points="0,800 1920,800 1920,1080 0,1080" fill="#18131d"/>
  <path d="M200 890 Q500 850 800 890" stroke="#f43f5e" stroke-width="12" opacity="0.45" stroke-linecap="round"/>
  <path d="M1000 900 Q1300 860 1600 900" stroke="#38bdf8" stroke-width="12" opacity="0.45" stroke-linecap="round"/>
  <!-- Aisha Winking Joyfully with Cutting Chai Glass (Left) -->
  <path d="M480 320 Q660 240 780 330 Q800 500 660 600 Q480 520 480 320 Z" fill="#fed7aa"/>
  <!-- Left Eye open, Right Eye Winking! -->
  <ellipse cx="570" cy="400" rx="30" ry="16" fill="#ffffff"/>
  <circle cx="575" cy="400" r="12" fill="#451a03"/>
  <circle cx="570" cy="395" r="4" fill="#ffffff"/>
  <path d="M640 405 Q675 425 710 405" stroke="#0f172a" stroke-width="9" stroke-linecap="round" fill="none"/>
  <!-- Broad joyful smile showing teeth -->
  <path d="M570 490 Q650 560 730 490 Z" fill="#be123c"/>
  <path d="M585 495 Q650 520 715 495 Z" fill="#ffffff"/>
  <!-- Hand raising cutting glass in toast -->
  <path d="M820 460 L890 460 L875 580 L835 580 Z" fill="#f59e0b" stroke="#ffffff" stroke-width="5"/>
  <!-- Vikram with Sheepish Smile pulling out phone/wallet (Right) -->
  <path d="M1300 360 Q1460 300 1540 400 Q1520 540 1380 610 Z" fill="#fcd34d"/>
  <rect x="1330" y="410" width="55" height="40" rx="6" fill="none" stroke="#78350f" stroke-width="6"/>
  <rect x="1410" y="410" width="55" height="40" rx="6" fill="none" stroke="#78350f" stroke-width="6"/>
  <!-- Squinting sheepish eyes -->
  <path d="M1340 430 Q1358 445 1375 430" stroke="#18181b" stroke-width="6" fill="none"/>
  <path d="M1420 430 Q1438 445 1455 430" stroke="#18181b" stroke-width="6" fill="none"/>
  <!-- Sheepish smile -->
  <path d="M1360 520 Q1410 545 1460 515" stroke="#78350f" stroke-width="7" stroke-linecap="round" fill="none"/>
  <!-- Phone in hand with UPI payment screen -->
  <rect x="1220" y="580" width="80" height="130" rx="10" fill="#1e293b" stroke="#10b981" stroke-width="4"/>
  <rect x="1235" y="605" width="50" height="80" rx="4" fill="#0f172a"/>
  <circle cx="1260" cy="640" r="10" fill="#10b981"/>
  <!-- Title Badge -->
  <rect x="80" y="930" width="750" height="80" rx="10" fill="rgba(15,23,42,0.92)" stroke="#f59e0b" stroke-width="3"/>
  <text x="120" y="980" font-family="'Noto Sans Devanagari'" font-size="28" font-weight="700" fill="#ffffff">आयशा: "चाय के पैसे तुम दोगे, पार्टनर!"</text>
</svg>
</body>
</html>"""
render_html_to_png(f4_html, os.path.join(OUTPUT_DIR, "frame_04.png"))

print("All 4 Storyboard Frames Rendered Successfully!")
