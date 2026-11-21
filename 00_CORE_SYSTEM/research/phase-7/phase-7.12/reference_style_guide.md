# MASTER AI: 9:16 VERTICAL REFERENCE STYLE GUIDE
**Target Format**: Instagram Reels / YouTube Shorts / TikTok  
**Resolution**: **1080 × 1920 (9:16 Vertical Portrait)**  
**Target Output**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.12\reference_style_guide.md`  
**Date**: 2026-11-18  

---

## 1. Vertical Screen Anatomy & Safe Zones (1080 × 1920)

```
+---------------------------------------------+ y = 0
| [TOP SAFE ZONE - 280px / 14.5%]             |
| Reserved: Native OS status bar, time, WiFi  |
| Allowed: High-contrast title header hook    |
+---------------------------------------------+ y = 280px
|                                             |
| [HERO VISUAL & ACTION ZONE - 1100px / 57%]  |
|                                             |
| Main characters, primary action, B-roll,    |
| motion graphics, UI screencasts, diagrams   |
| Center of optical interest at y = 800-1000px|
|                                             |
+---------------------------------------------+ y = 1380px
| [KINETIC CAPTION ZONE - 220px / 11.5%]      |
| High-contrast karaoke captions (1-3 words)  |
+---------------------------------------------+ y = 1600px
| [BOTTOM UI DANGER ZONE - 320px / 16.7%]     |
| Reserved: Instagram username, audio track,  |
| caption drawer, like/comment buttons.       |
| STRICT RULE: NEVER place vital info here!   |
+---------------------------------------------+ y = 1920px
```

### Margin Specifications
- **Left Margin**: 72px minimum inset from edge (action safe).
- **Right Margin**: 120px minimum inset (avoids native like/comment/share overlay buttons on right edge).
- **Top Inset**: 280px from top edge.
- **Bottom Inset**: 320px from bottom edge.

---

## 2. Color Grading & Lighting Architecture

### Palette Schemes by Narrative Tone

1. **Tech / Modern Explainer (Inspired by Ref 01 & Ref 03)**:
   - Primary Background: Deep Slate `#0F172A` or Clean Porcelain `#F8FAFC`.
   - Card Surfaces: Solid neutral with 1px border `#334155` or `#E2E8F0`.
   - Primary Accent: Neon Cyan `#06B6D4` or Electric Royal Blue `#2563EB`.
   - Warning / Alert: Energetic Amber `#F59E0B` or Signal Red `#EF4444`.

2. **Narrative Chaptering (Inspired by Ref 04)**:
   - Color grading shifts harmoniously with dramatic acts.
   - Act 1 (Hook / Tension): Ice Blue / Desaturated Cool (`#B1C3CE`).
   - Act 2 (Discovery / Investigation): Sage Green / Forest Mist (`#ADC3B1`).
   - Act 3 (Climax / Reveal): Warm Coral / Amber Glow (`#D7A39E` to `#D8C08C`).

### Contrast & Legibility Rules
- All text must satisfy WCAG AAA contrast ratio (≥ 7:1 against background).
- When text overlays variable video or illustration, an intentional backing card (e.g. solid rounded box with 85% opacity) or dark outline (3px stroke) must be enforced.

---

## 3. Typography & Kinetic Subtitle Standards

### Font Hierarchy
- **Header Hook**: Bold Sans-Serif (e.g., Montserrat ExtraBold, Inter Black, Bebas Neue), 64–78pt, uppercase.
- **Kinetic Subtitles**: Heavy Sans-Serif (e.g., Inter Bold, Proxima Nova Bold), 52–60pt.
- **Technical UI / Code**: Monospace (e.g., JetBrains Mono, Fira Code), 38–44pt.

### Kinetic Animation Types
1. **Karaoke Word Bounce**: The full line appears in clean white; the active spoken word pops up 1.15x scale in bright yellow (`#FACC15`) with a 0.15s ease-out snap.
2. **Word Stagger Reveal**: Words appear one by one synchronized with voice syllables (maximum 3 words on screen simultaneously).
3. **Card Pop**: High-value takeaway keywords appear inside an animated pill container.

---

## 4. Visual Media Integration Rules

1. **Never crop a 16:9 landscape video into 9:16 by center-punch zooming alone.** Center-cropping 16:9 degrades pixel fidelity and cuts off peripheral narrative details.
2. **Proper 16:9 to 9:16 Translation Modes**:
   - **Split Screen / Multi-Tier**: 16:9 clip centered in the middle zone (y = 540 to 1380), with blurred cloned background above and below, topped by bold animated title header.
   - **Dynamic Camera Pan & Scan**: Smooth virtual camera tracking the subject across the 16:9 source.
   - **Native 9:16 Generation**: Produce the master art or video directly in 1080×1920 viewport.
