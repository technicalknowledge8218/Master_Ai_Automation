"""
generate_characters_and_storyboard_774.py
=========================================
Generates 1920x1080 Character Design Sheets and Master Storyboard for:
"कोड रेड: डिलीवरी" (Code Red: 10-Minute Delivery) - Phase 7.7.4
"""

import os
import subprocess
import tempfile

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4"
CHAR_DIR = os.path.join(BASE_DIR, "character_sheets")
STORY_DIR = os.path.join(BASE_DIR, "storyboard")
os.makedirs(CHAR_DIR, exist_ok=True)
os.makedirs(STORY_DIR, exist_ok=True)

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_BIN):
    CHROME_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_str, out_path, w=1920, h=1080):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_str)
        tmp = tf.name
    try:
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={w},{h}",
            f"--screenshot={out_path}",
            tmp
        ]
        subprocess.run(cmd, check=True)
        print(f"Generated: {out_path}")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

# =============================================================================
# 1. ARYAN CHARACTER SHEET
# =============================================================================
aryan_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+Devanagari:wght@700;800&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 30px 50px;
    background: #070e1b; color: #f8fafc;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px; overflow: hidden;
  }
  .header {
    border-bottom: 3px solid #0284c7; padding-bottom: 15px; margin-bottom: 25px;
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  h1 { margin: 0; font-size: 34px; font-weight: 900; letter-spacing: 1px; color: #38bdf8; }
  .meta { font-size: 14px; color: #94a3b8; font-weight: 600; }
  .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; height: 860px; }
  .panel {
    background: #0f172a; border: 2px solid #1e293b; border-radius: 16px; padding: 24px;
    display: flex; flex-direction: column; align-items: center; justify-content: space-between;
  }
  .panel h2 { font-size: 20px; color: #38bdf8; margin: 0 0 15px 0; text-transform: uppercase; }
  .swatch-row { display: flex; gap: 12px; margin-top: 15px; }
  .swatch { width: 55px; height: 55px; border-radius: 10px; border: 2px solid #334155; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>CHARACTER DESIGN SHEET: आर्यन (ARYAN)</h1>
      <div class="meta">Role: Electric Scooter Delivery Rider • Age: 21 • Modern Bengaluru Indie Setting</div>
    </div>
    <div class="meta" style="text-align:right;">
      Phase 7.7.4 Production • High-Vis Teal Jacket, Sleek Rain Visor Helmet
    </div>
  </div>
  <div class="grid">
    <!-- Turnaround Front -->
    <div class="panel">
      <h2>Front Turnaround</h2>
      <svg width="340" height="620" viewBox="0 0 340 620">
        <!-- Legs & Dark Pants -->
        <line x1="130" y1="440" x2="120" y2="580" stroke="#1e293b" stroke-width="32" stroke-linecap="round"/>
        <line x1="210" y1="440" x2="220" y2="580" stroke="#1e293b" stroke-width="32" stroke-linecap="round"/>
        <rect x="95" y="575" width="45" height="24" rx="8" fill="#0284c7"/>
        <rect x="200" y="575" width="45" height="24" rx="8" fill="#0284c7"/>
        <!-- Torso & High-Vis Teal/Amber Jacket -->
        <rect x="100" y="240" width="140" height="210" rx="20" fill="#0284c7" stroke="#0369a1" stroke-width="4"/>
        <path d="M100,320 L240,320" stroke="#f59e0b" stroke-width="18"/>
        <!-- Arms -->
        <path d="M100,260 L60,390" stroke="#0284c7" stroke-width="26" stroke-linecap="round"/>
        <circle cx="60" cy="390" r="16" fill="#fdba74"/>
        <path d="M240,260 L280,390" stroke="#0284c7" stroke-width="26" stroke-linecap="round"/>
        <circle cx="280" cy="390" r="16" fill="#fdba74"/>
        <!-- Neck & Head -->
        <rect x="155" y="210" width="30" height="40" fill="#fdba74"/>
        <circle cx="170" cy="150" r="75" fill="#0f172a" stroke="#0284c7" stroke-width="6"/> <!-- Helmet -->
        <!-- Clear Visor -->
        <path d="M115,140 Q170,120 225,140 L220,185 Q170,205 120,185 Z" fill="#38bdf8" opacity="0.85" stroke="#bae6fd" stroke-width="3"/>
        <!-- Eyes inside visor -->
        <ellipse cx="145" cy="155" rx="10" ry="8" fill="#ffffff"/><circle cx="145" cy="155" r="4.5" fill="#1e293b"/>
        <ellipse cx="195" cy="155" rx="10" ry="8" fill="#ffffff"/><circle cx="195" cy="155" r="4.5" fill="#1e293b"/>
      </svg>
      <div style="font-size:12px; color:#94a3b8; text-align:center;">Frontal orthographic key</div>
    </div>
    <!-- 3/4 Action Pose -->
    <div class="panel">
      <h2>3/4 Scooter Riding Pose</h2>
      <svg width="340" height="620" viewBox="0 0 340 620">
        <!-- Scooter Handlebar -->
        <line x1="80" y1="360" x2="260" y2="340" stroke="#64748b" stroke-width="12" stroke-linecap="round"/>
        <!-- Smartphone Mount with glowing countdown -->
        <rect x="150" y="300" width="40" height="65" rx="6" fill="#180606" stroke="#ef4444" stroke-width="3"/>
        <text x="170" y="338" font-family="'Montserrat'" font-size="10" font-weight="900" fill="#ef4444" text-anchor="middle">09:59</text>
        <!-- Aryan Hands gripping handlebar -->
        <circle cx="100" cy="360" r="18" fill="#fdba74"/>
        <circle cx="240" cy="340" r="18" fill="#fdba74"/>
        <!-- Leaning Torso & Helmet -->
        <path d="M120,240 L220,220 L240,400 L140,420 Z" fill="#0284c7"/>
        <circle cx="170" cy="140" r="70" fill="#0f172a" stroke="#0284c7" stroke-width="5"/>
        <path d="M125,130 Q170,115 215,135 L210,175 Q170,195 130,175 Z" fill="#38bdf8" opacity="0.9"/>
      </svg>
      <div style="font-size:12px; color:#94a3b8; text-align:center;">Action posture: Aerodynamic lean</div>
    </div>
    <!-- Expressions & Palette -->
    <div class="panel">
      <h2>Expressions & Palette</h2>
      <div style="display:flex; flex-direction:column; gap:20px; width:100%; align-items:center;">
        <!-- Focused Eye -->
        <div style="background:#070a12; border:1px solid #1e293b; border-radius:10px; padding:10px; width:100%; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:#38bdf8; margin-bottom:6px;">1. FOCUSED DETERMINATION</div>
          <svg width="240" height="70" viewBox="0 0 240 70">
            <ellipse cx="80" cy="35" rx="22" ry="16" fill="#ffffff"/><circle cx="85" cy="35" r="8" fill="#78350f"/>
            <ellipse cx="160" cy="35" rx="22" ry="16" fill="#ffffff"/><circle cx="165" cy="35" r="8" fill="#78350f"/>
            <path d="M55,20 Q80,15 105,25" stroke="#1e293b" stroke-width="5" fill="none"/>
            <path d="M135,25 Q160,15 185,20" stroke="#1e293b" stroke-width="5" fill="none"/>
          </svg>
        </div>
        <!-- Stressed Panic -->
        <div style="background:#070a12; border:1px solid #1e293b; border-radius:10px; padding:10px; width:100%; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:#ef4444; margin-bottom:6px;">2. DEADLINE TENSION</div>
          <svg width="240" height="70" viewBox="0 0 240 70">
            <ellipse cx="80" cy="35" rx="26" ry="22" fill="#ffffff"/><circle cx="80" cy="35" r="7" fill="#78350f"/>
            <ellipse cx="160" cy="35" rx="26" ry="22" fill="#ffffff"/><circle cx="160" cy="35" r="7" fill="#78350f"/>
          </svg>
        </div>
        <!-- Warm Smile -->
        <div style="background:#070a12; border:1px solid #1e293b; border-radius:10px; padding:10px; width:100%; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:#10b981; margin-bottom:6px;">3. WARM OUTRO SMILE</div>
          <svg width="240" height="70" viewBox="0 0 240 70">
            <path d="M70,30 Q90,15 110,30" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M130,30 Q150,15 170,30" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M85,50 Q120,68 155,50" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
          </svg>
        </div>
      </div>
      <!-- Color Swatches -->
      <div style="width:100%;">
        <div style="font-size:13px; font-weight:700; color:#94a3b8; margin-bottom:6px;">PRODUCTION COLOR SWATCHES</div>
        <div class="swatch-row">
          <div class="swatch" style="background:#0284c7;" title="Teal Jacket"></div>
          <div class="swatch" style="background:#f59e0b;" title="Amber Stripe"></div>
          <div class="swatch" style="background:#38bdf8;" title="Rain Visor"></div>
          <div class="swatch" style="background:#0f172a;" title="Dark Helmet"></div>
          <div class="swatch" style="background:#fdba74;" title="Skin Tone"></div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

render_html_to_png(aryan_html, os.path.join(CHAR_DIR, "aryan_character_sheet.png"))

# =============================================================================
# 2. ANANYA CHARACTER SHEET
# =============================================================================
ananya_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+Devanagari:wght@700;800&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 30px 50px;
    background: #091316; color: #f8fafc;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px; overflow: hidden;
  }
  .header {
    border-bottom: 3px solid #059669; padding-bottom: 15px; margin-bottom: 25px;
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  h1 { margin: 0; font-size: 34px; font-weight: 900; letter-spacing: 1px; color: #34d399; }
  .meta { font-size: 14px; color: #94a3b8; font-weight: 600; }
  .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; height: 860px; }
  .panel {
    background: #0d1b1e; border: 2px solid #134e4a; border-radius: 16px; padding: 24px;
    display: flex; flex-direction: column; align-items: center; justify-content: space-between;
  }
  .panel h2 { font-size: 20px; color: #34d399; margin: 0 0 15px 0; text-transform: uppercase; }
  .swatch-row { display: flex; gap: 12px; margin-top: 15px; }
  .swatch { width: 55px; height: 55px; border-radius: 10px; border: 2px solid #115e59; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>CHARACTER DESIGN SHEET: डॉ. अनन्या (DR. ANANYA)</h1>
      <div class="meta">Role: Resident Emergency Doctor • Age: 26 • St. Martha's Hospital</div>
    </div>
    <div class="meta" style="text-align:right;">
      Phase 7.7.4 Production • Surgical Scrubs (`#059669`), Stethoscope, Scrub Cap
    </div>
  </div>
  <div class="grid">
    <!-- Front Turnaround -->
    <div class="panel">
      <h2>Front Turnaround</h2>
      <svg width="340" height="620" viewBox="0 0 340 620">
        <!-- Pants -->
        <line x1="135" y1="440" x2="125" y2="580" stroke="#047857" stroke-width="30" stroke-linecap="round"/>
        <line x1="205" y1="440" x2="215" y2="580" stroke="#047857" stroke-width="30" stroke-linecap="round"/>
        <!-- Scrub Top -->
        <rect x="105" y="240" width="130" height="210" rx="16" fill="#059669" stroke="#047857" stroke-width="4"/>
        <path d="M145,240 L170,280 L195,240" stroke="#047857" stroke-width="4" fill="none"/>
        <!-- Stethoscope -->
        <path d="M140,240 Q170,350 200,240" stroke="#cbd5e1" stroke-width="6" fill="none"/>
        <circle cx="170" cy="330" r="12" fill="#94a3b8"/>
        <!-- Head & Scrub Cap -->
        <circle cx="170" cy="150" r="65" fill="#fed7aa"/>
        <path d="M105,145 Q170,80 235,145 Z" fill="#065f46"/> <!-- Scrub cap -->
        <!-- Eyes -->
        <ellipse cx="148" cy="150" rx="9" ry="7" fill="#ffffff"/><circle cx="148" cy="150" r="4" fill="#1e293b"/>
        <ellipse cx="192" cy="150" rx="9" ry="7" fill="#ffffff"/><circle cx="192" cy="150" r="4" fill="#1e293b"/>
        <path d="M155,180 Q170,190 185,180" stroke="#78350f" stroke-width="4" fill="none"/>
      </svg>
      <div style="font-size:12px; color:#94a3b8; text-align:center;">Frontal orthographic key</div>
    </div>
    <!-- 3/4 Holding Delivery Box -->
    <div class="panel">
      <h2>3/4 Holding Surprise Pastry</h2>
      <svg width="340" height="620" viewBox="0 0 340 620">
        <!-- Body -->
        <rect x="110" y="240" width="120" height="220" rx="16" fill="#059669"/>
        <!-- Head tilted down at pastry -->
        <circle cx="170" cy="150" r="65" fill="#fed7aa"/>
        <path d="M105,145 Q170,80 235,145 Z" fill="#065f46"/>
        <!-- Hands holding box -->
        <rect x="100" y="360" width="140" height="90" rx="10" fill="#fef08a" stroke="#ca8a04" stroke-width="3"/>
        <!-- Strawberry pastry inside with candle -->
        <rect x="130" y="380" width="80" height="40" rx="8" fill="#fda4af"/>
        <line x1="170" y1="380" x2="170" y2="360" stroke="#ffffff" stroke-width="3"/>
        <circle cx="170" cy="355" r="6" fill="#facc15"/> <!-- Flame -->
      </svg>
      <div style="font-size:12px; color:#94a3b8; text-align:center;">Emotional discovery keyframe</div>
    </div>
    <!-- Expressions & Palette -->
    <div class="panel">
      <h2>Expressions & Palette</h2>
      <div style="display:flex; flex-direction:column; gap:20px; width:100%; align-items:center;">
        <!-- Weary / Exhausted -->
        <div style="background:#070a12; border:1px solid #134e4a; border-radius:10px; padding:10px; width:100%; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:#94a3b8; margin-bottom:6px;">1. 36-HOUR POST-OP EXHAUSTION</div>
          <svg width="240" height="70" viewBox="0 0 240 70">
            <ellipse cx="80" cy="35" rx="20" ry="12" fill="#ffffff"/><circle cx="80" cy="38" r="5" fill="#1e293b"/>
            <ellipse cx="160" cy="35" rx="20" ry="12" fill="#ffffff"/><circle cx="160" cy="38" r="5" fill="#1e293b"/>
            <!-- Under eye dark circles -->
            <path d="M60,45 Q80,55 100,45" stroke="#94a3b8" stroke-width="2" fill="none"/>
            <path d="M140,45 Q160,55 180,45" stroke="#94a3b8" stroke-width="2" fill="none"/>
          </svg>
        </div>
        <!-- Surprise -->
        <div style="background:#070a12; border:1px solid #134e4a; border-radius:10px; padding:10px; width:100%; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:#38bdf8; margin-bottom:6px;">2. DISCOVERY OF MOM'S NOTE</div>
          <svg width="240" height="70" viewBox="0 0 240 70">
            <ellipse cx="80" cy="35" rx="22" ry="20" fill="#ffffff"/><circle cx="80" cy="35" r="7" fill="#1e293b"/>
            <ellipse cx="160" cy="35" rx="22" ry="20" fill="#ffffff"/><circle cx="160" cy="35" r="7" fill="#1e293b"/>
          </svg>
        </div>
        <!-- Tearful Smile -->
        <div style="background:#070a12; border:1px solid #134e4a; border-radius:10px; padding:10px; width:100%; text-align:center;">
          <div style="font-size:13px; font-weight:700; color:#34d399; margin-bottom:6px;">3. DEEPLY TOUCHED SMILE</div>
          <svg width="240" height="70" viewBox="0 0 240 70">
            <path d="M65,35 Q85,20 105,35" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M135,35 Q155,20 175,35" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M85,50 Q120,70 155,50" stroke="#78350f" stroke-width="5" fill="none" stroke-linecap="round"/>
            <!-- Tear of joy -->
            <ellipse cx="180" cy="45" rx="4" ry="7" fill="#38bdf8"/>
          </svg>
        </div>
      </div>
      <!-- Color Swatches -->
      <div style="width:100%;">
        <div style="font-size:13px; font-weight:700; color:#94a3b8; margin-bottom:6px;">PRODUCTION COLOR SWATCHES</div>
        <div class="swatch-row">
          <div class="swatch" style="background:#059669;" title="Medical Scrubs"></div>
          <div class="swatch" style="background:#065f46;" title="Scrub Cap"></div>
          <div class="swatch" style="background:#fda4af;" title="Strawberry Pastry"></div>
          <div class="swatch" style="background:#cbd5e1;" title="Stethoscope"></div>
          <div class="swatch" style="background:#fed7aa;" title="Skin Tone"></div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

render_html_to_png(ananya_html, os.path.join(CHAR_DIR, "ananya_character_sheet.png"))

# =============================================================================
# 3. MASTER 8-PANEL STORYBOARD
# =============================================================================
storyboard_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+Devanagari:wght@700;800&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 20px 30px;
    background: #070a12; color: #f8fafc;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px; overflow: hidden;
  }
  .header {
    border-bottom: 2px solid #0284c7; padding-bottom: 8px; margin-bottom: 12px;
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  h1 { margin: 0; font-size: 26px; font-weight: 800; color: #38bdf8; }
  .grid {
    display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: 1fr 1fr; gap: 14px; height: 950px;
  }
  .card {
    background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 10px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .card-header {
    display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; color: #38bdf8; margin-bottom: 6px;
  }
  .visual {
    width: 100%; height: 230px; background: #070e1b; border-radius: 6px; overflow: hidden; border: 1px solid #1e293b;
  }
  .meta { font-size: 10px; color: #94a3b8; margin-top: 6px; line-height: 1.35; }
  .dialogue {
    font-family: 'Noto Sans Devanagari', sans-serif; font-size: 11px; font-weight: 600; color: #38bdf8;
    background: rgba(14, 165, 233, 0.1); padding: 4px 6px; border-radius: 4px; margin-top: 4px;
    border-left: 2px solid #38bdf8;
  }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>DIRECTORIAL STORYBOARD: "कोड रेड: डिलीवरी" (CODE RED: 10-MINUTE DELIVERY)</h1>
      <div style="font-size:12px; color:#f59e0b; font-weight:700;">60.00s Complete 2D Film • 8 Cinematic Beats • Shot Grammar & Motivated Cuts</div>
    </div>
    <div style="font-size:11px; color:#94a3b8; text-align:right;">
      Phase: <strong>7.7.4</strong> • Aspect: <strong>16:9 1080p</strong> • FPS: <strong>24.0 CFR</strong> • Budget: <strong>₹0.00</strong>
    </div>
  </div>
  <div class="grid">
    <!-- Beat 1 -->
    <div class="card">
      <div class="card-header"><span>BEAT 1: THE COUNTDOWN [ECU]</span><span>0.0s – 7.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#180606"/>
          <rect x="140" y="30" width="160" height="170" rx="14" fill="#090d16" stroke="#ef4444" stroke-width="4"/>
          <text x="220" y="80" font-family="'Montserrat'" font-size="14" font-weight="900" fill="#ef4444" text-anchor="middle">URGENT ORDER #402</text>
          <text x="220" y="130" font-family="'Montserrat'" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">09:59</text>
          <text x="220" y="165" font-family="'Montserrat'" font-size="10" font-weight="700" fill="#fca5a5" text-anchor="middle">CANCEL IN 10 MIN</text>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> START | <strong>Shot:</strong> Extreme Close-Up | <strong>Move:</strong> Dolly-In<br>
        <div class="dialogue">आर्यन: "दस मिनट... और पूरा शहर ट्रैफ़िक में डूबा है! पर ये ऑर्डर कैंसल नहीं होगा!"</div>
      </div>
    </div>

    <!-- Beat 2 -->
    <div class="card">
      <div class="card-header"><span>BEAT 2: THE KITCHEN [MED]</span><span>7.5s – 15.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#1c0e08"/>
          <!-- Fiery Wok -->
          <circle cx="160" cy="140" r="45" fill="#f97316"/>
          <circle cx="160" cy="130" r="30" fill="#facc15"/>
          <!-- Vikram Chef -->
          <circle cx="280" cy="90" r="35" fill="#fed7aa"/>
          <rect x="245" y="125" width="70" height="90" fill="#ffffff"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> MATCH_CUT | <strong>Shot:</strong> Medium Shot | <strong>Move:</strong> Pan Right<br>
        <div class="dialogue">विक्रम: "आर्यन, गरम है! संभल के ले जाना, किसी का ख़ास ऑर्डर है!"</div>
      </div>
    </div>

    <!-- Beat 3 -->
    <div class="card">
      <div class="card-header"><span>BEAT 3: KINETIC LAUNCH [LOW]</span><span>15.0s – 22.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#070e1b"/>
          <!-- Low angle wheel puddle splash -->
          <circle cx="200" cy="160" r="50" fill="#0f172a" stroke="#0284c7" stroke-width="8"/>
          <!-- Water spray -->
          <path d="M140,190 Q200,160 260,190" stroke="#38bdf8" stroke-width="6" fill="none"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> WHIP_PAN | <strong>Shot:</strong> Low-Angle Tracking | <strong>Move:</strong> Fast Parallax<br>
        <div class="dialogue">आर्यन: "चिंता मत करो शेफ़! घड़ी टिक रही है, और मैं उड़ रहा हूँ!"</div>
      </div>
    </div>

    <!-- Beat 4 -->
    <div class="card">
      <div class="card-header"><span>BEAT 4: GRIDLOCK POV [POV]</span><span>22.5s – 30.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#080c14"/>
          <!-- Red tail lights through rain-streaked visor -->
          <circle cx="120" cy="115" r="25" fill="#ef4444" opacity="0.8"/>
          <circle cx="200" cy="115" r="25" fill="#ef4444" opacity="0.8"/>
          <circle cx="300" cy="115" r="25" fill="#ef4444" opacity="0.8"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> HARD_CUT | <strong>Shot:</strong> POV / Extreme CU | <strong>Move:</strong> Camera Shake<br>
        <div class="dialogue">आर्यन: "सिर्फ़ तीन मिनट बचे हैं... रास्ता निकालना ही पड़ेगा!"</div>
      </div>
    </div>

    <!-- Beat 5 -->
    <div class="card">
      <div class="card-header"><span>BEAT 5: FINAL SECONDS [INSERT]</span><span>30.0s – 37.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#180606"/>
          <!-- Ticking countdown clock -->
          <rect x="120" y="60" width="200" height="110" rx="14" fill="#090d16" stroke="#ef4444" stroke-width="6"/>
          <text x="220" y="135" font-family="'Montserrat'" font-size="44" font-weight="900" fill="#ef4444" text-anchor="middle">00:15</text>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> MATCH_CUT | <strong>Shot:</strong> Insert Detail | <strong>Move:</strong> Dolly-Zoom<br>
        <div class="dialogue">[SFX: Rapid heartbeat + ticking countdown beeps + tyre water screech]</div>
      </div>
    </div>

    <!-- Beat 6 -->
    <div class="card">
      <div class="card-header"><span>BEAT 6: ARRIVAL AT GATE [WIDE]</span><span>37.5s – 45.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#06121e"/>
          <!-- Hospital entrance in rain -->
          <rect x="80" y="40" width="280" height="150" fill="#091b29" stroke="#38bdf8" stroke-width="2"/>
          <text x="220" y="80" font-family="'Montserrat'" font-size="14" font-weight="800" fill="#38bdf8" text-anchor="middle">EMERGENCY ENTRANCE</text>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> HARD_CUT | <strong>Shot:</strong> Wide Establishing | <strong>Move:</strong> Deceleration Stop<br>
        <div class="dialogue">आर्यन: "पहुंच गया! ठीक दो सेकंड पहले... अस्पताल का गेट!"</div>
      </div>
    </div>

    <!-- Beat 7 -->
    <div class="card">
      <div class="card-header"><span>BEAT 7: THE SURPRISE [MCU]</span><span>45.0s – 52.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#091316"/>
          <!-- Ananya looking down at birthday pastry -->
          <circle cx="180" cy="100" r="40" fill="#fed7aa"/>
          <rect x="145" y="140" width="70" height="80" fill="#059669"/>
          <!-- Strawberry pastry with glowing candle -->
          <rect x="250" y="120" width="80" height="40" rx="8" fill="#fda4af"/>
          <circle cx="290" cy="105" r="8" fill="#facc15"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> HARD_CUT | <strong>Shot:</strong> Medium Close-Up | <strong>Move:</strong> Slow Push-In<br>
        <div class="dialogue">अनन्या: "माँ... तुम्हें याद था? आज छत्तीस घंटे की ड्यूटी के बाद... ये सबसे खूबसूरत सरप्राइज़ है।"</div>
      </div>
    </div>

    <!-- Beat 8 -->
    <div class="card">
      <div class="card-header"><span>BEAT 8: OUTRO SMILE [MED]</span><span>52.5s – 60.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#070a12"/>
          <circle cx="150" cy="115" r="40" fill="#fdba74"/>
          <!-- Salute arm -->
          <line x1="175" y1="140" x2="200" y2="85" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
          <circle cx="290" cy="110" r="38" fill="#fed7aa"/>
          <rect x="110" y="15" width="220" height="30" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="220" y="35" font-family="'Noto Sans Devanagari'" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">कोड रेड: डिलीवरी</text>
        </svg>
      </div>
      <div class="meta">
        <strong>Cut:</strong> CROSSFADE | <strong>Shot:</strong> Medium Shot | <strong>Move:</strong> Pull Back<br>
        <div class="dialogue">आर्यन: "हैप्पी बर्थडे डॉक्टर साहिबा! आपकी मुस्कान ही हमारी मंज़िल थी।"</div>
      </div>
    </div>
  </div>
</body>
</html>"""

render_html_to_png(storyboard_html, os.path.join(STORY_DIR, "storyboard_master.png"))

# Also render individual 8 keyframe stills
keyframes = [
    ("scene_01_key.png", "BEAT 1: THE 10-MINUTE COUNTDOWN", "0.0s – 7.5s", "#180606",
     """
     <rect x='660' y='240' width='600' height='600' rx='36' fill='#090d16' stroke='#ef4444' stroke-width='10'/>
     <text x='960' y='360' font-family="'Montserrat'" font-size='36' font-weight='900' fill='#ef4444' text-anchor='middle'>URGENT ORDER #402</text>
     <text x='960' y='540' font-family="'Montserrat'" font-size='120' font-weight='900' fill='#ffffff' text-anchor='middle'>09:59</text>
     <text x='960' y='660' font-family="'Montserrat'" font-size='32' font-weight='700' fill='#fca5a5' text-anchor='middle'>CANCEL IN 10 MINUTES</text>
     """,
     "आर्यन: \"दस मिनट... और पूरा शहर ट्रैफ़िक में डूबा है! पर ये ऑर्डर कैंसल नहीं होगा!\""),

    ("scene_02_key.png", "BEAT 2: THE CHAOTIC CLOUD KITCHEN", "7.5s – 15.0s", "#1c0e08",
     """
     <circle cx='600' cy='620' r='140' fill='#f97316'/>
     <circle cx='600' cy='580' r='90' fill='#facc15'/>
     <circle cx='1200' cy='420' r='120' fill='#fed7aa'/>
     <rect x='1120' y='540' width='160' height='300' fill='#ffffff'/>
     """,
     "विक्रम: \"आर्यन, गरम है! संभल के ले जाना, किसी का ख़ास ऑर्डर है!\""),

    ("scene_03_key.png", "BEAT 3: KINETIC LAUNCH", "15.0s – 22.5s", "#070e1b",
     """
     <circle cx='800' cy='650' r='160' fill='#0f172a' stroke='#0284c7' stroke-width='24'/>
     <path d='M500,780 Q800,640 1100,780' stroke='#38bdf8' stroke-width='18' fill='none'/>
     """,
     "आर्यन: \"चिंता मत करो शेफ़! घड़ी टिक रही है, और मैं उड़ रहा हूँ!\""),

    ("scene_04_key.png", "BEAT 4: THE TRAFFIC GRIDLOCK", "22.5s – 30.0s", "#080c14",
     """
     <circle cx='500' cy='500' r='80' fill='#ef4444' opacity='0.85'/>
     <circle cx='850' cy='500' r='80' fill='#ef4444' opacity='0.85'/>
     <circle cx='1300' cy='500' r='80' fill='#ef4444' opacity='0.85'/>
     """,
     "आर्यन: \"सिर्फ़ तीन मिनट बचे हैं... रास्ता निकालना ही पड़ेगा!\""),

    ("scene_05_key.png", "BEAT 5: THE FINAL SECONDS", "30.0s – 37.5s", "#180606",
     """
     <rect x='560' y='320' width='800' height='440' rx='30' fill='#090d16' stroke='#ef4444' stroke-width='12'/>
     <text x='960' y='580' font-family="'Montserrat'" font-size='160' font-weight='900' fill='#ef4444' text-anchor='middle'>00:15</text>
     """,
     "[SFX: Rapid heartbeat + ticking countdown beeps + tyre water screech]"),

    ("scene_06_key.png", "BEAT 6: ARRIVAL AT ST. MARTHA'S", "37.5s – 45.0s", "#06121e",
     """
     <rect x='360' y='220' width='1200' height='580' fill='#091b29' stroke='#38bdf8' stroke-width='6'/>
     <text x='960' y='380' font-family="'Montserrat'" font-size='56' font-weight='900' fill='#38bdf8' text-anchor='middle'>ST. MARTHA'S HOSPITAL</text>
     <text x='960' y='460' font-family="'Montserrat'" font-size='38' font-weight='800' fill='#ef4444' text-anchor='middle'>EMERGENCY / TRAUMA CARE</text>
     """,
     "आर्यन: \"पहुंच गया! ठीक दो सेकंड पहले... अस्पताल का गेट!\""),

    ("scene_07_key.png", "BEAT 7: THE BIRTHDAY SURPRISE", "45.0s – 52.5s", "#091316",
     """
     <circle cx='680' cy='460' r='130' fill='#fed7aa'/>
     <rect x='580' y='590' width='200' height='280' fill='#059669'/>
     <rect x='1080' y='500' width='360' height='200' rx='20' fill='#fda4af' stroke='#e11d48' stroke-width='6'/>
     <line x1='1260' y1='500' x2='1260' y2='420' stroke='#ffffff' stroke-width='8'/>
     <circle cx='1260' cy='400' r='20' fill='#facc15'/>
     """,
     "अनन्या: \"माँ... तुम्हें याद था? आज छत्तीस घंटे की ड्यूटी के बाद... ये सबसे खूबसूरत सरप्राइज़ है।\""),

    ("scene_08_key.png", "BEAT 8: TRIUMPH & SMILE", "52.5s – 60.0s", "#070a12",
     """
     <circle cx='650' cy='480' r='120' fill='#fdba74'/>
     <line x1='730' y1='540' x2='820' y2='380' stroke='#0284c7' stroke-width='36' stroke-linecap='round'/>
     <circle cx='1250' cy='480' r='120' fill='#fed7aa'/>
     <rect x='460' y='140' width='1000' height='120' rx='16' fill='#0f172a' stroke='#38bdf8' stroke-width='4'/>
     <text x='960' y='215' font-family=\"'Noto Sans Devanagari'\" font-size='46' font-weight='800' fill='#ffffff' text-anchor='middle'>कोड रेड: डिलीवरी</text>
     """,
     "आर्यन: \"हैप्पी बर्थडे डॉक्टर साहिबा! आपकी मुस्कान ही हमारी मंज़िल थी।\"")
]

for filename, title, timing, bg, svg_body, dialogue in keyframes:
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
    border-bottom: 3px solid #0284c7; padding-bottom: 12px;
  }}
  .header h2 {{ font-size: 32px; font-weight: 900; margin: 0; letter-spacing: 1px; color: #38bdf8; }}
  .header .time {{ font-size: 26px; font-weight: 800; color: #f59e0b; }}
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

    out_file = os.path.join(STORY_DIR, filename)
    render_html_to_png(html, out_file)

print("Character sheets and storyboards rendered successfully!")
