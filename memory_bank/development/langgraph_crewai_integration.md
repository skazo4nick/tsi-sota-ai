# LangGraph and CrewAI Integration

## Overview
This document details the integration of LangGraph and CrewAI in our Research Assistant System, focusing on the information processing pipeline implementation and multi-agent coordination. It also explains the differentiation between CrewAI agents and non-agentic nodes in our workflows.

## Version Information
- Version: 1.0.0
- Last Updated: 2024-04-28
- Status: Active Development

## Component Differentiation

### CrewAI Agents
CrewAI agents are specialized, stateful components that handle complex tasks requiring decision-making, communication, and tool usage. They are characterized by:

1. **State Management**
   - Maintain their own state
   - Track task progress
   - Manage context
   - Handle memory

2. **Communication Capabilities**
   - Interact with other agents
   - Share information
   - Coordinate tasks
   - Handle feedback

3. **Tool Integration**
   - Use specialized tools
   - Access external systems
   - Process complex data
   - Handle errors

4. **Decision Making**
   - Make context-aware decisions
   - Adapt to changing conditions
   - Handle uncertainty
   - Manage priorities

Example Implementation:
```python
class SearchAgent(Agent):
    """Agent responsible for information search and retrieval"""
    def __init__(self):
        super().__init__(
            role="Search Specialist",
            goal="Find and retrieve relevant research papers",
            backstory="Expert in academic search and information retrieval"
        )
        self.state = {
            'search_history': [],
            'current_context': None,
            'active_tools': set()
        }
    
    async def execute(self, task: Task) -> str:
        """Execute search and retrieval task"""
        # Complex decision-making and tool usage
        pass
```

### Non-Agentic Nodes
Non-agentic nodes are functional components that handle specific, well-defined tasks without maintaining state or making complex decisions. They are characterized by:

1. **Stateless Operation**
   - No persistent state
   - Pure functions
   - Deterministic output
   - Clear input/output

2. **Focused Functionality**
   - Single responsibility
   - Simple processing
   - No decision-making
   - No tool usage

3. **Integration Points**
   - State transitions
   - Data transformation
   - Error handling
   - Monitoring

Example Implementation:
```python
def process_node(state: ResearchState) -> Dict[str, Any]:
    """Process research documents without agentic behavior"""
    try:
        # Simple, deterministic processing
        updates = {
            'processed_documents': process_documents(state['documents']),
            'status': 'processed'
        }
        return updates
    except Exception as e:
        return {'error': str(e)}
```

## Implementation Details

### 1. Information Processing Pipeline

#### Search and Retrieval Stage
```python
class SearchAgent(Agent):
    """Agent responsible for information search and retrieval"""
    def __init__(self):
        super().__init__(
            role="Search Specialist",
            goal="Find and retrieve relevant research papers",
            backstory="Expert in academic search and information retrieval"
        )
    
    async def execute(self, task: Task) -> str:
        """Execute search and retrieval task"""
        # Implementation details
        pass
```

#### Document Processing Stage
```python
class ProcessingAgent(Agent):
    """Agent responsible for document parsing and processing"""
    def __init__(self):
        super().__init__(
            role="Document Processor",
            goal="Parse and process research documents",
            backstory="Expert in document processing and analysis"
        )
    
    async def execute(self, task: Task) -> str:
        """Execute document processing task"""
        # Implementation details
        pass
```

#### Analysis Stage
```python
class AnalysisAgent(Agent):
    """Agent responsible for content analysis and extraction"""
    def __init__(self):
        super().__init__(
            role="Content Analyst",
            goal="Analyze and extract key information from documents",
            backstory="Expert in research paper analysis and information extraction"
        )
    
    async def execute(self, task: Task) -> str:
        """Execute analysis task"""
        # Implementation details
        pass
```

#### Storage Stage
```python
class StorageAgent(Agent):
    """Agent responsible for storing information in multiple systems"""
    def __init__(self):
        super().__init__(
            role="Storage Manager",
            goal="Store information in appropriate storage systems",
            backstory="Expert in data storage and retrieval systems"
        )
    
    async def execute(self, task: Task) -> str:
        """Execute storage task"""
        # Implementation details
        pass
```

### 2. Workflow Orchestration

#### LangGraph Implementation
```python
class ResearchWorkflow:
    """Orchestrates the research workflow using LangGraph"""
    def __init__(self):
        self.graph = StateGraph(ResearchState)
        self.setup_workflow()
    
    def setup_workflow(self):
        """Setup the research workflow"""
        # Add agent nodes (CrewAI agents)
        self.graph.add_node("search", search_agent_node)
        self.graph.add_node("analyze", analysis_agent_node)
        
        # Add non-agentic nodes
        self.graph.add_node("process", process_node)
        self.graph.add_node("validate", validate_node)
        self.graph.add_node("monitor", monitor_node)
        
        # Add edges
        self.graph.add_edge("search", "process")
        self.graph.add_edge("process", "validate")
        self.graph.add_edge("validate", "analyze")
        self.graph.add_edge("analyze", "monitor")
        
        # Set entry point
        self.graph.set_entry_point("search")
```

#### CrewAI Integration
```python
class ResearchCrew:
    """Manages the research crew of specialized agents"""
    def __init__(self):
        self.setup_crew()
    
    def setup_crew(self):
        """Setup the research crew"""
        self.search_agent = SearchAgent()
        self.processing_agent = ProcessingAgent()
        self.analysis_agent = AnalysisAgent()
        self.storage_agent = StorageAgent()
        
        self.crew = Crew(
            agents=[
                self.search_agent,
                self.processing_agent,
                self.analysis_agent,
                self.storage_agent
            ],
            tasks=[
                Task(description="Search for relevant papers"),
                Task(description="Process retrieved documents"),
                Task(description="Analyze document content"),
                Task(description="Store processed information")
            ]
        )
```

### 3. State Management

#### ResearchState Definition
```python
class ResearchState(TypedDict):
    """Core state for research workflows"""
    # Research Context
    research_question: str
    methodology: str
    current_phase: str
    
    # Document Processing
    processed_papers: List[Dict[str, Any]]
    current_paper: Optional[Dict[str, Any]]
    citation_network: Dict[str, List[str]]
    
    # Analysis State
    findings: List[Dict[str, Any]]
    hypotheses: List[str]
    validation_results: Dict[str, Any]]
    
    # Storage State
    object_storage: Dict[str, Any]
    vector_storage: Dict[str, Any]
    graph_storage: Dict[str, Any]
    fulltext_storage: Dict[str, Any]
    
    # Agent Coordination
    active_agents: List[str]
    agent_states: Dict[str, Dict[str, Any]]
    last_activity: datetime
```

### 4. Storage Integration

#### Multi-Storage System Integration
```python
class StorageManager:
    """Manages multiple storage systems"""
    def __init__(self):
        self.object_storage = ObjectStorage()
        self.vector_storage = VectorStorage()
        self.graph_storage = GraphStorage()
        self.fulltext_storage = FulltextStorage()
    
    async def store(self, data: Dict[str, Any]) -> None:
        """Store data in appropriate systems"""
        # Store in object storage
        await self.object_storage.store(data)
        
        # Store in vector storage
        await self.vector_storage.store(data)
        
        # Store in graph storage
        await self.graph_storage.store(data)
        
        # Store in fulltext storage
        await self.fulltext_storage.store(data)
```

## Best Practices

### 1. Agent Design
- Keep agents focused and single-purpose
- Implement proper error handling
- Use async/await for I/O operations
- Maintain clear agent roles and responsibilities
- Ensure proper state management
- Implement robust communication patterns

### 2. Non-Agentic Node Design
- Keep nodes simple and focused
- Ensure stateless operation
- Implement clear error handling
- Use type hints for clarity
- Document input/output expectations
- Avoid complex decision-making

### 3. State Management
- Use TypedDict for type safety
- Keep state structure flat
- Implement proper state validation
- Use efficient data structures

### 4. Workflow Design
- Design clear workflow stages
- Implement proper error handling
- Use conditional edges for flexibility
- Monitor workflow execution

### 5. Storage Integration
- Implement proper error handling
- Use connection pooling
- Monitor storage performance
- Implement retry mechanisms

## References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Research Assistant Architecture](research_agent_architecture.md) 