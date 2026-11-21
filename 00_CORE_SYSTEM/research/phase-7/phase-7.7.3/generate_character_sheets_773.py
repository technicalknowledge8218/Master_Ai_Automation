"""
generate_character_sheets_773.py
================================
Generates broadcast-grade 2D Character Design Sheets for:
- Kabir (23, Junior Game Developer)
- Meera (24, Senior Game Animator / Pragmatic Co-founder)
Includes:
- Full body turnarounds (Front, 3/4 Hero, Side)
- Expression Matrix (Panic, Focus, Disbelief, Deadpan Smirk, Triumphant Grin)
- Complete color palettes with hex swatches
- Anatomical and costuming callouts
Rendered at 1920x1080 Full HD using Chromium (Blink/HarfBuzz/Skia).
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3\character_sheets"
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

# =============================================================================
# 1. KABIR CHARACTER DESIGN SHEET (1920x1080)
# =============================================================================
kabir_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 25px 35px;
    background: #0b0f19; color: #f1f5f9;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px; overflow: hidden;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid #f97316; padding-bottom: 12px; margin-bottom: 20px;
  }
  .title-block h1 {
    font-size: 34px; font-weight: 800; margin: 0; color: #ffffff;
  }
  .title-block .sub {
    font-size: 15px; color: #f97316; font-weight: 600; margin-top: 4px; text-transform: uppercase; letter-spacing: 2px;
  }
  .grid {
    display: grid; grid-template-columns: 2fr 3fr; gap: 25px; height: 920px;
  }
  .panel {
    background: #141b2a; border: 1px solid #243044; border-radius: 12px; padding: 22px; position: relative;
  }
  .panel-title {
    font-size: 15px; font-weight: 700; color: #f97316; text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 12px; border-bottom: 1px solid #243044; padding-bottom: 6px;
  }
  .turnarounds {
    display: flex; justify-content: space-around; align-items: flex-end; height: 620px;
  }
  .figure-box { text-align: center; }
  .figure-label {
    margin-top: 8px; font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase;
  }
  .expressions-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px;
  }
  .expr-box {
    background: #0f1522; border: 1px solid #202b3c; border-radius: 8px; padding: 12px; text-align: center;
  }
  .expr-title { font-size: 13px; font-weight: 700; color: #f8fafc; margin-top: 6px; }
  .expr-desc { font-size: 11px; color: #64748b; margin-top: 2px; }
  .palette { display: flex; gap: 14px; margin-top: 18px; align-items: center; }
  .swatch { display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .color-chip { width: 48px; height: 48px; border-radius: 8px; border: 2px solid rgba(255,255,255,0.1); }
  .hex { font-size: 10px; font-weight: 600; color: #94a3b8; }
  .callouts { margin-top: 18px; font-size: 12.5px; line-height: 1.55; color: #cbd5e1; }
  .callouts li { margin-bottom: 5px; }
  .callouts strong { color: #f97316; }
</style>
</head>
<body>

  <div class="header">
    <div class="title-block">
      <h1>CHARACTER SHEET: KABIR (कबीर)</h1>
      <div class="sub">Protagonist • Junior Game Developer • Age: 23 • Bengaluru</div>
    </div>
    <div style="text-align:right; font-size:13px; color:#94a3b8;">
      Film: <strong>"लास्ट बग" (The Last Bug)</strong> • Phase: <strong>7.7.3 60s Animated Short</strong><br>
      Visual Style: <strong>Contemporary High-Fidelity 2D Digital Vector Art</strong>
    </div>
  </div>

  <div class="grid">
    <!-- LEFT: FULL BODY VIEWS & PALETTE -->
    <div class="panel">
      <div class="panel-title">1. Full Body Turnaround (Height: 7.2 Heads)</div>
      <div class="turnarounds">
        <!-- Front View -->
        <div class="figure-box">
          <svg width="220" height="580" viewBox="0 0 220 580">
            <defs>
              <linearGradient id="hoodieGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fb923c"/>
                <stop offset="100%" stop-color="#ea580c"/>
              </linearGradient>
            </defs>
            <!-- High-Top Sneakers -->
            <path d="M68 450 L65 540 L50 565 L82 565 L82 450 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
            <path d="M152 450 L155 540 L138 565 L170 565 L138 450 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
            <!-- Dark Grey Cargo Joggers -->
            <path d="M62 300 L68 455 L88 455 L110 325 L132 455 L152 455 L158 300 Z" fill="#334155"/>
            <!-- Oversized Coral Hoodie -->
            <path d="M42 165 L32 310 L75 320 L110 315 L145 320 L188 310 L178 165 Z" fill="url(#hoodieGrad)"/>
            <!-- Pouch Pocket & White Drawstrings -->
            <path d="M65 240 L155 240 L145 305 L75 305 Z" fill="#c2410c"/>
            <line x1="102" y1="165" x2="98" y2="215" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
            <line x1="118" y1="165" x2="122" y2="215" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
            <!-- Neck & Face -->
            <path d="M96 125 L124 125 L120 165 L100 165 Z" fill="#fdba74"/>
            <path d="M80 65 Q110 42 140 65 Q145 110 110 132 Q75 110 80 65 Z" fill="#fdba74"/>
            <!-- Expressive Eyes -->
            <ellipse cx="96" cy="88" rx="7" ry="5" fill="#ffffff"/>
            <circle cx="97" cy="88" r="3.5" fill="#78350f"/>
            <circle cx="95" cy="86" r="1.2" fill="#ffffff"/>
            <ellipse cx="124" cy="88" rx="7" ry="5" fill="#ffffff"/>
            <circle cx="123" cy="88" r="3.5" fill="#78350f"/>
            <circle cx="121" cy="86" r="1.2" fill="#ffffff"/>
            <path d="M88 78 Q96 74 104 78" stroke="#18181b" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M116 78 Q124 74 132 78" stroke="#18181b" stroke-width="2.5" stroke-linecap="round"/>
            <!-- Nose & Open Mouth -->
            <path d="M108 92 L111 102 L106 104" stroke="#ea580c" stroke-width="1.8" stroke-linecap="round" fill="none"/>
            <path d="M102 114 Q110 118 118 114" stroke="#78350f" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <!-- Messy Curls popping under Backwards Cap -->
            <path d="M78 65 C70 45, 150 45, 142 65 C146 80, 142 95, 138 100 C132 65, 126 52, 110 50 C85 52, 82 68, 78 100 Z" fill="#18181b"/>
            <!-- Backwards Slate Baseball Cap -->
            <path d="M74 62 Q110 32 146 62 Q148 48 110 40 Q72 48 74 62 Z" fill="#475569"/>
            <path d="M68 62 L90 58 L85 68 Z" fill="#334155"/> <!-- Cap Brim turned backwards -->
          </svg>
          <div class="figure-label">Front View</div>
        </div>

        <!-- 3/4 Hero View (Hands on Head in Crisis Panic) -->
        <div class="figure-box">
          <svg width="220" height="580" viewBox="0 0 220 580">
            <!-- Legs 3/4 -->
            <path d="M75 450 L75 540 L60 565 L92 565 L90 450 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
            <path d="M135 450 L140 540 L125 565 L158 565 L148 450 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
            <path d="M68 300 L75 455 L95 455 L112 325 L125 455 L145 455 L152 300 Z" fill="#334155"/>
            <!-- Hoodie 3/4 -->
            <path d="M55 165 L45 315 L88 322 L112 315 L140 322 L175 310 L168 165 Z" fill="url(#hoodieGrad)"/>
            <!-- Arms raised to head in panic! -->
            <path d="M52 175 L25 110 L55 90 L75 165 Z" fill="#ea580c"/>
            <path d="M168 175 L195 110 L165 90 L145 165 Z" fill="#ea580c"/>
            <ellipse cx="45" cy="85" rx="15" ry="12" fill="#fdba74"/>
            <ellipse cx="175" cy="85" rx="15" ry="12" fill="#fdba74"/>
            <!-- Head 3/4 -->
            <path d="M96 125 L120 128 L116 165 L96 165 Z" fill="#fdba74"/>
            <path d="M78 65 Q106 42 136 62 Q144 110 112 132 Q76 110 78 65 Z" fill="#fdba74"/>
            <!-- Shocked Saucer Eyes -->
            <ellipse cx="94" cy="88" rx="8" ry="7" fill="#ffffff"/>
            <circle cx="94" cy="88" r="4.2" fill="#78350f"/>
            <circle cx="92" cy="85" r="1.5" fill="#ffffff"/>
            <ellipse cx="122" cy="88" rx="8" ry="7" fill="#ffffff"/>
            <circle cx="122" cy="88" r="4.2" fill="#78350f"/>
            <circle cx="120" cy="85" r="1.5" fill="#ffffff"/>
            <!-- Distressed Eyebrows & Dropped Mouth -->
            <path d="M86 78 Q96 82 104 76" stroke="#18181b" stroke-width="2.6" fill="none"/>
            <path d="M114 76 Q122 82 132 78" stroke="#18181b" stroke-width="2.6" fill="none"/>
            <ellipse cx="108" cy="116" rx="9" ry="12" fill="#451a03"/>
            <!-- Cap 3/4 -->
            <path d="M72 62 Q108 32 144 60 Q146 48 108 40 Q70 48 72 62 Z" fill="#475569"/>
            <path d="M66 62 L88 56 L83 66 Z" fill="#334155"/>
          </svg>
          <div class="figure-label">3/4 Hero (Panic Pose)</div>
        </div>
      </div>

      <div class="palette">
        <span style="font-size:11px; font-weight:700; color:#f97316; text-transform:uppercase;">Color Palette:</span>
        <div class="swatch"><div class="color-chip" style="background:#fdba74;"></div><div class="hex">#FDBA74<br>Skin</div></div>
        <div class="swatch"><div class="color-chip" style="background:#f97316;"></div><div class="hex">#F97316<br>Coral Hoodie</div></div>
        <div class="swatch"><div class="color-chip" style="background:#334155;"></div><div class="hex">#334155<br>Cargos</div></div>
        <div class="swatch"><div class="color-chip" style="background:#475569;"></div><div class="hex">#475569<br>Cap</div></div>
        <div class="swatch"><div class="color-chip" style="background:#38bdf8;"></div><div class="hex">#38bdf8<br>High-Tops</div></div>
      </div>
    </div>

    <!-- RIGHT: FACIAL EXPRESSIONS & STYLING RULES -->
    <div class="panel">
      <div class="panel-title">2. Facial Expressions Matrix</div>
      <div class="expressions-grid">
        <!-- 1. Panic Alarm -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 45 Q70 20 102 45 Q106 85 70 110 Q34 85 38 45 Z" fill="#fdba74"/>
            <!-- Giant shocked pupils -->
            <ellipse cx="54" cy="62" rx="9" ry="8" fill="#ffffff"/>
            <circle cx="54" cy="62" r="5" fill="#78350f"/>
            <ellipse cx="86" cy="62" rx="9" ry="8" fill="#ffffff"/>
            <circle cx="86" cy="62" r="5" fill="#78350f"/>
            <path d="M46 50 Q56 55 64 48" stroke="#18181b" stroke-width="2.6" fill="none"/>
            <path d="M76 48 Q84 55 94 50" stroke="#18181b" stroke-width="2.6" fill="none"/>
            <!-- Big open yelling mouth -->
            <ellipse cx="70" cy="92" rx="14" ry="16" fill="#451a03"/>
            <ellipse cx="70" cy="85" rx="9" ry="6" fill="#ef4444"/>
            <!-- Sweat drop on temple -->
            <path d="M98 48 Q104 56 98 62 Q92 56 98 48 Z" fill="#38bdf8"/>
            <path d="M34 45 Q70 15 106 45 Q108 30 70 24 Q32 30 34 45 Z" fill="#475569"/>
          </svg>
          <div class="expr-title">1. Code Red Panic</div>
          <div class="expr-desc">"सर्वनाश हो गया! गेम क्रैश हो रहा है!"</div>
        </div>

        <!-- 2. Stunned Disbelief -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 45 Q70 20 102 45 Q106 85 70 110 Q34 85 38 45 Z" fill="#fdba74"/>
            <!-- Saucer eyes -->
            <ellipse cx="54" cy="62" rx="10" ry="9" fill="#ffffff"/>
            <circle cx="54" cy="62" r="4.5" fill="#78350f"/>
            <ellipse cx="86" cy="62" rx="10" ry="9" fill="#ffffff"/>
            <circle cx="86" cy="62" r="4.5" fill="#78350f"/>
            <path d="M46 48 L64 48" stroke="#18181b" stroke-width="2.2"/>
            <path d="M76 48 L94 48" stroke="#18181b" stroke-width="2.2"/>
            <!-- Slack horizontal open jaw -->
            <rect x="58" y="86" width="24" height="18" rx="6" fill="#451a03"/>
            <path d="M34 45 Q70 15 106 45 Q108 30 70 24 Q32 30 34 45 Z" fill="#475569"/>
          </svg>
          <div class="expr-title">2. Stunned Slack-Jaw</div>
          <div class="expr-desc">When Meera lifts the Bhujia packet</div>
        </div>

        <!-- 3. Sheepish Laugh -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 45 Q70 20 102 45 Q106 85 70 110 Q34 85 38 45 Z" fill="#fdba74"/>
            <!-- Crinkled happy eyes -->
            <path d="M46 62 Q54 68 62 62" stroke="#18181b" stroke-width="2.5" fill="none"/>
            <path d="M78 62 Q86 68 94 62" stroke="#18181b" stroke-width="2.5" fill="none"/>
            <!-- Wide sheepish grin -->
            <path d="M52 82 Q70 96 88 82 Z" fill="#c2410c"/>
            <path d="M54 84 Q70 90 86 84 Z" fill="#ffffff"/>
            <path d="M34 45 Q70 15 106 45 Q108 30 70 24 Q32 30 34 45 Z" fill="#475569"/>
          </svg>
          <div class="expr-title">3. Sheepish Relief</div>
          <div class="expr-desc">Laughing at himself as app deploys</div>
        </div>
      </div>

      <div class="panel-title" style="margin-top:20px;">3. Anatomy, Rigging & Styling Rules</div>
      <ul class="callouts">
        <li><strong>Anatomy & Proportions:</strong> Head-to-body ratio is exactly 1:7.2. Long dynamic limbs suitable for high-energy comedic exaggeration.</li>
        <li><strong>Facial Construction:</strong> Elastic, highly expressive facial landmarks; hazel pupils with specular glints; expressive brow curves.</li>
        <li><strong>Clothing Folds:</strong> Oversized coral hoodie features organic drape folds around elbows and kangaroo pouch.</li>
        <li><strong>Personality:</strong> Hyper-focused, prone to catastrophizing, deeply passionate about his code, takes himself a little too seriously until proven comically wrong.</li>
      </ul>
    </div>
  </div>

</body>
</html>"""
render_html_to_png(kabir_html, os.path.join(OUTPUT_DIR, "kabir_character_sheet.png"))

# =============================================================================
# 2. MEERA CHARACTER DESIGN SHEET (1920x1080)
# =============================================================================
meera_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 25px 35px;
    background: #0b0f19; color: #f1f5f9;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px; overflow: hidden;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid #8b5cf6; padding-bottom: 12px; margin-bottom: 20px;
  }
  .title-block h1 {
    font-size: 34px; font-weight: 800; margin: 0; color: #ffffff;
  }
  .title-block .sub {
    font-size: 15px; color: #a78bfa; font-weight: 600; margin-top: 4px; text-transform: uppercase; letter-spacing: 2px;
  }
  .grid {
    display: grid; grid-template-columns: 2fr 3fr; gap: 25px; height: 920px;
  }
  .panel {
    background: #141b2a; border: 1px solid #243044; border-radius: 12px; padding: 22px; position: relative;
  }
  .panel-title {
    font-size: 15px; font-weight: 700; color: #a78bfa; text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 12px; border-bottom: 1px solid #243044; padding-bottom: 6px;
  }
  .turnarounds {
    display: flex; justify-content: space-around; align-items: flex-end; height: 620px;
  }
  .figure-box { text-align: center; }
  .figure-label {
    margin-top: 8px; font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase;
  }
  .expressions-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px;
  }
  .expr-box {
    background: #0f1522; border: 1px solid #202b3c; border-radius: 8px; padding: 12px; text-align: center;
  }
  .expr-title { font-size: 13px; font-weight: 700; color: #f8fafc; margin-top: 6px; }
  .expr-desc { font-size: 11px; color: #64748b; margin-top: 2px; }
  .palette { display: flex; gap: 14px; margin-top: 18px; align-items: center; }
  .swatch { display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .color-chip { width: 48px; height: 48px; border-radius: 8px; border: 2px solid rgba(255,255,255,0.1); }
  .hex { font-size: 10px; font-weight: 600; color: #94a3b8; }
  .callouts { margin-top: 18px; font-size: 12.5px; line-height: 1.55; color: #cbd5e1; }
  .callouts li { margin-bottom: 5px; }
  .callouts strong { color: #a78bfa; }
</style>
</head>
<body>

  <div class="header">
    <div class="title-block">
      <h1>CHARACTER SHEET: MEERA (मीरा)</h1>
      <div class="sub">Deuteragonist • Lead Game Animator • Age: 24 • Bengaluru</div>
    </div>
    <div style="text-align:right; font-size:13px; color:#94a3b8;">
      Film: <strong>"लास्ट बग" (The Last Bug)</strong> • Phase: <strong>7.7.3 60s Animated Short</strong><br>
      Visual Style: <strong>Contemporary High-Fidelity 2D Digital Vector Art</strong>
    </div>
  </div>

  <div class="grid">
    <!-- LEFT: FULL BODY VIEWS & PALETTE -->
    <div class="panel">
      <div class="panel-title">1. Full Body Turnaround (Height: 7 Heads)</div>
      <div class="turnarounds">
        <!-- Front View -->
        <div class="figure-box">
          <svg width="220" height="580" viewBox="0 0 220 580">
            <defs>
              <linearGradient id="denimGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#3b82f6"/>
                <stop offset="100%" stop-color="#1d4ed8"/>
              </linearGradient>
            </defs>
            <!-- Minimalist White Sneakers -->
            <path d="M72 440 L70 535 L58 560 L88 560 L88 440 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M148 440 L150 535 L132 560 L162 560 L132 440 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <!-- High-Waisted Black Cigarette Trousers -->
            <path d="M68 280 L72 445 L92 445 L110 315 L128 445 L148 445 L152 280 Z" fill="#18181b"/>
            <!-- Washed Denim Jacket over Cream Turtleneck -->
            <path d="M48 160 L38 310 L82 320 L110 315 L138 320 L182 310 L172 160 Z" fill="url(#denimGrad)"/>
            <path d="M85 140 L110 240 L135 140 Z" fill="#fef3c7"/> <!-- Cream Turtleneck -->
            <!-- Denim Collar -->
            <path d="M85 155 Q110 170 135 155 L138 168 Q110 185 82 168 Z" fill="#1e40af"/>
            <!-- Neck & Face -->
            <path d="M96 115 L124 115 L120 150 L100 150 Z" fill="#fed7aa"/>
            <path d="M82 60 Q110 40 138 60 Q145 100 110 122 Q75 100 82 60 Z" fill="#fed7aa"/>
            <!-- Circular Wire-Rim Glasses -->
            <circle cx="96" cy="80" r="14" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="124" cy="80" r="14" fill="none" stroke="#d97706" stroke-width="2"/>
            <line x1="110" y1="80" x2="110" y2="80" stroke="#d97706" stroke-width="2.5"/>
            <!-- Eyes behind Glasses -->
            <ellipse cx="96" cy="80" rx="5" ry="3.5" fill="#ffffff"/>
            <circle cx="96" cy="80" r="2.5" fill="#312e81"/>
            <circle cx="95" cy="79" r="0.8" fill="#ffffff"/>
            <ellipse cx="124" cy="80" rx="5" ry="3.5" fill="#ffffff"/>
            <circle cx="124" cy="80" r="2.5" fill="#312e81"/>
            <circle cx="123" cy="79" r="0.8" fill="#ffffff"/>
            <path d="M90 73 Q96 70 102 73" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <path d="M118 73 Q124 70 130 73" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <!-- Nose & Calm Smile -->
            <path d="M109 84 L111 92 L107 93" stroke="#ea580c" stroke-width="1.4" fill="none"/>
            <path d="M103 104 Q110 107 117 104" stroke="#9333ea" stroke-width="2.2" stroke-linecap="round" fill="none"/>
            <!-- Chic High Bun with Lavender Streak -->
            <path d="M78 60 C75 25, 145 25, 142 60 C146 80, 142 95, 138 100 C132 65, 126 52, 110 50 C85 52, 82 68, 78 100 Z" fill="#18181b"/>
            <!-- Top Bun -->
            <circle cx="110" cy="24" r="22" fill="#18181b"/>
            <!-- Lavender Accent Streak framing cheek -->
            <path d="M82 50 Q75 80 84 105" stroke="#c084fc" stroke-width="4.5" stroke-linecap="round" fill="none"/>
            <!-- Silver Hoop Earrings -->
            <circle cx="78" cy="82" r="5" fill="none" stroke="#e2e8f0" stroke-width="1.8"/>
            <circle cx="142" cy="82" r="5" fill="none" stroke="#e2e8f0" stroke-width="1.8"/>
          </svg>
          <div class="figure-label">Front View</div>
        </div>

        <!-- 3/4 Hero View (Holding Ceramic Coffee Mug with Deadpan Smirk) -->
        <div class="figure-box">
          <svg width="220" height="580" viewBox="0 0 220 580">
            <!-- Legs 3/4 -->
            <path d="M78 440 L80 535 L68 560 L98 560 L96 440 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M125 440 L132 535 L120 560 L150 560 L140 440 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M72 280 L78 445 L98 445 L112 315 L122 445 L144 445 L148 280 Z" fill="#18181b"/>
            <!-- Denim Jacket 3/4 -->
            <path d="M55 160 L45 315 L90 325 L115 318 L142 325 L175 310 L168 160 Z" fill="url(#denimGrad)"/>
            <path d="M85 140 L108 240 L130 140 Z" fill="#fef3c7"/>
            <!-- Head 3/4 -->
            <path d="M96 115 L120 118 L116 150 L96 150 Z" fill="#fed7aa"/>
            <path d="M78 60 Q106 40 136 58 Q144 98 112 122 Q76 100 78 60 Z" fill="#fed7aa"/>
            <!-- Glasses 3/4 -->
            <circle cx="95" cy="80" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="122" cy="80" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <line x1="108" y1="80" x2="110" y2="80" stroke="#d97706" stroke-width="2.5"/>
            <circle cx="95" cy="80" r="2.5" fill="#312e81"/>
            <circle cx="122" cy="80" r="2.5" fill="#312e81"/>
            <!-- Smirk -->
            <path d="M101 104 Q110 108 120 101" stroke="#9333ea" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <!-- Bun & Lavender Hair -->
            <circle cx="115" cy="24" r="22" fill="#18181b"/>
            <path d="M78 50 Q72 80 82 105" stroke="#c084fc" stroke-width="4.5" stroke-linecap="round" fill="none"/>
            <!-- Hand holding Ceramic Coffee Mug -->
            <path d="M158 165 L175 235 L145 245 L135 185 Z" fill="#1e40af"/>
            <!-- Yellow Ceramic Coffee Mug -->
            <rect x="135" y="235" width="28" height="32" rx="4" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
            <path d="M163 242 Q172 251 163 260" stroke="#d97706" stroke-width="2.5" fill="none"/>
          </svg>
          <div class="figure-label">3/4 Hero (Coffee Pose)</div>
        </div>
      </div>

      <div class="palette">
        <span style="font-size:11px; font-weight:700; color:#a78bfa; text-transform:uppercase;">Color Palette:</span>
        <div class="swatch"><div class="color-chip" style="background:#fed7aa;"></div><div class="hex">#FED7AA<br>Skin</div></div>
        <div class="swatch"><div class="color-chip" style="background:#2563eb;"></div><div class="hex">#2563EB<br>Denim Blue</div></div>
        <div class="swatch"><div class="color-chip" style="background:#c084fc;"></div><div class="hex">#C084FC<br>Lavender Streak</div></div>
        <div class="swatch"><div class="color-chip" style="background:#d97706;"></div><div class="hex">#D97706<br>Gold Glasses</div></div>
        <div class="swatch"><div class="color-chip" style="background:#fbbf24;"></div><div class="hex">#FBBF24<br>Coffee Mug</div></div>
      </div>
    </div>

    <!-- RIGHT: FACIAL EXPRESSIONS & STYLING RULES -->
    <div class="panel">
      <div class="panel-title">2. Facial Expressions Matrix</div>
      <div class="expressions-grid">
        <!-- 1. Calm Sarcasm -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 42 Q70 20 102 42 Q106 80 70 105 Q34 80 38 42 Z" fill="#fed7aa"/>
            <circle cx="56" cy="62" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="84" cy="62" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="56" cy="62" r="2.5" fill="#312e81"/>
            <circle cx="84" cy="62" r="2.5" fill="#312e81"/>
            <!-- One arched brow over glasses -->
            <path d="M48 55 Q56 52 64 55" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <path d="M76 49 Q84 44 92 50" stroke="#0f172a" stroke-width="2.4" fill="none"/>
            <!-- Sarcastic smirk -->
            <path d="M62 88 Q70 90 80 84" stroke="#9333ea" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <circle cx="70" cy="18" r="18" fill="#18181b"/>
            <path d="M42 42 Q36 70 45 92" stroke="#c084fc" stroke-width="4" stroke-linecap="round" fill="none"/>
          </svg>
          <div class="expr-title">1. Sarcastic Calm</div>
          <div class="expr-desc">"शांत हो जाओ कोडिंग के शेरलॉक!"</div>
        </div>

        <!-- 2. Sharp Focus -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 42 Q70 20 102 42 Q106 80 70 105 Q34 80 38 42 Z" fill="#fed7aa"/>
            <circle cx="56" cy="62" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="84" cy="62" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="58" cy="62" r="2.5" fill="#312e81"/>
            <circle cx="86" cy="62" r="2.5" fill="#312e81"/>
            <path d="M48 52 L64 52" stroke="#0f172a" stroke-width="2.2"/>
            <path d="M76 52 L92 52" stroke="#0f172a" stroke-width="2.2"/>
            <line x1="64" y1="88" x2="76" y2="88" stroke="#9333ea" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="70" cy="18" r="18" fill="#18181b"/>
            <path d="M42 42 Q36 70 45 92" stroke="#c084fc" stroke-width="4" stroke-linecap="round" fill="none"/>
          </svg>
          <div class="expr-title">2. Diagnosing Error</div>
          <div class="expr-desc">Inspecting mechanical keyboard</div>
        </div>

        <!-- 3. Triumphant Punchline -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 42 Q70 20 102 42 Q106 80 70 105 Q34 80 38 42 Z" fill="#fed7aa"/>
            <circle cx="56" cy="62" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="84" cy="62" r="13" fill="none" stroke="#d97706" stroke-width="2"/>
            <circle cx="56" cy="62" r="2.5" fill="#312e81"/>
            <circle cx="84" cy="62" r="2.5" fill="#312e81"/>
            <path d="M48 54 Q56 50 64 54" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <path d="M76 54 Q84 50 92 54" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <!-- Open amused grin -->
            <path d="M58 84 Q70 94 82 84 Z" fill="#9333ea"/>
            <path d="M60 85 Q70 90 80 85 Z" fill="#ffffff"/>
            <circle cx="70" cy="18" r="18" fill="#18181b"/>
            <path d="M42 42 Q36 70 45 92" stroke="#c084fc" stroke-width="4" stroke-linecap="round" fill="none"/>
          </svg>
          <div class="expr-title">3. The Bhujia Reveal</div>
          <div class="expr-desc">"इंटरनेशनल हैकर था... भुजिया!"</div>
        </div>
      </div>

      <div class="panel-title" style="margin-top:20px;">3. Anatomy, Rigging & Styling Rules</div>
      <ul class="callouts">
        <li><strong>Anatomy & Proportions:</strong> Head-to-body ratio is exactly 1:7. Poised, confident, upright posture.</li>
        <li><strong>Distinctive Silhouette:</strong> High top-knot bun with lavender hair streak and circular gold glasses create instant visual recognition.</li>
        <li><strong>Costuming:</strong> Indigo washed denim jacket over warm cream turtleneck; clean graphic linework.</li>
        <li><strong>Personality:</strong> Pragmatic, unbothered, razor-sharp detective intuition; loves teasing Kabir's over-dramatic tech panic.</li>
      </ul>
    </div>
  </div>

</body>
</html>"""
render_html_to_png(meera_html, os.path.join(OUTPUT_DIR, "meera_character_sheet.png"))

print("Both Character Sheets Generated Successfully in 1080p!")
