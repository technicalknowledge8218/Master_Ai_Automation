# 📱 Master AI — Guide 3: Android Termux Installation Guide
**Platform**: Master AI powered by Zovron Technologies  
**Target Audience**: Smartphone Creators & Mobile Developers  
**Prerequisites**: Any Android Phone (No PC/Laptop required!), Termux App from F-Droid  

---

## 1. Quick Overview

You do **NOT** need a computer or laptop! Master AI runs directly inside your Android smartphone using **Termux**. You can generate broadcast-quality 1080x1920 reels and save them directly to your phone's **Gallery / Downloads** folder ready to post on Instagram, YouTube Shorts, or TikTok.

---

## 2. ⚡ 1-Click Super Fast Install (Recommended)

Just open the **Termux** app on your phone, paste this single line, and hit Enter:

```bash
curl -sSL https://raw.githubusercontent.com/technicalknowledge8218/Master_Ai_Automation/main/install.sh | bash
```
*(This automatically installs packages, asks for your language, installs the lightweight 10MB video profile, and launches the wizard!)*

---

## 3. Manual Step-by-Step Installation (Alternative)

### Step 1: Open Termux & Update Packages
Open the Termux app on your phone and paste this single command:
```bash
pkg update && pkg install git python ffmpeg python-pillow python-numpy -y
```

### Step 2: Grant Phone Storage Permission
This allows Master AI to save rendered videos directly to your phone's Gallery / Downloads folder:
```bash
termux-setup-storage
```
*(A popup will appear on your phone screen: Tap **"Allow"**).*

### Step 3: Clone Master AI Repository
```bash
git clone https://github.com/technicalknowledge8218/Master_Ai_Automation.git
cd Master_Ai_Automation
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Method A: Interactive Mobile Terminal Wizard (Termux Grill-Me)

To produce a video directly from your phone's Termux command line:

```bash
python run.py
```

Termux will immediately launch the interactive **Grill-Me Protocol**:

```text
==============================================================
 ⚡ MASTER AI — INTERACTIVE REEL STUDIO (GRILL-ME PROTOCOL)
 Powered by Zovron Technologies | Universal Windows/Termux
==============================================================

[1/4] वीडियो का टॉपिक / टेक हुक क्या है?
(Default: Claude Code On Mobile Termux) > Best Android AI Tools 2026

[2/4] कैरेक्टर चुनें:
   1. Dev (Solo Tech Creator / Modern Builder)
   2. Neha (Tech Host & Explainer)
   3. Dr. Kabir (Senior Tech Mentor)
   4. Arjun (Energetic Builder)
नंबर चुनें [1-4] (Default: 1) > 1

[3/4] वीडियो कहाँ सेव करनी है?
   डिफ़ॉल्ट मोबाइल पाथ: /sdcard/Download/Master_AI_Videos
नया पाथ डालें या Enter दबाएं > [Press Enter]

[4/4] कॉल-टू-एक्शन (CTA) क्या रखें?
(Default: Comment TERMUX for Full Guide) > Share with Android Creators!
```

### 📱 Where to Find Your Video on Phone:
The video will be saved directly into your phone's internal storage:  
👉 **Files / File Manager $\to$ Downloads $\to$ Master_AI_Videos**  
You can open your phone's Gallery or Instagram app and upload it immediately!

---

## 4. Method B: Mobile Chrome Web Dashboard

If you prefer using your phone's touch screen with visual buttons instead of typing in Termux:

### Step 1: Start Mobile Server
In Termux, simply run:
```bash
bash start.sh
```

### Step 2: Open Mobile Chrome
Termux will automatically open your phone's browser, or you can manually open Chrome / Brave and visit:
👉 **`http://localhost:8080`**

### Step 3: Use the Responsive Touch Dashboard
1. **Tap & Type**: Enter your topic in the topic box.
2. **Tap Character**: Tap Dev, Neha, Dr. Kabir, or Arjun.
3. **Voice Vault**: Tap the Key icon to paste your Gemini API Key directly from your mobile clipboard.
4. **Tap Render**: Tap the **"Render Reel"** button.
5. The video renders on your phone's CPU and plays directly inside your mobile browser. Tap **Download** to save to your Gallery!
