# Article Downloader and Thematic Organizer

## Task

This application is designed to automate the process of downloading research articles based on a list of publications (e.g., from a CSV file). It aims to:

1.  **Retrieve Full-Text Content:**  Download the full text of scientific articles, prioritizing open access sources.
2.  **Organize by Theme:**  Cluster articles thematically based on their abstracts and organize downloaded PDFs into folders corresponding to these clusters.
3.  **Store Data:**  Store article metadata, full text (in Markdown format), and local PDF paths in a structured pandas DataFrame, which can be saved to a JSON file for further analysis.

## Description of the App

The Article Downloader and Thematic Organizer, primarily orchestrated by the `../notebooks/article_downloader.ipynb` Jupyter Notebook, is designed to streamline the collection and organization of scientific research publications. It takes a CSV file as input, containing a list of articles with metadata like titles, DOIs, and abstracts.

**Key Features:**

*   **Automated Full-Text Retrieval:** Attempts to download the full text of articles in two formats:
    *   **Markdown:** Extracts full article content from HTML pages of journals and converts it to Markdown format, suitable for text analysis and storage in DataFrames.
    *   **PDF:** Downloads PDF files of articles for local storage and archival.
*   **Intelligent PDF Resolution:** Employs a multi-strategy approach to find and download PDF files, including DOI resolution, journal website scraping, and potential integration with open access APIs (Unpaywall, CORE - future enhancement).
*   **Thematic Clustering:** (Optional, configurable) Clusters articles based on the semantic similarity of their abstracts using embedding models (placeholder for future implementation - e.g., OpenAI, Google embeddings).
*   **Cluster-Based PDF Organization:** (Optional, configurable) Organizes downloaded PDF files into local folders, with each folder representing a thematic cluster.
*   **Structured Data Storage:**  Stores all relevant information, including article metadata, full-text Markdown content, local PDF file paths, retrieval methods, and cluster assignments in a pandas DataFrame. This DataFrame can be saved as a JSON file for further analysis, integration with tools like NotebookLM, or building Retrieval Augmented Generation (RAG) applications.
*   **Configurable Settings:** Allows customization through a `config.yaml` file and environment variables, including:
    *   Enabling/disabling clustering.
    *   Number of clusters.
    *   Choice of HTML parser (currently BeautifulSoup, with potential for Jina-AI WebReader in the future).
    *   Rate limiting parameters for ethical web scraping.
    *   API keys for optional services (placeholder for future API integrations).
*   **Robust Error Handling and Logging:** Implements error handling and logging to ensure application stability and provide insights into the processing workflow.
*   **Rate Limiting and Ethical Scraping Practices:** Includes rate limiting mechanisms and encourages ethical web scraping by respecting `robots.txt` and setting User-Agent headers.

**Workflow:**

1.  **Input Data:** Takes a CSV file (e.g., `data/references/your_articles.csv`) as input. The specific path and filename should be configured within the `../notebooks/article_downloader.ipynb` notebook.
2.  **Content Retrieval:** For each article in the input CSV:
    *   Resolves the article's journal page URL using the DOI.
    *   Attempts to download the full text in Markdown format by parsing the HTML of the journal page.
    *   Attempts to download the PDF file of the article.
3.  **Clustering (Optional):** If enabled in the configuration:
    *   Generates embeddings for article abstracts (placeholder for future implementation).
    *   Clusters articles based on these embeddings using K-Means clustering.
    *   Assigns a cluster ID to each article.
4.  **PDF Organization (Optional):** If clustering is enabled, organizes downloaded PDFs into folders as configured in `config.yaml` (e.g., `data/pdfs/cluster_0/` by default, relative to the project root).
5.  **Data Storage:** Creates a pandas DataFrame containing:
    *   Original article metadata from the input CSV.
    *   Full-text Markdown content (if retrieved).
    *   Local PDF file path (if downloaded).
    *   Retrieval method used.
    *   Download success status.
    *   Cluster ID (if clustering is enabled).
    *   Saves the DataFrame to a JSON file (e.g., `data/processed_articles_fulltext.json`, path configurable in the notebook, relative to project root).

## Project Structure

The components of this application module (`core_api_downloader.py`, `html_parser.py`, etc.) are located within the `app/` directory. Configuration is managed by `app/config.yaml` and `/.env` (at the project root).


## Third-Party Services Used

This application currently utilizes the following third-party services and libraries directly or has placeholders for future integration:

*   **Jina AI WebReader (or BeautifulSoup + html2text):**  Used for parsing HTML content from journal websites and extracting article text in Markdown format. Jina-AI WebReader is a more advanced option potentially offering better accuracy and handling of complex HTML structures. BeautifulSoup and html2text provide a simpler, widely-used alternative.
*   **Unpaywall API (Future Enhancement):**  Planned for future integration to enhance PDF retrieval by leveraging Unpaywall's extensive database of open access articles and direct links to PDFs.  Requires a free Unpaywall API key (email registration may be required).
*   **CORE API:** Integrated as a source for open access article retrieval, especially for articles in repositories. Requires a free CORE API key. The following features are supported:
    *   **Search by Keywords:** Uses the `/search/works` endpoint to retrieve publications matching a keyword query. Returns metadata including DOI, title, authors, abstract, etc.
    *   **Retrieve by DOI:** Uses the `/works/{doi}` endpoint to fetch metadata for a specific publication by DOI.
    *   **Retrieve Full Text by DOI:** Uses the `/discover` endpoint to attempt to retrieve the full text for a publication by DOI (if available).
    *   See `core_api_client.py` for usage examples and details.
*   **OpenAI or Google Embedding Models (Future Enhancement):** Placeholder for integrating embedding models from OpenAI (e.g., `text-embedding-3-small`) or Google (e.g., Gemini via `google-generativeai`) to generate embeddings for article abstracts, enabling semantic clustering. Requires API keys for the respective services.
*   **Python Libraries:**
    *   **pandas:** For data manipulation and storage in DataFrames.
    *   **requests:** For making HTTP requests to fetch web pages and PDFs.
    *   **beautifulsoup4:** (Optional, initial HTML parser) For parsing HTML and XML.
    *   **html2text:** (Optional, initial HTML parser) For converting HTML to Markdown.
    *   **scikit-learn:** For K-Means clustering and potentially t-SNE visualization.
    *   **python-dotenv:** For loading environment variables from a `.env` file.
    *   **tqdm:** For displaying progress bars during data processing.
    *   **pydantic-settings:** For structured configuration management using YAML files and environment variables.
    *   **pyyaml:** For parsing YAML configuration files.
    *   **aiohttp:** (Optional, for future asynchronous scraping) For asynchronous HTTP requests.
    *   **requests-cache:** (Optional, for future caching) For HTTP caching to improve efficiency.
    *   **diskcache:** (Optional, for future caching) For file-based caching.
    *   **matplotlib, seaborn:** (Optional, for future visualization) For data visualization (e.g., cluster plots).
    *   **ipykernel, notebook:** For running and interacting with IPython Notebooks.

## Prerequisites

Before running the Article Downloader and Thematic Organizer, you need to complete the following prerequisites:

1.  **Install Python:** Ensure you have Python 3.7 or higher installed on your system. It's recommended to use Python 3.11 as specified in `environment.yml`.
2.  **Install Conda (Recommended):** It is highly recommended to use Conda to manage your Python environment and dependencies. If you don't have Conda installed, follow the instructions on the [Anaconda website](https://www.anaconda.com/products/distribution).
3.  **Create Conda Environment (Optional but Recommended):**
    *   From the project root, run `conda env create -f app/environment.yml`. Alternatively, navigate to the `app/` directory and run `conda env create -f environment.yml`.
    *   Activate the environment: `conda activate article_downloader_env` (Ensure `article_downloader_env` is the name defined in `app/environment.yml`).
4.  **Install Python Dependencies (Alternative to Conda):** If you are not using Conda, you can install the required Python packages using pip.
    *   Navigate to the project root directory (e.g., `/SCS_Module`).
    *   Install dependencies from `requirements.txt`: `pip install -r requirements.txt`.
    *   Note: This project primarily uses the root `requirements.txt`. The `app/requirements.txt` file may contain dependencies specific to the app module if run in isolation, but for the integrated project, the root file and `app/environment.yml` are preferred.
5.  **Prepare Input CSV File:** Prepare your input CSV file (e.g., based on examples in `data/references/`) and update its path in the `../notebooks/article_downloader.ipynb` notebook. The paths in the notebook should be relative to the project root. Example CSV structure (first line is header):

    ```csv
    date,title,doi,authors,journal,short_journal,volume,year,publisher,issue,page,abstract
    2023-09-29,Defining human-AI teaming the human-centered way: a scoping review and network analysis,10.3389/frai.2023.1250725,"[{'author_name': 'Sophie Berretta', ...}]",Frontiers in Artificial Intelligence,Front. Artif. Intell.,6,2023,Frontiers Media SA,,,"IntroductionWith the advancement of technology..."
    2023-11-01,Configurations of human-centered AI at work: seven actor-structure engagements in organizations,10.3389/frai.2023.1272159,"[{'author_name': 'Uta Wilkens', ...}]",Frontiers in Artificial Intelligence,Front. Artif. Intell.,6,2023,Frontiers Media SA,,,"PurposeThe discourse on the human-centricity of AI at work needs contextualization..."
    ...
    ```

6.  **Configuration (Optional):**
    *   **`config.yaml`:**  Review and adjust settings in the `app/config.yaml` file as needed. This file allows you to configure clustering, rate limiting, choice of HTML parser, and other application parameters. Paths within `config.yaml` (like `pdf_dir_root`, `cluster_dir_format`) are relative to the project root directory (e.g., `./data/pdfs` means `<project_root>/data/pdfs`).
    *   **`.env`:**  This file is used to store sensitive configuration information, such as API keys.
        *   **Jina AI API Key (Required if using Jina Reader API):** If you want to use the Jina Reader API for HTML parsing (which may offer improved parsing quality), you need to:
            *   Obtain a free Jina AI API key from [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey).
            *   Create a `.env` file in the project root directory (i.e., `/SCS_Module/.env`) (if it doesn't exist).
            *   Add the following line to your `.env` file, replacing `YOUR_JINA_API_KEY` with your actual API key:

                ```env
                JINA_API_KEY=YOUR_JINA_API_KEY
                ```
        *   **Google API Key (Required for Gemini Embeddings):** If you want to use Gemini embeddings for article clustering, you need to:
            *   Obtain a Google API key. You may need to create a project in the Google Cloud Console and enable the Gemini API.
            *   Add the following line to your `.env` file, replacing `YOUR_GOOGLE_API_KEY` with your actual Google API key:

                ```env
                GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
                ```
        *   **Other API Keys (Optional, for future features):** If you plan to use API-based features in the future (e.g., for enhanced PDF retrieval), you will also add API keys for those services (OpenAI, CORE API) to this `.env` file.  **Important:** Keep your `.env` file secure and do not commit it to public repositories as it contains sensitive API keys.

## Configuration

The application's behavior can be configured using two files: `config.yaml` and `.env`.

*   **`app/config.yaml`:** This file, located in `app/config.yaml`, contains general application settings in YAML format. Paths within this file (e.g., `pdf_dir_root`, `cluster_dir_format`) are relative to the project root directory. You can modify the following parameters:
    *   `pdf_dir_root`:  Root directory where downloaded PDFs will be stored (default: `data/pdfs`, relative to project root).
    *   `cluster_dir_format`: Format string for cluster-specific PDF directories (default: `data/cluster_{}`, relative to project root).
    *   `use_clustering_in_pipeline`:  Boolean flag to enable or disable thematic clustering of articles (default: `true`).
    *   `n_clusters`:  Number of clusters to use for K-Means clustering (default: `20`).
    *   `user_agent`:  User-Agent string used for HTTP requests (default: `"MyArticleDownloader/1.0 (Contact: your-email@example.com)"`).
    *   `rate_limit_delay_min`: Minimum delay (in seconds) between web requests for rate limiting (default: `0.5`).
    *   `rate_limit_delay_max`: Maximum delay (in seconds) between web requests for rate limiting (default: `1.5`).
    *   `use_jina_reader_api_config`: Boolean flag to enable or disable using Jina Reader API for HTML parsing. Set to `true` to use Jina Reader API (requires `JINA_API_KEY` to be set in `.env`), `false` to use BeautifulSoup and html2text (default: `false`).
    *   `unpaywall_email`: Email address for Unpaywall API (optional, for future Unpaywall integration).
    *   `core_api_key`: API key for CORE API (optional, for future CORE API integration).
    *   `openai_api_key`: API key for OpenAI API (optional, for future embedding generation).
    *   `google_api_key`: API key for Google API (optional, for future embedding generation - e.g., Gemini).

*   **`.env`:** This file is used to store sensitive information as environment variables. **It is crucial to keep this file secure and NOT commit it to public version control.** You should add the following API keys to your `.env` file if you intend to use the corresponding features (create the file if it doesn't exist in the project root directory):
    *   `JINA_API_KEY`: Your Jina AI Reader API key (required if you set `use_jina_reader_api_config: true` in `app/config.yaml`). Get it from [https://jina.ai/?sui=apikey](https://jina.ai/?sui=apikey).
    *   `OPENAI_API_KEY`: Your OpenAI API key (optional, for future embedding generation). Obtain it from the OpenAI platform.
    *   `GOOGLE_API_KEY`: Your Google API key (optional, for future embedding generation - e.g., Gemini). Obtain it from the Google Cloud Console.
    *   `CORE_API_KEY`: Your CORE API key (optional, for future CORE API integration). Obtain it by registering on the CORE website.

    **Example `.env` file:**

    ```env
    JINA_API_KEY=YOUR_JINA_API_KEY
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    # GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY  # Optional, uncomment and add if needed
    # CORE_API_KEY=YOUR_CORE_API_KEY      # Optional, uncomment and add if needed
    ```

    **Important:**  When using the Jina Reader API, ensure that you have set the `JINA_API_KEY` in your `.env` file and set `use_jina_reader_api_config: true` in `app/config.yaml`. If `use_jina_reader_api_config` is `false` or if the `JINA_API_KEY` is not found in `.env`, the application will default to using BeautifulSoup and html2text for HTML parsing.

## Usage Instructions

1.  **Activate Conda Environment (if used):** `conda activate article_downloader_env` (Ensure this is the name defined in `app/environment.yml`).
2.  **Navigate to Project Directory:** In your terminal, navigate to the project root directory (e.g., `/SCS_Module`). **It is recommended to run the Jupyter Notebook (`notebooks/article_downloader.ipynb`) from the project root directory for proper module and path resolution.**
3.  **Start Jupyter Notebook:** Run `jupyter notebook` or `jupyter lab` in your terminal (from the project root). This will open the Jupyter Notebook interface in your web browser.
4.  **Open `notebooks/article_downloader.ipynb`:**  Open the `notebooks/article_downloader.ipynb` file in the Jupyter Notebook interface.
5.  **Run the Notebook Cells:** Execute the notebook cells sequentially by clicking on each cell and pressing `Shift + Enter`.
6.  **Monitor Progress and Logs:** Observe the output of each cell. Logs (e.g., `scraper.log`, if generated by the notebook) will typically be created in the directory from which the notebook is run (i.e., the project root). Ensure logging paths are configured as needed within the notebook or its imported modules.
7.  **Output Data:**
    *   **`processed_articles_fulltext.json`:**  The processed DataFrame containing article metadata, full text, PDF paths, etc., will be saved to a path configured in the notebook (e.g., `data/processed_articles_fulltext.json`, relative to project root).
    *   **`data/pdfs/`:** If PDF downloading ... downloaded PDF files will be stored in subfolders within the directory specified in `app/config.yaml` (e.g. `data/pdfs/` by default, relative to project root)...

## Optional Features and Customization

*   **Clustering:** You can enable or disable thematic clustering of articles by modifying the `use_clustering_in_pipeline` setting in `app/config.yaml`. You can also adjust the number of clusters (`n_clusters`).
*   **HTML Parser:** Currently, the application uses BeautifulSoup and html2text for HTML parsing. Future versions may support switching to Jina-AI WebReader for potentially improved parsing accuracy by modifying the `parse_article_html` function in `html_parser.py` (located in `app/html_parser.py`).
*   **Rate Limiting:** You can adjust rate limiting parameters (minimum and maximum delay between requests) in the `app/config.yaml` file to control the scraping speed and be more respectful to journal websites.
*   **API Integration:** Future enhancements will include integration with Unpaywall and CORE APIs to improve PDF retrieval. You will be able to configure API keys in the `.env` file (at project root) and enable/disable API usage in `app/config.yaml`. Embedding model integration (OpenAI, Google) for clustering will also be configurable in future versions.

## Ethical Considerations and Disclaimer

This application is intended for educational and research purposes to facilitate the collection and organization of **open access** scientific research articles.

**It is crucial to use this application ethically and responsibly:**

*   **Respect `robots.txt`:** Always check and adhere to the `robots.txt` file of any website you are scraping.
*   **Rate Limiting:** Implement and respect rate limits to avoid overloading website servers. The application includes basic rate limiting, but you may need to adjust it based on the target websites.
*   **Terms of Service:** Review and comply with the terms of service of the journal websites you are scraping. Scraping might be prohibited or restricted on some websites.
*   **Copyright and Usage:** Respect copyright laws and intellectual property rights. Use the downloaded content responsibly and ethically, adhering to fair use principles.
*   **No Warranty:** This application is provided "as is" without warranty of any kind. The developers are not responsible for any misuse or consequences arising from the use of this application.

**Use this application at your own risk and always prioritize ethical and legal considerations when web scraping.**

---

**Author:** Maksim Ilin | TSI

**Contact:** Ilin.M@tsi.lv

**License:** MIT License