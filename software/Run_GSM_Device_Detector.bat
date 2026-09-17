@echo off
TITLE GSM Fix Hub - Device Mode Detector & Web Linker Launcher
COLOR 0B
CLS

echo ===============================================================================
echo   GSM FIX HUB - AUTO MOBILE DEVICE MODE DETECTOR & WEB LINKER (PRO 2026)
echo   Lead Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
echo ===============================================================================
echo.
echo Checking for Python 3 installation...

where python >nul 2>nul
if %errorlevel% neq 0 (
    COLOR 0C
    echo [!] Python 3 was not found in your system PATH.
    echo [!] Please install Python 3.8+ from https://www.python.org/
    echo [!] Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [*] Python found! Launching GSM Fix Hub Device Detector GUI...
start pythonw "%~dp0gsm_device_detector_gui.py"

if %errorlevel% neq 0 (
    echo [!] pythonw failed, launching with standard python console...
    python "%~dp0gsm_device_detector_gui.py"
)

exit /b 0
