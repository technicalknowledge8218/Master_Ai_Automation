"""
assemble_master_video_772.py
============================
Assembles the master 1080p video for "चाय और चाल" (The Chai Gambit):
- 4 high-fidelity animated scenes with dynamic xfade transitions
- Multiplexes the master audio track (final_mix.wav)
- Encodes broadcast H.264 High Profile @ 24.0 FPS CFR at exactly 30.000s net duration.
"""

import os
import sys
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.2"
SCENES_DIR = os.path.join(OUTPUT_DIR, "scenes_1080p")

s1_mp4 = os.path.join(SCENES_DIR, "scene_01.mp4")
s2_mp4 = os.path.join(SCENES_DIR, "scene_02.mp4")
s3_mp4 = os.path.join(SCENES_DIR, "scene_03.mp4")
s4_mp4 = os.path.join(SCENES_DIR, "scene_04.mp4")
audio_wav = os.path.join(OUTPUT_DIR, "final_mix.wav")
output_mp4 = os.path.join(OUTPUT_DIR, "final_video.mp4")

filtergraph = (
    "[0:v][1:v]xfade=transition=smoothleft:duration=0.5:offset=7.5[v01];"
    "[v01][2:v]xfade=transition=wipeleft:duration=0.5:offset=15.0[v02];"
    "[v02][3:v]xfade=transition=dissolve:duration=0.5:offset=22.5[v03];"
    "[v03]fade=t=out:st=29.2:d=0.8[vout]"
)

cmd = [
    FFMPEG, "-y",
    "-i", s1_mp4,
    "-i", s2_mp4,
    "-i", s3_mp4,
    "-i", s4_mp4,
    "-i", audio_wav,
    "-filter_complex", filtergraph,
    "-map", "[vout]",
    "-map", "4:a",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "24",
    "-crf", "17",
    "-preset", "medium",
    "-c:a", "aac",
    "-b:a", "192k",
    "-ar", "44100",
    "-t", "30.00",
    "-movflags", "+faststart",
    output_mp4
]

print("Assembling final_video.mp4 via FFmpeg...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("FFmpeg Error:", res.stderr)
    sys.exit(res.returncode)

print(f"Master Film Assembled: {output_mp4}")
