"""
Example script demonstrating how to use the RAG evaluation pipeline.
This script shows how to:
1. Load multiple test datasets
2. Run evaluations on different domains
3. Generate versioned reports with CSV output
4. Compare results across domains
"""

import json
from pathlib import Path
from src.reporting.report_generator import RAGEvaluationReporter
from src.metrics.retrieval_metrics import RetrievalMetrics
from src.utils.data_types import SearchQuery, RetrievalResult

def load_test_data(corpus_file: str, queries_file: str):
    """Load test data from specified files"""
    base_dir = Path(__file__).parent.parent
    test_data_dir = base_dir / "tests" / "test_data"
    
    with open(test_data_dir / corpus_file) as f:
        corpus = json.load(f)
    with open(test_data_dir / queries_file) as f:
        test_cases = json.load(f)
    
    return corpus, test_cases

def evaluate_single_query(metrics: RetrievalMetrics, query: dict, result: dict):
    """Demonstrate single query evaluation"""
    print(f"\nEvaluating query: {query['query']}")
    
    # Convert to proper types
    query_obj = SearchQuery(**query)
    result_obj = RetrievalResult(**result)
    
    # Get evaluation results
    evaluation_results = metrics.evaluate_retrieval(query_obj, result_obj)
    
    # Print results
    print("\nMetric Results:")
    for metric in evaluation_results:
        print(f"- {metric.metric_name}: {metric.score:.3f}")
        if metric.details:
            print(f"  Details: {metric.details}")

def evaluate_domain(domain_name: str, corpus_file: str, queries_file: str):
    """Evaluate RAG system on a specific domain"""
    print(f"\n=== Evaluating {domain_name} Domain ===")
    
    # Load domain-specific data
    corpus, test_cases = load_test_data(corpus_file, queries_file)
    
    # Initialize metrics
    metrics = RetrievalMetrics()
    
    # Example 1: Single query evaluation
    print(f"\n1. Single Query Evaluation for {domain_name}")
    test_case = test_cases["test_cases"][0]
    evaluate_single_query(metrics, test_case["query"], test_case["simulated_result"])
    
    # Example 2: Generate full report
    print(f"\n2. Generating Full Evaluation Report for {domain_name}")
    reporter = RAGEvaluationReporter(output_dir=f"example_reports/{domain_name.lower()}")
    report_path = reporter.generate_report(test_cases, corpus)
    
    print(f"\nFull evaluation report generated at: {report_path}")
    print("\nReport includes:")
    print("- Overall performance metrics (CSV)")
    print("- Query-by-query analysis (Markdown)")
    print("- Metric distributions (PNG)")
    print("- Statistical summaries (CSV)")
    print("- Version information (JSON)")
    
    return report_path

def main():
    # Define test domains
    domains = [
        {
            "name": "Finance",
            "corpus": "financial_corpus.json",
            "queries": "test_queries.json"
        },
        {
            "name": "MachineLearning",
            "corpus": "ml_corpus.json",
            "queries": "ml_queries.json"
        }
    ]
    
    # Evaluate each domain
    report_paths = {}
    for domain in domains:
        report_paths[domain["name"]] = evaluate_domain(
            domain["name"],
            domain["corpus"],
            domain["queries"]
        )
    
    # Print summary
    print("\n=== Evaluation Complete ===")
    print("\nReport Locations:")
    for domain, path in report_paths.items():
        print(f"{domain}: {path}")
    
    print("\nTo compare results across domains, check the metric_summaries.csv files in each report directory.")

if __name__ == "__main__":
    main() 