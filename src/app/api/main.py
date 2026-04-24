from fastapi import FastAPI, Query

from app.services.retrieval import RetrievalService

app = FastAPI()
service = RetrievalService(
    products_path="artifacts/embeddings/products_with_text.csv",
    index_path="artifacts/faiss/products.index",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(...), top_k: int = 10):
    results = service.search(q, top_k)
    return {"query": q, "top_k": top_k, "results": results}
