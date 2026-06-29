import streamlit as st
from database import update_user

def show_profile():

    st.title("👤 Create Your Fashion Profile")

    st.caption("Let's personalize Dressify for you.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Full Name")

        gender = st.selectbox(
            "Gender",
            ["Female", "Male", "Other"]
        )

        age = st.slider(
            "Age",
            10,
            70,
            20
        )

        height = st.number_input(
            "Height (cm)",
            100,
            220,
            165
        )

        weight = st.number_input(
            "Weight (kg)",
            30,
            200,
            60
        )

    with col2:

        body = st.selectbox(
            "Body Type",
            [
                "Pear",
                "Apple",
                "Rectangle",
                "Hourglass",
                "Triangle",
                "Athletic"
            ]
        )

        skin = st.selectbox(
            "Skin Tone",
            [
                "Fair",
                "Wheatish",
                "Olive",
                "Dark"
            ]
        )

        hair_length = st.selectbox(
            "Hair Length",
            [
                "Short",
                "Medium",
                "Long"
            ]
        )

        hair_type = st.selectbox(
            "Hair Type",
            [
                "Straight",
                "Wavy",
                "Curly"
            ]
        )

    st.markdown("---")

    st.subheader("Fashion Preferences")

    preferred_style = st.selectbox(
        "Preferred Style",
        [
            "Korean",
            "Streetwear",
            "Old Money",
            "Corporate",
            "Minimalist",
            "Y2K",
            "Ethnic",
            "Casual"
        ]
    )

    favorite_colors = st.multiselect(
        "Favorite Colors",
        [
            "White",
            "Black",
            "Blue",
            "Beige",
            "Brown",
            "Pink",
            "Green",
            "Grey"
        ]
    )

    budget = st.select_slider(
        "Budget",
        [
            "Budget",
            "Mid-Range",
            "Premium",
            "Luxury"
        ]
    )

    lifestyle = st.selectbox(
        "Lifestyle",
        [
            "Student",
            "Working Professional",
            "Freelancer",
            "Homemaker",
            "Other"
        ]
    )

    st.markdown("")

    if st.button("💾 Save Profile", use_container_width=True):

        profile = {

            "name": name,
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "body_type": body,
            "skin_tone": skin,
            "hair_length": hair_length,
            "hair_type": hair_type,
            "preferred_style": preferred_style,
            "favorite_colors": ",".join(favorite_colors),
            "budget": budget,
            "lifestyle": lifestyle

        }

        save_user(profile)

        st.success("✅ Profile Saved Successfully!")

        st.balloons()