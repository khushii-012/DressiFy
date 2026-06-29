import streamlit as st


def show_stats():

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.markdown("""
        <div class="dashboard-card">
        <h2>👗</h2>
        <h1>0</h1>
        <p>Wardrobe</p>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="dashboard-card">
        <h2>✨</h2>
        <h1>0</h1>
        <p>AI Looks</p>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="dashboard-card">
        <h2>❤️</h2>
        <h1>0</h1>
        <p>Favorites</p>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="dashboard-card">
        <h2>🎨</h2>
        <h1>10</h1>
        <p>Styles</p>
        </div>
        """,unsafe_allow_html=True)