PYTHON := .venv/bin/python

.PHONY: help ingest prepare embeddings index search clean

help:
	@echo "Available targets:"
	@echo "  make ingest      - Load and filter raw Amazon metadata into processed CSV"
	@echo "  make corpus      - Only keep certain categories for a curated retrieval list"
	@echo "  make prepare     - Build searchable_text column"
	@echo "  make embeddings  - Generate embedding vectors"
	@echo "  make index       - Build FAISS index"
	@echo "  make search      - Run local search test queries"
	@echo "  make pipeline    - Run full pipeline"
	@echo "  make clean       - Remove generated artifacts"

ingest:
	$(PYTHON) src/pipelines/ingest_products.py

corpus:
	$(PYTHON) src/pipelines/build_retrieval_corpus.py

prepare:
	$(PYTHON) src/pipelines/prepare_products.py

embeddings:
	$(PYTHON) src/pipelines/build_embeddings.py

index:
	$(PYTHON) src/pipelines/build_index.py

search:
	$(PYTHON) src/scripts/test_search.py

pipeline: ingest corpus prepare embeddings index search

clean:
	rm -f data/processed/products.csv
	rm -f data/processed/retrieval_products.csv
	rm -f artifacts/embeddings/products_with_text.csv
	rm -f artifacts/embeddings/product_embeddings.npy
	rm -f artifacts/faiss/products.index
