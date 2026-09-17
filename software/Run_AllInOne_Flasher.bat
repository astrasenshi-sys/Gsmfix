@echo off
TITLE GSM Fix Hub - All-in-One Mobile Flasher Pro
COLOR 0B
CLS

echo ===============================================================================
echo   GSM FIX HUB — ALL-IN-ONE MULTI-BRAND MOBILE FLASHER PRO (2026)
echo   Architect: Bhuwan Bastola | Gopal Electronics, Surkhet
echo ===============================================================================
echo.
echo Launching All-in-One Flasher (MediaTek, Samsung Odin, SPD, Xiaomi, Qualcomm)...
start pythonw "%~dp0gsm_allinone_flasher_pro.py"
if %errorlevel% neq 0 (
    python "%~dp0gsm_allinone_flasher_pro.py"
)
exit /b 0
