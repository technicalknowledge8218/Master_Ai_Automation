import urllib.request
import urllib.error
import json

key = os.environ.get("GEMINI_API_KEY", "")

print("--- Testing key on Generative Language API ---")
url1 = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
try:
    with urllib.request.urlopen(url1) as resp:
        print("Test 1 (Query Param ?key=): SUCCESS 200 OK")
        data = json.loads(resp.read().decode())
        print(f"Total models returned: {len(data.get('models', []))}")
except urllib.error.HTTPError as e:
    print(f"Test 1 Failed: {e.code} - {e.read().decode()[:200]}")

req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models", headers={"Authorization": f"Bearer {key}"})
try:
    with urllib.request.urlopen(req) as resp:
        print("Test 2 (Bearer Header): SUCCESS 200 OK")
except urllib.error.HTTPError as e:
    print(f"Test 2 Failed: {e.code} - {e.read().decode()[:200]}")
