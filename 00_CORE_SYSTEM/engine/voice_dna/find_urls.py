import json
import re

path = r"C:\Users\Sangam\.gemini\antigravity\brain\d97bdd64-3973-442c-a0dd-850f28dc3c0d\.system_generated\logs\transcript.jsonl"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        try:
            d = json.loads(line)
            if d.get("source") == "USER_EXPLICIT":
                text = d.get("content", "")
                urls = re.findall(r"https?://[^\s\"\'\<\>]+", text)
                for u in urls:
                    print(f"User URL (line {i}): {u}")
        except Exception:
            pass
