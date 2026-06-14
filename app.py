import streamlit as st
import pandas as pd
import os
import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(page_title="DressiFy AI ML", layout="centered")

st.title("👗 DressiFy AI — Machine Learning Mode")

# -------------------------
# MEMORY FILES
# -------------------------
DATA_FILE = "fashion_data.csv"
FEEDBACK_FILE = "user_feedback.json"

# -------------------------
# CREATE INITIAL TRAINING DATA (if not exists)
# -------------------------
if not os.path.exists(DATA_FILE):
    data = pd.DataFrame({
        "style": [0,1,2,0,1,2,0,1],
        "weather": [0,1,2,2,1,0,1,2],
        "occasion": [0,1,2,1,0,2,1,0],
        "label": [0,1,2,1,0,2,1,0]
    })
    data.to_csv(DATA_FILE, index=False)

# -------------------------
# LOAD DATA
# -------------------------
data = pd.read_csv(DATA_FILE)

X = data[["style", "weather", "occasion"]]
y = data["label"]

model = DecisionTreeClassifier()
model.fit(X, y)

# -------------------------
# ENCODING
# -------------------------
style_map = {"Casual":0, "Trendy":1, "Formal":2}
weather_map = {"Sunny":0, "Rainy":1, "Cold":2}
occasion_map = {"Casual":0, "Party":1, "Formal":2}

outfit_map = {
    0: "👕 Casual Outfit (T-shirt + Jeans + Sneakers)",
    1: "✨ Trendy Outfit (Stylish shirt + Slim jeans)",
    2: "👔 Formal Outfit (Shirt + Trousers + Shoes)"
}

# -------------------------
# USER INPUT
# -------------------------
style = st.selectbox("Style", list(style_map.keys()))
weather = st.selectbox("Weather", list(weather_map.keys()))
occasion = st.selectbox("Occasion", list(occasion_map.keys()))

# -------------------------
# PREDICT FUNCTION
# -------------------------
def predict_outfit():
    input_data = [[
        style_map[style],
        weather_map[weather],
        occasion_map[occasion]
    ]]

    pred = model.predict(input_data)[0]
    return outfit_map[pred], pred

# -------------------------
# LOAD FEEDBACK
# -------------------------


FEEDBACK_FILE = "user_feedback.json"

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []

    try:
        with open(FEEDBACK_FILE, "r") as f:
            data = f.read().strip()
            if data == "":
                return []
            return json.loads(data)
    except json.JSONDecodeError:
        return []
    except Exception:
        return []

def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f)

feedback_data = load_feedback()

# -------------------------
# PREDICTION BUTTON
# -------------------------
if st.button("🤖 Get AI Outfit Prediction"):
    outfit, label = predict_outfit()

    st.subheader("👗 Recommended Outfit")
    st.success(outfit)

    st.session_state["last_input"] = [
        style_map[style],
        weather_map[weather],
        occasion_map[occasion],
        label
    ]

# -------------------------
# FEEDBACK SYSTEM
# -------------------------
if "last_input" in st.session_state:

    st.write("Did you like this outfit?")

    col1, col2 = st.columns(2)

    if col1.button("👍 Yes"):
        feedback_data.append({
            "input": st.session_state["last_input"],
            "liked": 1
        })
        

def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    return o

with open(FEEDBACK_FILE, "w") as f:
    json.dump(feedback_data, f, default=convert)
    st.success("Great! Model will learn your preference 🧠")

    if col2.button("👎 No"):
        feedback_data.append({
            "input": st.session_state["last_input"],
            "liked": 0
        })
        json.dump(feedback_data, open(FEEDBACK_FILE, "w"))
        st.info("Got it! Improving recommendations...")

# -------------------------
# SHOW LEARNING DATA
# -------------------------
st.markdown("---")
st.subheader("🧠 Learning Status")

st.write(f"Training samples: {len(data)}")
st.write(f"User feedback entries: {len(feedback_data)}")