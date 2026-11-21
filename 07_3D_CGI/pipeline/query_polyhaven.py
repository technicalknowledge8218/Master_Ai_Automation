import urllib.request
import json

headers = {"User-Agent": "MasterAI-AssetEngine/1.0"}

# Check Poly Haven HDRIs
req = urllib.request.Request("https://api.polyhaven.com/assets?t=hdris", headers=headers)
with urllib.request.urlopen(req) as resp:
    hdris = json.loads(resp.read().decode())
    savanna_hdris = [k for k, v in hdris.items() if any(tag in v.get("tags", []) or tag in k for tag in ["sunset", "sun", "field", "africa", "desert", "plains"])]
    print("Found matching HDRIs:", savanna_hdris[:10])

# Check Poly Haven Textures
req_tex = urllib.request.Request("https://api.polyhaven.com/assets?t=textures", headers=headers)
with urllib.request.urlopen(req_tex) as resp:
    texs = json.loads(resp.read().decode())
    ground_texs = [k for k, v in texs.items() if any(tag in v.get("tags", []) or tag in k for tag in ["ground", "mud", "sand", "dirt", "rock"])]
    print("Found matching Ground Textures:", ground_texs[:10])
