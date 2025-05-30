# Research Analytics Application - Requirements Analysis

This document summarizes the requirements for the Research Analytics Application for the "Agentic AI in SCM" SLR and provides initial thoughts on its development within or alongside the existing Knowledge Retrieval Agentic System.

## 1. Core Purpose

The primary purpose of this Python application is to automate and support the quantitative analysis of research trends related to LLM-powered and agentic AI in Supply Chain Management (SCM) and Logistics, as described in Section 2.2 of the SLR document "Agentic AI in SCM (Ilin, May 2025) ver. 0.7.docx". The application will collect, process, analyze, and visualize publication metadata to identify shifts in research focus. The outputs are intended to directly populate Section 3.1.1 of the SLR.

## 2. Key Functional Modules

The application will be structured around the following key modules:

*   **Data Acquisition:** Fetches publication metadata (titles, authors, abstracts, keywords, dates) from arXiv, CORE, and OpenAlex APIs. Supports configurable search queries (keywords, Boolean logic, timeframes) and handles API rate limits, pagination, and data persistence.
*   **Data Processing & Structuring:** Cleans, standardizes metadata from different sources, and consolidates it into a structured format (e.g., pandas DataFrame), including deduplication and handling missing values.
*   **Keyword Analysis:** Extracts keywords provided by APIs and uses NLP techniques (TF-IDF, RAKE, YAKE!) on abstracts for further extraction. Performs frequency and temporal distribution analysis of these keywords.
*   **Semantic Embedding & Clustering:** Generates dense vector embeddings for abstracts using pre-trained sentence transformer models (e.g., BGE-M3). Applies unsupervised clustering algorithms (K-Means, optionally DBSCAN/HDBSCAN) to group publications into thematic clusters.
*   **Visualization & Reporting:** Creates visual outputs like temporal trend plots for keywords/themes, 2D scatter plots of semantic clusters (using PCA/UMAP for dimensionality reduction), and thematic evolution diagrams. Allows export of plots and processed data.
*   **Configuration Management:** Uses external configuration files (YAML, JSON, .env) for API keys, search parameters, paths, and model/algorithm parameters. Includes a CLI for running pipeline stages.

## 3. Technical Stack Highlights

The core recommended libraries and technologies include:

*   **Python 3.9+**
*   **Core Libraries:**
    *   `requests` (API communication)
    *   `pandas` (Data manipulation)
    *   `numpy` (Numerical operations)
    *   `scikit-learn` (K-Means, PCA, TF-IDF)
    *   `sentence-transformers` (Embedding models like BGE-M3)
    *   `nltk` or `spaCy` (NLP tasks)
    *   `umap-learn` (UMAP dimensionality reduction)
    *   `matplotlib`, `seaborn`, `plotly` (Visualizations)
*   **Configuration:** `PyYAML` or `python-dotenv`
*   **Version Control:** Git

## 4. Initial Thoughts & Questions

*   **Integration with Existing Project:** The requirements suggest this could be a fork or a separate functional module (e.g., an `.ipynb` notebook). This needs careful consideration. A modular approach within the existing project might leverage shared utilities, while a fork offers more independence.
*   **API Client Similarities:** The existing project has `springernature_api_client/` and `app/core_api_downloader.py`. The new app requires CORE API, plus arXiv and OpenAlex. There's potential for reuse or extension of existing API handling logic.
*   **Data Storage & Overlap:** The existing project uses `data/` for various outputs. The new app also needs data persistence. We need to define if and how data storage might be shared or kept separate to avoid conflicts.
*   **Embedding & Clustering:** The existing project mentions Qdrant for vector storage and has clustering analysis notebooks (`notebooks/2_publications_clustering.ipynb`). The new app specifies BGE-M3 and K-Means/UMAP. There might be reusable code for embedding generation, storage (if not Qdrant, then local caching), and clustering logic.
*   **Configuration:** Both projects require robust configuration (API keys, paths). A shared approach or a clear distinction is needed. The existing `app/config.yaml` and `/.env` structure can serve as a template.
*   **Notebook-Driven Workflow:** The user prefers an `.ipynb` solution. This is feasible, especially for a research-focused application. The existing `notebooks/article_downloader.ipynb` can serve as an architectural pattern for a modular notebook that calls underlying Python modules.
*   **Modularity:** The non-functional requirement for modularity is key, regardless of whether it's a single large notebook importing custom modules or a more formal application structure.

## 5. Analysis of Reusable Components from Existing Project

Based on the current "Knowledge Retrieval Agentic System" repository, several components could be reused or adapted for the new "Research Analytics Application":

*   **API Client Logic (Data Acquisition Module):**
    *   `app/core_api_downloader.py`: Directly reusable for CORE API access. Contains patterns for requests, responses, pagination, and rate limits.
    *   `core_api_client.py` (root level): If this is an abstract base class for API clients, it can be used for building new clients for arXiv and OpenAlex.
    *   Patterns from `springernature_api_client/openaccess.py` (even if a dummy) can inform new client structure.

*   **Data Processing & Structuring Module:**
    *   `app/utils.py`: Likely contains utility functions applicable for data cleaning and standardization.
    *   The workflow pattern in `notebooks/article_downloader.ipynb` (fetch, process, structure data into pandas DataFrames) is a reusable model.
    *   Configuration handling via `app/config.yaml` can be adopted.

*   **Keyword Analysis Module:**
    *   `notebooks/1_keywords_analysis.ipynb`: May contain existing code for keyword analysis or visualization that can be adapted.

*   **Semantic Embedding & Clustering Module:**
    *   `notebooks/2_publications_clustering.ipynb`: Offers a template for embedding generation and clustering workflows.
    *   Existing data files (`data/abstract_embeddings.npy`, `data/clusters_df.json`) indicate prior art in handling and storing embedding/clustering outputs.

*   **Visualization & Reporting Module:**
    *   Existing notebooks likely contain Matplotlib/Seaborn usage that can serve as a template for new visualizations.

*   **Configuration Management:**
    *   The use of `app/config.yaml` and `python-dotenv` for `.env` files is a directly reusable pattern.

*   **General Structure and Workflow:**
    *   The modular approach of `notebooks/article_downloader.ipynb` (a notebook orchestrating functionality from `app/` modules) is a strong pattern for the new application.

## 6. Proposed Realization Options

Here are three potential options for developing the "Research Analytics Application":

**Option 1: New Standalone `.ipynb` Notebook with Supporting Modules (Leveraging Existing Utilities)**
*   **Description:** Create a new primary Jupyter Notebook (e.g., `research_analytics_slr.ipynb`) in `notebooks/` or a new subdirectory (e.g., `notebooks/slr_analytics/`). This notebook would orchestrate the entire workflow. New Python modules specific to this SLR analysis (e.g., for new API clients, keyword/semantic analysis) would be created in a dedicated directory like `app/slr_modules/` or a top-level `slr_app/`.
*   **Reuse:** Leverages `app/core_api_downloader.py`, `app/utils.py`, configuration patterns, and insights from existing analysis notebooks.
*   **Pros:** Aligns with user's preference for `.ipynb`, lightweight, focused, clear separation if new modules are well-defined.
*   **Cons:** New module directory needs careful integration to avoid feeling tacked on; risk of minor code duplication if common utilities aren't refactored well.

**Option 2: Integrated Feature Set within the Existing Project Structure**
*   **Description:** Enhance the existing project by adding new modules/functionalities directly into `app/` and new notebooks into `notebooks/`. For instance, new API clients would reside in `app/`, and a new primary notebook `notebooks/slr_quantitative_analysis.ipynb` would drive the SLR workflow.
*   **Reuse:** Maximizes reuse of all relevant existing components and benefits from the established environment.
*   **Pros:** Single repository, easier refactoring of shared code, maintains project coherence if new features are seen as an extension.
*   **Cons:** `app/` and `notebooks/` could become cluttered; original project scope might blur; user might navigate a larger-than-needed project.

**Option 3: Fork the Existing Repository to Create a Dedicated SLR Analytics Application**
*   **Description:** Create a complete fork of the current repository. This fork would then be streamlined specifically for the "Research Analytics Application," removing unnecessary components and adapting existing ones.
*   **Reuse:** Starts with a full copy, allowing selective reuse and modification of all code.
*   **Pros:** Maximum independence, clean and tailored environment for the SLR app, clear separation of project evolution.
*   **Cons:** Initial codebase duplication, effort to remove unneeded parts, manual updates from original repo if needed.
