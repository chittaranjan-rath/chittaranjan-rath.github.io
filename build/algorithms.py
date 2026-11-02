"""Algorithm data for the ML algorithm framework infographic.

Each entry follows the schema the assignment asks for:
  name, family (band), kind (Supervised/Unsupervised), kind_note,
  domains (subset of tabular/vision/language/generative),
  how (brief explanation of how it works), uses (real-world use cases).
"""

DOMAINS = [
    ("tabular", "Tabular data"),
    ("vision", "Computer vision"),
    ("language", "Natural language"),
    ("generative", "Generative AI"),
]

BANDS = [
    ("classical-supervised", "Classical supervised learning",
     "Learns from examples that already carry the right answer. The output is a number (regression) or a category (classification)."),
    ("classical-unsupervised", "Classical unsupervised learning",
     "Works on unlabeled data and finds structure in it: groups, directions of variation, outliers."),
    ("deep", "Deep learning",
     "Neural networks with many layers that learn their own features from raw pixels, tokens, or audio. These power computer vision, language models, and generative AI."),
]

ALGORITHMS = [
    # ---------- Classical supervised ----------
    dict(
        name="Linear regression", fig="linreg", year=1805, origin="Legendre, least squares",
        short="Fits the straight line that minimizes the squared gap to every point.",
        tags=["Price forecasting", "Delivery time estimates", "Demand projection"], task="Regression", band="classical-supervised", kind="Supervised",
        domains=["tabular"],
        how="Fits a straight line (or a flat plane in many dimensions) through the training points by choosing the weight for each feature that minimizes the squared gap between predicted and actual values.",
        uses="Forecasting house prices from size and location, estimating delivery time from distance and load, projecting monthly demand.",
    ),
    dict(
        name="Logistic regression", fig="logreg", year=1958, origin="Cox",
        short="Squashes a weighted sum through an S-curve to get a probability, then thresholds it.",
        tags=["Credit scoring", "Spam filtering", "Churn prediction"], task="Classification", band="classical-supervised", kind="Supervised",
        domains=["tabular", "language"],
        how="Takes a weighted sum of the features and squashes it through an S-shaped curve so the result is a probability between 0 and 1, then applies a threshold to assign a class.",
        uses="Credit default and loan approval scoring, spam filtering, customer churn prediction, baseline sentiment classifiers on bag-of-words text.",
    ),
    dict(
        name="Naive Bayes", fig="bayes", year=1961, origin="Maron",
        short="Multiplies how likely each feature is under each class and picks the most probable class.",
        tags=["Spam and phishing filters", "Email routing", "Sentiment baselines"], task="Classification", band="classical-supervised", kind="Supervised",
        domains=["language", "tabular"],
        how="Applies Bayes' theorem while assuming each feature is independent of the others given the class: it multiplies how likely each feature value is under each class and picks the class with the highest combined probability.",
        uses="Spam and phishing filters, routing support emails by topic, quick sentiment baselines, symptom-based triage where features are counts or yes-or-no flags.",
    ),
    dict(
        name="Decision tree", fig="tree", year=1984, origin="Breiman et al., CART",
        short="Asks yes-or-no questions one feature at a time, each chosen to make the groups purest.",
        tags=["Readable loan rules", "Medical triage", "Produce sorting"], task="Classification, regression", band="classical-supervised", kind="Supervised",
        domains=["tabular"],
        how="Asks a sequence of yes-or-no questions about one feature at a time, choosing each question so the resulting groups are as pure as possible (Gini impurity or entropy), until each leaf holds mostly one class.",
        uses="Loan approval rules that a reviewer can read, medical triage checklists, sorting produce by measured size, color, and shape.",
    ),
    dict(
        name="Random forest", fig="forest", year=2001, origin="Breiman",
        short="Hundreds of trees grown on random samples of rows and features vote on the answer.",
        tags=["Fraud detection", "Churn prediction", "Feature importance"], task="Classification, regression", band="classical-supervised", kind="Supervised",
        domains=["tabular"],
        how="Trains hundreds of decision trees, each on a random sample of rows and a random subset of features, and lets them vote. Averaging many imperfect trees cancels out the overfitting of any single one.",
        uses="Fraud detection on transaction records, churn prediction, ranking which features matter most in a dataset.",
    ),
    dict(
        name="Gradient boosting (XGBoost, LightGBM)", fig="boost", year=2001, origin="Friedman; XGBoost 2016",
        short="Small trees built in sequence, each one fitted to the errors the earlier ones left.",
        tags=["Click prediction", "Risk pricing", "Tabular competitions"], task="Classification, regression", band="classical-supervised", kind="Supervised",
        domains=["tabular"],
        how="Builds small trees one after another; each new tree is fitted to the errors the ensemble is still making, so the model improves in the direction of steepest error reduction.",
        uses="Click-through and conversion prediction, insurance risk pricing, the most common winner of tabular data competitions.",
    ),
    dict(
        name="Support vector machine", fig="svm", year=1995, origin="Cortes and Vapnik",
        short="Finds the boundary with the widest margin between classes; kernels let it curve.",
        tags=["Text categorization", "Digit recognition", "Bioinformatics"], task="Classification", band="classical-supervised", kind="Supervised",
        domains=["tabular", "language"],
        how="Finds the boundary between classes that leaves the widest possible margin to the nearest training points. Kernel functions let the same idea draw curved boundaries.",
        uses="Text categorization with TF-IDF features, handwritten digit recognition, protein classification in bioinformatics.",
    ),
    dict(
        name="K-nearest neighbors", fig="knn", year=1967, origin="Cover and Hart",
        short="Finds the k closest stored examples and takes their majority label.",
        tags=["Similar-item recommendations", "Anomaly detection", "Small image baselines"], task="Classification, regression", band="classical-supervised", kind="Supervised",
        domains=["tabular", "vision"],
        how="Keeps the whole training set. To classify a new item it measures the distance to every stored item, takes the k closest, and returns their majority label (or their average for regression).",
        uses="Similar-item recommendations, anomaly detection in sensor readings, quick baselines for small image datasets.",
    ),
    # ---------- Classical unsupervised ----------
    dict(
        name="K-means clustering", fig="kmeans", year=1957, origin="Lloyd; MacQueen 1967",
        short="Assigns points to the nearest of k centers, moves each center to the mean, repeats.",
        tags=["Customer segmentation", "Color quantization", "Ticket grouping"], task="Clustering", band="classical-unsupervised", kind="Unsupervised",
        domains=["tabular", "vision"],
        how="Places k center points, assigns every item to its nearest center, moves each center to the average of its members, and repeats until the assignments stop changing.",
        uses="Customer segmentation for marketing, reducing an image to a palette of k colors, grouping similar support tickets or documents.",
    ),
    dict(
        name="Principal component analysis", fig="pca", year=1901, origin="Pearson",
        short="Projects the data onto the few directions along which it varies most.",
        tags=["Feature compression", "2D visualization", "Noise reduction"], task="Dimensionality reduction", band="classical-unsupervised", kind="Unsupervised",
        domains=["tabular", "vision"],
        how="Finds the directions along which the data varies the most and projects every item onto the top few, so dozens of correlated features collapse into a handful of uncorrelated ones.",
        uses="Compressing features before training another model, plotting high-dimensional data in two dimensions, removing noise from measurements, the classic eigenfaces approach to face recognition.",
    ),
    dict(
        name="Hierarchical clustering", fig="hier", year=1963, origin="Ward",
        short="Merges the two closest clusters again and again, building a tree you can cut at any height.",
        tags=["Customer taxonomies", "Gene expression groups", "Nested topics"], task="Clustering", band="classical-unsupervised", kind="Unsupervised",
        domains=["tabular"],
        how="Starts with every item as its own cluster and repeatedly merges the two closest clusters. The result is a tree (dendrogram) that can be cut at any height to get as many groups as wanted.",
        uses="Building a customer or product taxonomy, grouping genes by expression pattern, organizing a document collection into nested topics.",
    ),
    dict(
        name="DBSCAN", fig="dbscan", year=1996, origin="Ester et al.",
        short="Grows clusters out of dense regions and leaves sparse points as noise.",
        tags=["Transaction anomalies", "Geographic hotspots", "Unknown cluster counts"], task="Clustering, anomaly detection", band="classical-unsupervised", kind="Unsupervised",
        domains=["tabular"],
        how="Grows clusters out of dense regions: any point with enough neighbors within a set radius becomes a core point, its neighbors join the cluster, and points in sparse regions are left unassigned as noise.",
        uses="Flagging anomalous transactions, finding geographic hotspots in GPS or delivery data, clustering without having to choose the number of groups in advance.",
    ),
    # ---------- Deep learning ----------
    dict(
        name="Convolutional neural network", fig="cnn", year=1998, origin="LeCun et al., LeNet-5",
        short="Slides learned filters across the image, building edges into textures into objects.",
        tags=["Image classification", "Object detection", "Medical imaging"], task="Classification, detection", band="deep", kind="Supervised",
        domains=["vision"],
        how="Slides small learned filters across the image. Early layers respond to edges and colors, middle layers to textures and parts, and late layers to whole objects, so the network builds its own visual features.",
        uses="Image classification, object detection for self-driving perception, tumor detection in medical scans, defect inspection on production lines.",
    ),
    dict(
        name="Transformer (BERT, GPT)", fig="transformer", year=2017, origin="Vaswani et al.",
        short="Attention lets every token weigh every other token, in parallel, to predict what comes next.",
        tags=["Chat assistants", "Translation and search", "RAG question answering"], task="Language modeling, generation", band="deep", kind="Unsupervised",
        kind_note="self-supervised pretraining, then supervised fine-tuning",
        domains=["language", "generative", "vision"],
        how="Turns each token into a vector and uses attention so every token can weigh how relevant every other token is, all in parallel. Stacking these layers lets the model represent meaning across a whole passage and predict what comes next.",
        uses="Chat assistants and code generation (GPT family), search and sentiment analysis (BERT), translation and summarization, retrieval-augmented question answering over company documents, image recognition with vision transformers.",
    ),
    dict(
        name="Generative adversarial network", fig="gan", year=2014, origin="Goodfellow et al.",
        short="A generator forges samples, a discriminator calls them out, and both improve until the fakes pass.",
        tags=["Face synthesis", "Sketch to photo", "Data augmentation"], task="Generation", band="deep", kind="Unsupervised",
        domains=["generative", "vision"],
        how="Two networks train against each other. The generator makes fake samples from random noise; the discriminator learns to tell fakes from real data. Each round the generator gets harder to catch, until its samples look real.",
        uses="Photorealistic face and product image synthesis, image-to-image translation (sketch to photo), super-resolution, generating extra training data for rare classes.",
    ),
    dict(
        name="Diffusion model (Stable Diffusion, DALL-E)", fig="diffusion", year=2020, origin="Ho et al., DDPM",
        short="Learns to remove noise step by step, so it can turn pure noise into a new image guided by a prompt.",
        tags=["Text-to-image", "Inpainting", "Video and audio generation"], task="Generation", band="deep", kind="Unsupervised",
        kind_note="self-supervised",
        domains=["generative", "vision"],
        how="Learns to undo a process that gradually turns an image into random noise. To generate, it starts from pure noise and removes a little noise at each step, steered by a text prompt, until a new image appears.",
        uses="Text-to-image generation, filling in or extending parts of an image, video and audio generation, concept art and product mock-ups.",
    ),
]

CONNECTIONS = [
    dict(
        title="Trees grow into ensembles",
        chain=["Decision tree", "Random forest", "Gradient boosting"],
        note="A single tree is easy to read but overfits. A random forest averages hundreds of trees grown on random samples; gradient boosting grows them in sequence, each one correcting the errors of the last. Accuracy rises at each step and interpretability falls.",
    ),
    dict(
        title="From a line to a network",
        chain=["Linear regression", "Logistic regression", "Neural network", "CNN and Transformer"],
        note="Logistic regression is linear regression with an S-shaped curve on the output. A neural network stacks many such units in layers. Convolutional networks and transformers are neural networks with structure added for images and sequences.",
    ),
    dict(
        title="Same distance, different question",
        chain=["K-nearest neighbors", "K-means"],
        note="Both measure distance between points, so both need scaled features. K-nearest neighbors uses the labels of nearby points (supervised); K-means has no labels and discovers the groups itself (unsupervised).",
    ),
    dict(
        title="Attention replaced recurrence",
        chain=["Recurrent network (LSTM)", "Transformer", "BERT, GPT, vision transformer"],
        note="Recurrent networks read text one token at a time and struggled with long passages. The transformer reads the whole sequence at once through attention, which made large language models possible and then carried over to images.",
    ),
    dict(
        title="Two roads to generation",
        chain=["GAN", "Diffusion model"],
        note="A GAN learns through a contest between two networks: fast to sample from, hard to train stably. A diffusion model learns to reverse added noise: slower to sample, stable to train, higher quality. Diffusion has largely replaced GANs for image generation since 2022.",
    ),
]

MAP_ORDER = [
    "Linear regression", "Decision tree", "Random forest", "Gradient boosting (XGBoost, LightGBM)",
    "Hierarchical clustering", "DBSCAN", "Logistic regression", "Naive Bayes", "Support vector machine",
    "K-nearest neighbors", "K-means clustering", "Principal component analysis",
    "Convolutional neural network", "Generative adversarial network",
    "Diffusion model (Stable Diffusion, DALL-E)", "Transformer (BERT, GPT)",
]

# Short display names for tight spaces (map stations, timeline, chain nodes)
SHORT_NAME = {
    "Gradient boosting (XGBoost, LightGBM)": "Gradient boosting",
    "Principal component analysis": "PCA",
    "Convolutional neural network": "CNN",
    "Transformer (BERT, GPT)": "Transformer",
    "Generative adversarial network": "GAN",
    "Diffusion model (Stable Diffusion, DALL-E)": "Diffusion model",
    "Support vector machine": "SVM",
    "K-nearest neighbors": "K-nearest neighbors",
}
