import os
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
WORK_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\explainer_reel_test"
AUDIO_DIR = os.path.join(WORK_DIR, "prabhat_swara_test")
OUTPUT_MP4 = os.path.join(WORK_DIR, "vibe_coding_swara_prabhat_master.mp4")

TRACKS = [
    {"id": "line1_j", "file": "l1_junior_swara.wav", "speaker": "junior", "sub": "Junior: 'Bhaiya! AI se sirf 10 min mein app bana diya! Dev kyu chahiye?'"},
    {"id": "line2_s", "file": "l2_senior_prabhat.wav", "speaker": "senior", "sub": "Senior: 'Wait bro! AI code generates fast, but 3 mistakes crash your app!'"},
    {"id": "line3_s", "file": "l3_senior_prabhat.wav", "speaker": "senior", "sub": "Senior: 'First mistake: Hardcoded API keys! Leak straight to public GitHub!'"},
    {"id": "line4_s", "file": "l4_senior_prabhat.wav", "speaker": "senior", "sub": "Senior: 'Second: Zero error handling! One network failure and screen blank!'"},
    {"id": "line5_j", "file": "l5_junior_swara.wav", "speaker": "junior", "sub": "Junior: 'Arre baap re! Matlab testing humein hi karni padegi?'"},
    {"id": "line6_s", "file": "l6_senior_prabhat.wav", "speaker": "senior", "sub": "Senior: 'AI is your junior coder, YOU are the senior architect! Follow for tips!'"}
]

def get_durations():
    durs = {}
    for t in TRACKS:
        fp = os.path.join(AUDIO_DIR, t["file"])
        data, sr = sf.read(fp)
        d = len(data) / sr
        durs[t["id"]] = d
        print(f"Loaded {t['file']}: {d:.2f}s")
    return durs

def build_timeline(durs):
    gap = 0.08  # Micro-pause
    cur_t = 0.3
    schedule = {}
    for t in TRACKS:
        sid = t["id"]
        d = durs[sid]
        schedule[sid] = {
            "start": cur_t,
            "end": cur_t + d,
            "dur": d,
            "speaker": t["speaker"],
            "sub": t["sub"],
            "file": t["file"]
        }
        cur_t += d + gap
    total_dur = cur_t + 0.8
    return schedule, total_dur

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 36)
FONT_CARD_DESC = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 30)

def draw_frame(f_idx, fps, schedule, total_duration):
    t = f_idx / fps
    w, h = 1080, 1920
    im = Image.new("RGBA", (w, h), (224, 242, 254, 255))
    draw = ImageDraw.Draw(im)
    
    # Subtle floor separator
    draw.rectangle([0, 1840, w, h], fill=(186, 230, 253, 255))
    draw.line([0, 1840, w, 1840], fill=(125, 211, 252, 255), width=3)
    
    # 1. WHITEBOARD
    draw.rounded_rectangle([72, 92, 1008, 1078], radius=28, fill=(148, 163, 184, 180))
    draw.rounded_rectangle([70, 90, 1010, 1070], radius=26, fill=(241, 245, 249, 255), outline=(30, 41, 59, 255), width=8)
    draw.rounded_rectangle([86, 106, 994, 1030], radius=18, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=3)
    
    # Tray & Markers
    draw.rounded_rectangle([250, 1056, 830, 1072], radius=6, fill=(71, 85, 105, 255), outline=(15, 23, 42, 255), width=2)
    draw.rounded_rectangle([320, 1050, 360, 1062], radius=3, fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([380, 1050, 420, 1062], radius=3, fill=(15, 23, 42, 255), outline=(15, 23, 42, 255), width=1)
    draw.rounded_rectangle([440, 1050, 480, 1062], radius=3, fill=(2, 132, 199, 255), outline=(15, 23, 42, 255), width=1)
    
    # Header Card
    draw.rounded_rectangle([100, 125, 980, 210], radius=18, fill=(15, 23, 42, 255))
    draw.text((540, 168), "AI CODING KI 3 SABSE BADI GALATIYAN! ⚠️", font=FONT_TITLE, fill=(255, 255, 255, 255), anchor="mm")
    
    # Hook Premise Card
    draw.rounded_rectangle([120, 230, 960, 315], radius=16, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=3)
    draw.text((540, 272), "VIBE CODING: KYA AB DEV KI ZAROORAT NAHI? 🚀", font=FONT_SUB, fill=(30, 41, 59, 255), anchor="mm")
    
    # Strike-through animation
    t_l2_start = schedule["line2_s"]["start"]
    if t >= t_l2_start + 0.6:
        strike_prog = min(1.0, (t - (t_l2_start + 0.6)) / 0.5)
        start_x = 160
        end_x = start_x + int(strike_prog * 760)
        draw.line([start_x, 272, end_x, 272], fill=(239, 68, 68, 255), width=10)
        if strike_prog >= 0.7:
            draw.rounded_rectangle([730, 236, 940, 308], radius=12, fill=(239, 68, 68, 255))
            draw.text((835, 272), "NAHI! ❌", font=FONT_SUB, fill=(255, 255, 255, 255), anchor="mm")
            
    # Points 1, 2, 3 reveals
    t_l3_start = schedule["line3_s"]["start"]
    if t >= t_l3_start + 0.2:
        draw.rounded_rectangle([110, 350, 970, 480], radius=18, fill=(254, 242, 242, 255), outline=(239, 68, 68, 255), width=3)
        draw.rounded_rectangle([135, 375, 215, 455], radius=16, fill=(239, 68, 68, 255))
        draw.text((175, 415), "1", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 395), "HARDCODED API KEYS & SECRETS 🔑", font=FONT_CARD_TITLE, fill=(153, 27, 27, 255), anchor="lm")
        draw.text((245, 442), "Code directly public GitHub pe leak ho jata hai!", font=FONT_CARD_DESC, fill=(185, 28, 28, 255), anchor="lm")
        
    t_l4_start = schedule["line4_s"]["start"]
    if t >= t_l4_start + 0.2:
        draw.rounded_rectangle([110, 510, 970, 640], radius=18, fill=(255, 247, 237, 255), outline=(249, 115, 22, 255), width=3)
        draw.rounded_rectangle([135, 535, 215, 615], radius=16, fill=(249, 115, 22, 255))
        draw.text((175, 575), "2", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 555), "ZERO ERROR HANDLING & TRY-CATCH 🛑", font=FONT_CARD_TITLE, fill=(154, 52, 18, 255), anchor="lm")
        draw.text((245, 602), "Ek network error aate hi screen blank ho jati hai!", font=FONT_CARD_DESC, fill=(194, 65, 12, 255), anchor="lm")

    t_l5_start = schedule["line5_j"]["start"]
    if t >= t_l5_start:
        draw.rounded_rectangle([110, 670, 970, 800], radius=18, fill=(238, 242, 255, 255), outline=(79, 70, 229, 255), width=3)
        draw.rounded_rectangle([135, 695, 215, 775], radius=16, fill=(79, 70, 229, 255))
        draw.text((175, 735), "3", font=FONT_BADGE, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((245, 715), "MISSING UNIT TESTS & EDGE CASES 🧪", font=FONT_CARD_TITLE, fill=(49, 46, 129, 255), anchor="lm")
        draw.text((245, 762), "AI code likhega, par QA tester tum ho!", font=FONT_CARD_DESC, fill=(67, 56, 202, 255), anchor="lm")

    t_l6_start = schedule["line6_s"]["start"]
    if t >= t_l6_start + 0.3:
        draw.rounded_rectangle([110, 830, 970, 1010], radius=22, fill=(6, 95, 70, 255), outline=(52, 211, 153, 255), width=4)
        draw.text((540, 880), "💡 GOLDEN RULE OF VIBE CODING:", font=FONT_SUB, fill=(167, 243, 208, 255), anchor="mm")
        draw.text((540, 950), "AI = JUNIOR CODER  |  TUM = SENIOR ARCHITECT! 🚀", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255), anchor="mm")

    # Speech state
    junior_speaking = False
    senior_speaking = False
    current_sub = ""
    for sid, sinfo in schedule.items():
        if sinfo["start"] <= t <= sinfo["end"]:
            if sinfo["speaker"] == "junior":
                junior_speaking = True
            else:
                senior_speaking = True
            current_sub = sinfo["sub"]
            break
            
    blink = (t % 3.2) < 0.15
    junior_shocked = (schedule["line5_j"]["start"] <= t <= schedule["line5_j"]["end"] + 0.5)

    # 2. JUNIOR CHARACTER (Female dev / Swara)
    j_cx, j_cy = 300, 1420
    j_bob = int(math.sin(t * 8.0) * 3) if junior_speaking else int(math.sin(t * 2.0) * 1.5)
    
    # Torso (Purple / Violet Hoodie)
    draw.polygon([[j_cx - 130, 1560 + j_bob], [j_cx + 130, 1560 + j_bob], [j_cx + 150, 1840], [j_cx - 150, 1840]], fill=(147, 51, 234, 255), outline=(15, 23, 42, 255))
    draw.rounded_rectangle([j_cx - 70, 1720 + j_bob, j_cx + 70, 1820], radius=12, fill=(126, 34, 206, 255), outline=(15, 23, 42, 255), width=2)
    # White strings
    draw.line([j_cx - 20, 1550 + j_bob, j_cx - 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    draw.line([j_cx + 20, 1550 + j_bob, j_cx + 20, 1630 + j_bob], fill=(255, 255, 255, 255), width=4)
    
    # Arms
    if junior_shocked:
        draw.line([j_cx - 120, 1580, j_cx - 80, 1460], fill=(147, 51, 234, 255), width=28)
        draw.line([j_cx + 120, 1580, j_cx + 80, 1460], fill=(147, 51, 234, 255), width=28)
        draw.ellipse([j_cx - 95, 1445, j_cx - 65, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 65, 1445, j_cx + 95, 1475], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    elif junior_speaking and (schedule["line1_j"]["start"] <= t <= schedule["line1_j"]["end"]):
        hand_lift = int(math.sin(t * 8.0) * 12)
        draw.line([j_cx + 120, 1600, j_cx + 160, 1430 + hand_lift], fill=(147, 51, 234, 255), width=28)
        draw.ellipse([j_cx + 145, 1410 + hand_lift, j_cx + 180, 1445 + hand_lift], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
    else:
        draw.line([j_cx - 120, 1590, j_cx - 80, 1720], fill=(147, 51, 234, 255), width=26)
        draw.line([j_cx + 120, 1590, j_cx + 80, 1720], fill=(147, 51, 234, 255), width=26)
        
    # Head & Ponytail Hair
    draw.ellipse([j_cx - 135, j_cy - 120 + j_bob, j_cx - 75, j_cy + 20 + j_bob], fill=(30, 27, 75, 255)) # Ponytail
    draw.ellipse([j_cx - 95, j_cy - 110 + j_bob, j_cx + 95, j_cy + 110 + j_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=4)
    # Bangs Hair
    draw.chord([j_cx - 100, j_cy - 120 + j_bob, j_cx + 100, j_cy + 30 + j_bob], 180, 360, fill=(30, 27, 75, 255))
    
    # Eyes
    if blink:
        draw.line([j_cx - 50, j_cy - 15 + j_bob, j_cx - 10, j_cy - 15 + j_bob], fill=(15, 23, 42, 255), width=4)
        draw.line([j_cx + 10, j_cy - 15 + j_bob, j_cx + 50, j_cy - 15 + j_bob], fill=(15, 23, 42, 255), width=4)
    elif junior_shocked:
        draw.ellipse([j_cx - 55, j_cy - 35 + j_bob, j_cx - 15, j_cy + 5 + j_bob], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx + 15, j_cy - 35 + j_bob, j_cx + 55, j_cy + 5 + j_bob], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
        draw.ellipse([j_cx - 38, j_cy - 18 + j_bob, j_cx - 32, j_cy - 12 + j_bob], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx + 32, j_cy - 18 + j_bob, j_cx + 38, j_cy - 12 + j_bob], fill=(15, 23, 42, 255))
    else:
        draw.ellipse([j_cx - 45, j_cy - 25 + j_bob, j_cx - 15, j_cy + 5 + j_bob], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx + 15, j_cy - 25 + j_bob, j_cx + 45, j_cy + 5 + j_bob], fill=(15, 23, 42, 255))
        draw.ellipse([j_cx - 32, j_cy - 22 + j_bob, j_cx - 24, j_cy - 14 + j_bob], fill=(255, 255, 255, 255))
        draw.ellipse([j_cx + 28, j_cy - 22 + j_bob, j_cx + 36, j_cy - 14 + j_bob], fill=(255, 255, 255, 255))
        
    # Mouth (Lip-sync)
    jm_y = j_cy + 40 + j_bob
    if junior_speaking:
        open_amt = int(abs(math.sin(t * 18.0)) * 16) + 4
        draw.ellipse([j_cx - 22, jm_y - open_amt, j_cx + 22, jm_y + open_amt], fill=(15, 23, 42, 255))
        draw.chord([j_cx - 16, jm_y - open_amt + 2, j_cx + 16, jm_y], 180, 360, fill=(255, 255, 255, 255)) # Teeth
    elif junior_shocked:
        draw.ellipse([j_cx - 16, jm_y - 12, j_cx + 16, jm_y + 16], fill=(15, 23, 42, 255))
    else:
        draw.arc([j_cx - 22, jm_y - 10, j_cx + 22, jm_y + 12], 10, 170, fill=(15, 23, 42, 255), width=3)

    # 3. SENIOR CHARACTER (Prabhat / Tech Lead)
    s_cx, s_cy = 780, 1380
    s_bob = int(math.sin(t * 8.0) * 3) if senior_speaking else int(math.sin(t * 2.0) * 1.5)
    
    # Body (Navy Jacket + White shirt + Yellow Tie)
    draw.polygon([[s_cx - 140, 1540 + s_bob], [s_cx + 140, 1540 + s_bob], [s_cx + 160, 1840], [s_cx - 160, 1840]], fill=(30, 41, 59, 255), outline=(15, 23, 42, 255))
    draw.polygon([[s_cx - 45, 1540 + s_bob], [s_cx + 45, 1540 + s_bob], [s_cx, 1660 + s_bob]], fill=(255, 255, 255, 255), outline=(203, 213, 225, 255))
    draw.polygon([[s_cx - 10, 1550 + s_bob], [s_cx + 10, 1550 + s_bob], [s_cx + 14, 1690 + s_bob], [s_cx, 1720 + s_bob], [s_cx - 14, 1690 + s_bob]], fill=(245, 158, 11, 255))
    
    # Senior Pointer Arm
    is_pointing = senior_speaking and (schedule["line2_s"]["start"] <= t <= schedule["line4_s"]["end"] + 0.3)
    if is_pointing:
        draw.line([s_cx - 130, 1570, s_cx - 240, 1180], fill=(30, 41, 59, 255), width=30)
        draw.ellipse([s_cx - 255, 1165, s_cx - 225, 1195], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=3)
        # Laser pointer stick
        draw.line([s_cx - 240, 1180, s_cx - 360, 960], fill=(239, 68, 68, 255), width=5)
        draw.ellipse([s_cx - 368, 952, s_cx - 352, 968], fill=(239, 68, 68, 255))
    else:
        draw.line([s_cx - 130, 1570, s_cx - 90, 1730], fill=(30, 41, 59, 255), width=26)
    draw.line([s_cx + 130, 1570, s_cx + 90, 1730], fill=(30, 41, 59, 255), width=26)

    # Head & Hair
    draw.ellipse([s_cx - 95, s_cy - 110 + s_bob, s_cx + 95, s_cy + 110 + s_bob], fill=(253, 230, 138, 255), outline=(15, 23, 42, 255), width=4)
    # Neat Quiff Hair
    draw.chord([s_cx - 100, s_cy - 130 + s_bob, s_cx + 100, s_cy + 10 + s_bob], 180, 360, fill=(51, 65, 85, 255))
    draw.polygon([[s_cx - 70, s_cy - 120 + s_bob], [s_cx + 30, s_cy - 145 + s_bob], [s_cx + 80, s_cy - 115 + s_bob]], fill=(51, 65, 85, 255))
    
    # Glasses
    draw.rounded_rectangle([s_cx - 70, s_cy - 30 + s_bob, s_cx - 15, s_cy + 15 + s_bob], radius=10, fill=(255, 255, 255, 120), outline=(15, 23, 42, 255), width=4)
    draw.rounded_rectangle([s_cx + 15, s_cy - 30 + s_bob, s_cx + 70, s_cy + 15 + s_bob], radius=10, fill=(255, 255, 255, 120), outline=(15, 23, 42, 255), width=4)
    draw.line([s_cx - 15, s_cy - 10 + s_bob, s_cx + 15, s_cy - 10 + s_bob], fill=(15, 23, 42, 255), width=4)
    
    # Eyes
    if blink:
        draw.line([s_cx - 55, s_cy - 10 + s_bob, s_cx - 30, s_cy - 10 + s_bob], fill=(15, 23, 42, 255), width=3)
        draw.line([s_cx + 30, s_cy - 10 + s_bob, s_cx + 55, s_cy - 10 + s_bob], fill=(15, 23, 42, 255), width=3)
    else:
        draw.ellipse([s_cx - 50, s_cy - 18 + s_bob, s_cx - 35, s_cy - 3 + s_bob], fill=(15, 23, 42, 255))
        draw.ellipse([s_cx + 35, s_cy - 18 + s_bob, s_cx + 50, s_cy - 3 + s_bob], fill=(15, 23, 42, 255))
        
    # Senior Mouth
    sm_y = s_cy + 45 + s_bob
    if senior_speaking:
        open_amt = int(abs(math.sin(t * 18.0)) * 14) + 4
        draw.ellipse([s_cx - 20, sm_y - open_amt, s_cx + 20, sm_y + open_amt], fill=(15, 23, 42, 255))
        if open_amt > 8:
            draw.chord([s_cx - 14, sm_y - open_amt + 2, s_cx + 14, sm_y], 180, 360, fill=(255, 255, 255, 255))
        else:
            draw.line([s_cx - 18, sm_y, s_cx + 18, sm_y], fill=(15, 23, 42, 255), width=3)
    else:
        draw.arc([s_cx - 20, sm_y - 8, s_cx + 20, sm_y + 10], 10, 170, fill=(15, 23, 42, 255), width=3)

    # 4. SUBTITLES
    if current_sub:
        draw.rounded_rectangle([60, 1765, 1020, 1845], radius=18, fill=(15, 23, 42, 230))
        draw.text((540, 1805), current_sub, font=FONT_CAPTION, fill=(255, 255, 255, 255), anchor="mm")
        
    return im.convert("RGB")

def render_video_stream(schedule, total_dur):
    fps = 30
    total_f = int(total_dur * fps)
    print(f"--- [1/3] Streaming {total_f} Frames @ {fps}fps to FFmpeg ({total_dur:.2f}s) ---")
    raw_video = os.path.join(WORK_DIR, "dual_voice_video_track.mp4")
    
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
        im = draw_frame(f_idx, fps, schedule, total_dur)
        proc.stdin.write(im.tobytes())
        if f_idx % 150 == 0:
            print(f"Frame {f_idx}/{total_f} ({f_idx/total_f*100:.1f}%)")
            
    proc.stdin.close()
    proc.wait()
    print("Dual voice video stream rendered successfully:", raw_video)
    return raw_video

def mix_dual_audio(schedule, total_dur):
    print("--- [2/3] Multi-Track Audio Mixing (Swara + Prabhat + SFX + BGM) ---")
    l1 = os.path.join(AUDIO_DIR, "l1_junior_swara.wav")
    l2 = os.path.join(AUDIO_DIR, "l2_senior_prabhat.wav")
    l3 = os.path.join(AUDIO_DIR, "l3_senior_prabhat.wav")
    l4 = os.path.join(AUDIO_DIR, "l4_senior_prabhat.wav")
    l5 = os.path.join(AUDIO_DIR, "l5_junior_swara.wav")
    l6 = os.path.join(AUDIO_DIR, "l6_senior_prabhat.wav")
    
    sfx_pop = os.path.join(WORK_DIR, "sfx_pop.wav")
    sfx_scratch = os.path.join(WORK_DIR, "sfx_scratch.wav")
    
    # Background lofi beat
    bgm_path = os.path.join(WORK_DIR, "bgm_dual_lofi.wav")
    cmd_bgm = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"sine=f=261.63:d={total_dur},volume=0.06",
        "-f", "lavfi",
        "-i", f"sine=f=329.63:d={total_dur},volume=0.04",
        "-f", "lavfi",
        "-i", f"sine=f=392.00:d={total_dur},volume=0.04",
        "-f", "lavfi",
        "-i", f"anoisesrc=d={total_dur}:c=brown:r=44100,lowpass=f=220,volume=0.1",
        "-filter_complex", f"[0:a][1:a][2:a][3:a]amix=inputs=4[m];[m]afade=t=out:st={total_dur-1.2:.2f}:d=1.2[out]",
        "-map", "[out]", bgm_path
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    d1 = int(schedule["line1_j"]["start"] * 1000)
    d2 = int(schedule["line2_s"]["start"] * 1000)
    d3 = int(schedule["line3_s"]["start"] * 1000)
    d4 = int(schedule["line4_s"]["start"] * 1000)
    d5 = int(schedule["line5_j"]["start"] * 1000)
    d6 = int(schedule["line6_s"]["start"] * 1000)
    
    d_scratch = int((schedule["line2_s"]["start"] + 0.6) * 1000)
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
        f"[6:a]volume=0.22[a6];"
        f"[7:a]adelay={d_scratch}|{d_scratch},volume=0.45[a7];"
        f"[8:a]adelay={d_p1}|{d_p1},volume=0.55[a8];"
        f"[9:a]adelay={d_p2}|{d_p2},volume=0.55[a9];"
        f"[10:a]adelay={d_p3}|{d_p3},volume=0.55[a10];"
        f"[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10]amix=inputs=11:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1.0[final_audio]"
    )
    
    final_audio = os.path.join(WORK_DIR, "dual_final_audio.wav")
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
    print("Dual audio mix compiled:", final_audio)
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
    print(f"\n🎉 DUAL VOICE MASTER REEL READY: {OUTPUT_MP4}")
    print(f"Duration: {total_dur:.2f}s | Resolution: 1080x1920 (9:16 Vertical)")

def main():
    durs = get_durations()
    schedule, total_dur = build_timeline(durs)
    print(f"Total Video Planned Duration: {total_dur:.2f}s")
    v_track = render_video_stream(schedule, total_dur)
    a_track = mix_dual_audio(schedule, total_dur)
    compile_final_mp4(v_track, a_track, total_dur)

if __name__ == "__main__":
    main()
