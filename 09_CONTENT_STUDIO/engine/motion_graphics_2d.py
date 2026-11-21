"""
Master AI - Phase 7.2 Professional 2D Motion Graphics Engine
Generates broadcast-grade animated maps, infographics, scientific charts,
kinetic typography, and title sequences with sub-pixel anti-aliasing
and high-speed streaming direct to FFmpeg.
"""

import os
import sys
import math
import subprocess
import json
import logging
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

logger = logging.getLogger("MasterAI.2D.MotionGraphics")
logging.basicConfig(level=logging.INFO)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

class MotionGraphics2DEngine:
    """Production 2D motion graphics and vector animation engine."""

    def __init__(self, res_x: int = 1280, res_y: int = 720, fps: int = 24):
        self.res_x = res_x
        self.res_y = res_y
        self.fps = fps
        self.font_large = self._load_font(32)
        self.font_title = self._load_font(24)
        self.font_body = self._load_font(16)
        self.font_mono = self._load_font(13)

    def _load_font(self, size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()

    def _load_hindi_font(self, size: int) -> ImageFont.ImageFont:
        candidates = [
            "C:/Windows/Fonts/Nirmala.ttc",
            "C:/Windows/Fonts/nirmala.ttf",
            "C:/Windows/Fonts/mangal.ttf",
            "C:/Windows/Fonts/arial.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
        return self._load_font(size)

    def render_territory_map_animation(
        self,
        output_mp4: str,
        duration_sec: float = 6.0,
        title: str = "AFRICAN LION — TERRITORIAL RANGE & SANCTUARIES"
    ) -> str:
        """
        Generate an animated geographic map illustrating lion habitat reduction
        and pride territory boundaries with kinetic typography and vector radars.
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
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

        # Simplified continent outline points (normalized 0..1 centered on Africa)
        # Scaled to canvas coordinates
        cx, cy = 640, 370
        scale = 320

        # Africa stylized polyline
        africa_poly = [
            (cx - 0.55 * scale, cy - 0.70 * scale), # Morocco
            (cx + 0.10 * scale, cy - 0.75 * scale), # Egypt
            (cx + 0.65 * scale, cy - 0.25 * scale), # Horn of Africa
            (cx + 0.50 * scale, cy + 0.20 * scale), # East Africa / Serengeti
            (cx + 0.35 * scale, cy + 0.75 * scale), # South Africa / Kruger
            (cx + 0.15 * scale, cy + 0.82 * scale), # Cape
            (cx - 0.20 * scale, cy + 0.50 * scale), # Namibia
            (cx - 0.45 * scale, cy + 0.05 * scale), # Congo Basin
            (cx - 0.75 * scale, cy - 0.25 * scale), # West Africa bulge
            (cx - 0.60 * scale, cy - 0.60 * scale)  # Return to NW
        ]

        # Key sanctuaries coordinates (Serengeti, Okavango, Kruger)
        sanctuaries = [
            {"name": "Serengeti / Mara", "pos": (cx + 0.42 * scale, cy + 0.15 * scale), "sqkm": "30,000 km²"},
            {"name": "Okavango Delta", "pos": (cx + 0.18 * scale, cy + 0.52 * scale), "sqkm": "15,000 km²"},
            {"name": "Kruger National Park", "pos": (cx + 0.32 * scale, cy + 0.68 * scale), "sqkm": "19,485 km²"}
        ]

        for f in range(1, total_frames + 1):
            frac = f / float(total_frames)
            t = f / float(self.fps)

            # Dark slate technical UI background
            im = Image.new("RGB", (self.res_x, self.res_y), color=(15, 23, 42))
            draw = ImageDraw.Draw(im)

            # 1. Subtle grid lines
            for gx in range(0, self.res_x, 80):
                draw.line([(gx, 0), (gx, self.res_y)], fill=(28, 41, 65), width=1)
            for gy in range(0, self.res_y, 80):
                draw.line([(gx, 0), (gx, self.res_y)], fill=(28, 41, 65), width=1)

            # 2. Header Bar & Kinetic Typography
            draw.rectangle([(0, 0), (self.res_x, 65)], fill=(24, 34, 53))
            draw.line([(0, 65), (self.res_x, 65)], fill=(56, 189, 248), width=2)

            slide_in = min(1.0, f / 18.0)
            title_x = int(35 + (1.0 - slide_in) * -120)
            draw.text((title_x, 18), title, fill=(240, 245, 255), font=self.font_title)
            draw.text((self.res_x - 280, 22), f"TIMECODE: 00:0{int(t)}:{int((t%1)*24):02d} // 24 FPS", fill=(148, 163, 184), font=self.font_mono)

            # 3. Draw Stylized Continent Outline
            draw.polygon(africa_poly, fill=(20, 30, 48), outline=(71, 85, 105))

            # 4. Historical Range (Animated shrinking perimeter)
            shrink_progress = min(1.0, max(0.0, (frac - 0.15) / 0.50))
            hist_color = (180, 83, 9, int(160 * (1.0 - shrink_progress * 0.7)))
            draw.polygon(africa_poly, outline=hist_color, width=3)

            # 5. Protected Sanctuary Focal Rings & Pulse
            pulse_rad = 8 + 6 * math.sin(t * 4.5)
            for s in sanctuaries:
                sx, sy = s["pos"]
                draw.ellipse([(sx - pulse_rad, sy - pulse_rad), (sx + pulse_rad, sy + pulse_rad)], outline=(245, 158, 11), width=2)
                draw.ellipse([(sx - 4, sy - 4), (sx + 4, sy + 4)], fill=(239, 68, 68))
                
                # Annotations card
                if frac > 0.25:
                    draw.rectangle([(sx + 15, sy - 14), (sx + 210, sy + 18)], fill=(30, 41, 59, 220), outline=(56, 189, 248))
                    draw.text((sx + 22, sy - 12), s["name"], fill=(255, 255, 255), font=self.font_body)
                    draw.text((sx + 22, sy + 3), f"Protected Area: {s['sqkm']}", fill=(148, 163, 184), font=self.font_mono)

            # 6. Sidebar Legend & Telemetry Card
            lx, ly = 45, 100
            draw.rectangle([(lx, ly), (lx + 280, ly + 220)], fill=(24, 34, 53, 230), outline=(51, 65, 85))
            draw.text((lx + 15, ly + 14), "GEOSPATIAL METRICS", fill=(56, 189, 248), font=self.font_body)
            draw.line([(lx + 15, ly + 36), (lx + 265, ly + 36)], fill=(51, 65, 85), width=1)

            draw.text((lx + 15, ly + 48), "• Historic Range: 100%", fill=(203, 213, 225), font=self.font_mono)
            draw.text((lx + 15, ly + 72), f"• Current Range: {max(8, int(100 - shrink_progress * 92))}%", fill=(239, 68, 68), font=self.font_mono)
            draw.text((lx + 15, ly + 96), "• Primary Biome: Savanna / Scrub", fill=(203, 213, 225), font=self.font_mono)
            draw.text((lx + 15, ly + 120), "• Habitat Fragmentation: Severe", fill=(245, 158, 11), font=self.font_mono)
            draw.text((lx + 15, ly + 144), "• Pride Density: 1 / 50-100 km²", fill=(56, 189, 248), font=self.font_mono)
            draw.text((lx + 15, ly + 168), "• Status: IUCN Vulnerable", fill=(239, 68, 68), font=self.font_mono)

            # 7. Progress Bar at bottom
            draw.rectangle([(0, self.res_y - 6), (int(self.res_x * frac), self.res_y)], fill=(56, 189, 248))

            # Clean fade-out over last 0.5s
            if frac > 0.90:
                fade = (frac - 0.90) / 0.10
                black_overlay = Image.new("RGB", (self.res_x, self.res_y), color=(0, 0, 0))
                im = Image.blend(im, black_overlay, fade)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Territory Map animation rendered to: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_biology_infographic_animation(
        self,
        output_mp4: str,
        duration_sec: float = 6.0,
        title: str = "PANTHERA LEO — APEX BIOLOGY & SOCIAL STRUCTURE"
    ) -> str:
        """
        Generate an animated scientific infographic detailing lion bite force,
        sprint velocity, and pride coalition dynamics.
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
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
            t = f / float(self.fps)

            im = Image.new("RGB", (self.res_x, self.res_y), color=(15, 23, 42))
            draw = ImageDraw.Draw(im)

            # Header
            draw.rectangle([(0, 0), (self.res_x, 65)], fill=(24, 34, 53))
            draw.line([(0, 65), (self.res_x, 65)], fill=(245, 158, 11), width=2)
            draw.text((35, 18), title, fill=(240, 245, 255), font=self.font_title)
            draw.text((self.res_x - 280, 22), "SCIENTIFIC BIOLOGY INFOGRAPHIC", fill=(148, 163, 184), font=self.font_mono)

            # Three scientific cards across the screen
            cards = [
                {"title": "BITE FORCE QUOTIENT", "val": "650 PSI", "desc": "Canine bone-crushing leverage designed for large ungulate prey.", "progress": min(1.0, frac * 1.5)},
                {"title": "SPRINT VELOCITY", "val": "80 KM/H", "desc": "Explosive short-burst acceleration across 100-200 meters.", "progress": min(1.0, frac * 1.8)},
                {"title": "PRIDE COALITION", "val": "2-4 MALES", "desc": "Defends pride territory spanning 100+ km² from rival nomadic coalitions.", "progress": min(1.0, frac * 1.2)}
            ]

            card_w = 360
            card_h = 320
            start_x = 45
            gap = 40

            for idx, c in enumerate(cards):
                cx = start_x + idx * (card_w + gap)
                cy = 130

                draw.rectangle([(cx, cy), (cx + card_w, cy + card_h)], fill=(24, 34, 53), outline=(51, 65, 85))
                draw.rectangle([(cx, cy), (cx + card_w, cy + 45)], fill=(30, 41, 59))
                draw.text((cx + 18, cy + 14), c["title"], fill=(245, 158, 11), font=self.font_body)

                # Hero Big Metric
                draw.text((cx + 25, cy + 70), c["val"], fill=(255, 255, 255), font=self.font_large)

                # Animated Gauge Bar
                bar_y = cy + 140
                draw.rectangle([(cx + 25, bar_y), (cx + card_w - 25, bar_y + 14)], fill=(15, 23, 42), outline=(51, 65, 85))
                bar_fill = int((card_w - 50) * c["progress"])
                draw.rectangle([(cx + 25, bar_y), (cx + 25 + bar_fill, bar_y + 14)], fill=(56, 189, 248))

                # Descriptive Body
                draw.text((cx + 25, cy + 180), c["desc"], fill=(203, 213, 225), font=self.font_body)
                draw.text((cx + 25, cy + 240), f"TELEMETRY SAMPLE: {int(c['progress']*100)}%", fill=(148, 163, 184), font=self.font_mono)

            # Footer telemetry readout
            draw.rectangle([(45, 500), (self.res_x - 45, 660)], fill=(20, 30, 48), outline=(51, 65, 85))
            draw.text((65, 518), "PHYSIOLOGICAL CLASSIFICATION // PANTHERA LEO", fill=(56, 189, 248), font=self.font_body)
            draw.text((65, 548), "• Kingdom: Animalia | Phylum: Chordata | Class: Mammalia | Order: Carnivora | Family: Felidae", fill=(203, 213, 225), font=self.font_mono)
            draw.text((65, 574), "• Average Mass: Male 190 kg (420 lb) | Female 130 kg (280 lb)", fill=(203, 213, 225), font=self.font_mono)
            draw.text((65, 600), "• Ecological Role: Keystroke Apex Predator regulating herbivore population balance", fill=(203, 213, 225), font=self.font_mono)
            draw.text((65, 626), "• Social Dynamic: Only truly social felid living in matriarchal family groups", fill=(245, 158, 11), font=self.font_mono)

            # Fade out
            if frac > 0.90:
                fade = (frac - 0.90) / 0.10
                black_overlay = Image.new("RGB", (self.res_x, self.res_y), color=(0, 0, 0))
                im = Image.blend(im, black_overlay, fade)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Biology Infographic animation rendered to: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_letter_unfolding_animation(
        self,
        output_mp4: str,
        duration_sec: float = 8.0,
        recipient_name: str = "मेरे प्यारे बेटे रोहित के लिए..."
    ) -> str:
        """
        Renders a cinematic aged parchment letter unfolding with progressive
        handwritten Devanagari Hindi text reveal and emotional styling.
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
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

        h_title = self._load_hindi_font(30)
        h_body = self._load_hindi_font(20)
        h_sub = self._load_hindi_font(16)

        lines = [
            (0.12, "जब यह पत्र तुम्हारे हाथों में होगा, मैं शायद इस दुनिया में नहीं होऊँगी।"),
            (0.32, "माफ़ करना, मैंने अपनी बीमारी तुमसे छुपाई ताकि तुम्हारी पढ़ाई और सपने न टूटें।"),
            (0.52, "पैतृक घर गिरवी रखकर तुम्हारी कॉलेज फीस भरी... तुम्हारी सफलता ही मेरी अंतिम जीत है।"),
            (0.72, "सदा सिर उठाकर जीना और दूसरों का सहारा बनना... तुम्हारी असीम प्यार करने वाली माँ।")
        ]

        for i in range(total_frames):
            frac = i / float(total_frames)
            im = Image.new("RGB", (self.res_x, self.res_y), color=(18, 16, 22))
            draw = ImageDraw.Draw(im)

            pw, ph = 840, 520
            px = (self.res_x - pw) // 2
            py = (self.res_y - ph) // 2

            # Drop shadow
            draw.rectangle([(px + 12, py + 12), (px + pw + 12, py + ph + 12)], fill=(8, 7, 10))
            # Aged parchment background
            draw.rectangle([(px, py), (px + pw, py + ph)], fill=(242, 234, 214), outline=(180, 160, 130), width=2)
            draw.rectangle([(px + 14, py + 14), (px + pw - 14, py + ph - 14)], outline=(210, 192, 165), width=1)

            # Header title
            draw.text((px + 45, py + 35), recipient_name, fill=(85, 40, 25), font=h_title)
            draw.line([(px + 45, py + 85), (px + pw - 45, py + 85)], fill=(170, 140, 110), width=1)

            cur_y = py + 125
            for threshold, line_text in lines:
                if frac >= threshold:
                    line_progress = min(1.0, (frac - threshold) / 0.16)
                    chars_to_show = int(len(line_text) * line_progress)
                    draw.text((px + 50, cur_y), line_text[:chars_to_show], fill=(40, 28, 22), font=h_body)
                cur_y += 65

            # Vintage seal mark at bottom right
            seal_x, seal_y = px + pw - 140, py + ph - 85
            draw.ellipse([(seal_x, seal_y), (seal_x + 60, seal_y + 60)], outline=(160, 60, 45), width=2)
            draw.text((seal_x + 10, seal_y + 18), "माँ", fill=(160, 60, 45), font=h_sub)

            # Fade out
            if frac > 0.90:
                fade = (frac - 0.90) / 0.10
                black_overlay = Image.new("RGB", (self.res_x, self.res_y), color=(0, 0, 0))
                im = Image.blend(im, black_overlay, fade)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Letter Unfolding animation rendered to: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_sacrifice_memory_timeline_animation(
        self,
        output_mp4: str,
        duration_sec: float = 8.0,
        title: str = "THE UNSEEN SACRIFICE // माँ का मूक त्याग"
    ) -> str:
        """
        Renders an animated emotional timeline illustrating the mother's unseen sacrifice
        with milestones, connecting glowing bars, and key narrative beats.
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
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

        h_title = self._load_hindi_font(28)
        h_sub = self._load_hindi_font(18)
        h_body = self._load_hindi_font(15)
        h_mono = self._load_hindi_font(13)

        milestones = [
            {"year": "2012", "label": "पैतृक घर गिरवी", "desc": "कॉलेज में प्रवेश के लिए घर गिरवी रखकर ₹3,50,000 की फीस भरी।", "color": (234, 88, 12)},
            {"year": "2016", "label": "खामोश संघर्ष", "desc": "देर रात तक सिलाई का काम कर कर्ज की मासिक किश्तें चुकाईं।", "color": (245, 158, 11)},
            {"year": "2020", "label": "छुपाई गई बीमारी", "desc": "कैंसर के इलाज का खर्च रोककर बेटे की उच्च शिक्षा जारी रखी।", "color": (239, 68, 68)},
            {"year": "2024", "label": "अमर धरोहर", "desc": "बेटे की सफलता और सम्मान ही माँ के जीवन की अंतिम विजय बनी।", "color": (56, 189, 248)}
        ]

        for i in range(total_frames):
            frac = i / float(total_frames)
            im = Image.new("RGB", (self.res_x, self.res_y), color=(14, 18, 28))
            draw = ImageDraw.Draw(im)

            draw.text((60, 45), title, fill=(245, 158, 11), font=h_title)
            draw.text((60, 85), "AN UNTOLD CHRONICLE OF MATERNAL DEVOTION & RESILIENCE", fill=(148, 163, 184), font=h_sub)
            draw.line([(60, 115), (self.res_x - 60, 115)], fill=(51, 65, 85), width=2)

            bar_y = 230
            draw.line([(100, bar_y), (self.res_x - 100, bar_y)], fill=(30, 41, 59), width=6)
            progress_line = int((self.res_x - 200) * min(1.0, frac / 0.85))
            draw.line([(100, bar_y), (100 + progress_line, bar_y)], fill=(245, 158, 11), width=6)

            card_w = 250
            card_h = 320
            card_gap = (self.res_x - 200 - 4 * card_w) // 3

            for idx, m in enumerate(milestones):
                cx = 100 + idx * (card_w + card_gap)
                cy = 280

                t_thresh = 0.10 + idx * 0.18
                if frac >= t_thresh:
                    draw.ellipse([(cx + card_w//2 - 12, bar_y - 12), (cx + card_w//2 + 12, bar_y + 12)], fill=m["color"], outline=(255, 255, 255), width=2)
                    draw.rectangle([(cx, cy), (cx + card_w, cy + card_h)], fill=(22, 30, 46), outline=(51, 65, 85), width=2)
                    draw.rectangle([(cx, cy), (cx + card_w, cy + 45)], fill=(30, 41, 60))
                    draw.text((cx + 15, cy + 10), m["year"], fill=(255, 255, 255), font=h_title)
                    draw.text((cx + 15, cy + 55), m["label"], fill=m["color"], font=h_sub)
                    draw.text((cx + 15, cy + 110), m["desc"], fill=(203, 213, 225), font=h_body)
                    draw.text((cx + 15, cy + 260), "STATUS: VERIFIED RECORD", fill=(100, 116, 139), font=h_mono)
                else:
                    draw.ellipse([(cx + card_w//2 - 8, bar_y - 8), (cx + card_w//2 + 8, bar_y + 8)], fill=(40, 50, 70))

            draw.rectangle([(60, 625), (self.res_x - 60, 685)], fill=(18, 25, 40), outline=(51, 65, 85))
            draw.text((80, 642), "FAMILY LEGACY ARCHIVE // CONFIDENTIAL DOCUMENTARY RECORD", fill=(148, 163, 184), font=h_mono)

            if frac > 0.90:
                fade = (frac - 0.90) / 0.10
                black_overlay = Image.new("RGB", (self.res_x, self.res_y), color=(0, 0, 0))
                im = Image.blend(im, black_overlay, fade)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Sacrifice Timeline animation rendered to: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4


if __name__ == "__main__":
    engine = MotionGraphics2DEngine()
    out1 = r"F:\Master AI\09_CONTENT_STUDIO\renders\pilot_lion_documentary\map_territory_2d.mp4"
    out2 = r"F:\Master AI\09_CONTENT_STUDIO\renders\pilot_lion_documentary\infographic_biology_2d.mp4"
    engine.render_territory_map_animation(out1, duration_sec=6.0)
    engine.render_biology_infographic_animation(out2, duration_sec=6.0)
