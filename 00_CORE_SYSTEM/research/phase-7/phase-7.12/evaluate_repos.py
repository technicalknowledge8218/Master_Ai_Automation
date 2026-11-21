import os
import json
import urllib.request

REPOS = [
    ("OpenMontage", "OpenMontageInc/OpenMontage"),
    ("OpenDirector", "seme-org/open-director"),
    ("ComfyUI", "Comfy-Org/ComfyUI"),
    ("OpenBone", "UXCentury/open-bone"),
    ("OpenToonz", "opentoonz/opentoonz")
]

OUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.12\repo_eval"
os.makedirs(OUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/vnd.github.v3+json"
}

summary = {}

for name, repo_slug in REPOS:
    print(f"\nEvaluating {name} ({repo_slug})...")
    repo_data = {}
    
    # 1. Repo info
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo_slug}", headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            repo_info = json.loads(r.read().decode("utf-8"))
            repo_data["info"] = {
                "name": repo_info.get("name"),
                "full_name": repo_info.get("full_name"),
                "description": repo_info.get("description"),
                "stars": repo_info.get("stargazers_count"),
                "forks": repo_info.get("forks_count"),
                "open_issues": repo_info.get("open_issues_count"),
                "created_at": repo_info.get("created_at"),
                "updated_at": repo_info.get("updated_at"),
                "pushed_at": repo_info.get("pushed_at"),
                "size_kb": repo_info.get("size"),
                "license": repo_info.get("license"),
                "default_branch": repo_info.get("default_branch"),
                "language": repo_info.get("language")
            }
            print(f"  Stars: {repo_info.get('stargazers_count')} | License: {repo_info.get('license', {}).get('spdx_id') if repo_info.get('license') else 'None'}")
    except Exception as e:
        print(f"  Failed repo info: {e}")
        repo_data["info_error"] = str(e)
        
    # 2. README
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo_slug}/readme", headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3.raw"})
        with urllib.request.urlopen(req, timeout=15) as r:
            readme_text = r.read().decode("utf-8", errors="ignore")
            repo_data["readme_excerpt"] = readme_text[:2000]
            with open(os.path.join(OUT_DIR, f"{name}_README.md"), "w", encoding="utf-8") as f_out:
                f_out.write(readme_text)
            print(f"  Saved {name}_README.md ({len(readme_text)} bytes)")
    except Exception as e:
        print(f"  Failed readme: {e}")
        repo_data["readme_error"] = str(e)
        
    # 3. Directory listing of root
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo_slug}/contents", headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            contents = json.loads(r.read().decode("utf-8"))
            repo_data["root_files"] = [c.get("name") for c in contents]
            print(f"  Root files: {repo_data['root_files'][:12]}")
    except Exception as e:
        print(f"  Failed root contents: {e}")
        repo_data["contents_error"] = str(e)

    summary[name] = repo_data

with open(os.path.join(OUT_DIR, "repos_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("\nSaved repos_metadata.json successfully!")
