# Agents and Tools Mapping
**Date:** 2024-04-29
**Status:** Active
**Version:** 1.0.0

## Version History

| Version | Date | Author | Changes | Review Status |
|---------|------|--------|---------|---------------|
| 1.0.0 | 2024-04-29 | AI Assistant | Initial document creation with agents, tools, and process mapping | Pending Review |
| | | | | |

## Change Documentation Template

```markdown
### Change Entry Template
**Version:** [Semantic Version]
**Date:** [YYYY-MM-DD]
**Author:** [Name/Role]
**Type of Change:** [Addition/Modification/Removal/Refactoring]

#### Changes Made
- [ ] Agent Updates
  - [ ] New agents added
  - [ ] Existing agent modifications
  - [ ] Agent removals
- [ ] Tool Updates
  - [ ] New tools added
  - [ ] Existing tool modifications
  - [ ] Tool removals
- [ ] Process Updates
  - [ ] New processes added
  - [ ] Existing process modifications
  - [ ] Process removals
- [ ] Mapping Updates
  - [ ] New agent-tool-process relationships
  - [ ] Modified relationships
  - [ ] Removed relationships

#### Rationale
[Brief explanation of why changes were made]

#### Impact Assessment
- **Dependencies:** [List affected dependencies]
- **Integration Points:** [List affected integration points]
- **Documentation Updates:** [List other documents that need updates]

#### Review Status
- [ ] Technical Review
- [ ] Architecture Review
- [ ] Implementation Review
- [ ] Documentation Review

#### Reviewers
- Technical: [Name]
- Architecture: [Name]
- Implementation: [Name]
- Documentation: [Name]

#### Next Steps
- [ ] Update implementation
- [ ] Update tests
- [ ] Update documentation
- [ ] Schedule follow-up review
```

## Table 1: Agents

| Agent Name | Role | Description | Capabilities | Dependencies |
|------------|------|-------------|--------------|--------------|
| Publication Retrieval Agent | Data Collection | Handles interactions with research publication APIs | - API rate limit management<br>- Data format normalization<br>- Error handling<br>- Cache management | - Arxiv API<br>- Semantic Scholar API<br>- CORE API<br>- Open Alex API |
| Content Analysis Agent | Text Processing | Analyzes and processes textual content from publications | - Text extraction<br>- Key information identification<br>- Relationship mapping<br>- Semantic analysis | - LLM providers<br>- Qdrant vector storage<br>- Meilisearch |
| Image Analysis Agent | Visual Content Processing | Analyzes scientific visualizations and diagrams | - Image recognition (Gemini 2.5 Flash)<br>- Diagram interpretation<br>- Graph data extraction<br>- Scientific visualization analysis | - Gemini API<br>- LayoutLM<br>- Image processing libraries |
| Table Analysis Agent | Tabular Data Processing | Processes and analyzes tabular data from publications | - Table extraction (Mistral OCR)<br>- Data processing (Pandas)<br>- Statistical analysis<br>- Visualization generation | - Mistral API<br>- Pandas<br>- Data visualization libraries |
| Research Agent | Core Research | Coordinates research activities and analysis | - Research planning<br>- Task delegation<br>- Result synthesis<br>- Quality control | - All other agents<br>- Workflow orchestration<br>- Context management |
| Analysis Agent | Data Analysis | Performs in-depth analysis of research data | - Data interpretation<br>- Pattern recognition<br>- Statistical analysis<br>- Trend identification | - Content Analysis Agent<br>- Table Analysis Agent<br>- Knowledge Graph |
| Writing Agent | Content Generation | Generates research summaries and reports | - Content structuring<br>- Summary generation<br>- Report formatting<br>- Citation management | - Content Analysis Agent<br>- Research Agent<br>- Knowledge Graph |

## Table 2: Tools

| Tool Name | Category | Description | Usage Context | Dependencies |
|-----------|----------|-------------|---------------|--------------|
| API Client | Infrastructure | Base class for API interactions | All API-related operations | - API endpoints<br>- Authentication systems |
| B2 Storage | Storage | Object storage for raw content | Document storage and retrieval | - Backblaze B2 API<br>- Storage management system |
| Qdrant Storage | Storage | Vector storage for semantic search | Embedding storage and retrieval | - Qdrant API<br>- Embedding models |
| Meilisearch Storage | Storage | Full-text search engine | Content indexing and search | - Meilisearch API<br>- Text processing utilities |
| Knowledge Graph | Storage | Neo4j-based knowledge representation | Relationship storage and querying | - Neo4j<br>- Graph algorithms |
| Context Manager | Processing | Manages hierarchical context | Context tracking and merging | - Context storage<br>- State management |
| Workflow Orchestrator | Processing | Manages agent workflows | Task coordination and execution | - smolagents framework<br>- Agent communication system |
| LayoutLM | Processing | Document layout analysis | PDF structure analysis | - LayoutLM model<br>- PDF processing libraries |
| Gemini 2.5 Flash | AI | Image recognition and analysis | Visual content processing | - Gemini API<br>- Image processing libraries |
| Mistral OCR | AI | Structured OCR for tables | Table extraction and analysis | - Mistral API<br>- OCR processing libraries |
| Pandas Processor | Processing | Data analysis and manipulation | Tabular data processing | - Pandas library<br>- Data processing utilities |

## Table 3: Agent-Tool-Process Mapping

| Process | Agent | Tools | Description |
|---------|-------|-------|-------------|
| Publication Retrieval | Publication Retrieval Agent | - API Client<br>- B2 Storage | Retrieves and stores publications from various sources |
| Content Processing | Content Analysis Agent | - Qdrant Storage<br>- Meilisearch Storage<br>- Knowledge Graph | Processes and indexes textual content |
| Visual Analysis | Image Analysis Agent | - Gemini 2.5 Flash<br>- LayoutLM<br>- Knowledge Graph | Analyzes and processes visual content |
| Table Processing | Table Analysis Agent | - Mistral OCR<br>- Pandas Processor<br>- Knowledge Graph | Extracts and analyzes tabular data |
| Research Coordination | Research Agent | - Context Manager<br>- Workflow Orchestrator<br>- All storage tools | Coordinates research activities and manages workflow |
| Data Analysis | Analysis Agent | - Knowledge Graph<br>- Pandas Processor<br>- Qdrant Storage | Performs in-depth data analysis |
| Content Generation | Writing Agent | - Knowledge Graph<br>- Meilisearch Storage<br>- Context Manager | Generates research summaries and reports |
| Workflow Management | All Agents | - Workflow Orchestrator<br>- Context Manager | Manages agent interactions and state |
| Knowledge Integration | All Agents | - Knowledge Graph<br>- Context Manager | Integrates and updates knowledge base |

## Notes
1. **Access Control**: All agents have access to the Workflow Orchestrator and Context Manager for coordination and state management.
2. **Storage Access**: Storage tools are accessed through standardized interfaces to maintain consistency.
3. **Process Dependencies**: Some processes may require sequential execution or parallel processing based on workflow requirements.
4. **Tool Versions**: All tools should be version-controlled and documented for reproducibility.

## References
1. [Research Agent Architecture ADR](2024_04_23_adr_research_agent_architecture.md)
2. [Image and Table Analysis ADR](2024_04_29_adr_image_table_analysis.md)
3. [Knowledge Retrieval System Architecture](2024_04_20_knowledge_retrieval_system_architecture.md)
4. [Design and Architecture](design_and_architecture.txt)

## Review Schedule
- **Monthly Review:** First Monday of each month
- **Trigger-based Review:** After significant system changes
- **Quarterly Deep Review:** Every three months
- **Annual Architecture Review:** Year-end comprehensive review

## Maintenance Guidelines
1. **Version Control**
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Update version with each significant change
   - Document all changes in version history

2. **Change Management**
   - Use the provided template for all changes
   - Ensure all changes are reviewed
   - Update related documentation

3. **Review Process**
   - Assign reviewers for each change
   - Track review status
   - Document review outcomes

4. **Documentation Updates**
   - Keep version history current
   - Maintain change documentation
   - Update references as needed 