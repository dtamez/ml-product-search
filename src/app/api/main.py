from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(...), top_k: int = 10):
    return {"query": q, "top_k": top_k, "results": []}
