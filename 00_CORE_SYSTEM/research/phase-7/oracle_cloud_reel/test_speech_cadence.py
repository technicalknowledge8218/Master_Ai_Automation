import asyncio
import edge_tts
import os

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel"

# Test 1: Plain single string (the old way)
plain_text = "Agar aap Oracle Cloud ka Free Tier VM use kar rahe ho, toh sunno! Saat din baad aapka server automatic DELETE ho sakta hai!"

# Test 2: Chunked SSML with natural human rhythm, pauses, and emphasis
ssml_text = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
    <voice name="hi-IN-MadhurNeural">
        <prosody rate="+12%" pitch="+2Hz">
            Agar aap Oracle Cloud ka Free Tier VM use kar rahe ho?
            <break time="250ms"/>
            Toh dhyan se sunna!
            <break time="300ms"/>
            Sirf saat din ke andar...
            <break time="150ms"/>
            Aapka poora server automatic DELETE ho sakta hai!
        </prosody>
    </voice>
</speak>"""

async def test():
    c1 = edge_tts.Communicate(plain_text, "hi-IN-MadhurNeural", rate="+15%")
    await c1.save(os.path.join(out_dir, "test_speech_plain.mp3"))
    print("Saved test_speech_plain.mp3")
    
    # Using SSML directly
    # Note: edge_tts supports passing text or SSML
    # If using Communicate, let's see how SSML behaves or if we use punctuated clauses
    # Let's also test punctuated burst chunks
    chunks = [
        ("Agar aap Oracle Cloud ka Free Tier VM use kar rahe ho?", "+14%", "+2Hz", 0.22),
        ("Toh dhyan se sunna!", "+16%", "+4Hz", 0.28),
        ("Saat din ke andar...", "+10%", "+1Hz", 0.18),
        ("Aapka server automatic DELETE ho sakta hai!", "+16%", "+3Hz", 0.35)
    ]
    
    # We will generate each burst and stitch them with exact micro-pauses
    import soundfile as sf
    import numpy as np
    
    stitched_audio = []
    sr = 24000
    
    for i, (txt, rate, pitch, pause_s) in enumerate(chunks):
        f = os.path.join(out_dir, f"burst_{i}.mp3")
        comm = edge_tts.Communicate(txt, "hi-IN-MadhurNeural", rate=rate, pitch=pitch)
        await comm.save(f)
        data, file_sr = sf.read(f)
        if len(data.shape) > 1: data = data.mean(axis=1)
        sr = file_sr
        stitched_audio.append(data)
        # Add human breathing pause
        pause_samples = int(pause_s * sr)
        stitched_audio.append(np.zeros(pause_samples, dtype=np.float32))
        
    full_audio = np.concatenate(stitched_audio)
    sf.write(os.path.join(out_dir, "test_speech_burst_stitched.wav"), full_audio, sr)
    print("Saved test_speech_burst_stitched.wav with human conversational cadence!")

asyncio.run(test())
