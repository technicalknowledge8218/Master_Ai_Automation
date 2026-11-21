# Module 05: 2D Character Animation & Rigging
## Video Director Academy Specialist Curriculum

**Discipline**: Character Vitality, Natural Movement & Lip-Sync  
**Status**: APPROVED & CODIFIED  

---

### 1. Learning Objectives
- Infuse characters with involuntary life-cycles: Poisson-distributed blinks (2.8s–4.1s) and subtle harmonic breathing (0.35Hz).
- Implement 4-viseme lip-sync driven by audio speech energy envelopes (`rest`, `consonant`, `vowel_mid`, `vowel_wide`).
- Eliminate unblinking stares and robotic static poses.
- Add micro-movements: eye saccades, head tilts during listening, emotional eyebrow shifts.

---

### 2. Practical Training Exercises
1. 5-second emotional reaction test: Character transitions from neutral listening to sudden surprise (eye widen, eyebrow lift, mouth gasp).
2. Continuous speech synchronization test with natural mouth phoneme shaping.

---

### 3. Master Film References & Examples
- Disney's 12 Principles of Animation (Anticipation, Staging, Secondary Action)
- Anime micro-acting in Kyoto Animation productions (eyelid flutters, subtle posture shifts)

---

### 4. Skill-Specific Evaluation Benchmarks
- **Life test**:  Does the character appear alive even when silent?
- **Speech alignment**:  Does the mouth close on pauses and open on vocal peaks?

---

### 5. Identified Historical Weaknesses
- Phase 7.6.1: Characters looked like cardboard dolls; mouths were fixed cutouts.
- Phase 7.7.1: Eyelids never blinked, producing an uncanny stare.

---

### 6. Reusable Production Improvements
- Engineered `BlinkController`, `LipSyncVisemeController`, and `BreathingController` in `motion_director.py`.
