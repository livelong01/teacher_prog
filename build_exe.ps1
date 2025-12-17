<#
Quick build script for Windows (PowerShell).

What it does:
- Installs PyInstaller into the project's venv (if missing)
- Runs PyInstaller to produce a single-file, windowed executable
- Bundles the `fotos` folder and `alunos.json` into the executable's output folder

Usage (from project root):
  .\build_exe.ps1

Notes:
- Requires PowerShell and the project's virtual environment at `venv`.
- The produced exe will be in `dist\main.exe` (rename if desired).
#>

Set-StrictMode -Version Latest

$venvPython = Join-Path -Path $PSScriptRoot -ChildPath "venv\Scripts\python.exe"
if (-Not (Test-Path $venvPython)) {
    Write-Error "Python executable not found at $venvPython. Ensure the venv exists."
    exit 1
}

Write-Host "Installing/ensuring PyInstaller in venv..."
& $venvPython -m pip install --upgrade pip setuptools wheel > $null
& $venvPython -m pip install pyinstaller > $null

$icon = Join-Path $PSScriptRoot "icon.ico"
$addData = "fotos;fotos"

Write-Host "Running PyInstaller (this may take a minute)..."
& $venvPython -m PyInstaller --noconfirm --onefile --windowed --clean --icon="$icon" --add-data $addData "main.py"

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed (exit $LASTEXITCODE)"
    exit $LASTEXITCODE
}

Write-Host "Build finished. Find the exe in the 'dist' folder (main.exe)."
