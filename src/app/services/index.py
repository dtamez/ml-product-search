import faiss
import numpy as np


class VectorIndex:
    def __init__(self, dimension: int):
        # inner product index
        self.index = faiss.IndexFlatIP(dimension)

    def add(self, embeddings: np.ndarray):
        embeddings = np.asarray(embeddings, dtype=np.float32)
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int = 10):
        query_embedding = np.asarray(query_embedding, dtype=np.float32)
        scores, indices = self.index.search(query_embedding, top_k)
        return scores, indices

    def save(self, path: str) -> None:
        faiss.write_index(self.index, path)

    @classmethod
    def load(cls, path: str):
        index = faiss.read_index(path)
        obj = cls(index.d)
        obj.index = index
        return obj
