"""
editing_director.py
===================
Master AI - Autonomous Cinematic Editing & Directorial Decision Engine
Analyzes narrative screenplay beats, selects optimal shot types,
determines motivated cuts and transitions, configures camera motion paths,
and plans J/L audio cuts.
"""

import json
from typing import List, Dict, Any

class ShotType:
    WIDE_ESTABLISHING = "WIDE_ESTABLISHING"
    MEDIUM_SHOT = "MEDIUM_SHOT"
    MEDIUM_CLOSE_UP = "MEDIUM_CLOSE_UP"
    CLOSE_UP = "CLOSE_UP"
    EXTREME_CLOSE_UP = "EXTREME_CLOSE_UP"
    POV = "POV"
    LOW_ANGLE_TRACKING = "LOW_ANGLE_TRACKING"
    INSERT_DETAIL = "INSERT_DETAIL"

class TransitionType:
    HARD_CUT = "HARD_CUT"
    MATCH_CUT = "MATCH_CUT"
    WHIP_PAN = "WHIP_PAN"
    PUSH_LEFT = "PUSH_LEFT"
    CROSSFADE = "CROSSFADE"
    ZOOM_CUT = "ZOOM_CUT"

class EditingDirector:
    """
    Directorial AI supervisor that takes dramatic script beats and formulates
    cinematic shot composition, camera choreography, and transition grammar.
    """
    
    GRAMMAR_RULES = {
        "URGENT_HOOK": {
            "preferred_shot": ShotType.EXTREME_CLOSE_UP,
            "camera_move": "DOLLY_IN_EASE_OUT",
            "incoming_cut": TransitionType.HARD_CUT,
            "pacing": "FAST",
            "vfx": ["IMPACT_VIBRATION", "SCREEN_GLOW"]
        },
        "ACTION_PREP": {
            "preferred_shot": ShotType.MEDIUM_SHOT,
            "camera_move": "PAN_RIGHT_SMOOTH",
            "incoming_cut": TransitionType.MATCH_CUT,
            "pacing": "DYNAMIC",
            "vfx": ["EMBER_PARTICLES", "WOK_STEAM"]
        },
        "KINETIC_LAUNCH": {
            "preferred_shot": ShotType.LOW_ANGLE_TRACKING,
            "camera_move": "TRACKING_PARALLAX_FAST",
            "incoming_cut": TransitionType.WHIP_PAN,
            "pacing": "HIGH_SPEED",
            "vfx": ["RAIN_STREAKS", "WHEEL_SPRAY", "NEON_BLUR"]
        },
        "FOCUSED_TENSION": {
            "preferred_shot": ShotType.POV,
            "camera_move": "CAMERA_SHAKE_SUBTLE",
            "incoming_cut": TransitionType.HARD_CUT,
            "pacing": "TENSE",
            "vfx": ["VISOR_WATER_DROPLETS", "EYE_TRACKING", "TRAFFIC_LIGHTS"]
        },
        "COUNTDOWN_RACE": {
            "preferred_shot": ShotType.INSERT_DETAIL,
            "camera_move": "DOLLY_ZOOM_VERTIGO",
            "incoming_cut": TransitionType.MATCH_CUT,
            "pacing": "CLIMACTIC",
            "vfx": ["PUDDLE_REFLECTION_SPLASH", "TIMER_PULSE"]
        },
        "ARRIVAL_RELIEF": {
            "preferred_shot": ShotType.WIDE_ESTABLISHING,
            "camera_move": "DECELERATION_STOP",
            "incoming_cut": TransitionType.HARD_CUT,
            "pacing": "SUDDEN_CALM",
            "vfx": ["MIST_FOG", "LAMPOST_HALO", "ENGINE_STEAM"]
        },
        "EMOTIONAL_REVEAL": {
            "preferred_shot": ShotType.MEDIUM_CLOSE_UP,
            "camera_move": "SLOW_PUSH_IN_CUBIC",
            "incoming_cut": TransitionType.HARD_CUT,
            "pacing": "TENDER",
            "vfx": ["CANDLE_GLOW_WARMTH", "EYE_BLINK_TEAR"]
        },
        "TRIUMPH_OUTRO": {
            "preferred_shot": ShotType.MEDIUM_SHOT,
            "camera_move": "PULL_BACK_EASE_OUT",
            "incoming_cut": TransitionType.CROSSFADE,
            "pacing": "WARM_CLOSING",
            "vfx": ["RAIN_GLISTEN", "TITLE_CARD_DISSOLVE"]
        }
    }

    @classmethod
    def plan_film(cls, screenplay_beats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes screenplay beats into a complete editing decision manifest.
        """
        decisions = []
        accumulated_time = 0.0

        for idx, beat in enumerate(screenplay_beats, start=1):
            intent = beat.get("dramatic_intent", "URGENT_HOOK")
            rule = cls.GRAMMAR_RULES.get(intent, cls.GRAMMAR_RULES["URGENT_HOOK"])
            
            dur = beat.get("duration_sec", 7.5)
            start_t = accumulated_time
            end_t = start_t + dur
            accumulated_time = end_t
            
            decision = {
                "beat_number": idx,
                "scene_id": beat.get("scene_id", f"scene_{idx:02d}"),
                "title": beat.get("title", f"Beat {idx}"),
                "timing": {
                    "start_sec": round(start_t, 2),
                    "end_sec": round(end_t, 2),
                    "duration_sec": round(dur, 2),
                    "frames_24fps": int(dur * 24)
                },
                "dramatic_intent": intent,
                "cinematography": {
                    "shot_type": rule["preferred_shot"],
                    "camera_movement": rule["camera_move"],
                    "cut_transition": rule["incoming_cut"] if idx > 1 else "START_OF_FILM",
                    "pacing_style": rule["pacing"]
                },
                "motion_and_vfx": {
                    "character_action": beat.get("action", ""),
                    "active_vfx": rule["vfx"],
                    "eyelid_behavior": beat.get("eyelid_behavior", "NATURAL_BLINKS"),
                    "lip_sync_target": beat.get("speaker", "NONE")
                },
                "audio_design": {
                    "dialogue_text": beat.get("dialogue", ""),
                    "speaker": beat.get("speaker", ""),
                    "music_movement": beat.get("music_theme", ""),
                    "foley_cues": beat.get("foley", [])
                }
            }
            decisions.append(decision)
            
        return {
            "film_title": screenplay_beats[0].get("film_title", "Untitled Short"),
            "target_runtime_sec": round(accumulated_time, 2),
            "target_fps": 24,
            "scene_count": len(decisions),
            "scenes": decisions
        }
