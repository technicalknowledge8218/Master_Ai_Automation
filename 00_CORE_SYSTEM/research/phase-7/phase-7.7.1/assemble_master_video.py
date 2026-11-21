"""
assemble_master_video.py
========================
Assembles the final master 1080p 24fps video for "पहली धुन" (The First Melody)
using FFmpeg xfade transitions, burning in pristine high-definition visual scenes
and multiplexing the master 44.1kHz stereo audio mix ('final_mix.wav').
"""

import os
import sys
import subprocess
import json
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.1"
SCENES_DIR = os.path.join(OUTPUT_DIR, "scenes_1080p")

s1_mp4 = os.path.join(SCENES_DIR, "scene_01.mp4")
s2_mp4 = os.path.join(SCENES_DIR, "scene_02.mp4")
s3_mp4 = os.path.join(SCENES_DIR, "scene_03.mp4")
s4_mp4 = os.path.join(SCENES_DIR, "scene_04.mp4")
audio_wav = os.path.join(OUTPUT_DIR, "final_mix.wav")
output_mp4 = os.path.join(OUTPUT_DIR, "final_video.mp4")

# Transitions:
# Scene 1: 8.0s (offset 7.5s, dur 0.5s) -> Scene 2
# Scene 2: 8.0s (offset 15.0s, dur 0.5s) -> Scene 3
# Scene 3: 8.0s (offset 22.5s, dur 0.5s) -> Scene 4 (7.5s)
# Total net video duration = 8.0 + 8.0 + 8.0 + 7.5 - (3 * 0.5) = 30.00s exactly!

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
    "-crf", "18",
    "-preset", "medium",
    "-c:a", "aac",
    "-b:a", "192k",
    "-ar", "44100",
    "-t", "30.00",
    "-movflags", "+faststart",
    output_mp4
]

print("Executing Master 1080p Video Assembly...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("FFmpeg Error:", res.stderr)
    sys.exit(res.returncode)

print(f"Master Video Assembled Successfully: {output_mp4}")
