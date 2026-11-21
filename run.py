"""
run.py
Master AI — Universal Tri-Lingual Interactive Reel Wizard (Grill-Me Protocol)
Works seamlessly on Windows PowerShell, macOS, Linux, and Android Termux!
Powered by Zovron Technologies (zovron.tech)
Zero hardcoded paths: 100% relative and dynamic.
"""

import os
import sys
import time
import json
import shutil
import platform
import subprocess
from pathlib import Path
import urllib.request
import urllib.error

# Resolve Workspace Root dynamically from current file location
WORKSPACE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE_ROOT))

CONFIG_DIR = WORKSPACE_ROOT / "00_CORE_SYSTEM" / "config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
PREFS_FILE = CONFIG_DIR / "user_preferences.json"


def get_user_language() -> str:
    """Loads saved language or prompts user on first launch."""
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "language" in data:
                    return data["language"]
        except Exception:
            pass

    # Prompt user on first run
    print("\n" + "=" * 62)
    print(" 🌐 CHOOSE YOUR LANGUAGE / अपनी भाषा चुनें")
    print(" Powered by Zovron Technologies")
    print("=" * 62)
    print("   1. हिन्दी (Pure Devanagari Hindi)")
    print("   2. Hinglish (Romanized Hindi - Recommended for Termux) [Default]")
    print("   3. English (International Standard)")
    choice = input("Select / चुनें [1-3] (Default: 2) > ").strip()

    lang_map = {"1": "hindi", "2": "hinglish", "3": "english"}
    chosen = lang_map.get(choice, "hinglish")

    # Save preference
    prefs = {"language": chosen, "profile": "video"}
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r", encoding="utf-8") as f:
                prefs = json.load(f)
        except Exception:
            pass
    prefs["language"] = chosen
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)

    return chosen


# Detect default save directory based on OS
def get_default_output_dir() -> Path:
    # Check if running inside Android Termux
    if "com.termux" in os.environ.get("PREFIX", ""):
        termux_download = Path.home() / "storage" / "downloads"
        termux_shared = Path.home() / "storage" / "shared" / "Download"
        if termux_download.exists():
            return termux_download / "Master_AI_Videos"
        elif termux_shared.exists():
            return termux_shared / "Master_AI_Videos"
        elif Path("/sdcard/Download").exists():
            return Path("/sdcard/Download/Master_AI_Videos")
        else:
            return WORKSPACE_ROOT / "output_videos"
    else:
        # Standard Desktop directory
        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            return desktop_dir / "Master_AI_Videos"
        else:
            return WORKSPACE_ROOT / "16_VIDEO_LIBRARY"


def generate_devanagari_script_via_gemini(topic: str, character: str, cta: str, api_key: str, language: str = "hinglish") -> str:
    """Uses Google Gemini REST API to autonomously draft a viral 15s script adapted to language choice."""
    clean_key = api_key.strip()
    if not clean_key or clean_key.startswith("YOUR_") or "DEMO" in clean_key:
        if language == "hindi":
            return "पहले टर्मक्स में नोड जेएस इन्स्टॉल करो, फिर क्लॉड कमांड रन करो और पूरा एआई मोबाइल में रेडी!"
        elif language == "english":
            return "First install Node.js in Termux, then run the Claude command, and your full AI workstation is ready on mobile!"
        else:
            return "Pehle Termux me Node.js install karo, fir Claude command run karo aur poora AI mobile me ready!"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
    headers = {"Content-Type": "application/json"}
    
    if language == "hindi":
        lang_rule = "Write in PURE DEVANAGARI HINDI PHONETICS even for English technical words (e.g. Termux -> टर्मक्स, Node.js -> नोड जेएस, Claude -> क्लॉड)."
    elif language == "english":
        lang_rule = "Write in energetic, punchy modern English."
    else:
        lang_rule = "Write in high-retention natural Hinglish (Romanized Hindi + technical English terms)."

    prompt_text = f"""
    Write a high-retention 15-second viral video reel script on topic: "{topic}".
    Speaker character: "{character}".
    Target Call to Action (CTA): "{cta}".
    
    CRITICAL RULES:
    1. {lang_rule}
    2. Hook must be explosive in the first 3 seconds.
    3. Length must be strictly between 25 and 35 words (fits 12-15 seconds speech).
    4. Return ONLY the spoken text. No character names, no brackets, no stage directions.
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 200}
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        candidate = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        candidate = candidate.replace('"', '').replace("'", "").replace("\n", " ").strip()
        return candidate
    except Exception:
        if language == "hindi":
            return "पहले टर्मक्स में नोड जेएस इन्स्टॉल करो, फिर क्लॉड कमांड रन करो और पूरा एआई मोबाइल में रेडी!"
        elif language == "english":
            return "First install Node.js in Termux, then run the Claude command, and your full AI workstation is ready on mobile!"
        else:
            return "Pehle Termux me Node.js install karo, fir Claude command run karo aur poora AI mobile me ready!"


def interactive_wizard():
    language = get_user_language()

    print("\n" + "=" * 62)
    print(" ⚡ MASTER AI — INTERACTIVE REEL STUDIO (GRILL-ME PROTOCOL)")
    print(" Powered by Zovron Technologies | Universal Windows/Termux")
    print("=" * 62 + "\n")

    # Localized Prompts
    if language == "hindi":
        p1 = "[1/4] वीडियो का मुख्य विषय / टेक हुक क्या है?\n(Default: Claude Code On Mobile Termux) > "
        p2_head = "\n[2/4] कैरेक्टर चुनें:"
        p3_head = "\n[3/4] वीडियो कहाँ सेव करनी है?"
        p3_def = "   डिफ़ॉल्ट पाथ:"
        p3_prompt = "नया पाथ डालें या Enter दबाएं > "
        p4 = "\n[4/4] कॉल-टू-एक्शन (CTA) क्या रखें?\n(Default: Comment TERMUX for Full Guide) > "
        perm_err = "Storage Permission नहीं मिली"
        perm_tip = "फोन गैलरी में सेव करने के लिए Termux में 'termux-setup-storage' रन करके Allow दबाएं"
        script_step = "🧠 [चरण 1/4] एआई से स्क्रिप्ट लिखवाई जा रही है..."
        voice_step = "🎙️ [चरण 2/4] वॉइस वॉल्ट से आवाज़ जनरेट हो रही है..."
        render_step = "🎬 [चरण 3/4] 2D कैरेक्टर रिग, लिप-सिंक व सबटाइटल्स रेंडर हो रहे हैं..."
        success_title = "🎉 बधाई! 1080x1920 वायरल रील तैयार हो गई है!"
    elif language == "english":
        p1 = "[1/4] What is your video topic or core hook?\n(Default: Claude Code On Mobile Termux) > "
        p2_head = "\n[2/4] Select Character Archetype:"
        p3_head = "\n[3/4] Where should the video be saved?"
        p3_def = "   Default Path:"
        p3_prompt = "Enter custom path or press Enter > "
        p4 = "\n[4/4] Call to Action (CTA)?\n(Default: Comment TERMUX for Full Guide) > "
        perm_err = "Storage Permission Denied"
        perm_tip = "Grant phone storage access in Termux via: termux-setup-storage"
        script_step = "🧠 [Step 1/4] AI is drafting high-retention viral script..."
        voice_step = "🎙️ [Step 2/4] Synthesizing speech via Voice Vault..."
        render_step = "🎬 [Step 3/4] Rendering 2D character rig, lip-sync & typography..."
        success_title = "🎉 Success! Broadcast-grade 1080x1920 reel rendered!"
    else:  # hinglish
        p1 = "[1/4] Video ka topic ya main hook kya hai?\n(Default: Claude Code On Mobile Termux) > "
        p2_head = "\n[2/4] Character Archetype chunein:"
        p3_head = "\n[3/4] Video kahan save karni hai?"
        p3_def = "   Default Path:"
        p3_prompt = "Custom path dalein ya Enter dabayein > "
        p4 = "\n[4/4] Call-to-Action (CTA) kya rakhein?\n(Default: Comment TERMUX for Full Guide) > "
        perm_err = "Storage Permission nahi mili"
        perm_tip = "Phone storage allow karne ke liye Termux me 'termux-setup-storage' run karke Allow dabayein"
        script_step = "🧠 [Step 1/4] AI viral script draft kar raha hai..."
        voice_step = "🎙️ [Step 2/4] Voice Vault se audio generate ho rahi hai..."
        render_step = "🎬 [Step 3/4] 2D Character rig, lip-sync aur subtitles render ho rahe hain..."
        success_title = "🎉 Badhaai! 1080x1920 viral reel render ho chuki hai!"

    # 1. Topic
    topic_input = input(p1).strip()
    topic = topic_input if topic_input else "Claude Code On Mobile Termux"

    # 2. Character
    print(p2_head)
    print("   1. Dev (Solo Tech Creator / Modern Builder)")
    print("   2. Neha (Tech Host & Explainer)")
    print("   3. Dr. Kabir (Senior Tech Mentor)")
    print("   4. Arjun (Energetic Builder)")
    char_choice = input("Select [1-4] (Default: 1) > ").strip()
    char_map = {"1": "dev", "2": "neha", "3": "kabir", "4": "arjun"}
    character = char_map.get(char_choice, "dev")

    # 3. Save Path
    default_save = get_default_output_dir()
    print(p3_head)
    print(f"{p3_def} {default_save}")
    user_save_path = input(p3_prompt).strip()

    if user_save_path:
        out_dir = Path(user_save_path).resolve()
    else:
        out_dir = default_save

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        fallback_dir = WORKSPACE_ROOT / "output_videos"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n   ⚠️ {perm_err}: {out_dir}")
        print(f"   📁 Fallback: {fallback_dir}")
        print(f"   💡 (Tip: {perm_tip})")
        out_dir = fallback_dir

    print(f"   ✔ Save Location: {out_dir}")

    # 4. CTA
    cta_input = input(p4).strip()
    cta = cta_input if cta_input else "Comment TERMUX for Full Guide"

    # Voice Vault Key Check
    import importlib
    vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
    vault = vv.vault

    gemini_keys = [k["key"] for k in vault.config.get("gemini", []) if k.get("status") == "active" and k.get("key") and not k.get("key", "").startswith("YOUR_") and "DEMO" not in k.get("label", "").upper()]
    primary_key = gemini_keys[0] if gemini_keys else os.getenv("GEMINI_API_KEY", "")

    if not primary_key:
        print("\n🔑 [Voice Vault Setup] No active Gemini API Key detected.")
        key_input = input("Paste your free Google Gemini API Key (or press Enter): ").strip()
        if key_input:
            primary_key = key_input
            vault.add_key("gemini", primary_key, label="User Mobile Key")
            print("   ✔ Gemini API Key saved to Voice Vault successfully!")

    print("\n" + "-" * 60)
    print(script_step)
    script_text = generate_devanagari_script_via_gemini(topic, character, cta, primary_key, language=language)
    print(f"   Script:\n   \"{script_text}\"")

    print(f"\n{voice_step}")
    speaker = "aditya" if character in ["dev", "arjun"] else ("Kore" if character == "kabir" else "neha")

    clean_topic = "".join(c if c.isalnum() else "_" for c in topic)[:25]
    output_filename = f"reel_{character}_{clean_topic}_{int(time.time())}.mp4"
    final_output_path = out_dir / output_filename

    vm = importlib.import_module("00_CORE_SYSTEM.engine.video_production.render_master_reel")
    print(f"\n{render_step}")

    try:
        rendered_file = vm.render_video(
            topic=topic,
            character=character,
            voice_speaker=speaker,
            script_text=script_text,
            cta=cta,
            output_name=str(final_output_path)
        )
    except Exception as e:
        err_msg = str(e)
        if "All TTS providers failed" in err_msg or "403" in err_msg or "Forbidden" in err_msg:
            print(f"\n⚠️ [Voice Vault Notice] TTS Key verification required.")
            print("👉 Please enter your free Gemini API Key from Google AI Studio:")
            new_key = input("Paste Gemini API Key > ").strip()
            if new_key:
                vault.add_key("gemini", new_key, label="Active Gemini Key")
                # Retry render with updated key
                rendered_file = vm.render_video(
                    topic=topic,
                    character=character,
                    voice_speaker=speaker,
                    script_text=script_text,
                    cta=cta,
                    output_name=str(final_output_path)
                )
            else:
                raise e
        else:
            raise e

    # Instant Android Gallery scan
    if shutil.which("termux-media-scan"):
        try:
            subprocess.run(["termux-media-scan", str(rendered_file)], check=False, stdout=subprocess.DEVNULL)
            print("   📱 Synced to Android Gallery / Downloads!")
        except Exception:
            pass

    print("\n" + "=" * 60)
    print(success_title)
    print(f"📁 Video Path: {rendered_file}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    interactive_wizard()
