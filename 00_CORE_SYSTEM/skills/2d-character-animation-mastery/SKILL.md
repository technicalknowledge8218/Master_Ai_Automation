---
name: 2d-character-animation-mastery
description: "Mastery blueprint and production specification for 2D character design, rigging, anatomy, multi-archetype viseme lip-sync, and locomotion based on industry standards (Dribbble, Adobe Stock, CharacterBazaar, Pinterest, Magnific)."
---

# 2D Character Animation & Rigging Mastery (LOCKED PRODUCTION SPECIFICATION)

> [!IMPORTANT]
> **PERMANENT PRODUCTION LOCK**: This specification defines the permanently locked standard for 2D character animations, story-type explainer reels, multi-character dialogues, and kinetic typography. All future story videos produced by the system MUST follow these exact rules.

---

## 1. Character Archetypes & Anatomical Proportions

To prevent uncanny valley and ensure visual variety, all characters must adhere to strict head-count proportions:

| Archetype | Head Ratio | Silhouette & Key Features | Movement Dynamics |
| :--- | :--- | :--- | :--- |
| **Baby Boy / Toddler** | `1 : 3.0` | Oversized rounded cranium, big sparkling pupils, chubby cheeks, short stubby limbs. | Bouncy, clumsy balance, exaggerated arm swings, wide-eyed wonder. |
| **Junior / School Kid** | `1 : 4.5` | Energetic proportions, bright expressive features, casual school/play wear. | Quick agile hops, spontaneous hand gestures, enthusiastic head tilts. |
| **Young / Teen Gamer** | `1 : 5.5` | Angular jawline, stylized hair, hoodies/bomber jackets, gaming headphones. | Grounded tech stance, deliberate pointing, micro head bobs synced to beat. |
| **Female Lead / Host** | `1 : 6.0` | Balanced proportions, clear jawline, expressive eyes, sleek modern apparel. | Fluid shoulder transitions, open-palm welcoming gestures, subtle hair sway. |
| **Senior / Mentor / Boss** | `1 : 6.0` | Spectacles, distinguished mustache/beard, structured blazers/kurtas. | Authoritative calm posture, deliberate hand gestures, slow measured nodding. |
| **Cartoon Mascot** | `1 : 2.5` | Dynamic rubber-hose or modern vector mascot with bold outlines and gloves. | Squashed & stretched squash dynamics, exaggerated anticipation and overshoot. |

---

## 2. Rigging Architecture & Zero Eye-Flicker Protocol

To prevent rapid, jarring eye flickering / spasming during character speech:

1. **Decoupled Layer Architecture**:
   * **Base Layer (Fixed Body & Face)**: The character's torso, clothes, neck, hair, head, and **wide-open eyes** are rendered as ONE immutable, 100% solid base layer.
   * **Mouth-Only Composite**: During speech, **ONLY the mouth region (from below nose to chin)** is updated. The eyes, eyebrows, and forehead NEVER swap during syllable pronunciation.
2. **Tri-State Viseme Dynamics**:
   * **`REST` (Closed Lips)**: Used during silence, audio gaps, and natural pauses between words.
   * **`MID` (Semi-Open Mouth)**: Used for consonants (`M`, `B`, `P`, `T`, `D`, `S`, `Z`, `F`, `V`) and transitional syllables.
   * **`OPEN` (Wide Open Cavity)**: Used for expressive vowels (`A`, `O`, `E`, `U`).
   * **Minimum Hold Time**: Each viseme state is held for at least 2 frames (66ms) to eliminate high-frequency visual chatter.
3. **Natural Human Eye Blinking ("Kabhi-Kabhi Kare, Na Ki Baar-Baar")**:
   * **Biological Interval**: Blinking is strictly decoupled from mouth speech. Characters blink naturally **once every 3.5 to 4.5 seconds**.
   * **Micro-Blink Duration**: A blink lasts exactly **3 frames (100 milliseconds)**:
     - Frame 1: 50% closed transition
     - Frame 2: 100% closed eyelid
     - Frame 3: 50% reopening transition
   * At all other times, eyes remain 100% open, focused, and steady.

---

## 3. Lip-Sync & Word-Level Forced Alignment

1. **Whisper Word-Level Timestamps**:
   * All voiceover tracks are processed through forced alignment to extract exact start and end timestamps `[w_start, w_end]` for every spoken word.
2. **Audio-Energy Envelope Modulation**:
   * Within a word interval, speech opening is modulated by a 3-frame rolling smoothed RMS audio energy curve.
   * Between words (silence, breathing gaps, punctuation pauses), the mouth immediately snaps to `REST` (closed).
3. **Turn-Based Speaker Isolation (Duo & Squad)**:
   * When one character has the floor, other characters stay in attentive resting poses with mouth closed. Only the active speaker's mouth animates.

---

## 4. Kinetic Typography Subtitles (No-Box Clean Pop Standard)

This standard replaces heavy background pill boxes with sleek, viral kinetic typography:

1. **NO Background Box**: Shabdon ke peeche koi rounded box ya pill nahi rahega. Background clean aur transparent rehta hai.
2. **Active Word Scale Pop (+25% Larger)**:
   * Jo word voice bol rahi hai, uska font size automatically thoda bada ho jata hai (e.g. `34px` $\to$ `44px`) bina kisi jitter ke.
3. **Signature Accent Color Switch**:
   * Sirf active bolta hua shabd character ke signature accent color mein glow karta hai:
     - **Young Gamer (Dev)**: Glowing Cyan (`#00E5FF`)
     - **Female Host (Neha)**: Vivid Mint Green (`#00FFB4`)
     - **Junior Kid (Chintu)**: Energetic Coral (`#FF5050`)
     - **Senior Mentor (Dr. Sharma)**: Rich Gold (`#FFBE32`)
4. **Sentence State Hierarchy**:
   * **Past Spoken Words**: Solid Clean White `(255, 255, 255)`
   * **Current Word**: Larger Letter Size + Character Accent Color
   * **Future Words**: Muted Subtle Gray `(125, 130, 140)`

---

## 5. Multi-Character Stage Staging & Framing

1. **Zero Screen Shake / Zero Zoom In-Out**:
   * Characters aur background elements 100% grounded aur fixed scale par rehte hain (no pulsing spotlight radii, no continuous resize).
2. **Duo Format (2 Characters - Dev & Neha)**:
   * Side-by-side split podiums (Pod Left: `475x780`, Pod Right: `475x780`).
   * Active speaker gets an illuminated accent border and `[SPEAKING]` tag; listener gets a dimmed gray border and `[LISTENING]` tag.
3. **Squad Format (4 Characters - Roundtable Panel)**:
   * 2×2 clean grid layout (`475x490` per box).
   * Mic handover dynamically illuminates whichever character has the turn; other 3 remain in calm resting poses.

---

## 6. Voice Synthesis Protocol (Strict Mandate)

1. **Google Gemini Neural TTS Only**:
   * Multi-model fallback pool: `gemini-3.8-flash-lite-tts` $\to$ `gemini-3.1-flash-tts-preview` $\to$ `gemini-2.5-flash-preview-tts`.
   * Standard voice casting:
     - Young Male Gamer: `Puck`
     - Female Host / Lead: `Kore`
     - Senior Mentor / Boss: `Charon`
     - Junior School Kid: `Puck` (high energy pitch)
2. **Zero Microsoft / Edge-TTS**:
   * Microsoft Edge-TTS package and voices are permanently removed and forbidden from the system.

---

## 7. Master Production References & Showcase Files

| Video Title | Format | File Path |
| :--- | :--- | :--- |
| **Duo Conversation Master** | 2-Char (Dev & Neha) | `F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\demo_05_duo_conversation.mp4` |
| **Squad Panel Master** | 4-Char Roundtable | `F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\demo_06_squad_4_characters.mp4` |
| **Young Gamer Solo** | Solo (Dev) | `F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\demo_01_young_male.mp4` |
| **Female Host Solo** | Solo (Neha) | `F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\demo_02_female_host.mp4` |
| **Senior Mentor Solo** | Solo (Dr. Sharma) | `F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\demo_03_senior_mentor.mp4` |
| **Junior Kid Solo** | Solo (Chintu) | `F:\Master AI\00_CORE_SYSTEM\engine\video_production\editing_showcase\demo_04_junior_kid.mp4` |
