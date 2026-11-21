"""
render_storyboard_keyframes_773.py
==================================
Renders all 8 individual 1920x1080 keyframe stills into storyboard/
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3\storyboard"
os.makedirs(OUTPUT_DIR, exist_ok=True)
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

scenes = [
    ("scene_01_key.png", "BEAT 1: THE 3:00 AM RED ALERT", "0.0s – 7.5s", "#3b0707",
     """
     <rect x='560' y='180' width='800' height='480' rx='16' fill='#180606' stroke='#ef4444' stroke-width='6'/>
     <text x='960' y='320' font-family="'Montserrat'" font-size='38' font-weight='800' fill='#ef4444' text-anchor='middle'>FATAL SYSTEM CRASH</text>
     <text x='960' y='400' font-family="'Montserrat'" font-size='22' font-weight='600' fill='#fca5a5' text-anchor='middle'>THREAD 0x8F94: UNRESPONSIVE DEADLOCK</text>
     <circle cx='960' cy='620' r='120' fill='#fdba74'/>
     <path d='M830,550 Q880,480 960,490 Q1040,480 1090,550 Q960,450 830,550 Z' fill='#334155'/>
     <ellipse cx='910' cy='610' rx='20' ry='16' fill='#ffffff'/>
     <circle cx='910' cy='610' r='8' fill='#78350f'/>
     <ellipse cx='1010' cy='610' rx='20' ry='16' fill='#ffffff'/>
     <circle cx='1010' cy='610' r='8' fill='#78350f'/>
     <ellipse cx='960' cy='680' rx='28' ry='36' fill='#7f1d1d'/>
     <path d='M840,710 L890,570 M1080,710 L1030,570' stroke='#f97316' stroke-width='28' stroke-linecap='round'/>
     """,
     "कबीर: \"अरे यार! सुबह के तीन बज रहे हैं और ये सर्वर फिर क्रैश हो गया?!\""),

    ("scene_02_key.png", "BEAT 2: THE CONSPIRACY & COFFEE", "7.5s – 15.0s", "#0c1322",
     """
     <circle cx='550' cy='520' r='100' fill='#fdba74'/>
     <path d='M440,460 Q490,400 550,410 Q610,400 660,460 Z' fill='#334155'/>
     <ellipse cx='520' cy='510' rx='16' ry='14' fill='#ffffff'/><circle cx='520' cy='510' r='7' fill='#78350f'/>
     <ellipse cx='580' cy='510' rx='16' ry='14' fill='#ffffff'/><circle cx='580' cy='510' r='7' fill='#78350f'/>
     <path d='M525,565 Q550,545 575,565' stroke='#78350f' stroke-width='6' fill='none' stroke-linecap='round'/>
     <circle cx='1300' cy='480' r='90' fill='#fed7aa'/>
     <circle cx='1300' cy='360' r='45' fill='#1e293b'/>
     <circle cx='1260' cy='480' r='26' fill='none' stroke='#38bdf8' stroke-width='6'/>
     <circle cx='1340' cy='480' r='26' fill='none' stroke='#38bdf8' stroke-width='6'/>
     <line x1='1286' y1='480' x2='1314' y2='480' stroke='#38bdf8' stroke-width='5'/>
     <rect x='1150' y='600' width='55' height='75' rx='8' fill='#f8fafc' stroke='#cbd5e1' stroke-width='4'/>
     <path d='M1140,620 Q1120,635 1140,655' stroke='#cbd5e1' stroke-width='6' fill='none'/>
     """,
     "मीरा: \"कबीर, सांस ले। कोई हैकर नहीं है। कॉफ़ी पी और शांत हो।\""),

    ("scene_03_key.png", "BEAT 3: THE DESPERATE ESCALATION", "15.0s – 22.5s", "#1e1022",
     """
     <rect x='460' y='320' width='1000' height='300' rx='30' fill='#dc2626' stroke='#f87171' stroke-width='10'/>
     <text x='960' y='460' font-family=\"'Montserrat'\" font-size='56' font-weight='900' fill='#ffffff' text-anchor='middle'>FORMAT & PURGE DATABASE</text>
     <text x='960' y='530' font-family=\"'Montserrat'\" font-size='26' font-weight='700' fill='#fee2e2' text-anchor='middle'>WARNING: IRREVERSIBLE ACTION</text>
     <path d='M350,780 L520,560' stroke='#f97316' stroke-width='36' stroke-linecap='round'/>
     """,
     "कबीर: \"नहीं मीरा, ये पक्का डीडीओएस है! मैं डेटाबेस फ़ॉर्मेट कर रहा हूँ!\""),

    ("scene_04_key.png", "BEAT 4: INVESTIGATION & DISCOVERY", "22.5s – 30.0s", "#061a2b",
     """
     <circle cx='960' cy='420' r='130' fill='#fed7aa'/>
     <circle cx='905' cy='420' r='36' fill='none' stroke='#38bdf8' stroke-width='8'/>
     <circle cx='1015' cy='420' r='36' fill='none' stroke='#38bdf8' stroke-width='8'/>
     <line x1='941' y1='420' x2='979' y2='420' stroke='#38bdf8' stroke-width='6'/>
     <ellipse cx='905' cy='405' rx='14' ry='12' fill='#1e293b'/>
     <ellipse cx='1015' cy='405' rx='14' ry='12' fill='#1e293b'/>
     <rect x='480' y='640' width='960' height='260' rx='12' fill='#09131f' stroke='#0284c7' stroke-width='4'/>
     <text x='520' y='710' font-family=\"'Montserrat'\" font-size='22' font-weight='700' fill='#38bdf8'>DEBUG CONSOLE & INPUT EVENTS:</text>
     <text x='520' y='770' font-family=\"'Montserrat'\" font-size='26' font-weight='800' fill='#f59e0b'>KEY_DOWN: F5 (HELD 10,480,210 ms)</text>
     <text x='520' y='830' font-family=\"'Montserrat'\" font-size='26' font-weight='800' fill='#f59e0b'>KEY_DOWN: ESC (HELD 10,480,210 ms)</text>
     """,
     "मीरा: \"हाथ हटा वहां से! ...रुक, ये क्या है? F5 और ESC की कंटीन्यूअस प्रेस?\""),

    ("scene_05_key.png", "BEAT 5: THE PHYSICAL CLUE", "30.0s – 37.5s", "#131926",
     """
     <rect x='260' y='200' width='1400' height='680' rx='20' fill='#1e293b' stroke='#334155' stroke-width='6'/>
     <rect x='400' y='360' width='1120' height='360' rx='16' fill='#0f172a' stroke='#64748b' stroke-width='5'/>
     <path d='M960,360 L960,200' stroke='#38bdf8' stroke-width='10' stroke-linecap='round'/>
     <rect x='520' y='300' width='140' height='260' rx='24' fill='#cbd5e1' stroke='#475569' stroke-width='6'/>
     <ellipse cx='590' cy='320' rx='60' ry='20' fill='#94a3b8'/>
     <polygon points='430,420 740,360 760,580 450,640' fill='#eab308' stroke='#ca8a04' stroke-width='6'/>
     <text x='590' y='510' font-family=\"'Montserrat'\" font-size='32' font-weight='900' fill='#991b1b' text-anchor='middle' transform='rotate(-8 590 510)'>HALDIRAM BHUJIA</text>
     """,
     "[SFX: Mechanical key switches heavily compressed under steel thermos & snack packet]"),

    ("scene_06_key.png", "BEAT 6: THE LIFT & CLACK", "37.5s – 45.0s", "#042f2e",
     """
     <polygon points='700,240 1010,180 1030,400 720,460' fill='#eab308' stroke='#ca8a04' stroke-width='6'/>
     <rect x='360' y='540' width='1200' height='420' rx='20' fill='#064e3b' stroke='#10b981' stroke-width='8'/>
     <text x='960' y='680' font-family=\"'Montserrat'\" font-size='44' font-weight='900' fill='#34d399' text-anchor='middle'>BUILD SUCCESSFUL • 248 TESTS PASSED</text>
     <text x='960' y='780' font-family=\"'Montserrat'\" font-size='56' font-weight='900' fill='#ffffff' text-anchor='middle'>READY TO DEPLOY • PRODUCTION V1.0</text>
     """,
     "[SFX: Crisp mechanical key spring CLACK • Triumphant server deployment chime]"),

    ("scene_07_key.png", "BEAT 7: STUNNED SLACK-JAW", "45.0s – 52.5s", "#0b1324",
     """
     <circle cx='600' cy='520' r='140' fill='#fdba74'/>
     <ellipse cx='550' cy='480' rx='24' ry='22' fill='#ffffff'/><circle cx='550' cy='480' r='9' fill='#78350f'/>
     <ellipse cx='650' cy='480' rx='24' ry='22' fill='#ffffff'/><circle cx='650' cy='480' r='9' fill='#78350f'/>
     <ellipse cx='600' cy='590' rx='32' ry='48' fill='#451a03'/>
     <circle cx='1320' cy='480' r='130' fill='#fed7aa'/>
     <circle cx='1260' cy='480' r='38' fill='none' stroke='#38bdf8' stroke-width='8'/>
     <circle cx='1380' cy='480' r='38' fill='none' stroke='#38bdf8' stroke-width='8'/>
     <path d='M1290,550 Q1320,580 1350,550' stroke='#78350f' stroke-width='6' fill='none'/>
     <polygon points='1480,440 1620,400 1630,550 1490,590' fill='#eab308' stroke='#ca8a04' stroke-width='5'/>
     """,
     "कबीर: \"ये... ये भुजिया थी?! पूरा दिन भुजिया की वजह से बर्बाद हुआ?!\""),

    ("scene_08_key.png", "BEAT 8: PUNCHLINE & VICTORY", "52.5s – 60.0s", "#090d16",
     """
     <circle cx='680' cy='500' r='130' fill='#fdba74'/>
     <path d='M780,560 L890,380' stroke='#f97316' stroke-width='40' stroke-linecap='round'/>
     <circle cx='1240' cy='480' r='130' fill='#fed7aa'/>
     <rect x='460' y='140' width='1000' height='120' rx='16' fill='#1e293b' stroke='#f97316' stroke-width='4'/>
     <text x='960' y='215' font-family=\"'Noto Sans Devanagari'\" font-size='46' font-weight='800' fill='#ffffff' text-anchor='middle'>लास्ट बग — जीत की भुजिया!</text>
     """,
     "मीरा: \"हाँ! तो हमारे सबसे बड़े 'इंटरनेशनल हैकर' का नाम था... हल्दीराम की स्पेशल भुजिया!\"")
]

for filename, title, timing, bg, svg_body, dialogue in scenes:
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+Devanagari:wght@700;800&display=swap');
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 0;
    width: 1920px; height: 1080px; overflow: hidden;
    background: {bg}; color: #ffffff;
    font-family: 'Montserrat', sans-serif;
    position: relative;
  }}
  .header {{
    position: absolute; top: 40px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 3px solid #f97316; padding-bottom: 12px;
  }}
  .header h2 {{ font-size: 32px; font-weight: 900; margin: 0; letter-spacing: 1px; }}
  .header .time {{ font-size: 26px; font-weight: 800; color: #f97316; }}
  .lower-dialogue {{
    position: absolute; bottom: 40px; left: 100px; right: 100px;
    background: rgba(15, 23, 42, 0.92); border: 2px solid #38bdf8;
    border-radius: 12px; padding: 18px 30px;
    font-family: 'Noto Sans Devanagari', sans-serif;
    font-size: 26px; font-weight: 700; color: #38bdf8; text-align: center;
  }}
</style>
</head>
<body>
  <div class="header">
    <h2>{title}</h2>
    <div class="time">{timing}</div>
  </div>
  <svg width="1920" height="1080" style="position:absolute; top:0; left:0;">
    {svg_body}
  </svg>
  <div class="lower-dialogue">{dialogue}</div>
</body>
</html>"""

    out_file = os.path.join(OUTPUT_DIR, filename)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html)
        tmp = tf.name
    try:
        cmd = [CHROME_BIN, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1920,1080", f"--screenshot={out_file}", tmp]
        subprocess.run(cmd, check=True)
        print(f"Rendered keyframe: {filename}")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

print("All 8 individual keyframes rendered successfully!")
