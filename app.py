import streamlit as st
import google.generativeai as genai
import os, json, random
from datetime import datetime, date
import database
from recommendation_engine import RecommendationEngine

st.set_page_config(
    page_title="DressiFy AI ✨",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STREAMLIT-CLOUD-SAFE CSS ──────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* Safe background override */
.stApp { background-color: #f7f4f0 !important; }
.stApp > div { background-color: #f7f4f0 !important; }

/* Sidebar */
[data-testid="stSidebar"] > div:first-child {
  background-color: #ffffff !important;
  border-right: 1px solid #ede9e3 !important;
}

/* Hide footer/menu */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Block container */
.block-container {
  padding-top: 1rem !important;
  padding-bottom: 2rem !important;
  max-width: 1280px !important;
}

/* Inputs */
.stSelectbox > div > div > div {
  background-color: #ffffff !important;
  border: 1.5px solid #ede9e3 !important;
  border-radius: 10px !important;
}
.stTextInput > div > div > input {
  background-color: #ffffff !important;
  border: 1.5px solid #ede9e3 !important;
  border-radius: 10px !important;
  color: #2c2018 !important;
}
.stNumberInput > div > div > input {
  background-color: #ffffff !important;
  border: 1.5px solid #ede9e3 !important;
  border-radius: 10px !important;
}
.stMultiSelect > div > div {
  background-color: #ffffff !important;
  border: 1.5px solid #ede9e3 !important;
  border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
  background-color: #1a1410 !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  padding: 0.5rem 1rem !important;
  width: 100% !important;
  transition: all 0.2s !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover {
  background-color: #c9956e !important;
  transform: translateY(-1px) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background-color: #ffffff !important;
  border-bottom: 2px solid #ede9e3 !important;
  border-radius: 12px 12px 0 0 !important;
  padding: 0 8px !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: #a89880 !important;
  border-bottom: 2px solid transparent !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
  padding: 12px 20px !important;
  margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
  color: #1a1410 !important;
  border-bottom-color: #c9956e !important;
}

/* ── CUSTOM HTML COMPONENTS ── */
.df-header {
  background: linear-gradient(135deg, #1a1410 0%, #2d2018 100%);
  border-radius: 18px;
  padding: 26px 30px;
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}
.df-header::after {
  content: '';
  position: absolute;
  top: -40px; right: -20px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(201,149,110,0.2), transparent 70%);
  border-radius: 50%;
}
.df-logo {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 900;
  background: linear-gradient(135deg, #c9956e, #e8b89a, #d4a0b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.1;
}
.df-sub {
  color: rgba(255,255,255,0.45);
  font-size: 0.72rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 5px;
  font-family: 'DM Sans', sans-serif;
}
.df-pills {
  display: flex;
  gap: 7px;
  flex-wrap: wrap;
  justify-content: flex-end;
  position: relative;
  z-index: 1;
}
.df-pill {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 20px;
  padding: 5px 13px;
  font-size: 0.7rem;
  color: rgba(255,255,255,0.75);
  font-family: 'DM Sans', sans-serif;
}

/* Sidebar styles */
.sb-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a1410;
  margin-bottom: 2px;
}
.sb-sub { font-size: 0.7rem; color: #a89880; margin-bottom: 14px; }
.sb-label {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #c9956e;
  margin: 12px 0 5px 0;
}
.sb-divider {
  height: 1px;
  background: linear-gradient(90deg, #c9956e44, #ede9e3, transparent);
  margin: 12px 0;
}

/* Section titles */
.sec-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #1a1410;
  margin-bottom: 3px;
}
.sec-sub { font-size: 0.78rem; color: #a89880; margin-bottom: 18px; }

/* White cards */
.df-card {
  background: #ffffff;
  border: 1.5px solid #ede9e3;
  border-radius: 18px;
  padding: 20px;
  margin-bottom: 14px;
  box-shadow: 0 2px 12px rgba(44,32,24,0.06);
  position: relative;
  overflow: hidden;
}
.df-card-accent::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #c9956e, #d4a0b5, #9b87b8);
  border-radius: 18px 18px 0 0;
}
.df-card-title {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 700;
  color: #1a1410;
  margin-bottom: 14px;
}

/* Context chips */
.chip {
  display: inline-block;
  background: rgba(201,149,110,0.1);
  border: 1px solid rgba(201,149,110,0.3);
  color: #c9956e;
  border-radius: 20px;
  padding: 3px 11px;
  font-size: 0.7rem;
  font-weight: 600;
  margin: 2px;
  font-family: 'DM Sans', sans-serif;
}
.chip-dark {
  display: inline-block;
  background: #1a1410;
  border: 1px solid #1a1410;
  color: white;
  border-radius: 20px;
  padding: 3px 11px;
  font-size: 0.7rem;
  font-weight: 600;
  margin: 2px;
  font-family: 'DM Sans', sans-serif;
}

/* Outfit rows */
.o-row {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fdfbf9;
  border: 1.5px solid #ede9e3;
  border-radius: 12px;
  padding: 11px 14px;
  margin-bottom: 8px;
  transition: all 0.2s;
  font-family: 'DM Sans', sans-serif;
}
.o-row:hover { border-color: #c9956e; box-shadow: 0 2px 10px rgba(201,149,110,0.1); }
.o-row-w { border-color: rgba(122,170,144,0.5) !important; background: rgba(122,170,144,0.04) !important; }
.o-emoji { font-size: 1.55rem; min-width: 30px; text-align: center; }
.o-cat   { font-size: 0.58rem; font-weight: 700; color: #c9956e; letter-spacing: 1.8px; text-transform: uppercase; }
.o-name  { font-size: 0.9rem; font-weight: 600; color: #1a1410; margin-top: 2px; }
.o-desc  { font-size: 0.7rem; color: #a89880; margin-top: 2px; }
.o-badge { margin-left: auto; font-size: 0.6rem; padding: 3px 9px; border-radius: 10px; font-weight: 700; white-space: nowrap; }
.badge-w  { background: rgba(122,170,144,0.15); color: #5a9a7a; border: 1px solid rgba(122,170,144,0.4); }
.badge-ai { background: rgba(201,149,110,0.1); color: #c9956e; border: 1px solid rgba(201,149,110,0.3); }

/* Score ring */
.score-wrap {
  background: #ffffff;
  border: 1.5px solid #ede9e3;
  border-radius: 18px;
  padding: 20px 14px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(44,32,24,0.06);
}
.score-ring {
  width: 96px; height: 96px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
}
.score-inner {
  width: 70px; height: 70px;
  border-radius: 50%;
  background: #fdfbf9;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.score-num  { font-family: 'Playfair Display',serif; font-size: 1.55rem; font-weight: 900; color: #c9956e; line-height: 1; }
.score-pct  { font-size: 0.52rem; color: #a89880; }
.score-conf { font-size: 0.74rem; font-weight: 700; color: #1a1410; margin-bottom: 4px; }
.score-fact { font-size: 0.67rem; color: #7aaa90; padding: 2px 0; text-align: left; }

/* Why card */
.why-card {
  background: linear-gradient(135deg,rgba(201,149,110,0.06),rgba(212,160,181,0.06));
  border: 1px solid rgba(201,149,110,0.2);
  border-left: 3px solid #c9956e;
  border-radius: 0 14px 14px 0;
  padding: 14px 18px;
  margin-top: 12px;
  font-family: 'DM Sans', sans-serif;
}
.why-title { font-weight: 700; color: #c9956e; font-size: 0.88rem; margin-bottom: 6px; }
.why-text  { font-size: 0.84rem; color: #6b5d52; line-height: 1.75; }

/* Pinterest cards */
.p-card {
  background: #ffffff;
  border: 1.5px solid #ede9e3;
  border-radius: 16px;
  padding: 14px 10px;
  text-align: center;
  transition: all 0.22s;
  font-family: 'DM Sans', sans-serif;
  margin-bottom: 8px;
}
.p-card:hover { transform: translateY(-4px); border-color: #c9956e; box-shadow: 0 8px 24px rgba(44,32,24,0.1); }
.p-type  { display: inline-block; font-size: 0.58rem; font-weight: 700; color: #c9956e; letter-spacing: 1.5px; text-transform: uppercase; background: rgba(201,149,110,0.1); border-radius: 6px; padding: 2px 7px; margin-bottom: 7px; }
.p-emoji { font-size: 2.1rem; margin-bottom: 6px; }
.p-name  { font-size: 0.73rem; font-weight: 700; color: #1a1410; line-height: 1.3; }
.p-meta  { font-size: 0.62rem; color: #a89880; margin-top: 4px; display: flex; align-items: center; justify-content: center; gap: 4px; }
.p-dot   { width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.p-worn  { font-size: 0.62rem; color: #7aaa90; margin-top: 3px; }
.p-id    { font-size: 0.56rem; color: #ddd8d0; margin-top: 2px; }

/* Stat cards */
.stat-card {
  background: #ffffff;
  border: 1.5px solid #ede9e3;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(44,32,24,0.05);
  font-family: 'DM Sans', sans-serif;
}
.stat-n { font-family: 'Playfair Display',serif; font-size: 2.1rem; font-weight: 900; color: #c9956e; line-height: 1; }
.stat-l { font-size: 0.65rem; font-weight: 700; color: #a89880; margin-top: 5px; letter-spacing: 1px; text-transform: uppercase; }

/* Bar chart */
.bar-row   { margin-bottom: 10px; }
.bar-label { display: flex; justify-content: space-between; font-size: 0.76rem; color: #6b5d52; margin-bottom: 4px; font-weight: 500; font-family: 'DM Sans',sans-serif; }
.bar-bg    { background: #f0ebe3; border-radius: 6px; height: 8px; overflow: hidden; }
.bar-fg    { height: 8px; border-radius: 6px; }

/* Missing chip */
.miss-chip { background: rgba(201,112,112,0.07); border: 1px solid rgba(201,112,112,0.25); border-radius: 12px; padding: 10px 14px; margin-bottom: 8px; font-family: 'DM Sans',sans-serif; }
.miss-type { font-size: 0.6rem; color: #c97070; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 3px; }
.miss-name { font-size: 0.84rem; font-weight: 700; color: #1a1410; }
.miss-why  { font-size: 0.7rem; color: #a89880; margin-top: 2px; }

/* History */
.hist-card { background: #ffffff; border: 1.5px solid #ede9e3; border-radius: 14px; padding: 16px 18px; margin-bottom: 10px; box-shadow: 0 1px 8px rgba(44,32,24,0.04); font-family: 'DM Sans',sans-serif; }
.hist-card-fav { border-color: #c9956e !important; }
.hist-top  { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.hist-occ  { font-weight: 700; font-size: 0.9rem; color: #1a1410; }
.hist-date { font-size: 0.68rem; color: #a89880; }
.hist-items{ font-size: 0.78rem; color: #6b5d52; line-height: 1.9; }
.hist-score{ display: inline-flex; align-items: center; gap: 5px; background: rgba(201,149,110,0.1); border: 1px solid rgba(201,149,110,0.3); border-radius: 8px; padding: 3px 10px; font-size: 0.7rem; color: #c9956e; font-weight: 700; margin-top: 8px; }

/* Wish */
.wish-card { background: #ffffff; border: 1.5px solid #ede9e3; border-radius: 14px; padding: 14px 16px; margin-bottom: 10px; display: flex; gap: 14px; align-items: center; font-family: 'DM Sans',sans-serif; }
.wish-emoji { font-size: 2rem; }
.wish-name  { font-weight: 700; font-size: 0.9rem; color: #1a1410; }
.wish-brand { font-size: 0.72rem; color: #a89880; }
.wish-price { font-size: 0.9rem; font-weight: 700; color: #c9956e; margin-top: 3px; }

/* Trend */
.trend-card { background: #ffffff; border: 1.5px solid #ede9e3; border-radius: 16px; padding: 18px; margin-bottom: 12px; border-left: 4px solid #c9956e; box-shadow: 0 2px 10px rgba(44,32,24,0.05); font-family: 'DM Sans',sans-serif; }
.trend-season { font-size: 0.62rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
.trend-title  { font-family: 'Playfair Display',serif; font-size: 1rem; font-weight: 700; color: #1a1410; margin-bottom: 4px; }
.trend-sub    { font-size: 0.78rem; color: #a89880; margin-bottom: 10px; }
.trend-tags   { display: flex; flex-wrap: wrap; gap: 5px; }
.trend-tag    { background: #f7f4f0; color: #6b5d52; border-radius: 12px; padding: 3px 10px; font-size: 0.68rem; font-weight: 600; }

/* Cal */
.cal-day { background: #ffffff; border: 1.5px solid #ede9e3; border-radius: 14px; padding: 12px 8px; text-align: center; min-height: 85px; font-family: 'DM Sans',sans-serif; }
.cal-day-today { border-color: #1a1410 !important; border-width: 2px !important; }
.cal-day-outfit { border-color: #e8b89a !important; background: rgba(201,149,110,0.04) !important; }
.cal-dayname { font-size: 0.62rem; color: #a89880; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.cal-date    { font-size: 1rem; font-weight: 700; color: #1a1410; margin: 4px 0; }
.cal-outfit  { font-size: 0.62rem; color: #c9956e; font-weight: 600; line-height: 1.3; }

/* Gallery */
.gallery-label { font-size: 0.75rem; font-weight: 700; color: #1a1410; margin: 14px 0 8px; display: flex; align-items: center; gap: 8px; font-family: 'DM Sans',sans-serif; }
.gallery-count { background: #f0ebe3; color: #a89880; border-radius: 10px; padding: 2px 8px; font-size: 0.68rem; }

.divider { height: 1px; background: linear-gradient(90deg,transparent,#ede9e3,transparent); margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ── INIT ──────────────────────────────────────
database.initialize_database()
engine = RecommendationEngine()
user   = database.get_or_create_user()
UID    = user["user_id"]

TYPE_EMOJI = {"top":"👕","bottom":"👖","shoes":"👟","accessory":"💍",
              "outerwear":"🧥","dress":"👗","traditional":"🥻"}
COLOR_HEX  = {"Neutral":"#b5aca0","Dark":"#3d3530","Warm":"#d4895a",
               "Cool":"#7a9dbf","Pastel":"#e8b4c8","Earthy":"#8b7355",
               "Pink":"#d4a0b5","Multi":"#c9956e"}

for k,v in [("outfit_result",None),("page","today"),("saved_id",None),
             ("cal_outfits",{}),("wishlist",[])]:
    if k not in st.session_state:
        st.session_state[k] = v

def ask_gemini(prompt):
    key = os.environ.get("GEMINI_API_KEY","")
    if not key:
        try: key = st.secrets.get("GEMINI_API_KEY","")
        except: pass
    if not key: return None
    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt).text.strip()
    except: return None

# ── HEADER ────────────────────────────────────
st.markdown("""
<div class="df-header">
  <div>
    <div class="df-logo">👗 DressiFy AI</div>
    <div class="df-sub">✦ Your Personal AI Fashion Stylist ✦</div>
  </div>
  <div class="df-pills">
    <span class="df-pill">✨ AI Scoring</span>
    <span class="df-pill">🧥 Smart Wardrobe</span>
    <span class="df-pill">🎨 Color Analysis</span>
    <span class="df-pill">📊 Analytics</span>
    <span class="df-pill">📅 Planner</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-title">👤 Style Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">Your fashion preferences</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-label">Personal Info</div>', unsafe_allow_html=True)
    name      = st.text_input("Name", value=user.get("name","User"), placeholder="Your name", label_visibility="collapsed")
    gender    = st.selectbox("Gender", ["Female","Male","Other"])
    age       = st.slider("Age", 13, 60, int(user.get("age",20)))
    body_type = st.selectbox("Body Type", ["All","Hourglass","Pear","Apple","Rectangle","Inverted Triangle"])
    skin_tone = st.selectbox("Skin Tone", ["All","Fair","Wheatish","Medium","Dark"])

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Style</div>', unsafe_allow_html=True)
    preferred_fit = st.selectbox("Preferred Fit", ["Regular","Oversized","Slim"])
    fav_colors    = st.multiselect("Fav Colors",
        ["Neutral","Dark","Warm","Cool","Pastel","Earthy","Pink","Multi"],
        default=["Neutral","Warm"])

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Today\'s Context</div>', unsafe_allow_html=True)
    occasion = st.selectbox("Occasion", ["College","Office","Interview","Wedding","Party","Date",
        "Casual Outing","Gym","Airport Look","Vacation","Festival","Traditional Function"])
    weather  = st.selectbox("Weather", ["Sunny","Rainy","Winter","Humid","Windy"])

    if st.button("💾 Save Profile"):
        database.update_user(UID, name=name, age=age, gender=gender,
            skin_tone=skin_tone, body_type=body_type, preferred_fit=preferred_fit,
            fav_colors=json.dumps(fav_colors))
        st.success("Saved! ✓")

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Pages</div>', unsafe_allow_html=True)

    nav_items = [
        ("🪞 Today's Look","today"),("👚 My Wardrobe","wardrobe"),
        ("📊 Analytics","analytics"),("📅 Calendar","calendar"),
        ("❤️ Saved Looks","saved"),("🛍️ Wishlist","wishlist"),("🔥 Trends","trends"),
    ]
    for label,key in nav_items:
        if st.button(label, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

# ════════════════════════════════════════════════
# PAGE: TODAY'S LOOK
# ════════════════════════════════════════════════
if st.session_state.page == "today":
    st.markdown('<div class="sec-title">✨ Today\'s Look</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">AI picks the perfect outfit for your profile, occasion & weather.</div>', unsafe_allow_html=True)

    lc, rc = st.columns([1, 1.8], gap="large")

    with lc:
        use_wardrobe = st.toggle("🧥 Style from my wardrobe", value=False)
        wcount = len(database.get_wardrobe(UID))
        if use_wardrobe and wcount == 0:
            st.warning("Wardrobe empty! Add items in My Wardrobe first.")

        g1, g2 = st.columns(2)
        with g1: gen_btn = st.button("✨ Generate Look", type="primary")
        with g2: regen   = st.button("🔁 Regenerate")

        st.markdown('<div class="df-card df-card-accent" style="margin-top:14px">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#c9956e;margin-bottom:8px;font-family:DM Sans,sans-serif">YOUR CONTEXT</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="chip-dark">{occasion}</span>'
            f'<span class="chip-dark">{weather}</span>'
            f'<span class="chip">{gender}</span>'
            f'<span class="chip">{body_type}</span>'
            f'<span class="chip">{skin_tone} Skin</span>'
            f'<span class="chip">{preferred_fit} Fit</span>',
            unsafe_allow_html=True)
        if fav_colors:
            st.markdown('<div style="margin-top:6px">'+''.join(f'<span class="chip">{c}</span>' for c in fav_colors)+'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if wcount > 0:
            st.markdown(f'<div style="color:#7aaa90;font-size:0.76rem;margin-top:6px;font-family:DM Sans,sans-serif">🧥 {wcount} items in wardrobe</div>', unsafe_allow_html=True)

    with rc:
        if gen_btn or regen:
            with st.spinner("Styling your look..."):
                result = engine.generate_outfit(
                    user_id=UID, gender=gender, age=age, body_type=body_type,
                    skin_tone=skin_tone, occasion=occasion, weather=weather,
                    preferred_fit=preferred_fit, fav_colors=fav_colors,
                    use_wardrobe=use_wardrobe)
                outfit_lines = "\n".join(f"- {k.upper()}: {v['item']}" for k,v in result["outfit"].items())
                expl = ask_gemini(f"DressiFy AI stylist. User: {gender}, {age}y, {body_type}, {skin_tone} skin, {occasion}, {weather}.\nOutfit:\n{outfit_lines}\n2-3 warm sentences why this works. Plain text only.") \
                    or f"Crafted for {occasion.lower()} in {weather.lower()} weather. Colours complement your {skin_tone.lower()} skin tone while the {preferred_fit.lower()} fit enhances your silhouette perfectly."
                result["explanation"] = expl
                st.session_state.outfit_result = result

        if st.session_state.outfit_result:
            res    = st.session_state.outfit_result
            outfit = res["outfit"]
            score  = res.get("ai_score",0)
            conf   = res.get("confidence","Match")

            oc1, oc2 = st.columns([2.2,1])
            with oc1:
                st.markdown('<div class="df-card df-card-accent">', unsafe_allow_html=True)
                st.markdown('<div class="df-card-title">✨ Today\'s Complete Look</div>', unsafe_allow_html=True)
                for cat,det in outfit.items():
                    is_w  = det["source"]=="wardrobe"
                    rcls  = "o-row o-row-w" if is_w else "o-row"
                    badge = '<span class="o-badge badge-w">👚 Closet</span>' if is_w else '<span class="o-badge badge-ai">✦ AI</span>'
                    desc  = f'<div class="o-desc">{det["description"]}</div>' if det.get("description") else ""
                    st.markdown(f"""<div class="{rcls}">
                      <span class="o-emoji">{det['emoji']}</span>
                      <div style="flex:1"><div class="o-cat">{cat.upper()}</div>
                      <div class="o-name">{det['item']}</div>{desc}</div>{badge}</div>""", unsafe_allow_html=True)
                hair = res["hair_options"][0]
                st.markdown(f"""<div class="o-row">
                  <span class="o-emoji">{hair[0]}</span>
                  <div style="flex:1"><div class="o-cat">HAIRSTYLE</div>
                  <div class="o-name">{hair[1]}</div>
                  <div class="o-desc">{hair[2]}</div></div></div>""", unsafe_allow_html=True)
                if len(res["hair_options"])>1:
                    alt=res["hair_options"][1]
                    st.markdown(f'<div style="font-size:0.73rem;color:#a89880;margin:4px 0 2px 6px;font-family:DM Sans,sans-serif">Alt: <b style="color:#c9956e">{alt[1]}</b> — {alt[2]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="why-card"><div class="why-title">🎨 Why This Works For You</div><div class="why-text">{res["explanation"]}</div></div>', unsafe_allow_html=True)

            with oc2:
                ring_c = "#c9956e" if score>=80 else "#9b87b8" if score>=65 else "#7aaa90"
                st.markdown(f"""<div class="score-wrap">
                  <div class="score-ring" style="background:conic-gradient({ring_c} {score*3.6}deg,#f0ebe3 0deg)">
                    <div class="score-inner">
                      <div class="score-num">{score}</div><div class="score-pct">/ 100</div>
                    </div>
                  </div>
                  <div class="score-conf">{conf}</div>
                  <div style="font-size:0.64rem;color:#a89880;margin-bottom:8px;font-family:DM Sans,sans-serif">AI Match Score</div>
                  {''.join(f'<div class="score-fact">✓ {f}</div>' for f in res.get("score_factors",[])[:3])}
                </div>""", unsafe_allow_html=True)

            s1,s2,s3 = st.columns(3)
            with s1:
                if st.button("❤️ Save Look"):
                    oid = database.save_outfit(UID,occasion=res["occasion"],weather=res["weather"],
                        items_dict={k:v["item"] for k,v in outfit.items()},
                        explanation=res["explanation"],ai_score=score,confidence=conf)
                    st.session_state.saved_id=oid; st.success("Saved! ✓")
            with s2:
                if st.button("👗 Mark Worn"):
                    if st.session_state.saved_id:
                        database.log_worn(UID,st.session_state.saved_id,occasion); st.success("Marked!")
                    else: st.info("Save first.")
            with s3:
                if st.button("🗑️ Clear"):
                    st.session_state.outfit_result=None; st.rerun()
        else:
            st.markdown("""<div style="background:linear-gradient(135deg,#f7f4f0,#fdfbf9);
                border:2px dashed #ddd8d0;border-radius:20px;padding:60px 40px;text-align:center;">
              <div style="font-size:4rem;margin-bottom:14px">👗</div>
              <div style="font-family:Playfair Display,serif;font-size:1.25rem;font-weight:700;color:#1a1410;margin-bottom:8px">Ready to get styled?</div>
              <div style="font-size:0.82rem;color:#a89880;font-family:DM Sans,sans-serif">Set your profile in the sidebar and click Generate Look</div>
            </div>""", unsafe_allow_html=True)

    # Wardrobe gallery
    wardrobe = database.get_wardrobe(UID)
    if wardrobe:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Playfair Display,serif;font-size:1rem;font-weight:700;color:#1a1410;margin-bottom:4px">Browse My Closet</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.74rem;color:#a89880;margin-bottom:14px;font-family:DM Sans,sans-serif">Your clothes organised by category</div>', unsafe_allow_html=True)
        tg = {}
        for item in wardrobe:
            tg.setdefault(item["item_type"],[]).append(item)
        for t in ["top","bottom","outerwear","shoes","accessory","dress","traditional"]:
            items = tg.get(t,[])
            if not items: continue
            em = TYPE_EMOJI.get(t,"🏷️")
            st.markdown(f'<div class="gallery-label">{em} {t.capitalize()}s <span class="gallery-count">{len(items)}</span></div>', unsafe_allow_html=True)
            gcols = st.columns(min(len(items),7))
            for i,item in enumerate(items[:7]):
                cf=item.get("color_family","Neutral"); hexc=COLOR_HEX.get(cf,"#b5aca0")
                worn=f"Worn {item['times_worn']}×" if item.get("times_worn",0)>0 else ""
                with gcols[i]:
                    st.markdown(f"""<div class="p-card">
                      <div class="p-emoji">{em}</div>
                      <div class="p-name">{item['item_name'][:16]}</div>
                      <div class="p-meta"><span class="p-dot" style="background:{hexc}"></span>{cf}</div>
                      {f'<div class="p-worn">{worn}</div>' if worn else ''}
                    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# PAGE: WARDROBE
# ════════════════════════════════════════════════
elif st.session_state.page == "wardrobe":
    st.markdown('<div class="sec-title">👚 My Wardrobe</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Your personal closet — add clothes for AI-powered styling.</div>', unsafe_allow_html=True)
    wa,wb = st.columns([1,2.2],gap="large")
    with wa:
        st.markdown("#### ➕ Add Item")
        TYPE_OPTS=["top","bottom","outerwear","shoes","accessory","dress","traditional"]
        w_type=st.selectbox("Category",TYPE_OPTS)
        sug=engine.df[engine.df["type"]==w_type]["item"].tolist() if not engine.df.empty else []
        w_pick=st.selectbox("From catalogue",["— type custom —"]+sug)
        w_name=st.text_input("Item Name",placeholder="e.g. White Oversized Tee")
        if w_pick!="— type custom —" and not w_name: w_name=w_pick
        w_color=st.text_input("Color",placeholder="e.g. White")
        w_cfam=st.selectbox("Color Family",["Neutral","Dark","Warm","Cool","Pastel","Earthy","Pink","Multi"])
        w_notes=st.text_input("Notes",placeholder="Brand, tags...")
        ca,cb=st.columns(2)
        with ca:
            if st.button("➕ Add"):
                fn=w_name.strip() or (w_pick if w_pick!="— type custom —" else "")
                if fn: database.add_wardrobe_item(UID,w_type,fn,w_color,w_cfam,"",w_notes); st.success(f"✓ {fn}"); st.rerun()
                else: st.error("Enter a name")
        with cb:
            if st.button("🗑️ Clear All"):
                conn=database.get_connection(); conn.execute("DELETE FROM wardrobe WHERE user_id=?",(UID,)); conn.commit(); conn.close(); st.rerun()
    with wb:
        wardrobe=database.get_wardrobe(UID)
        wf1,wf2=st.columns(2)
        with wf1: type_f=st.selectbox("Filter",["All"]+["top","bottom","outerwear","shoes","accessory","dress","traditional"],key="wft")
        with wf2: fav_only=st.checkbox("❤️ Favs only")
        wshow=wardrobe
        if type_f!="All": wshow=[w for w in wshow if w["item_type"]==type_f]
        if fav_only: wshow=[w for w in wshow if w.get("is_favourite")]
        st.markdown(f'<div style="font-size:0.74rem;color:#a89880;margin-bottom:12px;font-family:DM Sans,sans-serif">{len(wshow)} items</div>', unsafe_allow_html=True)
        if wshow:
            cols=st.columns(4)
            for i,item in enumerate(wshow):
                em=TYPE_EMOJI.get(item["item_type"],"🏷️"); cf=item.get("color_family","Neutral")
                hexc=COLOR_HEX.get(cf,"#b5aca0"); fav="❤️" if item.get("is_favourite") else "🤍"
                worn=f"Worn {item['times_worn']}×" if item.get("times_worn",0)>0 else "Never worn"
                with cols[i%4]:
                    st.markdown(f"""<div class="p-card">
                      <div class="p-type">{item['item_type']}</div>
                      <div class="p-emoji">{em}</div>
                      <div class="p-name">{item['item_name']}</div>
                      <div class="p-meta"><span class="p-dot" style="background:{hexc}"></span>{item.get('color','') or cf}</div>
                      <div class="p-worn">{worn}</div>
                      <div class="p-id">ID: {item['item_id']}</div>
                      <div style="font-size:0.8rem;margin-top:4px">{fav}</div>
                    </div>""", unsafe_allow_html=True)
            d1,d2=st.columns(2)
            with d1:
                did=st.number_input("Delete ID",min_value=0,step=1,value=0)
                if st.button("✕ Remove") and did: database.delete_wardrobe_item(did); st.rerun()
            with d2:
                fid=st.number_input("Fav ID",min_value=0,step=1,value=0,key="fid")
                if st.button("❤️ Toggle") and fid: database.toggle_wardrobe_favourite(fid); st.rerun()
        else:
            st.markdown('<div style="text-align:center;padding:50px;color:#a89880;font-family:DM Sans,sans-serif">No items yet! 👗</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# PAGE: ANALYTICS
# ════════════════════════════════════════════════
elif st.session_state.page == "analytics":
    st.markdown('<div class="sec-title">📊 Closet Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Smart insights into your wardrobe.</div>', unsafe_allow_html=True)
    wardrobe=database.get_wardrobe(UID); analytics=database.get_wardrobe_analytics(UID)
    missing=engine.find_missing_items(wardrobe,gender); color_data=engine.analyze_colors(wardrobe)
    if analytics["total"]==0:
        st.info("Add clothes to see analytics! 👗")
    else:
        s1,s2,s3,s4=st.columns(4)
        for col,(num,lbl) in zip([s1,s2,s3,s4],[(analytics["total"],"Total Items"),(len(analytics["by_type"]),"Categories"),(sum(1 for w in wardrobe if w.get("is_favourite")),"Favourites"),(sum(1 for w in wardrobe if w.get("times_worn",0)==0),"Never Worn")]):
            with col: st.markdown(f'<div class="stat-card"><div class="stat-n">{num}</div><div class="stat-l">{lbl}</div></div>', unsafe_allow_html=True)
        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        ac1,ac2,ac3=st.columns([1.2,1.2,1],gap="large")
        with ac1:
            st.markdown('<div class="df-card"><div class="df-card-title">By Category</div>', unsafe_allow_html=True)
            mx=max(analytics["by_type"].values()) if analytics["by_type"] else 1
            for t,cnt in sorted(analytics["by_type"].items(),key=lambda x:-x[1]):
                pct=int(cnt/mx*100); em=TYPE_EMOJI.get(t,"🏷️")
                st.markdown(f'<div class="bar-row"><div class="bar-label"><span>{em} {t.capitalize()}s</span><span style="color:#c9956e;font-weight:700">{cnt}</span></div><div class="bar-bg"><div class="bar-fg" style="width:{pct}%;background:linear-gradient(90deg,#c9956e,#d4a0b5)"></div></div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with ac2:
            st.markdown('<div class="df-card"><div class="df-card-title">Colour Distribution</div>', unsafe_allow_html=True)
            if color_data.get("distribution"):
                mx2=max(color_data["distribution"].values())
                for cf,cnt in sorted(color_data["distribution"].items(),key=lambda x:-x[1]):
                    pct=int(cnt/mx2*100); hexc=COLOR_HEX.get(cf,"#888")
                    st.markdown(f'<div class="bar-row"><div class="bar-label"><span style="display:flex;align-items:center;gap:6px"><span style="background:{hexc};width:10px;height:10px;border-radius:50%;display:inline-block"></span>{cf}</span><span style="color:#c9956e;font-weight:700">{cnt}</span></div><div class="bar-bg"><div class="bar-fg" style="width:{pct}%;background:{hexc}"></div></div></div>', unsafe_allow_html=True)
            if color_data.get("missing_colors"):
                st.markdown(f'<div style="font-size:0.72rem;color:#a89880;margin-top:10px;font-family:DM Sans,sans-serif">Missing: {", ".join(color_data["missing_colors"])}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with ac3:
            st.markdown('<div class="df-card"><div class="df-card-title">🔍 Missing Items</div>', unsafe_allow_html=True)
            if not missing: st.markdown('<div style="color:#7aaa90;font-size:0.85rem;font-family:DM Sans,sans-serif">Complete! ✓</div>', unsafe_allow_html=True)
            else:
                for m in missing: st.markdown(f'<div class="miss-chip"><div class="miss-type">{m["type"]}</div><div class="miss-name">+ {m["suggestion"]}</div><div class="miss-why">{m["reason"]}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        mw1,mw2=st.columns(2)
        with mw1:
            st.markdown('<div class="df-card"><div class="df-card-title">🔥 Most Worn</div>', unsafe_allow_html=True)
            mw=[i for i in analytics.get("most_worn",[]) if i["times_worn"]>0]
            if mw:
                for item in mw: st.markdown(f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f0ebe3;font-family:DM Sans,sans-serif"><span style="font-size:0.85rem">{item["item_name"]}</span><span style="color:#c9956e;font-weight:700">{item["times_worn"]}×</span></div>', unsafe_allow_html=True)
            else: st.markdown('<div style="color:#a89880;font-size:0.82rem;font-family:DM Sans,sans-serif">No data yet.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with mw2:
            st.markdown('<div class="df-card"><div class="df-card-title">😴 Never Worn</div>', unsafe_allow_html=True)
            nw=analytics.get("never_worn",[])[:5]
            if nw:
                for item in nw: em=TYPE_EMOJI.get(item["item_type"],"🏷️"); st.markdown(f'<div style="padding:8px 0;border-bottom:1px solid #f0ebe3;font-size:0.85rem;color:#6b5d52;font-family:DM Sans,sans-serif">{em} {item["item_name"]}</div>', unsafe_allow_html=True)
            else: st.markdown('<div style="color:#7aaa90;font-size:0.82rem;font-family:DM Sans,sans-serif">All worn! ✓</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# PAGE: CALENDAR
# ════════════════════════════════════════════════
elif st.session_state.page == "calendar":
    from datetime import timedelta
    st.markdown('<div class="sec-title">📅 Outfit Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Plan outfits for the week.</div>', unsafe_allow_html=True)
    today=date.today(); week_start=today-timedelta(days=today.weekday())
    week_dates=[week_start+timedelta(days=i) for i in range(7)]
    days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    cal_cols=st.columns(7)
    for i,(day,dt) in enumerate(zip(days,week_dates)):
        key=str(dt); has_fit=key in st.session_state.cal_outfits; is_today=dt==today
        preview=st.session_state.cal_outfits.get(key,"")
        cls="cal-day cal-day-today" if is_today else ("cal-day cal-day-outfit" if has_fit else "cal-day")
        with cal_cols[i]:
            st.markdown(f'<div class="{cls}"><div class="cal-dayname">{day}</div><div class="cal-date">{dt.day}</div><div class="cal-outfit">{preview[:22] if preview else ("📍 Today" if is_today else "")}</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    pc1,pc2=st.columns(2)
    with pc1: plan_date=st.date_input("Select Date",value=today)
    with pc2: plan_occ=st.selectbox("Occasion",["College","Office","Party","Date","Casual Outing","Vacation","Gym"])
    if st.button("📅 Generate & Plan"):
        result=engine.generate_outfit(user_id=UID,gender=gender,age=age,body_type=body_type,skin_tone=skin_tone,occasion=plan_occ,weather=weather,preferred_fit=preferred_fit,fav_colors=fav_colors,use_wardrobe=False)
        preview=" · ".join(v["item"] for v in list(result["outfit"].values())[:3])
        st.session_state.cal_outfits[str(plan_date)]=f"{plan_occ}: {preview}"; st.success(f"Planned! ✓")
    if st.session_state.cal_outfits:
        st.markdown("#### Planned Outfits")
        for dt_str,fit in sorted(st.session_state.cal_outfits.items()):
            st.markdown(f'<div class="hist-card"><span style="color:#c9956e;font-weight:700;font-family:DM Sans,sans-serif">{dt_str}</span> — <span style="font-family:DM Sans,sans-serif">{fit}</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# PAGE: SAVED
# ════════════════════════════════════════════════
elif st.session_state.page == "saved":
    st.markdown('<div class="sec-title">❤️ Saved Looks</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Your favourite outfits.</div>', unsafe_allow_html=True)
    history=database.get_outfit_history(UID,limit=40)
    if not history:
        st.markdown('<div style="text-align:center;padding:60px;color:#a89880;font-family:DM Sans,sans-serif">No saved looks yet. Generate and save your first! ✨</div>', unsafe_allow_html=True)
    else:
        hf1,hf2=st.columns(2)
        with hf1: fav_f=st.checkbox("❤️ Favs only")
        with hf2: occ_f=st.selectbox("Filter",["All"]+list({h["occasion"] for h in history}),key="sf")
        hshow=history
        if fav_f: hshow=[h for h in hshow if h.get("is_favourite")]
        if occ_f!="All": hshow=[h for h in hshow if h["occasion"]==occ_f]
        st.markdown(f'<div style="font-size:0.74rem;color:#a89880;margin-bottom:14px;font-family:DM Sans,sans-serif">{len(hshow)} outfits</div>', unsafe_allow_html=True)
        for h in hshow:
            items=h.get("items",{}); items_s=" · ".join(f"{k}: {v}" for k,v in items.items()) if items else "—"
            stars="⭐"*h.get("rating",0) if h.get("rating") else "☆☆☆☆☆"
            fav_icon="❤️" if h.get("is_favourite") else "🤍"
            score_b=f'<div class="hist-score">✨ {h["ai_score"]}% — {h["confidence"]}</div>' if h.get("ai_score") else ""
            card_cls="hist-card hist-card-fav" if h.get("is_favourite") else "hist-card"
            st.markdown(f'<div class="{card_cls}"><div class="hist-top"><div class="hist-occ">{fav_icon} {h["occasion"]} · {h["weather"]}</div><div style="display:flex;align-items:center;gap:8px"><span>{stars}</span><div class="hist-date">{h.get("created_at","")[:10]}</div></div></div><div class="hist-items">{items_s}</div>{score_b}</div>', unsafe_allow_html=True)
            hc1,hc2,hc3=st.columns(3)
            with hc1:
                r=st.select_slider("★",options=[1,2,3,4,5],value=max(1,h.get("rating",1)),key=f"rs_{h['outfit_id']}",label_visibility="collapsed")
                if st.button("⭐ Rate",key=f"rb_{h['outfit_id']}"): database.rate_outfit(h["outfit_id"],r); st.rerun()
            with hc2:
                if st.button("💔 Unfav" if h.get("is_favourite") else "❤️ Fav",key=f"fh_{h['outfit_id']}"): database.toggle_outfit_favourite(h["outfit_id"]); st.rerun()
            with hc3:
                if st.button("👗 Worn",key=f"wh_{h['outfit_id']}"): database.log_worn(UID,h["outfit_id"],h["occasion"]); st.success("Marked!")

# ════════════════════════════════════════════════
# PAGE: WISHLIST
# ════════════════════════════════════════════════
elif st.session_state.page == "wishlist":
    st.markdown('<div class="sec-title">🛍️ Wishlist</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Save items you want to buy.</div>', unsafe_allow_html=True)
    wl1,wl2=st.columns([1,2])
    with wl1:
        st.markdown("#### + Add Item")
        wl_name=st.text_input("Item Name",placeholder="e.g. Nike Air Force 1")
        wl_brand=st.text_input("Brand",placeholder="e.g. Nike")
        wl_price=st.text_input("Price",placeholder="e.g. ₹6,500")
        wl_link=st.text_input("Link",placeholder="https://...")
        wl_type=st.selectbox("Category",["top","bottom","shoes","accessory","outerwear","dress"])
        if st.button("➕ Add to Wishlist"):
            if wl_name:
                st.session_state.wishlist.append({"name":wl_name,"brand":wl_brand,"price":wl_price,"link":wl_link,"type":wl_type,"added":str(date.today())})
                st.success(f"✓ {wl_name}")
    with wl2:
        if not st.session_state.wishlist:
            st.markdown('<div style="text-align:center;padding:50px;color:#a89880;font-family:DM Sans,sans-serif">Wishlist empty. Start adding! 🛍️</div>', unsafe_allow_html=True)
        else:
            for item in st.session_state.wishlist:
                em=TYPE_EMOJI.get(item["type"],"🛍️")
                link_html=f'<a href="{item["link"]}" style="font-size:0.72rem;color:#c9956e;font-family:DM Sans,sans-serif" target="_blank">View →</a>' if item.get("link") else ""
                st.markdown(f'<div class="wish-card"><div class="wish-emoji">{em}</div><div><div class="wish-name">{item["name"]}</div><div class="wish-brand">{item.get("brand","")} · {item.get("added","")}</div><div class="wish-price">{item.get("price","")}</div>{link_html}</div></div>', unsafe_allow_html=True)
            if st.button("🗑️ Clear Wishlist"): st.session_state.wishlist=[]; st.rerun()

# ════════════════════════════════════════════════
# PAGE: TRENDS
# ════════════════════════════════════════════════
elif st.session_state.page == "trends":
    st.markdown('<div class="sec-title">🔥 Fashion Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">What\'s trending — Summer 2026 edition.</div>', unsafe_allow_html=True)
    trends=[
        {"season":"Summer 2026","title":"Linen Everything","sub":"Breathable, elegant, effortless","items":["Linen Shirt","Linen Co-ord","Linen Trousers","Linen Shorts"],"color":"#d4895a"},
        {"season":"Summer 2026","title":"Earth Tones","sub":"Warm, grounded, nature-inspired","items":["Rust Crop Top","Camel Trousers","Terracotta Dress","Olive Jacket"],"color":"#8b7355"},
        {"season":"Summer 2026","title":"Co-ord Sets","sub":"Matching sets are the new power move","items":["Sage Green Set","White Linen Set","Brown Knit Set","Beige Set"],"color":"#7a9dbf"},
        {"season":"Summer 2026","title":"Minimal Silver","sub":"Less is more","items":["Thin Gold Chain","Silver Cuff","Minimal Watch","Hoop Earrings"],"color":"#9b87b8"},
        {"season":"Summer 2026","title":"Wide-Leg Denim","sub":"The 90s are back","items":["Baggy Blue Jeans","Wide-Leg White","Mom Jeans","Barrel Leg"],"color":"#7aaa90"},
        {"season":"Summer 2026","title":"Sporty Luxe","sub":"Gym-to-street looks","items":["Crop Sports Bra","Track Pants","Windbreaker","Chunky Sneakers"],"color":"#c97070"},
    ]
    tc=st.columns(3)
    for i,trend in enumerate(trends):
        with tc[i%3]:
            tags_html = "".join(f'<span class="trend-tag">{item}</span>' for item in trend["items"])
            st.markdown(f'<div class="trend-card" style="border-left-color:{trend["color"]}"><div class="trend-season" style="color:{trend["color"]}">{trend["season"]}</div><div class="trend-title">{trend["title"]}</div><div class="trend-sub">{trend["sub"]}</div><div class="trend-tags">{tags_html}</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    if st.button("🧠 Get AI Trend Advice"):
        wardrobe=database.get_wardrobe(UID)
        w_items=", ".join(w["item_name"] for w in wardrobe[:10]) if wardrobe else "basic wardrobe"
        advice=ask_gemini(f"DressiFy AI: 3 practical Summer 2026 tips for user with: {w_items}. Under 100 words, no markdown.") or "Linen and earth tones dominate Summer 2026. Try a sage green co-ord or camel wide-leg trousers. Minimalist silver jewellery pairs perfectly with neutrals."
        st.markdown(f'<div class="why-card"><div class="why-title">✨ AI Style Advice</div><div class="why-text">{advice}</div></div>', unsafe_allow_html=True)