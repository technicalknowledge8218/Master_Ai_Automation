"""
Master AI - 3D CGI Production Module
Blender Engine Adapter (Enterprise Production Grade)

Provides an abstracted, pluggable interface for headless 3D scene generation,
procedural modeling, EEVEE Next rendering (Blender 4.2 & 5.2 LTS compatible),
resource monitoring, process-tree cancellation, crash recovery, output validation,
and persistent job tracking.
"""

import os
import sys
import subprocess
import time
import json
import logging
import re
import psutil
from typing import Dict, Any, Optional, List, Callable

logger = logging.getLogger("MasterAI.3D.BlenderAdapter")
logging.basicConfig(level=logging.INFO)

class BlenderAdapter:
    ENGINE_BASE_DIR = r"F:\Master AI\07_3D_CGI\engine"
    PREFERRED_5_2_DIR = os.path.join(ENGINE_BASE_DIR, "blender_5_2_lts")
    FALLBACK_4_2_DIR = os.path.join(ENGINE_BASE_DIR, "blender")
    JOBS_LEDGER_PATH = r"F:\Master AI\07_3D_CGI\adapters\render_jobs_ledger.json"

    def __init__(self, custom_blender_path: Optional[str] = None, force_legacy_4_2: bool = False):
        self.force_legacy = force_legacy_4_2
        self.blender_exe = self._detect_blender(custom_blender_path)
        self.version_info = self._get_version() if self.blender_exe else {}
        self.active_process = None
        self.job_history = self._load_ledger()

    def _detect_blender(self, custom_path: Optional[str] = None) -> Optional[str]:
        """Detect official portable Blender executable with 5.2 priority and 4.2 rollback."""
        candidates = []
        if custom_path:
            candidates.append(custom_path)

        if not self.force_legacy:
            # 1. Preferred: Blender 5.2 LTS
            if os.path.exists(self.PREFERRED_5_2_DIR):
                for root, dirs, files in os.walk(self.PREFERRED_5_2_DIR):
                    if "blender.exe" in files:
                        candidates.append(os.path.join(root, "blender.exe"))
                        break

        # 2. Fallback / Rollback: Blender 4.2 LTS
        if os.path.exists(self.FALLBACK_4_2_DIR):
            for root, dirs, files in os.walk(self.FALLBACK_4_2_DIR):
                if "blender.exe" in files:
                    candidates.append(os.path.join(root, "blender.exe"))
                    break

        # 3. System PATH via where.exe
        try:
            res = subprocess.run(["where.exe", "blender"], capture_output=True, text=True)
            if res.returncode == 0:
                for line in res.stdout.strip().splitlines():
                    if line.strip():
                        candidates.append(line.strip())
        except Exception:
            pass

        # 4. Standard Program Files
        candidates.extend([
            r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
        ])

        for path in candidates:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                logger.info(f"Blender executable selected: {path}")
                return os.path.abspath(path)

        logger.warning("No valid Blender executable found.")
        return None

    def is_installed(self) -> bool:
        return self.blender_exe is not None and os.path.isfile(self.blender_exe)

    def _get_version(self) -> Dict[str, Any]:
        """Extract Blender version, major/minor integers, and build metadata."""
        if not self.blender_exe:
            return {}
        try:
            res = subprocess.run([self.blender_exe, "-b", "--version"], capture_output=True, text=True, timeout=12)
            if res.returncode == 0:
                first_line = res.stdout.strip().splitlines()[0]
                m = re.search(r"Blender\s+([0-9]+)\.([0-9]+)\.([0-9]+)\s*(\w*)", first_line)
                major = int(m.group(1)) if m else 4
                minor = int(m.group(2)) if m else 2
                patch = int(m.group(3)) if m else 0
                edition = m.group(4) if m else "LTS"
                return {
                    "raw": first_line,
                    "version_str": f"{major}.{minor}.{patch}",
                    "major": major,
                    "minor": minor,
                    "patch": patch,
                    "edition": edition,
                    "executable": self.blender_exe,
                    "default_eevee_engine": "BLENDER_EEVEE" if major >= 5 else "BLENDER_EEVEE_NEXT"
                }
        except Exception as e:
            logger.error(f"Error querying Blender version: {e}")
        return {"executable": self.blender_exe, "major": 4, "default_eevee_engine": "BLENDER_EEVEE_NEXT"}

    def get_compatible_engine_name(self) -> str:
        """Return the correct EEVEE engine identifier for the active Blender version."""
        major = self.version_info.get("major", 4)
        return "BLENDER_EEVEE" if major >= 5 else "BLENDER_EEVEE_NEXT"

    def _load_ledger(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.JOBS_LEDGER_PATH):
            try:
                with open(self.JOBS_LEDGER_PATH, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_ledger(self):
        os.makedirs(os.path.dirname(self.JOBS_LEDGER_PATH), exist_ok=True)
        try:
            with open(self.JOBS_LEDGER_PATH, "w") as f:
                json.dump(self.job_history[-50:], f, indent=2) # Keep last 50 jobs
        except Exception as e:
            logger.error(f"Failed to persist jobs ledger: {e}")

    def render_scene(
        self,
        scene_script_path: str,
        output_prefix: str,
        start_frame: int = 1,
        end_frame: int = 1,
        resolution_x: int = 1280,
        resolution_y: int = 720,
        samples: int = 16,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
        timeout_sec: int = 600
    ) -> Dict[str, Any]:
        """
        Execute a headless background render job with process-tree isolation,
        real-time telemetry parsing, memory peak tracking, and output validation.
        """
        if not self.is_installed():
            raise RuntimeError("Blender is not installed or executable not found.")

        if not os.path.isfile(scene_script_path):
            raise FileNotFoundError(f"Scene script not found: {scene_script_path}")

        out_dir = os.path.dirname(os.path.abspath(output_prefix))
        os.makedirs(out_dir, exist_ok=True)

        engine_name = self.get_compatible_engine_name()

        # Build execution command
        cmd = [
            self.blender_exe, "-b",
            "-P", os.path.abspath(scene_script_path),
            "-o", os.path.abspath(output_prefix),
            "-s", str(start_frame),
            "-e", str(end_frame),
            "-a"
        ]

        t_start = time.perf_counter()
        total_frames = end_frame - start_frame + 1
        completed_frames = 0
        frame_latencies = []
        peak_rss_mb = 0.0

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        self.active_process = proc

        ps_proc = None
        try:
            ps_proc = psutil.Process(proc.pid)
        except Exception:
            pass

        stdout_lines = []
        job_error = None

        try:
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None:
                    break
                if line:
                    stdout_lines.append(line)
                    # Check frame render progress
                    # Fra:10 Mem:55.51M (Peak 69.57M) | Time:00:00.80 (Saving: 00:00.11)
                    # or Blender 5.2 format: 00:14.687 render | Saved: '...'
                    m = re.search(r"Fra:(\d+).*Time:\s*(\d+):(\d+\.\d+)\s*\(Saving", line)
                    if m:
                        completed_frames += 1
                        sec = float(m.group(2)) * 60 + float(m.group(3))
                        frame_latencies.append(sec)
                        if progress_callback:
                            progress_callback(completed_frames, total_frames, sec)
                    elif "Saved: '" in line or "Fra:" in line:
                        m2 = re.search(r"Fra:(\d+)", line)
                        if m2:
                            completed_frames = max(completed_frames, int(m2.group(1)))

                    # Monitor process-tree memory
                    if ps_proc and ps_proc.is_running():
                        try:
                            rss = ps_proc.memory_info().rss
                            for child in ps_proc.children(recursive=True):
                                rss += child.memory_info().rss
                            rss_mb = rss / (1024 * 1024)
                            if rss_mb > peak_rss_mb:
                                peak_rss_mb = rss_mb
                        except Exception:
                            pass

                # Check timeout
                if time.perf_counter() - t_start > timeout_sec:
                    self.cancel_active_job()
                    job_error = f"Render job timed out after {timeout_sec} seconds."
                    break

            proc.wait()
        except Exception as ex:
            self.cancel_active_job()
            job_error = str(ex)
        finally:
            self.active_process = None

        t_elapsed = time.perf_counter() - t_start
        ret_code = proc.returncode

        if ret_code != 0 and not job_error:
            err_msg = "".join(stdout_lines[-30:])
            job_error = f"Blender exited with code {ret_code}.\nError tail:\n{err_msg}"

        # 4. Output Validation: Verify that generated frame files exist
        valid_files = []
        for f_idx in range(start_frame, end_frame + 1):
            expected_file = f"{output_prefix}{f_idx:04d}.png"
            if os.path.isfile(expected_file) and os.path.getsize(expected_file) > 1024:
                valid_files.append(expected_file)

        output_valid = (len(valid_files) == total_frames)
        if not output_valid and not job_error:
            job_error = f"Output validation failed: expected {total_frames} frames, found {len(valid_files)} valid frames."

        avg_lat = sum(frame_latencies) / len(frame_latencies) if frame_latencies else (t_elapsed / total_frames if total_frames > 0 else 0)

        job_result = {
            "job_id": f"job_{int(time.time()*1000)}",
            "status": "PASS" if (ret_code == 0 and output_valid) else "FAIL",
            "returncode": ret_code,
            "error": job_error,
            "wall_time_sec": t_elapsed,
            "frames_rendered": len(valid_files),
            "total_frames": total_frames,
            "average_frame_sec": avg_lat,
            "effective_fps": total_frames / t_elapsed if t_elapsed > 0 else 0,
            "peak_memory_mb": peak_rss_mb,
            "engine": engine_name,
            "blender_version": self.version_info.get("version_str", "Unknown"),
            "blender_executable": self.blender_exe,
            "output_directory": out_dir,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        self.job_history.append(job_result)
        self._save_ledger()

        if job_error:
            raise RuntimeError(job_error)

        return job_result

    def cancel_active_job(self) -> bool:
        """Terminate the active render process and all child processes recursively."""
        if self.active_process and self.active_process.poll() is None:
            pid = self.active_process.pid
            logger.warning(f"Initiating process-tree termination for Blender PID {pid}...")
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.terminate()
                    except Exception:
                        pass
                parent.terminate()
                gone, alive = psutil.wait_procs(children + [parent], timeout=2.0)
                for p in alive:
                    try:
                        p.kill()
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Error terminating process tree: {e}")
                try:
                    self.active_process.kill()
                except Exception:
                    pass
            logger.info("Blender process-tree terminated.")
            return True
        return False
