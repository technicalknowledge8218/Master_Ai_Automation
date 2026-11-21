"""subtitle_engine.py
MASTER-AI Automatic Subtitle Generator & Validator

Generates SRT and ASS (Advanced SubStation Alpha) subtitle files with full support for:
- Hindi Devanagari script
- English translations and transliterations
- Accurate scene-level and sentence-level timecodes
- Automated QA validation: detects overlaps, negative durations, out-of-range bounds, and excessive character speeds.
"""

import os
import sys
import re
from typing import Dict, Any, List, Optional, Tuple


def format_srt_time(seconds: float) -> str:
    """Formats float seconds into SRT timestamp: HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def format_ass_time(seconds: float) -> str:
    """Formats float seconds into ASS timestamp: H:MM:SS.cc"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{centis:02d}"


class SubtitleEngine:
    """Generates and validates multilingual subtitle tracks."""

    def __init__(self):
        pass

    def generate_srt(self, segments: List[Dict[str, Any]], output_path: str) -> Dict[str, Any]:
        """Generates a standard SubRip (.srt) subtitle file."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        lines = []

        for idx, seg in enumerate(segments, start=1):
            start_str = format_srt_time(seg["start_sec"])
            end_str = format_srt_time(seg["end_sec"])
            text = seg["text"].strip()
            lines.append(f"{idx}\n{start_str} --> {end_str}\n{text}\n")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "format": "SRT",
            "subtitle_path": output_path,
            "segment_count": len(segments),
            "file_size_bytes": os.path.getsize(output_path),
            "status": "SUCCESS"
        }

    def generate_ass(
        self,
        segments: List[Dict[str, Any]],
        output_path: str,
        title: str = "Master AI Documentary Subtitles"
    ) -> Dict[str, Any]:
        """Generates an Advanced SubStation Alpha (.ass) subtitle file with typography styling."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        header = f"""[Script Info]
Title: {title}
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00121212,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,60,1
Style: HindiDevanagari,Nirmala UI,52,&H00F5D547,&H000000FF,&H00101010,&H90000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        for seg in segments:
            start_str = format_ass_time(seg["start_sec"])
            end_str = format_ass_time(seg["end_sec"])
            text = seg["text"].replace("\n", " ").strip()
            style_name = "HindiDevanagari" if any("\u0900" <= c <= "\u097f" for c in text) else "Default"
            events.append(f"Dialogue: 0,{start_str},{end_str},{style_name},,0,0,0,,{text}")

        full_content = header + "\n".join(events) + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        return {
            "format": "ASS",
            "subtitle_path": output_path,
            "segment_count": len(segments),
            "file_size_bytes": os.path.getsize(output_path),
            "status": "SUCCESS"
        }

    def validate_subtitles(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Performs rigorous quality assurance on subtitle timing and readability."""
        errors = []
        warnings = []

        prev_end = -1.0
        for i, s in enumerate(segments, start=1):
            start = s.get("start_sec", 0.0)
            end = s.get("end_sec", 0.0)
            text = s.get("text", "").strip()

            if not text:
                errors.append(f"Segment #{i}: Subtitle text is empty.")

            if start < 0 or end < 0:
                errors.append(f"Segment #{i}: Negative timestamp detected ({start}s -> {end}s).")

            if start >= end:
                errors.append(f"Segment #{i}: Inverted or zero duration ({start}s -> {end}s).")

            if start < prev_end - 0.05:
                warnings.append(f"Segment #{i}: Timecode overlaps with previous segment by {round(prev_end - start, 2)}s.")

            # Reading speed check (characters per second)
            dur = end - start
            if dur > 0:
                cps = len(text) / dur
                if cps > 30.0:
                    warnings.append(f"Segment #{i}: Reading speed high ({round(cps, 1)} chars/sec).")

            prev_end = max(prev_end, end)

        passed = len(errors) == 0
        return {
            "valid": passed,
            "total_segments": len(segments),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": errors,
            "warnings": warnings,
            "status": "PASS" if passed else "FAIL"
        }

    def generate_from_scene_narration(
        self,
        scene_narrations: List[Dict[str, Any]],
        max_video_duration: float,
        srt_output_path: str,
        ass_output_path: str
    ) -> Dict[str, Any]:
        """Builds and validates SRT and ASS files from real scene narration timing records."""
        segments = []
        for sn in scene_narrations:
            scene_offset = sn.get("timeline_start_sec", 0.0)
            boundaries = sn.get("sentence_boundaries", [])
            text = sn.get("text", "")
            duration = sn.get("duration_sec", 10.0)

            if boundaries:
                for b in boundaries:
                    b_start = min(max_video_duration - 0.2, round(scene_offset + b["offset_sec"], 3))
                    b_end = min(max_video_duration, round(scene_offset + b["offset_sec"] + b["duration_sec"], 3))
                    if b_end > b_start:
                        segments.append({
                            "start_sec": b_start,
                            "end_sec": b_end,
                            "text": b.get("text", text)
                        })
            else:
                s_start = min(max_video_duration - 1.0, round(scene_offset + 0.5, 3))
                s_end = min(max_video_duration, round(scene_offset + duration - 0.5, 3))
                if s_end > s_start:
                    segments.append({
                        "start_sec": s_start,
                        "end_sec": s_end,
                        "text": text
                    })

        segments.sort(key=lambda x: x["start_sec"])
        cleaned = []
        last_end = 0.0
        for seg in segments:
            st = max(last_end, seg["start_sec"])
            en = max(st + 0.5, seg["end_sec"])
            if en <= max_video_duration:
                cleaned.append({"start_sec": st, "end_sec": en, "text": seg["text"]})
                last_end = en

        val = self.validate_subtitles(cleaned)
        srt_res = self.generate_srt(cleaned, srt_output_path)
        ass_res = self.generate_ass(cleaned, ass_output_path)
        return {
            "srt": srt_res,
            "ass": ass_res,
            "validation": val,
            "segment_count": len(cleaned)
        }
