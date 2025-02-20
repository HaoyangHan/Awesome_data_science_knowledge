# Question Evaluation Analysis Report
## Score Statistics

### LLM Generated Score Statistics:
```
count    35.000000
mean      0.727714
std       0.150002
min       0.510000
25%       0.590000
50%       0.720000
75%       0.830000
max       0.980000
```

### Human Evaluation Score Statistics:
```
count    35.000000
mean      0.715429
std       0.139523
min       0.520000
25%       0.605000
50%       0.700000
75%       0.855000
max       0.940000
```

## Distribution Analysis
```
LLM Stats: {'mean': np.float64(0.7277142857142858), 'std': np.float64(0.14784327057076768), 'median': np.float64(0.72), 'skewness': np.float64(0.27118952095742066), 'kurtosis': np.float64(-1.1751567519563864)}
Human Stats: {'mean': np.float64(0.7154285714285715), 'std': np.float64(0.13751556498173176), 'median': np.float64(0.7), 'skewness': np.float64(0.19194605530178152), 'kurtosis': np.float64(-1.3217295120506165)}
KS Test: {'statistic': np.float64(0.11428571428571428), 'pvalue': np.float64(0.9793840108821031)}
```

### Zscore Normalization Differences
```
{'mean_diff': np.float64(3.7430376258790997e-16), 'std_diff': np.float64(0.0), 'median_diff': np.float64(0.06001628316282926), 'range_diff': np.float64(0.124842506630082), 'ks_statistic': np.float64(0.11428571428571428)}
```

### Minmax Normalization Differences
```
{'mean_diff': np.float64(-0.0020842379504995012), 'std_diff': np.float64(-0.012857861710696583), 'median_diff': np.float64(0.018237082066869303), 'range_diff': np.float64(0.0), 'ks_statistic': np.float64(0.08571428571428572)}
```

### Robust Normalization Differences
```
{'mean_diff': np.float64(-0.029571428571428693), 'std_diff': np.float64(0.06595136745127128), 'median_diff': np.float64(0.0), 'range_diff': np.float64(0.27833333333333243), 'ks_statistic': np.float64(0.11428571428571428)}
```

## Comprehensive Evaluation Metrics

### Agreement Metrics
```
Agreement Score: 0.314
Rank Correlation: 0.007
Cohen's Kappa: 0.036
```

## Bias Analysis

### LLM Generated Score
```
Position Bias: -0.043
Length Bias: 0.096
```

### Human Evaluation Score
```
Position Bias: 0.014
Length Bias: -0.271
```

## High Agreement Examples

### Example 4:
- Ground Truth: What is the role of neural networks in AI?
- Generated: What is the role of neural networks in AI?
- LLM Score: 0.80
- Human Score: 0.81

### Example 6:
- Ground Truth: What are the applications of natural language processing?
- Generated: What are the applications of natural language processing?
- LLM Score: 0.58
- Human Score: 0.55

### Example 15:
- Ground Truth: How do we evaluate machine learning models?
- Generated: How do we evaluate machine learning models?
- LLM Score: 0.59
- Human Score: 0.58
