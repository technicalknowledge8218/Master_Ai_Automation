import os
import sys
import fitz
import cv2
import numpy as np

# 1. Inspect decoded frames from final_video.mp4
cap = cv2.VideoCapture(r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\final_video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"final_video.mp4: {w}x{h} @ {fps}fps, total frames: {count}")

# Check differences between frame n and frame n+1 across different scenes
# Scene 1: frame 30
# Scene 2: frame 210
# Scene 3: frame 390
# Scene 4: frame 570
# Scene 5: frame 750
# Scene 6: frame 930
# Scene 7: frame 1110
# Scene 8: frame 1290

scene_starts = [0, 180, 360, 540, 720, 900, 1080, 1260]

for s_idx, start_f in enumerate(scene_starts):
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_f + 30)
    ret, f1 = cap.read()
    ret, f2 = cap.read()
    ret, f3 = cap.read()
    if ret:
        diff12 = np.mean(np.abs(f2.astype(float) - f1.astype(float)))
        diff23 = np.mean(np.abs(f3.astype(float) - f2.astype(float)))
        
        # Check vertical shift via cross-correlation on central crop
        crop1 = cv2.cvtColor(f1[200:880, 400:1520], cv2.COLOR_BGR2GRAY)
        crop2 = cv2.cvtColor(f2[200:880, 400:1520], cv2.COLOR_BGR2GRAY)
        crop3 = cv2.cvtColor(f3[200:880, 400:1520], cv2.COLOR_BGR2GRAY)
        
        # phase correlate
        shift12, response12 = cv2.phaseCorrelate(crop1.astype(np.float32), crop2.astype(np.float32))
        shift23, response23 = cv2.phaseCorrelate(crop2.astype(np.float32), crop3.astype(np.float32))
        
        print(f"Scene {s_idx+1} (frame {start_f+30}): diff12={diff12:.2f}, shift12={shift12}, shift23={shift23}")

cap.release()
