from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(chunks):
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, embeddings

def save_index(index, path="embeddings/faiss_index"):
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, f"{path}/index.faiss")

def load_index(path="embeddings/faiss_index/index.faiss"):
    return faiss.read_index(path)
