"""
generate_storyboard_773.py
==========================
Generates the 8-scene Master Production Storyboard for:
"लास्ट बग" (The Last Bug) - 60.00s Animated Short
Includes:
- Master 8-Panel 1920x1080 Grid
- Individual keyframe stills for each of the 8 cinematic beats
"""

import os
import subprocess
import tempfile

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3\storyboard"
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
# 8-PANEL MASTER STORYBOARD GRID (1920x1080)
# =============================================================================
master_grid_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Noto+Sans+Devanagari:wght@600;700&display=swap');
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 20px 30px;
    background: #090d16; color: #f1f5f9;
    font-family: 'Montserrat', sans-serif;
    width: 1920px; height: 1080px; overflow: hidden;
  }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 2px solid #f97316; padding-bottom: 8px; margin-bottom: 12px;
  }
  .title-block h1 { font-size: 26px; font-weight: 800; margin: 0; color: #ffffff; }
  .title-block .sub { font-size: 13px; color: #f97316; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; }

  .grid {
    display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: 1fr 1fr; gap: 14px; height: 950px;
  }
  .card {
    background: #111726; border: 1px solid #222f42; border-radius: 8px; padding: 10px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .card-header {
    display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; color: #f97316; margin-bottom: 6px;
  }
  .visual {
    width: 100%; height: 230px; background: #070a12; border-radius: 6px; overflow: hidden; border: 1px solid #1a2332;
  }
  .meta {
    font-size: 10.5px; color: #94a3b8; margin-top: 6px; line-height: 1.35;
  }
  .dialogue {
    font-family: 'Noto Sans Devanagari', sans-serif; font-size: 11.5px; font-weight: 600; color: #38bdf8;
    background: rgba(14, 165, 233, 0.1); padding: 4px 6px; border-radius: 4px; margin-top: 4px;
    border-left: 2px solid #38bdf8;
  }
</style>
</head>
<body>

  <div class="header">
    <div class="title-block">
      <h1>PRODUCTION STORYBOARD: "लास्ट बग" (THE LAST BUG)</h1>
      <div class="sub">60.00s Complete 2D Animated Short • 8 Cinematic Beats • Contemporary Bengaluru Indie Studio</div>
    </div>
    <div style="text-align:right; font-size:12px; color:#94a3b8;">
      Phase: <strong>7.7.3 Production</strong> • Aspect: <strong>16:9 Full HD (1920x1080)</strong> • FPS: <strong>24.0 CFR</strong>
    </div>
  </div>

  <div class="grid">
    <!-- BEAT 1 -->
    <div class="card">
      <div class="card-header"><span>BEAT 1: THE 3:00 AM CRISIS</span><span>0.0s – 7.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#0f172a"/>
          <rect x="60" y="30" width="320" height="150" fill="#450a0a" stroke="#ef4444" stroke-width="3" rx="6"/>
          <text x="220" y="70" font-family="'Montserrat'" font-size="14" font-weight="800" fill="#ef4444" text-anchor="middle">FATAL RUNTIME EXCEPTION</text>
          <text x="220" y="105" font-family="'Montserrat'" font-size="20" font-weight="800" fill="#ffffff" text-anchor="middle">LAUNCH: 00:00:59</text>
          <ellipse cx="220" cy="190" rx="35" ry="25" fill="#f97316"/>
          <!-- Hands on head -->
          <circle cx="195" cy="165" r="12" fill="#fdba74"/>
          <circle cx="245" cy="165" r="12" fill="#fdba74"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Hook:</strong> Flashing red alarm monitors at 3 AM. Kabir in total panic clutching hair.<br>
        <div class="dialogue">कबीर: "अरे मीरा! सर्वनाश हो गया! गेम क्रैश हो रहा है... लॉन्च में सिर्फ़ एक मिनट बचा है!"</div>
      </div>
    </div>

    <!-- BEAT 2 -->
    <div class="card">
      <div class="card-header"><span>BEAT 2: HACKER PARANOIA</span><span>7.5s – 15.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#0d1424"/>
          <!-- Kabir wildly pacing & pointing -->
          <ellipse cx="140" cy="140" rx="28" ry="40" fill="#ea580c"/>
          <circle cx="140" cy="85" r="18" fill="#fdba74"/>
          <line x1="140" y1="120" x2="220" y2="90" stroke="#fdba74" stroke-width="6" stroke-linecap="round"/>
          <!-- Meera enters holding coffee mug -->
          <ellipse cx="330" cy="140" rx="26" ry="45" fill="#2563eb"/>
          <circle cx="330" cy="80" r="16" fill="#fed7aa"/>
          <circle cx="330" cy="62" r="10" fill="#18181b"/> <!-- Top bun -->
          <rect x="290" y="125" width="16" height="20" fill="#fbbf24"/> <!-- Coffee mug -->
        </svg>
      </div>
      <div class="meta">
        <strong>Action:</strong> Kabir suspects a rival cyberattack. Meera enters calmly holding coffee.<br>
        <div class="dialogue">कबीर: "ज़रूर प्रतिद्वंद्वी कंपनी के हैकर ने कोड हैक कर लिया है!" मीरा: "शांत हो जाओ कबीर।"</div>
      </div>
    </div>

    <!-- BEAT 3 -->
    <div class="card">
      <div class="card-header"><span>BEAT 3: THE FORMAT BUTTON</span><span>15.0s – 22.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#0b101c"/>
          <!-- Giant Red Format Button on Monitor -->
          <rect x="80" y="50" width="280" height="130" fill="#1e293b" stroke="#64748b" stroke-width="2" rx="8"/>
          <rect x="110" y="80" width="220" height="70" fill="#dc2626" rx="6"/>
          <text x="220" y="122" font-family="'Montserrat'" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">PURGE &amp; FORMAT</text>
          <!-- Trembling cursor -->
          <polygon points="260,110 275,135 268,135 272,148 264,150 260,138 250,144" fill="#ffffff"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Conflict:</strong> Kabir prepares to wipe the entire database. High tension countdown.<br>
        <div class="dialogue">कबीर: "मैं सब कुछ फॉर्मेट कर रहा हूँ... कम से कम हमारा कोड तो नहीं चुरा पाएंगे!"</div>
      </div>
    </div>

    <!-- BEAT 4 -->
    <div class="card">
      <div class="card-header"><span>BEAT 4: MEERA STEPS IN</span><span>22.5s – 30.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#0c1220"/>
          <!-- Meera close-up over glasses -->
          <circle cx="220" cy="110" r="50" fill="#fed7aa"/>
          <circle cx="195" cy="105" r="16" fill="none" stroke="#d97706" stroke-width="3"/>
          <circle cx="245" cy="105" r="16" fill="none" stroke="#d97706" stroke-width="3"/>
          <circle cx="195" cy="105" r="4" fill="#312e81"/>
          <circle cx="245" cy="105" r="4" fill="#312e81"/>
          <path d="M190 70 Q170 120 185 160" stroke="#c084fc" stroke-width="6" stroke-linecap="round"/>
          <line x1="210" y1="180" x2="130" y2="210" stroke="#2563eb" stroke-width="14" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Turn:</strong> Meera pushes his trembling hand aside, eyes narrowing behind circular glasses.<br>
        <div class="dialogue">मीरा: "रुक जाओ कोडिंग के शेरलॉक होम्स! ज़रा मुझे देखने दो।"</div>
      </div>
    </div>

    <!-- BEAT 5 -->
    <div class="card">
      <div class="card-header"><span>BEAT 5: THE DESK DISCOVERY</span><span>30.0s – 37.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#1e1b18"/>
          <!-- Macro Table Shot -->
          <rect x="60" y="110" width="320" height="90" fill="#0f172a" rx="4"/>
          <!-- Mechanical Keyboard with RGB glow -->
          <line x1="80" y1="130" x2="360" y2="130" stroke="#f43f5e" stroke-width="3"/>
          <line x1="80" y1="150" x2="360" y2="150" stroke="#38bdf8" stroke-width="3"/>
          <!-- Giant Bhujia Packet & Steel Thermos pressing F5/ESC -->
          <polygon points="110,80 180,65 190,135 120,150" fill="#eab308" stroke="#ca8a04" stroke-width="2"/>
          <text x="145" y="115" font-family="'Montserrat'" font-size="10" font-weight="800" fill="#991b1b">BHUJIA</text>
          <rect x="210" y="45" width="45" height="110" rx="6" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Discovery:</strong> Meera tracks the cable: Kabir's steel thermos & Bhujia packet are wedged on F5 & ESC.<br>
        <div class="dialogue">[SFX: Mechanical keys jammed under heavy snack packet]</div>
      </div>
    </div>

    <!-- BEAT 6 -->
    <div class="card">
      <div class="card-header"><span>BEAT 6: THE LIFT & CLACK</span><span>37.5s – 45.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#042f2e"/>
          <!-- Hand lifting packet -->
          <polygon points="150,40 220,25 230,95 160,110" fill="#eab308"/>
          <!-- Emerald Green Compilation Pass Screen -->
          <rect x="80" y="130" width="280" height="85" fill="#064e3b" stroke="#10b981" stroke-width="2" rx="6"/>
          <text x="220" y="165" font-family="'Montserrat'" font-size="13" font-weight="800" fill="#34d399" text-anchor="middle">BUILD SUCCESSFUL • 248 TESTS PASSED</text>
          <text x="220" y="195" font-family="'Montserrat'" font-size="15" font-weight="800" fill="#ffffff" text-anchor="middle">READY TO DEPLOY</text>
        </svg>
      </div>
      <div class="meta">
        <strong>The Fix:</strong> Meera lifts the packet with two fingers. Keys pop up. Screen turns blazing green.<br>
        <div class="dialogue">[SFX: Crisp mechanical key spring CLACK • Triumphant server chime]</div>
      </div>
    </div>

    <!-- BEAT 7 -->
    <div class="card">
      <div class="card-header"><span>BEAT 7: STUNNED SLACK-JAW</span><span>45.0s – 52.5s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#0b1324"/>
          <!-- Kabir Stunned Face -->
          <circle cx="160" cy="115" r="45" fill="#fdba74"/>
          <ellipse cx="145" cy="105" rx="8" ry="7" fill="#ffffff"/>
          <circle cx="145" cy="105" r="3.5" fill="#78350f"/>
          <ellipse cx="175" cy="105" rx="8" ry="7" fill="#ffffff"/>
          <circle cx="175" cy="105" r="3.5" fill="#78350f"/>
          <ellipse cx="160" cy="140" rx="10" ry="14" fill="#451a03"/> <!-- Slack mouth -->
          <!-- Meera holding Bhujia packet smiling -->
          <circle cx="310" cy="110" r="40" fill="#fed7aa"/>
          <polygon points="340,90 380,80 385,120 345,130" fill="#eab308"/>
        </svg>
      </div>
      <div class="meta">
        <strong>Reaction:</strong> Kabir is frozen in comic disbelief. Meera takes a slow sip, raising the Bhujia.<br>
        <div class="dialogue">कबीर: "ये... ये भुजिया थी?!"</div>
      </div>
    </div>

    <!-- BEAT 8 -->
    <div class="card">
      <div class="card-header"><span>BEAT 8: PUNCHLINE & VICTORY</span><span>52.5s – 60.0s</span></div>
      <div class="visual">
        <svg width="100%" height="100%" viewBox="0 0 440 230">
          <rect width="440" height="230" fill="#090d16"/>
          <!-- App deployed popup -->
          <circle cx="150" cy="115" r="40" fill="#fdba74"/>
          <!-- Fist pump -->
          <line x1="180" y1="140" x2="205" y2="90" stroke="#f97316" stroke-width="12" stroke-linecap="round"/>
          <circle cx="300" cy="110" r="40" fill="#fed7aa"/>
          <rect x="110" y="15" width="220" height="30" rx="6" fill="#1e293b" stroke="#f97316" stroke-width="1.5"/>
          <text x="220" y="35" font-family="'Noto Sans Devanagari'" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">लास्ट बग — जीत की भुजिया</text>
        </svg>
      </div>
      <div class="meta">
        <strong>Ending:</strong> Meera delivers the punchline. Kabir laughs sheepishly, pumping fist as app deploys.<br>
        <div class="dialogue">मीरा: "हाँ! तो 'इंटरनेशनल हैकर' का नाम था... हल्दीराम की स्पेशल भुजिया!"</div>
      </div>
    </div>
  </div>

</body>
</html>"""
render_html_to_png(master_grid_html, os.path.join(OUTPUT_DIR, "storyboard_master.png"))
print("Master 8-Panel Storyboard Generated Successfully!")
