# Module 03: Cinematography & Camera Language
## Video Director Academy Specialist Curriculum

**Discipline**: Optical Physics, Shot Scales & Multi-Plane Parallax  
**Status**: APPROVED & CODIFIED  

---

### 1. Learning Objectives
- Master shot scale taxonomy: Extreme Close-Up (ECU), Close-Up (CU), Medium Shot (MS), Wide (WS), Extreme Wide (EWS).
- Apply multi-plane parallax depth: background (0.2x), midground (0.7x), subject (1.0x), foreground (1.4x).
- Replace robotic linear camera zooms with cubic easing curves (`ease_in_out_cubic`, `ease_out_back`).
- Integrate realistic camera physics: inertia, damped harmonic shake, and optical depth of field.

---

### 2. Practical Training Exercises
1. 5-second eased dolly zoom (Vertigo effect) combining optical scale expansion with background compression.
2. Multi-plane parallax lateral tracking shot with 4 distinct spatial layers.

---

### 3. Master Film References & Examples
- Roger Deakins' naturalistic focal choices in *Blade Runner 2049*
- Hayao Miyazaki's lush multi-plane cel animation depth in *Spirited Away*

---

### 4. Skill-Specific Evaluation Benchmarks
- **Parallax integrity**:  Do layers move at geometrically consistent optical speeds?
- **Camera smoothness**:  Is camera acceleration derivative continuous (no jerk/snapping)?

---

### 5. Identified Historical Weaknesses
- Phase 7.6: Single-layer flat pans looked like moving a photocopy.
- Phase 7.7.4: 24Hz camera shake aliased into severe scanline vibration.

---

### 6. Reusable Production Improvements
- Upgraded `Camera2D` in `motion_director.py` with 4-plane parallax and Nyquist-safe 6.0Hz damped harmonic vibration.
