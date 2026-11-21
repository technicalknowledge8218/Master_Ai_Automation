# MASTER AI — REPAIR LOG
## Phase 7.7.4.1: Rendering Pipeline & Motion Physics Stabilization

**Date**: November 18, 2026  
**Files Modified**:
- `F:\Master AI\09_CONTENT_STUDIO\engine\motion_director.py`
- `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4.1\engine\motion_director.py`
- `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\engine\motion_director.py`

---

### 1. Root Cause Fix: Stride & DPI Normalization

#### Problem:
- In Phase 7.7.4, `render_svg_to_image` passed `dpi=96` to PyMuPDF.
- Because the base SVG coordinate system is in 72 pt/inch, PyMuPDF scaled 1920x1080 up to **2560x1440** pixels ($11,059,200\text{ bytes}$).
- The FFmpeg stdin rawvideo consumer was configured for **1920x1080** ($6,220,800\text{ bytes}$).
- This caused an unhandled $4,838,400\text{ byte}$ ($840\text{ scanline}$) rolling offset every single frame, resulting in catastrophic vertical scanline wrapping and tearing glitch.

#### Solution Implemented:
- Implemented `render_svg_to_image_safe()` in `motion_director.py`:
  1. Calls `page.get_pixmap(dpi=72)` to enforce 1:1 pixel mapping for 1920x1080 SVG layouts.
  2. Verifies `img.size == (1920, 1080)`. If not, resizes with Lanczos antialiasing.
  3. Verifies `len(img.tobytes()) == 1920 * 1080 * 3 == 6,220,800` bytes before any write.
  4. Raises an immediate `ValueError` if a single byte discrepancy is detected.

---

### 2. Camera Motion & Nyquist Stabilization

#### Problem:
- In Phase 7.7.4, `Camera2D.trigger_shake()` invoked `decay_shake` with `freq = 24.0 Hz` at a 24 FPS framerate.
- This violated the Nyquist sampling criterion ($f_s \ge 2 f_{\max}$), causing mathematical aliasing and violent polarity flips on alternating frames.
- Re-triggering shake via `t % 0.6s` created harsh discontinuity spikes every 14 frames.

#### Solution Implemented:
- Clamped `decay_shake` frequency to **6.0 Hz on X** and **5.0 Hz on Y**, with quadrature phase offset ($+0.05\text{s}$) to produce gentle, continuous elliptical damping.
- Clamped maximum vibration amplitude to $6.0\text{ px}$.
- Added `Camera2D.set_position(x, y, zoom, angle)` and `get_svg_transform()` to ensure all layer projections use stable, centered coordinate transformations without snapping.

---

### 3. Verification Protocol Upgrade

#### Problem:
- Automated tests in Phase 7.7.4 relied on `Mean SAD > 5.0` to confirm "motion presence."
- Because scanlines were rolling by 840 rows every frame, SAD was measured at $21.43$, which the automated script falsely categorized as high-quality active motion.

#### Solution Implemented:
- Created a dual optical flow and phase correlation stability detector:
  1. Computes Farneback dense optical flow and phase correlation shifts ($\Delta x, \Delta y$).
  2. Tracks vertical acceleration $\Delta^2 y / \Delta t^2$ and sign reversals.
  3. Rejects any video displaying cyclic scanline offsets or bulk unexplained jumps $> 10\text{ px}$.
