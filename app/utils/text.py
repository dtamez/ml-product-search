import pandas as pd


def clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def build_searchable_text(product: dict) -> str:
    title = clean_text(product.get("title", ""))
    brand = clean_text(product.get("brand", ""))
    category = clean_text(product.get("category", ""))
    description = clean_text(product.get("description", ""))

    parts = [
        title,
        f"Brand: {brand}" if brand else "",
        f"Category: {category}" if category else "",
        description,
    ]

    return ". ".join(p for p in parts if p).strip()
