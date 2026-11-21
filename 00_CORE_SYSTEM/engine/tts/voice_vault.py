"""
Master AI - Multi-Provider Voice Vault & Auto-Failover Engine
Voice Engine Hierarchy (Strict Order):
1. Google Gemini TTS (gemini-3.8-flash-tts / 2.5-flash with Multi-Key Pool)
2. ElevenLabs TTS
3. Sarvam AI (bulbul:v3 - Native Indian Hindi)

Features:
- Live Key Ping & Verification
- Key Masking & Security
- Delete / Disable Keys
- Real-time Quota & Usage Tracking
- Manual Primary Engine Switching
"""

import os
import sys
import json
import base64
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any

# Root discovery - 100% dynamic
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
VAULT_CONFIG_FILE = WORKSPACE_ROOT / "00_CORE_SYSTEM" / "engine" / "tts" / "vault_config.json"
ENV_FILE = WORKSPACE_ROOT / ".env"

DEFAULT_CONFIG = {
    "active_primary": "gemini",
    "active_secondary": "elevenlabs",
    "active_tertiary": "sarvam",
    "gemini": [
        {
            "key": "YOUR_GEMINI_API_KEY_HERE",
            "label": "Gemini Account 1 (Demo)",
            "status": "active",
            "last_used": None,
            "requests_count": 0,
            "quota_limit": 10
        }
    ],
    "elevenlabs": [],
    "sarvam": [
        {
            "key": "YOUR_SARVAM_API_KEY_HERE",
            "label": "Sarvam AI (Demo)",
            "status": "active",
            "model": "bulbul:v3",
            "last_used": None,
            "requests_count": 0,
            "credits_total": 100
        }
    ]
}


def load_config() -> dict:
    if VAULT_CONFIG_FILE.exists():
        try:
            with open(VAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG


def save_config(cfg: dict) -> None:
    VAULT_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VAULT_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def mask_key(k: str) -> str:
    k = k.strip()
    if len(k) <= 8:
        return "••••••••"
    return k[:4] + "••••••••" + k[-4:]


# -------------------------------------------------------------------------
# Provider 1: Google Gemini TTS (Primary)
# -------------------------------------------------------------------------
class GeminiTTSProvider:
    MODELS = [
        "gemini-3.8-flash-tts",
        "gemini-2.5-flash-preview-tts",
        "gemini-3.1-flash-tts-preview"
    ]

    @classmethod
    def verify(cls, api_key: str) -> Dict[str, Any]:
        """Probes Gemini API to check validity and quota."""
        clean_key = api_key.strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return {"valid": True, "message": "Key is active and responsive"}
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return {"valid": True, "warning": "Rate limit / quota reached (429)", "quota_exhausted": True}
            return {"valid": False, "error": f"HTTP {e.code}: Invalid API Key or Unauthorized"}
        except Exception as ex:
            return {"valid": False, "error": str(ex)}
        return {"valid": False, "error": "Unknown verification error"}

    @classmethod
    def synthesize(cls, text: str, api_key: str, voice_name: str = "Puck", out_path: str = None) -> str:
        clean_key = api_key.strip()
        for model in cls.MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={clean_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": text}]}],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": voice_name
                            }
                        }
                    }
                }
            }

            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                part = data["candidates"][0]["content"]["parts"][0]
                inline_data = part.get("inlineData", {})
                b64_audio = inline_data.get("data")
                mime_type = inline_data.get("mimeType", "")

                if not b64_audio:
                    continue

                raw_bytes = base64.b64decode(b64_audio)
                if not out_path:
                    out_path = str(WORKSPACE_ROOT / "00_CORE_SYSTEM" / "voice_chunks" / f"gemini_{voice_name}_{int(time.time())}.wav")

                Path(out_path).parent.mkdir(parents=True, exist_ok=True)

                if "audio/wav" in mime_type:
                    with open(out_path, "wb") as f:
                        f.write(raw_bytes)
                else:
                    import wave
                    with wave.open(out_path, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(24000)
                        wf.writeframes(raw_bytes)

                return out_path
            except urllib.error.HTTPError as he:
                if he.code == 429:
                    raise RuntimeError(f"Gemini 429 Quota Exceeded on key {clean_key[:10]}...")
                continue
            except Exception:
                continue

        raise RuntimeError("All Gemini TTS models failed for this key.")


# -------------------------------------------------------------------------
# Provider 2: ElevenLabs TTS (Secondary)
# -------------------------------------------------------------------------
class ElevenLabsProvider:
    @classmethod
    def verify(cls, api_key: str) -> Dict[str, Any]:
        clean_key = api_key.strip()
        url = "https://api.elevenlabs.io/v1/user"
        headers = {"xi-api-key": clean_key}
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                sub = data.get("subscription", {})
                tier = sub.get("tier", "free")
                limit = sub.get("character_limit", 10000)
                used = sub.get("character_count", 0)
                return {"valid": True, "tier": tier, "limit": limit, "used": used}
        except urllib.error.HTTPError as e:
            return {"valid": False, "error": f"HTTP {e.code}: Invalid ElevenLabs Key"}
        except Exception as ex:
            return {"valid": False, "error": str(ex)}

    @classmethod
    def synthesize(cls, text: str, api_key: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", out_path: str = None) -> str:
        if not api_key:
            raise RuntimeError("ElevenLabs API Key not configured")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key.strip()
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw_bytes = resp.read()

        if not out_path:
            out_path = str(WORKSPACE_ROOT / "00_CORE_SYSTEM" / "voice_chunks" / f"elevenlabs_{int(time.time())}.mp3")

        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(raw_bytes)

        return out_path


# -------------------------------------------------------------------------
# Provider 3: Sarvam AI (Tertiary / Fallback)
# -------------------------------------------------------------------------
class SarvamAIProvider:
    URL = "https://api.sarvam.ai/text-to-speech"
    VALID_SPEAKERS = [
        "anushka", "abhilash", "manisha", "vidya", "arya", "karun",
        "hitesh", "aditya", "ritu", "priya", "neha", "rahul", "pooja", "rohan"
    ]

    @classmethod
    def verify(cls, api_key: str) -> Dict[str, Any]:
        clean_key = api_key.strip()
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": clean_key
        }
        payload = {
            "inputs": ["नमस्ते"],
            "target_language_code": "hi-IN",
            "speaker": "aditya",
            "model": "bulbul:v3"
        }
        try:
            req = urllib.request.Request(cls.URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    return {"valid": True, "message": "Sarvam AI Key active (~₹100 tier)"}
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return {"valid": True, "warning": "Rate limit / quota exceeded", "quota_exhausted": True}
            return {"valid": False, "error": f"HTTP {e.code}: Invalid Sarvam Key"}
        except Exception as ex:
            return {"valid": False, "error": str(ex)}
        return {"valid": False, "error": "Unknown error"}

    @classmethod
    def synthesize(cls, text: str, api_key: str, speaker: str = "neha", model: str = "bulbul:v3", out_path: str = None) -> str:
        if speaker.lower() not in cls.VALID_SPEAKERS:
            speaker = "neha"

        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": api_key.strip()
        }
        payload = {
            "inputs": [text],
            "target_language_code": "hi-IN",
            "speaker": speaker.lower(),
            "pitch": 0,
            "pace": 1.05,
            "loudness": 1.5,
            "speech_sample_rate": 24000,
            "enable_preprocessing": True,
            "model": model
        }

        req = urllib.request.Request(
            cls.URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        audios = data.get("audios", [])
        if not audios:
            raise RuntimeError("Sarvam AI returned empty audio response")

        raw_bytes = base64.b64decode(audios[0])
        if not out_path:
            out_path = str(WORKSPACE_ROOT / "00_CORE_SYSTEM" / "voice_chunks" / f"sarvam_{speaker}_{int(time.time())}.wav")

        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(raw_bytes)

        return out_path


# -------------------------------------------------------------------------
# Master Voice Vault Manager
# -------------------------------------------------------------------------
class VoiceVault:
    def __init__(self):
        self.config = load_config()

    def get_status(self) -> dict:
        gemini_keys = self.config.get("gemini", [])
        eleven_keys = self.config.get("elevenlabs", [])
        sarvam_keys = self.config.get("sarvam", [])
        primary = self.config.get("active_primary", "gemini")

        def _format_keys(klist):
            out = []
            for idx, k in enumerate(klist):
                raw = k.get("key", "")
                out.append({
                    "id": idx,
                    "label": k.get("label", f"Account {idx+1}"),
                    "masked": mask_key(raw),
                    "status": k.get("status", "active"),
                    "requests": k.get("requests_count", 0),
                    "quota_limit": k.get("quota_limit", 10),
                    "last_used": k.get("last_used") or "Never"
                })
            return out

        return {
            "active_primary": primary,
            "hierarchy": [
                f"1. {primary.capitalize()} (Active Primary)",
                "2. ElevenLabs (Secondary)" if primary != "elevenlabs" else "2. Gemini (Secondary)",
                "3. Sarvam AI (Tertiary)" if primary != "sarvam" else "3. Gemini (Fallback)"
            ],
            "gemini": {
                "total_keys": len(gemini_keys),
                "active_keys": sum(1 for k in gemini_keys if k.get("status") == "active"),
                "keys": _format_keys(gemini_keys)
            },
            "elevenlabs": {
                "total_keys": len(eleven_keys),
                "active_keys": sum(1 for k in eleven_keys if k.get("status") == "active"),
                "keys": _format_keys(eleven_keys)
            },
            "sarvam": {
                "total_keys": len(sarvam_keys),
                "active_keys": sum(1 for k in sarvam_keys if k.get("status") == "active"),
                "keys": _format_keys(sarvam_keys)
            }
        }

    def verify_key(self, provider: str, key: str) -> dict:
        provider = provider.lower()
        if provider == "gemini":
            return GeminiTTSProvider.verify(key)
        elif provider == "sarvam":
            return SarvamAIProvider.verify(key)
        elif provider == "elevenlabs":
            return ElevenLabsProvider.verify(key)
        return {"valid": False, "error": f"Unknown provider: {provider}"}

    def add_key(self, provider: str, key: str, label: str = "") -> dict:
        provider = provider.lower()
        if provider not in ["gemini", "elevenlabs", "sarvam"]:
            return {"success": False, "error": f"Invalid provider {provider}"}

        clean_key = key.strip()
        if not clean_key:
            return {"success": False, "error": "Empty key provided"}

        # Live Verify
        v_res = self.verify_key(provider, clean_key)
        if not v_res.get("valid"):
            return {"success": False, "error": v_res.get("error", "Key verification failed")}

        keys_list = self.config.setdefault(provider, [])
        for entry in keys_list:
            if entry.get("key") == clean_key:
                entry["status"] = "active"
                if label:
                    entry["label"] = label
                save_config(self.config)
                return {"success": True, "message": "Key re-activated"}

        keys_list.append({
            "key": clean_key,
            "label": label or f"{provider.capitalize()} Account {len(keys_list)+1}",
            "status": "active",
            "last_used": None,
            "requests_count": 0,
            "quota_limit": 10 if provider == "gemini" else 1000
        })
        save_config(self.config)
        return {"success": True, "message": "Key verified and registered"}

    def delete_key(self, provider: str, key_id: int) -> bool:
        provider = provider.lower()
        if provider not in self.config:
            return False
        keys_list = self.config[provider]
        if 0 <= key_id < len(keys_list):
            keys_list.pop(key_id)
            save_config(self.config)
            return True
        return False

    def toggle_key(self, provider: str, key_id: int) -> bool:
        provider = provider.lower()
        if provider not in self.config:
            return False
        keys_list = self.config[provider]
        if 0 <= key_id < len(keys_list):
            curr = keys_list[key_id].get("status", "active")
            keys_list[key_id]["status"] = "disabled" if curr == "active" else "active"
            save_config(self.config)
            return True
        return False

    def set_primary(self, provider: str) -> bool:
        provider = provider.lower()
        if provider in ["gemini", "elevenlabs", "sarvam"]:
            self.config["active_primary"] = provider
            save_config(self.config)
            return True
        return False

    def synthesize_with_failover(self, text: str, speaker_or_voice: str = "Puck", out_path: str = None) -> Dict[str, Any]:
        """
        Synthesize audio following dynamic hierarchy starting with active_primary.
        """
        errors = []
        primary = self.config.get("active_primary", "gemini")
        providers_order = [primary] + [p for p in ["gemini", "elevenlabs", "sarvam"] if p != primary]

        for p in providers_order:
            if p == "gemini":
                gemini_keys = [k for k in self.config.get("gemini", []) if k.get("status") == "active"]
                gemini_voice = "Kore" if speaker_or_voice in ["neha", "female", "priya", "Kore"] else "Puck"
                for key_obj in gemini_keys:
                    try:
                        out = GeminiTTSProvider.synthesize(text=text, api_key=key_obj["key"], voice_name=gemini_voice, out_path=out_path)
                        key_obj["requests_count"] = key_obj.get("requests_count", 0) + 1
                        key_obj["last_used"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        save_config(self.config)
                        return {"status": "success", "provider": "gemini", "voice": gemini_voice, "path": out}
                    except Exception as e:
                        err_msg = str(e)
                        errors.append(f"Gemini ({key_obj.get('label')}): {err_msg}")
                        if "429" in err_msg or "quota" in err_msg.lower():
                            key_obj["status"] = "quota_exhausted"
                        save_config(self.config)

            elif p == "elevenlabs":
                eleven_keys = [k for k in self.config.get("elevenlabs", []) if k.get("status") == "active" and k.get("key")]
                for key_obj in eleven_keys:
                    try:
                        out = ElevenLabsProvider.synthesize(text=text, api_key=key_obj["key"], out_path=out_path)
                        key_obj["requests_count"] = key_obj.get("requests_count", 0) + 1
                        key_obj["last_used"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        save_config(self.config)
                        return {"status": "success", "provider": "elevenlabs", "path": out}
                    except Exception as e:
                        errors.append(f"ElevenLabs ({key_obj.get('label')}): {e}")

            elif p == "sarvam":
                sarvam_keys = [k for k in self.config.get("sarvam", []) if k.get("status") == "active"]
                sarvam_speaker = speaker_or_voice if speaker_or_voice in SarvamAIProvider.VALID_SPEAKERS else ("neha" if speaker_or_voice in ["Kore", "female"] else "aditya")
                for key_obj in sarvam_keys:
                    try:
                        out = SarvamAIProvider.synthesize(text=text, api_key=key_obj["key"], speaker=sarvam_speaker, out_path=out_path)
                        key_obj["requests_count"] = key_obj.get("requests_count", 0) + 1
                        key_obj["last_used"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        save_config(self.config)
                        return {"status": "success", "provider": "sarvam", "speaker": sarvam_speaker, "path": out}
                    except Exception as e:
                        err_msg = str(e)
                        errors.append(f"Sarvam AI ({key_obj.get('label')}): {err_msg}")
                        if "401" in err_msg or "unauthorized" in err_msg.lower():
                            key_obj["status"] = "invalid_key"
                        elif "429" in err_msg or "quota" in err_msg.lower():
                            key_obj["status"] = "quota_exhausted"
                        save_config(self.config)

        raise RuntimeError(f"All TTS providers failed in order ({' -> '.join(providers_order)}):\n" + "\n".join(errors))


vault = VoiceVault()

if __name__ == "__main__":
    print(json.dumps(vault.get_status(), indent=2))
