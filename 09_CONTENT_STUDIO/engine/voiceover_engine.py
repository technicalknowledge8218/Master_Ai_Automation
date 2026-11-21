"""voiceover_engine.py
MASTER-AI Professional Voiceover & Narration Synthesis Engine
Powers voiceover synthesis exclusively using Google Gemini Voice Engine (gemini-3.8-flash-tts).
All Microsoft Edge-TTS components have been permanently deleted per user mandate.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
import wave
import subprocess
from typing import Dict, Any, List, Optional, Tuple

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

class VoiceoverEngine:
    """Enterprise Google Gemini voice synthesis engine."""

    VOICES = {
        "Hindi": {
            "Male": "Puck",
            "Female": "Kore",
            "Deep": "Charon",
            "Dramatic": "Fenrir",
            "default": "Puck"
        },
        "English": {
            "Male": "Puck",
            "Female": "Kore",
            "Deep": "Charon",
            "default": "Puck"
        }
    }

    def __init__(self, api_key: str = None):
        self.provider_id = "google_gemini_tts"
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = "gemini-3.8-flash-tts"

    def list_available_voices(self, language: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
            {"id": "Puck", "name": "Puck (Energetic Male)", "language": "Hindi / English", "gender": "Male", "engine": "Google Gemini"},
            {"id": "Charon", "name": "Charon (Documentary Deep Male)", "language": "Hindi / English", "gender": "Male", "engine": "Google Gemini"},
            {"id": "Fenrir", "name": "Fenrir (Dramatic Male)", "language": "Hindi / English", "gender": "Male", "engine": "Google Gemini"},
            {"id": "Kore", "name": "Kore (Professional Female)", "language": "Hindi / English", "gender": "Female", "engine": "Google Gemini"},
            {"id": "Aoede", "name": "Aoede (Storyteller Female)", "language": "Hindi / English", "gender": "Female", "engine": "Google Gemini"}
        ]

    def check_engine_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {"status": "UNAVAILABLE", "error": "Missing GEMINI_API_KEY"}
        return {"status": "AVAILABLE", "provider": "Google Gemini TTS", "model": self.model}

    def synthesize_cue(
        self,
        text: str,
        output_wav: str,
        language: str = "Hindi",
        voice_name: Optional[str] = None,
        rate: str = "+0%",
        volume: str = "+0%"
    ) -> Dict[str, Any]:
        """Synthesizes speech using Google Gemini TTS API."""
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is required for voice synthesis.")

        selected_voice = voice_name or "Puck"
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

        temp_pcm = output_wav + ".raw.wav"
        os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)

        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            parts = res.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            pcm_bytes = None
            for p in parts:
                if "inlineData" in p:
                    pcm_bytes = base64.b64decode(p["inlineData"]["data"])
                    break

            if not pcm_bytes:
                raise RuntimeError("No audio data returned by Google Gemini TTS.")

            with wave.open(temp_pcm, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(pcm_bytes)

        # Convert to broadcast WAV (44.1kHz, 16-bit mono, loudnorm)
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", temp_pcm,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ac", "1",
            "-ar", "44100",
            "-c:a", "pcm_s16le",
            output_wav
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        if os.path.exists(temp_pcm):
            os.remove(temp_pcm)

        return {
            "output_path": output_wav,
            "provider": "google_gemini_tts",
            "voice": selected_voice,
            "text": text
        }
