# ML-Powered Product Search (Embeddings + FAISS + FastAPI)

A production-style semantic search system for product discovery, built using dense embeddings and vector similarity search.

This project demonstrates how to take raw product catalog data and turn it into a scalable, ML-driven search service.

---

## Features

* Semantic search using dense embeddings (Sentence Transformers)
* Fast vector retrieval with FAISS
* End-to-end ML pipeline:

  * data ingestion
  * corpus curation
  * text normalization
  * embedding generation
  * indexing
* FastAPI service with `/search` endpoint
* Optional category filtering
* Reproducible pipeline via Makefile
* Sample dataset included for quick demo

---

## Architecture Overview

```
Raw Data (Amazon Metadata)
        ↓
Ingestion & Filtering
        ↓
Curated Retrieval Corpus
        ↓
Text Normalization (searchable_text)
        ↓
Embedding Generation (Sentence Transformers)
        ↓
Vector Index (FAISS)
        ↓
FastAPI Service (/search)
```

---

## Quick Start (30 seconds)

Run the project using the included sample dataset:

```bash
make sample
make prepare
make embeddings
make index
make search
```

Or start the API:

```bash
uvicorn app.api.main:app --reload
```

Then open:

```
http://localhost:8000/docs
```

Example query:

```bash
curl "http://localhost:8000/search?q=wireless+earbuds"
```

---

## Example Queries

* `wireless earbuds`
* `gaming keyboard`
* `bluetooth speaker`
* `laptop charger`
* `usb flash drive`
* `computer monitor`

The system handles semantic matching and even minor typos.

---

## Full Pipeline (Real Data)

To run on full dataset:

1. Download metadata from
   Amazon Product Data (UCSD)

2. Place file at:

```
data/raw/meta_Electronics.json
```

3. Run:

```bash
make pipeline
```

---

## Project Structure

```
src/
  app/
    api/        # FastAPI endpoints
    services/   # embedding, indexing, retrieval
    utils/      # text + JSON helpers
  pipelines/    # data + ML pipeline steps

data/
  raw/          # (ignored) raw dataset
  processed/    # (ignored) cleaned datasets
  sample/       # small demo dataset

artifacts/      # (ignored) embeddings + FAISS index
```

---

## Design Decisions

### Why embeddings?

Traditional keyword search struggles with:

* synonyms
* phrasing variation
* noisy queries

Dense embeddings enable semantic similarity:

> "wireless earbuds" ≈ "bluetooth earphones"

---

### Why FAISS?

* Fast vector similarity search
* Production-proven
* Simple to integrate for MVP

---

### Why normalize embeddings + inner product?

Using normalized vectors with inner product:

* approximates cosine similarity
* efficient and stable
* widely used in vector search systems

---

### Why curate the corpus?

Raw product catalogs contain:

* noisy categories (books, media)
* low-value items (cases, skins)

Filtering improves:

* relevance
* result quality
* system performance

---

## What This Demonstrates

* Building ML systems beyond notebooks
* Handling messy real-world data
* Designing retrieval pipelines
* Separating data, artifacts, and code
* Serving ML models via APIs

---

## Future Improvements

* Hybrid search (keyword + vector)
* Result re-ranking
* Query logging & analytics
* Incremental re-indexing
* Deployment (Docker / cloud)

---

## Discussion

This project focuses on building a production-style ML retrieval system rather than model training. The emphasis is on data pipelines, indexing strategies, and serving ML systems reliably.

Happy to discuss design decisions, tradeoffs, or extensions.
