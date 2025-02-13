# Advanced Answer Evaluation Analysis

This directory contains advanced analysis tools for evaluating LLM-generated answers against human evaluations.

## Features

The analysis toolkit provides the following capabilities:

1. **Score Statistics**
   - Basic statistical analysis of scores (mean, std, quartiles, etc.)
   - Separate analysis for LLM and human evaluations
   - Comparison across all evaluation metrics

2. **LLM-Human Agreement Analysis**
   - Correlation analysis between LLM and human scores
   - Mean Absolute Error (MAE) calculation
   - Root Mean Square Error (RMSE) calculation

3. **High Quality Answer Analysis**
   - Identification of high-scoring answers
   - Analysis of agreement between LLM and human evaluations
   - Example extraction of high-quality answers

4. **Visualization**
   - Score distribution plots
   - LLM vs Human comparison visualizations
   - Metric-wise analysis plots

5. **Comprehensive Reporting**
   - Markdown report generation
   - Detailed analysis summaries
   - Example showcases

## Usage

1. Basic Usage:
```python
from llm_as_judge.answer_evaluation import AnswerEvaluationAnalyzer

# Initialize analyzer
analyzer = AnswerEvaluationAnalyzer('path/to/evaluation_data.csv')

# Get basic statistics
stats = analyzer.get_score_statistics()

# Generate comprehensive report
analyzer.generate_report('output/report.md')
```

2. Run Example Analysis:
```bash
python answer_evaluation_analysis.py
```

## Data Format

The analyzer expects a CSV file with the following columns:
- Chunk: Context information
- Question: The question being evaluated
- Answer: The generated answer
- LLM/Human metrics:
  - Stand-alone Quality
  - Readiness
  - Relevance
  - Completeness

## Output

The analysis generates:
1. Statistical summaries
2. Agreement analysis
3. Visualization plots
4. Comprehensive markdown report

## Example Output Structure

```
output/
├── score_distributions.png
└── evaluation_report.md
```

## Advanced Usage

For more advanced analysis, you can customize:
- Score thresholds for high-quality analysis
- Visualization parameters
- Report format and content
- Statistical measures

See `answer_evaluation_analysis.py` for detailed examples. 