/* Builds the "Inside a Neural Network" presentation (AIML-501 portfolio artifact 2).
 *
 * Structured deck: theme + layouts + placeholders, with content composed slide by slide
 * in scheme colors. Figures come from figures.py (../figures). Run: node deck.js
 */
const path = require("path");
const fs = require("fs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fi = require("react-icons/fi");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("./apply_theme.js");

const FIG = path.join(__dirname, "figures");   // output of figures.py
const OUT_DIR = path.join(__dirname, "out");
fs.mkdirSync(OUT_DIR, { recursive: true });
const OUT = path.join(OUT_DIR, "Rath_Neural_Network_Components.pptx");
const results = JSON.parse(fs.readFileSync(path.join(FIG, "results.json"), "utf8"));
const SIZES = JSON.parse(fs.readFileSync(path.join(FIG, "sizes.json"), "utf8"));

// ---------- theme (portfolio palette, apple.com inspired) ----------
const THEME = {
  name: "Rath Portfolio",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1D1D1F", // text
    lt1: "FFFFFF", // page
    dk2: "6E6E73", // secondary text
    lt2: "F5F5F7", // tiles
    accent1: "2997FF", // layers (blue)
    accent2: "BF5AF2", // neurons (purple)
    accent3: "30D158", // weights (green)
    accent4: "FF9F0A", // activation (orange)
    accent5: "FF375F", // loss (red)
    accent6: "5E5CE6", // optimization (indigo)
    hlink: "0066CC",
    folHlink: "0066CC",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Chittaranjan Rath";
pres.title = "Inside a Neural Network: Components and How They Work Together";
pres.subject = "AIML-501 Model Development, portfolio artifact";
const C = pres.SchemeColor;

const W = 13.333;
const M = 0.6; // outer margin
const CONTENT_W = W - 2 * M; // 12.133
const TOP = 1.45; // first content row
const BOTTOM = 6.82; // last content row

const COMP = {
  layers: { name: "Layers", scheme: C.accent1, icon: "FiLayers", n: 1, tint: "E8F3FF" },
  neurons: { name: "Neurons", scheme: C.accent2, icon: "FiCpu", n: 2, tint: "F6ECFC" },
  weights: { name: "Weights", scheme: C.accent3, icon: "FiSliders", n: 3, tint: "E9F9EE" },
  activation: { name: "Activation functions", scheme: C.accent4, icon: "FiActivity", n: 4, tint: "FFF3E0" },
  loss: { name: "Loss functions", scheme: C.accent5, icon: "FiTarget", n: 5, tint: "FFE9EE" },
  optimizer: { name: "Optimization algorithms", scheme: C.accent6, icon: "FiTrendingDown", n: 6, tint: "ECECFC" },
};

// ---------- icons (react-icons -> white PNG data URIs) ----------
const iconCache = {};
async function icon(name, color = "#FFFFFF") {
  const key = name + color;
  if (iconCache[key]) return iconCache[key];
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(fi[name], { color, size: 256, strokeWidth: 2 }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  iconCache[key] = "image/png;base64," + buf.toString("base64");
  return iconCache[key];
}

// ---------- layouts ----------
const FOOTER = "Chittaranjan Rath  ·  Inside a Neural Network  ·  AIML-501 Model Development, Indiana Wesleyan University";
pres.defineSlideMaster({
  title: "LIGHT",
  background: { color: THEME.colors.lt1 },
  objects: [
    { text: { text: FOOTER, options: { x: M, y: 7.02, w: 10.5, h: 0.3, fontSize: 9, color: C.text2, margin: 0, valign: "middle" } } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.42, w: CONTENT_W, h: 0.75, fontSize: 30, bold: true, color: C.text1, margin: 0, valign: "middle", align: "left" } } },
  ],
  slideNumber: { x: 12.1, y: 7.02, w: 0.65, h: 0.3, fontSize: 9, color: C.text2, align: "right" },
});
pres.defineSlideMaster({
  title: "COMPONENT",
  background: { color: THEME.colors.lt1 },
  objects: [
    { text: { text: FOOTER, options: { x: M, y: 7.02, w: 10.5, h: 0.3, fontSize: 9, color: C.text2, margin: 0, valign: "middle" } } },
    { placeholder: { options: { name: "title", type: "title", x: M + 0.82, y: 0.42, w: CONTENT_W - 0.82, h: 0.75, fontSize: 30, color: C.text1, margin: 0, valign: "middle", align: "left" } } },
  ],
  slideNumber: { x: 12.1, y: 7.02, w: 0.65, h: 0.3, fontSize: 9, color: C.text2, align: "right" },
});
pres.defineSlideMaster({
  title: "DARK",
  background: { color: THEME.colors.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.42, w: CONTENT_W, h: 0.75, fontSize: 30, bold: true, color: C.background1, margin: 0, valign: "middle", align: "left" } } },
  ],
});

// ---------- helpers ----------
function tile(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.16,
    fill: { color: opts.fill || C.background2 },
    line: { color: opts.fill || C.background2, width: 0 },
    objectName: opts.name || "tile",
  });
}

function circle(slide, x, y, d, color, name = "badge") {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 }, objectName: name });
}

async function badge(slide, x, y, d, comp, { number = false } = {}) {
  circle(slide, x, y, d, comp.scheme, comp.name + " badge");
  if (number) {
    slide.addText(String(comp.n), { x, y, w: d, h: d, fontSize: d * 26, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  } else {
    const s = d * 0.52;
    slide.addImage({ data: await icon(comp.icon), x: x + (d - s) / 2, y: y + (d - s) / 2, w: s, h: s, altText: comp.name + " icon" });
  }
}

// Text tile: heading + body (string or array of runs)
function textTile(slide, x, y, w, h, heading, body, opts = {}) {
  tile(slide, x, y, w, h, { fill: opts.fill, name: (heading || "text") + " tile" });
  const pad = 0.22;
  let top = y + pad;
  if (heading) {
    slide.addText(heading, { x: x + pad, y: top, w: w - 2 * pad, h: 0.32, fontSize: opts.headSize || 15, bold: true, color: opts.headColor || C.text1, margin: 0, valign: "top", isTextBox: true });
    top += 0.38;
  }
  slide.addText(body, { x: x + pad, y: top, w: w - 2 * pad, h: y + h - top - pad + 0.05, fontSize: opts.size || 14, color: opts.color || C.text1, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: opts.paraSpaceAfter ?? 6 });
}

function bullets(items, extra = {}) {
  return items.map((t, i) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: i < items.length - 1, ...extra } }));
}

// Place a figure inside a box, preserving its aspect ratio. Returns the placed rectangle.
function figure(slide, file, x, y, maxW, maxH, alt, align = "left") {
  const [pw, ph] = SIZES[file];
  let w = maxW, h = maxW * ph / pw;
  if (h > maxH) { h = maxH; w = maxH * pw / ph; }
  const fx = align === "center" ? x + (maxW - w) / 2 : x;
  slide.addImage({ path: path.join(FIG, file), x: fx, y, w, h, altText: alt });
  return { x: fx, y, w, h, bottom: y + h, right: fx + w };
}

function caption(slide, text, x, y, w, h = 0.3) {
  slide.addText(text, { x, y, w, h, fontSize: 11, color: C.text2, margin: 0, valign: "top", isTextBox: true, align: "center" });
}

async function componentTitle(slide, comp, subtitle) {
  await badge(slide, M, 0.47, 0.62, comp, { number: true });
  slide.addText([
    { text: comp.name, options: { bold: true } },
    { text: "   " + subtitle, options: { fontSize: 16, color: C.text2 } },
  ], { placeholder: "title" });
}

// Stack tiles down a column: rows = [{head, body, h, opts}]
function column(slide, x, y, w, rows, gap = 0.16) {
  let cy = y;
  for (const r of rows) {
    textTile(slide, x, cy, w, r.h, r.head, r.body, r.opts || {});
    cy += r.h + gap;
  }
  return cy - gap;
}

async function build() {
  // =====================================================================
  // Slide 1: title (dark)
  // =====================================================================
  pres.addSection({ title: "Introduction" });
  {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Introduction" });
    s.addText("AIML-501 MODEL DEVELOPMENT  ·  PORTFOLIO ARTIFACT", { x: M, y: 1.35, w: 6.6, h: 0.35, fontSize: 11, color: C.text2, charSpacing: 2, margin: 0, isTextBox: true });
    s.addText("Inside a Neural Network", { x: M, y: 1.8, w: 6.6, h: 1.75, fontSize: 44, bold: true, color: C.background1, margin: 0, valign: "top", isTextBox: true });
    s.addText("Six components, how they work together in training, and what the TensorFlow Playground shows about each", { x: M, y: 3.75, w: 6.2, h: 1.1, fontSize: 18, color: "D2D2D7", margin: 0, valign: "top", isTextBox: true });
    s.addText("Chittaranjan Rath\nIndiana Wesleyan University  ·  November 2026", { x: M, y: 5.6, w: 6.6, h: 0.75, fontSize: 13, color: C.text2, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 2 });
    figure(s, "title-network.png", 7.45, 1.95, 5.3, 3.4, "A small neural network diagram: three input neurons, two hidden layers of five, and two output neurons");
    s.addNotes("This presentation is my second portfolio artifact for AIML-501. It defines the six components every neural network is built from, shows how data flows through the architecture, and connects each component to what I observed while training models in the TensorFlow Neural Network Playground. The deck is meant to be readable on its own, so each slide pairs a visual with a short explanation.");
  }

  // =====================================================================
  // Slide 2: overview of the six components
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Introduction" });
    s.addText("Six components, one system", { placeholder: "title" });
    const defs = [
      [COMP.layers, "Groups of neurons stacked so that each layer's output becomes the next layer's input."],
      [COMP.neurons, "The unit of computation: a weighted sum of inputs plus a bias, passed through an activation."],
      [COMP.weights, "The numbers on the connections between neurons. Training is the process of adjusting them."],
      [COMP.activation, "The bend applied to each neuron's sum. Without it a deep network can only draw straight lines."],
      [COMP.loss, "One number that measures how wrong the network's predictions are on the training data."],
      [COMP.optimizer, "The procedure that uses the loss to move every weight a small step in the right direction."],
    ];
    const gap = 0.2;
    const groups = [
      { label: "Structure: what a network is made of", items: defs.slice(0, 4), labelY: 1.32, tileY: 1.68, th: 1.95 },
      { label: "Learning: how the network gets better", items: defs.slice(4), labelY: 3.9, tileY: 4.26, th: 1.5 },
    ];
    for (const g of groups) {
      s.addText(g.label, { x: M, y: g.labelY, w: CONTENT_W, h: 0.32, fontSize: 13, bold: true, color: C.text2, margin: 0, valign: "middle", isTextBox: true, charSpacing: 0.5 });
      const tw = (CONTENT_W - gap * (g.items.length - 1)) / g.items.length;
      for (let i = 0; i < g.items.length; i++) {
        const [comp, text] = g.items[i];
        const x = M + i * (tw + gap);
        const y = g.tileY;
        tile(s, x, y, tw, g.th, { name: comp.name + " tile" });
        await badge(s, x + 0.22, y + 0.22, 0.55, comp);
        s.addText(comp.name, { x: x + 0.9, y: y + 0.2, w: tw - 1.05, h: 0.6, fontSize: 16, bold: true, color: C.text1, margin: 0, valign: "middle", isTextBox: true });
        s.addText(text, { x: x + 0.22, y: y + 0.92, w: tw - 0.44, h: g.th - 1.0, fontSize: 14, color: C.text1, margin: 0, valign: "top", isTextBox: true });
      }
    }
    s.addText("Slides 3 to 10 define and illustrate each component in this order and show how they combine during training. Slides 11 to 13 test them with experiments modeled on the TensorFlow Playground (Smilkov & Carter, 2016).", { x: M, y: 6.2, w: CONTENT_W, h: 0.62, fontSize: 13, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    s.addNotes("The six components the assignment asks for are shown here as one system in two groups. The top row (layers, neurons, weights, activation functions) describes the structure of a network and what happens during a forward pass; the components are ordered the way data meets them. The bottom row (loss functions and optimization algorithms) describes how the network learns. Biases are treated as part of the weights slide because they are learned the same way, and backpropagation is treated as part of optimization because it is the step that supplies the gradient the optimizer uses. Keeping the two groups in mind makes the training loop on slide 10 easy to follow.");
  }

  // =====================================================================
  // Slide 3: architecture
  // =====================================================================
  pres.addSection({ title: "Architecture and components" });
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Architecture and components" });
    s.addText("The architecture: data flows from input to output", { placeholder: "title" });
    const f = figure(s, "architecture.png", M, TOP, 7.4, 4.85, "Feed-forward network with three inputs, two hidden layers of five and four neurons, and one output, with data flowing left to right");
    caption(s, "Every line is a weight. Every circle after the input layer is a neuron.", M, f.bottom + 0.1, f.w);
    const cx = f.right + 0.35, cw = W - M - cx;
    column(s, cx, TOP, cw, [
      { head: "Input layer", h: 1.68, body: "One neuron per feature. In the Playground that is x₁ and x₂, the coordinates of each point. No computation happens here." },
      { head: "Hidden layers", h: 1.68, body: "Each neuron combines every value from the layer before it, so each layer describes the data in new terms (LeCun et al., 2015)." },
      { head: "Output layer", h: 1.68, body: "Produces the prediction: a probability for classification, a number for regression." },
    ]);
    s.addNotes("A feed-forward network is read left to right. The input layer holds the features, each hidden layer transforms the output of the layer before it, and the output layer turns the final representation into a prediction. Nothing flows backward during prediction; the backward direction appears only in training, when gradients travel from the loss back to every weight (slide 10). The counts of neurons here are illustrative; the Playground lets you choose up to six hidden layers of up to eight neurons.");
  }

  // =====================================================================
  // Slide 4: layers
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "COMPONENT", sectionTitle: "Architecture and components" });
    await componentTitle(s, COMP.layers, "the stages data passes through");
    const f = figure(s, "layers.png", M, TOP, 7.3, 3.4, "The same network with its input, hidden and output layer groups highlighted and the depth marked as two hidden layers", "center");
    textTile(s, M, f.bottom + 0.2, 7.3, BOTTOM - (f.bottom + 0.2), "What each kind of layer does",
      bullets([
        "Input layer: holds the features, does no math.",
        "Hidden layers: each turns the previous output into new features.",
        "Output layer: turns the last features into the answer.",
      ]), { paraSpaceAfter: 3 });
    const cx = M + 7.3 + 0.35, cw = W - M - cx;
    column(s, cx, TOP, cw, [
      { head: "Definition", h: 1.85, body: "A layer is a set of neurons that receive the same inputs and compute at the same time. A network is a stack of layers, and data moves through them in a fixed order: input, hidden, output (Goodfellow et al., 2016)." },
      { head: "Depth and width", h: 1.8, body: "Depth is the number of hidden layers; width is the neurons in each. One wide layer can in principle fit any smooth boundary (Cybenko, 1989); depth gets there with fewer neurons." },
      { head: "In the Playground", h: BOTTOM - TOP - 1.85 - 1.8 - 0.32, body: "With zero hidden layers the model could only draw a straight line. Two hidden layers of 8 solved the circle and XOR data (slide 11).", opts: { fill: COMP.layers.tint } },
    ]);
    s.addNotes("Layers are the organizing unit of a network. The input layer is passive: it only holds the feature values. Each hidden layer applies the same operation (weighted sum, bias, activation) in parallel across its neurons, so a hidden layer can be read as a new description of the data. Depth and width are the two architecture choices the Playground exposes through its plus and minus buttons. Cybenko's 1989 result says one hidden layer is enough in principle if it is wide enough; in practice deeper networks reach the same boundary with far fewer neurons. In my experiments a model with no hidden layer could separate the two Gaussian blobs and nothing else, while two hidden layers of eight neurons were enough for the circle and XOR datasets.");
  }

  // =====================================================================
  // Slide 5: neurons
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "COMPONENT", sectionTitle: "Architecture and components" });
    await componentTitle(s, COMP.neurons, "the unit of computation");
    const f = figure(s, "neuron.png", M, TOP, 7.5, 2.6, "One neuron: three inputs multiplied by weights, summed with a bias, passed through an activation function to produce one output", "center");
    const fy = f.bottom + 0.2;
    tile(s, M, fy, 7.5, 0.95, { name: "formula tile" });
    s.addText([
      { text: "a = f(w₁x₁ + w₂x₂ + w₃x₃ + b)", options: { fontSize: 22, bold: true, color: C.text1, breakLine: true } },
      { text: "weighted sum, plus bias, then the activation", options: { fontSize: 12, color: C.text2 } },
    ], { x: M + 0.25, y: fy + 0.08, w: 7.0, h: 0.8, margin: 0, valign: "middle", align: "center", isTextBox: true });
    textTile(s, M, fy + 1.1, 7.5, BOTTOM - (fy + 1.1), "In the Playground",
      "Hovering over a neuron shows the pattern it has learned as a small heat map over the input space. First-layer neurons learn straight splits; deeper neurons combine those splits into curves and corners.", { fill: COMP.neurons.tint });
    const cx = M + 7.5 + 0.35, cw = W - M - cx;
    column(s, cx, TOP, cw, [
      { head: "Definition", h: 2.5, body: "A neuron multiplies each input by its own weight, adds the products together with a bias, and passes the total through an activation function. Its single output becomes an input to the next layer (Nielsen, 2015)." },
      { head: "What a neuron does", h: BOTTOM - TOP - 2.5 - 0.16, body: bullets([
        "Acts as a small detector: it responds strongly to some input patterns and weakly to others.",
        "The bias shifts the threshold, so a neuron can respond even when every input is zero.",
        "A layer of neurons is many detectors reading the same input at once.",
      ]), opts: { paraSpaceAfter: 4 } },
    ]);
    s.addNotes("The neuron is where all of the arithmetic happens. The weighted sum z is a linear operation; the activation f adds the nonlinearity. The bias is often forgotten but it matters: without it, every neuron's boundary would have to pass through the origin. The Playground's neuron thumbnails are the best visual explanation of this I have seen. Each first-layer thumbnail is a straight split of the plane, and the thumbnails in deeper layers are visibly built from combinations of the layer before.");
  }

  // =====================================================================
  // Slide 6: weights and biases
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "COMPONENT", sectionTitle: "Architecture and components" });
    await componentTitle(s, COMP.weights, "the numbers that training changes");
    const leftW = 5.2;
    const f = figure(s, "weights.png", M, TOP, leftW, 3.45, "A 2-4-1 network trained on XOR data; each connection is drawn thicker for a larger weight, blue for positive and orange for negative", "center");
    textTile(s, M, f.bottom + 0.2, leftW, BOTTOM - (f.bottom + 0.2), "In the Playground",
      "Connection lines are drawn thicker for larger weights and colored by sign, blue for positive and orange for negative. Hovering over a line shows its value.", { fill: COMP.weights.tint });
    const cx = M + leftW + 0.35, cw = W - M - cx;
    const bottomRow = 1.3;
    column(s, cx, TOP, cw, [
      { head: "Definition", h: 1.95, body: "A weight is the number attached to each connection. It scales the signal on that connection: large and positive amplifies it, negative flips it, near zero switches it off. A bias is one extra number per neuron that shifts its threshold." },
      { head: "What training changes", h: BOTTOM - TOP - 1.95 - bottomRow - 0.32, body: "Weights and biases are the only things training changes. The architecture, activation and loss are fixed by the designer. Training starts from random values and adjusts them a little per step." },
    ]);
    const sy = BOTTOM - bottomRow;
    tile(s, cx, sy, cw * 0.42, bottomRow, { name: "parameter count tile" });
    s.addText([
      { text: "105", options: { fontSize: 32, bold: true, color: C.accent3, breakLine: true } },
      { text: "learnable parameters in a 2-8-8-1 network", options: { fontSize: 11, color: C.text2 } },
    ], { x: cx + 0.2, y: sy + 0.08, w: cw * 0.42 - 0.4, h: bottomRow - 0.16, margin: 0, valign: "middle", align: "left", isTextBox: true });
    textTile(s, cx + cw * 0.42 + 0.16, sy, cw * 0.58 - 0.16, bottomRow, null,
      "(2×8 + 8) + (8×8 + 8) + (8×1 + 1). Every connection has a weight and every neuron a bias, so the count grows fast with width and depth.", { size: 12, color: C.text2 });
    s.addNotes("Weights are what a trained model actually is: the architecture is a container, and the weights are the content. The figure shows a two-input, four-neuron, one-output network trained on the XOR data, with each connection drawn according to its learned weight. The parameter count on the right is worth doing once by hand, because it shows how quickly the number grows: a network with two hidden layers of eight has 105 numbers to learn, and a modern language model has billions. The Playground draws weights the same way, and editing a weight by hand and watching the boundary change is a good way to feel what each one does.");
  }

  // =====================================================================
  // Slide 7: activation functions
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "COMPONENT", sectionTitle: "Architecture and components" });
    await componentTitle(s, COMP.activation, "the bend that makes depth useful");
    const f = figure(s, "activations.png", M, 1.35, CONTENT_W, 2.85, "Four activation functions plotted: linear, sigmoid, tanh and ReLU, with their formulas", "center");
    const ty = f.bottom + 0.3, th = BOTTOM - ty;
    const tw = (CONTENT_W - 0.4) / 3;
    textTile(s, M, ty, tw, th, "Why they exist",
      "A weighted sum of weighted sums is still a weighted sum. Without a nonlinear activation, a stack of layers collapses into one linear model that can only draw straight boundaries. The activation adds the bend that lets layers build curves.");
    textTile(s, M + tw + 0.2, ty, tw, th, "Which to use",
      "ReLU is the default for hidden layers: cheap, and it keeps gradients alive in deep networks (Nair & Hinton, 2010). Sigmoid turns one output into a probability; softmax does the same across classes. Tanh is the Playground's default.");
    textTile(s, M + 2 * (tw + 0.2), ty, tw, th, "In the Playground",
      `Same spiral data, same three hidden layers of 8. Linear activation: ${results["spiral-activation:identity"]}% test accuracy and a straight line. Tanh: ${results["spiral-activation:tanh"]}%. ReLU: ${results["spiral-activation:relu"]}%, with the sharp corners a piecewise-linear function produces (slide 12).`, { fill: COMP.activation.tint });
    s.addNotes("The activation function is the reason depth works at all. Composing linear functions gives another linear function, so without an activation a ten-layer network has exactly the power of a one-layer one. Sigmoid and tanh were the historical choices; ReLU (Nair and Hinton, 2010) became the default for hidden layers because it is cheap and avoids the vanishing gradients that squashing functions cause in deep networks. The Playground offers all four, and the spiral experiment on slide 12 makes the difference visible: the linear option never gets past a straight line.");
  }

  // =====================================================================
  // Slide 8: loss functions
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "COMPONENT", sectionTitle: "Architecture and components" });
    await componentTitle(s, COMP.loss, "the score that training tries to lower");
    const f = figure(s, "losses.png", M, 1.35, CONTENT_W, 2.85, "Mean squared error and cross-entropy curves, and a chart of training loss and test loss over 250 epochs on noisy circle data", "center");
    const ty = f.bottom + 0.3, th = BOTTOM - ty;
    const tw = (CONTENT_W - 0.4) / 3;
    textTile(s, M, ty, tw, th, "Definition",
      "The loss function compares a prediction with the true answer and returns one number: zero when the prediction is right, larger the more wrong it is, averaged over the training examples. Training is a search for the weights that make it small.");
    textTile(s, M + tw + 0.2, ty, tw, th, "Two common choices",
      "Mean squared error for regression: the average squared difference between prediction and target. Cross-entropy for classification: the negative log of the probability given to the correct class, which punishes confident mistakes hardest.");
    textTile(s, M + 2 * (tw + 0.2), ty, tw, th, "In the Playground",
      `The Playground plots training and test loss every epoch. Test loss comes from points the network never trained on, so a widening gap means memorizing rather than learning. At 50% noise my test loss reached ${results.noise[2].test_loss} while training loss stayed at ${results.noise[2].train_loss} (slide 13).`, { fill: COMP.loss.tint });
    s.addNotes("The loss function defines what 'better' means for the network. Mean squared error is the natural choice for regression, cross-entropy for classification; both are zero for a perfect prediction and grow with the error, but cross-entropy grows without bound as a confident prediction becomes wrong, which is what makes it such a strong training signal. The right-hand chart is a real run on noisy circle data: training loss keeps falling for 250 epochs while test loss reaches its minimum near epoch 55 and then rises. That gap is overfitting, and the Playground shows the same two curves in its top-right corner.");
  }

  // =====================================================================
  // Slide 9: optimization algorithms
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "COMPONENT", sectionTitle: "Architecture and components" });
    await componentTitle(s, COMP.optimizer, "how the weights get better");
    const f = figure(s, "optimizer.png", M, TOP, 6.9, 4.7, "Contour plot of a loss surface over two weights with three gradient descent paths at learning rates 0.02, 0.09 and 0.19");
    caption(s, "Each axis is one weight; shading is the loss. The star is the minimum the optimizer is looking for.", M, f.bottom + 0.1, f.w, 0.35);
    const cx = f.right + 0.35, cw = W - M - cx;
    column(s, cx, TOP, cw, [
      { head: "Gradient descent", h: 1.85, body: "Backpropagation computes, for every weight, how the loss would change if that weight moved slightly (Rumelhart et al., 1986). Gradient descent then moves every weight a small step downhill, and repeats." },
      { head: "Variants", h: 1.75, body: "Stochastic gradient descent (SGD) steps from a small batch instead of the whole dataset. Momentum carries part of the previous step forward. Adam adapts the step per weight (Kingma & Ba, 2015)." },
      { head: "Learning rate", h: BOTTOM - TOP - 1.85 - 1.75 - 0.32, body: "The step size. Too small and training crawls; too large and the weights overshoot and bounce. The Playground offers 0.00001 to 10 (slide 13).", opts: { fill: COMP.optimizer.tint } },
    ]);
    s.addNotes("The optimizer closes the loop. Backpropagation (Rumelhart, Hinton and Williams, 1986) is the efficient way to get the gradient of the loss with respect to every weight at once; gradient descent is the rule that uses it. Plain gradient descent uses the whole dataset per step, stochastic gradient descent uses a small batch, and Adam (Kingma and Ba, 2015) adds per-weight step sizes and momentum. The figure is a two-weight toy problem so the paths can be drawn: the small learning rate creeps, the middle one converges quickly, and the large one bounces across the valley. Slide 13 shows the same three behaviors on a real network.");
  }

  // =====================================================================
  // Slide 10: the training loop
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Architecture and components" });
    s.addText("How the six components work together", { placeholder: "title" });
    const steps = [
      { head: "1  Forward pass", comps: [COMP.layers, COMP.neurons, COMP.weights, COMP.activation], body: "Input flows through the layers. Each neuron applies its weights, bias and activation, and the output layer produces a prediction." },
      { head: "2  Loss", comps: [COMP.loss], body: "The loss function scores the prediction against the true label and returns one number." },
      { head: "3  Backpropagation", comps: [COMP.loss, COMP.weights], body: "The gradient of the loss is computed for every weight and bias, output layer first, working backward." },
      { head: "4  Update", comps: [COMP.optimizer], body: "The optimizer moves every weight and bias a small step against its gradient, scaled by the learning rate." },
    ];
    const bw = 2.7, bh = 2.75, gap = 0.44, by = 1.6;
    const total = 4 * bw + 3 * gap;
    const bx0 = (W - total) / 2;
    const centers = [];
    for (let i = 0; i < steps.length; i++) {
      const x = bx0 + i * (bw + gap);
      centers.push(x + bw / 2);
      tile(s, x, by, bw, bh, { name: steps[i].head + " tile" });
      let dx = x + 0.25;
      for (const comp of steps[i].comps) {
        circle(s, dx, by + 0.25, 0.3, comp.scheme, comp.name + " dot");
        dx += 0.38;
      }
      s.addText(steps[i].head, { x: x + 0.25, y: by + 0.65, w: bw - 0.5, h: 0.4, fontSize: 16, bold: true, color: C.text1, margin: 0, valign: "top", isTextBox: true });
      s.addText(steps[i].body, { x: x + 0.25, y: by + 1.1, w: bw - 0.5, h: bh - 1.3, fontSize: 13, color: C.text1, margin: 0, valign: "top", isTextBox: true });
      if (i < steps.length - 1) {
        s.addShape(pres.ShapeType.rightArrow, { x: x + bw + 0.08, y: by + bh / 2 - 0.17, w: gap - 0.16, h: 0.34, fill: { color: "C7C7CC" }, line: { color: "C7C7CC", width: 0 }, objectName: "arrow" });
      }
    }
    const ry = by + bh + 0.55;
    const lineOpts = () => ({ color: "86868B", width: 1.75 });
    s.addShape(pres.ShapeType.line, { x: centers[3], y: by + bh, w: 0, h: ry - (by + bh), line: lineOpts(), objectName: "return path" });
    s.addShape(pres.ShapeType.line, { x: centers[0], y: ry, w: centers[3] - centers[0], h: 0, line: lineOpts(), objectName: "return path" });
    s.addShape(pres.ShapeType.line, { x: centers[0], y: by + bh, w: 0, h: ry - (by + bh), line: { ...lineOpts(), beginArrowType: "triangle" }, objectName: "return path" });
    s.addShape(pres.ShapeType.roundRect, { x: W / 2 - 2.6, y: ry - 0.22, w: 5.2, h: 0.44, rectRadius: 0.22, fill: { color: C.background1 }, line: { color: "86868B", width: 1 }, objectName: "loop label" });
    s.addText("Next batch. One pass over all the training data is an epoch.", { x: W / 2 - 2.6, y: ry - 0.22, w: 5.2, h: 0.44, fontSize: 12, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true });
    const legendItems = [COMP.layers, COMP.neurons, COMP.weights, COMP.activation, COMP.loss, COMP.optimizer];
    let lx = bx0;
    const ly = 5.55;
    for (const comp of legendItems) {
      circle(s, lx, ly + 0.06, 0.2, comp.scheme, comp.name + " legend dot");
      const label = comp.name.replace(" functions", "").replace(" algorithms", "");
      const lw = 0.2 + label.length * 0.1;
      s.addText(label, { x: lx + 0.27, y: ly, w: lw, h: 0.32, fontSize: 12, color: C.text2, margin: 0, valign: "middle", isTextBox: true });
      lx += 0.27 + lw + 0.3;
    }
    textTile(s, M, 6.0, CONTENT_W, 0.82, null,
      "In the Playground, pressing play runs this loop. The epoch counter and the two loss curves at the top show the loop working, and the boundary redraws after every update.", { size: 13 });
    s.addNotes("This is the slide that ties the six definitions together. Step 1 uses the first four components; steps 2 to 4 use the last two. One trip around the loop is a training step; one pass over the whole training set is an epoch. Everything the Playground animates is this loop: the epoch counter counts laps, the loss curves record step 2, the thickening and thinning of connection lines is step 4, and the background colors redraw after each update as the boundary moves.");
  }

  // =====================================================================
  // Slide 11: experiment 1, depth
  // =====================================================================
  pres.addSection({ title: "Playground experiments" });
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Playground experiments" });
    s.addText("Experiment 1: depth and the shape of the boundary", { placeholder: "title" });
    const f = figure(s, "playground-grid.png", M, 1.4, 8.0, 4.6, "Decision boundaries on circle, XOR, Gaussian and spiral data: a linear model in the top row and a two-hidden-layer network in the bottom row, with test accuracies");
    caption(s, "Blue and orange shading is the network's output over the whole plane; dots are the test points.", M, f.bottom + 0.08, f.w);
    const cx = f.right + 0.35, cw = W - M - cx;
    column(s, cx, 1.4, cw, [
      { head: "Setup", h: 1.75, body: "The Playground's four datasets, recreated in Python (Pedregosa et al., 2011) so the boundaries print sharply. 400 points each, half for training and half for testing, no noise." },
      { head: "Result", h: 2.35, body: `No hidden layer draws one straight line: enough for the Gaussian blobs (${results["Gaussian:linear"]}%), useless for the circle (${results["Circle:linear"]}%) and XOR (${results["Exclusive or:linear"]}%). Two hidden layers of 8 solve circle and XOR and reach ${results["Spiral:deep"]}% on the spiral.` },
      { head: "Takeaway", h: BOTTOM - 1.4 - 1.75 - 2.35 - 0.32, body: "Depth buys the ability to bend the boundary. The spiral needed more.", opts: { fill: COMP.layers.tint } },
    ]);
    s.addNotes("In the Playground I ran each dataset with the hidden-layer count set to zero and then to two. To get boundaries sharp enough for a slide, I reproduced the Playground's four data generators in Python and trained the same small networks with scikit-learn; the behavior matches what the Playground shows. The top row is the limit of a linear model: one straight cut. The bottom row shows what two hidden layers of eight tanh neurons add. The spiral is the standard hard case and the only one that was not solved outright at this depth.");
  }

  // =====================================================================
  // Slide 12: experiments 2 and 3, activation and features
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Playground experiments" });
    s.addText("Experiments 2 and 3: activation functions and input features", { placeholder: "title" });
    const lh = 2.55;
    const lw = lh * SIZES["activation-experiment.png"][0] / SIZES["activation-experiment.png"][1];
    const rw = lh * SIZES["feature-experiment.png"][0] / SIZES["feature-experiment.png"][1];
    const gapX = CONTENT_W - lw - rw;
    const fl = figure(s, "activation-experiment.png", M, 1.4, lw, lh, "Spiral data with three hidden layers of eight under linear, tanh and ReLU activations, with test accuracies 55, 94 and 96 percent");
    const fr = figure(s, "feature-experiment.png", M + lw + gapX, 1.4, rw, lh, "Circle data separated by a linear model given squared features, and XOR data separated by a linear model given the product feature");
    caption(s, "Spiral data, three hidden layers of 8, only the activation changed", fl.x, fl.bottom + 0.06, fl.w);
    caption(s, "No hidden layer, extra input features added", fr.x, fr.bottom + 0.06, fr.w);
    const ty = fl.bottom + 0.5, th = BOTTOM - ty;
    const tw = (CONTENT_W - 0.2) / 2;
    textTile(s, M, ty, tw, th, "Activation: depth needs a bend",
      `With the architecture fixed and only the activation changed, spiral accuracy went from ${results["spiral-activation:identity"]}% (linear) to ${results["spiral-activation:tanh"]}% (tanh) and ${results["spiral-activation:relu"]}% (ReLU). Three layers with a linear activation have the same power as no hidden layer at all; the 55% here and the 59% on slide 11 differ only by the random split. ReLU's boundary is made of straight segments, which is what a piecewise-linear function produces.`);
    textTile(s, M + tw + 0.2, ty, tw, th, "Features: good inputs can replace layers",
      `The Playground lets you add x₁², x₂², x₁x₂, sin(x₁) and sin(x₂) as inputs. With x₁² and x₂² added, a model with no hidden layer separated the circle at ${results["circle:linear+squares"]}%; with x₁x₂ added, it solved XOR at ${results["xor:linear+product"]}%. The feature does the bending, so the network does not have to learn it.`);
    s.addNotes("Two experiments that make the role of the activation function concrete. On the left, the spiral with three hidden layers of eight: switching the activation to linear collapses the network to a straight-line classifier, exactly as the theory on slide 7 predicts, while tanh and ReLU both learn the spiral, with ReLU's characteristic straight-edged boundary. On the right, the Playground's feature checkboxes: adding squared or product features lets a model with no hidden layer solve the circle and XOR problems, because the nonlinearity now comes from the inputs. This is the same idea feature engineering has always used, and it is a useful reminder that layers are one way to get nonlinearity and features are another.");
  }

  // =====================================================================
  // Slide 13: experiments 4 and 5, noise and learning rate
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Playground experiments" });
    s.addText("Experiments 4 and 5: noise and the learning rate", { placeholder: "title" });
    const colw = (CONTENT_W - 0.4) / 2;
    const nz = results.noise;
    const rows = [
      [{ text: "Noise", options: { bold: true } }, { text: "Training loss", options: { bold: true } }, { text: "Test loss", options: { bold: true } }, { text: "Test accuracy", options: { bold: true } }],
      ...nz.map(r => [`${r.noise}%`, r.train_loss.toFixed(3), r.test_loss.toFixed(3), `${r.test_acc}%`]),
    ];
    s.addText("Noise slider: circle data, two hidden layers of 8, tanh", { x: M, y: 1.4, w: colw, h: 0.35, fontSize: 13, bold: true, color: C.text1, margin: 0, isTextBox: true });
    s.addTable(rows, {
      x: M, y: 1.85, w: colw, colW: [colw * 0.19, colw * 0.27, colw * 0.24, colw * 0.3],
      fontSize: 13, fontFace: "Arial", color: THEME.colors.dk1, fill: { color: THEME.colors.lt2 },
      border: { type: "solid", pt: 1.5, color: "FFFFFF" }, align: "left", valign: "middle", margin: [0.08, 0.14, 0.08, 0.14], rowH: 0.46,
    });
    textTile(s, M, 4.0, colw, BOTTOM - 4.0, "What noise did",
      `Raising the noise slider blurs the border between the classes. The network kept fitting its training points (training loss ${nz[2].train_loss}) while test loss climbed to ${nz[2].test_loss} and test accuracy fell to ${nz[2].test_acc}%: it was memorizing noise. The Playground's remedies are the ones used in practice: fewer neurons, more data, or the L1/L2 regularization dropdown.`);
    const rx = M + colw + 0.4;
    const f = figure(s, "learning-rate.png", rx, 1.4, colw, 3.1, "Training loss per epoch on circle data at learning rates 0.001, 0.1 and 10; only 0.1 converges", "center");
    const lr = results["learning-rate"];
    textTile(s, rx, f.bottom + 0.25, colw, BOTTOM - (f.bottom + 0.25), "What the learning rate did",
      `Same network, three learning rates. At 0.001 the loss barely moved in 200 epochs (${lr[0].test_acc}% test accuracy). At 0.1 it fell smoothly to near zero (${lr[1].test_acc}%). At 10 it bounced between about 3 and 9 and never settled (${lr[2].test_acc}%). The learning rate decides whether training works at all.`, { fill: COMP.optimizer.tint });
    s.addNotes("Two more Playground controls, tested the same way. Noise is the clearest demonstration of overfitting I know: the training loss stays low because the network has enough capacity to memorize the noisy points, while the test loss rises because that memorized detail does not transfer. The learning rate experiment reproduces the three behaviors from the optimizer slide on a real network. The Playground's learning-rate dropdown covers the same range, and the loss curves in its top-right corner show the same flat, falling and jumping patterns.");
  }

  // =====================================================================
  // Slide 14: summary (dark)
  // =====================================================================
  pres.addSection({ title: "Summary and references" });
  {
    const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Summary and references" });
    s.addText("Summary", { placeholder: "title" });
    const colw = (CONTENT_W - 0.4) / 2;
    const darkTile = "2C2C2E";
    const th = 5.1;
    tile(s, M, TOP, colw, th, { fill: darkTile, name: "why visualize tile" });
    tile(s, M + colw + 0.4, TOP, colw, th, { fill: darkTile, name: "insights tile" });
    s.addText("Why visualize a neural network", { x: M + 0.3, y: TOP + 0.25, w: colw - 0.6, h: 0.4, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    s.addText(bullets([
      "A diagram turns six abstract definitions into one picture: layers are columns, neurons are circles, weights are the lines between them, and activation, loss and optimizer are what happens as data crosses it.",
      "Watching the boundary and the loss curves change during training makes cause and effect visible. A change to depth, activation or learning rate shows up within seconds.",
      "Visuals are how these ideas reach teammates and stakeholders who will never read the equations, which is most of the people a model has to be explained to.",
    ], { color: C.background1 }), { x: M + 0.3, y: TOP + 0.8, w: colw - 0.6, h: th - 1.0, fontSize: 15, color: C.background1, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 12 });
    s.addText("Key insights from the exercise", { x: M + colw + 0.7, y: TOP + 0.25, w: colw - 0.6, h: 0.4, fontSize: 18, bold: true, color: C.accent4, margin: 0, isTextBox: true });
    s.addText(bullets([
      "No hidden layer means a straight line, however long you train.",
      "Depth only helps with a nonlinear activation. Tanh and ReLU both worked; linear did not.",
      "Weights and biases are the only things training changes. Everything else is a design decision made before training starts.",
      "Whether a model will generalize shows up as the gap between training loss and test loss, and noise widens that gap.",
      "Good input features can do the work of extra layers, and the learning rate decides whether training works at all.",
    ], { color: C.background1 }), { x: M + colw + 0.7, y: TOP + 0.8, w: colw - 0.6, h: th - 1.0, fontSize: 15, color: C.background1, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 9 });
    s.addNotes("Two things to take away. First, visualization is how I understood these components, and it is how I would explain them to anyone else: the architecture diagram is the definitions, and the Playground is the definitions in motion. Second, the experiments changed how I think about model design at work: capacity (depth and width) is cheap to add and easy to overuse, the activation and the learning rate are not details, and the only honest measure of a model is its behavior on data it has not seen.");
  }

  // =====================================================================
  // Slide 15: references
  // =====================================================================
  {
    const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Summary and references" });
    s.addText("References", { placeholder: "title" });
    const refs = [
      [{ text: "Cybenko, G. (1989). Approximation by superpositions of a sigmoidal function. " }, { text: "Mathematics of Control, Signals and Systems, 2", options: { italic: true } }, { text: "(4), 303–314. https://doi.org/10.1007/BF02551274" }],
      [{ text: "Goodfellow, I., Bengio, Y., & Courville, A. (2016). " }, { text: "Deep learning", options: { italic: true } }, { text: ". MIT Press. https://www.deeplearningbook.org/" }],
      [{ text: "Kingma, D. P., & Ba, J. (2015). Adam: A method for stochastic optimization. In " }, { text: "3rd International Conference on Learning Representations (ICLR 2015)", options: { italic: true } }, { text: ". https://doi.org/10.48550/arXiv.1412.6980" }],
      [{ text: "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. " }, { text: "Nature, 521", options: { italic: true } }, { text: "(7553), 436–444. https://doi.org/10.1038/nature14539" }],
      [{ text: "Nair, V., & Hinton, G. E. (2010). Rectified linear units improve restricted Boltzmann machines. In " }, { text: "Proceedings of the 27th International Conference on Machine Learning", options: { italic: true } }, { text: " (pp. 807–814). Omnipress." }],
      [{ text: "Nielsen, M. A. (2015). " }, { text: "Neural networks and deep learning", options: { italic: true } }, { text: ". Determination Press. http://neuralnetworksanddeeplearning.com/" }],
      [{ text: "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. " }, { text: "Journal of Machine Learning Research, 12", options: { italic: true } }, { text: ", 2825–2830." }],
      [{ text: "Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. " }, { text: "Nature, 323", options: { italic: true } }, { text: "(6088), 533–536. https://doi.org/10.1038/323533a0" }],
      [{ text: "Smilkov, D., & Carter, S. (2016). " }, { text: "A neural network playground", options: { italic: true } }, { text: " [Interactive web application]. TensorFlow. https://playground.tensorflow.org/" }],
    ];
    const paras = [];
    refs.forEach((runs, i) => {
      runs.forEach((r, j) => {
        const o = { ...(r.options || {}) };
        if (j === runs.length - 1 && i < refs.length - 1) o.breakLine = true;
        paras.push({ text: r.text, options: o });
      });
    });
    s.addText(paras, { x: M, y: 1.4, w: CONTENT_W, h: 4.9, fontSize: 13, color: C.text1, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 9 });
    s.addText("Figures and experiments: the Playground's four datasets were recreated in Python (NumPy, scikit-learn, Matplotlib) so that decision boundaries and loss curves could be rendered at print resolution. Explanations and code were drafted and reviewed with Claude (Anthropic).", { x: M, y: 6.35, w: CONTENT_W, h: 0.5, fontSize: 10.5, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    s.addNotes("References in APA style for the sources behind the definitions and the historical notes in the deck. Cybenko (1989) is the universal approximation result cited on the layers slide; Rumelhart, Hinton and Williams (1986) is backpropagation; Kingma and Ba (2015) is Adam; Nair and Hinton (2010) is ReLU. Goodfellow et al. and Nielsen are the two textbooks I used for the definitions.");
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
}

build().catch((e) => { console.error(e); process.exit(1); });
