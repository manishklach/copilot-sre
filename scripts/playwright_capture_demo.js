const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

async function captureFrame(page, outDir, name) {
  const filePath = path.join(outDir, name);
  await page.screenshot({ path: filePath });
  return filePath;
}

async function main() {
  const outDir = process.argv[2];
  if (!outDir) {
    throw new Error("Expected output directory argument");
  }
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1400 } });

  await page.goto("http://127.0.0.1:8765", { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await captureFrame(page, outDir, "frame-01.png");

  await page.click("#demoPlayBtn");
  await page.waitForTimeout(1600);
  await captureFrame(page, outDir, "frame-02.png");

  await page.waitForTimeout(4200);
  await captureFrame(page, outDir, "frame-03.png");

  await page.waitForTimeout(4200);
  await captureFrame(page, outDir, "frame-04.png");

  await page.waitForTimeout(4200);
  await captureFrame(page, outDir, "frame-05.png");

  await page.waitForTimeout(4200);
  await captureFrame(page, outDir, "frame-06.png");

  await page.waitForTimeout(4200);
  await captureFrame(page, outDir, "frame-07.png");

  await page.waitForTimeout(4200);
  await captureFrame(page, outDir, "frame-08.png");

  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
