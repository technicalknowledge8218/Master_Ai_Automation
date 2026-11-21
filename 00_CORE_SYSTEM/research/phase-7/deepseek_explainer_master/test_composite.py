from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
OUT_IMG = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\test_composite.jpg"

w, h = 1080, 1920
# Pastel background
bg_color = (244, 197, 66, 255) # Warm Yellow
im = Image.new("RGBA", (w, h), bg_color)
draw = ImageDraw.Draw(im)

# Floor line
draw.line([0, 1830, w, 1830], fill=(60, 50, 40, 255), width=4)

# 1. Whiteboard
wb = Image.open(os.path.join(ASSETS_DIR, "clean_whiteboard_empty.png")).convert("RGBA")
im.alpha_composite(wb, (35, 80))

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
font_caption = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)

# Write inside Whiteboard (X: 100 to 980, Y: 120 to 980)
# Header
draw.rounded_rectangle([90, 140, 990, 225], radius=16, fill=(15, 23, 42, 255))
draw.text((540, 182), "DEEPSEEK R1 VS CHATGPT-4o ⚡", font=font_title, fill=(255, 255, 255, 255), anchor="mm")

# Card
draw.rounded_rectangle([110, 250, 970, 350], radius=16, fill=(255, 255, 255, 255), outline=(30, 41, 59, 255), width=4)
draw.text((540, 300), "CHATGPT PLUS: $20/MONTH SUBSCRIPTION 💸", font=font_sub, fill=(30, 41, 59, 255), anchor="mm")

# Red Strikethrough
draw.line([140, 300, 750, 300], fill=(239, 68, 68, 255), width=8)
draw.rounded_rectangle([750, 260, 950, 340], radius=12, fill=(239, 68, 68, 255))
draw.text((850, 300), "CANCEL? ❌", font=font_sub, fill=(255, 255, 255, 255), anchor="mm")

# 2. Characters
# Junior Hands Up
j_up = Image.open(os.path.join(ASSETS_DIR, "clean_junior_hands_up.png")).convert("RGBA")
# Place at bottom left
im.alpha_composite(j_up, (90, 1020))

# Senior Clasped
s_clasp = Image.open(os.path.join(ASSETS_DIR, "clean_senior_clasped.png")).convert("RGBA")
im.alpha_composite(s_clasp, (560, 1020))

# 3. Subtitles
sub_text = "Wait! Should I cancel my $20 ChatGPT sub? DeepSeek is literally free!"
draw.text((540, 1860), sub_text, font=font_caption, fill=(255, 255, 255, 255), stroke_width=5, stroke_fill=(15, 23, 42, 255), anchor="mm")

im.convert("RGB").save(OUT_IMG, quality=95)
print("Saved test_composite.jpg successfully!")
