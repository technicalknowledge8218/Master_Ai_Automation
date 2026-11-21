# Module 07: Motion Graphics & Visual Effects
## Video Director Academy Specialist Curriculum

**Discipline**: Typography, HUD Interfaces & Particle Physics  
**Status**: APPROVED & CODIFIED  

---

### 1. Learning Objectives
- Render pristine Devanagari typography with 100% accurate conjuncts, matras, and ligatures using HarfBuzz text shaping.
- Simulate atmospheric environmental particles: slanted velocity-blurred rain, rising embers, drifting smoke.
- Design futuristic yet grounded in-world HUD telemetry (digital speedometers, GPS navigation, countdown timers).
- Eliminate broken font glyphs and misaligned text overlays.

---

### 2. Practical Training Exercises
1. Render dynamic Devanagari title sequence with alpha-channel fade and drop shadow.
2. Generate deterministic heavy rain particle system with splash ripples on asphalt.

---

### 3. Master Film References & Examples
- Contemporary Bollywood neo-noir title sequences (*Sacred Games*, *Andhadhun*)
- Industrial Light & Magic atmospheric particle compositing

---

### 4. Skill-Specific Evaluation Benchmarks
- **Devanagari legibility**:  Are all complex conjuncts rendered correctly without missing matras?
- **Particle velocity**:  Does rain angle match camera movement velocity?

---

### 5. Identified Historical Weaknesses
- Phase 7.6.1: PIL font rendering produced broken, garbled Hindi characters.
- Phase 7.7.4: Particle randomness without deterministic seeding caused flickering.

---

### 6. Reusable Production Improvements
- Built Headless Chrome Devanagari Renderer and deterministic SVG `ParticleSystem` in `motion_director.py`.
