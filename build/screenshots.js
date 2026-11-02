// Render each page at desktop and phone widths for review.
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const root = path.resolve(__dirname, "..");
  const pages = [
    ["index.html", "home"],
    ["artifacts/ml-algorithm-framework.html", "artifact1"],
    ["artifacts/decision-tree-fruit-classification.html", "artifact2"],
    ["infographic/index.html", "infographic-web"],
  ];
  const browser = await chromium.launch();
  for (const [rel, name] of pages) {
    for (const [w, tag] of [[1280, "desktop"], [390, "phone"]]) {
      const page = await browser.newPage({ viewport: { width: w, height: 900 } });
      await page.goto("file://" + path.join(root, rel));
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: `/tmp/shot-${name}-${tag}.png`, fullPage: true });
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      console.log(name, tag, "height", h);
      await page.close();
    }
  }
  await browser.close();
})();
