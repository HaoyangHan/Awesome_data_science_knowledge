import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_question_evaluation(data_path: str, output_dir: Path):
    """Basic analysis of question evaluation data.
    
    Args:
        data_path: Path to the question evaluation CSV file
        output_dir: Directory to save outputs
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Basic statistics
    print("\n=== Basic Statistics ===")
    print("\nLLM Generated Score Statistics:")
    print(df['LLM Generated Score'].describe())
    print("\nHuman Evaluation Score Statistics:")
    print(df['Human Evaluation Score'].describe())
    
    # Score correlation
    correlation = df['LLM Generated Score'].corr(df['Human Evaluation Score'])
    print(f"\nCorrelation between LLM and Human scores: {correlation:.3f}")
    
    # Plot score distributions
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df['LLM Generated Score'], label='LLM Score')
    sns.kdeplot(data=df['Human Evaluation Score'], label='Human Score')
    plt.title('Score Distribution: LLM vs Human Evaluation')
    plt.xlabel('Score')
    plt.ylabel('Density')
    plt.legend()
    
    # Save plot
    plt.savefig(output_dir / 'question_score_distribution.png')
    plt.close()
    
    # Find examples of high agreement
    high_agreement = df[abs(df['LLM Generated Score'] - df['Human Evaluation Score']) < 0.1]
    
    # Generate report
    report = ["# Question Evaluation Analysis Report\n",
              "## Score Statistics\n",
              "### LLM Generated Score Statistics:\n",
              "```\n" + df['LLM Generated Score'].describe().to_string() + "\n```\n",
              "\n### Human Evaluation Score Statistics:\n",
              "```\n" + df['Human Evaluation Score'].describe().to_string() + "\n```\n",
              f"\n## Score Correlation\nCorrelation between LLM and Human scores: {correlation:.3f}\n",
              "\n## High Agreement Examples\n"]
    
    for _, row in high_agreement.head(3).iterrows():
        report.extend([
            f"\n### Example {_+1}:\n",
            f"- Ground Truth: {row['Ground Truth Question']}\n",
            f"- Generated: {row['LLM Generated Question']}\n",
            f"- LLM Score: {row['LLM Generated Score']:.2f}\n",
            f"- Human Score: {row['Human Evaluation Score']:.2f}\n"
        ])
    
    with open(output_dir / 'question_evaluation_report.md', 'w') as f:
        f.write(''.join(report))
    
    print("\n=== Examples of High Agreement ===")
    for _, row in high_agreement.head(3).iterrows():
        print(f"\nGround Truth: {row['Ground Truth Question']}")
        print(f"Generated: {row['LLM Generated Question']}")
        print(f"Scores - LLM: {row['LLM Generated Score']:.2f}, Human: {row['Human Evaluation Score']:.2f}")

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