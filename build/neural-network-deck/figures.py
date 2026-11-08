"""Figures for the neural network components presentation.

Everything is drawn with matplotlib so the deck, the web viewer and the portfolio
page all share the same artwork. Colors follow the portfolio palette (apple.com
inspired): near-black text, grey secondary text, and the system accent colors.
Run:  python3 figures.py   (writes PNGs into ../figures)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neural_network import MLPClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

# ---------- palette ----------
BLUE = "#2997FF"      # layers
PURPLE = "#BF5AF2"    # neurons
GREEN = "#30D158"     # weights
ORANGE = "#FF9F0A"    # activation functions
RED = "#FF375F"       # loss functions
INDIGO = "#5E5CE6"    # optimization
TEXT = "#1D1D1F"
TEXT2 = "#6E6E73"
TEXT3 = "#86868B"
RULE = "#D2D2D7"
GREY = "#F5F5F7"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "font.family": "Inter",
    "font.size": 11,
    "axes.edgecolor": RULE,
    "axes.labelcolor": TEXT2,
    "xtick.color": TEXT2,
    "ytick.color": TEXT2,
    "text.color": TEXT,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

RNG = np.random.default_rng(7)


def save(fig, name, transparent=False):
    path = os.path.join(OUT, name)
    fig.savefig(path, transparent=transparent, facecolor="none" if transparent else WHITE)
    plt.close(fig)
    print("wrote", path)


# =====================================================================
# Network drawing helper
# =====================================================================
def layer_positions(sizes, width=10.0, height=6.0, x0=0.0, y0=0.0):
    """Return a list (per layer) of arrays of (x, y) node centers."""
    xs = np.linspace(x0 + 0.6, x0 + width - 0.6, len(sizes))
    positions = []
    for layer_index, n in enumerate(sizes):
        if n == 1:
            ys = np.array([y0 + height / 2])
        else:
            pad = (height - 0.9) * (1 - n / max(sizes)) / 2 + 0.45
            ys = np.linspace(y0 + height - pad, y0 + pad, n)
        positions.append(np.column_stack([np.full(n, xs[layer_index]), ys]))
    return positions


def draw_network(ax, sizes, node_colors, radius=0.26, edge_color=RULE, edge_width=1.0,
                 weights=None, node_labels=None, width=10.0, height=6.0, x0=0.0, y0=0.0,
                 node_face=WHITE, label_color=TEXT):
    """Draw a feed-forward network. weights: list of (n_in x n_out) matrices to style edges."""
    pos = layer_positions(sizes, width, height, x0, y0)
    # edges first so nodes sit on top
    for li in range(len(sizes) - 1):
        for i, (xa, ya) in enumerate(pos[li]):
            for j, (xb, yb) in enumerate(pos[li + 1]):
                if weights is not None:
                    w = weights[li][i, j]
                    color = BLUE if w >= 0 else ORANGE
                    lw = 0.4 + 3.2 * abs(w) / max(1e-9, np.abs(weights[li]).max())
                    alpha = 0.55 + 0.45 * abs(w) / max(1e-9, np.abs(weights[li]).max())
                else:
                    color, lw, alpha = edge_color, edge_width, 1.0
                ax.plot([xa + radius, xb - radius], [ya, yb], color=color, lw=lw, alpha=alpha,
                        solid_capstyle="round", zorder=1)
    for li, layer in enumerate(pos):
        for ni, (x, y) in enumerate(layer):
            face = node_face if node_face is not None else WHITE
            ax.add_patch(Circle((x, y), radius, facecolor=face, edgecolor=node_colors[li],
                                lw=2.2, zorder=3))
            if node_labels and node_labels[li] and ni < len(node_labels[li]):
                ax.text(x, y, node_labels[li][ni], ha="center", va="center", fontsize=9.5,
                        color=label_color, zorder=4)
    return pos


def blank_axes(fig, xlim, ylim):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


# =====================================================================
# 1. Decorative network for the title slide (dark background)
# =====================================================================
def fig_title_network():
    fig = plt.figure(figsize=(7, 4.6))
    ax = blank_axes(fig, (-0.2, 10.2), (-0.2, 6.2))
    sizes = [3, 5, 5, 2]
    colors = [BLUE, PURPLE, PURPLE, GREEN]
    draw_network(ax, sizes, colors, radius=0.3, edge_color="#5A5A60", edge_width=1.1,
                 node_face="#1D1D1F")
    save(fig, "title-network.png", transparent=True)


# =====================================================================
# 2. Architecture: data flow from input to output
# =====================================================================
def fig_architecture():
    fig = plt.figure(figsize=(11, 6.2))
    ax = blank_axes(fig, (-0.3, 11.3), (-1.35, 6.6))
    sizes = [3, 5, 4, 1]
    colors = [BLUE, PURPLE, PURPLE, GREEN]
    labels = [["x₁", "x₂", "x₃"], None, None, ["ŷ"]]
    pos = draw_network(ax, sizes, colors, radius=0.3, edge_color="#C7C7CC", edge_width=1.1,
                       node_labels=labels, width=11.0, height=6.0)
    # layer captions
    captions = ["Input layer", "Hidden layer 1", "Hidden layer 2", "Output layer"]
    sub = ["one neuron per feature", "5 neurons", "4 neurons", "the prediction"]
    for li, layer in enumerate(pos):
        x = layer[0, 0]
        caption_colors = ["#0066CC", "#8A3FC7", "#8A3FC7", "#1B7F3B"]
        ax.text(x, -0.45, captions[li], ha="center", va="top", fontsize=12.5, fontweight="semibold",
                color=caption_colors[li])
        ax.text(x, -0.92, sub[li], ha="center", va="top", fontsize=10.5, color=TEXT2)
    # data flow arrow across the top
    ax.add_patch(FancyArrowPatch((0.6, 6.35), (10.4, 6.35), arrowstyle="-|>", mutation_scale=18,
                                 lw=1.6, color=TEXT2))
    ax.text(5.5, 6.5, "Forward pass: data flows left to right", ha="center", va="bottom",
            fontsize=11.5, color=TEXT2)
    # feature annotations on the left
    feats = ["feature 1", "feature 2", "feature 3"]
    for (x, y), f in zip(pos[0], feats):
        ax.text(x - 0.42, y, f, ha="right", va="center", fontsize=10, color=TEXT2)
    ax.text(pos[3][0, 0] + 0.42, pos[3][0, 1], "class or value", ha="left", va="center",
            fontsize=10, color=TEXT2)
    save(fig, "architecture.png")


# =====================================================================
# 3. Layers: the same network with the three layer groups marked
# =====================================================================
def fig_layers():
    fig = plt.figure(figsize=(11, 6.0))
    ax = blank_axes(fig, (-0.3, 11.3), (-1.2, 6.9))
    sizes = [3, 5, 4, 1]
    colors = [BLUE, BLUE, BLUE, BLUE]
    pos = layer_positions(sizes, 11.0, 6.0)
    # translucent bands behind each layer group
    groups = [([0], "Input layer", "Receives the raw features. No computation here."),
              ([1, 2], "Hidden layers", "Each layer re-describes its input as new features."),
              ([3], "Output layer", "Turns the last features into the answer.")]
    for idxs, title, desc in groups:
        x_left = pos[idxs[0]][0, 0] - 0.75
        x_right = pos[idxs[-1]][0, 0] + 0.75
        ax.add_patch(FancyBboxPatch((x_left, -0.1), x_right - x_left, 6.2,
                                    boxstyle="round,pad=0,rounding_size=0.35",
                                    facecolor=BLUE, alpha=0.08, edgecolor="none", zorder=0))
        cx = (x_left + x_right) / 2
        ax.text(cx, 6.55, title, ha="center", va="bottom", fontsize=13, fontweight="semibold",
                color=TEXT)
    draw_network(ax, sizes, colors, radius=0.3, edge_color="#C7C7CC", edge_width=1.1,
                 width=11.0, height=6.0)
    # depth annotation
    ax.annotate("", xy=(pos[2][0, 0] + 0.75, -0.45), xytext=(pos[1][0, 0] - 0.75, -0.45),
                arrowprops=dict(arrowstyle="<->", color=TEXT2, lw=1.2))
    ax.text((pos[1][0, 0] + pos[2][0, 0]) / 2, -0.62, "depth = number of hidden layers (2 here)",
            ha="center", va="top", fontsize=10.5, color=TEXT2)
    save(fig, "layers.png")


# =====================================================================
# 4. A single neuron
# =====================================================================
def fig_neuron():
    fig = plt.figure(figsize=(11, 4.6))
    ax = blank_axes(fig, (-0.2, 11.2), (-0.3, 4.6))
    inputs_y = [3.6, 2.15, 0.7]
    labels = ["x₁", "x₂", "x₃"]
    wlabels = ["w₁", "w₂", "w₃"]
    sum_center = (5.0, 2.15)
    # inputs
    for y, lab, wl in zip(inputs_y, labels, wlabels):
        ax.add_patch(Circle((1.0, y), 0.36, facecolor=WHITE, edgecolor=BLUE, lw=2.2, zorder=3))
        ax.text(1.0, y, lab, ha="center", va="center", fontsize=12, color=TEXT, zorder=4)
        ax.plot([1.38, sum_center[0] - 0.62], [y, sum_center[1]], color=GREEN, lw=2.6, zorder=1,
                solid_capstyle="round")
        # weight label along the edge
        mx = (1.38 + sum_center[0] - 0.62) / 2
        my = (y + sum_center[1]) / 2
        ax.text(mx, my + 0.22 if y >= sum_center[1] else my - 0.22, wl, ha="center",
                va="center", fontsize=11.5, color="#1B7F3B", fontweight="semibold",
                bbox=dict(boxstyle="round,pad=0.15", facecolor=WHITE, edgecolor="none"))
    ax.text(1.0, 4.35, "inputs", ha="center", va="center", fontsize=11, color=TEXT2)
    ax.text(3.0, 4.35, "weights", ha="center", va="center", fontsize=11, color=TEXT2)
    # summation node
    ax.add_patch(Circle(sum_center, 0.62, facecolor=WHITE, edgecolor=PURPLE, lw=2.6, zorder=3))
    ax.text(sum_center[0], sum_center[1] + 0.1, "Σ", ha="center", va="center", fontsize=22,
            color=TEXT, zorder=4)
    ax.text(sum_center[0], sum_center[1] - 0.33, "+ b", ha="center", va="center", fontsize=10.5,
            color=TEXT2, zorder=4)
    ax.text(sum_center[0], 4.35, "weighted sum", ha="center", va="center", fontsize=11, color=TEXT2)
    ax.text(sum_center[0], 1.2, "z = w₁x₁ + w₂x₂ + w₃x₃ + b", ha="center", va="center",
            fontsize=11, color=TEXT2)
    # bias input
    ax.add_patch(Circle((5.0, 3.85), 0.3, facecolor=WHITE, edgecolor=TEXT3, lw=1.6, zorder=3))
    ax.text(5.0, 3.85, "1", ha="center", va="center", fontsize=11, color=TEXT2, zorder=4)
    ax.plot([5.0, 5.0], [3.55, 2.78], color=TEXT3, lw=1.6, zorder=1)
    ax.text(5.38, 3.3, "b", ha="left", va="center", fontsize=11.5, color=TEXT2)
    # arrow to activation
    ax.add_patch(FancyArrowPatch((5.65, 2.15), (6.75, 2.15), arrowstyle="-|>", mutation_scale=16,
                                 lw=1.8, color=TEXT2))
    # activation box with a small ReLU glyph
    ax.add_patch(FancyBboxPatch((6.85, 1.35), 1.9, 1.6, boxstyle="round,pad=0,rounding_size=0.25",
                                facecolor=WHITE, edgecolor=ORANGE, lw=2.6, zorder=3))
    gx = np.linspace(-1, 1, 50)
    gy = np.maximum(0, gx)
    ax.plot(7.8 + gx * 0.6, 1.85 + gy * 0.75, color=ORANGE, lw=2.4, zorder=4)
    ax.plot([7.2, 8.4], [1.85, 1.85], color=RULE, lw=0.8, zorder=3)
    ax.text(7.8, 1.0, "activation f(z)", ha="center", va="center", fontsize=11, color=TEXT2)
    ax.text(7.8, 4.35, "activation", ha="center", va="center", fontsize=11, color=TEXT2)
    # output
    ax.add_patch(FancyArrowPatch((8.8, 2.15), (9.75, 2.15), arrowstyle="-|>", mutation_scale=16,
                                 lw=1.8, color=TEXT2))
    ax.add_patch(Circle((10.2, 2.15), 0.4, facecolor=WHITE, edgecolor=GREEN, lw=2.2, zorder=3))
    ax.text(10.2, 2.15, "a", ha="center", va="center", fontsize=13, color=TEXT, zorder=4)
    ax.text(10.2, 4.35, "output", ha="center", va="center", fontsize=11, color=TEXT2)
    ax.text(10.2, 1.2, "a = f(z)", ha="center", va="center", fontsize=11, color=TEXT2)
    save(fig, "neuron.png")


# =====================================================================
# Playground-style datasets (modeled on the TensorFlow Playground generators)
# =====================================================================
def make_circle(n, noise):
    radius = 5.0
    pts, labels = [], []
    for inside in (True, False):
        for _ in range(n // 2):
            r = RNG.uniform(0, radius * 0.5) if inside else RNG.uniform(radius * 0.7, radius)
            angle = RNG.uniform(0, 2 * np.pi)
            x = r * np.sin(angle) + RNG.uniform(-radius, radius) * noise
            y = r * np.cos(angle) + RNG.uniform(-radius, radius) * noise
            pts.append((x, y))
            labels.append(1 if inside else 0)
    return np.array(pts), np.array(labels)


def make_xor(n, noise):
    pts, labels = [], []
    for _ in range(n):
        x = RNG.uniform(-5, 5)
        x += 0.3 if x > 0 else -0.3
        y = RNG.uniform(-5, 5)
        y += 0.3 if y > 0 else -0.3
        nx = RNG.uniform(-5, 5) * noise
        ny = RNG.uniform(-5, 5) * noise
        pts.append((x + nx, y + ny))
        labels.append(1 if x * y >= 0 else 0)
    return np.array(pts), np.array(labels)


def make_gauss(n, noise):
    variance = 0.5 + (4 - 0.5) * noise  # Playground maps noise 0..0.5 onto 0.5..4
    pts, labels = [], []
    for center, label in (((2, 2), 1), ((-2, -2), 0)):
        for _ in range(n // 2):
            pts.append(RNG.normal(center, np.sqrt(variance)))
            labels.append(label)
    return np.array(pts), np.array(labels)


def make_spiral(n, noise):
    pts, labels = [], []
    half = n // 2
    for delta, label in ((0, 1), (np.pi, 0)):
        for i in range(half):
            r = i / half * 5
            t = 1.75 * i / half * 2 * np.pi + delta
            x = r * np.sin(t) + RNG.uniform(-1, 1) * noise
            y = r * np.cos(t) + RNG.uniform(-1, 1) * noise
            pts.append((x, y))
            labels.append(label)
    return np.array(pts), np.array(labels)


DATASETS = [("Circle", make_circle), ("Exclusive or", make_xor),
            ("Gaussian", make_gauss), ("Spiral", make_spiral)]


def split(X, y, ratio=0.5):
    idx = RNG.permutation(len(X))
    cut = int(len(X) * ratio)
    tr, te = idx[:cut], idx[cut:]
    return X[tr], y[tr], X[te], y[te]


def boundary(ax, model, X, y, title=None, note=None, transform=None):
    grid_x, grid_y = np.meshgrid(np.linspace(-6, 6, 220), np.linspace(-6, 6, 220))
    grid = np.column_stack([grid_x.ravel(), grid_y.ravel()])
    feats = transform(grid) if transform else grid
    prob = model.predict_proba(feats)[:, 1].reshape(grid_x.shape)
    ax.contourf(grid_x, grid_y, prob, levels=np.linspace(0, 1, 21),
                cmap=matplotlib.colors.LinearSegmentedColormap.from_list("pb", [ORANGE, WHITE, BLUE]),
                alpha=0.75, antialiased=True)
    ax.contour(grid_x, grid_y, prob, levels=[0.5], colors=[TEXT2], linewidths=0.8)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], s=9, c=BLUE, edgecolors=WHITE, linewidths=0.3)
    ax.scatter(X[y == 0, 0], X[y == 0, 1], s=9, c=ORANGE, edgecolors=WHITE, linewidths=0.3)
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor(RULE)
    if title:
        ax.set_title(title, fontsize=11.5, color=TEXT, pad=6)
    if note:
        ax.text(0.5, -0.06, note, transform=ax.transAxes, ha="center", va="top", fontsize=10,
                color=TEXT2)


RESULTS = {}


def fig_playground_grid():
    """Two rows: a model with no hidden layer, and a network with two hidden layers of 8."""
    fig, axes = plt.subplots(2, 4, figsize=(12.4, 6.9))
    row_titles = ["No hidden layer\n(linear boundary)", "Two hidden layers\nof 8 neurons, tanh"]
    for col, (name, maker) in enumerate(DATASETS):
        X, y = maker(400, 0.0)
        Xtr, ytr, Xte, yte = split(X, y)
        linear = LogisticRegression().fit(Xtr, ytr)
        deep = MLPClassifier(hidden_layer_sizes=(8, 8), activation="tanh", max_iter=3000,
                             random_state=3, learning_rate_init=0.03).fit(Xtr, ytr)
        acc_lin = accuracy_score(yte, linear.predict(Xte))
        acc_deep = accuracy_score(yte, deep.predict(Xte))
        RESULTS[f"{name}:linear"] = round(acc_lin * 100)
        RESULTS[f"{name}:deep"] = round(acc_deep * 100)
        boundary(axes[0, col], linear, Xte, yte, title=name, note=f"test accuracy {acc_lin:.0%}")
        boundary(axes[1, col], deep, Xte, yte, note=f"test accuracy {acc_deep:.0%}")
    for row in range(2):
        axes[row, 0].text(-0.08, 0.5, row_titles[row], transform=axes[row, 0].transAxes,
                          ha="right", va="center", fontsize=11, color=TEXT, rotation=90,
                          multialignment="center")
    fig.subplots_adjust(left=0.07, right=0.99, top=0.93, bottom=0.07, wspace=0.12, hspace=0.3)
    save(fig, "playground-grid.png")


def fig_activation_experiment():
    """Spiral: identity activation vs tanh vs relu with three hidden layers of 8."""
    X, y = make_spiral(400, 0.0)
    Xtr, ytr, Xte, yte = split(X, y)
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.9))
    for ax, (act, label) in zip(axes, [("identity", "Linear activation"), ("tanh", "Tanh"),
                                       ("relu", "ReLU")]):
        model = MLPClassifier(hidden_layer_sizes=(8, 8, 8), activation=act, max_iter=4000,
                              random_state=3, learning_rate_init=0.03).fit(Xtr, ytr)
        acc = accuracy_score(yte, model.predict(Xte))
        RESULTS[f"spiral-activation:{act}"] = round(acc * 100)
        boundary(ax, model, Xte, yte, title=label, note=f"test accuracy {acc:.0%}")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.1, wspace=0.12)
    save(fig, "activation-experiment.png")


def fig_feature_experiment():
    """A linear model solves XOR and the circle once the right features are added."""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9))
    X, y = make_circle(400, 0.0)
    Xtr, ytr, Xte, yte = split(X, y)
    squares = lambda P: np.column_stack([P, P[:, 0] ** 2, P[:, 1] ** 2])
    lin = LogisticRegression().fit(squares(Xtr), ytr)
    acc = accuracy_score(yte, lin.predict(squares(Xte)))
    RESULTS["circle:linear+squares"] = round(acc * 100)
    boundary(axes[0], lin, Xte, yte, title="Circle with x₁², x₂² added",
             note=f"no hidden layer, test accuracy {acc:.0%}", transform=squares)
    X, y = make_xor(400, 0.0)
    Xtr, ytr, Xte, yte = split(X, y)
    product = lambda P: np.column_stack([P, P[:, 0] * P[:, 1]])
    lin = LogisticRegression().fit(product(Xtr), ytr)
    acc = accuracy_score(yte, lin.predict(product(Xte)))
    RESULTS["xor:linear+product"] = round(acc * 100)
    boundary(axes[1], lin, Xte, yte, title="XOR with x₁x₂ added",
             note=f"no hidden layer, test accuracy {acc:.0%}", transform=product)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.1, wspace=0.12)
    save(fig, "feature-experiment.png")


def noise_experiment():
    """Circle dataset at three noise levels, same network; records test loss and accuracy."""
    rows = []
    for noise in (0.0, 0.25, 0.5):
        X, y = make_circle(400, noise)
        Xtr, ytr, Xte, yte = split(X, y)
        model = MLPClassifier(hidden_layer_sizes=(8, 8), activation="tanh", max_iter=3000,
                              random_state=3, learning_rate_init=0.03).fit(Xtr, ytr)
        tr_loss = log_loss(ytr, model.predict_proba(Xtr))
        te_loss = log_loss(yte, model.predict_proba(Xte))
        acc = accuracy_score(yte, model.predict(Xte))
        rows.append(dict(noise=int(noise * 100), train_loss=round(tr_loss, 3),
                         test_loss=round(te_loss, 3), test_acc=round(acc * 100)))
    RESULTS["noise"] = rows


# =====================================================================
# 5. Weights: a trained 2-4-1 network on XOR, edges styled by learned weight
# =====================================================================
def fig_weights():
    X, y = make_xor(400, 0.0)
    model = MLPClassifier(hidden_layer_sizes=(4,), activation="tanh", max_iter=5000,
                          random_state=5, learning_rate_init=0.03).fit(X, y)
    W = [model.coefs_[0], model.coefs_[1]]
    RESULTS["xor-2-4-1:train_acc"] = round(accuracy_score(y, model.predict(X)) * 100)
    fig = plt.figure(figsize=(7.4, 4.8))
    ax = blank_axes(fig, (-0.4, 7.6), (-0.9, 5.3))
    pos = draw_network(ax, [2, 4, 1], [BLUE, PURPLE, GREEN], radius=0.32, weights=W,
                       node_labels=[["x₁", "x₂"], None, ["ŷ"]], width=7.0, height=4.6)
    # legend
    ax.plot([0.3, 1.1], [-0.45, -0.45], color=BLUE, lw=3.2); ax.text(1.25, -0.45, "positive weight", va="center", fontsize=10, color=TEXT2)
    ax.plot([3.3, 4.1], [-0.45, -0.45], color=ORANGE, lw=3.2); ax.text(4.25, -0.45, "negative weight", va="center", fontsize=10, color=TEXT2)
    ax.text(3.5, 5.05, "Thicker line = larger |w|. Weights learned on the XOR data.", ha="center",
            va="center", fontsize=10.5, color=TEXT2)
    save(fig, "weights.png")


# =====================================================================
# 6. Activation functions
# =====================================================================
def fig_activations():
    z = np.linspace(-4, 4, 400)
    funcs = [("Linear", z, "f(z) = z", "no bend: stacking linear layers\nstill gives a linear model"),
             ("Sigmoid", 1 / (1 + np.exp(-z)), "f(z) = 1 / (1 + e⁻ᶻ)", "squashes to (0, 1);\nused for probabilities"),
             ("Tanh", np.tanh(z), "f(z) = tanh(z)", "squashes to (−1, 1);\nzero-centered"),
             ("ReLU", np.maximum(0, z), "f(z) = max(0, z)", "zero for negatives, identity for\npositives; the default for hidden layers")]
    fig, axes = plt.subplots(1, 4, figsize=(12.4, 3.6))
    ranges = {"Linear": ((-4.2, 4.2), [-4, 0, 4]), "Sigmoid": ((-0.25, 1.25), [0, 1]),
              "Tanh": ((-1.25, 1.25), [-1, 0, 1]), "ReLU": ((-0.5, 4.2), [0, 4])}
    for ax, (name, fz, formula, note) in zip(axes, funcs):
        ax.axhline(0, color=RULE, lw=0.8); ax.axvline(0, color=RULE, lw=0.8)
        ax.plot(z, fz, color=ORANGE, lw=2.6)
        ylim, yticks = ranges[name]
        ax.set_xlim(-4, 4); ax.set_ylim(*ylim)
        ax.set_title(name, fontsize=13, color=TEXT, pad=8, fontweight="semibold")
        ax.text(0.5, -0.2, formula, transform=ax.transAxes, ha="center", va="top", fontsize=11,
                color=TEXT)
        ax.text(0.5, -0.36, note, transform=ax.transAxes, ha="center", va="top", fontsize=9.5,
                color=TEXT2, linespacing=1.3)
        ax.set_xticks([-4, 4]); ax.set_yticks(yticks); ax.tick_params(labelsize=9)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.subplots_adjust(left=0.04, right=0.99, top=0.86, bottom=0.36, wspace=0.3)
    save(fig, "activations.png")


# =====================================================================
# 7. Loss functions
# =====================================================================
def fig_losses():
    fig, axes = plt.subplots(1, 3, figsize=(12.4, 3.6))
    # MSE
    err = np.linspace(-2, 2, 300)
    axes[0].plot(err, err ** 2, color=RED, lw=2.6)
    axes[0].set_title("Mean squared error", fontsize=13, color=TEXT, pad=8, fontweight="semibold")
    axes[0].set_xlabel("prediction − target", fontsize=10)
    axes[0].set_ylabel("loss", fontsize=10)
    axes[0].text(0.5, -0.36, "regression: small misses cost little,\nlarge misses cost a lot",
                 transform=axes[0].transAxes, ha="center", va="top", fontsize=9.5, color=TEXT2)
    # cross-entropy
    p = np.linspace(0.01, 1, 300)
    axes[1].plot(p, -np.log(p), color=RED, lw=2.6)
    axes[1].set_title("Cross-entropy", fontsize=13, color=TEXT, pad=8, fontweight="semibold")
    axes[1].set_xlabel("probability given to the correct class", fontsize=10)
    axes[1].set_ylabel("loss", fontsize=10)
    axes[1].text(0.5, -0.36, "classification: confident wrong answers\nare punished hardest",
                 transform=axes[1].transAxes, ha="center", va="top", fontsize=9.5, color=TEXT2)
    # training vs test loss over epochs, real run on a noisy circle
    X, y = make_circle(300, 0.35)
    Xtr, ytr, Xte, yte = split(X, y)
    model = MLPClassifier(hidden_layer_sizes=(16, 16), activation="tanh", max_iter=1,
                          warm_start=True, random_state=1, learning_rate_init=0.05,
                          solver="sgd", momentum=0.0, batch_size=10)
    train_curve, test_curve = [], []
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for _ in range(250):
            model.fit(Xtr, ytr)
            train_curve.append(log_loss(ytr, model.predict_proba(Xtr)))
            test_curve.append(log_loss(yte, model.predict_proba(Xte)))
    epochs = np.arange(1, len(train_curve) + 1)
    axes[2].plot(epochs, train_curve, color=TEXT2, lw=2.2, label="training loss")
    axes[2].plot(epochs, test_curve, color=RED, lw=2.2, label="test loss")
    axes[2].set_title("Loss during training", fontsize=13, color=TEXT, pad=8, fontweight="semibold")
    axes[2].set_xlabel("epoch", fontsize=10)
    axes[2].set_ylabel("cross-entropy", fontsize=10)
    axes[2].legend(frameon=False, fontsize=9.5, loc="upper right")
    axes[2].text(0.5, -0.36, "noisy circle data: training loss keeps falling\nwhile test loss levels off, the sign of overfitting",
                 transform=axes[2].transAxes, ha="center", va="top", fontsize=9.5, color=TEXT2)
    RESULTS["loss-curve"] = dict(final_train=round(train_curve[-1], 3), final_test=round(test_curve[-1], 3),
                                 min_test=round(min(test_curve), 3), min_test_epoch=int(np.argmin(test_curve)) + 1)
    for ax in axes:
        ax.tick_params(labelsize=9)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.subplots_adjust(left=0.05, right=0.99, top=0.86, bottom=0.34, wspace=0.3)
    save(fig, "losses.png")


# =====================================================================
# 8. Optimization: gradient descent on a loss surface at three learning rates
# =====================================================================
def fig_optimizer():
    def loss(x, y):
        return x ** 2 + 5 * y ** 2

    def grad(x, y):
        return np.array([2 * x, 10 * y])

    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    gx, gy = np.meshgrid(np.linspace(-4.6, 3.4, 300), np.linspace(-2.6, 2.6, 300))
    ax.contourf(gx, gy, loss(gx, gy), levels=18, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
        "ind", ["#FFFFFF", "#D9D8FA", INDIGO]), alpha=0.85)
    ax.contour(gx, gy, loss(gx, gy), levels=18, colors=["#FFFFFF"], linewidths=0.5, alpha=0.6)
    start = np.array([-4.0, 2.0])
    runs = [(0.02, TEXT2, "learning rate 0.02: creeps toward the minimum"),
            (0.09, GREEN, "learning rate 0.09: reaches the minimum quickly"),
            (0.19, ORANGE, "learning rate 0.19: overshoots and zigzags")]
    for lr, color, label in runs:
        p = start.copy()
        path = [p.copy()]
        for _ in range(40):
            p = p - lr * grad(*p)
            path.append(p.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], color=color, lw=1.8, marker="o", ms=3.2, label=label,
                markeredgecolor=WHITE, markeredgewidth=0.4)
    ax.plot(0, 0, marker="*", ms=14, color=TEXT, markeredgecolor=WHITE)
    ax.text(0.1, -0.28, "minimum", fontsize=10, color=TEXT)
    ax.plot(*start, marker="o", ms=7, color=TEXT, markeredgecolor=WHITE)
    ax.text(start[0] + 0.15, start[1] + 0.12, "random start", fontsize=10, color=TEXT)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-4.6, 3.4); ax.set_ylim(-2.6, 2.6)
    leg = ax.legend(fontsize=9.5, loc="lower right", framealpha=0.92, edgecolor=RULE,
                    fancybox=True, borderpad=0.8)
    leg.get_frame().set_linewidth(0.6)
    for s in ax.spines.values():
        s.set_edgecolor(RULE)
    ax.set_title("Gradient descent on a loss surface (each axis is one weight)", fontsize=12,
                 color=TEXT, pad=8, fontweight="semibold")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.03)
    save(fig, "optimizer.png")


def build_all():
    fig_title_network()
    fig_architecture()
    fig_layers()
    fig_neuron()
    fig_weights()
    fig_activations()
    fig_losses()
    fig_optimizer()
    fig_playground_grid()
    fig_activation_experiment()
    fig_feature_experiment()
    noise_experiment()
    with open(os.path.join(OUT, "results.json"), "w") as fh:
        json.dump(RESULTS, fh, indent=2)
    print(json.dumps(RESULTS, indent=2))


# =====================================================================
# 9. Learning rate experiment: training loss per epoch at three learning rates
# =====================================================================
def fig_learning_rate():
    import warnings
    X, y = make_circle(400, 0.0)
    Xtr, ytr, Xte, yte = split(X, y)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    runs = [(0.001, TEXT2, "0.001"), (0.1, GREEN, "0.1"), (10.0, ORANGE, "10")]
    out = []
    for lr, color, label in runs:
        model = MLPClassifier(hidden_layer_sizes=(8, 8), activation="tanh", solver="sgd",
                              momentum=0.0, batch_size=10, learning_rate_init=lr, max_iter=200,
                              random_state=3, n_iter_no_change=1000, tol=0)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(Xtr, ytr)
        curve = model.loss_curve_
        acc = accuracy_score(yte, model.predict(Xte))
        out.append(dict(lr=lr, first_loss=round(curve[0], 3), final_loss=round(curve[-1], 3),
                        max_loss=round(max(curve), 3), test_acc=round(acc * 100), epochs=len(curve)))
        ax.plot(np.arange(1, len(curve) + 1), curve, color=color, lw=2.2,
                label=f"learning rate {label}: test accuracy {acc:.0%}")
    RESULTS["learning-rate"] = out
    ax.set_yscale("log")
    ax.set_xlabel("epoch", fontsize=10); ax.set_ylabel("training loss (log scale)", fontsize=10)
    ax.set_title("Circle data, two hidden layers of 8, tanh", fontsize=12, color=TEXT, pad=8,
                 fontweight="semibold")
    ax.legend(frameon=False, fontsize=9.5, loc="center right")
    ax.tick_params(labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.88, bottom=0.14)
    save(fig, "learning-rate.png")


if __name__ == "__main__":
    import sys
    if "--all" in sys.argv:
        build_all()
    fig_learning_rate()
    with open(os.path.join(OUT, "results.json")) as fh:
        existing = json.load(fh)
    existing.update(RESULTS)
    with open(os.path.join(OUT, "results.json"), "w") as fh:
        json.dump(existing, fh, indent=2)
    print(json.dumps(RESULTS["learning-rate"], indent=2))
