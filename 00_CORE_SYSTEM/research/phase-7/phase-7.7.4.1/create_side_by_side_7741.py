"""
create_side_by_side_7741.py
===========================
Generates a 10.00-second Full HD (1920x1080) side-by-side comparison video:
- Left (960x1080): Failed Phase 7.7.4 output (Scanline stride mismatch, violent jitter)
- Right (960x1080): Repaired Phase 7.7.4.1 output (Stride verified, zero-defect rasterization)
"""

import os
import subprocess
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4.1"
FAILED_MP4 = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\final_video.mp4"
REPAIRED_MP4 = os.path.join(BASE_DIR, "calibration_video.mp4")
OUTPUT_MP4 = os.path.join(BASE_DIR, "side_by_side_comparison.mp4")

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

# Filtergraph:
# Take first 10s of input 0 (failed), crop/scale to 960x1080
# Take first 10s of input 1 (repaired), crop/scale to 960x1080
# Stack horizontally (hstack), add top banner overlay
filter_graph = (
    "[0:v]trim=duration=10,setpts=PTS-STARTPTS,scale=960:1080:force_original_aspect_ratio=decrease,pad=960:1080:(ow-iw)/2:(oh-ih)/2,drawtext=text='FAILED (Phase 7.7.4 - Scanline Jitter)':x=40:y=60:fontsize=32:fontcolor=white:box=1:boxcolor=red@0.8:boxborderw=10[vleft];"
    "[1:v]trim=duration=10,setpts=PTS-STARTPTS,scale=960:1080:force_original_aspect_ratio=decrease,pad=960:1080:(ow-iw)/2:(oh-ih)/2,drawtext=text='REPAIRED (Phase 7.7.4.1 - Zero Glitch)':x=40:y=60:fontsize=32:fontcolor=white:box=1:boxcolor=green@0.8:boxborderw=10[vright];"
    "[vleft][vright]hstack=inputs=2,format=yuv420p[vout]"
)

cmd = [
    FFMPEG_BIN, "-y",
    "-i", FAILED_MP4,
    "-i", REPAIRED_MP4,
    "-filter_complex", filter_graph,
    "-map", "[vout]",
    "-map", "1:a",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "256k",
    "-t", "10.000",
    "-movflags", "+faststart",
    OUTPUT_MP4
]

print("Executing side-by-side assembly...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("FFmpeg error:\n", res.stderr)
    # Fallback to simple hstack without drawtext if drawtext filter lacks font
    fallback_filter = (
        "[0:v]trim=duration=10,setpts=PTS-STARTPTS,scale=960:1080[vleft];"
        "[1:v]trim=duration=10,setpts=PTS-STARTPTS,scale=960:1080[vright];"
        "[vleft][vright]hstack=inputs=2,format=yuv420p[vout]"
    )
    cmd[cmd.index("-filter_complex") + 1] = fallback_filter
    subprocess.run(cmd, check=True)

print(f"Side-by-side comparison video created: {OUTPUT_MP4}")
print(f"Size: {os.path.getsize(OUTPUT_MP4):,} bytes")
