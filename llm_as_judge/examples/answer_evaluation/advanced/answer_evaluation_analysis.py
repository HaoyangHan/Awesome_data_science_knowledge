import os
from pathlib import Path
from llm_as_judge.answer_evaluation import AnswerEvaluationAnalyzer
from llm_as_judge.metrics.metrics_recorder import MetricsRecorder
from llm_as_judge.score_analysis.score_distribution_analyzer import ScoreDistributionAnalyzer
import numpy as np

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Setup paths
    data_path = project_root / 'data' / 'llm_judge_answer_evaluation_sample.csv'
    output_dir = Path(__file__).parent / 'output'  # Fixed output path
    output_dir.mkdir(exist_ok=True)
    
    # Initialize analyzer and metrics recorder
    analyzer = AnswerEvaluationAnalyzer(data_path)
    metrics_recorder = MetricsRecorder(evaluation_type="answer_advanced")
    
    # Dictionary to store all metrics
    all_metrics = {}
    
    # 1. Generate basic statistics
    print("\n=== Score Statistics ===")
    stats = analyzer.get_score_statistics()
    print(stats)
    all_metrics.update({f"stats_{k}": v for k, v in stats.to_dict().items()})
    
    # 2. Calculate LLM-Human agreement
    print("\n=== LLM-Human Agreement Analysis ===")
    agreement = analyzer.calculate_agreement()
    print(agreement)
    all_metrics.update({f"agreement_{k}": v for k, v in agreement.to_dict().items()})
    
    # 3. Analyze high quality answers
    print("\n=== High Quality Answer Analysis ===")
    quality_analysis = analyzer.analyze_answer_quality(min_score=4.0)
    for metric, data in quality_analysis.items():
        print(f"\n{metric}:")
        print(f"LLM High Scores: {data['llm_count']}")
        print(f"Human High Scores: {data['human_count']}")
        print(f"Agreement Count: {data['agreement_count']}")
        all_metrics.update({
            f"quality_{metric}_llm_count": data['llm_count'],
            f"quality_{metric}_human_count": data['human_count'],
            f"quality_{metric}_agreement_count": data['agreement_count']
        })
    
    # 4. Generate visualizations
    print("\n=== Generating Visualizations ===")
    plot_path = output_dir / 'score_distributions.png'
    analyzer.plot_score_distributions(str(plot_path))
    print(f"Score distribution plot saved to: {plot_path}")
    
    # 5. New: Analyze score distributions and normalization
    print("\n=== Score Distribution Analysis ===")
    metrics = ['Stand-alone Quality', 'Readiness', 'Relevance', 'Completeness']
    df = analyzer.data
    
    for metric in metrics:
        llm_scores = df[f'LLM {metric}'].values
        human_scores = df[f'Human {metric}'].values
        
        dist_analyzer = ScoreDistributionAnalyzer(llm_scores, human_scores)
        
        # Analyze raw distributions
        dist_analysis = dist_analyzer.analyze_distributions()
        print(f"\n{metric} Distribution Analysis:")
        print(f"LLM Stats: {dist_analysis['llm_stats']}")
        print(f"Human Stats: {dist_analysis['human_stats']}")
        print(f"KS Test: {dist_analysis['ks_test']}")
        
        # Store distribution metrics
        all_metrics.update({
            f"{metric.lower().replace('-', '_')}_distribution": dist_analysis
        })
        
        # Generate normalized distribution plots
        for norm_method in ['zscore', 'minmax', 'robust']:
            # Plot normalized distributions
            norm_plot_path = output_dir / f'{metric.lower().replace(" ", "_")}_{norm_method}_normalized.png'
            dist_analyzer.plot_distributions(
                str(norm_plot_path),
                normalized=True,
                method=norm_method,
                title=f'{metric} - {norm_method.capitalize()} Normalized Distributions'
            )
            
            # Calculate and store normalization differences
            norm_diff = dist_analyzer.get_normalization_differences(method=norm_method)
            all_metrics.update({
                f"{metric.lower().replace('-', '_')}_{norm_method}_differences": norm_diff
            })
            print(f"\n{metric} - {norm_method} Normalization Differences:")
            print(norm_diff)
    
    # 6. Generate comprehensive report
    report_path = output_dir / 'evaluation_report.md'
    analyzer.generate_report(str(report_path))
    print(f"\nComprehensive report generated at: {report_path}")
    
    # 7. Record all metrics
    metrics_recorder.record_metrics(all_metrics)
    print(f"\nMetrics recorded in: {metrics_recorder.output_path}")

if __name__ == "__main__":
    main() 