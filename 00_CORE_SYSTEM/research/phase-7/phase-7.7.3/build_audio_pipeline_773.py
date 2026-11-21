"""
build_audio_pipeline_773.py
===========================
Generates the complete 60.00-second professional audio suite for:
"लास्ट बग" (The Last Bug) - Phase 7.7.3

Deliverables:
- final_voiceover.wav (60.00s, 44.1kHz mono PCM, dual-character)
- final_music.wav     (60.00s, 44.1kHz stereo PCM, 8-beat dynamic score)
- final_sfx.wav       (60.00s, 44.1kHz stereo PCM, synchronized spot foley)
- final_mix.wav       (60.00s, 44.1kHz stereo PCM, sidechain ducked & mastered)
- final_subtitles.srt (Synchronized Devanagari Hindi subtitles)
"""

import os
import sys
import asyncio
import wave
import struct
import math
import numpy as np
import edge_tts
import imageio_ffmpeg

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.3"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

SR = 44100
TOTAL_DURATION = 60.00
TOTAL_SAMPLES = int(SR * TOTAL_DURATION)  # 2,646,000 samples

# =============================================================================
# 1. DIALOGUE DEFINITION & VOICEOVER SYNTHESIS (EDGE-TTS WITH SSML)
# =============================================================================
# Dual Voice Personas:
# Kabir: hi-IN-MadhurNeural (agitated, rapid, panic tempo, expressive)
# Meera: hi-IN-SwaraNeural  (grounded, calm, deadpan, sarcastic)

DIALOGUE_CUES = [
    {
        "id": 1,
        "scene": 1,
        "character": "Kabir",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 1.00,
        "rate": "+25%",
        "pitch": "+15Hz",
        "text": "अरे यार! सुबह के तीन बज रहे हैं और ये सर्वर फिर क्रैश हो गया?!"
    },
    {
        "id": 2,
        "scene": 2,
        "character": "Meera",
        "voice": "hi-IN-SwaraNeural",
        "start_time": 7.80,
        "rate": "+18%",
        "pitch": "-5Hz",
        "text": "कबीर, सांस ले। कोई हैकर नहीं है। कॉफ़ी पी और शांत हो।"
    },
    {
        "id": 3,
        "scene": 3,
        "character": "Kabir",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 15.30,
        "rate": "+25%",
        "pitch": "+18Hz",
        "text": "नहीं मीरा! ये पक्का डीडीओएस अटैक है! मैं डेटाबेस फ़ॉर्मेट कर रहा हूँ!"
    },
    {
        "id": 4,
        "scene": 4,
        "character": "Meera",
        "voice": "hi-IN-SwaraNeural",
        "start_time": 22.70,
        "rate": "+22%",
        "pitch": "+5Hz",
        "text": "हाथ हटा वहां से! रुक, ये क्या है? F5 और ESC की कंटीन्यूअस प्रेस?"
    },
    {
        "id": 5,
        "scene": 5,
        "character": "Kabir",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 30.50,
        "rate": "+20%",
        "pitch": "+10Hz",
        "text": "क्या मतलब?! मैंने तो कीबोर्ड छुआ भी नहीं!"
    },
    {
        "id": 6,
        "scene": 6,
        "character": "Meera",
        "voice": "hi-IN-SwaraNeural",
        "start_time": 39.50,
        "rate": "+8%",
        "pitch": "-2Hz",
        "text": "तूने नहीं छुआ, लेकिन इस पर कुछ भारी रखा ज़रूर है!"
    },
    {
        "id": 7,
        "scene": 7,
        "character": "Kabir",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 45.40,
        "rate": "+15%",
        "pitch": "+12Hz",
        "text": "ये... ये भुजिया थी?! पूरा दिन भुजिया की वजह से बर्बाद हुआ?!"
    },
    {
        "id": 8,
        "scene": 8,
        "character": "Meera",
        "voice": "hi-IN-SwaraNeural",
        "start_time": 52.70,
        "rate": "+25%",
        "pitch": "+5Hz",
        "text": "हाँ! तो हमारे सबसे बड़े इंटरनेशनल हैकर का नाम था... हल्दीराम की स्पेशल भुजिया!"
    }
]

async def synthesize_cue(cue):
    mp3_path = os.path.join(AUDIO_DIR, f"cue_{cue['id']}.mp3")
    wav_path = os.path.join(AUDIO_DIR, f"cue_{cue['id']}.wav")
    
    # Generate MP3 using Edge-TTS with clean text, custom rate and pitch
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(
                text=cue["text"],
                voice=cue["voice"],
                rate=cue["rate"],
                pitch=cue["pitch"]
            )
            await communicate.save(mp3_path)
            break
        except Exception as e:
            print(f"Retry cue {cue['id']} attempt {attempt+1}: {e}")
            await asyncio.sleep(1.0)
            
    # Decode to 44.1kHz mono WAV
    import subprocess
    cmd = [
        FFMPEG_BIN, "-y", "-i", mp3_path,
        "-ar", str(SR), "-ac", "1",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Read samples
    with wave.open(wav_path, "rb") as wf:
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        
    duration = len(samples) / SR
    print(f"Cue {cue['id']} ({cue['character']}): {duration:.2f}s (Start: {cue['start_time']}s, End: {cue['start_time'] + duration:.2f}s)")
    return samples, duration

async def build_voiceover_track():
    print("\n--- SYNTHESIZING DUAL-VOICE DIALOGUE ---")
    master_vo = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    cue_actuals = []
    
    for cue in DIALOGUE_CUES:
        samples, duration = await synthesize_cue(cue)
        start_idx = int(cue["start_time"] * SR)
        end_idx = start_idx + len(samples)
        
        # Check boundary
        if end_idx > TOTAL_SAMPLES:
            samples = samples[:TOTAL_SAMPLES - start_idx]
            end_idx = TOTAL_SAMPLES
            
        master_vo[start_idx:end_idx] += samples
        cue_actuals.append({
            "id": cue["id"],
            "character": cue["character"],
            "text": cue["text"],
            "start": cue["start_time"],
            "end": cue["start_time"] + duration
        })
        
    # Normalize VO track to -2.0 dBFS Peak
    max_val = np.max(np.abs(master_vo))
    if max_val > 0:
        master_vo = master_vo * (0.8 / max_val)
        
    # Write final_voiceover.wav
    vo_wav_path = os.path.join(BASE_DIR, "final_voiceover.wav")
    int_samples = (master_vo * 32767.0).astype(np.int16)
    with wave.open(vo_wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_samples.tobytes())
    print(f"Saved: {vo_wav_path} ({TOTAL_DURATION:.2f}s, mono)")
    
    # Write final_subtitles.srt
    srt_path = os.path.join(BASE_DIR, "final_subtitles.srt")
    def to_srt_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        
    with open(srt_path, "w", encoding="utf-8") as sf:
        for idx, item in enumerate(cue_actuals, start=1):
            sf.write(f"{idx}\n")
            sf.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            sf.write(f"{item['character']}: {item['text']}\n\n")
    print(f"Saved: {srt_path}")
    
    return master_vo, cue_actuals

# =============================================================================
# 2. MUSIC SYNTHESIS (8-BEAT DYNAMIC ELECTRONIC / CYBER-FUNK SOUNDTRACK)
# =============================================================================
def generate_music_track():
    print("\n--- GENERATING 60-SECOND DYNAMIC MUSIC TRACK ---")
    t = np.linspace(0, TOTAL_DURATION, TOTAL_SAMPLES, endpoint=False)
    
    left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    
    # Tempo: 120 BPM -> 1 beat = 0.5s, 1 bar = 2.0s
    beat_dur = 0.5
    
    # 8 Beat Structure (Matching the 8 Story Scenes):
    # Beat 1 (0.0 - 7.5s): Urgent cyber alarm pulse + frantic minor arpeggio (C minor / D# / G / Bb)
    # Beat 2 (7.5 - 15.0s): Smooth lofi jazz-funk groove (Fm9 -> Bb13 -> Ebmaj7) as Meera brings coffee
    # Beat 3 (15.0 - 22.5s): Escalating tension riser, heavy bass pulse, alarm dissonance as Kabir panics
    # Beat 4 (22.5 - 30.0s): Analytical groove, crisp Rhodes chords, muted detective bass
    # Beat 5 (30.0 - 37.5s): Mystery build, comedic pizzicato synth, ticking percussion
    # Beat 6 (37.5 - 45.0s): Sudden drop at 37.8s -> Triumphant bright major chords (F major -> G -> C maj9)
    # Beat 7 (45.0 - 52.5s): Playful funk groove, walking slap bass, syncopated rhythm
    # Beat 8 (52.5 - 60.0s): Full triumphant celebratory outro fanfare with crisp cymbal decay
    
    # Synthesize Drum Groove (Kick on 1 & 3, Snare on 2 & 4, 16th Hi-Hats)
    for i in range(int(TOTAL_DURATION / beat_dur)):
        bt_start = i * beat_dur
        bt_end = bt_start + beat_dur
        s_idx = int(bt_start * SR)
        e_idx = int(bt_end * SR)
        
        # Don't play heavy drums during the discovery pause (36.0s - 37.8s)
        if 36.0 <= bt_start < 37.8:
            continue
            
        dur_samples = e_idx - s_idx
        local_t = np.linspace(0, beat_dur, dur_samples, endpoint=False)
        
        # Kick on beats 0 and 2 of each 4-beat bar
        if (i % 4 == 0) or (i % 4 == 2):
            freq = 140.0 * np.exp(-local_t * 22.0) + 45.0
            phase = 2.0 * np.pi * np.cumsum(freq) / SR
            kick = np.sin(phase) * np.exp(-local_t * 12.0) * 0.45
            left[s_idx:e_idx] += kick
            right[s_idx:e_idx] += kick
            
        # Snare on beats 1 and 3 of each bar
        if (i % 4 == 1) or (i % 4 == 3):
            noise = np.random.uniform(-1, 1, dur_samples) * np.exp(-local_t * 18.0) * 0.22
            tone = np.sin(2 * np.pi * 180.0 * local_t) * np.exp(-local_t * 22.0) * 0.25
            snare = noise + tone
            left[s_idx:e_idx] += snare * 0.9
            right[s_idx:e_idx] += snare * 1.0
            
        # 16th Hi-Hats (4 per beat)
        for h in range(4):
            h_start = s_idx + int(h * (beat_dur / 4.0) * SR)
            h_len = int(0.04 * SR)
            if h_start + h_len <= TOTAL_SAMPLES:
                hh = np.random.uniform(-1, 1, h_len) * np.exp(-np.linspace(0, 1, h_len) * 20.0) * 0.08
                pan = 0.3 if h % 2 == 0 else -0.3
                left[h_start:h_start+h_len] += hh * (1.0 - pan)
                right[h_start:h_start+h_len] += hh * (1.0 + pan)

    # Harmonic Layers Across the 8 Sections
    chord_map = [
        (0.0, 7.5, 130.81, "minor_panic"),    # C minor
        (7.5, 15.0, 116.54, "funk_smooth"),   # Bb9 / F minor
        (15.0, 22.5, 123.47, "tension_riser"),# B dim / C minor
        (22.5, 30.0, 146.83, "tech_groove"),  # D dorian
        (30.0, 37.5, 130.81, "mystery_pulse"),# C suspended
        (37.5, 45.0, 174.61, "victory_major"),# F major / C
        (45.0, 52.5, 146.83, "playful_funk"), # D major 7
        (52.5, 60.0, 130.81, "outro_triumph") # C major epic
    ]
    
    for start_s, end_s, root_f, style in chord_map:
        s_idx = int(start_s * SR)
        e_idx = int(end_s * SR)
        seg_t = t[s_idx:e_idx]
        seg_len = len(seg_t)
        
        # Bassline synthesis
        if style in ["minor_panic", "tension_riser"]:
            bass_env = np.abs(np.sin(2 * np.pi * 4.0 * seg_t)) ** 2
            bass = np.sin(2 * np.pi * root_f * 0.5 * seg_t) + 0.4 * np.sin(2 * np.pi * root_f * seg_t)
            bass *= bass_env * 0.35
        elif style in ["funk_smooth", "tech_groove", "playful_funk"]:
            bass_f = root_f * 0.5 * (1.0 + 0.25 * np.sin(2 * np.pi * 0.5 * seg_t))
            bass = (np.sin(2 * np.pi * bass_f * seg_t) + 0.3 * np.sin(4 * np.pi * bass_f * seg_t)) * 0.30
        elif style == "mystery_pulse":
            bass = np.sin(2 * np.pi * root_f * 0.5 * seg_t) * (np.sin(2 * np.pi * 2.0 * seg_t) > 0.4) * 0.28
        else: # victory_major, outro_triumph
            bass = np.sin(2 * np.pi * root_f * 0.5 * seg_t) + 0.5 * np.sin(2 * np.pi * root_f * seg_t)
            bass *= 0.32
            
        # Warm Rhodes/Synthesizer Chord Pads
        chord_3rd = root_f * (1.20 if "minor" in style or "panic" in style else 1.25)
        chord_5th = root_f * 1.50
        chord_7th = root_f * (1.78 if "funk" in style or "triumph" in style else 1.88)
        
        pad = (np.sin(2 * np.pi * root_f * seg_t) * 0.3 +
               np.sin(2 * np.pi * chord_3rd * seg_t) * 0.25 +
               np.sin(2 * np.pi * chord_5th * seg_t) * 0.25 +
               np.sin(2 * np.pi * chord_7th * seg_t) * 0.2)
        
        # Chorus & stereo spread
        l_layer = (bass + pad * 0.9) * 0.40
        r_layer = (bass + pad * 1.1) * 0.40
        
        fade_samples = int(0.15 * SR)
        env = np.ones(seg_len, dtype=np.float32)
        if seg_len > 2 * fade_samples:
            env[:fade_samples] = np.linspace(0, 1, fade_samples)
            env[-fade_samples:] = np.linspace(1, 0, fade_samples)
            
        left[s_idx:e_idx] += l_layer * env
        right[s_idx:e_idx] += r_layer * env
        
    # Global Fade-In (0.5s) and Fade-Out (1.2s at end)
    fade_in_len = int(0.5 * SR)
    fade_out_len = int(1.5 * SR)
    left[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    right[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    left[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    right[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    
    # Normalize Music track to -4.0 dBFS Peak
    max_m = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if max_m > 0:
        gain = 0.63 / max_m
        left *= gain
        right *= gain
        
    # Save final_music.wav (Stereo)
    music_wav_path = os.path.join(BASE_DIR, "final_music.wav")
    stereo_music = np.vstack((left, right)).T
    int_music = (stereo_music * 32767.0).astype(np.int16)
    with wave.open(music_wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_music.tobytes())
    print(f"Saved: {music_wav_path} ({TOTAL_DURATION:.2f}s, stereo)")
    
    return left, right

# =============================================================================
# 3. SOUND EFFECTS SYNTHESIS (SYNCHRONIZED FOLEY SUITE)
# =============================================================================
def generate_sfx_track():
    print("\n--- GENERATING 60-SECOND SYNCHRONIZED SFX TRACK ---")
    left_sfx = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    right_sfx = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    t = np.linspace(0, TOTAL_DURATION, TOTAL_SAMPLES, endpoint=False)
    
    # 1. 3:00 AM Ambient Server Drone & Fan Hum (0.0s to 60.0s)
    fan_drone = (np.sin(2 * np.pi * 60.0 * t) * 0.08 +
                 np.sin(2 * np.pi * 120.0 * t) * 0.04 +
                 np.random.normal(0, 0.015, TOTAL_SAMPLES))
    left_sfx += fan_drone * 0.6
    right_sfx += fan_drone * 0.6
    
    # 2. Red Alert Klaxon Pulses in Scene 1 (0.8s, 2.8s, 4.8s) & Scene 3 (15.5s, 17.8s)
    alarm_times = [0.8, 2.8, 4.8, 15.5, 17.8]
    for at in alarm_times:
        s_idx = int(at * SR)
        dur = int(0.6 * SR)
        lt = np.linspace(0, 0.6, dur, endpoint=False)
        klaxon = (np.sin(2 * np.pi * (880.0 + 120.0 * np.sin(2 * np.pi * 6.0 * lt)) * lt) *
                  np.exp(-lt * 2.5) * 0.25)
        left_sfx[s_idx:s_idx+dur] += klaxon * 0.7
        right_sfx[s_idx:s_idx+dur] += klaxon * 0.9
        
    # 3. Frantic Mechanical Keyboard Typing Clatter (Scene 1: 0.1s - 2.0s; Scene 3: 15.2s - 17.2s)
    def add_typing(start_time, end_time):
        current = start_time
        while current < end_time:
            s_idx = int(current * SR)
            k_len = int(0.035 * SR)
            if s_idx + k_len < TOTAL_SAMPLES:
                kt = np.linspace(0, 0.035, k_len, endpoint=False)
                click = (np.sin(2 * np.pi * 2400.0 * kt) * np.exp(-kt * 180.0) * 0.28 +
                         np.random.uniform(-1, 1, k_len) * np.exp(-kt * 140.0) * 0.15)
                pan = np.random.uniform(-0.4, 0.4)
                left_sfx[s_idx:s_idx+k_len] += click * (1.0 - pan)
                right_sfx[s_idx:s_idx+k_len] += click * (1.0 + pan)
            current += np.random.uniform(0.04, 0.12)
            
    add_typing(0.1, 2.0)
    add_typing(15.2, 17.2)
    
    # 4. Ceramic Coffee Mug Clink & Desk Slide (Scene 2: 7.6s)
    mug_idx = int(7.6 * SR)
    mug_len = int(0.4 * SR)
    mt = np.linspace(0, 0.4, mug_len, endpoint=False)
    mug_clink = (np.sin(2 * np.pi * 3200.0 * mt) * np.exp(-mt * 45.0) * 0.30 +
                 np.sin(2 * np.pi * 1800.0 * mt) * np.exp(-mt * 30.0) * 0.20)
    left_sfx[mug_idx:mug_idx+mug_len] += mug_clink * 0.5
    right_sfx[mug_idx:mug_idx+mug_len] += mug_clink * 0.9
    
    # 5. Heavy Bhujia Snack Packet Crinkle & Thermos Clatter (Scene 5: 32.0s - 34.5s)
    bhujia_idx = int(32.5 * SR)
    bhujia_len = int(1.2 * SR)
    bt = np.linspace(0, 1.2, bhujia_len, endpoint=False)
    crinkle = (np.random.normal(0, 0.25, bhujia_len) *
               (np.sin(2 * np.pi * 8.0 * bt) > 0.2) *
               np.exp(-bt * 1.5) * 0.25)
    thermos_clatter = np.sin(2 * np.pi * 650.0 * bt) * np.exp(-bt * 12.0) * 0.35
    left_sfx[bhujia_idx:bhujia_idx+bhujia_len] += (crinkle + thermos_clatter * 0.4)
    right_sfx[bhujia_idx:bhujia_idx+bhujia_len] += (crinkle + thermos_clatter * 0.6)
    
    # 6. CRUCIAL STORY BEAT: The Lift & Mechanical Key Switch Release CLACK (Scene 6: 37.80s)
    clack_idx = int(37.80 * SR)
    clack_len = int(0.15 * SR)
    ct = np.linspace(0, 0.15, clack_len, endpoint=False)
    pop = (np.sin(2 * np.pi * 1450.0 * ct) * np.exp(-ct * 80.0) * 0.55 +
           np.sin(2 * np.pi * 3800.0 * ct) * np.exp(-ct * 140.0) * 0.40 +
           np.random.uniform(-1, 1, clack_len) * np.exp(-ct * 120.0) * 0.25)
    left_sfx[clack_idx:clack_idx+clack_len] += pop
    right_sfx[clack_idx:clack_idx+clack_len] += pop
    
    # 7. HIGH-TECH SERVER COMPILATION TRIUMPH CHIME (Scene 6: 38.20s - 41.5s)
    chime_idx = int(38.20 * SR)
    chime_len = int(2.8 * SR)
    cht = np.linspace(0, 2.8, chime_len, endpoint=False)
    chime_tones = [
        (0.00, 1046.5),
        (0.12, 1318.5),
        (0.24, 1567.98),
        (0.36, 2093.00)
    ]
    chime_wave = np.zeros(chime_len, dtype=np.float32)
    for delay, cf in chime_tones:
        d_idx = int(delay * SR)
        remain = chime_len - d_idx
        lt = np.linspace(0, remain / SR, remain, endpoint=False)
        tone = (np.sin(2 * np.pi * cf * lt) + 0.3 * np.sin(4 * np.pi * cf * lt)) * np.exp(-lt * 2.8) * 0.32
        chime_wave[d_idx:] += tone
    left_sfx[chime_idx:chime_idx+chime_len] += chime_wave * 0.8
    right_sfx[chime_idx:chime_idx+chime_len] += chime_wave * 1.0
    
    # 8. Outro Celebration Pop / App Deployed Ping (Scene 8: 58.5s)
    pop_idx = int(58.5 * SR)
    pop_len = int(0.5 * SR)
    pt = np.linspace(0, 0.5, pop_len, endpoint=False)
    deploy_ping = np.sin(2 * np.pi * 1760.0 * pt) * np.exp(-pt * 6.0) * 0.35
    left_sfx[pop_idx:pop_idx+pop_len] += deploy_ping
    right_sfx[pop_idx:pop_idx+pop_len] += deploy_ping
    
    # Normalize SFX track to -3.0 dBFS Peak
    max_s = max(np.max(np.abs(left_sfx)), np.max(np.abs(right_sfx)))
    if max_s > 0:
        gain = 0.70 / max_s
        left_sfx *= gain
        right_sfx *= gain
        
    # Save final_sfx.wav (Stereo)
    sfx_wav_path = os.path.join(BASE_DIR, "final_sfx.wav")
    stereo_sfx = np.vstack((left_sfx, right_sfx)).T
    int_sfx = (stereo_sfx * 32767.0).astype(np.int16)
    with wave.open(sfx_wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_sfx.tobytes())
    print(f"Saved: {sfx_wav_path} ({TOTAL_DURATION:.2f}s, stereo)")
    
    return left_sfx, right_sfx

# =============================================================================
# 4. MASTER MIXDOWN WITH DYNAMIC SIDECHAIN DUCKING & LIMITER
# =============================================================================
def build_master_mix(vo_mono, music_l, music_r, sfx_l, sfx_r):
    print("\n--- MASTERING FINAL MIX WITH -14dB SIDECHAIN DUCKING ---")
    
    vo_abs = np.abs(vo_mono)
    attack_samples = int(0.08 * SR)
    release_samples = int(0.35 * SR)
    
    duck_gain = np.ones(TOTAL_SAMPLES, dtype=np.float32)
    current_duck = 1.0
    duck_target_level = 0.20  # -14 dB attenuation during speech
    
    for i in range(TOTAL_SAMPLES):
        if vo_abs[i] > 0.03:
            current_duck += (duck_target_level - current_duck) / attack_samples
        else:
            current_duck += (1.0 - current_duck) / release_samples
        duck_gain[i] = current_duck
        
    # Apply ducking to Music track
    ducked_music_l = music_l * duck_gain
    ducked_music_r = music_r * duck_gain
    
    # Sum components: VO (centered) + Ducked Music + SFX
    master_l = vo_mono + ducked_music_l + sfx_l * 0.75
    master_r = vo_mono + ducked_music_r + sfx_r * 0.75
    
    # Master Limiter with Soft Knee (-2.5 dBFS True Peak ceiling = 0.75)
    PEAK_CEILING = 0.75
    max_peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    print(f"Pre-master peak: {max_peak:.4f} ({20*math.log10(max_peak + 1e-9):.2f} dBFS)")
    
    if max_peak > PEAK_CEILING:
        scale = PEAK_CEILING / max_peak
        master_l *= scale
        master_r *= scale
        
    master_l = np.tanh(master_l / PEAK_CEILING) * PEAK_CEILING
    master_r = np.tanh(master_r / PEAK_CEILING) * PEAK_CEILING
    
    final_peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    final_rms = math.sqrt(0.5 * (np.mean(master_l**2) + np.mean(master_r**2)))
    print(f"Master True Peak: {final_peak:.4f} ({20*math.log10(final_peak):.2f} dBFS)")
    print(f"Master RMS: {final_rms:.4f} ({20*math.log10(final_rms):.2f} dBFS)")
    
    mix_wav_path = os.path.join(BASE_DIR, "final_mix.wav")
    stereo_mix = np.vstack((master_l, master_r)).T
    int_mix = (stereo_mix * 32767.0).astype(np.int16)
    with wave.open(mix_wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_mix.tobytes())
    print(f"Saved: {mix_wav_path} ({TOTAL_DURATION:.2f}s, stereo, mastered)")

# =============================================================================
# MAIN ENTRYPOINT
# =============================================================================
async def main():
    print("=================================================================")
    print("MASTER AI — PHASE 7.7.3: AUDIO PRODUCTION PIPELINE")
    print("Story: 'लास्ट बग' (The Last Bug) • Runtime: 60.00 Seconds")
    print("=================================================================")
    
    vo_mono, cue_actuals = await build_voiceover_track()
    music_l, music_r = generate_music_track()
    sfx_l, sfx_r = generate_sfx_track()
    build_master_mix(vo_mono, music_l, music_r, sfx_l, sfx_r)
    
    print("\nAudio pipeline finished successfully!")

if __name__ == "__main__":
    asyncio.run(main())
