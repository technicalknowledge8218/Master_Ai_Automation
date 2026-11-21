import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
test_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\rig_test_v2"
os.makedirs(test_dir, exist_ok=True)

# Load Neha and Kabir
im_neha = Image.open(os.path.join(CHAR_LIB, "neha_shocked.png")).convert("RGBA")
im_kabir = Image.open(os.path.join(CHAR_LIB, "dr_kabir_explaining.png")).convert("RGBA")

print(f"Neha size: {im_neha.size}, Kabir size: {im_kabir.size}")

# Let's write an accurate Animated Character Renderer function
def animate_character(base_img, char_type="neha", rms=0.05, is_speaking=True, is_blinking=False):
    # Make a copy
    im = base_img.copy()
    draw = ImageDraw.Draw(im)
    w, h = im.size
    
    # 1. Mouth Coordinates based on character type
    if char_type == "neha":
        # Neha face is roughly centered around X = w * 0.48, Y = h * 0.19
        mx = int(w * 0.49)
        my = int(h * 0.20)
        skin_color = (250, 220, 195, 255) # Warm skin tone
        mouth_w = 26
    elif char_type == "kabir":
        # Dr. Kabir face is centered around X = w * 0.50, Y = h * 0.20
        mx = int(w * 0.51)
        my = int(h * 0.21)
        skin_color = (235, 195, 165, 255)
        mouth_w = 24
        
    # 2. Draw Animated Mouth
    if is_speaking and rms > 0.018:
        # Mouth open height based on RMS volume (from 6px to 22px)
        open_h = int(min(24, max(6, (rms - 0.018) * 220 + 8)))
        
        # First: clean background patch over resting mouth
        draw.ellipse([mx - mouth_w//2 - 2, my - open_h//2 - 2, mx + mouth_w//2 + 2, my + open_h//2 + 2], fill=skin_color)
        
        # Dark open mouth cavity
        draw.ellipse([mx - mouth_w//2, my - open_h//2, mx + mouth_w//2, my + open_h//2], fill=(30, 10, 15, 255), outline=(20, 20, 20, 255), width=2)
        
        # Teeth line at top
        teeth_h = max(2, open_h // 3)
        draw.rectangle([mx - mouth_w//2 + 3, my - open_h//2 + 1, mx + mouth_w//2 - 3, my - open_h//2 + teeth_h], fill=(255, 255, 255, 255))
        
        # Tongue curve at bottom
        if open_h > 12:
            tongue_h = open_h // 3
            draw.ellipse([mx - mouth_w//3, my + open_h//2 - tongue_h, mx + mouth_w//3, my + open_h//2], fill=(230, 80, 100, 255))
    else:
        # Resting mouth: slight natural curved smile line
        # Draw clean smile curve
        draw.arc([mx - 12, my - 6, mx + 12, my + 6], start=10, end=170, fill=(40, 20, 20, 255), width=3)
        
    # 3. Eye Blinking
    if is_blinking:
        if char_type == "neha":
            # Cover eyes with skin color and draw closed curved eyelid lines
            ey = int(h * 0.155)
            ex1, ex2 = int(w * 0.40), int(w * 0.58)
            draw.ellipse([ex1 - 12, ey - 10, ex1 + 12, ey + 10], fill=skin_color)
            draw.ellipse([ex2 - 12, ey - 10, ex2 + 12, ey + 10], fill=skin_color)
            draw.arc([ex1 - 10, ey - 5, ex1 + 10, ey + 5], start=190, end=350, fill=(20, 20, 20, 255), width=3)
            draw.arc([ex2 - 10, ey - 5, ex2 + 10, ey + 5], start=190, end=350, fill=(20, 20, 20, 255), width=3)
        elif char_type == "kabir":
            ey = int(h * 0.165)
            ex1, ex2 = int(w * 0.42), int(w * 0.60)
            draw.ellipse([ex1 - 10, ey - 8, ex1 + 10, ey + 8], fill=skin_color)
            draw.ellipse([ex2 - 10, ey - 8, ex2 + 10, ey + 8], fill=skin_color)
            draw.arc([ex1 - 9, ey - 4, ex1 + 9, ey + 4], start=190, end=350, fill=(20, 20, 20, 255), width=3)
            draw.arc([ex2 - 9, ey - 4, ex2 + 9, ey + 4], start=190, end=350, fill=(20, 20, 20, 255), width=3)
            
    return im

# Generate test frames
test_neha_open = animate_character(im_neha, "neha", rms=0.07, is_speaking=True, is_blinking=False)
test_neha_blink = animate_character(im_neha, "neha", rms=0.0, is_speaking=False, is_blinking=True)
test_kabir_open = animate_character(im_kabir, "kabir", rms=0.06, is_speaking=True, is_blinking=False)
test_kabir_rest = animate_character(im_kabir, "kabir", rms=0.0, is_speaking=False, is_blinking=False)

test_neha_open.save(os.path.join(test_dir, "test_neha_speaking.png"))
test_neha_blink.save(os.path.join(test_dir, "test_neha_blinking.png"))
test_kabir_open.save(os.path.join(test_dir, "test_kabir_speaking.png"))
test_kabir_rest.save(os.path.join(test_dir, "test_kabir_resting.png"))

print("Saved rigged animated character test frames!")
