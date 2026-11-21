"""
generate_editing_plan_774.py
============================
Generates the formalized Editing Decision Sheet for:
"कोड रेड: डिलीवरी" (Code Red: 10-Minute Delivery) - Phase 7.7.4
"""

import os
import sys
import json

ENGINE_DIR = r"F:\Master AI\09_CONTENT_STUDIO\engine"
sys.path.append(ENGINE_DIR)

from editing_director import EditingDirector

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4"

beats = [
    {
        "film_title": "कोड रेड: डिलीवरी (Code Red: 10-Minute Delivery)",
        "scene_id": "scene_01",
        "title": "BEAT 1: THE 10-MINUTE COUNTDOWN",
        "duration_sec": 7.5,
        "dramatic_intent": "URGENT_HOOK",
        "action": "Smartphone vibrating on scooter mount: 09:59... ORDER #402. Aryan snaps helmet visor down with determination.",
        "speaker": "Aryan",
        "dialogue": "दस मिनट... और पूरा शहर ट्रैफ़िक में डूबा है! पर ये ऑर्डर कैंसल नहीं होगा!",
        "music_theme": "Fast pulsing synth bass, ticking digital clock tempo",
        "foley": ["Smartphone vibration buzz", "Helmet visor snap", "Rain drizzle"]
    },
    {
        "scene_id": "scene_02",
        "title": "BEAT 2: THE CHAOTIC CLOUD KITCHEN",
        "duration_sec": 7.5,
        "dramatic_intent": "ACTION_PREP",
        "action": "Vikram Chef expertly tosses a fiery wok with flying embers, packaging hot insulated box and passing to Aryan.",
        "speaker": "Vikram Chef",
        "dialogue": "आर्यन, गरम है! संभल के ले जाना, किसी का ख़ास ऑर्डर है!",
        "music_theme": "Industrial percussive funk groove, metallic clatter rhythm",
        "foley": ["Flaming wok sizzle", "Metal ladle clank", "Paper box tape seal"]
    },
    {
        "scene_id": "scene_03",
        "title": "BEAT 3: RAIN & IGNITION",
        "duration_sec": 7.5,
        "dramatic_intent": "KINETIC_LAUNCH",
        "action": "Low-angle tracking shot of electric scooter wheels accelerating through street puddles with water spray and neon parallax.",
        "speaker": "Aryan",
        "dialogue": "चिंता मत करो शेफ़! घड़ी टिक रही है, और मैं उड़ रहा हूँ!",
        "music_theme": "Driving synthwave rhythm with electric guitar lead",
        "foley": ["Electric motor whine", "Puddle splash spray", "Road tire whoosh"]
    },
    {
        "scene_id": "scene_04",
        "title": "BEAT 4: THE TRAFFIC GRIDLOCK",
        "duration_sec": 7.5,
        "dramatic_intent": "FOCUSED_TENSION",
        "action": "POV shot through water-streaked visor. Focused eyes darting as scooter swerves between bumper-to-bumper red tail lights.",
        "speaker": "Aryan",
        "dialogue": "सिर्फ़ तीन मिनट बचे हैं... रास्ता निकालना ही पड़ेगा!",
        "music_theme": "Tension riser with rising filtered saw synth",
        "foley": ["Distant traffic horns", "Visor wiper squeak", "Motor rev"]
    },
    {
        "scene_id": "scene_05",
        "title": "BEAT 5: THE FINAL SECONDS",
        "duration_sec": 7.5,
        "dramatic_intent": "COUNTDOWN_RACE",
        "action": "Insert on handlebar timer ticking down: 00:30... 00:15... 00:05... Scooter takes a sharp leaning turn.",
        "speaker": "SFX_Pacing",
        "dialogue": "[SFX: Rapid heartbeat + ticking countdown beeps + tyre water screech]",
        "music_theme": "Intense cinematic riser crescendo, sub bass drops",
        "foley": ["Digital timer rapid beeping", "Tire water screech", "Heartbeat pulse"]
    },
    {
        "scene_id": "scene_06",
        "title": "BEAT 6: ARRIVAL AT ST. MARTHA'S",
        "duration_sec": 7.5,
        "dramatic_intent": "ARRIVAL_RELIEF",
        "action": "Scooter slides to a smooth stop at hospital emergency gate at 00:02s before cancel. Rain falling softly under warm lamppost.",
        "speaker": "Aryan",
        "dialogue": "पहुंच गया! ठीक दो सेकंड पहले... अस्पताल का गेट!",
        "music_theme": "Sudden drop in music, gentle warm Rhodes chords enter",
        "foley": ["Smooth regenerative brake whir", "Kickstand drop", "Rain on hood"]
    },
    {
        "scene_id": "scene_07",
        "title": "BEAT 7: THE BIRTHDAY SURPRISE",
        "duration_sec": 7.5,
        "dramatic_intent": "EMOTIONAL_REVEAL",
        "action": "Dr. Ananya steps out in weary surgical scrubs. Aryan hands over parcel. She opens box: fresh strawberry pastry with candle and note from Mom.",
        "speaker": "Dr. Ananya",
        "dialogue": "माँ... तुम्हें याद था? आज छत्तीस घंटे की ड्यूटी के बाद... ये सबसे खूबसूरत सरप्राइज़ है।",
        "music_theme": "Emotional acoustic piano & warm cello melody",
        "foley": ["Sliding hospital door", "Box opening rustle", "Tiny candle match strike"]
    },
    {
        "scene_id": "scene_08",
        "title": "BEAT 8: TRIUMPH & SMILE",
        "duration_sec": 7.5,
        "dramatic_intent": "TRIUMPH_OUTRO",
        "action": "Dr. Ananya smiles through happy tears. Aryan gives a warm salute, smiling under his helmet, and turns into the night rain as title card dissolves.",
        "speaker": "Aryan",
        "dialogue": "हैप्पी बर्थडे डॉक्टर साहिबा! आपकी मुस्कान ही हमारी मंज़िल थी।",
        "music_theme": "Inspiring orchestral swell with gentle rain outro",
        "foley": ["Ananya soft blowing of candle", "Visor click", "Electric scooter fade"]
    }
]

plan = EditingDirector.plan_film(beats)

# Save JSON
json_path = os.path.join(OUTPUT_DIR, "editing_decision_sheet.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)
print(f"Saved: {json_path}")

# Save Markdown
md_path = os.path.join(OUTPUT_DIR, "editing_decision_sheet.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# MASTER AI — SCENE-WISE EDITING DECISION SHEET\n")
    f.write(f"## Film: {plan['film_title']}\n")
    f.write(f"**Target Runtime**: {plan['target_runtime_sec']:.2f} Seconds | **FPS**: {plan['target_fps']} CFR | **Total Scenes**: {plan['scene_count']}\n\n")
    f.write("---\n\n")
    
    for s in plan["scenes"]:
        f.write(f"### Scene {s['beat_number']:02d}: {s['title']}\n")
        f.write(f"- **Timing**: {s['timing']['start_sec']}s – {s['timing']['end_sec']}s ({s['timing']['duration_sec']}s / {s['timing']['frames_24fps']} frames)\n")
        f.write(f"- **Dramatic Intent**: `{s['dramatic_intent']}`\n")
        f.write(f"- **Shot Type**: `{s['cinematography']['shot_type']}`\n")
        f.write(f"- **Camera Movement**: `{s['cinematography']['camera_movement']}`\n")
        f.write(f"- **Cut / Transition**: `{s['cinematography']['cut_transition']}`\n")
        f.write(f"- **Character Action**: {s['motion_and_vfx']['character_action']}\n")
        f.write(f"- **Visual Effects (VFX)**: {', '.join(s['motion_and_vfx']['active_vfx'])}\n")
        f.write(f"- **Speaker**: `{s['audio_design']['speaker']}`\n")
        f.write(f"- **Dialogue**: *\"{s['audio_design']['dialogue_text']}\"*\n")
        f.write(f"- **Music Theme**: {s['audio_design']['music_movement']}\n")
        f.write(f"- **Foley SFX**: {', '.join(s['audio_design']['foley_cues'])}\n\n")

print(f"Saved: {md_path}")
