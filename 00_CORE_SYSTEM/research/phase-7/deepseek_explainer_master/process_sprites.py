import cv2
import numpy as np
import os

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"

def make_transparent(crop_img, bg_sample_pos=(10, 10), thresh=28):
    h, w, _ = crop_img.shape
    bg_val = crop_img[bg_sample_pos[1], bg_sample_pos[0]].astype(np.float32)
    
    # Color distance to background
    diff = np.sqrt(np.sum((crop_img.astype(np.float32) - bg_val) ** 2, axis=2))
    
    # Mask: 0 where close to background, 255 where foreground
    mask = np.where(diff < thresh, 0, 255).astype(np.uint8)
    
    # Also clean up the floor line if needed (floor is usually below y=1830 in full frame, or at bottom of crop)
    # Morphological clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    rgba = cv2.cvtColor(crop_img, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = mask
    return rgba

# Process Junior Pose 18 (pointing)
p18_j = cv2.imread(os.path.join(ASSETS_DIR, "junior_pose18_raw.png"))
rgba_j18 = make_transparent(p18_j, (10, 10), 30)
cv2.imwrite(os.path.join(ASSETS_DIR, "junior_pointing.png"), rgba_j18)

# Process Senior Pose 18 (clasped)
p18_s = cv2.imread(os.path.join(ASSETS_DIR, "senior_pose18_raw.png"))
rgba_s18 = make_transparent(p18_s, (350, 10), 30)
cv2.imwrite(os.path.join(ASSETS_DIR, "senior_clasped.png"), rgba_s18)

# Process Junior Hands Up (pose 3s)
p3_j = cv2.imread(os.path.join(ASSETS_DIR, "junior_hands_up_raw.png"))
rgba_j3 = make_transparent(p3_j, (10, 10), 30)
cv2.imwrite(os.path.join(ASSETS_DIR, "junior_hands_up.png"), rgba_j3)

# Process Junior Shrug (pose 25s)
p25_j = cv2.imread(os.path.join(ASSETS_DIR, "junior_shrug_raw.png"))
rgba_j25 = make_transparent(p25_j, (10, 10), 30)
cv2.imwrite(os.path.join(ASSETS_DIR, "junior_shrug.png"), rgba_j25)

# Process Senior Pointing Up (pose 25s)
p25_s = cv2.imread(os.path.join(ASSETS_DIR, "senior_point_raw.png"))
rgba_s25 = make_transparent(p25_s, (10, 10), 30)
cv2.imwrite(os.path.join(ASSETS_DIR, "senior_pointing_up.png"), rgba_s25)

print("Created transparent PNG sprites!")
