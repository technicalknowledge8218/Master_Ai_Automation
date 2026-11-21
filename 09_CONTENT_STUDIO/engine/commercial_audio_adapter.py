"""
Master AI - Phase 7.3 Commercial-Safe Audio Engine & Adapter
Manages voiceover synthesis, user-recorded narration checkpoints,
procedural sound design, commercial licensing clearance,
and automated acoustic quality assurance (silence & clipping detection).
"""

import os
import sys
import json
import math
import struct
import wave
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger("MasterAI.Audio.CommercialAdapter")
logging.basicConfig(level=logging.INFO)

class CommercialAudioSourceType:
    COMMERCIALLY_PERMITTED_OFFLINE_TTS = "COMMERCIALLY_PERMITTED_OFFLINE_TTS"
    USER_RECORDED_NARRATION = "USER_RECORDED_NARRATION"
    COMMERCIALLY_LICENSED_EXTERNAL = "COMMERCIALLY_LICENSED_EXTERNAL"
    PROCEDURAL_SFX = "PROCEDURAL_SFX"
    COMMERCIALLY_PERMITTED_MUSIC = "COMMERCIALLY_PERMITTED_MUSIC"
    UNVERIFIED_OR_RESTRICTED = "UNVERIFIED_OR_RESTRICTED"

class CommercialAudioAdapter:
    """Enterprise commercial audio adapter enforcing strict zero-cost & commercial safety."""

    # Banned / Quarantined engines for commercial video distribution
    QUARANTINED_ENGINES = {
        "microsoft_edge_tts": {
            "reason": "Microsoft Edge online service terms restrict synthesized audio to personal, non-commercial browser use.",
            "status": "QUARANTINED_FROM_COMMERCIAL_EXPORT"
        }
    }

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or r"F:\Master AI\09_CONTENT_STUDIO\renders\commercial_audio"
        os.makedirs(self.output_dir, exist_ok=True)

    def verify_audio_source_license(self, source_type: str, provider_name: str) -> Dict[str, Any]:
        """Audit commercial clearance of an audio source."""
        if provider_name.lower() in self.QUARANTINED_ENGINES:
            q_info = self.QUARANTINED_ENGINES[provider_name.lower()]
            return {
                "commercial_cleared": False,
                "source_type": CommercialAudioSourceType.UNVERIFIED_OR_RESTRICTED,
                "provider": provider_name,
                "status": q_info["status"],
                "rejection_reason": q_info["reason"]
            }

        if source_type in [
            CommercialAudioSourceType.USER_RECORDED_NARRATION,
            CommercialAudioSourceType.PROCEDURAL_SFX,
            CommercialAudioSourceType.COMMERCIALLY_PERMITTED_MUSIC,
            CommercialAudioSourceType.COMMERCIALLY_PERMITTED_OFFLINE_TTS
        ]:
            return {
                "commercial_cleared": True,
                "source_type": source_type,
                "provider": provider_name,
                "status": "APPROVED_FOR_COMMERCIAL_EXPORT",
                "license": "Commercial Safe (Zero-Budget / CC0 / User Owned / Permissive Open Source)"
            }

        return {
            "commercial_cleared": False,
            "source_type": CommercialAudioSourceType.UNVERIFIED_OR_RESTRICTED,
            "provider": provider_name,
            "status": "REQUIRES_MANUAL_LEGAL_CLEARANCE",
            "rejection_reason": "Source license and dataset provenance not verified."
        }

    def create_user_narration_checkpoint(
        self,
        script_sentences: List[Dict[str, Any]],
        target_duration_sec: float,
        language: str = "Hindi",
        checkpoint_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates a structured user narration recording handbook & pending checkpoint
        when no permanent commercially cleared offline TTS voice is active.
        """
        cdir = checkpoint_dir or self.output_dir
        os.makedirs(cdir, exist_ok=True)

        guide_path = os.path.join(cdir, "narration_recording_script.txt")
        manifest_path = os.path.join(cdir, "audio_checkpoint.json")

        lines = [
            "=" * 70,
            f"MASTER AI — NARRATION RECORDING HANDBOOK ({language.upper()})",
            "=" * 70,
            f"Target Runtime: {target_duration_sec:.1f} Seconds",
            "Commercial Clearance: 100% User Owned (Zero External Copyright)",
            "Recording Format: WAV or MP3 (44.1 kHz, Mono or Stereo)",
            f"Drop File To: {os.path.join(cdir, 'user_narration.wav')}",
            "-" * 70,
            "SCRIPT & TIMING GUIDELINES:\n"
        ]

        for idx, s in enumerate(script_sentences):
            t_start = s.get("start_sec", idx * 6.0)
            t_dur = s.get("duration_sec", 6.0)
            dev = s.get("text_hindi", s.get("text", ""))
            rom = s.get("transliteration", "")
            eng = s.get("translation_en", "")

            lines.append(f"SCENE {idx+1:02d} [{t_start:.1f}s - {t_start+t_dur:.1f}s] (Duration: {t_dur:.1f}s)")
            lines.append(f"  Devanagari:    {dev}")
            if rom:
                lines.append(f"  Pronunciation: {rom}")
            if eng:
                lines.append(f"  Meaning (EN):  {eng}")
            lines.append("")

        lines.append("=" * 70)
        lines.append("INSTRUCTIONS:")
        lines.append("1. Record each line clearly with a calm documentary tone.")
        lines.append(f"2. Save the final continuous audio file to: {os.path.join(cdir, 'user_narration.wav')}")
        lines.append("3. The orchestrator will automatically pick up and mix the recording upon resumption.")
        lines.append("=" * 70)

        with open(guide_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        checkpoint = {
            "checkpoint_id": f"CHK_AUDIO_{int(target_duration_sec)}S",
            "language": language,
            "status": "PENDING_USER_AUDIO",
            "target_duration_sec": target_duration_sec,
            "sentence_count": len(script_sentences),
            "expected_audio_path": os.path.join(cdir, "user_narration.wav"),
            "handbook_path": guide_path
        }

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=2)

        logger.info(f"Created User Narration Checkpoint at: {manifest_path}")
        return checkpoint

    def generate_procedural_documentary_soundscape(
        self,
        output_wav: str,
        duration_sec: float = 60.0,
        sample_rate: int = 44100
    ) -> str:
        """
        Synthesizes a continuous, broadcast-calibrated savanna ambient soundscape
        using pure Python math (zero external dependencies, zero copyright, 100% free).
        Simulates warm wind drafts, distant low-frequency rumble, and rhythmic sub-bass pads.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)
        total_samples = int(duration_sec * sample_rate)

        # Procedural sound parameters
        # Warm sub drone at 55 Hz (A1) + harmonic overtone at 110 Hz
        # Modulated pink-like noise simulating savanna breeze
        samples = []
        seed = 42

        for i in range(total_samples):
            t = i / float(sample_rate)

            # 1. Warm low drone (55 Hz & 82.5 Hz fifth)
            drone = 0.12 * math.sin(2.0 * math.pi * 55.0 * t) + 0.06 * math.sin(2.0 * math.pi * 82.5 * t)

            # 2. Gentle savanna breeze envelope (0.15 Hz slow undulation)
            wind_mod = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.12 * t)
            # Pseudo-random noise smoothed
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            raw_noise = ((seed / float(0x7FFFFFFF)) * 2.0 - 1.0)
            wind = 0.04 * raw_noise * wind_mod

            # 3. Pacing swell (subtle volume rise towards mid-point, fade out at end)
            fade_in = min(1.0, t / 3.0)
            fade_out = min(1.0, (duration_sec - t) / 3.0)
            envelope = fade_in * fade_out

            val = (drone + wind) * envelope
            # Clamp to prevent clipping
            val = max(-0.95, min(0.95, val))
            samples.append(int(val * 32767.0))

        with wave.open(output_wav, "wb") as wf:
            wf.setnchannels(1) # Mono
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(sample_rate)
            data = struct.pack(f"<{len(samples)}h", *samples)
            wf.writeframes(data)

        logger.info(f"Synthesized procedural ambient soundscape: {output_wav} ({os.path.getsize(output_wav)} bytes)")
        return output_wav

    def generate_procedural_melancholic_soundscape(
        self,
        output_wav: str,
        duration_sec: float = 59.0,
        sample_rate: int = 44100
    ) -> str:
        """
        Synthesizes a continuous, broadcast-calibrated melancholic ambient soundscape
        for emotional family drama and mystery in minor key (A minor / D minor),
        with slow evolving strings, gentle piano chords, subtle rain/wind drone,
        and emotional resolution at the twist.
        100% pure Python math, zero external dependencies, 100% free / royalty-free.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)
        total_samples = int(duration_sec * sample_rate)
        samples = []
        seed = 123456

        for i in range(total_samples):
            t = i / float(sample_rate)

            # Chord progression blending
            if t < 18.0:
                f1, f2, f3 = 110.0, 130.81, 164.81 # Am
            elif t < 36.0:
                f1, f2, f3 = 73.42, 87.31, 146.83 # Dm
            elif t < 50.0:
                blend = (t - 36.0) / 14.0
                f1 = 87.31 * (1 - blend) + 82.41 * blend
                f2 = 110.0 * (1 - blend) + 98.00 * blend
                f3 = 130.81 * (1 - blend) + 123.47 * blend
            else:
                f1, f2, f3 = 110.0, 130.81, 220.0 # Am resolution

            vib = 1.0 + 0.003 * math.sin(2.0 * math.pi * 3.5 * t)
            s1 = 0.08 * math.sin(2.0 * math.pi * (f1 * vib) * t)
            s2 = 0.06 * math.sin(2.0 * math.pi * (f2 * vib) * t)
            s3 = 0.05 * math.sin(2.0 * math.pi * (f3 * vib) * t)
            sub = 0.05 * math.sin(2.0 * math.pi * (f1 * 0.5) * t)

            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            raw_noise = ((seed / float(0x7FFFFFFF)) * 2.0 - 1.0)
            wind_mod = 0.4 + 0.3 * math.sin(2.0 * math.pi * 0.08 * t)
            wind = 0.035 * raw_noise * wind_mod

            tone_cycle = t % 6.0
            tone_decay = math.exp(-tone_cycle * 1.2)
            tone_freq = f3 * 2.0
            tone = 0.05 * math.sin(2.0 * math.pi * tone_freq * t) * tone_decay

            fade_in = min(1.0, t / 2.5)
            fade_out = min(1.0, (duration_sec - t) / 3.0)
            master_env = fade_in * fade_out

            if 35.0 <= t <= 50.0:
                swell = 1.0 + 0.35 * math.sin(math.pi * (t - 35.0) / 15.0)
            else:
                swell = 1.0

            val = (s1 + s2 + s3 + sub + wind + tone) * master_env * swell
            val = max(-0.92, min(0.92, val))
            samples.append(int(val * 32767.0))

        with wave.open(output_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            data = struct.pack(f"<{len(samples)}h", *samples)
            wf.writeframes(data)

        logger.info(f"Synthesized procedural melancholic soundscape: {output_wav} ({os.path.getsize(output_wav)} bytes)")
        return output_wav

    def inspect_audio_for_defects(
        self,
        wav_path: str,
        expected_duration_sec: Optional[float] = None,
        max_silence_gap_sec: float = 2.0
    ) -> Dict[str, Any]:
        """
        Deep acoustic inspection:
        - Detects silence intervals > max_silence_gap_sec (flags Phase 7.2 25s dead silence bug!)
        - Detects peak clipping (samples >= 0.99)
        - Computes overall RMS loudness
        - Verifies duration against timeline expectation
        """
        if not os.path.isfile(wav_path):
            raise FileNotFoundError(f"Audio file not found: {wav_path}")

        with wave.open(wav_path, "rb") as wf:
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            rate = wf.getframerate()
            frames = wf.getnframes()
            raw = wf.readframes(frames)

        duration = frames / float(rate)
        fmt = f"<{frames * channels}h" if width == 2 else None
        if not fmt:
            return {"valid": False, "error": f"Unsupported sample width: {width}"}

        samples = struct.unpack(fmt, raw)
        # Convert to float -1.0 .. 1.0
        float_samples = [s / 32768.0 for s in samples]

        # Scan for clipping
        clipped_count = sum(1 for s in float_samples if abs(s) >= 0.99)

        # Scan for silence intervals in 0.5s windows
        window_size = int(rate * channels * 0.5)
        silence_runs = 0
        max_consecutive_silence = 0
        current_consecutive_silence = 0
        sum_sq = 0.0

        for i in range(0, len(float_samples), window_size):
            chunk = float_samples[i:i + window_size]
            if not chunk:
                break
            rms = math.sqrt(sum(x * x for x in chunk) / len(chunk))
            sum_sq += sum(x * x for x in chunk)

            if rms < 0.002: # Silence threshold
                current_consecutive_silence += 0.5
                max_consecutive_silence = max(max_consecutive_silence, current_consecutive_silence)
            else:
                current_consecutive_silence = 0

        total_rms = math.sqrt(sum_sq / max(1, len(float_samples)))

        # Validation rules
        has_dead_silence = max_consecutive_silence > max_silence_gap_sec
        has_clipping = clipped_count > 50
        duration_mismatch = False
        if expected_duration_sec is not None:
            duration_mismatch = abs(duration - expected_duration_sec) > 0.75

        is_valid = not (has_dead_silence or has_clipping or duration_mismatch)

        return {
            "valid": is_valid,
            "path": wav_path,
            "duration_sec": round(duration, 3),
            "expected_duration_sec": expected_duration_sec,
            "duration_mismatch": duration_mismatch,
            "total_rms": round(total_rms, 5),
            "clipped_samples": clipped_count,
            "has_clipping": has_clipping,
            "max_consecutive_silence_sec": round(max_consecutive_silence, 2),
            "has_dead_silence_defect": has_dead_silence,
            "channels": channels,
            "sample_rate": rate
        }

if __name__ == "__main__":
    adapter = CommercialAudioAdapter()
    test_wav = r"F:\Master AI\09_CONTENT_STUDIO\renders\commercial_audio\test_ambient.wav"
    adapter.generate_procedural_documentary_soundscape(test_wav, duration_sec=5.0)
    report = adapter.inspect_audio_for_defects(test_wav, expected_duration_sec=5.0)
    print("Acoustic Inspection Report:")
    print(json.dumps(report, indent=2))
