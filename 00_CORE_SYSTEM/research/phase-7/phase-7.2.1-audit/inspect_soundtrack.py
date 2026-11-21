"""
Inspect audio contents of DOC-26c9a068\\soundtrack_final.wav
"""
import wave
import numpy as np

path = r"F:\Master AI\09_CONTENT_STUDIO\documentaries\DOC-26c9a068\soundtrack_final.wav"
with wave.open(path, "rb") as wf:
    print("Channels:", wf.getnchannels())
    print("Framerate:", wf.getframerate())
    print("Sample Width:", wf.getsampwidth())
    print("Total Frames:", wf.getnframes())
    print("Duration (s):", wf.getnframes() / wf.getframerate())
