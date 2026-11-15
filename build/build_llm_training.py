"""Build the LLM training infographic (infographic/llm-training/index.html).

Every number on the page lives in this file with its source, so a correction
here regenerates the cards, the charts and the table together.

    python3 build/build_llm_training.py
    node build/export_llm_training.js      # PNG, PDF, preview and thumbnail
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "infographic" / "llm-training" / "index.html"

# ---------------------------------------------------------------- palette
# Resource colors, validated with the dataviz palette checker (light surface).
DATA, COMPUTE, ENERGY, TIME, PEOPLE = "#0a84c9", "#8a3fc7", "#d97706", "#1b7f3b", "#6e6e73"

# ---------------------------------------------------------------- icons (24 x 24, stroke)
ICON = {
    "data": '<ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v6c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6M4.5 12v6c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-6"/>',
    "compute": '<rect x="6.5" y="6.5" width="11" height="11" rx="1.5"/><rect x="10" y="10" width="4" height="4"/><path d="M9.5 3v3.5M14.5 3v3.5M9.5 17.5V21M14.5 17.5V21M3 9.5h3.5M3 14.5h3.5M17.5 9.5H21M17.5 14.5H21"/>',
    "energy": '<path d="M13.5 2.5 5 13.5h6l-1 8 8.5-11h-6z"/>',
    "time": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
    "people": '<circle cx="12" cy="8" r="3.5"/><path d="M4.5 20.5c.8-4 3.8-6 7.5-6s6.700 2 7.500 6"/>',
    "collect": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.500c-3 3-3 14 0 17M12 3.500c3 3 3 14 0 17"/>',
    "clean": '<path d="M3.500 5h17l-6.500 7.500v6l-4 2v-8z"/>',
    "tokenize": '<rect x="3" y="9" width="5" height="6" rx="1"/><rect x="9.500" y="9" width="5" height="6" rx="1"/><rect x="16" y="9" width="5" height="6" rx="1"/><path d="M5.500 5v2M12 5v2M18.500 5v2M5.500 17v2M12 17v2M18.500 17v2"/>',
    "pretrain": '<circle cx="5" cy="7" r="2"/><circle cx="5" cy="17" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="7" r="2"/><circle cx="19" cy="17" r="2"/><path d="M6.700 8.200 10.300 10.800M6.700 15.800 10.300 13.200M13.700 10.800 17.300 8.200M13.700 13.200 17.300 15.800"/>',
    "finetune": '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    "evaluate": '<path d="M12 3 4.500 6v5.500c0 4.500 3 8 7.500 9.500 4.500-1.500 7.500-5 7.500-9.500V6z"/><path d="m8.500 12 2.500 2.500 4.500-5"/>',
    "deploy": '<path d="M7 18.500h10.500a4 4 0 0 0 .5-7.970A6 6 0 0 0 6.500 9.500 4.500 4.500 0 0 0 7 18.500z"/><path d="M12 16v-5M9.800 13l2.200-2.200 2.200 2.200"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.700" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def chip(kind, label=None):
    names = {"data": "Data", "compute": "Compute", "energy": "Energy", "time": "Time", "people": "People"}
    return f'<span class="chip {kind}">{icon(kind)}{label or names[kind]}</span>'


# ---------------------------------------------------------------- content
# Opening tiles. Three documented runs; the web page lets the reader switch, the poster shows the last.
# spark = the same quantity for all three models, in this order, for the small bars in each tile.
HERO_ORDER = ["gpt3", "llama2", "llama31"]
HERO_NAMES = {"gpt3": "GPT-3", "llama2": "Llama 2 70B", "llama31": "Llama 3.1 405B"}
HERO_CAPTION = {
    "gpt3": "GPT-3, OpenAI, 2020. Hardware, days and energy are independent estimates (Patterson et al., 2021).",
    "llama2": "Llama 2 70B, Meta, July 2023. Energy is calculated from published GPU-hours.",
    "llama31": "Llama 3.1 405B, Meta, July 2024. Energy and days are calculated from published GPU-hours.",
}
HERO = {
    "data": dict(label="Data", spark=[0.3, 2, 15], spark_unit="trillion tokens", models={
        "gpt3": ("300 billion", "tokens of text", "≈ 1,700 years of nonstop reading"),
        "llama2": ("2 trillion", "tokens of text", "≈ 11,000 years of nonstop reading"),
        "llama31": ("15 trillion+", "tokens of text", "≈ 85,000 years of nonstop reading"),
    }),
    "compute": dict(label="Compute", spark=[3.55, 1.72, 30.84], spark_unit="million GPU-hours", models={
        "gpt3": ("≈ 3.55 million", "GPU-hours on V100s", "≈ 400 years on a single GPU"),
        "llama2": ("1.72 million", "GPU-hours on A100s", "≈ 200 years on a single GPU"),
        "llama31": ("30.84 million", "GPU-hours on H100s", "≈ 3,500 years on a single GPU"),
    }),
    "energy": dict(label="Energy", spark=[1287, 688, 21588], spark_unit="MWh", models={
        "gpt3": ("1,287", "megawatt-hours", "≈ 120 US homes for a year"),
        "llama2": ("≈ 688", "megawatt-hours", "≈ 64 US homes for a year"),
        "llama31": ("≈ 21,600", "megawatt-hours", "≈ 2,000 US homes for a year"),
    }),
    "time": dict(label="Time", spark=[15, None, 80], spark_unit="days", models={
        "gpt3": ("≈ 15 days", "on about 10,000 GPUs", "Two weeks of a whole cluster"),
        "llama2": ("Not published", "run length for the 70B model", "Trained between Jan and Jul 2023"),
        "llama31": ("≈ 80 days", "on 16,000+ GPUs, nonstop", "Nearly a quarter of a year"),
    }),
}
HERO_FOOT = ("Reading time assumes 0.75 words per token and 250 words a minute. Homes use the rate implied by the "
             "GPT-3 comparison (about 10.7 MWh a year). GPU-hours for GPT-3 are 10,000 GPUs × 14.8 days.")

# Thickness of each resource at each step in the scale diagram (relative units, my judgment from the sources).
STREAM = [
    ("data", "Data", [5, 5, 3, 5, 3, 1, 0]),
    ("compute", "Compute", [1, 1, 1, 14, 3, 1, 3]),
    ("energy", "Energy", [1, 1, 1, 14, 1, 1, 3]),
    ("time", "Time", [2, 2, 1, 12, 2, 2, 1]),
    ("people", "People", [2, 2, 1, 2, 5, 5, 2]),
]

# What each resource buys, one line each (sits under the scale diagram).
WHY = [
    ("data", "Data", "sets what the model can know. Most raw text is thrown away before training."),
    ("compute", "Compute", "sets how large a model can be trained. Chips are 44% of the hardware bill."),
    ("energy", "Energy", "is 2 to 6% of the cost and all of the carbon footprint."),
    ("time", "Time", "sets how fast a lab can learn. A failed run costs weeks of a whole cluster."),
    ("people", "People", "curate data, tune and test. Staff are 29 to 49% of development cost."),
]

# Disclosure chart. State: P published by the developer, E estimate or calculation only, N not disclosed.
DISCLOSE_COLS = [("data", "Data"), ("compute", "Compute"), ("energy", "Energy"), ("time", "Time"), ("cost", "Cost")]
DISCLOSE = [
    ("GPT-3", "OpenAI, 2020", [("P", "300B tokens"), ("P", "3.14 × 10²³ operations"), ("E", "1,287 MWh"), ("E", "≈ 15 days"), ("E", "$4.3M")]),
    ("GPT-4", "OpenAI, 2023", [("N", ""), ("N", ""), ("N", ""), ("N", ""), ("E", "$78M")]),
    ("Gemini Ultra", "Google, 2023", [("N", ""), ("N", ""), ("N", ""), ("N", ""), ("E", "$191M")]),
    ("Claude", "Anthropic", [("N", ""), ("N", ""), ("N", ""), ("N", ""), ("E", "≈ $100M class")]),
    ("LLaMA 65B", "Meta, Feb 2023", [("P", "1.4T tokens"), ("P", "2,048 A100 GPUs"), ("P", "2,638 MWh, project"), ("P", "21 days"), ("N", "")]),
    ("Llama 2 70B", "Meta, Jul 2023", [("P", "2T tokens"), ("P", "1.72M GPU-hours"), ("P", "291 t CO₂e"), ("P", "Jan to Jul 2023"), ("E", "$3.9M")]),
    ("Llama 3.1 405B", "Meta, Jul 2024", [("P", "15T+ tokens"), ("P", "30.84M GPU-hours"), ("P", "8,930 t CO₂e"), ("E", "≈ 80 days"), ("N", "")]),
]

PHASES = [("Prepare", 3), ("Train", 1), ("Refine", 2), ("Release", 1)]

STEPS = [
    dict(n=1, key="collect", title="Collect data",
         what="Gather text at web scale: crawled pages, books, code, reference works.",
         fact="GPT-3 started from 45 TB of compressed Common Crawl text.",
         chips=["data", "time"]),
    dict(n=2, key="clean", title="Clean and curate",
         what="Filter for quality, remove duplicates and unsafe content, balance the mix.",
         fact="Filtering cut that 45 TB to 570 GB, about 1.3% of the original.",
         chips=["data", "people"]),
    dict(n=3, key="tokenize", title="Tokenize",
         what="Split text into sub-word tokens and map each one to a number the model can read.",
         fact="GPT-3 saw 300 billion tokens; Llama 3.1 saw over 15 trillion.",
         chips=["data"]),
    dict(n=4, key="pretrain", title="Pretrain",
         what="Predict the next token, measure the error, adjust billions of weights. Repeat for weeks.",
         fact="Llama 3.1 405B: 30.84 million GPU-hours on more than 16,000 H100s.",
         chips=["compute", "energy", "time"]),
    dict(n=5, key="finetune", title="Fine-tune and align",
         what="Teach the raw model to follow instructions and hold a conversation, using curated examples and human feedback.",
         fact="Llama 2 used over 1 million new human-annotated examples.",
         chips=["people", "data"]),
    dict(n=6, key="evaluate", title="Evaluate and test",
         what="Score the model on benchmarks, red-team it for harmful output, and decide whether it is ready.",
         fact="Llama 3.1 405B scored 85.2 on MMLU (5-shot) in its model card.",
         chips=["people", "time"]),
    dict(n=7, key="deploy", title="Deploy",
         what="Compress the model, serve it behind an API or release the weights, then monitor it in use.",
         fact="Meta released the Llama weights openly, so others can build on them without repeating the training.",
         chips=["compute", "energy"]),
]

# Three generations of Meta's flagship: (label, tokens in trillions, GPU-hours in millions, MWh).
LLAMA = [
    ("LLaMA 65B", "Feb 2023", 1.4, 1.03, 413),
    ("Llama 2 70B", "Jul 2023", 2.0, 1.72, 688),
    ("Llama 3.1 405B", "Jul 2024", 15.0, 30.84, 21588),
]

# Estimated cost of compute for the final training run, cloud rental prices (AI Index 2024).
COSTS = [
    (2017, "Transformer", 930, "$930"),
    (2019, "RoBERTa Large", 160018, "$160K"),
    (2020, "GPT-3", 4324883, "$4.3M"),
    (2022, "PaLM", 12389056, "$12.4M"),
    (2023, "Llama 2 70B", 3931897, "$3.9M"),
    (2023, "GPT-4", 78352034, "$78M"),
    (2023, "Gemini Ultra", 191400000, "$191M"),
]

# Hardware-side cost of a training run, average across frontier models (Cottier et al., 2024).
HARDWARE_SPLIT = [
    ("AI accelerator chips", 44, COMPUTE, "compute"),
    ("Other server parts", 29, "#b08ad9", "compute"),
    ("Cluster networking", 17, "#d3bdea", "compute"),
    ("Energy", 9, ENERGY, "energy"),
]
# Whole development cost of GPT-4 and Gemini Ultra class models (same source), as ranges.
DEV_SPLIT = [("Hardware", 47, 67, COMPUTE), ("R&D staff", 29, 49, PEOPLE), ("Energy", 2, 6, ENERGY)]

SOURCES = [
    "Brown et al. (2020), <em>Language models are few-shot learners</em>: GPT-3 size, data and filtering.",
    "Patterson et al. (2021), <em>Carbon emissions and large neural network training</em>: GPT-3 energy, emissions, GPU count and days.",
    "Touvron et al. (2023), LLaMA and Llama 2 papers; Meta (2024), Llama 3.1 model card and launch post: tokens, GPUs, GPU-hours, emissions.",
    "Maslej et al. (2024), <em>AI Index Report 2024</em>, Stanford HAI: training cost estimates at cloud rental prices.",
    "Cottier et al. (2024), <em>The rising costs of training frontier AI models</em>: cost shares, owned-hardware estimates, 2.4× yearly growth.",
    "Saul and Bass (2023), Bloomberg: US-homes comparison. Morales (2024), Tom's Hardware: Anthropic CEO on $100M and $1B runs.",
    "Wolfram (2023), <em>What is ChatGPT doing … and why does it work?</em>: the next-token training loop.",
]


# ---------------------------------------------------------------- pieces
def spark(key, vals, unit, active=2):
    """Three small bars (GPT-3, Llama 2, Llama 3.1) with the selected model at full strength."""
    W, H, bw, gap = 96, 44, 26, 9
    mx = max(v for v in vals if v is not None)
    out = [f'<svg class="spark" viewBox="0 0 {W} {H}" role="img" aria-label="{unit}: ' +
           ", ".join(f"{HERO_NAMES[m]} {'not published' if v is None else format(v, 'g')}" for m, v in zip(HERO_ORDER, vals)) + '">']
    for i, v in enumerate(vals):
        x = i * (bw + gap)
        if v is None:
            out.append(f'<rect class="sb na" data-i="{i}" x="{x + .5}" y="{H - 13.5}" width="{bw - 1}" height="13" rx="3" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>')
        else:
            h = max(3, (H - 2) * v / mx)
            out.append(f'<rect class="sb{" on" if i == active else ""}" data-i="{i}" x="{x}" y="{H - h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="currentColor"/>')
    out.append('</svg>')
    return "".join(out)


def hero_tiles():
    out = []
    for key in ["data", "compute", "energy", "time"]:
        t = HERO[key]
        big, unit, human = t["models"]["llama31"]
        out.append(f"""<div class="tile {key}" data-key="{key}">
  <div class="tile-top">{icon(key, "tile-ico")}<span class="tile-label">{t["label"]}</span>{spark(key, t["spark"], t["spark_unit"])}</div>
  <p class="big">{big}</p>
  <p class="unit">{unit}</p>
  <p class="human">{human}</p>
</div>""")
    return "\n".join(out)


def switcher():
    btns = "".join(f'<button type="button" data-model="{m}" aria-pressed="{"true" if m == "llama31" else "false"}">{HERO_NAMES[m]}</button>'
                   for m in HERO_ORDER)
    return f'<div class="switch" role="group" aria-label="Choose a model">{btns}</div>'


def hero_script():
    import json
    data = {k: v["models"] for k, v in HERO.items()}
    return ("<script>(function(){var D=" + json.dumps(data, ensure_ascii=False) + ",C=" + json.dumps(HERO_CAPTION, ensure_ascii=False) +
            ",O=" + json.dumps(HERO_ORDER) + r""";
var btns=document.querySelectorAll('.switch button');
function show(m){var i=O.indexOf(m);
  document.querySelectorAll('.tile').forEach(function(t){var d=D[t.dataset.key][m];
    t.querySelector('.big').textContent=d[0];t.querySelector('.unit').textContent=d[1];t.querySelector('.human').textContent=d[2];
    t.querySelectorAll('.sb').forEach(function(b){b.classList.toggle('on',+b.dataset.i===i);});});
  document.querySelector('.tiles-cap').textContent=C[m];
  btns.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.model===m?'true':'false');});}
btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.model);});});})();</script>""")


def stream_svg():
    """The pipeline drawn to scale: one layer per resource, thickness = how hard each step leans on it."""
    W, H, gap, unit, sep = 1160, 300, 14, 5.200, 2
    cw = (W - 6 * gap) / 7
    xs = [i * (cw + gap) + cw / 2 for i in range(7)]
    totals = [sum(layer[2][i] for layer in STREAM) for i in range(7)]
    colors = {"data": DATA, "compute": COMPUTE, "energy": ENERGY, "time": TIME, "people": "#8e8e93"}

    def edge(points, reverse=False):
        pts = [(0, points[0])] + list(zip(xs, points)) + [(W, points[-1])]
        if reverse:
            pts = pts[::-1]
        d = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            mid = (x0 + x1) / 2
            d.append(f"C{mid:.1f} {y0:.1f} {mid:.1f} {y1:.1f} {x1:.1f} {y1:.1f}")
        return pts[0], " ".join(d)

    out = [f'<svg class="stream" viewBox="0 0 {W} {H}" role="img" aria-labelledby="st-t st-d">',
           '<title id="st-t">The training pipeline drawn to scale</title>',
           '<desc id="st-d">A band flows left to right through the seven steps. It is thin through data collection, cleaning and tokenizing, '
           'swells to several times that thickness at pretraining where compute, energy and time dominate, then narrows through fine-tuning, '
           'evaluation and deployment, where people become the largest layer.</desc>',
           '<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".93" stop-color="#fff"/>'
           '<stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient>'
           f'<mask id="fm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>',
           f'<g mask="url(#fm)">']
    for x in xs:
        out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H}" stroke="#2c2c2e" stroke-dasharray="2 5"/>')
    acc = [0.0] * 7
    labels = []
    for key, name, vals in STREAM:
        top = [H / 2 - totals[i] * unit / 2 + acc[i] * unit for i in range(7)]
        bot = [top[i] + vals[i] * unit for i in range(7)]
        (sx, sy), d1 = edge(top)
        (ex, ey), d2 = edge(bot, reverse=True)
        out.append(f'<path d="M{sx} {sy:.1f} {d1} L{ex} {ey:.1f} {d2} Z" fill="{colors[key]}" stroke="#000" stroke-width="{sep}">'
                   f'<title>{name}</title></path>')
        i = max(range(7), key=lambda k: vals[k])  # label each layer where it is thickest
        if key == "people":
            i = 4
        labels.append((xs[i], (top[i] + bot[i]) / 2, name, vals[i] * unit))
        acc = [acc[k] + vals[k] for k in range(7)]
    out.append('</g>')
    for x, y, name, thick in labels:
        size = 15 if thick > 40 else 12
        out.append(f'<text x="{x:.1f}" y="{y + size * .36:.1f}" text-anchor="middle" class="stl" style="font-size:{size}px">{name}</text>')
    out.append(f'<text x="{W - 4}" y="{H / 2 - 28:.1f}" text-anchor="end" class="stn">continues as</text>')
    out.append(f'<text x="{W - 4}" y="{H / 2 - 13:.1f}" text-anchor="end" class="stn">daily use →</text>')
    out.append('</svg>')
    return "".join(out)


def pipeline():
    heads, col = [], 1
    for name, span in PHASES:
        heads.append(f'<div class="phase" style="grid-column:{col} / span {span}"><span>{name}</span></div>')
        col += span
    tops = "".join(f'<div class="st-head"><span class="num">{s["n"]}</span>{icon(s["key"], "step-ico")}<h3>{s["title"]}</h3></div>' for s in STEPS)
    cards = []
    for s in STEPS:
        chips = "".join(chip(c) for c in s["chips"])
        cards.append(f"""<li class="step">
  <h3 class="step-title"><span class="num">{s["n"]}</span>{s["title"]}</h3>
  <p class="what">{s["what"]}</p>
  <p class="fact">{s["fact"]}</p>
  <p class="needs">{chips}</p>
</li>""")
    why = "".join(f'<li class="{k}">{icon(k, "why-ico")}<p><b>{n}</b> {t}</p></li>' for k, n, t in WHY)
    return (f'<div class="phases" aria-hidden="true">{"".join(heads)}</div>\n<div class="st-heads" aria-hidden="true">{tops}</div>\n'
            f'<div class="scroll">{stream_svg()}</div>\n<ol class="steps">{"".join(cards)}</ol>\n<ul class="why">{why}</ul>')


def loop_svg():
    # Five stations on a loop: batch, predict, compare, adjust, repeat.
    boxes = [
        (24, 56, "1", "Take a batch of text", "“The cat sat on the …”", DATA),
        (319, 56, "2", "Predict the next token", "mat 41% · floor 22% · sofa 9%", COMPUTE),
        (614, 56, "3", "Compare with the truth", "Real token: “mat”. The gap is the loss", COMPUTE),
        (614, 222, "4", "Adjust the weights", "Backpropagation nudges each weight", ENERGY),
        (24, 222, "5", "Repeat", "Billions of batches, for weeks", TIME),
    ]
    parts = ['<svg class="loop" viewBox="0 0 900 378" role="img" aria-labelledby="loop-t loop-d">',
             '<title id="loop-t">The pretraining loop</title>',
             '<desc id="loop-d">Five steps in a cycle: take a batch of text, predict the next token, compare the prediction with the real token, adjust the weights, and repeat.</desc>',
             '<defs><marker id="ah" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#86868b"/></marker></defs>']
    for x, y, n, title, sub, color in boxes:
        parts.append(f'<g><rect x="{x}" y="{y}" width="262" height="100" rx="16" fill="#fff" stroke="#d2d2d7"/>'
                     f'<rect x="{x}" y="{y + 16}" width="5" height="68" rx="2.500" fill="{color}"/>'
                     f'<circle cx="{x + 36}" cy="{y + 34}" r="14" fill="#1d1d1f"/>'
                     f'<text x="{x + 36}" y="{y + 39}" text-anchor="middle" class="ln">{n}</text>'
                     f'<text x="{x + 60}" y="{y + 40}" class="lt">{title}</text>'
                     f'<text x="{x + 22}" y="{y + 76}" class="ls">{sub}</text></g>')
    arrows = ["M290 106H313", "M585 106H608", "M745 160V216", "M608 272H292", "M155 218V162"]
    for d in arrows:
        parts.append(f'<path d="{d}" stroke="#86868b" stroke-width="2" fill="none" marker-end="url(#ah)"/>')
    parts.append('<text x="450" y="260" text-anchor="middle" class="lc">one training step</text>')
    parts.append('</svg>')
    return "".join(parts)


def fmt(v, kind):
    if kind == "tokens":
        return f"{v:g}T"
    if kind == "hours":
        return f"{v:g}M"
    return f"{v:,.0f}"


def llama_panels():
    panels = [
        ("data", "Data", "Training tokens, trillions", 2, "tokens", DATA),
        ("compute", "Compute and time", "GPU-hours, millions", 3, "hours", COMPUTE),
        ("energy", "Energy", "Megawatt-hours (GPU-hours × rated GPU power)", 4, "mwh", ENERGY),
    ]
    out = []
    W, H, base, top, bw = 380, 215, 161, 34, 76
    for key, title, sub, idx, kind, color in panels:
        vals = [row[idx] for row in LLAMA]
        mx = max(vals)
        s = [f'<svg class="mini" viewBox="0 0 {W} {H}" role="img" aria-label="{title}: ' +
             ", ".join(f"{row[0]} {fmt(row[idx], kind)}" for row in LLAMA) + '">']
        s.append(f'<line x1="20" y1="{base}" x2="{W - 20}" y2="{base}" stroke="#d2d2d7"/>')
        for i, row in enumerate(LLAMA):
            v = row[idx]
            h = max(3, (base - top) * v / mx)
            x = 44 + i * 108
            y = base - h
            r = min(4, h)
            s.append(f'<path d="M{x} {base}V{y + r}q0-{r} {r}-{r}h{bw - 2 * r}q{r} 0 {r} {r}V{base}z" fill="{color}">'
                     f'<title>{row[0]} ({row[1]}): {fmt(v, kind)}</title></path>')
            s.append(f'<text x="{x + bw / 2}" y="{y - 8}" text-anchor="middle" class="bv">{fmt(v, kind)}</text>')
            s.append(f'<text x="{x + bw / 2}" y="{base + 20}" text-anchor="middle" class="bl">{row[0]}</text>')
            s.append(f'<text x="{x + bw / 2}" y="{base + 37}" text-anchor="middle" class="bd">{row[1]}</text>')
        s.append('</svg>')
        growth = vals[-1] / vals[0]
        out.append(f'''<figure class="panel">
  <figcaption>{chip(key, title)}<span class="psub">{sub}</span></figcaption>
  {"".join(s)}
  <p class="grow"><b>{growth:.0f}×</b> from the first generation to the third</p>
</figure>''')
    return "\n".join(out)


def cost_chart():
    W, H = 640, 350
    l, r, t, b = 64, 150, 24, 44
    x0, x1 = 2016.500, 2023.500
    y0, y1 = 2, 9  # log10 dollars

    def X(year):
        return l + (W - l - r) * (year - x0) / (x1 - x0)

    def Y(v):
        return H - b - (H - t - b) * (math.log10(v) - y0) / (y1 - y0)

    s = [f'<svg class="cost" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cost-t cost-d">',
         '<title id="cost-t">Estimated compute cost of the final training run, 2017 to 2023</title>',
         '<desc id="cost-d">Dot plot on a logarithmic dollar scale. ' +
         "; ".join(f"{n} ({y}) {lab}" for y, n, _, lab in COSTS) + '.</desc>']
    for e, lab in [(3, "$1K"), (4, "$10K"), (5, "$100K"), (6, "$1M"), (7, "$10M"), (8, "$100M")]:
        y = Y(10 ** e)
        s.append(f'<line x1="{l}" y1="{y:.1f}" x2="{W - r + 20}" y2="{y:.1f}" stroke="#d2d2d7"/>')
        s.append(f'<text x="{l - 10}" y="{y + 4:.1f}" text-anchor="end" class="ax">{lab}</text>')
    for year in range(2017, 2024):
        s.append(f'<text x="{X(year):.1f}" y="{H - b + 22}" text-anchor="middle" class="ax">{year}</text>')
    # label placement: (dx, dy, anchor) tuned by hand so nothing collides
    place = {"Transformer": (12, 4, "start"), "RoBERTa Large": (12, 4, "start"), "GPT-3": (-12, -8, "end"),
             "PaLM": (-12, -8, "end"), "Llama 2 70B": (14, 14, "start"), "GPT-4": (14, 6, "start"),
             "Gemini Ultra": (14, 0, "start")}
    for year, name, v, lab in COSTS:
        cx, cy = X(year), Y(v)
        dx, dy, anchor = place[name]
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{COMPUTE}" stroke="#f5f5f7" stroke-width="2">'
                 f'<title>{name} ({year}): about ${v:,.0f}</title></circle>')
        s.append(f'<text x="{cx + dx:.1f}" y="{cy + dy:.1f}" text-anchor="{anchor}" class="pl">{name} '
                 f'<tspan class="pv">{lab}</tspan></text>')
    s.append('</svg>')
    return "".join(s)


def hardware_bar():
    W, H, x, w, y, h = 560, 150, 0, 560, 46, 40
    total = sum(p for _, p, _, _ in HARDWARE_SPLIT)
    s = [f'<svg class="stack" viewBox="0 0 {W} {H}" role="img" aria-label="Hardware-side cost of a training run: ' +
         ", ".join(f"{n} {p} percent" for n, p, _, _ in HARDWARE_SPLIT) + '">']
    cx = x
    for i, (name, pct, color, _) in enumerate(HARDWARE_SPLIT):
        seg = w * pct / total
        gap = 0 if i == len(HARDWARE_SPLIT) - 1 else 2
        s.append(f'<rect x="{cx:.1f}" y="{y}" width="{seg - gap:.1f}" height="{h}" rx="4" fill="{color}">'
                 f'<title>{name}: {pct}%</title></rect>')
        s.append(f'<text x="{cx + 2:.1f}" y="{y - 12}" class="sv">{pct}%</text>')
        for j, word in enumerate({"AI accelerator chips": ["AI accelerator", "chips"], "Other server parts": ["Other server", "parts"]}.get(name, name.split(" "))):
            s.append(f'<text x="{cx + 2:.1f}" y="{y + h + 20 + 17 * j}" class="sl">{word}</text>')
        cx += seg
    s.append('</svg>')
    return "".join(s)


def dev_ranges():
    W, rowh = 560, 44
    H = rowh * len(DEV_SPLIT) + 34
    l, r = 96, 20

    def X(p):
        return l + (W - l - r) * p / 80

    s = [f'<svg class="ranges" viewBox="0 0 {W} {H}" role="img" aria-label="Share of total development cost: ' +
         ", ".join(f"{n} {a} to {b} percent" for n, a, b, _ in DEV_SPLIT) + '">']
    for p in range(0, 81, 10):
        s.append(f'<line x1="{X(p):.1f}" y1="4" x2="{X(p):.1f}" y2="{H - 30}" stroke="#d2d2d7"/>')
        s.append(f'<text x="{X(p):.1f}" y="{H - 10}" text-anchor="middle" class="ax">{p}%</text>')
    for i, (name, a, b, color) in enumerate(DEV_SPLIT):
        y = 10 + i * rowh
        s.append(f'<text x="0" y="{y + 17}" class="sl">{name}</text>')
        s.append(f'<rect x="{X(a):.1f}" y="{y + 2}" width="{X(b) - X(a):.1f}" height="22" rx="4" fill="{color}">'
                 f'<title>{name}: {a} to {b}% of development cost</title></rect>')
        s.append(f'<text x="{X(b) + 8:.1f}" y="{y + 18}" class="sv2">{a}–{b}%</text>')
    s.append('</svg>')
    return "".join(s)


def disclosure():
    state_word = {"P": "published by the developer", "E": "estimate or calculation only", "N": "not disclosed"}
    head = "".join(f'<th scope="col">{chip(k, n) if k != "cost" else "<span class=\"chip cost\">Cost</span>"}</th>' for k, n in DISCLOSE_COLS)
    rows = []
    for name, who, cells in DISCLOSE:
        tds = []
        for (k, _), (state, text) in zip(DISCLOSE_COLS, cells):
            tds.append(f'<td><div class="cell"><span class="sq {state} {k}" title="{name}, {k}: {state_word[state]}"></span>'
                       f'<span class="sqv">{text or "<span class=\"sr\">not disclosed</span>"}</span></div></td>')
        n = sum(1 for st, _ in cells if st == "P")
        rows.append(f'<tr><th scope="row"><span class="mname">{name}</span><span class="mwho">{who}</span></th>{"".join(tds)}'
                    f'<td class="count"><b>{n}</b> of 5</td></tr>')
    return f"""<table class="disc">
<thead><tr><th scope="col" class="first">Model</th>{head}<th scope="col" class="count">Published</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>"""


CSS = """
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Regular.woff2") format("woff2"); font-weight: 400; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Medium.woff2") format("woff2"); font-weight: 500; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-SemiBold.woff2") format("woff2"); font-weight: 600; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Bold.woff2") format("woff2"); font-weight: 700; font-display: swap; }
  :root {
    --text: #1d1d1f; --text2: #6e6e73; --text3: #86868b; --white: #fff; --grey: #f5f5f7; --grey2: #e8e8ed; --rule: #d2d2d7;
    --blue: #0071e3; --link: #0066cc;
    --data: #0a84c9; --data-ink: #0066a8; --data-bg: rgba(10,132,201,.11);
    --compute: #8a3fc7; --compute-ink: #7a32b5; --compute-bg: rgba(138,63,199,.11);
    --energy: #d97706; --energy-ink: #b45309; --energy-bg: rgba(217,119,6,.13);
    --time: #1b7f3b; --time-ink: #1b7f3b; --time-bg: rgba(27,127,59,.12);
    --people: #6e6e73; --people-ink: #55555a; --people-bg: rgba(110,110,115,.12);
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
  .scroll, .matrix td { position: relative; }
  .sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }

  .topbar { font-size: 14px; padding: 14px 0 0; margin: 0; }
  .topwrap a { color: #2997ff; }
  body.poster .topwrap { display: none; }
  body.poster .topbar { display: none; }

  .hero { padding: 76px 0 40px; text-align: center; }
  .hero.dark { background: #000; }
  .eyebrow { font-size: 14px; font-weight: 600; color: #a1a1a6; letter-spacing: .02em; margin: 0 0 12px; }
  h1 { font-size: 64px; line-height: 1.05; font-weight: 600; letter-spacing: -0.025em; margin: 0 0 16px; text-wrap: balance; }
  .hero .sub { font-size: 23px; line-height: 1.33; color: #a1a1a6; max-width: 40em; margin: 0 auto 32px; text-wrap: balance; }
  .switch { display: inline-flex; gap: 4px; padding: 4px; border-radius: 980px; background: #1d1d1f; margin: 0 0 24px; }
  .switch button { font: inherit; font-size: 14px; font-weight: 500; color: #a1a1a6; background: none; border: 0; padding: 8px 18px; border-radius: 980px; cursor: pointer; }
  .switch button:hover { color: #f5f5f7; }
  .switch button[aria-pressed="true"] { background: #f5f5f7; color: #1d1d1f; }
  .switch button:focus-visible { outline: 3px solid var(--blue); outline-offset: 2px; }
  body.poster .switch { display: none; }
  .tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: left; }
  .tile { background: #1d1d1f; border-radius: 18px; padding: 22px 22px 20px; border-top: 5px solid var(--c); }
  .tile.data { --c: var(--data); --ink: #6cc0f5; } .tile.compute { --c: var(--compute); --ink: #c79bf2; }
  .tile.energy { --c: var(--energy); --ink: #f5b55a; } .tile.time { --c: var(--time); --ink: #6fd08c; }
  .tile-top { display: flex; align-items: flex-end; gap: 8px; color: var(--ink); font-weight: 600; font-size: 15px; }
  .tile-ico { width: 24px; height: 24px; }
  .spark { width: 96px; height: 44px; margin-left: auto; color: var(--c); }
  .spark .sb { opacity: .5; transition: opacity .2s; }
  .spark .sb.on { opacity: 1; }
  .spark .sb.na { opacity: .5; color: #86868b; }
  .spark .sb.na.on { opacity: 1; }
  .big { font-size: 38px; line-height: 1.05; font-weight: 600; letter-spacing: -0.02em; margin: 18px 0 2px; white-space: nowrap; }
  .unit { font-size: 16px; font-weight: 500; color: #d2d2d7; margin: 0 0 14px; }
  .human { font-size: 15px; line-height: 1.35; font-weight: 600; color: var(--ink); margin: 0; padding-top: 12px; border-top: 1px solid #38383a; }
  .tiles-cap { font-size: 14px; color: #a1a1a6; margin: 18px 0 4px; }
  .tiles-foot { font-size: 12px; color: #86868b; margin: 0 auto; max-width: 70em; }
  .mini-legend { display: none; }

  .chip { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 600; line-height: 1; padding: 6px 11px 6px 8px; border-radius: 980px; margin: 0 6px 6px 0; vertical-align: middle; white-space: nowrap; }
  .chip .ico { width: 14px; height: 14px; }
  .chip.data { color: var(--data-ink); background: var(--data-bg); }
  .chip.compute { color: var(--compute-ink); background: var(--compute-bg); }
  .chip.energy { color: var(--energy-ink); background: var(--energy-bg); }
  .chip.time { color: var(--time-ink); background: var(--time-bg); }
  .chip.people { color: var(--people-ink); background: var(--people-bg); }
  .chip.cost { color: var(--text); background: var(--grey2); padding-left: 11px; }

  section { padding: 56px 0; }
  .band-head { max-width: 800px; margin: 0 0 28px; }
  h2 { font-size: 40px; line-height: 1.1; font-weight: 600; letter-spacing: -0.015em; margin: 0 0 10px; }
  .band-head p { font-size: 19px; line-height: 1.42; color: var(--text2); margin: 0; }
  .dark .band-head p { color: #a1a1a6; }

  /* pipeline, drawn to scale */
  .scale { padding-top: 40px; }
  .phases { display: grid; grid-template-columns: repeat(7, 1fr); gap: 14px; margin-bottom: 14px; }
  .phase { font-size: 13px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: #a1a1a6; border-bottom: 2px solid #f5f5f7; padding-bottom: 6px; }
  .st-heads { display: grid; grid-template-columns: repeat(7, 1fr); gap: 14px; }
  .st-head { text-align: center; }
  .st-head .num { margin: 0 auto 6px; }
  .st-head .step-ico { display: block; margin: 0 auto 6px; width: 30px; height: 30px; color: #f5f5f7; }
  .st-head h3 { font-size: 16px; font-weight: 600; letter-spacing: -0.01em; margin: 0; line-height: 1.2; }
  .num { display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: #f5f5f7; color: #000; font-size: 13px; font-weight: 600; }
  .stream { width: 100%; height: auto; display: block; margin: 10px 0 6px; }
  .stream .stl { font-weight: 600; fill: #fff; paint-order: stroke; stroke: rgba(0,0,0,.35); stroke-width: 2.500px; }
  .stream .stn { font-size: 12px; fill: #a1a1a6; }
  .stream-cap { font-size: 13px; color: #86868b; margin: 0 0 22px; max-width: 70em; }
  .steps { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(7, 1fr); gap: 14px; }
  .step { background: #1d1d1f; border-radius: 14px; padding: 14px 13px 8px; display: flex; flex-direction: column; }
  .step-title { display: none; font-size: 17px; font-weight: 600; margin: 0 0 8px; align-items: center; gap: 8px; }
  .what { font-size: 13px; line-height: 1.42; margin: 0 0 10px; color: #f5f5f7; }
  .fact { font-size: 12px; line-height: 1.4; color: #a1a1a6; border-left: 2px solid #48484a; padding: 0 0 0 9px; margin: 0 0 12px; }
  .needs { margin: auto 0 0; }
  .needs .chip { font-size: 11px; padding: 5px 9px 5px 7px; margin-right: 4px; }
  .dark .chip.data { color: #6cc0f5; background: rgba(10,132,201,.24); }
  .dark .chip.compute { color: #c79bf2; background: rgba(138,63,199,.28); }
  .dark .chip.energy { color: #f5b55a; background: rgba(217,119,6,.24); }
  .dark .chip.time { color: #6fd08c; background: rgba(27,127,59,.30); }
  .dark .chip.people { color: #c7c7cc; background: rgba(142,142,147,.24); }
  .why { list-style: none; margin: 28px 0 0; padding: 22px 0 0; border-top: 1px solid #38383a; display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; }
  .why li { display: flex; gap: 10px; align-items: flex-start; }
  .why-ico { width: 22px; height: 22px; flex: none; margin-top: 1px; }
  .why .data { color: #6cc0f5; } .why .compute { color: #c79bf2; } .why .energy { color: #f5b55a; } .why .time { color: #6fd08c; } .why .people { color: #c7c7cc; }
  .why p { font-size: 13px; line-height: 1.42; color: #a1a1a6; margin: 0; }
  .why b { color: #f5f5f7; font-weight: 600; }

  /* loop */
  .loopwrap { display: grid; grid-template-columns: minmax(0, 1.700fr) minmax(0, 1fr); gap: 40px; align-items: center; }
  .loop { width: 100%; height: auto; display: block; background: var(--grey); border-radius: 18px; }
  .loop .ln { font-size: 14px; font-weight: 600; fill: #fff; }
  .loop .lt { font-size: 17px; font-weight: 600; fill: var(--text); }
  .loop .ls { font-size: 13px; fill: var(--text2); }
  .loop .lc { font-size: 13px; font-weight: 600; fill: var(--text3); letter-spacing: .04em; text-transform: uppercase; }
  .loopside p { font-size: 16px; line-height: 1.5; margin: 0 0 14px; }
  .loopside .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .loopside .callout { background: var(--grey); border-radius: 18px; padding: 18px 20px; }
  .loopside .callout b { display: block; font-size: 26px; white-space: nowrap; line-height: 1.1; font-weight: 600; letter-spacing: -0.02em; }
  .loopside .callout span { font-size: 14px; color: var(--text2); }

  /* llama panels */
  .panels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .panel { margin: 0; background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 18px; padding: 20px 20px 16px; }
  .panel figcaption { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; margin-bottom: 4px; }
  .panel figcaption .chip { font-size: 13px; margin: 0 0 4px; }
  .psub { font-size: 13px; color: var(--text2); }
  .mini { width: 100%; height: auto; display: block; }
  .mini .bv { font-size: 15px; font-weight: 600; fill: var(--text); }
  .mini .bl { font-size: 12px; font-weight: 600; fill: var(--text); }
  .mini .bd { font-size: 11px; fill: var(--text2); }
  .grow { font-size: 14px; color: var(--text2); margin: 6px 0 0; }
  .grow b { font-size: 24px; color: var(--text); font-weight: 600; letter-spacing: -0.015em; margin-right: 4px; }
  .chart-note { font-size: 13px; color: var(--text2); margin: 16px 0 0; max-width: 62em; }

  /* cost */
  .costgrid { display: grid; grid-template-columns: minmax(0, 1.150fr) minmax(0, 1fr); gap: 20px; }
  .cardbox { background: var(--grey); border-radius: 18px; padding: 22px 24px 20px; }
  .cardbox h3 { font-size: 19px; font-weight: 600; letter-spacing: -0.01em; margin: 0 0 4px; }
  .cardbox .csub { font-size: 13px; color: var(--text2); margin: 0 0 12px; }
  .cardbox + .cardbox { margin-top: 20px; }
  .cost, .stack, .ranges { width: 100%; height: auto; display: block; }
  .ax { font-size: 12px; fill: var(--text3); }
  .pl { font-size: 13px; font-weight: 500; fill: var(--text); }
  .pv { font-weight: 700; }
  .sv { font-size: 17px; font-weight: 600; fill: var(--text); }
  .sv2 { font-size: 14px; font-weight: 600; fill: var(--text); }
  .sl { font-size: 13px; fill: var(--text2); }
  .rate { display: flex; align-items: baseline; gap: 12px; margin-top: 10px; padding-top: 14px; border-top: 1px solid var(--rule); }
  .rate b { font-size: 34px; font-weight: 600; letter-spacing: -0.02em; line-height: 1; white-space: nowrap; }
  .rate span { font-size: 14px; color: var(--text2); line-height: 1.4; }

  /* disclosure chart */
  .disc { width: 100%; border-collapse: collapse; table-layout: fixed; }
  .disc thead th { text-align: left; padding: 0 10px 10px; border-bottom: 2px solid var(--text); font-size: 13px; vertical-align: bottom; }
  .disc thead th.first { width: 190px; padding-left: 0; }
  .disc thead .chip { margin: 0; }
  .disc th.count, .disc td.count { width: 110px; text-align: right; padding-right: 0; }
  .shade .sq.N { background: var(--grey); }
  .disc tbody th { text-align: left; padding: 12px 10px 12px 0; border-bottom: 1px solid var(--rule); font-weight: 400; }
  .disc td { padding: 12px 10px; border-bottom: 1px solid var(--rule); vertical-align: middle; position: relative; }
  .disc td .cell { display: flex; align-items: center; }
  .disc td .sq { flex: none; }
  .disc tbody tr:nth-child(4) th, .disc tbody tr:nth-child(4) td { border-bottom: 2px solid var(--text3); }
  .mname { display: block; font-size: 17px; font-weight: 600; letter-spacing: -0.01em; }
  .mwho { display: block; font-size: 12px; color: var(--text2); }
  .sq { display: inline-block; width: 26px; height: 26px; border-radius: 7px; vertical-align: middle; margin-right: 10px; --c: var(--text); }
  .sq.data { --c: var(--data); } .sq.compute { --c: var(--compute); } .sq.energy { --c: var(--energy); } .sq.time { --c: var(--time); } .sq.cost { --c: #48484a; }
  .sq.P { background: var(--c); }
  .sq.E { background: repeating-linear-gradient(135deg, var(--c) 0 3px, transparent 3px 7px); box-shadow: inset 0 0 0 2px var(--c); }
  .sq.N { box-shadow: inset 0 0 0 1.500px var(--rule); background: var(--white); }
  .sqv { font-size: 13px; vertical-align: middle; }
  .disc td.count { font-size: 13px; color: var(--text2); }
  .disc td.count b { font-size: 22px; font-weight: 600; color: var(--text); letter-spacing: -0.015em; }
  .key { font-size: 13px; color: var(--text2); margin: 16px 0 0; max-width: 74em; line-height: 1.6; }
  .key .sq { width: 16px; height: 16px; border-radius: 4px; margin: 0 6px 0 0; vertical-align: -3px; --c: var(--text2); }
  .key span.k { white-space: nowrap; margin-right: 18px; }

  /* takeaways */
  .takes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .take { background: #1d1d1f; border-radius: 18px; padding: 24px; }
  .take b { display: block; font-size: 44px; font-weight: 600; letter-spacing: -0.02em; line-height: 1; margin-bottom: 12px; }
  .take h3 { font-size: 19px; font-weight: 600; margin: 0 0 6px; }
  .take p { font-size: 15px; line-height: 1.45; color: #a1a1a6; margin: 0; }

  .foot { padding: 28px 0 44px; font-size: 13px; color: var(--text2); }
  .foot .inner { display: grid; grid-template-columns: minmax(0, 2.200fr) minmax(0, 1fr); gap: 32px; }
  .foot p { margin: 0 0 6px; }
  .foot ol { margin: 0; padding-left: 1.3em; }
  .foot li { margin-bottom: 3px; }
  .credit { text-align: right; }

  @media (max-width: 1100px) {
    body:not(.poster) .tiles { grid-template-columns: repeat(2, 1fr); }
    body:not(.poster) .steps { grid-template-columns: repeat(2, 1fr); }
    body:not(.poster) .st-heads, body:not(.poster) .phases { display: none; }
    body:not(.poster) .step-title { display: flex; }
    body:not(.poster) .why { grid-template-columns: repeat(2, 1fr); }
    body:not(.poster) .panels, body:not(.poster) .takes, body:not(.poster) .costgrid, body:not(.poster) .loopwrap { grid-template-columns: 1fr; }
    body:not(.poster) .scroll { overflow-x: auto; }
    body:not(.poster) .disc { min-width: 900px; }
  }
  @media (max-width: 760px) {
    body:not(.poster) h1 { font-size: 38px; } body:not(.poster) h2 { font-size: 30px; } body:not(.poster) .hero .sub { font-size: 19px; }
    body:not(.poster) .inner { padding: 0 20px; } body:not(.poster) section { padding: 44px 0; }
    body:not(.poster) .tiles, body:not(.poster) .steps, body:not(.poster) .why { grid-template-columns: 1fr; }
    body:not(.poster) .switch button { padding: 8px 12px; font-size: 13px; }
    body:not(.poster) .stream, body:not(.poster) .loop { min-width: 720px; }
    body:not(.poster) .foot .inner { grid-template-columns: 1fr; } body:not(.poster) .credit { text-align: left; }
  }
  @media print { .topbar { display: none; } .step, .panel, .cardbox, .take { break-inside: avoid; } }
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What it takes to train a large language model: seven steps and four resources</title>
<meta name="description" content="An infographic of the seven steps in training a generative AI large language model, the four resources each step consumes (data, compute, energy, time), and documented figures for GPT-3, GPT-4, Gemini Ultra, LLaMA and Claude.">
<style>{CSS}</style>
</head>
<body>
<div class="dark topwrap"><div class="inner"><p class="topbar"><a href="../../artifacts/llm-training-costs.html">&larr; Back to the artifact page</a></p></div></div>

<header class="hero dark">
  <div class="inner">
    <p class="eyebrow">Generative AI infrastructure</p>
    <h1>What it takes to train a large language model</h1>
    <p class="sub">Seven steps turn raw text into a deployed model. Four resources pay for them: data, compute, energy and time.</p>
    {switcher()}
    <div class="tiles">
{hero_tiles()}
    </div>
    <p class="tiles-cap">{HERO_CAPTION["llama31"]}</p>
    <p class="tiles-foot">Small bars compare GPT-3, Llama 2 70B and Llama 3.1 405B, in that order. {HERO_FOOT}</p>
  </div>
</header>

<section class="dark scale">
  <div class="inner">
    <div class="band-head">
      <h2>The pipeline, drawn to scale</h2>
      <p>Seven steps in four phases. The band is as thick as the demand each step puts on each resource, so the cost of pretraining is visible before you read a word.</p>
    </div>
    {pipeline()}
    <p class="stream-cap" style="margin-top:18px">Band thickness is my own estimate from the sources, on a relative scale. No lab publishes a step-by-step breakdown, so read the shape and ignore the exact widths.</p>
  </div>
</section>

<section class="light">
  <div class="inner">
    <div class="band-head">
      <h2>Inside step 4: the pretraining loop</h2>
      <p>Almost all of the compute, energy and time goes into one small cycle repeated an enormous number of times.</p>
    </div>
    <div class="loopwrap">
      <div class="scroll">{loop_svg()}</div>
      <div class="loopside">
        <p>The model reads a stretch of text and guesses the token that comes next. The guess is compared with the real token, and every weight is nudged slightly toward a better guess. No human labels are needed, because the text supplies its own answers.</p>
        <div class="pair"><div class="callout"><b>175 billion</b><span>weights adjusted in GPT-3</span></div>
        <div class="callout"><b>300 billion</b><span>tokens, each one a prediction to check</span></div></div>
      </div>
    </div>
  </div>
</section>

<section class="shade">
  <div class="inner">
    <div class="band-head">
      <h2>One model family, three generations</h2>
      <p>Meta publishes more training detail than any other frontier lab, so its LLaMA line shows how fast every resource grows from one generation to the next.</p>
    </div>
    <div class="panels">
{llama_panels()}
    </div>
    <p class="chart-note">Each panel has its own scale. GPU-hours for LLaMA 65B are calculated from the paper (2,048 GPUs × 21 days). Energy is calculated as GPU-hours × the rated power Meta reports (400 W for the A100, 700 W for the H100), so it leaves out cooling and other overhead that Meta did not report separately.</p>
  </div>
</section>

<section class="light">
  <div class="inner">
    <div class="band-head">
      <h2>What the bill looks like</h2>
      <p>Independent estimates put the compute for one frontier training run in the tens to hundreds of millions of dollars, and the chips are where most of that goes.</p>
    </div>
    <div class="costgrid">
      <div class="cardbox">
        <h3>Compute cost of the final training run</h3>
        <p class="csub">Estimated at cloud rental prices, US dollars, logarithmic scale. Each gridline is ten times the one below it.</p>
        {cost_chart()}
        <div class="rate"><b>2.4× a year</b><span>Growth in the cost of the largest training runs since 2016.</span></div>
      </div>
      <div>
        <div class="cardbox">
          <h3>Where the hardware money goes</h3>
          <p class="csub">Hardware and energy cost of a training run, average across frontier models.</p>
          {hardware_bar()}
        </div>
        <div class="cardbox">
          <h3>The whole development budget</h3>
          <p class="csub">Share of total cost for GPT-4 and Gemini Ultra class models, with staff included. Shown as ranges.</p>
          {dev_ranges()}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="shade">
  <div class="inner">
    <div class="band-head">
      <h2>Who tells you what training took</h2>
      <p>A filled square is a figure the developer published. The empty squares are the finding: three of the four labs publish almost nothing about their recent models.</p>
    </div>
    <div class="scroll">{disclosure()}</div>
    <p class="key"><span class="k"><span class="sq P"></span>Published by the developer</span><span class="k"><span class="sq E"></span>Independent estimate or my calculation only</span><span class="k"><span class="sq N"></span>Not disclosed</span><br>
    Cost is compute for the final run at cloud rental prices (AI Index). Priced as owned hardware plus energy, GPT-4 is about $40M and Gemini Ultra about $30M (Cottier et al.). The Claude figure is a 2024 remark by Anthropic's CEO about models then in service. LLaMA 65B energy covers the whole five-month project. Llama emissions are location-based.</p>
  </div>
</section>

<section class="dark">
  <div class="inner">
    <div class="band-head">
      <h2>Three things to take away</h2>
      <p>For anyone planning, funding or evaluating an AI project.</p>
    </div>
    <div class="takes">
      <div class="take"><b>1</b><h3>Pretraining is the expensive step</h3><p>Six of the seven steps matter for quality, but one of them consumes nearly all of the compute, energy and time.</p></div>
      <div class="take"><b>2</b><h3>The four resources scale together</h3><p>More data needs more compute, which draws more energy for more time. In Meta's line, data grew 11 times while GPU-hours grew 30 times.</p></div>
      <div class="take"><b>3</b><h3>Few can afford the frontier</h3><p>With costs multiplying 2.4 times a year, training from scratch belongs to a handful of labs. Most teams build on a model someone else trained.</p></div>
    </div>
  </div>
</section>

<footer class="foot light">
  <div class="inner">
    <div>
      <p><strong>Sources</strong></p>
      <ol>{"".join(f"<li>{s}</li>" for s in SOURCES)}</ol>
    </div>
    <div class="credit">
      <p>Chittaranjan Rath</p>
      <p>AIML-501 Model Development</p>
      <p>Indiana Wesleyan University, November 2026</p>
    </div>
  </div>
</footer>
{hero_script()}
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HTML, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), f"{len(HTML):,} bytes")
