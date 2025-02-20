import numpy as np
from typing import List, Dict, Set
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ..utils.data_types import SearchQuery, RetrievalResult, MetricResult

class RetrievalMetrics:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def precision_at_k(self, retrieved_docs: List[str], relevant_docs: Set[str], k: int) -> float:
        """Calculate Precision@k metric"""
        if k == 0:
            return 0.0
        # Only consider the first k documents
        retrieved_k = retrieved_docs[:k]
        # Count how many of the first k documents are relevant
        relevant_in_k = sum(1 for doc in retrieved_k if doc in relevant_docs)
        return relevant_in_k / k if k > 0 else 0.0

    def recall_at_k(self, retrieved_docs: List[str], relevant_docs: Set[str], k: int) -> float:
        """Calculate Recall@k metric"""
        if not relevant_docs:
            return 0.0
        retrieved_k = set(retrieved_docs[:k])
        relevant_in_k = len(retrieved_k.intersection(relevant_docs))
        return relevant_in_k / len(relevant_docs)

    def mean_average_precision(self, retrieved_docs: List[str], relevant_docs: Set[str]) -> float:
        """Calculate Mean Average Precision (MAP)"""
        if not relevant_docs:
            return 0.0
        
        precisions = []
        relevant_found = 0
        
        for i, doc in enumerate(retrieved_docs, 1):
            if doc in relevant_docs:
                relevant_found += 1
                precisions.append(relevant_found / i)
        
        return np.mean(precisions) if precisions else 0.0

    def ndcg_at_k(self, retrieved_docs: List[str], relevant_docs: Dict[str, float], k: int) -> float:
        """Calculate Normalized Discounted Cumulative Gain (NDCG)"""
        def dcg_at_k(r: List[float], k: int) -> float:
            r = np.array(r[:k])
            if r.size:
                return np.sum(r / np.log2(np.arange(2, r.size + 2)))
            return 0.0

        retrieved_relevance = [relevant_docs.get(doc, 0.0) for doc in retrieved_docs[:k]]
        ideal_relevance = sorted([rel for rel in relevant_docs.values()], reverse=True)[:k]
        
        dcg = dcg_at_k(retrieved_relevance, k)
        idcg = dcg_at_k(ideal_relevance, k)
        
        return dcg / idcg if idcg > 0 else 0.0

    def semantic_similarity(self, query: str, retrieved_docs: List[str]) -> float:
        """Calculate semantic similarity between query and retrieved documents"""
        if not retrieved_docs:
            return 0.0
        
        # Get embeddings for query and documents
        query_embedding = self.model.encode([query])[0]
        doc_embeddings = self.model.encode(retrieved_docs)
        
        # Calculate cosine similarities
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        
        # Weight similarities by position (earlier documents count more)
        weights = np.array([1.0 / (i + 1) for i in range(len(similarities))])
        weighted_similarities = similarities * weights
        
        return float(np.sum(weighted_similarities) / np.sum(weights))

    def keyword_coverage(self, keywords: List[str], retrieved_docs: List[str]) -> float:
        """Calculate keyword coverage in retrieved documents"""
        if not keywords or not retrieved_docs:
            return 0.0
            
        keywords_lower = set(kw.lower() for kw in keywords)
        covered_keywords = set()
        
        # Weight by document position
        for i, doc in enumerate(retrieved_docs):
            doc_lower = doc.lower()
            weight = 1.0 / (i + 1)  # Earlier documents have higher weight
            
            for keyword in keywords_lower:
                if keyword in doc_lower:
                    covered_keywords.add(keyword)
        
        return len(covered_keywords) / len(keywords_lower)

    def evaluate_retrieval(self, query: SearchQuery, result: RetrievalResult, k: int = 5) -> List[MetricResult]:
        """Evaluate retrieval results using multiple metrics"""
        # Extract document IDs and contents
        retrieved_docs = [list(doc.keys())[0] for doc in result.retrieved_documents]
        retrieved_contents = [list(doc.values())[0] for doc in result.retrieved_documents]
        
        # Create relevance dictionary based on must_contain criteria
        relevant_docs = set()
        for doc_id, content in zip(retrieved_docs, retrieved_contents):
            if any(must_term.lower() in content.lower() for must_term in query.relevance_criteria.must_contain):
                relevant_docs.add(doc_id)

        metrics = []
        
        # Precision@k
        precision = self.precision_at_k(retrieved_docs, relevant_docs, k)
        metrics.append(MetricResult(
            metric_name="precision_at_k",
            score=precision,
            details={"k": k}
        ))
        
        # Recall@k
        recall = self.recall_at_k(retrieved_docs, relevant_docs, k)
        metrics.append(MetricResult(
            metric_name="recall_at_k",
            score=recall,
            details={"k": k}
        ))
        
        # MAP
        map_score = self.mean_average_precision(retrieved_docs, relevant_docs)
        metrics.append(MetricResult(
            metric_name="mean_average_precision",
            score=map_score
        ))
        
        # Semantic Similarity
        sem_sim = self.semantic_similarity(query.query, retrieved_contents)
        metrics.append(MetricResult(
            metric_name="semantic_similarity",
            score=sem_sim
        ))
        
        # Keyword Coverage
        kw_coverage = self.keyword_coverage(query.keywords, retrieved_contents)
        metrics.append(MetricResult(
            metric_name="keyword_coverage",
            score=kw_coverage
        ))
        
        return metrics
