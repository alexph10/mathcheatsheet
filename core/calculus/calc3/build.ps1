# Build calc3.pdf with tectonic.
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
    & $tectonic --synctex calc3.tex
    Write-Host "`nBuilt: $PSScriptRoot\calc3.pdf"
} finally {
    Pop-Location
}
