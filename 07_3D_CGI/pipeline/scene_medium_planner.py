"""
Master AI - Phase 7.2 Scene Medium Planner
Intelligently assigns the optimal production medium (Real Footage, 3D CGI, 2D Motion Graphics)
to each scene in a documentary storyboard based on narrative intent, visual requirements,
and technical viability.
"""

from typing import Dict, Any, List

class SceneMediumPlanner:
    """Decides optimal visual production medium for each scene."""

    MEDIUM_REAL_FOOTAGE = "REAL_WILDLIFE_FOOTAGE"
    MEDIUM_3D_CGI = "3D_CGI_ANIMATION"
    MEDIUM_2D_MOTION = "2D_MOTION_GRAPHICS"

    def plan_scene_medium(self, scene_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze narrative goals and return medium decision with justification.
        """
        genre = scene_spec.get("genre", "documentary")
        intent = scene_spec.get("intent", "").lower()
        subject = scene_spec.get("subject", "").lower()

        # Decision Logic:
        if any(kw in intent for kw in ["map", "territory", "statistics", "data", "bite force", "speed", "taxonomy", "infographic"]):
            medium = self.MEDIUM_2D_MOTION
            reason = "Abstract spatial, statistical, or anatomical metrics are best communicated via kinetic vector typography and infographics."
            suggested_transition = "wipeleft"
        elif any(kw in intent for kw in ["hero", "establishing", "cgi", "anatomical model", "sunrise environment", "3d camera"]):
            medium = self.MEDIUM_3D_CGI
            reason = "Cinematic camera choreography, dynamic atmospheric lighting, and close-up procedural anatomical fidelity require 3D CGI rasterization."
            suggested_transition = "fade"
        elif any(kw in intent for kw in ["real", "wildlife", "hunting", "pride life", "actual behavior", "photographic"]):
            medium = self.MEDIUM_REAL_FOOTAGE
            reason = "Live-action behavioral authenticity and un-stylized wildlife realism require genuine photographic footage."
            suggested_transition = "fade"
        else:
            medium = self.MEDIUM_REAL_FOOTAGE
            reason = "Defaulting to live-action documentary footage for baseline naturalism."
            suggested_transition = "fade"

        return {
            "scene_id": scene_spec.get("id"),
            "title": scene_spec.get("title"),
            "selected_medium": medium,
            "duration_sec": scene_spec.get("duration_sec", 6.0),
            "suggested_transition": suggested_transition,
            "justification": reason
        }

    def plan_documentary_storyboard(self, storyboard: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Plan mediums across all scenes in a storyboard."""
        return [self.plan_scene_medium(sc) for sc in storyboard]

if __name__ == "__main__":
    planner = SceneMediumPlanner()
    sample_storyboard = [
        {"id": "SC-01", "title": "Dawn on the Kopje", "intent": "Establishing real lion wildlife at sunrise", "duration_sec": 8.0},
        {"id": "SC-02", "title": "The Savanna Ecosystem", "intent": "Establishing 3D camera sweep across savanna environment", "duration_sec": 6.0},
        {"id": "SC-03", "title": "Hero Lion Stalking", "intent": "3D anatomical hero lion character closeup and breathing", "duration_sec": 6.0},
        {"id": "SC-04", "title": "Territory & Pride Dynamics", "intent": "Animated territory map showing habitat fragmentation", "duration_sec": 8.0},
        {"id": "SC-05", "title": "Apex Physiology", "intent": "Infographic showing bite force and sprint velocity", "duration_sec": 8.0},
        {"id": "SC-06", "title": "Pride in the Wilderness", "intent": "Real photographic footage of lion pride resting together", "duration_sec": 10.0}
    ]
    decisions = planner.plan_documentary_storyboard(sample_storyboard)
    print("Storyboard Medium Planning:")
    for d in decisions:
        print(f" - [{d['scene_id']}]: {d['title']} -> {d['selected_medium']} ({d['duration_sec']}s)")
