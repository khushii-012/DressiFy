import streamlit as st
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


def show_hero():

    img = get_base64_image("static/images/hero/hero.jpg")

    st.markdown(
        f"""
        <style>
        .hero {{
            position: relative;
            height: 520px;
            border-radius:30px;
            overflow:hidden;
            background-image:
                linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35)),
                url("data:image/jpg;base64,{img}");
            background-size:cover;
            background-position:center;
            display:flex;
            justify-content:center;
            align-items:center;
            text-align:center;
            margin-bottom:40px;
        }}

        .hero-content h1{{
            color:white;
            font-size:72px;
            font-weight:800;
            margin-bottom:8px;
        }}

        .hero-content p{{
            color:white;
            font-size:24px;
            margin-bottom:25px;
        }}

        .hero-btn{{
            background:#FF4FA3;
            color:white;
            padding:15px 40px;
            border-radius:50px;
            font-size:18px;
            font-weight:700;
            display:inline-block;
        }}
        </style>

        <div class="hero">

            <div class="hero-content">

                <h1>👗 Dressify</h1>

                <p>Your Personal AI Fashion Stylist</p>

                <div class="hero-btn">
                    Discover Your Style →
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )