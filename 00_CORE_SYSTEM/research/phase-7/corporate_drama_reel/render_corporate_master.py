import os
import json
import math
import subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# --- Configuration & Paths ---
PROJECT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\corporate_drama_reel"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
SFX_DIR = os.path.join(PROJECT_DIR, "sfx")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
SNAPSHOT_DIR = os.path.join(PROJECT_DIR, "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "lala_company_drama_master.mp4")
TEMP_VIDEO = os.path.join(PROJECT_DIR, "temp_corporate_video.mp4")
TEMP_AUDIO = os.path.join(PROJECT_DIR, "temp_corporate_audio.wav")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# --- 1. Load Audio Cues & Assembly ---
with open(os.path.join(AUDIO_DIR, "corporate_drama_meta.json"), "r", encoding="utf-8") as f:
    dialogue_cues = json.load(f)

sr = 44100
timeline = []
cur_time = 0.0

# Pre-load audio data and compute RMS envelopes for lip sync
audio_data_dict = {}

for c in dialogue_cues:
    wav_path = c["wav"]
    data, r = sf.read(wav_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1) # Mono
    
    # Store audio data
    audio_data_dict[c["id"]] = {
        "data": data,
        "sr": r,
        "dur": len(data) / r
    }

    timeline.append({
        "id": c["id"],
        "speaker": c["speaker"],
        "char": c["char"],
        "sub": c["sub"],
        "topic": c["topic"],
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

# 1.2 Mix Lo-Fi Background Music
bg_path = os.path.join(SFX_DIR, "lofi_bg_track.wav")
if os.path.exists(bg_path):
    bg_data, _ = sf.read(bg_path)
    if len(bg_data.shape) > 1:
        bg_data = bg_data.mean(axis=1)
    repeats = int(math.ceil(total_samples / len(bg_data)))
    bg_full = np.tile(bg_data, repeats)[:total_samples]
    # Subtle corporate tension volume
    master_audio += bg_full * 0.18

# 1.3 Mix Spot SFX at key narrative beats
def add_sfx(sfx_name, t_sec, vol=0.45):
    p = os.path.join(SFX_DIR, sfx_name)
    if os.path.exists(p):
        sfx_data, _ = sf.read(p)
        if len(sfx_data.shape) > 1:
            sfx_data = sfx_data.mean(axis=1)
        st = int(t_sec * sr)
        en = min(total_samples, st + len(sfx_data))
        master_audio[st:en] += sfx_data[:en - st] * vol

for c in timeline:
    if c["start"] > 0:
        add_sfx("whoosh.wav", c["start"] - 0.15, vol=0.35)

# Narrative SFX cues
add_sfx("pop.wav", timeline[0]["start"] + 1.2, vol=0.4)    # Walk in card
add_sfx("buzz.wav", timeline[1]["start"] + 1.5, vol=0.4)   # Gaslight 1
add_sfx("buzz.wav", timeline[1]["start"] + 6.0, vol=0.4)   # Gaslight 2
add_sfx("buzz.wav", timeline[1]["start"] + 10.5, vol=0.45) # 0% Appraisal trap
add_sfx("ding.wav", timeline[2]["start"] + 1.2, vol=0.5)   # 14h Weekend proof
add_sfx("ding.wav", timeline[2]["start"] + 4.2, vol=0.5)   # Client appreciation
add_sfx("ding.wav", timeline[2]["start"] + 7.5, vol=0.5)   # 0 Bugs
add_sfx("buzz.wav", timeline[3]["start"] + 1.0, vol=0.45)  # Ultimatum start
add_sfx("buzz.wav", timeline[3]["start"] + 6.5, vol=0.5)   # Paper slam
add_sfx("pop.wav", timeline[4]["start"] + 0.8, vol=0.4)    # Dilemma EMI
add_sfx("ding.wav", timeline[5]["start"] + 1.0, vol=0.5)   # Audience question
add_sfx("pop.wav", timeline[5]["start"] + 6.0, vol=0.45)   # Part 2 hook

# Normalize master audio
peak = np.max(np.abs(master_audio))
if peak > 0:
    master_audio = master_audio / peak * 0.92

sf.write(TEMP_AUDIO, master_audio, sr)
print(f"Master mixed audio saved: {TEMP_AUDIO}")

# --- 2. Visual Setup (1080x1920 Full HD) ---
W, H = 1080, 1920
FPS = 30
TOTAL_FRAMES = int(total_duration * FPS)

# Load Fonts
FONT_TOP_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)
FONT_CARD_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
FONT_CARD_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28)
FONT_SUB_MAIN = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_SUB_TAG = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)

# Load & Prepare Images
bg_raw = Image.open(os.path.join(ASSETS_DIR, "office_cabin_bg.jpg")).convert("RGB")
bg_img = bg_raw.resize((W, H), Image.Resampling.LANCZOS)

# Employee Cutout
emp_img_raw = Image.open(os.path.join(ASSETS_DIR, "employee_cutout.png")).convert("RGBA")
# Crop tight
emp_bbox = emp_img_raw.getbbox()
emp_cropped = emp_img_raw.crop(emp_bbox)
# Target height ~920
target_h_emp = 920
emp_w = int(emp_cropped.width * (target_h_emp / emp_cropped.height))
emp_main = emp_cropped.resize((emp_w, target_h_emp), Image.Resampling.LANCZOS)

# Manager Poses
mgr_poses = []
for p_idx in [1, 0, 3]: # Pose 1: pointing, Pose 0: neutral, Pose 3: stern
    mgr_path = os.path.join(ASSETS_DIR, f"manager_pose_{p_idx}_rgba.png")
    mgr_raw = Image.open(mgr_path).convert("RGBA")
    m_bbox = mgr_raw.getbbox()
    m_cropped = mgr_raw.crop(m_bbox)
    target_h_mgr = 880
    mw = int(m_cropped.width * (target_h_mgr / m_cropped.height))
    mgr_scaled = m_cropped.resize((mw, target_h_mgr), Image.Resampling.LANCZOS)
    mgr_poses.append(mgr_scaled)

print("Character assets successfully loaded & scaled.")

# --- 3. Zero-Overflow Card & Text Rendering Utilities ---

def draw_safe_box(draw, x0, y0, x1, y1, fill_color, outline_color=None, width=2, radius=16):
    """Draws rounded rectangle strictly clamped inside [x0, y0, x1, y1] with zero border bleed."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill_color, outline=outline_color, width=width)

def draw_wrapped_words(draw, text, x0, y0, max_w, font, text_color, line_h=38):
    """Wraps words strictly within max_w and returns the final y coordinate. Zero word cutoff."""
    words = text.split()
    lines = []
    cur_line = []
    for w in words:
        test = " ".join(cur_line + [w])
        bbox = draw.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= max_w or not cur_line:
            cur_line.append(w)
        else:
            lines.append(" ".join(cur_line))
            cur_line = [w]
    if cur_line:
        lines.append(" ".join(cur_line))
    
    y = y0
    for l in lines:
        draw.text((x0, y), l, font=font, fill=text_color)
        y += line_h
    return y, len(lines)

def render_safe_subtitle_box(draw, speaker_label, char_name, sub_text, y_bottom=1790):
    """
    Renders dynamic auto-sized subtitle box.
    Guarantees words NEVER overflow the box, with 36px horizontal padding.
    """
    pad_x = 36
    pad_y = 20
    box_w = 960
    box_x0 = (W - box_w) // 2
    box_x1 = box_x0 + box_w
    avail_w = box_w - (pad_x * 2)

    # Word wrapping
    words = sub_text.split()
    lines = []
    cur_line = []
    for w in words:
        test = " ".join(cur_line + [w])
        bbox = draw.textbbox((0, 0), test, font=FONT_SUB_MAIN)
        if (bbox[2] - bbox[0]) <= avail_w or not cur_line:
            cur_line.append(w)
        else:
            lines.append(" ".join(cur_line))
            cur_line = [w]
    if cur_line:
        lines.append(" ".join(cur_line))

    line_h = 42
    text_total_h = len(lines) * line_h
    box_h = pad_y * 2 + text_total_h + 24
    box_y0 = y_bottom - box_h
    box_y1 = y_bottom

    # Card background (Deep glassmorphism dark navy)
    outline_col = (99, 102, 241) if char_name == "aryan" else (239, 68, 68)
    draw_safe_box(draw, box_x0, box_y0, box_x1, box_y1, (15, 23, 42), outline_color=outline_col, width=3, radius=20)

    # Speaker Pill Badge
    badge_bg = (79, 70, 229) if char_name == "aryan" else (220, 38, 38)
    badge_bbox = draw.textbbox((0, 0), speaker_label, font=FONT_SUB_TAG)
    badge_w = (badge_bbox[2] - badge_bbox[0]) + 28
    draw_safe_box(draw, box_x0 + 20, box_y0 - 16, box_x0 + 20 + badge_w, box_y0 + 20, badge_bg, radius=10)
    draw.text((box_x0 + 34, box_y0 - 11), speaker_label, font=FONT_SUB_TAG, fill=(255, 255, 255))

    # Render wrapped lines centered
    text_y = box_y0 + pad_y + 12
    for l in lines:
        l_bbox = draw.textbbox((0, 0), l, font=FONT_SUB_MAIN)
        l_w = l_bbox[2] - l_bbox[0]
        l_x = box_x0 + (box_w - l_w) // 2
        draw.text((l_x, text_y), l, font=FONT_SUB_MAIN, fill=(255, 255, 255))
        text_y += line_h

# --- 4. Dynamic Kinetic Whiteboard / Corporate Cards ---

def draw_corporate_dilemma_card(draw, scene_id, rel_t):
    """
    Renders top kinetic corporate cards with zero border bleed and clear narrative punch.
    Outer Card: x=65..1015, y=140..780
    """
    CX0, CY0, CX1, CY1 = 65, 140, 1015, 780
    
    # Base clear white canvas
    draw_safe_box(draw, CX0, CY0, CX1, CY1, (255, 255, 255), outline_color=(203, 213, 225), width=3, radius=22)

    # Inner padding coordinates
    ix0 = CX0 + 28
    iy0 = CY0 + 24
    inner_w = (CX1 - CX0) - 56

    if scene_id == "scene1_hook":
        # Header Badge
        draw_safe_box(draw, ix0, iy0, ix0 + 380, iy0 + 44, (238, 242, 255), outline_color=(99, 102, 241), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "CORPORATE DRAMA • EPISODE 1", font=FONT_BADGE, fill=(67, 56, 202))

        draw.text((ix0, iy0 + 60), "LALA COMPANY APPRAISAL DAY", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "2 Saal Hard Work Ka Sach...", font=FONT_CARD_BODY, fill=(100, 116, 139))

        # Item 1 pops at 0.5s
        if rel_t >= 0.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 245, (248, 250, 252), outline_color=(226, 232, 240), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 115, iy0 + 196, (224, 231, 255), radius=6)
            draw.text((ix0 + 24, iy0 + 172), "ROLE", font=FONT_BADGE, fill=(67, 56, 202))
            draw.text((ix0 + 125, iy0 + 172), "Senior Software Engineer (Aryan)", font=FONT_CARD_BOLD, fill=(30, 41, 59))
            draw.text((ix0 + 20, iy0 + 208), "Track Record: 100% On-time delivery & client praised", font=FONT_CARD_BODY, fill=(71, 85, 105))

        # Item 2 pops at 2.5s
        if rel_t >= 2.5:
            draw_safe_box(draw, ix0, iy0 + 265, ix0 + inner_w, iy0 + 355, (254, 249, 195), outline_color=(234, 179, 8), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 278, ix0 + 115, iy0 + 306, (254, 240, 138), radius=6)
            draw.text((ix0 + 22, iy0 + 282), "GOAL", font=FONT_BADGE, fill=(161, 98, 7))
            draw.text((ix0 + 125, iy0 + 282), "Market Standard 20-30% Increment", font=FONT_CARD_BOLD, fill=(161, 98, 7))
            draw.text((ix0 + 20, iy0 + 318), "EMI, Rent & Family Dependents on this Appraisal", font=FONT_CARD_BODY, fill=(133, 77, 14))

        # Item 3 pops at 5.0s
        if rel_t >= 5.0:
            draw_safe_box(draw, ix0, iy0 + 375, ix0 + inner_w, iy0 + 475, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 388, ix0 + 125, iy0 + 416, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 392), "ALERT", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 135, iy0 + 392), "Summon: 'Cabin Mein Aao Abhi!'", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 430), "Manager Mr. Sharma called into closed cabin...", font=FONT_CARD_BODY, fill=(153, 27, 27))

    elif scene_id == "scene2_manager_gaslight":
        # Header Badge
        draw_safe_box(draw, ix0, iy0, ix0 + 340, iy0 + 44, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "THE TOXIC GASLIGHT TRAP", font=FONT_BADGE, fill=(185, 28, 28))

        draw.text((ix0, iy0 + 60), "MANAGER'S VERDICT: 0% HIKE!", font=FONT_CARD_TITLE, fill=(185, 28, 28))
        draw.text((ix0, iy0 + 108), "Classic excuses used to deny appraisal:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        # Gaslight 1 pops at 1.5s
        if rel_t >= 1.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 245, (255, 247, 237), outline_color=(249, 115, 22), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 85, iy0 + 196, (254, 215, 170), radius=6)
            draw.text((ix0 + 24, iy0 + 172), "[X]", font=FONT_BADGE, fill=(194, 65, 12))
            draw.text((ix0 + 95, iy0 + 172), "Excuse 1: 'Ownership Missing Hai!'", font=FONT_CARD_BOLD, fill=(194, 65, 12))
            draw.text((ix0 + 20, iy0 + 208), "Translation: 14 ghante kaam ke baad bhi loyalty ka drama", font=FONT_CARD_BODY, fill=(154, 52, 18))

        # Gaslight 2 pops at 6.0s
        if rel_t >= 6.0:
            draw_safe_box(draw, ix0, iy0 + 265, ix0 + inner_w, iy0 + 355, (255, 247, 237), outline_color=(249, 115, 22), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 278, ix0 + 85, iy0 + 306, (254, 215, 170), radius=6)
            draw.text((ix0 + 24, iy0 + 282), "[X]", font=FONT_BADGE, fill=(194, 65, 12))
            draw.text((ix0 + 95, iy0 + 282), "Excuse 2: 'Global Market Bahut Down Hai!'", font=FONT_CARD_BOLD, fill=(194, 65, 12))
            draw.text((ix0 + 20, iy0 + 318), "Client budget cuts ka bahana dekar mehnat ka paisa dabana", font=FONT_CARD_BODY, fill=(154, 52, 18))

        # Gaslight 3 pops at 10.5s
        if rel_t >= 10.5:
            draw_safe_box(draw, ix0, iy0 + 375, ix0 + inner_w, iy0 + 475, (254, 242, 242), outline_color=(220, 38, 38), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 388, ix0 + 115, iy0 + 416, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 392), "TRAP", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 125, iy0 + 392), "'Toh Is Saal Appraisal Bhool Jao!'", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 430), "Pure 2 saal ki mehnat par ek minute mein paani phera!", font=FONT_CARD_BODY, fill=(153, 27, 27))

    elif scene_id == "scene3_employee_shock":
        # Header Badge
        draw_safe_box(draw, ix0, iy0, ix0 + 350, iy0 + 44, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "EMPLOYEE EVIDENCE & FACTS", font=FONT_BADGE, fill=(21, 128, 61))

        draw.text((ix0, iy0 + 60), "THE BITTER REALITY (FACTS)", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "Aryan presents hard proof on the table:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        # Fact 1 pops at 1.0s
        if rel_t >= 1.0:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 245, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 95, iy0 + 196, (187, 247, 208), radius=6)
            draw.text((ix0 + 24, iy0 + 172), "FACT 1", font=FONT_BADGE, fill=(21, 128, 61))
            draw.text((ix0 + 105, iy0 + 172), "6 Months: Har Weekend 14 Ghante Login Kiya!", font=FONT_CARD_BOLD, fill=(21, 128, 61))
            draw.text((ix0 + 20, iy0 + 208), "No overtime pay, personal life sacrificed completely", font=FONT_CARD_BODY, fill=(22, 101, 52))

        # Fact 2 pops at 4.2s
        if rel_t >= 4.2:
            draw_safe_box(draw, ix0, iy0 + 265, ix0 + inner_w, iy0 + 355, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 278, ix0 + 95, iy0 + 306, (187, 247, 208), radius=6)
            draw.text((ix0 + 24, iy0 + 282), "FACT 2", font=FONT_BADGE, fill=(21, 128, 61))
            draw.text((ix0 + 105, iy0 + 282), "Client Appreciation: 'Best Engineer in Team'", font=FONT_CARD_BOLD, fill=(21, 128, 61))
            draw.text((ix0 + 20, iy0 + 318), "Direct appreciation email from US client manager", font=FONT_CARD_BODY, fill=(22, 101, 52))

        # Fact 3 pops at 7.5s
        if rel_t >= 7.5:
            draw_safe_box(draw, ix0, iy0 + 375, ix0 + inner_w, iy0 + 475, (254, 249, 195), outline_color=(234, 179, 8), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 388, ix0 + 115, iy0 + 416, (254, 240, 138), radius=6)
            draw.text((ix0 + 22, iy0 + 392), "QUERY", font=FONT_BADGE, fill=(161, 98, 7))
            draw.text((ix0 + 125, iy0 + 392), "Aur Ab 'Market Down' Ka Bahana?!", font=FONT_CARD_BOLD, fill=(161, 98, 7))
            draw.text((ix0 + 20, iy0 + 430), "Kya ek honest engineer ki koi value nahi hai?", font=FONT_CARD_BODY, fill=(133, 77, 14))

    elif scene_id == "scene4_manager_ultimatum":
        # Header Badge
        draw_safe_box(draw, ix0, iy0, ix0 + 320, iy0 + 44, (254, 242, 242), outline_color=(220, 38, 38), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "THE TOXIC ULTIMATUM", font=FONT_BADGE, fill=(185, 28, 28))

        draw.text((ix0, iy0 + 60), "MANAGER'S DEADLINE: 2 CHOICES", font=FONT_CARD_TITLE, fill=(185, 28, 28))
        draw.text((ix0, iy0 + 108), "Blank paper pushed across the desk:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        # Option A pops at 1.0s
        if rel_t >= 1.0:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 255, (255, 247, 237), outline_color=(234, 88, 12), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 115, iy0 + 196, (254, 215, 170), radius=6)
            draw.text((ix0 + 22, iy0 + 172), "CHOICE A", font=FONT_BADGE, fill=(194, 65, 12))
            draw.text((ix0 + 125, iy0 + 172), "Ghuto Aur Kaam Karo!", font=FONT_CARD_BOLD, fill=(194, 65, 12))
            draw.text((ix0 + 20, iy0 + 210), "0% Hike par 14 ghante kaam karte raho chup-chaap", font=FONT_CARD_BODY, fill=(154, 52, 18))

        # Option B pops at 6.0s
        if rel_t >= 6.0:
            draw_safe_box(draw, ix0, iy0 + 275, ix0 + inner_w, iy0 + 375, (254, 242, 242), outline_color=(220, 38, 38), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 288, ix0 + 115, iy0 + 316, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 292), "CHOICE B", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 125, iy0 + 292), "Resignation Dalo Aur Niklo!", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 330), "Table par resignation rakho aur 90 din notice kaato", font=FONT_CARD_BODY, fill=(153, 27, 27))

        # Warning pops at 10.0s
        if rel_t >= 10.0:
            draw_safe_box(draw, ix0, iy0 + 395, ix0 + inner_w, iy0 + 475, (254, 249, 195), outline_color=(234, 179, 8), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 408, ix0 + 105, iy0 + 436, (254, 240, 138), radius=6)
            draw.text((ix0 + 22, iy0 + 412), "THREAT", font=FONT_BADGE, fill=(161, 98, 7))
            draw.text((ix0 + 115, iy0 + 412), "'Market mein job nahi hai... Soch lo!'", font=FONT_CARD_BOLD, fill=(161, 98, 7))

    elif scene_id == "scene5_cliffhanger":
        # Header Badge
        draw_safe_box(draw, ix0, iy0, ix0 + 330, iy0 + 44, (241, 245, 249), outline_color=(100, 116, 139), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "THE MORAL DILEMMA", font=FONT_BADGE, fill=(51, 65, 85))

        draw.text((ix0, iy0 + 60), "EMI KA DARR vs SELF-RESPECT", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "Har middle class employee ki asli majboori:", font=FONT_CARD_BODY, fill=(100, 116, 139))

        # Side A pops at 0.5s
        if rel_t >= 0.5:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 275, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 125, iy0 + 196, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 172), "EXPENSE", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 135, iy0 + 172), "Home Loan EMI + Ghar Ka Kharcha:", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 215), "Rs 45,000 Har Mahine Account Se Katna Hai", font=FONT_CARD_TITLE, fill=(220, 38, 38))

        # Side B pops at 3.2s
        if rel_t >= 3.2:
            draw_safe_box(draw, ix0, iy0 + 295, ix0 + inner_w, iy0 + 415, (254, 249, 195), outline_color=(202, 138, 4), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 308, ix0 + 125, iy0 + 336, (254, 240, 138), radius=6)
            draw.text((ix0 + 22, iy0 + 312), "DIGNITY", font=FONT_BADGE, fill=(161, 98, 7))
            draw.text((ix0 + 135, iy0 + 312), "Aur Doosri Taraf:", font=FONT_CARD_BOLD, fill=(161, 98, 7))
            draw.text((ix0 + 20, iy0 + 355), "Meri Self-Respect Ki Nilami Ho Rahi Thi...", font=FONT_CARD_TITLE, fill=(133, 77, 14))

    elif scene_id == "scene6_audience_question":
        # Header Badge
        draw_safe_box(draw, ix0, iy0, ix0 + 370, iy0 + 44, (238, 242, 255), outline_color=(99, 102, 241), width=2, radius=10)
        draw.text((ix0 + 16, iy0 + 10), "QUESTION FOR AUDIENCE • VOTE", font=FONT_BADGE, fill=(67, 56, 202))

        draw.text((ix0, iy0 + 60), "AGAR MERI JAGAH TUM HOTE...", font=FONT_CARD_TITLE, fill=(15, 23, 42))
        draw.text((ix0, iy0 + 108), "Toh tum kya faisla lete?", font=FONT_CARD_BODY, fill=(100, 116, 139))

        # Option 1 pops at 1.0s
        if rel_t >= 1.0:
            draw_safe_box(draw, ix0, iy0 + 155, ix0 + inner_w, iy0 + 245, (254, 242, 242), outline_color=(239, 68, 68), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 168, ix0 + 115, iy0 + 196, (254, 202, 202), radius=6)
            draw.text((ix0 + 22, iy0 + 172), "OPTION A", font=FONT_BADGE, fill=(185, 28, 28))
            draw.text((ix0 + 125, iy0 + 172), "EMI Ke Darr Se Chup-Chaap Seh Lete?", font=FONT_CARD_BOLD, fill=(185, 28, 28))
            draw.text((ix0 + 20, iy0 + 208), "Paisa zaroori hai, majboori mein compromise karte", font=FONT_CARD_BODY, fill=(153, 27, 27))

        # Option 2 pops at 4.0s
        if rel_t >= 4.0:
            draw_safe_box(draw, ix0, iy0 + 265, ix0 + inner_w, iy0 + 355, (240, 253, 244), outline_color=(34, 197, 94), width=2, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 278, ix0 + 115, iy0 + 306, (187, 247, 208), radius=6)
            draw.text((ix0 + 22, iy0 + 282), "OPTION B", font=FONT_BADGE, fill=(21, 128, 61))
            draw.text((ix0 + 125, iy0 + 282), "Resignation Dete Aur Self-Respect Chunte?", font=FONT_CARD_BOLD, fill=(21, 128, 61))
            draw.text((ix0 + 20, iy0 + 318), "Aatmasamman pehle hai, aage jo hoga dekha jayega", font=FONT_CARD_BODY, fill=(22, 101, 52))

        # Outro Part 2 Hook pops at 7.5s
        if rel_t >= 7.5:
            draw_safe_box(draw, ix0, iy0 + 375, ix0 + inner_w, iy0 + 475, (245, 243, 255), outline_color=(147, 51, 234), width=3, radius=14)
            draw_safe_box(draw, ix0 + 16, iy0 + 388, ix0 + 105, iy0 + 416, (233, 213, 255), radius=6)
            draw.text((ix0 + 22, iy0 + 392), "ACTION", font=FONT_BADGE, fill=(126, 34, 206))
            draw.text((ix0 + 115, iy0 + 392), "COMMENT APNA ANSWER (A ya B?)", font=FONT_CARD_TITLE, fill=(126, 34, 206))
            draw.text((ix0 + 20, iy0 + 432), "Maine Kya Faisla Liya... DEKHO PART 2 MEIN!", font=FONT_CARD_BOLD, fill=(109, 40, 217))

# --- 5. Natural Lip-Sync & Viseme Drawer ---

def get_audio_rms_at_time(scene_id, rel_t):
    """Computes exact audio RMS power at current timestamp."""
    item = audio_data_dict[scene_id]
    data = item["data"]
    sr = item["sr"]
    idx = int(rel_t * sr)
    window_size = int(0.04 * sr) # 40ms window
    if idx < 0 or idx >= len(data):
        return 0.0
    start = max(0, idx - window_size // 2)
    end = min(len(data), idx + window_size // 2)
    chunk = data[start:end]
    if len(chunk) == 0:
        return 0.0
    rms = np.sqrt(np.mean(chunk**2))
    return float(rms)

def draw_natural_mouth(draw, cx, cy, rms, is_speaking, char_name):
    """
    Renders 4-viseme natural lip-sync based on real-time audio RMS energy.
    When not speaking: keep original character face clean (no red line).
    When speaking: first cover mouth area with skin tone, then draw viseme!
    """
    if not is_speaking or rms < 0.015:
        return

    skin_col = (205, 142, 102) if char_name == "aryan" else (186, 134, 104)
    lip_col = (110, 40, 48) if char_name == "aryan" else (90, 32, 40)

    # First clean the static mouth area with smooth skin patch
    draw.rounded_rectangle([cx - 20, cy - 8, cx + 20, cy + 8], radius=6, fill=skin_col)

    # Speaking visemes based on RMS amplitude
    if rms > 0.065:
        # AH - Wide Open Vowel
        draw.ellipse([cx - 15, cy - 12, cx + 15, cy + 12], fill=(30, 15, 20))
        # Top teeth
        draw.rectangle([cx - 9, cy - 11, cx + 9, cy - 5], fill=(245, 245, 250))
        # Pink tongue
        draw.ellipse([cx - 10, cy + 2, cx + 10, cy + 11], fill=(225, 95, 115))
        # Lips outline
        draw.ellipse([cx - 16, cy - 13, cx + 16, cy + 13], outline=lip_col, width=2)
    elif rms > 0.035:
        # OH - Round Open
        draw.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(30, 15, 20))
        draw.rectangle([cx - 7, cy - 9, cx + 7, cy - 5], fill=(245, 245, 250))
        draw.ellipse([cx - 7, cy + 2, cx + 7, cy + 9], fill=(225, 95, 115))
        draw.ellipse([cx - 12, cy - 11, cx + 12, cy + 11], outline=lip_col, width=2)
    else:
        # EE - Semi-Open / Smile Vowel
        draw.ellipse([cx - 15, cy - 5, cx + 15, cy + 5], fill=(30, 15, 20))
        draw.rectangle([cx - 11, cy - 4, cx + 11, cy + 1], fill=(245, 245, 250))
        draw.ellipse([cx - 16, cy - 6, cx + 16, cy + 6], outline=lip_col, width=2)

# --- 6. Master Video Rendering Loop ---
print("--- Starting Master Kinetic Video Render via FFmpeg Pipe ---")

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

# Active scene tracker
scene_idx = 0
active_cue = timeline[0]

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS

    # Update active cue
    while scene_idx < len(timeline) - 1 and t >= timeline[scene_idx]["end"]:
        scene_idx += 1
    active_cue = timeline[scene_idx]
    scene_id = active_cue["id"]
    rel_t = t - active_cue["start"]
    speaking_char = active_cue["char"]

    # Clone base background
    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame)

    # 6.1 Top Whiteboard / Dilemma Card
    draw_corporate_dilemma_card(draw, scene_id, rel_t)

    # 6.2 Character Placements & Animation
    # Aryan parameters
    is_aryan_speaking = (speaking_char == "aryan")
    is_mgr_speaking = (speaking_char == "sharma")
    
    # Aryan Walk-in Entrance during Scene 1
    if scene_id == "scene1_hook":
        walk_dur = 3.5
        if rel_t < walk_dur:
            progress = rel_t / walk_dur
            aryan_x = int(-200 + (130 - (-200)) * progress)
            # Walking vertical bounce
            aryan_y = 800 - int(abs(math.sin(rel_t * 9.0)) * 14)
        else:
            aryan_x = 130
            aryan_y = 800 + int(math.sin(rel_t * 2.5) * 3) # subtle breathing
    elif scene_id == "scene3_employee_shock":
        # Aryan steps closer to table
        aryan_x = 160
        aryan_y = 795 + int(math.sin(rel_t * 3.0) * 3)
    elif scene_id in ["scene5_cliffhanger", "scene6_audience_question"]:
        # Aryan centered / addressing audience directly
        aryan_x = 210
        aryan_y = 790 + int(math.sin(rel_t * 2.5) * 3)
    else:
        aryan_x = 130
        aryan_y = 800 + int(math.sin(rel_t * 2.5) * 3)

    # Manager parameters
    mgr_x = 610
    mgr_y = 830 + int(math.sin(rel_t * 2.0) * 2)

    # Select manager pose
    if scene_id in ["scene2_manager_gaslight", "scene4_manager_ultimatum"]:
        mgr_sprite = mgr_poses[0] # Pointing / aggressive pose
    elif scene_id == "scene3_employee_shock":
        mgr_sprite = mgr_poses[2] # Stern listening pose
    else:
        mgr_sprite = mgr_poses[1] # Neutral desk pose

    # Overlay Manager onto background
    frame.paste(mgr_sprite, (mgr_x, mgr_y), mgr_sprite)

    # Overlay Aryan onto background
    frame.paste(emp_main, (aryan_x, aryan_y), emp_main)

    # 6.3 Lip-Sync & Face Detailing
    rms_val = get_audio_rms_at_time(scene_id, rel_t)

    # Exact Aryan mouth position:
    aryan_mouth_cx = aryan_x + 138
    aryan_mouth_cy = aryan_y + 118

    # Exact Manager mouth position:
    mgr_mouth_cx = mgr_x + 150
    mgr_mouth_cy = mgr_y + 158

    # Draw mouths
    draw_natural_mouth(draw, aryan_mouth_cx, aryan_mouth_cy, rms_val, is_aryan_speaking, "aryan")
    draw_natural_mouth(draw, mgr_mouth_cx, mgr_mouth_cy, rms_val, is_mgr_speaking, "sharma")

    # Natural Eye Blinking (every 3.8s for 4 frames)
    blink_cycle = (f_idx % 114) # ~3.8s at 30fps
    if blink_cycle < 4:
        # Blink Aryan eyes
        draw.line([aryan_mouth_cx - 36, aryan_mouth_cy - 45, aryan_mouth_cx - 16, aryan_mouth_cy - 45], fill=(30, 20, 25), width=3)
        draw.line([aryan_mouth_cx + 16, aryan_mouth_cy - 45, aryan_mouth_cx + 36, aryan_mouth_cy - 45], fill=(30, 20, 25), width=3)
        # Blink Manager eyes
        draw.line([mgr_mouth_cx - 28, mgr_mouth_cy - 42, mgr_mouth_cx - 10, mgr_mouth_cy - 42], fill=(30, 20, 25), width=3)
        draw.line([mgr_mouth_cx + 10, mgr_mouth_cy - 42, mgr_mouth_cx + 28, mgr_mouth_cy - 42], fill=(30, 20, 25), width=3)

    # 6.4 Top Progress Bar (0 to 1080px)
    pct = t / total_duration
    draw.rectangle([0, 0, W, 8], fill=(226, 232, 240))
    draw.rectangle([0, 0, int(W * pct), 8], fill=(99, 102, 241))

    # 6.5 Safe Dynamic Subtitle Box (ZERO OVERFLOW)
    speaker_tag = active_cue["speaker"]
    sub_text = active_cue["sub"]
    render_safe_subtitle_box(draw, speaker_tag, speaking_char, sub_text, y_bottom=1780)

    # Pipe frame to FFmpeg
    pipe.stdin.write(frame.tobytes())

    # Save representative snapshots
    if f_idx in [60, 350, 750, 1150, 1500, 1850]:
        snap_p = os.path.join(SNAPSHOT_DIR, f"master_snap_{f_idx}.jpg")
        frame.save(snap_p)
        print(f"Saved snapshot {snap_p} at frame {f_idx} (t={t:.1f}s)")

    if f_idx % 300 == 0:
        print(f"Rendered {f_idx}/{TOTAL_FRAMES} frames ({f_idx*100/TOTAL_FRAMES:.1f}%)")

pipe.stdin.close()
pipe.wait()
print(f"Video stream rendered: {TEMP_VIDEO}")

# --- 7. Mux Video & Audio Master ---
print("--- Muxing Master Broadcast Reel ---")
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
print(f"Master Broadcast Reel Successfully Generated: {OUTPUT_VIDEO}")

# Clean up temp files
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

print("ALL PROCESSES COMPLETED CLEANLY.")
