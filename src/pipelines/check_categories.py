import pandas as pd

df = pd.read_csv("data/processed/products_with_text.csv")

print(df[["title", "category"]].head(100))
