"""
generate_storyboard.py
======================
Generates the 4-scene Master Production Storyboard for:
"चाय और चाल" (Chai & Chaal / The Chai Gambit)
Includes:
- Individual storyboard scene frames (frame_01 to frame_04)
- Master 1920x1080 Storyboard Grid with action notes, camera setups, and dialogue
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2\storyboard"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content: str, output_png: str, w=1920, h=1080):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_content)
        temp_html = tf.name

    try:
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={w},{h}",
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

# =============================================================================
# MASTER 4-PANEL STORYBOARD SHEET (1920x1080)
# =============================================================================
storyboard_master_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 25px 35px;
    background: #090d16;
    color: #f1f5f9;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px;
    overflow: hidden;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid #f59e0b; padding-bottom: 12px; margin-bottom: 20px;
  }
  .title-block h1 {
    font-size: 32px; font-weight: 800; margin: 0; color: #ffffff;
  }
  .title-block .sub {
    font-size: 14px; color: #f59e0b; font-weight: 600; margin-top: 4px; text-transform: uppercase; letter-spacing: 2px;
  }
  .grid {
    display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 20px; height: 920px;
  }
  .frame-card {
    background: #131b2a; border: 1px solid #233044; border-radius: 10px; padding: 15px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .frame-header {
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;
    font-size: 13px; font-weight: 700; color: #f59e0b;
  }
  .visual-box {
    width: 100%; height: 260px; background: #0b0f19; border-radius: 6px; overflow: hidden;
    position: relative; border: 1px solid #1e293b;
  }
  .frame-details {
    margin-top: 10px; font-size: 12px; color: #cbd5e1; line-height: 1.45;
  }
  .dialogue {
    font-family: 'Noto Sans Devanagari', sans-serif; font-size: 14px; font-weight: 600; color: #38bdf8;
    background: rgba(14, 165, 233, 0.12); padding: 6px 10px; border-radius: 4px; margin-top: 6px;
    border-left: 3px solid #38bdf8;
  }
</style>
</head>
<body>

  <div class="header">
    <div class="title-block">
      <h1>PRODUCTION STORYBOARD: "चाय और चाल" (THE CHAI GAMBIT)</h1>
      <div class="sub">30.00s Animated Short • 4 Cinematic Beats • Contemporary Mumbai Neo-Noir / Urban Slice of Life</div>
    </div>
    <div style="text-align:right; font-size:13px; color:#94a3b8;">
      Master AI Phase: <strong>7.7.2 Professional Character Redesign</strong><br>
      Aspect: <strong>16:9 (1920x1080)</strong> • Frame Rate: <strong>24.0 FPS CFR</strong>
    </div>
  </div>

  <div class="grid">
    <!-- PANEL 1 -->
    <div class="frame-card">
      <div class="frame-header">
        <span>BEAT 1: THE CONFRONTATION & THE NAPKIN</span>
        <span>00:00.00 – 00:07.50 (180 FRAMES)</span>
      </div>
      <div class="visual-box">
        <svg width="100%" height="100%" viewBox="0 0 880 260">
          <defs>
            <linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0b1329"/>
              <stop offset="100%" stop-color="#182238"/>
            </linearGradient>
          </defs>
          <rect width="880" height="260" fill="url(#bg1)"/>
          <!-- Rainy window & neon cafe sign bokeh -->
          <circle cx="180" cy="80" r="45" fill="#f43f5e" opacity="0.25"/>
          <circle cx="320" cy="60" r="35" fill="#38bdf8" opacity="0.2"/>
          <text x="80" y="50" font-family="'Montserrat'" font-size="22" font-weight="800" fill="#f59e0b" opacity="0.4">CHAI & CO.</text>
          <!-- Table -->
          <polygon points="0,210 880,210 880,260 0,260" fill="#292019"/>
          <!-- Vikram leaning in with smug grin -->
          <path d="M520 120 Q620 90 680 140 Q690 190 620 220 Z" fill="#fcd34d"/>
          <!-- Glasses & smug smile -->
          <rect x="560" y="140" width="30" height="20" rx="3" fill="none" stroke="#78350f" stroke-width="3"/>
          <circle cx="575" cy="150" r="3" fill="#1e1b4b"/>
          <path d="M565 180 Q595 190 620 175" stroke="#78350f" stroke-width="3.5" fill="none"/>
          <path d="M500 180 L440 215 L530 220 Z" fill="#047857"/>
          <!-- Napkin sliding across table -->
          <polygon points="410,215 470,212 485,235 425,238" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M425 218 L460 216" stroke="#ef4444" stroke-width="2"/>
          <!-- Aisha seated opposite, back 3/4 listening calmly -->
          <path d="M180 150 Q230 130 270 170 Q250 220 190 220 Z" fill="#eab308"/>
          <path d="M210 130 Q250 110 270 140 Q250 180 210 180 Z" fill="#1e1b4b"/>
        </svg>
      </div>
      <div class="frame-details">
        <strong>Camera:</strong> Medium Over-the-Shoulder two-shot. Depth of field with neon city rain bokeh.<br>
        <strong>Action:</strong> Vikram slides napkin with stolen design idea, leaning in with overconfident arrogance.<br>
        <div class="dialogue">विक्रम: "बुरा मत मानना आयशा, लेकिन तुम्हारा पिच मैंने थोड़ा 'अपग्रेड' कर दिया... डील फाइनल है!"</div>
      </div>
    </div>

    <!-- PANEL 2 -->
    <div class="frame-card">
      <div class="frame-header">
        <span>BEAT 2: THE UNFLINCHING SIP</span>
        <span>00:07.50 – 00:15.00 (180 FRAMES)</span>
      </div>
      <div class="visual-box">
        <svg width="100%" height="100%" viewBox="0 0 880 260">
          <rect width="880" height="260" fill="#101826"/>
          <!-- Neon warm chai corner lights -->
          <circle cx="700" cy="70" r="50" fill="#f59e0b" opacity="0.2"/>
          <circle cx="150" cy="90" r="40" fill="#10b981" opacity="0.15"/>
          <!-- Close-up Aisha -->
          <path d="M340 70 Q440 35 520 75 Q540 155 440 195 Q330 155 340 70 Z" fill="#fed7aa"/>
          <!-- Almond Eyes half-lidded, perfectly calm -->
          <ellipse cx="400" cy="115" rx="14" ry="7" fill="#ffffff"/>
          <circle cx="402" cy="115" r="5" fill="#451a03"/>
          <circle cx="400" cy="113" r="1.5" fill="#ffffff"/>
          <ellipse cx="460" cy="115" rx="14" ry="7" fill="#ffffff"/>
          <circle cx="458" cy="115" r="5" fill="#451a03"/>
          <circle cx="456" cy="113" r="1.5" fill="#ffffff"/>
          <!-- Eyelash wings -->
          <path d="M386 110 Q402 103 416 110" stroke="#0f172a" stroke-width="3" fill="none"/>
          <path d="M446 110 Q462 103 476 110" stroke="#0f172a" stroke-width="3" fill="none"/>
          <!-- Subtle smirk and cutting chai glass held at lips -->
          <path d="M410 162 Q430 166 450 158" stroke="#be123c" stroke-width="4" stroke-linecap="round" fill="none"/>
          <!-- Cutting Chai Glass in Hand -->
          <path d="M415 155 L455 155 L448 215 L422 215 Z" fill="#f59e0b" stroke="#ffffff" stroke-width="2.5"/>
          <path d="M430 148 Q436 130 428 118 Q436 106 432 95" stroke="#ffffff" stroke-width="2.2" fill="none" opacity="0.75"/>
          <!-- Stylish Asymmetrical Bob Hair -->
          <path d="M330 75 C320 20, 530 20, 520 75 C535 140, 535 210, 485 235 C475 165, 455 110, 455 90 C410 75, 360 100, 345 135 Z" fill="#1e1b4b"/>
        </svg>
      </div>
      <div class="frame-details">
        <strong>Camera:</strong> Cinematic Intimate Close-Up on Aisha. Soft depth-of-field, amber warmth.<br>
        <strong>Action:</strong> Aisha doesn't flinch. She takes a slow, poised sip of cutting chai, her eyes sparkling with amusement.<br>
        <div class="dialogue">आयशा: "अच्छा? ज़रा अपना इनबॉक्स चेक कर लो, विक्रम।"</div>
      </div>
    </div>

    <!-- PANEL 3 -->
    <div class="frame-card">
      <div class="frame-header">
        <span>BEAT 3: THE IPAD REVEAL & JAW DROP</span>
        <span>00:15.00 – 00:22.50 (180 FRAMES)</span>
      </div>
      <div class="visual-box">
        <svg width="100%" height="100%" viewBox="0 0 880 260">
          <rect width="880" height="260" fill="#0d1422"/>
          <!-- Table -->
          <polygon points="0,195 880,195 880,260 0,260" fill="#292019"/>
          <!-- Luminous iPad turned towards Vikram -->
          <rect x="240" y="70" width="220" height="145" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
          <rect x="250" y="80" width="200" height="125" rx="4" fill="#0f172a"/>
          <!-- Client CEO Email Glowing Content -->
          <text x="260" y="105" font-family="'Montserrat'" font-size="12" font-weight="700" fill="#38bdf8">CLIENT APPROVAL • APEX CORP</text>
          <text x="260" y="125" font-family="'Montserrat'" font-size="11" font-weight="600" fill="#f8fafc">"Loved Aisha's Design!"</text>
          <text x="260" y="145" font-family="'Montserrat'" font-size="10" font-weight="400" fill="#94a3b8">Aisha is appointed Project Lead.</text>
          <text x="260" y="162" font-family="'Montserrat'" font-size="10" font-weight="400" fill="#f59e0b">Vikram assigned as Junior Assist.</text>
          <circle cx="430" cy="185" r="8" fill="#10b981"/>
          <!-- Vikram Jaw Drop Reaction (Right) -->
          <path d="M600 65 Q680 35 730 75 Q740 145 680 185 Q610 155 600 65 Z" fill="#fcd34d"/>
          <!-- Big shocked pupils behind crooked glasses -->
          <rect x="620" y="85" width="32" height="24" rx="3" fill="none" stroke="#78350f" stroke-width="3"/>
          <rect x="665" y="85" width="32" height="24" rx="3" fill="none" stroke="#78350f" stroke-width="3"/>
          <circle cx="636" cy="97" r="5" fill="#1e1b4b"/>
          <circle cx="681" cy="97" r="5" fill="#1e1b4b"/>
          <!-- Open 'O' Shocked Mouth -->
          <ellipse cx="660" cy="148" rx="14" ry="20" fill="#451a03"/>
          <!-- Biscuit dropping into tea! -->
          <ellipse cx="560" cy="190" rx="12" ry="6" fill="#d97706"/>
          <!-- Chai splash droplets -->
          <circle cx="550" cy="182" r="3" fill="#f59e0b"/>
          <circle cx="568" cy="180" r="2.5" fill="#f59e0b"/>
        </svg>
      </div>
      <div class="frame-details">
        <strong>Camera:</strong> Dynamic Dutch-angle two-shot focusing on the glowing iPad screen.<br>
        <strong>Action:</strong> Aisha spins her tablet. Vikram reads the verdict; his smugness shatters into total disbelief as his Parle-G biscuit drops into his tea.<br>
        <div class="dialogue">विक्रम: "व्हाट?! 'आयशा इज़ द न्यू प्रोजेक्ट हेड'...?!"</div>
      </div>
    </div>

    <!-- PANEL 4 -->
    <div class="frame-card">
      <div class="frame-header">
        <span>BEAT 4: THE PUNCHLINE & THE WIN</span>
        <span>00:22.50 – 00:30.00 (180 FRAMES)</span>
      </div>
      <div class="visual-box">
        <svg width="100%" height="100%" viewBox="0 0 880 260">
          <rect width="880" height="260" fill="#0a0f1d"/>
          <!-- Glowing neon reflections on wet street pavement outside -->
          <path d="M0 200 L880 200 L880 260 L0 260 Z" fill="#1b171c"/>
          <path d="M100 230 Q250 215 400 230" stroke="#f43f5e" stroke-width="4" opacity="0.4"/>
          <path d="M500 235 Q650 220 800 235" stroke="#38bdf8" stroke-width="4" opacity="0.4"/>
          <!-- Aisha Winking with Cutting Glass (Left) -->
          <path d="M220 70 Q300 40 360 80 Q370 145 300 185 Q220 150 220 70 Z" fill="#fed7aa"/>
          <circle cx="265" cy="110" r="5" fill="#451a03"/> <!-- Left eye open -->
          <path d="M295 112 Q310 118 325 110" stroke="#0f172a" stroke-width="3.5" fill="none"/> <!-- Right eye wink! -->
          <path d="M260 148 Q285 168 315 148" stroke="#be123c" stroke-width="4" fill="none"/> <!-- Big joyful smile -->
          <!-- Vikram pulling out wallet with sheepish surrender (Right) -->
          <path d="M620 90 Q680 70 720 105 Q710 160 650 185 Z" fill="#fcd34d"/>
          <rect x="635" y="105" width="24" height="18" rx="2" fill="none" stroke="#78350f" stroke-width="2.5"/>
          <rect x="670" y="105" width="24" height="18" rx="2" fill="none" stroke="#78350f" stroke-width="2.5"/>
          <!-- Sheepish smile -->
          <path d="M645 152 Q665 160 685 150" stroke="#78350f" stroke-width="3" fill="none"/>
          <!-- Leather wallet open in hand -->
          <polygon points="560,185 610,180 615,210 565,215" fill="#78350f"/>
          <!-- Outro badge overlay badge preview -->
          <rect x="290" y="15" width="300" height="38" rx="6" fill="rgba(15, 23, 42, 0.9)" stroke="#f59e0b" stroke-width="2"/>
          <text x="440" y="40" font-family="'Noto Sans Devanagari'" font-size="18" font-weight="700" fill="#ffffff" text-anchor="middle">चाय और चाल — जीत की घूँट</text>
        </svg>
      </div>
      <div class="frame-details">
        <strong>Camera:</strong> Wide Cinematic Two-Shot with atmospheric neon rain reflections.<br>
        <strong>Action:</strong> Aisha raises her cutting glass with a triumphant, playful wink. Vikram sheepishly taps his phone for UPI payment.<br>
        <div class="dialogue">आयशा: "हाँ... और इस जीत की चाय के पैसे तुम दोगे, पार्टनर!"</div>
      </div>
    </div>
  </div>

</body>
</html>"""
render_html_to_png(storyboard_master_html, os.path.join(OUTPUT_DIR, "storyboard_master.png"))

print("Master Storyboard Generated Successfully!")
