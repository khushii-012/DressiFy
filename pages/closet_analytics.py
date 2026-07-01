import streamlit as st
import pandas as pd
from collections import Counter
import database

database.initialize_database()
user = database.get_or_create_user()
user_id = user["user_id"]

def main():
    st.set_page_config(
        page_title="DressiFy - Closet Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 Closet Analytics")

    wardrobe = database.get_wardrobe(user_id)
    if not wardrobe:
        st.info("Your wardrobe is empty. Add items in the main app to see analytics.")
        return

    # Convert wardrobe to DataFrame
    df = pd.DataFrame(wardrobe)

    st.subheader("Items by Category")
    if "item_type" in df.columns:
        cat_counts = df["item_type"].value_counts()
        st.bar_chart(cat_counts)
    else:
        st.write("No item_type info in wardrobe table.")

    st.subheader("Most Worn Items (based on saved outfits)")
    history = database.get_outfit_history(user_id, limit=200)
    usage_counter = Counter()

    for rec in history:
        items = rec.get("items", {})
        # items is already a dict like {"top": "White tee", "bottom": "Blue jeans"}
        for item_name in items.values():
            usage_counter[item_name] += 1

    if usage_counter:
        usage_df = pd.DataFrame(
            [{"item": k, "uses": v} for k, v in usage_counter.items()]
        ).sort_values("uses", ascending=False)
        st.table(usage_df.head(15))
    else:
        st.info("No saved outfits yet. Save looks to see wear stats.")

if __name__ == "__main__":
    main()