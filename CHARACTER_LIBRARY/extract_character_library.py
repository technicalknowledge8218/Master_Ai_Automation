import os
from PIL import Image
import numpy as np

CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
os.makedirs(CHAR_LIB, exist_ok=True)

brain_dir = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d"

# Files
f_arjun = os.path.join(brain_dir, "arjun_character_spritesheet_1795031979222.jpg")
f_kabir = os.path.join(brain_dir, "dr_kabir_sprite_sheet_1795031985639.jpg")
f_neha = os.path.join(brain_dir, "neha_character_spritesheet_1795031991404.jpg")

def process_sheet(img_path, prefix, pose_names):
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        return
    
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    print(f"Processing {prefix}: {w}x{h}")
    
    # Check layout: 2x2 grid or 1x4 horizontal?
    # Usually AI generates a 2x2 grid (4 poses) or 1x4 row.
    # Let's inspect image dimensions:
    aspect = w / h
    crops = []
    if 0.8 <= aspect <= 1.2:
        # 2x2 Grid
        hw, hh = w // 2, h // 2
        crops = [
            (0, 0, hw, hh),          # Top-Left
            (hw, 0, w, hh),          # Top-Right
            (0, hh, hw, h),          # Bottom-Left
            (hw, hh, w, h)           # Bottom-Right
        ]
    elif aspect > 1.8:
        # 1x4 Horizontal strip
        sw = w // 4
        for i in range(4):
            crops.append((i * sw, 0, (i + 1) * sw, h))
    else:
        # 4x1 Vertical strip
        sh = h // 4
        for i in range(4):
            crops.append((0, i * sh, w, (i + 1) * sh))
            
    for i, box in enumerate(crops):
        if i >= len(pose_names): break
        crop_im = im.crop(box)
        # Background removal (pure white background to transparent)
        arr = np.array(crop_im)
        # Check white background threshold
        # White or near white: R>240, G>240, B>240
        mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240)
        
        # Create RGBA
        rgba = np.dstack((arr, np.full((crop_im.height, crop_im.width), 255, dtype=np.uint8)))
        rgba[mask, 3] = 0
        
        # Crop tight bounding box around non-transparent pixels
        alpha = rgba[:, :, 3]
        y_indices, x_indices = np.where(alpha > 10)
        if len(y_indices) > 0 and len(x_indices) > 0:
            min_y, max_y = np.min(y_indices), np.max(y_indices)
            min_x, max_x = np.min(x_indices), np.max(x_indices)
            tight_rgba = rgba[min_y:max_y+1, min_x:max_x+1]
            out_img = Image.fromarray(tight_rgba, "RGBA")
        else:
            out_img = Image.fromarray(rgba, "RGBA")
            
        out_name = f"{prefix}_{pose_names[i]}.png"
        out_path = os.path.join(CHAR_LIB, out_name)
        out_img.save(out_path)
        print(f"Saved transparent sprite: {out_name} ({out_img.size})")

process_sheet(f_arjun, "arjun", ["pointing", "shocked", "shrug", "thumbsup"])
process_sheet(f_kabir, "kabir", ["explaining", "tablet", "proud", "warning"])
process_sheet(f_neha, "neha", ["laptop", "pointing", "shocked", "peace"])
print("ALL CHARACTER SPRITES PROCESSED & SAVED TO CHARACTER_LIBRARY!")
