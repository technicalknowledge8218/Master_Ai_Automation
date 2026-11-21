"""goal_decomposer.py
MASTER-AI Goal Interpretation & Task Decomposition Engine

Translates natural language user goals into structured Directed Acyclic Graph (DAG)
execution plans with agent assignments, dependency waves, resource estimates,
and validation criteria.
"""

import os
import sys
import uuid
import re
from typing import Dict, Any, List, Optional, Set, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

try:
    from .agent_registry import AgentRegistry
except ImportError:
    from agent_registry import AgentRegistry


class GoalDecomposer:
    """Interprets user intent and constructs executable DAG plans."""

    def __init__(self, registry: Optional[AgentRegistry] = None):
        self.registry = registry or AgentRegistry()

    def interpret_goal(self, goal_text: str) -> Dict[str, Any]:
        """Extracts intent, domain, language, deliverable format, and risk tier."""
        text_lower = goal_text.lower()

        # Target language extraction
        target_language = "English"
        if "hindi" in text_lower:
            target_language = "Hindi"
        elif "spanish" in text_lower:
            target_language = "Spanish"
        elif "french" in text_lower:
            target_language = "French"
        elif "german" in text_lower:
            target_language = "German"

        # Intent classification
        if any(w in text_lower for w in ["documentary", "video", "film", "production plan", "script"]):
            intent = "CONTENT_CREATION"
        elif any(w in text_lower for w in ["build", "implement", "develop", "code", "refactor"]):
            intent = "SOFTWARE_DEVELOPMENT"
        elif any(w in text_lower for w in ["audit", "vulnerability", "security check"]):
            intent = "SECURITY_AUDIT"
        elif any(w in text_lower for w in ["discover", "github", "find repo"]):
            intent = "DISCOVERY"
        elif any(w in text_lower for w in ["research", "investigate", "study"]):
            intent = "RESEARCH_AND_PLAN"
        else:
            intent = "GENERAL_EXECUTION"

        # Complexity determination
        word_count = len(goal_text.split())
        has_multi_step = any(w in text_lower for w in ["and", "then", "plan", "documentary", "full", "pipeline"])
        if has_multi_step or word_count > 8:
            complexity = "FULL_LIFECYCLE_FEDERATION"
        elif word_count > 4:
            complexity = "COMPLEX_PIPELINE"
        else:
            complexity = "MODERATE_SEQUENTIAL"

        # Genre and Topic extraction
        is_drama = any(w in text_lower for w in ["drama", "family", "emotional", "sad", "mystery", "suspense", "story", "twist", "chitti", "चिट्ठी", "letter"])
        genre = "FAMILY_DRAMA" if is_drama else ("WILDLIFE_DOCUMENTARY" if "lion" in text_lower else "DOCUMENTARY")

        title_match = re.search(r"['\"]([^'\"]+)['\"]", goal_text)
        if title_match:
            topic = title_match.group(1).strip()
        elif "lion" in text_lower:
            topic = "African Lion"
        else:
            topic_match = re.search(r"(?:about|on|for|research)\s+([a-zA-Z0-9\s]+?)(?:\s+in|\s+for|\s+and|\s+to|$)", goal_text, re.IGNORECASE)
            if topic_match:
                topic = topic_match.group(1).strip()
            else:
                topic = " आखिरी चिट्ठी" if is_drama else "African Lion"

        # Duration extraction
        dur_match = re.search(r"(\d+)[-\s]*(?:second|sec|s\b)", text_lower)
        target_duration_sec = int(dur_match.group(1)) if dur_match else 60

        is_cinematic = any(w in text_lower for w in ["cinematic", "video", "documentary", "film", "youtube", "render", "story", "drama"])

        return {
            "raw_goal": goal_text,
            "intent": intent,
            "genre": genre,
            "topic": topic,
            "target_language": target_language,
            "target_duration_sec": target_duration_sec,
            "is_cinematic": is_cinematic,
            "complexity": complexity,
            "zero_paid_cost": True
        }

    def create_execution_plan(
        self,
        goal_text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generates a complete, dependency-ordered execution plan."""
        analysis = self.interpret_goal(goal_text)
        plan_id = f"PLAN-{uuid.uuid4().hex[:8]}"

        subtasks = self._decompose_into_subtasks(plan_id, analysis, context or {})
        waves = self._build_dependency_waves(subtasks)

        # Estimate duration
        total_est_seconds = sum(t.get("timeout_seconds", 30) for t in subtasks)

        return {
            "plan_id": plan_id,
            "goal": goal_text,
            "analysis": analysis,
            "complexity": analysis["complexity"],
            "waves": waves,
            "subtasks": subtasks,
            "subtask_count": len(subtasks),
            "estimated_duration_sec": total_est_seconds,
            "estimated_cost_usd": 0.00,  # Sovereign local execution
            "requires_human_approval": False,  # Pure local plan defaults to approved unless sensitive triggers exist
            "approval_ticket_id": None
        }

    def _decompose_into_subtasks(
        self,
        plan_id: str,
        analysis: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decomposes analysis into specific ordered subtasks with dependencies."""
        intent = analysis["intent"]
        topic = analysis["topic"]
        lang = analysis["target_language"]
        genre = analysis.get("genre", "DOCUMENTARY")

        subtasks = []

        if intent == "CONTENT_CREATION":
            if analysis.get("is_cinematic", False):
                target_dur = analysis.get("target_duration_sec", 60)

                if genre == "FAMILY_DRAMA":
                    # -------------------------------------------------------------
                    # GENRE: FAMILY DRAMA / MYSTERY & SUSPENSE PRODUCTION DAG
                    # -------------------------------------------------------------
                    # Wave 1: Research Agent
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-01",
                        "title": f"Narrative Themes & Cultural Research: {topic}",
                        "description": f"Gather emotional themes, maternal sacrifice archetypes, psychological family dynamics, and dramatic narrative structure for {topic}.",
                        "assigned_agent": "AGT-001",
                        "priority": "HIGH",
                        "depends_on": [],
                        "inputs": {"topic": topic, "genre": "FAMILY_DRAMA", "scope": "comprehensive"},
                        "expected_outputs": ["research_dossier.json", "factual_citations.md"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })

                    # Wave 2: Scriptwriter & Security/Compliance Auditor
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-02",
                        "title": f"Dramatic Narration Script ({lang}) & Emotional Arc Calibration",
                        "description": f"Author duration-calibrated {lang} emotional drama script with sentence timestamps, twist reveal, Devanagari Hindi text, and Romanized guidance.",
                        "assigned_agent": "AGT-009",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-01"],
                        "inputs": {"target_duration_sec": target_dur, "language": lang, "genre": "FAMILY_DRAMA"},
                        "expected_outputs": [f"narration_script_{lang.lower()}.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-03",
                        "title": "Content Licensing & Storytelling Compliance Audit",
                        "description": "Pre-screen script, narrative claims, and emotional references for copyright safety and ethical storytelling.",
                        "assigned_agent": "AGT-006",
                        "priority": "MEDIUM",
                        "depends_on": [f"{plan_id}-ST-01"],
                        "inputs": {"compliance_standard": "creative_commons_fair_use"},
                        "expected_outputs": ["content_risk_audit.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 1
                    })

                    # Wave 3: Storyboard Director
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-04",
                        "title": "Visual Storyboard & Dramatic Scene Timeline Breakdown",
                        "description": f"Design 9-scene dramatic storyboard with exact durations and crossfade allocations summing to {target_dur}s.",
                        "assigned_agent": "AGT-010",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-02"],
                        "inputs": {"target_duration_sec": target_dur, "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["documentary_storyboard.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })

                    # Wave 4: Medium Planning & Asset Clearance
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-05",
                        "title": "Visual Medium Planning (2D, 3D, Real Footage)",
                        "description": "Intelligently classify each dramatic scene into 2D Motion Graphics, 3D CGI in Blender, or Real Footage based on narrative intent.",
                        "assigned_agent": "AGT-008",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-04"],
                        "inputs": {"genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["scene_medium_plan.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-06",
                        "title": "Open-Source CC0 Atmospheric Asset Discovery & Clearance",
                        "description": "Query local library and remote sources for CC0 atmospheric footage, vintage interior props, and PBR textures.",
                        "assigned_agent": "AGT-011",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05"],
                        "inputs": {"license_filter": "CC0_PUBLIC_DOMAIN", "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["asset_clearance_manifest.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })

                    # Wave 5: Production Execution (3D, 2D, Real Footage, Audio)
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-07",
                        "title": "3D CGI Scene Generation (Blender 5.2.4 LTS Antique Room & Desk)",
                        "description": "Render 3D CGI ancestral room, antique writing desk, and keepsake letterbox with cinematic lighting via Blender EEVEE.",
                        "assigned_agent": "AGT-003",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05", f"{plan_id}-ST-06"],
                        "inputs": {"engine": "BLENDER_5_2_EEVEE", "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["3d_scenes_manifest.json"],
                        "timeout_seconds": 120,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-08",
                        "title": "2D Vector Motion Graphics & Handwritten Letter Sequence",
                        "description": "Render 2D animated handwritten Hindi letter reveal sequence, memory timeline, and dramatic title cards.",
                        "assigned_agent": "AGT-003",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05"],
                        "inputs": {"resolution": "1280x720", "fps": 24, "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["2d_scenes_manifest.json"],
                        "timeout_seconds": 60,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-09",
                        "title": "Authentic Atmospheric Real Footage Conforming & Provenance",
                        "description": "Conform genuine camera recordings of weathered house, rain, and dusk with verified SHA256 sidecars.",
                        "assigned_agent": "AGT-011",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05", f"{plan_id}-ST-06"],
                        "inputs": {"reject_zoompan": True, "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["real_footage_manifest.json"],
                        "timeout_seconds": 45,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-10",
                        "title": "Melancholic Emotional Soundscape & Voice Narration Checkpoint",
                        "description": "Synthesize continuous minor-key emotional ambient soundscape and stage user voice recording handbook.",
                        "assigned_agent": "AGT-012",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-02"],
                        "inputs": {"genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["audio_manifest.json", "audio_checkpoint.json"],
                        "timeout_seconds": 45,
                        "retry_budget": 2
                    })

                    # Wave 6: Programmatic Timeline Assembly
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-11",
                        "title": "Programmatic Multi-Scene Timeline Assembly & Crossfading",
                        "description": "Assemble 9-scene continuous master video with 1.0s crossfades, audio ducking, and 720p H.264 mastering.",
                        "assigned_agent": "AGT-013",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-07", f"{plan_id}-ST-08", f"{plan_id}-ST-09", f"{plan_id}-ST-10"],
                        "inputs": {"transition_duration_sec": 1.0, "resolution": "1280x720", "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["master_timeline_assembly.json"],
                        "timeout_seconds": 90,
                        "retry_budget": 2
                    })

                    # Wave 7: Subtitling
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-12",
                        "title": "Synchronized Multilingual Subtitle Authoring",
                        "description": "Generate broadcast time-aligned SRT and ASS subtitle tracks from verified sentence timings.",
                        "assigned_agent": "AGT-014",
                        "priority": "MEDIUM",
                        "depends_on": [f"{plan_id}-ST-02", f"{plan_id}-ST-11"],
                        "inputs": {"language": lang, "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["subtitles_manifest.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })

                    # Wave 8: Media QA Gate
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-13",
                        "title": "Comprehensive Media Quality Assurance & Provenance Audit",
                        "description": "Perform full frame-by-frame decode check, freeze/black frame detection, audio continuity check, and license validation.",
                        "assigned_agent": "AGT-015",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-11", f"{plan_id}-ST-12"],
                        "inputs": {"max_silence_gap_sec": 2.0, "genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["final_media_qa_report.json"],
                        "timeout_seconds": 45,
                        "retry_budget": 1
                    })

                    # Wave 9: Packaging & Final Dossier
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-14",
                        "title": "Production Dossier & Final Deliverable Packaging",
                        "description": "Compile verified master video package, production handbook, contact sheet, and publication metadata.",
                        "assigned_agent": "AGT-008",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-13"],
                        "inputs": {"genre": "FAMILY_DRAMA"},
                        "expected_outputs": ["PRODUCTION_DOSSIER.json", "PUBLICATION_METADATA.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 1
                    })

                else:
                    # -------------------------------------------------------------
                    # GENRE: WILDLIFE DOCUMENTARY PRODUCTION DAG (Phase 7.3 baseline)
                    # -------------------------------------------------------------
                    # Wave 1: Research Agent
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-01",
                        "title": f"Scientific & Habitat Research: {topic}",
                        "description": f"Gather factual data, biological traits, pride behavior, ecological impact, and conservation status for {topic}.",
                        "assigned_agent": "AGT-001",
                        "priority": "HIGH",
                        "depends_on": [],
                        "inputs": {"topic": topic, "scope": "comprehensive"},
                        "expected_outputs": ["research_dossier.json", "factual_citations.md"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })

                    # Wave 2: Scriptwriter & Security/Compliance Auditor
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-02",
                        "title": f"Documentary Narration Script ({lang}) & Pacing Calibration",
                        "description": f"Author duration-calibrated {lang} voiceover script with sentence timestamps, Devanagari Hindi text, and Romanized guidance.",
                        "assigned_agent": "AGT-009",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-01"],
                        "inputs": {"target_duration_sec": target_dur, "language": lang},
                        "expected_outputs": [f"narration_script_{lang.lower()}.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-03",
                        "title": "Content Licensing & Educational Compliance Audit",
                        "description": "Pre-screen script, claims, and references for educational accuracy and copyright safety.",
                        "assigned_agent": "AGT-006",
                        "priority": "MEDIUM",
                        "depends_on": [f"{plan_id}-ST-01"],
                        "inputs": {"compliance_standard": "educational_fair_use"},
                        "expected_outputs": ["content_risk_audit.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 1
                    })
    
                    # Wave 3: Storyboard Director
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-04",
                        "title": "Visual Storyboard & Multi-Scene Timeline Breakdown",
                        "description": f"Design 9-scene visual storyboard with exact durations and crossfade allocations summing to {target_dur}s.",
                        "assigned_agent": "AGT-010",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-02"],
                        "inputs": {"target_duration_sec": target_dur},
                        "expected_outputs": ["documentary_storyboard.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
    
                    # Wave 4: Medium Planning & Asset Clearance
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-05",
                        "title": "Visual Medium Planning (2D, 3D, Real Footage)",
                        "description": "Intelligently classify each scene into 2D Motion Graphics, 3D CGI, or Real Footage based on narrative intent.",
                        "assigned_agent": "AGT-008",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-04"],
                        "inputs": {},
                        "expected_outputs": ["scene_medium_plan.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-06",
                        "title": "Open-Source CC0 Asset Discovery & Provenance Clearance",
                        "description": "Query local library and remote sources for CC0 HDRI, PBR textures, and authentic wildlife clips.",
                        "assigned_agent": "AGT-011",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05"],
                        "inputs": {"license_filter": "CC0_PUBLIC_DOMAIN"},
                        "expected_outputs": ["asset_clearance_manifest.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
    
                    # Wave 5: Production Execution (3D, 2D, Real Footage, Audio)
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-07",
                        "title": "3D CGI Scene Generation (Blender 5.2.4 LTS Rigged Character)",
                        "description": "Render 3D CGI hero character with skeletal armature, IK constraints, and savanna environment via Blender EEVEE.",
                        "assigned_agent": "AGT-003",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05", f"{plan_id}-ST-06"],
                        "inputs": {"engine": "BLENDER_5_2_EEVEE", "rig_required": True},
                        "expected_outputs": ["3d_scenes_manifest.json"],
                        "timeout_seconds": 120,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-08",
                        "title": "2D Vector Motion Graphics & Scientific Infographics",
                        "description": "Render broadcast 2D animated territory range map, apex biology infographic, and title cards.",
                        "assigned_agent": "AGT-003",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05"],
                        "inputs": {"resolution": "1280x720", "fps": 24},
                        "expected_outputs": ["2d_scenes_manifest.json"],
                        "timeout_seconds": 60,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-09",
                        "title": "Authentic Wildlife Real Footage Conforming & Provenance",
                        "description": "Conform genuine camera recordings with verified SHA256 sidecars (rejecting synthetic zoompan).",
                        "assigned_agent": "AGT-011",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-05", f"{plan_id}-ST-06"],
                        "inputs": {"reject_zoompan": True},
                        "expected_outputs": ["real_footage_manifest.json"],
                        "timeout_seconds": 45,
                        "retry_budget": 2
                    })
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-10",
                        "title": "Commercial-Safe Audio Soundscape & Voice Checkpoint",
                        "description": "Verify commercial audio clearance, synthesize procedural continuous soundscape, and stage user voice recording handbook.",
                        "assigned_agent": "AGT-012",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-02"],
                        "inputs": {"quarantine_edge_tts": True},
                        "expected_outputs": ["audio_manifest.json", "audio_checkpoint.json"],
                        "timeout_seconds": 45,
                        "retry_budget": 2
                    })
    
                    # Wave 6: Programmatic Timeline Assembly
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-11",
                        "title": "Programmatic Multi-Scene Timeline Assembly & Crossfading",
                        "description": "Assemble 9-scene continuous master video with 1.0s crossfades, audio ducking, and 720p H.264 mastering.",
                        "assigned_agent": "AGT-013",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-07", f"{plan_id}-ST-08", f"{plan_id}-ST-09", f"{plan_id}-ST-10"],
                        "inputs": {"transition_duration_sec": 1.0, "resolution": "1280x720"},
                        "expected_outputs": ["master_timeline_assembly.json"],
                        "timeout_seconds": 90,
                        "retry_budget": 2
                    })
    
                    # Wave 7: Subtitling
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-12",
                        "title": "Synchronized Multilingual Subtitle Authoring",
                        "description": "Generate broadcast time-aligned SRT and ASS subtitle tracks from verified sentence timings.",
                        "assigned_agent": "AGT-014",
                        "priority": "MEDIUM",
                        "depends_on": [f"{plan_id}-ST-02", f"{plan_id}-ST-11"],
                        "inputs": {"language": lang},
                        "expected_outputs": ["subtitles_manifest.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 2
                    })
    
                    # Wave 8: Media QA Gate
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-13",
                        "title": "Comprehensive Media Quality Assurance & Provenance Audit",
                        "description": "Perform full frame-by-frame decode check, freeze/black frame detection, audio continuity check, and license validation.",
                        "assigned_agent": "AGT-015",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-11", f"{plan_id}-ST-12"],
                        "inputs": {"max_silence_gap_sec": 2.0},
                        "expected_outputs": ["final_media_qa_report.json"],
                        "timeout_seconds": 45,
                        "retry_budget": 1
                    })
    
                    # Wave 9: Packaging & Final Dossier
                    subtasks.append({
                        "subtask_id": f"{plan_id}-ST-14",
                        "title": "Production Dossier & Final Deliverable Packaging",
                        "description": "Compile verified master video package, production handbook, contact sheet, and publication metadata.",
                        "assigned_agent": "AGT-008",
                        "priority": "HIGH",
                        "depends_on": [f"{plan_id}-ST-13"],
                        "inputs": {},
                        "expected_outputs": ["PRODUCTION_DOSSIER.json", "PUBLICATION_METADATA.json"],
                        "timeout_seconds": 30,
                        "retry_budget": 1
                    })
    
            else:
                # Standard textual planning subtasks
                subtasks.append({
                    "subtask_id": f"{plan_id}-ST-01",
                    "title": f"Scientific & Habitat Research: {topic}",
                    "description": f"Gather factual data, biological traits, pride behavior, ecological impact, and conservation status for {topic}.",
                    "assigned_agent": "AGT-001",
                    "priority": "HIGH",
                    "depends_on": [],
                    "inputs": {"topic": topic, "scope": "comprehensive"},
                    "expected_outputs": ["research_dossier.json", "factual_citations.md"],
                    "timeout_seconds": 30,
                    "retry_budget": 2
                })

                subtasks.append({
                    "subtask_id": f"{plan_id}-ST-02",
                    "title": f"Documentary Architecture & 5-Minute Storyboard",
                    "description": f"Design 4-act documentary pacing (300 seconds total), scene breakdown, visual cues, and audio soundscape.",
                    "assigned_agent": "AGT-002",
                    "priority": "HIGH",
                    "depends_on": [f"{plan_id}-ST-01"],
                    "inputs": {"target_duration_sec": 300, "act_count": 4},
                    "expected_outputs": ["documentary_storyboard.json", "scene_pacing_spec.md"],
                    "timeout_seconds": 30,
                    "retry_budget": 2
                })

                subtasks.append({
                    "subtask_id": f"{plan_id}-ST-03",
                    "title": "Storyboard Timing & Factual Verification",
                    "description": "Perform mathematical verification of scene timings (summing to 300s) and validate factual alignment.",
                    "assigned_agent": "AGT-004",
                    "priority": "MEDIUM",
                    "depends_on": [f"{plan_id}-ST-02"],
                    "inputs": {"required_duration_sec": 300},
                    "expected_outputs": ["timing_validation_report.json"],
                    "timeout_seconds": 30,
                    "retry_budget": 2
                })

                subtasks.append({
                    "subtask_id": f"{plan_id}-ST-04",
                    "title": "Content Compliance & Licensing Audit",
                    "description": "Verify educational compliance, copyright safety of proposed references, and content appropriateness.",
                    "assigned_agent": "AGT-006",
                    "priority": "MEDIUM",
                    "depends_on": [f"{plan_id}-ST-01", f"{plan_id}-ST-02"],
                    "inputs": {"compliance_standard": "educational_fair_use"},
                    "expected_outputs": ["content_risk_audit.json"],
                    "timeout_seconds": 30,
                    "retry_budget": 1
                })

                subtasks.append({
                    "subtask_id": f"{plan_id}-ST-05",
                    "title": f"Production Plan & {lang} Narration Script",
                    "description": f"Compile comprehensive production handbook with complete {lang} voiceover script (Devanagari & Romanized), director cues, and audio-visual cues.",
                    "assigned_agent": "AGT-005",
                    "priority": "HIGH",
                    "depends_on": [f"{plan_id}-ST-03", f"{plan_id}-ST-04"],
                    "inputs": {"target_language": lang, "include_transliteration": True},
                    "expected_outputs": [f"documentary_production_plan_{lang.lower()}.md", "narration_script.json"],
                    "timeout_seconds": 45,
                    "retry_budget": 2
                })

        elif intent == "SOFTWARE_DEVELOPMENT":
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-01",
                "title": f"Architecture Specification & API Design",
                "description": f"Design modular specifications, data contracts, and architectural blueprint for {topic}.",
                "assigned_agent": "AGT-002",
                "priority": "HIGH",
                "depends_on": [],
                "inputs": {"topic": topic},
                "expected_outputs": ["system_architecture_spec.json", "ADR-001.md"],
                "timeout_seconds": 30,
                "retry_budget": 2
            })
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-02",
                "title": f"Implementation: {topic}",
                "description": f"Write pure-Python implementation code strictly adhering to architectural specification.",
                "assigned_agent": "AGT-003",
                "priority": "HIGH",
                "depends_on": [f"{plan_id}-ST-01"],
                "inputs": {},
                "expected_outputs": ["service.py"],
                "timeout_seconds": 60,
                "retry_budget": 2
            })
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-03",
                "title": "Unit & Integration Test Suite",
                "description": "Author exhaustive tests covering positive and negative edge cases.",
                "assigned_agent": "AGT-004",
                "priority": "HIGH",
                "depends_on": [f"{plan_id}-ST-02"],
                "inputs": {},
                "expected_outputs": ["test_service.py", "test_report.json"],
                "timeout_seconds": 45,
                "retry_budget": 2
            })
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-04",
                "title": "Security & Static Analysis Audit",
                "description": "Audit implementation against secret leaks, AST risks, and unpinned dependencies.",
                "assigned_agent": "AGT-006",
                "priority": "HIGH",
                "depends_on": [f"{plan_id}-ST-02", f"{plan_id}-ST-03"],
                "inputs": {},
                "expected_outputs": ["security_audit_report.json"],
                "timeout_seconds": 30,
                "retry_budget": 1
            })
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-05",
                "title": "Technical Documentation & Runbook",
                "description": "Author API reference, quick-start guide, and operational runbook.",
                "assigned_agent": "AGT-005",
                "priority": "MEDIUM",
                "depends_on": [f"{plan_id}-ST-04"],
                "inputs": {},
                "expected_outputs": ["README.md", "RUNBOOK.md"],
                "timeout_seconds": 30,
                "retry_budget": 1
            })

        else:
            # Default General Execution Pipeline
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-01",
                "title": f"Initial Research: {topic}",
                "description": f"Gather research data and relevant technical references for {topic}.",
                "assigned_agent": "AGT-001",
                "priority": "HIGH",
                "depends_on": [],
                "inputs": {"topic": topic},
                "expected_outputs": ["research_summary.md"],
                "timeout_seconds": 30,
                "retry_budget": 2
            })
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-02",
                "title": f"Execution & Solution Design",
                "description": "Structure technical findings and formulate execution steps.",
                "assigned_agent": "AGT-002",
                "priority": "MEDIUM",
                "depends_on": [f"{plan_id}-ST-01"],
                "inputs": {},
                "expected_outputs": ["execution_blueprint.json"],
                "timeout_seconds": 30,
                "retry_budget": 2
            })
            subtasks.append({
                "subtask_id": f"{plan_id}-ST-03",
                "title": "Final Documentation & Verification",
                "description": "Synthesize final deliverable document.",
                "assigned_agent": "AGT-005",
                "priority": "MEDIUM",
                "depends_on": [f"{plan_id}-ST-02"],
                "inputs": {},
                "expected_outputs": ["final_deliverable.md"],
                "timeout_seconds": 30,
                "retry_budget": 1
            })

        return subtasks

    def _build_dependency_waves(self, subtasks: List[Dict[str, Any]]) -> List[List[str]]:
        """Groups subtask IDs into sequential execution waves based on DAG dependencies."""
        completed_ids: Set[str] = set()
        remaining = list(subtasks)
        waves = []

        while remaining:
            current_wave = []
            for st in remaining:
                deps = set(st.get("depends_on", []))
                if deps.issubset(completed_ids):
                    current_wave.append(st)

            if not current_wave:
                # Cycle or unresolved dependency detected: break cycle by taking the first remaining
                current_wave = [remaining[0]]

            wave_ids = [st["subtask_id"] for st in current_wave]
            waves.append(wave_ids)
            completed_ids.update(wave_ids)
            remaining = [st for st in remaining if st["subtask_id"] not in completed_ids]

        return waves
