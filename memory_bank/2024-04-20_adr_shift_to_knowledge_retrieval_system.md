# ADR: Shift from Decision Support System to Knowledge Retrieval Agentic System

## Status
Accepted

## Context
The project initially focused on developing an AI-powered Decision Support System (DSS) for Supply Chain Management (SCM). The system was designed to integrate Large Language Models (LLMs) and AI agent networks to enhance decision-making in SCM. However, during the development process, it became clear that the core components being developed were more aligned with a Knowledge Retrieval System (KRS) than a traditional DSS.

The project had already implemented or was planning to implement several components that are essential for a KRS:
- API integrations for content retrieval (SpringerNature, CORE)
- Document processing and storage capabilities
- Vector storage for semantic search
- Markdown content storage
- Agent-based workflows

## Decision
We have decided to shift the project's focus from a Decision Support System for SCM to a Knowledge Retrieval Agentic System. This shift will allow us to leverage the existing components more effectively and create a more versatile and powerful system for information retrieval and research.

The new system will include:
1. **API Integration Layer**: Abstract base class for API clients with implementations for SpringerNature, CORE, and future APIs
2. **Storage Layer**: 
   - Backblaze B2 for object storage
   - Qdrant for vector storage
   - Meilisearch for markdown content
3. **Knowledge Graph (Neo4j)**: Entity and relationship management, citation networks, concept relationships
4. **Context Management**: Hierarchical context structure with merging capabilities
5. **Workflow Orchestration**: Based on smolagents framework with modular agent design
6. **Retrieval Interface**: Semantic search, context-aware retrieval, and knowledge graph navigation

## Consequences
### Positive
- The system will be more versatile and can be applied to various domains beyond SCM
- The focus on knowledge retrieval aligns better with the implemented and planned components
- The system will provide more comprehensive information retrieval and research capabilities
- The modular architecture allows for easier extension and customization

### Negative
- Some SCM-specific features may need to be generalized or removed
- The project's scope has expanded, which may require additional development time
- Documentation and code may need to be updated to reflect the new focus

## Implementation Plan
1. Update project documentation (README.md, instructions.yaml, etc.)
2. Refactor existing components to align with the new architecture
3. Implement new components (Knowledge Graph, Context Management, etc.)
4. Develop the agent-based workflow orchestration
5. Create a comprehensive retrieval interface

## References
- [Knowledge Retrieval System Architecture](2024-04-20_knowledge_retrieval_system_architecture.md)
- [Design and Architecture](design_and_architecture.txt)
- [Project Description](project_description.txt) 