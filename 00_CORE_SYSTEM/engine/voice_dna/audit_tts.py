import os

root = r"F:\Master AI"
tts_files = []
for dirpath, dirnames, filenames in os.walk(root):
    if ".venv" in dirpath or "node_modules" in dirpath or ".git" in dirpath:
        continue
    for f in filenames:
        if "tts" in f.lower() or "voice" in f.lower():
            tts_files.append(os.path.join(dirpath, f))

print(f"Total TTS/Voice files found in Master AI: {len(tts_files)}")
for p in tts_files[:25]:
    print(f" - {p}")
