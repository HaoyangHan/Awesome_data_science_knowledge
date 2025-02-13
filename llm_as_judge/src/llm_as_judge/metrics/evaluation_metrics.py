import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import cohen_kappa_score
from typing import List, Dict, Union, Optional

class EvaluationMetrics:
    """Implementation of comprehensive LLM-as-Judge evaluation metrics."""
    
    @staticmethod
    def calculate_agreement(llm_scores: np.ndarray, human_scores: np.ndarray, threshold: float = 0.1) -> float:
        """Calculate exact agreement between LLM and human scores.
        
        Args:
            llm_scores: Array of LLM scores
            human_scores: Array of human scores
            threshold: Threshold for considering scores as agreeing
            
        Returns:
            Agreement score between 0 and 1
        """
        return np.mean(np.abs(llm_scores - human_scores) <= threshold)
    
    @staticmethod
    def calculate_rank_correlation(llm_scores: np.ndarray, human_scores: np.ndarray) -> float:
        """Calculate Spearman's rank correlation.
        
        Args:
            llm_scores: Array of LLM scores
            human_scores: Array of human scores
            
        Returns:
            Spearman correlation coefficient
        """
        return stats.spearmanr(llm_scores, human_scores)[0]
    
    @staticmethod
    def calculate_cohens_kappa(llm_scores: np.ndarray, human_scores: np.ndarray, n_bins: int = 5) -> float:
        """Calculate Cohen's Kappa for inter-rater reliability.
        
        Args:
            llm_scores: Array of LLM scores
            human_scores: Array of human scores
            n_bins: Number of bins for discretizing scores
            
        Returns:
            Cohen's Kappa score
        """
        # Discretize scores into bins
        llm_bins = pd.qcut(llm_scores, n_bins, labels=False)
        human_bins = pd.qcut(human_scores, n_bins, labels=False)
        
        # Calculate Cohen's Kappa
        return cohen_kappa_score(llm_bins, human_bins)
    
    @staticmethod
    def calculate_bias_metrics(df: pd.DataFrame, score_columns: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate position and length bias metrics.
        
        Args:
            df: DataFrame containing answers and scores
            score_columns: List of score column names
            
        Returns:
            Dictionary containing bias metrics
        """
        # Calculate answer lengths
        if 'Answer' in df.columns:
            df['answer_length'] = df['Answer'].str.len()
        elif 'LLM Generated Question' in df.columns:
            df['answer_length'] = df['LLM Generated Question'].str.len()
        
        bias_metrics = {}
        for col in score_columns:
            # Position bias
            position_corr = stats.spearmanr(np.arange(len(df)), df[col])[0]
            
            # Length bias
            length_corr = stats.spearmanr(df['answer_length'], df[col])[0]
            
            bias_metrics[col] = {
                'position_bias': position_corr,
                'length_bias': length_corr
            }
        
        return bias_metrics
    
    @staticmethod
    def calculate_robustness(original_scores: np.ndarray, perturbed_scores: List[np.ndarray]) -> float:
        """Calculate robustness score based on score variance under perturbations.
        
        Args:
            original_scores: Array of original scores
            perturbed_scores: List of arrays containing scores after perturbations
            
        Returns:
            Robustness score between 0 and 1
        """
        original_var = np.var(original_scores)
        perturbed_var = np.mean([np.var(scores) for scores in perturbed_scores])
        
        return 1 - (perturbed_var / original_var if original_var > 0 else 0)
    
    @staticmethod
    def generate_comprehensive_metrics(
        df: pd.DataFrame,
        llm_columns: List[str],
        human_columns: List[str],
        agreement_threshold: float = 0.1,
        n_bins_kappa: int = 5
    ) -> Dict[str, Dict[str, float]]:
        """Generate comprehensive evaluation metrics.
        
        Args:
            df: DataFrame containing scores
            llm_columns: List of LLM score columns
            human_columns: List of human score columns
            agreement_threshold: Threshold for agreement calculation
            n_bins_kappa: Number of bins for Cohen's Kappa
            
        Returns:
            Dictionary containing all metrics
        """
        metrics = {}
        
        for llm_col, human_col in zip(llm_columns, human_columns):
            metric_name = llm_col.replace('LLM ', '')
            llm_scores = df[llm_col].values
            human_scores = df[human_col].values
            
            metrics[metric_name] = {
                'agreement': EvaluationMetrics.calculate_agreement(llm_scores, human_scores, agreement_threshold),
                'rank_correlation': EvaluationMetrics.calculate_rank_correlation(llm_scores, human_scores),
                'cohens_kappa': EvaluationMetrics.calculate_cohens_kappa(llm_scores, human_scores, n_bins_kappa)
            }
            
        # Add bias metrics
        bias_metrics = EvaluationMetrics.calculate_bias_metrics(df, llm_columns + human_columns)
        metrics['bias'] = bias_metrics
        
        return metrics 