import urllib.request

for ver in ["4.2.23", "4.2.22", "4.2.21", "4.2.0"]:
    url = f"https://download.blender.org/release/Blender4.2/blender-{ver}.sha256"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode('utf-8')
            for line in text.splitlines():
                if "windows-x64.zip" in line:
                    print(f"Blender {ver} SHA256: {line.strip()}")
    except Exception as e:
        print(f"Error {ver}:", e)
