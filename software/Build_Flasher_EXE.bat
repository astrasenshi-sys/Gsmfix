@echo off
TITLE GSM Fix Hub - Compile Standalone Universal Flasher (.EXE)
COLOR 0A
CLS

echo ===============================================================================
echo   GSM FIX HUB - COMPILER FOR FLASHER STANDALONE WINDOWS EXECUTABLE (.EXE)
echo   Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
echo ===============================================================================
echo.

where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] PyInstaller not detected. Installing PyInstaller via pip...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        COLOR 0C
        echo [!] Failed to install PyInstaller. Please check internet connection.
        pause
        exit /b 1
    )
)

echo [*] Compiling gsm_universal_flasher_pro.py into a standalone .EXE...
echo [*] Bundling: SP Flash Tool + Odin3 + SPD PAC + QFIL EDL 9008 + Fastboot...
pyinstaller --noconfirm --onefile --windowed --name "GSM_Fix_Hub_Universal_Flasher" "%~dp0gsm_universal_flasher_pro.py"

if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo [SUCCESS] Standalone Executable created successfully!
    echo Location: dist\GSM_Fix_Hub_Universal_Flasher.exe
    echo ===============================================================================
    echo.
) else (
    COLOR 0C
    echo [!] Build failed. Please review compiler log output above.
)

pause
exit /b 0
