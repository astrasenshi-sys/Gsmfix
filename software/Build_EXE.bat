@echo off
TITLE GSM Fix Hub - Compile Standalone Windows Executable (.EXE)
COLOR 0A
CLS

echo ===============================================================================
echo   GSM FIX HUB - COMPILER FOR STANDALONE WINDOWS EXECUTABLE (.EXE)
echo   Architect: Bhuwan Bastola | Gopal Electronics, Surkhet
echo ===============================================================================
echo.

where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] PyInstaller not found. Installing PyInstaller via pip...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        COLOR 0C
        echo [!] Failed to install PyInstaller. Check your internet connection.
        pause
        exit /b 1
    )
)

echo [*] Compiling gsm_device_detector_gui.py into single-file executable...
pyinstaller --noconfirm --onedir --windowed --name "GSM_Device_Detector_Pro" "%~dp0gsm_device_detector_gui.py"

if %errorlevel% equ 0 (
    echo.
    echo [OK] Compilation Succeeded!
    echo [*] Your executable is located in: dist\GSM_Device_Detector_Pro\GSM_Device_Detector_Pro.exe
    echo.
) else (
    COLOR 0C
    echo [!] Build failed. Please inspect the log messages above.
)

pause
exit /b 0
