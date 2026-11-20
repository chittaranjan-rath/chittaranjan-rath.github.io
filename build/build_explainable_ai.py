"""Build the explainable AI infographic (infographic/explainable-ai/index.html).

Every figure on the page lives in this file with its source, so a correction
here regenerates the tiles, the diagrams and the charts together.

    python3 build/build_explainable_ai.py
    node build/export_explainable_ai.js      # PNG, PDF, preview and thumbnail
"""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "infographic" / "explainable-ai" / "index.html"

# ---------------------------------------------------------------- palette
# One color per way of building trust. Same four hues as the LLM training infographic,
# which were validated for color-vision deficiency on the light and the dark surface.
ASK, PROBE, INSIDE, CHECK = "#d97706", "#0a84c9", "#8a3fc7", "#1b7f3b"
LENS_COLOR = {"ask": ASK, "probe": PROBE, "inside": INSIDE, "check": CHECK}
LENS_SHORT = {"ask": "ask", "probe": "outside", "inside": "inside"}
LENS_NAME = {"ask": "Ask the model", "probe": "Test from outside", "inside": "Look inside", "check": "Validate and measure"}

# ---------------------------------------------------------------- icons (24 x 24, stroke)
ICON = {
    "ask": '<path d="M4 5.5h16v10.5H11l-4.5 3.500V16H4z"/><path d="M8 9.500h8M8 12.500h5"/>',
    "probe": '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    "inside": '<circle cx="10.500" cy="10.500" r="6"/><path d="m15 15 5.500 5.500"/><circle cx="10.500" cy="10.500" r="1.500"/>',
    "check": '<path d="M12 3 4.500 6v5.500c0 4.500 3 8 7.500 9.500 4.500-1.500 7.500-5 7.500-9.500V6z"/><path d="m8.500 12 2.500 2.500 4.500-5"/>',
    "finance": '<path d="M3.500 9.500 12 4l8.500 5.500z"/><path d="M5.500 10v7M9.800 10v7M14.200 10v7M18.500 10v7M3.500 20h17M4.500 17.500h15"/>',
    "health": '<path d="M12 20.500s-7.500-4.500-7.500-10A4.200 4.200 0 0 1 12 8a4.200 4.200 0 0 1 7.500 2.500c0 5.500-7.500 10-7.500 10z"/><path d="M7.500 12.500h2.500l1.200-2.500 1.800 4.500 1.200-2h2.300"/>',
    "law": '<path d="M12 4v16M7.500 20h9M5 7h14"/><path d="M5 7 2.500 13a2.700 2.700 0 0 0 5 0zM19 7l-2.500 6a2.700 2.700 0 0 0 5 0z"/>',
    "accuracy": '<circle cx="12" cy="12" r="8.500"/><circle cx="12" cy="12" r="4.500"/><circle cx="12" cy="12" r="1"/>',
    "calibration": '<path d="M4 16.500a8 8 0 0 1 16 0"/><path d="m12 16.500 4-5.500"/><path d="M4 19.500h16"/>',
    "robustness": '<path d="M12 3 4.500 6v5.500c0 4.500 3 8 7.500 9.500 4.500-1.500 7.500-5 7.500-9.500V6z"/>',
    "fairness": '<path d="M5 9h14M5 15h14"/>',
    "bias": '<path d="M12 5v14M5 9.500 19 7"/><path d="M5 9.500 3.500 13.500h3zM19 7l-1.500 4h3z"/>',
    "toxicity": '<path d="M12 4 3 19.500h18z"/><path d="M12 10v4.500M12 17v.300"/>',
    "efficiency": '<path d="M13.500 2.500 5 13.500h6l-1 8 8.500-11h-6z"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.700" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def chip(kind, label=None):
    return f'<span class="chip {kind}">{icon(kind)}{label or LENS_NAME[kind]}</span>'


def wrap(text, width):
    """Greedy word wrap for SVG labels."""
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- content
# Opening tiles: one number per way of building trust.
HERO = [
    ("inside", "The black box", "175 billion", "weights in GPT-3",
     "An answer comes from all of them at once (Brown et al., 2020)"),
    ("ask", "The explanation", "25 in 100", "times the written reasoning admitted the hint it used",
     "Claude 3.7 Sonnet in a 2025 faithfulness test (Chen et al., 2025)"),
    ("probe", "The hidden influence", "Up to 36%", "accuracy lost when prompts were quietly biased",
     "The explanations left the bias out (Turpin et al., 2023)"),
    ("check", "The safety net", "7 metrics", "in one full evaluation of a language model",
     "Accuracy is one of the seven (Liang et al., 2023)"),
]

# Faithfulness test: how often the chain of thought mentioned a hint that changed the answer (Chen et al., 2025).
FAITHFUL = [("Claude 3.7 Sonnet", "Anthropic", 25), ("DeepSeek R1", "DeepSeek", 39)]

# NIST AI RMF 1.0, section 3.5: three related ideas and the question each one answers.
DEFINITIONS = [
    ("Transparency", "What happened?", "Being open about the system: what data it used, how it was built and tested, and what it produced."),
    ("Explainability", "How was the decision made?", "A description of the mechanism inside the system that produced the output."),
    ("Interpretability", "Why, and what does it mean for me?", "The meaning of the output in the setting where a person has to act on it."),
]

SECTORS = [
    ("finance", "Finance", "A lender must give the specific reasons for a credit denial, even when an algorithm made the call.", "CFPB Circular 2023-03"),
    ("health", "Healthcare", "A clinician must be able to interpret the output of a high-risk system before acting on it.", "EU AI Act, Article 13"),
    ("law", "Law and public decisions", "A person affected by a high-risk AI decision can ask for an explanation of the role the system played.", "EU AI Act, Article 86"),
]

OBSTACLES = [
    ("scale", "Too many parts", "GPT-3 has 175 billion weights and Llama 3.1 has 405 billion. No single weight holds a fact. Each answer is the combined effect of all of them.",
     "Brown et al. (2020); Meta (2024)"),
    ("tangle", "Concepts are tangled together", "One neuron often responds to several unrelated things. GPT-4 tried to explain all 307,200 neurons in GPT-2, and just over 1,000 got a high-scoring explanation.",
     "Bills et al. (2023)"),
    ("posthoc", "Explanations come after the fact", "A model writes its reasoning as more text, and can leave out what drove the answer. Quietly biased prompts cut accuracy by up to 36%, and the explanations left the bias out.",
     "Turpin et al. (2023)"),
    ("data", "The data carries its own flaws", "Models absorb the bias and noise in the text they learn from. Full evaluations therefore score fairness, bias and toxicity separately from accuracy.",
     "Liang et al. (2023)"),
]

# Regulation timeline. (months since Jan 2023, side, date label, text). EU dates follow the 2026 Digital Omnibus amendments.
RULES = [
    (8, "below", "Sep 2023", "US: CFPB says lenders using AI still owe specific reasons for a denial"),
    (19, "above", "Aug 2024", "EU AI Act enters into force"),
    (25, "below", "Feb 2025", "EU: prohibited practices banned"),
    (39, "below", "Apr 2026", "US bank model-risk guidance (SR 26-2) leaves generative AI out of scope"),
    (43, "above", "Aug 2026", "EU: transparency duties apply (Article 50)"),
    (59, "above", "Dec 2027", "EU: high-risk rules apply, including Article 13 (moved from Aug 2026)"),
]

LENSES = [
    ("ask", "Ask the model", "Chain-of-thought · reasoning summaries",
     "Anyone can do it, in plain words", "Admitted a hint 25% of the time"),
    ("probe", "Test from outside", "Input perturbation · attribution scores",
     "Shows which inputs carried the decision", "Stops short of how the model used them"),
    ("inside", "Look inside", "Attention maps · probing · features · circuits",
     "Shows steps on the way, such as Texas before Austin", "Covers part of the model; attention maps can mislead"),
]

# Industry efforts. (company, months since Jan 2023, lens, side, date label, text, hollow)
LANES = ["Anthropic", "OpenAI", "Google", "Meta"]
EFFORTS = [
    ("Anthropic", 16, "inside", "above", "May 2024", "Millions of features mapped in Claude 3 Sonnet", False),
    ("Anthropic", 26, "inside", "below", "Mar 2025", "Attribution graphs trace steps in Claude 3.5 Haiku", False),
    ("Anthropic", 30, "ask", "above", "Apr 2025", "Reasoning admits a hint 25% of the time", False),
    ("Anthropic", 40, "inside", "above", "May 2026", "Internal activity turned into readable text", False),
    ("OpenAI", 4, "inside", "above", "May 2023", "GPT-4 explains all 307,200 GPT-2 neurons", False),
    ("OpenAI", 17, "inside", "below", "Jun 2024", "16 million features found in GPT-4", False),
    ("OpenAI", 35, "ask", "above", "Dec 2025", "13 tests of how well reasoning can be monitored", False),
    ("Google", 18, "inside", "above", "Jul 2024", "Gemma Scope: 400+ open autoencoders", False),
    ("Google", 28, "ask", "below", "May 2025", "Thought summaries in the Gemini API", False),
    ("Meta", 11, "probe", "above", "Dec 2023", "Captum 0.7 explains generative models", False),
    ("Meta", 29, "inside", "below", "May 2025", "Open Llama weights traced by outside tools", True),
]

# Three dates from the rules that ask for explanations. EU dates follow the 2026 amendments.
RULE_DATES = [
    ("Sep 2023", "United States", "Lenders using AI still owe an applicant the specific reasons for a denial."),
    ("Aug 2026", "European Union", "Transparency duties under Article 50 of the AI Act start to apply."),
    ("Dec 2027", "European Union", "High-risk rules, Article 13 included, apply. They were moved back 16 months."),
]

# Report card: INVENTED scores for an example model, to show the shape a full evaluation gives. Not data.
REPORT = [0.90, 0.42, 0.70, 0.60, 0.66, 0.86, 0.50]

# Validation, as US bank regulators describe it (SR 26-2, April 2026).
VALIDATION = [
    ("1", "Is the design sound?", "Conceptual soundness", "Review the assumptions, the data and the testing behind the model."),
    ("2", "Do outputs match reality?", "Outcomes analysis", "Compare what the model said with what happened. Back-test it."),
    ("3", "Is it still working?", "Ongoing monitoring", "Keep checking as data, users and conditions change."),
]

# HELM's seven metrics (Liang et al., 2023), each as the plain question it answers.
METRICS = [
    ("accuracy", "Accuracy", "Is the answer right?"),
    ("calibration", "Calibration", "Does its confidence match how often it is right?"),
    ("robustness", "Robustness", "Does it hold up when the input changes a little?"),
    ("fairness", "Fairness", "Does it work equally well for different groups?"),
    ("bias", "Bias", "Does its output lean on stereotypes?"),
    ("toxicity", "Toxicity", "Does it produce harmful language?"),
    ("efficiency", "Efficiency", "How much time and compute does it need?"),
]
COVERAGE = [("Before HELM", 17.9), ("After HELM", 96.0)]  # share of core scenarios each model had been tested on

# Foundation Model Transparency Index, score out of 100. (name, 2024, 2025, note)
FMTI = [
    ("Anthropic", 51, 46, "calc"),
    ("Google", 47, 41, "calc"),
    ("OpenAI", 49, 35, ""),
    ("Meta", 60, 31, ""),
    ("All developers", 58, 41, "mean"),
]

SOURCES = [
    "NIST (2023), <em>AI Risk Management Framework 1.0</em>: definitions of transparency, explainability, interpretability and validation.",
    "Brown et al. (2020); Meta (2024), Llama 3.1 model card: model sizes.",
    "Anthropic (2025), <em>Tracing the thoughts of a large language model</em>: the 36 + 59 and Dallas examples, limits of the method.",
    "Chen et al. (2025), <em>Reasoning models don't always say what they think</em>; Turpin et al. (2023): faithfulness of written reasoning. Jain and Wallace (2019): attention maps as explanations.",
    "Lab work: Bills et al. (2023) and OpenAI (2024, 2025); Anthropic (2024, 2025, 2026); Lieberum et al. (2024) and Basu Mallick et al. (2025), Google; Miglani et al. (2023), Meta.",
    "Liang et al. (2023), <em>Holistic evaluation of language models</em>: seven metrics and coverage. Wan et al. (2025), <em>The 2025 Foundation Model Transparency Index</em>.",
    "Regulation (EU) 2024/1689 (AI Act), with 2026 dates from Goodwin Procter (2026); CFPB Circular 2023-03; Federal Reserve, FDIC and OCC (2026), SR 26-2.",
]


# ---------------------------------------------------------------- pieces
def did_svg():
    """What the interpretability tools saw for 36 + 59: two parallel paths that meet at the answer."""
    W, H = 560, 250
    box = lambda x, y, w, h, fill, stroke: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}"/>'
    s = [f'<svg class="did" viewBox="0 0 {W} {H}" role="img" aria-labelledby="did-t did-d">',
         '<title id="did-t">What the model did to add 36 and 59</title>',
         '<desc id="did-d">The sum splits into two parallel paths. One estimates the rough size of the answer. The other works out that the last digit is 5. The two paths combine to give 95.</desc>',
         '<defs><marker id="dh" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#c79bf2"/></marker></defs>']
    s.append(box(8, 95, 96, 60, "#2c2c2e", "#48484a"))
    s.append('<text x="56" y="131" text-anchor="middle" class="dn">36 + 59</text>')
    for y, title, sub in [(22, "Path 1: rough size", "About how big is the sum?"), (158, "Path 2: last digit", "6 + 9 ends in 5")]:
        s.append(box(160, y, 232, 70, "rgba(138,63,199,.22)", INSIDE))
        s.append(f'<text x="176" y="{y + 29}" class="dt">{title}</text>')
        s.append(f'<text x="176" y="{y + 51}" class="ds">{sub}</text>')
    s.append(box(448, 95, 104, 60, "#f5f5f7", "#f5f5f7"))
    s.append('<text x="500" y="134" text-anchor="middle" class="da">95</text>')
    for d in ["M104 112C130 112 130 57 156 57", "M104 138C130 138 130 193 156 193",
              "M392 57C420 57 420 112 444 112", "M392 193C420 193 420 138 444 138"]:
        s.append(f'<path d="{d}" fill="none" stroke="#c79bf2" stroke-width="2" marker-end="url(#dh)"/>')
    s.append('<text x="276" y="129" text-anchor="middle" class="dc">both run at the same time</text>')
    s.append('</svg>')
    return "".join(s)


def waffle(name, who, pct):
    cells = "".join(f'<rect x="{(i % 10) * 17}" y="{(i // 10) * 17}" width="14" height="14" rx="3" class="{"on" if i < pct else "off"}"/>' for i in range(100))
    return f"""<div class="waf">
  <svg viewBox="0 0 167 167" role="img" aria-label="{name}: mentioned the hint in {pct} of 100 cases">{cells}</svg>
  <div><p class="wafn">{pct}%</p><p class="wafm">{name}</p><p class="wafw">{who}</p></div>
</div>"""


def obstacle_svg(kind):
    W, H = 240, 110
    s = [f'<svg class="obs" viewBox="0 0 {W} {H}" aria-hidden="true">']
    if kind == "scale":
        rng = random.Random(7)
        hot = {rng.randrange(26 * 10) for _ in range(22)}
        for i in range(26 * 10):
            x, y = 8 + (i % 26) * 8.800, 10 + (i // 26) * 10
            s.append(f'<circle cx="{x:.1f}" cy="{y}" r="{2.600 if i in hot else 1.800}" fill="{INSIDE if i in hot else "#c7c7cc"}"/>')
    elif kind == "tangle":
        labels = ["a recipe", "a legal clause", "a line of code", "a city name"]
        s.append(f'<circle cx="34" cy="55" r="15" fill="{INSIDE}"/><text x="34" y="59" text-anchor="middle" class="ow">1</text>')
        for i, lab in enumerate(labels):
            y = 14 + i * 27
            s.append(f'<path d="M49 55C80 55 80 {y} 108 {y}" fill="none" stroke="#a1a1a6" stroke-width="1.500"/>')
            s.append(f'<rect x="110" y="{y - 10}" width="122" height="20" rx="10" fill="#fff" stroke="#d2d2d7"/>')
            s.append(f'<text x="171" y="{y + 4}" text-anchor="middle" class="ol">{lab}</text>')
    elif kind == "posthoc":
        s.append('<defs><marker id="oh" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="#6e6e73"/></marker></defs>')
        s.append('<rect x="4" y="8" width="96" height="30" rx="8" fill="#fff" stroke="#d2d2d7"/><text x="52" y="27" text-anchor="middle" class="ol">what drove it</text>')
        s.append(f'<rect x="4" y="72" width="96" height="30" rx="8" fill="#fff" stroke="{ASK}" stroke-dasharray="4 3"/><text x="52" y="91" text-anchor="middle" class="ol">stated reason</text>')
        s.append('<rect x="160" y="40" width="74" height="30" rx="8" fill="#1d1d1f"/><text x="197" y="59" text-anchor="middle" class="ow">answer</text>')
        s.append('<path d="M100 23C130 23 130 50 156 52" fill="none" stroke="#6e6e73" stroke-width="1.800" marker-end="url(#oh)"/>')
        s.append(f'<path d="M156 60C130 62 130 87 104 87" fill="none" stroke="{ASK}" stroke-width="1.800" stroke-dasharray="4 3"/>')
        s.append('<text x="130" y="104" text-anchor="middle" class="on">written afterwards</text>')
    else:  # data
        mix = [(46, "#48484a"), (22, "#8e8e93"), (9, "#c7c7cc"), (4, "#e5e5ea")]
        for x0, lab in [(6, "training text"), (160, "model output")]:
            y = 12
            for h, c in mix:
                s.append(f'<rect x="{x0}" y="{y}" width="74" height="{h - 2}" rx="3" fill="{c}"/>')
                y += h
            s.append(f'<text x="{x0 + 37}" y="106" text-anchor="middle" class="on">{lab}</text>')
        s.append('<path d="M88 52h62" stroke="#6e6e73" stroke-width="1.800"/><path d="m144 46 8 6-8 6" fill="none" stroke="#6e6e73" stroke-width="1.800"/>')
        s.append('<text x="119" y="44" text-anchor="middle" class="on">same skew</text>')
    s.append('</svg>')
    return "".join(s)


def obstacles():
    out = []
    for i, (kind, title, text, src) in enumerate(OBSTACLES, 1):
        out.append(f"""<li class="obstacle">
  {obstacle_svg(kind)}
  <h3><span class="num">{i}</span>{title}</h3>
  <p>{text}</p>
  <p class="src">{src}</p>
</li>""")
    return "\n".join(out)


def box_glyph(stage, dark=False):
    """The running motif: a cover slides off the box, stage 0 (closed) to 6 (open), showing the network inside."""
    t = stage / 6
    ink = "#f5f5f7" if dark else "#1d1d1f"
    node = "#c79bf2" if dark else INSIDE
    cid = f"bx{stage}{'d' if dark else 'l'}"
    pts = [(x, y) for y in (17, 32, 47) for x in (17, 32, 47)]
    edges = [(0, 4), (4, 2), (3, 4), (4, 8), (6, 4), (1, 5), (5, 8), (3, 7)]
    g = [f'<svg class="boxg" viewBox="0 0 64 64" role="img" aria-label="The box, step {stage + 1} of 7: {"closed" if stage == 0 else "open" if stage == 6 else "opening"}">',
         f'<defs><clipPath id="{cid}"><rect x="4" y="4" width="56" height="56" rx="13"/></clipPath></defs><g clip-path="url(#{cid})">']
    for i, j in edges:
        g.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" stroke="{node}" stroke-width="1.500" opacity=".65"/>')
    for x, y in pts:
        g.append(f'<circle cx="{x}" cy="{y}" r="3.400" fill="{node}"/>')
    g.append(f'<rect x="{4 + 56 * t:.1f}" y="4" width="{56 * (1 - t):.1f}" height="56" fill="{ink}"/></g>'
             f'<rect x="4" y="4" width="56" height="56" rx="13" fill="none" stroke="{ink}" stroke-width="2.500"/></svg>')
    return "".join(g)


def head(stage, title, text, dark=False):
    return f'<div class="band-head withbox">{box_glyph(stage, dark)}<div><h2>{title}</h2><p>{text}</p></div></div>'


def defs_svg():
    """One picture for the three NIST terms: where each one points on the path from question to person."""
    W, H = 1160, 318
    rng = random.Random(3)
    s = [f'<svg class="defmap" viewBox="0 0 {W} {H}" role="img" aria-labelledby="dm-t dm-d">',
         '<title id="dm-t">Transparency, explainability and interpretability</title>',
         '<desc id="dm-d">A question goes into a model and an answer comes out to a person. Explainability points inside the model and asks how the decision was made. '
         'Interpretability points at the answer reaching the person and asks why, and what it means for them. Transparency spans the whole path and asks what happened.</desc>',
         '<defs><marker id="mh" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#86868b"/></marker></defs>']
    s.append('<rect x="20" y="126" width="180" height="60" rx="14" fill="#fff" stroke="#d2d2d7"/><text x="110" y="161" text-anchor="middle" class="dml">A question goes in</text>')
    s.append('<rect x="310" y="96" width="300" height="120" rx="20" fill="#1d1d1f"/>')
    for c in range(9):
        for r in range(3):
            s.append(f'<circle cx="{350 + c * 27.500:.1f}" cy="{128 + r * 22}" r="3.500" fill="#f5f5f7" opacity="{rng.choice([.18, .3, .5])}"/>')
    s.append('<text x="460" y="204" text-anchor="middle" class="dmk" style="fill:#a1a1a6">THE MODEL</text>')
    s.append('<rect x="720" y="126" width="180" height="60" rx="14" fill="#fff" stroke="#d2d2d7"/><text x="810" y="161" text-anchor="middle" class="dml">An answer comes out</text>')
    s.append('<circle cx="1040" cy="140" r="17" fill="none" stroke="#1d1d1f" stroke-width="2.500"/><path d="M1008 190c4-20 16-28 32-28s28 8 32 28" fill="none" stroke="#1d1d1f" stroke-width="2.500" stroke-linecap="round"/>')
    s.append('<text x="1040" y="212" text-anchor="middle" class="dms">the person who acts on it</text>')
    for d in ["M200 156H302", "M610 156H712", "M900 156H996"]:
        s.append(f'<path d="{d}" stroke="#86868b" stroke-width="2" marker-end="url(#mh)"/>')
    for x, term, q, desc, y_to in [(460, "EXPLAINABILITY", "How was the decision made?", "The mechanism inside the system", 96),
                                   (930, "INTERPRETABILITY", "Why, and what does it mean for me?", "The meaning of the output for the person using it", 148)]:
        s.append(f'<text x="{x}" y="18" text-anchor="middle" class="dmk">{term}</text><text x="{x}" y="46" text-anchor="middle" class="dmq">{q}</text>'
                 f'<text x="{x}" y="67" text-anchor="middle" class="dms">{desc}</text><line x1="{x}" y1="76" x2="{x}" y2="{y_to}" stroke="#1d1d1f" stroke-width="1.500"/>'
                 f'<circle cx="{x}" cy="{y_to}" r="4" fill="#1d1d1f"/>')
    s.append('<path d="M20 232V244H900V232" fill="none" stroke="#1d1d1f" stroke-width="1.500"/>')
    s.append('<text x="460" y="266" text-anchor="middle" class="dmk">TRANSPARENCY</text><text x="460" y="293" text-anchor="middle" class="dmq">What happened?</text>'
             '<text x="460" y="313" text-anchor="middle" class="dms">What data was used, how the system was built and tested, and what it produced</text>')
    s.append('</svg>')
    return "".join(s)


def rule_cards():
    return "".join(f'<div class="rule"><b>{d}</b><span class="where">{w}</span><span>{t}</span></div>' for d, w, t in RULE_DATES)


def lens_svg():
    """One question passing through a model, with the three places to look and what each is good and bad at."""
    W, H = 1160, 500
    rng = random.Random(11)
    info = {k: (n, tech, good, limit) for k, n, tech, good, limit in LENSES}
    my = 250  # vertical middle of the model

    def label(key, x, y, anchor="start"):
        n, tech, good, limit = info[key]
        c = LENS_COLOR[key]
        return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="ll" style="fill:{c}">{n}</text>'
                f'<text x="{x}" y="{y + 20}" text-anchor="{anchor}" class="lt2" style="fill:{c}">{tech}</text>'
                f'<text x="{x}" y="{y + 42}" text-anchor="{anchor}" class="ls2"><tspan class="lb">Strength</tspan> {good}</text>'
                f'<text x="{x}" y="{y + 61}" text-anchor="{anchor}" class="ls2"><tspan class="lb">Limit</tspan> {limit}</text>')

    s = [f'<svg class="lensmap" viewBox="0 0 {W} {H}" role="img" aria-labelledby="lm-t lm-d">',
         '<title id="lm-t">Three places to look for an explanation</title>',
         '<desc id="lm-d">A prompt asks for the capital of the state containing Dallas. It passes through the layers of the model and comes out as the answer Austin. '
         'Looking inside finds the concepts Dallas, Texas and capital along the way. Testing from outside swaps a word in the prompt and watches the answer change. '
         'Asking the model produces a written explanation next to the answer. Each way of looking is listed with its techniques, its strength and its limit.</desc>',
         '<defs><marker id="lh" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#86868b"/></marker>'
         f'<marker id="lp" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="{PROBE}"/></marker></defs>']
    s.append(f'<g><rect x="10" y="{my - 42}" width="230" height="84" rx="14" fill="#fff" stroke="#d2d2d7"/>'
             f'<text x="26" y="{my - 18}" class="lk">PROMPT</text>'
             f'<text x="26" y="{my + 5}" class="lq">The capital of the state</text><text x="26" y="{my + 24}" class="lq">containing Dallas is …</text></g>')
    s.append(f'<g><rect x="940" y="{my - 42}" width="210" height="84" rx="14" fill="#1d1d1f"/>'
             f'<text x="956" y="{my - 18}" class="lk" style="fill:#a1a1a6">ANSWER</text><text x="956" y="{my + 18}" class="la">Austin</text></g>')
    s.append(f'<path d="M240 {my}H292" stroke="#86868b" stroke-width="2" marker-end="url(#lh)"/><path d="M880 {my}H932" stroke="#86868b" stroke-width="2" marker-end="url(#lh)"/>')
    s.append(f'<rect x="300" y="{my - 76}" width="580" height="152" rx="18" fill="#fff" stroke="#d2d2d7"/>')
    s.append(f'<text x="590" y="{my + 68}" text-anchor="middle" class="lk">THE MODEL: LAYERS OF UNITS</text>')
    feats = {(1, 2): "Dallas", (4, 1): "Texas", (7, 3): "capital", (10, 2): "Austin"}
    pos = {}
    for c in range(12):
        for rrow in range(5):
            x, y = 330 + c * 47.300, my - 56 + rrow * 23
            pos[(c, rrow)] = (x, y)
            if (c, rrow) not in feats:
                s.append(f'<circle cx="{x:.1f}" cy="{y}" r="4" fill="#d2d2d7" opacity="{rng.choice([.45, .7, 1])}"/>')
    order = list(feats)
    g = ['<g class="lens lens-inside">']
    track = [f"M300 {my}"]
    for i, key in enumerate(order):
        x1, y1 = pos[key]
        x0, y0 = (300, my) if i == 0 else pos[order[i - 1]]
        seg = f"C{(x0 + x1) / 2:.1f} {y0} {(x0 + x1) / 2:.1f} {y1} {x1:.1f} {y1}"
        track.append(seg)
        if i:
            g.append(f'<path d="M{x0:.1f} {y0}{seg}" fill="none" stroke="{INSIDE}" stroke-width="2.500"/>')
    xl, yl = pos[order[-1]]
    track.append(f"C{(xl + 880) / 2:.1f} {yl} {(xl + 880) / 2:.1f} {my} 880 {my}")
    # motion on the web version only: a pulse runs the path the answer took
    g.append(f'<circle class="pulse" r="7" fill="#fff" stroke="{INSIDE}" stroke-width="3"><animateMotion dur="3.600s" repeatCount="indefinite" path="{" ".join(track)}"/></circle>')
    for key, name in feats.items():
        x, y = pos[key]
        w = 12 + 7.600 * len(name)
        g.append(f'<rect x="{x - w / 2:.1f}" y="{y - 11}" width="{w:.1f}" height="22" rx="11" fill="{INSIDE}"/>'
                 f'<text x="{x:.1f}" y="{y + 4.500}" text-anchor="middle" class="lf">{name}</text>')
    g.append(f'<path d="M300 {my - 84}V{my - 92}H830V{my - 84}" fill="none" stroke="{INSIDE}" stroke-width="2"/>')
    g.append(label("inside", 565, 52, "middle"))
    g.append('</g>')
    s.append("".join(g))
    s.append(f'<g class="lens lens-probe"><path d="M125 {my + 46}C125 {my + 150} 1045 {my + 150} 1045 {my + 48}" fill="none" stroke="{PROBE}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#lp)"/>'
             f'<rect x="380" y="{my + 96}" width="420" height="140" rx="14" fill="#fff" stroke="{PROBE}"/>'
             + label("probe", 590, my + 122, "middle") +
             f'<text x="590" y="{my + 222}" text-anchor="middle" class="lex">Swap Dallas for Oakland. Does it say Sacramento?</text></g>')
    s.append(f'<g class="lens lens-ask"><path d="M1045 {my - 42}V{my - 84}" stroke="{ASK}" stroke-width="2"/>'
             f'<rect x="852" y="20" width="302" height="{my - 104}" rx="14" fill="#fff" stroke="{ASK}"/>'
             + label("ask", 868, 44) +
             f'<text x="868" y="134" class="lex">“Dallas is in Texas, and the capital of</text><text x="868" y="151" class="lex">Texas is Austin.”</text></g>')
    s.append('</svg>')
    return "".join(s)


def radar_svg():
    """Report card for an example model. The scores are invented to show the shape; the seven axes are HELM's."""
    import math
    W, H, cx, cy, R = 660, 440, 330, 222, 128
    n = len(METRICS)
    ang = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    pt = lambda i, v: (cx + R * v * math.cos(ang[i]), cy + R * v * math.sin(ang[i]))
    poly = lambda v: " ".join(f"{pt(i, v[i] if isinstance(v, list) else v)[0]:.1f},{pt(i, v[i] if isinstance(v, list) else v)[1]:.1f}" for i in range(n))
    s = [f'<svg class="radar" viewBox="0 0 {W} {H}" role="img" aria-label="Illustrative report card on seven metrics: ' +
         "; ".join(f"{name}, {q}" for _, name, q in METRICS) + '. The example model scores high on accuracy and low on calibration.">']
    for ring in (.25, .5, .75, 1):
        s.append(f'<polygon points="{poly(ring)}" fill="{"#fff" if ring == 1 else "none"}" stroke="#d2d2d7"/>')
    s.append(f'<polygon points="{poly(.25)}" fill="none" stroke="#d2d2d7"/><polygon points="{poly(.5)}" fill="none" stroke="#d2d2d7"/><polygon points="{poly(.75)}" fill="none" stroke="#d2d2d7"/>')
    for i in range(n):
        x, y = pt(i, 1)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d2d2d7"/>')
    s.append(f'<polygon points="{poly(REPORT)}" fill="{CHECK}" fill-opacity=".22" stroke="{CHECK}" stroke-width="2.500" stroke-linejoin="round"/>')
    for i, (key, name, q) in enumerate(METRICS):
        x, y = pt(i, REPORT[i])
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.500" fill="{CHECK}" stroke="#fff" stroke-width="1.500"/>')
        lx, ly = pt(i, 1.120)
        c = math.cos(ang[i])
        anchor = "start" if c > .3 else "end" if c < -.3 else "middle"
        lines = wrap(q, 23)
        if anchor == "middle":
            ly -= 15 * len(lines) + 6
        elif math.sin(ang[i]) > .5:
            ly += 8
        s.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="{anchor}" class="rn">{name}</text>')
        for j, line in enumerate(lines):
            s.append(f'<text x="{lx:.1f}" y="{ly + 20 + 15 * j:.1f}" text-anchor="{anchor}" class="rq">{line}</text>')
    s.append('</svg>')
    return "".join(s)


def lens_switch():
    btns = '<button type="button" data-lens="all" aria-pressed="true">All three</button>' + "".join(
        f'<button type="button" data-lens="{k}" aria-pressed="false">{n}</button>' for k, n, *_ in LENSES)
    return f'<div class="switch" role="group" aria-label="Highlight one way of looking">{btns}</div>'


def lanes_svg():
    W, lane_h, top, gut = 1160, 138, 6, 118
    H = top + lane_h * len(LANES) + 26
    X = lambda m: gut + 26 + (W - gut - 60) * m / 47
    s = [f'<svg class="lanes" viewBox="0 0 {W} {H}" role="img" aria-label="Explainability work by company, 2023 to 2026: ' +
         "; ".join(f"{c}, {d}, {t}" for c, _, _, _, d, t, _ in EFFORTS) + '">']
    for year in range(2023, 2028):
        x = X((year - 2023) * 12)
        if year < 2027:
            s.append(f'<text x="{x + 6:.1f}" y="{H - 6}" class="ry">{year}</text>')
        s.append(f'<line x1="{x:.1f}" y1="4" x2="{x:.1f}" y2="{H - 2}" stroke="#e5e5ea"/>')
    for i, company in enumerate(LANES):
        y = top + i * lane_h + lane_h / 2
        s.append(f'<line x1="{gut}" y1="{y}" x2="{W - 14}" y2="{y}" stroke="#c7c7cc" stroke-width="2"/>')
        s.append(f'<text x="0" y="{y + 6}" class="lc">{company}</text>')
        if i:
            s.append(f'<line x1="0" y1="{top + i * lane_h}" x2="{W}" y2="{top + i * lane_h}" stroke="#d2d2d7"/>')
    for company, m, lens, side, date, text, hollow in EFFORTS:
        y = top + LANES.index(company) * lane_h + lane_h / 2
        x, color = X(m), LENS_COLOR[lens]
        lines = wrap(text, 30)
        up = side == "above"
        y0 = y - 22 - 15 * len(lines) if up else y + 30
        s.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y - 14 if up else y + 14}" stroke="{color}" stroke-width="1.500"/>')
        if hollow:
            s.append(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="#fff" stroke="{color}" stroke-width="3"><title>{date}: {text}</title></circle>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{y}" r="8" fill="{color}" stroke="#fff" stroke-width="2"><title>{date}: {text}</title></circle>')
        s.append(f'<text x="{x:.1f}" y="{y0:.1f}" text-anchor="middle" class="rd" style="fill:{color}">{date} · {LENS_SHORT[lens]}</text>')
        for j, line in enumerate(lines):
            s.append(f'<text x="{x:.1f}" y="{y0 + 16 + 15 * j:.1f}" text-anchor="middle" class="rt">{line}</text>')
    s.append('</svg>')
    return "".join(s)


def validation_svg():
    W, H = 580, 352
    spots = [(170, 10), (334, 218), (6, 218)]
    s = [f'<svg class="vloop" viewBox="0 0 {W} {H}" role="img" aria-labelledby="vl-t vl-d">',
         '<title id="vl-t">The validation cycle</title>',
         '<desc id="vl-d">Three checks in a repeating cycle: conceptual soundness, outcomes analysis, and ongoing monitoring.</desc>',
         f'<defs><marker id="vh" viewBox="0 0 10 10" refX="8.500" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="{CHECK}"/></marker></defs>']
    for d in ["M414 66C492 88 500 160 470 212", "M328 280H252", "M96 212C70 160 86 88 164 66"]:
        s.append(f'<path d="{d}" fill="none" stroke="{CHECK}" stroke-width="2.500" marker-end="url(#vh)"/>')
    for (x, y), (n, q, name, text) in zip(spots, VALIDATION):
        s.append(f'<rect x="{x}" y="{y}" width="240" height="124" rx="16" fill="#fff" stroke="#d2d2d7"/>'
                 f'<rect x="{x}" y="{y + 16}" width="5" height="92" rx="2.500" fill="{CHECK}"/>'
                 f'<circle cx="{x + 32}" cy="{y + 30}" r="13" fill="#1d1d1f"/><text x="{x + 32}" y="{y + 35}" text-anchor="middle" class="vn">{n}</text>'
                 f'<text x="{x + 54}" y="{y + 35}" class="vq">{q}</text>'
                 f'<text x="{x + 20}" y="{y + 60}" class="vk">{name}</text>')
        for j, line in enumerate(wrap(text, 35)):
            s.append(f'<text x="{x + 20}" y="{y + 79 + 15 * j}" class="vt">{line}</text>')
    s.append('<text x="290" y="166" text-anchor="middle" class="vc">repeat for as long</text><text x="290" y="183" text-anchor="middle" class="vc">as the model is in use</text>')
    s.append('</svg>')
    return "".join(s)


def fmti_svg():
    W, H, l, base, top = 680, 280, 40, 214, 24
    gw = (W - l - 10) / len(FMTI)
    Y = lambda v: base - (base - top) * v / 70
    s = [f'<svg class="fmti" viewBox="0 0 {W} {H}" role="img" aria-label="Foundation Model Transparency Index scores out of 100, 2024 then 2025: ' +
         ", ".join(f"{n} {a} then {b}" for n, a, b, _ in FMTI) + '">']
    for v in range(0, 71, 10):
        s.append(f'<line x1="{l}" y1="{Y(v):.1f}" x2="{W}" y2="{Y(v):.1f}" stroke="{"#86868b" if v == 0 else "#e5e5ea"}"/>')
        s.append(f'<text x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end" class="ax">{v}</text>')
    for i, (name, a, b, note) in enumerate(FMTI):
        x = l + i * gw + gw / 2
        if note == "mean":
            s.append(f'<line x1="{x - gw / 2 + 4:.1f}" y1="{top - 14}" x2="{x - gw / 2 + 4:.1f}" y2="{H - 8}" stroke="#d2d2d7" stroke-dasharray="3 4"/>')
        for dx, v, fill, yr in [(-37, a, "#c7c7cc", 2024), (3, b, "#1d1d1f", 2025)]:
            y = Y(v)
            s.append(f'<path d="M{x + dx:.1f} {base}V{y + 4:.1f}q0-4 4-4h26q4 0 4 4V{base}z" fill="{fill}"><title>{name}, {yr}: {v} of 100</title></path>')
            s.append(f'<text x="{x + dx + 17:.1f}" y="{y - 7:.1f}" text-anchor="middle" class="bv">{v}</text>')
        s.append(f'<text x="{x:.1f}" y="{base + 20}" text-anchor="middle" class="bl">{name}</text>')
        s.append(f'<text x="{x:.1f}" y="{base + 40}" text-anchor="middle" class="bd">{b - a:+d} points</text>'.replace("-", "−"))
    s.append('</svg>')
    return "".join(s)


def script():
    return r"""<script>(function(){
var btns=document.querySelectorAll('.switch button'),band=document.querySelector('.lensband');
function show(k){band.setAttribute('data-show',k);
  btns.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.lens===k?'true':'false');});}
btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.lens);});});
// the "said" panel appears first, then the "did" panel, so the gap lands as a reveal
var parts=document.querySelectorAll('.reveal');
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  document.body.classList.add('anim');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.35});
  parts.forEach(function(el){io.observe(el);});}
})();</script>"""


CSS = """
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Regular.woff2") format("woff2"); font-weight: 400; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Medium.woff2") format("woff2"); font-weight: 500; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-SemiBold.woff2") format("woff2"); font-weight: 600; font-display: swap; }
  @font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Bold.woff2") format("woff2"); font-weight: 700; font-display: swap; }
  :root {
    --text: #1d1d1f; --text2: #6e6e73; --text3: #86868b; --white: #fff; --grey: #f5f5f7; --grey2: #e8e8ed; --rule: #d2d2d7;
    --blue: #0071e3; --link: #0066cc;
    --ask: #d97706; --ask-ink: #b45309; --ask-bg: rgba(217,119,6,.13); --ask-lite: #f5b55a;
    --probe: #0a84c9; --probe-ink: #0066a8; --probe-bg: rgba(10,132,201,.11); --probe-lite: #6cc0f5;
    --inside: #8a3fc7; --inside-ink: #7a32b5; --inside-bg: rgba(138,63,199,.11); --inside-lite: #c79bf2;
    --check: #1b7f3b; --check-ink: #1b7f3b; --check-bg: rgba(27,127,59,.12); --check-lite: #6fd08c;
  }
  *, *::before, *::after { box-sizing: border-box; }
  html { font-size: 17px; -webkit-font-smoothing: antialiased; }
  body { margin: 0; background: var(--white); color: var(--text); line-height: 1.47;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif; }
  a { color: var(--link); text-decoration: none; }
  a:hover { text-decoration: underline; }
  svg text { font-family: inherit; }
  .inner { max-width: 1240px; margin: 0 auto; padding: 0 40px; }
  .light { background: var(--white); }
  .shade { background: var(--grey); }
  .dark { background: #000; color: #f5f5f7; }
  .scroll { position: relative; }

  .topbar { font-size: 14px; padding: 14px 0 0; margin: 0; }
  .topwrap a { color: #2997ff; }
  body.poster .topwrap { display: none; }

  .hero { padding: 76px 0 44px; text-align: center; }
  .eyebrow { font-size: 14px; font-weight: 600; color: #a1a1a6; letter-spacing: .02em; margin: 0 0 12px; }
  h1 { font-size: 64px; line-height: 1.05; font-weight: 600; letter-spacing: -0.025em; margin: 0 0 16px; text-wrap: balance; }
  .hero .sub { font-size: 23px; line-height: 1.33; color: #a1a1a6; max-width: 36em; margin: 0 auto 30px; text-wrap: balance; }
  .tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: left; }
  .tile { background: #1d1d1f; border-radius: 18px; padding: 22px 22px 20px; border-top: 5px solid var(--c); display: flex; flex-direction: column; }
  .tile.ask { --c: var(--ask); --ink: var(--ask-lite); } .tile.probe { --c: var(--probe); --ink: var(--probe-lite); }
  .tile.inside { --c: var(--inside); --ink: var(--inside-lite); } .tile.check { --c: var(--check); --ink: var(--check-lite); }
  .tile-top { display: flex; align-items: center; gap: 8px; color: var(--ink); font-weight: 600; font-size: 15px; }
  .tile-ico { width: 24px; height: 24px; }
  .big { font-size: 38px; line-height: 1.05; font-weight: 600; letter-spacing: -0.02em; margin: 18px 0 4px; white-space: nowrap; }
  .unit { font-size: 16px; line-height: 1.3; font-weight: 500; color: #d2d2d7; margin: 0 0 14px; }
  .human { font-size: 13px; line-height: 1.4; font-weight: 500; color: var(--ink); margin: auto 0 0; padding-top: 12px; border-top: 1px solid #38383a; }
  .tiles-foot { font-size: 13px; color: #86868b; margin: 18px auto 0; max-width: 70em; }

  .chip { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 600; line-height: 1; padding: 6px 11px 6px 8px; border-radius: 980px; margin: 0 6px 6px 0; vertical-align: middle; white-space: nowrap; }
  .chip .ico { width: 14px; height: 14px; }
  .chip.ask { color: var(--ask-ink); background: var(--ask-bg); } .chip.probe { color: var(--probe-ink); background: var(--probe-bg); }
  .chip.inside { color: var(--inside-ink); background: var(--inside-bg); } .chip.check { color: var(--check-ink); background: var(--check-bg); }

  section { padding: 42px 0; }
  .band-head { max-width: 820px; margin: 0 0 28px; }
  h2 { font-size: 40px; line-height: 1.1; font-weight: 600; letter-spacing: -0.015em; margin: 0 0 10px; }
  .band-head p { font-size: 19px; line-height: 1.42; color: var(--text2); margin: 0; }
  .dark .band-head p { color: #a1a1a6; }
  .num { display: inline-grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--text); color: #fff; font-size: 13px; font-weight: 600; flex: none; }
  .note { font-size: 13px; color: var(--text2); margin: 16px 0 0; max-width: 72em; }
  .dark .note { color: #86868b; }

  /* said and did */
  .gap { padding-top: 36px; }
  .saydo { display: grid; grid-template-columns: minmax(0, 1fr) 64px minmax(0, 1.150fr); align-items: stretch; }
  .panel { background: #1d1d1f; border-radius: 18px; padding: 22px 24px; }
  .panel h3 { font-size: 13px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; margin: 0 0 16px; }
  .panel.said h3 { color: var(--ask-lite); } .panel.didp h3 { color: var(--inside-lite); }
  .panel.said { border-top: 5px solid var(--ask); } .panel.didp { border-top: 5px solid var(--inside); }
  .bubble { font-size: 16px; line-height: 1.4; border-radius: 16px; padding: 10px 14px; margin: 0 0 10px; max-width: 88%; }
  .bubble.q { background: #38383a; margin-left: auto; border-bottom-right-radius: 4px; }
  .bubble.a { background: rgba(217,119,6,.22); border: 1px solid var(--ask); border-bottom-left-radius: 4px; }
  .bubble.a.plain { background: #2c2c2e; border-color: #48484a; }
  .neq { display: grid; place-items: center; }
  .neq span { display: grid; place-items: center; width: 48px; height: 48px; border-radius: 50%; background: #f5f5f7; color: #000; font-size: 26px; font-weight: 600; }
  .did { width: 100%; height: auto; display: block; }
  .did .dn { font-size: 17px; font-weight: 600; fill: #f5f5f7; } .did .dt { font-size: 15px; font-weight: 600; fill: #f5f5f7; }
  .did .ds { font-size: 13px; fill: #d2d2d7; } .did .da { font-size: 30px; font-weight: 600; fill: #000; }
  .did .dc { font-size: 12px; fill: #a1a1a6; }
  .saycap { font-size: 15px; line-height: 1.45; color: #d2d2d7; margin: 20px 0 0; max-width: 62em; }
  .wafs { display: grid; grid-template-columns: minmax(0, 1.100fr) repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 32px; padding-top: 28px; border-top: 1px solid #38383a; align-items: center; }
  .wafs .lead h3 { font-size: 24px; line-height: 1.15; font-weight: 600; letter-spacing: -0.015em; margin: 0 0 8px; }
  .wafs .lead p { font-size: 15px; line-height: 1.45; color: #a1a1a6; margin: 0; }
  .waf { display: flex; align-items: center; gap: 18px; background: #1d1d1f; border-radius: 18px; padding: 18px 20px; }
  .waf svg { width: 150px; height: 150px; flex: none; }
  .waf .on { fill: var(--ask); } .waf .off { fill: #38383a; }
  .wafn { font-size: 44px; font-weight: 600; letter-spacing: -0.02em; line-height: 1; margin: 0 0 6px; }
  .wafm { font-size: 16px; font-weight: 600; margin: 0; } .wafw { font-size: 13px; color: #a1a1a6; margin: 0; }

  /* definitions and sectors */
  .defs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .def { background: var(--grey); border-radius: 18px; padding: 22px 24px; }
  .def .term { font-size: 13px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--text2); margin: 0 0 8px; }
  .def h3 { font-size: 26px; line-height: 1.15; font-weight: 600; letter-spacing: -0.015em; margin: 0 0 10px; }
  .def p { font-size: 15px; line-height: 1.45; color: var(--text2); margin: 0; }
  .def.mid { background: var(--text); color: #f5f5f7; } .def.mid .term, .def.mid p { color: #a1a1a6; }
  .subhead { font-size: 22px; font-weight: 600; letter-spacing: -0.01em; margin: 30px 0 14px; }
  .sectors { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .sector { display: grid; grid-template-columns: 44px 1fr; gap: 14px; border-top: 2px solid var(--text); padding-top: 16px; }
  .sector-ico { width: 40px; height: 40px; }
  .sector h3 { font-size: 19px; font-weight: 600; margin: 0 0 4px; }
  .sector p { font-size: 15px; line-height: 1.45; margin: 0 0 6px; }
  .src { font-size: 12px; color: var(--text3); margin: 0; }

  /* obstacles */
  .obstacles { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
  .obstacle { background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 18px; padding: 18px 20px 16px; display: flex; flex-direction: column; }
  .obs { width: 100%; height: auto; display: block; background: var(--grey); border-radius: 12px; margin-bottom: 14px; }
  .obs .ol { font-size: 11px; fill: var(--text); } .obs .ow { font-size: 12px; font-weight: 600; fill: #fff; } .obs .on { font-size: 10.500px; fill: var(--text2); }
  .obstacle h3 { display: flex; align-items: center; gap: 9px; font-size: 18px; line-height: 1.2; font-weight: 600; letter-spacing: -0.01em; margin: 0 0 8px; }
  .obstacle p { font-size: 14px; line-height: 1.45; margin: 0 0 10px; }
  .obstacle .src { margin-top: auto; }
  .rulebox { background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 18px; padding: 20px 24px 12px; margin-top: 20px; }
  .rulebox h3 { display: flex; align-items: center; gap: 9px; font-size: 18px; font-weight: 600; margin: 0 0 4px; }
  .rulebox .csub { font-size: 14px; color: var(--text2); margin: 0 0 6px; max-width: 70em; }
  .rules, .lanes, .lensmap, .cover, .fmti, .vloop { width: 100%; height: auto; display: block; }
  .ry { font-size: 12px; font-weight: 600; fill: var(--text3); }
  .rd { font-size: 12px; font-weight: 600; fill: var(--text); }
  .rt { font-size: 13px; fill: var(--text); }

  /* lenses */
  .switch { display: inline-flex; gap: 4px; padding: 4px; border-radius: 980px; background: var(--grey2); margin: 0 0 20px; }
  .switch button { font: inherit; font-size: 14px; font-weight: 500; color: var(--text2); background: none; border: 0; padding: 8px 18px; border-radius: 980px; cursor: pointer; }
  .switch button:hover { color: var(--text); }
  .switch button[aria-pressed="true"] { background: var(--text); color: #fff; }
  .switch button:focus-visible { outline: 3px solid var(--blue); outline-offset: 2px; }
  body.poster .switch { display: none; }
  .lensmap { background: var(--grey); border-radius: 18px; }
  .lensmap .lk { font-size: 11px; font-weight: 600; letter-spacing: .06em; fill: var(--text3); }
  .lensmap .lq { font-size: 15px; font-weight: 500; fill: var(--text); } .lensmap .la { font-size: 28px; font-weight: 600; fill: #fff; }
  .lensmap .lf { font-size: 12px; font-weight: 600; fill: #fff; } .lensmap .ll { font-size: 15px; font-weight: 600; }
  .lensmap .ls2 { font-size: 13px; fill: var(--text); }
  .lens, .lenscard { transition: opacity .2s; }
  .lensband[data-show="ask"] .lens:not(.lens-ask), .lensband[data-show="probe"] .lens:not(.lens-probe), .lensband[data-show="inside"] .lens:not(.lens-inside),
  .lensband[data-hover="ask"] .lens:not(.lens-ask), .lensband[data-hover="probe"] .lens:not(.lens-probe), .lensband[data-hover="inside"] .lens:not(.lens-inside) { opacity: .12; }
  .lensband[data-show="ask"] .lenscard:not(.ask), .lensband[data-show="probe"] .lenscard:not(.probe), .lensband[data-show="inside"] .lenscard:not(.inside) { opacity: .35; }
  .lenscards { list-style: none; margin: 20px 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .lenscard { border-radius: 18px; padding: 20px 22px 16px; border-top: 5px solid var(--c); background: var(--grey); }
  .lenscard.ask { --c: var(--ask); --ink: var(--ask-ink); } .lenscard.probe { --c: var(--probe); --ink: var(--probe-ink); } .lenscard.inside { --c: var(--inside); --ink: var(--inside-ink); }
  .lenscard h3 { display: flex; align-items: center; gap: 8px; font-size: 20px; font-weight: 600; letter-spacing: -0.01em; color: var(--ink); margin: 0 0 8px; }
  .lens-ico { width: 24px; height: 24px; }
  .lenscard p { font-size: 15px; line-height: 1.45; margin: 0 0 10px; }
  .lenscard .tech { font-size: 13px; font-weight: 600; color: var(--ink); margin: -2px 0 10px; }
  .lenscard .pro, .lenscard .con { font-size: 14px; padding-top: 10px; border-top: 1px solid var(--rule); }
  .lenscard b { display: block; font-size: 11px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--text2); margin-bottom: 2px; }
  .lanebox { margin-top: 30px; }
  .lanebox .legend { margin: 0 0 8px; }
  .lanes .lc { font-size: 17px; font-weight: 600; fill: var(--text); letter-spacing: -0.01em; }

  /* validation and metrics */
  .valgrid { display: grid; grid-template-columns: minmax(0, 1.050fr) minmax(0, 1fr); gap: 40px; align-items: center; }
  .vloop .vn { font-size: 13px; font-weight: 600; fill: #fff; } .vloop .vq { font-size: 14px; font-weight: 600; fill: var(--text); }
  .vloop .vk { font-size: 11px; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; fill: var(--check); }
  .vloop .vt { font-size: 12.500px; fill: var(--text2); } .vloop .vc { font-size: 12px; font-weight: 600; fill: var(--text3); letter-spacing: .04em; text-transform: uppercase; }
  .valside p { font-size: 16px; line-height: 1.5; margin: 0 0 14px; }
  .callout { background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 18px; padding: 18px 20px; border-left: 5px solid var(--check); }
  .callout b { display: block; font-size: 11px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--check); margin-bottom: 4px; }
  .callout span { font-size: 15px; line-height: 1.45; }
  .callout + .callout { margin-top: 12px; border-left-color: var(--text3); } .callout + .callout b { color: var(--text2); }
  .metrics { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(7, 1fr); gap: 14px; }
  .metric { background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 14px; padding: 14px 13px 14px; text-align: left; position: relative; }
  .metric .num { position: absolute; top: 14px; right: 13px; background: var(--grey2); color: var(--text2); width: 22px; height: 22px; font-size: 12px; }
  .metric-ico { width: 30px; height: 30px; color: var(--check); display: block; margin-bottom: 8px; }
  .metric h3 { font-size: 16px; font-weight: 600; letter-spacing: -0.01em; margin: 0 0 4px; }
  .metric p { font-size: 13px; line-height: 1.4; color: var(--text2); margin: 0; }
  .coverbox { margin-top: 28px; }
  .coverbox h3 { font-size: 19px; font-weight: 600; margin: 0 0 4px; } .coverbox .csub { font-size: 14px; color: var(--text2); margin: 0 0 12px; max-width: 70em; }
  .cover .cl { font-size: 14px; font-weight: 600; fill: var(--text); } .cover .cv { font-size: 20px; font-weight: 600; fill: var(--text); letter-spacing: -0.01em; }

  /* transparency index */
  .fmtigrid { display: grid; grid-template-columns: minmax(0, 1.300fr) minmax(0, 1fr); gap: 40px; align-items: center; }
  .cardbox { background: var(--grey); border-radius: 18px; padding: 22px 24px 16px; }
  .cardbox h3 { font-size: 19px; font-weight: 600; letter-spacing: -0.01em; margin: 0 0 4px; }
  .cardbox .csub { font-size: 13px; color: var(--text2); margin: 0 0 10px; }
  .key2 { font-size: 13px; color: var(--text2); margin: 0 0 6px; } .key2 i { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin: 0 6px 0 0; vertical-align: -1px; } .key2 span { margin-right: 16px; white-space: nowrap; }
  .ax { font-size: 12px; fill: var(--text3); }
  .fmti .bv { font-size: 15px; font-weight: 600; fill: var(--text); } .fmti .bl { font-size: 13px; font-weight: 600; fill: var(--text); } .fmti .bd { font-size: 12px; fill: var(--text2); }
  .facts2 { display: grid; gap: 12px; }
  .fact2 { display: flex; align-items: baseline; gap: 14px; padding-bottom: 12px; border-bottom: 1px solid var(--rule); }
  .fact2 b { font-size: 34px; font-weight: 600; letter-spacing: -0.02em; line-height: 1; white-space: nowrap; min-width: 92px; }
  .fact2 span { font-size: 15px; line-height: 1.4; }

  /* takeaways */
  .takes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .take { background: #1d1d1f; border-radius: 18px; padding: 24px; }
  .take b { display: block; font-size: 44px; font-weight: 600; letter-spacing: -0.02em; line-height: 1; margin-bottom: 12px; }
  .take h3 { font-size: 19px; font-weight: 600; margin: 0 0 6px; }
  .take p { font-size: 15px; line-height: 1.45; color: #a1a1a6; margin: 0; }
  .sum { display: grid; grid-template-columns: 1fr 34px 1fr 34px 1fr 34px 1.100fr; align-items: stretch; margin: 0 0 20px; text-align: left; }
  .sum div { border-radius: 14px; padding: 14px 16px; border: 1px solid #48484a; }
  .sum div b { display: block; font-size: 17px; font-weight: 600; margin-bottom: 2px; } .sum div span { font-size: 13px; line-height: 1.4; color: #a1a1a6; display: block; }
  .sum i { display: grid; place-items: center; font-style: normal; font-size: 24px; font-weight: 600; color: #a1a1a6; }
  .sum .e { border-color: var(--inside); } .sum .e b { color: var(--inside-lite); }
  .sum .v, .sum .m { border-color: var(--check); } .sum .v b, .sum .m b { color: var(--check-lite); }
  .sum .t { background: #f5f5f7; border-color: #f5f5f7; } .sum .t b { color: #000; } .sum .t span { color: #48484a; }

  .foot { padding: 28px 0 44px; font-size: 13px; color: var(--text2); }
  .foot .inner { display: grid; grid-template-columns: minmax(0, 2.200fr) minmax(0, 1fr); gap: 32px; }
  .foot p { margin: 0 0 6px; }
  .foot ol { margin: 0; padding-left: 1.3em; }
  .foot li { margin-bottom: 3px; }
  .credit { text-align: right; }

  /* v3: box motif, hero comparison, stat strip, definition map, rule cards, lens labels, report card */
  .hero { padding: 64px 0 44px; }
  .hero .boxg { width: 56px; height: 56px; margin: 0 auto 18px; display: block; }
  .withbox { display: flex; gap: 22px; align-items: flex-start; max-width: 900px; }
  .withbox .boxg { width: 64px; height: 64px; flex: none; margin-top: 2px; }
  .herolabel { font-size: 17px; color: #a1a1a6; margin: 34px auto 18px; max-width: 46em; }
  .hero .saydo { text-align: left; grid-template-columns: minmax(0, 1fr) 72px minmax(0, 1.150fr); }
  .hero .panel { padding: 26px 28px 28px; }
  .hero .bubble { font-size: 19px; padding: 12px 18px; margin-bottom: 12px; }
  .hero .saycap { margin: 20px auto 0; text-align: center; font-size: 17px; color: #f5f5f7; }
  .hero .saycap span { color: #a1a1a6; }
  .hero .wafs { text-align: left; margin-top: 28px; padding-top: 26px; }
  .hero .note { text-align: left; }
  .strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; text-align: left; margin-top: 26px; padding-top: 24px; border-top: 1px solid #38383a; }
  .stat { display: flex; gap: 12px; align-items: flex-start; }
  .stat-ico { width: 26px; height: 26px; flex: none; margin-top: 4px; color: var(--ink); }
  .stat.inside { --ink: var(--inside-lite); } .stat.probe { --ink: var(--probe-lite); } .stat.check { --ink: var(--check-lite); }
  .stat p { font-size: 15px; line-height: 1.4; color: #d2d2d7; margin: 0; }
  .stat b { display: block; font-size: 30px; line-height: 1.1; font-weight: 600; letter-spacing: -0.02em; color: var(--ink); margin-bottom: 2px; }
  .stat span { color: #86868b; font-size: 13px; }
  .anim .reveal { opacity: 0; transform: translateY(14px); transition: opacity .6s ease, transform .6s ease; }
  .anim .reveal.d1 { transition-delay: .5s; } .anim .reveal.d2 { transition-delay: 1.100s; }
  .anim .reveal.in, body.poster .reveal { opacity: 1; transform: none; }
  body.poster .reveal { transition: none; }
  body.poster .pulse { display: none; }
  @media (prefers-reduced-motion: reduce) { .pulse { display: none; } }

  .defmap, .radar { width: 100%; height: auto; display: block; }
  .valgrid > *, .fmtigrid > *, .saydo > * { min-width: 0; }
  .defmap .dmk { font-size: 12px; font-weight: 600; letter-spacing: .08em; fill: var(--text2); }
  .defmap .dmq { font-size: 24px; font-weight: 600; letter-spacing: -0.015em; fill: var(--text); }
  .defmap .dms { font-size: 14px; fill: var(--text2); } .defmap .dml { font-size: 15px; font-weight: 500; fill: var(--text); }
  .sectors { margin-top: 34px; padding-top: 28px; border-top: 1px solid var(--rule); }
  .sector { display: block; border-top: 0; padding-top: 0; text-align: center; }
  .sector-ico { width: 60px; height: 60px; padding: 12px; border-radius: 50%; background: var(--text); color: #fff; margin: 0 auto 12px; display: block; }
  .sector h3 { font-size: 20px; } .sector p { max-width: 21em; margin: 0 auto 6px; }
  .owed { font-size: 13px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--text2); text-align: center; margin: 0 0 22px; }

  .obstacle p { font-size: 14px; }
  .rulerow { display: grid; grid-template-columns: 250px repeat(3, 1fr); gap: 20px; margin-top: 20px; align-items: stretch; }
  .rulelead { display: flex; gap: 10px; align-items: flex-start; padding-top: 4px; }
  .rulelead h3 { font-size: 18px; line-height: 1.2; font-weight: 600; margin: 0 0 6px; } .rulelead p { font-size: 13px; line-height: 1.4; color: var(--text2); margin: 0; }
  .rule { background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 18px; padding: 16px 20px; }
  .rule b { display: block; font-size: 28px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.1; }
  .rule .where { display: block; font-size: 11px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--text2); margin: 4px 0 6px; }
  .rule span { font-size: 14px; line-height: 1.4; }

  .lensmap .lt2 { font-size: 12.500px; font-weight: 600; } .lensmap .lb { font-size: 10.500px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; fill: var(--text2); }
  .lensmap .lex { font-size: 13px; font-style: italic; fill: var(--text2); } .lensmap .ll { font-size: 17px; }

  .valgrid { grid-template-columns: minmax(0, 1fr) minmax(0, 1.180fr); gap: 28px; align-items: start; }
  .radarbox { background: var(--white); box-shadow: 0 2px 14px rgba(0,0,0,.06); border-radius: 18px; padding: 18px 16px 12px; }
  .radarbox h3 { font-size: 19px; font-weight: 600; margin: 0 6px 2px; } .radarbox .csub { font-size: 13px; color: var(--text2); margin: 0 6px; }
  .radar .rn { font-size: 14px; font-weight: 600; fill: var(--text); } .radar .rq { font-size: 12px; fill: var(--text2); }
  .valnotes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 24px; }
  .valnotes .callout + .callout { margin-top: 0; }
  .valnotes .callout.k { border-left-color: var(--check); } .valnotes .callout.k b { color: var(--check); }
  .callout strong { display: block; font-size: 26px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 4px; }

  @media (max-width: 1100px) {
    body:not(.poster) .strip, body:not(.poster) .rulerow, body:not(.poster) .valnotes { grid-template-columns: 1fr; }
    body:not(.poster) .hero .saydo { grid-template-columns: 1fr; }
    body:not(.poster) .defmap { min-width: 1000px; } body:not(.poster) .radar { min-width: 560px; }
  }
  @media (max-width: 760px) { body:not(.poster) .withbox .boxg { width: 44px; height: 44px; } body:not(.poster) .withbox { gap: 14px; } body:not(.poster) .hero .bubble { font-size: 16px; } }
  @media (max-width: 1100px) {
    body:not(.poster) .tiles, body:not(.poster) .obstacles { grid-template-columns: repeat(2, 1fr); }
    body:not(.poster) .defs, body:not(.poster) .sectors, body:not(.poster) .lenscards, body:not(.poster) .takes,
    body:not(.poster) .valgrid, body:not(.poster) .fmtigrid, body:not(.poster) .wafs { grid-template-columns: 1fr; }
    body:not(.poster) .saydo { grid-template-columns: 1fr; } body:not(.poster) .neq { padding: 12px 0; }
    body:not(.poster) .metrics { grid-template-columns: repeat(2, 1fr); }
    body:not(.poster) .sum { grid-template-columns: 1fr; } body:not(.poster) .sum i { padding: 4px 0; }
    body:not(.poster) .scroll { overflow-x: auto; }
    body:not(.poster) .rules, body:not(.poster) .lanes, body:not(.poster) .lensmap { min-width: 1000px; }
  }
  @media (max-width: 760px) {
    body:not(.poster) h1 { font-size: 38px; } body:not(.poster) h2 { font-size: 30px; } body:not(.poster) .hero .sub { font-size: 19px; }
    body:not(.poster) .inner { padding: 0 20px; } body:not(.poster) section { padding: 44px 0; }
    body:not(.poster) .tiles, body:not(.poster) .obstacles { grid-template-columns: 1fr; }
    body:not(.poster) .switch { flex-wrap: wrap; border-radius: 18px; } body:not(.poster) .switch button { padding: 8px 12px; font-size: 13px; }
    body:not(.poster) .cover, body:not(.poster) .fmti { min-width: 560px; }
    body:not(.poster) .foot .inner { grid-template-columns: 1fr; } body:not(.poster) .credit { text-align: left; }
  }
  @media print { .topbar { display: none; } .obstacle, .lenscard, .cardbox, .take, .metric { break-inside: avoid; } }
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Why did the model say that? Explainable AI, validation and metrics for large language models</title>
<meta name="description" content="An infographic on explainable AI for large language models: what it is and why it matters, why it is hard, how validation and performance metrics build trust, and what Anthropic, OpenAI, Google and Meta are doing to open the black box.">
<style>{CSS}</style>
</head>
<body>
<div class="dark topwrap"><div class="inner"><p class="topbar"><a href="../../artifacts/explainable-ai.html">&larr; Back to the artifact page</a></p></div></div>

<header class="hero dark">
  <div class="inner">
    {box_glyph(0, True)}
    <p class="eyebrow">Explainable AI for large language models</p>
    <h1>Why did the model say that?</h1>
    <p class="sub">Explainability shows how an answer was produced. Validation and metrics show whether it can be relied on. Trust needs both.</p>
    <div class="sum">
      <div class="e"><b>Explainability</b><span>How the answer was made</span></div><i>+</i>
      <div class="v"><b>Validation</b><span>Evidence it does its job</span></div><i>+</i>
      <div class="m"><b>Metrics</b><span>How well, in numbers</span></div><i>=</i>
      <div class="t"><b>Trust you can defend</b><span>To a customer, an auditor or a regulator</span></div>
    </div>
    <p class="herolabel">Researchers asked a Claude model to add two numbers, asked how it got the answer, then looked inside to see what had happened.</p>
    <div class="saydo">
      <div class="panel said reveal">
        <h3>What the model said</h3>
        <p class="bubble q">What is 36 + 59?</p>
        <p class="bubble a plain">95</p>
        <p class="bubble q">How did you work that out?</p>
        <p class="bubble a">I added the ones, 6 and 9, to get 15. I carried the 1, then added the tens to get 95.</p>
      </div>
      <div class="neq reveal d2" aria-hidden="true"><span>≠</span></div>
      <div class="panel didp reveal d1">
        <h3>What the model did</h3>
        {did_svg()}
      </div>
    </div>
    <p class="saycap">The answer was right. The explanation described a method the model had not used. <span>(Claude 3.5 Haiku; Anthropic, 2025)</span></p>
    <div class="wafs">
      <div class="lead">
        <h3>How often does the written reasoning own up?</h3>
        <p>Testers slipped a hint into the prompt. Where the hint changed the answer, they counted how often the model's step-by-step reasoning mentioned it. Each square is one case in a hundred (Chen et al., 2025).</p>
      </div>
      {"".join(waffle(*f) for f in FAITHFUL)}
    </div>
    <p class="tiles-foot">Four colors keep one meaning down the page: {" · ".join(LENS_NAME[k].lower() for k in ["ask", "probe", "inside", "check"])}. The box beside each heading opens a little further as the page goes on.</p>
  </div>
</header>

<section class="light">
  <div class="inner">
    {head(1, "What explainable AI means", "Explainable AI is the work of making a model's outputs and decisions understandable to people. The US standards body NIST separates three ideas that often get mixed up.")}
    <div class="scroll">{defs_svg()}</div>
    <ul class="sectors">
      {"".join(f'<li class="sector">{icon(k, "sector-ico")}<h3>{n}</h3><p>{t}</p><p class="src">{src}</p></li>' for k, n, t, src in SECTORS)}
    </ul>
  </div>
</section>

<section class="shade">
  <div class="inner">
    {head(2, "Why it is hard", "Four obstacles come from how the models are built and trained. A fifth comes from outside: the rules are arriving before the science is finished.")}
    <ol class="obstacles">
{obstacles()}
    </ol>
    <div class="rulerow">
      <div class="rulelead"><span class="num">5</span><div><h3>Rules that ask for explanations</h3><p>Three dates from US and EU rules (CFPB, 2023; Goodwin Procter, 2026).</p></div></div>
      {rule_cards()}
    </div>
  </div>
</section>

<section class="light lensband" data-show="all">
  <div class="inner">
    {head(3, "Three ways to look, and who is building them", "Current techniques differ in where they look. Each one sees something the others miss, so labs use them together.")}
    {lens_switch()}
    <div class="scroll">{lens_svg()}</div>
    <p class="note">The example follows Anthropic (2025). Attention maps often disagree with other measures of which inputs mattered (Jain and Wallace, 2019), and feature methods take hours of expert work for one short prompt.</p>
    <div class="lanebox">
      <h3 class="subhead">What the four labs have published</h3>
      <p class="legend">{chip("ask")}{chip("probe")}{chip("inside")}</p>
      <div class="scroll">{lanes_svg()}</div>
      <p class="note">A selection of dated, public work. A hollow dot marks work another group carried out on a lab's open model.</p>
    </div>
  </div>
</section>

<section class="shade">
  <div class="inner">
    {head(4, "Validation and metrics: checking the answer either way", "An explanation says how a model reached an answer. Validation gathers evidence that the model does its job, and metrics put that evidence into numbers. They work even when the inside of the model stays closed.")}
    <div class="valgrid">
      <div>
        <h3 class="subhead" style="margin-top:0">Validation: three checks that repeat</h3>
        <div class="scroll">{validation_svg()}</div>
      </div>
      <div class="radarbox">
        <h3>Metrics: a report card with seven lines</h3>
        <p class="csub">The seven metrics of Stanford's HELM benchmark. The shape is an illustration with invented scores: this example model answers well and judges its own confidence poorly, which an accuracy score would hide.</p>
        <div class="scroll">{radar_svg()}</div>
      </div>
    </div>
    <div class="valnotes">
      <div class="callout k"><b>Validation, defined</b><span>Confirming with objective evidence that a system meets the requirements of its intended use (NIST, 2023).</span></div>
      <div class="callout k"><b>Same test for everyone</b><span><strong>17.9% → 96.0%</strong>Share of core test scenarios covered per model, before and after HELM tested 30 models the same way.</span></div>
      <div class="callout"><b>The catch</b><span>US bank regulators restated the three checks in April 2026 and left generative AI out of scope, so teams using language models carry them over themselves.</span></div>
    </div>
  </div>
</section>

<section class="light">
  <div class="inner">
    {head(5, "Transparency can be scored too", "Stanford's Foundation Model Transparency Index rates developers on 100 indicators. The four labs sit in the middle, and all four slipped in 2025.")}
    <div class="fmtigrid">
      <div class="cardbox">
        <h3>Transparency score out of 100</h3>
        <p class="key2"><span><i style="background:#c7c7cc"></i>2024</span><span><i style="background:#1d1d1f"></i>2025</span></p>
        <div class="scroll">{fmti_svg()}</div>
        <p class="csub">2024 scores for Anthropic and Google are calculated from the changes the 2025 report states. The average covers 14 developers in 2024 and 13 in 2025, and the 2025 edition tightened its indicators.</p>
      </div>
      <div class="facts2">
        <div class="fact2"><b>95</b><span>IBM's 2025 score, the highest in the index's history. High scores are possible.</span></div>
        <div class="fact2"><b>31</b><span>Meta's score. It releases open model weights and still discloses little, so open weights and transparency are separate things.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="inner">
    {head(6, "Three things to take away", "For anyone deciding whether to rely on a language model.", True)}
    <div class="takes">
      <div class="take"><b>1</b><h3>Treat an explanation as a claim</h3><p>A model's account of its reasoning is more generated text. It can be right, and it can leave out what drove the answer. Test it before relying on it.</p></div>
      <div class="take"><b>2</b><h3>Use more than one way of looking</h3><p>Asking is easy and unreliable. Testing from outside shows what mattered. Looking inside shows steps and covers part of the model. Together they say more.</p></div>
      <div class="take"><b>3</b><h3>Validate whatever the explanation says</h3><p>Evidence and metrics catch problems an explanation hides: wrong answers, overconfidence, bias, drift over time. They are how a claim about a model gets checked.</p></div>
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
{script()}
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HTML, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), f"{len(HTML):,} bytes")
