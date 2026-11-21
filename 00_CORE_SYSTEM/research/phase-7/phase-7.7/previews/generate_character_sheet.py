import os
import subprocess

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 24px 32px;
    background: #0f172a;
    color: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
    width: 1920px;
    height: 1080px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #f59e0b;
    padding-bottom: 10px;
    margin-bottom: 16px;
  }
  .title-block h1 {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
  }
  .title-block p {
    font-size: 13px;
    color: #94a3b8;
    margin: 4px 0 0 0;
  }
  .badge {
    background: #1e293b;
    border: 1px solid #f59e0b;
    color: #f59e0b;
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 700;
  }
  .main-grid {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 20px;
    height: 970px;
  }
  .char-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .char-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 8px;
  }
  .char-name {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
  }
  .char-hindi {
    font-family: 'Noto Sans Devanagari';
    color: #f59e0b;
    font-size: 19px;
    margin-left: 8px;
  }
  .char-role {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
    background: #0f172a;
    padding: 4px 10px;
    border-radius: 4px;
  }
  .visual-area {
    display: flex;
    gap: 14px;
    flex: 1;
  }
  .model-box {
    flex: 1.1;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
  }
  .model-box h4 {
    margin: 0 0 6px 0;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #f59e0b;
  }
  .expressions-box {
    flex: 0.9;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .exp-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    flex: 1;
  }
  .exp-card {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .exp-card svg {
    width: 82px;
    height: 98px;
  }
  .exp-card span {
    font-size: 11px;
    font-weight: 600;
    color: #cbd5e1;
    margin-top: 4px;
  }
  .swatches-bar {
    display: flex;
    gap: 8px;
    align-items: center;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 12px;
  }
  .swatch {
    width: 22px;
    height: 22px;
    border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.2);
  }
  .swatch-label {
    font-size: 11px;
    color: #94a3b8;
    margin-right: 4px;
  }
  .specs-list {
    font-size: 12px;
    color: #cbd5e1;
    line-height: 1.5;
    background: #0f172a;
    border-radius: 6px;
    padding: 10px 14px;
    border: 1px solid #334155;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>MASTER AI — PHASE 7.7 CHARACTER DESIGN & ANATOMY MODEL SHEET</h1>
      <p>Original 2D Production: 'पहला ऑर्डर' (The First Order) // Professional Stylized Human Anatomy Specification</p>
    </div>
    <div class="badge">STUDIO SPECIFICATION v1.0</div>
  </div>

  <div class="main-grid">
    <!-- CHARACTER 1: AANYA -->
    <div class="char-card">
      <div class="char-header">
        <div>
          <span class="char-name">Aanya</span>
          <span class="char-hindi">आन्या</span>
        </div>
        <span class="char-role">PROTAGONIST // ARTISAN HOME BAKER (AGE 22)</span>
      </div>

      <div class="visual-area">
        <!-- Full Body Model SVG -->
        <div class="model-box">
          <h4>Full Body Model (7.5 Heads Anatomy)</h4>
          <svg viewBox="0 0 240 420" width="230" height="390">
            <defs>
              <linearGradient id="skinGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#fcd5b5"/>
                <stop offset="100%" stop-color="#e5a782"/>
              </linearGradient>
              <linearGradient id="hairGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#3d2314"/>
                <stop offset="100%" stop-color="#1f1108"/>
              </linearGradient>
              <linearGradient id="linenGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#fdfbf7"/>
                <stop offset="100%" stop-color="#e8e2d5"/>
              </linearGradient>
              <linearGradient id="apronGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#1e293b"/>
                <stop offset="100%" stop-color="#0f172a"/>
              </linearGradient>
            </defs>

            <!-- Ground Shadow -->
            <ellipse cx="120" cy="408" rx="45" ry="6" fill="#020617" opacity="0.6"/>

            <!-- Legs & Casual Trousers -->
            <path d="M102 270 L98 385 L90 388 L90 398 L108 398 L110 385 L112 270 Z" fill="#334155"/>
            <path d="M128 270 L130 385 L132 388 L132 398 L150 398 L148 385 L138 270 Z" fill="#334155"/>
            <!-- White Sneakers -->
            <rect x="86" y="394" width="24" height="10" rx="4" fill="#f8fafc"/>
            <rect x="130" y="394" width="24" height="10" rx="4" fill="#f8fafc"/>

            <!-- Cream Linen Top & Sleeves -->
            <path d="M92 110 L148 110 L158 200 L82 200 Z" fill="url(#linenGrad)"/>
            <!-- Left Arm -->
            <path d="M92 112 L72 170 L84 175 L100 120 Z" fill="url(#linenGrad)"/>
            <path d="M72 170 L65 240 L76 242 L84 175 Z" fill="url(#skinGrad)"/>
            <!-- Right Arm -->
            <path d="M148 112 L168 170 L156 175 L140 120 Z" fill="url(#linenGrad)"/>
            <path d="M168 170 L175 240 L164 242 L156 175 Z" fill="url(#skinGrad)"/>

            <!-- Navy Baker Apron -->
            <path d="M100 135 L140 135 L148 290 L92 290 Z" fill="url(#apronGrad)" stroke="#020617" stroke-width="1.5"/>
            <!-- Apron Straps & Brass Buckles -->
            <line x1="106" y1="112" x2="104" y2="135" stroke="#b45309" stroke-width="3"/>
            <line x1="134" y1="112" x2="136" y2="135" stroke="#b45309" stroke-width="3"/>
            <circle cx="104" cy="135" r="3.5" fill="#f59e0b"/>
            <circle cx="136" cy="135" r="3.5" fill="#f59e0b"/>
            <!-- Front pocket with whisk embroidery -->
            <rect x="105" y="210" width="30" height="26" rx="3" fill="#0f172a" stroke="#334155" stroke-width="1"/>
            <line x1="120" y1="216" x2="120" y2="228" stroke="#f59e0b" stroke-width="1.5"/>

            <!-- Neck & Collarbone -->
            <path d="M112 88 L128 88 L126 112 L114 112 Z" fill="url(#skinGrad)"/>
            <line x1="110" y1="108" x2="118" y2="112" stroke="#d48b5f" stroke-width="1"/>
            <line x1="130" y1="108" x2="122" y2="112" stroke="#d48b5f" stroke-width="1"/>

            <!-- Head & Face (Hero View) -->
            <path d="M102 52 C102 32 138 32 138 52 C138 78 128 88 120 90 C112 88 102 78 102 52 Z" fill="url(#skinGrad)"/>
            <!-- Ears -->
            <ellipse cx="100" cy="60" rx="3.5" ry="6" fill="#e5a782"/>
            <ellipse cx="140" cy="60" rx="3.5" ry="6" fill="#e5a782"/>
            <!-- Almond Hazel Eyes -->
            <ellipse cx="111" cy="56" rx="4.5" ry="3" fill="#ffffff"/>
            <ellipse cx="129" cy="56" rx="4.5" ry="3" fill="#ffffff"/>
            <circle cx="112" cy="56" r="2.2" fill="#78350f"/>
            <circle cx="128" cy="56" r="2.2" fill="#78350f"/>
            <circle cx="113" cy="55" r="0.8" fill="#ffffff"/>
            <circle cx="129" cy="55" r="0.8" fill="#ffffff"/>
            <!-- Brows & Nose & Mouth -->
            <path d="M107 50 Q111 48 116 50" stroke="#3d2314" stroke-width="1.4" fill="none"/>
            <path d="M124 50 Q129 48 133 50" stroke="#3d2314" stroke-width="1.4" fill="none"/>
            <path d="M120 57 L119 65 L122 66" stroke="#c8784d" stroke-width="1.2" fill="none"/>
            <path d="M115 74 Q120 78 125 74" stroke="#be123c" stroke-width="1.5" fill="none"/>

            <!-- Hair (Messy Textured Bun with Face Tendrils) -->
            <path d="M98 52 C98 32 108 20 120 20 C132 20 142 32 142 52 C142 40 134 32 120 32 C106 32 98 40 98 52 Z" fill="url(#hairGrad)"/>
            <!-- Top Bun -->
            <ellipse cx="120" cy="16" rx="16" ry="13" fill="url(#hairGrad)"/>
            <!-- Tendrils -->
            <path d="M100 55 Q96 70 102 76" stroke="#3d2314" stroke-width="1.5" fill="none"/>
            <path d="M140 55 Q144 70 138 76" stroke="#3d2314" stroke-width="1.5" fill="none"/>
          </svg>
        </div>

        <!-- 4 Expressions Grid -->
        <div class="expressions-box">
          <h4 style="margin:0; font-size:11px; text-transform:uppercase; color:#f59e0b;">Key Expression Studies</h4>
          <div class="exp-grid">
            <!-- 1. Anxious -->
            <div class="exp-card">
              <svg viewBox="0 0 100 110">
                <path d="M25 45 C25 20 75 20 75 45 C75 80 60 92 50 94 C40 92 25 80 25 45 Z" fill="url(#skinGrad)"/>
                <ellipse cx="50" cy="14" rx="16" ry="12" fill="url(#hairGrad)"/>
                <path d="M22 45 C22 24 35 18 50 18 C65 18 78 24 78 45 Z" fill="url(#hairGrad)"/>
                <path d="M33 46 Q40 43 45 47" stroke="#3d2314" stroke-width="1.8" fill="none"/>
                <path d="M67 46 Q60 43 55 47" stroke="#3d2314" stroke-width="1.8" fill="none"/>
                <ellipse cx="38" cy="54" rx="4.5" ry="4" fill="#fff"/><circle cx="39" cy="54" r="2.2" fill="#78350f"/>
                <ellipse cx="62" cy="54" rx="4.5" ry="4" fill="#fff"/><circle cx="61" cy="54" r="2.2" fill="#78350f"/>
                <path d="M44 78 Q50 74 56 78" stroke="#be123c" stroke-width="2" fill="none"/>
                <rect x="46" y="74" width="8" height="3" rx="1" fill="#fff"/>
              </svg>
              <span>1. Anxious Doubt</span>
            </div>

            <!-- 2. Shock/Gasp -->
            <div class="exp-card">
              <svg viewBox="0 0 100 110">
                <path d="M25 45 C25 20 75 20 75 45 C75 80 60 92 50 94 C40 92 25 80 25 45 Z" fill="url(#skinGrad)"/>
                <ellipse cx="50" cy="14" rx="16" ry="12" fill="url(#hairGrad)"/>
                <path d="M22 45 C22 24 35 18 50 18 C65 18 78 24 78 45 Z" fill="url(#hairGrad)"/>
                <path d="M32 40 Q40 36 47 41" stroke="#3d2314" stroke-width="1.8" fill="none"/>
                <path d="M68 40 Q60 36 53 41" stroke="#3d2314" stroke-width="1.8" fill="none"/>
                <ellipse cx="38" cy="52" rx="6" ry="6" fill="#fff"/><circle cx="38" cy="52" r="3.2" fill="#78350f"/><circle cx="39" cy="50" r="1.2" fill="#fff"/>
                <ellipse cx="62" cy="52" rx="6" ry="6" fill="#fff"/><circle cx="62" cy="52" r="3.2" fill="#78350f"/><circle cx="63" cy="50" r="1.2" fill="#fff"/>
                <ellipse cx="50" cy="77" rx="5" ry="7" fill="#be123c"/>
              </svg>
              <span>2. Sudden Gasp</span>
            </div>

            <!-- 3. Tearful Joy -->
            <div class="exp-card">
              <svg viewBox="0 0 100 110">
                <path d="M25 45 C25 20 75 20 75 45 C75 80 60 92 50 94 C40 92 25 80 25 45 Z" fill="url(#skinGrad)"/>
                <ellipse cx="50" cy="14" rx="16" ry="12" fill="url(#hairGrad)"/>
                <path d="M22 45 C22 24 35 18 50 18 C65 18 78 24 78 45 Z" fill="url(#hairGrad)"/>
                <path d="M34 45 Q40 43 46 45" stroke="#3d2314" stroke-width="1.6" fill="none"/>
                <path d="M66 45 Q60 43 54 45" stroke="#3d2314" stroke-width="1.6" fill="none"/>
                <path d="M34 54 Q40 50 46 54" stroke="#78350f" stroke-width="2.2" fill="none"/>
                <path d="M54 54 Q60 50 66 54" stroke="#78350f" stroke-width="2.2" fill="none"/>
                <circle cx="34" cy="58" r="2.2" fill="#38bdf8"/>
                <circle cx="66" cy="58" r="2.2" fill="#38bdf8"/>
                <path d="M38 72 Q50 84 62 72" stroke="#be123c" stroke-width="2.2" fill="#be123c"/>
                <path d="M41 73 Q50 78 59 73" fill="#fff"/>
              </svg>
              <span>3. Tearful Relief</span>
            </div>

            <!-- 4. Determination -->
            <div class="exp-card">
              <svg viewBox="0 0 100 110">
                <path d="M25 45 C25 20 75 20 75 45 C75 80 60 92 50 94 C40 92 25 80 25 45 Z" fill="url(#skinGrad)"/>
                <ellipse cx="50" cy="14" rx="16" ry="12" fill="url(#hairGrad)"/>
                <path d="M22 45 C22 24 35 18 50 18 C65 18 78 24 78 45 Z" fill="url(#hairGrad)"/>
                <path d="M34 44 Q41 42 47 45" stroke="#3d2314" stroke-width="1.8" fill="none"/>
                <path d="M66 44 Q59 42 53 45" stroke="#3d2314" stroke-width="1.8" fill="none"/>
                <ellipse cx="40" cy="53" rx="4.5" ry="3.5" fill="#fff"/><circle cx="41" cy="53" r="2.2" fill="#78350f"/>
                <ellipse cx="60" cy="53" rx="4.5" ry="3.5" fill="#fff"/><circle cx="59" cy="53" r="2.2" fill="#78350f"/>
                <path d="M41 74 Q50 80 59 74" stroke="#be123c" stroke-width="2.4" fill="none"/>
              </svg>
              <span>4. Resolute Baker</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Swatches -->
      <div class="swatches-bar">
        <span class="swatch-label">Palette:</span>
        <div class="swatch" style="background:#fcd5b5;" title="Skin Tint #FCD5B5"></div>
        <div class="swatch" style="background:#e5a782;" title="Skin Shadow #E5A782"></div>
        <div class="swatch" style="background:#3d2314;" title="Hair Brown #3D2314"></div>
        <div class="swatch" style="background:#fdfbf7;" title="Linen Cream #FDFBF7"></div>
        <div class="swatch" style="background:#1e293b;" title="Apron Navy #1E293B"></div>
        <div class="swatch" style="background:#f59e0b;" title="Brass Gold #F59E0B"></div>
        <div class="swatch" style="background:#78350f;" title="Hazel Iris #78350F"></div>
      </div>
    </div>

    <!-- CHARACTER 2: KABIR -->
    <div class="char-card">
      <div class="char-header">
        <div>
          <span class="char-name">Kabir</span>
          <span class="char-hindi">कबीर</span>
        </div>
        <span class="char-role">SUPPORTING // YOUNGER BROTHER (AGE 16)</span>
      </div>

      <div class="visual-area">
        <!-- Kabir Model -->
        <div class="model-box" style="flex:1;">
          <h4>Full Body Model (7.2 Heads Anatomy)</h4>
          <svg viewBox="0 0 200 420" width="190" height="390">
            <!-- Ground Shadow -->
            <ellipse cx="100" cy="408" rx="40" ry="6" fill="#020617" opacity="0.6"/>
            <!-- Jeans & High-top sneakers -->
            <path d="M84 260 L80 380 L72 384 L72 396 L92 396 L94 380 L96 260 Z" fill="#1e293b"/>
            <path d="M106 260 L108 380 L110 384 L110 396 L130 396 L128 380 L118 260 Z" fill="#1e293b"/>
            <rect x="68" y="392" width="24" height="10" rx="4" fill="#f43f5e"/>
            <rect x="110" y="392" width="24" height="10" rx="4" fill="#f43f5e"/>

            <!-- Olive Green Drop-shoulder T-Shirt -->
            <path d="M70 110 L130 110 L136 215 L64 215 Z" fill="#4d7c0f"/>
            <!-- Sleeves -->
            <path d="M70 110 L52 165 L66 170 L80 120 Z" fill="#4d7c0f"/>
            <path d="M52 165 L56 230 L66 230 L66 170 Z" fill="#fcd5b5"/>
            <path d="M130 110 L148 165 L134 170 L120 120 Z" fill="#4d7c0f"/>
            <path d="M148 165 L144 230 L134 230 L134 170 Z" fill="#fcd5b5"/>

            <!-- Holding Chai Cup in Right Hand -->
            <rect x="138" y="220" width="16" height="18" rx="3" fill="#fbbf24"/>
            <path d="M154 224 Q158 229 154 234" stroke="#d97706" stroke-width="2" fill="none"/>

            <!-- Neck & Face -->
            <rect x="93" y="88" width="14" height="24" fill="#e5a782"/>
            <path d="M82 48 C82 30 118 30 118 48 C118 76 110 88 100 90 C90 88 82 76 82 48 Z" fill="#fcd5b5"/>
            <!-- Wavy Dark Hair with Bangs -->
            <path d="M78 46 C78 24 88 14 100 14 C112 14 122 24 122 46 C122 36 112 28 100 28 C86 28 78 36 78 46 Z" fill="#172554"/>
            <path d="M80 36 Q92 26 102 34 Q114 26 120 38" fill="#172554"/>

            <!-- Expressive Eyes & Smirk -->
            <ellipse cx="92" cy="54" rx="4" ry="3" fill="#fff"/><circle cx="92" cy="54" r="2" fill="#0f172a"/>
            <ellipse cx="108" cy="54" rx="4" ry="3" fill="#fff"/><circle cx="108" cy="54" r="2" fill="#0f172a"/>
            <path d="M88 47 Q92 45 97 48" stroke="#172554" stroke-width="1.5" fill="none"/>
            <path d="M103 48 Q108 45 112 47" stroke="#172554" stroke-width="1.5" fill="none"/>
            <!-- Playful Confident Smirk -->
            <path d="M94 72 Q100 75 108 70" stroke="#be123c" stroke-width="2" fill="none"/>
          </svg>
        </div>

        <!-- Kabir Details & Poses -->
        <div style="flex:1; display:flex; flex-direction:column; gap:12px;">
          <div class="specs-list">
            <h4 style="margin:0 0 6px 0; color:#f59e0b;">Anatomy & Styling:</h4>
            • Age 16, 5'9" lean high-school athletic build.<br>
            • Tousled midnight-navy waves with loose fringe.<br>
            • Olive-green cotton drop-shoulder boxy tee.<br>
            • Charcoal washed denim and red retro skate sneakers.<br>
            • Props: Ceramic cutting-chai glass & Baker's Apron.
          </div>

          <div class="specs-list">
            <h4 style="margin:0 0 6px 0; color:#f59e0b;">Acting Keyframes:</h4>
            • <b>Frame 40</b>: Leaning back on kitchen stool, sipping chai.<br>
            • <b>Frame 190</b>: Startled upright by notification ping.<br>
            • <b>Frame 280</b>: Proudly handing apron to Aanya with a triumphant grin.
          </div>

          <div class="swatches-bar">
            <span class="swatch-label">Palette:</span>
            <div class="swatch" style="background:#fcd5b5;" title="Skin"></div>
            <div class="swatch" style="background:#172554;" title="Dark Navy Hair"></div>
            <div class="swatch" style="background:#4d7c0f;" title="Olive Green Tee"></div>
            <div class="swatch" style="background:#1e293b;" title="Charcoal Denim"></div>
            <div class="swatch" style="background:#fbbf24;" title="Chai Glass"></div>
            <div class="swatch" style="background:#f43f5e;" title="Red Sneakers"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

out_png = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\character_design_sheet.png"
temp_html = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\char_sheet.tmp.html"

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1920,1080",
    f"--screenshot={out_png}",
    temp_html
]
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(temp_html):
    os.remove(temp_html)

print("Character Design Sheet Render Status:", res.returncode)
print("File size:", os.path.getsize(out_png) if os.path.exists(out_png) else 0)
