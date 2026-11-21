from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
OUT_IMG = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\test_composite_v2.jpg"

w, h = 1080, 1920
bg_color = (244, 197, 66, 255) # Warm Yellow (#F4C542)
im = Image.new("RGBA", (w, h), bg_color)
draw = ImageDraw.Draw(im)

# Studio Floor line (Dark brownish-gray line)
draw.line([0, 1830, w, 1830], fill=(70, 60, 50, 255), width=4)

# ==========================================
# 1. WHITEBOARD (Ref_04 Style)
# ==========================================
# Outer Stand / Legs if any
draw.rounded_rectangle([32, 78, 1048, 1082], radius=30, fill=(160, 175, 190, 180)) # subtle drop shadow
draw.rounded_rectangle([30, 75, 1050, 1075], radius=28, fill=(255, 255, 255, 255), outline=(30, 41, 59, 255), width=8)
draw.rounded_rectangle([48, 92, 1032, 1058], radius=18, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=3)

# Tray & Markers
draw.rounded_rectangle([200, 1060, 880, 1078], radius=6, fill=(100, 116, 139, 255), outline=(15, 23, 42, 255), width=3)
# Red marker
draw.rounded_rectangle([280, 1052, 370, 1066], radius=4, fill=(239, 68, 68, 255), outline=(15, 23, 42, 255), width=2)
# Black marker
draw.rounded_rectangle([410, 1052, 500, 1066], radius=4, fill=(15, 23, 42, 255), outline=(15, 23, 42, 255), width=2)
# Blue marker
draw.rounded_rectangle([540, 1052, 630, 1066], radius=4, fill=(37, 99, 235, 255), outline=(15, 23, 42, 255), width=2)

# ==========================================
# 2. WHITEBOARD CARDS (Clean modern graphics)
# ==========================================
font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 42)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
font_caption = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 36)

# Header Card
draw.rounded_rectangle([80, 130, 1000, 220], radius=16, fill=(15, 23, 42, 255))
draw.text((540, 175), "DEEPSEEK R1 VS CHATGPT-4o ⚡", font=font_title, fill=(255, 255, 255, 255), anchor="mm")

# Hook Card
draw.rounded_rectangle([100, 260, 980, 370], radius=18, fill=(248, 250, 252, 255), outline=(30, 41, 59, 255), width=4)
draw.text((540, 315), "CHATGPT PLUS: $20/MONTH SUBSCRIPTION 💸", font=font_sub, fill=(30, 41, 59, 255), anchor="mm")

# Red Strikethrough & Cancel Stamp
draw.line([130, 315, 760, 315], fill=(239, 68, 68, 255), width=10)
draw.rounded_rectangle([750, 275, 960, 355], radius=14, fill=(239, 68, 68, 255), outline=(153, 27, 27, 255), width=3)
draw.text((855, 315), "CANCEL? ❌", font=font_sub, fill=(255, 255, 255, 255), anchor="mm")

# ==========================================
# 3. REAL CHARACTER SPRITES
# ==========================================
# Junior Pointing
j_pt = Image.open(os.path.join(ASSETS_DIR, "clean_junior_pointing.png")).convert("RGBA")
im.alpha_composite(j_pt, (110, 1010))

# Senior Pointing Up
s_pt = Image.open(os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png")).convert("RGBA")
im.alpha_composite(s_pt, (530, 1010))

# ==========================================
# 4. CAPTIONS WITH BLACK OUTLINE (Ref_04 Style)
# ==========================================
sub_text = "Wait! Should I cancel my $20 ChatGPT sub?"
draw.text((540, 1860), sub_text, font=font_caption, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(15, 23, 42, 255), anchor="mm")

im.convert("RGB").save(OUT_IMG, quality=95)
print("Saved test_composite_v2.jpg successfully!")
