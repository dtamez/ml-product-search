import os

import numpy as np
import pandas as pd

from app.services.index import VectorIndex

EMBEDDINGS_PATH = "artifacts/embeddings/product_embeddings.npy"
PRODUCTS_PATH = "artifacts/embeddings/products_with_text.csv"
INDEX_PATH = "artifacts/faiss/products.index"


def main():
    embeddings = np.load(EMBEDDINGS_PATH)
    df = pd.read_csv(PRODUCTS_PATH)

    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Products shape: {df.shape}")

    dimension = embeddings.shape[1]
    index = VectorIndex(dimension=dimension)
    index.add(embeddings)

    os.makedirs("artifacts/faiss", exist_ok=True)
    index.save(INDEX_PATH)

    print(f"Saved FAISS index to {INDEX_PATH}")
    print(f"Indexed {index.index.ntotal} products")


if __name__ == "__main__":
    main()
