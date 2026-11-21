# MASTER AI — RENDERING REGRESSION TEST SPECIFICATION
## Automated Safeguards Against Stride Mismatches, Aliasing & False QA Passes

**Project Root**: `F:\Master AI`  
**Workspace**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8\`  
**Test Suite File**: [`regression_tests/test_rendering_pipeline.py`](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.8/regression_tests/test_rendering_pipeline.py)  
**Execution Status**: **5/5 TESTS PASSING (0.067s)**  
**Date**: November 18, 2026  

---

### 1. Purpose & Protection Scope

The regression test suite permanently prevents the recurrence of catastrophic visual and algorithmic defects identified during Phases 7.6 through 7.7.4.1.

Every test operates as a non-bypassable pre-commit gate before any production rendering is permitted:

```
                           REGRESSION TEST SUITE
                                     |
       +-----------------------------+-----------------------------+
       |                                                           |
       v                                                           v
[TEST 01: Stride Byte Assertion]           [TEST 02: Nyquist Sampling Limit]
Asserts len == 1920*1080*3 bytes           Clamps shake freq <= 6.0 Hz at 24fps
Guards against 840-line wrap               Guards against polarity sign flips
       |                                                           |
       v                                                           v
[TEST 03: Optical Stability Gate]          [TEST 04: Editorial Rule Validation]
Detects jumps > 20px as tearing            Rejects unmotivated routine crossfades
Guards against naive SAD false PASS        Enforces motivated cutting grammar
       |                                                           |
       +-----------------------------+-----------------------------+
                                     |
                                     v
                       [TEST 05: Audio Loudness Gate]
                       Enforces -14dB sidechain ducking
                       Guards against drowned dialogue
```

---

### 2. Test Cases & Mathematical Assertions

#### Test 01: `test_01_svg_raster_stride_integrity`
- **Guards Against**: Phase 7.7.4 primary root cause (PyMuPDF `dpi=96` outputting 2560x1440 = 11,059,200 bytes into a 1920x1080 FFmpeg rawvideo pipe).
- **Assertion**:
  $$\text{Target Resolution} = (1920, 1080)$$
  $$\text{Buffer Size} = 1920 \times 1080 \times 3 = \mathbf{6,220,800\text{ bytes}}$$
  $$\text{Tolerance} = \mathbf{0\text{ bytes}}$$

#### Test 02: `test_02_nyquist_camera_shake_safety`
- **Guards Against**: Phase 7.7.4 secondary root cause (24 Hz shake sampled at 24 FPS creating high-frequency alternating sign flips).
- **Assertion**:
  $$f_{\text{shake}} \le \frac{f_s}{2} = 12.0\text{ Hz}$$
  $$\text{Sign Flips per Second} \le 8\text{ flips/sec}$$

#### Test 03: `test_03_optical_flow_jitter_rejection_gate`
- **Guards Against**: Naive SAD metric falsely reporting PASS when scanlines are rolling.
- **Assertion**:
  - Smooth camera moves ($\text{std}(\Delta y) < 0.5\text{ px}$) $\to$ **PASS**
  - Scanline tearing wrap ($\max(|\Delta y|) > 20.0\text{ px}$) $\to$ **REJECT / FAIL**

#### Test 04: `test_04_creative_decision_engine_rules`
- **Guards Against**: Routine unmotivated crossfades and excessive camera shake.
- **Assertion**:
  - Rejects crossfades where `motivating_reason` does not specify a temporal or spatial chapter jump.
  - Rejects shake intensity $> 6.0\text{ px}$.

#### Test 05: `test_05_audio_broadcast_loudness_spec`
- **Guards Against**: Dialogue being overpowered by background music.
- **Assertion**:
  - Asserts vocal sidechain ducking attenuation is configured to $\le -14.0\text{ dB}$.

---

### 3. Execution Verification

The suite executes in under 0.1 seconds via standard Python `unittest`:
```
Ran 5 tests in 0.067s
OK
```
All tests are integrated into the autonomous execution pipeline and run automatically before every training exercise and production render.
