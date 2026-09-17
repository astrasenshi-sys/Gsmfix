@echo off
TITLE GSM Fix Hub - Universal Mobile Flasher Pro Launcher
COLOR 0B
CLS

echo ===============================================================================
echo   GSM FIX HUB - UNIVERSAL MULTI-PLATFORM MOBILE FLASHER PRO (2026)
echo   Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
echo ===============================================================================
echo.
echo Checking for Python 3 on Windows...

where python >nul 2>nul
if %errorlevel% neq 0 (
    COLOR 0C
    echo [!] Python 3 was not found in your system PATH.
    echo [!] Please install Python 3.8+ from https://www.python.org/
    echo [!] Remember to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [*] Launching GSM Fix Hub Universal Mobile Flasher...
start pythonw "%~dp0gsm_universal_flasher_pro.py"

if %errorlevel% neq 0 (
    python "%~dp0gsm_universal_flasher_pro.py"
)

exit /b 0
