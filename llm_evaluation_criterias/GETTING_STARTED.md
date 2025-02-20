# Getting Started with RAG Evaluation Pipeline

This guide will help you set up and run the RAG Evaluation Pipeline example.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- git

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd rag_eval_pipeline
```

2. Create and activate a virtual environment:

For macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
rag_eval_pipeline/
├── src/
│   ├── metrics/
│   │   └── retrieval_metrics.py
│   ├── reporting/
│   │   └── report_generator.py
│   ├── utils/
│   │   └── data_types.py
│   └── api/
│       └── main.py
├── tests/
│   ├── test_data/
│   │   ├── financial_corpus.json
│   │   └── test_queries.json
│   └── test_retrieval_metrics.py
├── examples/
│   └── evaluate_rag.py
├── requirements.txt
└── README.md
```

## Running the Example

1. Make sure your virtual environment is activated:
```bash
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows
```

2. Run the example script:
```bash
PYTHONPATH=. python examples/evaluate_rag.py
```

The example script will:
1. Load test data from the financial corpus
2. Run a single query evaluation
3. Generate a comprehensive evaluation report
4. Demonstrate individual metric calculations

## Understanding the Output

The example generates several outputs in the `example_reports` directory:

```
example_reports/
└── v{timestamp}/
    ├── csv/
    │   ├── detailed_results.csv      # Query-by-query evaluation results
    │   ├── metric_summaries.csv      # Statistical summaries of metrics
    │   └── metric_values.csv         # Raw metric values
    ├── plots/
    │   ├── metric_visualizations.png # Combined metric visualizations
    │   └── {metric}_distribution.png # Individual metric distributions
    ├── markdown/
    │   └── evaluation_report.md      # Comprehensive markdown report
    └── version_info.json             # Version and file information
```

### Report Contents

1. **CSV Reports**:
   - `detailed_results.csv`: Contains evaluation results for each query
   - `metric_summaries.csv`: Statistical summaries (mean, min, max, std) for each metric
   - `metric_values.csv`: Raw metric values for all queries

2. **Visualizations**:
   - Box plots showing metric distributions
   - Bar charts showing average metric values
   - Individual histograms for each metric

3. **Markdown Report**:
   - Overall performance summary
   - Detailed results table
   - Query-by-query analysis
   - Test dataset statistics
   - Improvement recommendations

4. **Version Information**:
   - Timestamp and version ID
   - Test case and corpus statistics
   - List of generated files

## Available Metrics

The pipeline evaluates retrieval performance using several metrics:

1. **Precision@k**
   - Measures the proportion of relevant documents in top-k results
   - Range: 0 to 1 (higher is better)

2. **Recall@k**
   - Measures the proportion of relevant documents retrieved
   - Range: 0 to 1 (higher is better)

3. **Mean Average Precision (MAP)**
   - Measures ranking quality considering precision at each position
   - Range: 0 to 1 (higher is better)

4. **Semantic Similarity**
   - Measures semantic relevance between query and retrieved documents
   - Range: 0 to 1 (higher is better)

5. **Keyword Coverage**
   - Measures coverage of query keywords in retrieved documents
   - Range: 0 to 1 (higher is better)

## Customizing the Evaluation

To evaluate your own RAG system:

1. Prepare your test data in the same format as the example files:
   - `financial_corpus.json`: Document corpus
   - `test_queries.json`: Test queries and expected results

2. Create a new script based on `examples/evaluate_rag.py`:
```python
from src.reporting.report_generator import RAGEvaluationReporter

# Load your data
corpus = load_your_corpus()
test_cases = load_your_test_cases()

# Generate report
reporter = RAGEvaluationReporter(output_dir="your_reports")
report_path = reporter.generate_report(test_cases, corpus)
```

## Troubleshooting

1. **Import Errors**:
   - Ensure PYTHONPATH includes the project root
   - Check virtual environment activation

2. **Dependency Issues**:
   - Try reinstalling requirements: `pip install -r requirements.txt --force-reinstall`
   - Check Python version compatibility

3. **Report Generation Issues**:
   - Ensure write permissions in output directory
   - Check available disk space

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 