"""Small SVG diagrams, one per algorithm, that show the idea behind each method.

Every diagram uses the same 240 x 140 canvas and the same four colors:
ink for structure, blue for the first class or the accent, orange for the second class,
grey for neutral points. Diagrams are returned as inline SVG strings.
"""

INK = "#1d1d1f"
BLUE = "#0071e3"
ORANGE = "#ff9f0a"
GREY = "#86868b"
LIGHT = "#d2d2d7"
PALE = "#e8e8ed"
W, H = 240, 140


def svg(body, label):
    return (f'<svg class="mini" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')


def dot(x, y, color, r=4.2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def ring(x, y, color, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="2.5"/>'


def line(x1, y1, x2, y2, color=INK, w=2.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def path(d, color=INK, w=2.5, fill="none", dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{da}/>'


def rect(x, y, w, h, color=INK, fill="none", r=4, sw=2.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{color}" stroke-width="{sw}"/>'


def arrow(x1, y1, x2, y2, color=INK, w=2.5):
    """Straight arrow with a small open head."""
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hl = 8
    ax1 = x2 - hl * math.cos(ang - 0.5)
    ay1 = y2 - hl * math.sin(ang - 0.5)
    ax2 = x2 - hl * math.cos(ang + 0.5)
    ay2 = y2 - hl * math.sin(ang + 0.5)
    return (line(x1, y1, x2, y2, color, w) +
            path(f"M{ax1:.1f},{ay1:.1f} L{x2},{y2} L{ax2:.1f},{ay2:.1f}", color, w))


def axes():
    return line(28, 118, 220, 118, LIGHT, 2) + line(28, 118, 28, 18, LIGHT, 2)


def mini_tree(x, y, scale=1.0, leaf_a=BLUE, leaf_b=ORANGE):
    """A root with two children and four leaves, centred at (x, y) top."""
    s = scale
    out = ""
    out += line(x, y, x - 26 * s, y + 24 * s, INK, 2) + line(x, y, x + 26 * s, y + 24 * s, INK, 2)
    out += line(x - 26 * s, y + 24 * s, x - 38 * s, y + 46 * s, INK, 2) + line(x - 26 * s, y + 24 * s, x - 12 * s, y + 46 * s, INK, 2)
    out += line(x + 26 * s, y + 24 * s, x + 12 * s, y + 46 * s, INK, 2) + line(x + 26 * s, y + 24 * s, x + 38 * s, y + 46 * s, INK, 2)
    out += rect(x - 9 * s, y - 8 * s, 18 * s, 14 * s, INK, "#fff", 3, 2)
    out += rect(x - 35 * s, y + 17 * s, 18 * s, 14 * s, INK, "#fff", 3, 2) + rect(x + 17 * s, y + 17 * s, 18 * s, 14 * s, INK, "#fff", 3, 2)
    out += dot(x - 38 * s, y + 50 * s, leaf_a, 4.5 * s) + dot(x - 12 * s, y + 50 * s, leaf_b, 4.5 * s)
    out += dot(x + 12 * s, y + 50 * s, leaf_a, 4.5 * s) + dot(x + 38 * s, y + 50 * s, leaf_b, 4.5 * s)
    return out


# ---------- the sixteen ----------

def linreg():
    pts = [(40, 104), (58, 92), (74, 98), (92, 78), (108, 84), (126, 64), (142, 70), (160, 50), (178, 58), (196, 38)]
    body = axes() + line(32, 110, 210, 34, BLUE, 3)
    body += "".join(dot(x, y, INK, 3.8) for x, y in pts)
    return svg(body, "A straight line fitted through scattered points")


def logreg():
    body = axes() + line(28, 68, 220, 68, LIGHT, 2, "4 4")
    body += path("M34,112 C100,112 110,24 214,24", BLUE, 3)
    body += "".join(dot(x, 116, BLUE, 3.8) for x in (44, 60, 76, 92))
    body += "".join(dot(x, 20, ORANGE, 3.8) for x in (152, 168, 184, 200))
    return svg(body, "An S-shaped curve separating two classes")


def bayes():
    body = axes()
    body += path("M34,116 C70,116 80,30 110,30 C140,30 150,116 186,116", BLUE, 3)
    body += path("M86,116 C122,116 132,48 162,48 C192,48 202,116 230,116", ORANGE, 3)
    body += line(146, 118, 146, 24, INK, 2, "4 4") + dot(146, 118, INK, 4.5)
    return svg(body, "Two probability curves; the taller one at the point wins")


def tree():
    return svg(mini_tree(120, 22, 1.25), "A decision tree with four leaves")


def forest():
    body = ""
    for x in (44, 120, 196):
        body += mini_tree(x, 18, 0.72)
    body += line(44, 60, 44, 96, LIGHT, 2) + line(120, 60, 120, 96, LIGHT, 2) + line(196, 60, 196, 96, LIGHT, 2)
    body += line(44, 96, 196, 96, LIGHT, 2) + arrow(120, 96, 120, 116, INK)
    body += dot(120, 124, BLUE, 7)
    return svg(body, "Three trees voting on one answer")


def boost():
    body = ""
    for i, x in enumerate((44, 120, 196)):
        body += mini_tree(x, 16, 0.62)
        err_w = 46 - i * 16
        body += rect(x - 23, 100, 46, 10, LIGHT, PALE, 2, 1.5)
        body += rect(x - 23, 100, err_w, 10, ORANGE, ORANGE, 2, 1.5)
    body += arrow(74, 60, 92, 60, INK) + arrow(150, 60, 168, 60, INK)
    return svg(body, "Trees added in sequence while the error bar shrinks")


def svm():
    a = [(46, 100), (60, 118), (72, 96), (54, 80), (86, 112), (40, 62)]
    b = [(150, 40), (170, 56), (186, 30), (200, 64), (168, 20), (206, 44)]
    body = "".join(dot(x, y, BLUE) for x, y in a) + "".join(dot(x, y, ORANGE) for x, y in b)
    body += line(60, 24, 210, 124, INK, 3)
    body += line(88, 12, 230, 108, GREY, 2, "5 5") + line(34, 40, 182, 136, GREY, 2, "5 5")
    body += ring(86, 112, INK) + ring(150, 40, INK)
    return svg(body, "A boundary with the widest margin between two classes")


def knn():
    a = [(40, 40), (60, 70), (52, 108), (90, 48), (108, 92), (128, 60)]
    b = [(150, 110), (176, 44), (196, 80), (210, 112), (168, 86), (140, 128)]
    body = "".join(dot(x, y, BLUE) for x, y in a) + "".join(dot(x, y, ORANGE) for x, y in b)
    body += f'<circle cx="146" cy="84" r="38" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="5 5"/>'
    body += ring(146, 84, INK, 6.5)
    return svg(body, "A new point surrounded by its closest neighbors")


def kmeans():
    clusters = [
        (BLUE, (58, 52), [(40, 40), (70, 36), (52, 68), (76, 60), (46, 54)]),
        (ORANGE, (178, 46), [(162, 32), (194, 38), (170, 62), (196, 60), (184, 50)]),
        (GREY, (118, 104), [(100, 92), (134, 96), (108, 120), (130, 118), (118, 106)]),
    ]
    body = ""
    for color, (cx, cy), pts in clusters:
        body += "".join(line(x, y, cx, cy, color, 1.2) for x, y in pts)
        body += "".join(dot(x, y, color) for x, y in pts)
        body += line(cx - 6, cy - 6, cx + 6, cy + 6, INK, 3) + line(cx - 6, cy + 6, cx + 6, cy - 6, INK, 3)
    return svg(body, "Three clusters, each gathered around a center mark")


def pca():
    pts = [(48, 108), (64, 96), (78, 104), (92, 84), (104, 92), (120, 70), (134, 80), (150, 60), (164, 68), (182, 46), (196, 56), (72, 82), (150, 84)]
    body = "".join(dot(x, y, GREY, 3.8) for x, y in pts)
    body += arrow(44, 116, 206, 36, BLUE, 3)
    body += arrow(124, 78, 100, 54, ORANGE, 2.5)
    return svg(body, "A point cloud with its main direction of variation")


def hier():
    body = ""
    leaves = [36, 68, 100, 132, 164, 196, 228]
    body += "".join(dot(x, 120, INK, 3.8) for x in leaves)
    body += path("M36,120 V100 H68 V120", INK, 2.2)      # leaves 1+2
    body += path("M100,120 V94 H132 V120", INK, 2.2)     # leaves 3+4
    body += path("M164,120 V98 H196 V120", INK, 2.2)     # leaves 5+6
    body += path("M52,100 V76 H116 V94", INK, 2.2)       # (1+2) with (3+4)
    body += path("M180,98 V80 H228 V120", INK, 2.2)      # (5+6) with leaf 7
    body += path("M84,76 V46 H204 V80", INK, 2.2)        # everything
    body += line(24, 62, 236, 62, ORANGE, 2.2, "5 5")    # the cut line
    return svg(body, "A dendrogram with a dashed cut line")


def dbscan():
    a = [(50, 50), (62, 40), (74, 56), (56, 66), (70, 70), (84, 44), (44, 38)]
    b = [(166, 86), (180, 76), (192, 92), (172, 102), (188, 108), (202, 80), (160, 98)]
    noise = [(126, 24), (210, 32), (118, 112), (38, 112)]
    body = f'<circle cx="64" cy="54" r="30" fill="{BLUE}" fill-opacity="0.12"/>'
    body += f'<circle cx="182" cy="92" r="30" fill="{ORANGE}" fill-opacity="0.14"/>'
    body += "".join(dot(x, y, BLUE) for x, y in a) + "".join(dot(x, y, ORANGE) for x, y in b)
    for x, y in noise:
        body += line(x - 4, y - 4, x + 4, y + 4, GREY, 2.2) + line(x - 4, y + 4, x + 4, y - 4, GREY, 2.2)
    return svg(body, "Two dense clusters and scattered noise points")


def cnn():
    body = ""
    for r in range(6):
        for c in range(6):
            body += rect(22 + c * 15, 26 + r * 15, 13, 13, LIGHT, PALE, 2, 1)
    body += rect(37, 41, 43, 43, BLUE, "none", 3, 3)
    body += arrow(118, 70, 142, 70, INK)
    for r in range(4):
        for c in range(4):
            body += rect(150 + c * 15, 41 + r * 15, 13, 13, BLUE, BLUE, 2, 1) if (r + c) % 3 == 0 else rect(150 + c * 15, 41 + r * 15, 13, 13, LIGHT, PALE, 2, 1)
    return svg(body, "A filter sliding over an image grid to produce a feature map")


def transformer():
    xs = [34, 72, 110, 148, 186]
    body = "".join(rect(x - 14, 96, 28, 22, INK, "#fff", 5, 2) for x in xs)
    arcs = [(0, 4, 3), (1, 4, 2), (2, 4, 3.2), (3, 4, 1.6), (0, 2, 1.4), (1, 3, 1.2)]
    for i, j, w in arcs:
        x1, x2 = xs[i], xs[j]
        h = 96 - (x2 - x1) * 0.45
        body += path(f"M{x1},96 Q{(x1 + x2) / 2},{h} {x2},96", BLUE, w)
    body += arrow(206, 107, 222, 107, INK) + rect(224 - 1, 96, 14, 22, ORANGE, ORANGE, 5, 2)
    return svg(body, "Tokens connected by attention arcs predicting the next token")


def gan():
    body = ""
    body += "".join(dot(x, y, GREY, 2.5) for x, y in [(24, 60), (30, 72), (22, 84), (34, 92), (28, 50)])
    body += arrow(40, 72, 56, 72, INK)
    body += rect(58, 52, 46, 40, BLUE, BLUE, 8, 2)
    body += arrow(106, 72, 130, 72, INK)
    body += rect(132, 58, 28, 28, INK, "#fff", 4, 2) + path("M136,80 L146,68 L152,76 L156,70 L160,80", INK, 2)
    body += arrow(162, 72, 186, 72, INK)
    body += rect(188, 52, 46, 40, ORANGE, ORANGE, 8, 2)
    body += path("M211,94 V118 H81 V94", INK, 2.2, dash="5 4") + path("M76,100 L81,94 L86,100", INK, 2.2)
    return svg(body, "A generator and a discriminator in a feedback loop")


def diffusion():
    body = ""
    import random
    rnd = random.Random(7)
    boxes = [(22, 1.0), (76, 0.6), (130, 0.25), (184, 0.0)]
    for x, noise in boxes:
        body += rect(x, 44, 44, 44, LIGHT, "#fff", 6, 1.5)
        # the clean image: a sun over a hill
        if noise < 0.9:
            op = 1 - noise
            body += f'<circle cx="{x + 30}" cy="{44 + 14}" r="6" fill="{ORANGE}" fill-opacity="{op:.2f}"/>'
            body += f'<path d="M{x + 2},{44 + 42} Q{x + 18},{44 + 16} {x + 42},{44 + 42} Z" fill="{BLUE}" fill-opacity="{op:.2f}"/>'
        n = int(70 * noise)
        for _ in range(n):
            px = x + 3 + rnd.random() * 38
            py = 47 + rnd.random() * 38
            body += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.6" fill="{INK}" fill-opacity="0.55"/>'
    body += arrow(66, 100, 76, 100, INK) + arrow(120, 100, 130, 100, INK) + arrow(174, 100, 184, 100, INK)
    body += line(22, 100, 66, 100, INK, 2.5) + line(76, 100, 120, 100, INK, 2.5) + line(130, 100, 174, 100, INK, 2.5)
    return svg(body, "Noise removed step by step until an image appears")


# ---------- extras used only in the connection chains ----------

def nn():
    cols = [(52, [40, 70, 100]), (120, [28, 52, 76, 100, 124]), (188, [52, 100])]
    body = ""
    for i in range(len(cols) - 1):
        x1, ys1 = cols[i]
        x2, ys2 = cols[i + 1]
        for y1 in ys1:
            for y2 in ys2:
                body += line(x1, y1, x2, y2, LIGHT, 1.2)
    for x, ys in cols:
        body += "".join(dot(x, y, BLUE if x != 188 else ORANGE, 6) for y in ys)
    return svg(body, "Layers of connected units")


def rnn():
    body = "".join(rect(x - 12, 100, 24, 20, INK, "#fff", 4, 2) for x in (34, 66, 98))
    body += arrow(112, 110, 128, 110, INK)
    body += rect(130, 48, 50, 44, BLUE, BLUE, 8, 2)
    body += path("M180,60 C210,40 210,100 180,80", INK, 2.5) + path("M184,74 L180,80 L187,82", INK, 2.5)
    return svg(body, "A unit that feeds its output back to itself")


def deep():
    body = ""
    for i, y in enumerate((96, 72, 48, 24)):
        body += rect(60 + i * 6, y, 120, 20, INK, "#fff" if i % 2 else PALE, 5, 2)
    return svg(body, "A stack of network layers")


def heads():
    body = rect(26, 48, 56, 44, BLUE, BLUE, 8, 2) + rect(92, 48, 56, 44, ORANGE, ORANGE, 8, 2) + rect(158, 48, 56, 44, INK, INK, 8, 2)
    return svg(body, "Three model families built on the same architecture")


DIAGRAMS = {
    "linreg": linreg, "logreg": logreg, "bayes": bayes, "tree": tree, "forest": forest,
    "boost": boost, "svm": svm, "knn": knn, "kmeans": kmeans, "pca": pca, "hier": hier,
    "dbscan": dbscan, "cnn": cnn, "transformer": transformer, "gan": gan, "diffusion": diffusion,
    "nn": nn, "rnn": rnn, "deep": deep, "heads": heads,
}


# ---------- domain icons (16 x 16) ----------

ICONS = {
    "tabular": '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 3h12v10H2z M2 7h12 M2 11h12 M6 3v10 M10 3v10" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    "vision": '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M1.5 8s2.5-4.5 6.5-4.5S14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8z" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="8" r="2.2" fill="currentColor"/></svg>',
    "language": '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3h11a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H7l-3.5 3v-3h-1a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    "generative": '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5l1.6 4.4L14 7.5l-4.4 1.6L8 13.5 6.4 9.1 2 7.5l4.4-1.6z" fill="currentColor"/></svg>',
}
