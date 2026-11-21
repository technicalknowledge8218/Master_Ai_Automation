import os
import cv2
import numpy as np
from PIL import Image

CHAR_LIB = r"F:\Master AI\CHARACTER_LIBRARY"
os.makedirs(CHAR_LIB, exist_ok=True)

brain_dir = r"<ARTIFACT_DIR>"

sheets = [
    {
        "file": os.path.join(brain_dir, "arjun_character_spritesheet_1795031979222.jpg"),
        "prefix": "arjun",
        "poses": ["pointing", "shocked", "shrug", "thumbsup"]
    },
    {
        "file": os.path.join(brain_dir, "dr_kabir_sprite_sheet_1795031985639.jpg"),
        "prefix": "dr_kabir",
        "poses": ["explaining", "tablet", "proud", "warning"]
    },
    {
        "file": os.path.join(brain_dir, "neha_character_spritesheet_1795031991404.jpg"),
        "prefix": "neha",
        "poses": ["laptop", "pointing", "shocked", "peace"]
    }
]

for s in sheets:
    p = s["file"]
    if not os.path.exists(p):
        print(f"Not found: {p}")
        continue
        
    img_bgr = cv2.imread(p)
    h, w = img_bgr.shape[:2]
    print(f"--- Extracting {s['prefix']} ({w}x{h}) ---")
    
    # 1. Detect background (white/near-white)
    # Convert to grayscale
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # Invert so characters are foreground (>0) and white background is 0
    fg_mask = (gray < 240).astype(np.uint8) * 255
    
    # Clean up small noise with morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    # 2. Find contours / connected components of characters
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(fg_mask)
    
    # Filter components by minimum area (to ignore small text/specks)
    valid_boxes = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        bw = stats[i, cv2.CC_STAT_WIDTH]
        bh = stats[i, cv2.CC_STAT_HEIGHT]
        bx = stats[i, cv2.CC_STAT_LEFT]
        by = stats[i, cv2.CC_STAT_TOP]
        
        # We expect full body characters to be tall (>300px)
        if bh > 250 and bw > 80:
            valid_boxes.append((bx, by, bw, bh, area))
            
    # Sort left to right by bx
    valid_boxes.sort(key=lambda b: b[0])
    
    # Merge overlapping or close boxes if needed
    merged_boxes = []
    for b in valid_boxes:
        if not merged_boxes:
            merged_boxes.append(list(b))
        else:
            prev = merged_boxes[-1]
            # If horizontal distance is small, merge them
            if b[0] < prev[0] + prev[2] + 20:
                nx1 = min(prev[0], b[0])
                ny1 = min(prev[1], b[1])
                nx2 = max(prev[0] + prev[2], b[0] + b[2])
                ny2 = max(prev[1] + prev[3], b[1] + b[3])
                merged_boxes[-1] = [nx1, ny1, nx2 - nx1, ny2 - ny1, prev[4] + b[4]]
            else:
                merged_boxes.append(list(b))
                
    # If merged boxes are 4, great! If not, divide horizontally into 4 regions
    if len(merged_boxes) != 4:
        print(f"Found {len(merged_boxes)} components, fallback to 4 column slices")
        merged_boxes = []
        cw = w // 4
        for i in range(4):
            merged_boxes.append([i * cw, 0, cw, h, 0])
            
    # 3. Create transparent RGBA crops
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    for idx, box in enumerate(merged_boxes[:4]):
        bx, by, bw, bh = box[0], box[1], box[2], box[3]
        
        # Add slight padding
        pad = 8
        x1 = max(0, bx - pad)
        y1 = max(0, by - pad)
        x2 = min(w, bx + bw + pad)
        y2 = min(h, by + bh + pad)
        
        crop_rgb = img_rgb[y1:y2, x1:x2]
        crop_gray = gray[y1:y2, x1:x2]
        
        # Alpha channel: transparent where white (gray > 242)
        alpha = np.where(crop_gray > 240, 0, 255).astype(np.uint8)
        
        # Soften edges slightly with feathering
        alpha_blur = cv2.GaussianBlur(alpha, (3, 3), 0)
        
        rgba = np.dstack((crop_rgb, alpha_blur))
        
        # Crop tight non-empty
        ys, xs = np.where(alpha > 10)
        if len(ys) > 0 and len(xs) > 0:
            tight_rgba = rgba[np.min(ys):np.max(ys)+1, np.min(xs):np.max(xs)+1]
        else:
            tight_rgba = rgba
            
        pose_name = s["poses"][idx] if idx < len(s["poses"]) else f"pose_{idx+1}"
        fname = f"{s['prefix']}_{pose_name}.png"
        fpath = os.path.join(CHAR_LIB, fname)
        
        Image.fromarray(tight_rgba, "RGBA").save(fpath)
        print(f"-> Saved: {fname} (Size: {tight_rgba.shape[1]}x{tight_rgba.shape[0]})")

print("\n--- MASTER CHARACTER LIBRARY READY ---")
