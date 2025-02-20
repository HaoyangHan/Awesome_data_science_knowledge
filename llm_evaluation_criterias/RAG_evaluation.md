# Technical Report: RAG System for a Financial Investment Banking Knowledge Base

**1. Introduction**

This report outlines the design and implementation considerations for a Retrieval-Augmented Generation (RAG) system built on a knowledge base of approximately 7000 documents and websites related to investment banking. The data includes diverse formats, notably PPTX (PowerPoint presentations), which presents unique challenges for structured data extraction. The system aims to provide both accurate information retrieval and high-quality content generation based on user queries.

**2. Challenges and Analysis**

The core challenges identified are:

*   **2.1 Accurate Retrieval:**
    *   **High Document Volume:** 7000 documents create a large search space, requiring efficient indexing and retrieval mechanisms.
    *   **Inter-Document Relationships:** Leveraging metadata (categories, related topics) is crucial for improving retrieval precision and recall.
    *   **PPTX Complexity:** PowerPoint files are inherently less structured than text documents. Extracting text and maintaining context (slide order, relationships between text, charts, and tables) is critical.
    *   **Large Retrieval Chunk Quality:** Dealing with large chunk number, need better evaluation metrics.
*   **2.2 Contextual Completeness:**
    *   **Fragmented Information:** Individual chunks may lack sufficient context. A naive chunking strategy could lead to incomplete or misleading information being retrieved.
*   **2.3 Evaluation:**
    *   **Search Evaluation:** Measuring the relevance and ranking of retrieved documents.
    *   **Content Generation Evaluation:** Assessing the fluency, coherence, factual accuracy, and relevance of generated text.

**3. Proposed Solutions and Technical Details**

**3.1 Data Preprocessing and Indexing**

*   **3.1.1 PPTX Extraction:**

    *   **Library:** Use a library like `python-pptx` to parse PPTX files.
    *   **Strategy:**
        *   Extract text from each slide, preserving slide order.
        *   Consider extracting text from speaker notes, if present and relevant.
        *   Attempt to identify and extract data from tables and charts (this can be very challenging and might require specialized OCR or table recognition techniques). If direct extraction is difficult, consider including placeholders or descriptions of charts/tables in the extracted text (e.g., "[Chart: Revenue Growth over 5 Years]").
        *   Example Code (Conceptual):

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
                        # Add handling for tables and charts (complex!)
                    all_text.append({"slide": slide_num + 1, "text": "\n".join(slide_text)})
                return all_text

            # Example usage:
            extracted_data = extract_pptx_content("example.pptx")
            # print(extracted_data) #Output will show list of dictionaries contains slide info.
            ```

*   **3.1.2 Chunking:**

    *   **Sentence-Based Chunking (Baseline):** Split text into sentences using a sentence tokenizer (e.g., from NLTK or spaCy). This is a simple starting point.
    *   **Fixed-Size Chunking:** Divide the text into chunks of a fixed number of tokens (e.g., 256, 512). This can help control the input size to the language model.
    *   **Semantic Chunking (Advanced):** Use a semantic similarity measure to group sentences that are topically related. This is more computationally expensive but can lead to more coherent chunks. Example: use sentence embeddings and cluster them.
    *   **Recursive Chunking:** Combine small chunks, and build hierarchical index.
    *   **Metadata-Aware Chunking:** Incorporate metadata into the chunking process. For example, ensure that chunks do not cross document boundaries or category boundaries.
    *   **Context Window Expansion (Addressing 2.2):**
        *   For a given retrieved chunk, also retrieve the *n* preceding and *n* succeeding chunks. This provides the language model with additional context.
        *   Experiment with different values of *n* to find the optimal balance between context and computational cost.

            ```python
            def get_context_window(chunks, current_chunk_index, n=2):
                start = max(0, current_chunk_index - n)
                end = min(len(chunks), current_chunk_index + n + 1)
                return chunks[start:end]
            ```

*   **3.1.3 Indexing:**

    *   **Vector Database (FAISS, Annoy, ScaNN):** Store chunk embeddings in a vector database for efficient similarity search. FAISS (Facebook AI Similarity Search) is a popular choice.
    *   **Embedding Model:** Use a pre-trained sentence embedding model like Sentence-BERT (SBERT) or a specialized financial embedding model (if available). Fine-tuning the embedding model on your specific corpus can further improve performance.

        ```python
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np

        # Load a pre-trained model
        model = SentenceTransformer('all-MiniLM-L6-v2')  # Or a financial-specific model

        # Example chunks (replace with your actual chunks)
        chunks = ["Mergers and acquisitions are complex.", "Investment banks advise on M&A deals.", "Pitch decks are used to present investment opportunities."]

        # Generate embeddings
        embeddings = model.encode(chunks)

        # Create a FAISS index (L2 distance)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))

        # Search for similar chunks
        query = "What is M&A?"
        query_embedding = model.encode([query]).astype('float32')
        k = 3  # Number of nearest neighbors
        distances, indices = index.search(query_embedding, k)

        print(f"Query: {query}")
        for i, (distance, index) in enumerate(zip(distances[0], indices[0])):
            print(f"  Result {i+1}: {chunks[index]} (Distance: {distance:.4f})")
        ```

    *   **Hybrid Indexing:** Combine vector search with keyword-based search (e.g., using BM25) to leverage both semantic and lexical matching. This can often improve recall.
    *   **Metadata Filtering:** Allow users to filter search results based on metadata (e.g., document type, category). Implement this using filtering capabilities within your vector database or a separate metadata index.

**3.2 Retrieval**

*   **3.2.1 Query Embedding:** Embed the user's query using the same embedding model used for indexing.
*   **3.2.2 Similarity Search:** Use the vector database to find the *k* nearest neighbor chunks to the query embedding.
*  **3.2.3 Re-ranking (Optional):** Improve retrieval quality, consider below options:
    *   **Cross-Encoder Re-ranking:** Use a more powerful model (e.g., a cross-encoder based on BERT) to re-rank the top *k* results from the initial retrieval. This is computationally more expensive but can significantly improve precision.
    *   **Metadata-Based Re-ranking:** Prioritize results that match the user's metadata filters or have higher metadata relevance scores.
    *   **Maximum Marginal Relevance (MMR):** Promote diversity in the retrieved results. MMR balances relevance with novelty to avoid retrieving multiple chunks that convey very similar information.

        ```python
        #Simplified MMR, assuming we have relevance scores and similarity scores
        def mmr(query, documents, relevance_scores, similarity_matrix, lambda_param=0.5, k=5):
            selected_docs = []
            unselected_docs = list(range(len(documents)))

            while len(selected_docs) < k and unselected_docs:
                best_doc = None
                best_score = -float('inf')

                for i in unselected_docs:
                    relevance = relevance_scores[i]
                    similarity = 0
                    if selected_docs:
                         similarity = max(similarity_matrix[i][j] for j in selected_docs) #Max similarity to selected

                    mmr_score = lambda_param * relevance - (1 - lambda_param) * similarity

                    if mmr_score > best_score:
                        best_score = mmr_score
                        best_doc = i

                selected_docs.append(best_doc)
                unselected_docs.remove(best_doc)

            return [documents[i] for i in selected_docs]

        # Example usage (you'd need to calculate relevance and similarity)
        # ... (code to get initial retrieval results and calculate scores) ...
        # reranked_results = mmr(query, retrieved_documents, relevance_scores, similarity_matrix)
        ```
**3.3 Content Generation**

*   **3.3.1 Prompt Engineering:** Carefully craft prompts that guide the language model to generate the desired output. Include the retrieved context and clearly specify the task (e.g., "Answer the following question based on the provided context: ...").
*   **3.3.2 Language Model Selection:** Use a powerful language model like GPT-3.5, GPT-4, or a fine-tuned open-source model (e.g., LLaMA 2, Mistral). Experiment with different models to find the best balance between quality and cost.
*   **3.3.3 Temperature and Top-p Sampling:** Control the randomness and creativity of the generated text using temperature and top-p parameters. Lower temperatures produce more deterministic output, while higher temperatures lead to more diverse and potentially creative (but also potentially less accurate) output.
*   **3.3.4 Fact Verification (Crucial):** Implement a post-processing step to verify the factual accuracy of the generated text. This is *essential* for a financial domain. Options include:
    *   **Entailment Checking:** Use an entailment model to check if the generated statements are logically supported by the retrieved context.
    *   **External Knowledge Base Lookup:** Query external knowledge bases (e.g., Wikidata, SEC EDGAR) to validate facts.
    *   **Numerical Reasoning:** If the generated text involves numbers or calculations, implement checks to ensure numerical consistency and accuracy.

**4. Evaluation**

**4.1 Search Evaluation**

*   **4.1.1 Metrics:**
    *   **Precision@k:** The proportion of relevant documents among the top *k* retrieved documents.
    *   **Recall@k:** The proportion of relevant documents retrieved among the top *k*, out of all relevant documents in the corpus.
    *   **Mean Average Precision (MAP):** Averages the precision over all recall levels.
    *   **Normalized Discounted Cumulative Gain (NDCG):** Measures the ranking quality, taking into account the position of relevant documents.
    *   **R-precision:** Precision at the R-th position in the ranking, where R is the total number of relevant documents for the query.
        ```python
        # Example calculation of Precision@k and Recall@k
        def precision_at_k(retrieved, relevant, k):
            retrieved_k = retrieved[:k]
            relevant_in_k = len(set(retrieved_k).intersection(relevant))
            return relevant_in_k / k

        def recall_at_k(retrieved, relevant, k):
            retrieved_k = retrieved[:k]
            relevant_in_k = len(set(retrieved_k).intersection(relevant))
            return relevant_in_k / len(relevant)

        # Example usage
        retrieved_docs = [1, 3, 5, 2, 4]  # Document IDs
        relevant_docs = [1, 2, 6]
        k = 3
        precision = precision_at_k(retrieved_docs, relevant_docs, k)
        recall = recall_at_k(retrieved_docs, relevant_docs, k)
        print(f"Precision@{k}: {precision:.4f}")
        print(f"Recall@{k}: {recall:.4f}")
        ```
*   **4.1.2 Test Set Creation:** Create a test set of queries and corresponding relevant documents. This should be done manually by domain experts to ensure high quality.

**4.2 Content Generation Evaluation**

*   **4.2.1 Metrics:**
    *   **BLEU (Bilingual Evaluation Understudy):** Measures the overlap of n-grams between the generated text and reference text. Useful as a basic measure of fluency but doesn't capture semantic meaning well.
    *   **ROUGE (Recall-Oriented Understudy for Gisting Evaluation):** Similar to BLEU but focuses on recall (how much of the reference text is captured in the generated text).
    *   **METEOR (Metric for Evaluation of Translation with Explicit ORdering):** Considers word order and uses stemming and synonym matching. Often better than BLEU.
    *   **BERTScore:** Uses BERT embeddings to measure the semantic similarity between the generated text and reference text.
    *   **Factuality Metrics:** Custom metrics designed to assess the factual accuracy of the generated text, based on the fact verification techniques described above. This is critical.
    *   **Human Evaluation:** The gold standard. Have domain experts rate the generated text on various dimensions (fluency, coherence, factual accuracy, relevance, helpfulness).
    *   **Perplexity:** Intrinsic evaluation metrics that are widely used.

*   **4.2.2 Test Set Creation:** Create a test set of queries and corresponding "gold standard" answers.

**5. Iteration and Improvement**

The RAG system should be continuously evaluated and improved. Key strategies include:

*   **Fine-tuning:** Fine-tune the embedding model and/or the language model on your specific corpus.
*   **Prompt Engineering:** Experiment with different prompts to optimize the performance of the language model.
*   **User Feedback:** Collect feedback from users to identify areas for improvement.
*   **A/B Testing:** Test different configurations of the system (e.g., different chunking strategies, embedding models, language models) to determine which performs best.

**6. Conclusion**

Building a robust RAG system for a financial investment banking knowledge base requires careful consideration of data preprocessing, indexing, retrieval, and generation techniques. The key challenges are handling the complexity of PPTX files, ensuring contextual completeness, and rigorously evaluating both search and generation performance. By combining vector search, semantic chunking, metadata utilization, and robust fact verification, a high-quality RAG system can be built to provide accurate and insightful information to users. Continuous evaluation and iteration are crucial for ongoing improvement.