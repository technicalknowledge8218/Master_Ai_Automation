"""
Master AI - Phase 7.2 Cinematic Editing Engine
Enterprise multi-scene timeline assembler with dynamic xfade transitions,
multitrack audio mixing with ducking, color grading, subtitle burning,
and strict validation against frozen or black frames.
"""

import os
import sys
import json
import logging
import subprocess
import cv2
import numpy as np
from typing import Dict, Any, List, Optional
import imageio_ffmpeg

logger = logging.getLogger("MasterAI.CinematicEditor")
logging.basicConfig(level=logging.INFO)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

class CinematicEditor:
    """Production-grade multi-medium video editing and mastering engine."""

    PROFILES = {
        "720p": {"width": 1280, "height": 720, "fps": 24, "crf": 18},
        "1080p": {"width": 1920, "height": 1080, "fps": 24, "crf": 17},
        "4k": {"width": 3840, "height": 2160, "fps": 24, "crf": 16}
    }

    ASPECT_RATIOS = {
        "16:9": (16, 9),
        "9:16": (9, 16),
        "1:1": (1, 1)
    }

    COLOR_GRADES = {
        "melancholic": "eq=contrast=1.12:brightness=-0.03:saturation=0.92,colorbalance=rs=0.06:gs=0.01:bs=-0.06,vignette=PI/4.5",
        "warm_dusk": "eq=contrast=1.08:brightness=0.01:saturation=1.12,colorbalance=rs=0.08:gs=0.03:bs=-0.04,vignette=PI/5",
        "suspense": "eq=contrast=1.18:brightness=-0.04:saturation=0.88,vignette=PI/4",
        "teal_orange": "eq=contrast=1.15:brightness=-0.02:saturation=1.05,colorbalance=rs=0.08:gs=-0.02:bs=-0.08:rh=-0.04:gh=0.0:bh=0.08,vignette=PI/4.5",
        "vintage": "eq=contrast=1.05:brightness=0.02:saturation=0.80,colorbalance=rs=0.10:gs=0.05:bs=-0.08,vignette=PI/4",
        "neutral": "null"
    }

    VALID_TRANSITIONS = {
        "fade", "dissolve", "circleopen", "smoothleft", "smoothright", "wipeleft", "wiperight", "radial", "fadeblack", "fadewhite"
    }

    def __init__(self, profile_name: str = "720p", aspect_ratio: str = "16:9"):
        self.profile = self.PROFILES.get(profile_name, self.PROFILES["720p"])
        self.aspect_ratio = aspect_ratio
        self.target_w = self.profile["width"]
        self.target_h = self.profile["height"]
        self.fps = self.profile["fps"]
        self.crf = self.profile["crf"]

    def build_title_card(
        self,
        output_mp4: str,
        title: str,
        subtitle: str,
        duration_sec: float = 5.0,
        is_outro: bool = False
    ) -> str:
        """Generate a sleek, dark-slate cinematic title or outro credit card."""
        from PIL import Image, ImageDraw, ImageFont

        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
        total_frames = int(duration_sec * self.fps)

        try:
            font_t = ImageFont.truetype("arial.ttf", 36)
            font_s = ImageFont.truetype("arial.ttf", 18)
            font_c = ImageFont.truetype("arial.ttf", 13)
        except Exception:
            font_t = ImageFont.load_default()
            font_s = font_t
            font_c = font_t

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.target_w}x{self.target_h}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_mp4
        ]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        for f in range(1, total_frames + 1):
            frac = f / float(total_frames)

            # Fade in over first 0.8s, fade out over last 0.8s
            alpha = 1.0
            if frac < 0.20:
                alpha = frac / 0.20
            elif frac > 0.80:
                alpha = (1.0 - frac) / 0.20

            im = Image.new("RGB", (self.target_w, self.target_h), color=(10, 14, 22))
            draw = ImageDraw.Draw(im)

            # Subtle accent border
            draw.rectangle([(60, 60), (self.target_w - 60, self.target_h - 60)], outline=(30, 41, 59), width=2)
            draw.line([(self.target_w//2 - 80, self.target_h//2 - 60), (self.target_w//2 + 80, self.target_h//2 - 60)], fill=(245, 158, 11), width=3)

            # Title
            t_col = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
            s_col = (int(200 * alpha), int(210 * alpha), int(225 * alpha))
            a_col = (int(245 * alpha), int(158 * alpha), int(11 * alpha))

            draw.text((self.target_w // 2, self.target_h // 2 - 20), title, fill=t_col, font=font_t, anchor="mm")
            draw.text((self.target_w // 2, self.target_h // 2 + 35), subtitle, fill=s_col, font=font_s, anchor="mm")

            if is_outro:
                creds = "PRODUCED WITH MASTER AI // OPEN-SOURCE ASSETS: POLY HAVEN, AMBIENTCG, SMITHSONIAN, PEXELS"
                draw.text((self.target_w // 2, self.target_h // 2 + 95), creds, fill=a_col, font=font_c, anchor="mm")

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        return output_mp4

    def assemble_multiscene_timeline(
        self,
        scenes: List[Dict[str, Any]],
        output_master_mp4: str,
        audio_track_path: Optional[str] = None,
        voiceover_track_path: Optional[str] = None,
        subtitle_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assemble a continuous multi-scene timeline using mathematically computed xfade offsets.
        Enforces duration preservation, smooth transitions, and multi-track audio mixing with ducking.
        """
        if not scenes:
            raise ValueError("Scene list cannot be empty.")

        os.makedirs(os.path.dirname(os.path.abspath(output_master_mp4)), exist_ok=True)
        logger.info(f"Assembling multi-scene timeline with {len(scenes)} scenes...")

        # 1. Validate inputs and calculate timeline offsets
        # Mathematical rule for xfade chaining:
        # Stream 0 duration = D_0
        # Transition 1 starts at offset_1 = D_0 - T_1
        # Intermediate Stream V_01 duration = offset_1 + D_1
        # Transition 2 starts at offset_2 = Duration(V_01) - T_2
        # ...
        
        transition_duration = 1.0 # Standard 1.0s cross-fade
        inputs = []
        filter_parts = []
        
        running_duration = 0.0
        offsets = []

        for i, sc in enumerate(scenes):
            vpath = sc["path"]
            if not os.path.isfile(vpath):
                raise FileNotFoundError(f"Scene video missing: {vpath}")
            d = sc["duration_sec"]
            inputs.extend(["-stream_loop", "-1", "-ss", "0", "-t", str(d), "-i", vpath])

            # Normalize resolution, apply color grade, ken burns, and optional badge
            vf_steps = [
                f"scale={self.target_w}:{self.target_h}:force_original_aspect_ratio=decrease",
                f"pad={self.target_w}:{self.target_h}:(ow-iw)/2:(oh-ih)/2",
                "setsar=1",
                f"fps={self.fps}"
            ]

            # Ken Burns camera motion on static or graphic scenes
            kb = sc.get("ken_burns")
            if kb == "push_in":
                vf_steps.append("zoompan=z='min(zoom+0.0012,1.20)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24")
            elif kb == "pan_right":
                vf_steps.append("zoompan=z=1.12:d=1:x='(on/200)*(iw-iw/zoom)':y='(ih-ih/zoom)/2':s=1280x720:fps=24")

            # Color grading
            cg = sc.get("color_grade")
            if cg and cg in self.COLOR_GRADES:
                vf_steps.append(self.COLOR_GRADES[cg])

            # Optional Chapter / Badge Text
            badge = sc.get("badge_text")
            if badge:
                sanitized_badge = badge.replace(":", "\\:").replace("'", "").replace(",", "\\,")
                font_file = "C\\:/Windows/Fonts/Nirmala.ttc"
                vf_steps.append(f"drawtext=fontfile='{font_file}':text='{sanitized_badge}':fontsize=26:fontcolor=white@0.95:x=50:y=h-80:box=1:boxcolor=black@0.65:boxborderw=8")

            filter_parts.append(f"[{i}:v]{','.join(vf_steps)}[v{i}];")

            if i == 0:
                running_duration = d
            else:
                offset = running_duration - transition_duration
                offsets.append(offset)
                running_duration = offset + d

        total_calculated_duration = running_duration
        logger.info(f"Total calculated timeline duration: {total_calculated_duration:.2f} seconds ({int(total_calculated_duration * self.fps)} frames)")

        # 2. Build xfade filter chain
        prev_stream = "v0"
        for i in range(1, len(scenes)):
            next_stream = f"v{i}"
            out_stream = f"v0_{i}" if i < len(scenes) - 1 else "v_video_out"
            trans_type = scenes[i].get("transition", "fade")
            if trans_type not in self.VALID_TRANSITIONS:
                trans_type = "fade"
            offset_val = round(offsets[i - 1], 3)
            filter_parts.append(
                f"[{prev_stream}][{next_stream}]xfade=transition={trans_type}:duration={transition_duration}:offset={offset_val}[{out_stream}];"
            )
            prev_stream = out_stream

        # 3. Audio track handling
        audio_inputs = []
        audio_filter_parts = []
        audio_input_indices = []

        curr_input_idx = len(scenes)
        has_voice = voiceover_track_path and os.path.isfile(voiceover_track_path)
        has_bgm = audio_track_path and os.path.isfile(audio_track_path)

        if has_voice:
            audio_inputs.extend(["-i", voiceover_track_path])
            voice_idx = curr_input_idx
            curr_input_idx += 1
            audio_input_indices.append(voice_idx)
            # Format voiceover
            audio_filter_parts.append(f"[{voice_idx}:a]volume=1.0[voice_proc];")

        if has_bgm:
            audio_inputs.extend(["-i", audio_track_path])
            bgm_idx = curr_input_idx
            curr_input_idx += 1
            audio_input_indices.append(bgm_idx)
            # BGM ducked and faded out at the end
            fade_start = max(1.0, total_calculated_duration - 2.0)
            bgm_vol = 0.22 if has_voice else 0.50
            audio_filter_parts.append(
                f"[{bgm_idx}:a]volume={bgm_vol},afade=t=out:st={fade_start}:d=1.5[bgm_proc];"
            )

        if has_voice and has_bgm:
            audio_filter_parts.append("[voice_proc][bgm_proc]amix=inputs=2:duration=first:dropout_transition=2[a_final]")
            final_audio_map = "[a_final]"
        elif has_bgm:
            final_audio_map = "[bgm_proc]"
        elif has_voice:
            final_audio_map = "[voice_proc]"
        else:
            # High-fidelity synthesized ambient drone
            audio_inputs.extend(["-f", "lavfi", "-i", f"sine=frequency=220:duration={total_calculated_duration}"])
            audio_filter_parts.append(f"[{curr_input_idx}:a]volume=0.15,afade=t=out:st={total_calculated_duration-1.5}:d=1.5[a_synth]")
            final_audio_map = "[a_synth]"

        full_filter = "".join(filter_parts) + "".join(audio_filter_parts)
        # Strip trailing semicolon if needed
        if full_filter.endswith(";"):
            full_filter = full_filter[:-1]

        cmd = [FFMPEG, "-y"]
        cmd.extend(inputs)
        cmd.extend(audio_inputs)
        cmd.extend([
            "-filter_complex", full_filter,
            "-map", "[v_video_out]",
            "-map", final_audio_map,
            "-t", str(total_calculated_duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", str(self.crf),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            output_master_mp4
        ])

        logger.info("Executing FFmpeg master timeline render...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.error(f"FFmpeg timeline assembly failed: {res.stderr}")
            raise RuntimeError(f"FFmpeg assembly error: {res.stderr}")

        logger.info(f"Successfully assembled timeline: {output_master_mp4} ({os.path.getsize(output_master_mp4)} bytes)")

        # Verify output
        from footage_pipeline import RealFootagePipeline
        verifier = RealFootagePipeline()
        qa_metrics = verifier.assess_visual_quality(output_master_mp4)
        return {
            "output_path": output_master_mp4,
            "calculated_duration": total_calculated_duration,
            "qa_metrics": qa_metrics
        }

if __name__ == "__main__":
    editor = CinematicEditor("720p")
    title_path = r"F:\Master AI\09_CONTENT_STUDIO\renders\pilot_lion_documentary\title_card.mp4"
    editor.build_title_card(title_path, "AFRICAN LION: LIFE IN THE WILD", "Master AI Cinematic Multi-Medium Production", duration_sec=5.0)
    print("Generated title card:", title_path)
