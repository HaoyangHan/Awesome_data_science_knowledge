# RAG System Evaluation Report (v20250220_171556)

Generated on: 2025-02-20 17:15:56

## Overall Performance Summary

- **precision_at_k**: 0.200 (average)
- **recall_at_k**: 1.000 (average)
- **mean_average_precision**: 1.000 (average)
- **semantic_similarity**: 0.592 (average)
- **keyword_coverage**: 0.917 (average)

## Detailed Results

| query_id   | query                                                         | expected_content                                                                                                                     |   precision_at_k |   recall_at_k |   mean_average_precision |   semantic_similarity |   keyword_coverage |
|:-----------|:--------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------|-----------------:|--------------:|-------------------------:|----------------------:|-------------------:|
| Q1         | What is market capitalization and how is it calculated?       | Market capitalization represents the total value of a company's shares, calculated by multiplying share price by outstanding shares. |              0.2 |             1 |                        1 |              0.620288 |               1    |
| Q2         | How do financial derivatives work and what are their types?   | Financial derivatives are contracts deriving value from underlying assets, including futures, options, swaps, and forwards.          |              0.2 |             1 |                        1 |              0.616457 |               1    |
| Q3         | What is the Efficient Market Hypothesis and its implications? | EMH states that stock prices reflect all available information, making it difficult to consistently outperform the market.           |              0.2 |             1 |                        1 |              0.538385 |               0.75 |

## Query-by-Query Analysis

### Query Q1
- **Query**: What is market capitalization and how is it calculated?
- **Expected Content**: Market capitalization represents the total value of a company's shares, calculated by multiplying share price by outstanding shares.
- **Metrics**:
  - precision_at_k: 0.200
  - recall_at_k: 1.000
  - mean_average_precision: 1.000
  - semantic_similarity: 0.620
  - keyword_coverage: 1.000

### Query Q2
- **Query**: How do financial derivatives work and what are their types?
- **Expected Content**: Financial derivatives are contracts deriving value from underlying assets, including futures, options, swaps, and forwards.
- **Metrics**:
  - precision_at_k: 0.200
  - recall_at_k: 1.000
  - mean_average_precision: 1.000
  - semantic_similarity: 0.616
  - keyword_coverage: 1.000

### Query Q3
- **Query**: What is the Efficient Market Hypothesis and its implications?
- **Expected Content**: EMH states that stock prices reflect all available information, making it difficult to consistently outperform the market.
- **Metrics**:
  - precision_at_k: 0.200
  - recall_at_k: 1.000
  - mean_average_precision: 1.000
  - semantic_similarity: 0.538
  - keyword_coverage: 0.750

## Test Dataset Statistics

- Number of test queries: 3
- Number of documents in corpus: 8

## Recommendations

- Consider improving the retrieval precision by:
  - Refining the document ranking algorithm
  - Adjusting relevance thresholds
  - Implementing better query preprocessing
- Enhance semantic understanding by:
  - Using a more sophisticated embedding model
  - Implementing query expansion
  - Adding domain-specific pre-training
