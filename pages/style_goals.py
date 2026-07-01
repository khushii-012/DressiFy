import streamlit as st
import json
import database

database.initialize_database()
user = database.get_or_create_user()
user_id = user["user_id"]

GOAL_OPTIONS = [
    "Use more colour",
    "Wear ethnic weekly",
    "Repeat outfits more",
    "Look more professional",
    "Experiment with accessories",
]

def main():
    st.set_page_config(
        page_title="DressiFy - Style Goals",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🎯 Style Goals")

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS style_goals (user_id INTEGER PRIMARY KEY, goals_json TEXT)"
    )
    conn.commit()

    # Load existing goals
    cursor.execute("SELECT goals_json FROM style_goals WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    current_goals = json.loads(row[0]) if row and row[0] else []

    selected_goals = st.multiselect("Choose your goals:", GOAL_OPTIONS, default=current_goals)

    if st.button("Save Goals"):
        goals_json = json.dumps(selected_goals)
        cursor.execute(
            "INSERT OR REPLACE INTO style_goals (user_id, goals_json) VALUES (?, ?)",
            (user_id, goals_json),
        )
        conn.commit()
        st.success("Goals saved!")

    st.subheader("Simple Progress (placeholder)")
    st.write("We will later connect this to analytics (colour usage, ethnic outfits, rewear count).")

    conn.close()

if __name__ == "__main__":
    main()