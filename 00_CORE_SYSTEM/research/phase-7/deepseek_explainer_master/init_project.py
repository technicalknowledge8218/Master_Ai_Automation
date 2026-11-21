import os

NEW_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\deepseek_explainer_master"
os.makedirs(os.path.join(NEW_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(NEW_DIR, "snapshots"), exist_ok=True)
print("Created production directory:", NEW_DIR)
