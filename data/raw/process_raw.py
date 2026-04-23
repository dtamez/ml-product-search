#!/usr/bin/env python3
import json

import pandas as pd


def process_raw_electronics_data():
    products = []
    processed = 0

    with open("meta_Electronics.json", "r") as fd:
        for line in fd:
            data = json.loads(line)
            products.append(data)
            processed += 1

            if processed > 40_000:
                break

    cleaned = []

    num_cleaned = 0
    # filter out anything without title, rename asin to product_id
    # collapse category and description to single string
    # 20K records is sufficient
    for p in products:
        if "title" not in p:
            continue

        cleaned.append(
            {
                "product_id": p.get("asin"),
                "title": p.get("title", ""),
                "brand": p.get("brand", ""),
                "category": " > ".join(p.get("category", [])),
                "description": " ".join(p.get("description", [])),
            }
        )
        num_cleaned += 1
        if num_cleaned > 20_000:
            break

    df = pd.DataFrame(cleaned)
    df.to_csv("../processed/products.csv", index=False)


if __name__ == "__main__":
    process_raw_electronics_data()
