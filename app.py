import streamlit as st
import google.generativeai as genai
import os, json, random
from datetime import datetime, date
import database
from recommendation_engine import RecommendationEngine

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="DressiFy",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
# CSS — App-Style UI (inspired by closet apps)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600;700&display=swap');

:root {
  --bg:       #f7f4f0;
  --surface:  #ffffff;
  --card:     #fdfbf9;
  --border:   #ede9e3;
  --border2:  #ddd8d0;
  --accent:   #c9956e;
  --accent2:  #e8b89a;
  --dark:     #1a1410;
  --text:     #2c2018;
  --text2:    #6b5d52;
  --muted:    #a89880;
  --pink:     #d4a0b5;
  --green:    #7aaa90;
  --red:      #c97070;
  --shadow:   0 2px 16px rgba(44,32,24,0.08);
  --shadow2:  0 8px 32px rgba(44,32,24,0.12);
}

html, body, [class*="css"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── APP SHELL ── */
.app-shell {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: 56px 1fr;
  height: 100vh;
  overflow: hidden;
  background: var(--bg);
}

/* ── TOP NAV ── */
.top-nav {
  grid-column: 1 / -1;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 16px;
  z-index: 100;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06);
}
.nav-logo {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  font-weight: 900;
  background: linear-gradient(135deg, #c9956e, #d4a0b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  margin-right: 8px;
}
.nav-tab {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--muted);
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  background: none;
  letter-spacing: 0.3px;
}
.nav-tab.active {
  background: var(--dark);
  color: #fff;
}
.nav-tab:hover:not(.active) { background: var(--border); color: var(--text); }

/* ── LEFT CLOSET PANEL ── */
.closet-panel {
  background: var(--surface);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 16px 12px;
}
.closet-title {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 12px;
  padding: 0 4px;
}
.closet-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 14px;
}
.closet-tab {
  flex: 1;
  padding: 7px 0;
  font-size: 0.72rem;
  font-weight: 600;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  background: var(--border);
  color: var(--text2);
  border: none;
  transition: all 0.2s;
}
.closet-tab.active { background: var(--dark); color: #fff; }

/* Closet item tiles (like the photo — small squares) */
.closet-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 12px;
}
.closet-tile {
  aspect-ratio: 1;
  background: var(--card);
  border: 1.5px solid var(--border);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  padding: 6px 4px;
  position: relative;
  overflow: hidden;
}
.closet-tile:hover {
  border-color: var(--accent);
  transform: scale(1.04);
  box-shadow: var(--shadow);
}
.closet-tile.selected {
  border-color: var(--accent);
  background: rgba(201,149,110,0.08);
}
.closet-tile.empty {
  border-style: dashed;
  color: var(--muted);
}
.closet-tile .t-emoji { font-size: 1.5rem; }
.closet-tile .t-name {
  font-size: 0.58rem;
  font-weight: 600;
  color: var(--text2);
  text-align: center;
  margin-top: 3px;
  line-height: 1.2;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 3px;
}
.closet-tile .t-remove {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 14px;
  height: 14px;
  background: var(--red);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.55rem;
  color: white;
  font-weight: 700;
  line-height: 1;
  opacity: 0;
  transition: opacity 0.2s;
}
.closet-tile:hover .t-remove { opacity: 1; }

.closet-section-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text2);
  margin: 10px 0 6px 2px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.closet-section-label span { color: var(--muted); font-weight: 400; }

/* ── CENTER / RIGHT PANEL ── */
.main-panel {
  overflow-y: auto;
  background: var(--bg);
  display: flex;
  flex-direction: column;
}

/* ── TODAY'S LOOK AREA (top of center) ── */
.look-area {
  background: linear-gradient(160deg, #f2ede7 0%, #faf8f5 100%);
  border-bottom: 1px solid var(--border);
  padding: 20px 24px;
  display: flex;
  gap: 20px;
  align-items: flex-start;
  min-height: 280px;
}

/* Avatar silhouette card */
.avatar-card {
  width: 160px;
  flex-shrink: 0;
  background: rgba(255,255,255,0.8);
  border: 1.5px solid var(--border);
  border-radius: 18px;
  padding: 16px 12px;
  text-align: center;
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow);
}
.avatar-figure {
  font-size: 5rem;
  line-height: 1;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.08));
}
.avatar-label {
  font-size: 0.65rem;
  color: var(--muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 6px;
  font-weight: 600;
}

/* Outfit breakdown (right of avatar) */
.outfit-breakdown {
  flex: 1;
}
.ob-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}
.ob-sub { font-size: 0.78rem; color: var(--muted); margin-bottom: 14px; }

.outfit-item-row {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.9);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 14px;
  margin-bottom: 7px;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
}
.outfit-item-row:hover {
  border-color: var(--accent2);
  transform: translateX(3px);
  box-shadow: var(--shadow);
}
.oi-emoji { font-size: 1.5rem; min-width: 30px; text-align: center; }
.oi-cat   { font-size: 0.58rem; color: var(--accent); font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
.oi-name  { font-size: 0.88rem; font-weight: 600; color: var(--text); margin-top: 1px; }
.oi-src   {
  margin-left: auto;
  font-size: 0.58rem;
  padding: 2px 8px;
  border-radius: 8px;
  font-weight: 700;
  white-space: nowrap;
}
.src-closet { background: rgba(122,170,144,0.15); color: var(--green); border: 1px solid rgba(122,170,144,0.3); }
.src-ai     { background: rgba(201,149,110,0.12); color: var(--accent); border: 1px solid rgba(201,149,110,0.3); }

/* Score ring */
.score-wrap {
  width: 120px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.score-ring {
  width: 90px; height: 90px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.score-inner {
  width: 68px; height: 68px;
  border-radius: 50%;
  background: var(--surface);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 2px 6px rgba(0,0,0,0.06);
}
.score-num  { font-family: 'Playfair Display',serif; font-size: 1.5rem; font-weight: 900; color: var(--accent); line-height: 1; }
.score-pct  { font-size: 0.55rem; color: var(--muted); }
.score-conf { font-size: 0.68rem; font-weight: 700; color: var(--text2); text-align: center; }

/* Why card */
.why-card {
  background: rgba(255,255,255,0.85);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 0 12px 12px 0;
  padding: 12px 16px;
  margin-top: 10px;
  font-size: 0.82rem;
  color: var(--text2);
  line-height: 1.7;
}

/* ── BOTTOM CATEGORY GALLERY ── */
.gallery-area {
  padding: 0 24px 20px;
}
.gallery-section {
  margin-top: 20px;
}
.gallery-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.gallery-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.3px;
}
.gallery-count {
  font-size: 0.7rem;
  color: var(--muted);
  background: var(--border);
  padding: 2px 8px;
  border-radius: 10px;
}
.gallery-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 6px;
  scrollbar-width: thin;
}
.gallery-scroll::-webkit-scrollbar { height: 3px; }
.gallery-scroll::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.gallery-card {
  flex-shrink: 0;
  width: 100px;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 14px;
  padding: 12px 8px 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.22s ease;
  position: relative;
}
.gallery-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: var(--shadow2);
}
.gallery-card.in-outfit {
  border-color: var(--accent);
  background: rgba(201,149,110,0.06);
}
.gc-emoji { font-size: 2rem; margin-bottom: 5px; }
.gc-name  { font-size: 0.66rem; font-weight: 600; color: var(--text2); line-height: 1.25; }
.gc-color {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 0.58rem;
  color: var(--muted);
  margin-top: 4px;
}
.gc-dot { width: 7px; height: 7px; border-radius: 50%; }
.gc-worn { font-size: 0.58rem; color: var(--green); margin-top: 3px; }
.gc-add-btn {
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  opacity: 0;
  transition: opacity 0.2s;
}
.gallery-card:hover .gc-add-btn { opacity: 1; }

/* ── ACTION BUTTONS ── */
.action-bar {
  display: flex;
  gap: 10px;
  margin-top: 14px;
  flex-wrap: wrap;
}
.btn-primary {
  background: var(--dark);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'DM Sans', sans-serif;
  letter-spacing: 0.3px;
}
.btn-primary:hover { background: #2d2018; transform: translateY(-1px); box-shadow: var(--shadow2); }
.btn-secondary {
  background: var(--surface);
  color: var(--text);
  border: 1.5px solid var(--border2);
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'DM Sans', sans-serif;
}
.btn-secondary:hover { border-color: var(--accent); color: var(--accent); }

/* ── TAGS ── */
.chip {
  display: inline-block;
  background: var(--border);
  color: var(--text2);
  border-radius: 16px;
  padding: 3px 10px;
  font-size: 0.7rem;
  font-weight: 600;
  margin: 2px;
}
.chip.accent { background: rgba(201,149,110,0.12); color: var(--accent); border: 1px solid rgba(201,149,110,0.3); }

/* ── ANALYTICS CARDS ── */
.stat-row { display: flex; gap: 12px; margin-bottom: 16px; }
.stat-box {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px;
  text-align: center;
  transition: all 0.2s;
}
.stat-box:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.stat-n { font-family: 'Playfair Display',serif; font-size: 2rem; font-weight: 900; color: var(--accent); line-height: 1; }
.stat-l { font-size: 0.68rem; font-weight: 700; color: var(--muted); margin-top: 4px; letter-spacing: 0.8px; text-transform: uppercase; }

.bar-row { margin-bottom: 8px; }
.bar-lbl { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text2); margin-bottom: 4px; }
.bar-bg  { background: var(--border); border-radius: 6px; height: 7px; }
.bar-fg  { height: 7px; border-radius: 6px; transition: width 0.8s ease; }

/* ── HISTORY ── */
.hist-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px 16px;
  margin-bottom: 10px;
  transition: all 0.2s;
}
.hist-card:hover { box-shadow: var(--shadow); }
.hist-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.hist-occ  { font-weight: 700; font-size: 0.88rem; }
.hist-date { font-size: 0.7rem; color: var(--muted); }
.hist-items{ font-size: 0.78rem; color: var(--text2); line-height: 1.9; }

/* ── WISHLIST ── */
.wish-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
  display: flex;
  gap: 12px;
  align-items: center;
  transition: all 0.2s;
}
.wish-card:hover { box-shadow: var(--shadow); }
.wish-emoji { font-size: 2rem; }
.wish-info { flex: 1; }
.wish-name  { font-weight: 700; font-size: 0.88rem; }
.wish-brand { font-size: 0.73rem; color: var(--muted); }
.wish-price { font-size: 0.88rem; font-weight: 700; color: var(--accent); margin-top: 3px; }

/* ── CALENDAR ── */
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; margin-bottom: 16px; }
.cal-day {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 6px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 80px;
}
.cal-day:hover { border-color: var(--accent); box-shadow: var(--shadow); }
.cal-day.has-outfit { border-color: var(--accent2); background: rgba(201,149,110,0.05); }
.cal-day.today { border-color: var(--dark); border-width: 2px; }
.cal-dayname { font-size: 0.65rem; color: var(--muted); font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.cal-date    { font-size: 0.9rem; font-weight: 700; color: var(--text); margin: 3px 0; }
.cal-outfit  { font-size: 0.65rem; color: var(--accent); font-weight: 600; margin-top: 4px; line-height: 1.3; }

/* ── TREND CARD ── */
.trend-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 10px;
  border-left: 3px solid var(--accent);
}
.trend-title { font-weight: 700; font-size: 0.92rem; margin-bottom: 5px; }
.trend-sub   { font-size: 0.78rem; color: var(--muted); margin-bottom: 8px; }
.trend-items { display: flex; flex-wrap: wrap; gap: 5px; }

/* ── STWIDGET RESET ── */
.stButton > button {
  background: var(--dark) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.82rem !important;
  padding: 0.55rem 1.2rem !important;
  transition: all 0.2s !important;
  width: 100% !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important; }
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--surface) !important;
  border: 1.5px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input,
.stTextArea textarea {
  background: var(--surface) !important;
  border: 1.5px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 10px !important;
}
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-bottom: 1.5px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  border-bottom: 2px solid transparent !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] { color: var(--text) !important; border-bottom-color: var(--dark) !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# INIT
# ──────────────────────────────────────────────
database.initialize_database()
engine = RecommendationEngine()
user   = database.get_or_create_user()
UID    = user["user_id"]

TYPE_EMOJI = {"top":"👕","bottom":"👖","shoes":"👟","accessory":"💍",
              "outerwear":"🧥","dress":"👗","traditional":"🥻"}
COLOR_HEX  = {"Neutral":"#b5aca0","Dark":"#3d3530","Warm":"#d4895a",
               "Cool":"#7a9dbf","Pastel":"#e8b4c8","Earthy":"#8b7355",
               "Pink":"#d4a0b5","Multi":"#c9956e"}

for k,v in [("outfit_result",None),("active_page","today"),("saved_id",None),
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

# ──────────────────────────────────────────────
# TOP NAV
# ──────────────────────────────────────────────
st.markdown('<div style="background:white;border-bottom:1px solid #ede9e3;padding:0 24px;display:flex;align-items:center;gap:8px;height:52px;box-shadow:0 1px 8px rgba(0,0,0,0.05)">', unsafe_allow_html=True)
st.markdown('<span style="font-family:Playfair Display,serif;font-size:1.35rem;font-weight:900;background:linear-gradient(135deg,#c9956e,#d4a0b5);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-0.5px;margin-right:8px">👗 DressiFy</span>', unsafe_allow_html=True)

nav_cols = st.columns([1,6,6])
with nav_cols[0]:
    st.markdown("")
with nav_cols[1]:
    pages = ["🪞 Today's Look","👚 My Closet","📊 Analytics","📅 Calendar","❤️ Saved","🛍️ Wishlist","🔥 Trends"]
    page_keys = ["today","closet","analytics","calendar","saved","wishlist","trends"]
    sel = st.selectbox("nav", pages, label_visibility="collapsed",
                       index=page_keys.index(st.session_state.active_page))
    st.session_state.active_page = page_keys[pages.index(sel)]
with nav_cols[2]:
    st.markdown("")

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PROFILE EXPANDER (always visible, collapsible)
# ──────────────────────────────────────────────
with st.expander("⚙️ Style Profile & Settings", expanded=False):
    pc1,pc2,pc3,pc4 = st.columns(4)
    with pc1:
        gender    = st.selectbox("Gender",["Female","Male","Other"])
        age       = st.slider("Age",13,60,int(user.get("age",20)))
    with pc2:
        body_type = st.selectbox("Body Type",["All","Hourglass","Pear","Apple","Rectangle","Inverted Triangle"])
        skin_tone = st.selectbox("Skin Tone",["All","Fair","Wheatish","Medium","Dark"])
    with pc3:
        preferred_fit = st.selectbox("Preferred Fit",["Regular","Oversized","Slim"])
        fav_colors = st.multiselect("Fav Colors",["Neutral","Dark","Warm","Cool","Pastel","Earthy","Pink","Multi"],default=["Neutral","Warm"])
    with pc4:
        occasion = st.selectbox("Occasion",["College","Office","Interview","Wedding","Party","Date","Casual Outing","Gym","Airport Look","Vacation","Festival","Traditional Function"])
        weather  = st.selectbox("Weather",["Sunny","Rainy","Winter","Humid","Windy"])
    if st.button("💾 Save Profile"):
        database.update_user(UID,name="User",age=age,gender=gender,skin_tone=skin_tone,
                             body_type=body_type,preferred_fit=preferred_fit,fav_colors=json.dumps(fav_colors))
        st.success("Saved ✓")

# Load profile from DB for defaults
try:
    gender        = gender
    body_type     = body_type
    skin_tone     = skin_tone
    preferred_fit = preferred_fit
    fav_colors    = fav_colors
    occasion      = occasion
    weather       = weather
except:
    gender="Female"; body_type="All"; skin_tone="Wheatish"; preferred_fit="Regular"
    fav_colors=["Neutral"]; occasion="College"; weather="Sunny"

st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# PAGE: TODAY'S LOOK
# ══════════════════════════════════════════════
if st.session_state.active_page == "today":

    left_col, main_col = st.columns([1, 2.8], gap="small")

    # ── LEFT: MINI CLOSET PANEL ──────────────
    with left_col:
        wardrobe = database.get_wardrobe(UID)
        st.markdown('<div style="background:white;border:1px solid #ede9e3;border-radius:16px;padding:14px;min-height:500px">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:10px">My Closet</div>', unsafe_allow_html=True)

        use_closet = st.toggle("Style from closet", value=False)
        wcount = len(wardrobe)
        st.markdown(f'<div style="font-size:0.72rem;color:#7aaa90;margin-bottom:10px">🧥 {wcount} items</div>' if wcount else '<div style="font-size:0.72rem;color:#a89880;margin-bottom:10px">Empty closet — add items in My Closet tab</div>', unsafe_allow_html=True)

        # Group by type and show grid tiles
        type_groups = {}
        for item in wardrobe[:24]:  # show max 24
            t = item["item_type"]
            type_groups.setdefault(t,[]).append(item)

        for t, items in type_groups.items():
            em = TYPE_EMOJI.get(t,"🏷️")
            st.markdown(f'<div style="font-size:0.65rem;font-weight:700;color:#6b5d52;margin:8px 0 5px 0;text-transform:uppercase;letter-spacing:1px">{em} {t}s</div>', unsafe_allow_html=True)
            # 3-col grid
            cols = st.columns(3)
            for i,item in enumerate(items[:6]):
                with cols[i%3]:
                    st.markdown(f"""
                    <div class="closet-tile">
                      <div class="t-emoji">{em}</div>
                      <div class="t-name">{item['item_name'][:12]}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: OUTFIT GENERATOR ───────────────
    with main_col:
        # Generate button row
        gc1, gc2, gc3 = st.columns([2,1,1])
        with gc1:
            gen_btn = st.button("✨ Generate AI Look", type="primary")
        with gc2:
            regen_btn = st.button("🔁 Regenerate")
        with gc3:
            save_btn = st.button("❤️ Save Look")

        if gen_btn or regen_btn:
            with st.spinner("Styling your look..."):
                result = engine.generate_outfit(
                    user_id=UID,gender=gender,age=age,body_type=body_type,
                    skin_tone=skin_tone,occasion=occasion,weather=weather,
                    preferred_fit=preferred_fit,fav_colors=fav_colors,
                    use_wardrobe=use_closet
                )
                outfit_lines = "\n".join(f"- {k.upper()}: {v['item']}" for k,v in result["outfit"].items())
                prompt = f"""You are DressiFy, an AI fashion stylist. User: Gender:{gender}, Age:{age}, Body:{body_type}, Skin:{skin_tone}, Occasion:{occasion}, Weather:{weather}.
Outfit:\n{outfit_lines}\nWrite 2-3 warm sentences: why colours suit skin tone, why fit flatters body, why perfect for occasion+weather. Plain text only."""
                expl = ask_gemini(prompt) or f"This look is crafted for {occasion.lower()} in {weather.lower()} weather. The colour palette complements your {skin_tone.lower()} skin tone while the {preferred_fit.lower()} fit enhances your silhouette beautifully."
                result["explanation"] = expl
                st.session_state.outfit_result = result

        if save_btn and st.session_state.outfit_result:
            res = st.session_state.outfit_result
            oid = database.save_outfit(UID,occasion=res["occasion"],weather=res["weather"],
                items_dict={k:v["item"] for k,v in res["outfit"].items()},
                explanation=res["explanation"],ai_score=res.get("ai_score",0),
                confidence=res.get("confidence",""))
            st.session_state.saved_id = oid
            st.success("Look saved! ❤️")

        # ── OUTFIT DISPLAY ──
        if st.session_state.outfit_result:
            res    = st.session_state.outfit_result
            outfit = res["outfit"]
            score  = res.get("ai_score",0)
            conf   = res.get("confidence","Match")

            # Context chips
            st.markdown(
                f'<div style="margin-bottom:12px">'
                f'<span class="chip">{occasion}</span>'
                f'<span class="chip">{weather}</span>'
                f'<span class="chip">{gender}</span>'
                f'<span class="chip accent">{score}% {conf}</span>'
                f'</div>', unsafe_allow_html=True
            )

            oa, ob = st.columns([2.5, 1])
            with oa:
                # Outfit as "Today's Look" card
                st.markdown("""
                <div style="background:linear-gradient(160deg,#f2ede7,#faf8f5);
                            border:1.5px solid #ede9e3;border-radius:18px;padding:18px;
                            box-shadow:0 2px 16px rgba(44,32,24,0.06)">
                <div style="font-family:Playfair Display,serif;font-size:1.1rem;font-weight:700;margin-bottom:12px;color:#2c2018">
                ✨ Today's Complete Look</div>""", unsafe_allow_html=True)

                for cat, det in outfit.items():
                    is_w   = det["source"]=="wardrobe"
                    src_cls= "src-closet" if is_w else "src-ai"
                    src_lbl= "👚 Closet" if is_w else "✦ AI"
                    desc   = f'<div class="oi-desc" style="font-size:0.71rem;color:#a89880">{det["description"]}</div>' if det.get("description") else ""
                    st.markdown(f"""
                    <div class="outfit-item-row">
                      <span class="oi-emoji">{det['emoji']}</span>
                      <div style="flex:1">
                        <div class="oi-cat">{cat.upper()}</div>
                        <div class="oi-name">{det['item']}</div>
                        {desc}
                      </div>
                      <span class="oi-src {src_cls}">{src_lbl}</span>
                    </div>""", unsafe_allow_html=True)

                # Hairstyle
                hair = res["hair_options"][0]
                st.markdown(f"""
                <div class="outfit-item-row">
                  <span class="oi-emoji">{hair[0]}</span>
                  <div style="flex:1">
                    <div class="oi-cat">HAIRSTYLE</div>
                    <div class="oi-name">{hair[1]}</div>
                    <div style="font-size:0.71rem;color:#a89880">{hair[2]}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Why card
                st.markdown(f'<div class="why-card"><b style="color:#c9956e">🎨 Why this works:</b><br>{res["explanation"]}</div>', unsafe_allow_html=True)

            with ob:
                # Score ring
                ring_c = "#c9956e" if score>=80 else "#9b87b8" if score>=65 else "#7aaa90"
                st.markdown(f"""
                <div style="background:white;border:1.5px solid #ede9e3;border-radius:18px;padding:20px 10px;text-align:center;box-shadow:0 2px 16px rgba(44,32,24,0.06)">
                  <div class="score-ring" style="background:conic-gradient({ring_c} {score*3.6}deg,#ede9e3 0deg);margin:0 auto 10px">
                    <div class="score-inner">
                      <div class="score-num">{score}</div>
                      <div class="score-pct">/ 100</div>
                    </div>
                  </div>
                  <div style="font-size:0.78rem;font-weight:700;color:#2c2018">{conf}</div>
                  <div style="font-size:0.68rem;color:#a89880;margin-top:6px">AI Match Score</div>
                  {''.join(f'<div style="font-size:0.68rem;color:#7aaa90;margin-top:4px">✓ {f}</div>' for f in res.get("score_factors",[])[:3])}
                </div>""", unsafe_allow_html=True)

                if len(res["hair_options"]) > 1:
                    alt = res["hair_options"][1]
                    st.markdown(f'<div style="margin-top:10px;background:white;border:1px solid #ede9e3;border-radius:12px;padding:12px;font-size:0.75rem"><div style="color:#a89880;font-size:0.63rem;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:4px">Alt Hairstyle</div><b>{alt[1]}</b><br><span style="color:#a89880">{alt[2]}</span></div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background:linear-gradient(160deg,#f2ede7,#faf8f5);border:1.5px dashed #ddd8d0;
                        border-radius:18px;padding:60px;text-align:center;margin-top:10px">
              <div style="font-size:3.5rem;margin-bottom:12px">👗</div>
              <div style="font-family:Playfair Display,serif;font-size:1.2rem;font-weight:700;color:#2c2018;margin-bottom:6px">
                Ready to get styled?</div>
              <div style="font-size:0.82rem;color:#a89880">Set your profile above and click Generate AI Look</div>
            </div>""", unsafe_allow_html=True)

        # ── CATEGORY GALLERY (bottom of center) ──
        wardrobe = database.get_wardrobe(UID)
        if wardrobe:
            st.markdown('<div style="margin-top:20px;font-family:Playfair Display,serif;font-size:1rem;font-weight:700;color:#2c2018;margin-bottom:4px">Browse My Closet</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.75rem;color:#a89880;margin-bottom:14px">Scroll categories to explore your wardrobe</div>', unsafe_allow_html=True)

            type_order = ["top","bottom","outerwear","shoes","accessory","dress","traditional"]
            type_groups2 = {}
            for item in wardrobe:
                t = item["item_type"]
                type_groups2.setdefault(t,[]).append(item)

            for t in type_order:
                items = type_groups2.get(t,[])
                if not items: continue
                em = TYPE_EMOJI.get(t,"🏷️")
                st.markdown(f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span style="font-size:0.78rem;font-weight:700;color:#2c2018">{em} {t.capitalize()}s</span><span style="font-size:0.68rem;background:#ede9e3;padding:2px 8px;border-radius:10px;color:#a89880">{len(items)}</span></div>', unsafe_allow_html=True)

                item_cols = st.columns(min(len(items), 7))
                for i, item in enumerate(items[:7]):
                    cf    = item.get("color_family","Neutral")
                    hexc  = COLOR_HEX.get(cf,"#b5aca0")
                    worn  = f"Worn {item['times_worn']}×" if item.get("times_worn",0)>0 else ""
                    with item_cols[i]:
                        st.markdown(f"""
                        <div class="gallery-card">
                          <div class="gc-emoji">{em}</div>
                          <div class="gc-name">{item['item_name'][:16]}</div>
                          <div class="gc-color">
                            <span class="gc-dot" style="background:{hexc}"></span>{cf}
                          </div>
                          {f'<div class="gc-worn">{worn}</div>' if worn else ''}
                        </div>""", unsafe_allow_html=True)

        elif not engine.df.empty:
            # Show catalogue gallery if no wardrobe
            st.markdown('<div style="margin-top:20px;font-family:Playfair Display,serif;font-size:1rem;font-weight:700;color:#2c2018;margin-bottom:4px">Fashion Catalogue</div>', unsafe_allow_html=True)
            for t in ["top","bottom","shoes","accessory"]:
                items_df = engine.df[engine.df["type"]==t].head(6)
                if items_df.empty: continue
                em = TYPE_EMOJI.get(t,"🏷️")
                st.markdown(f'<div style="font-size:0.78rem;font-weight:700;color:#2c2018;margin:12px 0 8px">{em} {t.capitalize()}s</div>', unsafe_allow_html=True)
                ccols = st.columns(6)
                for i,(_,row) in enumerate(items_df.iterrows()):
                    cf   = row.get("color_family","Neutral")
                    hexc = COLOR_HEX.get(cf,"#b5aca0")
                    with ccols[i]:
                        st.markdown(f"""
                        <div class="gallery-card">
                          <div class="gc-emoji">{em}</div>
                          <div class="gc-name">{row['item'][:16]}</div>
                          <div class="gc-color">
                            <span class="gc-dot" style="background:{hexc}"></span>{cf}
                          </div>
                        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: MY CLOSET
# ══════════════════════════════════════════════
elif st.session_state.active_page == "closet":
    st.markdown('<div style="padding:20px 24px 0">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;margin-bottom:4px">My Closet 👚</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#a89880;margin-bottom:18px">Add your real clothes. DressiFy will style outfits from what you own.</div>', unsafe_allow_html=True)

    c_add, c_view = st.columns([1, 2.2], gap="large")

    with c_add:
        st.markdown("#### Add Item")
        TYPE_OPTS = ["top","bottom","outerwear","shoes","accessory","dress","traditional"]
        w_type  = st.selectbox("Category", TYPE_OPTS)
        sug     = engine.df[engine.df["type"]==w_type]["item"].tolist() if not engine.df.empty else []
        w_pick  = st.selectbox("Pick from catalogue", ["— type custom —"]+sug)
        w_name  = st.text_input("Item Name", placeholder="e.g. White Oversized Tee")
        if w_pick != "— type custom —" and not w_name:
            w_name = w_pick
        w_color = st.text_input("Color", placeholder="e.g. White")
        w_cfam  = st.selectbox("Color Family", ["Neutral","Dark","Warm","Cool","Pastel","Earthy","Pink","Multi"])
        w_notes = st.text_input("Notes (optional)", placeholder="Brand, occasion, etc.")

        ca, cb = st.columns(2)
        with ca:
            if st.button("➕ Add"):
                fn = w_name.strip() or (w_pick if w_pick!="— type custom —" else "")
                if fn:
                    database.add_wardrobe_item(UID,w_type,fn,w_color,w_cfam,"",w_notes)
                    st.success(f"✓ Added: {fn}"); st.rerun()
                else: st.error("Enter item name")
        with cb:
            if st.button("🗑️ Clear"):
                conn=database.get_connection(); conn.execute("DELETE FROM wardrobe WHERE user_id=?",(UID,)); conn.commit(); conn.close(); st.rerun()

    with c_view:
        wardrobe = database.get_wardrobe(UID)
        type_filter = st.selectbox("Filter", ["All"]+TYPE_OPTS, key="cf_type")
        fav_only    = st.checkbox("❤️ Favourites only")
        wshow = wardrobe
        if type_filter!="All": wshow=[w for w in wshow if w["item_type"]==type_filter]
        if fav_only: wshow=[w for w in wshow if w.get("is_favourite")]

        st.markdown(f'<div style="font-size:0.75rem;color:#a89880;margin-bottom:12px">{len(wshow)} items</div>', unsafe_allow_html=True)

        if wshow:
            # Pinterest grid — 5 cols
            cols = st.columns(5)
            for i, item in enumerate(wshow):
                em   = TYPE_EMOJI.get(item["item_type"],"🏷️")
                cf   = item.get("color_family","Neutral")
                hexc = COLOR_HEX.get(cf,"#b5aca0")
                fav  = "❤️" if item.get("is_favourite") else "🤍"
                worn = f"Worn {item['times_worn']}×" if item.get("times_worn",0)>0 else "Never worn"
                with cols[i%5]:
                    st.markdown(f"""
                    <div class="p-card" style="background:white;border:1.5px solid #ede9e3;border-radius:16px;
                         padding:14px 10px;text-align:center;margin-bottom:10px;transition:all 0.2s;
                         {'border-color:#c9956e' if item.get('is_favourite') else ''}">
                      <div style="font-size:0.6rem;font-weight:700;color:#c9956e;letter-spacing:1.5px;
                           text-transform:uppercase;background:rgba(201,149,110,0.1);border-radius:6px;
                           padding:2px 7px;margin-bottom:6px">{item['item_type']}</div>
                      <div style="font-size:2.2rem;margin-bottom:6px">{em}</div>
                      <div style="font-size:0.75rem;font-weight:700;color:#2c2018;line-height:1.3">{item['item_name']}</div>
                      <div style="display:flex;align-items:center;justify-content:center;gap:4px;margin-top:5px">
                        <span style="background:{hexc};width:8px;height:8px;border-radius:50%;display:inline-block"></span>
                        <span style="font-size:0.63rem;color:#a89880">{item.get('color','') or cf}</span>
                      </div>
                      <div style="font-size:0.63rem;color:#7aaa90;margin-top:4px">{worn}</div>
                      <div style="font-size:0.75rem;margin-top:4px">{fav}</div>
                      <div style="font-size:0.58rem;color:#a89880;margin-top:2px">ID: {item['item_id']}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:50px;color:#a89880">No items yet. Add clothes to see them here!</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:14px"></div>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            did = st.number_input("Delete by ID", min_value=0, step=1, value=0)
            if st.button("✕ Remove") and did:
                database.delete_wardrobe_item(did); st.rerun()
        with d2:
            fid = st.number_input("Toggle Fav by ID", min_value=0, step=1, value=0, key="fav_id")
            if st.button("❤️ Toggle") and fid:
                database.toggle_wardrobe_favourite(fid); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════
elif st.session_state.active_page == "analytics":
    st.markdown('<div style="padding:20px 24px">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;margin-bottom:4px">Closet Analytics 📊</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#a89880;margin-bottom:20px">Smart insights into your wardrobe.</div>', unsafe_allow_html=True)

    wardrobe  = database.get_wardrobe(UID)
    analytics = database.get_wardrobe_analytics(UID)
    missing   = engine.find_missing_items(wardrobe, gender if 'gender' in dir() else "Female")
    color_data= engine.analyze_colors(wardrobe)

    if analytics["total"] == 0:
        st.info("Add some clothes to see analytics!")
    else:
        # Stats
        s1,s2,s3,s4 = st.columns(4)
        for col,(num,lbl) in zip([s1,s2,s3,s4],[
            (analytics["total"],"Total Items"),
            (len(analytics["by_type"]),"Categories"),
            (sum(1 for w in wardrobe if w.get("is_favourite")),"Favourites"),
            (sum(1 for w in wardrobe if w.get("times_worn",0)==0),"Never Worn"),
        ]):
            col.markdown(f'<div class="stat-box"><div class="stat-n">{num}</div><div class="stat-l">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        ac1, ac2, ac3 = st.columns([1.2,1.2,1], gap="large")

        with ac1:
            st.markdown('<div style="background:white;border:1px solid #ede9e3;border-radius:16px;padding:18px">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:12px">Items by Category</div>', unsafe_allow_html=True)
            mx = max(analytics["by_type"].values()) if analytics["by_type"] else 1
            for t,cnt in sorted(analytics["by_type"].items(),key=lambda x:-x[1]):
                pct = int(cnt/mx*100)
                em  = TYPE_EMOJI.get(t,"🏷️")
                st.markdown(f'<div class="bar-row"><div class="bar-lbl"><span>{em} {t.capitalize()}s</span><span style="color:#c9956e;font-weight:700">{cnt}</span></div><div class="bar-bg"><div class="bar-fg" style="width:{pct}%;background:linear-gradient(90deg,#c9956e,#d4a0b5)"></div></div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with ac2:
            st.markdown('<div style="background:white;border:1px solid #ede9e3;border-radius:16px;padding:18px">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:12px">Colour Distribution</div>', unsafe_allow_html=True)
            if color_data.get("distribution"):
                mx2 = max(color_data["distribution"].values())
                for cf,cnt in sorted(color_data["distribution"].items(),key=lambda x:-x[1]):
                    pct  = int(cnt/mx2*100)
                    hexc = COLOR_HEX.get(cf,"#888")
                    st.markdown(f'<div class="bar-row"><div class="bar-lbl"><span style="display:flex;align-items:center;gap:6px"><span style="background:{hexc};width:10px;height:10px;border-radius:50%;display:inline-block"></span>{cf}</span><span style="color:#c9956e;font-weight:700">{cnt}</span></div><div class="bar-bg"><div class="bar-fg" style="width:{pct}%;background:{hexc}"></div></div></div>', unsafe_allow_html=True)
            if color_data.get("missing_colors"):
                st.markdown(f'<div style="font-size:0.72rem;color:#a89880;margin-top:10px">Missing: {", ".join(color_data["missing_colors"])}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with ac3:
            st.markdown('<div style="background:white;border:1px solid #ede9e3;border-radius:16px;padding:18px">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:10px">🔍 Missing Items</div>', unsafe_allow_html=True)
            if not missing:
                st.markdown('<div style="color:#7aaa90;font-size:0.82rem">Wardrobe looks complete! ✓</div>', unsafe_allow_html=True)
            else:
                for m in missing:
                    st.markdown(f'<div style="background:rgba(201,112,112,0.07);border:1px solid rgba(201,112,112,0.2);border-radius:10px;padding:10px;margin-bottom:7px"><div style="font-size:0.6rem;color:#c97070;font-weight:700;letter-spacing:1.5px;text-transform:uppercase">{m["type"]}</div><div style="font-size:0.85rem;font-weight:700;color:#2c2018">+ {m["suggestion"]}</div><div style="font-size:0.7rem;color:#a89880;margin-top:2px">{m["reason"]}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Most / Never worn
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        mw1, mw2 = st.columns(2)
        with mw1:
            st.markdown('<div style="background:white;border:1px solid #ede9e3;border-radius:16px;padding:18px">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:10px">🔥 Most Worn</div>', unsafe_allow_html=True)
            for item in analytics.get("most_worn",[]):
                if item["times_worn"]>0:
                    st.markdown(f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #ede9e3"><span style="font-size:0.85rem">{item["item_name"]}</span><span style="color:#c9956e;font-weight:700">{item["times_worn"]}×</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with mw2:
            st.markdown('<div style="background:white;border:1px solid #ede9e3;border-radius:16px;padding:18px">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:10px">😴 Never Worn</div>', unsafe_allow_html=True)
            for item in analytics.get("never_worn",[])[:5]:
                em = TYPE_EMOJI.get(item["item_type"],"🏷️")
                st.markdown(f'<div style="padding:7px 0;border-bottom:1px solid #ede9e3;font-size:0.85rem;color:#6b5d52">{em} {item["item_name"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: CALENDAR PLANNER (Phase 8)
# ══════════════════════════════════════════════
elif st.session_state.active_page == "calendar":
    st.markdown('<div style="padding:20px 24px">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;margin-bottom:4px">Outfit Planner 📅</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#a89880;margin-bottom:18px">Plan outfits for the week — no repeats, always prepared.</div>', unsafe_allow_html=True)

    today = date.today()
    days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    from datetime import timedelta
    week_start = today - timedelta(days=today.weekday())
    week_dates = [week_start + timedelta(days=i) for i in range(7)]

    st.markdown('<div class="cal-grid">', unsafe_allow_html=True)
    for i, (day, dt) in enumerate(zip(days, week_dates)):
        key     = str(dt)
        has_fit = key in st.session_state.cal_outfits
        is_today= dt == today
        outfit_preview = st.session_state.cal_outfits.get(key,"")
        today_cls = "cal-day today" if is_today else ("cal-day has-outfit" if has_fit else "cal-day")
        st.markdown(f"""
        <div class="{today_cls}">
          <div class="cal-dayname">{day}</div>
          <div class="cal-date">{dt.day}</div>
          <div class="cal-outfit">{outfit_preview[:30] if outfit_preview else ("Today" if is_today else "")}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Plan outfit for a date
    st.markdown("#### Plan an Outfit")
    plan_date = st.date_input("Select Date", value=today)
    plan_occ  = st.selectbox("Occasion for this day", ["College","Office","Party","Date","Casual Outing","Vacation","Gym"])
    if st.button("📅 Generate & Plan"):
        result = engine.generate_outfit(user_id=UID,gender="Female",age=22,body_type="All",
            skin_tone="Wheatish",occasion=plan_occ,weather="Sunny",preferred_fit="Regular",
            fav_colors=["Neutral"],use_wardrobe=False)
        preview = " · ".join(v["item"] for v in list(result["outfit"].values())[:3])
        st.session_state.cal_outfits[str(plan_date)] = f"{plan_occ}: {preview}"
        st.success(f"Planned for {plan_date}!")

    if st.session_state.cal_outfits:
        st.markdown("#### Planned Outfits")
        for dt, fit in sorted(st.session_state.cal_outfits.items()):
            st.markdown(f'<div style="background:white;border:1px solid #ede9e3;border-radius:10px;padding:10px 14px;margin-bottom:6px;font-size:0.82rem"><b style="color:#c9956e">{dt}</b> — {fit}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: SAVED LOOKS (Phase 9)
# ══════════════════════════════════════════════
elif st.session_state.active_page == "saved":
    st.markdown('<div style="padding:20px 24px">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;margin-bottom:4px">Saved Looks ❤️</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#a89880;margin-bottom:18px">Your favourite outfits — organised by occasion.</div>', unsafe_allow_html=True)

    history = database.get_outfit_history(UID, limit=40)
    if not history:
        st.markdown('<div style="text-align:center;padding:60px;color:#a89880">No saved looks yet. Generate and save your first outfit! ✨</div>', unsafe_allow_html=True)
    else:
        hf1,hf2 = st.columns(2)
        with hf1: fav_f = st.checkbox("❤️ Favourites only")
        with hf2: occ_f = st.selectbox("Filter Occasion",["All"]+list({h["occasion"] for h in history}))
        hshow = history
        if fav_f:  hshow=[h for h in hshow if h.get("is_favourite")]
        if occ_f!="All": hshow=[h for h in hshow if h["occasion"]==occ_f]

        # Group by occasion
        occ_groups = {}
        for h in hshow:
            occ_groups.setdefault(h["occasion"],[]).append(h)

        for occ_name, looks in occ_groups.items():
            st.markdown(f'<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin:16px 0 8px 0">{occ_name} ({len(looks)})</div>', unsafe_allow_html=True)
            hcols = st.columns(min(len(looks),3))
            for i,h in enumerate(looks[:3]):
                items    = h.get("items",{})
                items_str= "\n".join(f"{k}: {v}" for k,v in items.items())
                stars    = "⭐"*h.get("rating",0) if h.get("rating") else ""
                score_b  = f'<div style="font-size:0.7rem;color:#c9956e;font-weight:700;margin-top:5px">✨ {h["ai_score"]}%</div>' if h.get("ai_score") else ""
                fav_icon = "❤️" if h.get("is_favourite") else "🤍"
                with hcols[i%3]:
                    st.markdown(f"""
                    <div class="hist-card">
                      <div class="hist-head">
                        <span style="font-weight:700;font-size:0.85rem">{fav_icon} {h['weather']}</span>
                        <span style="font-size:0.68rem;color:#a89880">{h.get('created_at','')[:10]}</span>
                      </div>
                      <div style="font-size:0.78rem;color:#6b5d52;line-height:1.9;white-space:pre-line">{items_str}</div>
                      {score_b}
                      <div style="margin-top:5px">{stars}</div>
                    </div>""", unsafe_allow_html=True)
                    rc1,rc2 = st.columns(2)
                    with rc1:
                        if st.button(f"❤️",key=f"fh_{h['outfit_id']}"):
                            database.toggle_outfit_favourite(h["outfit_id"]); st.rerun()
                    with rc2:
                        r = st.select_slider("★",options=[1,2,3,4,5],value=max(1,h.get("rating",1)),
                                             key=f"rs_{h['outfit_id']}",label_visibility="collapsed")
                        if st.button("Rate",key=f"rb_{h['outfit_id']}"):
                            database.rate_outfit(h["outfit_id"],r); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: WISHLIST (Phase 10)
# ══════════════════════════════════════════════
elif st.session_state.active_page == "wishlist":
    st.markdown('<div style="padding:20px 24px">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;margin-bottom:4px">Wishlist 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#a89880;margin-bottom:18px">Save items you want to buy. Track brand, price, and links.</div>', unsafe_allow_html=True)

    wl_c1, wl_c2 = st.columns([1,2])
    with wl_c1:
        st.markdown("#### + Add Item")
        wl_name  = st.text_input("Item Name", placeholder="e.g. White Nike Air Force 1")
        wl_brand = st.text_input("Brand", placeholder="e.g. Nike")
        wl_price = st.text_input("Price", placeholder="e.g. ₹6,500")
        wl_link  = st.text_input("Link (optional)", placeholder="https://...")
        wl_type  = st.selectbox("Category", ["top","bottom","shoes","accessory","outerwear","dress"])
        if st.button("➕ Add to Wishlist"):
            if wl_name:
                st.session_state.wishlist.append({
                    "name":wl_name,"brand":wl_brand,"price":wl_price,
                    "link":wl_link,"type":wl_type,"added":str(date.today())
                })
                st.success(f"✓ Added: {wl_name}")

    with wl_c2:
        if not st.session_state.wishlist:
            st.markdown('<div style="text-align:center;padding:50px;color:#a89880">Your wishlist is empty. Start adding items! 🛍️</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:0.75rem;color:#a89880;margin-bottom:12px">{len(st.session_state.wishlist)} items saved</div>', unsafe_allow_html=True)
            for i, item in enumerate(st.session_state.wishlist):
                em = TYPE_EMOJI.get(item["type"],"🛍️")
                st.markdown(f"""
                <div class="wish-card">
                  <div class="wish-emoji">{em}</div>
                  <div class="wish-info">
                    <div class="wish-name">{item['name']}</div>
                    <div class="wish-brand">{item.get('brand','')} · Added {item.get('added','')}</div>
                    <div class="wish-price">{item.get('price','')}</div>
                    {f'<a href="{item["link"]}" style="font-size:0.72rem;color:#c9956e" target="_blank">View Product →</a>' if item.get('link') else ''}
                  </div>
                </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Clear Wishlist"):
                st.session_state.wishlist = []; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: TRENDS (Phase 11)
# ══════════════════════════════════════════════
elif st.session_state.active_page == "trends":
    st.markdown('<div style="padding:20px 24px">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Playfair Display,serif;font-size:1.5rem;font-weight:700;margin-bottom:4px">Fashion Trends 🔥</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#a89880;margin-bottom:18px">What\'s trending right now — Summer 2026 edition.</div>', unsafe_allow_html=True)

    trends = [
        {"season":"Summer 2026","title":"Linen Everything","sub":"Breathable, elegant, effortless",
         "items":["Linen Shirt","Linen Co-ord","Linen Wide-Leg Pants","Linen Shorts"],"color":"#d4895a"},
        {"season":"Summer 2026","title":"Earth Tones","sub":"Warm, grounded, nature-inspired",
         "items":["Rust Crop Top","Camel Trousers","Terracotta Dress","Olive Jacket"],"color":"#8b7355"},
        {"season":"Summer 2026","title":"Co-ord Sets","sub":"Matching sets are the new power move",
         "items":["Sage Green Co-ord","White Linen Set","Brown Knit Set","Beige Shirt Set"],"color":"#7a9dbf"},
        {"season":"Summer 2026","title":"Minimalist Accessories","sub":"Less is more — silver, clean, simple",
         "items":["Thin Gold Chain","Silver Cuff","Minimalist Watch","Simple Hoop Earrings"],"color":"#9b87b8"},
        {"season":"Summer 2026","title":"Wide-Leg Denim","sub":"The 90s are back and thriving",
         "items":["Baggy Blue Jeans","Wide-Leg White Denim","Mom Jeans","Barrel Leg Jeans"],"color":"#7aaa90"},
        {"season":"Summer 2026","title":"Sporty Luxe","sub":"Gym-to-street transition outfits",
         "items":["Crop Sports Bra","Track Pants","Windbreaker Jacket","Chunky Sneakers"],"color":"#c97070"},
    ]

    t_cols = st.columns(3)
    for i, trend in enumerate(trends):
        with t_cols[i%3]:
            st.markdown(f"""
            <div class="trend-card" style="border-left-color:{trend['color']}">
              <div style="font-size:0.62rem;color:{trend['color']};font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:4px">{trend['season']}</div>
              <div class="trend-title">{trend['title']}</div>
              <div class="trend-sub">{trend['sub']}</div>
              <div class="trend-items">
                {''.join(f'<span style="background:rgba(0,0,0,0.05);color:#6b5d52;border-radius:12px;padding:3px 9px;font-size:0.68rem;font-weight:600">{item}</span>' for item in trend["items"])}
              </div>
            </div>""", unsafe_allow_html=True)

    # AI Trend Insights
    st.markdown('<div style="margin-top:20px">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#a89880;margin-bottom:12px">✨ AI STYLE INSIGHT</div>', unsafe_allow_html=True)
    if st.button("🧠 Get AI Trend Advice"):
        wardrobe = database.get_wardrobe(UID)
        w_items = ", ".join(w["item_name"] for w in wardrobe[:10]) if wardrobe else "a basic wardrobe"
        prompt = f"As DressiFy AI stylist, give 3 specific trend-based fashion tips for Summer 2026. The user has: {w_items}. Tips should be practical, mention trending items, and suggest how to incorporate 2026 trends. Keep it under 150 words, conversational, no markdown symbols."
        advice = ask_gemini(prompt) or "Linen and earth tones are dominating Summer 2026. Consider adding a sage green co-ord set or camel wide-leg trousers to your wardrobe. Minimalist silver jewellery pairs perfectly with your existing neutral pieces."
        st.markdown(f'<div style="background:rgba(201,149,110,0.08);border:1px solid rgba(201,149,110,0.25);border-left:3px solid #c9956e;border-radius:0 12px 12px 0;padding:14px 18px;font-size:0.85rem;color:#2c2018;line-height:1.7">{advice}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)