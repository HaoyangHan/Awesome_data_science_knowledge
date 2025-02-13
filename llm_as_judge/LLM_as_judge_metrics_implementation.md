# **LLM-as-a-Judge Metrics Implementation Guide**

This document provides detailed implementation details of the evaluation metrics used in our LLM-as-a-Judge system. It serves as a practical companion to the theoretical metrics documentation in `LLM_as_judge_evaluation_metrics.md`.

## **1. Implementation of Key Metrics**

### **1.1 Agreement Implementation**
**Implementation Details**: 
```python
def calculate_agreement(llm_scores: np.ndarray, human_scores: np.ndarray, threshold: float = 0.1) -> float:
    return np.mean(np.abs(llm_scores - human_scores) <= threshold)
```
- Uses numpy's vectorized operations for efficiency
- Implements a threshold-based agreement (default 0.1) instead of exact matches
- Returns a float between 0 and 1

---

### **1.2 Spearman's Rank Correlation Implementation**
**Implementation Details**:
```python
def calculate_rank_correlation(llm_scores: np.ndarray, human_scores: np.ndarray) -> float:
    return stats.spearmanr(llm_scores, human_scores)[0]
```
- Utilizes scipy.stats for efficient calculation
- Returns only the correlation coefficient (first element of tuple)
- Handles ties automatically through scipy's implementation

---

### **1.3 Cohen's Kappa Implementation**
**Implementation Details**:
```python
def calculate_cohens_kappa(llm_scores: np.ndarray, human_scores: np.ndarray, n_bins: int = 5) -> float:
    # Discretize scores into bins
    llm_bins = pd.qcut(llm_scores, n_bins, labels=False)
    human_bins = pd.qcut(human_scores, n_bins, labels=False)
    return cohen_kappa_score(llm_bins, human_bins)
```
- Uses pandas qcut for equal-frequency binning
- Implements sklearn's cohen_kappa_score
- Discretizes continuous scores into n_bins categories (default 5)

---

## **2. Bias Metrics Implementation**

### **2.1 Position Bias Implementation**
**Implementation Details**:
```python
# Inside calculate_bias_metrics method
position_corr = stats.spearmanr(np.arange(len(df)), df[col])[0]
```
- Creates position array using numpy's arange
- Correlates position with scores using Spearman correlation
- Returns a single correlation coefficient

---

### **2.2 Length Bias Implementation**
**Implementation Details**:
```python
# Length calculation
df['answer_length'] = df['Answer'].str.len()  # or 'LLM Generated Question'

# Correlation calculation
length_corr = stats.spearmanr(df['answer_length'], df[col])[0]
```
- Calculates character length using pandas string methods
- Correlates length with scores using Spearman correlation
- Adapts to both answer and question evaluation scenarios

---

## **3. Robustness Implementation**
**Implementation Details**:
```python
def calculate_robustness(original_scores: np.ndarray, 
                        perturbed_scores: List[np.ndarray]) -> float:
    original_var = np.var(original_scores)
    perturbed_var = np.mean([np.var(scores) for scores in perturbed_scores])
    return 1 - (perturbed_var / original_var if original_var > 0 else 0)
```
- Calculates variance using numpy's var function
- Handles multiple perturbation sets through list comprehension
- Returns normalized score between 0 and 1

---

## **4. Comprehensive Metrics Generation**

### **4.1 Main Implementation**
**Implementation Details**:
```python
def generate_comprehensive_metrics(
    df: pd.DataFrame,
    llm_columns: List[str],
    human_columns: List[str],
    agreement_threshold: float = 0.1,
    n_bins_kappa: int = 5
) -> Dict[str, Dict[str, float]]:
    metrics = {}
    for llm_col, human_col in zip(llm_columns, human_columns):
        metric_name = llm_col.replace('LLM ', '')
        llm_scores = df[llm_col].values
        human_scores = df[human_col].values
        
        metrics[metric_name] = {
            'agreement': calculate_agreement(llm_scores, human_scores),
            'rank_correlation': calculate_rank_correlation(llm_scores, human_scores),
            'cohens_kappa': calculate_cohens_kappa(llm_scores, human_scores)
        }
    
    metrics['bias'] = calculate_bias_metrics(df, llm_columns + human_columns)
    return metrics
```
- Processes multiple metrics in parallel
- Returns nested dictionary structure
- Handles both single and multi-metric scenarios

---

## **5. Implementation Notes**

### **5.1 Dependencies**
- numpy: For efficient array operations
- scipy.stats: For statistical calculations
- pandas: For data manipulation and binning
- sklearn.metrics: For Cohen's Kappa calculation

### **5.2 Performance Considerations**
- Uses vectorized operations where possible
- Minimizes loop operations
- Leverages efficient library implementations

### **5.3 Error Handling**
- Handles zero variance cases in robustness calculation
- Manages missing data through pandas operations
- Validates input data types and shapes

---

## **6. Usage Examples**

### **6.1 Basic Usage**
```python
from llm_as_judge.metrics.evaluation_metrics import EvaluationMetrics

# Initialize with data
metrics = EvaluationMetrics.generate_comprehensive_metrics(
    df=your_dataframe,
    llm_columns=['LLM Score'],
    human_columns=['Human Score']
)
```

### **6.2 Advanced Usage**
```python
# Custom threshold for agreement
agreement = EvaluationMetrics.calculate_agreement(
    llm_scores=scores1,
    human_scores=scores2,
    threshold=0.15
)

# Detailed bias analysis
bias_metrics = EvaluationMetrics.calculate_bias_metrics(
    df=your_dataframe,
    score_columns=['LLM Score', 'Human Score']
)
```

---

This implementation guide serves as a practical reference for understanding and using the evaluation metrics in the LLM-as-Judge system. For theoretical background and metric definitions, please refer to `LLM_as_judge_evaluation_metrics.md`. 