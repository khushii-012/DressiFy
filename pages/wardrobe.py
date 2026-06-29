import streamlit as st
from database import add_wardrobe_item, get_wardrobe, get_or_create_default_user
from services.wardrobe_service import save_uploaded_image


def show_wardrobe():

    st.title("👚 My Wardrobe")
    st.caption("Manage your personal clothing collection.")

    # ----------------------------
    # Get Current User
    # ----------------------------
    user = get_or_create_default_user()

    if user is None:
        st.warning("⚠ Please create your profile first.")
        return

    st.markdown("---")

    # ----------------------------
    # Add Clothing Form
    # ----------------------------
    with st.expander("➕ Add New Clothing", expanded=True):

        category = st.selectbox(
            "Category",
            [
                "Topwear",
                "Bottomwear",
                "Footwear",
                "Accessories",
                "Outerwear",
                "Ethnic Wear"
            ]
        )

        sub_category = st.text_input("Sub Category")

        item_name = st.text_input("Item Name")

        color = st.selectbox(
            "Color",
            [
                "White",
                "Black",
                "Blue",
                "Grey",
                "Beige",
                "Brown",
                "Pink",
                "Green",
                "Red"
            ]
        )

        style = st.selectbox(
            "Style",
            [
                "Casual",
                "Korean",
                "Old Money",
                "Streetwear",
                "Corporate",
                "Minimalist"
            ]
        )

        season = st.selectbox(
            "Season",
            [
                "Summer",
                "Winter",
                "Monsoon",
                "All Season"
            ]
        )

        occasion = st.selectbox(
            "Occasion",
            [
                "College",
                "Office",
                "Party",
                "Travel",
                "Wedding",
                "Casual"
            ]
        )

        uploaded_image = st.file_uploader(
            "📷 Upload Clothing Image",
            type=["jpg", "jpeg", "png"]
        )

        # ----------------------------
        # Save Clothing
        # ----------------------------
        if st.button("💾 Save Clothing"):

            image_path = save_uploaded_image(uploaded_image)

            clothing = {
                "user_id": user["user_id"],
                "category": category,
                "sub_category": sub_category,
                "item_name": item_name,
                "color": color,
                "style": style,
                "season": season,
                "occasion": occasion,
                "image_path": image_path
            }

            add_wardrobe_item(
             user["user_id"],
             clothing["category"].lower(),
             clothing["sub_category"],
             clothing["color"],
             clothing["style"],
             clothing["image_path"]
)
            st.success("✅ Clothing Added Successfully!")

            st.rerun()

    # ----------------------------
    # Display Wardrobe
    # ----------------------------
    st.markdown("---")
    st.subheader("🧥 Your Collection")

    clothes = get_wardrobe(user["user_id"])

    if len(clothes) == 0:
        st.info("Your wardrobe is empty.")
        return

    for cloth in clothes:

        with st.container(border=True):

            st.markdown(f"### 👕 {cloth['item_name']}")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Category:** {cloth['category']}")
                st.write(f"**Sub Category:** {cloth['sub_category']}")
                st.write(f"**Color:** {cloth['color']}")
                st.write(f"**Style:** {cloth['style']}")
                st.write(f"**Season:** {cloth['season']}")
                st.write(f"**Occasion:** {cloth['occasion']}")

            with col2:
                if cloth["image_path"]:
                    st.image(cloth["image_path"], width=150)
                else:
                    st.info("No Image")

            st.markdown("---")