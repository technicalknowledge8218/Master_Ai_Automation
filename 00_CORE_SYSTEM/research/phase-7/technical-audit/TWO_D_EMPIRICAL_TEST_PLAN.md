# 2D ANIMATION & MOTION GRAPHICS EMPIRICAL TEST PLAN
**Master AI — Phase 7.0.3 Independent Technical Reality Audit**  
**Audit Target:** 2D Motion Graphics, Infographics & Kinetic Typography Pipeline  
**Core Technologies:** Manim Community Edition (MIT) & Lemo-Opuscar Frame-Piper Pattern (MIT)  
**Execution Environment:** Windows 11, Intel Core i5-1245U, 32 GB RAM, Python 3.14  
**Status Classification Standard:**
- `Verified from official documentation`
- `Verified by actual local testing`
- `Estimated but untested`
- `Unverified`
- `Unsupported or incorrect`

---

## 1. Test Objective & Scope

This test plan defines the empirical validation protocol for Master AI's Mode A (2D Production Engine) to be executed during Phase 7.1 implementation. It establishes a repeatable, automated benchmark to verify that the system can procedurally generate professional-grade 2D animated scenes without manual human intervention.

### Core Capabilities Validated:
1. **Procedural Scene Scripting:** Automatic generation of clean, error-free Python animation scripts.
2. **Kinetic Typography:** High-contrast text layout, kerning, word-by-word reveal, and spatial transitions.
3. **Dynamic Infographic Elements:** Smooth vector graphing, coordinate system drawing, and animated statistics.
4. **Alpha Channel & Overlay Support:** Rendering with transparent backgrounds (ProRes 4444 or PNG image sequences) for seamless compositing over real footage.
5. **Render Throughput & Hardware Load:** Benchmarking frame generation times on the host CPU.

---

## 2. Test Scene Architecture: "The Apex Predator Metrics"

To rigorously stress-test the 2D rendering pipeline, the test scene is designed with multiple concurrent vector layers:

```
+---------------------------------------------------------------+
|  [00:00 - 00:02] Kinetic Title: "AFRICAN LION: ROAR DYNAMICS" |
|  - Font: Sans-serif bold, glow outline, letter-by-letter fade |
|                                                               |
|  [00:02 - 00:07] Animated Infographic & Radial Gauge:         |
|  - Sound Intensity: 114 dB vs 80 km/h Sprint Velocity          |
|  - Real-time animated SVG arcs and coordinate axes            |
|                                                               |
|  [00:07 - 00:10] Outro & Metric Callout:                      |
|  - "Heard Across 8.0 Kilometers" with pulse wave animation     |
|  - Directional wipe transition to transparent alpha           |
+---------------------------------------------------------------+
```

### Technical Parameters:
- **Duration:** 10.00 seconds (300 frames @ 30 FPS or 240 frames @ 24 FPS)
- **Target Resolution:** 1920 × 1080 (1080p Full HD)
- **Pixel Aspect Ratio:** 1:1 (Square pixels)
- **Color Space:** BT.709 / sRGB
- **Target Video Codec:** H.264 (libx264, profile=high, crf=18, yuv420p)
- **Optional Alpha Master:** QuickTime Animation or ProRes 4444 (`yuva444p10le`)

---

## 3. Step-by-Step Test Execution Protocol

### Step 1: Automated Script Generation
The Master AI 2D Agent synthesizes an autonomous Python script (`test_2d_infographic.py`) adhering strictly to Manim Community API standards:

```python
from manim import *

class LionRoarMetrics(Scene):
    def construct(self):
        # Configure color palette
        GOLD = "#FFB300"
        DARK_SLATE = "#1E293B"
        WHITE = "#FFFFFF"

        # Background card
        bg_card = RoundedRectangle(corner_radius=0.3, height=6.0, width=12.0, fill_color=DARK_SLATE, fill_opacity=0.85, stroke_color=GOLD, stroke_width=2)
        self.play(FadeIn(bg_card, shift=UP * 0.5), run_time=1.0)

        # Kinetic Title
        title = Text("AFRICAN LION: ACOUSTIC POWER", font="Montserrat", font_size=38, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=1.2)
        self.play(Write(title), run_time=1.2)

        # Metrics Axes & Bar
        axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 120, 30],
            x_length=6,
            y_length=3,
            axis_config={"color": GREY_B},
        ).shift(DOWN * 0.6 + LEFT * 2.5)

        labels = axes.get_axis_labels(x_label="Distance (km)", y_label="SPL (dB)")
        graph = axes.plot(lambda x: 114 - 12 * np.log2(x + 1), color=YELLOW, x_range=[0.1, 7.8])

        self.play(Create(axes), Write(labels), run_time=1.5)
        self.play(Create(graph), run_time=1.8)

        # Metric Pulse Callout
        callout_box = Rectangle(width=4.0, height=2.5, fill_color="#0F172A", fill_opacity=0.9, stroke_color=YELLOW)
        callout_box.shift(RIGHT * 3.5 + DOWN * 0.6)
        stat_num = Text("114 dB", font_size=44, color=YELLOW, weight=BOLD).move_to(callout_box.get_top() + DOWN * 0.8)
        stat_lbl = Text("Audible over 8 km", font_size=20, color=WHITE).next_to(stat_num, DOWN, buff=0.3)

        self.play(FadeIn(callout_box, scale=0.8), Write(stat_num), FadeIn(stat_lbl), run_time=1.5)
        self.wait(1.5)

        # Outro Transition
        self.play(FadeOut(Group(bg_card, title, axes, labels, graph, callout_box, stat_num, stat_lbl), shift=DOWN * 0.8), run_time=1.5)
```

### Step 2: Headless Command-Line Execution
Run Manim in batch headless mode via subprocess:
```bash
manim render -ql test_2d_infographic.py LionRoarMetrics --format=mp4   # For 480p preview (15 fps)
manim render -qh test_2d_infographic.py LionRoarMetrics --format=mp4   # For 1080p final (60 fps)
```
- Capture CPU utilization, RAM consumption, and elapsed wall-clock seconds.

### Step 3: FFprobe Automated QA Verification
The resulting MP4 file must be validated with the standard Master AI video verification suite:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames,duration,codec_name -of json output.mp4
```

---

## 4. Empirical Acceptance Thresholds

| Metric | Target Specification | Minimum Pass Threshold | Test Method | Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Duration Precision** | 10.00 seconds (±0.05s) | 9.90s ≤ duration ≤ 10.10s | FFprobe duration check | `Verified from official documentation` |
| **Resolution** | 1920 × 1080 | Exact 1920x1080 | Stream metadata | `Verified from official documentation` |
| **Frame Integrity** | 300 frames (at 30 FPS) | 0 dropped or torn frames | FFmpeg decode test (`null` muxer) | `Verified from official documentation` |
| **Frame Generation Speed** | ≤ 0.25 sec/frame (4+ FPS render) | ≤ 0.80 sec/frame (1.25 FPS) | Host benchmark timer | `Estimated but untested` |
| **Peak Memory Consumption** | < 2.0 GB RAM | < 4.0 GB RAM | Process monitor log | `Estimated but untested` |
| **Visual Legibility** | High contrast (>7:1 ratio) | Text readable at 720p scaling | Automated luminance check | `Estimated but untested` |

---

## 5. Contingency & Fallback Strategy

1. **Missing System Dependencies (Cairo/Pango):** If local Cairo libraries encounter Windows DLL binding issues, fall back to pure SVG rasterization via `svglib` + `Pillow` or headless browser Canvas rendering via Playwright (`take_screenshot` per frame).
2. **Framerate Drift:** If Manim outputs variable frame rates, pipe raw frames directly into FFmpeg through stdin using the Lemo-Opuscar pattern (`ffmpeg -f rawvideo -pix_fmt rgba -s 1920x1080 -r 30 -i - -c:v libx264 -crf 18 output.mp4`).
3. **Classification:** `Verified from official documentation`.
