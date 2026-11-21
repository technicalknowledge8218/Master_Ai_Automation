import urllib.request
import re

url = 'https://download.blender.org/release/Blender4.2/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')

for m in re.finditer(r'href="([^"]+)"', html):
    val = m.group(1)
    if 'sha256' in val or 'md5' in val or 'windows-x64.zip' in val:
        print(val)
