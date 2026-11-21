"""
build_audio_pipeline_774.py
===========================
Generates the complete 60.00-second professional audio suite for:
"कोड रेड: डिलीवरी" (Code Red: 10-Minute Delivery) - Phase 7.7.4

Deliverables:
- final_voiceover.wav (60.00s, 44.1kHz mono PCM, multi-character)
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

BASE_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

SR = 44100
TOTAL_DURATION = 60.00
TOTAL_SAMPLES = int(SR * TOTAL_DURATION)  # 2,646,000 samples

# Dialogue Cues
DIALOGUE_CUES = [
    {
        "id": 1,
        "scene": 1,
        "character": "आर्यन (Aryan)",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 0.50,
        "rate": "+26%",
        "pitch": "+12Hz",
        "text": "दस मिनट... और पूरा शहर ट्रैफ़िक में डूबा है! पर ये ऑर्डर कैंसल नहीं होगा!"
    },
    {
        "id": 2,
        "scene": 2,
        "character": "विक्रम शेफ़ (Vikram Chef)",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 8.00,
        "rate": "+15%",
        "pitch": "-8Hz",
        "text": "आर्यन, गरम है! संभल के ले जाना, किसी का ख़ास ऑर्डर है!"
    },
    {
        "id": 3,
        "scene": 3,
        "character": "आर्यन (Aryan)",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 15.50,
        "rate": "+25%",
        "pitch": "+15Hz",
        "text": "चिंता मत करो शेफ़! घड़ी टिक रही है, और मैं उड़ रहा हूँ!"
    },
    {
        "id": 4,
        "scene": 4,
        "character": "आर्यन (Aryan)",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 23.00,
        "rate": "+20%",
        "pitch": "+10Hz",
        "text": "सिर्फ़ तीन मिनट बचे हैं... रास्ता निकालना ही पड़ेगा!"
    },
    # Scene 5 (30.0s - 37.5s): Pure tension music & foley race beat (heartbeat, beeps, screech)
    {
        "id": 6,
        "scene": 6,
        "character": "आर्यन (Aryan)",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 38.50,
        "rate": "+18%",
        "pitch": "+5Hz",
        "text": "पहुंच गया! ठीक दो सेकंड पहले... अस्पताल का गेट!"
    },
    {
        "id": 7,
        "scene": 7,
        "character": "डॉ. अनन्या (Dr. Ananya)",
        "voice": "hi-IN-SwaraNeural",
        "start_time": 45.80,
        "rate": "+22%",
        "pitch": "-2Hz",
        "text": "माँ, तुम्हें याद था?! ड्यूटी के बाद... ये सबसे प्यारा सरप्राइज़ है!"
    },
    {
        "id": 8,
        "scene": 8,
        "character": "आर्यन (Aryan)",
        "voice": "hi-IN-MadhurNeural",
        "start_time": 53.00,
        "rate": "+22%",
        "pitch": "+8Hz",
        "text": "हैप्पी बर्थडे डॉक्टर साहिबा! आपकी मुस्कान ही जीत है!"
    }
]

async def synthesize_cue(cue):
    mp3_path = os.path.join(AUDIO_DIR, f"cue_{cue['id']}.mp3")
    wav_path = os.path.join(AUDIO_DIR, f"cue_{cue['id']}.wav")
    
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
            
    import subprocess
    cmd = [
        FFMPEG_BIN, "-y", "-i", mp3_path,
        "-ar", str(SR), "-ac", "1",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    with wave.open(wav_path, "rb") as wf:
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        
    duration = len(samples) / SR
    print(f"Cue {cue['id']} ({cue['character']}): {duration:.2f}s (Start: {cue['start_time']}s, End: {cue['start_time'] + duration:.2f}s)")
    return samples, duration

async def build_voiceover_track():
    print("\n--- 1. SYNTHESIZING MULTI-CHARACTER HINDI VOICEOVER ---")
    master_vo = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    cue_actuals = []
    
    for cue in DIALOGUE_CUES:
        samples, duration = await synthesize_cue(cue)
        start_idx = int(cue["start_time"] * SR)
        end_idx = start_idx + len(samples)
        
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
        
    max_val = np.max(np.abs(master_vo))
    if max_val > 0:
        master_vo = master_vo * (0.8 / max_val)
        
    vo_wav_path = os.path.join(BASE_DIR, "final_voiceover.wav")
    int_samples = (master_vo * 32767.0).astype(np.int16)
    with wave.open(vo_wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_samples.tobytes())
    print(f"Saved: {vo_wav_path} ({TOTAL_DURATION:.2f}s, mono)")
    
    # Write subtitles
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
# 2. MUSIC SYNTHESIS (8-BEAT DYNAMIC CINEMATIC SOUNDTRACK)
# =============================================================================
def generate_music_track():
    print("\n--- 2. GENERATING 60-SECOND DYNAMIC SOUNDTRACK ---")
    t = np.linspace(0, TOTAL_DURATION, TOTAL_SAMPLES, endpoint=False)
    left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    
    beat_dur = 0.5  # 120 BPM
    
    # Drum Groove
    for i in range(int(TOTAL_DURATION / beat_dur)):
        bt_start = i * beat_dur
        bt_end = bt_start + beat_dur
        s_idx = int(bt_start * SR)
        e_idx = int(bt_end * SR)
        
        # Drop drums during emotional reveal (44.5s to 52.0s)
        if 44.5 <= bt_start < 52.0:
            continue
            
        dur_samples = e_idx - s_idx
        local_t = np.linspace(0, beat_dur, dur_samples, endpoint=False)
        
        # Kick drum on 0 and 2
        if (i % 4 == 0) or (i % 4 == 2):
            freq = 150.0 * np.exp(-local_t * 24.0) + 40.0
            phase = 2.0 * np.pi * np.cumsum(freq) / SR
            kick = np.sin(phase) * np.exp(-local_t * 12.0) * 0.45
            left[s_idx:e_idx] += kick
            right[s_idx:e_idx] += kick
            
        # Snare drum on 1 and 3
        if (i % 4 == 1) or (i % 4 == 3):
            noise = np.random.uniform(-1, 1, dur_samples) * np.exp(-local_t * 18.0) * 0.22
            tone = np.sin(2 * np.pi * 190.0 * local_t) * np.exp(-local_t * 22.0) * 0.25
            snare = noise + tone
            left[s_idx:e_idx] += snare * 0.95
            right[s_idx:e_idx] += snare * 0.95
            
        # 16th Hi-Hats
        for h in range(4):
            h_start = s_idx + int(h * (beat_dur / 4.0) * SR)
            h_len = int(0.04 * SR)
            if h_start + h_len <= TOTAL_SAMPLES:
                hh = np.random.uniform(-1, 1, h_len) * np.exp(-np.linspace(0, 1, h_len) * 22.0) * 0.08
                pan = 0.25 if h % 2 == 0 else -0.25
                left[h_start:h_start+h_len] += hh * (1.0 - pan)
                right[h_start:h_start+h_len] += hh * (1.0 + pan)

    # 8 Harmonic Movements matching Screenplay Beats
    chord_map = [
        (0.0, 7.5, 110.00, "countdown_pulse"), # A minor tension
        (7.5, 15.0, 116.54, "kitchen_funk"),    # Bb dominant 7
        (15.0, 22.5, 130.81, "kinetic_drive"),  # C minor synthwave
        (22.5, 30.0, 123.47, "traffic_riser"),  # B diminished tension
        (30.0, 37.5, 110.00, "final_seconds"),  # A minor rapid heartbeat
        (37.5, 45.0, 146.83, "hospital_calm"),  # D major 7 warm Rhodes
        (45.0, 52.5, 174.61, "emotional_piano"),# F major 9 acoustic warmth
        (52.5, 60.0, 130.81, "outro_triumph")   # C major orchestral swell
    ]
    
    for start_s, end_s, root_f, style in chord_map:
        s_idx = int(start_s * SR)
        e_idx = int(end_s * SR)
        seg_t = t[s_idx:e_idx]
        seg_len = len(seg_t)
        
        # Bassline
        if style in ["countdown_pulse", "traffic_riser", "final_seconds"]:
            bass_env = np.abs(np.sin(2 * np.pi * 4.0 * seg_t)) ** 2
            bass = np.sin(2 * np.pi * root_f * 0.5 * seg_t) * bass_env * 0.35
        elif style in ["kitchen_funk", "kinetic_drive"]:
            bass_f = root_f * 0.5 * (1.0 + 0.2 * np.sin(2 * np.pi * 0.5 * seg_t))
            bass = np.sin(2 * np.pi * bass_f * seg_t) * 0.30
        elif style == "emotional_piano":
            bass = np.sin(2 * np.pi * root_f * 0.5 * seg_t) * 0.22
        else: # hospital_calm, outro_triumph
            bass = (np.sin(2 * np.pi * root_f * 0.5 * seg_t) + 0.4 * np.sin(2 * np.pi * root_f * seg_t)) * 0.32
            
        chord_3rd = root_f * (1.20 if "minor" in style or "pulse" in style or "riser" in style else 1.25)
        chord_5th = root_f * 1.50
        chord_7th = root_f * 1.78
        
        pad = (np.sin(2 * np.pi * root_f * seg_t) * 0.30 +
               np.sin(2 * np.pi * chord_3rd * seg_t) * 0.25 +
               np.sin(2 * np.pi * chord_5th * seg_t) * 0.25 +
               np.sin(2 * np.pi * chord_7th * seg_t) * 0.20)
        
        l_layer = (bass + pad * 0.9) * 0.42
        r_layer = (bass + pad * 1.1) * 0.42
        
        fade_samples = int(0.15 * SR)
        env = np.ones(seg_len, dtype=np.float32)
        if seg_len > 2 * fade_samples:
            env[:fade_samples] = np.linspace(0, 1, fade_samples)
            env[-fade_samples:] = np.linspace(1, 0, fade_samples)
            
        left[s_idx:e_idx] += l_layer * env
        right[s_idx:e_idx] += r_layer * env
        
    fade_in_len = int(0.5 * SR)
    fade_out_len = int(1.5 * SR)
    left[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    right[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    left[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    right[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    
    max_m = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if max_m > 0:
        gain = 0.63 / max_m
        left *= gain
        right *= gain
        
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
# 3. SOUND EFFECTS SYNTHESIS (SPOT FOLEY SUITE)
# =============================================================================
def generate_sfx_track():
    print("\n--- 3. GENERATING 60-SECOND SYNCHRONIZED SFX TRACK ---")
    left_sfx = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    right_sfx = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    t = np.linspace(0, TOTAL_DURATION, TOTAL_SAMPLES, endpoint=False)
    
    # 1. Rain Ambience (0.0s to 60.0s)
    rain_noise = np.random.normal(0, 0.04, TOTAL_SAMPLES)
    rain_filter = np.convolve(rain_noise, np.ones(32)/32, mode='same')
    left_sfx += rain_filter * 0.4
    right_sfx += rain_filter * 0.4
    
    # 2. Smartphone Vibration & Beep in Scene 1
    for vt in [0.2, 0.8, 1.4]:
        s_idx = int(vt * SR)
        dur = int(0.25 * SR)
        lt = np.linspace(0, 0.25, dur, endpoint=False)
        buzz = np.sin(2 * np.pi * 180.0 * lt) * np.exp(-lt * 4.0) * 0.35
        beep = np.sin(2 * np.pi * 1200.0 * lt) * np.exp(-lt * 8.0) * 0.25
        left_sfx[s_idx:s_idx+dur] += (buzz + beep) * 0.8
        right_sfx[s_idx:s_idx+dur] += (buzz + beep) * 0.8
        
    # 3. Visor Snap Click in Scene 1 & 8
    for st in [6.2, 58.2]:
        s_idx = int(st * SR)
        dur = int(0.12 * SR)
        lt = np.linspace(0, 0.12, dur, endpoint=False)
        snap = (np.sin(2 * np.pi * 1800.0 * lt) * np.exp(-lt * 90.0) * 0.45 +
                np.random.uniform(-1, 1, dur) * np.exp(-lt * 120.0) * 0.25)
        left_sfx[s_idx:s_idx+dur] += snap
        right_sfx[s_idx:s_idx+dur] += snap
        
    # 4. Sizzling Wok Fire in Scene 2
    wok_idx = int(7.8 * SR)
    wok_dur = int(4.5 * SR)
    wt = np.linspace(0, 4.5, wok_dur, endpoint=False)
    sizzle = np.random.normal(0, 0.18, wok_dur) * (1.0 + 0.4 * np.sin(2 * np.pi * 3.0 * wt)) * 0.35
    ladle = np.sin(2 * np.pi * 2200.0 * wt) * (np.sin(2 * np.pi * 1.5 * wt) > 0.8) * 0.25
    left_sfx[wok_idx:wok_idx+wok_dur] += (sizzle + ladle) * 0.7
    right_sfx[wok_idx:wok_idx+wok_dur] += (sizzle + ladle) * 0.9
    
    # 5. Electric Scooter Whine & Puddle Splash in Scene 3
    scoot_idx = int(15.2 * SR)
    scoot_dur = int(6.5 * SR)
    sct = np.linspace(0, 6.5, scoot_dur, endpoint=False)
    motor = np.sin(2 * np.pi * (350.0 + 150.0 * (sct/6.5)) * sct) * 0.22
    splash = np.random.normal(0, 0.15, scoot_dur) * (1.0 + 0.3 * np.sin(2 * np.pi * 4.0 * sct)) * 0.25
    left_sfx[scoot_idx:scoot_idx+scoot_dur] += (motor + splash) * 0.7
    right_sfx[scoot_idx:scoot_idx+scoot_dur] += (motor + splash) * 0.8
    
    # 6. Countdown Beeps & Heartbeat in Scene 5
    hb_idx = int(30.0 * SR)
    for sec in range(7):
        t_sub = hb_idx + int(sec * SR)
        hb_dur = int(0.18 * SR)
        hbt = np.linspace(0, 0.18, hb_dur, endpoint=False)
        thump = np.sin(2 * np.pi * 55.0 * hbt) * np.exp(-hbt * 14.0) * 0.45
        left_sfx[t_sub:t_sub+hb_dur] += thump
        right_sfx[t_sub:t_sub+hb_dur] += thump
        beep_dur = int(0.08 * SR)
        bpt = np.linspace(0, 0.08, beep_dur, endpoint=False)
        alarm_beep = np.sin(2 * np.pi * 1760.0 * bpt) * 0.30
        left_sfx[t_sub:t_sub+beep_dur] += alarm_beep * 0.8
        right_sfx[t_sub:t_sub+beep_dur] += alarm_beep * 0.8
        
    # 7. Brake Whir in Scene 6
    brake_idx = int(37.2 * SR)
    brake_dur = int(1.2 * SR)
    bkt = np.linspace(0, 1.2, brake_dur, endpoint=False)
    brake_whir = np.sin(2 * np.pi * (600.0 * (1.0 - bkt/1.2)) * bkt) * np.exp(-bkt * 2.0) * 0.28
    left_sfx[brake_idx:brake_idx+brake_dur] += brake_whir
    right_sfx[brake_idx:brake_idx+brake_dur] += brake_whir
    
    # 8. Sliding Hospital Doors in Scene 7
    door_idx = int(45.0 * SR)
    door_dur = int(1.5 * SR)
    drt = np.linspace(0, 1.5, door_dur, endpoint=False)
    door_whir = (np.sin(2 * np.pi * 280.0 * drt) * np.exp(-drt * 1.5) * 0.18 +
                 np.random.normal(0, 0.05, door_dur) * np.exp(-drt * 1.2))
    left_sfx[door_idx:door_idx+door_dur] += door_whir
    right_sfx[door_idx:door_idx+door_dur] += door_whir
    
    max_s = max(np.max(np.abs(left_sfx)), np.max(np.abs(right_sfx)))
    if max_s > 0:
        gain = 0.70 / max_s
        left_sfx *= gain
        right_sfx *= gain
        
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
# 4. MASTER MIXDOWN WITH -14dB DUCKING & LIMITER
# =============================================================================
def build_master_mix(vo_mono, music_l, music_r, sfx_l, sfx_r):
    print("\n--- 4. MASTERING FINAL MIX WITH -14dB SIDECHAIN DUCKING ---")
    
    vo_abs = np.abs(vo_mono)
    attack_samples = int(0.08 * SR)
    release_samples = int(0.35 * SR)
    
    duck_gain = np.ones(TOTAL_SAMPLES, dtype=np.float32)
    current_duck = 1.0
    duck_target_level = 0.20
    
    for i in range(TOTAL_SAMPLES):
        if vo_abs[i] > 0.03:
            current_duck += (duck_target_level - current_duck) / attack_samples
        else:
            current_duck += (1.0 - current_duck) / release_samples
        duck_gain[i] = current_duck
        
    ducked_music_l = music_l * duck_gain
    ducked_music_r = music_r * duck_gain
    
    master_l = vo_mono + ducked_music_l + sfx_l * 0.75
    master_r = vo_mono + ducked_music_r + sfx_r * 0.75
    
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
    print(f"Master RMS:       {final_rms:.4f} ({20*math.log10(final_rms):.2f} dBFS)")
    
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
    print("MASTER AI — PHASE 7.7.4: AUDIO PRODUCTION PIPELINE")
    print("Story: 'कोड रेड: डिलीवरी' (Code Red: 10-Minute Delivery)")
    print("=================================================================")
    
    vo_mono, cue_actuals = await build_voiceover_track()
    music_l, music_r = generate_music_track()
    sfx_l, sfx_r = generate_sfx_track()
    build_master_mix(vo_mono, music_l, music_r, sfx_l, sfx_r)
    
    print("\nAudio pipeline finished successfully!")

if __name__ == "__main__":
    asyncio.run(main())
