@echo off
TITLE GSM Fix Hub — Standalone Setup & Executable (.EXE) Compiler
COLOR 0A
CLS

echo ===============================================================================
echo   GSM FIX HUB — FULL SETUP & STANDALONE (.EXE) COMPILER (2026 EDITION)
echo   Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
echo ===============================================================================
echo.
echo [*] Checking Python 3 and PyInstaller environment...

where python >nul 2>nul
if %errorlevel% neq 0 (
    COLOR 0C
    echo [!] Python 3 was not detected in PATH.
    echo [!] Please install Python from https://www.python.org/ and check "Add to PATH".
    pause
    exit /b 1
)

where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] PyInstaller not detected. Automatically installing PyInstaller via pip...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        COLOR 0C
        echo [!] Failed to install PyInstaller. Check internet connectivity.
        pause
        exit /b 1
    )
)

echo.
echo [*] Compiling GSM Universal Flasher into Single-File Full Setup Executable...
echo [*] Target: dist\GSM_Fix_Hub_Setup_v5.0.exe
echo.

pyinstaller --noconfirm --onefile --windowed --name "GSM_Fix_Hub_Setup_v5.0" "%~dp0gsm_universal_flasher_pro.py"

if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo [SUCCESS] Standalone Executable Created Successfully!
    echo Location: %~dp0dist\GSM_Fix_Hub_Setup_v5.0.exe
    echo ===============================================================================
    echo.
    echo You can distribute or run GSM_Fix_Hub_Setup_v5.0.exe on any Windows 7/8/10/11 PC
    echo with zero external dependencies required!
    echo.
) else (
    COLOR 0C
    echo [!] Compilation encountered an error. Please inspect the log output above.
)

pause
exit /b 0
