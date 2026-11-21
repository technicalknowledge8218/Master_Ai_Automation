# UNIFIED 2D + 3D + REAL FOOTAGE PRODUCTION ARCHITECTURE
## Tri-Modal Visual Production Core, Scene Medium Planner & Hybrid Compositing Architecture

**Document Version:** 1.0.0-unified-production  
**Project Root:** `F:\Master AI`  
**Target Path:** `00_CORE_SYSTEM\research\phase-7\unified-visual-production\UNIFIED_2D_3D_REAL_FOOTAGE_ARCHITECTURE.md`  
**Classification:** Core System Architecture & Visual Pipeline Design  
**Status:** Approved Master Architecture  

---

## 1. VISION & CORE ARCHITECTURAL PRINCIPLE

Master AI treats **2D Animation**, **True 3D CGI**, and **Genuine Real Footage** as three equal, first-class production modes.

No single visual format is universally superior:
- 3D CGI is not mandatory for an explainer that communicates best through clean 2D vector infographics.
- 2D animation is not acceptable where audience expectations demand photorealistic wildlife behavior.
- Real footage cannot display internal mechanical cutaways or astronomical planetary orbits.

The fundamental architectural principle of Master AI Phase 7.0.2 is **Tri-Modal Scene Harmonization**:
> *Every scene is assigned to the visual medium best suited for its narrative goal, and multiple mediums can seamlessly intersect within a single shot or timeline at a permanent operating cost of ₹0 / $0.*

---

## 2. TRI-MODAL SYSTEM ARCHITECTURE

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                    MASTER AI UNIFIED TRI-MODAL PRODUCTION HOUSE (₹0)                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│                           ┌───────────────────────────────┐                            │
│                           │      SCENE MEDIUM PLANNER     │                            │
│                           │   (SceneMediumPlanner.py)     │                            │
│                           └───────────────┬───────────────┘                            │
│                                           │                                            │
│            ┌──────────────────────────────┼──────────────────────────────┐             │
│            ▼                              ▼                              ▼             │
│  ┌───────────────────────┐  ┌───────────────────────────┐  ┌────────────────────────┐  │
│  │   MODE A: 2D CORE     │  │   MODE B: 3D CGI CORE     │  │  MODE C: REAL FOOTAGE  │  │
│  │ (TwoDAnimationAdapter)│  │   (ThreeDCGIAdapter)      │  │  (RealFootageAdapter)  │  │
│  ├───────────────────────┤  ├───────────────────────────┤  ├────────────────────────┤  │
│  │ • Lemo-Opuscar MIT    │  │ • Blender 4.x Headless bpy│  │ • Pexels Video API     │  │
│  │   (Canvas/SVG/WebGL)  │  │   (EEVEE Next / Iris Xe)  │  │   (Verified 1080p/4K)  │  │
│  │ • Manim Python Engine │  │ • Cycles CPU (Embree/OIDN)│  │ • Wikimedia Commons API│  │
│  │   (Math/Vector Plots) │  │ • glTF 2.0 / USD Loaders  │  │   (CC0 / Public Domain)│  │
│  │ • Kinetic Typography  │  │ • Rigged Skeletal Anims   │  │ • User Raw Video B-Roll│  │
│  │ • Parallax Cartography│  │ • Poly Haven CC0 Models   │  │ • SHA-256 Provenance   │  │
│  └───────────┬───────────┘  └─────────────┬─────────────┘  └───────────┬────────────┘  │
│              │                            │                            │               │
│              └────────────────────────────┼────────────────────────────┘               │
│                                           ▼                                            │
│                             ┌───────────────────────────┐                              │
│                             │   HYBRID SCENE COMPOSER   │                              │
│                             │ (HybridSceneComposer.py)  │                              │
│                             ├───────────────────────────┤                              │
│                             │ Multi-layer overlay, alpha│                              │
│                             │ masks, HUD data callouts  │                              │
│                             └─────────────┬─────────────┘                              │
│                                           ▼                                            │
│                             ┌───────────────────────────┐                              │
│                             │   UNIFIED TIMELINE ENGINE │                              │
│                             │ (UnifiedTimelineEngine.py)│                              │
│                             ├───────────────────────────┤                              │
│                             │ • FFmpeg 7.1 Complex Graph│                              │
│                             │ • Cinematic 3D LUTs       │                              │
│                             │ • EBU R128 Loudness Master│                              │
│                             │ • Multilingual ASS Subtitle                              │
│                             └─────────────┬─────────────┘                              │
│                                           ▼                                            │
│                             ┌───────────────────────────┐                              │
│                             │ VISUAL QUALITY EVALUATOR  │                              │
│                             │ & ASSET LICENSE VERIFIER  │                              │
│                             ├───────────────────────────┤                              │
│                             │ • 2D Animation QA Checks  │                              │
│                             │ • 3D True Depth QA Checks │                              │
│                             │ • Real Footage Provenance │                              │
│                             │ • Zero-Budget Spend Gate  │                              │
│                             └───────────────────────────┘                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. THE THREE VISUAL PRODUCTION MODES

### 3.1 MODE A: 2D Production Core (`TwoDAnimationAdapter`)
- **Domain Responsibilities:** Motion graphics, animated vector cartography, statistical data infographics, technical callouts, educational explainers, kinetic typography, and character illustration.
- **Engine Implementations:**
  1. *Lemo-Opuscar MIT Frame-Piper:* Headless Playwright/Chromium rendering HTML5 Canvas, SVG, and CSS animations directly to FFmpeg stdin at 20–30 FPS.
  2. *Manim Python (`manim`):* Programmatic mathematical equations, vector coordinate transforms, and dynamic charting.
  3. *Glaxnimate / Pillow:* Static vector rendering, raster thumbnails, and multi-layer parallax scrolling.

### 3.2 MODE B: True 3D CGI Production Core (`ThreeDCGIAdapter`)
- **Domain Responsibilities:** True geometric 3D characters, orbital camera paths, astronomical bodies, mechanical cutaways, product visualizers, and spatial physics simulations.
- **Engine Implementation:** Headless **Blender 4.x** driven by Python (`bpy`).
  - *Rasterizer Engine:* Blender **EEVEE Next** utilizing hardware Direct3D 11 on Intel Iris Xe graphics (1.2–2.5s/frame).
  - *Raytracing Engine:* Blender **Cycles CPU** utilizing Intel Embree and Open Image Denoise (OIDN) for photorealistic soft shadows and caustics (15–30s/frame).
  - *Asset Ecosystem:* Poly Haven, ambientCG, Smithsonian Open Access, and NASA 3D open CC0 models.

### 3.3 MODE C: Real Footage Production Core (`RealFootageAdapter`)
- **Domain Responsibilities:** Living wild animal behavior, authentic natural habitats, historical archives, real human documentaries, and verified b-roll.
- **Engine Implementation:**
  - *Commercial Free Tier:* **Pexels Video API** (20,000 free 1080p/4K downloads/month under Pexels License).
  - *Public Domain:* **Wikimedia Commons Official API** (Millions of CC0 and Public Domain scientific and documentary videos).
  - *Verification:* Computes SHA-256 hash on download, verifies valid video bitstream headers, and binds an immutable `.provenance.json` manifest.

---

## 4. HYBRID COMPOSITION: INTERSECTING MODES IN A SINGLE VIDEO

Master AI uniquely enables **multi-medium intersection within the same scene or timeline**:

```
SCENE 1: REAL FOOTAGE (Lions stalking prey across savanna)
   ↓ (1.0s Film Dissolve)
SCENE 2: TRUE 3D CGI (Blender 3D anatomical cutaway showing lion heart rate and muscle contraction)
   ↓ (0.8s Wipe Transition)
SCENE 3: 2D MOTION GRAPHICS (Lemo-Opuscar animated vector map showing historic vs present pride range)
   ↓ (1.0s Crossfade)
SCENE 4: HYBRID OVERLAY (Real footage of lion pride resting, overlaid with 2D kinetic telemetry and 3D terrain wireframe)
```

The **`HybridSceneComposer`** manages multi-layer compositing in FFmpeg, placing 2D motion graphics and telemetry overlays directly on top of 3D renders or real video footage with full alpha transparency.

---

## 5. REUSABLE COMPONENT ARCHITECTURE & INTERFACES

```python
class BaseVisualModeAdapter(ABC):
    """Universal interface for 2D, 3D, and Real Footage adapters."""

    @abstractmethod
    def generate_scene(
        self,
        scene_spec: Dict[str, Any],
        duration_sec: float,
        resolution: Tuple[int, int],
        fps: int,
        output_path: str
    ) -> SceneAssetResult:
        """Renders or acquires the video stream according to the specified mode."""
        pass

    @abstractmethod
    def verify_authenticity(self, asset_path: str) -> Dict[str, Any]:
        """Validates that the generated artifact matches its claimed medium and license."""
        pass
```

- **`TwoDAnimationAdapter`:** Validates resolution, frame rate, and vector smoothness.
- **`ThreeDCGIAdapter`:** Validates true geometric depth, virtual camera motion, and PBR lighting.
- **`RealFootageAdapter`:** Validates external URL origin, SHA-256 hash, and license attribution.
- **`AssetLicenseVerifier`:** Rejects any asset with non-commercial restrictions or unknown origins.
- **`UnifiedTimelineEngine`:** Compiles all scenes into a continuous, color-graded, audio-ducked master MP4.
