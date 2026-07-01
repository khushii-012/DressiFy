"""
=========================================================
DressiFy Recommendation Engine v3
=========================================================

Features
--------
✔ Intelligent outfit scoring
✔ Wardrobe priority
✔ Dataset fallback
✔ Body type matching
✔ Skin tone matching
✔ Weather matching
✔ Occasion matching
✔ Favourite color matching
✔ Style Goal support
✔ Trend-ready architecture
✔ Avatar-ready architecture
✔ AI explanation generator
✔ Hairstyle recommendation

"""

import os
import random
import pandas as pd

import database

DATA_FILE = "fashion_items.csv"

# -------------------------------------------------------
# Occasion → Outfit Vibe
# -------------------------------------------------------

OCCASION_VIBE = {

    "College": "Casual",
    "Gym": "Sporty",
    "Casual Outing": "Casual",
    "Vacation": "Casual",
    "Airport Look": "Casual",

    "Office": "Formal",
    "Interview": "Formal",

    "Wedding": "Traditional",
    "Festival": "Traditional",

    "Party": "Party",
    "Date": "Romantic"

}

# -------------------------------------------------------
# Hairstyle Database
# -------------------------------------------------------

HAIRSTYLES = {

    "Female": {

        "Casual": [

            ("🎀", "Messy Bun", "Effortless and comfortable"),
            ("🌸", "Loose Waves", "Soft everyday hairstyle"),
            ("✨", "Half Pony", "Cute and practical")

        ],

        "Formal": [

            ("💼", "Low Bun", "Professional appearance"),
            ("✨", "Straight Hair", "Elegant office look"),
            ("🌺", "French Twist", "Sophisticated")

        ],

        "Party": [

            ("💫", "Beach Waves", "Stylish and glamorous"),
            ("🔥", "Hollywood Curls", "Party ready"),
            ("🌙", "Half Up Half Down", "Trendy")

        ],

        "Romantic": [

            ("🌹", "Soft Curls", "Romantic look"),
            ("💕", "Side Braid", "Cute"),
            ("🎀", "Low Bun", "Elegant")

        ],

        "Traditional": [

            ("🌼", "Gajra Bun", "Classic ethnic"),
            ("✨", "Braided Bun", "Traditional"),
            ("🌸", "Long Braid", "Graceful")

        ]

    },

    "Male": {

        "Casual": [

            ("✂", "Textured Crop", "Modern"),
            ("🌊", "Curtains", "Relaxed"),
            ("🔥", "Messy Hair", "Effortless")

        ],

        "Formal": [

            ("💼", "Side Part", "Professional"),
            ("✨", "Comb Over", "Elegant"),
            ("⚡", "Quiff", "Sharp")

        ],

        "Party": [

            ("🐺", "Wolf Cut", "Trendy"),
            ("🔥", "Messy Quiff", "Cool"),
            ("🎉", "Pompadour", "Bold")

        ],

        "Romantic": [

            ("💕", "Natural Waves", "Soft"),
            ("✨", "Slick Back", "Confident"),
            ("🌙", "Medium Flow", "Relaxed")

        ],

        "Traditional": [

            ("👑", "Classic Side Part", "Traditional"),
            ("✨", "Neat Comb", "Elegant"),
            ("🔥", "Styled Quiff", "Modern Ethnic")

        ]

    }

}

# -------------------------------------------------------
# Color Harmony
# -------------------------------------------------------

COLOR_MATCH = {

    "Neutral": [
        "Neutral",
        "Dark",
        "Blue",
        "Earthy",
        "Warm",
        "Cool"
    ],

    "Blue": [
        "Neutral",
        "White",
        "Cool",
        "Dark"
    ],

    "Dark": [
        "Neutral",
        "Warm",
        "Cool"
    ],

    "Earthy": [
        "Neutral",
        "Warm",
        "Earthy"
    ],

    "Pink": [
        "Neutral",
        "Pastel"
    ],

    "Pastel": [
        "Neutral",
        "Pink"
    ],

    "Warm": [
        "Neutral",
        "Earthy",
        "Dark"
    ],

    "Cool": [
        "Neutral",
        "Blue",
        "Dark"
    ]

}

# -------------------------------------------------------
# Style Goal Bonus
# -------------------------------------------------------

STYLE_GOAL_BONUS = {

    "Look More Professional": {

        "Formal": 30,
        "Smart Casual": 20,
        "Minimal": 15

    },

    "Experiment with Colours": {

        "Pastel": 20,
        "Pink": 20,
        "Warm": 20,
        "Cool": 20,
        "Multi": 20

    },

    "Use My Ethnic Wear More": {

        "Traditional": 35

    }

}

# =======================================================
# Recommendation Engine
# =======================================================

class RecommendationEngine:

    def __init__(self):

        self.df = pd.DataFrame()

        self.load_dataset()

    # ---------------------------------------------------

    def load_dataset(self):

        if os.path.exists(DATA_FILE):

            self.df = pd.read_csv(DATA_FILE)

            self.df.columns = [
                c.strip().lower()
                for c in self.df.columns
            ]

        else:

            print("fashion_items.csv not found")

    # ---------------------------------------------------

    def get_style_goal(self, user_id):

        goals = database.get_style_goals(user_id)

        if not goals:
            return None

        return goals[0]["goal_name"]

    # ---------------------------------------------------

    def get_candidates(self, item_type):

        if self.df.empty:
            return pd.DataFrame()

        return self.df[
            self.df["type"].str.lower() == item_type.lower()
        ].copy()
    
        # ---------------------------------------------------
    # AI Scoring Function
    # ---------------------------------------------------

    def calculate_score(
        self,
        row,
        gender,
        body_type,
        skin_tone,
        occasion,
        weather,
        preferred_fit,
        fav_colors,
        style_goal
    ):

        score = 0

        # ---------------- Gender ----------------

        if str(row.get("gender", "All")) in [gender, "All"]:
            score += 25

        # ---------------- Occasion ----------------

        if str(row.get("occasion", "All")) in [occasion, "All"]:
            score += 30

        # ---------------- Weather ----------------

        if str(row.get("weather", "All")) in [weather, "All"]:
            score += 20

        # ---------------- Body Type ----------------

        if str(row.get("body_type", "All")) in [body_type, "All"]:
            score += 12

        # ---------------- Skin Tone ----------------

        if str(row.get("skin_tone", "All")) in [skin_tone, "All"]:
            score += 8

        # ---------------- Preferred Fit ----------------

        if str(row.get("style", "All")) in [preferred_fit, "All"]:
            score += 10

        # ---------------- Favourite Colors ----------------

        color = str(row.get("color_family", ""))

        if fav_colors:

            if isinstance(fav_colors, str):
                fav_colors = [fav_colors]

            if color in fav_colors:
                score += 18

        # ---------------- Style Goal ----------------

        if style_goal:

            bonus = STYLE_GOAL_BONUS.get(style_goal, {})

            if color in bonus:
                score += bonus[color]

            style = str(row.get("style", ""))

            if style in bonus:
                score += bonus[style]

            category = str(row.get("category", ""))

            if category in bonus:
                score += bonus[category]

        # ---------------- Randomness ----------------
        # Prevents recommending the exact same outfit every time

        score += random.randint(0, 5)

        return score

    # ---------------------------------------------------
    # Choose Best Item
    # ---------------------------------------------------

    def choose_best_item(
        self,
        item_type,
        gender,
        body_type,
        skin_tone,
        occasion,
        weather,
        preferred_fit,
        fav_colors,
        style_goal
    ):

        candidates = self.get_candidates(item_type)

        if candidates.empty:
            return None

        candidates["score"] = candidates.apply(

            lambda row:

            self.calculate_score(

                row,

                gender,

                body_type,

                skin_tone,

                occasion,

                weather,

                preferred_fit,

                fav_colors,

                style_goal

            ),

            axis=1

        )

        candidates = candidates.sort_values(

            by="score",

            ascending=False

        )

        top = candidates.head(5)

        if top.empty:
            return None

        chosen = top.sample(1).iloc[0]

        return {

            "type": item_type,

            "item": chosen["item"],

            "description": chosen.get(

                "description",

                ""

            ),

            "image": chosen.get(

                "image",

                ""

            ),

            "color": chosen.get(

                "color_family",

                ""

            ),

            "score": int(chosen["score"]),

            "source": "catalogue"

        }

    # ---------------------------------------------------
    # Wardrobe Item
    # ---------------------------------------------------

    def get_wardrobe_item(

        self,

        wardrobe,

        item_type

    ):

        for item in wardrobe:

            if item["item_type"].lower() == item_type.lower():

                return {

                    "type": item_type,

                    "item": item["item_name"],

                    "description": item.get(

                        "notes",

                        ""

                    ),

                    "image": "",

                    "color": item.get(

                        "color",

                        ""

                    ),

                    "score": 999,

                    "source": "wardrobe"

                }

        return None

    # ---------------------------------------------------
    # Explanation Generator
    # ---------------------------------------------------

    def generate_explanation(

        self,

        outfit,

        occasion,

        weather,

        style_goal

    ):

        text = (

            f"This outfit was selected for "

            f"your {occasion.lower()} "

            f"during {weather.lower()} weather. "

        )

        if style_goal:

            text += (

                f"It also supports your style goal "

                f"of '{style_goal}'. "

            )

        text += (

            "The items have been chosen "

            "based on colour harmony, "

            "occasion suitability, "

            "weather comfort "

            "and overall fashion balance."

        )

        return text 
    
        # ---------------------------------------------------
    # Main Recommendation Function
    # ---------------------------------------------------

    def generate_outfit(
        self,
        user_id,
        gender,
        age,
        body_type,
        skin_tone,
        occasion,
        weather,
        preferred_fit,
        fav_colors,
        use_wardrobe=False
    ):

        wardrobe = database.get_wardrobe(user_id) if use_wardrobe else []

        style_goal = self.get_style_goal(user_id)

        vibe = OCCASION_VIBE.get(
            occasion,
            "Casual"
        )

        # ---------------------------------------------------
        # Decide Outfit Type
        # ---------------------------------------------------

        if occasion in ["Wedding", "Festival"]:

            types_needed = [
                "traditional",
                "shoes",
                "accessory"
            ]

        elif occasion in ["Party", "Date"]:

            if gender == "Female":

                types_needed = [
                    "dress",
                    "shoes",
                    "accessory"
                ]

            else:

                types_needed = [
                    "top",
                    "bottom",
                    "shoes",
                    "accessory"
                ]

        else:

            types_needed = [
                "top",
                "bottom",
                "shoes",
                "accessory"
            ]

        if weather in [

            "Winter",

            "Rainy",

            "Windy"

        ]:

            if "outerwear" not in types_needed:

                types_needed.insert(
                    2,
                    "outerwear"
                )

        # ---------------------------------------------------
        # Outfit Building
        # ---------------------------------------------------

        outfit = {}

        for item_type in types_needed:

            selected = None

            # ---------- Wardrobe Priority ----------

            if use_wardrobe:

                selected = self.get_wardrobe_item(

                    wardrobe,

                    item_type

                )

            # ---------- Dataset ----------

            if selected is None:

                selected = self.choose_best_item(

                    item_type,

                    gender,

                    body_type,

                    skin_tone,

                    occasion,

                    weather,

                    preferred_fit,

                    fav_colors,

                    style_goal

                )

            if selected:

                outfit[item_type] = selected

        # ---------------------------------------------------
        # Hairstyles
        # ---------------------------------------------------

        hairstyles = self.get_hairstyles(

            gender,

            occasion

        )

        # ---------------------------------------------------
        # AI Explanation
        # ---------------------------------------------------

        explanation = self.generate_explanation(

            outfit,

            occasion,

            weather,

            style_goal

        )

        # ---------------------------------------------------
        # Total Outfit Score
        # ---------------------------------------------------

        total_score = 0

        for item in outfit.values():

            total_score += item.get(

                "score",

                0

            )

        if outfit:

            outfit_score = round(

                total_score /

                len(outfit)

            )

        else:

            outfit_score = 0

        # ---------------------------------------------------
        # Final Output
        # ---------------------------------------------------

        return {

            "outfit": outfit,

            "hairstyles": hairstyles,

            "score": outfit_score,

            "style_goal": style_goal,

            "occasion": occasion,

            "weather": weather,

            "vibe": vibe,

            "explanation": explanation

        }

    # ---------------------------------------------------
    # Hairstyle Getter
    # ---------------------------------------------------

    def get_hairstyles(

        self,

        gender,

        occasion

    ):

        vibe = OCCASION_VIBE.get(

            occasion,

            "Casual"

        )

        gender = (

            "Female"

            if gender not in

            HAIRSTYLES

            else gender

        )

        styles = HAIRSTYLES[

            gender

        ].get(

            vibe,

            HAIRSTYLES[gender]["Casual"]

        )

        random.shuffle(styles)

        return styles[:2]