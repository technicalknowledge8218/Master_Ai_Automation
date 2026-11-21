"""Master AI - Phase 1 Foundational Infrastructure Smoke Test Suite.

Verifies end-to-end functionality of:
1. Python 3.14 Runtime & Architecture
2. FastAPI Application & TestClient Health Routing
3. Qdrant In-Memory Vector Operations (Collection, Ingestion, Query)
4. LiteLLM Gateway Initialization & Offline Mock Handling
5. Portable FFmpeg 7.1 Binary Execution
6. Ollama Local Daemon Connectivity (Native Windows)
7. Package Audit & WDAC Application Control Policy Check
"""

from __future__ import annotations

import importlib.metadata
import os
import platform
import sys
import unittest
import urllib.request
import json
from pathlib import Path

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


class TestPhase1Foundation(unittest.TestCase):
    """Rigorous verification suite for Phase 1 foundational infrastructure."""

    def test_01_python_runtime_environment(self) -> None:
        """Verify Python version 3.14.x on 64-bit Windows architecture."""
        self.assertEqual(sys.version_info.major, 3)
        self.assertEqual(sys.version_info.minor, 14)
        self.assertEqual(platform.system(), "Windows")
        self.assertIn("64", platform.architecture()[0])
        print(f"\n[PASS] Python Runtime: {sys.version.split()[0]} on {platform.system()} ({platform.machine()})")

    def test_02_fastapi_and_testclient(self) -> None:
        """Verify FastAPI app instantiation and TestClient health routing."""
        from fastapi import FastAPI
        from starlette.testclient import TestClient

        app = FastAPI(title="Master AI Foundation API")

        @app.get("/health")
        def health_check() -> dict[str, str]:
            return {"status": "healthy", "architecture": "master-ai-cpu-first"}

        client = TestClient(app)
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("architecture"), "master-ai-cpu-first")

        fastapi_ver = importlib.metadata.version("fastapi")
        print(f"[PASS] FastAPI {fastapi_ver}: Health routing and TestClient verified.")

    def test_03_qdrant_vector_memory(self) -> None:
        """Verify Qdrant embedded client collection creation, insertion, and query."""
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, PointStruct, VectorParams

        client = QdrantClient(location=":memory:")
        collection_name = "test_memory_phase1"

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=4, distance=Distance.COSINE),
        )

        test_points = [
            PointStruct(
                id=1,
                vector=[0.1, 0.2, 0.3, 0.4],
                payload={"tag": "system_prompt", "agent": "orchestrator"},
            ),
            PointStruct(
                id=2,
                vector=[0.9, 0.8, 0.7, 0.6],
                payload={"tag": "code_snippet", "agent": "coding_specialist"},
            ),
        ]
        client.upsert(collection_name=collection_name, points=test_points)

        results = client.query_points(
            collection_name=collection_name,
            query=[0.1, 0.2, 0.3, 0.4],
            limit=1,
        )

        self.assertGreater(len(results.points), 0)
        top_match = results.points[0]
        self.assertEqual(top_match.id, 1)
        self.assertEqual(top_match.payload.get("agent"), "orchestrator")

        qdrant_ver = importlib.metadata.version("qdrant-client")
        print(f"[PASS] Qdrant Client {qdrant_ver}: In-memory collection, ingestion, and cosine search verified.")

    def test_04_litellm_gateway(self) -> None:
        """Verify LiteLLM gateway initialization and model resolution."""
        import litellm

        self.assertTrue(hasattr(litellm, "completion"))
        self.assertTrue(hasattr(litellm, "embedding"))

        # Verify offline mock completion capability
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Ping"}],
            mock_response="Master AI Foundation Operational",
        )
        content = response.choices[0].message.content
        self.assertIn("Master AI Foundation Operational", content)

        litellm_ver = importlib.metadata.version("litellm")
        print(f"[PASS] LiteLLM {litellm_ver}: Mock provider execution verified.")

    def test_05_portable_ffmpeg_runner(self) -> None:
        """Verify the portable FFmpeg runner executes and returns version info."""
        import importlib
        ffmpeg_runner = importlib.import_module("16_VIDEO_LIBRARY.tools.ffmpeg_runner")
        get_ffmpeg_version = ffmpeg_runner.get_ffmpeg_version
        is_ffmpeg_available = ffmpeg_runner.is_ffmpeg_available
        resolve_ffmpeg_path = ffmpeg_runner.resolve_ffmpeg_path
        run_ffmpeg = ffmpeg_runner.run_ffmpeg

        self.assertTrue(is_ffmpeg_available(), "FFmpeg binary must be available.")
        exe_path = resolve_ffmpeg_path()
        self.assertIsNotNone(exe_path)
        self.assertTrue(exe_path.is_file())

        version_str = get_ffmpeg_version()
        self.assertIn("ffmpeg version 7.1", version_str)

        proc = run_ffmpeg(["-version"], timeout=10)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("configuration:", proc.stdout)

        print(f"[PASS] FFmpeg 7.1: Portable execution verified at {exe_path.name}.")

    def test_06_ollama_local_daemon(self) -> None:
        """Verify local Ollama daemon connectivity on http://127.0.0.1:11434."""
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            body = json.loads(resp.read().decode("utf-8"))
            self.assertIn("models", body)
            model_count = len(body.get("models", []))

        print(f"[PASS] Ollama Daemon: Responsive on 127.0.0.1:11434 ({model_count} models loaded).")

    def test_07_core_packages_wdac_audit(self) -> None:
        """Verify all essential Master AI libraries load without WDAC policy blocks."""
        packages_to_verify = [
            "fastapi",
            "uvicorn",
            "pydantic",
            "litellm",
            "qdrant_client",
            "mcp",
            "openai",
            "edge_tts",
            "PIL",
            "cv2",
            "numpy",
            "psutil",
        ]
        for pkg in packages_to_verify:
            mod = __import__(pkg)
            self.assertIsNotNone(mod)

        print(f"[PASS] WDAC Audit: {len(packages_to_verify)} core platform packages verified without DLL blocks.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
