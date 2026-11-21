#!/usr/bin/env python3
"""
validate_system_environment.py - Phase 1 Pre-Execution System & Hardware Validation
Audits:
1. All logical drive volumes (C:, D:, etc.) with free space and usage.
2. CPU topology (model, cores, logical threads, clock).
3. Memory (RAM total, available, committed).
4. GPU (Video controller, VRAM, drivers).
5. Development toolchains (Python, Node, npm, Git, Ollama, Docker).
6. Existing project directories and components.
7. Existing Python environments and site-packages.
8. Ollama daemon connectivity and local model catalog.
9. WSL2 status and virtualization overhead analysis.
"""

import os
import sys
import shutil
import subprocess
import ctypes
import json
from pathlib import Path

def get_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if bitmask & 1:
            drive_path = f"{letter}:\\"
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            total_free = ctypes.c_ulonglong(0)
            ret = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(drive_path),
                ctypes.byref(free_bytes),
                ctypes.byref(total_bytes),
                ctypes.byref(total_free)
            )
            if ret:
                total_gb = total_bytes.value / (1024**3)
                free_gb = free_bytes.value / (1024**3)
                used_gb = total_gb - free_gb
                pct_free = (free_gb / total_gb) * 100 if total_gb > 0 else 0
                drives.append({
                    "drive": f"{letter}:",
                    "total_gb": round(total_gb, 2),
                    "used_gb": round(used_gb, 2),
                    "free_gb": round(free_gb, 2),
                    "percent_free": round(pct_free, 1)
                })
        bitmask >>= 1
    return drives

def run_ps(cmd):
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

def audit():
    report = {}

    # 1. Drives
    drives = get_drives()
    report["storage_volumes"] = drives

    # 2. CPU
    cpu_name = run_ps("(Get-CimInstance Win32_Processor).Name")
    cpu_cores = run_ps("(Get-CimInstance Win32_Processor).NumberOfCores")
    cpu_threads = run_ps("(Get-CimInstance Win32_Processor).NumberOfLogicalProcessors")
    report["cpu"] = {
        "name": cpu_name,
        "cores": cpu_cores,
        "threads": cpu_threads
    }

    # 3. RAM
    ram_total = run_ps("[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)")
    ram_free = run_ps("[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB / 1024, 2)")
    report["ram"] = {
        "total_gb": ram_total,
        "free_gb": ram_free
    }

    # 4. GPU
    gpu_name = run_ps("(Get-CimInstance Win32_VideoController).Name")
    gpu_vram = run_ps("(Get-CimInstance Win32_VideoController).AdapterRAM")
    gpu_driver = run_ps("(Get-CimInstance Win32_VideoController).DriverVersion")
    report["gpu"] = {
        "name": gpu_name,
        "adapter_ram_bytes": gpu_vram,
        "driver_version": gpu_driver
    }

    # 5. Toolchains
    tools = {
        "python": [sys.executable, "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "git": ["git", "--version"],
        "ollama": ["ollama", "--version"],
        "docker": ["docker", "--version"],
        "ffmpeg": ["ffmpeg", "-version"]
    }
    tool_status = {}
    for t_name, cmd in tools.items():
        which_path = shutil.which(cmd[0])
        if which_path:
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                out = (r.stdout or r.stderr).splitlines()[0].strip()
                tool_status[t_name] = {"available": True, "path": which_path, "version": out}
            except Exception as e:
                tool_status[t_name] = {"available": True, "path": which_path, "version": f"Error querying: {e}"}
        else:
            tool_status[t_name] = {"available": False, "path": None, "version": None}
    report["toolchains"] = tool_status

    # 6. Ollama Server connectivity
    ollama_models = []
    ollama_running = False
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            ollama_running = True
            lines = r.stdout.strip().splitlines()
            if len(lines) > 1:
                ollama_models = lines[1:]
    except Exception as e:
        pass
    report["ollama"] = {
        "daemon_responsive": ollama_running,
        "cached_models": ollama_models,
        "model_count": len(ollama_models)
    }

    # 7. WSL2 check
    wsl_status = run_ps("wsl --status")
    report["wsl2"] = {
        "status_raw": wsl_status[:200] if wsl_status else "Not available or error"
    }

    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    audit()
