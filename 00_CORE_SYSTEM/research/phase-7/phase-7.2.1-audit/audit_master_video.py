"""
Master AI - Phase 7.2.1 Independent Audit Script: Master Video Verification
Audits F:\\Master AI\\09_CONTENT_STUDIO\\renders\\pilot_lion_documentary\\african_lion_life_in_the_wild_720p.mp4
"""

import os
import sys
import json
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VIDEO_PATH = r"F:\Master AI\09_CONTENT_STUDIO\renders\pilot_lion_documentary\african_lion_life_in_the_wild_720p.mp4"
AUDIT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.2.1-audit"

def run_ffprobe(video_path):
    cmd = [
        FFMPEG, "-i", video_path, "-hide_banner"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stderr

def audit_video_stream(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Failed to open video container"}

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    reported_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    decoded_frames = 0
    black_frames = []
    static_frames = []
    prev_gray = None
    luminance_vals = []

    sampled_frames_for_contact_sheet = []
    sample_interval = max(1, reported_frames // 16)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        decoded_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_lum = float(np.mean(gray))
        luminance_vals.append(mean_lum)

        if mean_lum < 5.0:
            black_frames.append(decoded_frames)

        if prev_gray is not None:
            diff = float(np.mean(cv2.absdiff(gray, prev_gray)))
            if diff < 0.2:
                static_frames.append(decoded_frames)
        prev_gray = gray

        if (decoded_frames - 1) % sample_interval == 0 and len(sampled_frames_for_contact_sheet) < 16:
            sampled_frames_for_contact_sheet.append((decoded_frames, frame.copy()))

    cap.release()

    duration_sec = decoded_frames / fps if fps > 0 else 0

    return {
        "width": width,
        "height": height,
        "fps": fps,
        "reported_frames": reported_frames,
        "decoded_frames": decoded_frames,
        "duration_sec": round(duration_sec, 3),
        "black_frames_count": len(black_frames),
        "black_frames_sample": black_frames[:15],
        "static_frames_count": len(static_frames),
        "mean_luminance": round(float(np.mean(luminance_vals)), 2),
        "min_luminance": round(float(np.min(luminance_vals)), 2),
        "max_luminance": round(float(np.max(luminance_vals)), 2),
        "file_size_bytes": os.path.getsize(video_path),
        "sampled_frames": sampled_frames_for_contact_sheet
    }

def audit_audio_stream(video_path):
    # Extract audio to temporary PCM WAV to inspect amplitude & properties
    temp_wav = os.path.join(AUDIT_DIR, "temp_extracted_audio.wav")
    cmd = [
        FFMPEG, "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
        temp_wav
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {"has_audio": False, "error": res.stderr}

    import wave
    with wave.open(temp_wav, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)

    audio_samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    duration_audio = n_frames / float(framerate)
    rms = float(np.sqrt(np.mean(audio_samples**2)))
    peak = float(np.max(np.abs(audio_samples)))
    silent_frames = int(np.sum(np.abs(audio_samples) < 0.005))
    silence_ratio = silent_frames / float(len(audio_samples))

    # Clean up temp wav
    if os.path.isfile(temp_wav):
        os.remove(temp_wav)

    return {
        "has_audio": True,
        "channels": n_channels,
        "sample_width_bytes": sampwidth,
        "framerate": framerate,
        "duration_sec": round(duration_audio, 3),
        "rms_amplitude": round(rms, 4),
        "peak_amplitude": round(peak, 4),
        "silence_ratio": round(silence_ratio, 4),
        "is_audible": rms > 0.01
    }

def build_contact_sheet(sampled_frames, output_png):
    tw, th = 320, 180
    hh = 30
    grid_w = tw * 4
    grid_h = (th + hh) * 4 + 50

    canvas = Image.new("RGB", (grid_w, grid_h), color=(15, 20, 26))
    draw = ImageDraw.Draw(canvas)

    try:
        font_h = ImageFont.truetype("arial.ttf", 16)
        font_s = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_h = ImageFont.load_default()
        font_s = font_h

    draw.text((20, 15), "INDEPENDENT AUDIT CONTACT SHEET // DIRECT MP4 DECODE (16 SAMPLES)", fill=(245, 158, 11), font=font_h)

    for i, (f_num, frame_bgr) in enumerate(sampled_frames[:16]):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame_rgb).resize((tw, th), Image.Resampling.LANCZOS)
        row = i // 4
        col = i % 4
        x = col * tw
        y = 50 + row * (th + hh)
        canvas.paste(im, (x, y))

        t_sec = f_num / 24.0
        draw.rectangle([(x, y + th), (x + tw, y + th + hh)], fill=(30, 41, 59))
        draw.text((x + 8, y + th + 6), f"Frame {f_num} | t={t_sec:.2f}s", fill=(255, 255, 255), font=font_s)

    canvas.save(output_png, quality=95)
    return output_png

def main():
    print("=== Phase 7.2.1 Independent Master Video Verification ===")
    if not os.path.isfile(VIDEO_PATH):
        print(f"ERROR: Video file not found at {VIDEO_PATH}")
        return

    ffprobe_log = run_ffprobe(VIDEO_PATH)
    print("\n--- FFprobe Container & Stream Probe ---")
    print(ffprobe_log)

    print("\n--- Video Frame-by-Frame Decode ---")
    v_metrics = audit_video_stream(VIDEO_PATH)
    sampled_frames = v_metrics.pop("sampled_frames")
    print(json.dumps(v_metrics, indent=2))

    print("\n--- Audio Stream Analysis ---")
    a_metrics = audit_audio_stream(VIDEO_PATH)
    print(json.dumps(a_metrics, indent=2))

    contact_sheet_path = os.path.join(AUDIT_DIR, "contact_sheet_verified_mp4.png")
    build_contact_sheet(sampled_frames, contact_sheet_path)
    print(f"\nContact sheet saved: {contact_sheet_path}")

    # Save full audit log to JSON
    audit_data = {
        "ffprobe_output": ffprobe_log,
        "video_metrics": v_metrics,
        "audio_metrics": a_metrics,
        "contact_sheet_path": contact_sheet_path
    }
    with open(os.path.join(AUDIT_DIR, "master_video_audit_data.json"), "w") as f:
        json.dump(audit_data, f, indent=2)

if __name__ == "__main__":
    main()
