import os
import sys
import json
import math
import subprocess
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

MASTER_AUDIO = os.path.join(AUDIO_DIR, "master_audio_track.wav")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "free_fullstack_master_reel.mp4")

with open(os.path.join(BASE_DIR, "timing_metadata.json"), "r") as f:
    timing = json.load(f)

TOTAL_DUR = timing["total_duration"]
SCENE_STARTS = timing["scene_starts"]
SCENE_DURS = timing["scene_durations"]
FPS = 30
TOTAL_FRAMES = int(TOTAL_DUR * FPS)
WIDTH, HEIGHT = 1080, 1920

def get_font(name="segoeuib.ttf", size=32):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

FONT_TITLE = get_font("segoeuib.ttf", 46)
FONT_SUBTITLE = get_font("segoeui.ttf", 30)
FONT_CARD_TITLE = get_font("segoeuib.ttf", 36)
FONT_BODY = get_font("segoeui.ttf", 28)
FONT_BOLD = get_font("segoeuib.ttf", 30)
FONT_SUBTITLE_TEXT = get_font("segoeuib.ttf", 32)

# High-visibility terminal fonts
FONT_TERM_CMD = get_font("consolas.ttf", 40)
FONT_TERM_OUT = get_font("consolas.ttf", 32)
FONT_TERM_BOX = get_font("consolas.ttf", 34)

FONT_BADGE = get_font("segoeuib.ttf", 24)
FONT_HUD = get_font("segoeuib.ttf", 26)

SCENE_SUBTITLES = [
    [
        "Agar tum abhi bhi Render ya Heroku par project host kar rahe ho,",
        "toh server 15 minute mein so jata hai aur portfolio kharab lagta hai!",
        "Aur AWS ya Vercel par surprise billing ka darr rehta hai."
    ],
    [
        "Toh ye hai 2026 ka zero rupee Lifetime Architecture!",
        "Frontend ke liye istemaal karo Cloudflare Pages.",
        "Jahan milti hai Unlimited Bandwidth aur free custom domain!"
    ],
    [
        "Database ke liye istemaal karo Supabase ya Neon DB,",
        "jahan milta hai free serverless PostgreSQL.",
        "Aur backend API ke liye Cloudflare Workers free mein!"
    ],
    [
        "Server ko 24 ghante jagaye rakhne ke liye,",
        "cron-job.org se ek free 10-minute automated ping laga do.",
        "Tumhara server kabhi nahi soyega aur 20 hazaar rupaye bachenge!"
    ],
    [
        "Is architecture ka ready GitHub starter template chahiye?",
        "Toh comment karo STACK, main direct DM bhej dunga!",
        "Aur follow karna mat bhoolna!"
    ]
]

def draw_badge(draw, x, y, text, fill_color, text_color=(255, 255, 255)):
    bbox = draw.textbbox((0, 0), text, font=FONT_BADGE)
    w = bbox[2] - bbox[0] + 36
    h = 44
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=fill_color)
    draw.text((x + 18, y + 8), text, fill=text_color, font=FONT_BADGE)
    return w, h

def draw_hud(draw, chapter_text, step_text):
    # Top HUD Bar (y=65 to 120)
    ch_box = draw.textbbox((0, 0), chapter_text, font=FONT_HUD)
    ch_w = ch_box[2] - ch_box[0] + 36
    draw.rounded_rectangle([60, 65, 60 + ch_w, 120], radius=14, fill=(255, 210, 30))
    draw.text((78, 77), chapter_text, fill=(15, 23, 42), font=FONT_HUD)
    
    center_text = "₹0 FULL-STACK ARCHITECTURE"
    c_box = draw.textbbox((0, 0), center_text, font=FONT_HUD)
    c_w = c_box[2] - c_box[0] + 36
    c_x = 60 + ch_w + 15
    draw.rounded_rectangle([c_x, 65, c_x + c_w, 120], radius=14, fill=(15, 25, 45, 240), outline=(0, 210, 255), width=2)
    draw.text((c_x + 18, 77), center_text, fill=(0, 210, 255), font=FONT_HUD)
    
    st_box = draw.textbbox((0, 0), step_text, font=FONT_HUD)
    st_w = st_box[2] - st_box[0] + 36
    st_x = 1020 - st_w
    draw.rounded_rectangle([st_x, 65, 1020, 120], radius=14, fill=(30, 41, 59, 240), outline=(148, 163, 184), width=2)
    draw.text((st_x + 18, 77), step_text, fill=(241, 245, 249), font=FONT_HUD)

def draw_subtitle_box(draw, lines, active_word=""):
    draw.rounded_rectangle([60, 1660, 1020, 1835], radius=24, fill=(11, 17, 32, 245), outline=(0, 229, 153), width=2)
    
    max_w = 900
    display_lines = []
    for raw_l in lines[:2]:
        words = raw_l.split()
        cur_l = []
        for w in words:
            test_l = " ".join(cur_l + [w])
            bbox = draw.textbbox((0, 0), test_l, font=FONT_SUBTITLE_TEXT)
            if bbox[2] - bbox[0] <= max_w:
                cur_l.append(w)
            else:
                display_lines.append(" ".join(cur_l))
                cur_l = [w]
        if cur_l:
            display_lines.append(" ".join(cur_l))
            
    y_offset = 1685 if len(display_lines) >= 2 else 1720
    for l_text in display_lines[:2]:
        words = l_text.split()
        line_w = sum(draw.textbbox((0, 0), w + " ", font=FONT_SUBTITLE_TEXT)[2] for w in words)
        start_x = max(80, (1080 - line_w) // 2)
        
        cur_x = start_x
        for w in words:
            w_box = draw.textbbox((0, 0), w, font=FONT_SUBTITLE_TEXT)
            w_w = w_box[2] - w_box[0]
            space_w = draw.textbbox((0, 0), " ", font=FONT_SUBTITLE_TEXT)[2]
            
            clean_w = w.lower().strip("!?,.")
            if active_word and clean_w == active_word.lower():
                draw.rounded_rectangle([cur_x - 6, y_offset - 4, cur_x + w_w + 6, y_offset + 38], radius=8, fill=(255, 210, 30))
                draw.text((cur_x, y_offset), w, fill=(15, 23, 42), font=FONT_SUBTITLE_TEXT)
            else:
                draw.text((cur_x, y_offset), w, fill=(255, 255, 255), font=FONT_SUBTITLE_TEXT)
            cur_x += w_w + space_w
        y_offset += 52

def render_frame_for_time(t):
    img = Image.new("RGBA", (1080, 1920), (10, 15, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Subtle background cyber grid
    for gx in range(0, 1080, 120):
        draw.line([(gx, 0), (gx, 1920)], fill=(20, 30, 50, 40), width=1)
    for gy in range(0, 1920, 120):
        draw.line([(0, gy), (1080, gy)], fill=(20, 30, 50, 40), width=1)
        
    scene_starts = SCENE_STARTS
    scene_durs = SCENE_DURS
    
    if t < scene_starts[1]:
        # Scene 1: The Cold Start Trap
        rel_t = t - scene_starts[0]
        draw_hud(draw, "// 01 · CLOUD TRAP", "STEP 1/5")
        
        # Primary Alert Card
        draw.rounded_rectangle([60, 200, 1020, 840], radius=28, fill=(22, 18, 28, 240), outline=(239, 68, 68), width=2)
        draw_badge(draw, 95, 235, "CRITICAL ALERT", fill_color=(239, 68, 68))
        
        draw.text((95, 305), "THE 15-MINUTE SLEEP TRAP", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "Why free hosting tiers ruin your portfolio:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        draw.rounded_rectangle([95, 430, 985, 520], radius=16, fill=(35, 20, 28), outline=(239, 68, 68, 120), width=1)
        draw.text((120, 455), "[!]  15-Min Inactivity: Server automatically spins down to 0", fill=(254, 202, 202), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 540, 985, 630], radius=16, fill=(35, 20, 28), outline=(239, 68, 68, 120), width=1)
        draw.text((120, 565), "[WAIT] 50+ Seconds Cold Start: Recruiter clicks and leaves!", fill=(254, 202, 202), font=FONT_BODY)
        
        # Dynamic Animated Loading Bar (grows over time)
        load_pct = min(0.85, 0.2 + (rel_t / scene_durs[0]) * 0.65)
        bar_w = int(95 + (985 - 95) * load_pct)
        draw.text((95, 660), f"Portfolio Loading Experience (~50s Delay):", fill=(148, 163, 184), font=FONT_BODY)
        draw.rounded_rectangle([95, 705, 985, 745], radius=12, fill=(30, 41, 59))
        draw.rounded_rectangle([95, 705, bar_w, 745], radius=12, fill=(239, 68, 68))
        draw.text((95, 765), f"Spin-down status: 52s delay (Visitor bounces away!)", fill=(239, 68, 68), font=FONT_BOLD)
        
        # Secondary Risk Card
        draw.rounded_rectangle([60, 875, 1020, 1480], radius=28, fill=(20, 24, 38, 240), outline=(245, 158, 11), width=2)
        draw_badge(draw, 95, 910, "SURPRISE BILLING RISK", fill_color=(245, 158, 11), text_color=(15, 23, 42))
        
        draw.text((95, 975), "AWS & VERCEL BILLING TRAP", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 1040), "Accidental loops or bot traffic trigger massive bills:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        draw.rounded_rectangle([95, 1105, 985, 1215], radius=18, fill=(38, 30, 20), outline=(245, 158, 11, 140), width=1)
        draw.text((120, 1125), "Average Surprise Bill: $20 to $120 / Month", fill=(253, 230, 138), font=FONT_CARD_TITLE)
        draw.text((120, 1170), "Credit Card charged automatically without warning!", fill=(251, 191, 36), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 1250, 985, 1410], radius=18, fill=(15, 30, 50), outline=(0, 210, 255, 180), width=2)
        draw.text((120, 1280), "[Q] CAN WE GET 100% FREE LIFETIME HOSTING?", fill=(0, 210, 255), font=FONT_CARD_TITLE)
        draw.text((120, 1335), "Yes! With zero cold starts & 0 surprise bills forever.", fill=(226, 232, 240), font=FONT_BODY)
        
        # Active Karaoke word tracking
        all_words = " ".join(SCENE_SUBTITLES[0]).split()
        active_idx = min(int((rel_t / scene_durs[0]) * len(all_words)), len(all_words) - 1)
        active_word = all_words[active_idx] if all_words else ""
        draw_subtitle_box(draw, SCENE_SUBTITLES[0], active_word=active_word)
        
    elif t < scene_starts[2]:
        # Scene 2: Frontend on Cloudflare Pages
        rel_t = t - scene_starts[1]
        draw_hud(draw, "// 02 · FRONTEND", "STEP 2/5")
        
        draw.rounded_rectangle([60, 200, 1020, 1500], radius=28, fill=(13, 27, 28, 240), outline=(0, 229, 153), width=2)
        draw_badge(draw, 95, 235, "FRONTEND ARCHITECTURE", fill_color=(0, 229, 153), text_color=(10, 25, 20))
        
        draw.text((95, 305), "CLOUDFLARE PAGES (0ms Edge)", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "The ultimate $0 production frontend platform:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        draw.rounded_rectangle([95, 435, 985, 615], radius=20, fill=(18, 38, 38), outline=(0, 229, 153, 120), width=1)
        draw.text((125, 460), "BANDWIDTH & TRAFFIC", fill=(148, 163, 184), font=FONT_BADGE)
        draw.text((125, 500), "UNLIMITED (100% FREE FOREVER)", fill=(0, 229, 153), font=FONT_CARD_TITLE)
        draw.text((125, 555), "No bandwidth caps, no overage fees, 0 surprise bills.", fill=(226, 232, 240), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 645, 985, 825], radius=20, fill=(18, 38, 38), outline=(0, 229, 153, 120), width=1)
        draw.text((125, 670), "COLD START LATENCY", fill=(148, 163, 184), font=FONT_BADGE)
        draw.text((125, 710), "0ms (Instant Global Edge Response)", fill=(0, 210, 255), font=FONT_CARD_TITLE)
        draw.text((125, 765), "Cached across 330+ cities worldwide on Cloudflare CDN.", fill=(226, 232, 240), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 855, 985, 1035], radius=20, fill=(18, 38, 38), outline=(0, 229, 153, 120), width=1)
        draw.text((125, 880), "CUSTOM DOMAIN & SECURITY", fill=(148, 163, 184), font=FONT_BADGE)
        draw.text((125, 920), "FREE CUSTOM DOMAIN + SSL", fill=(255, 210, 30), font=FONT_CARD_TITLE)
        draw.text((125, 975), "Connect your .com / .dev domain in 1-click with DDoS guard.", fill=(226, 232, 240), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 1075, 985, 1430], radius=22, fill=(15, 23, 42), outline=(148, 163, 184, 180), width=2)
        draw.text((125, 1110), "COST COMPARISON:", fill=(255, 255, 255), font=FONT_CARD_TITLE)
        
        draw.text((125, 1175), "Vercel Pro (Bandwidth Overage):", fill=(239, 68, 68), font=FONT_BODY)
        draw.text((700, 1175), "$20 / month", fill=(239, 68, 68), font=FONT_BOLD)
        
        draw.text((125, 1245), "Cloudflare Pages (Unlimited):", fill=(0, 229, 153), font=FONT_BODY)
        draw.text((700, 1245), "$0 / Lifetime", fill=(0, 229, 153), font=FONT_BOLD)
        
        draw.text((125, 1330), "[!] 100% Free Lifetime Hosting without limits!", fill=(255, 210, 30), font=FONT_BOLD)
        
        all_words = " ".join(SCENE_SUBTITLES[1]).split()
        active_idx = min(int((rel_t / scene_durs[1]) * len(all_words)), len(all_words) - 1)
        active_word = all_words[active_idx] if all_words else ""
        draw_subtitle_box(draw, SCENE_SUBTITLES[1], active_word=active_word)
        
    elif t < scene_starts[3]:
        # Scene 3: Backend & Database + Live Typing Terminal
        rel_t = t - scene_starts[2]
        draw_hud(draw, "// 03 · BACKEND & DB", "STEP 3/5")
        
        # Database Card
        draw.rounded_rectangle([60, 200, 1020, 460], radius=24, fill=(18, 24, 40, 240), outline=(0, 210, 255), width=2)
        draw_badge(draw, 95, 230, "DATABASE: SERVERLESS PG", fill_color=(0, 210, 255), text_color=(10, 20, 35))
        
        draw.text((95, 295), "SUPABASE / NEON POSTGRESQL", fill=(255, 255, 255), font=FONT_CARD_TITLE)
        draw.text((95, 350), "500MB Free Database Storage + Instant REST & GraphQL API", fill=(226, 232, 240), font=FONT_BODY)
        draw.text((95, 395), "Auto connection pooling: handles 10,000+ concurrent users!", fill=(0, 229, 153), font=FONT_BOLD)
        
        # macOS Terminal Window
        draw.rounded_rectangle([60, 500, 1020, 1520], radius=24, fill=(12, 16, 24, 255), outline=(51, 65, 85), width=2)
        
        draw.ellipse([95, 535, 119, 559], fill=(255, 95, 86))
        draw.ellipse([132, 535, 156, 559], fill=(255, 189, 46))
        draw.ellipse([169, 535, 193, 559], fill=(39, 201, 63))
        
        draw.text((230, 532), "bash - developer@global-edge: ~/my-api", fill=(148, 163, 184), font=FONT_TERM_OUT)
        draw.line([(60, 580), (1020, 580)], fill=(51, 65, 85), width=1)
        
        # Dynamic Character-by-Character Typing Effect
        cmd1 = "developer@edge:~$ npx wrangler init my-api"
        cmd2 = "developer@edge:~$ npx supabase db push"
        cmd3 = "developer@edge:~$ npm run deploy --prod"
        
        y_t = 615
        # Line 1
        t_c1 = min(1.0, max(0.0, rel_t / 2.5))
        chars1 = int(len(cmd1) * t_c1)
        draw.text((95, y_t), cmd1[:chars1], fill=(0, 229, 153), font=FONT_TERM_CMD)
        y_t += 60
        
        if rel_t > 2.5:
            draw.text((95, y_t), "[OK] Worker ready: 100,000 reqs/day 100% FREE", fill=(241, 245, 249), font=FONT_TERM_OUT)
        y_t += 75
        
        # Line 2
        if rel_t > 3.5:
            t_c2 = min(1.0, max(0.0, (rel_t - 3.5) / 2.5))
            chars2 = int(len(cmd2) * t_c2)
            draw.text((95, y_t), cmd2[:chars2], fill=(0, 229, 153), font=FONT_TERM_CMD)
        y_t += 60
        
        if rel_t > 6.0:
            draw.text((95, y_t), "[OK] Connected to Serverless PostgreSQL on port 5432", fill=(241, 245, 249), font=FONT_TERM_OUT)
        y_t += 75
        
        # Line 3
        if rel_t > 7.0:
            t_c3 = min(1.0, max(0.0, (rel_t - 7.0) / 2.0))
            chars3 = int(len(cmd3) * t_c3)
            draw.text((95, y_t), cmd3[:chars3], fill=(0, 229, 153), font=FONT_TERM_CMD)
        y_t += 70
        
        # Deploy Result Box
        if rel_t > 9.0:
            draw.rounded_rectangle([95, y_t, 985, y_t + 280], radius=16, fill=(18, 28, 42), outline=(0, 229, 153), width=2)
            y_box = y_t + 25
            draw.text((120, y_box), "================================================", fill=(100, 116, 139), font=FONT_TERM_BOX)
            y_box += 42
            draw.text((120, y_box), "[LIVE] STATUS: LIVE ON GLOBAL EDGE NETWORK", fill=(0, 229, 153), font=FONT_TERM_BOX)
            y_box += 48
            draw.text((120, y_box), "[FAST] DEPLOY: 0.42s  |  EDGE: 330+ CITIES", fill=(0, 210, 255), font=FONT_TERM_BOX)
            y_box += 48
            draw.text((120, y_box), "[COST] BILL: $0.00 / MONTH (LIFETIME FREE)", fill=(255, 210, 30), font=FONT_TERM_BOX)
            y_box += 42
            draw.text((120, y_box), "================================================", fill=(100, 116, 139), font=FONT_TERM_BOX)
            
        # Blinking cursor
        cursor_char = "█" if int(rel_t * 2.5) % 2 == 0 else ""
        draw.text((95, y_t + 320), f"developer@edge:~$ {cursor_char}", fill=(0, 229, 153), font=FONT_TERM_CMD)
        
        all_words = " ".join(SCENE_SUBTITLES[2]).split()
        active_idx = min(int((rel_t / scene_durs[2]) * len(all_words)), len(all_words) - 1)
        active_word = all_words[active_idx] if all_words else ""
        draw_subtitle_box(draw, SCENE_SUBTITLES[2], active_word=active_word)
        
    elif t < scene_starts[4]:
        # Scene 4: The 24/7 Keep-Alive Hack & Cost Comparison
        rel_t = t - scene_starts[3]
        draw_hud(draw, "// 04 · KEEP-ALIVE HACK", "STEP 4/5")
        
        draw.rounded_rectangle([60, 200, 1020, 830], radius=28, fill=(16, 26, 42, 240), outline=(0, 210, 255), width=2)
        draw_badge(draw, 95, 235, "THE 24/7 AUTOMATION HACK", fill_color=(0, 210, 255), text_color=(10, 20, 35))
        
        draw.text((95, 305), "KEEP ANY SERVER HOT 24/7", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "How to bypass spin-down sleep on any free backend:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        draw.rounded_rectangle([95, 430, 985, 520], radius=16, fill=(24, 38, 60), outline=(0, 210, 255, 100), width=1)
        draw.text((125, 455), "1. Create free account on cron-job.org (Takes 30s)", fill=(241, 245, 249), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 540, 985, 630], radius=16, fill=(24, 38, 60), outline=(0, 210, 255, 100), width=1)
        draw.text((125, 565), "2. Add automated HTTP ping to your /health API every 10 mins", fill=(241, 245, 249), font=FONT_BODY)
        
        draw.rounded_rectangle([95, 650, 985, 740], radius=16, fill=(24, 38, 60), outline=(0, 210, 255, 100), width=1)
        draw.text((125, 675), "3. Result: Server never sleeps, 0s delay for all visitors!", fill=(0, 229, 153), font=FONT_BODY)
        
        # Bottom Cost Comparison Bar Graph
        draw.rounded_rectangle([60, 865, 1020, 1520], radius=28, fill=(18, 24, 38, 240), outline=(255, 210, 30), width=2)
        draw_badge(draw, 95, 900, "ANNUAL COST SAVINGS", fill_color=(255, 210, 30), text_color=(15, 23, 42))
        
        draw.text((95, 965), "YEARLY HOSTING BILL COMPARISON", fill=(255, 255, 255), font=FONT_TITLE)
        
        draw.text((95, 1040), "Standard Cloud (AWS / Render / Vercel Pro):", fill=(239, 68, 68), font=FONT_BODY)
        draw.rounded_rectangle([95, 1080, 985, 1140], radius=14, fill=(40, 20, 25))
        draw.rounded_rectangle([95, 1080, 880, 1140], radius=14, fill=(239, 68, 68))
        draw.text((900, 1095), "$240", fill=(239, 68, 68), font=FONT_BOLD)
        draw.text((120, 1095), "₹20,000 / Year (Waste of money for portfolio apps)", fill=(255, 255, 255), font=FONT_BOLD)
        
        draw.text((95, 1175), "This Smart Architecture (Cloudflare + Supabase):", fill=(0, 229, 153), font=FONT_BODY)
        draw.rounded_rectangle([95, 1215, 985, 1275], radius=14, fill=(20, 40, 30))
        draw.rounded_rectangle([95, 1215, 250, 1275], radius=14, fill=(0, 229, 153))
        draw.text((270, 1230), "$0.00 / LIFETIME", fill=(0, 229, 153), font=FONT_BOLD)
        
        draw.rounded_rectangle([95, 1320, 985, 1460], radius=18, fill=(35, 45, 20), outline=(255, 210, 30), width=2)
        draw.text((120, 1345), "[SAVINGS] TOTAL MONEY SAVED: ₹20,000+ / YR", fill=(255, 210, 30), font=FONT_CARD_TITLE)
        draw.text((120, 1400), "100% Legal, 100% Production Grade, Zero Maintenance.", fill=(241, 245, 249), font=FONT_BODY)
        
        all_words = " ".join(SCENE_SUBTITLES[3]).split()
        active_idx = min(int((rel_t / scene_durs[3]) * len(all_words)), len(all_words) - 1)
        active_word = all_words[active_idx] if all_words else ""
        draw_subtitle_box(draw, SCENE_SUBTITLES[3], active_word=active_word)
        
    else:
        # Scene 5: Claim Blueprint / Viral CTA
        rel_t = t - scene_starts[4]
        draw_hud(draw, "// 05 · CLAIM BLUEPRINT", "STEP 5/5")
        
        draw.rounded_rectangle([60, 200, 1020, 1520], radius=28, fill=(22, 18, 38, 240), outline=(168, 85, 247), width=2)
        draw_badge(draw, 95, 235, "FREE BLUEPRINT & TEMPLATE", fill_color=(168, 85, 247))
        
        draw.text((95, 305), "WANT THE COMPLETE CODE TEMPLATE?", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "Get the 1-click deploy GitHub repository:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        # Step 1 Button (with width fitting full text cleanly)
        draw.rounded_rectangle([95, 445, 985, 605], radius=22, fill=(28, 48, 40), outline=(0, 229, 153), width=2)
        
        # Pulsing button effect with exact text width
        pulse = 0.5 + 0.5 * math.sin(rel_t * 5.0)
        btn_glow = (int(0 + 40 * pulse), int(229), int(153 + 30 * pulse))
        draw.rounded_rectangle([125, 475, 660, 535], radius=14, fill=btn_glow)
        draw.text((145, 487), "COMMENT 'STACK'", fill=(10, 25, 20), font=FONT_TITLE)
        draw.text((125, 550), "Automated bot will DM you the starter repo link instantly", fill=(241, 245, 249), font=FONT_BODY)
        
        # Step 2 Button
        draw.rounded_rectangle([95, 645, 985, 805], radius=22, fill=(35, 25, 55), outline=(168, 85, 247, 180), width=1)
        draw.text((125, 675), "2. CLONE & DEPLOY IN 5 MINUTES", fill=(255, 255, 255), font=FONT_CARD_TITLE)
        draw.text((125, 730), "Pre-configured React + Cloudflare + Supabase setup included", fill=(203, 213, 225), font=FONT_BODY)
        
        # Step 3 Button
        draw.rounded_rectangle([95, 845, 985, 1005], radius=22, fill=(30, 35, 55), outline=(0, 210, 255, 180), width=1)
        draw.text((125, 875), "3. SAVE THIS REEL FOR FUTURE PROJECTS", fill=(0, 210, 255), font=FONT_CARD_TITLE)
        draw.text((125, 930), "Never lose the architecture blueprint when you need it", fill=(203, 213, 225), font=FONT_BODY)
        
        # Follow Banner
        draw.rounded_rectangle([95, 1050, 985, 1460], radius=22, fill=(15, 23, 42), outline=(255, 210, 30), width=2)
        draw.text((125, 1095), "[!] LEVEL UP YOUR DEVELOPER SKILLS:", fill=(255, 210, 30), font=FONT_CARD_TITLE)
        draw.text((125, 1160), "- Daily 10x Developer Hacks & Architectures", fill=(241, 245, 249), font=FONT_BODY)
        draw.text((125, 1215), "- Free Tier Cloud Masterclasses", fill=(241, 245, 249), font=FONT_BODY)
        draw.text((125, 1270), "- Full-Stack Production Templates", fill=(241, 245, 249), font=FONT_BODY)
        
        draw.rounded_rectangle([125, 1345, 955, 1415], radius=14, fill=(255, 210, 30))
        draw.text((280, 1362), "FOLLOW FOR DAILY 10X DEV HACKS", fill=(15, 23, 42), font=FONT_BOLD)
        
        all_words = " ".join(SCENE_SUBTITLES[4]).split()
        active_idx = min(int((rel_t / scene_durs[4]) * len(all_words)), len(all_words) - 1)
        active_word = all_words[active_idx] if all_words else ""
        draw_subtitle_box(draw, SCENE_SUBTITLES[4], active_word=active_word)
        
    return img

def main():
    print(f"=== Rendering Master Video ===")
    print(f"Duration: {TOTAL_DUR:.2f}s | Total Frames: {TOTAL_FRAMES} @ {FPS} FPS")
    print(f"Resolution: {WIDTH}x{HEIGHT} (9:16 Vertical HD)")
    
    temp_video = os.path.join(BASE_DIR, "temp_video.mp4")
    
    # FFmpeg process to receive raw video frames via stdin pipe
    video_cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        temp_video
    ]
    
    pipe = subprocess.Popen(video_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    for f_idx in range(TOTAL_FRAMES):
        t = f_idx / FPS
        frame = render_frame_for_time(t)
        # Convert to RGB bytes
        raw_bytes = frame.convert("RGB").tobytes()
        pipe.stdin.write(raw_bytes)
        
        if f_idx % 150 == 0 or f_idx == TOTAL_FRAMES - 1:
            pct = (f_idx + 1) / TOTAL_FRAMES * 100
            print(f"Progress: {f_idx + 1}/{TOTAL_FRAMES} frames ({pct:.1f}%) - Time: {t:.2f}s")
            
    pipe.stdin.close()
    pipe.wait()
    print("Video track rendered.")
    
    # Multiplex audio and video
    print("Muxing final master MP4 with broadcast audio...")
    mux_cmd = [
        FFMPEG, "-y",
        "-i", temp_video,
        "-i", MASTER_AUDIO,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    if os.path.exists(temp_video):
        os.remove(temp_video)
        
    file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"MASTER REEL SUCCESSFULLY GENERATED:")
    print(f"Path: {OUTPUT_VIDEO}")
    print(f"Size: {file_size_mb:.2f} MB")
    print(f"Duration: {TOTAL_DUR:.2f}s")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
