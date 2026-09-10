param(
  [ValidateSet('draft','review','release','print','all','clean')]
  [string]$Task = 'draft',
  [string]$Profile = 'generic',
  [string]$Engine = 'xelatex',
  [int]$Timeout = 180
)

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
  $python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
  }
  if (-not $python) {
    throw 'Python was not found in PATH.'
  }

  if ($python.Name -eq 'py.exe' -or $python.Name -eq 'py') {
    & $python.Source -3 build.py $Task --profile $Profile --engine $Engine --timeout $Timeout
  } else {
    & $python.Source build.py $Task --profile $Profile --engine $Engine --timeout $Timeout
  }

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
} finally {
  Pop-Location
}
