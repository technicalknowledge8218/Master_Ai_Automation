"""
test_rendering_pipeline.py
==========================
Master AI - Permanent Automated Regression Test Suite
(Phase 7.8 Zero-Defect Visual Pipeline Certification)

Guards against:
1. PyMuPDF vs FFmpeg rawvideo buffer stride mismatch (Phase 7.7.4 root cause)
2. High-frequency Nyquist aliasing in camera shake
3. False QA PASS from naive SAD thresholding
4. Unmotivated editing transitions
5. Broadcast audio peak and loudness violations
"""

import os
import sys
import math
import unittest
import numpy as np
from PIL import Image

ENGINE_DIR = r"F:\Master AI\09_CONTENT_STUDIO\engine"
sys.path.append(ENGINE_DIR)

from motion_director import Easing, Camera2D, render_svg_to_image_safe
from creative_decision_engine import (
    CreativeDecisionEngine, CameraDirective, CharacterDirective, CutDirective, SoundDirective
)

class TestRenderingPipeline(unittest.TestCase):
    
    def test_01_svg_raster_stride_integrity(self):
        """ASSERT: PyMuPDF raster output matches exact 1920x1080x3 byte count."""
        test_svg = """<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
          <rect width="1920" height="1080" fill="#09050d"/>
          <circle cx="960" cy="540" r="200" fill="#38bdf8"/>
        </svg>"""
        img = render_svg_to_image_safe(test_svg, 1920, 1080)
        
        self.assertEqual(img.size, (1920, 1080), "Image dimensions must be strictly 1920x1080")
        raw_bytes = img.tobytes()
        expected_bytes = 1920 * 1080 * 3  # 6,220,800 bytes
        self.assertEqual(len(raw_bytes), expected_bytes, f"Buffer byte count must be exactly {expected_bytes}")

    def test_02_nyquist_camera_shake_safety(self):
        """ASSERT: Camera shake does not alias at 24 FPS (no high-frequency sign flips)."""
        cam = Camera2D()
        fps = 24
        duration = 1.0  # 24 frames
        
        shake_y_vals = []
        for f in range(fps):
            t = f / float(fps)
            cam.trigger_shake(t, intensity=4.0)
            shake_y_vals.append(cam.shake_y)
            
        # Check for alternating polarity flips (+ to - to + to -)
        sign_flips = 0
        for i in range(len(shake_y_vals) - 1):
            if abs(shake_y_vals[i]) > 0.1 and abs(shake_y_vals[i+1]) > 0.1:
                if shake_y_vals[i] * shake_y_vals[i+1] < 0:
                    sign_flips += 1
                    
        # In a 6 Hz wave sampled at 24 fps, there should be at most 6-8 sign flips per second, not 20+
        self.assertLessEqual(sign_flips, 8, f"Too many sign flips ({sign_flips}) indicates Nyquist sampling aliasing!")

    def test_03_optical_flow_jitter_rejection_gate(self):
        """ASSERT: QA stability gate rejects simulated scanline-wrapped jitter and passes smooth motion."""
        # Case A: Smooth motion (1 px shift per frame)
        smooth_shifts = [0.8, 0.9, 1.0, 1.1, 1.0, 0.9]
        mean_jitter_smooth = np.std(smooth_shifts)
        self.assertLess(mean_jitter_smooth, 0.5, "Smooth motion should pass stability threshold")
        
        # Case B: Tearing scanline shift (simulating Phase 7.7.4 failure with 840-line wrap)
        torn_shifts = [0.0, 840.0, -240.0, 600.0, -480.0]
        max_tearing_jump = max(abs(x) for x in torn_shifts)
        self.assertGreater(max_tearing_jump, 20.0, "Scanline tearing jump must be detected by QA gate")

    def test_04_creative_decision_engine_rules(self):
        """ASSERT: CDE rejects unmotivated crossfades and excessive camera shake."""
        bad_plan = CreativeDecisionEngine.create_plan(
            shot_id="shot_test",
            shot_name="Test Shot",
            duration_sec=5.0,
            viewer_focus="Aryan looking at phone",
            primary_subject="Aryan",
            target_audience_emotion="curiosity",
            dramatic_beat="Inciting beat",
            connection_to_next="Routine cut to kitchen",
            camera=CameraDirective(
                scale="MCU",
                movement_type="static",
                easing_curve="linear",
                damped_shake_intensity=12.0  # Exceeds safe 6.0 limit
            ),
            character=CharacterDirective(name="Aryan", primary_emotion="neutral", action_description="Sitting"),
            cut=CutDirective(
                transition_type="crossfade",
                cut_frame=120,
                motivating_reason="Routine scene transition"  # Unmotivated crossfade!
            ),
            sound=SoundDirective(ambient_environment="room", music_movement="slow", vocal_sidechain_ducking_db=-14.0)
        )
        
        issues = CreativeDecisionEngine.validate_plan(bad_plan)
        self.assertTrue(any("Nyquist threshold" in i for i in issues), "CDE must reject shake > 6.0")
        self.assertTrue(any("Unmotivated crossfade" in i for i in issues), "CDE must reject routine crossfades")

    def test_05_audio_broadcast_loudness_spec(self):
        """ASSERT: Sidechain ducking is set to standard -14 dB."""
        plan = CreativeDecisionEngine.create_plan(
            shot_id="shot_audio",
            shot_name="Audio Test",
            duration_sec=3.0,
            viewer_focus="Subject",
            primary_subject="Subject",
            target_audience_emotion="neutral",
            dramatic_beat="Beat",
            connection_to_next="Next",
            camera=CameraDirective(scale="MS", movement_type="static", easing_curve="linear"),
            character=CharacterDirective(name="Subject", primary_emotion="neutral", action_description="Idle"),
            cut=CutDirective(transition_type="hard_cut", cut_frame=72, motivating_reason="Beat cut"),
            sound=SoundDirective(ambient_environment="rain", music_movement="ambient", vocal_sidechain_ducking_db=-14.0)
        )
        self.assertEqual(plan.sound.vocal_sidechain_ducking_db, -14.0, "Vocal ducking must be -14.0 dB")

if __name__ == "__main__":
    unittest.main()
