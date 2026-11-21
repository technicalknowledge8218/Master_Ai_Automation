# 💻 Master AI — Guide 2: Windows PC & PowerShell Installation Guide
**Platform**: Master AI powered by JobRun Technologies  
**Target Audience**: Windows PC Users, Content Creators & Developers  
**Prerequisites**: Windows 10/11, Python 3.10+, Git (No AI software needed!)  

---

## 1. Quick Overview

You do **NOT** need any AI tool (no Cursor, no Claude, no Antigravity) installed on your PC. Master AI runs completely standalone via Windows **PowerShell** or through your browser via a lightweight local web dashboard.

---

## 2. Step-by-Step Copy-Paste Installation

### Step 1: Open Windows PowerShell
Press `Win + X` and select **Terminal** or **PowerShell**.

### Step 2: Clone the Master AI Repository
```powershell
git clone https://github.com/technicalknowledge8218/Master_Ai_Automation.git
cd Master_Ai_Automation
```

### Step 3: Install Required Dependencies
Run this single command to install video rendering and audio packages:
```powershell
pip install -r requirements.txt
```

---

## 3. Method A: Interactive Terminal Wizard (PowerShell Grill-Me)

To produce a video directly from your PowerShell terminal without opening a browser:

```powershell
python run.py
```

The interactive terminal wizard will immediately guide you step-by-step:

```text
==============================================================
 ⚡ MASTER AI — INTERACTIVE REEL STUDIO (GRILL-ME PROTOCOL)
 Powered by JobRun Technologies | Universal Windows/Termux
==============================================================

[1/4] वीडियो का टॉपिक / टेक हुक क्या है?
(Default: Claude Code On Mobile Termux) > AI Voice Clone Scam

[2/4] कैरेक्टर चुनें:
   1. Dev (Solo Tech Creator / Modern Builder)
   2. Neha (Tech Host & Explainer)
   3. Dr. Kabir (Senior Tech Mentor)
   4. Arjun (Energetic Builder)
नंबर चुनें [1-4] (Default: 1) > 2

[3/4] वीडियो कहाँ सेव करनी है?
   डिफ़ॉल्ट पाथ: C:\Users\Username\Desktop\Master_AI_Videos
नया पाथ डालें या Enter दबाएं > D:\My_Instagram_Reels

[4/4] कॉल-टू-एक्शन (CTA) क्या रखें?
(Default: Comment TERMUX for Full Guide) > Follow for Daily AI Safety Tips
```

### What Happens Next?
1. 🧠 **Autonomous Scriptwriting**: The Python script calls the Google Gemini REST API to write a viral 15s Devanagari Hindi script.
2. 🎙️ **Voice Synthesis**: Routed through the Multi-Provider Voice Vault (Gemini $\to$ ElevenLabs $\to$ Sarvam AI).
3. 🎬 **Local 2D Rendering**: FFmpeg generates the 1080x1920 video with decoupled mouth lip-sync, natural blinks, and dynamic subtitles.
4. 📁 **Final Video**: Saved directly to your selected folder (`D:\My_Instagram_Reels`)!

---

## 4. Method B: Visual Localhost Web Dashboard

If you prefer a visual web interface with buttons and live video preview:

### Step 1: Double-Click Startup
Double-click `start_dashboard.bat` (or run in PowerShell):
```powershell
.\start_dashboard.bat
```

### Step 2: Access in Browser
Your default browser will automatically open:
👉 **`http://localhost:8080`**

### Step 3: Configure Multi-Account Voice Vault
1. Click the **Voice API Vault** tab.
2. Add your free Google Gemini API Key (`AQ...` or `AIzaSy...`), ElevenLabs, or Sarvam AI key.
3. You can add 10 to 15 keys for automatic quota failover.

### Step 4: 1-Click Video Render
1. Enter your topic.
2. Select your character (Dev, Neha, Kabir, Arjun).
3. Click **RENDER VIRAL 1080x1920 REEL**.
4. Watch the video render live in the 9:16 vertical player, click play, and download!
