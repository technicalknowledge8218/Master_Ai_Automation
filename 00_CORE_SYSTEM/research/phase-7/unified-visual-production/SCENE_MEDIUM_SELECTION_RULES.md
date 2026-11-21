# SCENE MEDIUM SELECTION RULES & PLANNER ALGORITHM
## Decision Matrices, Heuristics, Medium Scoring Algorithms & Multi-Genre Workflows

**Document Version:** 1.0.0-unified-production  
**Project Root:** `F:\Master AI`  
**Target Path:** `00_CORE_SYSTEM\research\phase-7\unified-visual-production\SCENE_MEDIUM_SELECTION_RULES.md`  
**Classification:** Core Planning Algorithm & Decision Architecture  
**Status:** Approved Algorithmic Specification  

---

## 1. OBJECTIVE OF THE SCENE MEDIUM PLANNER

The `SceneMediumPlanner` is the intelligence layer within Master AI that prevents monolithic production mistakes. It evaluates each scene in the storyboard and deterministically assigns it to **Mode A (2D)**, **Mode B (3D CGI)**, **Mode C (Real Footage)**, or **Hybrid Composition**.

---

## 2. DECISION MATRIX: EVALUATING SCENE REQUIREMENTS

The planner scores candidate mediums across eight operational dimensions:

| Decision Factor | Mode A: 2D Animation / Motion Graphics | Mode B: True 3D CGI Animation | Mode C: Genuine Real Footage |
| :--- | :--- | :--- | :--- |
| **Primary Narrative Goal** | Conceptual clarity, data, typography, abstract rules | Spatial depth, mechanical disassembly, astronomical scale | Emotional empathy, authentic biological behavior, history |
| **Realism Expectation** | Stylized (Vector, Line Art, Infographic) | Geometric Realism (PBR Materials, Physics) | Absolute Optical Photorealism (Real Cameras) |
| **Subject Feasibility** | Math formulas, UI mockups, population charts | Planetary orbits, engine cutaways, anatomical skeletons | Living wildlife, natural weather, historical events |
| **Render Latency on Host**| **Fast:** 20–30 FPS (~1.5 min per 60s clip) | **Moderate:** 1.5–2.5s/frame (~3.5 min per 5s clip) | **Instant:** 5–15 seconds total download |
| **Hardware Demand** | Low CPU / RAM footprint (<2 GB) | Moderate (Intel Iris Xe Direct3D 11 / CPU) | Near-zero compute load (I/O network bound) |
| **Zero-Budget Asset Base**| Lemo-Opuscar styles, Manim Python, Glaxnimate | Poly Haven CC0, Smithsonian, NASA 3D | Pexels Video API (20k/mo), Wikimedia Commons |
| **Camera Freedom** | 2D Pan, Zoom, Multi-layer Parallax | Full 6-DOF Virtual Camera (Dolly, Orbit, Crane) | Pre-recorded camera moves (Curated selection) |
| **Licensing Risk** | Zero (MIT / GPL code) | Zero (CC0 3D models / GPL Blender) | Verified (Pexels License / CC0 Provenance) |

---

## 3. SELECTION ALGORITHM (`SceneMediumPlanner.py`)

```python
class SceneMediumPlanner:
    """Intelligently plans the visual medium for every storyboard act/scene."""

    def plan_scene_medium(self, scene_spec: Dict[str, Any], genre: str) -> str:
        intent = scene_spec.get("intent", "").lower()
        subject = scene_spec.get("subject", "").lower()

        # Rule 1: Mathematical, Statistical or Text-Heavy Scenes -> Mode A (2D)
        if any(k in intent for k in ["statistic", "percentage", "chart", "trend", "typography", "quote"]):
            return "MODE_A_2D_MOTION"

        # Rule 2: Maps, Geographic Ranges, Corridors -> Mode A (2D Vector Cartography)
        if any(k in intent for k in ["map", "territory_range", "migration_corridor", "border"]):
            return "MODE_A_2D_MAP"

        # Rule 3: Mechanical, Anatomical, Planetary, Spatial Simulation -> Mode B (3D CGI)
        if any(k in intent for k in ["cutaway", "anatomy", "orbit", "mechanical", "3d_space", "inside_the"]):
            return "MODE_B_3D_CGI"

        # Rule 4: Biological Wildlife Behavior, Living Nature -> Mode C (Real Footage)
        if genre.lower() == "wildlife_documentary":
            if any(k in subject for k in ["lion", "predator", "cubs", "hunt", "stalk", "pride"]):
                return "MODE_C_REAL_FOOTAGE"

        # Rule 5: Historical Archives -> Mode C (Public Domain Archives)
        if "historical_archive" in intent:
            return "MODE_C_REAL_FOOTAGE"

        # Rule 6: Overlay Telemetry or Split Scenes -> Hybrid
        if scene_spec.get("has_overlay_telemetry", False):
            return "HYBRID_REAL_AND_2D"

        # Default fallback based on genre
        if genre.lower() in ["science_explainer", "technology_review"]:
            return "MODE_B_3D_CGI"
        elif genre.lower() in ["business_explainer", "news_explainer"]:
            return "MODE_A_2D_MOTION"
        else:
            return "MODE_C_REAL_FOOTAGE"
```

---

## 4. CONCRETE GENRE BREAKDOWN EXAMPLES

### Example 1: 5-Minute Lion Wildlife Documentary (The Hybrid Sovereign Model)
- **Act 1: Dawn on the Savannah (50s):** `MODE_C_REAL_FOOTAGE` (Authentic 1080p Pexels video of lion on sunrise kopje) + `MODE_A_2D_MOTION` (OpenFilm kinetic title sequence).
- **Act 2: The Pride Social Bonds (50s):** `MODE_C_REAL_FOOTAGE` (Authentic Wikimedia CC0 footage of lionesses grooming cubs).
- **Act 3: The Silent Stalk & Hunt (50s):** `MODE_C_REAL_FOOTAGE` (Authentic 1080p footage of lionesses stalking through tall grass).
- **Act 4: Anatomy of the Apex Roar (50s):** `MODE_B_3D_CGI` (Blender 3D anatomical cutaway showing skull structure, vocal fold vibration, and soundwave physics).
- **Act 5: Territory & Historical Range (50s):** `MODE_A_2D_MAP` (Lemo-Opuscar animated vector map of Africa showing 90% habitat contraction over 100 years).
- **Act 6: Conservation & Modern Sanctuaries (50s):** `MODE_C_REAL_FOOTAGE` (Authentic footage of Gir National Park lions) + `MODE_A_2D_MOTION` (Closing credits and call-to-action).

### Example 2: Solar System Orbital Explainer (Mode B 3D Primary)
- **Primary Medium:** `MODE_B_3D_CGI` (Blender 3D NASA orbital models with true planetary lighting and smooth camera flythroughs).
- **Secondary Medium:** `MODE_A_2D_MOTION` (HUD telemetry overlays displaying orbital velocity, distance in AU, and mass comparisons).

### Example 3: SaaS Platform Explainer (Mode A 2D Primary)
- **Primary Medium:** `MODE_A_2D_MOTION` (Lemo-Opuscar `swiss-motion` and `dataviz` styles with smooth UI mockups, animated cursor clicks, and bold kinetic typography).
