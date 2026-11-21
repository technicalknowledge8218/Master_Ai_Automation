"""
creative_decision_engine.py
===========================
Master AI - Creative Decision Engine (CDE)
(Phase 7.8 Directorial Intelligence Core)

Before rendering every scene or micro-exercise, the CDE generates an explicit,
executable Directorial Plan answering the 9 cardinal filmmaking questions:
1. What should the viewer see?
2. Which character or object deserves attention?
3. What camera angle/scale is appropriate?
4. Should the camera move or remain still (and with what easing curve)?
5. What should the character do (posture, eye motion, facial expression)?
6. When should the shot cut and with what transition grammar?
7. What sound design and Foley should accompany the action?
8. What emotion should the audience feel?
9. How does this scene visually and acoustic connect to the next?

The plan is output as an executable Python object and JSON EDL directly consumed
by the rendering pipeline.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional

@dataclass
class CameraDirective:
    scale: str  # "ECU", "CU", "MCU", "MS", "WS", "EWS"
    movement_type: str  # "static", "pan", "tilt", "dolly_in", "dolly_out", "dolly_zoom", "tracking"
    easing_curve: str  # "linear", "ease_in_quad", "ease_out_quad", "ease_in_out_cubic", "ease_out_back"
    start_pos: List[float] = field(default_factory=lambda: [0.0, 0.0])
    end_pos: List[float] = field(default_factory=lambda: [0.0, 0.0])
    start_zoom: float = 1.0
    end_zoom: float = 1.0
    damped_shake_intensity: float = 0.0  # Safe max <= 4.0 px at 6.0 Hz
    parallax_enabled: bool = True

@dataclass
class CharacterDirective:
    name: str
    primary_emotion: str  # "neutral", "curious", "tense", "urgent", "relieved", "amused"
    action_description: str
    involuntary_blinks: bool = True
    harmonic_breathing: bool = True
    breathing_amplitude_px: float = 2.0
    eye_saccade_target: List[float] = field(default_factory=lambda: [0.0, 0.0])
    lip_sync_active: bool = False
    vocal_envelope_stem: Optional[str] = None

@dataclass
class CutDirective:
    transition_type: str  # "hard_cut", "match_cut", "whip_pan", "crossfade", "j_cut", "l_cut"
    cut_frame: int
    motivating_reason: str
    audio_bridge_sec: float = 0.4  # L-cut / J-cut acoustic overlap
    match_feature: Optional[str] = None  # e.g. "circular_geometry", "directional_velocity"

@dataclass
class SoundDirective:
    ambient_environment: str
    music_movement: str
    spot_foley_events: List[Dict[str, Any]] = field(default_factory=list)
    vocal_sidechain_ducking_db: float = -14.0
    target_lufs: float = -23.0

@dataclass
class CreativeDirectionPlan:
    shot_id: str
    shot_name: str
    duration_sec: float
    fps: int
    frame_count: int
    viewer_focus: str
    primary_subject: str
    target_audience_emotion: str
    dramatic_beat: str
    connection_to_next: str
    camera: CameraDirective
    character: CharacterDirective
    cut: CutDirective
    sound: SoundDirective
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

class CreativeDecisionEngine:
    """
    Directorial Intelligence Core:
    Translates screenplay narrative beats into executable CreativeDirectionPlans.
    """
    @classmethod
    def create_plan(
        cls,
        shot_id: str,
        shot_name: str,
        duration_sec: float,
        viewer_focus: str,
        primary_subject: str,
        target_audience_emotion: str,
        dramatic_beat: str,
        connection_to_next: str,
        camera: CameraDirective,
        character: CharacterDirective,
        cut: CutDirective,
        sound: SoundDirective,
        fps: int = 24,
        notes: str = ""
    ) -> CreativeDirectionPlan:
        frame_count = int(round(duration_sec * fps))
        return CreativeDirectionPlan(
            shot_id=shot_id,
            shot_name=shot_name,
            duration_sec=duration_sec,
            fps=fps,
            frame_count=frame_count,
            viewer_focus=viewer_focus,
            primary_subject=primary_subject,
            target_audience_emotion=target_audience_emotion,
            dramatic_beat=dramatic_beat,
            connection_to_next=connection_to_next,
            camera=camera,
            character=character,
            cut=cut,
            sound=sound,
            notes=notes
        )

    @classmethod
    def validate_plan(cls, plan: CreativeDirectionPlan) -> List[str]:
        """Validates that directorial decisions obey professional filmmaking rules."""
        issues = []
        if plan.duration_sec <= 0:
            issues.append(f"Invalid duration: {plan.duration_sec}s")
            
        # Camera physics sanity check
        if plan.camera.damped_shake_intensity > 6.0:
            issues.append(f"Shake intensity {plan.camera.damped_shake_intensity} exceeds safe Nyquist threshold (max 6.0)")
            
        # Transition rule: crossfades only for major temporal/spatial jumps
        if plan.cut.transition_type == "crossfade" and "time_jump" not in plan.cut.motivating_reason.lower() and "outro" not in plan.cut.motivating_reason.lower():
            issues.append("Unmotivated crossfade: Crossfades should only be used for temporal jumps or contemplative chapter ends, not routine scene changes.")
            
        # Subject focus check
        if not plan.viewer_focus or len(plan.viewer_focus.strip()) < 5:
            issues.append("Missing viewer focus: Director must specify what the audience should look at.")
            
        return issues
