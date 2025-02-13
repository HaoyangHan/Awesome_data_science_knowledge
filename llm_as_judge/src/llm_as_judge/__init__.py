"""
LLM-as-Judge Evaluation Module

This module provides tools and metrics for evaluating LLM-based evaluation systems
against human judgments in question-answering tasks.
"""

from .core.config import LLMJudgeConfig
from .core.evaluator import LLMJudgeEvaluator
from .metrics import (
    agreement_metrics,
    correlation_metrics,
    bias_metrics,
    robustness_metrics
)

__version__ = "0.1.0"
__author__ = "Your Name"

# Export main classes
__all__ = [
    'LLMJudgeConfig',
    'LLMJudgeEvaluator'
] 