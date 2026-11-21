"""Master AI Portable FFmpeg Runner.

Locates and executes the static FFmpeg binary on Windows without requiring
global administrative installations or system-level environment modifications.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Sequence


def resolve_ffmpeg_path() -> Path | None:
    """Resolve the FFmpeg executable path with fallback priority:

    1. Environment variable FFMPEG_PATH.
    2. imageio_ffmpeg bundled binary.
    3. System PATH.
    """
    env_path = os.getenv("FFMPEG_PATH")
    if env_path and Path(env_path).is_file():
        return Path(env_path)

    try:
        import imageio_ffmpeg

        bundled = imageio_ffmpeg.get_ffmpeg_exe()
        if bundled and Path(bundled).is_file():
            return Path(bundled)
    except Exception:
        pass

    system_exe = shutil.which("ffmpeg")
    if system_exe and Path(system_exe).is_file():
        return Path(system_exe)

    return None


def is_ffmpeg_available() -> bool:
    """Return True if a valid FFmpeg binary can be located."""
    return resolve_ffmpeg_path() is not None


def get_ffmpeg_version() -> str:
    """Retrieve the installed FFmpeg version string."""
    ffmpeg_exe = resolve_ffmpeg_path()
    if not ffmpeg_exe:
        raise FileNotFoundError("FFmpeg executable was not found.")

    res = subprocess.run(
        [str(ffmpeg_exe), "-version"],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )
    first_line = res.stdout.splitlines()[0] if res.stdout else "unknown"
    return first_line.strip()


def run_ffmpeg(
    args: Sequence[str],
    timeout: int = 120,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Execute FFmpeg with provided arguments.

    Args:
        args: Command-line arguments to pass to FFmpeg.
        timeout: Maximum execution time in seconds.
        check: Whether to raise CalledProcessError on non-zero exit code.

    Returns:
        CompletedProcess instance containing stdout and stderr.
    """
    ffmpeg_exe = resolve_ffmpeg_path()
    if not ffmpeg_exe:
        raise FileNotFoundError("FFmpeg executable was not found.")

    full_cmd = [str(ffmpeg_exe)] + list(args)
    return subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
        check=check,
        timeout=timeout,
    )


if __name__ == "__main__":
    if is_ffmpeg_available():
        print(f"[OK] FFmpeg found at: {resolve_ffmpeg_path()}")
        print(f"[OK] Version: {get_ffmpeg_version()}")
    else:
        print("[FAIL] FFmpeg not found.")
