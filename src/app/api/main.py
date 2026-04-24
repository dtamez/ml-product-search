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
def search(q: str = Query(...), top_k: int = 10, category: str | None = None):
    results = service.search(q, top_k)
    if category:
        results = [
            r for r in results if category.lower() in r.get("category", "").lower()
        ]
    return {"query": q, "top_k": top_k, "results": results}
