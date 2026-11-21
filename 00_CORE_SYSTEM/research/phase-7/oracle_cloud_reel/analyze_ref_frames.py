import cv2
import os
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ref4_path = r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04.mp4"
out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\ref_forensics"
os.makedirs(out_dir, exist_ok=True)

# 1. Extract 10 consecutive frames at 3.0s (when junior is speaking)
cap = cv2.VideoCapture(ref4_path)
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"ref_04 FPS: {fps}")

start_f = int(3.0 * fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, start_f)

for i in range(12):
    ret, frame = cap.read()
    if not ret: break
    cv2.imwrite(os.path.join(out_dir, f"ref4_speaking_f{i}.jpg"), frame)
    
print("Saved 12 consecutive speech frames from ref_04!")

# 2. Extract Audio from ref_04 to analyze voice
import subprocess
audio_out = os.path.join(out_dir, "ref_04_audio.wav")
cmd = [FFMPEG, "-y", "-i", ref4_path, "-vn", "-ac", "1", "-ar", "24000", audio_out]
subprocess.run(cmd, check=True)
print("Extracted ref_04 audio:", audio_out)
