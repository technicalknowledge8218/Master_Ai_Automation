"""
analyze_reference_video.py
==========================
Forensic Analyzer for demo_reference.mp4
Extracts:
1. Scene cut timestamps & durations using FFmpeg scene change filter.
2. Representative keyframe for every detected shot.
3. Audio track extraction & speech/silence analysis.
4. Editorial statistics: ASL (Average Shot Length), cut frequency, pacing curve.
"""

import os
import sys
import json
import math
import subprocess
import imageio_ffmpeg
import numpy as np
from PIL import Image

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.10"
REF_VIDEO = r"F:\Master AI\15_ASSETS\reference_videos\demo_reference.mp4"
FRAMES_DIR = os.path.join(BASE_DIR, "extracted_frames")
OUT_JSON = os.path.join(BASE_DIR, "reference_analysis", "forensic_data.json")

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

def detect_scenes(threshold=0.25):
    print(f"Running FFmpeg scene detection (threshold={threshold})...")
    # Use select='gt(scene,threshold)',showinfo filter to find exact cut timestamps
    cmd = [
        FFMPEG_BIN,
        "-i", REF_VIDEO,
        "-filter_complex", f"select='gt(scene,{threshold})',showinfo",
        "-f", "null",
        "-"
    ]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    
    scene_times = [0.0]
    for line in p.stderr:
        if "pts_time:" in line:
            try:
                parts = line.split("pts_time:")[1].split()[0]
                t = float(parts)
                # Filter out immediate false positives (< 0.4s apart)
                if t - scene_times[-1] >= 0.4:
                    scene_times.append(t)
            except Exception:
                pass
    p.wait()
    
    # Total duration is 108.20s
    total_dur = 108.20
    if scene_times[-1] < total_dur - 0.5:
        scene_times.append(total_dur)
        
    print(f"Detected {len(scene_times) - 1} shots across {total_dur:.2f}s.")
    return scene_times

def extract_representative_frames(scene_times):
    print("Extracting representative keyframes for each shot...")
    shots = []
    
    for i in range(len(scene_times) - 1):
        start_t = scene_times[i]
        end_t = scene_times[i + 1]
        dur = end_t - start_t
        mid_t = start_t + dur * 0.5
        
        shot_id = f"shot_{i+1:02d}"
        frame_name = f"{shot_id}_{mid_t:.2f}s.jpg"
        frame_path = os.path.join(FRAMES_DIR, frame_name)
        
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", f"{mid_t:.3f}",
            "-i", REF_VIDEO,
            "-vframes", "1",
            "-q:v", "2",
            frame_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        shots.append({
            "shot_id": shot_id,
            "shot_index": i + 1,
            "start_time": round(start_t, 3),
            "end_time": round(end_t, 3),
            "duration": round(dur, 3),
            "mid_time": round(mid_t, 3),
            "frame_image": frame_name
        })
        
    return shots

def analyze_audio():
    print("Extracting audio and analyzing volume/silence profiles...")
    wav_path = os.path.join(BASE_DIR, "reference_analysis", "ref_audio.wav")
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", REF_VIDEO,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Read wave file
    import wave
    with wave.open(wav_path, 'rb') as wf:
        n_ch = wf.getnchannels()
        sr = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
        
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    true_peak = float(np.max(np.abs(data)))
    true_peak_db = 20.0 * math.log10(max(1e-6, true_peak))
    rms = float(np.sqrt(np.mean(data ** 2)))
    rms_db = 20.0 * math.log10(max(1e-6, rms))
    
    # Silence detection with window of 0.25s
    win_samples = int(sr * 0.25)
    rms_envelope = []
    num_windows = n_frames // win_samples
    for w in range(num_windows):
        segment = data[w * win_samples * 2 : (w + 1) * win_samples * 2]
        w_rms = float(np.sqrt(np.mean(segment ** 2)))
        w_db = 20.0 * math.log10(max(1e-6, w_rms))
        rms_envelope.append(round(w_db, 1))
        
    silence_windows = sum(1 for d in rms_envelope if d < -38.0)
    silence_pct = (silence_windows / max(1, len(rms_envelope))) * 100.0
    
    return {
        "true_peak_dbfs": round(true_peak_db, 2),
        "rms_dbfs": round(rms_db, 2),
        "duration_sec": round(n_frames / float(sr), 2),
        "sample_rate": sr,
        "channels": n_ch,
        "silence_percentage": round(silence_pct, 2)
    }

def main():
    scene_times = detect_scenes(threshold=0.25)
    shots = extract_representative_frames(scene_times)
    audio_stats = analyze_audio()
    
    # Calculate editorial stats
    durations = [s["duration"] for s in shots]
    asl = float(np.mean(durations))
    median_shot = float(np.median(durations))
    min_shot = min(durations)
    max_shot = max(durations)
    cuts_per_minute = (len(shots) / 108.20) * 60.0
    
    report_data = {
        "file": REF_VIDEO,
        "video_properties": {
            "resolution": "1080x1920",
            "aspect_ratio": "9:16 (Vertical)",
            "codec": "hevc (H.265)",
            "framerate": 30.00,
            "framerate_mode": "CFR",
            "bitrate_kbps": 7452,
            "duration_sec": 108.20
        },
        "audio_properties": audio_stats,
        "editorial_statistics": {
            "total_shots": len(shots),
            "average_shot_length_sec": round(asl, 2),
            "median_shot_length_sec": round(median_shot, 2),
            "min_shot_length_sec": round(min_shot, 2),
            "max_shot_length_sec": round(max_shot, 2),
            "cuts_per_minute": round(cuts_per_minute, 2)
        },
        "shots": shots
    }
    
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    print(f"Forensic data saved to: {OUT_JSON}")
    print(f"Total Shots: {len(shots)} | ASL: {asl:.2f}s | Cuts/Min: {cuts_per_minute:.1f}")

if __name__ == "__main__":
    main()
