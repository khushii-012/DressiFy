import pandas as pd
import random

# Read original dataset
df = pd.read_csv("datasets/fashion_items.csv")
print(df.columns.tolist())
print(df.head())
exit()

BRANDS = [
    "Zara",
    "H&M",
    "Uniqlo",
    "Nike",
    "Adidas",
    "Levis",
    "Forever21",
    "Roadster",
    "Puma",
    "ONLY",
    "Allen Solly",
    "Rare Rabbit",
    "Snitch",
    "Mango"
]

MATERIALS = [
    "Cotton",
    "Denim",
    "Linen",
    "Silk",
    "Polyester",
    "Rayon",
    "Leather",
    "Wool",
    "Knitted",
    "Satin"
]

PRICE_RANGE = [
    "Budget",
    "Affordable",
    "Premium",
    "Luxury"
]

SEASONS = [
    "Summer",
    "Winter",
    "Monsoon",
    "All Season"
]

records = []

product_id = 1000

for i in range(3000):

    row = df.sample(1).iloc[0].copy()

    row["product_id"] = product_id
    product_id += 1

    row["brand"] = random.choice(BRANDS)

    row["material"] = random.choice(MATERIALS)

    row["price_range"] = random.choice(PRICE_RANGE)

    if row["price_range"] == "Budget":
        row["price"] = random.randint(399,999)

    elif row["price_range"] == "Affordable":
        row["price"] = random.randint(1000,2499)

    elif row["price_range"] == "Premium":
        row["price"] = random.randint(2500,5999)

    else:
        row["price"] = random.randint(6000,15000)

    row["rating"] = round(random.uniform(3.8,5.0),1)

    row["trend_score"] = random.randint(60,100)

    row["style_score"] = random.randint(65,100)

    row["ai_score"] = random.randint(70,100)

    row["season"] = random.choice(SEASONS)

    row["availability"] = random.choice([
        "In Stock",
        "Limited",
        "Few Left"
    ])

    row["sustainable"] = random.choice([
        "Yes",
        "No"
    ])

    row["likes"] = random.randint(100,15000)

    row["views"] = random.randint(1000,100000)

    records.append(row)

large_df = pd.DataFrame(records)


# -------------------------------
# Smart Compatibility Features
# -------------------------------

COLOR_MATCH = {
    "Neutral": ["Dark", "Blue", "Earthy", "Pastel", "Warm"],
    "Dark": ["Neutral", "Warm", "Cool"],
    "Blue": ["Neutral", "White", "Cool"],
    "Earthy": ["Neutral", "Warm"],
    "Warm": ["Neutral", "Earthy", "Dark"],
    "Cool": ["Neutral", "Blue"],
    "Pastel": ["Neutral", "Pink", "Cool"],
    "Pink": ["Neutral", "Pastel"],
    "Multi": ["Neutral", "Dark"]
}

STYLE_MATCH = {
    "Casual": ["Casual", "Streetwear", "Minimal"],
    "Streetwear": ["Streetwear", "Casual"],
    "Minimal": ["Minimal", "Smart Casual"],
    "Smart Casual": ["Smart Casual", "Minimal", "Formal"],
    "Formal": ["Formal", "Smart Casual"],
    "Trendy": ["Trendy", "Party"],
    "Party": ["Party", "Trendy"],
    "Traditional": ["Traditional"],
    "Sporty": ["Sporty", "Casual"],
    "Feminine": ["Feminine", "Minimal"]
}

for i in range(len(large_df)):

    color = large_df.loc[i, "color_family"]

    style = large_df.loc[i, "style"]

    large_df.loc[i, "matching_colors"] = ", ".join(
        COLOR_MATCH.get(color, ["Neutral"])
    )

    large_df.loc[i, "compatible_styles"] = ", ".join(
        STYLE_MATCH.get(style, ["Casual"])
    )

    large_df.loc[i, "occasion_score"] = random.randint(70, 100)

    large_df.loc[i, "weather_score"] = random.randint(70, 100)

    large_df.loc[i, "comfort_score"] = random.randint(75, 100)

    large_df.loc[i, "fashion_score"] = random.randint(70, 100)

    large_df.loc[i, "versatility_score"] = random.randint(60, 100)

    large_df.loc[i, "overall_score"] = round(
        (
            large_df.loc[i, "occasion_score"] +
            large_df.loc[i, "weather_score"] +
            large_df.loc[i, "comfort_score"] +
            large_df.loc[i, "fashion_score"] +
            large_df.loc[i, "versatility_score"]
        ) / 5,
        1
    )


    # -------------------------------
# Shuffle & Save Dataset
# -------------------------------

# Shuffle records
large_df = large_df.sample(frac=1).reset_index(drop=True)

# Save final dataset
large_df.to_csv("datasets/fashion_items_3000.csv", index=False)

print("=" * 50)
print("✅ AI Fashion Dataset Generated Successfully!")
print(f"Total Records : {len(large_df)}")
print(f"Total Columns : {len(large_df.columns)}")
print("Saved as      : fashion_items_3000.csv")
print("=" * 50)

# Preview
print("\nFirst 10 Records:\n")
print(large_df.head(10))
   