@echo off
TITLE GSM Fix Hub — Universal Flasher & Service Suite Installer (Windows)
COLOR 0B
CLS

echo ===============================================================================
echo   GSM FIX HUB — UNIVERSAL MOBILE FLASHER PRO FULL SETUP WIZARD (2026)
echo   Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
echo ===============================================================================
echo.
echo Installing GSM Fix Hub Flashing Suite on your Windows Workstation...

set "INSTALL_DIR=%LOCALAPPDATA%\GSM_Fix_Hub"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [*] Copying software files to: %INSTALL_DIR%
xcopy /E /I /Y "%~dp0*" "%INSTALL_DIR%\" >nul

echo [*] Creating Desktop Shortcut...
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'GSM Fix Hub Flasher Pro.lnk')); $s.TargetPath = '%INSTALL_DIR%\Run_GSM_Flasher.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.WindowStyle = 1; $s.Description = 'GSM Fix Hub Universal Flashing Suite by Bhuwan Bastola'; $s.Save()"

echo [*] Creating Start Menu Shortcut...
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $sm = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'GSM Fix Hub'); if (!(Test-Path $sm)) { New-Item -ItemType Directory -Path $sm }; $s = $ws.CreateShortcut([System.IO.Path]::Combine($sm, 'GSM Fix Hub Flasher Pro.lnk')); $s.TargetPath = '%INSTALL_DIR%\Run_GSM_Flasher.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo ===============================================================================
echo [SUCCESS] Installation Completed Successfully!
echo [*] Desktop Shortcut created: "GSM Fix Hub Flasher Pro"
echo [*] Software installed to: %INSTALL_DIR%
echo ===============================================================================
echo.
set /p LAUNCH_NOW="Do you want to launch GSM Fix Hub Flasher now? (Y/N): "
if /i "%LAUNCH_NOW%"=="Y" (
    start "" "%INSTALL_DIR%\Run_GSM_Flasher.bat"
)

exit /b 0
