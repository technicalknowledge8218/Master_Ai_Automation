import urllib.request
import json

headers = {"User-Agent": "MasterAI-AssetEngine/1.0 (Research&Education)"}

try:
    req = urllib.request.Request("https://ambientcg.com/api/v2/full_json?limit=1", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print("ambientCG API: SUCCESS, count:", len(data.get("foundAssets", [])))
except Exception as e:
    print("ambientCG API:", e)

try:
    req2 = urllib.request.Request("https://api.polyhaven.com/assets?t=textures", headers=headers)
    with urllib.request.urlopen(req2, timeout=10) as resp:
        data2 = json.loads(resp.read().decode())
        print("Poly Haven API: SUCCESS, count:", len(data2.keys()))
except Exception as e:
    print("Poly Haven API:", e)
