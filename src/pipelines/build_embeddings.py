import os

import numpy as np
import pandas as pd

from app.services.embedder import Embedder

INPUT_PATH = "data/processed/products_with_text.csv"
OUTPUT_EMBEDDINGS = "artifacts/embeddings/product_embeddings.npy"
OUTPUT_PRODUCTS = "artifacts/embeddings/products_with_text.csv"


def main():
    df = pd.read_csv(INPUT_PATH)

    if "searchable_text" not in df.columns:
        raise ValueError(
            "searchable_text column missing. Run preprocessing step first."
        )

    texts = df["searchable_text"].tolist()

    print(f"Generating embeddings for {len(texts)} products")

    embedder = Embedder()
    embeddings = embedder.encode(texts)

    print(f"Embeddings shape: {embeddings.shape}")

    os.makedirs("artifacts/embeddings", exist_ok=True)

    np.save(OUTPUT_EMBEDDINGS, embeddings)
    df.to_csv(OUTPUT_PRODUCTS, index=False)

    print(f"Saved embeddings to {OUTPUT_EMBEDDINGS}")
    print(f"Saved products to {OUTPUT_PRODUCTS}")


if __name__ == "__main__":
    main()
