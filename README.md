# Knowledge Retrieval Agentic System

## Overview

This repository contains code and resources for a Knowledge Retrieval Agentic System that leverages Large Language Models (LLMs) and AI-powered agent networks. The system integrates multiple storage solutions and knowledge representation techniques to provide comprehensive information retrieval and research capabilities.

## System Architecture

The system is built on a modular architecture with the following key components:

- **API Integration Layer**: Abstract base class for API clients with implementations for SpringerNature, CORE, and future APIs
- **Storage Layer**: 
  - Backblaze B2 for object storage
  - Qdrant for vector storage
  - Meilisearch for markdown content
- **Knowledge Graph (Neo4j)**: Entity and relationship management, citation networks, concept relationships
- **Context Management**: Hierarchical context structure with merging capabilities
- **Workflow Orchestration**: Based on smolagents framework with modular agent design

## Project Structure

The project is organized into several key components:

- **data/**: Contains datasets used for knowledge retrieval and analysis
- **app/**: Contains Python scripts and modules for data retrieval (e.g., `core_api_downloader.py`, `sn_xml_downloader.py`), processing (`html_parser.py`, `pdf_ocr.py`), and related utilities. Detailed documentation for this component can be found in `app/README.md`.
- **notebooks/**: Jupyter notebooks for exploratory data analysis, workflow execution (e.g., `article_downloader.ipynb`), and experimental work.
- **memory_bank/**: Stores key architectural decision records (ADRs), design documents, project planning notes (like `project_description.txt`), and other core guiding documentation for the system's development and evolution.
- **springernature_api_client/**: Implementation for SpringerNature API
- **dashboard/**: Visual interface for system insights
- **requirements.txt**: Lists the required Python packages for the project
- **app/environment.yml**: Conda environment file for setting up the development environment, primarily for the `app` components. See "Dependency Management" section below.
- **body_of_knowledge/**: Contains detailed research notes, literature reviews, and explorations of specific concepts relevant to the project.

## Key Features

- **Multi-Source Content Retrieval**: Integration with academic APIs (SpringerNature, CORE) for comprehensive content access. The CORE API integration supports keyword-based search, metadata retrieval by DOI, and full text retrieval by DOI (see `app/README.md` and `core_api_client.py`).
- **Semantic Search**: Vector-based retrieval using Qdrant for context-aware search
- **Knowledge Graph**: Neo4j-based graph for relationship discovery and complex querying
- **Context-Aware Retrieval**: Hierarchical context management for improved search relevance
- **Agent-Based Workflows**: Orchestrated research and analysis workflows using smolagents
- **Interactive Dashboard**: Visual interface for system insights and data exploration

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API keys and storage credentials
4. The primary application workflow for article downloading and processing is initiated via the Jupyter Notebook: `notebooks/article_downloader.ipynb`. Refer to `app/README.md` for detailed instructions on its usage and configuration. For the dashboard, see `dashboard/README.md`.

## Dependency Management

This project uses both `requirements.txt` (at the root) and `app/environment.yml` (for Conda users) to manage Python dependencies.

*   **`requirements.txt`**: Contains a list of core Python packages required for the entire project. Install using `pip install -r requirements.txt`. This is the recommended way to install dependencies for general use.
*   **`app/environment.yml`**: Defines a Conda environment specifically tailored for the development and execution of components within the `app/` directory, including the `notebooks/article_downloader.ipynb` workflow. It includes all necessary packages and ensures a consistent environment. To use it:
    1.  Ensure you have Conda installed.
    2.  Navigate to the `app/` directory.
    3.  Create and activate the environment:
        ```bash
        conda env create -f environment.yml
        conda activate article_downloader_env
        ```
    *(Note: The main `requirements.txt` and `app/environment.yml` should be kept largely consistent. If using Conda, managing dependencies primarily through `app/environment.yml` is advised for the article processing workflow.)*

## Documentation

For detailed information about the system architecture, implementation details, and design decisions, please refer to:

- [Overall Project Structure and Core Concepts](README.md) (this document)
- [Application Modules and Article Processing (app/)](app/README.md)
- [Dashboard Functionality (dashboard/)](dashboard/README.md)
- [Knowledge Retrieval System Architecture](memory_bank/2024-04-20_knowledge_retrieval_system_architecture.md)
- [Design and Architecture](memory_bank/design_and_architecture.txt)
- [Project Description](memory_bank/project_description.txt)
- [Project Backlog and Publication Selection](memory_bank/project_management/backlog.md)

## Checking Development Status

To stay informed about the current development status of the project, developers should regularly check the following resources:

1. **Development Status Report**
   - Located in `memory_bank/reports/`
   - Updated bi-weekly with sprint progress

2. **Documentation Changelog**
   - Location: `memory_bank/development/changelog/documentation_changelog.md`
   - Contains: Recent documentation changes and updates
   - Updated: With each significant documentation change

3. **Git History**
   - Command: `git log --since="1 day ago" --pretty=format:"%h - %s (%ad)" --date=short`
   - Shows: Recent commits and changes
   - Updated: With each commit

4. **Documentation Standards**
   - Location: `memory_bank/development/documentation_standards.md`
   - Contains: Guidelines for maintaining and updating documentation
   - Updated: As standards evolve

Key information to track:
- Current sprint and timeline
- Completed components
- In-progress development
- Technical debt and risks
- Quality metrics
- Resource allocation
- Dependencies and blockers

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the terms specified in the LICENSE file.
