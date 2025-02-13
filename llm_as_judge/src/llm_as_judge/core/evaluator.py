"""Core evaluator class for LLM-as-Judge."""

from typing import Optional, Union, Dict, Any

import numpy as np
import pandas as pd
from loguru import logger

from .config import LLMJudgeConfig
from ..metrics import (
    agreement_metrics,
    correlation_metrics,
    bias_metrics,
    robustness_metrics
)

class LLMJudgeEvaluator:
    """Main evaluator class that integrates all metrics with robust error handling."""
    
    def __init__(
        self,
        data: Union[pd.DataFrame, Dict[str, list]],
        config: Optional[LLMJudgeConfig] = None
    ):
        """
        Initialize the evaluator with data and configuration.
        
        Args:
            data: Input data containing questions and scores
            config: Configuration instance, uses default if None
        """
        self.config = config or LLMJudgeConfig()
        self.df = pd.DataFrame(data) if isinstance(data, dict) else data.copy()
        self._validate_data()
        logger.info(f"Initialized evaluator with {len(self.df)} samples")
        
    def _validate_data(self) -> None:
        """Validate input data format and values."""
        # Check required columns
        missing = [col for col in self.config.required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        # Validate score ranges
        for score_col in ['LLM Generated Score', 'Human Evaluation Score']:
            if not self.config.validate_score_range(self.df[score_col].tolist()):
                logger.warning(f"Some scores in {score_col} are outside expected range {self.config.score_range}")
                
        logger.debug("Data validation completed")
        
    def compute_agreement_metrics(self) -> Dict[str, float]:
        """Compute agreement-based metrics with error handling."""
        try:
            metrics = {
                'exact_match': agreement_metrics.exact_match_agreement(
                    self.df['LLM Generated Score'],
                    self.df['Human Evaluation Score']
                ),
                'cohen_kappa': agreement_metrics.cohen_kappa(
                    self.df['LLM Generated Score'],
                    self.df['Human Evaluation Score'],
                    n_bins=self.config.n_bins_kappa
                )
            }
            logger.debug(f"Agreement metrics computed: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error computing agreement metrics: {str(e)}")
            raise
            
    def compute_correlation_metrics(self) -> Dict[str, float]:
        """Compute correlation-based metrics with error handling."""
        try:
            spearman_corr, spearman_p = correlation_metrics.spearman_correlation(
                self.df['LLM Generated Score'],
                self.df['Human Evaluation Score']
            )
            pearson_corr, pearson_p = correlation_metrics.pearson_correlation(
                self.df['LLM Generated Score'],
                self.df['Human Evaluation Score']
            )
            
            metrics = {
                'spearman_correlation': spearman_corr,
                'spearman_p_value': spearman_p,
                'pearson_correlation': pearson_corr,
                'pearson_p_value': pearson_p
            }
            logger.debug(f"Correlation metrics computed: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error computing correlation metrics: {str(e)}")
            raise
            
    def compute_bias_metrics(self) -> Dict[str, float]:
        """Compute bias-related metrics with error handling."""
        try:
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
            
            metrics = {
                'position_bias': pos_corr,
                'position_bias_p_value': pos_p,
                'length_bias': len_corr,
                'length_bias_p_value': len_p
            }
            logger.debug(f"Bias metrics computed: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error computing bias metrics: {str(e)}")
            raise
            
    def compute_robustness_metrics(
        self,
        perturbed_scores: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Compute robustness metrics with error handling.
        
        Args:
            perturbed_scores: Optional pre-computed perturbed scores
            
        Returns:
            Dictionary containing robustness metrics
        """
        try:
            if perturbed_scores is None:
                # Simulate perturbations
                perturbed_scores = (
                    self.df['LLM Generated Score'] +
                    np.random.normal(0, self.config.robustness_perturbation_std, len(self.df))
                )
                perturbed_scores = np.clip(perturbed_scores, *self.config.score_range)
                
            metrics = {
                'variance_ratio': robustness_metrics.score_variance_ratio(
                    self.df['LLM Generated Score'],
                    perturbed_scores
                ),
                'stability': robustness_metrics.score_stability(
                    self.df['LLM Generated Score'],
                    perturbed_scores,
                    threshold=self.config.robustness_stability_threshold
                )
            }
            logger.debug(f"Robustness metrics computed: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error computing robustness metrics: {str(e)}")
            raise
            
    def evaluate(
        self,
        include_robustness: bool = True,
        perturbed_scores: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Run full evaluation pipeline with comprehensive error handling.
        
        Args:
            include_robustness: Whether to include robustness metrics
            perturbed_scores: Optional pre-computed perturbed scores
            
        Returns:
            Dictionary containing all computed metrics
        """
        logger.info("Starting evaluation pipeline")
        try:
            metrics = {}
            metrics.update(self.compute_agreement_metrics())
            metrics.update(self.compute_correlation_metrics())
            metrics.update(self.compute_bias_metrics())
            
            if include_robustness:
                metrics.update(self.compute_robustness_metrics(perturbed_scores))
                
            logger.info("Evaluation pipeline completed successfully")
            return metrics
        except Exception as e:
            logger.error(f"Error in evaluation pipeline: {str(e)}")
            raise 