import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # Initialize report
    report = ["# Answer Evaluation Analysis Report\n"]
    
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
        
        print("\nHuman Scores:")
        human_stats = df[f'Human {metric}'].describe()
        print(human_stats)
        report.extend(["\n#### Human Scores:\n```\n", human_stats.to_string(), "\n```\n"])
    
    # Calculate correlations
    print("\n=== LLM-Human Score Correlations ===")
    report.extend(["\n## LLM-Human Score Correlations\n"])
    correlations = []
    for metric in metrics:
        correlation = df[f'LLM {metric}'].corr(df[f'Human {metric}'])
        print(f"{metric}: {correlation:.3f}")
        correlations.append({"Metric": metric, "Correlation": correlation})
    
    corr_df = pd.DataFrame(correlations)
    report.extend(["\n```\n", corr_df.to_string(), "\n```\n"])
    
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
    
    # Save report
    with open(output_dir / 'answer_evaluation_report.md', 'w') as f:
        f.write(''.join(report))

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