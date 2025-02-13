# LLM-as-Judge: Comprehensive Evaluation Framework

A Python package for evaluating LLM-based systems against human judgments in question-answering tasks, supporting both single-metric and multi-metric evaluation approaches.

## Overview

This framework provides tools for two main evaluation scenarios:
1. **Question Generation Evaluation**: Single-metric evaluation comparing LLM-generated questions with human judgments
2. **Answer Generation Evaluation**: Multi-metric evaluation assessing answer quality across multiple dimensions

## Key Features

- **Flexible Evaluation Approaches**:
  - Single-metric evaluation for simple tasks
  - Multi-metric evaluation for complex assessments
  - Customizable scoring ranges and thresholds
  
- **Comprehensive Metrics Suite**:
  - Basic agreement metrics (correlation, MAE, RMSE)
  - Advanced statistical measures (Cohen's Kappa, Spearman's Rank)
  - Bias detection (position, length)
  - Robustness testing
  
- **Visualization and Reporting**:
  - Score distribution plots
  - Agreement analysis charts
  - Comprehensive markdown reports
  - Interactive notebooks

## Installation

```bash
pip install -e .
```

## Quick Start

### Single-Metric Evaluation (Question Generation)
```python
from llm_as_judge.question_evaluation import QuestionEvaluationAnalyzer

# Initialize analyzer
analyzer = QuestionEvaluationAnalyzer('path/to/data.csv')

# Get basic statistics
stats = analyzer.get_score_statistics()

# Generate comprehensive report
analyzer.generate_report('output/report.md')
```

### Multi-Metric Evaluation (Answer Generation)
```python
from llm_as_judge.answer_evaluation import AnswerEvaluationAnalyzer

# Initialize analyzer
analyzer = AnswerEvaluationAnalyzer('path/to/data.csv')

# Analyze across multiple metrics
stats = analyzer.get_score_statistics()
agreement = analyzer.calculate_agreement()
quality = analyzer.analyze_answer_quality()

# Generate visualizations and report
analyzer.plot_score_distributions('output/plots.png')
analyzer.generate_report('output/report.md')
```

## Understanding Evaluation Approaches

### Single-Metric Evaluation
- **Use Case**: Simple tasks with clear right/wrong answers
- **Advantages**:
  - Easier to interpret
  - Faster to compute
  - Good for basic quality assessment
- **Limitations**:
  - May miss nuanced differences
  - Less suitable for complex tasks
- **Example**: Question generation evaluation using single agreement score

### Multi-Metric Evaluation
- **Use Case**: Complex tasks requiring nuanced assessment
- **Advantages**:
  - More comprehensive assessment
  - Captures different quality aspects
  - Better for complex tasks
- **Metrics Used**:
  1. Stand-alone Quality: Overall answer quality
  2. Readiness: Immediate usability
  3. Relevance: Connection to question
  4. Completeness: Coverage of required information
- **Example**: Answer generation evaluation using multiple quality dimensions

## Practical Considerations

### When to Use Single-Metric Evaluation
1. Quick quality checks
2. Simple task assessment
3. Binary decision making
4. Limited computational resources

### When to Use Multi-Metric Evaluation
1. Complex answer assessment
2. Detailed quality analysis
3. Performance debugging
4. Research and development

## Examples and Documentation

- **Basic Examples**: See `examples/` directory for starter code
- **Advanced Usage**: Check `examples/advanced/` for detailed analysis
- **Metrics Documentation**: See `LLM_as_judge_evaluation_metrics.md`
- **Interactive Examples**: Available in `examples/notebooks/`

## Data Format Requirements

### Single-Metric Format
```csv
Ground Truth Question,LLM Generated Question,LLM Generated Score,Human Evaluation Score
```

### Multi-Metric Format
```csv
Chunk,Question,Answer,LLM Stand-alone Quality,Human Stand-alone Quality,...
```

## Contributing

We welcome contributions! Please see our contributing guidelines for more details.

## License

MIT License 