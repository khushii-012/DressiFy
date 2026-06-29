"""
DressiFy Recommendation Engine v2
- Integrates with SQLite wardrobe DB
- Filters by gender, body type, skin tone, occasion, weather, color
- Falls back to CSV dataset if wardrobe is empty
- Returns scored, ranked outfit
"""

import os
import pandas as pd
import database

DATA_FILE = "fashion_items.csv"

OCCASION_VIBE = {
    "College": "Casual", "Gym": "Casual", "Casual Outing": "Casual",
    "Vacation": "Casual", "Airport Look": "Casual",
    "Interview": "Formal", "Office": "Formal",
    "Wedding": "Formal", "Traditional Function": "Formal",
    "Party": "Party", "Date": "Romantic", "Festival": "Casual"
}

HAIRSTYLES = {
    "Female": {
        "Casual":   [("🎀", "Messy Bun", "Effortless & chic"), ("🎗️", "High Ponytail", "Clean & sporty")],
        "Formal":   [("✨", "Sleek Straight", "Polished & sharp"), ("🌸", "Soft Waves", "Elegant & feminine")],
        "Party":    [("💫", "Beach Waves", "Glamorous & textured"), ("🌙", "Half Up Half Down", "Playful & stylish")],
        "Romantic": [("🌹", "Soft Curls", "Romantic & flirty"), ("🎀", "Low Bun", "Effortlessly beautiful")],
    },
    "Male": {
        "Casual":   [("✂️", "Textured Crop", "Modern & low-effort"), ("🌊", "Curtains", "Retro & trendy")],
        "Formal":   [("💼", "Side Part", "Classic & professional"), ("⚡", "Quiff", "Sharp & confident")],
        "Party":    [("🐺", "Wolf Cut", "Edgy & trendy"), ("🔥", "Messy Textured", "Cool & effortless")],
        "Romantic": [("✨", "Slicked Back", "Suave & sophisticated"), ("💫", "Natural Waves", "Relaxed & attractive")],
    }
}

class RecommendationEngine:
    def __init__(self):
        self.df = pd.DataFrame()
        self._load_dataset()

    def _load_dataset(self):
        if os.path.exists(DATA_FILE):
            self.df = pd.read_csv(DATA_FILE)
        else:
            print("⚠ fashion_items.csv not found")

    # ─── FILTER CSV DATASET ───────────────────────────────
    def _filter_dataset(self, item_type, gender, body_type, skin_tone,
                        occasion, weather, fav_colors, preferred_fit):
        if self.df.empty:
            return None

        pool = self.df[self.df["type"] == item_type].copy()

        g = gender if gender != "Other" else "Female"
        pool = pool[pool["gender"].isin([g, "All"])]
        pool = pool[pool["weather"].isin([weather, "All"])]
        pool = pool[pool["occasion"].isin([occasion, "All"])]

        if body_type and body_type != "All":
            pool = pool[pool["body_type"].isin([body_type, "All"])]
        if skin_tone and skin_tone != "All":
            pool = pool[pool["skin_tone"].isin([skin_tone, "All"])]

        if fav_colors:
            colored = pool[pool["color_family"].isin(fav_colors)]
            if not colored.empty:
                pool = colored

        if pool.empty:
            return None
        return pool.sample(1).iloc[0].to_dict()

    # ─── FILTER WARDROBE ──────────────────────────────────
    def _filter_wardrobe(self, wardrobe, item_type):
        matches = [w for w in wardrobe if w["item_type"] == item_type]
        return matches[0] if matches else None

    # ─── MAIN GENERATE ────────────────────────────────────
    def generate_outfit(self, user_id, gender, age, body_type, skin_tone,
                        occasion, weather, preferred_fit, fav_colors,
                        use_wardrobe=False):

        wardrobe = database.get_wardrobe(user_id) if use_wardrobe else []
        vibe = OCCASION_VIBE.get(occasion, "Casual")
        g_key = gender if gender in ("Female", "Male") else "Female"
        hair_options = HAIRSTYLES[g_key].get(vibe, HAIRSTYLES[g_key]["Casual"])

        outfit = {}
        types_needed = ["top", "bottom", "shoes", "accessory"]
        if weather in ("Winter", "Rainy", "Windy"):
            types_needed.insert(2, "outerwear")

        emojis = {
            "top": "👕", "bottom": "👖", "outerwear": "🧥",
            "shoes": "👟", "accessory": "👜"
        }

        for t in types_needed:
            item = None

            # Try wardrobe first
            if use_wardrobe and wardrobe:
                w = self._filter_wardrobe(wardrobe, t)
                if w:
                    item = {
                        "type": t,
                        "item": w["item_name"],
                        "description": f"{w['color']} — {w.get('notes','')}" if w.get('color') else w.get('notes',''),
                        "source": "wardrobe",
                        "emoji": emojis.get(t, "🏷️")
                    }

            # Fallback to dataset
            if not item:
                row = self._filter_dataset(t, gender, body_type, skin_tone,
                                           occasion, weather, fav_colors, preferred_fit)
                if row:
                    item = {
                        "type": t,
                        "item": row["item"],
                        "description": row.get("description", ""),
                        "source": "catalogue",
                        "emoji": emojis.get(t, "🏷️")
                    }

            if item:
                outfit[t] = item

        return {
            "outfit": outfit,
            "hair_options": hair_options,
            "vibe": vibe,
            "occasion": occasion,
            "weather": weather
        }

    def get_hairstyles(self, gender, occasion):
        vibe = OCCASION_VIBE.get(occasion, "Casual")
        g_key = gender if gender in ("Female", "Male") else "Female"
        return HAIRSTYLES[g_key].get(vibe, HAIRSTYLES[g_key]["Casual"])