import cv2
import numpy as np
import os

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
POSES_DIR = r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04_poses"

def extract_clean_sprite(full_img_path, crop_box, bg_sample_point=(20, 20), thresh=45):
    img = cv2.imread(full_img_path)
    x1, y1, x2, y2 = crop_box
    crop = img[y1:y2, x1:x2].copy()
    
    bg_color = img[bg_sample_point[1], bg_sample_point[0]].astype(np.float32)
    diff = np.sqrt(np.sum((crop.astype(np.float32) - bg_color) ** 2, axis=2))
    
    # 0 where background, 255 where foreground
    mask = np.where(diff < thresh, 0, 255).astype(np.uint8)
    
    # Also handle the floor line: floor is at y=1830 in full image, so in crop it's y = 1830 - y1
    floor_in_crop = 1830 - y1
    if 0 < floor_in_crop < crop.shape[0]:
        # Sample floor color at bottom corner
        floor_color = crop[floor_in_crop + 20, 10].astype(np.float32)
        diff_floor = np.sqrt(np.sum((crop[floor_in_crop:, :].astype(np.float32) - floor_color) ** 2, axis=2))
        mask[floor_in_crop:, :][diff_floor < 35] = 0
        
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = mask
    return rgba

# 1. Junior Hands Up (pose_3s, yellow bg)
rgba_j_up = extract_clean_sprite(
    os.path.join(POSES_DIR, "pose_3s.jpg"),
    (80, 1030, 470, 1920),
    (20, 20),
    50
)
cv2.imwrite(os.path.join(ASSETS_DIR, "junior_hands_up.png"), rgba_j_up)

# 2. Junior Shrug (pose_25s, green bg)
rgba_j_shrug = extract_clean_sprite(
    os.path.join(POSES_DIR, "pose_25s.jpg"),
    (0, 1030, 560, 1920),
    (20, 20),
    45
)
cv2.imwrite(os.path.join(ASSETS_DIR, "junior_shrug.png"), rgba_j_shrug)

# 3. Junior Pointing (pose_18s, blue bg)
rgba_j_point = extract_clean_sprite(
    os.path.join(POSES_DIR, "pose_18s.jpg"),
    (130, 1030, 550, 1920),
    (20, 20),
    45
)
cv2.imwrite(os.path.join(ASSETS_DIR, "junior_pointing.png"), rgba_j_point)

# 4. Senior Clasped (pose_18s, blue bg)
rgba_s_clasp = extract_clean_sprite(
    os.path.join(POSES_DIR, "pose_18s.jpg"),
    (570, 1030, 940, 1920),
    (20, 20),
    45
)
cv2.imwrite(os.path.join(ASSETS_DIR, "senior_clasped.png"), rgba_s_clasp)

# 5. Senior Pointing Up (pose_25s, green bg)
rgba_s_point = extract_clean_sprite(
    os.path.join(POSES_DIR, "pose_25s.jpg"),
    (530, 1030, 980, 1920),
    (20, 20),
    45
)
cv2.imwrite(os.path.join(ASSETS_DIR, "senior_pointing_up.png"), rgba_s_point)

# 6. Senior Explaining / Open Arms (pose_10s, blue bg)
rgba_s_open = extract_clean_sprite(
    os.path.join(POSES_DIR, "pose_12s.jpg"),
    (480, 1030, 990, 1920),
    (20, 20),
    45
)
cv2.imwrite(os.path.join(ASSETS_DIR, "senior_explaining.png"), rgba_s_open)

print("All 6 sprites cleanly extracted and saved!")
