# Professional portfolio of Chittaranjan Rath

A static site (plain HTML and CSS, no build step needed to serve it) for the AI/ML professional portfolio at Indiana Wesleyan University.

## Publishing

This is the `chittaranjan-rath.github.io` repository, served by GitHub Pages at https://chittaranjan-rath.github.io/. Upload the contents of this folder to the root of the repository (replacing the old `index.html`) and commit; Pages redeploys within a minute or two.

The earlier coursework page that used to be the home page now lives at `previous-coursework/index.html` and is reachable from the "Earlier coursework" button on the home page and in the navigation.

The `.nojekyll` file tells GitHub Pages to serve the files exactly as they are.

## Layout

```
index.html                                   home: value proposition, artifact list, bio, earlier coursework button
artifacts/ml-algorithm-framework.html        AIML-501 artifact 1 (all nine required fields)
artifacts/decision-tree-fruit-classification.html   AIML-501 artifact 2
infographic/index.html                       the algorithm framework as a live web page
previous-coursework/index.html               the earlier course portfolio (five artifacts), unchanged apart from links back
assets/css/site.css                          styles for the AIML-501 pages
assets/fonts/                                Inter (SIL Open Font License), self-hosted fallback for the system font
assets/img/                                  figures and thumbnails
assets/downloads/                            PNG, PDF, and Word deliverables
build/                                       scripts that generate the infographic and exports (not needed to serve the site)
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
