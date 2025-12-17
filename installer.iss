[Setup]
AppName=Meets dos Alunos
AppVersion=1.0
DefaultDirName={pf}\MeetsDosAlunos
DefaultGroupName=Meets dos Alunos
OutputBaseFilename=MeetsInstaller
Compression=lzma
SolidCompression=yes

[Files]
; Point this to the single exe (from PyInstaller) and resource folder in the project
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "fotos\*"; DestDir: "{app}\fotos"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "alunos.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Meets dos Alunos"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Run Meets dos Alunos"; Flags: nowait postinstall skipifsilent
