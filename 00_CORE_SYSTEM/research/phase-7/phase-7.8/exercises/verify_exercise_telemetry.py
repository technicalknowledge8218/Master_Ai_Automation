"""
verify_exercise_telemetry.py
============================
Decodes all 7 exercise videos, inspects frame stability, measures optical flow,
and outputs verified technical telemetry for training_exercise_results.md.
"""

import os
import cv2
import numpy as np

EXERCISES_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8\exercises"

exercises = [
    ("ex01_cinematic_zoom.mp4", 120, 5.0, "Module 03: Cinematography"),
    ("ex02_character_reaction.mp4", 120, 5.0, "Module 05: Character Animation"),
    ("ex03_dialogue_lipsync.mp4", 120, 5.0, "Module 05 & 09: Lip-Sync & Dialogue"),
    ("ex04_suspense_editing.mp4", 120, 5.0, "Module 04 & 11: Suspense & Metric Cuts"),
    ("ex05_action_impact.mp4", 120, 5.0, "Module 03 & 07: Action & Damped Shake"),
    ("ex06_continuity_multishot.mp4", 240, 10.0, "Module 02 & 04: Multi-Shot Continuity"),
    ("ex07_comedy_timing.mp4", 240, 10.0, "Module 11: Comedy Timing & Pacing")
]

results = []

for fn, exp_frames, exp_sec, mod in exercises:
    path = os.path.join(EXERCISES_DIR, fn)
    cap = cv2.VideoCapture(path)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size_bytes = os.path.getsize(path)
    
    frames = []
    for _ in range(count):
        ret, f = cap.read()
        if ret: frames.append(f)
    cap.release()
    
    # Measure stability
    shifts_y = []
    for i in range(len(frames) - 1):
        g1 = cv2.cvtColor(frames[i][200:880, 400:1520], cv2.COLOR_BGR2GRAY)
        g2 = cv2.cvtColor(frames[i+1][200:880, 400:1520], cv2.COLOR_BGR2GRAY)
        shift, _ = cv2.phaseCorrelate(g1.astype(np.float32), g2.astype(np.float32))
        shifts_y.append(abs(shift[1]))
        
    mean_dy = float(np.mean(shifts_y)) if shifts_y else 0.0
    max_dy = float(np.max(shifts_y)) if shifts_y else 0.0
    
    res = {
        "file": fn,
        "module": mod,
        "frames": len(frames),
        "target_frames": exp_frames,
        "duration": len(frames) / fps if fps else 0.0,
        "resolution": f"{w}x{h}",
        "size_kb": size_bytes / 1024.0,
        "mean_dy": mean_dy,
        "max_dy": max_dy,
        "status": "PASS" if len(frames) == exp_frames and w == 1920 and h == 1080 else "FAIL"
    }
    results.append(res)
    print(f"{fn:30s} | {res['resolution']} | Frames: {res['frames']}/{exp_frames} | Mean dy: {mean_dy:.4f}px | {res['status']}")

# Save telemetry summary
import json
with open(os.path.join(EXERCISES_DIR, "exercises_telemetry.json"), "w") as f:
    json.dump(results, f, indent=2)
print("Saved exercises_telemetry.json")
