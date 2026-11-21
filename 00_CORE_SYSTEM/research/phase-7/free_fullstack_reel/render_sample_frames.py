import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\free_fullstack_reel"
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

with open(os.path.join(BASE_DIR, "timing_metadata.json"), "r") as f:
    timing = json.load(f)

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
FONT_TERM_CMD = get_font("consolas.ttf", 34)
FONT_TERM_OUT = get_font("consolas.ttf", 28)
FONT_TERM_BOX = get_font("consolas.ttf", 30)

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
    # Left pill: Chapter
    ch_box = draw.textbbox((0, 0), chapter_text, font=FONT_HUD)
    ch_w = ch_box[2] - ch_box[0] + 36
    draw.rounded_rectangle([60, 65, 60 + ch_w, 120], radius=14, fill=(255, 210, 30))
    draw.text((78, 77), chapter_text, fill=(15, 23, 42), font=FONT_HUD)
    
    # Center pill: Topic Title
    center_text = "₹0 FULL-STACK ARCHITECTURE"
    c_box = draw.textbbox((0, 0), center_text, font=FONT_HUD)
    c_w = c_box[2] - c_box[0] + 36
    c_x = 60 + ch_w + 15
    draw.rounded_rectangle([c_x, 65, c_x + c_w, 120], radius=14, fill=(15, 25, 45, 240), outline=(0, 210, 255), width=2)
    draw.text((c_x + 18, 77), center_text, fill=(0, 210, 255), font=FONT_HUD)
    
    # Right pill: Step
    st_box = draw.textbbox((0, 0), step_text, font=FONT_HUD)
    st_w = st_box[2] - st_box[0] + 36
    st_x = 1020 - st_w
    draw.rounded_rectangle([st_x, 65, 1020, 120], radius=14, fill=(30, 41, 59, 240), outline=(148, 163, 184), width=2)
    draw.text((st_x + 18, 77), step_text, fill=(241, 245, 249), font=FONT_HUD)

def draw_subtitle_box(draw, lines, active_word=""):
    # Bottom Subtitle Box at y=1660, h=175
    draw.rounded_rectangle([60, 1660, 1020, 1835], radius=24, fill=(11, 17, 32, 245), outline=(0, 229, 153), width=2)
    
    # Wrap lines cleanly
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
            
    # Draw at most 2 lines
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

def render_frame(t):
    img = Image.new("RGBA", (1080, 1920), (10, 15, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Subtle background cyber grid
    for gx in range(0, 1080, 120):
        draw.line([(gx, 0), (gx, 1920)], fill=(20, 30, 50, 40), width=1)
    for gy in range(0, 1920, 120):
        draw.line([(0, gy), (1080, gy)], fill=(20, 30, 50, 40), width=1)
        
    scene_starts = timing["scene_starts"]
    
    if t < scene_starts[1]:
        # Scene 1: The Cold Start Trap
        draw_hud(draw, "// 01 · CLOUD TRAP", "STEP 1/5")
        
        # Primary Alert Card
        draw.rounded_rectangle([60, 200, 1020, 840], radius=28, fill=(22, 18, 28, 240), outline=(239, 68, 68), width=2)
        draw_badge(draw, 95, 235, "CRITICAL ALERT", fill_color=(239, 68, 68))
        
        draw.text((95, 305), "THE 15-MINUTE SLEEP TRAP", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "Why free hosting tiers ruin your portfolio:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        # Point 1
        draw.rounded_rectangle([95, 430, 985, 520], radius=16, fill=(35, 20, 28), outline=(239, 68, 68, 120), width=1)
        draw.text((120, 455), "[!]  15-Min Inactivity: Server automatically spins down to 0", fill=(254, 202, 202), font=FONT_BODY)
        
        # Point 2
        draw.rounded_rectangle([95, 540, 985, 630], radius=16, fill=(35, 20, 28), outline=(239, 68, 68, 120), width=1)
        draw.text((120, 565), "[WAIT] 50+ Seconds Cold Start: Recruiter clicks and leaves!", fill=(254, 202, 202), font=FONT_BODY)
        
        # Progress Bar
        draw.text((95, 660), "Portfolio Loading Experience (50s Delay):", fill=(148, 163, 184), font=FONT_BODY)
        draw.rounded_rectangle([95, 705, 985, 745], radius=12, fill=(30, 41, 59))
        draw.rounded_rectangle([95, 705, 750, 745], radius=12, fill=(239, 68, 68))
        draw.text((95, 765), "Spin-down status: 52s delay (Visitor bounces away!)", fill=(239, 68, 68), font=FONT_BOLD)
        
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
        
        draw_subtitle_box(draw, SCENE_SUBTITLES[0], active_word="render")
        
    elif t < scene_starts[2]:
        # Scene 2: Frontend on Cloudflare Pages
        draw_hud(draw, "// 02 · FRONTEND", "STEP 2/5")
        
        draw.rounded_rectangle([60, 200, 1020, 1500], radius=28, fill=(13, 27, 28, 240), outline=(0, 229, 153), width=2)
        draw_badge(draw, 95, 235, "FRONTEND ARCHITECTURE", fill_color=(0, 229, 153), text_color=(10, 25, 20))
        
        draw.text((95, 305), "CLOUDFLARE PAGES (0ms Edge)", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "The ultimate $0 production frontend platform:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        # Metric Box 1: Bandwidth
        draw.rounded_rectangle([95, 435, 985, 615], radius=20, fill=(18, 38, 38), outline=(0, 229, 153, 120), width=1)
        draw.text((125, 460), "BANDWIDTH & TRAFFIC", fill=(148, 163, 184), font=FONT_BADGE)
        draw.text((125, 500), "UNLIMITED (100% FREE FOREVER)", fill=(0, 229, 153), font=FONT_CARD_TITLE)
        draw.text((125, 555), "No bandwidth caps, no overage fees, 0 surprise bills.", fill=(226, 232, 240), font=FONT_BODY)
        
        # Metric Box 2: Cold Start
        draw.rounded_rectangle([95, 645, 985, 825], radius=20, fill=(18, 38, 38), outline=(0, 229, 153, 120), width=1)
        draw.text((125, 670), "COLD START LATENCY", fill=(148, 163, 184), font=FONT_BADGE)
        draw.text((125, 710), "0ms (Instant Global Edge Response)", fill=(0, 210, 255), font=FONT_CARD_TITLE)
        draw.text((125, 765), "Cached across 330+ cities worldwide on Cloudflare CDN.", fill=(226, 232, 240), font=FONT_BODY)
        
        # Metric Box 3: Custom Domain
        draw.rounded_rectangle([95, 855, 985, 1035], radius=20, fill=(18, 38, 38), outline=(0, 229, 153, 120), width=1)
        draw.text((125, 880), "CUSTOM DOMAIN & SECURITY", fill=(148, 163, 184), font=FONT_BADGE)
        draw.text((125, 920), "FREE CUSTOM DOMAIN + SSL", fill=(255, 210, 30), font=FONT_CARD_TITLE)
        draw.text((125, 975), "Connect your .com / .dev domain in 1-click with DDoS guard.", fill=(226, 232, 240), font=FONT_BODY)
        
        # Comparison Bottom Pill
        draw.rounded_rectangle([95, 1075, 985, 1430], radius=22, fill=(15, 23, 42), outline=(148, 163, 184, 180), width=2)
        draw.text((125, 1110), "COST COMPARISON:", fill=(255, 255, 255), font=FONT_CARD_TITLE)
        
        draw.text((125, 1175), "Vercel Pro (Bandwidth Overage):", fill=(239, 68, 68), font=FONT_BODY)
        draw.text((700, 1175), "$20 / month", fill=(239, 68, 68), font=FONT_BOLD)
        
        draw.text((125, 1245), "Cloudflare Pages (Unlimited):", fill=(0, 229, 153), font=FONT_BODY)
        draw.text((700, 1245), "$0 / Lifetime", fill=(0, 229, 153), font=FONT_BOLD)
        
        draw.text((125, 1330), "[!] 100% Free Lifetime Hosting without limits!", fill=(255, 210, 30), font=FONT_BOLD)
        
        draw_subtitle_box(draw, SCENE_SUBTITLES[1], active_word="cloudflare")
        
    elif t < scene_starts[3]:
        # Scene 3: Backend & Database + Live macOS Terminal
        draw_hud(draw, "// 03 · BACKEND & DB", "STEP 3/5")
        
        # Top Database Info Bar
        draw.rounded_rectangle([60, 200, 1020, 460], radius=24, fill=(18, 24, 40, 240), outline=(0, 210, 255), width=2)
        draw_badge(draw, 95, 230, "DATABASE: SERVERLESS PG", fill_color=(0, 210, 255), text_color=(10, 20, 35))
        
        draw.text((95, 295), "SUPABASE / NEON POSTGRESQL", fill=(255, 255, 255), font=FONT_CARD_TITLE)
        draw.text((95, 350), "500MB Free Database Storage + Instant REST & GraphQL API", fill=(226, 232, 240), font=FONT_BODY)
        draw.text((95, 395), "Auto connection pooling: handles 10,000+ concurrent users!", fill=(0, 229, 153), font=FONT_BOLD)
        
        # macOS Terminal Window
        draw.rounded_rectangle([60, 500, 1020, 1520], radius=24, fill=(12, 16, 24, 255), outline=(51, 65, 85), width=2)
        
        # Traffic Lights
        draw.ellipse([95, 535, 119, 559], fill=(255, 95, 86))    # Red
        draw.ellipse([132, 535, 156, 559], fill=(255, 189, 46))  # Yellow
        draw.ellipse([169, 535, 193, 559], fill=(39, 201, 63))   # Green
        
        draw.text((230, 532), "bash - developer@global-edge: ~/my-api", fill=(148, 163, 184), font=FONT_TERM_OUT)
        draw.line([(60, 580), (1020, 580)], fill=(51, 65, 85), width=1)
        
        # Terminal Typing Lines (Larger and bolder)
        y_t = 615
        draw.text((95, y_t), "developer@edge:~$ npx wrangler init my-api", fill=(0, 229, 153), font=FONT_TERM_CMD)
        y_t += 55
        draw.text((95, y_t), "[OK] Worker ready: 100,000 reqs/day 100% FREE", fill=(241, 245, 249), font=FONT_TERM_OUT)
        y_t += 75
        
        draw.text((95, y_t), "developer@edge:~$ npx supabase db push", fill=(0, 229, 153), font=FONT_TERM_CMD)
        y_t += 55
        draw.text((95, y_t), "[OK] Connected to Serverless PostgreSQL on port 5432", fill=(241, 245, 249), font=FONT_TERM_OUT)
        y_t += 75
        
        draw.text((95, y_t), "developer@edge:~$ npm run deploy --prod", fill=(0, 229, 153), font=FONT_TERM_CMD)
        y_t += 65
        
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
        draw.text((95, y_t + 320), "developer@edge:~$ _", fill=(0, 229, 153), font=FONT_TERM_CMD)
        
        draw_subtitle_box(draw, SCENE_SUBTITLES[2], active_word="supabase")
        
    elif t < scene_starts[4]:
        # Scene 4: The 24/7 Keep-Alive Hack & Cost Comparison
        draw_hud(draw, "// 04 · KEEP-ALIVE HACK", "STEP 4/5")
        
        draw.rounded_rectangle([60, 200, 1020, 830], radius=28, fill=(16, 26, 42, 240), outline=(0, 210, 255), width=2)
        draw_badge(draw, 95, 235, "THE 24/7 AUTOMATION HACK", fill_color=(0, 210, 255), text_color=(10, 20, 35))
        
        draw.text((95, 305), "KEEP ANY SERVER HOT 24/7", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "How to bypass spin-down sleep on any free backend:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        # Step 1
        draw.rounded_rectangle([95, 430, 985, 520], radius=16, fill=(24, 38, 60), outline=(0, 210, 255, 100), width=1)
        draw.text((125, 455), "1. Create free account on cron-job.org (Takes 30s)", fill=(241, 245, 249), font=FONT_BODY)
        
        # Step 2
        draw.rounded_rectangle([95, 540, 985, 630], radius=16, fill=(24, 38, 60), outline=(0, 210, 255, 100), width=1)
        draw.text((125, 565), "2. Add automated HTTP ping to your /health API every 10 mins", fill=(241, 245, 249), font=FONT_BODY)
        
        # Step 3
        draw.rounded_rectangle([95, 650, 985, 740], radius=16, fill=(24, 38, 60), outline=(0, 210, 255, 100), width=1)
        draw.text((125, 675), "3. Result: Server never sleeps, 0s delay for all visitors!", fill=(0, 229, 153), font=FONT_BODY)
        
        # Bottom Cost Comparison Bar Graph
        draw.rounded_rectangle([60, 865, 1020, 1520], radius=28, fill=(18, 24, 38, 240), outline=(255, 210, 30), width=2)
        draw_badge(draw, 95, 900, "ANNUAL COST SAVINGS", fill_color=(255, 210, 30), text_color=(15, 23, 42))
        
        draw.text((95, 965), "YEARLY HOSTING BILL COMPARISON", fill=(255, 255, 255), font=FONT_TITLE)
        
        # Red Bar: Standard Cloud
        draw.text((95, 1040), "Standard Cloud (AWS / Render / Vercel Pro):", fill=(239, 68, 68), font=FONT_BODY)
        draw.rounded_rectangle([95, 1080, 985, 1140], radius=14, fill=(40, 20, 25))
        draw.rounded_rectangle([95, 1080, 880, 1140], radius=14, fill=(239, 68, 68))
        draw.text((900, 1095), "$240", fill=(239, 68, 68), font=FONT_BOLD)
        draw.text((120, 1095), "₹20,000 / Year (Waste of money for portfolio apps)", fill=(255, 255, 255), font=FONT_BOLD)
        
        # Green Bar: This Architecture
        draw.text((95, 1175), "This Smart Architecture (Cloudflare + Supabase):", fill=(0, 229, 153), font=FONT_BODY)
        draw.rounded_rectangle([95, 1215, 985, 1275], radius=14, fill=(20, 40, 30))
        draw.rounded_rectangle([95, 1215, 250, 1275], radius=14, fill=(0, 229, 153))
        draw.text((270, 1230), "$0.00 / LIFETIME", fill=(0, 229, 153), font=FONT_BOLD)
        
        # Savings Highlight Box (Fitting inside width with 30px padding)
        draw.rounded_rectangle([95, 1320, 985, 1460], radius=18, fill=(35, 45, 20), outline=(255, 210, 30), width=2)
        draw.text((120, 1345), "[SAVINGS] TOTAL MONEY SAVED: ₹20,000+ / YR", fill=(255, 210, 30), font=FONT_CARD_TITLE)
        draw.text((120, 1400), "100% Legal, 100% Production Grade, Zero Maintenance.", fill=(241, 245, 249), font=FONT_BODY)
        
        draw_subtitle_box(draw, SCENE_SUBTITLES[3], active_word="cron-job.org")
        
    else:
        # Scene 5: Claim Blueprint / Viral CTA
        draw_hud(draw, "// 05 · CLAIM BLUEPRINT", "STEP 5/5")
        
        draw.rounded_rectangle([60, 200, 1020, 1520], radius=28, fill=(22, 18, 38, 240), outline=(168, 85, 247), width=2)
        draw_badge(draw, 95, 235, "FREE BLUEPRINT & TEMPLATE", fill_color=(168, 85, 247))
        
        draw.text((95, 305), "WANT THE COMPLETE CODE TEMPLATE?", fill=(255, 255, 255), font=FONT_TITLE)
        draw.text((95, 370), "Get the 1-click deploy GitHub repository:", fill=(148, 163, 184), font=FONT_SUBTITLE)
        
        # Step 1 Button
        draw.rounded_rectangle([95, 445, 985, 605], radius=22, fill=(28, 48, 40), outline=(0, 229, 153), width=2)
        draw.rounded_rectangle([125, 475, 480, 535], radius=14, fill=(0, 229, 153))
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
        
        draw_subtitle_box(draw, SCENE_SUBTITLES[4], active_word="stack")
        
    return img

def main():
    test_times = [
        ("snap_scene1.jpg", 3.0),
        ("snap_scene2.jpg", 18.0),
        ("snap_scene3.jpg", 35.0),
        ("snap_scene4.jpg", 50.0),
        ("snap_scene5.jpg", 65.0),
    ]
    for filename, t in test_times:
        frame = render_frame(t)
        out_path = os.path.join(SNAPSHOTS_DIR, filename)
        frame.convert("RGB").save(out_path, quality=95)
        print(f"Saved {filename} at t={t}s")
        
        brain_path = os.path.join(r"<ARTIFACT_DIR>", filename)
        frame.convert("RGB").save(brain_path, quality=95)

if __name__ == "__main__":
    main()
