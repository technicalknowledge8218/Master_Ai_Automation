import os
import sys
import json
import base64
import wave
import time
import urllib.request
import urllib.error
import numpy as np
import soundfile as sf
import scipy.signal
from PIL import Image, ImageDraw, ImageFont

# Set UTF-8 encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PROJECT_DIR = r"F:\Master AI\00_CORE_SYSTEM\engine\video_production\ai_voice_scam_reel"
os.makedirs(PROJECT_DIR, exist_ok=True)
ARTIFACT_DIR = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash-preview-tts"

print(">>> [STAGE 1] Generating Story Dialogue Audio with Gemini TTS...")

dialogue_script = [
    {
        "id": "scene_1_aman_hook",
        "speaker": "Aman (Victim)",
        "voice": "Puck",
        "badge": "🚨 EMERGENCY CALL",
        "pose": "junior_hands_up",
        "text": "भाई, कल मेरे दोस्त की हूबहू आवाज़ में कॉल आया कि वो इमरजेंसी में है, और मैंने तुरंत 50 हज़ार ट्रांसफर कर दिए... लेकिन बाद में पता चला उसने कॉल किया ही नहीं!",
        "subtitle_hi": "कल मेरे दोस्त की हूबहू आवाज़ में कॉल आया...",
        "subtitle_en": "Got a call in my friend's exact voice... and lost ₹50,000!"
    },
    {
        "id": "scene_2_kabir_reveal",
        "speaker": "Kabir (Cyber Expert)",
        "voice": "Charon",
        "badge": "⚠️ AI VOICE SCAM EXPOSED",
        "pose": "senior_pointing_up",
        "text": "अमन, तुम 'AI वॉइस क्लोनिंग स्कैम' का शिकार हो चुके हो! आज के AI टूल्स सिर्फ तुम्हारी 3 सेकंड की इंस्टाग्राम रील या वॉइस नोट से तुम्हारी पूरी आवाज़ हूबहू कॉपी कर लेते हैं!",
        "subtitle_hi": "AI सिर्फ 3 सेकंड के ऑडियो से तुम्हारी आवाज़ कॉपी कर लेता है!",
        "subtitle_en": "AI clones your exact voice from just 3 seconds of audio!"
    },
    {
        "id": "scene_3_aman_question",
        "speaker": "Aman (Victim)",
        "voice": "Puck",
        "badge": "❓ HOW TO IDENTIFY?",
        "pose": "junior_shrug",
        "text": "तो फिर असली और नकली आवाज़ में फर्क कैसे पहचानें Kabir bhai? कोई तरीका है बचने का?",
        "subtitle_hi": "तो फिर असली और नकली आवाज़ में फर्क कैसे पहचानें?",
        "subtitle_en": "How to tell real voice from AI voice clone?"
    },
    {
        "id": "scene_4_kabir_solution",
        "speaker": "Kabir (Cyber Expert)",
        "voice": "Charon",
        "badge": "🛡️ BULLETPROOF SAFETY RULE",
        "pose": "senior_explaining",
        "text": "सिर्फ एक नियम बना लो: अपनी फैमिली के साथ एक सीक्रेट 'सेफ्टी कोडवर्ड' तय करो! जब भी कोई इमरजेंसी में पैसे मांगे, वो कोडवर्ड पूछो। स्कैमर कभी वो कोडवर्ड नहीं बता पाएगा! अपने परिवार को बचाने के लिए ये रील तुरंत शेयर करो!",
        "subtitle_hi": "फैमिली के साथ एक सीक्रेट 'सेफ्टी कोडवर्ड' तय करो!",
        "subtitle_en": "Set a Secret Safety Codeword with your family today!"
    }
]

generated_segments = []

for idx, item in enumerate(dialogue_script):
    wav_path = os.path.join(PROJECT_DIR, f"{item['id']}.wav")
    print(f"    Synthesizing Turn {idx+1}: {item['speaker']} ({item['voice']})...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": item["text"]}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": item["voice"]
                    }
                }
            }
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    max_retries = 4
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode())
                parts = res["candidates"][0]["content"]["parts"]
                for p in parts:
                    if "inlineData" in p:
                        raw_pcm = base64.b64decode(p["inlineData"]["data"])
                        with wave.open(wav_path, "wb") as wf:
                            wf.setnchannels(1)
                            wf.setsampwidth(2)
                            wf.setframerate(24000)
                            wf.writeframes(raw_pcm)
                break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait_sec = 8 * (attempt + 1)
                print(f"        [Rate Limit 429] Waiting {wait_sec}s for quota window...")
                time.sleep(wait_sec)
            else:
                print(f"        [Fallback to Edge Neural TTS] for {item['speaker']}...")
                # Fallback to Edge-TTS if Gemini quota is cooling down
                import asyncio, edge_tts
                fallback_voice = "hi-IN-MadhurNeural" if "Aman" in item["speaker"] else "hi-IN-MadhurNeural"
                pitch = "+2Hz" if "Aman" in item["speaker"] else "-3Hz"
                async def _fb():
                    tmp = wav_path.replace(".wav", "_tmp.mp3")
                    comm = edge_tts.Communicate(item["text"], fallback_voice, pitch=pitch)
                    await comm.save(tmp)
                    d, sr_fb = sf.read(tmp)
                    sf.write(wav_path, d, 24000)
                    if os.path.exists(tmp): os.remove(tmp)
                asyncio.run(_fb())
                break

    # Clean & Trim pause
    data, sr = sf.read(wav_path)
    threshold = 0.015 * np.max(np.abs(data)) if np.max(np.abs(data)) > 0 else 0.015
    non_silent = np.where(np.abs(data) > threshold)[0]
    if len(non_silent) > 0:
        data = data[max(0, non_silent[0]-int(0.02*sr)):min(len(data), non_silent[-1]+int(0.04*sr))]
    sf.write(wav_path, data, sr)
    dur = len(data) / sr
    print(f"    Turn {idx+1} complete: {dur:.2f}s | Saved: {wav_path}")
    generated_segments.append((item, wav_path, dur))

# -------------------------------------------------------------
# STAGE 2: Master Audio Stitching & BGM Ducking
# -------------------------------------------------------------
print("\n>>> [STAGE 2] Assembling Master Dialogue & BGM Ducking...")
sr = 24000
pause_gap = np.zeros(int(0.12 * sr), dtype=np.float32) # 120ms human pause
scene_timeline = []

combined_audio = []
current_time = 0.0

for item, wav_path, dur in generated_segments:
    data, _ = sf.read(wav_path)
    if data.ndim > 1: data = data.mean(axis=1)
    data = data.astype(np.float32)
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

full_speech = np.concatenate(combined_audio)
total_duration = len(full_speech) / sr
print(f"    Total Dialogue Track Duration: {total_duration:.2f}s")

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

# -------------------------------------------------------------
# STAGE 3: Video Frame Rendering (1080x1920, 24 FPS)
# -------------------------------------------------------------
print("\n>>> [STAGE 3] Rendering Visual Frames & Typography (1080x1920)...")
WIDTH = 1080
HEIGHT = 1920
FPS = 24
total_frames = int(total_duration * FPS) + (FPS * 1) # add 1s buffer

# Load Character Sprites
ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
sprite_paths = {
    "junior_hands_up": os.path.join(ASSETS_DIR, "clean_junior_hands_up.png"),
    "junior_shrug": os.path.join(ASSETS_DIR, "clean_junior_shrug.png"),
    "senior_pointing_up": os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png"),
    "senior_explaining": os.path.join(ASSETS_DIR, "clean_senior_explaining.png"),
    "whiteboard": os.path.join(ASSETS_DIR, "clean_whiteboard_empty.png")
}

loaded_sprites = {}
for k, path in sprite_paths.items():
    if os.path.exists(path):
        loaded_sprites[k] = Image.open(path).convert("RGBA")
    else:
        print(f"Warning: Missing sprite {path}")

# Fonts
try:
    font_badge = ImageFont.truetype("arialbd.ttf", 36)
    font_speaker = ImageFont.truetype("arialbd.ttf", 44)
    font_sub_hi = ImageFont.truetype("mangal.ttf", 46)
    font_sub_en = ImageFont.truetype("arialbd.ttf", 40)
    font_title = ImageFont.truetype("arialbd.ttf", 52)
except Exception:
    font_badge = ImageFont.load_default()
    font_speaker = ImageFont.load_default()
    font_sub_hi = ImageFont.load_default()
    font_sub_en = ImageFont.load_default()
    font_title = ImageFont.load_default()

FRAMES_DIR = os.path.join(PROJECT_DIR, "rendered_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

# Generate background gradient image once
bg_base = Image.new("RGBA", (WIDTH, HEIGHT), (12, 16, 26, 255))
bg_draw = ImageDraw.Draw(bg_base)
for y in range(HEIGHT):
    r = int(10 + (30 - 10) * (y / HEIGHT))
    g = int(14 + (20 - 14) * (y / HEIGHT))
    b = int(24 + (45 - 24) * (y / HEIGHT))
    bg_draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

print(f"    Rendering {total_frames} frames at {FPS} FPS...")
t_start = time.time()

for frame_idx in range(total_frames):
    t = frame_idx / FPS

    # Find active scene
    active_scene = None
    for sc in scene_timeline:
        if sc["start"] <= t < sc["end"]:
            active_scene = sc
            break
    if not active_scene:
        active_scene = scene_timeline[-1]

    frame = bg_base.copy()
    draw = ImageDraw.Draw(frame)

    # 1. Header Bar (Channel / Topic Badge)
    header_box = [(40, 70), (WIDTH - 40, 210)]
    draw.rounded_rectangle(header_box, radius=24, fill=(20, 26, 42, 230), outline=(239, 68, 68, 255), width=3)
    draw.text((WIDTH // 2, 115), "🚨 AI SCAM ALERT: 2026 CYBER THREAT", font=font_title, fill=(248, 113, 113), anchor="mm")
    draw.text((WIDTH // 2, 165), "HOW 3-SECOND AUDIO CAN DRAIN YOUR BANK ACCOUNT", font=font_badge, fill=(226, 232, 240), anchor="mm")

    # 2. Character Rendering with subtle breathing/sway animation
    pose_key = active_scene["item"]["pose"]
    sprite = loaded_sprites.get(pose_key)
    if sprite:
        # Subtle breathing bounce
        bounce_y = int(np.sin(t * 4.0) * 8)
        
        # Scale sprite to fill center-bottom
        target_w = 780
        target_h = int(sprite.height * (target_w / sprite.width))
        char_resized = sprite.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Position in center
        char_x = (WIDTH - target_w) // 2
        char_y = 520 + bounce_y
        frame.alpha_composite(char_resized, (char_x, char_y))

    # 3. Dynamic Visual Waveform / Call Simulation in center
    wave_box = [(120, 320), (WIDTH - 120, 480)]
    draw.rounded_rectangle(wave_box, radius=20, fill=(15, 23, 42, 220), outline=(56, 189, 248, 220), width=2)
    
    # Draw animated audio bars
    bar_count = 28
    bar_w = 16
    spacing = 8
    start_bx = (WIDTH - (bar_count * (bar_w + spacing))) // 2
    for b in range(bar_count):
        bar_h = int(20 + 70 * np.abs(np.sin(t * 8.0 + b * 0.4)))
        bx = start_bx + b * (bar_w + spacing)
        by = 400 - (bar_h // 2)
        bar_color = (239, 68, 68) if b % 2 == 0 else (56, 189, 248)
        draw.rounded_rectangle([(bx, by), (bx + bar_w, by + bar_h)], radius=6, fill=bar_color)

    draw.text((WIDTH // 2, 355), f"CALL DETECTED: {active_scene['item']['badge']}", font=font_badge, fill=(255, 255, 255), anchor="mm")

    # 4. Speaker Identity Badge
    spk_color = (245, 158, 11) if "Aman" in active_scene["item"]["speaker"] else (59, 130, 246)
    draw.rounded_rectangle([(80, 1320), (450, 1400)], radius=18, fill=spk_color)
    draw.text((265, 1360), f"👤 {active_scene['item']['speaker']}", font=font_speaker, fill=(255, 255, 255), anchor="mm")

    # 5. Kinetic Subtitle Container (Bottom Card - 0% Overflow Guarantee)
    sub_box = [(60, 1420), (WIDTH - 60, 1820)]
    draw.rounded_rectangle(sub_box, radius=28, fill=(15, 23, 42, 245), outline=(147, 197, 253, 200), width=3)
    
    # Subtitle Hindi (Big, Bold, Yellow)
    draw.text((WIDTH // 2, 1530), active_scene["item"]["subtitle_hi"], font=font_sub_hi, fill=(253, 224, 71), anchor="mm")
    
    # Subtitle English / Hinglish (Clean White)
    draw.text((WIDTH // 2, 1630), active_scene["item"]["subtitle_en"], font=font_sub_en, fill=(255, 255, 255), anchor="mm")

    # CTA Footer Indicator
    draw.text((WIDTH // 2, 1740), "🔔 SUBSCRIBE & SHARE TO PROTECT OTHERS", font=font_badge, fill=(148, 163, 184), anchor="mm")

    # Save frame image
    frame_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.jpg")
    frame.convert("RGB").save(frame_path, quality=90)

    if frame_idx % 120 == 0:
        pct = (frame_idx / total_frames) * 100
        print(f"    Progress: {frame_idx}/{total_frames} frames ({pct:.1f}%)")

print(f"    Frame rendering complete in {time.time() - t_start:.1f}s!")

# -------------------------------------------------------------
# STAGE 4: Final Video Compilation via FFmpeg
# -------------------------------------------------------------
print("\n>>> [STAGE 4] Encoding Final High-Resolution MP4 (1080x1920)...")
final_mp4 = os.path.join(PROJECT_DIR, "ai_voice_scam_master_reel.mp4")

import subprocess
try:
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    ffmpeg_exe = "ffmpeg"

print(f"    Using FFmpeg executable: {ffmpeg_exe}")

ffmpeg_cmd = [
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

import subprocess
subprocess.run(ffmpeg_cmd, check=True)

# Mirror to Artifact Directory
import shutil
artifact_mp4 = os.path.join(ARTIFACT_DIR, "ai_voice_scam_master_reel.mp4")
shutil.copy2(final_mp4, artifact_mp4)

print(f"\n>>> [COMPLETE] Video Successfully Exported!")
print(f"    - Output File: {final_mp4}")
print(f"    - Artifact Mirror: {artifact_mp4}")
print(f"    - File Size: {os.path.getsize(artifact_mp4) / (1024*1024):.2f} MB")
