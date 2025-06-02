# OpenAlex pyalex Integration Status Report

**Date:** 2025-06-02

## 1. Background and Motivation

The current repository implements a modular API Integration Layer for publication retrieval, with custom HTTP clients for sources like OpenAlex and CORE. The previous OpenAlex client was basic, only supported works, and did not leverage advanced query/filter capabilities or pagination. The CORE API module was recently updated to fully support all major endpoints, including direct work retrieval, outputs, stats, TEI XML, and file download, following the official API documentation.

## 2. pyalex Integration Plan

To address the limitations of the current OpenAlex integration and align with best practices, we propose the following plan for integrating the [pyalex](https://github.com/J535D165/pyalex) library:

### Step 1: Planning
- Identify and design the following pyalex-based modules:
  - `openalex_client.py`: Thin wrapper for pyalex, project config, and base access.
  - `openalex_publication_retriever.py`: Publication search/retrieval (works).
  - `openalex_author_retriever.py`: Author search/retrieval.
  - `openalex_concept_retriever.py`: Concept/field-of-study search.
  - `openalex_utils.py`: Helpers for normalization, error handling, and conversion.
  - (Optional) `openalex_bulk_downloader.py`: Batch/bulk download support.

### Step 2: Document in ADR
- Create `memory_bank/development/adr_openalex_pyalex_integration.md` with:
  - Motivation, design decisions, mapping to project needs, interface, and testing strategy.

### Step 3: Develop Modules
- Implement the modules above using pyalex, with clear docstrings and usage examples.

### Step 4: Develop Unit Tests
- Create tests for each module, covering all major functions and edge cases.

### Step 5: Run and Debug
- Run all tests, debug, and update modules until robust and fully covered.

### Step 6: Document Results
- Create `memory_bank/development/openalex_pyalex_report.md` with:
  - Integration summary, challenges, comparison to previous approach, usage examples, and recommendations.

## 3. CORE API Module Update (May/June 2025)
- The `core_api_client.py` module was refactored to:
  - Support all major endpoints: GET /works/{id}, /works/{id}/outputs, /works/{id}/stats, /works/tei/{id}, /works/{id}/download.
  - Provide robust error handling and type checks.
  - Add flexible search functions for DOI, title, author, and generic fields.
  - Align with official API documentation and best practices.

## 4. Next Steps
- Draft the OpenAlex/pyalex ADR.
- Begin implementation of the new OpenAlex modules.
- Develop and run unit tests.
- Document and report on the integration process.

---

*Prepared by GitHub Copilot, 2025-06-02*
