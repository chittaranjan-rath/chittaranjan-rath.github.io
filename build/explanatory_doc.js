// Explanatory document for the LLM training infographic (APA student paper format).
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, HeadingLevel, PageBreak, Header, PageNumber } = require("docx");

const root = path.resolve(__dirname, "..");
const FONT = "Times New Roman";
const DOUBLE = { line: 480, before: 0, after: 0 };

// Inline italics are written as *text*
const runs = (text, extra = {}) => text.split(/(\*[^*]+\*)/).filter(Boolean).map((part) =>
  part.startsWith("*") ? new TextRun({ text: part.slice(1, -1), italics: true, ...extra }) : new TextRun({ text: part, ...extra }));
const body = (text) => new Paragraph({ children: runs(text), spacing: DOUBLE, indent: { firstLine: 720 } });
const centered = (text, bold = false) => new Paragraph({ children: [new TextRun({ text, bold })], alignment: AlignmentType.CENTER, spacing: DOUBLE });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text })], alignment: AlignmentType.CENTER });
const ref = (text) => new Paragraph({ children: runs(text), spacing: DOUBLE, indent: { left: 720, hanging: 720 } });
const blank = () => new Paragraph({ children: [], spacing: DOUBLE });

const TITLE = "What It Takes to Train a Large Language Model: Explanatory Document for the Training Process and Resource Cost Infographic";

const children = [
  blank(), blank(), blank(),
  centered(TITLE, true),
  blank(),
  centered("Chittaranjan Rath"),
  centered("Indiana Wesleyan University"),
  centered("AIML-501-01R3I: Model Development (3FA2026)"),
  centered("Professor John Wishart"),
  centered("November 14, 2026"),
  new Paragraph({ children: [new PageBreak()] }),

  centered(TITLE, true),
  body("This document accompanies my infographic on how generative AI large language models are trained and what that training consumes. The infographic is published as an artifact in my professional portfolio at https://chittaranjan-rath.github.io/artifacts/llm-training-costs.html, where it can be viewed as a web page or downloaded as a PNG or PDF. Figure 1 shows its opening section. The sections below summarize the main points, describe the considerations that shaped the content, explain the design choices and the way I classified the material, and close with a reflection on what I learned."),

  new Paragraph({ children: [new TextRun({ text: "Figure 1", bold: true })], spacing: DOUBLE }),
  new Paragraph({ children: [new TextRun({ text: "Opening Section of the Infographic", italics: true })], spacing: DOUBLE }),
  new Paragraph({ children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(root, "assets", "img", "llm-training-costs-thumb.png")), transformation: { width: 468, height: 351 }, altText: { title: "Infographic opening section", description: "Four resource tiles for data, compute, energy and time on a dark band, above the start of the pipeline drawn to scale", name: "figure1" } })], spacing: { before: 0, after: 120 } }),
  new Paragraph({ children: runs("*Note.* The full infographic continues with the rest of the scale diagram, the pretraining loop, growth charts, cost charts, and a disclosure chart of seven models."), spacing: DOUBLE }),

  h1("Summary of Main Points"),
  body("The infographic makes three points. The first is that training follows a pipeline of seven steps: collecting data, cleaning and curating it, tokenizing it, pretraining the model, fine-tuning and aligning it, evaluating it, and deploying it. Pretraining is the step where the model learns by predicting the next token in a passage and adjusting its weights after every guess. Wolfram (2023) describes this loop in detail and notes that the network behind ChatGPT had about 175 billion weights fitted to a few hundred billion words of text."),
  body("The second point is that four resources pay for the pipeline, and they grow together. GPT-3 was trained on 300 billion tokens (Brown et al., 2020) and used an estimated 1,287 megawatt-hours of electricity, which produced about 552 metric tons of carbon dioxide equivalent (Patterson et al., 2021). Four years later, Llama 3.1 405B was trained on more than 15 trillion tokens using more than 16,000 Nvidia H100 GPUs for 30.84 million GPU-hours (Meta, 2024a, 2024b). Multiplying those GPU-hours by the 700 watts Meta reports per GPU gives roughly 21,600 megawatt-hours, about 17 times the GPT-3 figure."),
  body("The third point is that the cost has moved out of reach for most organizations. The Stanford AI Index estimates the compute for the original Transformer in 2017 at about $930, for GPT-4 at $78 million, and for Gemini Ultra at $191 million (Maslej et al., 2024). Cottier et al. (2024) found that the cost of the largest training runs has grown about 2.4 times per year since 2016. Within the hardware bill, AI accelerator chips account for about 44%, other server components 29%, cluster networking 17%, and energy 9%."),

  h1("Key Considerations"),
  body("The main consideration was evidence. Numbers about AI training circulate widely with no source attached, so I limited the infographic to figures I could trace to a paper, a model card, or a named independent study. I labeled each one as published by the developer, estimated by a third party, or calculated by me from published numbers. Several popular claims about the size and hardware of GPT-4 did not meet that standard, and I left them out. The disclosure chart therefore shows many squares as empty. I kept those empty squares on purpose, because the lack of disclosure from OpenAI, Google, and Anthropic is itself something a reader should know. For Claude, the only figure I could source was a public remark by the chief executive of Anthropic that models in service in 2024 cost around $100 million to train and that runs near $1 billion were under way (Morales, 2024)."),
  body("A second consideration was that cost estimates depend on method. GPT-4 comes out at $78 million when priced at cloud rental rates and at $40 million when priced as owned hardware plus energy (Cottier et al., 2024; Maslej et al., 2024). I show both and say which is which. A third consideration was audience. The assignment asks for a graphic that works for varied readers, so I wrote the step descriptions in plain language, explained the logarithmic scale in one sentence next to the chart, and added a familiar comparison where one existed, such as GPT-3's training energy being about what 120 American homes use in a year (Saul & Bass, 2023)."),

  h1("Design Rationale"),
  body("I chose an infographic over a slide deck because the content is a single connected argument that benefits from being seen on one page: steps, then resources, then the numbers that link them. The page reads from general to specific. It opens with four large numbers, one per resource, each paired with an everyday comparison such as 2,000 homes for a year, so a reader who stops after ten seconds still leaves with the scale. The centerpiece comes next. I drew the pipeline as a band whose thickness shows resource demand, because my first version used seven cards of equal size and that layout implied the steps were equal while the text said otherwise. In the band, the swelling at pretraining makes the point without a caption. I also replaced a text-heavy comparison table with a chart of filled, striped, and empty squares, since the pattern of who discloses what is easier to see than to read. The later sections add depth for readers who want it, and on the web version a switch lets the viewer compare three models directly."),
  body("Color carries one meaning throughout. Blue is data, purple is compute, orange is energy, and green is time. Each color always appears with an icon and a word, so the meaning survives for a reader with a color vision deficiency or a grayscale printout. I tested the four colors with a palette validator on both the light and the dark background and replaced my first choice of blue after it proved too close to the purple under simulated deuteranopia. Each chart shows one resource, and I avoided dual axes. The cost chart uses a logarithmic scale because the values span from $930 to $191 million, and a linear scale would have flattened every point but the last two. The typography, spacing, and rounded tiles match the rest of my portfolio, while the dark opening band gives this artifact a look of its own."),

  h1("Classification Process"),
  body("I sorted the content along two dimensions. The first was sequence. I grouped the seven steps into four phases: prepare, train, refine, and release. The first three steps all act on text before a model exists, so they belong together. Fine-tuning and evaluation both act on a working model and feed back into each other, so they form the refine phase. I kept pretraining as a phase by itself, because it consumes nearly all of the compute, energy, and time, and merging it with other steps would have hidden that."),
  body("The second dimension was cost. I started with the four resources named in the assignment and added a fifth, people, after reading that research staff make up 29% to 49% of the full development cost of a frontier model (Cottier et al., 2024). People appear in grey so the four assigned resources remain the focus. Time was the hardest category to separate, since a GPU-hour measures compute and time at once. I treated GPU-hours as the shared unit and used wall-clock days wherever a source reported them, such as the 21 days Meta needed to train LLaMA 65B on 2,048 GPUs (Touvron, Lavril, et al., 2023)."),
  body("Crossing the two dimensions produced the scale diagram in the infographic, where the thickness of each colored layer shows how heavily each step draws on each resource. Those thicknesses are my own judgment on a relative scale, and the caption says so, because no lab publishes a breakdown by step. The classification revealed a pattern I had not expected to be so sharp. Cost is concentrated in one step out of seven, and the resources are coupled: across three generations of Meta's model, training data grew about 11 times while GPU-hours grew about 30 times (Meta, 2024b; Touvron, Lavril, et al., 2023; Touvron, Martin, et al., 2023)."),

  h1("Reflection on Learning"),
  body("Before this assignment I thought of training cost mainly as a hardware number. Working through the sources changed that. I learned that energy is a small share of the dollar cost, between 2% and 6% of development spending (Cottier et al., 2024), while being the entire source of the carbon footprint, and that the footprint depends heavily on where the data center gets its power. Meta reports 8,930 metric tons of location-based emissions for Llama 3.1 405B and zero after matching with renewable energy (Meta, 2024b). Both numbers are correct, and choosing which to show is a communication decision as much as a technical one."),
  body("The biggest challenge was the uneven quality of information. My strategy was to work only from primary sources and to label my own arithmetic. That approach has a limitation that I want to be clear about. My energy figures for the LLaMA models multiply GPU-hours by rated power, which leaves out cooling and other overhead for the earlier models, and the layer thicknesses in my scale diagram are qualitative. A second challenge was deciding what to leave out. An earlier outline had a section on inference cost, which I cut because the assignment is about training. My first complete version also carried a band of resource cards that repeated numbers shown elsewhere, and removing it made the page shorter and the main diagram more prominent."),
  body("The work connects to the course in two ways. The pretraining loop in the infographic is the same forward pass, loss, and weight update that I illustrated at small scale in my neural network presentation for the previous portfolio artifact, repeated here across hundreds of billions of weights. The IBM Technology (2023) video frames a large language model as data, architecture, and training, and this assignment showed me how much of the practical difficulty sits in the third of those. The broader application is to my own work on retrieval-augmented generation. Seeing these numbers side by side made it concrete why almost every team should build on an existing model and spend its effort on data quality, retrieval, and evaluation."),

  new Paragraph({ children: [new PageBreak()] }),
  centered("References", true),
  ...JSON.parse(fs.readFileSync(path.join(__dirname, "llm_training_refs.json"), "utf8"))
    .map((r) => ref(r.replace(/<em>(.*?)<\/em>/g, "*$1*").replace(/&amp;/g, "&"))),
];

const doc = new Document({
  creator: "Chittaranjan Rath",
  title: "What It Takes to Train a Large Language Model: Explanatory Document",
  styles: {
    default: {
      document: { run: { font: FONT, size: 24 } },
      heading1: { run: { font: FONT, size: 24, bold: true, color: "000000" }, paragraph: { spacing: { line: 480, before: 0, after: 0 }, keepNext: true } },
    },
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT] })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(root, "assets", "downloads", "Rath_AIML501_LLM_Training_Explanatory_Document.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", path.relative(root, out));
});
