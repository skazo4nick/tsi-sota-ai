# ADR: OpenAlex/pyalex Integration

**Status:** Proposed  
**Date:** 2025-06-02  
**Location:** memory_bank/development/adr_openalex_pyalex_integration.md

---

## Context and Problem Statement

The project requires robust, maintainable, and feature-complete access to the OpenAlex scholarly metadata API. The previous custom OpenAlex client was limited in scope, lacked advanced query/filter support, and did not leverage the official Python ecosystem. The [pyalex](https://github.com/J535D165/pyalex) library is a well-maintained, community-driven Python client for OpenAlex, supporting all major endpoints and advanced features.

## Decision Drivers
- Need for full OpenAlex API coverage (works, authors, concepts, etc.)
- Maintainability and alignment with Python best practices
- Reduced technical debt and code duplication
- Improved error handling, normalization, and extensibility
- Consistency with other API client modules (e.g., CORE)

## Considered Options
1. **Continue with custom HTTP client**
   - Pros: Full control, minimal dependencies
   - Cons: High maintenance, limited features, more bugs, slower development
2. **Adopt pyalex as the core OpenAlex integration**
   - Pros: Feature-rich, maintained, tested, supports all endpoints, less code to maintain
   - Cons: External dependency, must adapt to pyalex API changes

## Decision Outcome

**We will adopt pyalex as the foundation for all OpenAlex API access in this project.**

- A set of thin wrapper modules will be created to encapsulate pyalex usage and provide project-specific interfaces:
  - `openalex_client.py`: Handles pyalex config, authentication, and base access
  - `openalex_publication_retriever.py`: Publication (works) search and retrieval
  - `openalex_author_retriever.py`: Author search and retrieval
  - `openalex_concept_retriever.py`: Concept/field-of-study search
  - `openalex_utils.py`: Helpers for normalization, error handling, and conversion
  - (Optional) `openalex_bulk_downloader.py`: Batch/bulk download support

## Implementation Plan
1. Design and implement the above modules with clear docstrings and usage examples
2. Develop comprehensive unit tests for all major functions and edge cases
3. Run and debug tests, iterate until robust
4. Document the integration process and update main documentation

## Testing Strategy
- Unit tests for each module and function
- Mocking of pyalex responses for edge cases and error handling
- Integration tests for real-world queries (where feasible)

## Consequences
- Faster development and easier maintenance for OpenAlex integration
- Consistent, robust, and feature-complete scholarly metadata access
- Some reliance on the pyalex library's ongoing maintenance

---

*Prepared by GitHub Copilot, 2025-06-02*
