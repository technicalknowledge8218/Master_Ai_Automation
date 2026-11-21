# Module 12: Final Quality Control & Regression Testing
## Video Director Academy Specialist Curriculum

**Discipline**: Zero-Defect Pipeline, Automated Telemetry & Human QA  
**Status**: APPROVED & CODIFIED  

---

### 1. Learning Objectives
- Enforce strict rasterization dimensions and byte stride verification: `len(buffer) == w * h * 3`.
- Detect scanline tearing, buffer offset wrapping, and frame jitter via Farneback optical flow and phase correlation.
- Verify Nyquist-Shannon sampling limits on all camera and procedural motion ($f \le f_s / 2$).
- Establish dual-gate QA: Technical compliance must never override human creative rejection.

---

### 2. Practical Training Exercises
1. Automated 240-frame decode audit verifying zero black frames, zero frozen frames, and zero scanline jitter.
2. Regression test asserting exact stride compliance across all SVG-to-raster operations.

---

### 3. Master Film References & Examples
- Pixar RenderMan automated regression testing pipelines
- Broadcast SMPTE compliance certification

---

### 4. Skill-Specific Evaluation Benchmarks
- **Stride safety**:  Does the engine raise an error on any dimensional mismatch?
- **Stability score**:  Is mean unintended jitter < 0.20 px?

---

### 5. Identified Historical Weaknesses
- Phase 7.7.4: Automated QA falsely passed an unwatchable video because scanline tearing caused high SAD.
- PyMuPDF 96 DPI mismatch caused 840-scanline buffer rolling offset.

---

### 6. Reusable Production Improvements
- Engineered `render_svg_to_image_safe` with mandatory byte assertions and dual optical stability QA in `regression_tests/`.
