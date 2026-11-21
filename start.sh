#!/bin/bash
# ==============================================================
# Master AI — 1-Click Startup for Android Termux & Linux
# Powered by JobRun Technologies
# ==============================================================

echo "=============================================================="
echo " ⚡ MASTER AI — AUTONOMOUS CREATOR ENGINE"
echo " Android Termux & Linux Fast Launch"
echo "=============================================================="

# 1. Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[!] Python is not installed. Installing via package manager..."
    if command -v pkg &> /dev/null; then
        pkg install python -y
    fi
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# 2. Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "[!] FFmpeg is not installed. Installing..."
    if command -v pkg &> /dev/null; then
        pkg install ffmpeg -y
    fi
fi

# 3. Grant Storage access on Termux if on Android
if command -v termux-setup-storage &> /dev/null; then
    if [ ! -d "$HOME/storage" ]; then
        echo "[+] Requesting Android storage permission..."
        termux-setup-storage
    fi
fi

# 4. Resolve Directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 5. Create default output directory on Android if exists
if [ -d "/sdcard/Download" ]; then
    mkdir -p "/sdcard/Download/Master_AI_Videos"
    echo "[+] Default Mobile Output: /sdcard/Download/Master_AI_Videos"
fi

echo ""
echo "🚀 Starting Master AI Dashboard on http://localhost:8080"
echo "👉 Open your mobile browser and go to: http://localhost:8080"
echo ""

# Try to auto-open URL in browser on Android / Linux
if command -v termux-open-url &> /dev/null; then
    termux-open-url http://localhost:8080 &
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080 &
fi

# Run Dashboard server
$PYTHON_CMD "00_CORE_SYSTEM/dashboard/server.py"
