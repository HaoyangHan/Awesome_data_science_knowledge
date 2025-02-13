import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from llm_as_judge.metrics.evaluation_metrics import EvaluationMetrics

def analyze_question_evaluation(data_path: str, output_dir: Path):
    """Basic analysis of question evaluation data.
    
    Args:
        data_path: Path to the question evaluation CSV file
        output_dir: Directory to save outputs
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Initialize report
    report = ["# Question Evaluation Analysis Report\n"]
    
    # Basic statistics
    print("\n=== Basic Statistics ===")
    report.append("## Score Statistics\n")
    
    print("\nLLM Generated Score Statistics:")
    llm_stats = df['LLM Generated Score'].describe()
    print(llm_stats)
    report.extend(["\n### LLM Generated Score Statistics:\n```\n", llm_stats.to_string(), "\n```\n"])
    
    print("\nHuman Evaluation Score Statistics:")
    human_stats = df['Human Evaluation Score'].describe()
    print(human_stats)
    report.extend(["\n### Human Evaluation Score Statistics:\n```\n", human_stats.to_string(), "\n```\n"])
    
    # Calculate comprehensive metrics
    comprehensive_metrics = EvaluationMetrics.generate_comprehensive_metrics(
        df,
        ['LLM Generated Score'],
        ['Human Evaluation Score']
    )
    
    # Add comprehensive metrics to report
    report.extend(["\n## Comprehensive Evaluation Metrics\n"])
    
    metric_values = comprehensive_metrics['Generated Score']
    report.extend([
        "\n### Agreement Metrics\n```\n",
        f"Agreement Score: {metric_values['agreement']:.3f}\n",
        f"Rank Correlation: {metric_values['rank_correlation']:.3f}\n",
        f"Cohen's Kappa: {metric_values['cohens_kappa']:.3f}\n",
        "```\n"
    ])
    
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
    
    # Save report
    with open(output_dir / 'question_evaluation_report.md', 'w') as f:
        f.write(''.join(report))

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