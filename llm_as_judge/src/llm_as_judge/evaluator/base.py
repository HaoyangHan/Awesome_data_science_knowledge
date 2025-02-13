"""Base evaluator class for LLM-as-Judge evaluation."""

import pandas as pd
import numpy as np
from ..metrics import (
    agreement_metrics,
    correlation_metrics,
    bias_metrics,
    robustness_metrics
)

class LLMJudgeEvaluator:
    """Main evaluator class that integrates all metrics."""
    
    def __init__(self, data):
        """
        Initialize the evaluator with evaluation data.
        
        Args:
            data (dict or pd.DataFrame): Data containing ground truth questions,
                LLM generated questions, LLM scores, and human scores.
        """
        self.df = pd.DataFrame(data) if isinstance(data, dict) else data
        self._validate_data()
        
    def _validate_data(self):
        """Validate that the required columns are present in the data."""
        required_columns = [
            'Ground Truth Question',
            'LLM Generated Question',
            'LLM Generated Score',
            'Human Evaluation Score'
        ]
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
    def compute_agreement_metrics(self):
        """Compute all agreement-based metrics."""
        return {
            'exact_match': agreement_metrics.exact_match_agreement(
                self.df['LLM Generated Score'],
                self.df['Human Evaluation Score']
            ),
            'cohen_kappa': agreement_metrics.cohen_kappa(
                self.df['LLM Generated Score'],
                self.df['Human Evaluation Score']
            )
        }
        
    def compute_correlation_metrics(self):
        """Compute all correlation-based metrics."""
        spearman_corr, spearman_p = correlation_metrics.spearman_correlation(
            self.df['LLM Generated Score'],
            self.df['Human Evaluation Score']
        )
        pearson_corr, pearson_p = correlation_metrics.pearson_correlation(
            self.df['LLM Generated Score'],
            self.df['Human Evaluation Score']
        )
        return {
            'spearman_correlation': spearman_corr,
            'spearman_p_value': spearman_p,
            'pearson_correlation': pearson_corr,
            'pearson_p_value': pearson_p
        }
        
    def compute_bias_metrics(self):
        """Compute all bias-related metrics."""
        # Position bias
        positions = np.arange(len(self.df))
        pos_corr, pos_p = bias_metrics.position_bias(
            positions,
            self.df['LLM Generated Score']
        )
        
        # Length bias
        lengths = self.df['LLM Generated Question'].apply(bias_metrics.calculate_word_count)
        len_corr, len_p = bias_metrics.length_bias(
            lengths,
            self.df['LLM Generated Score']
        )
        
        return {
            'position_bias': pos_corr,
            'position_bias_p_value': pos_p,
            'length_bias': len_corr,
            'length_bias_p_value': len_p
        }
        
    def compute_robustness_metrics(self, perturbed_scores=None):
        """
        Compute robustness metrics.
        
        Args:
            perturbed_scores (array-like, optional): Scores after perturbation.
                If None, simulated perturbations will be used.
        """
        if perturbed_scores is None:
            # Simulate perturbations for demonstration
            perturbed_scores = self.df['LLM Generated Score'] + np.random.normal(0, 0.05, len(self.df))
            perturbed_scores = np.clip(perturbed_scores, 0, 1)
            
        return {
            'variance_ratio': robustness_metrics.score_variance_ratio(
                self.df['LLM Generated Score'],
                perturbed_scores
            ),
            'stability': robustness_metrics.score_stability(
                self.df['LLM Generated Score'],
                perturbed_scores
            )
        }
        
    def evaluate(self, include_robustness=True, perturbed_scores=None):
        """
        Run full evaluation pipeline.
        
        Args:
            include_robustness (bool): Whether to include robustness metrics
            perturbed_scores (array-like, optional): Scores after perturbation
            
        Returns:
            dict: Dictionary containing all computed metrics
        """
        metrics = {}
        metrics.update(self.compute_agreement_metrics())
        metrics.update(self.compute_correlation_metrics())
        metrics.update(self.compute_bias_metrics())
        
        if include_robustness:
            metrics.update(self.compute_robustness_metrics(perturbed_scores))
            
        return metrics 