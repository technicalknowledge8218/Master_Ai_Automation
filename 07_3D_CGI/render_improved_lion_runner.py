"""
Runner to render Improved Lion scene using Blender 5.2.4 LTS via BlenderAdapter.
"""
import os
import sys
import time

sys.path.insert(0, r"F:\Master AI\07_3D_CGI\adapters")
from blender_adapter import BlenderAdapter

def main():
    adapter = BlenderAdapter()
    print("Detected Blender:", adapter.blender_exe)
    print("Blender Version:", adapter.version_info)
    
    scene_script = r"F:\Master AI\07_3D_CGI\scenes\scene_improved_lion.py"
    output_prefix = r"F:\Master AI\07_3D_CGI\renders\improved_lion\frame_"
    
    os.makedirs(r"F:\Master AI\07_3D_CGI\renders\improved_lion", exist_ok=True)
    
    def on_progress(cur, total, sec):
        if cur % 10 == 0 or cur == total:
            print(f"[Render Progress] Frame {cur}/{total} ({cur/total*100:.1f}%) - Frame render time: {sec:.2f}s")
            
    print("Starting rendering of Improved Lion (72 frames @ 720p)...")
    t0 = time.time()
    res = adapter.render_scene(
        scene_script_path=scene_script,
        output_prefix=output_prefix,
        start_frame=1,
        end_frame=72,
        resolution_x=1280,
        resolution_y=720,
        samples=16,
        progress_callback=on_progress,
        timeout_sec=600
    )
    t1 = time.time()
    print("Render Result Status:", res.get("status"))
    print("Total wall clock time:", t1 - t0, "seconds")
    print("Metrics:", res.get("metrics"))
    print("Output files found:", len(res.get("output_files", [])))

if __name__ == "__main__":
    main()
