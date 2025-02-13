"""Configuration management for LLM-as-Judge module."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from loguru import logger

@dataclass
class LLMJudgeConfig:
    """Configuration for LLM-as-Judge evaluation."""
    
    # Data configuration
    score_range: tuple[float, float] = (0.5, 1.0)
    required_columns: tuple[str, ...] = (
        'Ground Truth Question',
        'LLM Generated Question',
        'LLM Generated Score',
        'Human Evaluation Score'
    )
    
    # Metric configuration
    n_bins_kappa: int = 5
    robustness_perturbation_std: float = 0.05
    robustness_stability_threshold: float = 0.1
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    def __post_init__(self):
        """Setup logging configuration."""
        logger.remove()  # Remove default handler
        logger.add(
            sink=lambda msg: print(msg),
            format=self.log_format,
            level=self.log_level,
            colorize=True
        )
        
    def validate_score_range(self, scores: list[float]) -> bool:
        """
        Validate that scores fall within the expected range.
        
        Args:
            scores: List of scores to validate
            
        Returns:
            bool: Whether all scores are within range
        """
        min_score, max_score = self.score_range
        return all(min_score <= score <= max_score for score in scores)
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'LLMJudgeConfig':
        """
        Create configuration from dictionary.
        
        Args:
            config_dict: Dictionary containing configuration values
            
        Returns:
            LLMJudgeConfig: New configuration instance
        """
        return cls(**{
            k: v for k, v in config_dict.items()
            if k in cls.__dataclass_fields__
        }) 