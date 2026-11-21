import os

keys = ['GEMINI_API_KEY', 'GOOGLE_API_KEY', 'AZURE_SPEECH_KEY', 'AZURE_SPEECH_REGION', 'ELEVEN_API_KEY']
for k in keys:
    val = os.environ.get(k)
    status = f"SET (len={len(val)})" if val else "NOT SET"
    print(f"{k}: {status}")
