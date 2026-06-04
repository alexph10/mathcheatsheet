# Build every NN-*.tex worksheet in this directory.
$ErrorActionPreference = 'Stop'

$tectonic = (Get-Command tectonic -ErrorAction SilentlyContinue)?.Source
if (-not $tectonic) {
    $candidate = "$env:USERPROFILE\.local\bin\tectonic.exe"
    if (Test-Path $candidate) { $tectonic = $candidate }
}
if (-not $tectonic) { Write-Error "tectonic not found." }

Push-Location $PSScriptRoot
try {
    Get-ChildItem -Filter '0*-*.tex' | ForEach-Object {
        Write-Host "==> $($_.Name)"
        & $tectonic $_.Name
    }
} finally { Pop-Location }
