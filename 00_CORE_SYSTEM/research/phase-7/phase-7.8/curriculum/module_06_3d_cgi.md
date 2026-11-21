# Module 06: 3D Animation & CGI Compositing
## Video Director Academy Specialist Curriculum

**Discipline**: Spatial Geometry, Viewport Shaders & Hybrid Compositing  
**Status**: APPROVED & CODIFIED  

---

### 1. Learning Objectives
- Bridge 3D assets (vehicles, architectural sets) into 2D composite layers using match-moving and depth passes.
- Apply realistic lighting: key light, rim light, and ambient fill to match 2D background color palettes.
- Implement smooth camera tracking through 3D space with natural lens distortion.

---

### 2. Practical Training Exercises
1. Composite a 3D motorcycle model turning across a 2D illustrated street with matching shadow and specular highlights.
2. Generate depth map passes for optical fog and distance falloff.

---

### 3. Master Film References & Examples
- Ufotable's hybrid 2D/3D compositing in *Demon Slayer*
- Spider-Man: *Into the Spider-Verse* (blending 3D geometry with 2D expressive line-work)

---

### 4. Skill-Specific Evaluation Benchmarks
- **Lighting integration**:  Does the 3D element blend seamlessly with the 2D scene?
- **Perspective consistency**:  Does the geometry align with background vanishing points?

---

### 5. Identified Historical Weaknesses
- Phase 7.3: 3D pipeline ran isolated without compositing into the narrative video timeline.

---

### 6. Reusable Production Improvements
- Built 2.5D compositing bridge in `09_CONTENT_STUDIO/engine/openfilm_adapter.py`.
