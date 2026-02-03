Technical Deep Dive: Indian Budget Analysis AI
This document provides a detailed breakdown of the architectural choices, mathematical models, and data processing pipelines used in this project.

1. Vector Embeddings & Semantic Search
Utilizing a Bi-Encoder architecture to transform unstructured budget text into high-dimensional vectors.

Embedding Model: all-MiniLM-L6-v2
Architecture: A fine-tuned version of MiniLM, optimized for semantic search.

Dimensionality: Each text chunk is mapped to a 384-dimensional vector space.

Why this model? It strikes a perfect balance between speed and performance. It is small enough to run on a CPU (perfect for local analysis) while maintaining a high rank on the MTEB (Massive Text Embedding Benchmark) for clustering and retrieval.

2. Vector Database: FAISS (IndexFlatL2)
For the retrieval layer, I implemented FAISS (Facebook AI Similarity Search).

Index Type: IndexFlatL2.

Logic: It performs an exhaustive "Brute Force" search. In a dataset of this size (3 years of budgets), this ensures 100% recall—meaning the system will never miss the most relevant chunk because it didn't look hard enough.

Scaling: For much larger datasets, pivoting to IndexIVFFlat to partition the search space, but for high-precision financial data, Flat is superior.

3. Data Processing Pipeline
The reliability of a RAG system depends on Chunking Strategy.

Recursive Character Splitting
Chunk Size: 500 characters.

Chunk Overlap: 100 characters.

The "Contextual Bridge": Using a 100-character overlap to ensure that if a vital piece of information (like a budget figure) is split between two chunks, the AI can still reconstruct the full context.

4. Deterministic Keyword Layer (The "Anchor")
To solve the "AI Hallucination" problem common in LLMs, I built a custom keyword frequency engine in analysis.py.

Purpose: While the LLM is probabilistic (it predicts the next word), the keyword engine is deterministic.

Validation: If the AI claims the 2026 budget focuses on "Solar," the user can immediately cross-reference the Industry Growth Chart. If the "Energy" sector bar is high, the AI is validated. If it's low, the user knows to be cautious.

5. Generation: Ollama (Llama 3)
The retrieved context is injected into a system prompt designed to prevent "hallucination":

"You are a professional financial analyst. Use the following context to answer the question. If the answer is not contained in the context, state that the information is unavailable."

By using a local instance of Llama 3 via Ollama, ensuring that the entire pipeline—from PDF reading to answer generation—is 100% private and offline.