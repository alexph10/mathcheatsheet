# Build calc2.pdf with tectonic.
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
    & $tectonic --synctex calc2.tex
    Write-Host "`nBuilt: $PSScriptRoot\calc2.pdf"
} finally {
    Pop-Location
}
