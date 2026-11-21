# MASTER AI: STRICT VISUAL STYLE LOCK SYSTEM
**Target Output**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.14\visual_style_lock_system.md`  
**Date**: 2026-11-18  

---

## 1. The Core Policy: Zero Accidental Style Mixing

> **MANDATORY DIRECTIVE**: Every Master AI production MUST select and lock exactly **ONE coherent visual style** before asset generation begins.
> 
> Under NO circumstances may asset generators mix flat 2D cartoon characters with photorealistic video footage, nor mix realistic human footage with cartoon vector backgrounds, unless an explicit artistic hybrid pipeline (e.g. *Who Framed Roger Rabbit* style with realistic drop shadows, cast lighting, and optical matching) is documented, tested, and approved in advance by the Creative Director.

---

## 2. The Five Authorized Master AI Visual Style Presets

Every production manifest must explicitly set `visual_style_preset` to one of the following:

### PRESET 1: `STYLE_VECTOR_EDITORIAL` (Kurzgesagt / Vox Explainer Style)
- **Visual Medium**: 100% 2D flat vector illustrations, clean lines (3–5px stroke weight), geometric forms.
- **Characters**: Stylized, expressive vector humans with clean silhouettes and consistent anatomical proportion.
- **Backgrounds**: Illustrated 2D vector environments (e.g. cozy room, urban street, server rack) matching character art.
- **Lighting**: Cel-shaded highlights and flat shadow planes. Zero photographic blur.
- **Target Best For**: Tech explainers, satirical stories, philosophical insights, relatable modern comedy.

### PRESET 2: `STYLE_TECH_SCREENCAST_MOTION` (Ref 01 Style)
- **Visual Medium**: 100% high-definition digital interfaces, code editors, terminal windows, and interactive UI cards.
- **Characters**: Optional voiceover-only narrator OR floating stylized avatar pill in the top corner.
- **Backgrounds**: Dark-mode `#0F172A` or High-key `#F8FAFC` clean workspace with subtle geometric grid lines.
- **Lighting**: Interface glow, illuminated syntax colors, soft Gaussian card drop shadows.
- **Target Best For**: Developer productivity, open-source repos, automation tutorials, tech tips.

### PRESET 3: `STYLE_KINETIC_INFOGRAPHIC` (Ref 04 Style)
- **Visual Medium**: Premium editorial typography, paper texture overlays, animated charts, and tactile document cards.
- **Characters**: None (Typography and graphic diagrams drive 100% of the narrative).
- **Backgrounds**: Chapter-based soft pastel color palettes (Ice Blue $\to$ Sage Green $\to$ Lilac $\to$ Warm Amber).
- **Lighting**: Soft ambient diffused illumination across flat paper layers.
- **Target Best For**: Business frameworks, productivity breakdowns, educational summaries.

### PRESET 4: `STYLE_CINEMATIC_REALISM` (100% Live-Action / Documentary)
- **Visual Medium**: 100% photorealistic video footage.
- **Characters**: Real human actors in recorded video or photorealistic AI video clips.
- **Backgrounds**: Authentic real-world locations (streets, cafes, offices, landscapes).
- **Lighting**: Natural optical lighting, volumetric haze, real depth-of-field focal blur.
- **Prohibition**: ZERO flat 2D cartoon characters or primitive SVG shapes permitted in the video track!

### PRESET 5: `STYLE_CEL_ANIME` (Studio Ghibli / Makoto Shinkai 2D Aesthetic)
- **Visual Medium**: 100% hand-drawn anime aesthetic.
- **Characters**: Detailed cel-shaded anime character models with painted hair highlights and expressive eyes.
- **Backgrounds**: Painterly, watercolor or gouache-textured 2D backgrounds.
- **Lighting**: Warm sunlight rays, bloom flares, painterly dusk/dawn tones.
- **Prohibition**: ZERO raw photorealistic camera footage permitted.

---

## 3. Automated Preflight Style Validator (`visual_style_validator.py`)

To ensure this policy cannot be bypassed by automated scripts, the Orchestrator runs an automated compatibility check before rendering:

```python
def validate_style_lock(manifest: dict) -> bool:
    style = manifest.get("visual_style_preset")
    if not style:
        raise ValueError("FATAL: Production manifest must specify a 'visual_style_preset'.")
        
    char_type = manifest.get("character_asset_type") # e.g. 'vector_2d', 'live_actor', 'none'
    bg_type = manifest.get("background_asset_type")   # e.g. 'vector_2d_env', 'live_video_footage', 'paper_ui'
    
    # FORBIDDEN COMBINATION: Flat 2D vector character + Live-action moving video
    if char_type == "vector_2d" and bg_type == "live_video_footage":
        raise StyleCollisionError(
            "VIOLATION: Attempted to combine 2D vector character with photorealistic live video footage! "
            "Every production must commit to ONE coherent visual reality. Use 'vector_2d_env' instead."
        )
    return True
```
