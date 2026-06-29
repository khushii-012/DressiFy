import streamlit as st
from recommendation_engine import RecommendationEngine
from database import get_user


def show_ai_generator():

    st.title("✨ AI Outfit Generator")
    st.caption("Get personalized outfit recommendations powered by AI.")

    engine = RecommendationEngine()

    user = get_user()

    if user is None:
        st.warning("⚠ Please create your profile first.")
        return

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        weather = st.selectbox(
            "🌦 Weather",
            ["Sunny", "Rainy", "Cold"]
        )

        occasion = st.selectbox(
            "🎯 Occasion",
            ["Casual", "Party", "Formal"]
        )

    with col2:
        style = st.selectbox(
            "✨ Preferred Style",
            [
                "Casual",
                "Korean",
                "Old Money",
                "Streetwear",
                "Corporate",
                "Minimalist"
            ]
        )

        mood = st.selectbox(
            "😊 Mood",
            [
                "Minimal",
                "Elegant",
                "Cute",
                "Bold",
                "Comfort"
            ]
        )

    st.markdown("")

    if st.button("✨ Generate Outfit", use_container_width=True):

        with st.spinner("Creating your perfect outfit... ✨"):

            outfit = engine.generate_outfit(
                user_id=user["user_id"],
                gender=user["gender"],
                age=user["age"],
                style=style,
                weather=weather,
                occasion=occasion
            )

        st.success("✨ Outfit Generated Successfully!")

        st.markdown("---")
        st.subheader("👗 Your AI Look")

        items = outfit["items"]

        for key in ["top", "bottom", "shoes", "accessory"]:

            if key in items:

                cloth = items[key]

                with st.container(border=True):

                    st.write(f"### {key.capitalize()}")
                    st.write(cloth["item"])

                    if cloth["image"]:
                        st.image(cloth["image"], width=220)

                    st.caption(f"Source: {cloth['source']}")

        st.markdown("---")

        st.subheader("🤖 AI Stylist")

        st.info(outfit["explanation"])