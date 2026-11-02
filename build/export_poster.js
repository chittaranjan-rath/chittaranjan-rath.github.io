// Export the infographic as a poster PNG (2x) and a single-page PDF using the bundled Chromium.
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const root = path.resolve(__dirname, "..");
  const url = "file://" + path.join(root, "infographic", "index.html");
  const browser = await chromium.launch();

  // PNG at 2x device scale for a crisp download
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto(url);
  await page.evaluate(() => document.body.classList.add("poster"));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(root, "assets", "downloads", "ml-algorithm-framework.png"), fullPage: true });

  // A smaller preview image for the artifact page (1x)
  const preview = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1 });
  await preview.goto(url);
  await preview.evaluate(() => document.body.classList.add("poster"));
  await preview.evaluate(() => document.fonts.ready);
  await preview.screenshot({ path: path.join(root, "assets", "img", "ml-algorithm-framework.png"), fullPage: true });
  // Thumbnail: top of the poster, cropped 4:3
  await preview.screenshot({ path: path.join(root, "assets", "img", "ml-algorithm-framework-thumb.png"), clip: { x: 0, y: 0, width: 1400, height: 1050 } });

  // Single-page PDF sized to the poster
  const height = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.pdf({
    path: path.join(root, "assets", "downloads", "ml-algorithm-framework.pdf"),
    width: "1400px",
    height: `${height + 2}px`,
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  console.log("poster height (css px):", height);
  await browser.close();
})();
