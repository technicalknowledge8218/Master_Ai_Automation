#!/usr/bin/env python3
"""
setup.py
Master AI — Interactive Modular Installer & Language Onboarding
Powered by Zovron Technologies
"""

import os
import sys
import json
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = WORKSPACE_ROOT / "00_CORE_SYSTEM" / "config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
PREFS_FILE = CONFIG_DIR / "user_preferences.json"


def load_preferences():
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"language": "hinglish", "profile": "video"}


def save_preferences(prefs):
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)


def run_setup():
    print("\n" + "=" * 65)
    print(" 🚀 MASTER AI — ONBOARDING & SETUP WIZARD")
    print(" Powered by Zovron Technologies (zovron.tech)")
    print("=" * 65 + "\n")

    prefs = load_preferences()

    # Step 1: Language Selection
    print("🌐 [1/2] Choose Your Preferred Language / अपनी भाषा चुनें:")
    print("   1. हिन्दी (Pure Devanagari Hindi)")
    print("   2. Hinglish (Romanized Hindi - Recommended for Termux) [Default]")
    print("   3. English (International Standard)")
    try:
        lang_choice = input("Select / चुनें [1-3] (Default: 2) > ").strip()
    except (EOFError, KeyboardInterrupt):
        lang_choice = "2"

    lang_map = {"1": "hindi", "2": "hinglish", "3": "english"}
    selected_lang = lang_map.get(lang_choice, "hinglish")
    prefs["language"] = selected_lang
    save_preferences(prefs)

    lang_labels = {
        "hindi": "हिन्दी (Hindi)",
        "hinglish": "Hinglish (रोमन हिंदी)",
        "english": "English"
    }
    print(f"   ✔ Selected Language: {lang_labels[selected_lang]}\n")

    # Step 2: Installation Profile Selection
    if selected_lang == "hindi":
        print("📦 [2/2] इंस्टॉलेशन प्रोफ़ाइल चुनें:")
        print("   1. 🎬 केवल वीडियो रील स्टूडियो (~10 MB - मोबाइल/टर्मक्स के लिए सबसे तेज़) [Default]")
        print("   2. ⚡ ऑटोमेशन और वर्कफ़्लो इंजन (~35 MB)")
        print("   3. 🖥️ संपूर्ण वर्कस्टेशन सूट (PC / वर्कस्टेशन के लिए - 250 MB+)")
    elif selected_lang == "hinglish":
        print("📦 [2/2] Installation Profile chunein:")
        print("   1. 🎬 Video Reel Studio Only (~10 MB - Mobile/Termux ke liye Fastest) [Default]")
        print("   2. ⚡ Automation & Workflow Engine (~35 MB)")
        print("   3. 🖥️ Full Workstation Suite (Desktop PC ke liye - 250 MB+)")
    else:
        print("📦 [2/2] Select Installation Profile:")
        print("   1. 🎬 Video Reel Studio Only (~10 MB - Recommended for Mobile/Termux) [Default]")
        print("   2. ⚡ Automation & Workflow Engine (~35 MB)")
        print("   3. 🖥️ Full Workstation Suite (PC Workstation - 250 MB+)")

    try:
        prof_choice = input("Select Profile [1-3] (Default: 1) > ").strip()
    except (EOFError, KeyboardInterrupt):
        prof_choice = "1"
    prof_map = {
        "1": ("video", "requirements-video.txt"),
        "2": ("automation", "requirements-automation.txt"),
        "3": ("full", "requirements-full.txt")
    }
    profile_key, req_file = prof_map.get(prof_choice, prof_map["1"])
    prefs["profile"] = profile_key
    save_preferences(prefs)

    req_path = WORKSPACE_ROOT / req_file
    print(f"\n⏳ Installing dependencies from {req_file}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_path)])
        print("\n✔ Dependencies installed successfully!")
    except Exception as e:
        print(f"\n⚠️ Installation notice: {e}")
        print("💡 On Termux, you can also run: pkg install python-pillow -y")

    # Success & launch guidance
    print("\n" + "=" * 65)
    if selected_lang == "hindi":
        print("🎉 सेटअप पूरा हुआ! अब आप मास्टर एआई शुरू कर सकते हैं:")
        print("   👉 टर्मिनल विज़ार्ड के लिए:  python run.py")
        print("   👉 वेब डैशबोर्ड के लिए:     bash start.sh  (ब्राउज़र: http://localhost:8080)")
        launch_prompt = "\n🚀 क्या आप अभी Localhost वेब डैशबोर्ड शुरू करना चाहते हैं? [Y/n] > "
    elif selected_lang == "english":
        print("🎉 Setup Complete! You can now launch Master AI:")
        print("   👉 Terminal Wizard:  python run.py")
        print("   👉 Web Dashboard:    bash start.sh  (Browser: http://localhost:8080)")
        launch_prompt = "\n🚀 Launch Localhost Web Dashboard now? [Y/n] > "
    else:
        print("🎉 Setup Complete! Ab aap Master AI start kar sakte hain:")
        print("   👉 Terminal Wizard ke liye:  python run.py")
        print("   👉 Web Dashboard ke liye:    bash start.sh  (Browser: http://localhost:8080)")
        launch_prompt = "\n🚀 Localhost Web Dashboard abhi start karein? [Y/n] > "
    print("=" * 65 + "\n")

    try:
        launch_now = input(launch_prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        launch_now = "y"

    if launch_now in ["", "y", "yes"]:
        import shutil
        if shutil.which("termux-open-url"):
            try:
                subprocess.Popen(["termux-open-url", "http://localhost:8080"])
            except Exception:
                pass
        elif shutil.which("xdg-open"):
            try:
                subprocess.Popen(["xdg-open", "http://localhost:8080"])
            except Exception:
                pass

        server_script = WORKSPACE_ROOT / "00_CORE_SYSTEM" / "dashboard" / "server.py"
        subprocess.call([sys.executable, str(server_script)])


if __name__ == "__main__":
    run_setup()
