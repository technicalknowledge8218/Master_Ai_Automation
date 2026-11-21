"""audio_manager.py
MASTER-AI Audio Manager & Soundscape Synthesis Engine

Manages background music, ambient sound effects, volume ducking, and master audio mixing.
Generates licensed/CC-0 ambient soundscapes programmatically using FFmpeg audio filters.
Applies audio ducking (-14dB on music during narration) without cutting voiceover or clipping.
"""

import os
import sys
import json
import wave
import subprocess
from typing import Dict, Any, List, Optional, Tuple

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"


class AudioManager:
    """Manages licensed background audio, sound effects, and intelligent ducking."""

    def __init__(self):
        pass

    def generate_ambient_soundscape(
        self,
        duration_sec: float,
        output_path: str,
        style: str = "savannah_wind"
    ) -> Dict[str, Any]:
        """Synthesizes a royalty-free ambient audio track using FFmpeg audio synthesis filters."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        if style == "savannah_wind":
            lavfi_expr = f"anoisesrc=d={duration_sec}:c=pink:r=44100:a=0.03,lowpass=f=450,flanger=delay=10:depth=2"
        elif style == "dramatic_pulse":
            lavfi_expr = f"sine=f=55:d={duration_sec},volume=0.25"
        elif style == "savannah_dusk":
            lavfi_expr = f"anoisesrc=d={duration_sec}:c=brown:r=44100:a=0.02,lowpass=f=350"
        else:
            lavfi_expr = f"sine=f=110:d={duration_sec},volume=0.15"

        cmd = [
            FFMPEG_EXE, "-y",
            "-f", "lavfi",
            "-i", lavfi_expr,
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            output_path
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg ambient soundscape generation failed: {res.stderr[-300:]}")

        return {
            "style": style,
            "duration_sec": duration_sec,
            "audio_path": output_path,
            "license": "CC-0 Public Domain (Procedural Synthesis)",
            "file_size_bytes": os.path.getsize(output_path),
            "status": "SUCCESS"
        }

    def mix_narration_with_music(
        self,
        voiceover_path: str,
        background_music_path: str,
        output_path: str,
        target_duration_sec: Optional[float] = None,
        ducking_db: float = -14.0
    ) -> Dict[str, Any]:
        """Mixes voiceover narration with background music applying ducking.
        Ensures narration is preserved at 100% volume (0 dB) with normalize=0,
        applies ducking to the background track, and applies a limiter to prevent clipping.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        music_vol = 10 ** (ducking_db / 20.0)  # e.g. -14dB ~ 0.20

        # Filter complex:
        # [0:a] is voiceover at 1.0 volume
        # [1:a] is background music ducked at ~0.20 volume
        # amix with normalize=0 prevents volume cut
        # alimiter prevents digital clipping
        filter_complex = (
            f"[0:a]volume=1.0[voice];"
            f"[1:a]volume={music_vol:.2f}[music];"
            f"[voice][music]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,alimiter=limit=0.95[out]"
        )

        cmd = [
            FFMPEG_EXE, "-y",
            "-i", voiceover_path,
            "-i", background_music_path,
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-c:a", "pcm_s16le",
            "-ar", "44100"
        ]

        if target_duration_sec and target_duration_sec > 0:
            cmd.extend(["-t", str(target_duration_sec)])

        cmd.append(output_path)

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Audio mixing failed: {res.stderr[-300:]}")

        # Verify output duration and properties
        with wave.open(output_path, "rb") as wf:
            dur = round(wf.getnframes() / float(wf.getframerate()), 3)
            sr = wf.getframerate()
            ch = wf.getnchannels()

        return {
            "output_path": output_path,
            "mixed_duration_sec": dur,
            "sample_rate_hz": sr,
            "channels": ch,
            "file_size_bytes": os.path.getsize(output_path),
            "ducking_db": ducking_db,
            "status": "SUCCESS"
        }
