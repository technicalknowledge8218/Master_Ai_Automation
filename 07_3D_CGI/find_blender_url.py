import urllib.request
import re

# Find available official portable Blender releases
base_url = "https://download.blender.org/release/"
req = urllib.request.Request(base_url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8')
    dirs = re.findall(r'href="(Blender\d+\.\d+)/"', html)
    print("Found release dirs:", dirs[-6:])

    # Check the latest LTS releases (e.g. Blender4.2, Blender4.1, Blender4.0, Blender3.6)
    target_dirs = ["Blender4.2", "Blender4.1", "Blender4.0", "Blender3.6"]
    for tdir in target_dirs:
        sub_url = f"{base_url}{tdir}/"
        sreq = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(sreq, timeout=10) as sresp:
                s_html = sresp.read().decode('utf-8')
            # Look for windows zip
            zips = re.findall(r'href="([^"]+windows[^"]+\.zip)"', s_html, re.IGNORECASE)
            print(f"\n--- {tdir} Windows ZIPs ---")
            for z in zips[-3:]:
                print(f"{sub_url}{z}")
        except Exception as se:
            print(f"Error checking {tdir}:", se)

except Exception as e:
    print("Error:", e)
