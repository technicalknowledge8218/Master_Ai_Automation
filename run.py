"""
run.py
Master AI — Universal Interactive Reel Wizard (Grill-Me Protocol)
Works seamlessly on Windows PowerShell, macOS, Linux, and Android Termux!
Zero hardcoded paths: 100% relative and dynamic.
"""

import os
import sys
import time
import json
import platform
from pathlib import Path
import urllib.request
import urllib.error

# Resolve Workspace Root dynamically from current file location
WORKSPACE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE_ROOT))

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


def generate_devanagari_script_via_gemini(topic: str, character: str, cta: str, api_key: str) -> str:
    """Uses Google Gemini REST API to autonomously draft a viral 15s Hindi script."""
    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt_text = f"""
    Write a high-retention 15-second viral Hindi video reel script on topic: "{topic}".
    Speaker character: "{character}".
    Target Call to Action (CTA): "{cta}".
    
    CRITICAL RULES:
    1. Write PURE DEVANAGARI HINDI PHONETICS even for English technical words.
       Example: Termux -> टर्मक्स, Node.js -> नोड जेएस, Claude Code -> क्लॉड कोड, AI -> एआई, Install -> इन्स्टॉल, Command -> कमांड, Ready -> रेडी.
    2. Hook must be explosive in the first 3 seconds.
    3. Length must be strictly between 25 and 35 Hindi words (fits 12-15 seconds speech).
    4. Return ONLY the spoken text in Devanagari. No character names, no brackets, no stage directions.
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
        # Clean any markdown or quotes
        candidate = candidate.replace('"', '').replace("'", "").replace("\n", " ").strip()
        return candidate
    except Exception as e:
        # Fallback robust default phonetic script if offline or API error
        return "पहले टर्मक्स में नोड जेएस इन्स्टॉल करो, फिर क्लॉड कमांड रन करो और पूरा एआई मोबाइल में रेडी!"


def interactive_wizard():
    print("\n" + "="*60)
    print(" ⚡ MASTER AI — INTERACTIVE REEL STUDIO (GRILL-ME PROTOCOL)")
    print(" Powered by JobRun Technologies | Universal Windows/Termux")
    print("="*60 + "\n")
    
    # 1. Topic / Hook
    topic_input = input("[1/4] वीडियो का टॉपिक / टेक हुक क्या है?\n(Default: Claude Code On Mobile Termux) > ").strip()
    topic = topic_input if topic_input else "Claude Code On Mobile Termux"
    
    # 2. Character Archetype
    print("\n[2/4] कैरेक्टर चुनें:")
    print("   1. Dev (Solo Tech Creator / Modern Builder)")
    print("   2. Neha (Tech Host & Explainer)")
    print("   3. Dr. Kabir (Senior Tech Mentor)")
    print("   4. Arjun (Energetic Builder)")
    char_choice = input("नंबर चुनें [1-4] (Default: 1) > ").strip()
    char_map = {"1": "dev", "2": "neha", "3": "kabir", "4": "arjun"}
    character = char_map.get(char_choice, "dev")
    
    # 3. Dynamic Output Save Path
    default_save = get_default_output_dir()
    print(f"\n[3/4] वीडियो कहाँ सेव करनी है?")
    print(f"   डिफ़ॉल्ट पाथ: {default_save}")
    user_save_path = input("नया पाथ डालें या Enter दबाएं > ").strip()
    
    if user_save_path:
        out_dir = Path(user_save_path).resolve()
    else:
        out_dir = default_save
        
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        # Graceful fallback to local workspace if storage permission isn't granted yet
        fallback_dir = WORKSPACE_ROOT / "output_videos"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n   ⚠️ Storage Permission नहीं मिली: {out_dir}")
        print(f"   📁 फॉलबैक: वीडियो ऐप फोल्डर में सेव होगी: {fallback_dir}")
        print(f"   💡 (टिप: फोन गैलरी में सेव करने के लिए Termux में 'termux-setup-storage' रन करके Allow दबाएं)")
        out_dir = fallback_dir
        
    print(f"   ✔ वीडियो सेव होगी: {out_dir}")
    
    # 4. Call to Action (CTA)
    cta_input = input("\n[4/4] कॉल-टू-एक्शन (CTA) क्या रखें?\n(Default: Comment TERMUX for Full Guide) > ").strip()
    cta = cta_input if cta_input else "Comment TERMUX for Full Guide"
    
    # Check Voice Vault
    import importlib
    vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
    vault = vv.vault
    
    # Check for Gemini API key to draft script
    gemini_keys = [k["key"] for k in vault.config.get("gemini", []) if k.get("status") == "active" and k.get("key")]
    primary_key = gemini_keys[0] if gemini_keys else os.getenv("GEMINI_API_KEY", "")
    
    print("\n" + "-"*60)
    print("🧠 [चरण 1/4] एआई से शुद्ध देवनागरी स्क्रिप्ट लिखवाई जा रही है...")
    script_text = generate_devanagari_script_via_gemini(topic, character, cta, primary_key)
    print(f"   स्क्रिप्ट:\n   \"{script_text}\"")
    
    print("\n🎙️ [चरण 2/4] वॉइस वॉल्ट से आवाज़ जनरेट हो रही है (Gemini -> ElevenLabs -> Sarvam)...")
    speaker = "aditya" if character in ["dev", "arjun"] else ("Kore" if character == "kabir" else "neha")
    
    # Filename
    clean_topic = "".join(c if c.isalnum() else "_" for c in topic)[:25]
    output_filename = f"reel_{character}_{clean_topic}_{int(time.time())}.mp4"
    final_output_path = out_dir / output_filename
    
    # Render Master Video
    vm = importlib.import_module("00_CORE_SYSTEM.engine.video_production.render_master_reel")
    print("\n🎬 [चरण 3/4] 2D कैरेक्टर रिग, लिप-सिंक व काइनेटिक सबटाइटल्स रेंडर हो रहे हैं...")
    
    rendered_file = vm.render_video(
        topic=topic,
        character=character,
        voice_speaker=speaker,
        script_text=script_text,
        cta=cta,
        output_name=str(final_output_path)
    )
    
    print("\n" + "="*60)
    print(f"🎉 बधाई! 1080x1920 वायरल रील सफलता से तैयार हो गई है!")
    print(f"📁 सेव लोकेशन: {rendered_file}")
    print("="*60 + "\n")


if __name__ == "__main__":
    interactive_wizard()
