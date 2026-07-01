import streamlit as st
import json
from datetime import date
import database
from recommendation_engine import RecommendationEngine

st.markdown("""
<style>
  /* paste the entire CSS from app.py here */
</style>
""", unsafe_allow_html=True)

engine = RecommendationEngine()
database.initialize_database()
user = database.get_or_create_user()
user_id = user["user_id"]

def main():
    st.set_page_config(
        page_title="DressiFy - Today's Look",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("✨ Today's Look")

    # Context inputs
    occasion = st.selectbox("Occasion", [
        "College", "Office", "Interview", "Wedding", "Party", "Date",
        "Casual Outing", "Gym", "Airport Look", "Vacation", "Festival", "Traditional Function"
    ])
    weather = st.selectbox("Weather", ["Sunny", "Rainy", "Winter", "Humid", "Windy"])

    # Optional mood
    mood = st.selectbox("Mood", ["Chill", "Bold", "Minimal", "Colourful"], index=0)

    use_wardrobe = st.toggle("🧥 Use my wardrobe items", value=False)

    if use_wardrobe and len(database.get_wardrobe(user_id)) == 0:
        st.warning("Wardrobe is empty — add items first in main app.")
        use_wardrobe = False

    if st.button("Generate Today's Look ✨"):
        with st.spinner("Styling your look..."):
            result = engine.generate_outfit(
                user_id=user_id,
                gender=user.get("gender", "Female"),
                age=int(user.get("age", 20)),
                body_type=user.get("body_type", "All"),
                skin_tone=user.get("skin_tone", "All"),
                occasion=occasion,
                weather=weather,
                preferred_fit=user.get("preferred_fit", "Regular"),
                fav_colors=json.loads(user.get("fav_colors", "[]")) if user.get("fav_colors") else [],
                use_wardrobe=use_wardrobe
            )

        outfit = result["outfit"]
        st.subheader("Today's Complete Look")
        for cat, details in outfit.items():
            st.write(f"**{cat.upper()}**: {details['item']} ({details['source']})")

        st.subheader("Why this works")
        st.write(result.get("explanation", "A well-balanced look for your context."))

        if st.button("💾 Save as Today's Look"):
            items_dict = {k: v["item"] for k, v in outfit.items()}
            oid = database.save_outfit(
                user_id=user_id,
                occasion=occasion,
                weather=weather,
                items_dict=items_dict,
                explanation=result.get("explanation", "")
            )
            st.success(f"Saved! Outfit ID: {oid}")

if __name__ == "__main__":
    main()