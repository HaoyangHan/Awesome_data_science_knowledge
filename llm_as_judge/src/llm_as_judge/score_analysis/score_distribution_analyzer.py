import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, List, Optional

class ScoreDistributionAnalyzer:
    """Analyzer for comparing and normalizing LLM and human score distributions."""
    
    def __init__(self, llm_scores: np.ndarray, human_scores: np.ndarray):
        """Initialize with LLM and human scores.
        
        Args:
            llm_scores: Array of LLM generated scores
            human_scores: Array of human evaluation scores
        """
        self.llm_scores = llm_scores
        self.human_scores = human_scores
        
    def analyze_distributions(self) -> Dict:
        """Analyze the statistical properties of both score distributions.
        
        Returns:
            Dict containing distribution analysis results
        """
        # Basic statistics
        llm_stats = {
            'mean': np.mean(self.llm_scores),
            'std': np.std(self.llm_scores),
            'median': np.median(self.llm_scores),
            'skewness': stats.skew(self.llm_scores),
            'kurtosis': stats.kurtosis(self.llm_scores)
        }
        
        human_stats = {
            'mean': np.mean(self.human_scores),
            'std': np.std(self.human_scores),
            'median': np.median(self.human_scores),
            'skewness': stats.skew(self.human_scores),
            'kurtosis': stats.kurtosis(self.human_scores)
        }
        
        # Distribution tests
        ks_statistic, ks_pvalue = stats.ks_2samp(self.llm_scores, self.human_scores)
        
        return {
            'llm_stats': llm_stats,
            'human_stats': human_stats,
            'ks_test': {
                'statistic': ks_statistic,
                'pvalue': ks_pvalue
            }
        }
    
    def normalize_scores(self, method: str = 'zscore') -> Tuple[np.ndarray, np.ndarray]:
        """Normalize both score distributions using specified method.
        
        Args:
            method: Normalization method ('zscore', 'minmax', or 'robust')
            
        Returns:
            Tuple of normalized (llm_scores, human_scores)
        """
        if method == 'zscore':
            llm_norm = stats.zscore(self.llm_scores)
            human_norm = stats.zscore(self.human_scores)
        elif method == 'minmax':
            llm_norm = (self.llm_scores - np.min(self.llm_scores)) / (np.max(self.llm_scores) - np.min(self.llm_scores))
            human_norm = (self.human_scores - np.min(self.human_scores)) / (np.max(self.human_scores) - np.min(self.human_scores))
        elif method == 'robust':
            llm_norm = (self.llm_scores - np.median(self.llm_scores)) / stats.iqr(self.llm_scores)
            human_norm = (self.human_scores - np.median(self.human_scores)) / stats.iqr(self.human_scores)
        else:
            raise ValueError(f"Unknown normalization method: {method}")
            
        return llm_norm, human_norm
    
    def plot_distributions(self, 
                         output_path: str,
                         normalized: bool = False,
                         method: str = 'zscore',
                         title: Optional[str] = None) -> None:
        """Plot the score distributions.
        
        Args:
            output_path: Path to save the plot
            normalized: Whether to plot normalized scores
            method: Normalization method if normalized=True
            title: Optional plot title
        """
        if normalized:
            llm_scores, human_scores = self.normalize_scores(method)
            score_label = f'Normalized Score ({method})'
        else:
            llm_scores, human_scores = self.llm_scores, self.human_scores
            score_label = 'Raw Score'
            
        plt.figure(figsize=(10, 6))
        sns.kdeplot(data=llm_scores, label='LLM Scores')
        sns.kdeplot(data=human_scores, label='Human Scores')
        plt.xlabel(score_label)
        plt.ylabel('Density')
        plt.title(title or ('Normalized Score Distribution' if normalized else 'Raw Score Distribution'))
        plt.legend()
        plt.savefig(output_path)
        plt.close()
    
    def get_normalization_differences(self, method: str = 'zscore') -> Dict:
        """Calculate differences between normalized distributions.
        
        Args:
            method: Normalization method to use
            
        Returns:
            Dict containing difference metrics
        """
        llm_norm, human_norm = self.normalize_scores(method)
        
        return {
            'mean_diff': np.mean(llm_norm) - np.mean(human_norm),
            'std_diff': np.std(llm_norm) - np.std(human_norm),
            'median_diff': np.median(llm_norm) - np.median(human_norm),
            'range_diff': (np.max(llm_norm) - np.min(llm_norm)) - (np.max(human_norm) - np.min(human_norm)),
            'ks_statistic': stats.ks_2samp(llm_norm, human_norm).statistic
        } 