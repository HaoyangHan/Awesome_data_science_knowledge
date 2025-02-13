import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_answer_evaluation(data_path: str):
    """Basic analysis of answer evaluation data.
    
    Args:
        data_path: Path to the answer evaluation CSV file
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Get metric columns
    metrics = ['Stand-alone Quality', 'Readiness', 'Relevance', 'Completeness']
    
    # Basic statistics for each metric
    print("\n=== Basic Statistics ===")
    for metric in metrics:
        print(f"\n{metric} Statistics:")
        print("\nLLM Scores:")
        print(df[f'LLM {metric}'].describe())
        print("\nHuman Scores:")
        print(df[f'Human {metric}'].describe())
    
    # Calculate correlations
    print("\n=== LLM-Human Score Correlations ===")
    for metric in metrics:
        correlation = df[f'LLM {metric}'].corr(df[f'Human {metric}'])
        print(f"{metric}: {correlation:.3f}")
    
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
    
    # Save plot
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'answer_score_distributions.png')
    plt.close()
    
    # Find high quality answers (score >= 4.0)
    print("\n=== High Quality Answer Examples ===")
    for metric in metrics:
        high_quality = df[
            (df[f'LLM {metric}'] >= 4.0) & 
            (df[f'Human {metric}'] >= 4.0)
        ]
        if not high_quality.empty:
            print(f"\n{metric} - Example high quality answer:")
            example = high_quality.iloc[0]
            print(f"Question: {example['Question']}")
            print(f"Answer: {example['Answer']}")
            print(f"LLM Score: {example[f'LLM {metric}']:.2f}")
            print(f"Human Score: {example[f'Human {metric}']:.2f}")

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Data path
    data_path = project_root / 'data' / 'llm_judge_answer_evaluation_sample.csv'
    
    # Run analysis
    analyze_answer_evaluation(str(data_path))
    print("\nAnalysis complete! Check 'outputs' directory for visualizations.")

if __name__ == "__main__":
    main() 