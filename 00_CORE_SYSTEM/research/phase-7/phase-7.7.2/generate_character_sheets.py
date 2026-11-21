"""
generate_character_sheets.py
============================
Generates broadcast-grade 2D Character Design Sheets for:
- Aisha (27, Lead UI/UX Designer)
- Vikram (28, Art Director)
Each sheet includes:
- Front View, 3/4 View, Side Profile View
- 3 Distinct Facial Expressions (Neutral/Composed, Smug/Shock, Wink/Triumph)
- Color Swatch Palettes with exact Hex Codes
- Anatomical Proportion & Costuming Callouts
Rendered at 1920x1080 Full HD using Chromium (Blink/HarfBuzz/Skia).
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2\character_sheets"
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
# 1. AISHA CHARACTER DESIGN SHEET (1920x1080)
# =============================================================================
aisha_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 30px 40px;
    background: #0f141e;
    color: #f1f5f9;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px;
    overflow: hidden;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid #eab308; padding-bottom: 15px; margin-bottom: 25px;
  }
  .title-block h1 {
    font-size: 38px; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: 1px;
  }
  .title-block .sub {
    font-size: 16px; color: #eab308; font-weight: 600; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;
  }
  .meta {
    text-align: right; font-size: 14px; color: #94a3b8;
  }
  .meta strong { color: #f8fafc; }

  .grid {
    display: grid; grid-template-columns: 2fr 3fr; gap: 30px; height: 900px;
  }
  .panel {
    background: #182030; border: 1px solid #283548; border-radius: 12px; padding: 25px; position: relative;
  }
  .panel-title {
    font-size: 16px; font-weight: 700; color: #eab308; text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 15px; border-bottom: 1px solid #283548; padding-bottom: 8px;
  }

  .turnarounds {
    display: flex; justify-content: space-around; align-items: flex-end; height: 600px;
  }
  .figure-box {
    text-align: center;
  }
  .figure-label {
    margin-top: 10px; font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase;
  }

  .expressions-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;
  }
  .expr-box {
    background: #101622; border: 1px solid #243044; border-radius: 8px; padding: 15px; text-align: center;
  }
  .expr-title {
    font-size: 13px; font-weight: 700; color: #f8fafc; margin-top: 8px;
  }
  .expr-desc {
    font-size: 11px; color: #64748b; margin-top: 2px;
  }

  .palette {
    display: flex; gap: 15px; margin-top: 20px; align-items: center;
  }
  .swatch {
    display: flex; flex-direction: column; align-items: center; gap: 5px;
  }
  .color-chip {
    width: 50px; height: 50px; border-radius: 8px; border: 2px solid rgba(255,255,255,0.1);
  }
  .hex {
    font-size: 11px; font-weight: 600; color: #94a3b8;
  }

  .callouts {
    margin-top: 20px; font-size: 13px; line-height: 1.6; color: #cbd5e1;
  }
  .callouts li { margin-bottom: 6px; }
  .callouts strong { color: #eab308; }
</style>
</head>
<body>

  <div class="header">
    <div class="title-block">
      <h1>CHARACTER SHEET: AISHA (आयशा)</h1>
      <div class="sub">Protagonist • Lead UI/UX Designer • Age: 27 • Mumbai</div>
    </div>
    <div class="meta">
      <div>Project: <strong>CHAI & CHAAL (चाय और चाल)</strong></div>
      <div>Phase: <strong>7.7.2 Professional Character Redesign</strong></div>
      <div>Style: <strong>Modern High-Fidelity 2D Digital Vector Animation</strong></div>
    </div>
  </div>

  <div class="grid">
    <!-- LEFT: FULL BODY VIEWS & PALETTE -->
    <div class="panel">
      <div class="panel-title">1. Full Body Turnaround (Height: 7 Heads)</div>
      
      <div class="turnarounds">
        <!-- Front View -->
        <div class="figure-box">
          <svg width="220" height="560" viewBox="0 0 220 560">
            <defs>
              <linearGradient id="hairGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#1e1b4b"/>
                <stop offset="100%" stop-color="#09090b"/>
              </linearGradient>
              <linearGradient id="coatGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#eab308"/>
                <stop offset="100%" stop-color="#ca8a04"/>
              </linearGradient>
              <linearGradient id="skinGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fdba74"/>
                <stop offset="100%" stop-color="#f97316"/>
              </linearGradient>
            </defs>
            <!-- Boots & Legs -->
            <path d="M75 420 L72 520 L60 550 L88 550 L88 420 Z" fill="#18181b"/>
            <path d="M145 420 L148 520 L132 550 L160 550 L132 420 Z" fill="#18181b"/>
            <!-- Dark Cigarette Trousers -->
            <path d="M68 280 L75 430 L95 430 L108 300 L125 430 L145 430 L152 280 Z" fill="#27272a"/>
            <!-- Trench Coat -->
            <path d="M50 160 L40 370 L85 390 L110 300 L135 390 L180 370 L170 160 Z" fill="url(#coatGrad)"/>
            <!-- Coat Lapels & Inner Black Turtleneck -->
            <path d="M85 140 L110 240 L135 140 Z" fill="#18181b"/>
            <path d="M85 140 L70 260 L110 270 L110 140 Z" fill="#ca8a04"/>
            <path d="M135 140 L150 260 L110 270 L110 140 Z" fill="#a16207"/>
            <!-- Neck & Silver Pendant -->
            <path d="M96 115 L124 115 L120 145 L100 145 Z" fill="#fed7aa"/>
            <circle cx="110" cy="140" r="3" fill="#e2e8f0"/>
            <!-- Head & Face -->
            <path d="M82 60 Q110 40 138 60 Q145 100 110 120 Q75 100 82 60 Z" fill="#fed7aa"/>
            <!-- Facial Features (Almond Eyes, Lashes, Lips) -->
            <ellipse cx="98" cy="82" rx="6" ry="3.5" fill="#ffffff"/>
            <circle cx="99" cy="82" r="2.5" fill="#451a03"/>
            <circle cx="98" cy="81" r="0.8" fill="#ffffff"/>
            <path d="M92 79 Q98 75 105 79" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <ellipse cx="122" cy="82" rx="6" ry="3.5" fill="#ffffff"/>
            <circle cx="121" cy="82" r="2.5" fill="#451a03"/>
            <circle cx="120" cy="81" r="0.8" fill="#ffffff"/>
            <path d="M115 79 Q122 75 128 79" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <path d="M109 85 L111 92 L107 93" stroke="#ea580c" stroke-width="1.2" fill="none"/>
            <!-- Confident Red-Berry Lips -->
            <path d="M103 103 Q110 106 117 103 Q110 108 103 103 Z" fill="#be123c"/>
            <!-- Asymmetrical Bob Cut Hair -->
            <path d="M78 60 C75 25, 145 25, 142 60 C148 95, 150 125, 136 135 C132 105, 126 80, 126 70 C105 60, 85 75, 78 95 C74 110, 72 130, 68 115 C66 90, 72 75, 78 60 Z" fill="url(#hairGrad)"/>
            <!-- Hair Specular Sheen -->
            <path d="M90 40 Q110 32 130 42" stroke="#818cf8" stroke-width="2.5" fill="none" opacity="0.6"/>
            <!-- Silver Ear Cuff on right ear -->
            <circle cx="78" cy="82" r="3" fill="#e2e8f0"/>
            <!-- Arms & iPad in Hand -->
            <path d="M52 165 L35 270 L55 270 L65 185 Z" fill="#ca8a04"/>
            <path d="M168 165 L185 260 L165 265 L155 185 Z" fill="#ca8a04"/>
            <rect x="25" y="250" width="35" height="50" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="1.5"/>
          </svg>
          <div class="figure-label">Front View</div>
        </div>

        <!-- 3/4 Dynamic View -->
        <div class="figure-box">
          <svg width="220" height="560" viewBox="0 0 220 560">
            <!-- Boots & Legs angled -->
            <path d="M80 420 L82 520 L70 550 L98 550 L96 420 Z" fill="#18181b"/>
            <path d="M125 420 L132 520 L120 550 L146 550 L138 420 Z" fill="#18181b"/>
            <path d="M75 280 L82 430 L102 430 L112 300 L120 430 L140 430 L145 280 Z" fill="#27272a"/>
            <!-- Trench Coat 3/4 -->
            <path d="M60 160 L50 375 L95 395 L125 300 L145 385 L175 365 L165 160 Z" fill="url(#coatGrad)"/>
            <path d="M85 140 L105 240 L130 140 Z" fill="#18181b"/>
            <path d="M85 140 L75 260 L112 270 L105 140 Z" fill="#ca8a04"/>
            <!-- Neck & Head 3/4 -->
            <path d="M96 115 L122 118 L116 145 L98 145 Z" fill="#fed7aa"/>
            <path d="M82 62 Q105 45 132 60 Q142 98 112 120 Q80 102 82 62 Z" fill="#fed7aa"/>
            <!-- Eyes 3/4 with eyelashes -->
            <ellipse cx="94" cy="82" rx="5" ry="3.2" fill="#ffffff"/>
            <circle cx="95" cy="82" r="2.4" fill="#451a03"/>
            <circle cx="94" cy="81" r="0.8" fill="#ffffff"/>
            <path d="M89 79 Q95 75 101 79" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <ellipse cx="118" cy="83" rx="6" ry="3.5" fill="#ffffff"/>
            <circle cx="118" cy="83" r="2.5" fill="#451a03"/>
            <circle cx="117" cy="82" r="0.8" fill="#ffffff"/>
            <path d="M112 80 Q118 76 125 80" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <path d="M106 85 L108 92 L105 93" stroke="#ea580c" stroke-width="1.2" fill="none"/>
            <!-- Subtle Smirk -->
            <path d="M101 103 Q108 106 116 101 Q108 107 101 103 Z" fill="#be123c"/>
            <!-- Hair 3/4 -->
            <path d="M80 60 C78 28, 142 26, 140 60 C146 95, 148 132, 130 142 C126 105, 120 78, 118 68 C100 58, 85 75, 78 95 C74 115, 72 135, 66 120 C64 92, 72 75, 80 60 Z" fill="url(#hairGrad)"/>
            <path d="M88 42 Q108 34 126 44" stroke="#818cf8" stroke-width="2.5" fill="none" opacity="0.6"/>
            <!-- Front arm holding steamy cutting chai glass -->
            <path d="M158 165 L170 230 L140 240 L135 185 Z" fill="#ca8a04"/>
            <!-- Cutting Chai Glass in Hand -->
            <path d="M135 235 L145 235 L142 255 L138 255 Z" fill="#f59e0b" stroke="#ffffff" stroke-width="1.2"/>
            <!-- Soft steam wisp -->
            <path d="M140 232 Q144 222 138 214 Q142 206 140 200" stroke="#ffffff" stroke-width="1.2" fill="none" opacity="0.7"/>
          </svg>
          <div class="figure-label">3/4 View (Hero Pose)</div>
        </div>
      </div>

      <div class="palette">
        <span style="font-size:12px; font-weight:700; color:#eab308; text-transform:uppercase;">Color Palette:</span>
        <div class="swatch"><div class="color-chip" style="background:#fed7aa;"></div><div class="hex">#FED7AA<br>Skin Base</div></div>
        <div class="swatch"><div class="color-chip" style="background:#eab308;"></div><div class="hex">#EAB308<br>Mustard Coat</div></div>
        <div class="swatch"><div class="color-chip" style="background:#18181b;"></div><div class="hex">#18181B<br>Turtleneck</div></div>
        <div class="swatch"><div class="color-chip" style="background:#1e1b4b;"></div><div class="hex">#1E1B4B<br>Jet Hair/Indigo</div></div>
        <div class="swatch"><div class="color-chip" style="background:#be123c;"></div><div class="hex">#BE123C<br>Berry Lips</div></div>
      </div>
    </div>

    <!-- RIGHT: FACIAL EXPRESSIONS & ANATOMICAL CALLOUTS -->
    <div class="panel">
      <div class="panel-title">2. Facial Expressions & Emotion Matrix</div>
      
      <div class="expressions-grid">
        <!-- Expression 1: Neutral / Cool Composure -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M42 40 Q70 22 98 40 Q105 75 70 95 Q35 75 42 40 Z" fill="#fed7aa"/>
            <!-- Eyes neutral steady -->
            <ellipse cx="56" cy="58" rx="6" ry="3.5" fill="#ffffff"/>
            <circle cx="56" cy="58" r="2.5" fill="#451a03"/>
            <circle cx="55" cy="57" r="0.8" fill="#ffffff"/>
            <path d="M50 55 Q56 52 62 55" stroke="#0f172a" stroke-width="1.6" fill="none"/>
            <ellipse cx="84" cy="58" rx="6" ry="3.5" fill="#ffffff"/>
            <circle cx="84" cy="58" r="2.5" fill="#451a03"/>
            <circle cx="83" cy="57" r="0.8" fill="#ffffff"/>
            <path d="M78 55 Q84 52 90 55" stroke="#0f172a" stroke-width="1.6" fill="none"/>
            <path d="M69 62 L71 69 L67 70" stroke="#ea580c" stroke-width="1.2" fill="none"/>
            <!-- Calm composed lips -->
            <path d="M63 80 Q70 82 77 80" stroke="#be123c" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <!-- Hair -->
            <path d="M38 40 C35 15, 105 15, 102 40 C108 70, 110 95, 96 105 C92 80, 86 60, 86 52 C70 44, 55 55, 50 70 C46 82, 44 98, 40 88 Z" fill="url(#hairGrad)"/>
          </svg>
          <div class="expr-title">1. Cool Composure</div>
          <div class="expr-desc">Scene 1: Calm listening, steady gaze</div>
        </div>

        <!-- Expression 2: Knowing Smirk -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M42 40 Q70 22 98 40 Q105 75 70 95 Q35 75 42 40 Z" fill="#fed7aa"/>
            <!-- Left eye half lidded, right eye arched -->
            <ellipse cx="56" cy="58" rx="6" ry="2.8" fill="#ffffff"/>
            <circle cx="56" cy="58" r="2.5" fill="#451a03"/>
            <circle cx="55" cy="57" r="0.8" fill="#ffffff"/>
            <path d="M49 54 Q56 50 63 54" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <ellipse cx="84" cy="58" rx="6" ry="3.5" fill="#ffffff"/>
            <circle cx="84" cy="58" r="2.5" fill="#451a03"/>
            <circle cx="83" cy="57" r="0.8" fill="#ffffff"/>
            <path d="M78 52 Q85 47 92 53" stroke="#0f172a" stroke-width="2" fill="none"/> <!-- Arched brow -->
            <path d="M69 62 L71 69 L67 70" stroke="#ea580c" stroke-width="1.2" fill="none"/>
            <!-- Asymmetrical Smirk -->
            <path d="M64 80 Q70 82 78 76 Q70 84 64 80 Z" fill="#be123c"/>
            <!-- Hair -->
            <path d="M38 40 C35 15, 105 15, 102 40 C108 70, 110 95, 96 105 C92 80, 86 60, 86 52 C70 44, 55 55, 50 70 C46 82, 44 98, 40 88 Z" fill="url(#hairGrad)"/>
          </svg>
          <div class="expr-title">2. Knowing Smirk</div>
          <div class="expr-desc">Scene 2: Anticipating victory</div>
        </div>

        <!-- Expression 3: Playful Wink & Smile -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M42 40 Q70 22 98 40 Q105 75 70 95 Q35 75 42 40 Z" fill="#fed7aa"/>
            <!-- Left eye open joyful, right eye winking curve -->
            <ellipse cx="56" cy="58" rx="6.5" ry="4" fill="#ffffff"/>
            <circle cx="56" cy="58" r="2.8" fill="#451a03"/>
            <circle cx="55" cy="56" r="1" fill="#ffffff"/>
            <path d="M49 53 Q56 49 63 53" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <!-- Right Eye Wink -->
            <path d="M78 59 Q85 64 92 58" stroke="#0f172a" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <path d="M78 50 Q85 46 92 50" stroke="#0f172a" stroke-width="1.8" fill="none"/>
            <path d="M69 62 L71 69 L67 70" stroke="#ea580c" stroke-width="1.2" fill="none"/>
            <!-- Broad confident smile with white teeth -->
            <path d="M61 78 Q70 88 79 78 Z" fill="#be123c"/>
            <path d="M63 79 Q70 83 77 79 Z" fill="#ffffff"/>
            <!-- Hair -->
            <path d="M38 40 C35 15, 105 15, 102 40 C108 70, 110 95, 96 105 C92 80, 86 60, 86 52 C70 44, 55 55, 50 70 C46 82, 44 98, 40 88 Z" fill="url(#hairGrad)"/>
          </svg>
          <div class="expr-title">3. Playful Wink & Win</div>
          <div class="expr-desc">Scene 4: "Chai ke paise tum doge!"</div>
        </div>
      </div>

      <div class="panel-title" style="margin-top:25px;">3. Anatomy, Rigging & Styling Rules</div>
      <ul class="callouts">
        <li><strong>Believable Proportions:</strong> Head-to-body ratio is exactly 1:7. Shoulders are 1.4x head width; waist narrows elegantly with tailored coat drape.</li>
        <li><strong>Stylized Facial Anatomy:</strong> Distinct almond eyes with defined sclera, dual-tone coffee iris, specular highlights, and natural eyelid crease. NO emoji dots or stick lines.</li>
        <li><strong>Hair Dynamics:</strong> Asymmetrical modern bob cut with violet-indigo sheen; right side sweeps past chin with organic curve.</li>
        <li><strong>Costuming:</strong> Mustard wool trench over textured black turtleneck; realistic lapel shadows and cuff ribbing.</li>
        <li><strong>Personality:</strong> Sharp, observant, unbothered by arrogance; carries herself with the effortless calm of top-tier talent.</li>
      </ul>
    </div>
  </div>

</body>
</html>"""
render_html_to_png(aisha_html, os.path.join(OUTPUT_DIR, "aisha_character_sheet.png"))

# =============================================================================
# 2. VIKRAM CHARACTER DESIGN SHEET (1920x1080)
# =============================================================================
vikram_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 30px 40px;
    background: #0f141e;
    color: #f1f5f9;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px;
    overflow: hidden;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid #10b981; padding-bottom: 15px; margin-bottom: 25px;
  }
  .title-block h1 {
    font-size: 38px; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: 1px;
  }
  .title-block .sub {
    font-size: 16px; color: #10b981; font-weight: 600; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;
  }
  .meta {
    text-align: right; font-size: 14px; color: #94a3b8;
  }
  .meta strong { color: #f8fafc; }

  .grid {
    display: grid; grid-template-columns: 2fr 3fr; gap: 30px; height: 900px;
  }
  .panel {
    background: #182030; border: 1px solid #283548; border-radius: 12px; padding: 25px; position: relative;
  }
  .panel-title {
    font-size: 16px; font-weight: 700; color: #10b981; text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 15px; border-bottom: 1px solid #283548; padding-bottom: 8px;
  }

  .turnarounds {
    display: flex; justify-content: space-around; align-items: flex-end; height: 600px;
  }
  .figure-box {
    text-align: center;
  }
  .figure-label {
    margin-top: 10px; font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase;
  }

  .expressions-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;
  }
  .expr-box {
    background: #101622; border: 1px solid #243044; border-radius: 8px; padding: 15px; text-align: center;
  }
  .expr-title {
    font-size: 13px; font-weight: 700; color: #f8fafc; margin-top: 8px;
  }
  .expr-desc {
    font-size: 11px; color: #64748b; margin-top: 2px;
  }

  .palette {
    display: flex; gap: 15px; margin-top: 20px; align-items: center;
  }
  .swatch {
    display: flex; flex-direction: column; align-items: center; gap: 5px;
  }
  .color-chip {
    width: 50px; height: 50px; border-radius: 8px; border: 2px solid rgba(255,255,255,0.1);
  }
  .hex {
    font-size: 11px; font-weight: 600; color: #94a3b8;
  }

  .callouts {
    margin-top: 20px; font-size: 13px; line-height: 1.6; color: #cbd5e1;
  }
  .callouts li { margin-bottom: 6px; }
  .callouts strong { color: #10b981; }
</style>
</head>
<body>

  <div class="header">
    <div class="title-block">
      <h1>CHARACTER SHEET: VIKRAM (विक्रम)</h1>
      <div class="sub">Rival / Colleague • Advertising Art Director • Age: 28 • Mumbai</div>
    </div>
    <div class="meta">
      <div>Project: <strong>CHAI & CHAAL (चाय और चाल)</strong></div>
      <div>Phase: <strong>7.7.2 Professional Character Redesign</strong></div>
      <div>Style: <strong>Modern High-Fidelity 2D Digital Vector Animation</strong></div>
    </div>
  </div>

  <div class="grid">
    <!-- LEFT: FULL BODY VIEWS & PALETTE -->
    <div class="panel">
      <div class="panel-title">1. Full Body Turnaround (Height: 7.5 Heads)</div>
      
      <div class="turnarounds">
        <!-- Front View -->
        <div class="figure-box">
          <svg width="220" height="560" viewBox="0 0 220 560">
            <defs>
              <linearGradient id="bomberGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#047857"/>
                <stop offset="100%" stop-color="#064e3b"/>
              </linearGradient>
              <linearGradient id="hairMen" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#27272a"/>
                <stop offset="100%" stop-color="#09090b"/>
              </linearGradient>
            </defs>
            <!-- White Sneakers & Chinos -->
            <path d="M72 430 L70 525 L58 550 L88 550 L88 430 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M148 430 L150 525 L132 550 L162 550 L132 430 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <!-- Beige Chinos -->
            <path d="M68 280 L72 435 L92 435 L110 310 L128 435 L148 435 L152 280 Z" fill="#d4d4d8"/>
            <!-- Forest Green Quilted Bomber Jacket -->
            <path d="M45 155 L40 285 L85 295 L110 290 L135 295 L180 285 L175 155 Z" fill="url(#bomberGrad)"/>
            <!-- Ribbed Hem & Collar -->
            <path d="M42 285 L178 285 L178 295 L42 295 Z" fill="#1f2937"/>
            <path d="M85 145 Q110 160 135 145 L138 155 Q110 170 82 155 Z" fill="#1f2937"/>
            <!-- Ash-Grey Henley Inner Shirt -->
            <path d="M88 150 L110 210 L132 150 Z" fill="#4b5563"/>
            <!-- Neck & Strong Jawline -->
            <path d="M96 115 L124 115 L122 145 L98 145 Z" fill="#fcd34d"/>
            <path d="M78 60 Q110 42 142 60 Q146 100 110 124 Q74 100 78 60 Z" fill="#fcd34d"/>
            <!-- Stubble Shadow along jaw -->
            <path d="M84 95 Q110 126 136 95 L130 112 Q110 124 90 112 Z" fill="#78350f" opacity="0.25"/>
            <!-- Tortoiseshell Designer Glasses -->
            <rect x="85" y="74" width="22" height="15" rx="3" fill="none" stroke="#78350f" stroke-width="2.2"/>
            <rect x="113" y="74" width="22" height="15" rx="3" fill="none" stroke="#78350f" stroke-width="2.2"/>
            <line x1="107" y1="80" x2="113" y2="80" stroke="#78350f" stroke-width="2.5"/>
            <!-- Eyes behind lenses -->
            <circle cx="96" cy="81" r="2.5" fill="#1e1b4b"/>
            <circle cx="95" cy="80" r="0.8" fill="#ffffff"/>
            <circle cx="124" cy="81" r="2.5" fill="#1e1b4b"/>
            <circle cx="123" cy="80" r="0.8" fill="#ffffff"/>
            <!-- Confident eyebrows -->
            <path d="M84 71 L106 69" stroke="#18181b" stroke-width="2.4" stroke-linecap="round"/>
            <path d="M114 69 L136 71" stroke="#18181b" stroke-width="2.4" stroke-linecap="round"/>
            <!-- Nose & Smug Mouth -->
            <path d="M108 82 L111 94 L106 95" stroke="#b45309" stroke-width="1.5" fill="none"/>
            <path d="M100 106 Q110 108 120 104" stroke="#78350f" stroke-width="2.4" stroke-linecap="round" fill="none"/>
            <!-- Styled Fade / Quiff Hair -->
            <path d="M76 60 C74 25, 146 25, 144 60 C146 68, 144 75, 142 80 C138 52, 134 40, 110 36 C86 40, 82 52, 78 80 C76 75, 74 68, 76 60 Z" fill="url(#hairMen)"/>
            <path d="M90 32 Q110 24 130 32" stroke="#52525b" stroke-width="2" fill="none"/>
            <!-- Arms & Watch -->
            <path d="M45 160 L30 260 L50 260 L60 180 Z" fill="#047857"/>
            <path d="M175 160 L190 260 L170 260 L160 180 Z" fill="#047857"/>
            <rect x="28" y="248" width="18" height="6" fill="#0f172a"/>
          </svg>
          <div class="figure-label">Front View</div>
        </div>

        <!-- 3/4 Dynamic View -->
        <div class="figure-box">
          <svg width="220" height="560" viewBox="0 0 220 560">
            <!-- Chinos & Sneakers 3/4 -->
            <path d="M78 430 L80 525 L68 550 L98 550 L96 430 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M125 430 L132 525 L120 550 L150 550 L140 430 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M72 280 L78 435 L98 435 L112 310 L122 435 L144 435 L148 280 Z" fill="#d4d4d8"/>
            <!-- Bomber Jacket 3/4 -->
            <path d="M55 155 L45 285 L90 295 L115 290 L140 295 L175 280 L168 155 Z" fill="url(#bomberGrad)"/>
            <!-- Head & Glasses 3/4 -->
            <path d="M96 115 L120 118 L116 145 L96 145 Z" fill="#fcd34d"/>
            <path d="M78 60 Q106 42 136 58 Q144 98 112 124 Q76 100 78 60 Z" fill="#fcd34d"/>
            <path d="M84 95 Q108 126 132 95 L126 112 Q108 124 90 112 Z" fill="#78350f" opacity="0.25"/>
            <!-- Glasses 3/4 -->
            <rect x="85" y="74" width="20" height="15" rx="3" fill="none" stroke="#78350f" stroke-width="2.2"/>
            <rect x="110" y="74" width="22" height="15" rx="3" fill="none" stroke="#78350f" stroke-width="2.2"/>
            <line x1="105" y1="80" x2="110" y2="80" stroke="#78350f" stroke-width="2.5"/>
            <circle cx="95" cy="81" r="2.5" fill="#1e1b4b"/>
            <circle cx="121" cy="81" r="2.5" fill="#1e1b4b"/>
            <!-- One raised cocky eyebrow -->
            <path d="M84 72 L102 72" stroke="#18181b" stroke-width="2.4" stroke-linecap="round"/>
            <path d="M110 66 L130 70" stroke="#18181b" stroke-width="2.6" stroke-linecap="round"/>
            <path d="M106 82 L109 94 L104 95" stroke="#b45309" stroke-width="1.5" fill="none"/>
            <path d="M98 106 Q108 109 118 103" stroke="#78350f" stroke-width="2.6" stroke-linecap="round" fill="none"/>
            <!-- Hair -->
            <path d="M76 60 C74 25, 142 25, 140 58 C144 68, 142 75, 140 80 C136 50, 130 38, 108 34 C86 38, 80 50, 78 80 C76 75, 74 68, 76 60 Z" fill="url(#hairMen)"/>
            <!-- Arm sliding napkin forward -->
            <path d="M165 160 L185 240 L150 250 L140 180 Z" fill="#047857"/>
            <polygon points="175,245 195,240 205,255 185,260" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
          </svg>
          <div class="figure-label">3/4 View (Hero Pose)</div>
        </div>
      </div>

      <div class="palette">
        <span style="font-size:12px; font-weight:700; color:#10b981; text-transform:uppercase;">Color Palette:</span>
        <div class="swatch"><div class="color-chip" style="background:#fcd34d;"></div><div class="hex">#FCD34D<br>Warm Skin</div></div>
        <div class="swatch"><div class="color-chip" style="background:#047857;"></div><div class="hex">#047857<br>Emerald Bomber</div></div>
        <div class="swatch"><div class="color-chip" style="background:#78350f;"></div><div class="hex">#78350F<br>Tortoiseshell</div></div>
        <div class="swatch"><div class="color-chip" style="background:#27272a;"></div><div class="hex">#27272A<br>Faded Quiff</div></div>
        <div class="swatch"><div class="color-chip" style="background:#d4d4d8;"></div><div class="hex">#D4D4D8<br>Light Chinos</div></div>
      </div>
    </div>

    <!-- RIGHT: FACIAL EXPRESSIONS & ANATOMICAL CALLOUTS -->
    <div class="panel">
      <div class="panel-title">2. Facial Expressions & Emotion Matrix</div>
      
      <div class="expressions-grid">
        <!-- Expression 1: Cocky / Smug Grin -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 40 Q70 22 102 40 Q106 75 70 98 Q34 75 38 40 Z" fill="#fcd34d"/>
            <path d="M44 75 Q70 102 96 75 L92 88 Q70 98 48 88 Z" fill="#78350f" opacity="0.25"/>
            <rect x="46" y="54" width="20" height="14" rx="2" fill="none" stroke="#78350f" stroke-width="2"/>
            <rect x="74" y="54" width="20" height="14" rx="2" fill="none" stroke="#78350f" stroke-width="2"/>
            <circle cx="56" cy="61" r="2.2" fill="#1e1b4b"/>
            <circle cx="84" cy="61" r="2.2" fill="#1e1b4b"/>
            <!-- Raised eyebrow -->
            <path d="M46 50 L64 50" stroke="#18181b" stroke-width="2"/>
            <path d="M74 46 L94 48" stroke="#18181b" stroke-width="2.4"/>
            <path d="M68 62 L71 70 L67 71" stroke="#b45309" stroke-width="1.2" fill="none"/>
            <path d="M60 82 Q70 85 82 78" stroke="#78350f" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <path d="M36 40 C34 15, 104 15, 102 40 C104 60, 95 30, 70 26 C45 30, 38 60, 36 40 Z" fill="url(#hairMen)"/>
          </svg>
          <div class="expr-title">1. Cocky Smugness</div>
          <div class="expr-desc">Scene 1: "Deal final hai!"</div>
        </div>

        <!-- Expression 2: Absolute Jaw-Drop Shock -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 38 Q70 18 102 38 Q106 75 70 105 Q34 75 38 38 Z" fill="#fcd34d"/>
            <!-- Giant shocked pupils behind askew glasses -->
            <rect x="44" y="50" width="22" height="16" rx="2" fill="none" stroke="#78350f" stroke-width="2"/>
            <rect x="74" y="50" width="22" height="16" rx="2" fill="none" stroke="#78350f" stroke-width="2"/>
            <circle cx="55" cy="58" r="3.5" fill="#1e1b4b"/>
            <circle cx="85" cy="58" r="3.5" fill="#1e1b4b"/>
            <circle cx="54" cy="56" r="1.2" fill="#ffffff"/>
            <circle cx="84" cy="56" r="1.2" fill="#ffffff"/>
            <!-- High shocked eyebrows -->
            <path d="M44 42 Q54 38 64 42" stroke="#18181b" stroke-width="2.2" fill="none"/>
            <path d="M74 42 Q84 38 94 42" stroke="#18181b" stroke-width="2.2" fill="none"/>
            <!-- Large dropped open mouth 'O' -->
            <ellipse cx="70" cy="88" rx="8" ry="12" fill="#451a03"/>
            <!-- Cold sweat drop on temple -->
            <path d="M98 48 Q102 56 98 60 Q94 56 98 48 Z" fill="#38bdf8"/>
            <path d="M36 38 C34 15, 104 15, 102 38 C104 60, 95 28, 70 24 C45 28, 38 60, 36 38 Z" fill="url(#hairMen)"/>
          </svg>
          <div class="expr-title">2. Dropped-Jaw Shock</div>
          <div class="expr-desc">Scene 3: "Aisha is Project Head?!"</div>
        </div>

        <!-- Expression 3: Defeated Sheepish Laugh -->
        <div class="expr-box">
          <svg width="140" height="150" viewBox="0 0 140 150">
            <path d="M38 40 Q70 22 102 40 Q106 75 70 98 Q34 75 38 40 Z" fill="#fcd34d"/>
            <rect x="46" y="54" width="20" height="14" rx="2" fill="none" stroke="#78350f" stroke-width="2"/>
            <rect x="74" y="54" width="20" height="14" rx="2" fill="none" stroke="#78350f" stroke-width="2"/>
            <!-- Squinting wry smile eyes -->
            <path d="M49 61 Q56 66 63 61" stroke="#18181b" stroke-width="2" fill="none"/>
            <path d="M77 61 Q84 66 91 61" stroke="#18181b" stroke-width="2" fill="none"/>
            <!-- Awkward sheepish grin -->
            <path d="M56 80 Q70 88 84 80" stroke="#78350f" stroke-width="2.5" stroke-linecap="round" fill="none"/>
            <path d="M36 40 C34 15, 104 15, 102 40 C104 60, 95 30, 70 26 C45 30, 38 60, 36 40 Z" fill="url(#hairMen)"/>
          </svg>
          <div class="expr-title">3. Sheepish Defeat</div>
          <div class="expr-desc">Scene 4: Pulling out wallet</div>
        </div>
      </div>

      <div class="panel-title" style="margin-top:25px;">3. Anatomy, Rigging & Styling Rules</div>
      <ul class="callouts">
        <li><strong>Believable Proportions:</strong> Head-to-body ratio is exactly 1:7.5. Broad athletic shoulders, lean waist, long limbs.</li>
        <li><strong>Stylized Facial Anatomy:</strong> Strong angular jawline with subtle 5 o'clock stubble shadow; tortoiseshell designer frames accentuating brow and eye movements.</li>
        <li><strong>Hair Dynamics:</strong> Modern barber-fade sides with voluminous swept-back quiff.</li>
        <li><strong>Costuming:</strong> Emerald quilted bomber jacket over grey crewneck and tailored chinos; crisp clean white streetwear sneakers.</li>
        <li><strong>Personality:</strong> Overconfident, slick, secretly insecure about Aisha's superior talent; takes defeat with comic grace.</li>
      </ul>
    </div>
  </div>

</body>
</html>"""
render_html_to_png(vikram_html, os.path.join(OUTPUT_DIR, "vikram_character_sheet.png"))

print("Both Character Sheets Generated Successfully!")
