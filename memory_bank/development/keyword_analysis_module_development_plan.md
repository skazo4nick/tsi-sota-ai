# Keyword Analysis Module Development Plan
**Project**: Research Analytics Application for "Agentic AI in SCM" SLR  
**Date**: June 4, 2025  
**Status**: Development Plan and Architecture  

## 1. Executive Summary

This document outlines the comprehensive development plan for implementing the Keyword Analysis Module as specified in the technical requirements. The module will be integrated into the existing TSI-SOTA-AI architecture while maintaining modularity and leveraging proven components.

## 2. Feasibility Analysis Report

### 2.1 API Integration Assessment

**✅ EXCELLENT COVERAGE:**
- **Semantic Scholar API**: Production-ready client with 561+ lines of code
- **CORE API**: Fully implemented in both standalone and integrated versions
- **OpenAlex API**: Enhanced with pyalex integration per ADR decisions
- **arXiv API**: Base implementation exists, may need completion

**Result**: 90% API coverage already available with proven functionality.

### 2.2 Data Processing & Architecture Alignment

**✅ PERFECT ALIGNMENT:**
- **ConfigManager**: YAML-based configuration matches requirement 4.6.1
- **DataAcquirer**: Multi-source data collection with standardized output
- **Storage Infrastructure**: B2, Qdrant, Meilisearch exceeds requirements
- **Data Standardization**: All APIs output consistent DataFrame format

**Result**: Core infrastructure fully supports requirements with no modifications needed.

### 2.3 Technical Stack Compatibility

**✅ REQUIREMENTS MET:**
```python
# Required vs Available
✓ Python 3.9+
✓ pandas, numpy, scikit-learn
✓ requests
✓ PyYAML configuration
✓ matplotlib, seaborn (in use)

# Need to Add:
+ sentence-transformers (BGE-M3)
+ umap-learn
+ nltk/spaCy for advanced NLP
+ yake for keyword extraction
```

### 2.4 Existing Analysis Capabilities

**✅ STRONG FOUNDATION:**
- `notebooks/1_keywords_analysis.ipynb`: Established keyword analysis patterns
- `notebooks/2_publications_clustering.ipynb`: Clustering workflows
- `data/abstract_embeddings.npy`: Evidence of embedding processing
- Proven visualization patterns across notebooks

**Result**: 80% of analysis patterns already implemented and tested.

## 3. Architectural Decision: Integrated Module Approach

**Selected Strategy**: Create integrated module components that can be:
1. Used as Python modules for programmatic access
2. Imported into Jupyter notebooks for interactive analysis
3. Orchestrated via CLI for batch processing

**Rationale**:
- Leverages existing proven infrastructure
- Maintains code reusability across use cases
- Provides flexibility for researcher workflow preferences
- Enables easy testing and incremental development

## 4. Implementation Architecture

### 4.1 Module Structure

```
slr_core/
├── keyword_analysis/
│   ├── __init__.py
│   ├── keyword_extractor.py     # API & NLP-based keyword extraction
│   ├── semantic_analyzer.py     # BGE-M3 embeddings & clustering  
│   ├── temporal_analyzer.py     # Time-series trend analysis
│   └── visualizer.py           # Plotting and visualization
├── api_clients.py              # [EXISTING] Enhanced
├── data_acquirer.py            # [EXISTING] Enhanced
└── config_manager.py           # [EXISTING] Enhanced

notebooks/
├── keyword_analysis_comprehensive.ipynb  # [NEW] Main analysis notebook
├── 1_keywords_analysis.ipynb            # [EXISTING] Enhanced
└── 2_publications_clustering.ipynb      # [EXISTING] Enhanced
```

### 4.2 Core Components Design

#### A. KeywordExtractor Class
```python
class KeywordExtractor:
    """Handles API keywords and NLP-based extraction"""
    
    def extract_api_keywords(self, publications_df: pd.DataFrame) -> pd.DataFrame
    def extract_nlp_keywords(self, texts: List[str], method: str = 'tfidf') -> Dict
    def extract_with_yake(self, texts: List[str]) -> List[Dict]
    def extract_with_rake(self, texts: List[str]) -> List[Dict]
    def calculate_keyword_frequencies(self, keywords_data: Dict) -> pd.DataFrame
```

#### B. SemanticAnalyzer Class  
```python
class SemanticAnalyzer:
    """BGE-M3 embeddings and clustering"""
    
    def load_embedding_model(self, model_name: str = 'BAAI/bge-m3') -> SentenceTransformer
    def generate_embeddings(self, texts: List[str]) -> np.ndarray
    def perform_clustering(self, embeddings: np.ndarray, method: str = 'kmeans') -> Dict
    def reduce_dimensions(self, embeddings: np.ndarray, method: str = 'umap') -> np.ndarray
```

#### C. TemporalAnalyzer Class
```python
class TemporalAnalyzer:
    """Time-series analysis and trend tracking"""
    
    def analyze_keyword_trends(self, keywords_df: pd.DataFrame) -> pd.DataFrame
    def calculate_yearly_distributions(self, data: pd.DataFrame) -> Dict
    def identify_emerging_keywords(self, trends_data: pd.DataFrame) -> List[str]
    def track_framework_mentions(self, publications: pd.DataFrame) -> Dict
```

#### D. Visualizer Class
```python
class Visualizer:
    """Plotting and export functionality"""
    
    def plot_temporal_trends(self, trends_data: pd.DataFrame) -> plt.Figure
    def plot_cluster_visualization(self, embeddings: np.ndarray, clusters: np.ndarray) -> plt.Figure
    def plot_thematic_evolution(self, cluster_data: pd.DataFrame) -> plt.Figure
    def export_visualizations(self, figures: List[plt.Figure], output_dir: str) -> None
```

## 5. Development Phases

### Phase 1: Foundation Setup (1-2 days)
**Deliverables**:
- Enhanced requirements.txt with new dependencies
- Updated configuration files
- Basic module structure creation
- Integration tests with existing DataAcquirer

**Tasks**:
1. Add required dependencies to requirements.txt
2. Enhance slr_config.yaml with keyword analysis settings
3. Create module structure in slr_core/keyword_analysis/
4. Implement base classes with stub methods
5. Test integration with existing API clients

### Phase 2: Core Implementation (3-4 days)
**Deliverables**:
- Complete KeywordExtractor implementation
- BGE-M3 integration and SemanticAnalyzer
- Basic temporal analysis functionality
- Unit tests for all core functions

**Tasks**:
1. Implement API keyword extraction from existing standardized data
2. Add NLP-based extraction (TF-IDF, RAKE, YAKE)
3. Integrate BGE-M3 model with local caching
4. Implement K-means and DBSCAN clustering
5. Create temporal trend analysis functions

### Phase 3: Visualization and Integration (2-3 days)
**Deliverables**:
- Complete visualization suite
- Comprehensive Jupyter notebook
- Enhanced existing notebooks
- End-to-end integration testing

**Tasks**:
1. Implement all required visualization functions
2. Create comprehensive analysis notebook
3. Enhance existing notebooks with new capabilities
4. Test complete pipeline with real data
5. Validate outputs against requirements

### Phase 4: Testing and Documentation (1-2 days)
**Deliverables**:
- Comprehensive test suite
- Updated documentation
- Usage examples and tutorials
- Performance optimization

**Tasks**:
1. Create comprehensive unit and integration tests
2. Update README with new functionality
3. Create usage examples and tutorials
4. Performance testing and optimization
5. Final validation against acceptance criteria

## 6. Testing Strategy

### 6.1 Limited Query Testing
**Approach**: Use focused queries that return 1-3 articles for rapid iteration:

```python
# Test queries for development
TEST_QUERIES = [
    "LangGraph supply chain",  # Specific framework - likely 1-2 results
    "YAKE keyword extraction SCM",  # Niche topic - 2-3 results
    "BGE-M3 embeddings logistics"  # Very specific - 1 result expected
]
```

### 6.2 Progressive Testing Levels
1. **Unit Tests**: Individual component functionality
2. **Integration Tests**: Module interactions with existing infrastructure  
3. **Pipeline Tests**: End-to-end workflow validation
4. **Performance Tests**: Large dataset handling capabilities

## 7. Enhanced Configuration

### 7.1 Extended slr_config.yaml
```yaml
keyword_analysis:
  nlp:
    methods: ['tfidf', 'rake', 'yake']
    tfidf:
      ngram_range: [1, 3]
      max_features: 1000
      min_df: 2
      max_df: 0.85
    rake:
      min_length: 1
      max_length: 4
    yake:
      language: "en"
      max_ngram_size: 3
      deduplication_threshold: 0.7
      num_keywords: 20
  
  embeddings:
    model: 'BAAI/bge-m3'
    cache_dir: './data/embeddings_cache'
    batch_size: 32
    device: 'cpu'  # or 'cuda' if available
  
  clustering:
    methods: ['kmeans', 'dbscan']
    kmeans:
      n_clusters: 10
      random_state: 42
    dbscan:
      eps: 0.5
      min_samples: 5
  
  visualization:
    output_dir: './data/visualizations'
    formats: ['png', 'svg']
    dpi: 300
    figsize: [12, 8]

# Test search queries for development
test_search_queries:
  limited_scope:
    - "LangGraph supply chain"
    - "YAKE keyword extraction SCM" 
    - "BGE-M3 embeddings logistics"
  timeframe:
    start: "2023-01-01"
    end: "2024-12-31"
```

## 8. Expected Deliverables

### 8.1 Code Components
- **slr_core/keyword_analysis/** - Complete module package (estimated 800+ lines)
- **Enhanced notebooks** - Interactive analysis capabilities
- **Updated configuration** - Extended YAML settings
- **Comprehensive tests** - 90%+ code coverage

### 8.2 Analysis Outputs
- **Keyword frequency tables** - CSV and Excel formats
- **Temporal trend visualizations** - PNG/SVG exports
- **Cluster analysis results** - Labeled thematic groups
- **Embedding visualizations** - 2D/3D scatter plots
- **Thematic evolution charts** - Publication distribution over time

### 8.3 Documentation
- **Technical documentation** - API reference and usage guide
- **Tutorial notebooks** - Step-by-step analysis workflows
- **Configuration guide** - Parameter explanations and tuning
- **Performance benchmarks** - Scaling characteristics and limits

## 9. Risk Mitigation

### 9.1 Technical Risks
- **Model Size**: BGE-M3 model storage managed via existing B2 infrastructure
- **Performance**: Leverage existing Qdrant vector storage for embeddings
- **Dependencies**: Pin versions in requirements.txt and test compatibility

### 9.2 Integration Risks  
- **API Changes**: Use established, proven API client patterns
- **Data Format**: Build on existing standardized output format
- **Configuration**: Extend proven ConfigManager approach

### 9.3 Quality Risks
- **Reproducibility**: Use fixed random seeds and version-pinned dependencies
- **Accuracy**: Validate outputs against existing keyword analysis notebook
- **Maintainability**: Follow established code patterns and documentation standards

## 10. Success Metrics

### 10.1 Functional Success
- [ ] Successfully extracts keywords from all 4 API sources
- [ ] Generates BGE-M3 embeddings for abstracts
- [ ] Performs semantic clustering with interpretable results
- [ ] Produces all required visualizations 
- [ ] Processes test queries in <30 seconds
- [ ] Handles 100+ publications without memory issues

### 10.2 Integration Success
- [ ] Seamlessly imports into existing notebooks
- [ ] Works with current ConfigManager and DataAcquirer
- [ ] Maintains backward compatibility with existing code
- [ ] Follows established error handling patterns

### 10.3 Quality Success
- [ ] 90%+ unit test coverage
- [ ] All integration tests passing
- [ ] Code follows PEP 8 standards
- [ ] Documentation complete and accurate
- [ ] Performance meets requirements

## 11. Next Steps

**Immediate Actions**:
1. ✅ Approve development plan and architecture
2. ⏳ Begin Phase 1: Foundation setup
3. ⏳ Set up development environment with new dependencies
4. ⏳ Create initial module structure
5. ⏳ Implement first integration test

**Success Dependencies**:
- Access to existing API credentials for testing
- Sufficient system resources for BGE-M3 model
- Approval for new dependency additions

This development plan provides a robust foundation for implementing the keyword analysis module while maximizing reuse of existing, proven infrastructure and maintaining high code quality standards.
