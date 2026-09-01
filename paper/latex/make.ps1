param([ValidateSet('draft','release','clean')][string]$Task='draft')
$ErrorActionPreference = 'Stop'
$build = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
if ($Task -eq 'clean') { Get-ChildItem $build -Force | Remove-Item -Force -Recurse; exit 0 }
Push-Location $PSScriptRoot
try {
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
  if ($Task -eq 'release') { Copy-Item build/main.pdf build/release.pdf -Force }
} finally { Pop-Location }
