import pandas as pd

from app.utils.text import build_searchable_text

df = pd.read_csv("data/processed/products.csv")

for col in ["title", "brand", "category", "description"]:
    if col in df.columns:
        df[col] = df[col].fillna("")

df["searchable_text"] = df.apply(lambda row: build_searchable_text(row), axis=1)
print(df[["title", "searchable_text"]].head())
