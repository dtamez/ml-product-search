import os

import pandas as pd

from app.utils.text import build_searchable_text

INPUT_PATH = "data/processed/products.csv"
OUTPUT_PATH = "data/processed/products_with_text.csv"


def main():
    df = pd.read_csv(INPUT_PATH)

    print(f"Loaded {len(df)} products")

    # make sure all columns are there with at least blank data
    for col in ["title", "brand", "category", "description"]:
        if col not in df.columns:
            df[col] = ""

    # populate missing values
    df[["title", "brand", "category", "description"]] = df[
        ["title", "brand", "category", "description"]
    ].fillna("")

    # add searchable text
    df["searchable_text"] = df.apply(build_searchable_text, axis=1)

    # get rid of rows with empty text
    df = df[df["searchable_text"].str.len() > 0]

    print(f"After cleaning, now have : {len(df)} products")

    os.makedirs("artifacts/embeddings", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
