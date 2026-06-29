import streamlit as st
import google.generativeai as genai
import os
import json
import database
from recommendation_engine import RecommendationEngine

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="DressiFy AI",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# THEME CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

  :root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --card: #1a1a26;
    --border: #2a2a3d;
    --accent: #c9a96e;
    --accent2: #e8c4a0;
    --text: #f0ede8;
    --muted: #8a8a9a;
    --pink: #d4a0b5;
    --purple: #9b87b8;
    --green: #7ab5a0;
  }

  html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
  }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0.5rem !important; max-width: 1300px; }

  /* HERO */
  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #c9a96e, #e8c4a0, #d4a0b5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    letter-spacing: -1px;
    margin: 0;
  }
  .hero-sub {
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    margin-top: 4px;
  }
  .fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 16px 0 20px 0;
    opacity: 0.35;
  }

  /* SIDEBAR */
  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span { color: var(--text) !important; }

  .sb-section {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
  }
  .sb-title {
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 700;
    margin-bottom: 10px;
    font-family: 'Inter', sans-serif;
  }

  /* INPUTS */
  .stSelectbox > div > div,
  .stMultiSelect > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
  }
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
  }

  /* BUTTONS */
  .stButton > button {
    background: linear-gradient(135deg, #c9a96e, #b8935a) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(201,169,110,0.35) !important;
  }

  /* CARDS */
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
  }
  .card-accent::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c9a96e, #d4a0b5, #9b87b8);
  }
  .card-title {
    font-family: 'Playfair Display', serif;
    color: var(--accent);
    font-size: 1.1rem;
    margin-bottom: 14px;
    font-weight: 700;
  }

  /* OUTFIT ITEMS */
  .outfit-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 11px 14px;
    background: rgba(255,255,255,0.025);
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid var(--border);
    transition: border-color 0.2s;
  }
  .outfit-row:hover { border-color: rgba(201,169,110,0.4); }
  .outfit-row.from-wardrobe { border-color: rgba(122,181,160,0.5); }
  .outfit-emoji { font-size: 1.6rem; min-width: 32px; }
  .outfit-label { font-size: 0.65rem; color: var(--accent); letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
  .outfit-name { font-size: 0.95rem; color: var(--text); font-weight: 500; margin-top: 1px; }
  .outfit-desc { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }
  .source-badge {
    margin-left: auto;
    font-size: 0.62rem;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
    white-space: nowrap;
  }
  .badge-wardrobe { background: rgba(122,181,160,0.15); color: var(--green); border: 1px solid rgba(122,181,160,0.3); }
  .badge-catalogue { background: rgba(201,169,110,0.1); color: var(--accent); border: 1px solid rgba(201,169,110,0.25); }

  /* WHY CARD */
  .why-card {
    background: linear-gradient(135deg, rgba(201,169,110,0.07), rgba(212,160,181,0.07));
    border: 1px solid rgba(201,169,110,0.25);
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 12px;
  }
  .why-text { color: var(--text); font-size: 0.9rem; line-height: 1.8; }

  /* WARDROBE */
  .w-group-title {
    font-size: 0.68rem; color: var(--accent);
    letter-spacing: 2px; text-transform: uppercase;
    font-weight: 700; margin: 14px 0 6px 0;
  }
  .w-item-row {
    display: flex; align-items: center; gap: 10px;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 10px; padding: 9px 12px; margin-bottom: 6px;
  }
  .w-item-name { font-size: 0.88rem; color: var(--text); }
  .w-item-meta { font-size: 0.75rem; color: var(--muted); }

  /* HISTORY */
  .hist-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
  }
  .hist-title { font-size: 0.82rem; color: var(--accent); font-weight: 600; margin-bottom: 6px; }
  .hist-items { font-size: 0.8rem; color: var(--muted); line-height: 1.8; }

  /* TAGS */
  .tag {
    display: inline-block;
    background: rgba(201,169,110,0.1);
    border: 1px solid rgba(201,169,110,0.3);
    color: var(--accent);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    margin: 2px;
    font-weight: 500;
  }

  /* TABS */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-bottom: 2px solid transparent !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.8px !important;
    padding: 10px 20px !important;
  }
  .stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
  }

  /* RATING STARS */
  .stars { font-size: 1.3rem; cursor: pointer; }

  /* DATAFRAME */
  [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# INIT DB + ENGINE
# ─────────────────────────────────────────
database.initialize_database()
engine = RecommendationEngine()
user = database.get_or_create_user()
user_id = user["user_id"]

# ─────────────────────────────────────────
# GEMINI
# ─────────────────────────────────────────
def gemini_explain(gender, age, body_type, skin_tone, occasion, weather,
                   preferred_fit, fav_colors, outfit_items):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except:
            pass
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        items_text = "\n".join([f"- {v['type'].upper()}: {v['item']}" for v in outfit_items.values()])
        prompt = f"""You are DressiFy, an AI fashion stylist. The user profile:
- Gender: {gender}, Age: {age}, Body Type: {body_type}, Skin Tone: {skin_tone}
- Occasion: {occasion}, Weather: {weather}, Preferred Fit: {preferred_fit}
- Favorite color families: {', '.join(fav_colors) if fav_colors else 'Any'}

Recommended outfit:
{items_text}

Write 3-4 confident, warm sentences explaining WHY this outfit works for this exact person.
Cover: how the colors suit their skin tone, how the fit flatters their body type, why it is perfect for the occasion and weather.
Be specific, fashion-forward, and encouraging. Plain text only — no asterisks or hashtags."""
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return None

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "outfit_result" not in st.session_state:
    st.session_state.outfit_result = None
if "saved_outfit_id" not in st.session_state:
    st.session_state.saved_outfit_id = None

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown('<div class="hero-title">DressiFy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">✦ Your Personal AI Fashion Stylist ✦</div>', unsafe_allow_html=True)
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR — PROFILE
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Playfair Display,serif; color:#c9a96e; font-size:1.15rem; font-weight:700; margin-bottom:14px;">👤 Style Profile</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="sb-section">', unsafe_allow_html=True)
        st.markdown('<div class="sb-title">Personal Info</div>', unsafe_allow_html=True)
        name = st.text_input("Your Name", value=user.get("name","User"), label_visibility="collapsed",
                             placeholder="Your Name")
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        age = st.slider("Age", 13, 60, int(user.get("age", 20)))
        body_type = st.selectbox("Body Type", ["All", "Hourglass", "Pear", "Apple", "Rectangle", "Inverted Triangle"])
        skin_tone = st.selectbox("Skin Tone", ["All", "Fair", "Wheatish", "Medium", "Dark"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-section">', unsafe_allow_html=True)
        st.markdown('<div class="sb-title">Style Preferences</div>', unsafe_allow_html=True)
        preferred_fit = st.selectbox("Preferred Fit", ["Regular", "Oversized", "Slim"])
        fav_colors = st.multiselect("Favourite Color Families",
            ["Neutral", "Dark", "Warm", "Cool", "Pastel", "Earthy", "Pink", "Multi"],
            default=["Neutral", "Dark"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-section">', unsafe_allow_html=True)
        st.markdown('<div class="sb-title">Today\'s Context</div>', unsafe_allow_html=True)
        occasion = st.selectbox("Occasion", [
            "College", "Office", "Interview", "Wedding", "Party", "Date",
            "Casual Outing", "Gym", "Airport Look", "Vacation", "Festival", "Traditional Function"
        ])
        weather = st.selectbox("Weather", ["Sunny", "Rainy", "Winter", "Humid", "Windy"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("💾 Save Profile"):
        database.update_user(user_id, name=name, age=age, gender=gender,
                             skin_tone=skin_tone, body_type=body_type,
                             preferred_fit=preferred_fit,
                             fav_colors=json.dumps(fav_colors),
                             style_pref="Casual")
        st.success("Profile saved!")

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "✨  AI Outfit",
    "👚  My Wardrobe",
    "📜  Outfit History",
    "📊  Catalogue"
])

# ══════════════════════════════════════════
# TAB 1 — AI OUTFIT GENERATOR
# ══════════════════════════════════════════
with tab1:
    col_ctrl, col_out = st.columns([1, 1.6], gap="large")

    with col_ctrl:
        st.markdown("### Generate Your Look")

        use_wardrobe = st.toggle("🧥 Use my wardrobe items", value=False,
            help="Toggle ON to style outfits from your own clothes in the Wardrobe tab")

        wardrobe_count = len(database.get_wardrobe(user_id))
        if use_wardrobe and wardrobe_count == 0:
            st.warning("⚠️ Wardrobe is empty — add items in the Wardrobe tab first.")

        gen_btn = st.button("✨ Generate AI Look", type="primary")

        # Context summary
        st.markdown('<div class="card card-accent" style="margin-top:14px">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="font-size:0.8rem; margin-bottom:8px;">YOUR CONTEXT</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="tag">{gender}</span>'
            f'<span class="tag">Age {age}</span>'
            f'<span class="tag">{body_type}</span>'
            f'<span class="tag">{skin_tone} Skin</span>'
            f'<span class="tag">{occasion}</span>'
            f'<span class="tag">{weather}</span>'
            f'<span class="tag">{preferred_fit} Fit</span>',
            unsafe_allow_html=True
        )
        if fav_colors:
            st.markdown(
                '<div style="margin-top:6px">'
                + ''.join(f'<span class="tag">{c}</span>' for c in fav_colors)
                + '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        if wardrobe_count > 0:
            st.markdown(f'<div style="color:#7ab5a0; font-size:0.78rem; margin-top:4px;">🧥 {wardrobe_count} items in your wardrobe</div>', unsafe_allow_html=True)

    with col_out:
        if gen_btn:
            with st.spinner("Styling your look..."):
                result = engine.generate_outfit(
                    user_id=user_id,
                    gender=gender, age=age, body_type=body_type,
                    skin_tone=skin_tone, occasion=occasion, weather=weather,
                    preferred_fit=preferred_fit, fav_colors=fav_colors,
                    use_wardrobe=use_wardrobe
                )

                # Gemini explanation
                explanation = gemini_explain(
                    gender, age, body_type, skin_tone, occasion, weather,
                    preferred_fit, fav_colors, result["outfit"]
                )
                if not explanation:
                    explanation = (
                        f"This outfit is curated for {occasion.lower()} in {weather.lower()} weather. "
                        f"The colour palette complements your {skin_tone.lower()} skin tone beautifully, "
                        f"while the {preferred_fit.lower()} fit enhances your natural silhouette. "
                        f"Every piece is chosen to keep you stylish and comfortable all day."
                    )
                result["explanation"] = explanation
                st.session_state.outfit_result = result

        if st.session_state.outfit_result:
            res = st.session_state.outfit_result
            outfit = res["outfit"]

            st.markdown("### ✨ Today's Complete Look")
            st.markdown('<div class="card card-accent">', unsafe_allow_html=True)

            for cat, details in outfit.items():
                badge_cls = "badge-wardrobe" if details["source"] == "wardrobe" else "badge-catalogue"
                badge_label = "👚 Wardrobe" if details["source"] == "wardrobe" else "✦ AI Pick"
                desc_html = f'<div class="outfit-desc">{details["description"]}</div>' if details.get("description") else ""
                row_cls = "outfit-row from-wardrobe" if details["source"] == "wardrobe" else "outfit-row"
                st.markdown(f"""
                <div class="{row_cls}">
                  <span class="outfit-emoji">{details['emoji']}</span>
                  <div style="flex:1">
                    <div class="outfit-label">{cat.upper()}</div>
                    <div class="outfit-name">{details['item']}</div>
                    {desc_html}
                  </div>
                  <span class="source-badge {badge_cls}">{badge_label}</span>
                </div>""", unsafe_allow_html=True)

            # Hairstyle
            hair = res["hair_options"][0]
            st.markdown(f"""
            <div class="outfit-row">
              <span class="outfit-emoji">{hair[0]}</span>
              <div style="flex:1">
                <div class="outfit-label">HAIRSTYLE</div>
                <div class="outfit-name">{hair[1]}</div>
                <div class="outfit-desc">{hair[2]}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            if len(res["hair_options"]) > 1:
                alt = res["hair_options"][1]
                st.markdown(f'<div style="color:#8a8a9a; font-size:0.78rem; margin:6px 0 2px 6px;">Alternate: <span style="color:#c9a96e; font-weight:600;">{alt[1]}</span> — {alt[2]}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Why card
            st.markdown(f"""
            <div class="why-card">
              <div style="color:#c9a96e; font-family:Playfair Display,serif; font-size:1rem; margin-bottom:8px;">🎨 Why This Works For You</div>
              <div class="why-text">{res['explanation']}</div>
            </div>""", unsafe_allow_html=True)

            # Save outfit
            st.markdown("")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.button("💾 Save This Outfit"):
                    oid = database.save_outfit(
                        user_id=user_id,
                        occasion=res["occasion"],
                        weather=res["weather"],
                        items_dict={k: v["item"] for k, v in outfit.items()},
                        explanation=res["explanation"]
                    )
                    st.session_state.saved_outfit_id = oid
                    st.success(f"Outfit saved! ✓")
            with col_s2:
                if st.button("🔁 Generate Another"):
                    st.session_state.outfit_result = None
                    st.rerun()


# ══════════════════════════════════════════
# TAB 2 — WARDROBE
# ══════════════════════════════════════════
with tab2:
    st.markdown("### 🧥 My Wardrobe")
    st.markdown('<div style="color:#8a8a9a; font-size:0.83rem; margin-bottom:18px">Add your real clothes. Toggle wardrobe mode in the AI tab to get looks from what you own.</div>', unsafe_allow_html=True)

    col_add, col_view = st.columns([1, 1.5], gap="large")

    with col_add:
        st.markdown("#### ➕ Add New Item")

        TYPE_OPTIONS = ["top", "bottom", "outerwear", "shoes", "accessory", "dress", "traditional"]
        w_type = st.selectbox("Category", TYPE_OPTIONS)

        # Show catalogue suggestions for that type
        from recommendation_engine import RecommendationEngine as RE
        _e = engine
        if not _e.df.empty:
            suggestions = _e.df[_e.df["type"] == w_type]["item"].tolist()
            w_from_cat = st.selectbox("Pick from catalogue", ["-- Type your own below --"] + suggestions)
        else:
            w_from_cat = "-- Type your own below --"

        w_name = st.text_input("Item Name", placeholder="e.g. White Oversized Graphic Tee")
        if w_from_cat != "-- Type your own below --" and not w_name:
            w_name = w_from_cat

        w_color = st.text_input("Color", placeholder="e.g. White, Navy Blue")
        w_notes = st.text_input("Notes (optional)", placeholder="e.g. Brand new, favourite")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("➕ Add Item"):
                final_name = w_name.strip() or w_from_cat
                if final_name and final_name != "-- Type your own below --":
                    database.add_wardrobe_item(user_id, w_type, final_name, w_color, "", w_notes)
                    st.success(f"✓ Added: {final_name}")
                    st.rerun()
                else:
                    st.error("Enter an item name.")
        with col_b:
            if st.button("🗑️ Clear All"):
                conn = database.get_connection()
                conn.execute("DELETE FROM wardrobe WHERE user_id=?", (user_id,))
                conn.commit()
                conn.close()
                st.rerun()

    with col_view:
        wardrobe = database.get_wardrobe(user_id)
        st.markdown(f"#### My Closet ({len(wardrobe)} items)")

        if not wardrobe:
            st.markdown('<div style="color:#8a8a9a; text-align:center; padding:40px 0">Wardrobe is empty.<br>Add some clothes to get started! 👗</div>', unsafe_allow_html=True)
        else:
            type_emojis = {"top":"👕","bottom":"👖","shoes":"👟","accessory":"💍",
                           "outerwear":"🧥","dress":"👗","traditional":"🥻"}
            # Group
            groups = {}
            for item in wardrobe:
                t = item["item_type"]
                groups.setdefault(t, []).append(item)

            for t, items in groups.items():
                emoji = type_emojis.get(t, "🏷️")
                st.markdown(f'<div class="w-group-title">{emoji} {t.upper()}S ({len(items)})</div>', unsafe_allow_html=True)
                for item in items:
                    col_i, col_d = st.columns([6, 1])
                    with col_i:
                        meta = f"{item['color']}" if item.get('color') else ""
                        if item.get('notes'):
                            meta += f" · {item['notes']}"
                        st.markdown(f"""
                        <div class="w-item-row">
                          <span>✓</span>
                          <div>
                            <div class="w-item-name">{item['item_name']}</div>
                            {f'<div class="w-item-meta">{meta}</div>' if meta else ''}
                          </div>
                        </div>""", unsafe_allow_html=True)
                    with col_d:
                        if st.button("✕", key=f"del_{item['item_id']}"):
                            database.delete_wardrobe_item(item["item_id"])
                            st.rerun()


# ══════════════════════════════════════════
# TAB 3 — OUTFIT HISTORY
# ══════════════════════════════════════════
with tab3:
    st.markdown("### 📜 Outfit History")
    history = database.get_outfit_history(user_id, limit=20)

    if not history:
        st.markdown('<div style="color:#8a8a9a; text-align:center; padding:50px 0">No saved outfits yet.<br>Generate and save your first look! ✨</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color:#8a8a9a; font-size:0.82rem; margin-bottom:16px">{len(history)} saved outfits</div>', unsafe_allow_html=True)
        for outfit_rec in history:
            items = outfit_rec.get("items", {})
            items_text = " · ".join(f"{k}: {v}" for k, v in items.items()) if items else "—"
            stars = "⭐" * outfit_rec.get("rating", 0) if outfit_rec.get("rating") else ""
            st.markdown(f"""
            <div class="hist-card">
              <div class="hist-title">{outfit_rec['occasion']} · {outfit_rec['weather']} {stars}</div>
              <div class="hist-items">{items_text}</div>
              <div style="color:#8a8a9a; font-size:0.72rem; margin-top:6px;">{outfit_rec.get('created_at','')}</div>
            </div>""", unsafe_allow_html=True)

            # Rating
            col_r = st.columns(5)
            for i, c in enumerate(col_r):
                with c:
                    if st.button(f"{'⭐' * (i+1)}", key=f"rate_{outfit_rec['outfit_id']}_{i}"):
                        database.rate_outfit(outfit_rec["outfit_id"], i+1)
                        st.rerun()


# ══════════════════════════════════════════
# TAB 4 — CATALOGUE
# ══════════════════════════════════════════
with tab4:
    st.markdown("### 📊 Fashion Catalogue")

    if engine.df.empty:
        st.error("fashion_items.csv not found!")
    else:
        st.markdown(f'<div style="color:#8a8a9a; font-size:0.83rem; margin-bottom:14px">{len(engine.df)} items in the DressiFy database</div>', unsafe_allow_html=True)

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            cat_f = st.selectbox("Type", ["All"] + sorted(engine.df["type"].unique().tolist()))
        with col_f2:
            gen_f = st.selectbox("Gender", ["All", "Female", "Male"])
        with col_f3:
            occ_f = st.selectbox("Occasion", ["All"] + sorted(engine.df["occasion"].unique().tolist()))

        filtered = engine.df.copy()
        if cat_f != "All":
            filtered = filtered[filtered["type"] == cat_f]
        if gen_f != "All":
            filtered = filtered[filtered["gender"] == gen_f]
        if occ_f != "All":
            filtered = filtered[filtered["occasion"] == occ_f]

        st.markdown(f'<span class="tag">{len(filtered)} results</span>', unsafe_allow_html=True)
        st.markdown("")

        display = filtered[["type","item","gender","style","occasion","weather","body_type","description"]].copy()
        display.columns = ["Type","Item","Gender","Style","Occasion","Weather","Body Type","Description"]
        st.dataframe(display, use_container_width=True, height=520, hide_index=True)