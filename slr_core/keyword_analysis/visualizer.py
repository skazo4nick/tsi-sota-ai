"""
Visualization Module for Keyword Analysis
Handles plotting and visualization of all keyword analysis results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import warnings
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime
import logging
from collections import Counter
import colorsys

warnings.filterwarnings('ignore')
plt.style.use('default')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class Visualizer:
    """
    Creates visualizations for keyword analysis results.
    
    Features:
    - Word clouds and frequency plots
    - Temporal trend visualizations
    - Semantic clustering plots
    - Lifecycle analysis charts
    - Comparative analysis visualizations
    - Interactive dashboards
    - Export capabilities
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Visualizer.
        
        Args:
            config: Configuration dictionary containing visualization settings
        """
        self.config = config
        self.viz_config = config.get('visualization', {})
        
        # Visualization parameters
        self.figure_size = tuple(self.viz_config.get('figure_size', [12, 8]))
        self.dpi = self.viz_config.get('dpi', 300)
        self.style = self.viz_config.get('style', 'seaborn-v0_8')
        self.color_palette = self.viz_config.get('color_palette', 'husl')
        self.save_format = self.viz_config.get('save_format', 'png')
        
        # Interactive visualization settings
        self.interactive = self.viz_config.get('interactive', True)
        self.plotly_theme = self.viz_config.get('plotly_theme', 'plotly_white')
        
        # Word cloud settings
        self.wordcloud_config = self.viz_config.get('wordcloud', {
            'max_words': 100,
            'width': 800,
            'height': 400,
            'background_color': 'white',
            'colormap': 'viridis'
        })
        
        # Set matplotlib style
        try:
            plt.style.use(self.style)
        except:
            plt.style.use('default')
        
        logger.info("Visualizer initialized")
    
    def create_word_cloud(self, keywords: Dict[str, int], title: str = "Keyword Word Cloud", 
                         output_path: Optional[str] = None) -> str:
        """
        Create a word cloud visualization.
        
        Args:
            keywords: Dictionary of keywords and their frequencies
            title: Title for the visualization
            output_path: Optional path to save the visualization
            
        Returns:
            Path to the saved visualization or base64 encoded image
        """
        logger.info(f"Creating word cloud: {title}")
        
        try:
            if not keywords:
                raise ValueError("No keywords provided for word cloud")
            
            # Create WordCloud object
            wordcloud = WordCloud(
                width=self.wordcloud_config['width'],
                height=self.wordcloud_config['height'],
                background_color=self.wordcloud_config['background_color'],
                max_words=self.wordcloud_config['max_words'],
                colormap=self.wordcloud_config['colormap'],
                relative_scaling=0.5,
                random_state=42
            ).generate_from_frequencies(keywords)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.axis('off')
            
            plt.tight_layout()
            
            # Save or return the plot
            if output_path:
                plt.savefig(output_path, format=self.save_format, bbox_inches='tight')
                plt.close()
                return output_path
            else:
                plt.show()
                return "displayed"
                
        except Exception as e:
            logger.error(f"Error creating word cloud: {str(e)}")
            raise
    
    def plot_keyword_frequencies(self, keywords: Dict[str, int], top_n: int = 20, 
                                title: str = "Top Keywords by Frequency", 
                                output_path: Optional[str] = None) -> str:
        """
        Create a bar plot of keyword frequencies.
        
        Args:
            keywords: Dictionary of keywords and their frequencies
            top_n: Number of top keywords to display
            title: Title for the visualization
            output_path: Optional path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        logger.info(f"Creating keyword frequency plot: {title}")
        
        try:
            if not keywords:
                raise ValueError("No keywords provided for frequency plot")
            
            # Get top keywords
            top_keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:top_n])
            
            if self.interactive:
                return self._create_interactive_frequency_plot(top_keywords, title, output_path)
            else:
                return self._create_static_frequency_plot(top_keywords, title, output_path)
                
        except Exception as e:
            logger.error(f"Error creating frequency plot: {str(e)}")
            raise
    
    def plot_temporal_trends(self, trend_data: Dict[str, Any], top_keywords: int = 10,
                           title: str = "Keyword Temporal Trends", 
                           output_path: Optional[str] = None) -> str:
        """
        Create temporal trend visualizations.
        
        Args:
            trend_data: Temporal trend analysis results
            top_keywords: Number of top keywords to plot
            title: Title for the visualization
            output_path: Optional path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        logger.info(f"Creating temporal trends plot: {title}")
        
        try:
            if 'individual_trends' not in trend_data:
                raise ValueError("No individual trends data provided")
            
            # Select top keywords by significance
            trends = trend_data['individual_trends']
            top_trends = sorted(trends.items(), 
                              key=lambda x: abs(x[1]['trend_slope']), 
                              reverse=True)[:top_keywords]
            
            if self.interactive:
                return self._create_interactive_trends_plot(top_trends, title, output_path)
            else:
                return self._create_static_trends_plot(top_trends, title, output_path)
                
        except Exception as e:
            logger.error(f"Error creating temporal trends plot: {str(e)}")
            raise
    
    def plot_semantic_clusters(self, cluster_data: Dict[str, Any], 
                             title: str = "Semantic Keyword Clusters",
                             output_path: Optional[str] = None) -> str:
        """
        Create semantic clustering visualization.
        
        Args:
            cluster_data: Semantic clustering analysis results
            title: Title for the visualization
            output_path: Optional path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        logger.info(f"Creating semantic clusters plot: {title}")
        
        try:
            if 'embeddings_2d' not in cluster_data or 'cluster_labels' not in cluster_data:
                raise ValueError("Missing clustering data for visualization")
            
            embeddings_2d = np.array(cluster_data['embeddings_2d'])
            cluster_labels = cluster_data['cluster_labels']
            keywords = cluster_data.get('keywords', [f"kw_{i}" for i in range(len(embeddings_2d))])
            
            if self.interactive:
                return self._create_interactive_cluster_plot(embeddings_2d, cluster_labels, keywords, title, output_path)
            else:
                return self._create_static_cluster_plot(embeddings_2d, cluster_labels, keywords, title, output_path)
                
        except Exception as e:
            logger.error(f"Error creating semantic clusters plot: {str(e)}")
            raise
    
    def plot_lifecycle_analysis(self, lifecycle_data: Dict[str, Any],
                               title: str = "Keyword Lifecycle Analysis",
                               output_path: Optional[str] = None) -> str:
        """
        Create keyword lifecycle visualization.
        
        Args:
            lifecycle_data: Lifecycle analysis results
            title: Title for the visualization
            output_path: Optional path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        logger.info(f"Creating lifecycle analysis plot: {title}")
        
        try:
            if 'individual_lifecycles' not in lifecycle_data:
                raise ValueError("No lifecycle data provided")
            
            lifecycles = lifecycle_data['individual_lifecycles']
            
            if self.interactive:
                return self._create_interactive_lifecycle_plot(lifecycles, title, output_path)
            else:
                return self._create_static_lifecycle_plot(lifecycles, title, output_path)
                
        except Exception as e:
            logger.error(f"Error creating lifecycle analysis plot: {str(e)}")
            raise
    
    def plot_comparative_analysis(self, comparative_data: Dict[str, Any],
                                 title: str = "Time Period Comparison",
                                 output_path: Optional[str] = None) -> str:
        """
        Create comparative analysis visualization.
        
        Args:
            comparative_data: Comparative analysis results
            title: Title for the visualization
            output_path: Optional path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        logger.info(f"Creating comparative analysis plot: {title}")
        
        try:
            if 'period_data' not in comparative_data:
                raise ValueError("No period data provided for comparison")
            
            period_data = comparative_data['period_data']
            
            if self.interactive:
                return self._create_interactive_comparison_plot(period_data, title, output_path)
            else:
                return self._create_static_comparison_plot(period_data, title, output_path)
                
        except Exception as e:
            logger.error(f"Error creating comparative analysis plot: {str(e)}")
            raise
    
    def create_dashboard(self, analysis_results: Dict[str, Any], 
                        output_path: Optional[str] = None) -> str:
        """
        Create an interactive dashboard with all visualizations.
        
        Args:
            analysis_results: Complete analysis results
            output_path: Optional path to save the dashboard
            
        Returns:
            Path to the saved dashboard
        """
        logger.info("Creating comprehensive dashboard")
        
        try:
            # Create subplots
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=['Keyword Frequencies', 'Temporal Trends', 
                              'Semantic Clusters', 'Lifecycle Analysis',
                              'Time Period Comparison', 'Summary Statistics'],
                specs=[[{"type": "bar"}, {"type": "scatter"}],
                       [{"type": "scatter"}, {"type": "scatter"}],
                       [{"type": "bar"}, {"type": "table"}]]
            )
            
            # Add frequency plot
            if 'keyword_frequencies' in analysis_results:
                self._add_frequency_subplot(fig, analysis_results['keyword_frequencies'], 1, 1)
            
            # Add temporal trends
            if 'temporal_analysis' in analysis_results:
                self._add_trends_subplot(fig, analysis_results['temporal_analysis'], 1, 2)
            
            # Add semantic clusters
            if 'semantic_analysis' in analysis_results:
                self._add_clusters_subplot(fig, analysis_results['semantic_analysis'], 2, 1)
            
            # Add lifecycle analysis
            if 'lifecycle_analysis' in analysis_results:
                self._add_lifecycle_subplot(fig, analysis_results['lifecycle_analysis'], 2, 2)
            
            # Add comparative analysis
            if 'comparative_analysis' in analysis_results:
                self._add_comparison_subplot(fig, analysis_results['comparative_analysis'], 3, 1)
            
            # Add summary table
            self._add_summary_table(fig, analysis_results, 3, 2)
            
            # Update layout
            fig.update_layout(
                height=1200,
                title_text="Keyword Analysis Dashboard",
                title_x=0.5,
                showlegend=True,
                template=self.plotly_theme
            )
            
            # Save or show the dashboard
            if output_path:
                fig.write_html(output_path)
                return output_path
            else:
                fig.show()
                return "displayed"
                
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            raise
    
    def _create_interactive_frequency_plot(self, keywords: Dict[str, int], title: str, 
                                         output_path: Optional[str]) -> str:
        """Create interactive frequency plot using Plotly."""
        keywords_list = list(keywords.keys())
        frequencies = list(keywords.values())
        
        fig = go.Figure(data=[
            go.Bar(x=keywords_list, y=frequencies, 
                  text=frequencies, textposition='auto',
                  marker_color=px.colors.qualitative.Set3)
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Keywords",
            yaxis_title="Frequency",
            template=self.plotly_theme,
            height=600
        )
        
        fig.update_layout(xaxis_tickangle=45)
        
        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            fig.show()
            return "displayed"
    
    def _create_static_frequency_plot(self, keywords: Dict[str, int], title: str, 
                                    output_path: Optional[str]) -> str:
        """Create static frequency plot using matplotlib."""
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        keywords_list = list(keywords.keys())
        frequencies = list(keywords.values())
        
        bars = ax.bar(keywords_list, frequencies, color=sns.color_palette(self.color_palette, len(keywords_list)))
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Keywords', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, format=self.save_format, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.show()
            return "displayed"
    
    def _create_interactive_trends_plot(self, trends: List[Tuple], title: str, 
                                      output_path: Optional[str]) -> str:
        """Create interactive trends plot using Plotly."""
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        
        for i, (keyword, trend_data) in enumerate(trends):
            if 'monthly_data' in trend_data:
                monthly_data = trend_data['monthly_data']
                dates = list(monthly_data.keys())
                values = list(monthly_data.values())
                
                fig.add_trace(go.Scatter(
                    x=dates, y=values,
                    mode='lines+markers',
                    name=keyword,
                    line=dict(color=colors[i % len(colors)]),
                    hovertemplate=f'<b>{keyword}</b><br>Date: %{{x}}<br>Count: %{{y}}<extra></extra>'
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Frequency",
            template=self.plotly_theme,
            height=600,
            hovermode='x unified'
        )
        
        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            fig.show()
            return "displayed"
    
    def _create_static_trends_plot(self, trends: List[Tuple], title: str, 
                                 output_path: Optional[str]) -> str:
        """Create static trends plot using matplotlib."""
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        colors = sns.color_palette(self.color_palette, len(trends))
        
        for i, (keyword, trend_data) in enumerate(trends):
            if 'monthly_data' in trend_data:
                monthly_data = trend_data['monthly_data']
                dates = pd.to_datetime(list(monthly_data.keys()))
                values = list(monthly_data.values())
                
                ax.plot(dates, values, marker='o', label=keyword, color=colors[i], linewidth=2)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, format=self.save_format, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.show()
            return "displayed"
    
    def _create_interactive_cluster_plot(self, embeddings_2d: np.ndarray, cluster_labels: List[int],
                                       keywords: List[str], title: str, 
                                       output_path: Optional[str]) -> str:
        """Create interactive cluster plot using Plotly."""
        # Create color map for clusters
        unique_clusters = list(set(cluster_labels))
        colors = px.colors.qualitative.Set1 * (len(unique_clusters) // len(px.colors.qualitative.Set1) + 1)
        
        fig = go.Figure()
        
        for i, cluster_id in enumerate(unique_clusters):
            cluster_mask = np.array(cluster_labels) == cluster_id
            cluster_embeddings = embeddings_2d[cluster_mask]
            cluster_keywords = [keywords[j] for j, mask in enumerate(cluster_mask) if mask]
            
            cluster_name = f'Cluster {cluster_id}' if cluster_id != -1 else 'Noise'
            
            fig.add_trace(go.Scatter(
                x=cluster_embeddings[:, 0],
                y=cluster_embeddings[:, 1],
                mode='markers',
                name=cluster_name,
                text=cluster_keywords,
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)],
                    opacity=0.7
                ),
                hovertemplate='<b>%{text}</b><br>Cluster: ' + cluster_name + '<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Dimension 1",
            yaxis_title="Dimension 2",
            template=self.plotly_theme,
            height=600
        )
        
        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            fig.show()
            return "displayed"
    
    def _create_static_cluster_plot(self, embeddings_2d: np.ndarray, cluster_labels: List[int],
                                  keywords: List[str], title: str, 
                                  output_path: Optional[str]) -> str:
        """Create static cluster plot using matplotlib."""
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        unique_clusters = list(set(cluster_labels))
        colors = sns.color_palette(self.color_palette, len(unique_clusters))
        
        for i, cluster_id in enumerate(unique_clusters):
            cluster_mask = np.array(cluster_labels) == cluster_id
            cluster_embeddings = embeddings_2d[cluster_mask]
            
            cluster_name = f'Cluster {cluster_id}' if cluster_id != -1 else 'Noise'
            
            ax.scatter(cluster_embeddings[:, 0], cluster_embeddings[:, 1], 
                      c=[colors[i]], label=cluster_name, alpha=0.7, s=50)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Dimension 1', fontsize=12)
        ax.set_ylabel('Dimension 2', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, format=self.save_format, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.show()
            return "displayed"
    
    def _create_interactive_lifecycle_plot(self, lifecycles: Dict[str, Any], title: str,
                                         output_path: Optional[str]) -> str:
        """Create interactive lifecycle plot using Plotly."""
        # Prepare data for bubble chart
        keywords = []
        growth_rates = []
        maturity_indices = []
        lifespans = []
        stages = []
        
        for keyword, lifecycle in lifecycles.items():
            keywords.append(keyword)
            growth_rates.append(lifecycle['growth_rate'])
            maturity_indices.append(lifecycle['maturity_index'])
            lifespans.append(lifecycle['lifespan_months'])
            stages.append(lifecycle['current_stage'])
        
        # Create color map for stages
        unique_stages = list(set(stages))
        stage_colors = {stage: px.colors.qualitative.Set2[i % len(px.colors.qualitative.Set2)] 
                       for i, stage in enumerate(unique_stages)}
        
        fig = go.Figure()
        
        for stage in unique_stages:
            stage_mask = [s == stage for s in stages]
            stage_keywords = [k for k, mask in zip(keywords, stage_mask) if mask]
            stage_growth = [g for g, mask in zip(growth_rates, stage_mask) if mask]
            stage_maturity = [m for m, mask in zip(maturity_indices, stage_mask) if mask]
            stage_lifespans = [l for l, mask in zip(lifespans, stage_mask) if mask]
            
            fig.add_trace(go.Scatter(
                x=stage_growth,
                y=stage_maturity,
                mode='markers',
                name=stage.replace('_', ' ').title(),
                text=stage_keywords,
                marker=dict(
                    size=[max(5, min(50, l)) for l in stage_lifespans],  # Size based on lifespan
                    color=stage_colors[stage],
                    opacity=0.7,
                    line=dict(width=1, color='black')
                ),
                hovertemplate='<b>%{text}</b><br>Growth Rate: %{x:.3f}<br>Maturity: %{y:.3f}<br>Stage: ' + stage + '<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Growth Rate",
            yaxis_title="Maturity Index",
            template=self.plotly_theme,
            height=600
        )
        
        # Add quadrant lines
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            fig.show()
            return "displayed"
    
    def _create_static_lifecycle_plot(self, lifecycles: Dict[str, Any], title: str,
                                    output_path: Optional[str]) -> str:
        """Create static lifecycle plot using matplotlib."""
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        # Prepare data
        growth_rates = [lifecycle['growth_rate'] for lifecycle in lifecycles.values()]
        maturity_indices = [lifecycle['maturity_index'] for lifecycle in lifecycles.values()]
        lifespans = [lifecycle['lifespan_months'] for lifecycle in lifecycles.values()]
        stages = [lifecycle['current_stage'] for lifecycle in lifecycles.values()]
        
        # Create scatter plot with different colors for stages
        unique_stages = list(set(stages))
        colors = sns.color_palette(self.color_palette, len(unique_stages))
        stage_colors = {stage: colors[i] for i, stage in enumerate(unique_stages)}
        
        for stage in unique_stages:
            stage_mask = [s == stage for s in stages]
            stage_growth = [g for g, mask in zip(growth_rates, stage_mask) if mask]
            stage_maturity = [m for m, mask in zip(maturity_indices, stage_mask) if mask]
            stage_lifespans = [l for l, mask in zip(lifespans, stage_mask) if mask]
            
            ax.scatter(stage_growth, stage_maturity, 
                      c=[stage_colors[stage]], 
                      s=[max(20, min(200, l*5)) for l in stage_lifespans],  # Size based on lifespan
                      label=stage.replace('_', ' ').title(), 
                      alpha=0.7, edgecolors='black', linewidth=0.5)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Growth Rate', fontsize=12)
        ax.set_ylabel('Maturity Index', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add quadrant lines
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, format=self.save_format, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.show()
            return "displayed"
    
    def _create_interactive_comparison_plot(self, period_data: Dict[str, Dict[str, int]], 
                                          title: str, output_path: Optional[str]) -> str:
        """Create interactive comparison plot using Plotly."""
        # Prepare data for stacked bar chart
        periods = list(period_data.keys())
        all_keywords = set()
        for keywords in period_data.values():
            all_keywords.update(keywords.keys())
        
        # Get top keywords across all periods
        keyword_totals = Counter()
        for keywords in period_data.values():
            keyword_totals.update(keywords)
        
        top_keywords = [kw for kw, _ in keyword_totals.most_common(15)]
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set3
        
        for i, period in enumerate(periods):
            period_counts = [period_data[period].get(kw, 0) for kw in top_keywords]
            
            fig.add_trace(go.Bar(
                name=period.replace('_', ' ').title(),
                x=top_keywords,
                y=period_counts,
                marker_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Keywords",
            yaxis_title="Frequency",
            barmode='group',
            template=self.plotly_theme,
            height=600
        )
        
        fig.update_layout(xaxis_tickangle=45)
        
        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            fig.show()
            return "displayed"
    
    def _create_static_comparison_plot(self, period_data: Dict[str, Dict[str, int]], 
                                     title: str, output_path: Optional[str]) -> str:
        """Create static comparison plot using matplotlib."""
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        # Prepare data
        periods = list(period_data.keys())
        all_keywords = set()
        for keywords in period_data.values():
            all_keywords.update(keywords.keys())
        
        # Get top keywords
        keyword_totals = Counter()
        for keywords in period_data.values():
            keyword_totals.update(keywords)
        
        top_keywords = [kw for kw, _ in keyword_totals.most_common(15)]
        
        # Create grouped bar chart
        x = np.arange(len(top_keywords))
        width = 0.8 / len(periods)
        colors = sns.color_palette(self.color_palette, len(periods))
        
        for i, period in enumerate(periods):
            period_counts = [period_data[period].get(kw, 0) for kw in top_keywords]
            bars = ax.bar(x + i * width, period_counts, width, 
                         label=period.replace('_', ' ').title(), 
                         color=colors[i], alpha=0.8)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Keywords', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_xticks(x + width * (len(periods) - 1) / 2)
        ax.set_xticklabels(top_keywords, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, format=self.save_format, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.show()
            return "displayed"
    
    def _add_frequency_subplot(self, fig, keyword_data, row, col):
        """Add frequency subplot to dashboard."""
        if isinstance(keyword_data, dict):
            keywords = list(keyword_data.keys())[:10]
            frequencies = [keyword_data[kw] for kw in keywords]
            
            fig.add_trace(
                go.Bar(x=keywords, y=frequencies, name="Frequency"),
                row=row, col=col
            )
    
    def _add_trends_subplot(self, fig, temporal_data, row, col):
        """Add trends subplot to dashboard."""
        if 'individual_trends' in temporal_data:
            trends = list(temporal_data['individual_trends'].items())[:5]
            
            for keyword, trend_data in trends:
                if 'monthly_data' in trend_data:
                    monthly_data = trend_data['monthly_data']
                    dates = list(monthly_data.keys())
                    values = list(monthly_data.values())
                    
                    fig.add_trace(
                        go.Scatter(x=dates, y=values, mode='lines', name=keyword),
                        row=row, col=col
                    )
    
    def _add_clusters_subplot(self, fig, semantic_data, row, col):
        """Add clusters subplot to dashboard."""
        if 'embeddings_2d' in semantic_data and 'cluster_labels' in semantic_data:
            embeddings_2d = np.array(semantic_data['embeddings_2d'])
            cluster_labels = semantic_data['cluster_labels']
            
            unique_clusters = list(set(cluster_labels))
            colors = px.colors.qualitative.Set1
            
            for i, cluster_id in enumerate(unique_clusters[:5]):  # Limit clusters for readability
                cluster_mask = np.array(cluster_labels) == cluster_id
                cluster_embeddings = embeddings_2d[cluster_mask]
                
                fig.add_trace(
                    go.Scatter(
                        x=cluster_embeddings[:, 0], 
                        y=cluster_embeddings[:, 1],
                        mode='markers',
                        name=f'Cluster {cluster_id}',
                        marker=dict(color=colors[i % len(colors)])
                    ),
                    row=row, col=col
                )
    
    def _add_lifecycle_subplot(self, fig, lifecycle_data, row, col):
        """Add lifecycle subplot to dashboard."""
        if 'individual_lifecycles' in lifecycle_data:
            lifecycles = lifecycle_data['individual_lifecycles']
            
            growth_rates = [lc['growth_rate'] for lc in lifecycles.values()]
            maturity_indices = [lc['maturity_index'] for lc in lifecycles.values()]
            keywords = list(lifecycles.keys())
            
            fig.add_trace(
                go.Scatter(
                    x=growth_rates,
                    y=maturity_indices,
                    mode='markers',
                    text=keywords,
                    name="Lifecycle"
                ),
                row=row, col=col
            )
    
    def _add_comparison_subplot(self, fig, comparative_data, row, col):
        """Add comparison subplot to dashboard."""
        if 'period_data' in comparative_data:
            period_data = comparative_data['period_data']
            periods = list(period_data.keys())
            
            # Simple comparison of total keywords per period
            totals = [sum(keywords.values()) for keywords in period_data.values()]
            
            fig.add_trace(
                go.Bar(x=periods, y=totals, name="Total Keywords"),
                row=row, col=col
            )
    
    def _add_summary_table(self, fig, analysis_results, row, col):
        """Add summary table to dashboard."""
        # Create summary statistics
        summary_data = []
        
        if 'keyword_frequencies' in analysis_results:
            total_keywords = len(analysis_results['keyword_frequencies'])
            summary_data.append(['Total Keywords', str(total_keywords)])
        
        if 'temporal_analysis' in analysis_results:
            temporal = analysis_results['temporal_analysis']
            if 'keyword_trends' in temporal and 'summary_statistics' in temporal['keyword_trends']:
                stats = temporal['keyword_trends']['summary_statistics']
                summary_data.append(['Trending Keywords', str(stats.get('positive_trends', 0))])
        
        if 'semantic_analysis' in analysis_results:
            semantic = analysis_results['semantic_analysis']
            if 'cluster_stats' in semantic:
                n_clusters = semantic['cluster_stats'].get('n_clusters', 0)
                summary_data.append(['Semantic Clusters', str(n_clusters)])
        
        # Add table
        if summary_data:
            fig.add_trace(
                go.Table(
                    header=dict(values=['Metric', 'Value']),
                    cells=dict(values=[[row[0] for row in summary_data], 
                                     [row[1] for row in summary_data]])
                ),
                row=row, col=col
            )
    
    def export_all_visualizations(self, analysis_results: Dict[str, Any], 
                                 output_dir: str) -> List[str]:
        """
        Export all possible visualizations to a directory.
        
        Args:
            analysis_results: Complete analysis results
            output_dir: Directory to save visualizations
            
        Returns:
            List of paths to exported visualizations
        """
        logger.info(f"Exporting all visualizations to {output_dir}")
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        exported_files = []
        
        try:
            # Word cloud
            if 'keyword_frequencies' in analysis_results:
                path = os.path.join(output_dir, f"wordcloud.{self.save_format}")
                self.create_word_cloud(analysis_results['keyword_frequencies'], 
                                     "Keyword Word Cloud", path)
                exported_files.append(path)
            
            # Frequency plot
            if 'keyword_frequencies' in analysis_results:
                path = os.path.join(output_dir, f"frequency_plot.{self.save_format}")
                self.plot_keyword_frequencies(analysis_results['keyword_frequencies'], 
                                            output_path=path)
                exported_files.append(path)
            
            # Temporal trends
            if 'temporal_analysis' in analysis_results:
                path = os.path.join(output_dir, f"temporal_trends.{self.save_format}")
                self.plot_temporal_trends(analysis_results['temporal_analysis'], 
                                        output_path=path)
                exported_files.append(path)
            
            # Semantic clusters
            if 'semantic_analysis' in analysis_results:
                path = os.path.join(output_dir, f"semantic_clusters.{self.save_format}")
                self.plot_semantic_clusters(analysis_results['semantic_analysis'], 
                                          output_path=path)
                exported_files.append(path)
            
            # Lifecycle analysis
            if 'lifecycle_analysis' in analysis_results:
                path = os.path.join(output_dir, f"lifecycle_analysis.{self.save_format}")
                self.plot_lifecycle_analysis(analysis_results['lifecycle_analysis'], 
                                           output_path=path)
                exported_files.append(path)
            
            # Comparative analysis
            if 'comparative_analysis' in analysis_results:
                path = os.path.join(output_dir, f"comparative_analysis.{self.save_format}")
                self.plot_comparative_analysis(analysis_results['comparative_analysis'], 
                                             output_path=path)
                exported_files.append(path)
            
            # Interactive dashboard
            dashboard_path = os.path.join(output_dir, "dashboard.html")
            self.create_dashboard(analysis_results, dashboard_path)
            exported_files.append(dashboard_path)
            
            logger.info(f"Exported {len(exported_files)} visualizations")
            return exported_files
            
        except Exception as e:
            logger.error(f"Error exporting visualizations: {str(e)}")
            raise
