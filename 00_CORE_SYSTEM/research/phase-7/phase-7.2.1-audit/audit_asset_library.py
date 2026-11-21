"""
Audit asset_catalog.json against disk files and SHA-256
"""
import os
import json
import hashlib

CATALOG_PATH = r"F:\Master AI\15_ASSETS\open_source_library\asset_catalog.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

assets = catalog.get("assets", {})
print(f"Total catalog entries: {len(assets)}")

verified_count = 0
quarantined_count = 0
failed_count = 0

for aid, rec in assets.items():
    lpath = rec.get("local_path")
    exists = os.path.isfile(lpath)
    stored_sha = rec.get("sha256")
    q_status = rec.get("quarantine_status")
    
    if not exists:
        print(f"[-] {aid}: FILE MISSING at {lpath}")
        failed_count += 1
        continue
        
    # Compute SHA-256
    hasher = hashlib.sha256()
    with open(lpath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    actual_sha = hasher.hexdigest()
    
    match = (actual_sha.lower() == stored_sha.lower())
    fsize = os.path.getsize(lpath)
    
    print(f"[{'PASS' if match else 'FAIL'}] {aid}: {rec.get('title')} ({fsize} bytes) | Status: {q_status} | SHA Match: {match}")
    if match and q_status == "APPROVED":
        verified_count += 1
    elif q_status == "QUARANTINED":
        quarantined_count += 1
    else:
        failed_count += 1

print(f"\nSummary: {verified_count} Approved & Verified, {quarantined_count} Quarantined, {failed_count} Failed.")
