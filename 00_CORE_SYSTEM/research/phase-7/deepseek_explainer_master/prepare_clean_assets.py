import cv2
import numpy as np
import os
from PIL import Image

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
POSES_DIR = r"F:\Master AI\15_ASSETS\reference_videos\instagram_refs\ref_04_poses"

# 1. Clean Empty Whiteboard
wb = cv2.imread(os.path.join(ASSETS_DIR, "whiteboard_frame.png"))
# The inner writable area is roughly from y=100 to y=920, x=100 to x=910
# We can flood-fill or fill the inner whiteboard area with clean whiteboard white (#FCFCFA)
# Keep the outer bezel and tray intact
h_wb, w_wb, _ = wb.shape
wb_clean = wb.copy()
# Inner rectangle is x=40 to w_wb-40, y=30 to h_wb-60
cv2.rectangle(wb_clean, (45, 35), (w_wb - 45, h_wb - 65), (250, 252, 252), -1)
# Restore inner subtle border line
cv2.rectangle(wb_clean, (45, 35), (w_wb - 45, h_wb - 65), (220, 226, 230), 2)
# Make outer corners transparent
bg_wb = wb_clean[10, 10].astype(np.float32)
diff_wb = np.sqrt(np.sum((wb_clean.astype(np.float32) - bg_wb)**2, axis=2))
mask_wb = np.where(diff_wb < 30, 0, 255).astype(np.uint8)
wb_rgba = cv2.cvtColor(wb_clean, cv2.COLOR_BGR2BGRA)
wb_rgba[:, :, 3] = mask_wb
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_whiteboard_empty.png"), wb_rgba)
print("Created clean_whiteboard_empty.png")

# 2. Process Junior Hands Up (remove speech bubble on top right)
j_up = cv2.imread(os.path.join(ASSETS_DIR, "junior_hands_up.png"), cv2.IMREAD_UNCHANGED)
# Crop speech bubble: any pixel at x > 280 and y < 150
j_up_clean = j_up.copy()
j_up_clean[:140, 260:, 3] = 0
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_junior_hands_up.png"), j_up_clean)
print("Created clean_junior_hands_up.png")

# 3. Process Senior Pointing Up (remove any sliver on the left)
s_pt = cv2.imread(os.path.join(ASSETS_DIR, "senior_pointing_up.png"), cv2.IMREAD_UNCHANGED)
s_pt_clean = s_pt.copy()
s_pt_clean[:, :50, 3] = 0 # Clean left margin
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png"), s_pt_clean)
print("Created clean_senior_pointing_up.png")

# 4. Process Senior Clasped
s_clasp = cv2.imread(os.path.join(ASSETS_DIR, "senior_clasped.png"), cv2.IMREAD_UNCHANGED)
s_clasp_clean = s_clasp.copy()
s_clasp_clean[:, :50, 3] = 0
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_senior_clasped.png"), s_clasp_clean)
print("Created clean_senior_clasped.png")

# 5. Process Junior Pointing
j_pt = cv2.imread(os.path.join(ASSETS_DIR, "junior_pointing.png"), cv2.IMREAD_UNCHANGED)
j_pt_clean = j_pt.copy()
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_junior_pointing.png"), j_pt_clean)
print("Created clean_junior_pointing.png")

# 6. Process Junior Shrug
j_shrug = cv2.imread(os.path.join(ASSETS_DIR, "junior_shrug.png"), cv2.IMREAD_UNCHANGED)
j_shrug_clean = j_shrug.copy()
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_junior_shrug.png"), j_shrug_clean)
print("Created clean_junior_shrug.png")

# 7. Process Senior Explaining
s_exp = cv2.imread(os.path.join(ASSETS_DIR, "senior_explaining.png"), cv2.IMREAD_UNCHANGED)
s_exp_clean = s_exp.copy()
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_senior_explaining.png"), s_exp_clean)
print("Created clean_senior_explaining.png")
