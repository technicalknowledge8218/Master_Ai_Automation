import cv2
import numpy as np
import os

ASSETS_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master\ref_assets"
wb = cv2.imread(os.path.join(ASSETS_DIR, "whiteboard_frame.png"))

# Inner fill box
cv2.rectangle(wb, (80, 75), (930, 920), (255, 255, 255), -1)

# Make background outside frame transparent
# In pose_18s, background was at corner (10, 10)
bg_col = wb[10, 10].astype(np.float32)
diff = np.sqrt(np.sum((wb.astype(np.float32) - bg_col)**2, axis=2))
mask = np.where(diff < 35, 0, 255).astype(np.uint8)

wb_rgba = cv2.cvtColor(wb, cv2.COLOR_BGR2BGRA)
wb_rgba[:, :, 3] = mask

cv2.imwrite(os.path.join(ASSETS_DIR, "perfect_whiteboard.png"), wb_rgba)
print("Saved perfect_whiteboard.png!")
