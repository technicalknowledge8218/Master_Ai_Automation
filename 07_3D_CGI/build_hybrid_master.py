import os
import subprocess
import imageio_ffmpeg
import cv2
import json

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
workdir = r"F:\Master AI\07_3D_CGI\renders"

real_clip = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\benchmark-7.0.4\real_footage_sample.webm"
cgi_3d_clip = os.path.join(workdir, "scene_b_lion.mp4")
anim_2d_clip = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\benchmark-7.0.4\benchmark_2d_720p.mp4"
out_master_mp4 = os.path.join(workdir, "true_hybrid_acceptance_720p.mp4")

def build_hybrid_video():
    print("================================================================================")
    print("ASSEMBLING MASTER AI THREE-MEDIUM HYBRID PRODUCTION ACCEPTANCE MASTER")
    print("================================================================================")
    
    # Check all three inputs exist
    for p, label in [(real_clip, "Real Footage"), (cgi_3d_clip, "3D CGI Animation"), (anim_2d_clip, "2D Motion Graphics")]:
        if not os.path.isfile(p):
            raise FileNotFoundError(f"Missing required input clip ({label}): {p}")
        print(f"Verified input [{label}]: {p} ({os.path.getsize(p)} bytes)")

    # Timeline design:
    # Scene 1: Real Footage (0.0 to 4.0s)
    # [Transition 1: xfade fade from 3.0 to 4.0s]
    # Scene 2: Actual 3D CGI (3.0 to 7.0s)
    # [Transition 2: xfade wipeleft from 6.0 to 7.0s]
    # Scene 3: 2D Infographics (6.0 to 10.0s)
    # Total Video Duration = 9.0s (or 10.0s depending on scene 3 cut)
    # Total frames = 216 frames @ 24 FPS
    
    cmd = [
        ffmpeg_exe, "-y",
        "-ss", "0", "-t", "4.0", "-i", real_clip,
        "-ss", "0", "-t", "4.0", "-i", cgi_3d_clip,
        "-ss", "0", "-t", "4.0", "-i", anim_2d_clip,
        "-f", "lavfi", "-i", "sine=frequency=320:duration=10.0",
        "-filter_complex",
        "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[v0];"
        "[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[v1];"
        "[2:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[v2];"
        "[v0][v1]xfade=transition=fade:duration=1.0:offset=3.0[v01];"
        "[v01][v2]xfade=transition=wipeleft:duration=1.0:offset=6.0[v_out];"
        "[3:a]volume=0.25,afade=t=out:st=8.0:d=1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "9.5",
        out_master_mp4
    ]

    print("Running FFmpeg multi-medium assembly pipeline...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg error:", res.stderr[-800:])
        raise RuntimeError("FFmpeg hybrid assembly failed.")

    print(f"Master Hybrid Video successfully generated: {out_master_mp4}")
    print(f"File size: {os.path.getsize(out_master_mp4)} bytes")

    # Deep OpenCV integrity verification
    cap = cv2.VideoCapture(out_master_mp4)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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

    print("\n--- HYBRID MASTER QA VERIFICATION ---")
    print(f"Resolution: {w}x{h}")
    print(f"FPS: {fps}")
    print(f"Total Frames: {total_frames}")
    print(f"Decoded Frames: {decoded}")
    print(f"Unreadable Frames: {unreadable}")
    status = "PASS" if decoded == total_frames and unreadable == 0 else "FAIL"
    print(f"Hybrid Acceptance Status: {status}")

    meta = {
        "output_file": out_master_mp4,
        "size_bytes": os.path.getsize(out_master_mp4),
        "resolution": f"{w}x{h}",
        "fps": fps,
        "total_frames": total_frames,
        "decoded_frames": decoded,
        "unreadable_frames": unreadable,
        "status": status,
        "medium_1_real_footage": real_clip,
        "medium_2_3d_cgi": cgi_3d_clip,
        "medium_3_2d_animation": anim_2d_clip
    }
    with open(os.path.join(workdir, "hybrid_master_metrics.json"), "w") as f:
        json.dump(meta, f, indent=2)

if __name__ == "__main__":
    build_hybrid_video()
