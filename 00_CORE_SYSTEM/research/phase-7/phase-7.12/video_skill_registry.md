# MASTER AI: REUSABLE VIDEO PRODUCTION SKILL REGISTRY
**Target Directory**: `F:\Master AI\00_CORE_SYSTEM\skills\video-production\`  
**Target Registry Doc**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.12\video_skill_registry.md`  
**Date**: 2026-11-18  

---

## 1. Registry Architecture & Discovery Protocol

The Master AI Skill Registry indexes all modular production skills. Each skill is packaged in a dedicated subdirectory containing:
- `SKILL.md`: Metadata (name, description, version, publisher), execution workflow, available tools, prompting techniques, quality gates, and failure recovery.
- Optional scripts, templates, and schemas.

The central Orchestrator discovers skills dynamically by reading `F:\Master AI\00_CORE_SYSTEM\skills\video-production\*\SKILL.md`.

---

## 2. Master Index of Registered Video Production Skills

| Skill ID | Subdirectory | Primary Purpose | Key Tools Utilized | Quality Metric |
| :--- | :--- | :--- | :--- | :--- |
| `creative-direction` | `skills/video-production/creative-direction/` | Directorial vision, genre definition, audience hook | LLM Directorial Logic | Clear logline & tone board |
| `story-writing` | `skills/video-production/story-writing/` | 4-act narrative arc formulation & scene conflict | Screenplay Validator | Narrative tension score |
| `dialogue-writing` | `skills/video-production/dialogue-writing/` | Conversational Hindi/Hinglish dialogues & pacing | Speech Rhythm Estimator | Turn latency $\le 0.35$s |
| `visual-research` | `skills/video-production/visual-research/` | Topic research, factual verification, trend analysis | Web Search, Wiki APIs | Grounded reference dossier |
| `reference-analysis` | `skills/video-production/reference-analysis/` | Reverse-engineering reference videos & editing grammar| `yt-dlp`, OpenCV, FFprobe | Frame-accurate ASL & style rules |
| `character-design` | `skills/video-production/character-design/` | Model sheets, facial expressions, OpenBone rigs | OpenBone, SVG Rig Builder | Visual uniqueness & consistency |
| `storyboard` | `skills/video-production/storyboard/` | 9:16 vertical panel blueprint & shot composition | Storyboard Generator | Visual diversity across panels |
| `cinematography` | `skills/video-production/cinematography/` | Camera kinematics, lenses, angles, safe zones | Virtual Camera Engine | Dynamic motion without jitter |
| `visual-generation` | `skills/video-production/visual-generation/` | B-roll video harvesting & background synthesis | Stock API, Fal.ai, ComfyUI | 1080p crispness, 0 artifacts |
| `character-animation`| `skills/video-production/character-animation/` | Skeletal mesh deformation & lip-sync acting | OpenBone, LipSync Engine | Natural gestures & viseme sync |
| `video-editing` | `skills/video-production/video-editing/` | NLE multi-track assembly, J/L-cuts, transitions | FFmpeg libx264, Remotion | Zero dropped frames, CFR 30fps |
| `voice-direction` | `skills/video-production/voice-direction/` | Neural voice acting, prosody & pitch modulation | Edge-TTS, Piper-TTS | Natural human prosody |
| `sound-design` | `skills/video-production/sound-design/` | Multi-movement score, Foley SFX, sidechain ducking | NumPy Synth, FFmpeg Audio | True Peak $\le -2.5$, RMS $-18\pm2$ |
| `color-grading` | `skills/video-production/color-grading/` | 9:16 color palettes, chapter grading, LUTs | OpenCV, Color Matrix | WCAG AAA contrast ratio |
| `quality-review` | `skills/video-production/quality-review/` | Independent creative & technical gatekeeping | Forensic QA Suite | Minimum 8/10 across all gates |
| `performance-optimization`| `skills/video-production/performance-optimization/`| Fast rendering, QuickSync acceleration, memory mgmt | Intel QSV, Pipe Streaming | Render speed $\ge 30$ FPS |

---

## 3. Dynamic Skill Loading Protocol

When an agent is assigned a task (e.g. `cinematography`), the Orchestrator executes:
```python
def load_production_skill(skill_id: str) -> str:
    skill_path = os.path.join(SKILLS_ROOT, skill_id, "SKILL.md")
    if not os.path.exists(skill_path):
        raise FileNotFoundError(f"Skill '{skill_id}' not found at {skill_path}")
    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()
```
The content is injected directly into the agent's task context, guaranteeing that the agent follows tested directorial grammar rather than improvising generic solutions.
