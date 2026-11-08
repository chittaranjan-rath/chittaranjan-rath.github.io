# Professional portfolio of Chittaranjan Rath

A static site (plain HTML and CSS, no build step needed to serve it) for the AI/ML professional portfolio at Indiana Wesleyan University.

## Publishing

This is the `chittaranjan-rath.github.io` repository, served by GitHub Pages at https://chittaranjan-rath.github.io/. Upload the contents of this folder to the root of the repository (replacing the old `index.html`) and commit; Pages redeploys within a minute or two.

The earlier coursework page that used to be the home page now lives at `previous-coursework/index.html` and is reachable from the "Earlier coursework" button on the home page and in the navigation.

The `.nojekyll` file tells GitHub Pages to serve the files exactly as they are.

## Layout

```
index.html                                   home: value proposition, artifact list, bio, earlier coursework button
artifacts/neural-network-components.html     AIML-501 directed artifact 2: the neural network presentation (nine required fields)
artifacts/ml-algorithm-framework.html        AIML-501 directed artifact 1 (nine required fields)
artifacts/decision-tree-fruit-classification.html   AIML-501 additional artifact
infographic/index.html                       the algorithm framework as a live web page
slides/neural-network-components/index.html  the neural network deck as a web slideshow (slide images + speaker notes)
assets/slides/neural-network-components/     the fifteen slide images used by the slideshow
previous-coursework/index.html               the earlier course portfolio (five artifacts), unchanged apart from links back
assets/css/site.css                          styles for the AIML-501 pages
assets/fonts/                                Inter (SIL Open Font License), self-hosted fallback for the system font
assets/img/                                  figures and thumbnails
assets/downloads/                            PNG, PDF, Word and PowerPoint deliverables
build/                                       scripts that generate the infographic and exports (not needed to serve the site)
build/neural-network-deck/                   figures.py (figures and experiments) and deck.js (the pptx) for the presentation
css/, js/, fonts/, img*.jpg                  files from the original repository; not referenced by any page, kept as they were
```

## Add a new artifact later

1. Copy `artifacts/ml-algorithm-framework.html` to a new file and replace the text under each of the nine headings (Introduction, Description, Objective, Process, Tools and technologies used, Value proposition, Unique value, Relevance, References).
2. Put the deliverable files in `assets/downloads/` and a figure or thumbnail in `assets/img/`.
3. Add a new `<li>` entry to the artifact list in `index.html`.

## Regenerate the infographic

The algorithm text lives in `build/algorithms.py` and the small diagrams in `build/diagrams.py`. After editing either:

```
python3 build/build_infographic.py    # rewrites infographic/index.html
node build/export_poster.js           # rewrites the PNG and PDF (needs Playwright with Chromium)
```

## Regenerate the neural network presentation

```
python3 build/neural-network-deck/figures.py --all   # figures + experiments (NumPy, scikit-learn, Matplotlib)
node build/neural-network-deck/deck.js               # the .pptx (pptxgenjs, react-icons, sharp)
```

Then export the PDF with LibreOffice, render the slide images with `pdftoppm`, and copy them into `assets/downloads/` and `assets/slides/neural-network-components/`. The slideshow page reads the images by number, so the file names must stay `slide-01.jpg` to `slide-15.jpg`.
