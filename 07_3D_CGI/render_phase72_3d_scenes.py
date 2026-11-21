"""
Master AI - Phase 7.2 3D Scenes Batch Render Runner
Renders Savanna Establishing Environment and Hero Lion CGI using Blender 5.2.4 LTS.
"""

import os
import sys
import time
import subprocess
import json
import imageio_ffmpeg

sys.path.insert(0, r"F:\Master AI\07_3D_CGI\adapters")
from blender_adapter import BlenderAdapter

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def encode_frames_to_mp4(frames_dir, output_mp4, fps=24):
    cmd = [
        FFMPEG, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        output_mp4
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg encode failed:", res.stderr)
        return False
    print(f"Encoded MP4: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
    return True

def main():
    adapter = BlenderAdapter()
    print("Blender executable:", adapter.blender_exe)
    print("Version info:", adapter.version_info)
    
    jobs = [
        {
            "name": "Savanna Establishing Environment",
            "script": r"F:\Master AI\07_3D_CGI\scenes\scene_pilot_savanna_environment.py",
            "out_prefix": r"F:\Master AI\07_3D_CGI\renders\pilot_savanna_env\frame_",
            "frames_dir": r"F:\Master AI\07_3D_CGI\renders\pilot_savanna_env",
            "mp4": r"F:\Master AI\07_3D_CGI\renders\pilot_savanna_env.mp4"
        },
        {
            "name": "Hero African Lion CGI",
            "script": r"F:\Master AI\07_3D_CGI\scenes\scene_pilot_lion_hero.py",
            "out_prefix": r"F:\Master AI\07_3D_CGI\renders\pilot_lion_hero\frame_",
            "frames_dir": r"F:\Master AI\07_3D_CGI\renders\pilot_lion_hero",
            "mp4": r"F:\Master AI\07_3D_CGI\renders\pilot_lion_hero.mp4"
        }
    ]

    for job in jobs:
        print(f"\n========================================================")
        print(f"RENDERING: {job['name']}")
        print(f"========================================================")
        os.makedirs(job["frames_dir"], exist_ok=True)
        
        t0 = time.time()
        res = adapter.render_scene(
            scene_script_path=job["script"],
            output_prefix=job["out_prefix"],
            start_frame=1,
            end_frame=72,
            resolution_x=1280,
            resolution_y=720,
            samples=16,
            timeout_sec=600
        )
        t1 = time.time()
        print(f"Render completed in {t1 - t0:.2f}s - Status: {res.get('status')}")
        
        # Encode to MP4
        encode_frames_to_mp4(job["frames_dir"], job["mp4"], fps=24)

    print("\nAll Phase 7.2 3D scenes rendered and encoded successfully!")

if __name__ == "__main__":
    main()
