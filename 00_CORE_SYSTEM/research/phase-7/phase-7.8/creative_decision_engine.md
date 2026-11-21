# MASTER AI — CREATIVE DECISION ENGINE (CDE) SPECIFICATION
## Pre-Render Directorial Intelligence & Executable Decision Architecture

**Project Root**: `F:\Master AI`  
**Workspace**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.8\`  
**Engine Module**: [`09_CONTENT_STUDIO/engine/creative_decision_engine.py`](file:///F:/Master%20AI/09_CONTENT_STUDIO/engine/creative_decision_engine.py)  
**Date**: November 18, 2026  

---

### 1. Purpose & Architectural Mandate

In previous iterations of Master AI, the rendering loop began directly with visual generation: an SVG string was formatted and pushed down a pipe without any preceding directorial reasoning. Consequently:
- Shots lacked intentional focal points.
- Camera moves were arbitrarily assigned without narrative justification.
- Transitions defaulted to lazy, unmotivated crossfades.
- Character faces remained rigid because the renderer had no emotional instruction.

The **Creative Decision Engine (CDE)** acts as the **internal Film Director** of Master AI. Before any frame is calculated, the CDE synthesizes the screenplay beats into an explicit, executable `CreativeDirectionPlan` answering the 9 cardinal filmmaking questions:

```
                          NARRATIVE SCREENPLAY BEAT
                                     |
                                     v
                 +---------------------------------------+
                 |       CREATIVE DECISION ENGINE        |
                 |      (Directorial Reasoning Core)     |
                 +-------------------+-------------------+
                                     |
    +--------------------------------+--------------------------------+
    |                                                                 |
    v                                                                 v
1. What should the viewer see?                    6. When should the shot cut & why?
2. Which subject commands attention?              7. What sound & Foley accompanies?
3. What camera angle & scale?                     8. What emotion should audience feel?
4. How should camera move (easing)?               9. How does shot connect to next?
5. What does the character do (acting)?
                                     |
                                     v
                 +---------------------------------------+
                 |       CREATIVE DIRECTION PLAN         |
                 |       (Executable JSON / Object)      |
                 +-------------------+-------------------+
                                     |
                                     v
                 +---------------------------------------+
                 |    ZERO-DEFECT RENDERER & AUDIO MIX   |
                 |  (Strict 1920x1080, Stride Assertion) |
                 +---------------------------------------+
```

---

### 2. The 9 Cardinal Directorial Questions & Schema

Every `CreativeDirectionPlan` codifies the 9 decisions into four strongly typed sub-directives:

#### A. Focal Hierarchy & Viewer Attention
- **`viewer_focus`**: Explicitly states what optical element the human eye must register first (e.g., *"Aryan's anxious eye reflection across the rain-streaked visor"*).
- **`primary_subject`**: The anchored visual entity (Character, Vehicle, Digital HUD, Prop).
- **`target_audience_emotion`**: The intended psychological reaction (e.g., *"visceral urgency"*, *"curiosity"*, *"deadpan amusement"*, *"cathartic relief"*).

#### B. Camera Language & Optical Physics (`CameraDirective`)
- **`scale`**: `ECU` (Extreme Close-Up), `CU` (Close-Up), `MCU` (Medium Close-Up), `MS` (Medium Shot), `WS` (Wide Shot), `EWS` (Extreme Wide Shot).
- **`movement_type`**: `static`, `pan`, `tilt`, `dolly_in`, `dolly_out`, `dolly_zoom`, `tracking`.
- **`easing_curve`**: `ease_in_out_cubic`, `ease_out_back`, `ease_out_quad`, `linear`.
- **`damped_shake_intensity`**: Clamped to $\le 4.0\text{ px}$ at $6.0\text{ Hz}$ to prevent Nyquist aliasing.
- **`parallax_enabled`**: Boolean enabling 4-layer optical depth projection.

#### C. Character Acting & Micro-Vitality (`CharacterDirective`)
- **`primary_emotion`**: Informs facial expression geometry (eyebrow angle, eye aperture).
- **`action_description`**: The physical blocking and posture.
- **`involuntary_blinks`**: Enables Poisson-distributed eyelid blinks every 2.8s–4.1s.
- **`harmonic_breathing`**: Enables 0.35 Hz harmonic chest/shoulder sway ($\pm 2.0\text{ px}$).
- **`lip_sync_active`**: Controls 4-viseme mouth modulation driven by audio vocal envelope.

#### D. Motivated Editorial Grammar (`CutDirective`)
- **`transition_type`**: `hard_cut`, `match_cut`, `whip_pan`, `crossfade`, `j_cut`, `l_cut`.
- **`cut_frame`**: Frame-accurate transition point.
- **`motivating_reason`**: Explicit justification for the cut (e.g., *"Hard cut on engine rev transient to accelerate action tempo"*).
- **`audio_bridge_sec`**: 0.3s to 0.6s L/J-cut acoustic overlap for seamless continuity.

#### E. Acoustic Environment & Foley (`SoundDirective`)
- **`ambient_environment`**: Realistic soundscape (e.g., *"heavy Mumbai rain on asphalt, distant thunder"*).
- **`spot_foley_events`**: Frame-synchronized sound events (helmet click, wok sizzle, motor whine, brake squeal).
- **`vocal_sidechain_ducking_db`**: Automated $-14\text{ dB}$ attenuation on music and ambient stems during dialogue.

---

### 3. Example Executable JSON Output

```json
{
  "shot_id": "shot_01",
  "shot_name": "The Ticking Visor",
  "duration_sec": 5.0,
  "fps": 24,
  "frame_count": 120,
  "viewer_focus": "Aryan's eyes reflecting red countdown timer through rain-slicked helmet visor",
  "primary_subject": "Aryan (Courier)",
  "target_audience_emotion": "tension and claustrophobic urgency",
  "dramatic_beat": "Inciting Incident: Aryan realizes this delivery has an unforgiving 10-minute timer",
  "connection_to_next": "Eye reflection match-cuts directly into the circular smartphone dispatch display",
  "camera": {
    "scale": "ECU",
    "movement_type": "dolly_in",
    "easing_curve": "ease_in_out_cubic",
    "start_zoom": 1.0,
    "end_zoom": 1.25,
    "damped_shake_intensity": 1.5,
    "parallax_enabled": true
  },
  "character": {
    "name": "Aryan",
    "primary_emotion": "tense",
    "action_description": "Breathing heavily inside helmet, pupils darting to GPS HUD",
    "involuntary_blinks": true,
    "harmonic_breathing": true,
    "breathing_amplitude_px": 2.0,
    "lip_sync_active": true
  },
  "cut": {
    "transition_type": "match_cut",
    "cut_frame": 120,
    "motivating_reason": "Geometric match on pupil reflection to round smartphone screen",
    "audio_bridge_sec": 0.4,
    "match_feature": "circular_geometry"
  },
  "sound": {
    "ambient_environment": "heavy_rain_mumbai_night",
    "spot_foley_events": [
      {"frame": 12, "name": "visor_snap_click"},
      {"frame": 48, "name": "hud_countdown_alarm_beep"}
    ],
    "music_movement": "electronic_synth_pulse_128bpm",
    "vocal_sidechain_ducking_db": -14.0,
    "target_lufs": -23.0
  }
}
```

---

### 4. Directorial Validation Gate

The CDE includes an automated `validate_plan()` gate:
- Rejects unmotivated crossfades unless justified by a temporal/spatial chapter jump.
- Rejects camera shake $> 6.0\text{ px}$ to protect against Nyquist sampling aliasing.
- Rejects shots with undefined viewer focus or ambiguous character objectives.
- Ensures every shot has a documented continuity bridge to the next scene.
