import pandas as pd

INPUT_PATH = "data/processed/products.csv"
OUTPUT_PATH = "data/processed/retrieval_products.csv"

KEEP_PATTERNS = [
    "Headphones",
    "Earbud Headphones",
    "On-Ear Headphones",
    "Over-Ear Headphones",
    "Speakers",
    "Bluetooth Speakers",
    "Webcams",
    "Monitors",
    "Keyboards",
    "Mice",
    "Laptops",
    "Tablets",
    "USB Cables",
    "Chargers",
    "Chargers & Adapters",
    "AC Adapters",
    "Flash Drives",
]

df = pd.read_csv(INPUT_PATH)

pattern = "|".join(KEEP_PATTERNS)
mask = df["category"].fillna("").str.contains(pattern, case=False, na=False)

df_retrieval = df[mask].copy()

# cull a few more that cloudy up the results
EXCLUDE_TERMS = [
    "skins",
    "decals",
    "battery",
    "batteries",
    "camcorder batteries",
]

mask = ~df["category"].fillna("").str.contains(
    "|".join(EXCLUDE_TERMS),
    case=False,
    na=False,
)

df_retrieval = df_retrieval[mask].copy()

print(f"retrieval rows: {len(df_retrieval)}")
print(df_retrieval["category"].value_counts().head(20))

df_retrieval.to_csv(OUTPUT_PATH, index=False)
