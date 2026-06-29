import streamlit as st
from database import create_tables
from pages.profile import show_profile
from pages.wardrobe import show_wardrobe
from utils.styles import load_css
from components.hero import show_hero
from components.stat_cards import show_stats
from pages.ai_outfit_generator import show_ai_generator
# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Dressify AI",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)
initialize_database()
load_css()
st.markdown("""
<div style="
background:red;
color:white;
padding:20px;
border-radius:20px;
font-size:30px;
text-align:center;
">
CSS is Working ❤️
</div>
""", unsafe_allow_html=True)
# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.title("👗 Dressify")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👤 Profile",
        "👚 My Wardrobe",
        "✨ AI Outfit Generator",
        "🎨 Color Studio",
        "💇 Hair Studio",
        "📊 Closet Analytics",
        "❤️ Saved Looks",
        "⚙ Settings"
    ]
)

# ------------------------------
# HOME
# ------------------------------
# HOME
# ------------------------------
if page == "🏠 Home":

    show_hero()
    st.markdown("## ✨ Discover Your Fashion Universe")

   
    st.markdown("---")

    st.header("✨ Trending Styles")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.success("🇰🇷 Korean Minimal")

    with c2:
        st.success("💼 Corporate Chic")

    with c3:
        st.success("🤍 Old Money")

    with c4:
        st.success("🖤 Quiet Luxury")

    st.markdown("---")

    st.header("💡 AI Fashion Tip")

    st.success(
        "Neutral colors like White, Beige, Black and Grey create timeless outfits."
    )

    st.markdown("---")

    st.header("🚀 Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("👚 Add Clothes", use_container_width=True)

    with c2:
        st.button("✨ Generate Outfit", use_container_width=True)

    with c3:
        st.button("📊 View Analytics", use_container_width=True)
# ------------------------------
# PROFILE
# ------------------------------
elif page == "👤 Profile":

    show_profile()

# ------------------------------
# WARDROBE
# ------------------------------
elif page == "👚 My Wardrobe":

    show_wardrobe()
# ------------------------------
# AI
# ------------------------------
elif page == "✨ AI Outfit Generator":
    show_ai_generator()

# ------------------------------
# COLOR
# ------------------------------
elif page == "🎨 Color Studio":

    st.title("🎨 Color Studio")

    st.write("Coming Soon...")

# ------------------------------
# HAIR
# ------------------------------
elif page == "💇 Hair Studio":

    st.title("💇 Hair Studio")

    st.write("Coming Soon...")

# ------------------------------
# ANALYTICS
# ------------------------------
elif page == "📊 Closet Analytics":

    st.title("📊 Closet Analytics")

    st.write("Coming Soon...")

# ------------------------------
# SAVED
# ------------------------------
elif page == "❤️ Saved Looks":

    st.title("❤️ Saved Looks")

    st.write("Coming Soon...")

# ------------------------------
# SETTINGS
# ------------------------------
elif page == "⚙ Settings":

    st.title("⚙ Settings")

    st.write("Coming Soon...")