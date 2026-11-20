# Professional portfolio of Chittaranjan Rath

A static site (plain HTML and CSS, no build step needed to serve it) for the AI/ML professional portfolio at Indiana Wesleyan University.

## Publishing

This is the `chittaranjan-rath.github.io` repository, served by GitHub Pages at https://chittaranjan-rath.github.io/. Upload the contents of this folder to the root of the repository (replacing the old `index.html`) and commit; Pages redeploys within a minute or two.

The earlier coursework page that used to be the home page now lives at `previous-coursework/index.html` and is reachable from the "Earlier coursework" button on the home page and in the navigation.

The `.nojekyll` file tells GitHub Pages to serve the files exactly as they are.

## Layout

```
index.html                                   home: value proposition, artifact list, about me, skills, earlier coursework button
artifacts/explainable-ai.html                AIML-501 directed artifact 4: the explainable AI infographic (nine required fields)
infographic/explainable-ai/index.html        the explainable AI infographic as a live web page
artifacts/llm-training-costs.html            AIML-501 directed artifact 3: the LLM training infographic (nine required fields)
infographic/llm-training/index.html          the LLM training infographic as a live web page
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

## Regenerate the LLM training infographic

Every figure, with its source, lives in `build/build_llm_training.py`. After editing it:

```
python3 build/build_llm_training.py    # rewrites infographic/llm-training/index.html
node build/export_llm_training.js      # rewrites the PNG, PDF, preview and thumbnail (needs Playwright with Chromium)
node build/explanatory_doc.js          # rewrites the explanatory Word document (needs the docx package)
```

## Regenerate the explainable AI infographic

Every figure, with its source, lives in `build/build_explainable_ai.py`, and the reference list lives in `build/explainable_ai_refs.json`. After editing either:

```
python3 build/build_explainable_ai.py        # rewrites infographic/explainable-ai/index.html
node build/export_explainable_ai.js          # rewrites the PNG, PDF, preview and thumbnail (needs Playwright with Chromium)
python3 build/build_explainable_ai_page.py   # rewrites artifacts/explainable-ai.html (text, image height, references)
node build/explainable_ai_doc.js             # rewrites the explanatory Word document (needs the docx package)
```
