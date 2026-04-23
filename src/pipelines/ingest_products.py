import json

import pandas as pd

INPUT_FILE = "data/raw/meta_Electronics.json"
OUTPUT_FILE = "data/processed/products.csv"


def process_raw_electronics_data():
    products = []
    processed = 0

    with open(INPUT_FILE, "r") as fd:
        for line in fd:
            data = json.loads(line)
            products.append(data)
            processed += 1

            if processed % 5_000 == 0:
                print(f"{processed} processed")

            if processed == 200_000:
                break

    cleaned = []

    # Filter out tons of ebooks, audiobooks, movies etc.
    EXCLUDE_CATEGORY_TERMS = {
        "eBook Readers",
        "eBook Readers &amp; Accessories",
        "MP3 &amp; MP4 Player AccessoriesAudio & Video Accessories",
        "CD-R Discs",
        "Headphones",
        "DVDs",
    }

    EXCLUDE_DESCRIPTION_TERMS = {
        "DVD",
        "Book",
        "book",
        "Handbook",
        "handbook",
        "Film",
        "film",
        "Movie",
        "movie",
    }

    num_cleaned = 0
    # filter out anything without title, rename asin to product_id
    # collapse category and description to single string
    # 20K records is sufficient
    for p in products:
        if "title" not in p:
            continue

        categories = set(p.get("category", []))

        if EXCLUDE_CATEGORY_TERMS.intersection(categories):
            print(f"skipping category: {categories}")
            continue

        description = p.get("description", [])
        if EXCLUDE_DESCRIPTION_TERMS.intersection(description):
            print(f"skipping description: {description}")
            continue

        title = p.get("title", "")
        if "book" in title or "Book" in title:
            print(f"Skipping title: {title}")
            continue

        cleaned.append(
            {
                "product_id": p.get("asin"),
                "title": title,
                "brand": p.get("brand", ""),
                "category": " > ".join(categories),
                "description": " ".join(description),
            }
        )
        num_cleaned += 1
        if num_cleaned == 20_000:
            break

    df = pd.DataFrame(cleaned)
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    process_raw_electronics_data()
