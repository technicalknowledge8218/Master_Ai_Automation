import subprocess
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()

# Extract 10s audio from ref_04
cmd = [
    FF, "-y", "-i", r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04.mp4",
    "-t", "15", "-vn", "-ar", "16000", "-ac", "1",
    r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\ref_04_snippet.wav"
]
subprocess.run(cmd, check=True)
print("ref_04 snippet extracted!")

# Also ref_01
cmd2 = [
    FF, "-y", "-i", r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_01.mp4",
    "-t", "15", "-vn", "-ar", "16000", "-ac", "1",
    r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\ref_01_snippet.wav"
]
subprocess.run(cmd2, check=True)
print("ref_01 snippet extracted!")
