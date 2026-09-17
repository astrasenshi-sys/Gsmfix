; =============================================================================
; Inno Setup Script for GSM Fix Hub Universal Flasher Pro (Windows Installer)
; Architect: Bhuwan Bastola | Gopal Electronics, Surkhet, Nepal
; =============================================================================

[Setup]
AppName=GSM Fix Hub Universal Flasher Pro
AppVersion=5.0
AppPublisher=Bhuwan Bastola (Gopal Electronics, Surkhet)
AppPublisherURL=https://www.gsmfixhub.com/
AppSupportURL=https://www.gsmfixhub.com/#repository
AppUpdatesURL=https://www.gsmfixhub.com/
DefaultDirName={autopf}\GSM Fix Hub
DefaultGroupName=GSM Fix Hub
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=GSM_Fix_Hub_Setup_v5.0_Wizard
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GSM Fix Hub Universal Flasher Pro"; Filename: "{app}\Run_GSM_Flasher.bat"
Name: "{group}\{cm:UninstallProgram,GSM Fix Hub Universal Flasher Pro}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\GSM Fix Hub Universal Flasher Pro"; Filename: "{app}\Run_GSM_Flasher.bat"; Tasks: desktopicon

[Run]
Filename: "{app}\Run_GSM_Flasher.bat"; Description: "{cm:LaunchProgram,GSM Fix Hub Universal Flasher Pro}"; Flags: shellexec postinstall nowait skipifsilent
