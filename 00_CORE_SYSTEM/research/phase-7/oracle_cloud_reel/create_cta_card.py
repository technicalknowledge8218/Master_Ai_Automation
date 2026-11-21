import os
from PIL import Image, ImageDraw, ImageFont

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\assets"

C_CARD_BG = (30, 41, 59, 255)
C_EMERALD = (16, 185, 129, 255)
C_NEON_CYAN = (6, 182, 212, 255)
C_WHITE = (255, 255, 255, 255)
C_MUTED = (148, 163, 184, 255)
C_AMBER = (245, 158, 11, 255)

font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
font_subtitle = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
font_body = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)

def create_cta_card():
    w, h = 920, 520
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    draw.rounded_rectangle([0, 0, w, h], radius=24, fill=C_CARD_BG, outline=C_NEON_CYAN, width=4)
    draw.rounded_rectangle([0, 0, w, 90], radius=24, fill=(15, 35, 55, 255))
    draw.text((40, 24), "🚀 LIFETIME FREE VM CHECKLIST", font=font_subtitle, fill=C_NEON_CYAN)
    
    # Checklist
    items = [
        ("✅ 4 ARM Cores & 24GB RAM:", "100% Free Forever"),
        ("✅ Method 1 (Official):", "Upgrade to PAYG ($0 Bill)"),
        ("✅ Method 2 (No Card):", "Run 'lookbusy' Idle Script"),
        ("📩 Setup Guide:", "Comment 'ORACLE' Below!")
    ]
    
    y = 120
    for label, val in items:
        draw.rounded_rectangle([40, y, w - 40, y + 75], radius=14, fill=(20, 30, 45, 255))
        draw.text((60, y + 20), label, font=font_body, fill=C_MUTED)
        draw.text((440, y + 20), val, font=font_subtitle, fill=C_AMBER if "ORACLE" in val else C_WHITE)
        y += 90
        
    im.save(os.path.join(out_dir, "card_cta.png"))
    print("Saved card_cta.png")

create_cta_card()
