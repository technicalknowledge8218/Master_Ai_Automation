"""
Master AI - Dedicated Google Gemini TTS Architecture
Exclusively powers production audio using Google Gemini Voice Engine (gemini-3.8-flash-tts).
All legacy/Microsoft TTS engines have been completely purged per user mandate.
"""

import os
import sys
import abc
import json
import base64
import wave
import urllib.request
import urllib.error
import numpy as np
import soundfile as sf

# -------------------------------------------------------------
# 1. Base TTS Provider Interface
# -------------------------------------------------------------
class TTSProvider(abc.ABC):
    @abc.abstractmethod
    def generate(self, text: str, language: str = "hi", voice: str = "default", **kwargs) -> str:
        """
        Generate audio from text.
        Returns the absolute file path to the generated WAV audio.
        """
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        """Check if provider credentials / dependencies are active."""
        pass


# -------------------------------------------------------------
# 2. Google Gemini TTS Provider (Strict Sole Engine)
# -------------------------------------------------------------
class GeminiTTSProvider(TTSProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.models_pool = [
            "gemini-2.5-flash-preview-tts",
            "gemini-3.1-flash-tts-preview",
            "gemini-3.8-flash-lite-tts",
            "gemini-3.8-flash-tts"
        ]
        # Prebuilt Google Gemini voices
        self.voice_map = {
            "energetic_male": "Puck",
            "documentary_male": "Charon",
            "dramatic_male": "Fenrir",
            "corporate_female": "Kore",
            "storyteller_female": "Aoede",
            "male": "Puck",
            "female": "Kore"
        }

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, text: str, language: str = "hi", voice: str = "Puck", out_path: str = None, **kwargs) -> str:
        if not self.is_available():
            raise RuntimeError("Gemini API Key is not configured. Google TTS requires an active key.")

        selected_voice = self.voice_map.get(voice, voice)
        last_error = None

        for model in self.models_pool:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

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
                    parts = res.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    for p in parts:
                        if "inlineData" in p:
                            raw_pcm = base64.b64decode(p["inlineData"]["data"])
                            if not out_path:
                                out_path = os.path.join(os.environ.get("TEMP", "."), "gemini_out.wav")
                            with wave.open(out_path, "wb") as wf:
                                wf.setnchannels(1)
                                wf.setsampwidth(2)
                                wf.setframerate(24000)
                                wf.writeframes(raw_pcm)
                            return out_path
            except urllib.error.HTTPError as e:
                err_body = e.read().decode(errors="ignore") if hasattr(e, "read") else ""
                last_error = f"{model} (HTTP {e.code}): {err_body}"
                continue
            except Exception as e:
                last_error = f"{model}: {str(e)}"
                continue

        raise RuntimeError(f"All Google Gemini TTS models failed: {last_error}")


# -------------------------------------------------------------
# 3. Audio Quality Control Pipeline (Trimming, Loudness, Limiter)
# -------------------------------------------------------------
class AudioQualityControl:
    @staticmethod
    def process(wav_path: str, target_lufs: float = -14.0, max_pause_ms: int = 120, out_path: str = None) -> str:
        """
        Applies:
        1. Silence trimming (> max_pause_ms cut to natural cadence).
        2. Peak limiting and normalization to -1.0 dBFS standard.
        """
        data, sr = sf.read(wav_path)
        if data.ndim > 1:
            data = data.mean(axis=1)
        data = data.astype(np.float32)

        # Trim leading and trailing dead air
        threshold = 0.015 * np.max(np.abs(data)) if np.max(np.abs(data)) > 0 else 0.015
        non_silent = np.where(np.abs(data) > threshold)[0]
        if len(non_silent) > 0:
            start_idx = max(0, non_silent[0] - int(0.02 * sr))
            end_idx = min(len(data), non_silent[-1] + int(0.04 * sr))
            data = data[start_idx:end_idx]

        # Compress internal gaps larger than max_pause_ms
        max_pause_samples = int((max_pause_ms / 1000.0) * sr)
        is_silent = np.abs(data) < threshold

        compressed = []
        silent_count = 0
        for sample, silent in zip(data, is_silent):
            if silent:
                silent_count += 1
                if silent_count <= max_pause_samples:
                    compressed.append(sample)
            else:
                silent_count = 0
                compressed.append(sample)

        processed = np.array(compressed, dtype=np.float32)

        # Peak normalization to -1.0 dBFS
        peak = np.max(np.abs(processed))
        if peak > 0:
            processed = (processed / peak) * 0.89

        save_path = out_path or wav_path
        sf.write(save_path, processed, sr)
        return save_path


# -------------------------------------------------------------
# 4. Master AI Central TTS Router (Strict Google Gemini Sole Engine)
# -------------------------------------------------------------
class TTSRouter:
    def __init__(self, gemini_key: str = None):
        self.gemini = GeminiTTSProvider(gemini_key)
        self.qc = AudioQualityControl()

    def route_and_generate(self, text: str, mode: str = "expressive", language: str = "hi", voice: str = "Puck", out_path: str = None) -> tuple:
        """
        Generates audio strictly using Google Gemini TTS with zero fallback.
        Available voices: Puck, Charon, Fenrir, Kore, Aoede.
        """
        target_path = out_path or os.path.join(os.environ.get("TEMP", "."), "master_ai_speech.wav")

        if not self.gemini.is_available():
            raise RuntimeError("Google Gemini TTS is unconfigured or missing API key.")

        selected_v = voice or ("Kore" if mode in ["female", "neha"] else "Puck")
        self.gemini.generate(text, language=language, voice=selected_v, out_path=target_path)
        provider_used = f"Google Gemini TTS ({selected_v})"

        # Apply QC Pipeline
        final_path = self.qc.process(target_path, target_lufs=-14.0, max_pause_ms=120)
        return final_path, provider_used
