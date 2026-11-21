"""
Inspect the audio content of african_lion_life_in_the_wild_720p.mp4
"""
import os
import subprocess
import imageio_ffmpeg
import numpy as np

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
mp4_path = r"F:\Master AI\09_CONTENT_STUDIO\renders\pilot_lion_documentary\african_lion_life_in_the_wild_720p.mp4"
out_wav = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.2.1-audit\extracted_pilot_audio.wav"

cmd = [
    FFMPEG, "-y", "-i", mp4_path,
    "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
    out_wav
]
subprocess.run(cmd, check=True)

import wave
with wave.open(out_wav, "rb") as wf:
    frames = wf.getnframes()
    rate = wf.getframerate()
    duration = frames / float(rate)
    data = wf.readframes(frames)

samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

print(f"Extracted Audio Duration: {duration:.2f}s, Samples: {len(samples)}")
print(f"RMS Energy: {np.sqrt(np.mean(samples**2)):.4f}")
print(f"Peak Energy: {np.max(np.abs(samples)):.4f}")

# Check segments of 5 seconds each to see energy across the timeline
print("\nSegment-by-Segment RMS Energy (5-second windows):")
for sec in range(0, int(duration), 5):
    sub = samples[sec*rate : (sec+5)*rate]
    if len(sub) > 0:
        sub_rms = np.sqrt(np.mean(sub**2))
        sub_peak = np.max(np.abs(sub))
        print(f"[{sec:02d}s - {sec+5:02d}s]: RMS={sub_rms:.4f}, Peak={sub_peak:.4f}")
