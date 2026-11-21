import urllib.request
import re

url = "https://download.blender.org/release/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')

dirs = re.findall(r'href="(Blender[^"/]+)/"', html)
print("Latest Blender release dirs:", dirs[-12:])

for target in ["Blender5.2", "Blender5.1", "Blender5.0", "Blender4.3"]:
    if target in dirs:
        sub_url = f"{url}{target}/"
        sreq = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(sreq, timeout=10) as sresp:
                s_html = sresp.read().decode('utf-8')
            zips = re.findall(r'href="([^"/]+windows[^"/]+\.zip)"', s_html)
            sha_files = re.findall(r'href="([^"/]+\.sha256)"', s_html)
            print(f"\n{target} Windows ZIPs:", zips)
            print(f"{target} SHA256 files:", sha_files[:5])
        except Exception as e:
            print(f"{target} error:", e)
