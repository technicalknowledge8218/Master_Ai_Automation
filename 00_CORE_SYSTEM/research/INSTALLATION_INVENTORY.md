# MASTER AI — INSTALLATION INVENTORY (PHASE 6.5)

**Generated:** 2026-11-17  
**Environment:** Windows 11 Enterprise (AMD64), Python 3.14.0, FFmpeg 7.1  
**Virtual Environment:** `F:\Master AI\.venv`  

---

## 1. System Packages and Virtual Environment Dependencies

| Package Name | Installed Version | Source / Wheel | Purpose | License |
|---|---|---|---|---|
| `faster-whisper` | `1.2.1` | PyPI (pure Python) | Speech recognition interface & VAD | MIT |
| `ctranslate2` | `4.9.0` | PyPI (Windows AMD64 wheel) | C++ fast inference engine (INT8 quantization) | MIT |
| `onnxruntime` | `1.32.0` | PyPI (Windows AMD64 wheel) | ONNX Runtime backend for Silero VAD | MIT |
| `av` (PyAV) | `19.0.2` | PyPI (Windows AMD64 wheel) | Native FFmpeg bindings for audio decoding | BSD-2-Clause |
| `tokenizers` | `0.22.1` | PyPI (Windows AMD64 wheel) | HuggingFace fast tokenization | Apache-2.0 |
| `huggingface-hub` | `1.14.0` | PyPI (pure Python) | Model weights caching & revision pinning | Apache-2.0 |
| `edge-tts` | `6.1.19` | PyPI (pure Python) | Neural TTS voiceover synthesis | LGPL-3.0 |
| `imageio-ffmpeg` | `0.6.0` | PyPI (pure Python) | Bundled static FFmpeg 7.1 executable | Apache-2.0 |
| `pillow` | `11.1.0` | PyPI (Windows AMD64 wheel) | Image synthesis & title rendering | HPND |
| `numpy` | `2.2.3` | PyPI (Windows AMD64 wheel) | Audio array and waveform processing | BSD-3-Clause |
| `qdrant-client` | `1.13.2` | PyPI (pure Python) | Local vector storage engine | Apache-2.0 |
| `pydantic` | `2.10.6` | PyPI (Windows AMD64 wheel) | Data validation & schemas | MIT |

---

## 2. Integrated Adapter Modules Inventory

| Adapter Name | Module File Path | Target Repository / Service | Version | Health Status |
|---|---|---|---|---|
| `FreeLLMAdapter` | `00_CORE_SYSTEM/discovery_engine/free_llm_adapter.py` | `nejib1/Free-LLM` | `1.0.0` | `HEALTHY` |
| `OmniRouteGatewayAdapter` | `04_LLM_AND_AI/gateways/omniroute_adapter.py` | `cheaper-inference/OmniRoute` | `1.0.0` | `HEALTHY` |
| `FireRedStorylineAdapter` | `09_CONTENT_STUDIO/engine/firered_storyline_adapter.py` | `FireRedTeam/FireRed-OpenStoryline` | `1.0.0` | `HEALTHY` |
| `OpenFilmAdapter` | `09_CONTENT_STUDIO/engine/openfilm_adapter.py` | `openfilm/openfilm` | `1.0.0` | `HEALTHY` |
| `WhisperTranscriptionAdapter` | `09_CONTENT_STUDIO/engine/whisper_transcription_adapter.py` | `SYSTRAN/faster-whisper` | `1.2.1` | `HEALTHY` |
| `SocialdropPublishingAdapter` | `10_SOCIAL_MEDIA/publishers/socialdrop_adapter.py` | `txrbgy/socialdrop` | `1.0.0` | `HEALTHY` |
| `PexelsMediaAdapter` | `09_CONTENT_STUDIO/engine/pexels_media_adapter.py` | `Pexels Video API v1` | `1.0.0` | `HEALTHY` |
| `WikimediaMediaAdapter` | `09_CONTENT_STUDIO/engine/wikimedia_media_adapter.py` | `MediaWiki Official Commons API` | `1.0.0` | `HEALTHY` |

---

## 3. Storage and Directory Allocations

- **Documentaries Output:** `F:\Master AI\09_CONTENT_STUDIO\documentaries\`
- **Staged Publications:** `F:\Master AI\10_SOCIAL_MEDIA\staged_publications\`
- **OpenFilm Projects:** `F:\Master AI\09_CONTENT_STUDIO\openfilm_projects\`
- **Stock Assets & Provenance:** `F:\Master AI\09_CONTENT_STUDIO\stock_assets\`
- **Whisper Cache:** `<USER_HOME>\.cache\huggingface\hub\models--Systran--faster-whisper-tiny` (~75 MB INT8 weights)
- **Snapshots & Backups:** `F:\Master AI\23_CHANGELOG_AND_BACKUP\snapshots\`
