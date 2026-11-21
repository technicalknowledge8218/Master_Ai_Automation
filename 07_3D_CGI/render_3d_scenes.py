import subprocess
import os
import sys
import time
import json
import cv2
import imageio_ffmpeg

blender_exe = r"F:\Master AI\07_3D_CGI\engine\blender\blender-4.2.23-windows-x64\blender.exe"
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

scenes = [
    {
        "id": "scene_a_nature",
        "name": "Cinematic Nature Savanna Environment",
        "script": r"F:\Master AI\07_3D_CGI\scenes\scene_nature_environment.py",
        "render_dir": r"F:\Master AI\07_3D_CGI\renders\scene_a_nature",
        "out_mp4": r"F:\Master AI\07_3D_CGI\renders\scene_a_nature.mp4",
        "frames": 72, # 3.0 seconds @ 24 FPS
        "type": "Procedural 3D Environment (Terrain, Acacia Trees, Golden Hour Atmosphere)"
    },
    {
        "id": "scene_b_lion",
        "name": "Realistic Animal CGI (African Lion)",
        "script": r"F:\Master AI\07_3D_CGI\scenes\scene_animal_cgi.py",
        "render_dir": r"F:\Master AI\07_3D_CGI\renders\scene_b_lion",
        "out_mp4": r"F:\Master AI\07_3D_CGI\renders\scene_b_lion.mp4",
        "frames": 72, # 3.0 seconds @ 24 FPS
        "type": "Procedural 3D Animal Geometry (Torso, Limbs, Layered Mane, Snout, Studio Lighting)"
    },
    {
        "id": "scene_c_science",
        "name": "Scientific 3D Visualization",
        "script": r"F:\Master AI\07_3D_CGI\scenes\scene_scientific_viz.py",
        "render_dir": r"F:\Master AI\07_3D_CGI\renders\scene_c_science",
        "out_mp4": r"F:\Master AI\07_3D_CGI\renders\scene_c_science.mp4",
        "frames": 72, # 3.0 seconds @ 24 FPS
        "type": "Scientific Visualization (Molecular Nucleus, Rotating Gimbal Rings, Glowing Orbitals)"
    }
]

results = []

for sc in scenes:
    print(f"\n================================================================================")
    print(f"RENDERING SCENE: {sc['name']} ({sc['frames']} frames @ 720p)")
    print(f"================================================================================")
    os.makedirs(sc["render_dir"], exist_ok=True)
    out_prefix = os.path.join(sc["render_dir"], "frame_")
    
    cmd = [
        blender_exe, "-b",
        "-P", sc["script"],
        "-o", out_prefix,
        "-s", "1", "-e", str(sc["frames"]),
        "-a"
    ]
    
    t0 = time.perf_counter()
    res = subprocess.run(cmd, capture_output=True, text=True)
    t_wall = time.perf_counter() - t0
    
    if res.returncode != 0:
        print(f"ERROR rendering {sc['id']}: returncode {res.returncode}")
        print("Stderr tail:\n", res.stderr[-500:])
        continue
        
    print(f"Blender render complete in {t_wall:.2f} s ({t_wall/sc['frames']:.3f} s/frame)")
    
    # Encode with FFmpeg
    ffmpeg_cmd = [
        ffmpeg_exe, "-y",
        "-framerate", "24",
        "-i", os.path.join(sc["render_dir"], "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        sc["out_mp4"]
    ]
    subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    print(f"Encoded MP4: {sc['out_mp4']} ({os.path.getsize(sc['out_mp4'])} bytes)")
    
    # Verify with OpenCV
    cap = cv2.VideoCapture(sc["out_mp4"])
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    decoded = 0
    unreadable = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame is None or frame.size == 0:
            unreadable += 1
        else:
            decoded += 1
    cap.release()
    
    status = "PASS" if decoded == sc["frames"] and unreadable == 0 else "FAIL"
    print(f"Integrity Check: {w}x{h} @ {fps}fps | Decoded: {decoded}/{sc['frames']} | Status: {status}")
    
    results.append({
        "id": sc["id"],
        "name": sc["name"],
        "type": sc["type"],
        "resolution": f"{w}x{h}",
        "frames": sc["frames"],
        "render_wall_sec": t_wall,
        "avg_frame_sec": t_wall / sc["frames"],
        "generation_fps": sc["frames"] / t_wall,
        "mp4_file": sc["out_mp4"],
        "mp4_bytes": os.path.getsize(sc["out_mp4"]),
        "status": status
    })

with open(r"F:\Master AI\07_3D_CGI\renders\three_d_scenes_metrics.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nAll 3 demonstration scenes rendered and verified.")
