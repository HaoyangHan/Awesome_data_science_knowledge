"""Metrics recorder for LLM-as-Judge evaluation."""

import os
from datetime import datetime
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Literal

class MetricsRecorder:
    """Records evaluation metrics with timestamps."""
    
    def __init__(
        self, 
        evaluation_type: Literal["answer_advanced", "answer_basic", "question_basic"],
        output_path: Optional[str] = None
    ):
        """
        Initialize the metrics recorder.
        
        Args:
            evaluation_type: Type of evaluation being performed
            output_path: Path to save the metrics CSV file. If None, uses default path.
        """
        if output_path is None:
            # Default path in the data directory with evaluation type subfolder
            base_path = Path(__file__).parent.parent.parent.parent / 'data' / 'evaluation_metrics'
            self.output_path = base_path / evaluation_type / 'metrics_history.csv'
        else:
            self.output_path = Path(output_path)
            
        # Create directory if it doesn't exist
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
    def record_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Record metrics with current timestamp.
        
        Args:
            metrics: Dictionary containing metric names and values
        """
        # Add timestamp
        metrics['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert to DataFrame
        df_new = pd.DataFrame([metrics])
        
        # Load existing data if file exists
        if self.output_path.exists():
            df_existing = pd.read_csv(self.output_path)
            df = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df = df_new
            
        # Save to CSV
        df.to_csv(self.output_path, index=False) 