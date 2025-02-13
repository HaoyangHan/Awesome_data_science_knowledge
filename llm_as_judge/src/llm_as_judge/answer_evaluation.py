import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class AnswerEvaluationAnalyzer:
    """A class for analyzing LLM and Human evaluations of answers."""
    
    def __init__(self, data_path: Union[str, Path]):
        """Initialize the analyzer with data path.
        
        Args:
            data_path: Path to the CSV file containing evaluation data
        """
        self.data = pd.read_csv(data_path)
        self.metrics = ['Stand-alone Quality', 'Readiness', 'Relevance', 'Completeness']
        self._validate_data()
    
    def _validate_data(self):
        """Validate that the data contains required columns."""
        required_cols = ['Chunk', 'Question', 'Answer']
        for metric in self.metrics:
            required_cols.extend([f'LLM {metric}', f'Human {metric}'])
        
        missing_cols = [col for col in required_cols if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def get_score_statistics(self, evaluator_type: str = 'all') -> pd.DataFrame:
        """Get basic statistics for all metrics.
        
        Args:
            evaluator_type: 'llm', 'human', or 'all'
            
        Returns:
            DataFrame with statistics for each metric
        """
        stats_list = []
        
        for metric in self.metrics:
            if evaluator_type.lower() in ['llm', 'all']:
                llm_stats = self.data[f'LLM {metric}'].describe()
                llm_stats.name = f'LLM {metric}'
                stats_list.append(llm_stats)
            
            if evaluator_type.lower() in ['human', 'all']:
                human_stats = self.data[f'Human {metric}'].describe()
                human_stats.name = f'Human {metric}'
                stats_list.append(human_stats)
        
        return pd.concat(stats_list, axis=1)
    
    def calculate_agreement(self) -> pd.DataFrame:
        """Calculate agreement between LLM and Human evaluations.
        
        Returns:
            DataFrame with correlation and mean absolute difference for each metric
        """
        agreement_data = []
        
        for metric in self.metrics:
            llm_scores = self.data[f'LLM {metric}']
            human_scores = self.data[f'Human {metric}']
            
            correlation = llm_scores.corr(human_scores)
            mae = np.abs(llm_scores - human_scores).mean()
            rmse = np.sqrt(((llm_scores - human_scores) ** 2).mean())
            
            agreement_data.append({
                'Metric': metric,
                'Correlation': correlation,
                'MAE': mae,
                'RMSE': rmse
            })
        
        return pd.DataFrame(agreement_data)
    
    def analyze_answer_quality(self, min_score: float = 4.0) -> Dict:
        """Analyze high quality answers based on score threshold.
        
        Args:
            min_score: Minimum score to consider an answer high quality
            
        Returns:
            Dictionary with analysis results
        """
        high_quality = {}
        
        for metric in self.metrics:
            llm_high = self.data[self.data[f'LLM {metric}'] >= min_score]
            human_high = self.data[self.data[f'Human {metric}'] >= min_score]
            
            # Find answers rated highly by both
            both_high = self.data[
                (self.data[f'LLM {metric}'] >= min_score) & 
                (self.data[f'Human {metric}'] >= min_score)
            ]
            
            high_quality[metric] = {
                'llm_count': len(llm_high),
                'human_count': len(human_high),
                'agreement_count': len(both_high),
                'example_answers': both_high['Answer'].tolist()[:3]  # Top 3 examples
            }
        
        return high_quality
    
    def plot_score_distributions(self, save_path: Optional[str] = None):
        """Plot distribution of scores for each metric.
        
        Args:
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Score Distributions: LLM vs Human Evaluations')
        
        for idx, metric in enumerate(self.metrics):
            ax = axes[idx // 2, idx % 2]
            
            sns.kdeplot(data=self.data[f'LLM {metric}'], ax=ax, label='LLM')
            sns.kdeplot(data=self.data[f'Human {metric}'], ax=ax, label='Human')
            
            ax.set_title(metric)
            ax.set_xlabel('Score')
            ax.set_ylabel('Density')
            ax.legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def generate_report(self, output_path: str):
        """Generate a comprehensive analysis report.
        
        Args:
            output_path: Path to save the markdown report
        """
        stats = self.get_score_statistics()
        agreement = self.calculate_agreement()
        quality_analysis = self.analyze_answer_quality()
        
        report = [
            "# Answer Evaluation Analysis Report\n",
            "## Score Statistics\n",
            f"```\n{stats.to_string()}\n```\n",
            "\n## LLM-Human Agreement\n",
            f"```\n{agreement.to_string()}\n```\n",
            "\n## High Quality Answer Analysis\n"
        ]
        
        for metric, data in quality_analysis.items():
            report.extend([
                f"\n### {metric}\n",
                f"- LLM High Scores: {data['llm_count']}\n",
                f"- Human High Scores: {data['human_count']}\n",
                f"- Agreement Count: {data['agreement_count']}\n",
                "\nExample High Quality Answers:\n"
            ])
            for idx, answer in enumerate(data['example_answers'], 1):
                report.append(f"{idx}. {answer}\n")
        
        with open(output_path, 'w') as f:
            f.write(''.join(report)) 