#!/usr/bin/env python3
"""
MASTER-AI Technical Research Metadata Verification Helper
Queries official package registries (PyPI, npm) to verify package existence, latest version, and license.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

def verify_pypi(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    req = urllib.request.Request(url, headers={"User-Agent": "MasterAI-Research/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            info = data.get("info", {})
            return {
                "ecosystem": "pypi",
                "name": info.get("name"),
                "version": info.get("version"),
                "license": info.get("license"),
                "summary": info.get("summary"),
                "project_url": info.get("project_url") or info.get("home_page"),
                "verified": True
            }
    except urllib.error.HTTPError as e:
        return {"ecosystem": "pypi", "name": package_name, "error": f"HTTP {e.code}: Not found", "verified": False}
    except Exception as e:
        return {"ecosystem": "pypi", "name": package_name, "error": str(e), "verified": False}

def verify_npm(package_name):
    url = f"https://registry.npmjs.org/{package_name}"
    req = urllib.request.Request(url, headers={"User-Agent": "MasterAI-Research/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            dist_tags = data.get("dist-tags", {})
            latest_version = dist_tags.get("latest")
            versions = data.get("versions", {})
            ver_info = versions.get(latest_version, {})
            return {
                "ecosystem": "npm",
                "name": data.get("name"),
                "version": latest_version,
                "license": ver_info.get("license") or data.get("license"),
                "summary": data.get("description"),
                "homepage": data.get("homepage"),
                "verified": True
            }
    except urllib.error.HTTPError as e:
        return {"ecosystem": "npm", "name": package_name, "error": f"HTTP {e.code}: Not found", "verified": False}
    except Exception as e:
        return {"ecosystem": "npm", "name": package_name, "error": str(e), "verified": False}

def main():
    parser = argparse.ArgumentParser(description="Verify package metadata on official registries")
    parser.add_argument("--package", required=True, help="Package name to verify")
    parser.add_argument("--ecosystem", choices=["pypi", "npm"], default="pypi", help="Registry ecosystem")
    args = parser.parse_args()

    if args.ecosystem == "pypi":
        result = verify_pypi(args.package)
    else:
        result = verify_npm(args.package)

    print(json.dumps(result, indent=2))
    if not result.get("verified"):
        sys.exit(1)

if __name__ == "__main__":
    main()
