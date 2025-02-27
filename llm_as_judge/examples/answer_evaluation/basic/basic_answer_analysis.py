import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from llm_as_judge.metrics.evaluation_metrics import EvaluationMetrics
from llm_as_judge.metrics.metrics_recorder import MetricsRecorder
from llm_as_judge.score_analysis.score_distribution_analyzer import ScoreDistributionAnalyzer
import numpy as np

def analyze_answer_evaluation(data_path: str, output_dir: Path):
    """Basic analysis of answer evaluation data.
    
    Args:
        data_path: Path to the answer evaluation CSV file
        output_dir: Directory to save outputs
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Get metric columns
    metrics = ['Stand-alone Quality', 'Readiness', 'Relevance', 'Completeness']
    llm_columns = [f'LLM {m}' for m in metrics]
    human_columns = [f'Human {m}' for m in metrics]
    
    # Initialize report and metrics dictionary
    report = ["# Answer Evaluation Analysis Report\n"]
    all_metrics = {}
    
    # Basic statistics for each metric
    print("\n=== Basic Statistics ===")
    report.append("## Score Statistics\n")
    
    for metric in metrics:
        print(f"\n{metric} Statistics:")
        report.extend([f"\n### {metric} Statistics\n"])
        
        print("\nLLM Scores:")
        llm_stats = df[f'LLM {metric}'].describe()
        print(llm_stats)
        report.extend(["\n#### LLM Scores:\n```\n", llm_stats.to_string(), "\n```\n"])
        all_metrics.update({f"llm_{metric.lower().replace('-', '_')}_{k}": v 
                           for k, v in llm_stats.to_dict().items()})
        
        print("\nHuman Scores:")
        human_stats = df[f'Human {metric}'].describe()
        print(human_stats)
        report.extend(["\n#### Human Scores:\n```\n", human_stats.to_string(), "\n```\n"])
        all_metrics.update({f"human_{metric.lower().replace('-', '_')}_{k}": v 
                           for k, v in human_stats.to_dict().items()})
        
        # New: Distribution Analysis
        llm_scores = df[f'LLM {metric}'].values
        human_scores = df[f'Human {metric}'].values
        dist_analyzer = ScoreDistributionAnalyzer(llm_scores, human_scores)
        
        # Analyze distributions
        dist_analysis = dist_analyzer.analyze_distributions()
        report.extend([
            f"\n### {metric} Distribution Analysis\n",
            "```\n",
            f"LLM Stats: {dist_analysis['llm_stats']}\n",
            f"Human Stats: {dist_analysis['human_stats']}\n",
            f"KS Test: {dist_analysis['ks_test']}\n",
            "```\n"
        ])
        all_metrics.update({
            f"{metric.lower().replace('-', '_')}_distribution": dist_analysis
        })
        
        # Generate normalized plots and analysis
        for norm_method in ['zscore', 'minmax', 'robust']:
            norm_plot_path = output_dir / f'{metric.lower().replace(" ", "_")}_{norm_method}_normalized.png'
            dist_analyzer.plot_distributions(
                str(norm_plot_path),
                normalized=True,
                method=norm_method,
                title=f'{metric} - {norm_method.capitalize()} Normalized Distributions'
            )
            
            norm_diff = dist_analyzer.get_normalization_differences(method=norm_method)
            report.extend([
                f"\n### {metric} - {norm_method.capitalize()} Normalization Differences\n",
                "```\n",
                f"{norm_diff}\n",
                "```\n"
            ])
            all_metrics.update({
                f"{metric.lower().replace('-', '_')}_{norm_method}_differences": norm_diff
            })
    
    # Calculate comprehensive metrics
    comprehensive_metrics = EvaluationMetrics.generate_comprehensive_metrics(
        df, llm_columns, human_columns
    )
    
    # Add comprehensive metrics to report and metrics dictionary
    report.extend(["\n## Comprehensive Evaluation Metrics\n"])
    
    for metric_name, metric_values in comprehensive_metrics.items():
        if metric_name != 'bias':
            report.extend([
                f"\n### {metric_name}\n",
                "```\n",
                f"Agreement Score: {metric_values['agreement']:.3f}\n",
                f"Rank Correlation: {metric_values['rank_correlation']:.3f}\n",
                f"Cohen's Kappa: {metric_values['cohens_kappa']:.3f}\n",
                "```\n"
            ])
            all_metrics.update({
                f"{metric_name.lower().replace('-', '_')}_agreement": metric_values['agreement'],
                f"{metric_name.lower().replace('-', '_')}_rank_correlation": metric_values['rank_correlation'],
                f"{metric_name.lower().replace('-', '_')}_cohens_kappa": metric_values['cohens_kappa']
            })
    
    # Add bias analysis
    report.extend(["\n## Bias Analysis\n"])
    for col, bias_values in comprehensive_metrics['bias'].items():
        report.extend([
            f"\n### {col}\n",
            "```\n",
            f"Position Bias: {bias_values['position_bias']:.3f}\n",
            f"Length Bias: {bias_values['length_bias']:.3f}\n",
            "```\n"
        ])
        all_metrics.update({
            f"{col.lower().replace(' ', '_')}_position_bias": bias_values['position_bias'],
            f"{col.lower().replace(' ', '_')}_length_bias": bias_values['length_bias']
        })
    
    # Plot score distributions
    plt.figure(figsize=(15, 10))
    for idx, metric in enumerate(metrics, 1):
        plt.subplot(2, 2, idx)
        sns.kdeplot(data=df[f'LLM {metric}'], label='LLM')
        sns.kdeplot(data=df[f'Human {metric}'], label='Human')
        plt.title(metric)
        plt.xlabel('Score')
        plt.ylabel('Density')
        plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'answer_score_distributions.png')
    plt.close()
    
    # Plot bias analysis
    plt.figure(figsize=(12, 6))
    
    # Position bias plot
    plt.subplot(1, 2, 1)
    for col in llm_columns:
        plt.scatter(range(len(df)), df[col], alpha=0.5, label=col)
    plt.title('Position Bias Analysis')
    plt.xlabel('Answer Position')
    plt.ylabel('Score')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'bias_analysis.png')
    plt.close()
    
    # Find high quality answers
    print("\n=== High Quality Answer Examples ===")
    report.extend(["\n## High Quality Answer Examples\n"])
    
    for metric in metrics:
        high_quality = df[
            (df[f'LLM {metric}'] >= 4.0) & 
            (df[f'Human {metric}'] >= 4.0)
        ]
        if not high_quality.empty:
            print(f"\n{metric} - Example high quality answer:")
            report.extend([f"\n### {metric}\n"])
            
            example = high_quality.iloc[0]
            print(f"Question: {example['Question']}")
            print(f"Answer: {example['Answer']}")
            print(f"LLM Score: {example[f'LLM {metric}']:.2f}")
            print(f"Human Score: {example[f'Human {metric}']:.2f}")
            
            report.extend([
                f"- Question: {example['Question']}\n",
                f"- Answer: {example['Answer']}\n",
                f"- LLM Score: {example[f'LLM {metric}']:.2f}\n",
                f"- Human Score: {example[f'Human {metric}']:.2f}\n"
            ])
            
            all_metrics.update({
                f"high_quality_{metric.lower().replace('-', '_')}_count": len(high_quality),
                f"high_quality_{metric.lower().replace('-', '_')}_example_llm_score": example[f'LLM {metric}'],
                f"high_quality_{metric.lower().replace('-', '_')}_example_human_score": example[f'Human {metric}']
            })
    
    # Save report
    with open(output_dir / 'answer_evaluation_report.md', 'w') as f:
        f.write(''.join(report))
        
    # Record metrics
    metrics_recorder = MetricsRecorder(evaluation_type="answer_basic")
    metrics_recorder.record_metrics(all_metrics)
    print(f"\nMetrics recorded in: {metrics_recorder.output_path}")

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Setup paths
    data_path = project_root / 'data' / 'llm_judge_answer_evaluation_sample.csv'
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Run analysis
    analyze_answer_evaluation(str(data_path), output_dir)
    print(f"\nAnalysis complete! Check outputs in: {output_dir}")

if __name__ == "__main__":
    main() 