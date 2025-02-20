<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# I have a rag system where it contains 7000 documents and websites belongs to a financial wikipedia contains information related to investment banking, you can imagine that this includes documents like Merge Acquisition, pitch deck, etc. Those files contains PPTX, which is worrying for structured data parsing.

Now I need to create a RAG system. The difficulty you can imagine is

1. how to do accurate retrieval. We have some metadata of those documents and website pages, they have inter-connections like belongs to same category, or explaining same topic, those might help. Another thing is the large retrieval chunk number, how to improve the retrieval quality and better evaluate?
2. some chunks contain very limited information, but their full content(in previous and next chunks) might containing enough information, how to deal with this?
3. I want to do search and content generation in this project. How to do Evaluation on both of them?

Now please generate a technical report with accurate, smart analyze on this topic. Give math formula whereever needed, and provide sample data if needed. Also provide sample code for solutions needed.
---

## Technical Report: RAG System for a Financial Investment Banking Knowledge Base

**1. Introduction**

This report outlines the design and implementation considerations for a Retrieval-Augmented Generation (RAG) system built on a knowledge base of approximately 7000 documents and websites related to investment banking. The data includes diverse formats, notably PPTX (PowerPoint presentations), which presents unique challenges for structured data extraction. The system aims to provide both accurate information retrieval and high-quality content generation based on user queries.

**2. Challenges and Analysis**

The core challenges identified are:

* **Accurate Retrieval:**
    * **High Document Volume:** The large number of documents necessitates efficient indexing and retrieval mechanisms.
    * **Inter-Document Relationships:** Leveraging metadata (categories, related topics) is crucial for improving retrieval precision and recall.
    * **PPTX Complexity:** PowerPoint files are inherently less structured than text documents. Extracting text while maintaining context (slide order, relationships between text, charts, and tables) is critical.
    * **Large Retrieval Chunk Quality:** Managing a high number of retrieval chunks requires better evaluation metrics.
* **Contextual Completeness:**
    * **Fragmented Information:** Individual chunks may lack sufficient context. A naive chunking strategy could lead to incomplete or misleading information being retrieved.
* **Evaluation:**
    * **Search Evaluation:** Measuring the relevance and ranking of retrieved documents.
    * **Content Generation Evaluation:** Assessing the fluency, coherence, factual accuracy, and relevance of generated text.

**3. Proposed Solutions and Technical Details**

**3.1 Data Preprocessing and Indexing**

* **PPTX Extraction:**
    * Use libraries like `python-pptx` to parse PPTX files, extracting text while preserving slide order.

```python
from pptx import Presentation

def extract_pptx_content(filepath):
    prs = Presentation(filepath)
    all_text = []
    for slide_num, slide in enumerate(prs.slides):
        slide_text = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    slide_text.append(paragraph.text)
        all_text.append({"slide": slide_num + 1, "text": "\n".join(slide_text)})
    return all_text

# Example usage:
extracted_data = extract_pptx_content("example.pptx")
```

* **Chunking Strategies:**
    * Implement various chunking methods including sentence-based chunking, fixed-size chunking, semantic chunking using embeddings, and context window expansion to improve contextual completeness.

```python
def get_context_window(chunks, current_chunk_index, n=2):
    start = max(0, current_chunk_index - n)
    end = min(len(chunks), current_chunk_index + n + 1)
    return chunks[start:end]
```

* **Indexing:**
    * Utilize vector databases like FAISS or Annoy for efficient similarity search. Fine-tune embedding models like Sentence-BERT on your specific corpus.

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2') 
chunks = ["Mergers and acquisitions are complex.", "Investment banks advise on M&A deals."]
embeddings = model.encode(chunks)

dimension = embeddings.shape[^1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

query = "What is M&A?"
query_embedding = model.encode([query]).astype('float32')
distances, indices = index.search(query_embedding, k=3)
```

**3.2 Retrieval**

* **Query Embedding:** Embed user queries using the same embedding model used for indexing.
* **Similarity Search:** Use the vector database to find the nearest neighbor chunks to the query embedding.
* **Re-ranking Options:** Consider cross-encoder re-ranking or Maximum Marginal Relevance (MMR) to improve retrieval quality.

```python
def mmr(query, documents, relevance_scores, similarity_matrix, lambda_param=0.5, k=5):
    selected_docs = []
    unselected_docs = list(range(len(documents)))
    
    while len(selected_docs) < k and unselected_docs:
        best_doc = None
        best_score = -float('inf')
        for i in unselected_docs:
            relevance = relevance_scores[i]
            similarity = max(similarity_matrix[i][j] for j in selected_docs) if selected_docs else 0
            mmr_score = lambda_param * relevance - (1 - lambda_param) * similarity
            
            if mmr_score > best_score:
                best_score = mmr_score
                best_doc = i
                
        selected_docs.append(best_doc)
        unselected_docs.remove(best_doc)
    
    return [documents[i] for i in selected_docs]
```

**3.3 Content Generation**

* **Prompt Engineering:** Design prompts that guide the language model effectively.
* **Model Selection:** Experiment with powerful models like GPT-4 or LLaMA.
* **Fact Verification:** Implement post-processing steps to verify factual accuracy using entailment checking or external knowledge base lookups.

**4. Evaluation**

**4.1 Search Evaluation Metrics:**

* Precision@k: Proportion of relevant documents among the top k retrieved documents.
* Recall@k: Proportion of relevant documents retrieved among the top k out of all relevant documents.
* Mean Average Precision (MAP): Averages precision over all recall levels.
* Normalized Discounted Cumulative Gain (NDCG): Measures ranking quality considering position of relevant documents.

```python
def precision_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    relevant_in_k = len(set(retrieved_k).intersection(relevant))
    return relevant_in_k / k

def recall_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    relevant_in_k = len(set(retrieved_k).intersection(relevant))
    return relevant_in_k / len(relevant)
```

**4.2 Content Generation Evaluation Metrics:**

* BLEU: Measures n-gram overlap between generated and reference text.
* ROUGE: Focuses on recall of reference text captured in generated output.
* BERTScore: Measures semantic similarity using BERT embeddings.
* Human evaluation remains crucial for assessing fluency and factual accuracy.

**5. Iteration and Improvement**

Continuous evaluation and improvement strategies include:

* Fine-tuning models on specific corpora.
* Experimenting with prompt engineering techniques.
* Collecting user feedback to identify areas for enhancement.

**6. Conclusion**

Building a robust RAG system for a financial investment banking knowledge base necessitates careful consideration of data preprocessing, indexing, retrieval strategies, and content generation techniques. By addressing the complexities of PPTX files and ensuring contextual completeness while rigorously evaluating both search performance and content generation quality, a high-quality RAG system can be developed to deliver accurate insights to users. Continuous iteration is essential for ongoing improvement in system performance.

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/53758792/2d5e97d7-347b-44ae-a5f9-7c187f643b26/paste.txt

[^2]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/53758792/6d8c2901-65b7-4fc1-a557-2da14f5914b0/paste.txt

[^3]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/53758792/673fc822-6028-4f4a-8082-7f16381e5cf8/paste-3.txt

[^4]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/53758792/fab5a52f-6f3a-4eda-8088-7d240be40c8d/paste-4.txt

[^5]: https://redis.io/glossary/retrieval-augmented-generation/

[^6]: https://www.deasie.com/post/improving-rag-models-with-metadata

[^7]: https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5

[^8]: https://unstructured.io/blog/chunking-for-rag-best-practices

[^9]: https://gradientflow.substack.com/p/best-practices-in-retrieval-augmented

[^10]: https://www.helicone.ai/blog/rag-chunking-strategies

[^11]: https://www.vellum.ai/blog/how-to-evaluate-your-rag-system

[^12]: https://www.tredence.com/blog/understanding-rag-systems-the-future-of-ai-interactions

[^13]: https://docs.databricks.com/en/generative-ai/tutorials/ai-cookbook/evaluate-assess-performance.html

[^14]: https://www.falkordb.com/blog/advanced-rag/

[^15]: https://haystack.deepset.ai/blog/extracting-metadata-filter

[^16]: https://antematter.io/blogs/optimizing-rag-advanced-chunking-techniques-study

[^17]: https://blog.premai.io/chunking-strategies-in-retrieval-augmented-generation-rag-systems/

[^18]: https://www.aporia.com/learn/rag-in-production/

[^19]: https://qdrant.tech/blog/rag-evaluation-guide/

[^20]: https://www.edenai.co/post/the-2025-guide-to-retrieval-augmented-generation-rag

[^21]: https://www.deepset.ai/blog/leveraging-metadata-in-rag-customization

[^22]: https://www.scoutos.com/blog/understanding-text-chunking-in-retrieval-augmented-generation-rag-systems

[^23]: https://squirro.com/squirro-blog/10-essential-considerations-for-constructing-a-retrieval-augmented-generation-rag-system

[^24]: https://www.f22labs.com/blogs/7-chunking-strategies-in-rag-you-need-to-know/

[^25]: https://cloud.google.com/use-cases/retrieval-augmented-generation

[^26]: https://community.aws/content/2gp2m3BJcl9mSMWT6njCIQNiz0e/techniques-to-enhance-retrieval-augmented-generation-rag?lang=en

[^27]: https://www.mattambrogi.com/posts/chunk-size-matters/

[^28]: https://www.intersystems.com/resources/retrieval-augmented-generation/

[^29]: https://arxiv.org/html/2410.04231v1

[^30]: https://cohere.com/blog/chunking-for-rag-maximize-enterprise-knowledge-retrieval

[^31]: https://www.reddit.com/r/LocalLLaMA/comments/1gd9o1w/whats_the_best_rag_retrievalaugmented_generation/

[^32]: https://www.reddit.com/r/Rag/comments/1i6e5u7/metadata_and_retriever/

[^33]: https://www.reddit.com/r/LangChain/comments/174dm18/effects_of_chunk_sizes_on_retrieval_augmented/

[^34]: https://www.valprovia.com/en/blog/mastering-rag-a-deep-dive-into-retrieval-augmented-generation

[^35]: https://community.databricks.com/t5/technical-blog/six-steps-to-improve-your-rag-application-s-data-foundation/ba-p/97700

[^36]: https://arxiv.org/abs/2501.02702

[^37]: https://arxiv.org/abs/2410.12248

[^38]: https://arxiv.org/abs/2406.11357

[^39]: https://www.semanticscholar.org/paper/667f2381f025a61c8beb6f7fa5ce68c24e84fdd5

[^40]: https://www.semanticscholar.org/paper/8d08391afa2dc3d1d47707cbd2594a4d98d46355

[^41]: https://www.ibm.com/think/tutorials/chunking-strategies-for-rag-with-langchain-watsonx-ai

[^42]: https://implementconsultinggroup.com/article/building-high-quality-rag-systems

[^43]: https://www.sagacify.com/news/a-guide-to-chunking-strategies-for-retrieval-augmented-generation-rag

[^44]: https://stackoverflow.blog/2024/12/27/breaking-up-is-hard-to-do-chunking-in-rag-applications/

[^45]: https://labelstud.io/blog/key-considerations-for-evaluating-rag-based-systems/

[^46]: https://www.reddit.com/r/LangChain/comments/1bgqc2o/optimal_way_to_chunk_word_document_for/

[^47]: https://www.eficode.com/blog/considerations-for-rag-systems-in-product-and-service-development

[^48]: https://community.openai.com/t/scaling-rag-chatbot-system-to-millions-of-documents/615386

[^49]: https://www.reddit.com/r/LLMDevs/comments/1h07sox/rag_is_easy_getting_usable_content_is_the_real/

[^50]: https://gradientflow.com/contextual-retrieval-rag/

[^51]: https://www.datacamp.com/blog/what-is-retrieval-augmented-generation-rag

[^52]: https://myscale.com/blog/ultimate-guide-to-evaluate-rag-system/

[^53]: https://www.pinecone.io/learn/series/vector-databases-in-production-for-busy-engineers/rag-evaluation/

[^54]: https://www.ridgerun.ai/post/how-to-evaluate-retrieval-augmented-generation-rag-systems

[^55]: https://weaviate.io/blog/rag-evaluation

[^56]: https://www.louisbouchard.ai/rag-evals/

[^57]: https://www.reddit.com/r/Rag/comments/1hjujfh/what_are_you_looking_for_in_a_tool_to_evaluate/

[^58]: https://arxiv.org/html/2405.07437v2

[^59]: https://huggingface.co/learn/cookbook/en/rag_evaluation

[^60]: https://orq.ai/blog/rag-evaluation

[^61]: https://cloud.google.com/blog/products/ai-machine-learning/optimizing-rag-retrieval

[^62]: https://blog.futuresmart.ai/a-beginners-guide-to-evaluating-rag-systems-with-langsmith

[^63]: https://www.protecto.ai/blog/understanding-llm-evaluation-metrics-for-better-rag-performance

