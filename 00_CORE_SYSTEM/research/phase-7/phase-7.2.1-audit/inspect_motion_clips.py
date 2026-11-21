"""
Inspect DOC-26c9a068 scene_01_motion.mp4 and scene_06_motion.mp4
"""
import os
import cv2
import numpy as np

for sc_name in ["scene_01_motion.mp4", "scene_06_motion.mp4"]:
    sc_path = os.path.join(r"F:\Master AI\09_CONTENT_STUDIO\documentaries\DOC-26c9a068\assets", sc_name)
    cap = cv2.VideoCapture(sc_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    ret, f0 = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, frames // 2)
    ret, fmid = cap.read()
    cap.release()
    
    diff = float(np.mean(cv2.absdiff(f0, fmid))) if ret else 0.0
    print(f"[{sc_name}]: {w}x{h} @ {fps}fps, {frames} frames, Diff(start, mid): {diff:.2f}")
