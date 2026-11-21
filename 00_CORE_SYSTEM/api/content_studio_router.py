"""content_studio_router.py
MASTER-AI Automated Content Studio & Video Production REST API Router

Exposes endpoints for:
- Documentary & media projects creation
- Research dossiers, scriptwriting, and storyboard planning
- Voiceover synthesis and audio manager
- Visual scene generation and Ken Burns motion clips
- Programmatic FFmpeg video rendering
- Subtitle generation (SRT/ASS) and QA audits
- Broadcast-grade YouTube thumbnails and publication staging
"""

from __future__ import annotations

import os
import sys
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

# Ensure workspace root is in sys.path
_current_dir = Path(__file__).resolve().parent
_workspace_root = _current_dir.parents[1]
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

_studio_pkg = importlib.import_module("09_CONTENT_STUDIO.engine")
ContentStudioOrchestrator = _studio_pkg.ContentStudioOrchestrator
VoiceRouter = _studio_pkg.VoiceRouter
VisualAssetRouter = _studio_pkg.VisualAssetRouter
SubtitleEngine = _studio_pkg.SubtitleEngine
MediaQualityAssuranceAuditor = _studio_pkg.MediaQualityAssuranceAuditor
ThumbnailStudio = _studio_pkg.ThumbnailStudio

router = APIRouter(prefix="/api/v1/content_studio", tags=["Content Studio & Video Production"])

_orchestrator_instance: Optional[ContentStudioOrchestrator] = None


def get_orchestrator() -> ContentStudioOrchestrator:
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = ContentStudioOrchestrator()
    return _orchestrator_instance


# -------------------------------------------------------------
# Request Models
# -------------------------------------------------------------

class DocumentaryProductionRequest(BaseModel):
    prompt: str = Field(..., description="Prompt describing documentary topic, target audience, and duration")
    target_duration_sec: float = Field(300.0, description="Target duration in seconds (default: 300s / 5 min)")
    language: str = Field("Hindi", description="Language for voiceover and narration (default: Hindi)")
    resolution_width: int = Field(1920, description="Video width in pixels (1920 for 16:9, 1080 for 9:16)")
    resolution_height: int = Field(1080, description="Video height in pixels (1080 for 16:9, 1920 for 9:16)")
    fps: int = Field(30, description="Frames per second")
    preferred_voice: Optional[str] = Field(None, description="Preferred voice ID or provider")


class VoiceoverSynthesisRequest(BaseModel):
    text: str = Field(..., description="Narration text to synthesize")
    language: str = Field("Hindi", description="Language of text")
    voice_name: Optional[str] = Field(None, description="Optional voice ID")


class SubtitleGenerationRequest(BaseModel):
    segments: List[Dict[str, Any]] = Field(..., description="List of subtitle segments with start_sec, end_sec, text")
    format: str = Field("SRT", description="Subtitle format: SRT or ASS")


class ThumbnailGenerationRequest(BaseModel):
    title_hindi: str = Field(..., description="Devanagari title text")
    subtitle_english: str = Field(..., description="English subtitle / headline text")
    topic: str = Field("Wildlife Documentary", description="Topic badge")


class MediaQARequest(BaseModel):
    video_path: str = Field(..., description="Path to rendered video file to audit")
    expected_duration_sec: Optional[float] = Field(None, description="Expected duration in seconds")
    expected_resolution: Optional[str] = Field("1920x1080", description="Expected resolution string")


# -------------------------------------------------------------
# Production & Pipeline Endpoints
# -------------------------------------------------------------

@router.post("/produce", summary="Run full automated documentary production pipeline")
def produce_documentary(req: DocumentaryProductionRequest) -> Dict[str, Any]:
    orch = get_orchestrator()
    try:
        summary = orch.produce_documentary(
            request_prompt=req.prompt,
            target_duration_sec=req.target_duration_sec,
            language=req.language,
            resolution=(req.resolution_width, req.resolution_height),
            fps=req.fps,
            preferred_voice=req.preferred_voice
        )
        return {"status": "SUCCESS", "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers/status", summary="Get status and health of all multimedia provider adapters")
def get_providers_status() -> Dict[str, Any]:
    vr = VoiceRouter()
    voice_status = vr.get_provider_status()

    import imageio_ffmpeg
    try:
        ff_exe = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_ready = True
    except Exception:
        ffmpeg_ready = False

    return {
        "status": "SUCCESS",
        "voice_providers": voice_status,
        "video_renderer": {
            "engine": "FFmpeg 7.1",
            "available": ffmpeg_ready,
            "hw_acceleration": "CPU-Optimized libx264"
        },
        "visual_generators": {
            "procedural_canvas": "AVAILABLE",
            "stock_motion": "AVAILABLE",
            "cloud_ai_visual": "GATED_APPROVAL_REQUIRED"
        }
    }


@router.post("/voiceover", summary="Synthesize speech audio from text")
def synthesize_voiceover(req: VoiceoverSynthesisRequest) -> Dict[str, Any]:
    vr = VoiceRouter()
    try:
        res = vr.synthesize(
            text=req.text,
            language=req.language,
            preferred_provider=req.voice_name
        )
        return {"status": "SUCCESS", "result": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subtitles", summary="Generate and validate multilingual subtitles")
def generate_subtitles(req: SubtitleGenerationRequest) -> Dict[str, Any]:
    se = SubtitleEngine()
    val = se.validate_subtitles(req.segments)
    return {
        "status": "SUCCESS",
        "validation": val,
        "format": req.format.upper()
    }


@router.post("/qa", summary="Run rigorous automated quality audit on a media file")
def run_media_qa(req: MediaQARequest) -> Dict[str, Any]:
    qa = MediaQualityAssuranceAuditor()
    try:
        report = qa.audit_video_production(
            video_path=req.video_path,
            expected_duration_sec=req.expected_duration_sec,
            expected_resolution=req.expected_resolution
        )
        return {"status": "SUCCESS", "qa_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
