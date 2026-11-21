import os
import json
import datetime
import argparse
import sys
import importlib
from pathlib import Path

# Resolve workspace root dynamically via centralized path configuration
_current_dir = Path(__file__).resolve().parent
_workspace_candidate = _current_dir.parents[1]
if str(_workspace_candidate) not in sys.path:
    sys.path.insert(0, str(_workspace_candidate))

try:
    _path_config = importlib.import_module("00_CORE_SYSTEM.config.path_config")
    WORKSPACE_ROOT = str(_path_config.WORKSPACE_ROOT)
except Exception:
    WORKSPACE_ROOT = os.getenv("MASTER_AI_ROOT", str(_workspace_candidate))

STAGES = [
    "DISCOVER", "RESEARCH", "VERIFY", "DOCUMENT",
    "TEST", "EVALUATE", "PROPOSE", "APPROVE", "INTEGRATE", "MONITOR"
]

CATEGORIES = [
    "Verified Knowledge", "Experimental Knowledge",
    "Research Notes", "Deprecated Knowledge",
    "Unverified Claims", "Reusable Engineering Patterns"
]

def create_knowledge_entry(topic, category, tech_name, tech_version, source_url, notes, experiment_code=None):
    if category not in CATEGORIES:
        raise ValueError(f"Category must be one of: {CATEGORIES}")

    year = datetime.datetime.now().strftime("%Y")
    # Count existing
    idx_path = os.path.join(WORKSPACE_ROOT, "00_CORE_SYSTEM", "registry", "KNOWLEDGE_INDEX.md")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    entry_id = f"KNOW-{year}-{timestamp[-4:]}"

    record = {
        "id": entry_id,
        "topic": topic,
        "category": category,
        "technology": tech_name,
        "technology_version": tech_version,
        "verification_status": "VERIFIED" if category in ["Verified Knowledge", "Reusable Engineering Patterns"] else "EXPERIMENTAL",
        "source_urls": [source_url],
        "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "notes": notes
    }

    # Decide target folder
    if category in ["Verified Knowledge", "Reusable Engineering Patterns"]:
        target_dir = os.path.join(WORKSPACE_ROOT, "13_MARKDOWN", "guides")
    elif category == "Experimental Knowledge":
        target_dir = os.path.join(WORKSPACE_ROOT, "21_LEARNING_LAB", "experiments")
    elif category == "Deprecated Knowledge":
        target_dir = os.path.join(WORKSPACE_ROOT, "13_MARKDOWN", "summaries", "deprecated")
    else:
        target_dir = os.path.join(WORKSPACE_ROOT, "21_LEARNING_LAB", "notes")

    os.makedirs(target_dir, exist_ok=True)
    slug = "".join([c if c.isalnum() else "_" for c in topic.lower()]).strip("_")[:40]
    filename = f"{entry_id}_{slug}.md"
    file_path = os.path.join(target_dir, filename)

    content = f"""---
id: {entry_id}
topic: "{topic}"
category: "{category}"
technology: "{tech_name}"
technology_version: "{tech_version}"
verification_status: "{record['verification_status']}"
source_urls:
  - "{source_url}"
created_date: "{record['created_date']}"
---

# {topic}

> **Knowledge ID**: `{entry_id}`  
> **Category**: `{category}`  
> **Lifecycle Stage**: `DOCUMENT` (Progressing through Lifecycle)  

## 1. Executive Summary
{notes}

## 2. Technical Details & Reproducible Evidence
- **Technology**: `{tech_name}` (`{tech_version}`)
- **Official Source**: [{source_url}]({source_url})
"""

    if experiment_code:
        content += f"""
```python
{experiment_code}
```
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created knowledge entry at: {file_path}")
    return file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tracked knowledge entry")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--category", choices=CATEGORIES, required=True)
    parser.add_argument("--tech", default="General")
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--url", default="https://official.example.com")
    parser.add_argument("--notes", default="Documented via learning lifecycle.")
    args = parser.parse_args()

    create_knowledge_entry(args.topic, args.category, args.tech, args.version, args.url, args.notes)
