import os
from pathlib import Path
from llm_as_judge.answer_evaluation import AnswerEvaluationAnalyzer
from llm_as_judge.metrics.metrics_recorder import MetricsRecorder

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
    
    # 5. Generate comprehensive report
    report_path = output_dir / 'evaluation_report.md'
    analyzer.generate_report(str(report_path))
    print(f"\nComprehensive report generated at: {report_path}")
    
    # 6. Record all metrics
    metrics_recorder.record_metrics(all_metrics)
    print(f"\nMetrics recorded in: {metrics_recorder.output_path}")

if __name__ == "__main__":
    main() 