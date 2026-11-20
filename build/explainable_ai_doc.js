// Explanatory document for the explainable AI infographic (APA student paper format).
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

const TITLE = "Why Did the Model Say That? Explanatory Document for the Explainable AI, Validation, and Metrics Infographic";

const children = [
  blank(), blank(), blank(),
  centered(TITLE, true),
  blank(),
  centered("Chittaranjan Rath"),
  centered("Indiana Wesleyan University"),
  centered("AIML-501-01R3I: Model Development (3FA2026)"),
  centered("Professor John Wishart"),
  centered("November 20, 2026"),
  new Paragraph({ children: [new PageBreak()] }),

  centered(TITLE, true),
  body("This document accompanies my infographic on explainable AI for large language models. The infographic is published as an artifact in my professional portfolio at https://chittaranjan-rath.github.io/artifacts/explainable-ai.html, where it can be viewed as a web page or downloaded as a PNG or PDF. Figure 1 shows its opening section. The sections below summarize the main points, explain the design choices, describe how I classified the material, and reflect on what I learned."),

  new Paragraph({ children: [new TextRun({ text: "Figure 1", bold: true })], spacing: DOUBLE, keepNext: true }),
  new Paragraph({ children: [new TextRun({ text: "Opening Section of the Infographic", italics: true })], spacing: DOUBLE, keepNext: true }),
  new Paragraph({ children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(root, "assets", "img", "explainable-ai-thumb.png")), transformation: { width: 468, height: 351 }, altText: { title: "Infographic opening section", description: "A row relating explainability, validation and metrics to trust, above two large panels comparing what a model said with what it did", name: "figure1" } })], spacing: { before: 0, after: 120 }, keepNext: true }),
  new Paragraph({ children: runs("*Note.* The full infographic continues with definitions, five obstacles, three ways of looking at a model, a timeline of work by four labs, the validation cycle, seven evaluation metrics, and transparency scores."), spacing: DOUBLE }),

  h1("Summary of Main Points"),
  body("The infographic makes one argument: an explanation from a large language model is a claim, and validation and performance metrics supply the evidence for it. Explainable AI is the work of making a model's outputs and decisions understandable to people, and the National Institute of Standards and Technology (NIST, 2023) separates it into transparency (what happened), explainability (how the decision was made), and interpretability (what the output means to the person using it). The infographic shows why this is hard for models such as GPT, Claude, Gemini, and Llama. GPT-3 spreads its behavior across 175 billion weights (Brown et al., 2020), single neurons respond to several unrelated things (Bills et al., 2023), and the explanation a model writes can differ from what it did. Anthropic (2025a) found that Claude added 36 and 59 with two parallel internal paths and then described the carry-the-one method from school, and Chen et al. (2025) found that Claude 3.7 Sonnet mentioned a hint that had changed its answer 25% of the time. Regulation adds pressure, since the EU AI Act and US credit rules require explanations in high-risk settings (Consumer Financial Protection Bureau, 2023; Regulation 2024/1689, 2024)."),
  body("The industry response falls into three approaches that I drew on one diagram: asking the model to show its reasoning, testing it from outside with attribution tools such as Meta's Captum (Miglani et al., 2023), and looking inside with the feature and circuit methods from Anthropic, OpenAI, and Google DeepMind (Anthropic, 2024; Lieberum et al., 2024; OpenAI, 2024). Each approach has limits its own authors report, so validation and metrics carry the rest of the load. Validation means confirming with objective evidence that a system meets the requirements of its intended use (NIST, 2023), and US bank regulators describe it as three recurring checks on design, outcomes, and ongoing performance (Board of Governors of the Federal Reserve System et al., 2026). Metrics turn those checks into numbers. The HELM benchmark measures accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency, and it raised the share of core scenarios on which 30 models had been tested from 17.9% to 96.0% (Liang et al., 2023). Explainability tells a user how an answer was produced, validation shows that the model does its job, and metrics show how well. Together they give an organization a basis for trust that it can defend to a customer or a regulator."),

  h1("Design Rationale"),
  body("The design choices follow from the audience, which is a non-technical reader deciding whether to rely on a model. I chose an infographic over a slide deck because the content is one connected argument that reads best on a single page. A row directly under the title states the relationship between explainability, validation, metrics, and trust, so the reader has the conclusion before the detail. The addition example fills the rest of the opening, because explainability is abstract and a reader can follow a sum without any background. I placed what the model said next to what it did, at a size that makes it the one image a viewer remembers, so that the gap is visible before any definition appears."),
  body("My first complete version was accurate but read like a report below the opening, with rows of text cards, so I rebuilt it around drawings. The three NIST terms became one picture of a question passing through a model to a person, with each term pointing at the part it concerns. The three technique cards became labels on the model diagram itself. The seven metrics became a seven-sided report card. Its scores are invented and labeled as an illustration, and I accepted that because the shape shows something a list cannot: a model can be strong on accuracy and weak on calibration at once. A small box beside each heading starts solid and opens a little further in every band, which ties the sections into one story about opening the black box. Four colors carry one meaning each across the whole page, with orange for asking, blue for testing from outside, purple for looking inside, and green for validation and metrics. Every color is paired with an icon and a word, so the meaning survives for a reader with a color vision deficiency or a grayscale printout. The work of Anthropic, OpenAI, Google, and Meta sits on a timeline with one lane per company, which shows at a glance that most published effort goes into looking inside the model. Every figure is tied to a named source, and I labeled the two transparency scores I calculated."),

  h1("Classification Process"),
  body("I sorted the material in two ways. The first sort was by where a technique looks. The research names (chain-of-thought, attribution, probing, sparse autoencoders, circuits) mean little to a non-technical reader, while the position of the observer is easy to picture. Asking the model covers chain-of-thought prompting and the reasoning summaries built into products. Testing from outside covers methods that change the input and watch the output, including the attribution scores Captum produces (Miglani et al., 2023). Looking inside covers attention maps, probing, features, and circuits. I first considered sorting by company, and I rejected it because the four labs work on overlapping methods and a company grouping would have repeated the same technique four times. The lab timeline keeps the company view as a second layer, with each dot colored by the way of looking."),
  body("Attention visualization was the hardest item to place. The assignment notes present it as a current tool, and my first version left it out because the lab work I could source has moved to features and circuits. I put it back inside the look-inside group with its main limit, which is that attention weights are frequently uncorrelated with other measures of which inputs mattered (Jain & Wallace, 2019). It belongs there because it reads the model's internal state, and the limit explains why the labs moved on."),
  body("The second sort separated explaining from checking. Explainability asks how an answer was made. Validation asks whether there is evidence the model does its job, and metrics express that evidence as numbers. I kept these apart because the sources show they can disagree: a model can give a correct answer with an explanation that does not describe what it did (Anthropic, 2025a). Two rules governed individual items. A piece of lab work went on the timeline only if it had a date and a public source from the lab or a peer-reviewed venue, and each way of looking had to carry a limit reported in the sources, such as OpenAI's note that passing GPT-4 through its 16 million features costs about as much performance as training with ten times less compute (OpenAI, 2024). Sorting the content this way showed a pattern I had not expected. Most published effort goes into looking inside, which is the least complete of the three approaches, while the easiest approach, asking the model, is the one with measured evidence of unreliability."),

  h1("Reflection on Learning"),
  body("Before this assignment I treated a model's step-by-step reasoning as a reasonable account of what it had done. The sources changed that. Turpin et al. (2023) showed that biasing a prompt could cut accuracy by up to 36% on 13 reasoning tasks while the written explanations left the bias out, and Chen et al. (2025) measured the same gap in models built to reason aloud. I now read a model's explanation as a second output that needs its own check, which is a more useful habit than either trusting it or dismissing it."),
  body("The main challenge was that the subject is moving. Two facts I started with were out of date. The EU had moved its high-risk requirements from August 2026 to December 2027 (Goodwin Procter, 2026), and US bank regulators had replaced their 2011 model risk guidance in April 2026 with a version that leaves generative AI out of scope (Board of Governors of the Federal Reserve System et al., 2026). My strategy was to confirm every date and figure against a primary source before drawing it and to keep all of them in one data file, so that a correction updates the whole page. A second challenge was abstraction. My early outline opened with definitions, and it read like a glossary. Opening with one worked case made the problem concrete, and the definitions then had something to attach to."),
  body("The work has limits that I want to state. The lab timeline is a selection of dated public work and does not measure how much each company has done. The 25% figure comes from one study of two models under one kind of test. The transparency index changed its indicators in 2025, so part of the fall in scores reflects a stricter test (Wan et al., 2025). The work connects to the course in two ways. The weights and activations I drew in my neural network presentation are the same units these interpretability methods try to read, and the scale I charted in my infographic on training costs is the reason no single weight explains an answer. The broader application is to my own work on retrieval-augmented generation in financial services. I would use this reasoning to explain to a risk team why a model's stated reasoning cannot stand alone, and the three validation checks and seven metrics give me the outline of the evidence that should accompany it."),

  new Paragraph({ children: [new PageBreak()] }),
  centered("References", true),
];

// Only the sources cited in this document, in the order of the shared reference list.
const cited = ["Anthropic. (2024", "Anthropic. (2025a", "Bills,", "Board of Governors", "Brown,", "Chen,", "Consumer Financial", "Goodwin", "Jain,", "Liang,", "Lieberum,", "Miglani,", "National Institute", "OpenAI. (2024", "Regulation (EU)", "Turpin,", "Wan,"];
const all = JSON.parse(fs.readFileSync(path.join(__dirname, "explainable_ai_refs.json"), "utf8"));
for (const key of cited) {
  const r = all.find((x) => x.startsWith(key));
  if (!r) throw new Error("missing reference: " + key);
  children.push(ref(r.replace(/<em>(.*?)<\/em>/g, "*$1*").replace(/&amp;/g, "&")));
}

const doc = new Document({
  creator: "Chittaranjan Rath",
  title: "Why Did the Model Say That? Explanatory Document",
  styles: { default: { document: { run: { font: FONT, size: 24 } }, heading1: { run: { font: FONT, size: 24, bold: true, color: "000000" }, paragraph: { spacing: { line: 480, before: 0, after: 0 }, keepNext: true } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT] })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(root, "assets", "downloads", "Rath_AIML501_Explainable_AI_Explanatory_Document.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", path.relative(root, out));
});
