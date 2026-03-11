$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$framesDir = Join-Path $root "docs\\demo-frames"
$screensDir = Join-Path $root "docs\\screenshots"

if (Test-Path $framesDir) {
  Remove-Item -Recurse -Force $framesDir
}
New-Item -ItemType Directory -Path $framesDir | Out-Null
if (-not (Test-Path $screensDir)) {
  New-Item -ItemType Directory -Path $screensDir | Out-Null
}

$job = Start-Job -ScriptBlock {
  param($repoRoot)
  Set-Location $repoRoot
  python -m copilot_sre ui --incident samples/incident-001 --host 127.0.0.1 --port 8765
} -ArgumentList $root

try {
  Start-Sleep -Seconds 4
  node (Join-Path $root "scripts\\playwright_capture_demo.js") $framesDir
  python (Join-Path $root "scripts\\make_demo_gif.py")
}
finally {
  Stop-Job $job | Out-Null
  Remove-Job $job | Out-Null
}
