from flask import Flask, jsonify, request, send_from_directory
import os
import json
import random
import database
from recommendation_engine import RecommendationEngine

app = Flask(__name__, static_folder="static", static_url_path="")

# Initialize Recommendation Engine
engine = RecommendationEngine()

# Ensure database is initialized
database.create_tables()
default_user = database.get_or_create_default_user()
database.seed_default_wardrobe(default_user["user_id"])

# ✅ Define allowed wardrobe types (6 types)
ITEM_TYPES = ["top", "bottom", "shoes", "accessory", "outerwear", "onepiece"]


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# ---------------- PROFILE ----------------
@app.route("/api/profile", methods=["GET"])
def get_profile():
    try:
        user = database.get_or_create_default_user()
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profile", methods=["POST"])
def update_profile():
    try:
        data = request.get_json()
        user = database.get_or_create_default_user()
        user_id = user["user_id"]

        name = data.get("name", user["name"])
        age = int(data.get("age", user["age"]))
        gender = data.get("gender", user["gender"])
        skin_tone = data.get("skin_tone", user["skin_tone"])
        body_type = data.get("body_type", user["body_type"])
        style_preference = data.get("style_preference", user["style_preference"])

        database.update_user(
            user_id,
            name,
            age,
            gender,
            skin_tone,
            body_type,
            style_preference
        )

        # return updated user
        updated_user = database.get_or_create_default_user()
        return jsonify(updated_user)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- WARDROBE ----------------
@app.route("/api/wardrobe", methods=["GET"])
def get_wardrobe():
    try:
        user = database.get_or_create_default_user()
        items = database.get_wardrobe(user["user_id"])
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wardrobe", methods=["POST"])
def add_wardrobe_item():
    try:
        data = request.get_json()
        user = database.get_or_create_default_user()
        user_id = user["user_id"]

        item_type = data.get("item_type", "").lower()

        # ✅ validate item type
        if item_type not in ITEM_TYPES:
            return jsonify({"error": f"Invalid item_type. Must be one of {ITEM_TYPES}"}), 400

        category = data.get("category", "casual").lower()
        color = data.get("color", "neutral")
        style = data.get("style", "casual")

        image_path = data.get("image_path")

        # Placeholder images if none provided
        if not image_path:
            placeholders = {
                "top": [
                    "https://images.unsplash.com/photo-1521572267360-ee0c2909d518",
                    "https://images.unsplash.com/photo-1596755094514-f87e34085b2c",
                ],
                "bottom": [
                    "https://images.unsplash.com/photo-1541099649105-f69ad21f3246",
                    "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae",
                ],
                "shoes": [
                    "https://images.unsplash.com/photo-1549298916-b41d501d3772",
                    "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa",
                ],
                "accessory": [
                    "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
                    "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5",
                ],
                "outerwear": [
                    "https://images.unsplash.com/photo-1520975928310-17a9a9d9c1c6",
                    "https://images.unsplash.com/photo-1602810318383-6c6c6c6c6c6c",
                ],
                "onepiece": [
                    "https://images.unsplash.com/photo-1520975869018-1f3f1f3f1f3f",
                    "https://images.unsplash.com/photo-1520975918310-2a2a2a2a2a2a",
                ]
            }

            image_path = random.choice(
                placeholders.get(item_type, [
                    "https://images.unsplash.com/photo-1483985988355-763728e1935b"
                ])
            )

        item_id = database.add_wardrobe_item(
            user_id, item_type, category, color, style, image_path
        )

        return jsonify({
            "success": True,
            "item_id": item_id,
            "item_type": item_type,
            "category": category,
            "color": color,
            "style": style,
            "image_path": image_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wardrobe/<int:item_id>", methods=["DELETE"])
def delete_wardrobe_item(item_id):
    try:
        database.delete_wardrobe_item(item_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- GENERATE OUTFIT ----------------
@app.route("/api/generate", methods=["POST"])
def generate_recommendation():
    try:
        data = request.get_json() or {}

        user = database.get_or_create_default_user()
        user_id = user["user_id"]

        gender = data.get("gender") or user["gender"]
        age = int(data.get("age", user["age"]))
        style = data.get("style") or user["style_preference"]
        weather = data.get("weather", "Sunny")
        occasion = data.get("occasion", "Casual")

        outfit_result = engine.generate_outfit(
            user_id, gender, age, style, weather, occasion
        )

        items_json = json.dumps(outfit_result["items"])
        outfit_id = database.save_outfit(
            user_id, occasion, items_json, outfit_result["explanation"]
        )

        outfit_result["outfit_id"] = outfit_id

        return jsonify(outfit_result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ---------------- HISTORY ----------------
@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        user = database.get_or_create_default_user()
        outfits = database.get_outfit_history(user["user_id"])

        for outfit in outfits:
            try:
                outfit["items"] = json.loads(outfit["items"])
            except:
                outfit["items"] = []

        return jsonify(outfits)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- FEEDBACK ----------------
@app.route("/api/feedback", methods=["POST"])
def update_feedback():
    try:
        data = request.get_json()

        outfit_id = int(data.get("outfit_id"))
        rating = int(data.get("rating"))  # 1, 0, -1

        database.update_outfit_rating(outfit_id, rating)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- MAIN ----------------
if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host="127.0.0.1", port=5000, debug=True)