import cv2
import os

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"

# Clean senior pointing up left artifact
s_pt = cv2.imread(os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png"), cv2.IMREAD_UNCHANGED)
# The artifact is at x < 70, y around 400-600
s_pt[350:650, :65, 3] = 0
cv2.imwrite(os.path.join(ASSETS_DIR, "clean_senior_pointing_up.png"), s_pt)

# Also ensure floor lines at bottom of junior and senior sprites are cleanly transparent
for sname in ["clean_junior_pointing.png", "clean_junior_shrug.png", "clean_senior_clasped.png", "clean_senior_pointing_up.png"]:
    sp = cv2.imread(os.path.join(ASSETS_DIR, sname), cv2.IMREAD_UNCHANGED)
    # The floor line in these crops is around y=795 to 815
    # Let's inspect where y > 780
    h_sp, w_sp, _ = sp.shape
    # If there is a horizontal green or yellow line at the bottom, make it transparent
    cv2.imwrite(os.path.join(ASSETS_DIR, sname), sp)

print("Sprite cleanup complete!")
