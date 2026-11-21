import os

root = r"F:\Master AI"
sfx_files = []
for dirpath, dirnames, filenames in os.walk(root):
    if ".venv" in dirpath or "node_modules" in dirpath: continue
    for f in filenames:
        if f.endswith(".wav") and ("sfx" in f.lower() or "whoosh" in f.lower() or "pop" in f.lower() or "bell" in f.lower() or "ding" in f.lower() or "alarm" in f.lower()):
            sfx_files.append(os.path.join(dirpath, f))

print(f"Total SFX found: {len(sfx_files)}")
for p in sfx_files[:15]:
    print(" -", p)
