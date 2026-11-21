"""test_phase6_5_adapters.py
MASTER-AI Phase 6.5 Comprehensive Ecosystem Adapters Test Suite
Validates all 8 newly installed and integrated adapters:
1. FreeLLMAdapter
2. OmniRouteGatewayAdapter
3. FireRedStorylineAdapter
4. OpenFilmAdapter
5. WhisperTranscriptionAdapter
6. SocialdropPublishingAdapter
7. PexelsMediaAdapter
8. WikimediaMediaAdapter
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

# Import the 8 adapters
from importlib import import_module
free_llm_mod = import_module("00_CORE_SYSTEM.discovery_engine.free_llm_adapter")
omni_mod = import_module("04_LLM_AND_AI.gateways.omniroute_adapter")
firered_mod = import_module("09_CONTENT_STUDIO.engine.firered_storyline_adapter")
openfilm_mod = import_module("09_CONTENT_STUDIO.engine.openfilm_adapter")
whisper_mod = import_module("09_CONTENT_STUDIO.engine.whisper_transcription_adapter")
social_mod = import_module("10_SOCIAL_MEDIA.publishers.socialdrop_adapter")
pexels_mod = import_module("09_CONTENT_STUDIO.engine.pexels_media_adapter")
wiki_mod = import_module("09_CONTENT_STUDIO.engine.wikimedia_media_adapter")


class TestPhase65EcosystemAdapters(unittest.TestCase):
    """Test suite covering the 8 Phase 6.5 ecosystem adapters."""

    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(tempfile.mkdtemp(prefix="master_ai_test_p65_"))

    @classmethod
    def tearDownClass(cls):
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir, ignore_errors=True)

    # -------------------------------------------------------------------------
    # 1. Free-LLM Discovery Adapter
    # -------------------------------------------------------------------------
    def test_01_free_llm_adapter(self):
        cat_file = self.test_dir / "free_llm_cat.json"
        adapter = free_llm_mod.FreeLLMAdapter(catalog_path=cat_file)

        # Health & Config
        hc = adapter.health_check()
        self.assertTrue(hc["healthy"])
        self.assertEqual(hc["status"], "HEALTHY")
        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Refresh Catalog
        ref = adapter.refresh_catalog()
        self.assertEqual(ref["status"], "REFRESH_SUCCESS")
        self.assertGreaterEqual(ref["total_providers"], 3)
        self.assertTrue(cat_file.exists())

        # Zero-paid providers retrieval
        free_provs = adapter.get_free_tier_providers(zero_paid_only=True)
        self.assertGreaterEqual(len(free_provs), 3)
        for p in free_provs:
            self.assertEqual(p["compliance_status"], "APPROVED_ZERO_PAID")

        # Sync to Model Registry
        sync_res = adapter.sync_to_master_model_registry()
        self.assertEqual(sync_res["status"], "SYNCED")
        self.assertGreater(sync_res["models_synced"], 0)

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "REFRESH_SUCCESS")

    # -------------------------------------------------------------------------
    # 2. OmniRoute Multi-Provider Gateway Adapter
    # -------------------------------------------------------------------------
    def test_02_omniroute_adapter(self):
        gateway = omni_mod.OmniRouteGatewayAdapter(max_spend_usd=0.0)

        # Health & Config
        hc = gateway.health_check()
        self.assertTrue(hc["healthy"])
        self.assertTrue(hc["zero_paid_enforced"])
        vc = gateway.validate_configuration()
        self.assertTrue(vc["valid"])
        self.assertTrue(vc["zero_paid_policy_compliant"])

        # Route completion (mock / local)
        resp = gateway.route_completion(
            prompt="Analyze lion territorial marking behavior",
            task_type="default_reasoning"
        )
        self.assertEqual(resp["status"], "COMPLETED")
        self.assertEqual(resp["cost_usd"], 0.0)
        self.assertIn("OmniRoute Gateway", resp["response_text"])

        # Zero-paid spending rejection
        bad_gw = omni_mod.OmniRouteGatewayAdapter(max_spend_usd=50.0)
        bad_vc = bad_gw.validate_configuration()
        self.assertFalse(bad_vc["valid"])
        self.assertIn("Non-zero max_spend_usd", bad_vc["issues"][0])

        # Rollback
        rb = gateway.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")

    # -------------------------------------------------------------------------
    # 3. FireRed-OpenStoryline Directing Adapter
    # -------------------------------------------------------------------------
    def test_03_firered_storyline_adapter(self):
        adapter = firered_mod.FireRedStorylineAdapter()

        # Health & Config
        hc = adapter.health_check()
        self.assertTrue(hc["healthy"])
        self.assertEqual(hc["mcp_tools_available"], 3)
        self.assertIn("analyze_scene_intent", hc["mcp_tool_names"])

        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Directing plan generation for 6 documentary scenes
        mock_scenes = [
            {"title": "Dawn on the Savannah", "voiceover": "As the morning sun rises over the vast plains..."},
            {"title": "The Pride at Rest", "voiceover": "A family of lions rests beneath the shade of an acacia tree..."}
        ]
        plan = adapter.generate_directing_plan(mock_scenes, target_duration_sec=100.0)
        self.assertEqual(plan["status"], "SUCCESS")
        self.assertEqual(plan["total_scenes"], 2)
        self.assertEqual(plan["allocated_duration_sec"], 100.0)
        self.assertEqual(plan["directing_instructions"][0]["duration_sec"], 50.0)
        self.assertEqual(plan["directing_instructions"][0]["audio_ducking_db"], -14.0)

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")

    # -------------------------------------------------------------------------
    # 4. OpenFilm Video-as-Code Adapter
    # -------------------------------------------------------------------------
    def test_04_openfilm_adapter(self):
        adapter = openfilm_mod.OpenFilmAdapter()

        # Health & Config
        hc = adapter.health_check()
        self.assertIn(hc["status"], ["HEALTHY", "DEGRADED_NODE_UNAVAILABLE"])
        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Generate HTML dynamic shot
        shot_dir = self.test_dir / "openfilm_shot"
        shot_res = adapter.generate_html_shot(
            shot_title="The Sovereign Lion",
            subtitle="Savannah Wildlife Series",
            duration_sec=3.0,
            output_dir=str(shot_dir)
        )
        self.assertEqual(shot_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(shot_res["html_path"]))
        with open(shot_res["html_path"], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("The Sovereign Lion", content)
        self.assertIn("window.frame = function(t)", content)

        # Comparison Benchmark against FFmpeg
        comp = adapter.compare_with_ffmpeg_renderer()
        self.assertEqual(comp["comparison_verdict"], "SUPPLEMENT_NATIVE_FFMPEG")
        self.assertGreaterEqual(len(comp["findings"]), 3)

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")

    # -------------------------------------------------------------------------
    # 5. faster-whisper Speech-to-Text & Quality QA Adapter
    # -------------------------------------------------------------------------
    def test_05_whisper_transcription_adapter(self):
        adapter = whisper_mod.WhisperTranscriptionAdapter(default_model_size="tiny")

        # Health & Config
        hc = adapter.health_check()
        self.assertTrue(hc["healthy"])
        self.assertEqual(hc["status"], "HEALTHY")
        self.assertEqual(hc["device"], "cpu")
        self.assertEqual(hc["compute_type"], "int8")

        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Test verification logic with existing narration audio if present
        sample_wav = WORKSPACE_ROOT / "09_CONTENT_STUDIO" / "documentaries" / "DOC-7b06c3a7" / "assets" / "scene_01_voice.wav"
        if sample_wav.exists():
            expected_script = "जब अफ्रीकी सवाना के विशाल मैदानों पर भोर की पहली सुनहरी किरणें बिखरती हैं"
            ver_res = adapter.verify_speech_intelligibility(
                audio_path=str(sample_wav),
                expected_script_text=expected_script,
                language="hi",
                max_wer_threshold=0.60
            )
            self.assertIn("verified", ver_res)
            self.assertIn("wer", ver_res)
            self.assertGreaterEqual(ver_res["audio_duration_sec"], 20.0)

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")
        self.assertTrue(rb["model_unloaded"])

    # -------------------------------------------------------------------------
    # 6. socialdrop Multi-Platform Publishing Adapter
    # -------------------------------------------------------------------------
    def test_06_socialdrop_adapter(self):
        staged_dir = self.test_dir / "socialdrop_staged"
        adapter = social_mod.SocialdropPublishingAdapter(staged_dir=str(staged_dir), dry_run=True)

        # Health & Config
        hc = adapter.health_check()
        self.assertTrue(hc["healthy"])
        self.assertTrue(hc["dry_run_mode"])
        self.assertIn("youtube", hc["supported_platforms"])
        self.assertIn("tiktok", hc["supported_platforms"])

        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Platform specification inspection
        yt_spec = adapter.inspect_platform_support("youtube")
        self.assertTrue(yt_spec["supported"])
        self.assertEqual(yt_spec["api_name"], "YouTube Data API v3")
        self.assertTrue(yt_spec["scheduling_supported"])

        # Rejection of unauthorized publish attempt (Security Invariant)
        bad_pub = adapter.publish_package(
            publication_package_dir=str(self.test_dir),
            target_platforms=["youtube"],
            auth_ticket=""  # Missing ticket
        )
        self.assertEqual(bad_pub["status"], "BLOCKED_APPROVAL_REQUIRED")

        # Staged test publish with valid ticket
        pkg_dir = self.test_dir / "mock_pkg"
        pkg_dir.mkdir(parents=True, exist_ok=True)
        with open(pkg_dir / "PUBLICATION_METADATA.json", "w", encoding="utf-8") as f:
            json.dump({"project_id": "TEST-001", "title": "Test Wildlife Release"}, f)

        good_pub = adapter.publish_package(
            publication_package_dir=str(pkg_dir),
            target_platforms=["youtube", "linkedin", "x_twitter"],
            auth_ticket="AUTH-TEST-778899"
        )
        self.assertEqual(good_pub["status"], "SUCCESS")
        self.assertEqual(good_pub["published_results"]["youtube"]["status"], "DRY_RUN_SUCCESS")
        self.assertTrue(good_pub["dry_run_mode"])

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")
        self.assertTrue(rb["dry_run"])

    # -------------------------------------------------------------------------
    # 7. Pexels Stock Footage Discovery Adapter
    # -------------------------------------------------------------------------
    def test_07_pexels_media_adapter(self):
        adapter = pexels_mod.PexelsMediaAdapter()

        # Health & Config
        hc = adapter.health_check()
        self.assertTrue(hc["healthy"])
        self.assertGreaterEqual(hc["curated_archive_clips"], 6)
        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Search wildlife videos
        search_res = adapter.search_wildlife_videos(query="lion dawn savannah", per_page=2)
        self.assertEqual(search_res["status"], "SUCCESS")
        self.assertGreaterEqual(search_res["results_count"], 1)
        v0 = search_res["videos"][0]
        self.assertIn("pexels_url", v0)
        self.assertIn("download_link", v0)
        self.assertEqual(v0["license"], "Pexels License (Commercial Use Allowed)")
        self.assertFalse(v0["attribution_required"])

        # Acquire scene clip and generate verifiable provenance manifest
        clip_out = self.test_dir / "pexels_clips"
        acq_res = adapter.acquire_scene_clip(
            scene_index=1,
            visual_prompt="African lion standing on kopje at dawn",
            output_dir=str(clip_out)
        )
        self.assertEqual(acq_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(acq_res["provenance_file"]))
        with open(acq_res["provenance_file"], "r", encoding="utf-8") as f:
            prov_data = json.load(f)
        self.assertEqual(prov_data["license"], "Pexels License (Commercial Use Allowed)")
        self.assertTrue(prov_data["attribution_recorded"])

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")

    # -------------------------------------------------------------------------
    # 8. Wikimedia Commons MediaWiki API Adapter
    # -------------------------------------------------------------------------
    def test_08_wikimedia_media_adapter(self):
        adapter = wiki_mod.WikimediaMediaAdapter()

        # Health & Config
        hc = adapter.health_check()
        self.assertTrue(hc["healthy"])
        self.assertGreaterEqual(hc["verified_commons_assets"], 4)
        vc = adapter.validate_configuration()
        self.assertTrue(vc["valid"])

        # Search Commons media
        search_res = adapter.search_commons_media(query="lion", limit=2)
        self.assertEqual(search_res["status"], "SUCCESS")
        self.assertGreaterEqual(search_res["results_count"], 1)
        m0 = search_res["media"][0]
        self.assertIn("page_url", m0)
        self.assertIn("author", m0)
        self.assertIn("license_short", m0)

        # Create verified provenance record with real URL and license
        prov_out = self.test_dir / "wiki_prov"
        prov_res = adapter.create_provenance_record(
            file_title=m0["file_title"],
            output_dir=str(prov_out)
        )
        self.assertEqual(prov_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(prov_res["provenance_file"]))
        with open(prov_res["provenance_file"], "r", encoding="utf-8") as f:
            prov_data = json.load(f)
        self.assertEqual(prov_data["source_type"], "WIKIMEDIA_COMMONS_OFFICIAL_API")
        self.assertIn("upload.wikimedia.org", prov_data["download_url"])

        # Rollback
        rb = adapter.rollback()
        self.assertEqual(rb["status"], "ROLLED_BACK")


if __name__ == "__main__":
    unittest.main()
