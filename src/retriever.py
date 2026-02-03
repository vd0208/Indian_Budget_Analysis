from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, index, chunks, k=5):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)
    return [chunks[i] for i in indices[0]]
