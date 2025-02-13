"""Bias detection metrics for LLM-as-Judge evaluation."""

import numpy as np
from scipy.stats import spearmanr

def position_bias(positions, scores):
    """
    Calculate position bias by correlating position with scores.
    
    Args:
        positions (array-like): Position indices of questions
        scores (array-like): Scores assigned by the LLM
        
    Returns:
        float: Position bias correlation coefficient
        float: p-value
    """
    return spearmanr(positions, scores)

def length_bias(lengths, scores):
    """
    Calculate length bias by correlating answer length with scores.
    
    Args:
        lengths (array-like): Lengths of answers (e.g., word count)
        scores (array-like): Scores assigned by the LLM
        
    Returns:
        float: Length bias correlation coefficient
        float: p-value
    """
    return spearmanr(lengths, scores)

def calculate_word_count(text):
    """
    Calculate word count for a given text.
    
    Args:
        text (str): Input text
        
    Returns:
        int: Number of words
    """
    return len(str(text).split()) 