import asyncio
import edge_tts

async def test_ssml():
    text_plain = "अरे भाई, ये तुमने क्या कर दिया? मैंने तुमसे कहा था कि फाइल मत डिलीट करना!"
    text_ssml = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
        <voice name="hi-IN-MadhurNeural">
            <prosody pitch="+5Hz" rate="+6%">
                अरे भाई! ये तुमने क्या कर दिया?!
            </prosody>
            <break time="250ms"/>
            <prosody pitch="-2Hz" rate="+2%">
                मैंने तुमसे साफ़-साफ़ कहा था कि फाइल मत छूना!
            </prosody>
        </voice>
    </speak>"""
    
    comm1 = edge_tts.Communicate(text_plain, "hi-IN-MadhurNeural")
    await comm1.save("F:/Master AI/00_CORE_SYSTEM/research/phase-7/phase-7.7.3/audio/test_plain.mp3")
    
    comm2 = edge_tts.Communicate(text_ssml, "hi-IN-MadhurNeural")
    await comm2.save("F:/Master AI/00_CORE_SYSTEM/research/phase-7/phase-7.7.3/audio/test_ssml.mp3")
    print("SSML test generated successfully!")

asyncio.run(test_ssml())
