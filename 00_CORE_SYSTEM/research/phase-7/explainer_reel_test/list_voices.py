import asyncio
import edge_tts

async def list_ind():
    voices = await edge_tts.list_voices()
    for v in voices:
        loc = v.get("Locale", "")
        if "IN" in loc or "hi-" in loc:
            print(f"{v['ShortName']:<30} | {v['Gender']:<8} | {v['Locale']}")

if __name__ == "__main__":
    asyncio.run(list_ind())
