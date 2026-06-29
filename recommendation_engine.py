import os
import random
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import database

print("🔥 Upgraded Recommendation Engine Loaded")


DATA_FILE = "fashion_items.csv"


# -------------------------
# ENCODING MAPS
# -------------------------
GENDER_MAP = {"Female": 0, "Male": 1, "Other": 2}
STYLE_MAP = {"Casual": 0, "Trendy": 1, "Formal": 2}
WEATHER_MAP = {"Sunny": 0, "Rainy": 1, "Cold": 2}
OCCASION_MAP = {"Casual": 0, "Party": 1, "Formal": 2}


class RecommendationEngine:

    def __init__(self):
        self.df = pd.DataFrame()
        self.model = None

        self.load_dataset()
        self.train_model()

    # -------------------------
    # LOAD DATASET
    # -------------------------
    def load_dataset(self):
        if os.path.exists(DATA_FILE):
            self.df = pd.read_csv(DATA_FILE)
        else:
            print("⚠ fashion_items.csv not found")

    # -------------------------
    # TRAIN MODEL
    # -------------------------
    def train_model(self):
        if self.df.empty:
            return

        try:
            X = self.df[["gender", "age", "style", "weather", "occasion"]]
            y = self.df["category"]

            self.model = DecisionTreeClassifier(random_state=42)
            self.model.fit(X, y)

        except Exception as e:
            print("Training Error:", e)
            self.model = None

    # -------------------------
    # PREDICT CATEGORY
    # -------------------------
    def predict_category(self, gender, age, style, weather, occasion):

        if self.model is None:
            return occasion.lower()

        try:
            return self.model.predict([[
                GENDER_MAP.get(gender, 0),
                int(age),
                STYLE_MAP.get(style, 0),
                WEATHER_MAP.get(weather, 0),
                OCCASION_MAP.get(occasion, 0)
            ]])[0]

        except:
            return occasion.lower()

    # -------------------------
    # SMART SCORE FUNCTION
    # -------------------------
    def score_item(self, item, category, style, weather, occasion):

        score = 0

        if item["category"].lower() == category.lower():
            score += 3

        if item.get("style", "").lower() == style.lower():
            score += 2

        if weather == "Cold" and item["item_type"] == "top":
            score += 2

        if weather == "Sunny" and item["item_type"] in ["top", "bottom"]:
            score += 1

        if occasion.lower() == "formal" and item["category"].lower() == "formal":
            score += 3

        return score

    # -------------------------
    # GENERATE OUTFIT (MAIN AI)
    # -------------------------
    def generate_outfit(self, user_id, gender, age, style, weather, occasion):

        category = self.predict_category(gender, age, style, weather, occasion)

        outfit = {}

        # FIX: convert DB rows → dict
        wardrobe = database.get_wardrobe(user_id)
        wardrobe = [dict(i) for i in wardrobe]

        type_mapping = {
            "top": "top",
            "bottom": "bottom",
            "shoes": "shoes",
            "accessory": "accessory"
        }

        # -------------------------
        # BUILD OUTFIT
        # -------------------------
        for outfit_type, db_type in type_mapping.items():

            # FILTER WARDROBE ITEMS
            candidates = [
                item for item in wardrobe
                if item["item_type"] == db_type
            ]

            if candidates:

                # 🔥 SORT BY SCORE (AI UPGRADE)
                ranked = sorted(
                    candidates,
                    key=lambda x: self.score_item(x, category, style, weather, occasion),
                    reverse=True
                )

                chosen = ranked[0]

                outfit[outfit_type] = {
                    "item": chosen.get("category", chosen.get("item_type", "item")),
                    "image": chosen.get("image_path", ""),
                    "source": "Smart Wardrobe AI"
                }

            else:

                # -------------------------
                # DATASET FALLBACK
                # -------------------------
                if not self.df.empty:

                    dataset_items = self.df[self.df["category"] == category]

                    if not dataset_items.empty:

                        row = dict(dataset_items.sample(1).iloc[0])

                        outfit[outfit_type] = {
                            "item": row.get("item", "Item"),
                            "image": row.get("image", ""),
                            "source": "AI Dataset Fallback"
                        }

                    else:

                        outfit[outfit_type] = {
                            "item": "No recommendation",
                            "image": "",
                            "source": "None"
                        }

                else:

                    outfit[outfit_type] = {
                        "item": "No recommendation",
                        "image": "",
                        "source": "None"
                    }

        # -------------------------
        # AI EXPLANATION
        # -------------------------
        explanation = (
            f"This AI-generated outfit is optimized for a {weather.lower()} day, "
            f"suitable for a {occasion.lower()} occasion, "
            f"and aligned with a {style.lower()} style preference. "
            f"It prioritizes wardrobe compatibility and smart style matching."
        )

        return {
            "category": category,
            "items": outfit,
            "explanation": explanation
        }


# -------------------------
# TEST RUN
# -------------------------
if __name__ == "__main__":

    engine = RecommendationEngine()

    result = engine.generate_outfit(
        user_id=1,
        gender="Female",
        age=20,
        style="Casual",
        weather="Sunny",
        occasion="Casual"
    )

    print("\nCATEGORY:", result["category"])
    print("\nOUTFIT:")
    for k, v in result["items"].items():
        print(k.upper(), ":", v["item"])

    print("\nEXPLANATION:", result["explanation"])