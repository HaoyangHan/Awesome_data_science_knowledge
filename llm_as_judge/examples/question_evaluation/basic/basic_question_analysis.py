import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_question_evaluation(data_path: str):
    """Basic analysis of question evaluation data.
    
    Args:
        data_path: Path to the question evaluation CSV file
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
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'question_score_distribution.png')
    plt.close()
    
    # Find examples of high agreement
    high_agreement = df[abs(df['LLM Generated Score'] - df['Human Evaluation Score']) < 0.1]
    print("\n=== Examples of High Agreement ===")
    for _, row in high_agreement.head(3).iterrows():
        print(f"\nGround Truth: {row['Ground Truth Question']}")
        print(f"Generated: {row['LLM Generated Question']}")
        print(f"Scores - LLM: {row['LLM Generated Score']:.2f}, Human: {row['Human Evaluation Score']:.2f}")

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Data path
    data_path = project_root / 'data' / 'llm_judge_evaluation_sample.csv'
    
    # Run analysis
    analyze_question_evaluation(str(data_path))
    print("\nAnalysis complete! Check 'outputs' directory for visualizations.")

if __name__ == "__main__":
    main() 