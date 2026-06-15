import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="DressiFy AI", layout="centered")

st.title("👗 DressiFy AI Fashion Assistant")
st.subheader("Your Smart AI Stylist ✨")
st.markdown("---")

# -------------------------
# LOAD DATASET
# -------------------------
DATA_FILE = "fashion_items.csv"

def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

# -------------------------
# CHECK DATA
# -------------------------
if df.empty:
    st.error("Dataset missing or empty!")
    st.stop()

# -------------------------
# ENCODING MAPS
# -------------------------
gender_map = {"Female": 0, "Male": 1, "Other": 2}
style_map = {"Casual": 0, "Trendy": 1, "Formal": 2}
weather_map = {"Sunny": 0, "Rainy": 1, "Cold": 2}
occasion_map = {"Casual": 0, "Party": 1, "Formal": 2}

# -------------------------
# USER INPUT
# -------------------------
gender = st.selectbox("Gender", list(gender_map.keys()))
age = st.slider("Age", 10, 60, 20)
style = st.selectbox("Style", list(style_map.keys()))
weather = st.selectbox("Weather", list(weather_map.keys()))
occasion = st.selectbox("Occasion", list(occasion_map.keys()))

# convert to numbers
gender_v = gender_map[gender]
style_v = style_map[style]
weather_v = weather_map[weather]
occasion_v = occasion_map[occasion]
age_v = age

# -------------------------
# TRAIN MODEL
# -------------------------
def train_model():
    if len(df) < 5:
        return None

    X = df[["gender", "age", "style", "weather", "occasion"]]
    y = df["category"]

    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

model = train_model()

if model is None:
    st.warning("⚠️ Using fallback AI (not enough training data)")

# -------------------------
# PREDICTION
# -------------------------
def predict_category():
    if model is None:
        # fallback logic
        if occasion_v == 2:
            return "formal"
        if weather_v == 1:
            return "casual"
        return "casual"

    return model.predict([[gender_v, age_v, style_v, weather_v, occasion_v]])[0]

# -------------------------
# ACCESSORIES SYSTEM
# -------------------------
accessories = {
    "casual": ["🕶️ Sunglasses", "⌚ Watch", "🎒 Backpack"],
    "formal": ["⌚ Classic Watch", "💼 Formal Bag", "👞 Shoes Polish Look"],
    "party": ["💎 Jewelry", "🕶️ Stylish Shades", "👜 Clutch Bag"]
}

# -------------------------
# GET OUTFIT
# -------------------------
def get_outfit(category):
    items = df[df["category"] == category]
    if len(items) == 0:
        return items
    return items.sample(min(3, len(items)))

# -------------------------
# MAIN BUTTON
# -------------------------
if st.button("👗 Generate Full AI Look"):

    category = predict_category()

    st.success(f"Recommended Style: {category.upper()}")

    # outfit
    st.subheader("🧥 Outfit Suggestion")

    st.subheader("🧥 Full Outfit Suggestion")

types = ["top", "bottom", "shoes", "accessory"]

for t in types:
    item = df[(df["category"] == category) & (df["type"] == t)]

    if not item.empty:
        row = item.sample(1).iloc[0]
        st.write(f"✔️ {t.upper()}: {row['item']}")
        st.image(row["image"], width=220)

    # accessories
    st.subheader("👜 Accessories & Full Look")

    for item in accessories.get(category, []):
        st.write("➕ " + item)

# -------------------------
# DATA STATUS
# -------------------------
st.markdown("---")
st.subheader("📊 System Status")
st.write("Total items in dataset:", len(df))