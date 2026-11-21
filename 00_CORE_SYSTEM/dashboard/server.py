"""
server.py
Master AI Autonomous Dashboard Server.
Zero-dependency, high-speed Python HTTP server with live REST APIs and WebSocket/Static serving.
Runs on http://localhost:8080.
"""

import os
import sys
import json
import time
import shutil
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Dynamic Workspace Discovery
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

STATIC_DIR = WORKSPACE_ROOT / "00_CORE_SYSTEM" / "dashboard" / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR = WORKSPACE_ROOT / "16_VIDEO_LIBRARY"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

PORT = 8080


class MasterAIDashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS and caching rules
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Static index
        if path == "/" or path == "/index.html":
            index_file = STATIC_DIR / "index.html"
            if index_file.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(index_file, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve generated videos
        if path.startswith("/videos/"):
            vid_name = path.replace("/videos/", "")
            vid_path = VIDEO_DIR / vid_name
            if vid_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(vid_path.stat().st_size))
                self.end_headers()
                with open(vid_path, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
                return
            else:
                self.send_error(404, "Video Not Found")
                return

        # API: System status
        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_data = {
                "status": "online",
                "platform": "Master AI by JobRun Technologies",
                "version": "2.0.0-sovereign",
                "uptime": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.wfile.write(json.dumps(status_data).encode("utf-8"))
            return

        # API: Voice vault status
        if path == "/api/vault/status":
            import importlib
            vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
            status = vv.vault.get_status()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(status).encode("utf-8"))
            return

        # API: List produced videos
        if path == "/api/videos":
            videos = []
            for f in sorted(VIDEO_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True):
                videos.append({
                    "name": f.name,
                    "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                    "created": time.strftime("%Y-%m-%d %H:%M", time.localtime(f.stat().st_mtime)),
                    "url": f"/videos/{f.name}"
                })
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(videos).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}

        # API: Add API key to Voice Vault (with verification)
        if path == "/api/vault/add_key":
            provider = req_data.get("provider", "")
            key = req_data.get("key", "")
            label = req_data.get("label", "")
            import importlib
            vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
            res = vv.vault.add_key(provider, key, label)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # API: Delete Key
        if path == "/api/vault/delete_key":
            provider = req_data.get("provider", "")
            key_id = int(req_data.get("key_id", 0))
            import importlib
            vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
            success = vv.vault.delete_key(provider, key_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}).encode("utf-8"))
            return

        # API: Toggle Key Status (Active / Disabled)
        if path == "/api/vault/toggle_key":
            provider = req_data.get("provider", "")
            key_id = int(req_data.get("key_id", 0))
            import importlib
            vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
            success = vv.vault.toggle_key(provider, key_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}).encode("utf-8"))
            return

        # API: Set Active Primary Engine
        if path == "/api/vault/set_primary":
            provider = req_data.get("provider", "gemini")
            import importlib
            vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
            success = vv.vault.set_primary(provider)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "active_primary": provider}).encode("utf-8"))
            return

        # API: Test Voice
        if path == "/api/tts/test":
            text = req_data.get("text", "नमस्ते, मास्टर एआई वॉइस वॉल्ट टेस्ट सफल रहा।")
            speaker = req_data.get("speaker", "neha")
            import importlib
            vv = importlib.import_module("00_CORE_SYSTEM.engine.tts.voice_vault")
            try:
                res = vv.vault.synthesize_with_failover(text, speaker_or_voice=speaker)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "result": res}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        # API: Render Video
        if path == "/api/video/render":
            topic = req_data.get("topic", "Claude Code On Mobile")
            character = req_data.get("character", "dev")
            creator_name = req_data.get("creator_name", "Dev")
            creator_role = req_data.get("creator_role", "Tech Builder")
            speaker = req_data.get("speaker", "aditya")
            script = req_data.get("script", "पहले टर्मक्स में नोड जेएस इन्स्टॉल करो, फिर क्लॉड कमांड रन करो और पूरा एआई मोबाइल में रेडी!")
            cta = req_data.get("cta", "Comment TERMUX for Full Guide")
            save_path = req_data.get("savePath", "").strip()

            import importlib
            vm = importlib.import_module("00_CORE_SYSTEM.engine.video_production.render_master_reel")
            try:
                clean_top = "".join(c if c.isalnum() else "_" for c in topic)[:25]
                vid_name = f"reel_{creator_name.lower()}_{clean_top}_{int(time.time())}.mp4"
                
                # Determine destination
                if save_path:
                    target_dir = Path(save_path).expanduser().resolve()
                else:
                    target_dir = VIDEO_DIR
                target_dir.mkdir(parents=True, exist_ok=True)
                full_dest = str(target_dir / vid_name)

                out_path = vm.render_video(
                    topic=topic,
                    character=character,
                    voice_speaker=speaker,
                    script_text=script,
                    cta=cta,
                    output_name=full_dest,
                    creator_name=creator_name,
                    creator_role=creator_role
                )
                
                # Also copy to VIDEO_DIR if saved elsewhere so web player can stream it
                if Path(out_path).resolve() != (VIDEO_DIR / vid_name).resolve():
                    shutil.copy2(out_path, str(VIDEO_DIR / vid_name))

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "video_url": f"/videos/{vid_name}", "name": vid_name, "saved_at": out_path}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        self.send_error(404, "Not Found")


def run_server(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, MasterAIDashboardHandler)
    print(f"============================================================")
    print(f" MASTER AI AUTONOMOUS DASHBOARD ONLINE")
    print(f" URL: http://localhost:{port}")
    print(f"============================================================")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
