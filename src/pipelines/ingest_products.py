import json
import os
from typing import Any

import pandas as pd

INPUT_PATH = "data/raw/meta_Electronics.json"
OUTPUT_PATH = "data/processed/products.csv"

# Filter out tons of ebooks, audiobooks, movies etc.
EXCLUDE_CATEGORY_TERMS = {
    "eBook Readers",
    "eBook Readers &amp; Accessories",
    "MP3 &amp; MP4 Player AccessoriesAudio & Video Accessories",
    "CD-R Discs",
    "Headphones",
    "DVDs",
    "ebook",
    "ebooks",
    "kindle",
    "book",
    "books",
    "textbook",
    "textbooks",
    "novel",
    "novels",
    "dvd",
    "dvds",
    "movie",
    "movies",
    "music",
    "cd",
    "cds",
    "mp3 downloads",
    "digital music",
}

EXCLUDE_DESCRIPTION_TERMS = {"This book"}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(v).strip() for v in value if v is not None).strip()
    return str(value).strip()


def normalize_category(category: Any) -> list[str]:
    if category is None:
        return []
    if isinstance(category, list):
        return [str(c).strip() for c in category if c is not None and str(c).strip()]
    text = str(category).strip()
    if not text:
        return []
    return [text]


def should_exclude_category(category_parts: list[str]) -> bool:
    joined = " > ".join(category_parts).lower()
    return any(term in joined for term in EXCLUDE_CATEGORY_TERMS)


def should_exclude_description(description: str):
    return any(term in description for term in EXCLUDE_DESCRIPTION_TERMS)


def is_valid_product(record: dict[str, Any]) -> bool:
    title = normalize_text(record.get("title"))
    description = normalize_text(record.get("description"))
    category_parts = normalize_category(record.get("category"))

    if not title:
        return False

    if not category_parts:
        return False

    if not category_parts[0].lower().startswith("electronics"):
        return False

    if should_exclude_category(category_parts):
        return False

    if not description and len(title) < 8:
        return False

    if should_exclude_description(description):
        return False

    return True


def transform_record(record: dict[str, Any]) -> dict[str, Any]:
    category_parts = normalize_category(record.get("category"))

    return {
        "product_id": normalize_text(record.get("asin")),
        "title": normalize_text(record.get("title")),
        "brand": normalize_text(record.get("brand")),
        "category": " > ".join(category_parts),
        "description": normalize_text(record.get("description")),
        "price": normalize_text(record.get("price")),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    total = 0
    kept = 0

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            total += 1
            record = json.loads(line)

            if not is_valid_product(record):
                continue

            rows.append(transform_record(record))
            kept += 1

    df = pd.DataFrame(rows).drop_duplicates(subset=["product_id"])

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Total records read: {total}")
    print(f"Records kept: {kept}")
    print(f"Rows after dedupe: {len(df)}")
    print(f"Saved to: {OUTPUT_PATH}")

    print("\nTop categories:")
    print(df["category"].value_counts().head(15))


if __name__ == "__main__":
    main()
