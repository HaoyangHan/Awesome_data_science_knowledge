import json
from pathlib import Path
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os
from ..metrics.retrieval_metrics import RetrievalMetrics
from ..utils.data_types import SearchQuery, RetrievalResult

class RAGEvaluationReporter:
    def __init__(self, output_dir: str = "example_reports", version: str = None):
        self.metrics = RetrievalMetrics()
        self.base_output_dir = Path(output_dir)
        self.version = version or datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create versioned output directory
        self.output_dir = self.base_output_dir / f"v{self.version}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different output types
        self.csv_dir = self.output_dir / "csv"
        self.plots_dir = self.output_dir / "plots"
        self.markdown_dir = self.output_dir / "markdown"
        
        for dir_path in [self.csv_dir, self.plots_dir, self.markdown_dir]:
            dir_path.mkdir(exist_ok=True)
        
    def generate_report(self, test_cases: Dict, corpus: Dict) -> str:
        """Generate a comprehensive evaluation report with versioning"""
        
        # Collect results
        all_results = []
        metric_summaries = {}
        
        for test_case in test_cases["test_cases"]:
            query = SearchQuery(**test_case["query"])
            result = RetrievalResult(**test_case["simulated_result"])
            
            # Get evaluation metrics
            evaluation_results = self.metrics.evaluate_retrieval(query, result)
            
            # Organize results
            result_dict = {
                "query_id": query.query_id,
                "query": query.query,
                "expected_content": query.expected_relevant_content
            }
            
            for metric in evaluation_results:
                result_dict[metric.metric_name] = metric.score
                
                # Collect metric summaries
                if metric.metric_name not in metric_summaries:
                    metric_summaries[metric.metric_name] = []
                metric_summaries[metric.metric_name].append(metric.score)
            
            all_results.append(result_dict)
        
        # Generate different report formats
        self._save_csv_reports(all_results, metric_summaries)
        self._generate_markdown_report(all_results, metric_summaries, test_cases, corpus)
        self._generate_visualizations(metric_summaries)
        
        # Create version info file
        self._save_version_info(test_cases, corpus)
        
        return str(self.output_dir)
    
    def _save_csv_reports(self, results: List[Dict], metric_summaries: Dict):
        """Save results in CSV format"""
        # Save detailed results
        detailed_results_path = self.csv_dir / "detailed_results.csv"
        pd.DataFrame(results).to_csv(detailed_results_path, index=False)
        
        # Save metric summaries
        summary_data = {
            metric: {
                'mean': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'std': pd.Series(values).std()
            }
            for metric, values in metric_summaries.items()
        }
        
        summary_df = pd.DataFrame.from_dict(summary_data, orient='index')
        summary_df.to_csv(self.csv_dir / "metric_summaries.csv")
        
        # Save raw metric values
        metric_values_df = pd.DataFrame(metric_summaries)
        metric_values_df.to_csv(self.csv_dir / "metric_values.csv", index=False)
    
    def _generate_markdown_report(self, results: List[Dict], metric_summaries: Dict, 
                                test_cases: Dict, corpus: Dict):
        """Generate detailed markdown report"""
        report_path = self.markdown_dir / "evaluation_report.md"
        
        with open(report_path, "w") as f:
            f.write(f"# RAG System Evaluation Report (v{self.version})\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall Summary
            f.write("## Overall Performance Summary\n\n")
            for metric_name, values in metric_summaries.items():
                avg_value = sum(values) / len(values)
                f.write(f"- **{metric_name}**: {avg_value:.3f} (average)\n")
            f.write("\n")
            
            # Detailed Results Table
            f.write("## Detailed Results\n\n")
            df = pd.DataFrame(results)
            f.write(df.to_markdown(index=False))
            f.write("\n\n")
            
            # Query Analysis
            f.write("## Query-by-Query Analysis\n\n")
            for result in results:
                f.write(f"### Query {result['query_id']}\n")
                f.write(f"- **Query**: {result['query']}\n")
                f.write(f"- **Expected Content**: {result['expected_content']}\n")
                f.write("- **Metrics**:\n")
                for key, value in result.items():
                    if key not in ['query_id', 'query', 'expected_content']:
                        f.write(f"  - {key}: {value:.3f}\n")
                f.write("\n")
            
            # Test Dataset Statistics
            f.write("## Test Dataset Statistics\n\n")
            f.write(f"- Number of test queries: {len(test_cases['test_cases'])}\n")
            f.write(f"- Number of documents in corpus: {len(corpus['documents'])}\n")
            f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            self._add_recommendations(f, metric_summaries)
    
    def _generate_visualizations(self, metric_summaries: Dict):
        """Generate visualization plots"""
        # Distribution plot
        plt.figure(figsize=(12, 6))
        
        plt.subplot(121)
        df = pd.DataFrame(metric_summaries)
        df.boxplot()
        plt.title("Metric Distributions")
        plt.xticks(rotation=45)
        
        # Average values plot
        plt.subplot(122)
        averages = {metric: sum(values)/len(values) for metric, values in metric_summaries.items()}
        plt.bar(averages.keys(), averages.values())
        plt.title("Average Metric Values")
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / "metric_visualizations.png")
        plt.close()
        
        # Generate individual metric plots
        for metric_name, values in metric_summaries.items():
            plt.figure(figsize=(8, 4))
            plt.hist(values, bins=10, alpha=0.7)
            plt.title(f"{metric_name} Distribution")
            plt.xlabel("Score")
            plt.ylabel("Frequency")
            plt.savefig(self.plots_dir / f"{metric_name}_distribution.png")
            plt.close()
    
    def _save_version_info(self, test_cases: Dict, corpus: Dict):
        """Save version information"""
        version_info = {
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "test_cases_count": len(test_cases["test_cases"]),
            "corpus_size": len(corpus["documents"]),
            "output_files": {
                "csv": [f.name for f in self.csv_dir.glob("*.csv")],
                "plots": [f.name for f in self.plots_dir.glob("*.png")],
                "markdown": [f.name for f in self.markdown_dir.glob("*.md")]
            }
        }
        
        with open(self.output_dir / "version_info.json", "w") as f:
            json.dump(version_info, f, indent=2)
    
    def _add_recommendations(self, f, metric_summaries: Dict):
        """Add recommendations based on metric performance"""
        averages = {metric: sum(values)/len(values) for metric, values in metric_summaries.items()}
        
        if averages.get('precision_at_k', 0) < 0.7:
            f.write("- Consider improving the retrieval precision by:\n")
            f.write("  - Refining the document ranking algorithm\n")
            f.write("  - Adjusting relevance thresholds\n")
            f.write("  - Implementing better query preprocessing\n")
        
        if averages.get('semantic_similarity', 0) < 0.7:
            f.write("- Enhance semantic understanding by:\n")
            f.write("  - Using a more sophisticated embedding model\n")
            f.write("  - Implementing query expansion\n")
            f.write("  - Adding domain-specific pre-training\n")
        
        if averages.get('keyword_coverage', 0) < 0.7:
            f.write("- Improve keyword coverage through:\n")
            f.write("  - Enhanced keyword extraction\n")
            f.write("  - Synonym expansion\n")
            f.write("  - Better document preprocessing\n") 