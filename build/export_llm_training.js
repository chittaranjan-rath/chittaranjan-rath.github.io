// Export the LLM training infographic as a poster PNG (2x), a preview, a thumbnail and a single-page PDF.
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const root = path.resolve(__dirname, "..");
  const url = "file://" + path.join(root, "infographic", "llm-training", "index.html");
  const browser = await chromium.launch();

  // Open the page in poster mode (fixed four-, seven- and three-column layouts, no back link)
  const open = async (scale) => {
    const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: scale });
    await page.goto(url);
    await page.evaluate(() => document.body.classList.add("poster"));
    await page.evaluate(() => document.fonts.ready);
    return page;
  };

  const page = await open(2);
  await page.screenshot({ path: path.join(root, "assets", "downloads", "llm-training-costs.png"), fullPage: true });

  const preview = await open(1);
  await preview.screenshot({ path: path.join(root, "assets", "img", "llm-training-costs.png"), fullPage: true });
  await preview.screenshot({ path: path.join(root, "assets", "img", "llm-training-costs-thumb.png"), clip: { x: 0, y: 0, width: 1400, height: 1050 } });

  const height = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.pdf({
    path: path.join(root, "assets", "downloads", "llm-training-costs.pdf"),
    width: "1400px",
    height: `${height + 2}px`,
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  console.log("poster height (css px):", height);
  await browser.close();
})();
