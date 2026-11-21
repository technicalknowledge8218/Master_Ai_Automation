import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\assets"
REF_ASSETS = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\test_frames"
os.makedirs(OUT_DIR, exist_ok=True)

# Load Character Sprites
junior_pointing = Image.open(os.path.join(REF_ASSETS, "clean_junior_pointing.png")).convert("RGBA")
junior_shrug = Image.open(os.path.join(REF_ASSETS, "clean_junior_shrug.png")).convert("RGBA")
senior_pointing = Image.open(os.path.join(REF_ASSETS, "clean_senior_pointing_up.png")).convert("RGBA")

# Load Cards
card_warning = Image.open(os.path.join(ASSETS_DIR, "card_warning.png")).convert("RGBA")
gauge_6 = Image.open(os.path.join(ASSETS_DIR, "gauge_cpu_6.png")).convert("RGBA")
gauge_24 = Image.open(os.path.join(ASSETS_DIR, "gauge_cpu_24.png")).convert("RGBA")
card_payg = Image.open(os.path.join(ASSETS_DIR, "card_payg.png")).convert("RGBA")
card_terminal = Image.open(os.path.join(ASSETS_DIR, "card_terminal.png")).convert("RGBA")

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
font_caption = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)

def compose_scene(bg_color, card_img, char_img, char_side="right", tag_text="CRITICAL", caption_text="", filename="scene.jpg"):
    w, h = 1080, 1920
    im = Image.new("RGBA", (w, h), bg_color)
    draw = ImageDraw.Draw(im)
    
    # 1. Subtle Radial / Gradient Glow in background
    # Top Header Banner
    draw.rounded_rectangle([60, 90, w - 60, 170], radius=16, fill=(15, 23, 42, 230), outline=(51, 65, 85, 255), width=2)
    draw.text((90, 112), f"🔥 TECH LIFE HACK  |  {tag_text}", font=font_badge, fill=(6, 182, 212, 255))
    
    # 2. Main Title Banner
    draw.text((60, 210), "ORACLE CLOUD FREE TIER", font=font_title, fill=(255, 255, 255, 255))
    
    # 3. Card Placement (Upper Center)
    cw, ch = card_img.size
    cx = (w - cw) // 2
    cy = 310
    im.paste(card_img, (cx, cy), card_img)
    
    # 4. Character Placement (Lower Section)
    ch_w, ch_h = char_img.size
    # Target height ~800px
    target_h = 820
    target_w = int(ch_w * (target_h / ch_h))
    char_resized = char_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    if char_side == "right":
        char_x = w - target_w + 40
        char_y = h - target_h + 30
    else:
        char_x = -40
        char_y = h - target_h + 30
        
    im.paste(char_resized, (char_x, char_y), char_resized)
    
    # 5. Speech / Action Callout Bubble
    bubble_w, bubble_h = 580, 140
    bx = 60 if char_side == "right" else w - 60 - bubble_w
    by = h - 650
    draw.rounded_rectangle([bx, by, bx + bubble_w, by + bubble_h], radius=20, fill=(15, 23, 42, 240), outline=(6, 182, 212, 255), width=3)
    draw.text((bx + 30, by + 25), "💡 PRO TIP:", font=font_badge, fill=(245, 158, 11, 255))
    draw.text((bx + 30, by + 65), "Don't let your free VM die!", font=font_caption, fill=(255, 255, 255, 255))
    
    # 6. Bottom Kinetic Subtitle Box
    sub_box_y = h - 220
    draw.rounded_rectangle([50, sub_box_y, w - 50, sub_box_y + 140], radius=18, fill=(10, 15, 26, 245), outline=(30, 41, 59, 255), width=2)
    
    # Wrap caption text
    words = caption_text.split()
    line1 = " ".join(words[:len(words)//2 + 1])
    line2 = " ".join(words[len(words)//2 + 1:])
    
    draw.text((80, sub_box_y + 25), line1, font=font_caption, fill=(255, 255, 255, 255))
    draw.text((80, sub_box_y + 75), line2, font=font_caption, fill=(250, 204, 21, 255))
    
    rgb_im = im.convert("RGB")
    p = os.path.join(OUT_DIR, filename)
    rgb_im.save(p, quality=95)
    print(f"Saved {p}")

# Test 4 scenes
compose_scene((24, 28, 48, 255), card_warning, junior_shrug, "right", "CRITICAL WARNING", "7 din baad aapka server automatic DELETE ho sakta hai!", "test_scene1.jpg")
compose_scene((30, 20, 25, 255), gauge_6, senior_pointing, "left", "IDLE RULE", "CPU usage 20% se kam raha toh instance TERMINATE ho jayega!", "test_scene2.jpg")
compose_scene((15, 35, 28, 255), card_payg, junior_pointing, "right", "OFFICIAL METHOD", "Pay As You Go mein upgrade karo: Rs. 0 charge forever!", "test_scene3.jpg")
compose_scene((16, 24, 40, 255), card_terminal, senior_pointing, "left", "CLI AUTOMATION", "Terminal mein 'lookbusy' run karo: CPU 22% safe lock!", "test_scene4.jpg")
