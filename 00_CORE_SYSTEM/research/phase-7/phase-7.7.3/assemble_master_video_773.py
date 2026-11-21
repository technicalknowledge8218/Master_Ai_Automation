"""
assemble_master_video_773.py
============================
Assembles the final 60.00-second Full HD master video package:
"लास्ट बग" (The Last Bug) - Phase 7.7.3

Pipeline:
1. Inputs: 8 scenes (scenes 1-7: 8.0s gross, scene 8: 7.5s gross)
2. 7 cinematic crossfades (xfade duration: 0.5s)
   - Scene 1 & 2 crossfade at 7.5s
   - Scene 2 & 3 crossfade at 15.0s
   - Scene 3 & 4 crossfade at 22.5s
   - Scene 4 & 5 crossfade at 30.0s
   - Scene 5 & 6 crossfade at 37.5s
   - Scene 6 & 7 crossfade at 45.0s
   - Scene 7 & 8 crossfade at 52.5s
   Net video duration: 60.000s (1440 frames @ 24.0 FPS CFR)
3. Audio: Multiplex final_mix.wav (60.00s stereo, AAC 320 kbps)
4. Container: MP4 (H.264 high profile, yuv420p, movflags +faststart)
5. Output: final_video.mp4
"""

import os
import subprocess
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3"
SCENES_DIR = os.path.join(BASE_DIR, "scenes_1080p")
FINAL_MIX_WAV = os.path.join(BASE_DIR, "final_mix.wav")
FINAL_VIDEO_MP4 = os.path.join(BASE_DIR, "final_video.mp4")

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

def assemble():
    print("=================================================================")
    print("MASTER AI — PHASE 7.7.3: FINAL MASTER TIMELINE ASSEMBLY")
    print("Target: 60.000s | 1440 Frames | 1920x1080 | 24.0 FPS CFR")
    print("=================================================================")
    
    # Verify input scenes
    scene_files = [os.path.join(SCENES_DIR, f"scene_{i:02d}.mp4") for i in range(1, 9)]
    for f in scene_files:
        if not os.path.isfile(f) or os.path.getsize(f) < 1000:
            raise FileNotFoundError(f"Missing or corrupted scene file: {f}")
            
    if not os.path.isfile(FINAL_MIX_WAV):
        raise FileNotFoundError(f"Missing final mix audio: {FINAL_MIX_WAV}")

    # Build complex filter graph for 7 smooth crossfades
    # Offset calculation:
    # Scene 1: 8.0s -> offset 7.5
    # Scene 2: 8.0s -> accumulated 15.5 - 0.5 = offset 15.0
    # Scene 3: 8.0s -> accumulated 23.0 - 0.5 = offset 22.5
    # Scene 4: 8.0s -> accumulated 30.5 - 0.5 = offset 30.0
    # Scene 5: 8.0s -> accumulated 38.0 - 0.5 = offset 37.5
    # Scene 6: 8.0s -> accumulated 45.5 - 0.5 = offset 45.0
    # Scene 7: 8.0s -> accumulated 53.0 - 0.5 = offset 52.5
    # Scene 8: 7.5s -> final duration = 52.5 + 7.5 = 60.000s exactly!
    
    filter_graph = (
        "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=7.5[v01];"
        "[v01][2:v]xfade=transition=fade:duration=0.5:offset=15.0[v02];"
        "[v02][3:v]xfade=transition=fade:duration=0.5:offset=22.5[v03];"
        "[v03][4:v]xfade=transition=fade:duration=0.5:offset=30.0[v04];"
        "[v04][5:v]xfade=transition=fade:duration=0.5:offset=37.5[v05];"
        "[v05][6:v]xfade=transition=fade:duration=0.5:offset=45.0[v06];"
        "[v06][7:v]xfade=transition=fade:duration=0.5:offset=52.5,format=yuv420p[vout]"
    )
    
    cmd = [
        FFMPEG_BIN, "-y"
    ]
    
    # 8 Video inputs
    for sf in scene_files:
        cmd.extend(["-i", sf])
        
    # Audio input (index 8)
    cmd.extend(["-i", FINAL_MIX_WAV])
    
    # Filter graph and mapping
    cmd.extend([
        "-filter_complex", filter_graph,
        "-map", "[vout]",
        "-map", "8:a",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-r", "24",
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "44100",
        "-t", "60.000",
        "-movflags", "+faststart",
        FINAL_VIDEO_MP4
    ])
    
    print("\nExecuting FFmpeg assembly...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:\n", res.stderr)
        raise RuntimeError("FFmpeg assembly failed")
        
    print(f"\nFINAL MASTER VIDEO ASSEMBLED: {FINAL_VIDEO_MP4}")
    print(f"File size: {os.path.getsize(FINAL_VIDEO_MP4):,} bytes")

if __name__ == "__main__":
    assemble()
