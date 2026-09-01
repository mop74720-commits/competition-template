$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  if (-not (Test-Path .git)) { git init -b main }
  git status --short
  Write-Host "`nRepository initialized. Review files, then create the first commit when ready."
} finally { Pop-Location }
