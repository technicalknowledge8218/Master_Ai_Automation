import os
import sys
import json
import subprocess
from pathlib import Path

root = Path("F:/Master AI")

print("Searching for files...")
for p in root.rglob("*.py"):
    if "motion" in p.name.lower() or "timeline" in p.name.lower() or "bridge" in p.name.lower():
        print(f"Found code: {p}")

for p in root.rglob("*.mp4"):
    if "scene" in p.name.lower() or "pilot" in p.name.lower():
        print(f"Found mp4: {p}")

