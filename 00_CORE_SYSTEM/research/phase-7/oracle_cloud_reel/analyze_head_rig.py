import os
from PIL import Image

cdir = r"F:\Master AI\CHARACTER_LIBRARY"
test_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\rig_test"
os.makedirs(test_dir, exist_ok=True)

# Arjun pointing (291x677): head is roughly the top 220px
im_arjun = Image.open(os.path.join(cdir, "arjun_pointing.png"))
head_arjun = im_arjun.crop((20, 0, 270, 220))
head_arjun.save(os.path.join(test_dir, "arjun_head_sample.png"))

# Dr. Kabir explaining (280x698): head is top 230px
im_kabir = Image.open(os.path.join(cdir, "dr_kabir_explaining.png"))
head_kabir = im_kabir.crop((20, 0, 260, 230))
head_kabir.save(os.path.join(test_dir, "dr_kabir_head_sample.png"))

print("Saved head crops for rig analysis!")
