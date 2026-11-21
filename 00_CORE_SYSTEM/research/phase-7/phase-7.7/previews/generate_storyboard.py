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
    background: #090d16;
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
    margin-bottom: 18px;
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
  .storyboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    height: 960px;
  }
  .sb-card {
    background: #131b2e;
    border: 1px solid #23314f;
    border-radius: 10px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .sb-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #23314f;
    padding-bottom: 6px;
  }
  .sb-title {
    font-size: 15px;
    font-weight: 800;
    color: #f8fafc;
  }
  .sb-time {
    font-size: 12px;
    font-weight: 700;
    color: #f59e0b;
    background: #090d16;
    padding: 3px 8px;
    border-radius: 4px;
  }
  .panel-art {
    height: 240px;
    background: #050811;
    border: 1px solid #23314f;
    border-radius: 6px;
    overflow: hidden;
    position: relative;
  }
  .sb-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    font-size: 11px;
    background: #090d16;
    border: 1px solid #23314f;
    border-radius: 6px;
    padding: 8px 12px;
  }
  .info-item b {
    color: #f59e0b;
  }
  .dialogue-box {
    background: #1a243b;
    border-left: 4px solid #f59e0b;
    padding: 6px 10px;
    border-radius: 0 4px 4px 0;
    font-size: 12px;
    color: #e2e8f0;
    font-family: 'Noto Sans Devanagari', sans-serif;
    line-height: 1.4;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>MASTER AI — PHASE 7.7 CINEMATIC STORYBOARD SPECIFICATION</h1>
      <p>Original 30-Second 2D Production: 'पहला ऑर्डर' (The First Order) // Visual Narrative Pacing & Shot Direction</p>
    </div>
    <div class="badge">STORYBOARD SEQUENCE // 4 KEY SCENES</div>
  </div>

  <div class="storyboard-grid">
    <!-- PANEL 1: SCENE 1 -->
    <div class="sb-card">
      <div class="sb-header">
        <span class="sb-title">SCENE 1: The Weight of Silence</span>
        <span class="sb-time">00:00 – 00:08 (8.0s)</span>
      </div>
      <div class="panel-art">
        <svg viewBox="0 0 440 240" width="100%" height="100%">
          <!-- Background Wall & Window -->
          <rect x="0" y="0" width="440" height="240" fill="#1e293b"/>
          <!-- Window with early morning cool haze -->
          <rect x="260" y="20" width="150" height="150" rx="8" fill="#cbd5e1" opacity="0.4"/>
          <line x1="335" y1="20" x2="335" y2="170" stroke="#0f172a" stroke-width="2"/>
          <line x1="260" y1="95" x2="410" y2="95" stroke="#0f172a" stroke-width="2"/>
          <!-- Counter -->
          <polygon points="0,170 440,170 440,240 0,240" fill="#78350f"/>
          <!-- Cupcake Box on counter -->
          <rect x="40" y="175" width="70" height="40" rx="3" fill="#fef3c7" stroke="#d97706"/>
          <!-- Aanya (Slumped, Biting Lip, Staring at Phone) -->
          <g transform="translate(130, 60)">
            <ellipse cx="40" cy="30" rx="14" ry="17" fill="#fcd5b5"/>
            <path d="M26 30 C26 15 35 10 40 10 C46 10 54 15 54 30 Z" fill="#3d2314"/>
            <ellipse cx="40" cy="8" rx="8" ry="7" fill="#3d2314"/> <!-- Bun -->
            <!-- Slumped shoulders -->
            <path d="M25 46 Q40 50 55 46 L65 110 L15 110 Z" fill="#fdfbf7"/>
            <!-- Head angled down in dejection -->
            <ellipse cx="34" cy="32" rx="2" ry="2" fill="#78350f"/>
            <path d="M30 40 Q35 44 40 40" stroke="#be123c" stroke-width="1.5" fill="none"/>
          </g>
          <!-- Phone on counter with black screen -->
          <rect x="220" y="185" width="20" height="32" rx="3" fill="#0f172a" stroke="#475569"/>
          <!-- Kabir sitting on stool sipping chai (Right) -->
          <g transform="translate(320, 90)">
            <ellipse cx="25" cy="25" rx="12" ry="14" fill="#fcd5b5"/>
            <path d="M20 20 Q26 12 32 20" fill="#172554"/>
            <rect x="12" y="38" width="28" height="50" rx="4" fill="#4d7c0f"/>
            <rect x="22" y="55" width="10" height="12" fill="#fbbf24"/> <!-- Chai glass -->
          </g>
        </svg>
      </div>
      <div class="sb-info">
        <div class="info-item"><b>Camera:</b> Slow Push-In (1.0x -> 1.06x), Eye-level</div>
        <div class="info-item"><b>Lighting:</b> Muted 4500K morning cool fill</div>
        <div class="info-item"><b>Acting:</b> Slumped posture, lip bite, phone glance</div>
        <div class="info-item"><b>SFX:</b> Soft ceramic mug clink on counter (4.5s)</div>
      </div>
      <div class="dialogue-box">
        <b>आन्या:</b> "तीन हफ्ते हो गए कबीर... एक भी कस्टमर नहीं आया। शायद मुझे ये सब बंद कर देना चाहिए।"
      </div>
    </div>

    <!-- PANEL 2: SCENE 2 -->
    <div class="sb-card">
      <div class="sb-header">
        <span class="sb-title">SCENE 2: The Electric Ding</span>
        <span class="sb-time">00:08 – 00:16 (8.0s)</span>
      </div>
      <div class="panel-art">
        <svg viewBox="0 0 440 240" width="100%" height="100%">
          <rect x="0" y="0" width="440" height="240" fill="#0f172a"/>
          <!-- Counter Top -->
          <polygon points="0,170 440,170 440,240 0,240" fill="#78350f"/>
          <!-- Cyan Screen Light Flash Beam! -->
          <polygon points="210,180 0,60 0,240 440,240 440,60" fill="#38bdf8" opacity="0.25"/>
          <ellipse cx="220" cy="190" rx="90" ry="40" fill="#38bdf8" opacity="0.4"/>
          <!-- Glowing Phone on counter -->
          <g transform="translate(205, 175)">
            <rect x="0" y="0" width="30" height="48" rx="4" fill="#0284c7" stroke="#ffffff" stroke-width="2"/>
            <circle cx="15" cy="18" r="6" fill="#ffffff"/> <!-- Ding Icon -->
          </g>
          <!-- Both Characters Startled & Looking Down -->
          <!-- Aanya Gasps (Left) -->
          <g transform="translate(110, 50)">
            <ellipse cx="40" cy="30" rx="15" ry="18" fill="#fcd5b5"/>
            <ellipse cx="40" cy="8" rx="9" ry="8" fill="#3d2314"/>
            <path d="M22 46 Q40 48 58 46 L68 115 L12 115 Z" fill="#fdfbf7"/>
            <!-- Wide startled eyes illuminated by cyan glow -->
            <ellipse cx="36" cy="28" rx="3.5" ry="4" fill="#ffffff"/><circle cx="36" cy="28" r="2" fill="#0284c7"/>
            <ellipse cx="46" cy="28" rx="3.5" ry="4" fill="#ffffff"/><circle cx="46" cy="28" r="2" fill="#0284c7"/>
            <ellipse cx="41" cy="40" rx="3.5" ry="5" fill="#be123c"/>
          </g>
          <!-- Kabir Points (Right) -->
          <g transform="translate(270, 50)">
            <ellipse cx="30" cy="28" rx="14" ry="16" fill="#fcd5b5"/>
            <path d="M20 18 Q30 10 38 18" fill="#172554"/>
            <rect x="18" y="44" width="30" height="60" rx="4" fill="#4d7c0f"/>
            <!-- Arm pointing toward phone -->
            <line x1="22" y1="55" x2="-20" y2="120" stroke="#fcd5b5" stroke-width="6"/>
          </g>
        </svg>
      </div>
      <div class="sb-info">
        <div class="info-item"><b>Camera:</b> Dynamic Whip Rack-Focus to phone screen</div>
        <div class="info-item"><b>Lighting:</b> Dramatic 6500K Cyan Screen Bloom flash</div>
        <div class="info-item"><b>Acting:</b> Sudden alert, dilated pupils, brother points</div>
        <div class="info-item"><b>SFX:</b> Crisp modern phone chime: 'DING!' (10.2s)</div>
      </div>
      <div class="dialogue-box">
        <b>कबीर:</b> "दीदी, इतनी जल्दी हिम्मत हारोगी?... अरे सुनो! फ़ोन पर क्या बजा?"
      </div>
    </div>

    <!-- PANEL 3: SCENE 3 -->
    <div class="sb-card">
      <div class="sb-header">
        <span class="sb-title">SCENE 3: The First Order Unlocked</span>
        <span class="sb-time">00:16 – 00:23 (7.0s)</span>
      </div>
      <div class="panel-art">
        <svg viewBox="0 0 440 240" width="100%" height="100%">
          <!-- Close-Up Framing -->
          <rect x="0" y="0" width="440" height="240" fill="#1e293b"/>
          <!-- Warm Amber Radiance Backdrop -->
          <ellipse cx="220" cy="120" rx="180" ry="120" fill="#f59e0b" opacity="0.2"/>
          <!-- Phone Interface in Center-Left (Aanya holding it) -->
          <rect x="40" y="30" width="150" height="180" rx="10" fill="#ffffff" stroke="#f59e0b" stroke-width="3"/>
          <rect x="55" y="45" width="120" height="26" rx="4" fill="#22c55e"/> <!-- Green Verified -->
          <text x="75" y="62" fill="#ffffff" font-size="11" font-weight="bold">ORDER #1001</text>
          <text x="55" y="95" fill="#0f172a" font-size="11" font-weight="bold">24 Truffle Cupcakes</text>
          <text x="55" y="115" fill="#64748b" font-size="10">Delivery: Today 4 PM</text>
          <text x="55" y="145" fill="#b45309" font-size="13" font-weight="bold">PAID: ₹2,400</text>

          <!-- Aanya Extreme Emotional Close-Up (Right) -->
          <g transform="translate(250, 20)">
            <path d="M30 40 C30 10 110 10 110 40 C110 120 90 150 70 155 C50 150 30 120 30 40 Z" fill="#fcd5b5"/>
            <!-- Messy Bun & Hair -->
            <ellipse cx="70" cy="10" rx="22" ry="18" fill="#3d2314"/>
            <!-- Huge Expressive Hazel Eyes with Glistening Tears -->
            <ellipse cx="54" cy="55" rx="10" ry="7" fill="#ffffff"/><circle cx="55" cy="55" r="4.5" fill="#78350f"/>
            <ellipse cx="88" cy="55" rx="10" ry="7" fill="#ffffff"/><circle cx="87" cy="55" r="4.5" fill="#78350f"/>
            <!-- Tear Droplets rolling down cheek -->
            <circle cx="50" cy="72" r="3.5" fill="#38bdf8"/>
            <circle cx="92" cy="72" r="3.5" fill="#38bdf8"/>
            <!-- Trembling Joyful Smile -->
            <path d="M52 105 Q70 125 88 105" stroke="#be123c" stroke-width="3.5" fill="none"/>
          </g>
        </svg>
      </div>
      <div class="sb-info">
        <div class="info-item"><b>Camera:</b> Tight emotive close-up, shallow depth</div>
        <div class="info-item"><b>Lighting:</b> Warm 3500K golden amber key-light</div>
        <div class="info-item"><b>Acting:</b> Trembling hands, happy tear drop, joyful smile</div>
        <div class="info-item"><b>SFX:</b> Fabric rustle as apron is unfolded (16.8s)</div>
      </div>
      <div class="dialogue-box">
        <b>आन्या:</b> "कबीर... देखो! सच में पहला ऑर्डर आ गया!"
      </div>
    </div>

    <!-- PANEL 4: SCENE 4 -->
    <div class="sb-card">
      <div class="sb-header">
        <span class="sb-title">SCENE 4: The Baker's Apron & The Dawn</span>
        <span class="sb-time">00:23 – 00:30 (7.0s)</span>
      </div>
      <div class="panel-art">
        <svg viewBox="0 0 440 240" width="100%" height="100%">
          <!-- Radiant Golden Morning Sunlight Flood -->
          <rect x="0" y="0" width="440" height="240" fill="#fef3c7"/>
          <polygon points="180,0 440,0 440,240 280,240" fill="#fde047" opacity="0.45"/>
          <!-- Window Background with City in Sunlight -->
          <rect x="220" y="20" width="190" height="140" rx="8" fill="#ffffff" opacity="0.6"/>
          <!-- Counter in Foreground -->
          <polygon points="0,180 440,180 440,240 0,240" fill="#92400e"/>

          <!-- Aanya Tying Apron with Radiant Smile (Center) -->
          <g transform="translate(140, 20)">
            <ellipse cx="60" cy="35" rx="16" ry="19" fill="#fcd5b5"/>
            <ellipse cx="60" cy="12" rx="10" ry="9" fill="#3d2314"/>
            <!-- Heroic Apron Tied firmly with straps pulled back -->
            <path d="M38 55 L82 55 L90 160 L30 160 Z" fill="#1e293b"/>
            <!-- Brass Buckles gleaming in sunlight -->
            <circle cx="44" cy="58" r="3.5" fill="#f59e0b"/>
            <circle cx="76" cy="58" r="3.5" fill="#f59e0b"/>
            <!-- Arms behind waist tying knot -->
            <line x1="30" y1="100" x2="15" y2="125" stroke="#fcd5b5" stroke-width="5"/>
            <line x1="90" y1="100" x2="105" y2="125" stroke="#fcd5b5" stroke-width="5"/>
            <!-- Radiant Confident Smile -->
            <ellipse cx="53" cy="34" rx="3.5" ry="3" fill="#ffffff"/><circle cx="53" cy="34" r="2" fill="#78350f"/>
            <ellipse cx="67" cy="34" rx="3.5" ry="3" fill="#ffffff"/><circle cx="67" cy="34" r="2" fill="#78350f"/>
            <path d="M52 48 Q60 54 68 48" stroke="#be123c" stroke-width="2.5" fill="none"/>
          </g>

          <!-- Kabir Cheering with proud thumb-up (Left) -->
          <g transform="translate(30, 60)">
            <ellipse cx="30" cy="26" rx="12" ry="14" fill="#fcd5b5"/>
            <path d="M22 16 Q30 10 38 16" fill="#172554"/>
            <rect x="18" y="40" width="28" height="55" rx="4" fill="#4d7c0f"/>
            <!-- Thumb-up hand -->
            <line x1="46" y1="55" x2="70" y2="40" stroke="#fcd5b5" stroke-width="5"/>
            <circle cx="72" cy="38" r="4" fill="#fcd5b5"/>
          </g>
        </svg>
      </div>
      <div class="sb-info">
        <div class="info-item"><b>Camera:</b> Wide cinematic pull-out into morning golden sun</div>
        <div class="info-item"><b>Lighting:</b> Soaring 3200K Golden Sunbeam flood</div>
        <div class="info-item"><b>Acting:</b> Apron tie knot, proud grin, radiant confidence</div>
        <div class="info-item"><b>SFX:</b> Apron strap snap (24.0s) & morning bird chirp</div>
      </div>
      <div class="dialogue-box">
        <b>कबीर:</b> "कहा था ना मैंने! अब अपना एप्रन पहनिए शेफ़ साहिबा... आपकी नई शुरुआत हो गई!"
      </div>
    </div>
  </div>
</body>
</html>"""

out_png = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\storyboard_panels.png"
temp_html = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7\previews\storyboard.tmp.html"

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

print("Storyboard Panels Render Status:", res.returncode)
print("File size:", os.path.getsize(out_png) if os.path.exists(out_png) else 0)
