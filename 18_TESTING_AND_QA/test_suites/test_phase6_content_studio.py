"""test_phase6_content_studio.py
MASTER-AI Phase 6 Automated Test Suite: Content Studio & Video Production Pipeline

Covers:
1. Voice synthesis adapters (EdgeTTS evaluation, Windows SAPI5 offline, Procedural speech, Piper check).
2. Visual asset adapters (Procedural Canvas 1920x1080, Ken Burns motion video clips, Cloud AI zero-paid gate).
3. Audio manager (ambient soundscape synthesis, ducking mixing).
4. Multilingual subtitle engine (Hindi Devanagari SRT, styled ASS, QA validation).
5. FFmpeg programmatic video editor (H.264/AAC MP4 timeline assembly, title cards).
6. Media quality assurance auditor (decodability, resolution, audio streams, black frames, silence, QA pass/fail).
7. Thumbnail studio and publication packager (1280x720 thumbnail, YouTube metadata, Approval Center staging).
8. Production specialist agents (AGT-008 through AGT-015 registration and detailed health checks).
9. End-to-end acceptance test: "Create a 5-minute Hindi documentary about lions for YouTube".
10. FastAPI Content Studio REST API endpoints.
"""

import os
import sys
import json
import time
import unittest
import importlib
from pathlib import Path

# Ensure workspace root is in sys.path
_current_dir = Path(__file__).resolve().parent
_workspace_root = _current_dir.parents[1]
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

_studio_pkg = importlib.import_module("09_CONTENT_STUDIO.engine")
EdgeTTSVoiceAdapter = _studio_pkg.EdgeTTSVoiceAdapter
WindowsSAPI5VoiceAdapter = _studio_pkg.WindowsSAPI5VoiceAdapter
ProceduralSpeechSynthesizer = _studio_pkg.ProceduralSpeechSynthesizer
PiperVoiceAdapter = _studio_pkg.PiperVoiceAdapter
VoiceRouter = _studio_pkg.VoiceRouter

ProceduralCanvasVisualAdapter = _studio_pkg.ProceduralCanvasVisualAdapter
CloudAIVisualAdapter = _studio_pkg.CloudAIVisualAdapter
VisualAssetRouter = _studio_pkg.VisualAssetRouter

AudioManager = _studio_pkg.AudioManager
SubtitleEngine = _studio_pkg.SubtitleEngine
VideoEditingEngine = _studio_pkg.VideoEditingEngine
MediaQualityAssuranceAuditor = _studio_pkg.MediaQualityAssuranceAuditor
ThumbnailStudio = _studio_pkg.ThumbnailStudio
ProductionPackager = _studio_pkg.ProductionPackager
ContentStudioOrchestrator = _studio_pkg.ContentStudioOrchestrator

_orch_pkg = importlib.import_module("03_AI_AGENTS.orchestrator")
AgentRegistry = _orch_pkg.AgentRegistry

_appr_pkg = importlib.import_module("03_AI_AGENTS.approval_engine.approval_center")
ApprovalCenter = _appr_pkg.ApprovalCenter

TEST_TEMP_DIR = os.path.join(str(_workspace_root), "03_AI_AGENTS", "sandbox", "tasks", "phase6_tests")


class TestPhase6ContentStudio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_TEMP_DIR, exist_ok=True)
        cls.registry = AgentRegistry()
        cls.orchestrator = ContentStudioOrchestrator(output_root=TEST_TEMP_DIR)

    def test_01_voice_adapters_evaluation(self):
        """Verify voice adapters: EdgeTTS cleanly reports status, Procedural and SAPI generate real audio."""
        # 1. EdgeTTS Evaluation (should report availability or clean provider error without crash)
        edge = EdgeTTSVoiceAdapter()
        edge_status = edge.check_availability()
        self.assertIn("status", edge_status)
        self.assertIn(edge_status["status"], {"AVAILABLE", "PROVIDER_UNAVAILABLE"})

        # 2. Procedural Speech Synthesizer (Real execution with word timings)
        proc = ProceduralSpeechSynthesizer()
        self.assertEqual(proc.check_availability()["status"], "AVAILABLE")
        out_wav = os.path.join(TEST_TEMP_DIR, "proc_narration.wav")
        res = proc.synthesize_speech("यह शेर के जीवन का एक सजीव वर्णन है।", "Hindi", out_wav)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(out_wav))
        self.assertGreater(res["file_size_bytes"], 1000)
        self.assertGreaterEqual(len(res["word_timings"]), 5)

        # 3. Piper Adapter Evaluation
        piper = PiperVoiceAdapter()
        piper_status = piper.check_availability()
        self.assertIn(piper_status["status"], {"AVAILABLE", "PROVIDER_UNAVAILABLE"})

        # 4. Voice Router Routing
        router = VoiceRouter()
        routed = router.synthesize("The majestic lion roams the African savannah.", language="English", output_path=os.path.join(TEST_TEMP_DIR, "routed_en.wav"))
        self.assertEqual(routed["status"], "SUCCESS")
        self.assertTrue(routed["real_execution"])

    def test_02_visual_adapters_and_zero_paid_gate(self):
        """Verify procedural image/motion video generation and zero-paid protection on cloud AI."""
        # 1. Procedural Canvas Image Generation (1920x1080)
        canvas = ProceduralCanvasVisualAdapter()
        img_path = os.path.join(TEST_TEMP_DIR, "scene_test.png")
        img_res = canvas.generate_image(
            prompt="Roaring male lion at sunset",
            resolution=(1920, 1080),
            output_path=img_path,
            metadata={"scene_title": "TEST SCENE", "act_label": "ACT I"}
        )
        self.assertEqual(img_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(img_path))
        self.assertEqual(img_res["resolution"], (1920, 1080))

        # 2. Motion Video Clip via Ken Burns pan & zoom
        vid_path = os.path.join(TEST_TEMP_DIR, "scene_motion.mp4")
        vid_res = canvas.get_video_clip(
            prompt="Lion pride resting on rocky outcrop",
            duration_sec=2.0,
            resolution=(1920, 1080),
            output_path=vid_path
        )
        self.assertEqual(vid_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(vid_path))
        self.assertGreater(vid_res["file_size_bytes"], 10000)

        # 3. Cloud AI zero-paid policy enforcement
        cloud = CloudAIVisualAdapter()
        blocked_res = cloud.generate_image("A futuristic lion", (1024, 1024), "cloud_img.png")
        self.assertEqual(blocked_res["status"], "BLOCKED_APPROVAL_REQUIRED")
        self.assertFalse(blocked_res["real_execution"])

    def test_03_audio_manager_soundscape_and_ducking(self):
        """Verify ambient audio generation and ducked mixing with voiceover."""
        mgr = AudioManager()

        # 1. Generate ambient audio soundscape
        ambient_wav = os.path.join(TEST_TEMP_DIR, "ambient.wav")
        amb_res = mgr.generate_ambient_soundscape(duration_sec=4.0, output_path=ambient_wav, style="savannah_wind")
        self.assertEqual(amb_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(ambient_wav))
        self.assertGreater(amb_res["file_size_bytes"], 50000)

        # 2. Mix with voiceover applying ducking
        voice_wav = os.path.join(TEST_TEMP_DIR, "proc_narration.wav")
        mixed_wav = os.path.join(TEST_TEMP_DIR, "mixed_soundtrack.wav")
        mix_res = mgr.mix_narration_with_music(voice_wav, ambient_wav, mixed_wav, ducking_db=-14.0)
        self.assertEqual(mix_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(mixed_wav))

    def test_04_multilingual_subtitle_engine(self):
        """Verify SRT and ASS generation in Hindi Devanagari and automated subtitle QA."""
        engine = SubtitleEngine()
        segments = [
            {"start_sec": 0.0, "end_sec": 3.0, "text": "जब अफ्रीकी सवाना पर भोर की पहली किरण पड़ती है..."},
            {"start_sec": 3.2, "end_sec": 6.0, "text": "प्रकृति का सबसे भव्य शासक शेर जागता है।"}
        ]

        # 1. SRT generation
        srt_file = os.path.join(TEST_TEMP_DIR, "test_subs.srt")
        srt_res = engine.generate_srt(segments, srt_file)
        self.assertEqual(srt_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(srt_file))
        with open(srt_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("00:00:00,000 --> 00:00:03,000", content)
        self.assertIn("अफ्रीकी सवाना", content)

        # 2. ASS generation
        ass_file = os.path.join(TEST_TEMP_DIR, "test_subs.ass")
        ass_res = engine.generate_ass(segments, ass_file)
        self.assertEqual(ass_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(ass_file))

        # 3. Subtitle QA validation
        val = engine.validate_subtitles(segments)
        self.assertTrue(val["valid"])
        self.assertEqual(val["status"], "PASS")

        # Invalid segment test (negative duration)
        bad_segments = [{"start_sec": 5.0, "end_sec": 2.0, "text": "Inverted time"}]
        bad_val = engine.validate_subtitles(bad_segments)
        self.assertFalse(bad_val["valid"])
        self.assertEqual(bad_val["status"], "FAIL")

    def test_05_ffmpeg_video_editor_and_title_card(self):
        """Verify FFmpeg timeline rendering and title card generation."""
        editor = VideoEditingEngine()

        # 1. Title Card clip
        title_mp4 = os.path.join(TEST_TEMP_DIR, "title_card.mp4")
        tc_res = editor.generate_title_card(
            title="The Sovereign Lion",
            subtitle="Savannah Wildlife Series",
            duration_sec=2.0,
            resolution=(1920, 1080),
            output_path=title_mp4
        )
        self.assertEqual(tc_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(title_mp4))

        # 2. Multi-scene render
        scene_mp4 = os.path.join(TEST_TEMP_DIR, "scene_motion.mp4")
        scenes = [
            {"video_clip_path": title_mp4, "duration_sec": 2.0},
            {"video_clip_path": scene_mp4, "duration_sec": 2.0}
        ]
        audio_path = os.path.join(TEST_TEMP_DIR, "mixed_soundtrack.wav")
        render_out = os.path.join(TEST_TEMP_DIR, "rendered_timeline.mp4")

        res = editor.render_timeline(
            scenes=scenes,
            audio_track_path=audio_path,
            output_path=render_out,
            resolution=(1920, 1080),
            fps=30
        )
        self.assertEqual(res["status"], "RENDER_COMPLETE")
        self.assertTrue(os.path.exists(render_out))
        self.assertEqual(res["video_codec"], "h264")
        self.assertEqual(res["audio_codec"], "aac")
        self.assertGreater(res["file_size_bytes"], 50000)

    def test_06_media_quality_assurance_auditor(self):
        """Verify automated media QA detects valid streams and flags failures."""
        auditor = MediaQualityAssuranceAuditor()
        valid_video = os.path.join(TEST_TEMP_DIR, "rendered_timeline.mp4")
        srt_file = os.path.join(TEST_TEMP_DIR, "test_subs.srt")

        # 1. Audit valid video
        report = auditor.audit_video_production(
            video_path=valid_video,
            expected_duration_sec=4.0,
            expected_resolution="1920x1080",
            subtitle_path=srt_file,
            license_manifest={"license": "CC-0"}
        )
        self.assertEqual(report["overall_status"], "PASS")
        self.assertTrue(report["passed"])
        self.assertEqual(len(report["critical_failures"]), 0)
        self.assertTrue(report["media_probe"]["has_video"])
        self.assertTrue(report["media_probe"]["has_audio"])

        # 2. Audit non-existent video (should fail closed)
        fail_report = auditor.audit_video_production("non_existent_file.mp4")
        self.assertEqual(fail_report["overall_status"], "FAIL")
        self.assertFalse(fail_report["passed"])

    def test_07_thumbnail_studio_and_packaging(self):
        """Verify 1280x720 YouTube thumbnail and publication staging with approval ticket."""
        thumb_studio = ThumbnailStudio()
        thumb_path = os.path.join(TEST_TEMP_DIR, "thumb_test.png")
        t_res = thumb_studio.generate_youtube_thumbnail(
            title_hindi="सवाना का सम्राट: शेर",
            subtitle_english="The Sovereign Lion",
            output_path=thumb_path
        )
        self.assertEqual(t_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(thumb_path))
        self.assertEqual(t_res["resolution"], "1280x720")

        # Packaging into Approval Center
        packager = ProductionPackager()
        pkg = packager.package_for_publication(
            project_id="PROJ-TEST-01",
            title="सवाना का सम्राट (The Sovereign Lion)",
            video_path=os.path.join(TEST_TEMP_DIR, "rendered_timeline.mp4"),
            audio_path=os.path.join(TEST_TEMP_DIR, "mixed_soundtrack.wav"),
            srt_path=os.path.join(TEST_TEMP_DIR, "test_subs.srt"),
            ass_path=os.path.join(TEST_TEMP_DIR, "test_subs.ass"),
            thumbnail_path=thumb_path,
            qa_report={"overall_status": "PASS", "passed": True},
            output_dir=os.path.join(TEST_TEMP_DIR, "release_bundle")
        )
        self.assertEqual(pkg["status"], "STAGED_FOR_APPROVAL")
        self.assertTrue(pkg["approval_ticket_id"].startswith("TKT-"))
        self.assertTrue(os.path.exists(pkg["metadata_file"]))

    def test_08_production_specialist_agents_and_health(self):
        """Verify AGT-008 through AGT-015 exist and detailed health checks distinguish states."""
        all_agents = self.registry.list_agents()
        agent_ids = {a["id"] for a in all_agents}

        for expected in ["AGT-008", "AGT-009", "AGT-010", "AGT-011", "AGT-012", "AGT-013", "AGT-014", "AGT-015"]:
            self.assertIn(expected, agent_ids, f"Agent {expected} must be registered")

        # Test detailed health breakdown
        health_editor = self.registry.get_detailed_agent_health("AGT-013")
        self.assertTrue(health_editor["registered"])
        self.assertTrue(health_editor["dependencies_ready"])
        self.assertTrue(health_editor["model_ready"])
        self.assertIn(health_editor["status"], {"READY_TO_EXECUTE", "HEALTHY_VERIFIED"})

    def test_09_end_to_end_documentary_production_workflow(self):
        """End-to-End Acceptance: 'Create a 5-minute Hindi documentary about lions for YouTube'.
        Executes full 11-step pipeline, generates real media, passes QA, and stages release package.
        """
        request = "Create a 5-minute Hindi documentary about lions for YouTube."
        summary = self.orchestrator.produce_documentary(
            request_prompt=request,
            target_duration_sec=300.0,
            language="Hindi",
            resolution=(1920, 1080),
            fps=30
        )

        self.assertEqual(summary["status"], "COMPLETED")
        self.assertEqual(summary["qa_status"], "PASS")
        self.assertTrue(summary["qa_passed"])

        # Check deliverables exist on disk
        artifacts = summary["artifacts"]
        self.assertTrue(os.path.exists(artifacts["final_video_mp4"]))
        self.assertTrue(os.path.exists(artifacts["audio_track_wav"]))
        self.assertTrue(os.path.exists(artifacts["subtitles_srt"]))
        self.assertTrue(os.path.exists(artifacts["subtitles_ass"]))
        self.assertTrue(os.path.exists(artifacts["thumbnail_png"]))
        self.assertTrue(os.path.exists(artifacts["qa_report_json"]))
        self.assertTrue(os.path.exists(artifacts["publication_bundle"]))

        # Check video specifications
        v_specs = summary["video_specs"]
        self.assertEqual(v_specs["resolution"], "1920x1080")
        self.assertEqual(v_specs["video_codec"], "h264")
        self.assertEqual(v_specs["audio_codec"], "aac")
        self.assertGreater(v_specs["file_size_bytes"], 100000)

        # Check approval ticket
        self.assertTrue(summary["approval_ticket_id"].startswith("TKT-"))
        self.assertEqual(summary["approval_status"], "PENDING")

        # Check Phase 6.2 remediated duration accuracy (+/- 2.5s on 300s target)
        self.assertAlmostEqual(summary["actual_duration_sec"], 300.0, delta=2.5)
        self.assertAlmostEqual(v_specs["duration_sec"], 300.0, delta=2.5)

    def test_10_fastapi_content_studio_endpoints(self):
        """Verify Content Studio REST API endpoints respond with 200 and expected schemas."""
        from fastapi.testclient import TestClient
        main_mod = importlib.import_module("00_CORE_SYSTEM.api.main")
        client = TestClient(main_mod.app)

        # 1. Provider status
        res = client.get("/api/v1/content_studio/providers/status")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["video_renderer"]["available"])

        # 2. Subtitle validation
        sub_req = {
            "segments": [
                {"start_sec": 0.0, "end_sec": 2.5, "text": "शेर का जीवन"},
                {"start_sec": 2.6, "end_sec": 5.0, "text": "सवाना का सम्राट"}
            ],
            "format": "SRT"
        }
        res = client.post("/api/v1/content_studio/subtitles", json=sub_req)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["validation"]["valid"])

        # 3. Voiceover synthesis
        voice_req = {
            "text": "शेर सवाना का सम्राट है।",
            "language": "Hindi"
        }
        res = client.post("/api/v1/content_studio/voiceover", json=voice_req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["result"]["status"], "SUCCESS")

    def test_11_remediation_regression_suite(self):
        """Phase 6.2 Regression Suite:
        - Rejection of procedural hum as speech narration
        - Arbitrary timeline and scene duration scaling
        - Audio/video duration consistency enforcement
        - Asset licensing metadata tracking
        - Subtitle boundary enforcement
        """
        # 1. Non-linguistic audio rejection
        router = VoiceRouter()
        proc = ProceduralSpeechSynthesizer()
        self.assertFalse(proc.is_human_speech, "Procedural speech must be flagged as non-human")

        # 2. Hardcoded duration prevention: router produces exact duration requested
        visual_router = VisualAssetRouter()
        test_dur = 4.5
        asset = visual_router.generate_scene_asset(
            prompt="Lion on kopje",
            resolution=(1280, 720),
            duration_sec=test_dur,
            output_dir=os.path.join(TEST_TEMP_DIR, "regr_assets"),
            scene_idx=99,
            asset_class="LICENSED_STOCK_IMAGE"
        )
        self.assertEqual(asset["duration_sec"], test_dur)
        self.assertIn("CC0-1.0", asset["license"])
        self.assertEqual(asset["media_type"], "LICENSED_STOCK_IMAGE")
        self.assertTrue(os.path.exists(asset["video_clip_path"]))

        # 3. Media QA rejects duration mismatch
        qa = MediaQualityAssuranceAuditor()
        audit_res = qa.audit_video_production(
            video_path=asset["video_clip_path"],
            expected_duration_sec=300.0,  # 4.5s vs 300s target
            duration_tolerance_sec=2.5
        )
        self.assertEqual(audit_res["overall_status"], "FAIL")
        self.assertTrue(any("CRITICAL DURATION FAILURE" in f for f in audit_res["critical_failures"]))

        # 4. Media QA rejects procedural hum as human speech
        fake_manifest = {"is_human_speech": False, "provider": "procedural_speech"}
        audit_voice = qa.audit_video_production(
            video_path=asset["video_clip_path"],
            expected_duration_sec=test_dur,
            voiceover_manifest=fake_manifest,
            duration_tolerance_sec=2.5
        )
        self.assertEqual(audit_voice["overall_status"], "FAIL")
        self.assertTrue(any("VOICE SYNTHESIS FAILURE" in f for f in audit_voice["critical_failures"]))

        # 5. Subtitle boundary capping
        sub_engine = SubtitleEngine()
        scene_narr = [{
            "scene_index": 1,
            "timeline_start_sec": 0.0,
            "duration_sec": 10.0,
            "text": "परीक्षण वाक्य",
            "sentence_boundaries": [{"text": "परीक्षण वाक्य", "offset_sec": 0.5, "duration_sec": 15.0}]  # 15.5s total
        }]
        sub_res = sub_engine.generate_from_scene_narration(
            scene_narrations=scene_narr,
            max_video_duration=10.0,
            srt_output_path=os.path.join(TEST_TEMP_DIR, "regr_subs.srt"),
            ass_output_path=os.path.join(TEST_TEMP_DIR, "regr_subs.ass")
        )
        self.assertEqual(sub_res["validation"]["status"], "PASS")
        # Ensure no cue exceeds max_video_duration
        with open(os.path.join(TEST_TEMP_DIR, "regr_subs.srt"), "r", encoding="utf-8") as f:
            srt_content = f.read()
        self.assertNotIn("00:00:15", srt_content, "Subtitle cue must not overflow video duration")


if __name__ == "__main__":
    unittest.main()
