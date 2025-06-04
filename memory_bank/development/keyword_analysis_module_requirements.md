
# Keyword Analysis Module Technical Specification

**Project Title:** Research Analytics Application for "Agentic AI in SCM" SLR

**1. Introduction and Purpose**
The primary purpose of this Python application is to automate and support the quantitative analysis of research trends as described in Section 2.2 of the SLR document "Agentic AI in SCM (Ilin, May 2025) ver. 0.7.docx". The application will facilitate the collection, processing, analysis, and visualization of publication metadata to identify and illustrate shifts in research focus concerning LLM-powered and agentic AI in Supply Chain Management (SCM) and Logistics. The outputs will directly populate Section 3.1.1 of the SLR.

**2. Scope of Work**
The application will perform the following key functions:

*   **Data Acquisition:** Programmatically fetch publication metadata from specified academic APIs.
*   **Data Processing & Structuring:** Clean, standardize, and structure the collected metadata.
*   **Keyword Analysis:** Identify, extract, and analyze the frequency and temporal distribution of keywords.
*   **Semantic Analysis:** Generate embeddings for abstracts and perform clustering to identify thematic groups.
*   **Visualization & Reporting:** Generate visual outputs (graphs, charts) and data summaries to illustrate research trends and thematic evolution.

**3. User Roles**
*   **Researcher (PhD Student):** The primary user who will configure, run, and interpret the outputs of the application.

**4. Functional Requirements**

    **4.1. Data Acquisition Module**
        4.1.1.  Support for multiple academic APIs:
                a.  arXiv API
                b.  CORE API (core.ac.uk)
                c.  OpenAlex API (openalex.org)
        4.1.2.  Configurable search queries:
                a.  Allow input of natural language phrases and domain-specific keywords (e.g., "Supply Chain Management," "AI," "Agent," "LLM," "Logistics," specific frameworks like "LangGraph").
                b.  Boolean operators for query construction (AND, OR, NOT).
                c.  Configurable timeframe for search (e.g., default 2020-2025, with flexibility to extend as per footnote [a], potentially back to 1980s for broader historical context on "agents in SCM" vs. "LLM agents in SCM").
        4.1.3.  Metadata extraction: Retrieve titles, authors, abstracts, keywords (if provided by API), and publication dates.
        4.1.4.  Data persistence: Store raw fetched data (e.g., JSON, CSV) to avoid re-fetching.
        4.1.5.  Handle API rate limits and pagination gracefully.

    **4.2. Data Preprocessing & Structuring Module**
        4.2.1.  Standardize metadata format across different API sources.
        4.2.2.  Consolidate data into a structured format (e.g., pandas DataFrame).
        4.2.3.  Basic data cleaning (e.g., handling missing values, deduplication of records).

    **4.3. Keyword Analysis Module (Supports Section 2.2.1)**
        4.3.1.  Extraction of existing keywords provided by APIs.
        4.3.2.  NLP-based keyword/keyphrase extraction from abstracts:
                a.  Tokenization, stop-word removal, lemmatization/stemming.
                b.  Techniques like TF-IDF, RAKE, or YAKE! for identifying relevant terms.
                c.  Configurable parameters for NLP processing (e.g., n-gram range).
        4.3.3.  Frequency analysis: Calculate the frequency of identified keywords/terms.
        4.3.4.  Temporal distribution analysis: Track keyword/term frequency over the specified timeframe (e.g., yearly, quarterly).

    **4.4. Semantic Embedding & Clustering Module (Supports Section 2.2.2)**
        4.4.1.  Abstract Embedding Generation:
                a.  Integrate a pre-trained sentence transformer model (specifically BGE-M3 as mentioned, or allow selection of others like SBERT).
                b.  Provide functionality for local hosting/loading of the model.
                c.  Transform preprocessed abstracts into dense vector embeddings.
                d.  Cache embeddings to avoid re-computation.
        4.4.2.  Unsupervised Semantic Clustering:
                a.  Implement clustering algorithms (e.g., K-Means as mentioned, optionally DBSCAN, HDBSCAN).
                b.  Allow configuration of clustering parameters (e.g., number of clusters for K-Means).
                c.  Assign publications to thematic clusters based on abstract embeddings.

    **4.5. Visualization & Reporting Module**
        4.5.1.  Temporal Trend Plots:
                a.  Line graphs showing the growth trajectory of research combining "SCM/Logistics" with "Agent(s)/MAS" over time.
                b.  Line graphs showing the emergence and frequency of "LLM Agent," "Generative AI Agent" in conjunction with SCM/Logistics.
                c.  Line graphs for specific framework names (e.g., "AutoGen SCM," "LangGraph SCM") if data permits.
        4.5.2.  Cluster Visualization:
                a.  Dimensionality reduction of embeddings (e.g., PCA, UMAP as mentioned).
                b.  2D scatter plots visualizing thematic clusters.
                c.  Option to label clusters with top keywords or representative documents.
        4.5.3.  Thematic Evolution Visualization:
                a.  Stacked bar charts or alluvial diagrams showing the temporal distribution of publications within semantic clusters to track theme evolution.
        4.5.4.  Exportable Outputs:
                a.  Save plots as image files (PNG, SVG).
                b.  Export processed data (DataFrames with keywords, cluster assignments) to CSV or Excel.

    **4.6. Configuration Management**
        4.6.1.  External configuration file(s) (e.g., YAML, JSON, .env) for:
                a.  API keys and endpoints.
                b.  Search parameters (keywords, date ranges).
                c.  Paths for data storage, model loading, and output generation.
                d.  Parameters for NLP, embedding, and clustering.
        4.6.2.  Command-line interface (CLI) for running different stages of the pipeline (e.g., `python main.py --fetch-data`, `python main.py --analyze-keywords`, `python main.py --cluster-abstracts`).

**5. Non-Functional Requirements**
    5.1.  **Modularity:** Code should be organized into logical modules (data acquisition, preprocessing, analysis, visualization).
    5.2.  **Usability:** Clear instructions for setup and execution. Well-documented configuration options.
    5.3.  **Maintainability:** Well-commented, clean, and readable Python code adhering to PEP 8 standards.
    5.4.  **Extensibility:** Design should allow for easy addition of new APIs, NLP techniques, embedding models, or clustering algorithms in the future.
    5.5.  **Reproducibility:** Given the same configuration and dataset, the analysis should produce consistent results.
    5.6.  **Error Handling & Logging:** Robust error handling and informative logging for troubleshooting.
    5.7.  **Performance:** While not a high-throughput system, operations like embedding generation for large datasets should be reasonably efficient. Consider batch processing where appropriate.

**6. Technical Stack (Recommended)**
    6.1.  **Programming Language:** Python 3.9+
    6.2.  **Core Libraries:**
            *   `requests`: For API communication.
            *   `pandas`: For data manipulation and structuring.
            *   `numpy`: For numerical operations.
            *   `scikit-learn`: For K-Means, PCA, TF-IDF.
            *   `sentence-transformers`: For BGE-M3 embedding model.
            *   `nltk` or `spaCy`: For NLP tasks (tokenization, stop-word removal, lemmatization).
            *   `umap-learn`: For UMAP dimensionality reduction.
            *   `matplotlib`, `seaborn`, `plotly` (optional, for more interactive plots): For visualizations.
    6.3.  **Configuration:** `PyYAML` or `python-dotenv`.
    6.4.  **Optional (for GUI if desired later):** `Streamlit` or `Gradio`.
    6.5.  **Version Control:** Git.

**7. Deliverables**
    7.1.  Fully functional Python application source code, including all modules and scripts.
    7.2.  `requirements.txt` file for easy dependency installation.
    7.3.  A `README.md` file detailing:
            *   Setup instructions (environment, dependencies, API key configuration).
            *   Usage instructions (how to run different analysis stages, CLI arguments).
            *   Explanation of configuration file options.
            *   Description of output files and visualizations.
    7.4.  Sample configuration file(s).
    7.5.  (Optional) A brief report or Jupyter Notebook demonstrating a sample run and its outputs, aligning with the needs of Section 3.1.1.

**8. Key Considerations / Constraints**
    8.1.  **API Access & Rate Limits:** The application must respect API terms of service and handle rate limiting. API keys will need to be managed securely (e.g., via environment variables or a config file not committed to version control).
    8.2.  **Local Model Hosting:** The BGE-M3 model needs to be downloadable and usable locally. Ensure sufficient disk space and computational resources (RAM, potentially GPU for faster embeddings if supported by the library).
    8.3.  **Data Volume:** Depending on the breadth of search queries and timeframes, the volume of collected data could become significant. Efficient data handling and storage will be necessary.
    8.4.  **Iterative Development:** The application can be developed in stages, starting with data acquisition and basic keyword analysis, then moving to semantic analysis and more complex visualizations.

**9. Acceptance Criteria / Success Metrics**
    9.1.  The application successfully fetches, processes, and stores metadata from the specified APIs based on user-defined queries.
    9.2.  The application generates keyword frequency lists and temporal trend visualizations as described in Section 2.2.1.
    9.3.  The application successfully generates abstract embeddings, performs semantic clustering, and produces visualizations of these clusters and their evolution as described in Section 2.2.2.
    9.4.  The outputs generated are suitable for direct inclusion or interpretation for Section 3.1.1 of the SLR.
    9.5.  The application is configurable and runs without critical errors on a standard research environment.

---
