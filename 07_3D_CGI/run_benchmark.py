import subprocess
import time
import os
import re
import psutil
import json
import cv2
import imageio_ffmpeg

blender_exe = r"F:\Master AI\07_3D_CGI\engine\blender\blender-4.2.23-windows-x64\blender.exe"
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
workdir = r"F:\Master AI\07_3D_CGI\renders\benchmark_720p"
os.makedirs(workdir, exist_ok=True)

out_mp4 = r"F:\Master AI\07_3D_CGI\renders\benchmark_3d_720p.mp4"

print("================================================================================")
print("STARTING BLENDER REAL-MACHINE HARDWARE BENCHMARK (EEVEE NEXT 720p)")
print("================================================================================")
print("Blender Executable:", blender_exe)
print("Host CPU:", psutil.cpu_count(logical=False), "physical cores,", psutil.cpu_count(logical=True), "logical threads")
vm = psutil.virtual_memory()
print(f"Host RAM: {vm.total/(1024**3):.1f} GB Total, {vm.available/(1024**3):.1f} GB Available")

# 1. Execute 720p 120-frame animation render (frames 1 to 120)
cmd_720p = [
    blender_exe, "-b",
    "-P", r"F:\Master AI\07_3D_CGI\scenes\scene_benchmark.py",
    "-s", "1", "-e", "120",
    "-a"
]

t0 = time.perf_counter()
proc_info = psutil.Process()
mem_start = proc_info.memory_info().rss / (1024*1024)

res = subprocess.run(cmd_720p, capture_output=True, text=True)
t_render = time.perf_counter() - t0

print("\n--- 720p BATCH RENDER COMPLETE ---")
print(f"Total Wall-Clock Time: {t_render:.2f} s")
print("Return Code:", res.returncode)

# Parse Blender output log for frame render times
frame_durations = []
for line in res.stdout.splitlines():
    m = re.search(r"Fra:(\d+).*Time:\s*(\d+):(\d+\.\d+)\s*\(Saving", line)
    if m:
        sec = float(m.group(2)) * 60 + float(m.group(3))
        frame_durations.append((int(m.group(1)), sec))

if frame_durations:
    durations_only = [d[1] for d in frame_durations]
    avg_frame = sum(durations_only) / len(durations_only)
    min_frame = min(durations_only)
    max_frame = max(durations_only)
    fps_render = 120.0 / t_render
    print(f"Parsed {len(frame_durations)} completed frame renders.")
    print(f"Average frame render time: {avg_frame:.3f} s ({fps_render:.2f} FPS effective speed)")
    print(f"Min frame time: {min_frame:.3f} s | Max frame time (includes shader compile): {max_frame:.3f} s")
    # Steady state (excluding first frame shader compile)
    if len(durations_only) > 1:
        steady_avg = sum(durations_only[1:]) / len(durations_only[1:])
        print(f"Steady-state average frame time: {steady_avg:.3f} s ({1.0/steady_avg:.2f} FPS)")
else:
    avg_frame = t_render / 120.0
    print(f"Estimated average: {avg_frame:.3f} s / frame")

# 2. Encode to MP4 with FFmpeg
print("\nEncoding 3D frames to MP4 with FFmpeg...")
t_enc0 = time.perf_counter()
ffmpeg_cmd = [
    ffmpeg_exe, "-y",
    "-framerate", "24",
    "-i", os.path.join(workdir, "frame_%04d.png"),
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    out_mp4
]
res_enc = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
t_encode = time.perf_counter() - t_enc0
print(f"FFmpeg encoding complete in {t_encode:.2f} s. Output size: {os.path.getsize(out_mp4)} bytes")

# 3. Verify MP4 video integrity
cap = cv2.VideoCapture(out_mp4)
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

print("\n--- MP4 VERIFICATION ---")
print(f"Resolution: {w}x{h}")
print(f"FPS: {fps}")
print(f"Reported Frames: {count}")
print(f"Decoded Frames: {decoded}")
print(f"Unreadable Frames: {unreadable}")
integrity_pass = (decoded == 120 and unreadable == 0)
print("Integrity Status:", "PASS" if integrity_pass else "FAIL")

# 4. Measure 1080p Single-Frame Benchmark
print("\n--- BENCHMARKING 1080p SCALING (Frame 60) ---")
out_1080p = r"F:\Master AI\07_3D_CGI\renders\bench_1080p_frame60.png"
script_1080p = f"""
import bpy
import sys
sys.path.append(r'F:\\Master AI\\07_3D_CGI\\scenes')
from scene_benchmark import setup_benchmark_scene
setup_benchmark_scene(res_x=1920, res_y=1080, total_frames=120, samples=16, output_path=r'{out_1080p}')
bpy.context.scene.frame_current = 60
bpy.context.scene.render.filepath = r'{out_1080p}'
bpy.ops.render.render(write_still=True)
"""
with open(r"F:\Master AI\07_3D_CGI\scenes\run_1080p_still.py", "w") as f:
    f.write(script_1080p)

t_1080_0 = time.perf_counter()
res_1080p = subprocess.run([
    blender_exe, "-b",
    "-P", r"F:\Master AI\07_3D_CGI\scenes\run_1080p_still.py"
], capture_output=True, text=True)
t_1080 = time.perf_counter() - t_1080_0
print(f"1080p Still Render Time: {t_1080:.2f} s")
if os.path.exists(out_1080p):
    print(f"1080p Still Output Size: {os.path.getsize(out_1080p)} bytes")

# Save complete metrics to JSON
metrics = {
    "engine": "BLENDER_EEVEE_NEXT",
    "blender_version": "4.2.23 LTS",
    "resolution_720p": {"width": 1280, "height": 720, "fps": 24, "frames": 120},
    "render_wall_time_720p_sec": t_render,
    "avg_frame_time_720p_sec": t_render / 120.0,
    "steady_state_frame_time_720p_sec": steady_avg if 'steady_avg' in locals() else t_render/120.0,
    "generation_fps_720p": 120.0 / t_render,
    "encode_time_sec": t_encode,
    "output_mp4_bytes": os.path.getsize(out_mp4),
    "decoded_frames": decoded,
    "unreadable_frames": unreadable,
    "render_1080p_still_sec": t_1080,
    "integrity_status": "PASS" if integrity_pass else "FAIL"
}

with open(r"F:\Master AI\07_3D_CGI\renders\benchmark_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\nHardware benchmark complete. Metrics saved to benchmark_metrics.json")
