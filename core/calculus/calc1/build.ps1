# Build calc1.pdf with tectonic.
# Looks for tectonic on PATH, otherwise falls back to %USERPROFILE%\.local\bin\tectonic.exe.
$ErrorActionPreference = 'Stop'

$tectonic = (Get-Command tectonic -ErrorAction SilentlyContinue)?.Source
if (-not $tectonic) {
    $candidate = "$env:USERPROFILE\.local\bin\tectonic.exe"
    if (Test-Path $candidate) { $tectonic = $candidate }
}
if (-not $tectonic) {
    Write-Error "tectonic not found. Install from https://tectonic-typesetting.github.io/ or place tectonic.exe on PATH."
}

Push-Location $PSScriptRoot
try {
    & $tectonic --keep-logs --synctex calc1.tex
    Write-Host "`nBuilt: $PSScriptRoot\calc1.pdf"
} finally {
    Pop-Location
}
