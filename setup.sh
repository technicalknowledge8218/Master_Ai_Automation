#!/bin/bash
# ==============================================================
# Master AI — Interactive Setup for Android Termux & Linux
# Powered by Zovron Technologies
# ==============================================================

# Ensure python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[!] Python not found. Installing..."
    if command -v pkg &> /dev/null; then
        pkg update && pkg install python ffmpeg -y
    fi
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

$PYTHON_CMD setup.py
