"""Generate infographic/index.html from algorithms.py and diagrams.py.

The page doubles as the poster: export_poster.js adds body.poster, which fixes the grids
to four columns and hides the web-only elements (top bar, expandable details).
"""
import html
from pathlib import Path
from algorithms import ALGORITHMS, BANDS, DOMAINS, CONNECTIONS, MAP_ORDER, SHORT_NAME
from diagrams import DIAGRAMS, ICONS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "infographic" / "index.html"
DOMAIN_LABEL = dict(DOMAINS)
BY_NAME = {a["name"]: a for a in ALGORITHMS}

# Diagram to show for each node in the connection chains (some nodes are not in the 16)
NODE_FIG = {
    "Decision tree": "tree", "Random forest": "forest", "Gradient boosting": "boost",
    "Linear regression": "linreg", "Logistic regression": "logreg", "Neural network": "nn",
    "CNN and Transformer": "deep", "K-nearest neighbors": "knn", "K-means": "kmeans",
    "Recurrent network (LSTM)": "rnn", "Transformer": "transformer",
    "BERT, GPT, vision transformer": "heads", "GAN": "gan", "Diffusion model": "diffusion",
}

# Line colors for the map on black, bright enough to read on a dark background
LINE_COLOR = {"tabular": "#2997ff", "vision": "#bf5af2", "language": "#30d158", "generative": "#ff9f0a"}


def esc(s):
    return html.escape(s, quote=True)


def short(name):
    return SHORT_NAME.get(name, name)


def kind_badge(a):
    cls = "kind supervised" if a["kind"] == "Supervised" else "kind unsupervised"
    return f'<span class="{cls}">{esc(a["kind"])}</span>'


def chips(a):
    return "".join(f'<span class="chip {d}">{ICONS[d]}{esc(DOMAIN_LABEL[d])}</span>' for d in a["domains"])


def card(a):
    tags = "".join(f'<li>{esc(t)}</li>' for t in a["tags"])
    note = f'<p class="kind-note">{esc(a["kind_note"])}</p>' if a.get("kind_note") else ""
    return f"""
      <article class="card">
        <div class="fig">{DIAGRAMS[a["fig"]]()}</div>
        <h3>{esc(a["name"])}</h3>
        <p class="pills">{kind_badge(a)}<span class="task">{esc(a["task"])}</span></p>
        {note}
        <p class="pills">{chips(a)}</p>
        <p class="how">{esc(a["short"])}</p>
        <ul class="tags" aria-label="Used for">{tags}</ul>
        <details class="more">
          <summary>More</summary>
          <p><strong>How it works.</strong> {esc(a["how"])}</p>
          <p><strong>Used for.</strong> {esc(a["uses"])}</p>
        </details>
      </article>"""


def band(b, tone):
    key, title, desc = b
    cards = "".join(card(a) for a in ALGORITHMS if a["band"] == key)
    return f"""
  <section class="band {tone}" aria-labelledby="{key}">
    <div class="inner">
      <div class="band-head">
        <h2 id="{key}">{esc(title)}.</h2>
        <p>{esc(desc)}</p>
      </div>
      <div class="grid">{cards}
      </div>
    </div>
  </section>"""


def connections():
    items = []
    for c in CONNECTIONS:
        nodes = []
        for n in c["chain"]:
            nodes.append(f'<figure class="node"><div class="node-fig">{DIAGRAMS[NODE_FIG[n]]()}</div><figcaption>{esc(n)}</figcaption></figure>')
        row = '<span class="arrow" aria-hidden="true">&rarr;</span>'.join(nodes)
        items.append(f"""
        <li class="chain">
          <h3>{esc(c["title"])}</h3>
          <div class="chain-row">{row}</div>
          <p class="chain-note">{esc(c["note"])}</p>
        </li>""")
    return f"""
  <section class="connections light" aria-labelledby="connections-heading">
    <div class="inner">
      <div class="band-head">
        <h2 id="connections-heading">How they connect.</h2>
        <p>The bands sort algorithms by how they learn. These five chains show how they descend from one another, which is usually the fastest way to choose between neighbors on the map.</p>
      </div>
      <ul class="chains">{"".join(items)}
      </ul>
    </div>
  </section>"""


def domain_map():
    """Subway-style map: four domain lines, one station per algorithm, interchanges where lines meet."""
    width, height = 1240, 470
    line_y = {"tabular": 72, "vision": 150, "language": 228, "generative": 306}
    x0, x1 = 150, 1200
    n = len(MAP_ORDER)
    step = (x1 - x0 - 40) / (n - 1)
    xs = [x0 + 20 + i * step for i in range(n)]
    parts = [f'<svg class="map" viewBox="0 0 {width} {height}" role="img" aria-label="Map of sixteen algorithms as stations on four domain lines" xmlns="http://www.w3.org/2000/svg">']
    # lines and their names
    for d, label in DOMAINS:
        y = line_y[d]
        parts.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LINE_COLOR[d]}" stroke-width="12" stroke-linecap="round"/>')
        parts.append(f'<text x="{x0 - 16}" y="{y + 5}" text-anchor="end" fill="#f5f5f7" font-size="15" font-weight="600">{esc(label)}</text>')
    # stations
    for x, name in zip(xs, MAP_ORDER):
        a = BY_NAME[name]
        ys = [line_y[d] for d in a["domains"]]
        if len(ys) == 1:
            parts.append(f'<circle cx="{x:.1f}" cy="{ys[0]}" r="9" fill="#fff" stroke="{LINE_COLOR[a["domains"][0]]}" stroke-width="4"/>')
        else:
            top, bot = min(ys), max(ys)
            parts.append(f'<rect x="{x - 11:.1f}" y="{top - 11}" width="22" height="{bot - top + 22}" rx="11" fill="#fff"/>')
            for d in a["domains"]:
                parts.append(f'<circle cx="{x:.1f}" cy="{line_y[d]}" r="5.5" fill="{LINE_COLOR[d]}"/>')
        label_y = 332
        parts.append(f'<line x1="{x:.1f}" y1="{max(ys) + 12}" x2="{x:.1f}" y2="{label_y - 6}" stroke="#48484a" stroke-width="1.5"/>')
        parts.append(f'<text transform="translate({x - 4:.1f},{label_y}) rotate(42)" fill="#f5f5f7" font-size="14">{esc(short(name))}</text>')
    parts.append('</svg>')
    return f"""
  <section class="mapsec dark" aria-labelledby="map-heading">
    <div class="inner">
      <div class="band-head">
        <h2 id="map-heading">Where the lines meet.</h2>
        <p>Four domains as four lines. Each algorithm is a station; where a station spans several lines, the same algorithm serves several domains. Tabular data runs almost entirely on classical methods; vision, language, and generative AI are served by deep learning, and the transformer is the only station on three lines.</p>
      </div>
      {"".join(parts)}
    </div>
  </section>"""


def timeline():
    """Seventy years on one axis, with a bucket for the two methods older than 1950."""
    width, height = 1240, 250
    axis_y = 128
    x0, x1 = 215, 1210
    y0, y1 = 1950, 2025

    def xpos(year):
        return x0 + (year - y0) / (y1 - y0) * (x1 - x0)

    items = []
    for a in ALGORITHMS:
        if a["year"] < y0:
            continue
        items.append((xpos(a["year"]), a))
    items.sort(key=lambda t: t[0])

    parts = [f'<svg class="timeline" viewBox="0 0 {width} {height}" role="img" aria-label="Timeline of when each algorithm was introduced" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<line x1="{x0}" y1="{axis_y}" x2="{x1}" y2="{axis_y}" stroke="#1d1d1f" stroke-width="2"/>')
    for yr in range(1950, 2030, 10):
        x = xpos(yr)
        parts.append(f'<line x1="{x:.1f}" y1="{axis_y - 5}" x2="{x:.1f}" y2="{axis_y + 5}" stroke="#1d1d1f" stroke-width="2"/>')
        parts.append(f'<text x="{x:.1f}" y="{axis_y + 22}" text-anchor="middle" fill="#86868b" font-size="12">{yr}</text>')
    # pre-1950 bucket with an axis break
    parts.append(f'<line x1="50" y1="{axis_y}" x2="180" y2="{axis_y}" stroke="#1d1d1f" stroke-width="2"/>')
    parts.append(f'<path d="M188,{axis_y + 7} L196,{axis_y - 7} M200,{axis_y + 7} L208,{axis_y - 7}" stroke="#1d1d1f" stroke-width="2" fill="none"/>')
    parts.append(f'<text x="115" y="{axis_y + 22}" text-anchor="middle" fill="#86868b" font-size="12">before 1950</text>')
    old = [(88, BY_NAME["Linear regression"]), (142, BY_NAME["Principal component analysis"])]

    # greedy label placement on alternating sides and stacked levels
    above = [axis_y - 30, axis_y - 56, axis_y - 82]
    below = [axis_y + 50, axis_y + 76, axis_y + 102]
    occupied = {("a", i): -1e9 for i in range(3)}
    occupied.update({("b", i): -1e9 for i in range(3)})

    def place(x, a, prefer):
        """Pick the first free level on the preferred side, else the other side."""
        text = f'{short(a["name"])}, {a["year"]}'
        w = len(text) * 6.4
        order = ["a", "b"] if prefer == "a" else ["b", "a"]
        for side in order:
            for i in range(3):
                if occupied[(side, i)] + 12 < x - w / 2:
                    occupied[(side, i)] = x + w / 2
                    return side, i, text
        side = order[0]
        occupied[(side, 2)] = x + w / 2
        return side, 2, text

    all_items = old + items
    for k, (x, a) in enumerate(all_items):
        side, lvl, text = place(x, a, "a" if k % 2 == 0 else "b")
        ly = above[lvl] if side == "a" else below[lvl]
        fill = "#1d1d1f" if a["kind"] == "Supervised" else "#fff"
        parts.append(f'<line x1="{x:.1f}" y1="{axis_y}" x2="{x:.1f}" y2="{ly + (6 if side == "a" else -12)}" stroke="#d2d2d7" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{axis_y}" r="6" fill="{fill}" stroke="#1d1d1f" stroke-width="2"/>')
        anchor_y = ly if side == "a" else ly
        parts.append(f'<text x="{x:.1f}" y="{anchor_y}" text-anchor="middle" fill="#1d1d1f" font-size="12.5">{esc(text)}</text>')
    parts.append('</svg>')
    return f"""
  <section class="timesec light" aria-labelledby="time-heading">
    <div class="inner">
      <div class="band-head">
        <h2 id="time-heading">Seventy years, one line.</h2>
        <p>When each algorithm was introduced. Filled dots are supervised, hollow dots unsupervised. The classical toolkit was complete by about 2001; everything that serves vision, language, and generation at scale arrived after 2012, when deep learning became practical on GPUs.</p>
      </div>
      {"".join(parts)}
    </div>
  </section>"""


def legend():
    doms = "".join(f'<span class="chip {d}">{ICONS[d]}{esc(l)}</span>' for d, l in DOMAINS)
    return f"""
      <div class="legend" aria-label="How to read this framework">
        <div><p class="legend-title">Learns from</p><p><span class="kind supervised">Supervised</span> labeled examples</p><p><span class="kind unsupervised">Unsupervised</span> unlabeled data</p></div>
        <div><p class="legend-title">Task</p><p><span class="task">Classification</span> <span class="task">Clustering</span> <span class="task">Generation</span></p></div>
        <div><p class="legend-title">Used in</p><p>{doms}</p></div>
      </div>"""


CSS = """
  @font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-Regular.woff2") format("woff2"); font-weight: 400; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-Medium.woff2") format("woff2"); font-weight: 500; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-SemiBold.woff2") format("woff2"); font-weight: 600; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-Bold.woff2") format("woff2"); font-weight: 700; font-display: swap; }
  :root {
    --text: #1d1d1f; --text2: #6e6e73; --text3: #86868b; --white: #fff; --grey: #f5f5f7; --grey2: #e8e8ed; --rule: #d2d2d7;
    --blue: #0071e3; --link: #0066cc;
    --tabular: #0066cc; --tabular-bg: rgba(0,113,227,.10);
    --vision: #8a3fc7; --vision-bg: rgba(175,82,222,.13);
    --language: #1b7f3b; --language-bg: rgba(52,199,89,.16);
    --generative: #c25e00; --generative-bg: rgba(255,149,0,.16);
  }
  *, *::before, *::after { box-sizing: border-box; }
  html { font-size: 17px; -webkit-font-smoothing: antialiased; }
  body { margin: 0; background: var(--white); color: var(--text); line-height: 1.47;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif; }
  a { color: var(--link); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .inner { max-width: 1240px; margin: 0 auto; padding: 0 40px; }
  .light { background: var(--white); }
  .shade { background: var(--grey); }
  .dark { background: #000; color: #f5f5f7; }

  .topbar { font-size: 14px; padding: 14px 0 0; }
  body.poster .topbar { display: none; }

  .hero { padding: 72px 0 48px; text-align: center; }
  h1 { font-size: 56px; line-height: 1.07; font-weight: 600; letter-spacing: -0.02em; margin: 0 0 14px; }
  .hero .sub { font-size: 23px; line-height: 1.33; color: var(--text2); max-width: 46em; margin: 0 auto 36px; font-weight: 400; }
  .legend { display: flex; justify-content: center; gap: 48px; flex-wrap: wrap; text-align: left; font-size: 14px; color: var(--text2); }
  .legend p { margin: 0 0 8px; }
  .legend-title { font-weight: 600; color: var(--text); }

  .kind { display: inline-block; font-size: 12px; font-weight: 600; line-height: 1; padding: 6px 11px; border-radius: 980px; border: 1.5px solid var(--text); margin: 0 6px 6px 0; vertical-align: middle; }
  .kind.supervised { background: var(--text); color: #fff; }
  .kind.unsupervised { background: transparent; color: var(--text); }
  .task { display: inline-block; font-size: 12px; font-weight: 500; line-height: 1; padding: 6px 11px; border-radius: 980px; background: var(--grey2); color: var(--text); margin: 0 6px 6px 0; vertical-align: middle; }
  .chip { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 600; line-height: 1; padding: 6px 11px 6px 9px; border-radius: 980px; margin: 0 6px 6px 0; vertical-align: middle; white-space: nowrap; }
  .chip .ico { width: 13px; height: 13px; }
  .chip.tabular { color: var(--tabular); background: var(--tabular-bg); }
  .chip.vision { color: var(--vision); background: var(--vision-bg); }
  .chip.language { color: var(--language); background: var(--language-bg); }
  .chip.generative { color: var(--generative); background: var(--generative-bg); }

  section { padding: 64px 0; }
  .band-head { max-width: 760px; margin: 0 0 32px; }
  h2 { font-size: 40px; line-height: 1.1; font-weight: 600; letter-spacing: -0.015em; margin: 0 0 10px; }
  .band-head p { font-size: 19px; line-height: 1.42; color: var(--text2); margin: 0; }
  .dark .band-head p { color: #a1a1a6; }

  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 20px; }
  body.poster .grid { grid-template-columns: repeat(4, 1fr); }
  .card { border-radius: 18px; padding: 18px 18px 14px; background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); }
  .light .card { background: var(--grey); box-shadow: none; }
  .fig { border-radius: 12px; background: var(--grey); padding: 6px; margin-bottom: 14px; }
  .light .fig { background: var(--white); }
  .mini { width: 100%; height: auto; display: block; }
  .card h3 { font-size: 19px; line-height: 1.2; font-weight: 600; margin: 0 0 10px; letter-spacing: -0.01em; }
  .card .pills { margin: 0 0 4px; }
  .kind-note { font-size: 12px; color: var(--text2); margin: -2px 0 8px; }
  .card .how { font-size: 14px; line-height: 1.45; margin: 6px 0 10px; }
  .tags { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
  .tags li { font-size: 12px; color: var(--text2); background: var(--grey2); border-radius: 980px; padding: 5px 10px; line-height: 1.2; }
  .light .tags li { background: var(--white); }
  .more { margin-top: 10px; font-size: 13px; color: var(--text2); }
  .more summary { cursor: pointer; color: var(--link); font-weight: 500; }
  .more p { margin: 8px 0 0; }
  body.poster .more { display: none; }

  .chains { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(520px, 1fr)); gap: 20px; }
  body.poster .chains { grid-template-columns: repeat(2, 1fr); }
  .chain { background: var(--grey); border-radius: 18px; padding: 20px 22px 18px; }
  .chain:last-child:nth-child(odd) { grid-column: 1 / -1; }
  .chain h3 { font-size: 21px; font-weight: 600; letter-spacing: -0.01em; margin: 0 0 14px; }
  .chain-row { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; margin-bottom: 12px; }
  .node { margin: 0; width: 100px; text-align: center; }
  .node-fig { background: var(--white); border-radius: 12px; padding: 4px; }
  .node figcaption { font-size: 12px; font-weight: 500; margin-top: 6px; line-height: 1.25; }
  .arrow { font-size: 22px; color: var(--text3); padding: 0 1px 22px; }
  .chain-note { margin: 0; font-size: 14px; line-height: 1.45; color: var(--text2); }

  .map, .timeline { width: 100%; height: auto; display: block; }
  .map { font-family: inherit; }
  .timesec { padding-bottom: 40px; }

  .foot { padding: 28px 0 44px; font-size: 13px; color: var(--text2); }
  .foot .inner { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 32px; border-top: 1px solid var(--rule); padding-top: 20px; }
  .foot p { margin: 0 0 6px; }
  .credit { text-align: right; }
  @media (max-width: 760px) {
    h1 { font-size: 36px; } h2 { font-size: 30px; } .hero .sub { font-size: 19px; }
    .inner { padding: 0 20px; } section { padding: 44px 0; }
    .chains { grid-template-columns: 1fr; } .chain:last-child:nth-child(odd) { grid-column: auto; }
    .foot .inner { grid-template-columns: 1fr; } .credit { text-align: left; }
  }
  @media print { .topbar, .more { display: none; } .card, .chain { break-inside: avoid; } }
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Machine learning algorithms, mapped: 16 algorithms by learning type, task, and domain</title>
<meta name="description" content="A visual framework of 16 machine learning algorithms with a diagram of each idea, classified by learning type, task, and application domain, with a domain map, a timeline, and the connections between them.">
<style>{CSS}</style>
</head>
<body>
  <div class="inner"><p class="topbar"><a href="../artifacts/ml-algorithm-framework.html">&larr; Back to the artifact page</a></p></div>
  <main>
    <header class="hero light">
      <div class="inner">
        <h1>Machine learning algorithms, mapped.</h1>
        <p class="sub">Sixteen algorithms, from linear regression to diffusion models, each drawn as the idea behind it and classified by how it learns, what it does, and where it is used.</p>
        {legend()}
      </div>
    </header>
    {band(BANDS[0], "shade")}
    {band(BANDS[1], "light")}
    {band(BANDS[2], "shade")}
    {connections()}
    {domain_map()}
    {timeline()}
    <footer class="foot shade">
      <div class="inner">
        <div>
          <p>Transformers, GANs, and diffusion models are marked unsupervised because their training signal comes from the data itself (the next token, the real-or-fake contest, the noise that was added), not from human labels. A supervised fine-tuning stage usually follows for a specific task.</p>
          <p>Domain chips show where each algorithm is a standard choice today; most can be pushed into other domains with suitable feature engineering.</p>
        </div>
        <div class="credit">
          <p>Chittaranjan Rath</p>
          <p>AIML-501 Model Development, Indiana Wesleyan University, November 2026</p>
        </div>
      </div>
    </footer>
  </main>
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print("wrote", OUT, f"({len(ALGORITHMS)} algorithms)")
