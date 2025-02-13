"""Robustness metrics for LLM-as-Judge evaluation."""

import numpy as np

def score_variance_ratio(original_scores, perturbed_scores):
    """
    Calculate robustness score based on variance ratio between original and perturbed scores.
    
    Args:
        original_scores (array-like): Original LLM scores
        perturbed_scores (array-like): Scores after perturbation
        
    Returns:
        float: Robustness score (1 - variance ratio)
    """
    original_var = np.var(original_scores)
    perturbed_var = np.var(perturbed_scores)
    
    if original_var == 0:
        return 0.0
        
    return 1 - (perturbed_var / original_var)

def score_stability(original_scores, perturbed_scores, threshold=0.1):
    """
    Calculate the proportion of scores that remain stable after perturbation.
    
    Args:
        original_scores (array-like): Original LLM scores
        perturbed_scores (array-like): Scores after perturbation
        threshold (float): Maximum allowed difference to consider scores stable
        
    Returns:
        float: Proportion of stable scores
    """
    differences = np.abs(np.array(original_scores) - np.array(perturbed_scores))
    return np.mean(differences <= threshold) 