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
    background: #0b1120;
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
  .main-layout {
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 20px;
    height: 970px;
  }
  .studio-art-box {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .art-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 8px;
  }
  .art-header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 800;
    color: #f8fafc;
  }
  .art-canvas {
    flex: 1;
    background: #020617;
    border-radius: 8px;
    border: 1px solid #334155;
    overflow: hidden;
    position: relative;
  }
  .sidebar-box {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .info-panel {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
  }
  .info-panel h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .info-panel p, .info-panel li {
    font-size: 12px;
    color: #cbd5e1;
    line-height: 1.6;
    margin: 4px 0;
  }
  .color-script {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 8px;
  }
  .cs-block {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
    text-align: center;
  }
  .cs-bar {
    height: 38px;
    border-radius: 4px;
    margin-bottom: 6px;
  }
  .cs-title {
    font-size: 11px;
    font-weight: 700;
    color: #f1f5f9;
  }
  .cs-sub {
    font-size: 10px;
    color: #94a3b8;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>MASTER AI — PHASE 7.7 VISUAL DIRECTION & STYLE REFERENCE BOARD</h1>
      <p>Artisan Studio Atmosphere // Layered Multi-Plane Lighting, Depth & Color Architecture</p>
    </div>
    <div class="badge">VISUAL STYLE SPECIFICATION v1.0</div>
  </div>

  <div class="main-layout">
    <!-- Visual Studio Concept Art -->
    <div class="studio-art-box">
      <div class="art-header">
        <h3>Master Studio Environment: Sunlit Artisan Kitchen & Workshop</h3>
        <span style="font-size:12px; color:#f59e0b; font-weight:600;">1080p Atmospheric 3-Plane Compositing</span>
      </div>

      <div class="art-canvas">
        <svg viewBox="0 0 960 540" width="100%" height="100%">
          <defs>
            <!-- Sky Gradient -->
            <linearGradient id="skyMorn" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#fdba74"/>
              <stop offset="50%" stop-color="#fef08a"/>
              <stop offset="100%" stop-color="#bfdbfe"/>
            </linearGradient>
            <!-- Golden Sunbeam Gradient -->
            <linearGradient id="sunBeam" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#fef08a" stop-opacity="0.55"/>
              <stop offset="40%" stop-color="#fef08a" stop-opacity="0.25"/>
              <stop offset="100%" stop-color="#fef08a" stop-opacity="0.0"/>
            </linearGradient>
            <!-- Wall Texture -->
            <linearGradient id="wallGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#f8fafc"/>
              <stop offset="70%" stop-color="#f1f5f9"/>
              <stop offset="100%" stop-color="#e2e8f0"/>
            </linearGradient>
            <!-- Wood Counter -->
            <linearGradient id="woodGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#78350f"/>
              <stop offset="60%" stop-color="#92400e"/>
              <stop offset="100%" stop-color="#b45309"/>
            </linearGradient>
          </defs>

          <!-- LAYER 1: BACKGROUND (City Horizon & Window) -->
          <!-- Wall Backdrop -->
          <rect x="0" y="0" width="960" height="540" fill="url(#wallGrad)"/>

          <!-- Grand Arched Studio Window (Center-Right) -->
          <g transform="translate(480, 40)">
            <!-- Outer Window Frame -->
            <path d="M0 160 A160 160 0 0 1 320 160 L320 400 L0 400 Z" fill="#0f172a"/>
            <!-- Glass Pane with Morning Sky -->
            <path d="M10 160 A150 150 0 0 1 310 160 L310 390 L10 390 Z" fill="url(#skyMorn)"/>

            <!-- Distant City Skyline Silhouettes -->
            <rect x="25" y="290" width="45" height="100" fill="#fed7aa" opacity="0.7"/>
            <rect x="75" y="260" width="55" height="130" fill="#fdba74" opacity="0.6"/>
            <rect x="135" y="310" width="40" height="80" fill="#fed7aa" opacity="0.8"/>
            <rect x="180" y="240" width="60" height="150" fill="#fca5a5" opacity="0.5"/>
            <rect x="245" y="280" width="50" height="110" fill="#fed7aa" opacity="0.7"/>

            <!-- Window Mullions & Grids -->
            <line x1="160" y1="10" x2="160" y2="390" stroke="#334155" stroke-width="4"/>
            <line x1="10" y1="200" x2="310" y2="200" stroke="#334155" stroke-width="3"/>
            <line x1="10" y1="300" x2="310" y2="300" stroke="#334155" stroke-width="3"/>

            <!-- Sheer Fluttering Linen Curtains -->
            <path d="M-10 120 Q30 240 10 390 L-20 390 Z" fill="#ffffff" opacity="0.65"/>
            <path d="M330 120 Q290 240 310 390 L340 390 Z" fill="#ffffff" opacity="0.65"/>
          </g>

          <!-- Volumetric Golden Sunbeams Streaming from Window -->
          <polygon points="490,160 960,320 960,540 540,540" fill="url(#sunBeam)"/>
          <polygon points="640,60 960,200 960,420 700,540" fill="url(#sunBeam)"/>

          <!-- Hanging Modern Brass Pendant Lamps (Left) -->
          <line x1="180" y1="0" x2="180" y2="140" stroke="#1e293b" stroke-width="2"/>
          <path d="M150 160 L210 160 L195 140 L165 140 Z" fill="#f59e0b"/>
          <circle cx="180" cy="165" r="8" fill="#fef08a"/>
          <circle cx="180" cy="165" r="35" fill="#fef08a" opacity="0.2"/>

          <line x1="320" y1="0" x2="320" y2="110" stroke="#1e293b" stroke-width="2"/>
          <path d="M295 130 L345 130 L332 110 L308 110 Z" fill="#f59e0b"/>
          <circle cx="320" cy="135" r="7" fill="#fef08a"/>
          <circle cx="320" cy="135" r="28" fill="#fef08a" opacity="0.2"/>

          <!-- Floating Flour Dust Particles in Sunbeam -->
          <circle cx="680" cy="240" r="1.5" fill="#ffffff" opacity="0.8"/>
          <circle cx="740" cy="280" r="2.0" fill="#ffffff" opacity="0.9"/>
          <circle cx="610" cy="320" r="1.2" fill="#ffffff" opacity="0.7"/>
          <circle cx="820" cy="210" r="1.8" fill="#ffffff" opacity="0.8"/>
          <circle cx="700" cy="380" r="2.2" fill="#ffffff" opacity="0.8"/>

          <!-- LAYER 2: MIDDLE-GROUND (Character Stool & Prep Island) -->
          <!-- Kitchen High Stool (Kabir's Stool) -->
          <g transform="translate(360, 290)">
            <ellipse cx="40" cy="40" rx="26" ry="7" fill="#334155"/>
            <line x1="22" y1="44" x2="14" y2="180" stroke="#0f172a" stroke-width="4"/>
            <line x1="58" y1="44" x2="66" y2="180" stroke="#0f172a" stroke-width="4"/>
            <line x1="40" y1="44" x2="40" y2="175" stroke="#0f172a" stroke-width="3"/>
            <ellipse cx="40" cy="120" rx="18" ry="4" fill="none" stroke="#0f172a" stroke-width="2.5"/>
          </g>

          <!-- LAYER 3: FOREGROUND (Artisan Wooden Counter & Props) -->
          <!-- Counter Top (Rustic Warm Walnut) -->
          <polygon points="0,380 960,380 960,540 0,540" fill="url(#woodGrad)"/>
          <line x1="0" y1="380" x2="960" y2="380" stroke="#fef3c7" stroke-width="2"/>
          <!-- Counter Front Drop Shadow -->
          <rect x="0" y="382" width="960" height="15" fill="#451a03" opacity="0.5"/>

          <!-- Foreground Prop 1: Handcrafted Floral Cupcakes Box (Hero Item) -->
          <g transform="translate(80, 395)">
            <!-- Kraft Gift Box -->
            <rect x="0" y="0" width="180" height="95" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
            <line x1="90" y1="0" x2="90" y2="95" stroke="#f59e0b" stroke-width="3"/> <!-- Ribbon -->
            <line x1="0" y1="45" x2="180" y2="45" stroke="#f59e0b" stroke-width="3"/>
            <!-- 4 Cupcakes inside with colorful frosting -->
            <circle cx="45" cy="22" r="16" fill="#f43f5e"/> <!-- Rose Pink -->
            <circle cx="135" cy="22" r="16" fill="#38bdf8"/> <!-- Sky Blue -->
            <circle cx="45" cy="70" r="16" fill="#fbbf24"/> <!-- Golden Vanilla -->
            <circle cx="135" cy="70" r="16" fill="#a855f7"/> <!-- Lavender -->
          </g>

          <!-- Foreground Prop 2: Smartphone on Counter with Screen Glow (Scene 2 Trigger) -->
          <g transform="translate(320, 420)">
            <rect x="0" y="0" width="45" height="75" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
            <rect x="3" y="3" width="39" height="69" rx="4" fill="#0284c7"/>
            <ellipse cx="22" cy="38" rx="28" ry="14" fill="#38bdf8" opacity="0.45"/> <!-- Screen Glow -->
            <line x1="10" y1="20" x2="34" y2="20" stroke="#ffffff" stroke-width="2"/>
            <line x1="10" y1="30" x2="28" y2="30" stroke="#ffffff" stroke-width="2"/>
          </g>

          <!-- Foreground Prop 3: Vintage Stainless Steel Whisk & Flour Bowl -->
          <g transform="translate(760, 405)">
            <ellipse cx="60" cy="75" rx="55" ry="25" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
            <ellipse cx="60" cy="70" rx="48" ry="18" fill="#f8fafc"/> <!-- Flour inside -->
            <!-- Whisk leaning -->
            <line x1="95" y1="20" x2="55" y2="75" stroke="#64748b" stroke-width="4"/>
            <ellipse cx="102" cy="12" rx="10" ry="6" fill="none" stroke="#475569" stroke-width="2.5" transform="rotate(-40 102 12)"/>
          </g>
        </svg>
      </div>
    </div>

    <!-- Directional Specifications Sidebar -->
    <div class="sidebar-box">
      <!-- Lighting & Camera -->
      <div class="info-panel">
        <h4>Cinematic Lighting & Camera Script</h4>
        <p>• <b>Morning Golden Hour</b>: 3500K warm volumetric keylight streaming through the arched studio window (direction: 45° from right).</p>
        <p>• <b>Ambient Fill</b>: Soft 5500K daylight ceiling fill bouncing off cream kitchen cabinets, preventing dark shadow clipping.</p>
        <p>• <b>Screen Bloom Event (00:10s)</b>: When order notification arrives, phone screen casts a vibrant 6500K cyan rim-light onto Aanya's hands and face.</p>
        <p>• <b>Camera Movement</b>: Gentle slow push-in (scale factor 1.0 -> 1.08) during Scene 1; snappy rack-focus whip to phone screen in Scene 2; wide triumphant pull-back into morning light in Scene 4.</p>
      </div>

      <!-- Color Script Across 4 Scenes -->
      <div class="info-panel">
        <h4>4-Scene Narrative Color Script</h4>
        <div class="color-script">
          <div class="cs-block">
            <div class="cs-bar" style="background: linear-gradient(135deg, #475569, #94a3b8);"></div>
            <div class="cs-title">Scene 1</div>
            <div class="cs-sub">Muted Doubt</div>
          </div>
          <div class="cs-block">
            <div class="cs-bar" style="background: linear-gradient(135deg, #0284c7, #38bdf8);"></div>
            <div class="cs-title">Scene 2</div>
            <div class="cs-sub">Cyan Ding</div>
          </div>
          <div class="cs-block">
            <div class="cs-bar" style="background: linear-gradient(135deg, #f59e0b, #fbbf24);"></div>
            <div class="cs-title">Scene 3</div>
            <div class="cs-sub">Warm Joy</div>
          </div>
          <div class="cs-block">
            <div class="cs-bar" style="background: linear-gradient(135deg, #fb923c, #fef08a);"></div>
            <div class="cs-title">Scene 4</div>
            <div class="cs-sub">Golden Sun</div>
          </div>
        </div>
      </div>

      <!-- Anti-Slideshow Standards -->
      <div class="info-panel">
        <h4>Mandatory Animation Standards</h4>
        <p>✔ <b>Multi-plane Parallax</b>: Window background, characters, and foreground counter operate on independent compositing layers.</p>
        <p>✔ <b>Secondary Dynamics</b>: Flour dust motes drift in sunbeams, sheer curtains wave, phone vibrates, apron straps swing.</p>
        <p>✔ <b>Acting Over Slideshows</b>: Body gestures (lip bite, gasp, tear drop, apron tie) communicate the story naturally.</p>
      </div>
    </div>
  </div>
</body>
</html>"""

out_png = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\visual_style_reference.png"
temp_html = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\style_ref.tmp.html"

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

print("Visual Style Reference Render Status:", res.returncode)
print("File size:", os.path.getsize(out_png) if os.path.exists(out_png) else 0)
