from typing import List, Dict, Optional
from pydantic import BaseModel

class RelevanceCriteria(BaseModel):
    must_contain: List[str]
    should_contain: List[str]
    semantic_aspects: List[str]

class SearchQuery(BaseModel):
    query_id: str
    query: str
    expected_relevant_content: str
    keywords: List[str]
    relevance_criteria: RelevanceCriteria

class RetrievalResult(BaseModel):
    query_id: str
    retrieved_documents: List[Dict[str, str]]  # List of {doc_id: content}
    scores: List[float]

class MetricResult(BaseModel):
    metric_name: str
    score: float
    details: Optional[Dict[str, float]] = None

class EvaluationResult(BaseModel):
    query_id: str
    metrics: List[MetricResult]
    average_score: float

class BatchEvaluationResult(BaseModel):
    results: List[EvaluationResult]
    overall_average: float
    metric_averages: Dict[str, float]
