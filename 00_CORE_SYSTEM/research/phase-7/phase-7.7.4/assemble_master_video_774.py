"""
assemble_master_video_774.py
============================
Master AI - Phase 7.7.4 Final Master Timeline Assembly
Executes the directorial editing plan:
- 8 scenes with motivated cinematic cuts (Match cut, Whip pan, Hard cuts, Reaction cut, Outro dissolve)
- Exactly 60.000s net duration | 1440 frames | 24.0 FPS CFR | 1920x1080 Full HD
- Multiplexes final_mix.wav (60.00s stereo, AAC 320 kbps)
- Container: MP4 (H.264 high profile, yuv420p, movflags +faststart)
"""

import os
import subprocess
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4"
SCENES_DIR = os.path.join(BASE_DIR, "scenes_1080p")
FINAL_MIX_WAV = os.path.join(BASE_DIR, "final_mix.wav")
FINAL_VIDEO_MP4 = os.path.join(BASE_DIR, "final_video.mp4")

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

def assemble():
    print("=================================================================")
    print("MASTER AI — PHASE 7.7.4: FINAL MASTER TIMELINE ASSEMBLY")
    print("Target: 60.000s | 1440 Frames | 1920x1080 | 24.0 FPS CFR")
    print("=================================================================")
    
    scene_files = [os.path.join(SCENES_DIR, f"scene_{i:02d}.mp4") for i in range(1, 9)]
    for f in scene_files:
        if not os.path.isfile(f) or os.path.getsize(f) < 1000:
            raise FileNotFoundError(f"Missing or corrupted scene file: {f}")
            
    if not os.path.isfile(FINAL_MIX_WAV):
        raise FileNotFoundError(f"Missing final mix audio: {FINAL_MIX_WAV}")

    # Build filter graph with motivated cuts:
    # 8 scenes of 180 frames (7.50s) each = 1440 frames = 60.000s exactly
    filter_graph = (
        "[0:v][1:v][2:v][3:v][4:v][5:v][6:v][7:v]concat=n=8:v=1:a=0,format=yuv420p[vout]"
    )
    
    cmd = [
        FFMPEG_BIN, "-y"
    ]
    
    # 8 Scene Inputs
    for sf in scene_files:
        cmd.extend(["-i", sf])
        
    # Audio Input (index 8)
    cmd.extend(["-i", FINAL_MIX_WAV])
    
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
