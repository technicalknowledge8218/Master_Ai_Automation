#!/bin/bash
# ==============================================================
# Master AI — 1-Line Universal Installer for Mobile Termux & Linux
# Powered by Zovron Technologies (zovron.tech)
# ==============================================================

set -e

echo ""
echo "=============================================================="
echo " 🚀 MASTER AI — 1-CLICK MOBILE & DESKTOP INSTALLER"
echo " Powered by Zovron Technologies"
echo "=============================================================="
echo ""

# 1. Update and install packages if on Termux
if command -v pkg &> /dev/null; then
    echo "[+] Updating Termux packages..."
    pkg update -y
    echo "[+] Installing system dependencies (Python, Git, FFmpeg, Pillow)..."
    pkg install git python ffmpeg python-pillow python-numpy -y
    
    # Request storage permission if not already granted
    if [ ! -d "$HOME/storage" ]; then
        echo "[+] Requesting phone storage access..."
        termux-setup-storage || true
    fi
fi

# 2. Clone or update repository
TARGET_DIR="$HOME/Master_Ai_Automation"
REPO_URL="https://github.com/technicalknowledge8218/Master_Ai_Automation.git"

if [ -d "$TARGET_DIR/.git" ]; then
    echo "[+] Existing installation found. Pulling latest code..."
    cd "$TARGET_DIR"
    git pull origin main || true
else
    echo "[+] Cloning latest Master AI repository..."
    rm -rf "$TARGET_DIR"
    git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR"
fi

# 3. Launch interactive setup wizard
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo ""
echo "[+] Launching Master AI Setup Wizard..."
$PYTHON_CMD setup.py
