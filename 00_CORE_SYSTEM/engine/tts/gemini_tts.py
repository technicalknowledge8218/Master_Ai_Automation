import os
import json
import base64
import wave
import urllib.request
import urllib.error

class GeminiTTS:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            # check .env
            from pathlib import Path
            env_path = Path(__file__).resolve().parents[3] / ".env"
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip()
                            break
        self.model = model or os.environ.get("GEMINI_TTS_MODEL", "gemini-3.8-flash-tts")
        
        # Google Prebuilt Voices:
        # Male: Puck, Charon, Fenrir, Orus
        # Female: Aoede, Kore, Leda
        self.voice_map = {
            "dev": "Puck",           # Energetic tech creator male
            "narrator": "Charon",     # Deep documentary male
            "dramatic": "Fenrir",     # Intense cinematic male
            "neha": "Aoede",          # Melodic friendly female
            "professional": "Kore",   # Corporate articulate female
            "puck": "Puck",
            "charon": "Charon",
            "kore": "Kore",
            "aoede": "Aoede",
            "fenrir": "Fenrir"
        }

    def generate(self, text: str, voice: str = "Puck", out_path: str = None) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        selected_voice = self.voice_map.get(voice.lower(), voice)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        payload = {
            "contents": [{"parts": [{"text": text}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": selected_voice
                        }
                    }
                }
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode())
                candidates = res.get("candidates", [])
                if not candidates:
                    raise RuntimeError(f"No candidates in Gemini response: {res}")
                parts = candidates[0].get("content", {}).get("parts", [])
                for p in parts:
                    if "inlineData" in p:
                        raw_pcm = base64.b64decode(p["inlineData"]["data"])
                        if not out_path:
                            out_path = "gemini_out.wav"
                        with wave.open(out_path, "wb") as wf:
                            wf.setnchannels(1)
                            wf.setsampwidth(2)
                            wf.setframerate(24000)
                            wf.writeframes(raw_pcm)
                        return out_path
                raise RuntimeError(f"No audio inlineData found in parts: {parts}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Gemini API HTTP Error {e.code}: {err_body}")
