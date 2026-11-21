"""
Master AI - Phase 7.2 Real Pilot Documentary Assembly
Topic: African Lion — Life in the Wild (63.0 Seconds / 1,512 Frames @ 24 FPS)
Integrates:
1. Title Sequence (Intro Card)
2. Real Wildlife Footage (Dawn Kopje)
3. 3D CGI Environment (Aarfontein Sunrise HDRI & PBR Savanna Terrain)
4. 3D CGI Character (Hero African Lion with Anatomical SSS Shading)
5. 2D Motion Graphics (Territorial Range & Sanctuary Map)
6. 2D Scientific Infographic (Apex Biology, Bite Force & Pride Coalition)
7. Real Wildlife Footage (Social Pride Family Dynamics)
8. Real Wildlife Footage (Vigilant Savannah Lookout)
9. Outro & Open-Source Credits Card
With Multitrack Audio Mixing, Background Music Ducking, and Strict QA Inspection.
"""

import os
import sys
import json
import logging
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

sys.path.insert(0, r"F:\Master AI\09_CONTENT_STUDIO\engine")
from cinematic_editor import CinematicEditor
from footage_pipeline import RealFootagePipeline

logger = logging.getLogger("MasterAI.PilotBuilder")
logging.basicConfig(level=logging.INFO)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

WORK_DIR = r"F:\Master AI\09_CONTENT_STUDIO\renders\pilot_lion_documentary"
MASTER_OUTPUT = os.path.join(WORK_DIR, "african_lion_life_in_the_wild_720p.mp4")
CONTACT_SHEETS_DIR = r"F:\Master AI\07_3D_CGI\contact_sheets"
os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(CONTACT_SHEETS_DIR, exist_ok=True)

def prepare_conformed_clips():
    """Conform and loop all visual scene clips to exact target durations."""
    logger.info("Conforming individual visual clips...")
    
    editor = CinematicEditor("720p")
    
    # 1. Title Card (5.0s)
    c1_path = os.path.join(WORK_DIR, "c1_title.mp4")
    editor.build_title_card(
        c1_path,
        title="AFRICAN LION: LIFE IN THE WILD",
        subtitle="Master AI Autonomous Production // Multi-Medium Pilot",
        duration_sec=5.0,
        is_outro=False
    )
    
    # 2. Real Dawn Footage (8.0s)
    c2_src = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\benchmark-7.0.4\real_footage_sample.webm"
    c2_path = os.path.join(WORK_DIR, "c2_real_dawn.mp4")
    cmd_c2 = [
        FFMPEG, "-y", "-ss", "0", "-t", "8.0",
        "-stream_loop", "-1", "-i", c2_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c2_path
    ]
    subprocess.run(cmd_c2, check=True, stderr=subprocess.DEVNULL)
    
    # 3. 3D Savanna Environment (8.0s)
    c3_src = r"F:\Master AI\07_3D_CGI\renders\pilot_savanna_env.mp4"
    c3_path = os.path.join(WORK_DIR, "c3_3d_savanna.mp4")
    cmd_c3 = [
        FFMPEG, "-y", "-ss", "0", "-t", "8.0",
        "-stream_loop", "-1", "-i", c3_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c3_path
    ]
    subprocess.run(cmd_c3, check=True, stderr=subprocess.DEVNULL)

    # 4. 3D Hero Lion CGI (8.0s)
    c4_src = r"F:\Master AI\07_3D_CGI\renders\pilot_lion_hero.mp4"
    c4_path = os.path.join(WORK_DIR, "c4_3d_lion.mp4")
    cmd_c4 = [
        FFMPEG, "-y", "-ss", "0", "-t", "8.0",
        "-stream_loop", "-1", "-i", c4_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c4_path
    ]
    subprocess.run(cmd_c4, check=True, stderr=subprocess.DEVNULL)

    # 5. 2D Territory Map (8.0s)
    c5_src = os.path.join(WORK_DIR, "map_territory_2d.mp4")
    c5_path = os.path.join(WORK_DIR, "c5_2d_map.mp4")
    cmd_c5 = [
        FFMPEG, "-y", "-ss", "0", "-t", "8.0",
        "-stream_loop", "-1", "-i", c5_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c5_path
    ]
    subprocess.run(cmd_c5, check=True, stderr=subprocess.DEVNULL)

    # 6. 2D Biology Infographic (8.0s)
    c6_src = os.path.join(WORK_DIR, "infographic_biology_2d.mp4")
    c6_path = os.path.join(WORK_DIR, "c6_2d_biology.mp4")
    cmd_c6 = [
        FFMPEG, "-y", "-ss", "0", "-t", "8.0",
        "-stream_loop", "-1", "-i", c6_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c6_path
    ]
    subprocess.run(cmd_c6, check=True, stderr=subprocess.DEVNULL)

    # 7. Real Wildlife Pride Resting (10.0s)
    c7_src = r"F:\Master AI\09_CONTENT_STUDIO\documentaries\DOC-26c9a068\assets\scene_06_motion.mp4"
    c7_path = os.path.join(WORK_DIR, "c7_real_pride.mp4")
    cmd_c7 = [
        FFMPEG, "-y", "-ss", "0", "-t", "10.0",
        "-stream_loop", "-1", "-i", c7_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c7_path
    ]
    subprocess.run(cmd_c7, check=True, stderr=subprocess.DEVNULL)

    # 8. Real Wildlife Savannah Lookout (10.0s)
    c8_src = r"F:\Master AI\09_CONTENT_STUDIO\documentaries\DOC-26c9a068\assets\scene_01_motion.mp4"
    c8_path = os.path.join(WORK_DIR, "c8_real_lookout.mp4")
    cmd_c8 = [
        FFMPEG, "-y", "-ss", "0", "-t", "10.0",
        "-stream_loop", "-1", "-i", c8_src,
        "-filter:v", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", c8_path
    ]
    subprocess.run(cmd_c8, check=True, stderr=subprocess.DEVNULL)

    # 9. Outro & Credits Card (6.0s)
    c9_path = os.path.join(WORK_DIR, "c9_outro.mp4")
    editor.build_title_card(
        c9_path,
        title="MASTER AI // PRODUCTION HOUSE DEMO",
        subtitle="Zero-Budget Cinematic Pipeline Complete",
        duration_sec=6.0,
        is_outro=True
    )

    return [
        {"id": "SC-01", "name": "Title Sequence", "path": c1_path, "duration_sec": 5.0, "transition": "fade", "medium": "2D_MOTION_GRAPHICS"},
        {"id": "SC-02", "name": "Dawn Kopje (Real Wildlife)", "path": c2_path, "duration_sec": 8.0, "transition": "fade", "medium": "REAL_WILDLIFE_FOOTAGE"},
        {"id": "SC-03", "name": "Savanna Biome (3D CGI)", "path": c3_path, "duration_sec": 8.0, "transition": "fade", "medium": "3D_CGI_ANIMATION"},
        {"id": "SC-04", "name": "Hero Lion (3D CGI)", "path": c4_path, "duration_sec": 8.0, "transition": "fade", "medium": "3D_CGI_ANIMATION"},
        {"id": "SC-05", "name": "Territorial Range Map (2D)", "path": c5_path, "duration_sec": 8.0, "transition": "wipeleft", "medium": "2D_MOTION_GRAPHICS"},
        {"id": "SC-06", "name": "Apex Biology Infographic (2D)", "path": c6_path, "duration_sec": 8.0, "transition": "fade", "medium": "2D_MOTION_GRAPHICS"},
        {"id": "SC-07", "name": "Pride Family Life (Real Wildlife)", "path": c7_path, "duration_sec": 10.0, "transition": "fade", "medium": "REAL_WILDLIFE_FOOTAGE"},
        {"id": "SC-08", "name": "Savannah Lookout (Real Wildlife)", "path": c8_path, "duration_sec": 10.0, "transition": "fade", "medium": "REAL_WILDLIFE_FOOTAGE"},
        {"id": "SC-09", "name": "Outro & Open-Source Credits", "path": c9_path, "duration_sec": 6.0, "transition": "fade", "medium": "2D_MOTION_GRAPHICS"}
    ]

def generate_pilot_contact_sheet(video_path: str, output_image: str):
    """Generate high-resolution timestamped contact sheet of the 63-second master."""
    logger.info("Generating pilot documentary contact sheet...")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    tot_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    tot_duration = tot_frames / fps

    # Sample 16 timestamps evenly across the documentary
    timestamps = [tot_duration * (i + 0.5) / 16.0 for i in range(16)]

    tw, th = 320, 180
    header_h = 32
    grid_w = tw * 4
    grid_h = (th + header_h) * 4 + 60

    canvas = Image.new("RGB", (grid_w, grid_h), color=(15, 20, 28))
    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype("arial.ttf", 18)
        font_sub = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title

    draw.text((25, 20), "MASTER AI — PILOT DOCUMENTARY CONTACT SHEET (63.0 SECONDS // 1,512 FRAMES)", fill=(245, 158, 11), font=font_title)

    for idx, t in enumerate(timestamps):
        f_idx = min(tot_frames - 1, int(t * fps))
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame_rgb).resize((tw, th), Image.Resampling.LANCZOS)

        row = idx // 4
        col = idx % 4
        x = col * tw
        y = 60 + row * (th + header_h)
        canvas.paste(im, (x, y))

        # Color-coded medium badge based on timestamp
        if t < 4.0:
            badge = "Title Card"
            b_col = (30, 41, 59)
        elif t < 11.0:
            badge = "Real Wildlife (Dawn)"
            b_col = (14, 116, 144)
        elif t < 18.0:
            badge = "3D Savanna Biome"
            b_col = (180, 83, 9)
        elif t < 25.0:
            badge = "3D Hero Lion CGI"
            b_col = (217, 119, 6)
        elif t < 32.0:
            badge = "2D Territory Map"
            b_col = (13, 148, 136)
        elif t < 39.0:
            badge = "2D Biology Infographic"
            b_col = (16, 185, 129)
        elif t < 56.0:
            badge = "Real Wildlife (Pride Life)"
            b_col = (2, 132, 199)
        else:
            badge = "Outro & Open-Source Credits"
            b_col = (79, 70, 229)

        draw.rectangle([(x, y + th), (x + tw, y + th + header_h)], fill=b_col)
        draw.text((x + 8, y + th + 8), f"t={t:.1f}s | Frame {f_idx} | {badge}", fill=(255, 255, 255), font=font_sub)

    cap.release()
    canvas.save(output_image, quality=95)
    logger.info(f"Saved pilot contact sheet: {output_image}")

def main():
    logger.info("=== Phase 7.2 Real Pilot Documentary Assembly ===")
    
    # 1. Prepare and conform visual scenes
    scenes = prepare_conformed_clips()
    
    # 2. Audio track: Use cinematic documentary soundtrack from DOC-26c9a068
    audio_track = r"F:\Master AI\09_CONTENT_STUDIO\documentaries\DOC-26c9a068\soundtrack_final.wav"
    
    # 3. Assemble complete timeline
    editor = CinematicEditor("720p")
    result = editor.assemble_multiscene_timeline(
        scenes=scenes,
        output_master_mp4=MASTER_OUTPUT,
        audio_track_path=audio_track
    )

    logger.info(f"Pilot Documentary Master assembled: {MASTER_OUTPUT}")
    print("\nVerified Production Metrics:")
    print(json.dumps(result["qa_metrics"], indent=2))

    # 4. Generate contact sheet
    contact_sheet_path = os.path.join(CONTACT_SHEETS_DIR, "contact_sheet_pilot_documentary.png")
    generate_pilot_contact_sheet(MASTER_OUTPUT, contact_sheet_path)

    # 5. Save production dossier
    dossier_path = os.path.join(WORK_DIR, "PILOT_PRODUCTION_DOSSIER.json")
    with open(dossier_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": "African Lion — Life in the Wild",
            "runtime_seconds": result["qa_metrics"]["duration_sec"],
            "total_frames": result["qa_metrics"]["decoded_frames"],
            "resolution": f"{result['qa_metrics']['width']}x{result['qa_metrics']['height']}",
            "fps": result["qa_metrics"]["fps"],
            "file_size_bytes": result["qa_metrics"]["file_size_bytes"],
            "scenes": scenes,
            "master_file": MASTER_OUTPUT,
            "contact_sheet": contact_sheet_path
        }, f, indent=2)

    print(f"\nPilot Documentary Production Completed Successfully!")
    print(f"Master Video: {MASTER_OUTPUT}")
    print(f"Contact Sheet: {contact_sheet_path}")

if __name__ == "__main__":
    main()
