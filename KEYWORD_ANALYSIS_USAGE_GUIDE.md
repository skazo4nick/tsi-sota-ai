# Keyword Analysis Module Usage Guide

## Quick Start

### 1. Basic Keyword Extraction

```python
from slr_core.keyword_analysis import KeywordExtractor
from slr_core.config_manager import ConfigManager
import pandas as pd

# Initialize
config = ConfigManager()
extractor = KeywordExtractor(config)

# Load your publication data
publications_df = pd.read_csv('your_publications.csv')

# Extract API-provided keywords
api_keywords = extractor.extract_api_keywords(publications_df)
print(f"Extracted {len(api_keywords)} API keywords")

# Extract NLP keywords from abstracts
abstracts = publications_df['abstract'].tolist()
nlp_keywords = extractor.extract_nlp_keywords(abstracts, method='tfidf')
print(f"Extracted {len(nlp_keywords['keywords'])} NLP keywords")
```

### 2. Semantic Analysis with Clustering

```python
from slr_core.keyword_analysis import SemanticAnalyzer

# Initialize semantic analyzer
analyzer = SemanticAnalyzer(config)

# Generate embeddings (requires BGE-M3 model download on first use)
embeddings = analyzer.generate_embeddings(abstracts[:50])  # Limit for demo

if embeddings is not None:
    # Perform clustering
    clusters = analyzer.perform_clustering(embeddings, method='kmeans')
    print(f"Created {clusters['n_clusters']} clusters")
    print(f"Silhouette score: {clusters['silhouette_score']:.3f}")
```

### 3. Temporal Trend Analysis

```python
from slr_core.keyword_analysis import TemporalAnalyzer

# Initialize temporal analyzer
temporal = TemporalAnalyzer(config.config)

# Prepare data
publications_list = publications_df.to_dict('records')
keywords_dict = {}

# Aggregate keywords from your data
for pub in publications_list:
    if 'keywords' in pub and pub['keywords']:
        for kw in pub['keywords']:
            if kw in keywords_dict:
                keywords_dict[kw]['frequency'] += 1
            else:
                keywords_dict[kw] = {'frequency': 1, 'importance': 0.5}

# Analyze trends
trends = temporal.analyze_keyword_trends(publications_list, keywords_dict)
print(f"Analyzed trends for {len(trends['individual_trends'])} keywords")
```

### 4. Visualization

```python
from slr_core.keyword_analysis import Visualizer

# Initialize visualizer
visualizer = Visualizer(config.config)

# Create keyword frequency dictionary
keyword_freqs = {}
for pub in publications_list:
    if 'keywords' in pub and pub['keywords']:
        for kw in pub['keywords']:
            keyword_freqs[kw] = keyword_freqs.get(kw, 0) + 1

# Create word cloud
wordcloud_result = visualizer.create_word_cloud(
    keyword_freqs, 
    title="Research Keywords Word Cloud"
)

# Create frequency plot
freq_plot_result = visualizer.plot_keyword_frequencies(
    keyword_freqs,
    title="Top Keywords Frequency"
)

print(f"Visualizations created: {wordcloud_result}, {freq_plot_result}")
```

## Advanced Usage

### Complete Analysis Pipeline

```python
from slr_core.keyword_analysis import *
from slr_core.config_manager import ConfigManager
import pandas as pd

def analyze_publications(publications_df):
    """Complete keyword analysis pipeline"""
    
    # Initialize all components
    config = ConfigManager()
    extractor = KeywordExtractor(config)
    analyzer = SemanticAnalyzer(config)
    temporal = TemporalAnalyzer(config.config)
    visualizer = Visualizer(config.config)
    
    results = {}
    
    # 1. Extract keywords
    print("Extracting keywords...")
    results['api_keywords'] = extractor.extract_api_keywords(publications_df)
    
    abstracts = publications_df['abstract'].dropna().tolist()[:100]  # Limit for performance
    results['nlp_keywords'] = extractor.extract_nlp_keywords(abstracts, method='all')
    
    # 2. Semantic analysis
    print("Performing semantic analysis...")
    embeddings = analyzer.generate_embeddings(abstracts[:50])
    if embeddings is not None:
        results['clusters'] = analyzer.perform_clustering(embeddings)
        results['reduced_embeddings'] = analyzer.reduce_dimensions(embeddings, method='umap')
    
    # 3. Temporal analysis
    print("Analyzing temporal trends...")
    publications_list = publications_df.to_dict('records')
    
    # Prepare keyword data
    keywords_dict = {}
    for idx, row in publications_df.iterrows():
        if 'keywords' in row and row['keywords'] is not None:
            keywords = row['keywords'] if isinstance(row['keywords'], list) else [row['keywords']]
            for kw in keywords:
                if kw in keywords_dict:
                    keywords_dict[kw]['frequency'] += 1
                else:
                    keywords_dict[kw] = {'frequency': 1, 'importance': 0.5}
    
    results['trends'] = temporal.analyze_keyword_trends(publications_list, keywords_dict)
    results['lifecycle'] = temporal.analyze_keyword_lifecycle(publications_list, keywords_dict)
    
    # 4. Create visualizations
    print("Creating visualizations...")
    keyword_freqs = {kw: data['frequency'] for kw, data in keywords_dict.items()}
    
    results['wordcloud'] = visualizer.create_word_cloud(keyword_freqs)
    results['frequency_plot'] = visualizer.plot_keyword_frequencies(keyword_freqs)
    
    return results

# Usage
# publications_df = pd.read_csv('your_data.csv')
# analysis_results = analyze_publications(publications_df)
```

### Configuration Customization

```python
# Customize TF-IDF parameters
config.config['keyword_analysis']['nlp']['tfidf'] = {
    'ngram_range': [1, 3],
    'max_features': 1000,
    'min_df': 2,
    'max_df': 0.85
}

# Customize clustering parameters
config.config['semantic_analysis']['clustering']['kmeans'] = {
    'n_clusters': 15,
    'random_state': 42
}

# Customize visualization
config.config['visualization']['wordcloud'] = {
    'max_words': 100,
    'width': 1200,
    'height': 600,
    'background_color': 'white',
    'colormap': 'viridis'
}
```

## Performance Tips

1. **Limit Dataset Size**: For initial testing, limit to 50-100 publications
2. **Use Caching**: Enable embedding caching for repeated analysis
3. **Batch Processing**: Process large datasets in smaller batches
4. **GPU Acceleration**: Use GPU if available for embeddings

## Common Issues & Solutions

### Issue: BGE-M3 Model Download Slow
**Solution**: The model downloads automatically on first use (~2GB). Be patient or pre-download.

### Issue: Memory Issues with Large Datasets
**Solution**: Process in smaller batches or increase available memory.

### Issue: Empty Results
**Solution**: Check that your data has the expected columns ('keywords', 'abstract', etc.).

## Data Format Requirements

Your publications DataFrame should have these columns:
- `title`: Publication title
- `abstract`: Publication abstract
- `keywords`: Keywords (list or comma-separated string)
- `publication_date`: Publication date
- `doi`: DOI (optional)
- `source`: Data source (optional)

## Running Tests

```bash
# Run the basic integration test
python integration_test.py

# Run comprehensive integration tests
python test_comprehensive_integration.py

# Test specific components
python test_keyword_analysis.py
```

## Need Help?

- Check the comprehensive test files for more examples
- Review the configuration in `config/slr_config.yaml`
- See the development plan in `memory_bank/development/keyword_analysis_module_development_plan.md`
