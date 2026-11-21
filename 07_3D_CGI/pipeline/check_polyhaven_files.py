import urllib.request
import json

headers = {"User-Agent": "MasterAI-AssetEngine/1.0"}

req = urllib.request.Request("https://api.polyhaven.com/files/aarfontein_sunrise", headers=headers)
with urllib.request.urlopen(req) as resp:
    files = json.loads(resp.read().decode())
    print("aarfontein_sunrise formats:", list(files.keys()))
    if "hdri" in files:
        print("hdri res:", list(files["hdri"].keys()))
        if "1k" in files["hdri"]:
            print("1k url:", files["hdri"]["1k"]["hdr"]["url"])

req2 = urllib.request.Request("https://api.polyhaven.com/files/aerial_ground_rock", headers=headers)
with urllib.request.urlopen(req2) as resp:
    files2 = json.loads(resp.read().decode())
    print("aerial_ground_rock formats:", list(files2.keys()))
    if "blend" in files2:
        print("blend:", files2["blend"])
    elif "diffuse" in files2:
        print("diffuse:", list(files2["diffuse"].keys()))
