@echo off
title Push Master AI to GitHub
echo ============================================================
echo   PUSH MASTER AI TO GITHUB REPOSITORY
echo   Repo: https://github.com/technicalknowledge8218/Master_Ai_Automation.git
echo ============================================================
echo.
cd /d "%~dp0"
echo [+] Checking Git Status...
git branch --show-current
echo.
echo [!] Pushing main branch to GitHub...
echo [!] (A browser window will open to sign in if you aren't already authenticated)
echo.
git push -u origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo ============================================================
    echo   [SUCCESS] Code pushed to GitHub successfully!
    echo   URL: https://github.com/technicalknowledge8218/Master_Ai_Automation
    echo ============================================================
) else (
    echo.
    echo [!] If Git asks for credentials:
    echo     1. Sign in via Browser
    echo     2. Or use GitHub Personal Access Token (PAT) as password.
)
echo.
pause
