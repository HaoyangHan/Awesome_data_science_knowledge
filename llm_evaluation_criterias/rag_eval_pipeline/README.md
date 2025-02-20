# RAG Evaluation Pipeline

A comprehensive evaluation pipeline for Retrieval-Augmented Generation (RAG) systems, focusing on retrieval quality metrics. This package provides tools and APIs to evaluate the performance of document retrieval systems in the context of RAG applications.

## Features

- Multiple evaluation metrics:
  - Precision@k
  - Recall@k
  - Mean Average Precision (MAP)
  - Normalized Discounted Cumulative Gain (NDCG)
  - Semantic Similarity
  - Keyword Coverage
- FastAPI-based REST API
- Batch evaluation support
- Detailed metric reporting
- Support for custom relevance criteria

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag_eval_pipeline
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the API Server

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`. Swagger documentation is available at `http://localhost:8000/docs`.

### API Endpoints

1. **Single Query Evaluation**
   - Endpoint: `POST /evaluate/single`
   - Evaluates a single query-result pair

2. **Batch Evaluation**
   - Endpoint: `POST /evaluate/batch`
   - Evaluates multiple query-result pairs

3. **Available Metrics**
   - Endpoint: `GET /metrics/available`
   - Lists all available evaluation metrics

### Example Request

```python
import requests
import json

# Single query evaluation
query = {
    "query_id": "Q1",
    "query": "What is market capitalization?",
    "expected_relevant_content": "Market capitalization represents the total value...",
    "keywords": ["market capitalization", "market cap", "value"],
    "relevance_criteria": {
        "must_contain": ["market capitalization", "value"],
        "should_contain": ["shares", "price"],
        "semantic_aspects": ["company valuation", "stock market"]
    }
}

result = {
    "query_id": "Q1",
    "retrieved_documents": [
        {"doc1": "Market capitalization is calculated by..."},
        {"doc2": "The total value of shares..."}
    ],
    "scores": [0.95, 0.85]
}

response = requests.post(
    "http://localhost:8000/evaluate/single",
    json={"query": query, "result": result}
)

print(json.dumps(response.json(), indent=2))
```

## Metrics Description

1. **Precision@k**
   - Measures the proportion of relevant documents among the top k retrieved documents
   - Range: 0 to 1 (higher is better)

2. **Recall@k**
   - Measures the proportion of relevant documents retrieved among all relevant documents
   - Range: 0 to 1 (higher is better)

3. **Mean Average Precision (MAP)**
   - Averages the precision values at each relevant document position
   - Range: 0 to 1 (higher is better)

4. **Normalized Discounted Cumulative Gain (NDCG)**
   - Measures ranking quality, taking into account position of relevant documents
   - Range: 0 to 1 (higher is better)

5. **Semantic Similarity**
   - Measures the semantic similarity between query and retrieved documents
   - Range: 0 to 1 (higher is better)

6. **Keyword Coverage**
   - Measures the proportion of query keywords found in retrieved documents
   - Range: 0 to 1 (higher is better)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Citation

If you use this evaluation pipeline in your research, please cite:

```bibtex
@software{rag_eval_pipeline,
  title = {RAG Evaluation Pipeline},
  year = {2024},
  description = {A comprehensive evaluation pipeline for Retrieval-Augmented Generation systems}
}
```
