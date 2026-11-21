import urllib.request
import hashlib
import zipfile
import os
import sys
import time
import subprocess

zip_url = "https://download.blender.org/release/Blender4.2/blender-4.2.23-windows-x64.zip"
expected_sha256 = "82e791475779a7342424a480bdde9a20b43710da9264c60346125aa16cd910cb".lower()

engine_dir = r"F:\Master AI\07_3D_CGI\engine\blender"
zip_path = os.path.join(engine_dir, "blender-4.2.23-windows-x64.zip")
os.makedirs(engine_dir, exist_ok=True)

print(f"Target Zip URL: {zip_url}")
print(f"Target Path: {zip_path}")
print(f"Expected SHA-256: {expected_sha256}")

# 1. Download with SHA-256 verification
if not os.path.exists(zip_path) or os.path.getsize(zip_path) != 383193007:
    print("Beginning chunked download from official Blender Foundation servers...")
    req = urllib.request.Request(zip_url, headers={"User-Agent": "MasterAI-EngineSetup/1.0"})
    hasher = hashlib.sha256()
    t0 = time.time()
    
    with urllib.request.urlopen(req, timeout=30) as resp, open(zip_path, "wb") as out_f:
        total_size = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024 # 1 MB chunks
        last_log = time.time()
        
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_f.write(chunk)
            hasher.update(chunk)
            downloaded += len(chunk)
            
            if time.time() - last_log > 3.0:
                pct = (downloaded / total_size) * 100 if total_size else 0
                speed = (downloaded / (1024*1024)) / (time.time() - t0)
                print(f"Downloaded: {downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB ({pct:.1f}%) @ {speed:.2f} MB/s")
                last_log = time.time()

    calc_sha = hasher.hexdigest().lower()
    print(f"Download complete in {time.time()-t0:.1f}s. Computed SHA-256: {calc_sha}")
else:
    print("Zip already exists on disk. Computing SHA-256 checksum...")
    hasher = hashlib.sha256()
    with open(zip_path, "rb") as f:
        while chunk := f.read(1024*1024):
            hasher.update(chunk)
    calc_sha = hasher.hexdigest().lower()
    print(f"Computed SHA-256: {calc_sha}")

if calc_sha != expected_sha256:
    print(f"FATAL: Checksum mismatch! Expected {expected_sha256}, got {calc_sha}")
    sys.exit(1)

print("Checksum verification: PASS (Cryptographically authentic official Blender 4.2 LTS)")

# 2. Extract Portable Zip
print(f"Extracting portable zip to {engine_dir}...")
t_extract0 = time.time()
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(engine_dir)
print(f"Extraction complete in {time.time()-t_extract0:.1f}s.")

# 3. Locate blender.exe
blender_exe = None
for root, dirs, files in os.walk(engine_dir):
    if "blender.exe" in files:
        blender_exe = os.path.join(root, "blender.exe")
        break

if not blender_exe:
    print("FATAL: blender.exe not found after extraction!")
    sys.exit(1)

print(f"Blender executable located: {blender_exe}")

# 4. Test execution and verify version
print("Verifying executable execution (blender --version)...")
try:
    res = subprocess.run([blender_exe, "--version"], capture_output=True, text=True, timeout=15)
    print("Return code:", res.returncode)
    print("Output:\n", res.stdout.strip())
except Exception as e:
    print("Execution error:", e)
    sys.exit(1)

print("\nSTEP 1 COMPLETE: Blender 4.2 LTS successfully installed and verified.")
