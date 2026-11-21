import cv2
import numpy as np
import os
from PIL import Image

OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
os.makedirs(OUT_DIR, exist_ok=True)

# Let's inspect pose_18s (Sky blue background #8DC5E8 approx)
img = cv2.imread(r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04_poses\pose_18s.jpg")
h, w, _ = img.shape

# The background color at (50, 50)
bg_color = img[50, 50].astype(int)
print("Detected BG Color at (50,50):", bg_color)

# Whiteboard crop: Y from 80 to 1080, X from 35 to 1045
wb_crop = img[80:1085, 35:1045]
cv2.imwrite(os.path.join(OUT_DIR, "whiteboard_frame.png"), wb_crop)
print("Saved whiteboard_frame.png:", wb_crop.shape)

# Junior Character crop from pose_18s (Junior is on the left: X from 120 to 560, Y from 1050 to 1920)
junior_crop = img[1050:1920, 130:560]
cv2.imwrite(os.path.join(OUT_DIR, "junior_pose18_raw.png"), junior_crop)

# Senior Character crop from pose_18s (Senior is on the right: X from 550 to 950, Y from 1050 to 1920)
senior_crop = img[1050:1920, 560:950]
cv2.imwrite(os.path.join(OUT_DIR, "senior_pose18_raw.png"), senior_crop)

# Also from pose_3s (Hands up Junior, Clasped Senior, Yellow background)
img3 = cv2.imread(r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04_poses\pose_3s.jpg")
junior_hands_up = img3[900:1920, 80:480]
cv2.imwrite(os.path.join(OUT_DIR, "junior_hands_up_raw.png"), junior_hands_up)

# Also from pose_25s (Shrugging Junior, Pointing Senior, Green background)
img25 = cv2.imread(r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04_poses\pose_25s.jpg")
junior_shrug = img25[1050:1920, 0:560]
cv2.imwrite(os.path.join(OUT_DIR, "junior_shrug_raw.png"), junior_shrug)
senior_point = img25[1050:1920, 520:980]
cv2.imwrite(os.path.join(OUT_DIR, "senior_point_raw.png"), senior_point)

print("Key crops extracted successfully!")
