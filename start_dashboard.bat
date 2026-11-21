@echo off
title Master AI Dashboard Server
echo ============================================================
echo   MASTER AI AUTONOMOUS DASHBOARD (Powered by Zovron)
echo   Localhost URL: http://localhost:8080
echo ============================================================
echo.

:: 1. Locate Master AI Project Directory
set "TARGET_DIR="

if exist "%~dp000_CORE_SYSTEM\dashboard\server.py" (
    set "TARGET_DIR=%~dp0"
) else if exist "%~dp0Master AI\00_CORE_SYSTEM\dashboard\server.py" (
    set "TARGET_DIR=%~dp0Master AI"
) else if exist "F:\Master AI\00_CORE_SYSTEM\dashboard\server.py" (
    set "TARGET_DIR=F:\Master AI"
) else if exist "%USERPROFILE%\Desktop\Master AI\00_CORE_SYSTEM\dashboard\server.py" (
    set "TARGET_DIR=%USERPROFILE%\Desktop\Master AI"
)

if "%TARGET_DIR%"=="" (
    echo [ERROR] Could not find Master AI project folder!
    echo Please make sure Master AI is placed in F:\Master AI or on your Desktop.
    pause
    exit /b 1
)

cd /d "%TARGET_DIR%"
echo [+] Project Root: %CD%

:: 2. Select Python Interpreter
set "PY_CMD=python"
if exist "%CD%\.venv\Scripts\python.exe" (
    set "PY_CMD=%CD%\.venv\Scripts\python.exe"
    echo [+] Using VirtualEnv Python: %PY_CMD%
) else (
    echo [+] Using System Python
)

:: 3. Launch Browser and Server
echo.
echo [!] Launching browser at http://localhost:8080 ...
start http://localhost:8080

echo [!] Starting Dashboard Web Server on Port 8080 ...
echo [!] Press Ctrl+C in this window anytime to stop the server.
echo.
"%PY_CMD%" "00_CORE_SYSTEM\dashboard\server.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Server stopped with error code %ERRORLEVEL%.
    pause
)
pause
