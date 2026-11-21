import os
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf
import numpy as np

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
PROJ_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master"
ASSETS_DIR = os.path.join(PROJ_DIR, "ref_assets")
AUDIO_DIR = os.path.join(PROJ_DIR, "viral_en_audio")
SNAP_DIR = os.path.join(PROJ_DIR, "snapshots_authentic")
os.makedirs(SNAP_DIR, exist_ok=True)
OUTPUT_MP4 = os.path.join(PROJ_DIR, "deepseek_authentic_cartoon_master.mp4")

TRACKS = [
    {
        "id": "line1_j",
        "file": "line1_j.wav",
        "speaker": "junior",
        "bg_color": (244, 197, 66, 255), # Warm Yellow
        "j_pose": "clean_junior_pointing.png",
        "s_pose": "clean_senior_clasped.png",
        "sub": "Junior: 'Wait! Should I cancel my $20 ChatGPT sub? DeepSeek is literally free!'"
    },
    {
        "id": "line2_s",
        "file": "line2_s.wav",
        "speaker": "senior",
        "bg_color": (141, 197, 232, 255), # Sky Blue
        "j_pose": "clean_junior_pointing.png",
        "s_pose": "clean_senior_pointing_up.png",
        "sub": "Senior: 'Hold on! In coding, DeepSeek is a beast, but know these 3 facts first!'"
    },
    {
        "id": "line3_s",
        "file": "line3_s.wav",
        "speaker": "senior",
        "bg_color": (141, 197, 232, 255), # Sky Blue
        "j_pose": "clean_junior_shrug.png",
        "s_pose": "clean_senior_pointing_up.png",
        "sub": "Senior: '1. Reasoning Power: In Python & math, DeepSeek R1 destroys GPT-4o!'"
    },
    {
        "id": "line4_s",
        "file": "line4_s.wav",
        "speaker": "senior",
        "bg_color": (168, 216, 185, 255), # Mint Green
        "j_pose": "clean_junior_shrug.png",
        "s_pose": "clean_senior_pointing_up.png",
        "sub": "Senior: '2. Privacy Warning: Never put company code in cloud! Run locally!'"
    },
    {
        "id": "line5_j",
        "file": "line5_j.wav",
        "speaker": "junior",
        "bg_color": (243, 167, 165, 255), # Coral Peach
        "j_pose": "clean_junior_shrug.png",
        "s_pose": "clean_senior_clasped.png",
        "sub": "Junior: 'Wait! We can run the entire model on our own laptop without internet?'"
    },
    {
        "id": "line6_s",
        "file": "line6_s.wav",
        "speaker": "senior",
        "bg_color": (243, 167, 165, 255), # Coral Peach
        "j_pose": "clean_junior_pointing.png",
        "s_pose": "clean_senior_pointing_up.png",
        "sub": "Senior: 'Exactly! 100% Free, zero leaks! Comment LOCAL for full setup guide!'"
    }
]

# Load audio & build timeline
def load_audio_timeline():
    audio_data = {}
    gap = 0.08
    cur_t = 0.3
    schedule = {}
    
    for t in TRACKS:
        fp = os.path.join(AUDIO_DIR, t["file"])
        data, sr = sf.read(fp)
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        dur = len(data) / sr
        
        audio_data[t["id"]] = {"data": data, "sr": sr, "dur": dur}
        schedule[t["id"]] = {
            "start": cur_t,
            "end": cur_t + dur,
            "dur": dur,
            "speaker": t["speaker"],
            "sub": t["sub"],
            "bg_color": t["bg_color"],
            "j_pose": t["j_pose"],
            "s_pose": t["s_pose"],
            "file": t["file"]
        }
        cur_t += dur + gap
        
    total_dur = cur_t + 0.8
    return audio_data, schedule, total_dur

# Calculate speech RMS amplitude
def get_speech_envelope(t, sid, schedule, audio_data):
    sinfo = schedule[sid]
    if not (sinfo["start"] <= t <= sinfo["end"]):
        return 0.0
    
    offset_s = t - sinfo["start"]
    data = audio_data[sid]["data"]
    sr = audio_data[sid]["sr"]
    center_idx = int(offset_s * sr)
    
    win = int(0.040 * sr)
    start_idx = max(0, center_idx - win // 2)
    end_idx = min(len(data), center_idx + win // 2)
    
    if start_idx >= end_idx:
        return 0.0
    
    chunk = data[start_idx:end_idx]
    rms = np.sqrt(np.mean(chunk**2))
    return float(rms)

# Load Sprites once
SPRITES = {
    "clean_junior_pointing.png": Image.open(os.path.join(ASSETS_DIR, "clean_junior_pointing.png")).convert("RGBA"),
    "clean_junior_shrug.png": Image.open(os.path.join(ASSETS_DIR, "clean_junior_shrug.png")).convert("RGBA"),
    "clean_senior_pointing_up.png": Image.open(os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png")).convert("RGBA"),
    "clean_senior_clasped.png": Image.open(os.path.join(ASSETS_DIR, "clean_senior_clasped.png")).convert("RGBA")
}

# Typography
FONT_MAIN_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
FONT_CARD_DESC = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
FONT_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)

def draw_frame(f_idx, fps, schedule, total_duration, audio_data):
    t = f_idx / fps
    w, h = 1080, 1920
    
    # 1. Determine active scene and background color
    current_bg = (244, 197, 66, 255) # default yellow
    current_sub = ""
    junior_speaking = False
    senior_speaking = False
    junior_rms = 0.0
    senior_rms = 0.0
    active_sid = "line1_j"
    
    for sid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"]:
            active_sid = sid
            current_bg = sinfo["bg_color"]
            current_sub = sinfo["sub"]
            if sinfo["speaker"] == "junior":
                junior_speaking = True
                junior_rms = get_speech_envelope(t, sid, schedule, audio_data)
            else:
                senior_speaking = True
                senior_rms = get_speech_envelope(t, sid, schedule, audio_data)
            break
        elif t < sinfo["start"]:
            break
        else:
            active_sid = sid
            current_bg = sinfo["bg_color"]
            
    # Draw Background Canvas
    im = Image.new("RGBA", (w, h), current_bg)
    draw = ImageDraw.Draw(im)
    
    # Studio Floor Line
    draw.line([0, 1830, w, 1830], fill=(50, 40, 30, 255), width=4)
    
    # ==========================================
    # 2. WHITEBOARD (Ref_04 Exact Vector Style)
    # ==========================================
    # Outer Frame with Bezel
    draw.rounded_rectangle([32, 78, 1048, 1082], radius=30, fill=(150, 165, 180, 160)) # shadow
    draw.rounded_rectangle([30, 75, 1050, 1075], radius=28, fill=(255, 255, 255, 255), outline=(30, 41, 59, 255), width=8)
    draw.rounded_rectangle([48, 92, 1032, 1058], radius=18, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=3)
    
    # Marker Tray & Dry-Erase Markers
    draw.rounded_rectangle([200, 1060, 880, 1078], radius=6, fill=(100, 116, 139, 255), outline=(15, 23, 42, 255), width=3)
    draw.rounded_rectangle([280, 1052, 370, 1066], radius=4, fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=2)
    draw.rounded_rectangle([410, 1052, 500, 1066], radius=4, fill=(15, 23, 42, 255), outline=(15, 23, 42, 255), width=2)
    draw.rounded_rectangle([540, 1052, 630, 1066], radius=4, fill=(37, 99, 235, 255), outline=(15, 23, 42, 255), width=2)
    
    # Header Title Inside Whiteboard
    draw.rounded_rectangle([80, 130, 1000, 220], radius=16, fill=(15, 23, 42, 255))
    draw.text((540, 175), "DEEPSEEK R1 VS CHATGPT-4o ⚡", font=FONT_MAIN_TITLE, fill=(255, 255, 255, 255), anchor="mm")
    
    # Hook Card (ChatGPT Plus $20/month)
    draw.rounded_rectangle([100, 250, 980, 360], radius=18, fill=(248, 250, 252, 255), outline=(30, 41, 59, 255), width=4)
    draw.text((540, 305), "CHATGPT PLUS: $20/MONTH SUBSCRIPTION 💸", font=FONT_CARD_TITLE, fill=(30, 41, 59, 255), anchor="mm")
    
    # Strikethrough Animation
    t_l2_start = schedule["line2_s"]["start"]
    if t >= t_l2_start + 0.4:
        strike_prog = min(1.0, (t - (t_l2_start + 0.4)) / 0.4)
        start_x = 130
        end_x = start_x + int(strike_prog * 630)
        draw.line([start_x, 305, end_x, 305], fill=(239, 68, 68, 255), width=10)
        if strike_prog >= 0.7:
            draw.rounded_rectangle([750, 265, 960, 345], radius=14, fill=(239, 68, 68, 255), outline=(153, 27, 27, 255), width=3)
            draw.text((855, 305), "CANCEL? ❌", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255), anchor="mm")

    # Point 1 Reveal: Reasoning & Complex Code
    t_l3_start = schedule["line3_s"]["start"]
    if t >= t_l3_start + 0.2:
        draw.rounded_rectangle([100, 390, 980, 520], radius=18, fill=(238, 242, 255, 255), outline=(79, 70, 229, 255), width=3)
        draw.rounded_rectangle([125, 415, 205, 495], radius=16, fill=(79, 70, 229, 255))
        draw.text((165, 455), "1", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((235, 435), "REASONING & COMPLEX CODE 🧠", font=FONT_CARD_TITLE, fill=(49, 46, 129, 255), anchor="lm")
        draw.text((235, 482), "DeepSeek R1 destroys GPT-4o in Python & Math! (100% Free)", font=FONT_CARD_DESC, fill=(67, 56, 202, 255), anchor="lm")
        draw.rounded_rectangle([780, 420, 955, 455], radius=8, fill=(30, 27, 75, 255))
        draw.text((867, 438), "BENCHMARK 🏆", font=FONT_TAG, fill=(165, 180, 252, 255), anchor="mm")

    # Point 2 Reveal: Privacy Warning
    t_l4_start = schedule["line4_s"]["start"]
    if t >= t_l4_start + 0.2:
        draw.rounded_rectangle([100, 550, 980, 680], radius=18, fill=(254, 242, 242, 255), outline=(239, 68, 68, 255), width=3)
        draw.rounded_rectangle([125, 575, 205, 655], radius=16, fill=(239, 68, 68, 255))
        draw.text((165, 615), "2", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((235, 595), "PRIVACY & DATA LEAK WARNING ⚠️", font=FONT_CARD_TITLE, fill=(153, 27, 27, 255), anchor="lm")
        draw.text((235, 642), "Never put company code in cloud! Run offline on laptop!", font=FONT_CARD_DESC, fill=(185, 28, 28, 255), anchor="lm")
        draw.rounded_rectangle([780, 580, 955, 615], radius=8, fill=(153, 27, 27, 255))
        draw.text((867, 598), "CLOUD = RISKY", font=FONT_TAG, fill=(254, 202, 202, 255), anchor="mm")

    # Point 3 Reveal: 100% Offline Local Model
    t_l5_start = schedule["line5_j"]["start"]
    if t >= t_l5_start:
        draw.rounded_rectangle([100, 710, 980, 840], radius=18, fill=(240, 253, 244, 255), outline=(34, 197, 94, 255), width=3)
        draw.rounded_rectangle([125, 735, 205, 815], radius=16, fill=(34, 197, 94, 255))
        draw.text((165, 775), "3", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((235, 755), "100% OFFLINE LAPTOP RUN 💻", font=FONT_CARD_TITLE, fill=(20, 83, 45, 255), anchor="lm")
        draw.text((235, 802), "Terminal: 'ollama run deepseek-r1:7b'", font=FONT_CARD_DESC, fill=(22, 101, 52, 255), anchor="lm")
        draw.rounded_rectangle([780, 740, 955, 775], radius=8, fill=(20, 83, 45, 255))
        draw.text((867, 758), "₹0 FOREVER ✅", font=FONT_TAG, fill=(187, 247, 208, 255), anchor="mm")

    # Call-to-Action Card
    t_l6_start = schedule["line6_s"]["start"]
    if t >= t_l6_start + 0.3:
        draw.rounded_rectangle([100, 865, 980, 1030], radius=20, fill=(15, 23, 42, 255), outline=(56, 189, 248, 255), width=4)
        draw.text((540, 915), "🚀 WANT TO RUN DEEPSEEK ON YOUR LAPTOP?", font=FONT_CARD_TITLE, fill=(56, 189, 248, 255), anchor="mm")
        draw.text((540, 980), "COMMENT 'LOCAL' FOR FULL STEP-BY-STEP SETUP! 📩", font=FONT_MAIN_TITLE, fill=(255, 255, 255, 255), anchor="mm")

    # ==========================================
    # 3. COMPOSITE REAL CHARACTER SPRITES
    # ==========================================
    sinfo_act = schedule[active_sid]
    j_sprite = SPRITES[sinfo_act["j_pose"]]
    s_sprite = SPRITES[sinfo_act["s_pose"]]
    
    # Slight micro-bob with speech
    j_bob = int(junior_rms * 18)
    s_bob = int(senior_rms * 18)
    
    # Place Junior at X=110, Y=1010 - j_bob
    im.alpha_composite(j_sprite, (110, 1010 - j_bob))
    
    # Place Senior at X=530, Y=1010 - s_bob
    im.alpha_composite(s_sprite, (530, 1010 - s_bob))

    # ==========================================
    # 4. REAL AUDIO WAVEFORM LIP-SYNC MOUTHS
    # ==========================================
    # Junior Mouth position in full canvas: CX ~ 265, CY ~ 1345 - j_bob
    if junior_speaking and junior_rms >= 0.018:
        j_mx, j_my = 265, 1345 - j_bob
        open_h = min(22, int((junior_rms - 0.018) * 160) + 4)
        draw.ellipse([j_mx - 22, j_my - open_h, j_mx + 22, j_my + open_h], fill=(15, 23, 42, 255))
        if open_h > 8:
            draw.chord([j_mx - 16, j_my - open_h + 2, j_mx + 16, j_my - 2], 180, 360, fill=(255, 255, 255, 255)) # teeth
            draw.chord([j_mx - 14, j_my + 2, j_mx + 14, j_my + open_h - 2], 0, 180, fill=(244, 114, 182, 255)) # tongue

    # Senior Mouth position in full canvas: CX ~ 685, CY ~ 1325 - s_bob
    if senior_speaking and senior_rms >= 0.018:
        s_mx, s_my = 685, 1325 - s_bob
        open_h = min(22, int((senior_rms - 0.018) * 160) + 4)
        draw.ellipse([s_mx - 20, s_my - open_h, s_mx + 20, s_my + open_h], fill=(15, 23, 42, 255))
        if open_h > 8:
            draw.chord([s_mx - 14, s_my - open_h + 2, s_mx + 14, s_my - 2], 180, 360, fill=(255, 255, 255, 255))
            draw.chord([s_mx - 12, s_my + 2, s_mx + 12, s_my + open_h - 2], 0, 180, fill=(244, 114, 182, 255))

    # ==========================================
    # 5. SUBTITLES (Viral Ref_04 Style)
    # ==========================================
    if current_sub:
        draw.text((540, 1860), current_sub, font=FONT_CAPTION, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(15, 23, 42, 255), anchor="mm")
        
    return im.convert("RGB")

def render_video_stream(schedule, total_dur, audio_data):
    fps = 30
    total_f = int(total_dur * fps)
    print(f"--- [1/3] Streaming {total_f} Frames @ {fps}fps to FFmpeg ({total_dur:.2f}s) ---")
    raw_video = os.path.join(PROJ_DIR, "authentic_video_track.mp4")
    
    # Save Keyframe Snapshots for verification
    test_frames = [
        (int(2.0 * fps), "snap_1_hook.jpg"),
        (int(schedule["line3_s"]["start"] * fps + 30), "snap_2_point1.jpg"),
        (int(schedule["line4_s"]["start"] * fps + 30), "snap_3_point2.jpg"),
        (int(schedule["line6_s"]["start"] * fps + 30), "snap_4_cta.jpg")
    ]
    for fi, sname in test_frames:
        if fi < total_f:
            sim = draw_frame(fi, fps, schedule, total_dur, audio_data)
            sim.save(os.path.join(SNAP_DIR, sname), quality=94)
            print(f"Saved snapshot {sname} at frame {fi}")
    
    cmd_ffmpeg = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "22",
        raw_video
    ]
    
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f_idx in range(total_f):
        im = draw_frame(f_idx, fps, schedule, total_dur, audio_data)
        proc.stdin.write(im.tobytes())
        if f_idx % 200 == 0:
            print(f"Rendered Frame {f_idx}/{total_f} ({f_idx/total_f*100:.1f}%)")
            
    proc.stdin.close()
    proc.wait()
    print("Video stream rendered successfully:", raw_video)
    return raw_video

def mix_audio(schedule, total_dur):
    print("--- [2/3] Multi-Track Broadcast Audio Mixing ---")
    l1 = os.path.join(AUDIO_DIR, "line1_j.wav")
    l2 = os.path.join(AUDIO_DIR, "line2_s.wav")
    l3 = os.path.join(AUDIO_DIR, "line3_s.wav")
    l4 = os.path.join(AUDIO_DIR, "line4_s.wav")
    l5 = os.path.join(AUDIO_DIR, "line5_j.wav")
    l6 = os.path.join(AUDIO_DIR, "line6_s.wav")
    
    sfx_pop = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\sfx_pop.wav"
    sfx_scratch = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test\sfx_scratch.wav"
    bgm_path = os.path.join(PROJ_DIR, "bgm_authentic_track.wav")
    
    # Warm lofi tech groove
    cmd_bgm = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"sine=f=220.00:d={total_dur},volume=0.05",
        "-f", "lavfi",
        "-i", f"sine=f=277.18:d={total_dur},volume=0.035",
        "-f", "lavfi",
        "-i", f"sine=f=329.63:d={total_dur},volume=0.035",
        "-f", "lavfi",
        "-i", f"anoisesrc=d={total_dur}:c=brown:r=44100,lowpass=f=200,volume=0.08",
        "-filter_complex", f"[0:a][1:a][2:a][3:a]amix=inputs=4[m];[m]afade=t=out:st={total_dur-1.5:.2f}:d=1.5[out]",
        "-map", "[out]", bgm_path
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    d1 = int(schedule["line1_j"]["start"] * 1000)
    d2 = int(schedule["line2_s"]["start"] * 1000)
    d3 = int(schedule["line3_s"]["start"] * 1000)
    d4 = int(schedule["line4_s"]["start"] * 1000)
    d5 = int(schedule["line5_j"]["start"] * 1000)
    d6 = int(schedule["line6_s"]["start"] * 1000)
    
    d_scratch = int((schedule["line2_s"]["start"] + 0.4) * 1000)
    d_p1 = int((schedule["line3_s"]["start"] + 0.2) * 1000)
    d_p2 = int((schedule["line4_s"]["start"] + 0.2) * 1000)
    d_p3 = int((schedule["line5_j"]["start"]) * 1000)
    
    mix_filter = (
        f"[0:a]adelay={d1}|{d1},volume=1.4[a0];"
        f"[1:a]adelay={d2}|{d2},volume=1.4[a1];"
        f"[2:a]adelay={d3}|{d3},volume=1.4[a2];"
        f"[3:a]adelay={d4}|{d4},volume=1.4[a3];"
        f"[4:a]adelay={d5}|{d5},volume=1.4[a4];"
        f"[5:a]adelay={d6}|{d6},volume=1.4[a5];"
        f"[6:a]volume=0.20[a6];"
        f"[7:a]adelay={d_scratch}|{d_scratch},volume=0.45[a7];"
        f"[8:a]adelay={d_p1}|{d_p1},volume=0.55[a8];"
        f"[9:a]adelay={d_p2}|{d_p2},volume=0.55[a9];"
        f"[10:a]adelay={d_p3}|{d_p3},volume=0.55[a10];"
        f"[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10]amix=inputs=11:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1.0[final_audio]"
    )
    
    final_audio = os.path.join(PROJ_DIR, "authentic_final_audio.wav")
    cmd_mix = [
        FFMPEG, "-y",
        "-i", l1,
        "-i", l2,
        "-i", l3,
        "-i", l4,
        "-i", l5,
        "-i", l6,
        "-i", bgm_path,
        "-i", sfx_scratch,
        "-i", sfx_pop,
        "-i", sfx_pop,
        "-i", sfx_pop,
        "-filter_complex", mix_filter,
        "-map", "[final_audio]",
        "-t", str(total_dur),
        final_audio
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("Master audio mix compiled:", final_audio)
    return final_audio

def compile_final_mp4(v_track, a_track, total_dur):
    print("--- [3/3] Assembling Final MP4 ---")
    cmd = [
        FFMPEG, "-y",
        "-i", v_track,
        "-i", a_track,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_dur),
        OUTPUT_MP4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n🎉 AUTHENTIC 2D CARTOON MASTER READY: {OUTPUT_MP4}")
    print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")

def main():
    audio_data, schedule, total_dur = load_audio_timeline()
    print(f"Total Video Planned Duration: {total_dur:.2f}s")
    v_track = render_video_stream(schedule, total_dur, audio_data)
    a_track = mix_audio(schedule, total_dur)
    compile_final_mp4(v_track, a_track, total_dur)

if __name__ == "__main__":
    main()
