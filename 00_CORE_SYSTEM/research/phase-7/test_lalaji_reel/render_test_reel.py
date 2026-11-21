import os
import json
import math
import subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

PROJECT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\test_lalaji_reel"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
SFX_DIR = os.path.join(PROJECT_DIR, "sfx")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
SNAPSHOT_DIR = os.path.join(PROJECT_DIR, "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "lalaji_unlimited_leave_scam_master.mp4")
TEMP_VIDEO = os.path.join(PROJECT_DIR, "temp_test_video.mp4")
TEMP_AUDIO = os.path.join(PROJECT_DIR, "temp_test_audio.wav")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# --- 1. Load Audio Cues & Assembly ---
with open(os.path.join(AUDIO_DIR, "reel_meta.json"), "r", encoding="utf-8") as f:
    dialogue_cues = json.load(f)

sr = 44100
timeline = []
cur_time = 0.0
audio_data_dict = {}

for c in dialogue_cues:
    wav_path = c["wav"]
    data, r = sf.read(wav_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1) # Mono
    
    audio_data_dict[c["id"]] = {
        "data": data,
        "sr": r,
        "dur": len(data) / r
    }

    timeline.append({
        "id": c["id"],
        "speaker": c["speaker"],
        "badge": c["badge"],
        "char": c["char"],
        "sub": c["sub"],
        "topic": c["topic"],
        "hud_pill": c["hud_pill"],
        "start": cur_time,
        "end": cur_time + c["dur"],
        "dur": c["dur"],
        "wav": wav_path
    })
    cur_time += c["dur"]

total_duration = cur_time
total_samples = int(total_duration * sr)
master_audio = np.zeros(total_samples, dtype=np.float32)

print(f"Total video duration: {total_duration:.2f}s ({len(timeline)} scenes)")

# 1.1 Mix Dialogue
for c in timeline:
    item = audio_data_dict[c["id"]]
    data = item["data"]
    start_s = int(c["start"] * sr)
    end_s = start_s + len(data)
    if end_s > total_samples:
        data = data[:total_samples - start_s]
        end_s = total_samples
    master_audio[start_s:end_s] += data * 0.95

# 1.2 Mix Lo-Fi / Acoustic Comedy BGM (-22dB with ducking)
bg_path = os.path.join(SFX_DIR, "lofi_bg_track.wav")
if os.path.exists(bg_path):
    bg_data, _ = sf.read(bg_path)
    if len(bg_data.shape) > 1:
        bg_data = bg_data.mean(axis=1)
    repeats = int(math.ceil(total_samples / len(bg_data)))
    bg_full = np.tile(bg_data, repeats)[:total_samples]
    master_audio += bg_full * 0.15 # Smooth background bed

# 1.3 Mix Spot SFX at precise camera cuts & punchlines
def add_sfx(sfx_name, t_sec, vol=0.45):
    p = os.path.join(SFX_DIR, sfx_name)
    if os.path.exists(p):
        sfx_data, _ = sf.read(p)
        if len(sfx_data.shape) > 1:
            sfx_data = sfx_data.mean(axis=1)
        st = int(t_sec * sr)
        en = min(total_samples, st + len(sfx_data))
        master_audio[st:en] += sfx_data[:en - st] * vol

# Camera transition whooshes (0.15s before cut)
for c in timeline:
    if c["start"] > 0:
        add_sfx("whoosh.wav", c["start"] - 0.10, vol=0.35)

# Narrative SFX cues
add_sfx("pop.wav", timeline[0]["start"] + 1.0, vol=0.40)   # Chintu leave request
add_sfx("buzz.wav", timeline[1]["start"] + 0.2, vol=0.50)  # Lalaji vine boom punch
add_sfx("pop.wav", timeline[1]["start"] + 4.5, vol=0.40)   # Unlimited policy badge
add_sfx("ding.wav", timeline[2]["start"] + 0.5, vol=0.45)  # Chintu portal card
add_sfx("buzz.wav", timeline[2]["start"] + 3.5, vol=0.50)  # REJECT sound
add_sfx("buzz.wav", timeline[3]["start"] + 0.2, vol=0.50)  # Lalaji reality punch
add_sfx("buzz.wav", timeline[3]["start"] + 7.5, vol=0.55)  # Ultimatum threat
add_sfx("ding.wav", timeline[4]["start"] + 0.8, vol=0.50)  # CTA vote card
add_sfx("pop.wav", timeline[4]["start"] + 4.5, vol=0.45)   # Comment reminder

# Normalize master audio to -1dB peak
peak = np.max(np.abs(master_audio))
if peak > 0:
    master_audio = master_audio / peak * 0.92

sf.write(TEMP_AUDIO, master_audio, sr)
print(f"Master mixed audio saved: {TEMP_AUDIO}")

# --- 2. Visual Assets & Scaling (1080x1920 Full HD) ---
W, H = 1080, 1920
FPS = 30
TOTAL_FRAMES = int(total_duration * FPS)

# Fonts
FONT_HUD_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 26)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
FONT_CARD_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28)
FONT_SUB_MAIN = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_SUB_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)

# Base Background
bg_raw = Image.open(os.path.join(ASSETS_DIR, "office_cabin_bg.jpg")).convert("RGB")
bg_wide = bg_raw.resize((W, H), Image.Resampling.LANCZOS)

# Chintu Assets (Wide & Close-up)
emp_raw = Image.open(os.path.join(ASSETS_DIR, "employee_cutout.png")).convert("RGBA")
emp_crop = emp_raw.crop(emp_raw.getbbox())

h_wide_emp = 920
w_wide_emp = int(emp_crop.width * (h_wide_emp / emp_crop.height))
chintu_wide = emp_crop.resize((w_wide_emp, h_wide_emp), Image.Resampling.LANCZOS)

h_close_emp = 1150
w_close_emp = int(emp_crop.width * (h_close_emp / emp_crop.height))
chintu_close = emp_crop.resize((w_close_emp, h_close_emp), Image.Resampling.LANCZOS)

# Lalaji Assets (Wide & Close-up)
mgr_raw = Image.open(os.path.join(ASSETS_DIR, "manager_pose_1_rgba.png")).convert("RGBA")
m_crop = mgr_raw.crop(mgr_raw.getbbox())

h_w = 880
mw_w = int(m_crop.width * (h_w / m_crop.height))
lalaji_wide = m_crop.resize((mw_w, h_w), Image.Resampling.LANCZOS)

h_c = 1150
mw_c = int(m_crop.width * (h_c / m_crop.height))
lalaji_close = m_crop.resize((mw_c, h_c), Image.Resampling.LANCZOS)

print("Visual assets prepared (Wide & Snap-Close rigs ready).")

# --- 3. HUD, Kinetic Cards & Karaoke Subtitles ---

def draw_safe_box(draw, x0, y0, x1, y1, fill_color, outline_color=None, width=2, radius=16):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill_color, outline=outline_color, width=width)

def draw_hud_header(draw, hud_pill, step_num, max_steps=5):
    """Mana5-style top HUD navigation header."""
    y = 55
    # Left Monospace Pill
    draw_safe_box(draw, 65, y, 380, y + 46, (254, 240, 138), outline_color=(202, 138, 4), width=2, radius=10)
    draw.text((85, y + 9), hud_pill, font=FONT_HUD_MONO, fill=(113, 63, 18))

    # Center Topic
    draw_safe_box(draw, 400, y, 780, y + 46, (15, 23, 42), outline_color=(99, 102, 241), width=2, radius=10)
    draw.text((435, y + 10), "UNLIMITED LEAVES SCAM", font=FONT_BADGE, fill=(255, 255, 255))

    # Right Step Counter
    draw_safe_box(draw, 800, y, 1015, y + 46, (238, 242, 255), outline_color=(99, 102, 241), width=2, radius=10)
    draw.text((830, y + 10), f"STEP {step_num}/{max_steps}", font=FONT_BADGE, fill=(67, 56, 202))

def draw_kinetic_cards(draw, scene_id, rel_t):
    """Renders mid-screen kinetic metric cards with zero border bleed."""
    CX0, CY0, CX1, CY1 = 65, 125, 1015, 680
    draw_safe_box(draw, CX0, CY0, CX1, CY1, (255, 255, 255), outline_color=(203, 213, 225), width=3, radius=22)

    ix0 = CX0 + 28
    iy0 = CY0 + 24
    inner_w = (CX1 - CX0) - 56

    if scene_id == "scene1_hook":
        draw_safe_box(draw, ix0, iy0, ix0 + 340, iy0 + 44, (238, 242, 255), outline_color=(99, 102, 241), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "CHINTU'S LEAVE APPLICATION", font=FONT_BADGE, fill=(67, 56, 202))

        draw.text((ix0, iy0 + 60), "1 YEAR NON-STOP DEV WORK", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "Applying for 3 days of sick leave...", font=FONT_CARD_BODY, fill=(100, 116, 139))

        if rel_t >= 0.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 245, (248, 250, 252), outline_color=(226, 232, 240), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 115, iy0 + 196, (224, 231, 255), radius=6)
            draw.text((ix0 + 24, iy0 + 172), "STATUS", font=FONT_BADGE, fill=(67, 56, 202))
            draw.text((ix0 + 125, iy0 + 172), "Total Leaves Taken This Year: 0", font=FONT_CARD_BOLD, fill=(30, 41, 59))
            draw.text((ix0 + 20, iy0 + 208), "Health: High fever, 100% burnout, seeking rest", font=FONT_CARD_BODY, fill=(71, 85, 105))

        if rel_t >= 2.5:
            draw_safe_box(draw, ix0, iy0 + 265, ix0 + inner_w, iy0 + 365, (254, 249, 195), outline_color=(234, 179, 8), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 278, ix0 + 125, iy0 + 306, (254, 240, 138), radius=6)
            draw.text((ix0 + 22, iy0 + 282), "REQUEST", font=FONT_BADGE, fill=(161, 98, 7))
            draw.text((ix0 + 135, iy0 + 282), "Applied: 3 Days Sick Leave", font=FONT_CARD_BOLD, fill=(161, 98, 7))
            draw.text((ix0 + 20, iy0 + 320), "Expected: Simple approval from Lala Ji", font=FONT_CARD_BODY, fill=(133, 77, 14))

        if rel_t >= 4.5:
            draw_safe_box(draw, ix0, iy0 + 385, ix0 + inner_w, iy0 + 485, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 398, ix0 + 115, iy0 + 426, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 402), "ALERT", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 125, iy0 + 402), "Lala Ji Summons to Executive Cabin!", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 440), "'Chintu, idhar aao!' — The confrontation begins", font=FONT_CARD_BODY, fill=(153, 27, 27))

    elif scene_id == "scene2_lalaji":
        draw_safe_box(draw, ix0, iy0, ix0 + 320, iy0 + 44, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "LALA JI CORPORATE LOGIC", font=FONT_BADGE, fill=(185, 28, 28))

        draw.text((ix0, iy0 + 60), "'HAMARI COMPANY TOH UNLIMITED HAI!'", font=FONT_CARD_TITLE, fill=(185, 28, 28))
        draw.text((ix0, iy0 + 108), "The classic startup HR trap revealed:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        if rel_t >= 0.8:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 255, (255, 247, 237), outline_color=(249, 115, 22), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 125, iy0 + 196, (254, 215, 170), radius=6)
            draw.text((ix0 + 22, iy0 + 172), "HR PITCH", font=FONT_BADGE, fill=(194, 65, 12))
            draw.text((ix0 + 135, iy0 + 172), "Offer Letter: 'Unlimited Paid Time Off'", font=FONT_CARD_BOLD, fill=(194, 65, 12))
            draw.text((ix0 + 20, iy0 + 210), "Sounds like Silicon Valley paradise to freshers", font=FONT_CARD_BODY, fill=(154, 52, 18))

        if rel_t >= 4.0:
            draw_safe_box(draw, ix0, iy0 + 275, ix0 + inner_w, iy0 + 465, (254, 242, 242), outline_color=(220, 38, 38), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 288, ix0 + 105, iy0 + 316, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 292), "SCAM", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 115, iy0 + 292), "REALITY: 0 Leaves Actually Approved!", font=FONT_CARD_TITLE, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 345), "Lala Ji: 'Jab hum unlimited bolte hain...'", font=FONT_CARD_BOLD, fill=(153, 27, 27))
            draw.text((ix0 + 20, iy0 + 390), "...toh chutti lene ka sochna bhi paap hai!", font=FONT_CARD_BODY, fill=(153, 27, 27))

    elif scene_id == "scene3_shock":
        draw_safe_box(draw, ix0, iy0, ix0 + 300, iy0 + 44, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "PORTAL REALITY CHECK", font=FONT_BADGE, fill=(21, 128, 61))

        draw.text((ix0, iy0 + 60), "THE HR PORTAL ILLUSION", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "How the HR software actually behaves:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        if rel_t >= 0.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 265, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 125, iy0 + 196, (187, 247, 208), radius=6)
            draw.text((ix0 + 24, iy0 + 172), "PORTAL", font=FONT_BADGE, fill=(21, 128, 61))
            draw.text((ix0 + 135, iy0 + 172), "Leave Balance: 999 Days Available", font=FONT_CARD_BOLD, fill=(21, 128, 61))
            draw.text((ix0 + 20, iy0 + 215), "Dashboard looks green and generous", font=FONT_CARD_BODY, fill=(22, 101, 52))

        if rel_t >= 3.2:
            draw_safe_box(draw, ix0, iy0 + 285, ix0 + inner_w, iy0 + 465, (254, 242, 242), outline_color=(220, 38, 38), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 298, ix0 + 135, iy0 + 326, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 302), "REJECTED", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 145, iy0 + 302), "Instant Manager Reject Button!", font=FONT_CARD_TITLE, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 355), "Reason: 'Critical Sprint Delivery Pending'", font=FONT_CARD_BOLD, fill=(153, 27, 27))
            draw.text((ix0 + 20, iy0 + 400), "Every single day is marked as 'critical sprint'!", font=FONT_CARD_BODY, fill=(153, 27, 27))

    elif scene_id == "scene4_punchline":
        draw_safe_box(draw, ix0, iy0, ix0 + 320, iy0 + 44, (254, 242, 242), outline_color=(220, 38, 38), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "LALA JI'S PUNCHLINE", font=FONT_BADGE, fill=(185, 28, 28))

        draw.text((ix0, iy0 + 60), "THE TRUE MEANING OF 'UNLIMITED'", font=FONT_CARD_TITLE, fill=(185, 28, 28))
        draw.text((ix0, iy0 + 108), "The dictionary definition according to Lala Ji:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        if rel_t >= 0.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 275, (255, 247, 237), outline_color=(234, 88, 12), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 135, iy0 + 196, (254, 215, 170), radius=6)
            draw.text((ix0 + 22, iy0 + 172), "DEFINITION", font=FONT_BADGE, fill=(194, 65, 12))
            draw.text((ix0 + 145, iy0 + 172), "'Company Unlimited Cancel Kar Sakti Hai!'", font=FONT_CARD_BOLD, fill=(194, 65, 12))
            draw.text((ix0 + 20, iy0 + 215), "Tumhare paas lene ka nahi, company ke paas kaatne ka adhikar hai", font=FONT_CARD_BODY, fill=(154, 52, 18))

        if rel_t >= 6.5:
            draw_safe_box(draw, ix0, iy0 + 295, ix0 + inner_w, iy0 + 465, (254, 242, 242), outline_color=(220, 38, 38), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 308, ix0 + 125, iy0 + 336, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 312), "THREAT", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 135, iy0 + 312), "MONDAY KO AAO YA PERMANENT CHUTTI!", font=FONT_CARD_TITLE, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 365), "Notice period counting starts immediately", font=FONT_CARD_BOLD, fill=(153, 27, 27))
            draw.text((ix0 + 20, iy0 + 410), "Full corporate drama at its finest!", font=FONT_CARD_BODY, fill=(153, 27, 27))

    elif scene_id == "scene5_cta":
        draw_safe_box(draw, ix0, iy0, ix0 + 350, iy0 + 44, (238, 242, 255), outline_color=(99, 102, 241), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "QUESTION FOR AUDIENCE", font=FONT_BADGE, fill=(67, 56, 202))

        draw.text((ix0, iy0 + 60), "KYA AAPKE YAHAN BHI LALA CULTURE HAI?", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "Vote and drop your honest comment:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        if rel_t >= 0.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 255, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 115, iy0 + 196, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 172), "VOTE A", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 125, iy0 + 172), "Haan! Humare yahan bhi leave mangna paap hai", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 210), "Sick leave par bhi laptop login karwate hain", font=FONT_CARD_BODY, fill=(153, 27, 27))

        if rel_t >= 3.5:
            draw_safe_box(draw, ix0, iy0 + 275, ix0 + inner_w, iy0 + 375, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 288, ix0 + 115, iy0 + 316, (187, 247, 208), radius=6)
            draw.text((ix0 + 22, iy0 + 292), "VOTE B", font=FONT_BADGE, fill=(21, 128, 61))
            draw.text((ix0 + 125, iy0 + 292), "Nahi! Humari company mein leaves milti hain", font=FONT_CARD_BOLD, fill=(21, 128, 61))
            draw.text((ix0 + 20, iy0 + 330), "Work-life balance follow hota hai", font=FONT_CARD_BODY, fill=(22, 101, 52))

        if rel_t >= 5.5:
            draw_safe_box(draw, ix0, iy0 + 395, ix0 + inner_w, iy0 + 475, (245, 243, 255), outline_color=(147, 51, 234), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 408, ix0 + 105, iy0 + 436, (233, 213, 255), radius=6)
            draw.text((ix0 + 22, iy0 + 412), "COMMENT", font=FONT_BADGE, fill=(126, 34, 206))
            draw.text((ix0 + 115, iy0 + 412), "SHARE APNA DARD IN COMMENTS!", font=FONT_CARD_TITLE, fill=(126, 34, 206))

def render_karaoke_subtitle_box(draw, badge_label, char_name, sub_text, rel_t, total_dur, y_bottom=1780):
    """
    Combines LalajiProMax Mint Speaker Badge + Mana5 Karaoke Word Highlight.
    Zero overflow guaranteed.
    """
    pad_x = 36
    pad_y = 20
    box_w = 960
    box_x0 = (W - box_w) // 2
    box_x1 = box_x0 + box_w
    avail_w = box_w - (pad_x * 2)

    words = sub_text.split()
    lines = []
    cur_line = []
    for w in words:
        test = " ".join(cur_line + [w])
        bbox = draw.textbbox((0, 0), test, font=FONT_SUB_MAIN)
        if (bbox[2] - bbox[0]) <= avail_w or not cur_line:
            cur_line.append(w)
        else:
            lines.append(cur_line)
            cur_line = [w]
    if cur_line:
        lines.append(cur_line)

    line_h = 44
    text_total_h = len(lines) * line_h
    box_h = pad_y * 2 + text_total_h + 24
    box_y0 = y_bottom - box_h
    box_y1 = y_bottom

    # Dark glass rounded container
    outline_col = (52, 211, 153) if char_name == "chintu" else (239, 68, 68)
    draw_safe_box(draw, box_x0, box_y0, box_x1, box_y1, (15, 23, 42), outline_color=outline_col, width=3, radius=20)

    # LalajiProMax Mint Green Speaker Badge
    badge_bg = (52, 211, 153) if char_name == "chintu" else (220, 38, 38)
    badge_txt_col = (6, 78, 59) if char_name == "chintu" else (255, 255, 255)
    badge_bbox = draw.textbbox((0, 0), f"[ {badge_label} ]", font=FONT_SUB_BADGE)
    badge_w = (badge_bbox[2] - badge_bbox[0]) + 28
    draw_safe_box(draw, box_x0 + 20, box_y0 - 16, box_x0 + 20 + badge_w, box_y0 + 20, badge_bg, radius=10)
    draw.text((box_x0 + 34, box_y0 - 11), f"[ {badge_label} ]", font=FONT_SUB_BADGE, fill=badge_txt_col)

    # Calculate which word is active based on progress (Mana5 Karaoke Highlight)
    total_words = len(words)
    progress = min(0.999, max(0.0, rel_t / total_dur))
    active_word_idx = int(progress * total_words)

    # Render wrapped lines with Karaoke highlight
    text_y = box_y0 + pad_y + 12
    global_word_count = 0

    for line_words in lines:
        # Measure line width for center alignment
        line_str = " ".join(line_words)
        l_bbox = draw.textbbox((0, 0), line_str, font=FONT_SUB_MAIN)
        line_w = l_bbox[2] - l_bbox[0]
        cur_x = box_x0 + (box_w - line_w) // 2

        for w in line_words:
            w_bbox = draw.textbbox((0, 0), w, font=FONT_SUB_MAIN)
            w_w = w_bbox[2] - w_bbox[0]
            sp_bbox = draw.textbbox((0, 0), " ", font=FONT_SUB_MAIN)
            sp_w = sp_bbox[2] - sp_bbox[0]

            if global_word_count == active_word_idx:
                # Active Karaoke Word: Mana5 Yellow Solid Pill (#FFD21E)
                draw.rounded_rectangle([cur_x - 4, text_y - 2, cur_x + w_w + 4, text_y + 36], radius=6, fill=(255, 210, 30))
                draw.text((cur_x, text_y), w, font=FONT_SUB_MAIN, fill=(0, 0, 0))
            else:
                draw.text((cur_x, text_y), w, font=FONT_SUB_MAIN, fill=(255, 255, 255))

            cur_x += w_w + sp_w
            global_word_count += 1

        text_y += line_h

# --- 4. Natural Lip-Sync Engine ---

def get_audio_rms_at_time(scene_id, rel_t):
    item = audio_data_dict[scene_id]
    data = item["data"]
    sr = item["sr"]
    idx = int(rel_t * sr)
    window_size = int(0.04 * sr)
    if idx < 0 or idx >= len(data):
        return 0.0
    start = max(0, idx - window_size // 2)
    end = min(len(data), idx + window_size // 2)
    chunk = data[start:end]
    if len(chunk) == 0:
        return 0.0
    return float(np.sqrt(np.mean(chunk**2)))

def draw_natural_mouth(draw, cx, cy, rms, is_speaking, char_name, scale=1.0):
    if not is_speaking or rms < 0.015:
        return

    skin_col = (205, 142, 102) if char_name == "chintu" else (186, 134, 104)
    lip_col = (110, 40, 48) if char_name == "chintu" else (90, 32, 40)

    rw = int(22 * scale)
    rh = int(9 * scale)
    draw.rounded_rectangle([cx - rw, cy - rh, cx + rw, cy + rh], radius=int(6 * scale), fill=skin_col)

    if rms > 0.065:
        # AH - Wide Open
        ew = int(16 * scale)
        eh = int(14 * scale)
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=(30, 15, 20))
        draw.rectangle([cx - int(10*scale), cy - int(13*scale), cx + int(10*scale), cy - int(5*scale)], fill=(245, 245, 250))
        draw.ellipse([cx - int(11*scale), cy + int(2*scale), cx + int(11*scale), cy + int(13*scale)], fill=(225, 95, 115))
        draw.ellipse([cx - ew - 1, cy - eh - 1, cx + ew + 1, cy + eh + 1], outline=lip_col, width=int(2*scale))
    elif rms > 0.035:
        # OH - Round Open
        ew = int(12 * scale)
        eh = int(11 * scale)
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=(30, 15, 20))
        draw.rectangle([cx - int(8*scale), cy - int(10*scale), cx + int(8*scale), cy - int(5*scale)], fill=(245, 245, 250))
        draw.ellipse([cx - int(8*scale), cy + int(2*scale), cx + int(8*scale), cy + int(10*scale)], fill=(225, 95, 115))
        draw.ellipse([cx - ew - 1, cy - eh - 1, cx + ew + 1, cy + eh + 1], outline=lip_col, width=int(2*scale))
    else:
        # EE - Semi-Open
        ew = int(16 * scale)
        eh = int(6 * scale)
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=(30, 15, 20))
        draw.rectangle([cx - int(12*scale), cy - int(5*scale), cx + int(12*scale), cy + int(1*scale)], fill=(245, 245, 250))
        draw.ellipse([cx - ew - 1, cy - eh - 1, cx + ew + 1, cy + eh + 1], outline=lip_col, width=int(2*scale))

# --- 5. Master Video Rendering Loop ---
print("--- Starting Master Video Render via FFmpeg Pipe ---")

cmd_video = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    TEMP_VIDEO
]

pipe = subprocess.Popen(cmd_video, stdin=subprocess.PIPE)

scene_idx = 0
active_cue = timeline[0]

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS

    while scene_idx < len(timeline) - 1 and t >= timeline[scene_idx]["end"]:
        scene_idx += 1
    active_cue = timeline[scene_idx]
    scene_id = active_cue["id"]
    rel_t = t - active_cue["start"]
    speaking_char = active_cue["char"]

    frame = bg_wide.copy()
    draw = ImageDraw.Draw(frame)

    rms_val = get_audio_rms_at_time(scene_id, rel_t)
    is_chintu_speaking = (speaking_char == "chintu")
    is_lalaji_speaking = (speaking_char == "lalaji")

    # 5.1 Mana5 Top Status Bar (HUD)
    draw_hud_header(draw, active_cue["hud_pill"], scene_idx + 1, len(timeline))

    # 5.2 Kinetic Dashboard Cards
    draw_kinetic_cards(draw, scene_id, rel_t)

    # 5.3 CINEMATIC CAMERA SHOTS (from LalajiProMax)
    if scene_id == "scene1_hook":
        # SHOT 1: Wide Cabin Entrance
        walk_dur = 2.5
        if rel_t < walk_dur:
            prog = rel_t / walk_dur
            cx = int(-180 + (130 - (-180)) * prog)
            cy = 800 - int(abs(math.sin(rel_t * 9.0)) * 14)
        else:
            cx = 130
            cy = 800 + int(math.sin(rel_t * 2.5) * 3)

        frame.paste(lalaji_wide, (610, 830), lalaji_wide)
        frame.paste(chintu_wide, (cx, cy), chintu_wide)

        # Mouth
        chintu_mouth_cx = cx + 138
        chintu_mouth_cy = cy + 118
        draw_natural_mouth(draw, chintu_mouth_cx, chintu_mouth_cy, rms_val, is_chintu_speaking, "chintu", scale=1.0)

    elif scene_id in ["scene2_lalaji", "scene4_punchline"]:
        # SHOT 2 & 4: SNAP PUNCH-ZOOM ON LALA JI (Center Close-up)
        lx = (W - lalaji_close.width) // 2 + 50
        ly = 700 + int(math.sin(rel_t * 2.5) * 3)

        # Chintu listening on left edge
        chintu_listen = chintu_wide.resize((int(chintu_wide.width * 0.88), int(chintu_wide.height * 0.88)), Image.Resampling.LANCZOS)
        frame.paste(chintu_listen, (-50, 840), chintu_listen)

        frame.paste(lalaji_close, (lx, ly), lalaji_close)

        lalaji_mouth_cx = lx + 222
        lalaji_mouth_cy = ly + 206
        draw_natural_mouth(draw, lalaji_mouth_cx, lalaji_mouth_cy, rms_val, is_lalaji_speaking, "lalaji", scale=1.25)

        # Dramatic red border warning in Scene 4
        if scene_id == "scene4_punchline" and rel_t >= 6.5:
            draw.rectangle([0, 0, W, H], outline=(239, 68, 68), width=6)

    elif scene_id in ["scene3_shock", "scene5_cta"]:
        # SHOT 3 & 5: SNAP PUNCH-ZOOM ON CHINTU (Center Close-up)
        cx = (W - chintu_close.width) // 2
        cy = 690 + int(math.sin(rel_t * 2.5) * 3)

        # Lalaji listening on right edge
        lalaji_listen = lalaji_wide.resize((int(lalaji_wide.width * 0.85), int(lalaji_wide.height * 0.85)), Image.Resampling.LANCZOS)
        frame.paste(lalaji_listen, (W - lalaji_listen.width + 40, 830), lalaji_listen)

        frame.paste(chintu_close, (cx, cy), chintu_close)

        chintu_mouth_cx = cx + 172
        chintu_mouth_cy = cy + 148
        draw_natural_mouth(draw, chintu_mouth_cx, chintu_mouth_cy, rms_val, is_chintu_speaking, "chintu", scale=1.25)

    # 5.4 Natural Eye Blinking
    blink_cycle = (f_idx % 114)
    if blink_cycle < 4:
        if scene_id in ["scene2_lalaji", "scene4_punchline"]:
            draw.line([lalaji_mouth_cx - 36, lalaji_mouth_cy - 52, lalaji_mouth_cx - 12, lalaji_mouth_cy - 52], fill=(30, 20, 25), width=3)
            draw.line([lalaji_mouth_cx + 12, lalaji_mouth_cy - 52, lalaji_mouth_cx + 36, lalaji_mouth_cy - 52], fill=(30, 20, 25), width=3)
        else:
            draw.line([chintu_mouth_cx - 44, chintu_mouth_cy - 56, chintu_mouth_cx - 18, chintu_mouth_cy - 56], fill=(30, 20, 25), width=3)
            draw.line([chintu_mouth_cx + 18, chintu_mouth_cy - 56, chintu_mouth_cx + 44, chintu_mouth_cy - 56], fill=(30, 20, 25), width=3)

    # 5.5 Top Progress Bar
    pct = t / total_duration
    draw.rectangle([0, 0, W, 8], fill=(226, 232, 240))
    draw.rectangle([0, 0, int(W * pct), 8], fill=(234, 179, 8))

    # 5.6 Safe Karaoke Subtitle Box (ZERO OVERFLOW + Active Word Highlight)
    badge_label = active_cue["badge"]
    sub_text = active_cue["sub"]
    render_karaoke_subtitle_box(draw, badge_label, speaking_char, sub_text, rel_t, active_cue["dur"], y_bottom=1780)

    # Pipe frame to FFmpeg
    pipe.stdin.write(frame.tobytes())

    # Save representative snapshots
    if f_idx in [60, 350, 700, 1000, 1250]:
        snap_p = os.path.join(SNAPSHOT_DIR, f"test_snap_{f_idx}.jpg")
        frame.save(snap_p)
        print(f"Saved snapshot {snap_p} at frame {f_idx} (t={t:.1f}s)")

    if f_idx % 300 == 0:
        print(f"Rendered {f_idx}/{TOTAL_FRAMES} frames ({f_idx*100/TOTAL_FRAMES:.1f}%)")

pipe.stdin.close()
pipe.wait()
print(f"Video stream rendered: {TEMP_VIDEO}")

# --- 6. Mux Video & Audio Master ---
print("--- Muxing Broadcast Reel ---")
cmd_mux = [
    ffmpeg_exe,
    "-y",
    "-i", TEMP_VIDEO,
    "-i", TEMP_AUDIO,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_VIDEO
]
subprocess.run(cmd_mux, check=True)
print(f"Master Reel Successfully Generated: {OUTPUT_VIDEO}")

# Clean temp files
if os.path.exists(TEMP_VIDEO):
    try:
        os.remove(TEMP_VIDEO)
    except Exception:
        pass
if os.path.exists(TEMP_AUDIO):
    try:
        os.remove(TEMP_AUDIO)
    except Exception:
        pass

print("PRACTICAL TEST REEL COMPLETED CLEANLY.")
