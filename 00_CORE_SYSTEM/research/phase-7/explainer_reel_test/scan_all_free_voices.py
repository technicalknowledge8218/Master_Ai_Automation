import asyncio
import os
import edge_tts

async def get_all_target_voices():
    voices = await edge_tts.list_voices()
    targets = ['hi-IN', 'en-IN', 'ur-IN', 'ur-PK', 'en-US', 'en-GB']
    selected = []
    for v in voices:
        loc = v.get('Locale', '')
        short_name = v.get('ShortName', '')
        if any(loc.startswith(t) for t in targets):
            selected.append({
                "short_name": short_name,
                "gender": v.get("Gender"),
                "locale": loc,
                "friendly_name": v.get("FriendlyName")
            })
    print(f"Total target Edge-TTS voices found: {len(selected)}")
    for s in selected:
        print(f"  {s['short_name']:<32} | {s['gender']:<6} | {s['locale']}")

if __name__ == "__main__":
    asyncio.run(get_all_target_voices())
