"""
DressiFy Recommendation Engine v3
- AI outfit scoring (0-100) with confidence label
- Color harmony analysis
- Missing item detection
- Body type + skin tone smart filtering
- Wardrobe-first with CSV fallback
"""

import os
import random
import pandas as pd
import database

DATA_FILE = "fashion_items.csv"

OCCASION_VIBE = {
    "College": "Casual", "Gym": "Sporty", "Casual Outing": "Casual",
    "Vacation": "Casual", "Airport Look": "Casual",
    "Interview": "Formal", "Office": "Formal",
    "Wedding": "Formal", "Traditional Function": "Formal",
    "Party": "Party", "Date": "Romantic", "Festival": "Festive"
}

HAIRSTYLES = {
    "Female": {
        "Casual":   [("🎀", "Messy Bun", "Effortless & chic"), ("🎗️", "High Ponytail", "Clean & sporty"), ("✨", "Soft Waves", "Relaxed & pretty")],
        "Formal":   [("✨", "Sleek Straight", "Polished & sharp"), ("🌸", "Low Chignon", "Elegant & professional"), ("💫", "French Twist", "Classic & refined")],
        "Party":    [("💫", "Beach Waves", "Glamorous & textured"), ("🌙", "Half Up Half Down", "Playful & stylish"), ("💎", "Hollywood Curls", "Dramatic & glam")],
        "Romantic": [("🌹", "Soft Curls", "Romantic & flirty"), ("🎀", "Braided Low Bun", "Effortlessly beautiful"), ("🌸", "Side Swept", "Feminine & elegant")],
        "Sporty":   [("⚡", "Sleek Ponytail", "Athletic & clean"), ("🎀", "Dutch Braid", "Sporty & trendy"), ("✂️", "Top Knot", "Practical & cute")],
        "Festive":  [("🌺", "Floral Hair", "Festive & vibrant"), ("💐", "Loose Curls", "Traditional & beautiful"), ("✨", "Accessorised Bun", "Ethnic & chic")],
    },
    "Male": {
        "Casual":   [("✂️", "Textured Crop", "Modern & low-effort"), ("🌊", "Curtains", "Retro & trendy"), ("💈", "Natural Tousled", "Effortlessly cool")],
        "Formal":   [("💼", "Side Part", "Classic & professional"), ("⚡", "Slicked Back", "Sharp & authoritative"), ("💈", "Clean Fade", "Modern & sharp")],
        "Party":    [("🐺", "Wolf Cut", "Edgy & trendy"), ("🔥", "Messy Textured", "Cool & effortless"), ("✨", "Quiff", "Bold & stylish")],
        "Romantic": [("✨", "Styled Quiff", "Suave & handsome"), ("💫", "Natural Waves", "Relaxed & charming"), ("💈", "Neat Side Part", "Classic & romantic")],
        "Sporty":   [("✂️", "Short Buzz", "Clean & athletic"), ("💈", "Crew Cut", "Sporty & neat"), ("🌊", "Textured Pompadour", "Athletic & stylish")],
        "Festive":  [("💈", "Neat Quiff", "Traditional & smart"), ("✂️", "Side Parted", "Classic & elegant"), ("⚡", "Slicked Back", "Formal & festive")],
    }
}

# Color harmony rules
COLOR_HARMONY = {
    "Neutral":  ["Dark", "Neutral", "Warm", "Cool", "Pastel", "Earthy", "Pink", "Multi"],
    "Dark":     ["Neutral", "Dark", "Warm", "Cool"],
    "Warm":     ["Neutral", "Warm", "Earthy", "Dark"],
    "Cool":     ["Neutral", "Cool", "Dark", "Pastel"],
    "Pastel":   ["Neutral", "Pastel", "Cool", "Pink"],
    "Earthy":   ["Neutral", "Earthy", "Warm", "Dark"],
    "Pink":     ["Neutral", "Pastel", "Dark", "Pink"],
    "Multi":    ["Neutral", "Dark"],
}

# What makes a complete outfit per occasion
REQUIRED_ITEMS = {
    "Interview":  ["top", "bottom", "shoes"],
    "Office":     ["top", "bottom", "shoes"],
    "Wedding":    ["top", "bottom", "shoes", "accessory"],
    "Party":      ["top", "bottom", "shoes", "accessory"],
    "Date":       ["top", "bottom", "shoes"],
    "College":    ["top", "bottom", "shoes"],
    "Gym":        ["top", "bottom", "shoes"],
    "Vacation":   ["top", "bottom", "shoes", "accessory"],
    "Casual Outing": ["top", "bottom", "shoes"],
    "Airport Look":  ["top", "bottom", "shoes", "accessory"],
    "Festival":   ["top", "bottom", "shoes", "accessory"],
    "Traditional Function": ["traditional", "shoes", "accessory"],
}

MISSING_SUGGESTIONS = {
    "top":        ["White Oversized Tee", "Linen Shirt", "Polo Shirt", "Knit Sweater"],
    "bottom":     ["Blue Straight Jeans", "Black Trousers", "Cargo Pants", "Wide-Leg Pants"],
    "shoes":      ["White Sneakers", "Loafers", "Black Ankle Boots", "Sandals"],
    "accessory":  ["Silver Watch", "Tote Bag", "Sunglasses", "Gold Chain"],
    "outerwear":  ["Denim Jacket", "Beige Blazer", "Black Leather Jacket", "Puffer Jacket"],
    "traditional":["Kurti + Dupatta", "Kurta Pajama", "Saree", "Anarkali Suit"],
}

class RecommendationEngine:
    def __init__(self):
        self.df = pd.DataFrame()
        self._load()

    def _load(self):
        if os.path.exists(DATA_FILE):
            self.df = pd.read_csv(DATA_FILE)

    # ── Filter CSV ─────────────────────────────────
    def _pick(self, item_type, gender, body_type, skin_tone, occasion, weather, fav_colors, exclude_names=None):
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
        if exclude_names:
            pool = pool[~pool["item"].isin(exclude_names)]
        if fav_colors:
            colored = pool[pool["color_family"].isin(fav_colors)]
            if not colored.empty:
                pool = colored
        if pool.empty:
            return None
        return pool.sample(1).iloc[0].to_dict()

    # ── Score Outfit 0-100 ─────────────────────────
    def _score_outfit(self, outfit_items, occasion, weather, gender, body_type, skin_tone, use_wardrobe):
        score = 50  # base
        factors = []

        # Completeness
        required = REQUIRED_ITEMS.get(occasion, ["top", "bottom", "shoes"])
        has = set(outfit_items.keys())
        completeness = len([r for r in required if r in has]) / len(required)
        score += int(completeness * 20)
        if completeness == 1.0:
            factors.append("Complete outfit ✓")

        # Color harmony
        colors = [v.get("color_family", "Neutral") for v in outfit_items.values() if v.get("color_family")]
        if colors:
            harmony_hits = 0
            for i, c1 in enumerate(colors):
                for c2 in colors[i+1:]:
                    if c2 in COLOR_HARMONY.get(c1, []):
                        harmony_hits += 1
            max_pairs = max(1, len(colors) * (len(colors)-1) // 2)
            harmony_ratio = harmony_hits / max_pairs
            score += int(harmony_ratio * 15)
            if harmony_ratio > 0.7:
                factors.append("Great colour harmony ✓")

        # Weather fit
        weather_types = [v.get("weather", "All") for v in outfit_items.values() if v.get("weather")]
        weather_fit = all(w in [weather, "All"] for w in weather_types)
        if weather_fit:
            score += 8
            factors.append(f"{weather} weather appropriate ✓")

        # Wardrobe bonus (personal items)
        if use_wardrobe:
            wardrobe_items = [v for v in outfit_items.values() if v.get("source") == "wardrobe"]
            if wardrobe_items:
                score += min(7, len(wardrobe_items) * 2)
                factors.append(f"{len(wardrobe_items)} items from your wardrobe ✓")

        score = min(99, max(55, score))

        if score >= 90:
            confidence = "Excellent Match"
        elif score >= 80:
            confidence = "Strong Match"
        elif score >= 70:
            confidence = "Good Match"
        else:
            confidence = "Decent Pick"

        return score, confidence, factors

    # ── Color Analysis ─────────────────────────────
    def analyze_colors(self, wardrobe):
        if not wardrobe:
            return {}
        family_counts = {}
        for item in wardrobe:
            cf = item.get("color_family", "Neutral")
            family_counts[cf] = family_counts.get(cf, 0) + 1
        dominant = max(family_counts, key=family_counts.get) if family_counts else "Neutral"
        missing = [c for c in ["Neutral", "Dark", "Warm", "Cool"] if c not in family_counts]
        return {
            "distribution": family_counts,
            "dominant": dominant,
            "missing_colors": missing,
            "total": len(wardrobe)
        }

    # ── Missing Items ──────────────────────────────
    def find_missing_items(self, wardrobe, gender):
        wardrobe_types = set(w["item_type"] for w in wardrobe)
        all_types = ["top", "bottom", "shoes", "accessory", "outerwear"]
        missing = []
        for t in all_types:
            if t not in wardrobe_types:
                suggestions = MISSING_SUGGESTIONS.get(t, [])
                if suggestions:
                    missing.append({
                        "type": t,
                        "suggestion": random.choice(suggestions),
                        "reason": f"You have no {t}s in your wardrobe"
                    })
            elif sum(1 for w in wardrobe if w["item_type"] == t) < 2:
                suggestions = MISSING_SUGGESTIONS.get(t, [])
                if suggestions:
                    missing.append({
                        "type": t,
                        "suggestion": random.choice([s for s in suggestions]),
                        "reason": f"Only {sum(1 for w in wardrobe if w['item_type']==t)} {t}(s) — consider adding more variety"
                    })
        return missing[:5]

    # ── MAIN GENERATE ──────────────────────────────
    def generate_outfit(self, user_id, gender, age, body_type, skin_tone,
                        occasion, weather, preferred_fit, fav_colors, use_wardrobe=False):
        wardrobe = database.get_wardrobe(user_id) if use_wardrobe else []
        vibe = OCCASION_VIBE.get(occasion, "Casual")
        g_key = gender if gender in ("Female", "Male") else "Female"
        hair_options = HAIRSTYLES[g_key].get(vibe, HAIRSTYLES[g_key]["Casual"])

        types_needed = ["top", "bottom", "shoes", "accessory"]
        if occasion == "Traditional Function":
            types_needed = ["traditional", "shoes", "accessory"]
        if weather in ("Winter", "Rainy", "Windy"):
            types_needed.insert(2, "outerwear")

        emojis = {"top":"👕","bottom":"👖","outerwear":"🧥","shoes":"👟",
                  "accessory":"👜","traditional":"🥻","dress":"👗"}
        
        outfit = {}
        used_names = []

        for t in types_needed:
            item = None
            # Wardrobe first
            if use_wardrobe and wardrobe:
                candidates = [w for w in wardrobe if w["item_type"] == t and w["item_name"] not in used_names]
                if candidates:
                    chosen = random.choice(candidates)
                    # Try to find color_family from CSV for matching
                    cf_match = self.df[self.df["item"] == chosen["item_name"]]["color_family"].values
                    cf = cf_match[0] if len(cf_match) > 0 else chosen.get("color_family", "Neutral")
                    item = {
                        "type": t,
                        "item": chosen["item_name"],
                        "description": f"{chosen['color']}" if chosen.get("color") else "",
                        "color_family": cf,
                        "weather": "All",
                        "source": "wardrobe",
                        "emoji": emojis.get(t, "🏷️")
                    }
                    used_names.append(chosen["item_name"])

            # CSV fallback
            if not item:
                row = self._pick(t, gender, body_type, skin_tone, occasion, weather, fav_colors, used_names)
                if row:
                    item = {
                        "type": t,
                        "item": row["item"],
                        "description": row.get("description", ""),
                        "color_family": row.get("color_family", "Neutral"),
                        "weather": row.get("weather", "All"),
                        "source": "catalogue",
                        "emoji": emojis.get(t, "🏷️")
                    }
                    used_names.append(row["item"])

            if item:
                outfit[t] = item

        # Score it
        ai_score, confidence, score_factors = self._score_outfit(
            outfit, occasion, weather, gender, body_type, skin_tone, use_wardrobe
        )

        return {
            "outfit": outfit,
            "hair_options": hair_options,
            "vibe": vibe,
            "occasion": occasion,
            "weather": weather,
            "ai_score": ai_score,
            "confidence": confidence,
            "score_factors": score_factors,
        }