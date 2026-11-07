
#define MyAppName "LinguaSync"
#define MyAppVersion "2.0.1"
#define MyAppPublisher "Maheswar Sahoo"
#define MyAppExeName "voice-translator.exe"

[Setup]
AppId={{8F6A1C24-9D73-4B51-A2E8-7C4D91F603B2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\LinguaSync
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=dist
OutputBaseFilename=LinguaSync_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "build\LinguaSync_Release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\LinguaSync"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\LinguaSync"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch LinguaSync"; Flags: postinstall skipifsilent
