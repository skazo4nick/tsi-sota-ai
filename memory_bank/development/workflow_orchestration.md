# Workflow Orchestration Documentation

## Overview
This document details the workflow orchestration system, including workflow management, state transitions, and error handling for the Research Assistant's multi-agent system.

## Version Information
- Version: 1.0.0
- Last Updated: 2024-04-28
- Status: Active Development

## Workflow Management

### 1. Workflow Definition
```python
class ResearchWorkflow:
    def __init__(self, name, description, agents):
        self.name = name
        self.description = description
        self.agents = agents
        self.states = {}
        self.transitions = {}
        self.current_state = None
        
    def add_state(self, state_name, state_handler):
        self.states[state_name] = state_handler
        
    def add_transition(self, from_state, to_state, condition):
        self.transitions[(from_state, to_state)] = condition
        
    async def execute(self, initial_state):
        self.current_state = initial_state
        while self.current_state:
            handler = self.states[self.current_state]
            next_state = await handler()
            if next_state in self.transitions:
                self.current_state = next_state
            else:
                break
```

### 2. State Management
```python
class WorkflowState:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data or {}
        self.timestamp = datetime.now()
        
    def update(self, new_data):
        self.data.update(new_data)
        self.timestamp = datetime.now()
        
    def to_dict(self):
        return {
            'name': self.name,
            'data': self.data,
            'timestamp': self.timestamp.isoformat()
        }
```

## Workflow Types

### 1. Literature Review Workflow
```python
class LiteratureReviewWorkflow(ResearchWorkflow):
    def __init__(self, agents):
        super().__init__(
            name="Literature Review",
            description="Systematic review of scientific literature",
            agents=agents
        )
        
        # Define states
        self.add_state("search", self._search_state)
        self.add_state("analyze", self._analyze_state)
        self.add_state("synthesize", self._synthesize_state)
        self.add_state("document", self._document_state)
        
        # Define transitions
        self.add_transition("search", "analyze", lambda: True)
        self.add_transition("analyze", "synthesize", lambda: True)
        self.add_transition("synthesize", "document", lambda: True)
```

### 2. Experimental Workflow
```python
class ExperimentalWorkflow(ResearchWorkflow):
    def __init__(self, agents):
        super().__init__(
            name="Experimental",
            description="Experimental design and execution",
            agents=agents
        )
        
        # Define states
        self.add_state("design", self._design_state)
        self.add_state("execute", self._execute_state)
        self.add_state("analyze", self._analyze_state)
        self.add_state("validate", self._validate_state)
        
        # Define transitions
        self.add_transition("design", "execute", lambda: True)
        self.add_transition("execute", "analyze", lambda: True)
        self.add_transition("analyze", "validate", lambda: True)
```

## Error Handling

### 1. Workflow Error Management
```python
class WorkflowError(Exception):
    def __init__(self, message, state, context):
        self.message = message
        self.state = state
        self.context = context
        super().__init__(self.message)

class WorkflowErrorHandler:
    def __init__(self, workflow):
        self.workflow = workflow
        self.error_log = []
        
    async def handle_error(self, error):
        self.error_log.append({
            'timestamp': datetime.now(),
            'error': str(error),
            'state': error.state,
            'context': error.context
        })
        
        # Recovery strategies
        if isinstance(error, StateTransitionError):
            await self._handle_transition_error(error)
        elif isinstance(error, AgentError):
            await self._handle_agent_error(error)
        else:
            await self._handle_generic_error(error)
```

### 2. State Recovery
```python
class StateRecovery:
    def __init__(self, workflow):
        self.workflow = workflow
        self.checkpoints = {}
        
    async def create_checkpoint(self, state_name):
        self.checkpoints[state_name] = {
            'state': self.workflow.current_state,
            'data': self.workflow.state_data,
            'timestamp': datetime.now()
        }
        
    async def restore_checkpoint(self, state_name):
        if state_name in self.checkpoints:
            checkpoint = self.checkpoints[state_name]
            self.workflow.current_state = checkpoint['state']
            self.workflow.state_data = checkpoint['data']
            return True
        return False
```

## Workflow Monitoring

### 1. Performance Metrics
```python
class WorkflowMetrics:
    def __init__(self):
        self.metrics = {
            'execution_time': {},
            'state_transitions': {},
            'error_count': 0,
            'success_rate': 0.0
        }
        
    def record_transition(self, from_state, to_state, duration):
        if from_state not in self.metrics['state_transitions']:
            self.metrics['state_transitions'][from_state] = {}
        self.metrics['state_transitions'][from_state][to_state] = duration
        
    def calculate_success_rate(self):
        total = len(self.metrics['state_transitions'])
        if total == 0:
            return 0.0
        successful = sum(1 for transitions in self.metrics['state_transitions'].values()
                        if any(transitions.values()))
        return successful / total
```

### 2. Monitoring Dashboard
```python
class WorkflowMonitor:
    def __init__(self, workflow):
        self.workflow = workflow
        self.metrics = WorkflowMetrics()
        self.alerts = []
        
    async def monitor_workflow(self):
        while True:
            current_state = self.workflow.current_state
            state_data = self.workflow.state_data
            
            # Record metrics
            self.metrics.record_transition(
                self.workflow.previous_state,
                current_state,
                datetime.now() - self.workflow.last_transition_time
            )
            
            # Check for anomalies
            if self._detect_anomaly(current_state, state_data):
                await self._raise_alert(current_state, state_data)
                
            await asyncio.sleep(1)  # Monitor every second
```

## Integration with LangGraph

### 1. LangGraph Workflow Definition
```python
from langgraph.graph import Graph, StateGraph

class LangGraphWorkflow:
    def __init__(self, workflow):
        self.workflow = workflow
        self.graph = StateGraph()
        
    def build_graph(self):
        # Add nodes for each state
        for state_name in self.workflow.states:
            self.graph.add_node(state_name, self.workflow.states[state_name])
            
        # Add edges for transitions
        for (from_state, to_state), condition in self.workflow.transitions.items():
            self.graph.add_edge(from_state, to_state, condition)
            
        return self.graph.compile()
```

### 2. State Management with LangGraph
```python
class LangGraphState:
    def __init__(self, workflow_state):
        self.workflow_state = workflow_state
        self.messages = []
        
    def update(self, message):
        self.messages.append(message)
        self.workflow_state.update({'messages': self.messages})
        
    def to_dict(self):
        return {
            'workflow_state': self.workflow_state.to_dict(),
            'messages': self.messages
        }
```

## References
- [Research Agent Architecture](research_agent_architecture.md)
- [Agent System](agent_system.md)
- [State Management System](state_management.md) 