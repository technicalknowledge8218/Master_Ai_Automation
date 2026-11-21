"""
generate_curriculum_specs.py
============================
Generates the 12 detailed curriculum specification documents for
Video Director Academy in F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8\curriculum\
"""

import os

CURRICULUM_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8\curriculum"
os.makedirs(CURRICULUM_DIR, exist_ok=True)

modules = [
    {
        "id": "module_01_storytelling.md",
        "title": "Module 01: Storytelling & Screenwriting",
        "discipline": "Narrative Architecture & Dialogue",
        "objectives": [
            "Master classic 3-act dramatic structure: Hook (Inciting Incident), Rising Obstacles (Midpoint), and Climax/Resolution.",
            "Eliminate predictable moralizing and formulaic 'lost letter / tragedy' tropes.",
            "Write authentic, contemporary conversational Hindi dialogue reflecting actual colloquial speech.",
            "Ensure every scene has a clear dramatic question that must be answered."
        ],
        "exercises": [
            "Write a 3-beat micro-story in Hindi: Character establishes a simple goal, meets an unexpected obstacle, and overcomes it with a clever twist.",
            "Transform an overly formal literary Hindi dialogue into crisp, modern colloquial urban speech."
        ],
        "examples": [
            "Hitchcock's Bomb Under the Table (Suspense vs Surprise)",
            "Studio Ghibli's 'Ma' (The intentional breathing pause between action beats)",
            "Contemporary Indian indie cinema dialogue cadence (natural pauses, overlapping thoughts, colloquial idioms)"
        ],
        "evaluation": [
            "Hook clarity: Does the opening line/action engage curiosity within 3 seconds?",
            "Subtext: Does the character have an unstated internal motive?",
            "Dialogue realism: Does it sound like people talking or a book being read aloud?"
        ],
        "weaknesses": [
            "Phase 7.4/7.7.2: Defaulted to repetitive sentimental tropes without subtext.",
            "Phase 7.7.1: Words were grammatically correct but spoken unnaturally without conversational contractions."
        ],
        "improvements": [
            "Created Genre-Specific Narrative Matrices in `goal_decomposer.py`.",
            "Integrated Hindi Conversational Phrasing Dictionary avoiding archaic idioms."
        ]
    },
    {
        "id": "module_02_film_direction.md",
        "title": "Module 02: Film Direction & Scene Blocking",
        "discipline": "Scene Directorial Staging & Visual Hierarchy",
        "objectives": [
            "Establish clear subject attention in every frame (Rule of Thirds, leading lines, high contrast).",
            "Maintain the 180-degree line (axis of action) across multi-shot character interactions.",
            "Direct emotional tone through deliberate camera height, Dutch tilts, and spatial staging.",
            "Enforce motivated character movement that reveals inner psychological state."
        ],
        "exercises": [
            "Block a two-character confrontation: Staging status shifts through physical height differences.",
            "Execute an emotional pivot: Transitioning a character from dominant power to vulnerability using camera elevation."
        ],
        "examples": [
            "Akira Kurosawa's triangular character blocking in *Seven Samurai*",
            "David Fincher's motivated camera alignment (the camera only moves when the character moves)"
        ],
        "evaluation": [
            "Visual clarity: Can a viewer immediately identify who owns the scene within 1 second?",
            "Axis continuity: Does crossing the line disorient the viewer?"
        ],
        "weaknesses": [
            "Phase 7.6: Characters stood rigidly side-by-side with no compositional depth or power dynamics.",
            "Phase 7.7.3: Camera hovered randomly without anchoring on dramatic focus."
        ],
        "improvements": [
            "Built `CreativeDecisionEngine` requiring an explicit `focal_subject` and `directorial_intent` vector for every shot."
        ]
    },
    {
        "id": "module_03_cinematography.md",
        "title": "Module 03: Cinematography & Camera Language",
        "discipline": "Optical Physics, Shot Scales & Multi-Plane Parallax",
        "objectives": [
            "Master shot scale taxonomy: Extreme Close-Up (ECU), Close-Up (CU), Medium Shot (MS), Wide (WS), Extreme Wide (EWS).",
            "Apply multi-plane parallax depth: background (0.2x), midground (0.7x), subject (1.0x), foreground (1.4x).",
            "Replace robotic linear camera zooms with cubic easing curves (`ease_in_out_cubic`, `ease_out_back`).",
            "Integrate realistic camera physics: inertia, damped harmonic shake, and optical depth of field."
        ],
        "exercises": [
            "5-second eased dolly zoom (Vertigo effect) combining optical scale expansion with background compression.",
            "Multi-plane parallax lateral tracking shot with 4 distinct spatial layers."
        ],
        "examples": [
            "Roger Deakins' naturalistic focal choices in *Blade Runner 2049*",
            "Hayao Miyazaki's lush multi-plane cel animation depth in *Spirited Away*"
        ],
        "evaluation": [
            "Parallax integrity: Do layers move at geometrically consistent optical speeds?",
            "Camera smoothness: Is camera acceleration derivative continuous (no jerk/snapping)?"
        ],
        "weaknesses": [
            "Phase 7.6: Single-layer flat pans looked like moving a photocopy.",
            "Phase 7.7.4: 24Hz camera shake aliased into severe scanline vibration."
        ],
        "improvements": [
            "Upgraded `Camera2D` in `motion_director.py` with 4-plane parallax and Nyquist-safe 6.0Hz damped harmonic vibration."
        ]
    },
    {
        "id": "module_04_editing.md",
        "title": "Module 04: Professional Video Editing & Montage",
        "discipline": "Editorial Grammar, Motivated Cuts & Rhythm",
        "objectives": [
            "Eradicate uniform crossfade dissolves; cut strictly with dramatic intent.",
            "Execute classic motivated cut types: Hard Cuts on audio transients, Match Cuts on visual geometry, Whip Pans for velocity, Reaction Cuts.",
            "Implement J-Cuts and L-Cuts (audio precedes or outlasts visual cuts by 0.3s–0.6s) to create seamless continuity.",
            "Control pacing through metric editing: cutting faster during action and lingering on emotional beats."
        ],
        "exercises": [
            "10-second metric cut sequence: Accelerating cuts from 2.5s down to 0.5s during a chase sequence.",
            "Match cut transition between two circular shapes (e.g., eye pupil to motorcycle wheel)."
        ],
        "examples": [
            "The Odessa Steps sequence in *Battleship Potemkin* (rhythmic montage)",
            "Edgar Wright's kinetic match-cutting and whip-pan scene transitions"
        ],
        "evaluation": [
            "Cut invisibility: Does the cut feel natural or jarring?",
            "Audio continuity: Does the L/J-cut bridge soften the transition?"
        ],
        "weaknesses": [
            "Phase 7.6 through 7.7.3: Every scene transition was a monotonous, unmotivated 0.5s crossfade.",
            "Audio abruptly cut off at video boundaries."
        ],
        "improvements": [
            "Created `EditingDirector` with rules mapping shot tension to cut type and automatic L/J-cut audio overhangs."
        ]
    },
    {
        "id": "module_05_character_animation.md",
        "title": "Module 05: 2D Character Animation & Rigging",
        "discipline": "Character Vitality, Natural Movement & Lip-Sync",
        "objectives": [
            "Infuse characters with involuntary life-cycles: Poisson-distributed blinks (2.8s–4.1s) and subtle harmonic breathing (0.35Hz).",
            "Implement 4-viseme lip-sync driven by audio speech energy envelopes (`rest`, `consonant`, `vowel_mid`, `vowel_wide`).",
            "Eliminate unblinking stares and robotic static poses.",
            "Add micro-movements: eye saccades, head tilts during listening, emotional eyebrow shifts."
        ],
        "exercises": [
            "5-second emotional reaction test: Character transitions from neutral listening to sudden surprise (eye widen, eyebrow lift, mouth gasp).",
            "Continuous speech synchronization test with natural mouth phoneme shaping."
        ],
        "examples": [
            "Disney's 12 Principles of Animation (Anticipation, Staging, Secondary Action)",
            "Anime micro-acting in Kyoto Animation productions (eyelid flutters, subtle posture shifts)"
        ],
        "evaluation": [
            "Life test: Does the character appear alive even when silent?",
            "Speech alignment: Does the mouth close on pauses and open on vocal peaks?"
        ],
        "weaknesses": [
            "Phase 7.6.1: Characters looked like cardboard dolls; mouths were fixed cutouts.",
            "Phase 7.7.1: Eyelids never blinked, producing an uncanny stare."
        ],
        "improvements": [
            "Engineered `BlinkController`, `LipSyncVisemeController`, and `BreathingController` in `motion_director.py`."
        ]
    },
    {
        "id": "module_06_3d_cgi.md",
        "title": "Module 06: 3D Animation & CGI Compositing",
        "discipline": "Spatial Geometry, Viewport Shaders & Hybrid Compositing",
        "objectives": [
            "Bridge 3D assets (vehicles, architectural sets) into 2D composite layers using match-moving and depth passes.",
            "Apply realistic lighting: key light, rim light, and ambient fill to match 2D background color palettes.",
            "Implement smooth camera tracking through 3D space with natural lens distortion."
        ],
        "exercises": [
            "Composite a 3D motorcycle model turning across a 2D illustrated street with matching shadow and specular highlights.",
            "Generate depth map passes for optical fog and distance falloff."
        ],
        "examples": [
            "Ufotable's hybrid 2D/3D compositing in *Demon Slayer*",
            "Spider-Man: *Into the Spider-Verse* (blending 3D geometry with 2D expressive line-work)"
        ],
        "evaluation": [
            "Lighting integration: Does the 3D element blend seamlessly with the 2D scene?",
            "Perspective consistency: Does the geometry align with background vanishing points?"
        ],
        "weaknesses": [
            "Phase 7.3: 3D pipeline ran isolated without compositing into the narrative video timeline."
        ],
        "improvements": [
            "Built 2.5D compositing bridge in `09_CONTENT_STUDIO/engine/openfilm_adapter.py`."
        ]
    },
    {
        "id": "module_07_motion_graphics.md",
        "title": "Module 07: Motion Graphics & Visual Effects",
        "discipline": "Typography, HUD Interfaces & Particle Physics",
        "objectives": [
            "Render pristine Devanagari typography with 100% accurate conjuncts, matras, and ligatures using HarfBuzz text shaping.",
            "Simulate atmospheric environmental particles: slanted velocity-blurred rain, rising embers, drifting smoke.",
            "Design futuristic yet grounded in-world HUD telemetry (digital speedometers, GPS navigation, countdown timers).",
            "Eliminate broken font glyphs and misaligned text overlays."
        ],
        "exercises": [
            "Render dynamic Devanagari title sequence with alpha-channel fade and drop shadow.",
            "Generate deterministic heavy rain particle system with splash ripples on asphalt."
        ],
        "examples": [
            "Contemporary Bollywood neo-noir title sequences (*Sacred Games*, *Andhadhun*)",
            "Industrial Light & Magic atmospheric particle compositing"
        ],
        "evaluation": [
            "Devanagari legibility: Are all complex conjuncts rendered correctly without missing matras?",
            "Particle velocity: Does rain angle match camera movement velocity?"
        ],
        "weaknesses": [
            "Phase 7.6.1: PIL font rendering produced broken, garbled Hindi characters.",
            "Phase 7.7.4: Particle randomness without deterministic seeding caused flickering."
        ],
        "improvements": [
            "Built Headless Chrome Devanagari Renderer and deterministic SVG `ParticleSystem` in `motion_director.py`."
        ]
    },
    {
        "id": "module_08_sound_design.md",
        "title": "Module 08: Sound Design & Foley",
        "discipline": "Acoustic Realism, Spot Foley & Audio Stems",
        "objectives": [
            "Eliminate generic procedural drone noise; construct multi-layered realistic soundscapes.",
            "Master audio stem hierarchy: Dialogue (Vocal), Spot Foley (Diegetic action), Ambience (Environment), and Score (Music).",
            "Synchronize transient Foley effects (footsteps, motor revs, doors, visor clicks) to exact video action frames.",
            "Enforce broadcast-grade vocal ducking (-14 dB attenuation on background stems during dialogue)."
        ],
        "exercises": [
            "Synchronize 5 spot Foley events to vehicle acceleration, brake squeal, and rain impacts.",
            "Master a 4-track audio mix complying with EBU R128 (-23 LUFS / -20 dBFS RMS, -2.5 dBFS True Peak)."
        ],
        "examples": [
            "Ben Burtt's tactile Foley sound design in *Star Wars*",
            "Gary Rydstrom's dynamic range and silence management in *Saving Private Ryan*"
        ],
        "evaluation": [
            "Speech clarity: Is dialogue 100% intelligible over music and rain?",
            "Foley timing: Do sound transients align within +/- 1 frame of visual contact?"
        ],
        "weaknesses": [
            "Phase 7.4/7.5: Used procedural white noise; sound effects were completely absent.",
            "Phase 7.6: Narration was drowned out by background music."
        ],
        "improvements": [
            "Built `SoundDesignEngine` with frame-accurate event cues and automated -14 dB vocal sidechain ducking."
        ]
    },
    {
        "id": "module_09_voice_acting.md",
        "title": "Module 09: Voice Acting & Dialogue Direction",
        "discipline": "Speech Prosody, Cadence & Vocal Acting",
        "objectives": [
            "Direct voice generation to reflect true emotional state: urgent whisper, breathless panic, relieved warmth.",
            "Eliminate robotic pauses and stilted sentence rhythm.",
            "Use natural Indian conversational cadence with appropriate contractions and pauses for breath.",
            "Master pacing variation: speaking rapidly during danger and slowing down during intimate realizations."
        ],
        "exercises": [
            "Generate high-urgency dialogue delivery under breathless exertion.",
            "Generate intimate emotional transition from grief to relief."
        ],
        "examples": [
            "Contemporary Mumbai urban voice acting in modern Hindi cinema",
            "Pixar voice direction for subtle emotional vulnerability"
        ],
        "evaluation": [
            "Human authenticity: Does the voice sound like a real person experiencing the situation?",
            "Prosody contour: Does pitch rise naturally on questions and drop on firm conclusions?"
        ],
        "weaknesses": [
            "Phase 7.7.1: Words were disconnected with artificial pauses between syllables.",
            "Phase 7.7.4: Initial voice cue dragged too long and overlapped subsequent lines."
        ],
        "improvements": [
            "Engineered prosodic envelope tuning, speech-rate modulation, and silence trimming in `voiceover_engine.py`."
        ]
    },
    {
        "id": "module_10_color_grading.md",
        "title": "Module 10: Color Grading & Visual Composition",
        "discipline": "Color Harmonies, Atmospheric Lighting & Cinematic Tone",
        "objectives": [
            "Apply deliberate color theory: Complementary (Teal & Orange), Split-Analogous, Monochromatic Noir.",
            "Establish emotional progression through color: Dark desaturated rainstorm shifting to warm golden dawn.",
            "Add optical vignette and depth shading to draw the viewer's eye directly to key subjects.",
            "Avoid flat, uninspired, or garish primary color clashes."
        ],
        "exercises": [
            "Grade a night rainstorm scene with deep slate-blue shadows, wet asphalt reflections, and neon crimson accents.",
            "Execute an emotional color grade transition from cold clinical hospital cyan to warm morning sunrise amber."
        ],
        "examples": [
            "Vittorio Storaro's color psychology in *The Last Emperor*",
            "The Coen Brothers' atmospheric sepia palettes in *O Brother, Where Art Thou?*"
        ],
        "evaluation": [
            "Palette cohesion: Do all elements belong to the same optical universe?",
            "Emotional resonance: Does the color grade reinforce the scene's emotional intent?"
        ],
        "weaknesses": [
            "Phase 7.6: Colors were garish and uncoordinated.",
            "Phase 7.7.2: Lighting was flat without shadow falloff or volumetric depth."
        ],
        "improvements": [
            "Defined Cinematic Color Scripts and dynamic vignette overlays in `motion_director.py`."
        ]
    },
    {
        "id": "module_11_pacing_and_timing.md",
        "title": "Module 11: Pacing, Suspense, Comedy & Emotional Timing",
        "discipline": "Temporal Rhythm, Anticipation & Payoff",
        "objectives": [
            "Understand that cinema is the art of manipulating time.",
            "Build suspense through escalating tempo: shortening shot durations as a deadline approaches.",
            "Execute comedic timing: the 3-beat rhythm (Setup, Expectation, Subversion/Awkward Pause).",
            "Give dramatic moments space to breathe: never cut away from a revelation too quickly."
        ],
        "exercises": [
            "10-second suspense sequence: Countdown clock accelerating cuts from 3s to 1s to 0.5s with rising audio frequency.",
            "10-second comedy sequence: High-stakes dramatic buildup punctured by a mundane, deadpan reality after a 1.2s awkward silence."
        ],
        "examples": [
            "Buster Keaton and Charlie Chaplin visual comedic timing",
            "Denis Villeneuve's tension stretches in *Sicario*"
        ],
        "evaluation": [
            "Anticipation factor: Does the audience lean forward waiting for the beat?",
            "Payoff impact: Does the resolution land with satisfying emotional force?"
        ],
        "weaknesses": [
            "Phase 7.7.3: Every scene was exactly 7.5 seconds, creating a mechanical metronome effect.",
            "Jokes lacked comedic pauses and fell completely flat."
        ],
        "improvements": [
            "Implemented Dynamic Metric Pacing in `EditingDirector` allowing variable shot durations (1.2s to 9.0s) driven by dramatic tension."
        ]
    },
    {
        "id": "module_12_quality_control.md",
        "title": "Module 12: Final Quality Control & Regression Testing",
        "discipline": "Zero-Defect Pipeline, Automated Telemetry & Human QA",
        "objectives": [
            "Enforce strict rasterization dimensions and byte stride verification: `len(buffer) == w * h * 3`.",
            "Detect scanline tearing, buffer offset wrapping, and frame jitter via Farneback optical flow and phase correlation.",
            "Verify Nyquist-Shannon sampling limits on all camera and procedural motion ($f \le f_s / 2$).",
            "Establish dual-gate QA: Technical compliance must never override human creative rejection."
        ],
        "exercises": [
            "Automated 240-frame decode audit verifying zero black frames, zero frozen frames, and zero scanline jitter.",
            "Regression test asserting exact stride compliance across all SVG-to-raster operations."
        ],
        "examples": [
            "Pixar RenderMan automated regression testing pipelines",
            "Broadcast SMPTE compliance certification"
        ],
        "evaluation": [
            "Stride safety: Does the engine raise an error on any dimensional mismatch?",
            "Stability score: Is mean unintended jitter < 0.20 px?"
        ],
        "weaknesses": [
            "Phase 7.7.4: Automated QA falsely passed an unwatchable video because scanline tearing caused high SAD.",
            "PyMuPDF 96 DPI mismatch caused 840-scanline buffer rolling offset."
        ],
        "improvements": [
            "Engineered `render_svg_to_image_safe` with mandatory byte assertions and dual optical stability QA in `regression_tests/`."
        ]
    }
]

for m in modules:
    filepath = os.path.join(CURRICULUM_DIR, m["id"])
    content = f"""# {m['title']}
## Video Director Academy Specialist Curriculum

**Discipline**: {m['discipline']}  
**Status**: APPROVED & CODIFIED  

---

### 1. Learning Objectives
{chr(10).join([f"- {obj}" for obj in m['objectives']])}

---

### 2. Practical Training Exercises
{chr(10).join([f"{i+1}. {ex}" for i, ex in enumerate(m['exercises'])])}

---

### 3. Master Film References & Examples
{chr(10).join([f"- {ex}" for ex in m['examples']])}

---

### 4. Skill-Specific Evaluation Benchmarks
{chr(10).join([f"- **{crit.split(':')[0]}**: {crit.split(':')[1]}" if ':' in crit else f"- {crit}" for crit in m['evaluation']])}

---

### 5. Identified Historical Weaknesses
{chr(10).join([f"- {w}" for w in m['weaknesses']])}

---

### 6. Reusable Production Improvements
{chr(10).join([f"- {imp}" for imp in m['improvements']])}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated curriculum spec: {m['id']}")

print("\nAll 12 Video Director Academy curriculum specs generated successfully.")
