$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$screensDir = Join-Path $root "docs\\screenshots"
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

  npx playwright screenshot --browser chromium --viewport-size "1440,1400" --wait-for-timeout 3000 http://127.0.0.1:8765 (Join-Path $screensDir "ui-overview.png")

  @'
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1400 } });
  await page.goto("http://127.0.0.1:8765", { waitUntil: "networkidle" });
  await page.click("#azureBtn");
  await page.waitForTimeout(1500);
  await page.locator('[data-demo-id="dashboards"]').scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: "docs/screenshots/ui-dashboard.png" });
  await browser.close();
})();
'@ | node
}
finally {
  Stop-Job $job | Out-Null
  Remove-Job $job | Out-Null
}
