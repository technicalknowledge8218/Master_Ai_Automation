import os
import sys
import time
import numpy as np
import soundfile as sf
import scipy.signal
import subprocess
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\ai_voice_scam_reel"
ARTIFACT_DIR = r"<ARTIFACT_DIR>"

print(">>> [RE-RENDER] Assembling 100% PURE GEMINI TTS Audio Tracks...")

segments = [
    {
        "id": "scene_1_aman_hook",
        "speaker": "Aman (Victim)",
        "voice": "Gemini Puck",
        "badge": "🚨 EMERGENCY CALL",
        "pose": "junior_hands_up",
        "subtitle_hi": "कल मेरे दोस्त की हूबहू आवाज़ में कॉल आया...",
        "subtitle_en": "Got a call in my friend's exact voice... and lost ₹50,000!"
    },
    {
        "id": "scene_2_kabir_reveal",
        "speaker": "Kabir (Cyber Expert)",
        "voice": "Gemini Charon",
        "badge": "⚠️ AI VOICE SCAM EXPOSED",
        "pose": "senior_pointing_up",
        "subtitle_hi": "AI सिर्फ 3 सेकंड के ऑडियो से तुम्हारी आवाज़ कॉपी कर लेता है!",
        "subtitle_en": "AI clones your exact voice from just 3 seconds of audio!"
    },
    {
        "id": "scene_3_aman_question",
        "speaker": "Aman (Victim)",
        "voice": "Gemini Puck",
        "badge": "❓ HOW TO IDENTIFY?",
        "pose": "junior_shrug",
        "subtitle_hi": "तो फिर असली और नकली आवाज़ में फर्क कैसे पहचानें?",
        "subtitle_en": "How to tell real voice from AI voice clone?"
    },
    {
        "id": "scene_4_kabir_solution",
        "speaker": "Kabir (Cyber Expert)",
        "voice": "Gemini Charon",
        "badge": "🛡️ BULLETPROOF SAFETY RULE",
        "pose": "senior_explaining",
        "subtitle_hi": "फैमिली के साथ एक सीक्रेट 'सेफ्टी कोडवर्ड' तय करो!",
        "subtitle_en": "Set a Secret Safety Codeword with your family today!"
    }
]

sr = 24000
pause_gap = np.zeros(int(0.12 * sr), dtype=np.float32)
scene_timeline = []
combined_audio = []
current_time = 0.0

for item in segments:
    wav_path = os.path.join(PROJECT_DIR, f"{item['id']}.wav")
    data, file_sr = sf.read(wav_path)
    if file_sr != sr:
        num_s = int(len(data) * sr / file_sr)
        data = scipy.signal.resample(data, num_s)
    if data.ndim > 1: data = data.mean(axis=1)
    data = data.astype(np.float32)

    # Trim leading/trailing dead air
    threshold = 0.015 * np.max(np.abs(data)) if np.max(np.abs(data)) > 0 else 0.015
    non_s = np.where(np.abs(data) > threshold)[0]
    if len(non_s) > 0:
        data = data[max(0, non_s[0]-int(0.02*sr)):min(len(data), non_s[-1]+int(0.04*sr))]

    dur = len(data) / sr
    start_t = current_time
    end_t = start_t + dur
    scene_timeline.append({
        "item": item,
        "start": start_t,
        "end": end_t,
        "dur": dur
    })
    combined_audio.append(data)
    combined_audio.append(pause_gap)
    current_time = end_t + 0.12
    print(f"    Segment {item['id']}: {dur:.2f}s ({item['voice']})")

full_speech = np.concatenate(combined_audio)
total_duration = len(full_speech) / sr
print(f"\n    Total Pure Gemini Audio Duration: {total_duration:.2f}s")

# Mix BGM
bgm_source = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\bgm_viral_track.wav"
if not os.path.exists(bgm_source):
    bgm_source = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel\sfx\lofi_bg_track.wav"

bgm_data, bgm_sr = sf.read(bgm_source)
if bgm_sr != sr:
    num_samples = int(len(bgm_data) * sr / bgm_sr)
    bgm_data = scipy.signal.resample(bgm_data, num_samples)
if bgm_data.ndim > 1: bgm_data = bgm_data.mean(axis=1)

target_samples = len(full_speech) + int(1.0 * sr)
if len(bgm_data) < target_samples:
    reps = int(np.ceil(target_samples / len(bgm_data)))
    bgm_data = np.tile(bgm_data, reps)
bgm_data = bgm_data[:target_samples].astype(np.float32)

# Duck BGM to -22 dB
bgm_gain = 10 ** (-22.0 / 20.0)
bgm_data = bgm_data * bgm_gain

# Fade out outro
fade_len = int(1.0 * sr)
bgm_data[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

padded_speech = np.pad(full_speech, (0, target_samples - len(full_speech)))
final_audio_mix = padded_speech + bgm_data

# Peak normalize to -1.0 dBFS
final_audio_mix = (final_audio_mix / np.max(np.abs(final_audio_mix))) * 0.92
master_audio_path = os.path.join(PROJECT_DIR, "final_soundtrack.wav")
sf.write(master_audio_path, final_audio_mix, sr)
print(f"    Master Soundtrack Saved: {master_audio_path}")

# Re-render frames
print("\n>>> [RE-RENDER] Rendering Visual Frames...")
WIDTH, HEIGHT = 1080, 1920
FPS = 24
total_frames = int(total_duration * FPS) + (FPS * 1)

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
sprite_paths = {
    "junior_hands_up": os.path.join(ASSETS_DIR, "clean_junior_hands_up.png"),
    "junior_shrug": os.path.join(ASSETS_DIR, "clean_junior_shrug.png"),
    "senior_pointing_up": os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png"),
    "senior_explaining": os.path.join(ASSETS_DIR, "clean_senior_explaining.png"),
}

loaded_sprites = {k: Image.open(p).convert("RGBA") for k, p in sprite_paths.items() if os.path.exists(p)}

try:
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_speaker = ImageFont.truetype("arialbd.ttf", 44)
    font_sub_hi = ImageFont.truetype("mangal.ttf", 46)
    font_sub_en = ImageFont.truetype("arialbd.ttf", 40)
    font_title = ImageFont.truetype("arialbd.ttf", 52)
except Exception:
    font_badge = font_speaker = font_sub_hi = font_sub_en = font_title = ImageFont.load_default()

FRAMES_DIR = os.path.join(PROJECT_DIR, "rendered_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

bg_base = Image.new("RGBA", (WIDTH, HEIGHT), (12, 16, 26, 255))
bg_draw = ImageDraw.Draw(bg_base)
for y in range(HEIGHT):
    r = int(10 + (30 - 10) * (y / HEIGHT))
    g = int(14 + (20 - 14) * (y / HEIGHT))
    b = int(24 + (45 - 24) * (y / HEIGHT))
    bg_draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

for frame_idx in range(total_frames):
    t = frame_idx / FPS
    active_scene = None
    for sc in scene_timeline:
        if sc["start"] <= t < sc["end"]:
            active_scene = sc
            break
    if not active_scene: active_scene = scene_timeline[-1]

    frame = bg_base.copy()
    draw = ImageDraw.Draw(frame)

    # 1. Header Bar
    draw.rounded_rectangle([(40, 70), (WIDTH - 40, 210)], radius=24, fill=(20, 26, 42, 230), outline=(239, 68, 68, 255), width=3)
    draw.text((WIDTH // 2, 115), "🚨 AI SCAM ALERT: 2026 CYBER THREAT", font=font_title, fill=(248, 113, 113), anchor="mm")
    draw.text((WIDTH // 2, 165), "HOW 3-SECOND AUDIO CAN DRAIN YOUR BANK ACCOUNT", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # 2. Character Sprite
    pose_key = active_scene["item"]["pose"]
    sprite = loaded_sprites.get(pose_key)
    if sprite:
        bounce_y = int(np.sin(t * 4.0) * 8)
        target_w = 780
        target_h = int(sprite.height * (target_w / sprite.width))
        char_resized = sprite.resize((target_w, target_h), Image.Resampling.LANCZOS)
        char_x = (WIDTH - target_w) // 2
        char_y = 520 + bounce_y
        frame.alpha_composite(char_resized, (char_x, char_y))

    # 3. Waveform Call Simulation
    draw.rounded_rectangle([(120, 320), (WIDTH - 120, 480)], radius=20, fill=(15, 23, 42, 220), outline=(56, 189, 248, 220), width=2)
    bar_count, bar_w, spacing = 28, 16, 8
    start_bx = (WIDTH - (bar_count * (bar_w + spacing))) // 2
    for b in range(bar_count):
        bar_h = int(20 + 70 * np.abs(np.sin(t * 8.0 + b * 0.4)))
        bx = start_bx + b * (bar_w + spacing)
        by = 400 - (bar_h // 2)
        bar_color = (239, 68, 68) if b % 2 == 0 else (56, 189, 248)
        draw.rounded_rectangle([(bx, by), (bx + bar_w, by + bar_h)], radius=6, fill=bar_color)

    draw.text((WIDTH // 2, 355), f"CALL DETECTED: {active_scene['item']['badge']}", font=font_badge, fill=(255, 255, 255), anchor="mm")

    # 4. Speaker Badge
    spk_color = (245, 158, 11) if "Aman" in active_scene["item"]["speaker"] else (59, 130, 246)
    draw.rounded_rectangle([(80, 1320), (450, 1400)], radius=18, fill=spk_color)
    draw.text((265, 1360), f"👤 {active_scene['item']['speaker']}", font=font_speaker, fill=(255, 255, 255), anchor="mm")

    # 5. Subtitle Container
    draw.rounded_rectangle([(60, 1420), (WIDTH - 60, 1820)], radius=28, fill=(15, 23, 42, 245), outline=(147, 197, 253, 200), width=3)
    draw.text((WIDTH // 2, 1530), active_scene["item"]["subtitle_hi"], font=font_sub_hi, fill=(253, 224, 71), anchor="mm")
    draw.text((WIDTH // 2, 1630), active_scene["item"]["subtitle_en"], font=font_sub_en, fill=(255, 255, 255), anchor="mm")
    draw.text((WIDTH // 2, 1740), "🔔 SUBSCRIBE & SHARE TO PROTECT OTHERS", font=font_badge, fill=(148, 163, 184), anchor="mm")

    frame.convert("RGB").save(os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.jpg"), quality=90)

print("    Frames rendered. Compiling MP4...")
import imageio_ffmpeg
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
final_mp4 = os.path.join(PROJECT_DIR, "ai_voice_scam_master_reel.mp4")

cmd = [
    ffmpeg_exe, "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.jpg"),
    "-i", master_audio_path,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-preset", "veryfast",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_mp4
]
subprocess.run(cmd, check=True)

import shutil
artifact_mp4 = os.path.join(ARTIFACT_DIR, "ai_voice_scam_master_reel.mp4")
shutil.copy2(final_mp4, artifact_mp4)
print(f">>> [SUCCESS] Pure Gemini Video Exported: {artifact_mp4} ({os.path.getsize(artifact_mp4)/(1024*1024):.2f} MB)")
