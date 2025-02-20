import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from llm_as_judge.metrics.evaluation_metrics import EvaluationMetrics
from llm_as_judge.metrics.metrics_recorder import MetricsRecorder
from llm_as_judge.score_analysis.score_distribution_analyzer import ScoreDistributionAnalyzer
import numpy as np

def analyze_question_evaluation(data_path: str, output_dir: Path):
    """Basic analysis of question evaluation data.
    
    Args:
        data_path: Path to the question evaluation CSV file
        output_dir: Directory to save outputs
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Initialize report and metrics dictionary
    report = ["# Question Evaluation Analysis Report\n"]
    all_metrics = {}
    
    # Basic statistics
    print("\n=== Basic Statistics ===")
    report.append("## Score Statistics\n")
    
    print("\nLLM Generated Score Statistics:")
    llm_stats = df['LLM Generated Score'].describe()
    print(llm_stats)
    report.extend(["\n### LLM Generated Score Statistics:\n```\n", llm_stats.to_string(), "\n```\n"])
    all_metrics.update({f"llm_generated_score_{k}": v for k, v in llm_stats.to_dict().items()})
    
    print("\nHuman Evaluation Score Statistics:")
    human_stats = df['Human Evaluation Score'].describe()
    print(human_stats)
    report.extend(["\n### Human Evaluation Score Statistics:\n```\n", human_stats.to_string(), "\n```\n"])
    all_metrics.update({f"human_evaluation_score_{k}": v for k, v in human_stats.to_dict().items()})
    
    # New: Distribution Analysis
    llm_scores = df['LLM Generated Score'].values
    human_scores = df['Human Evaluation Score'].values
    dist_analyzer = ScoreDistributionAnalyzer(llm_scores, human_scores)
    
    # Analyze distributions
    dist_analysis = dist_analyzer.analyze_distributions()
    report.extend([
        "\n## Distribution Analysis\n",
        "```\n",
        f"LLM Stats: {dist_analysis['llm_stats']}\n",
        f"Human Stats: {dist_analysis['human_stats']}\n",
        f"KS Test: {dist_analysis['ks_test']}\n",
        "```\n"
    ])
    all_metrics.update({
        'score_distribution': dist_analysis
    })
    
    # Generate normalized plots and analysis
    for norm_method in ['zscore', 'minmax', 'robust']:
        norm_plot_path = output_dir / f'score_{norm_method}_normalized.png'
        dist_analyzer.plot_distributions(
            str(norm_plot_path),
            normalized=True,
            method=norm_method,
            title=f'{norm_method.capitalize()} Normalized Score Distributions'
        )
        
        norm_diff = dist_analyzer.get_normalization_differences(method=norm_method)
        report.extend([
            f"\n### {norm_method.capitalize()} Normalization Differences\n",
            "```\n",
            f"{norm_diff}\n",
            "```\n"
        ])
        all_metrics.update({
            f'score_{norm_method}_differences': norm_diff
        })
    
    # Calculate comprehensive metrics
    comprehensive_metrics = EvaluationMetrics.generate_comprehensive_metrics(
        df,
        ['LLM Generated Score'],
        ['Human Evaluation Score']
    )
    
    # Add comprehensive metrics to report and metrics dictionary
    report.extend(["\n## Comprehensive Evaluation Metrics\n"])
    
    metric_values = comprehensive_metrics['Generated Score']
    report.extend([
        "\n### Agreement Metrics\n```\n",
        f"Agreement Score: {metric_values['agreement']:.3f}\n",
        f"Rank Correlation: {metric_values['rank_correlation']:.3f}\n",
        f"Cohen's Kappa: {metric_values['cohens_kappa']:.3f}\n",
        "```\n"
    ])
    all_metrics.update({
        'agreement_score': metric_values['agreement'],
        'rank_correlation': metric_values['rank_correlation'],
        'cohens_kappa': metric_values['cohens_kappa']
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
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df['LLM Generated Score'], label='LLM Score')
    sns.kdeplot(data=df['Human Evaluation Score'], label='Human Score')
    plt.title('Score Distribution: LLM vs Human Evaluation')
    plt.xlabel('Score')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig(output_dir / 'question_score_distribution.png')
    plt.close()
    
    # Plot bias analysis
    plt.figure(figsize=(12, 6))
    
    # Position bias plot
    plt.subplot(1, 2, 1)
    plt.scatter(range(len(df)), df['LLM Generated Score'], alpha=0.5, label='LLM Scores')
    plt.scatter(range(len(df)), df['Human Evaluation Score'], alpha=0.5, label='Human Scores')
    plt.title('Position Bias Analysis')
    plt.xlabel('Question Position')
    plt.ylabel('Score')
    plt.legend()
    
    # Length bias plot
    plt.subplot(1, 2, 2)
    df['question_length'] = df['LLM Generated Question'].str.len()
    plt.scatter(df['question_length'], df['LLM Generated Score'], alpha=0.5, label='LLM Scores')
    plt.scatter(df['question_length'], df['Human Evaluation Score'], alpha=0.5, label='Human Scores')
    plt.title('Length Bias Analysis')
    plt.xlabel('Question Length')
    plt.ylabel('Score')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'bias_analysis.png')
    plt.close()
    
    # Find examples of high agreement
    high_agreement = df[abs(df['LLM Generated Score'] - df['Human Evaluation Score']) < 0.1]
    print("\n=== Examples of High Agreement ===")
    report.extend(["\n## High Agreement Examples\n"])
    
    for idx, row in high_agreement.head(3).iterrows():
        print(f"\nGround Truth: {row['Ground Truth Question']}")
        print(f"Generated: {row['LLM Generated Question']}")
        print(f"Scores - LLM: {row['LLM Generated Score']:.2f}, Human: {row['Human Evaluation Score']:.2f}")
        
        report.extend([
            f"\n### Example {idx+1}:\n",
            f"- Ground Truth: {row['Ground Truth Question']}\n",
            f"- Generated: {row['LLM Generated Question']}\n",
            f"- LLM Score: {row['LLM Generated Score']:.2f}\n",
            f"- Human Score: {row['Human Evaluation Score']:.2f}\n"
        ])
        
        all_metrics.update({
            f"high_agreement_example_{idx+1}_llm_score": row['LLM Generated Score'],
            f"high_agreement_example_{idx+1}_human_score": row['Human Evaluation Score']
        })
    
    # Add high agreement statistics
    all_metrics.update({
        'high_agreement_count': len(high_agreement),
        'high_agreement_percentage': len(high_agreement) / len(df) * 100
    })
    
    # Save report
    with open(output_dir / 'question_evaluation_report.md', 'w') as f:
        f.write(''.join(report))
        
    # Record metrics
    metrics_recorder = MetricsRecorder(evaluation_type="question_basic")
    metrics_recorder.record_metrics(all_metrics)
    print(f"\nMetrics recorded in: {metrics_recorder.output_path}")

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Setup paths
    data_path = project_root / 'data' / 'llm_judge_evaluation_sample.csv'
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Run analysis
    analyze_question_evaluation(str(data_path), output_dir)
    print(f"\nAnalysis complete! Check outputs in: {output_dir}")

if __name__ == "__main__":
    main() 