from fastapi import FastAPI, HTTPException
from typing import List
from ..utils.data_types import (
    SearchQuery,
    RetrievalResult,
    EvaluationResult,
    BatchEvaluationResult,
    MetricResult
)
from ..metrics.retrieval_metrics import RetrievalMetrics

app = FastAPI(
    title="RAG Evaluation Pipeline",
    description="API for evaluating Retrieval-Augmented Generation systems",
    version="1.0.0"
)

# Initialize metrics
metrics = RetrievalMetrics()

@app.get("/")
async def root():
    return {"message": "RAG Evaluation Pipeline API"}

@app.post("/evaluate/single", response_model=EvaluationResult)
async def evaluate_single_query(query: SearchQuery, result: RetrievalResult):
    """
    Evaluate a single query-result pair using multiple retrieval metrics
    """
    try:
        evaluation_metrics = metrics.evaluate_retrieval(query, result)
        average_score = sum(m.score for m in evaluation_metrics) / len(evaluation_metrics)
        
        return EvaluationResult(
            query_id=query.query_id,
            metrics=evaluation_metrics,
            average_score=average_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate/batch", response_model=BatchEvaluationResult)
async def evaluate_batch(queries: List[SearchQuery], results: List[RetrievalResult]):
    """
    Evaluate multiple query-result pairs and provide aggregated metrics
    """
    if len(queries) != len(results):
        raise HTTPException(
            status_code=400,
            detail="Number of queries must match number of results"
        )
    
    try:
        evaluation_results = []
        metric_sums = {}
        metric_counts = {}
        
        for query, result in zip(queries, results):
            metrics_list = metrics.evaluate_retrieval(query, result)
            average_score = sum(m.score for m in metrics_list) / len(metrics_list)
            
            # Aggregate metrics
            for metric in metrics_list:
                if metric.metric_name not in metric_sums:
                    metric_sums[metric.metric_name] = 0.0
                    metric_counts[metric.metric_name] = 0
                metric_sums[metric.metric_name] += metric.score
                metric_counts[metric.metric_name] += 1
            
            evaluation_results.append(
                EvaluationResult(
                    query_id=query.query_id,
                    metrics=metrics_list,
                    average_score=average_score
                )
            )
        
        # Calculate metric averages
        metric_averages = {
            metric_name: metric_sums[metric_name] / metric_counts[metric_name]
            for metric_name in metric_sums
        }
        
        # Calculate overall average
        overall_average = sum(result.average_score for result in evaluation_results) / len(evaluation_results)
        
        return BatchEvaluationResult(
            results=evaluation_results,
            overall_average=overall_average,
            metric_averages=metric_averages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/available")
async def get_available_metrics():
    """
    Get list of available evaluation metrics
    """
    return {
        "metrics": [
            {
                "name": "precision_at_k",
                "description": "Proportion of relevant documents among top k retrieved"
            },
            {
                "name": "recall_at_k",
                "description": "Proportion of relevant documents retrieved among all relevant"
            },
            {
                "name": "mean_average_precision",
                "description": "Average precision at each relevant document position"
            },
            {
                "name": "ndcg_at_k",
                "description": "Normalized Discounted Cumulative Gain at k"
            },
            {
                "name": "semantic_similarity",
                "description": "Average semantic similarity between query and retrieved documents"
            },
            {
                "name": "keyword_coverage",
                "description": "Proportion of query keywords found in retrieved documents"
            }
        ]
    }
