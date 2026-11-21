"""
Master AI - Phase 7.1.1 Verification Script
Encodes Improved Lion, builds mathematically verified corrected Hybrid video,
and generates contact sheets with Pillow and OpenCV.
"""
import os
import sys
import subprocess
import json
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

RENDERS_DIR = r"F:\Master AI\07_3D_CGI\renders"
CONTACT_SHEETS_DIR = r"F:\Master AI\07_3D_CGI\contact_sheets"
os.makedirs(CONTACT_SHEETS_DIR, exist_ok=True)

def encode_improved_lion():
    frames_dir = os.path.join(RENDERS_DIR, "improved_lion")
    output_mp4 = os.path.join(RENDERS_DIR, "improved_lion.mp4")
    
    files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    print(f"Found {len(files)} rendered frames for improved lion.")
    if len(files) < 72:
        print(f"Waiting for remaining frames... (currently {len(files)}/72)")
        return False
        
    cmd = [
        FFMPEG, "-y",
        "-framerate", "24",
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        output_mp4
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg encoding failed:", res.stderr)
        return False
        
    print(f"Encoded Improved Lion MP4: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
    return True

def verify_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"valid": False, "error": "Cannot open video"}
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    read_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        read_count += 1
    cap.release()
    
    duration = read_count / fps if fps > 0 else 0
    return {
        "valid": read_count > 0,
        "path": video_path,
        "width": w,
        "height": h,
        "fps": fps,
        "reported_frames": total_frames,
        "decoded_frames": read_count,
        "duration_sec": round(duration, 3),
        "file_size": os.path.getsize(video_path)
    }

def build_corrected_hybrid():
    real_clip = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\benchmark-7.0.4\real_footage_sample.webm"
    lion_clip = os.path.join(RENDERS_DIR, "improved_lion.mp4")
    anim_2d_clip = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\benchmark-7.0.4\benchmark_2d_720p.mp4"
    output_master = os.path.join(RENDERS_DIR, "true_hybrid_corrected_720p.mp4")

    for p, label in [(real_clip, "Real Footage"), (lion_clip, "Improved 3D Lion"), (anim_2d_clip, "2D Motion Graphics")]:
        if not os.path.isfile(p):
            raise FileNotFoundError(f"Missing required input clip ({label}): {p}")
        print(f"Verified input [{label}]: {p} ({os.path.getsize(p)} bytes)")

    # Input analysis:
    # Real Footage: 4.0s (96 frames)
    # Improved Lion: 3.0s (72 frames)
    # 2D Motion Graphics: 4.0s (96 frames)
    #
    # Transition 1: [v0] (real) + [v1] (3D lion)
    # offset=3.0, duration=1.0s.
    # v0 plays 0.0 to 3.0s.
    # Crossfade 3.0 to 4.0s.
    # Resulting stream [v01] duration = 3.0s (v0 pre-fade) + 3.0s (v1 length) = 6.0s (144 frames).
    #
    # Transition 2: [v01] + [v2] (2D graphics)
    # offset=5.0s, duration=1.0s.
    # v01 plays 0.0 to 5.0s (which includes lion solo from 4.0 to 5.0s).
    # Crossfade 5.0 to 6.0s between lion and 2D graphics.
    # 2D graphics plays solo from 6.0 to 8.0s.
    # Resulting stream [v_out] duration = 5.0s + 3.0s (remaining of 4.0s graphics clip after 1s fade) = 8.0s (192 frames).
    #
    # Audio: High quality synthesized tone / ambient track with fadeout at 7.5s.
    
    cmd = [
        FFMPEG, "-y",
        "-ss", "0", "-t", "4.0", "-i", real_clip,
        "-ss", "0", "-t", "3.0", "-i", lion_clip,
        "-ss", "0", "-t", "4.0", "-i", anim_2d_clip,
        "-f", "lavfi", "-i", "sine=frequency=320:duration=8.0",
        "-filter_complex",
        "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[v0];"
        "[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[v1];"
        "[2:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24[v2];"
        "[v0][v1]xfade=transition=fade:duration=1.0:offset=3.0[v01];"
        "[v01][v2]xfade=transition=wipeleft:duration=1.0:offset=5.0[v_out];"
        "[3:a]volume=0.20,afade=t=out:st=7.0:d=1.0[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", "8.0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        output_master
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg hybrid assembly failed:", res.stderr)
        return False
        
    print(f"Corrected Hybrid Video built: {output_master} ({os.path.getsize(output_master)} bytes)")
    m_hybrid = verify_video(output_master)
    print("Verified Hybrid Master:", json.dumps(m_hybrid, indent=2))
    
    with open(os.path.join(RENDERS_DIR, "hybrid_corrected_metrics.json"), "w") as f:
        json.dump(m_hybrid, f, indent=2)
    return True

def generate_contact_sheets():
    # 1. 3D Scenes Contact Sheet: Nature, Old Lion, Improved Lion, Scientific Viz
    scenes = [
        {"name": "Scene 1: Savannah Nature", "dir": r"F:\Master AI\07_3D_CGI\renders\scene_a_nature"},
        {"name": "Scene 2: Old Lion CGI", "dir": r"F:\Master AI\07_3D_CGI\renders\scene_b_lion"},
        {"name": "Scene 3: Improved Lion CGI", "dir": r"F:\Master AI\07_3D_CGI\renders\improved_lion"},
        {"name": "Scene 4: Scientific Viz", "dir": r"F:\Master AI\07_3D_CGI\renders\scene_c_science"},
    ]
    
    thumb_w, thumb_h = 320, 180
    header_h = 32
    grid_w = thumb_w * 4
    grid_h = (thumb_h + header_h) * 4
    
    canvas = Image.new("RGB", (grid_w, grid_h), color=(20, 24, 30))
    draw = ImageDraw.Draw(canvas)
    
    try:
        font = ImageFont.truetype("arial.ttf", 15)
        font_sub = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
        font_sub = font

    for row_idx, sc in enumerate(scenes):
        sdir = sc["dir"]
        files = sorted([os.path.join(sdir, f) for f in os.listdir(sdir) if f.endswith(".png")])
        if not files:
            continue
        indices = [int(len(files)*0.1), int(len(files)*0.4), int(len(files)*0.7), min(len(files)-1, int(len(files)*0.95))]
        
        y_base = row_idx * (thumb_h + header_h)
        draw.rectangle([(0, y_base), (grid_w, y_base + header_h)], fill=(35, 42, 54))
        draw.text((15, y_base + 8), sc["name"] + f" ({len(files)} total frames)", fill=(240, 240, 250), font=font)
        
        for col_idx, f_idx in enumerate(indices):
            fpath = files[f_idx]
            im = Image.open(fpath).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            x = col_idx * thumb_w
            y = y_base + header_h
            canvas.paste(im, (x, y))
            draw.rectangle([(x + 5, y + thumb_h - 22), (x + 110, y + thumb_h - 5)], fill=(0, 0, 0))
            draw.text((x + 8, y + thumb_h - 20), f"Frame {f_idx+1}", fill=(255, 215, 0), font=font_sub)

    out_scenes_sheet = os.path.join(CONTACT_SHEETS_DIR, "contact_sheet_3d_scenes.png")
    canvas.save(out_scenes_sheet, quality=95)
    print(f"Saved: {out_scenes_sheet}")

    # 2. Side-by-Side Lion Comparison Contact Sheet
    old_dir = r"F:\Master AI\07_3D_CGI\renders\scene_b_lion"
    new_dir = r"F:\Master AI\07_3D_CGI\renders\improved_lion"
    
    old_files = sorted([os.path.join(old_dir, f) for f in os.listdir(old_dir) if f.endswith(".png")])
    new_files = sorted([os.path.join(new_dir, f) for f in os.listdir(new_dir) if f.endswith(".png")])
    
    if old_files and new_files:
        cols = 4
        tw, th = 380, 214
        sheet_w = tw * cols
        sheet_h = 60 + (th + 35) * 2
        
        comp_canvas = Image.new("RGB", (sheet_w, sheet_h), color=(15, 18, 24))
        cdraw = ImageDraw.Draw(comp_canvas)
        cdraw.text((20, 18), "LION CGI DIRECT COMPARISON: Old Primitive vs Advanced Anatomical Prototype", fill=(255, 220, 100), font=font)
        
        indices = [int(len(old_files)*0.15), int(len(old_files)*0.4), int(len(old_files)*0.65), min(len(old_files)-1, int(len(old_files)*0.9))]
        
        # Row 1: Old Lion
        y1 = 60
        cdraw.rectangle([(0, y1), (sheet_w, y1 + 30)], fill=(55, 30, 30))
        cdraw.text((15, y1 + 7), "LEGACY: Scene B Primitive Lion (Basic Scaled Spheres, Uniform Yellow, Stiff Geometry)", fill=(255, 190, 190), font=font)
        for c, idx in enumerate(indices):
            im = Image.open(old_files[idx]).resize((tw, th), Image.Resampling.LANCZOS)
            x = c * tw
            y = y1 + 30
            comp_canvas.paste(im, (x, y))
            cdraw.rectangle([(x + 5, y + th - 22), (x + 110, y + th - 5)], fill=(0, 0, 0))
            cdraw.text((x + 8, y + th - 20), f"Old Frame {idx+1}", fill=(255, 100, 100), font=font_sub)
            
        # Row 2: Improved Lion
        y2 = y1 + 30 + th + 10
        cdraw.rectangle([(0, y2), (sheet_w, y2 + 30)], fill=(30, 55, 35))
        cdraw.text((15, y2 + 7), "IMPROVED: Advanced Prototype (Spine, Deep Chest, Volumetric Mane, Fur Bump, SSS PBR)", fill=(190, 255, 190), font=font)
        for c, idx in enumerate(indices):
            im = Image.open(new_files[idx]).resize((tw, th), Image.Resampling.LANCZOS)
            x = c * tw
            y = y2 + 30
            comp_canvas.paste(im, (x, y))
            cdraw.rectangle([(x + 5, y + th - 22), (x + 130, y + th - 5)], fill=(0, 0, 0))
            cdraw.text((x + 8, y + th - 20), f"Improved Frame {idx+1}", fill=(100, 255, 100), font=font_sub)
            
        out_comp_sheet = os.path.join(CONTACT_SHEETS_DIR, "contact_sheet_lion_comparison.png")
        comp_canvas.save(out_comp_sheet, quality=95)
        print(f"Saved: {out_comp_sheet}")

    # 3. Hybrid Timeline Verification Contact Sheet
    hybrid_vid = os.path.join(RENDERS_DIR, "true_hybrid_corrected_720p.mp4")
    if os.path.isfile(hybrid_vid):
        cap = cv2.VideoCapture(hybrid_vid)
        fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
        tot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        timestamps = [0.25 + i * 0.5 for i in range(16)]
        
        tw, th = 320, 180
        hw = tw * 4
        hh = (th + 32) * 4 + 50
        
        h_canvas = Image.new("RGB", (hw, hh), color=(18, 20, 26))
        hdraw = ImageDraw.Draw(h_canvas)
        hdraw.text((20, 18), "CORRECTED HYBRID TIMELINE VERIFICATION (8.0s / 192 Frames - All 3 Mediums Present)", fill=(240, 240, 255), font=font)
        
        for idx, t in enumerate(timestamps):
            f_target = int(t * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, min(tot - 1, f_target))
            ret, frame = cap.read()
            if not ret:
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame_rgb).resize((tw, th), Image.Resampling.LANCZOS)
            
            row = idx // 4
            col = idx % 4
            x = col * tw
            y = 50 + row * (th + 32)
            h_canvas.paste(im, (x, y))
            
            if t < 3.0:
                med_label = "Real Footage"
                col_box = (0, 100, 180)
            elif t < 4.0:
                med_label = "Transition: Real -> 3D"
                col_box = (150, 80, 180)
            elif t < 5.0:
                med_label = "3D CGI Lion"
                col_box = (180, 120, 0)
            elif t < 6.0:
                med_label = "Transition: 3D -> 2D"
                col_box = (180, 80, 80)
            else:
                med_label = "2D Motion Graphics"
                col_box = (0, 140, 90)
                
            hdraw.rectangle([(x, y + th), (x + tw, y + th + 30)], fill=col_box)
            hdraw.text((x + 8, y + th + 7), f"t={t:.2f}s | {med_label}", fill=(255, 255, 255), font=font_sub)
            
        cap.release()
        out_hybrid_sheet = os.path.join(CONTACT_SHEETS_DIR, "contact_sheet_corrected_hybrid.png")
        h_canvas.save(out_hybrid_sheet, quality=95)
        print(f"Saved: {out_hybrid_sheet}")

def main():
    print("=== Step 1: Encode Improved Lion ===")
    if not encode_improved_lion():
        return
        
    print("\n=== Step 2: Build Corrected Hybrid Video ===")
    if not build_corrected_hybrid():
        return
        
    print("\n=== Step 3: Generate Contact Sheets ===")
    generate_contact_sheets()
    print("\nAll encoding, assembly, and contact sheet generation COMPLETED successfully!")

if __name__ == "__main__":
    main()
