import cv2
import os

f_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\ref_forensics"

# Crop the character face region at frame 0, 2, 4, 6, 8
for i in [0, 2, 4, 6, 8]:
    im = cv2.imread(os.path.join(f_dir, f"ref4_speaking_f{i}.jpg"))
    # Junior is on the left: X ~ [150, 450], Y ~ [1050, 1500]
    face_crop = im[1080:1450, 200:450]
    cv2.imwrite(os.path.join(f_dir, f"crop_face_f{i}.jpg"), face_crop)
    
print("Saved face crops!")
