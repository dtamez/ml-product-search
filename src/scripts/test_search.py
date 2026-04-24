from app.services.retrieval import RetrievalService


def main():
    service = RetrievalService(
        products_path="artifacts/embeddings/products_with_text.csv",
        index_path="artifacts/faiss/products.index",
    )

    queries = [
        "wireless earbuds",
        "gaming keyboard",
        "bluetooth speaker",
        "laptop charger",
        "usb flash drive",
        "computer monitor",
    ]

    for query in queries:
        print(f"\nQUERY: {query}")
        results = service.search(query, top_k=5)

        for i, result in enumerate(results, start=1):
            print(
                f"{i}. score={result['score']:.4f} | "
                f"title={result.get('title', '')} | "
                f"category={result.get('category', '')} | "
                f"brand={result.get('brand', '')}"
            )


if __name__ == "__main__":
    main()
