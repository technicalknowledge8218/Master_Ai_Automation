"""thumbnail_and_packaging.py
MASTER-AI Thumbnail Studio & Final Publication Packaging Engine

Generates:
1. High-impact 1280x720 YouTube thumbnails with Devanagari typography, badges, and focal art.
2. Complete publication package including video, audio, subtitles, QA report, SEO metadata,
   and staging into the Central Approval Center for human publish authorization.
"""

import os
import sys
import json
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

import importlib
try:
    ApprovalCenter = importlib.import_module("03_AI_AGENTS.approval_engine.approval_center").ApprovalCenter
except Exception:
    ApprovalCenter = None


class ThumbnailStudio:
    """Generates broadcast-grade 1280x720 YouTube thumbnails."""

    def __init__(self):
        pass

    def generate_youtube_thumbnail(
        self,
        title_hindi: str,
        subtitle_english: str,
        output_path: str,
        topic: str = "Lion Documentary",
        badge_text: str = "5 MIN • 4K UHD"
    ) -> Dict[str, Any]:
        """Creates a vibrant, high-CTR YouTube thumbnail (1280x720)."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), (15, 18, 26))
        draw = ImageDraw.Draw(img)

        # 1. Dramatic Background (Savannah sunset fire gradient)
        for y in range(height):
            ratio = y / height
            r = int(30 * (1 - ratio) + 180 * ratio * 0.8 + 20)
            g = int(20 * (1 - ratio) + 80 * ratio * 0.8 + 10)
            b = int(40 * (1 - ratio) + 20 * ratio * 0.8 + 10)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Golden Sun Glow (Right side)
        glow_x, glow_y = int(width * 0.72), int(height * 0.45)
        for radius in range(int(height * 0.45), 20, -10):
            alpha_ratio = 1 - (radius / (height * 0.45))
            gold_val = int(255 * alpha_ratio)
            draw.ellipse(
                [glow_x - radius, glow_y - radius, glow_x + radius, glow_y + radius],
                outline=(240, 180, 50),
                width=2
            )

        # 3. Silhouette Motif (Pride Rock & Roaring Lion)
        rock_pts = [
            (int(width * 0.48), height),
            (int(width * 0.58), int(height * 0.55)),
            (int(width * 0.85), int(height * 0.58)),
            (width, height)
        ]
        draw.polygon(rock_pts, fill=(10, 10, 12))

        # Lion head silhouette
        lx = int(width * 0.65)
        ly = int(height * 0.48)
        draw.ellipse([lx - 40, ly - 40, lx + 40, ly + 30], fill=(8, 8, 10))  # Mane
        draw.ellipse([lx + 15, ly - 20, lx + 55, ly + 15], fill=(8, 8, 10))  # Snout
        # Ears
        draw.polygon([(lx - 10, ly - 45), (lx - 25, ly - 65), (lx + 5, ly - 48)], fill=(8, 8, 10))

        # 4. Typography Panel (Left half)
        # Translucent dark backing box for crisp text readability
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        o_draw = ImageDraw.Draw(overlay)
        o_draw.rectangle([40, 40, int(width * 0.55), height - 40], fill=(8, 10, 16, 215))

        # Topic Tag
        o_draw.rectangle([60, 70, 260, 115], fill=(220, 50, 40, 240))
        o_draw.text((80, 80), "WILDLIFE DOC", fill=(255, 255, 255, 255))

        # Hindi Title
        o_draw.text((60, 140), title_hindi, fill=(255, 220, 80, 255))

        # English Subtitle
        o_draw.text((60, 230), subtitle_english.upper(), fill=(255, 255, 255, 255))

        # Feature bullet points
        bullets = [
            "• सवाना के सम्राट का जीवन (Life of the King)",
            "• झुंड और शिकार का अद्भुत तालमेल",
            "• 4K सिनेमैटिक विजुअल्स और हिंदी विवरण"
        ]
        b_y = 330
        for b in bullets:
            o_draw.text((60, b_y), b, fill=(200, 210, 225, 240))
            b_y += 50

        # Duration & Quality Badge (Bottom-Left)
        o_draw.rectangle([60, height - 120, 340, height - 70], fill=(240, 160, 30, 240))
        o_draw.text((80, height - 110), badge_text, fill=(10, 10, 15, 255))

        # Brand mark (Bottom-Right)
        o_draw.text((width - 240, height - 70), "MASTER AI STUDIOS", fill=(220, 220, 230, 200))

        final_img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        final_img.save(output_path, "PNG", quality=95)

        return {
            "thumbnail_path": output_path,
            "resolution": "1280x720",
            "aspect_ratio": "16:9",
            "file_size_bytes": os.path.getsize(output_path),
            "status": "SUCCESS"
        }


class ProductionPackager:
    """Consolidates media assets into a publication package and stages for human approval."""

    def __init__(self, approval_center: Optional[ApprovalCenter] = None):
        self.approval_center = approval_center or ApprovalCenter()

    def package_for_publication(
        self,
        project_id: str,
        title: str,
        video_path: str,
        audio_path: str,
        srt_path: str,
        ass_path: str,
        thumbnail_path: str,
        qa_report: Dict[str, Any],
        output_dir: str,
        chapters: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Assembles full release metadata and requests publication approval."""
        os.makedirs(output_dir, exist_ok=True)

        # Build YouTube Description with Timestamps
        desc_lines = [
            f"🎬 {title}",
            "",
            "सवाना का सम्राट: शेर के जीवन, सामाजिक व्यवस्था (प्राइड) और शिकार की रणनीति पर आधारित एक प्रमाणिक 5-मिनट वन्यजीव वृत्तचित्र।",
            "",
            "📌 अध्याय (Chapter Markers):",
            "00:00 - अंक 1: सवाना की सुबह (Act I: Dawn on the Savannah)",
            "01:00 - अंक 2: झुंड और शिकार का संतुलन (Act II: The Pride & The Hunt)",
            "02:30 - अंक 3: सीमाओं की रक्षा और संघर्ष (Act III: Territorial Defense)",
            "04:00 - अंक 4: संरक्षण और अमर विरासत (Act IV: Twilight & Conservation)",
            "",
            "🔬 निर्माण: मास्टर एआई स्वायत्त सामग्री स्टूडियो (Master AI Sovereign Content Studio)",
            "📜 लाइसेंस: CC-BY 4.0 / Public Domain Educational Facts",
            "🔊 विवरण भाषा: हिंदी (Hindi) with English Subtitles"
        ]
        description_text = "\n".join(desc_lines)

        tags = [
            "lion documentary", "शेर वन्यजीव वृत्तचित्र", "panthera leo",
            "wildlife documentary hindi", "african savannah", "gir national park",
            "master ai content studio", "hindi voiceover documentary", "apex predators"
        ]

        metadata = {
            "project_id": project_id,
            "title": title,
            "category_id": "28",  # Science & Technology / Nature
            "language": "hi",
            "default_audio_language": "hi",
            "privacy_status": "private",  # Staged as private
            "tags": tags,
            "description": description_text,
            "assets": {
                "video": video_path,
                "audio": audio_path,
                "subtitles_srt": srt_path,
                "subtitles_ass": ass_path,
                "thumbnail": thumbnail_path
            },
            "qa_status": qa_report.get("overall_status", "UNKNOWN"),
            "packaging_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        meta_path = os.path.join(output_dir, "PUBLICATION_METADATA.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Register Approval Request in Approval Center
        approval_ticket = self.approval_center.request_approval(
            category="EXTERNAL_PUBLISH",
            title=f"YouTube Release: {title}",
            description=f"Automated quality-checked video package ready for publishing (QA Status: {qa_report.get('overall_status')}).",
            requesting_agent="AGT-008",
            target_resource="youtube_channel_release",
            ttl_seconds=86400,
            metadata={"project_id": project_id, "qa_passed": qa_report.get("passed", False)}
        )

        return {
            "project_id": project_id,
            "package_dir": output_dir,
            "metadata_file": meta_path,
            "approval_ticket_id": approval_ticket["ticket_id"],
            "approval_status": approval_ticket["status"],
            "qa_passed": qa_report.get("passed", False),
            "status": "STAGED_FOR_APPROVAL"
        }
