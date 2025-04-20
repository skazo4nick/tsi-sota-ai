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
- **app/**: Includes Python scripts for data retrieval, processing, analysis, and visualization
- **notebooks/**: Jupyter notebooks demonstrating exploratory data analysis and key findings
- **memory_bank/**: Documentation and architectural decisions
- **springernature_api_client/**: Implementation for SpringerNature API
- **dashboard/**: Visual interface for system insights
- **requirements.txt**: Lists the required Python packages for the project

## Key Features

- **Multi-Source Content Retrieval**: Integration with academic APIs (SpringerNature, CORE) for comprehensive content access
- **Semantic Search**: Vector-based retrieval using Qdrant for context-aware search
- **Knowledge Graph**: Neo4j-based graph for relationship discovery and complex querying
- **Context-Aware Retrieval**: Hierarchical context management for improved search relevance
- **Agent-Based Workflows**: Orchestrated research and analysis workflows using smolagents
- **Interactive Dashboard**: Visual interface for system insights and data exploration

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API keys and storage credentials
4. Run the application: `python app/main.py`

## Documentation

For detailed information about the system architecture, implementation details, and design decisions, please refer to:

- [Knowledge Retrieval System Architecture](memory_bank/2024-04-20_knowledge_retrieval_system_architecture.md)
- [Design and Architecture](memory_bank/design_and_architecture.txt)
- [Project Description](memory_bank/project_description.txt)

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the terms specified in the LICENSE file.
