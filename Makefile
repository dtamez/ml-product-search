PYTHON := .venv/bin/python

.PHONY: help ingest prepare embeddings index search clean

help:
	@echo "Available targets:"
	@echo "  make ingest      - Load and filter raw Amazon metadata into processed CSV"
	@echo "  make prepare     - Build searchable_text column"
	@echo "  make embeddings  - Generate embedding vectors"
	@echo "  make index       - Build FAISS index"
	@echo "  make search      - Run local search test queries"
	@echo "  make pipeline    - Run full pipeline"
	@echo "  make clean       - Remove generated artifacts"

ingest:
	$(PYTHON) src/pipelines/ingest_products.py

prepare:
	$(PYTHON) src/pipelines/prepare_products.py

embeddings:
	$(PYTHON) src/pipelines/build_embeddings.py

index:
	$(PYTHON) src/pipelines/build_index.py

search:
	$(PYTHON) src/pipelines/test_search.py

pipeline: ingest prepare embeddings index search

clean:
	rm -f data/processed/products.csv
	rm -f artifacts/embeddings/products_with_text.csv
	rm -f artifacts/embeddings/product_embeddings.npy
	rm -f artifacts/faiss/products.index
