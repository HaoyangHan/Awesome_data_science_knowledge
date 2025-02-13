# LLM-as-Judge Examples

This directory contains example code and notebooks demonstrating how to use the LLM-as-Judge evaluation framework.

## Directory Structure

```
examples/
├── question_evaluation/      # Examples for evaluating question generation
│   ├── basic/              # Basic question evaluation examples
│   └── advanced/           # Advanced question evaluation analysis
│
├── answer_evaluation/       # Examples for evaluating answer generation
│   ├── basic/              # Basic answer evaluation examples
│   └── advanced/           # Advanced answer evaluation analysis
│
└── notebooks/              # Jupyter notebooks with interactive examples
```

## Quick Start

### Question Generation Evaluation

```python
from llm_as_judge.question_evaluation import QuestionEvaluationAnalyzer

# Initialize analyzer
analyzer = QuestionEvaluationAnalyzer('path/to/question_evaluation_data.csv')

# Generate analysis
analyzer.generate_report('output/report.md')
```

### Answer Generation Evaluation

```python
from llm_as_judge.answer_evaluation import AnswerEvaluationAnalyzer

# Initialize analyzer
analyzer = AnswerEvaluationAnalyzer('path/to/answer_evaluation_data.csv')

# Generate analysis
analyzer.generate_report('output/report.md')
```

## Example Data

- `data/llm_judge_evaluation_sample.csv`: Sample data for question evaluation
- `data/llm_judge_answer_evaluation_sample.csv`: Sample data for answer evaluation

## Running Examples

1. Question Evaluation:
```bash
python question_evaluation/advanced/question_evaluation_analysis.py
```

2. Answer Evaluation:
```bash
python answer_evaluation/advanced/answer_evaluation_analysis.py
```

See individual directories for more detailed examples and documentation. 