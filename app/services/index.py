import faiss
import numpy as np


class VectorIndex:
    def __init__(self, dimension: int):
        # inner product index
        self.index = faiss.IndexFlatIP(dimension)

    def add(self, embeddings: np.ndarray):
        self.index.add(embeddings.astype("float32"))

    def search(self, query_embedding: np.ndarray, top_k: int = 10):
        # normalized query
        scores, indices = self.index.search(query_embedding.astype("float32"), top_k)
        return scores, indices
