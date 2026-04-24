import pandas as pd

from app.services.embedder import Embedder
from app.services.index import VectorIndex
from app.utils.json import clean_for_json


class RetrievalService:
    def __init__(self, products_path: str, index_path: str):
        self.products = pd.read_csv(products_path)
        self.index = VectorIndex.load(index_path)
        self.embedder = Embedder()

    def search(self, query: str, top_k: int = 10):
        # embed query
        query_embedding = self.embedder.encode([query])

        # search FAISS
        scores, indices = self.index.search(query_embedding, top_k=top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            row = self.products.iloc[idx].to_dict()
            row["score"] = float(score)
            results.append(clean_for_json(row))

        return results
