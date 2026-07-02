import sqlite3
import json
from datetime import datetime

DB_NAME = "fashion.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT DEFAULT 'User',
        age           INTEGER DEFAULT 20,
        gender        TEXT DEFAULT 'Female',
        skin_tone     TEXT DEFAULT 'Wheatish',
        body_type     TEXT DEFAULT 'All',
        preferred_fit TEXT DEFAULT 'Regular',
        fav_colors    TEXT DEFAULT '[]',
        style_pref    TEXT DEFAULT 'Casual',
        height        TEXT DEFAULT '',
        weight        TEXT DEFAULT ''
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS wardrobe (
        item_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER,
        item_type     TEXT,
        item_name     TEXT,
        color         TEXT DEFAULT '',
        color_family  TEXT DEFAULT 'Neutral',
        style         TEXT DEFAULT '',
        notes         TEXT DEFAULT '',
        times_worn    INTEGER DEFAULT 0,
        last_worn     TEXT DEFAULT '',
        is_favourite  INTEGER DEFAULT 0,
        date_added    TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS outfits (
        outfit_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER,
        occasion      TEXT,
        weather       TEXT,
        items_json    TEXT,
        explanation   TEXT,
        ai_score      INTEGER DEFAULT 0,
        confidence    TEXT DEFAULT '',
        rating        INTEGER DEFAULT 0,
        is_favourite  INTEGER DEFAULT 0,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS worn_log (
        log_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER,
        outfit_id     INTEGER,
        worn_date     TEXT DEFAULT CURRENT_TIMESTAMP,
        occasion      TEXT DEFAULT ''
    )""")

    conn.commit()
    conn.close()

# ── USER ──────────────────────────────────────────────
def get_or_create_user():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users LIMIT 1")
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (name) VALUES ('User')")
        conn.commit()
        c.execute("SELECT * FROM users LIMIT 1")
        user = c.fetchone()
    conn.close()
    return dict(user)

def update_user(user_id, **kwargs):
    conn = get_connection()
    c = conn.cursor()
    fields = ", ".join(f"{k}=?" for k in kwargs)
    values = list(kwargs.values()) + [user_id]
    c.execute(f"UPDATE users SET {fields} WHERE user_id=?", values)
    conn.commit()
    conn.close()

# ── WARDROBE ──────────────────────────────────────────
def get_wardrobe(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM wardrobe WHERE user_id=? ORDER BY item_type, item_name", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_wardrobe_item(user_id, item_type, item_name, color="", color_family="Neutral", style="", notes=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO wardrobe (user_id,item_type,item_name,color,color_family,style,notes) VALUES (?,?,?,?,?,?,?)",
        (user_id, item_type, item_name, color, color_family, style, notes)
    )
    conn.commit()
    iid = c.lastrowid
    conn.close()
    return iid

def delete_wardrobe_item(item_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM wardrobe WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()

def mark_item_worn(item_id):
    conn = get_connection()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("UPDATE wardrobe SET times_worn=times_worn+1, last_worn=? WHERE item_id=?", (today, item_id))
    conn.commit()
    conn.close()

def toggle_wardrobe_favourite(item_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE wardrobe SET is_favourite=1-is_favourite WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()

def get_wardrobe_analytics(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT item_type, COUNT(*) as cnt FROM wardrobe WHERE user_id=? GROUP BY item_type", (user_id,))
    by_type = {r["item_type"]: r["cnt"] for r in c.fetchall()}
    c.execute("SELECT color_family, COUNT(*) as cnt FROM wardrobe WHERE user_id=? GROUP BY color_family ORDER BY cnt DESC", (user_id,))
    by_color = {r["color_family"]: r["cnt"] for r in c.fetchall()}
    c.execute("SELECT item_name, times_worn FROM wardrobe WHERE user_id=? ORDER BY times_worn DESC LIMIT 5", (user_id,))
    most_worn = [dict(r) for r in c.fetchall()]
    c.execute("SELECT item_name, last_worn FROM wardrobe WHERE user_id=? AND last_worn!='' ORDER BY last_worn DESC LIMIT 3", (user_id,))
    recently_worn = [dict(r) for r in c.fetchall()]
    c.execute("SELECT item_name, item_type FROM wardrobe WHERE user_id=? AND times_worn=0", (user_id,))
    never_worn = [dict(r) for r in c.fetchall()]
    conn.close()
    return {
        "by_type": by_type,
        "by_color": by_color,
        "most_worn": most_worn,
        "recently_worn": recently_worn,
        "never_worn": never_worn,
        "total": sum(by_type.values())
    }

# ── OUTFITS ───────────────────────────────────────────
def save_outfit(user_id, occasion, weather, items_dict, explanation, ai_score=0, confidence=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO outfits (user_id,occasion,weather,items_json,explanation,ai_score,confidence) VALUES (?,?,?,?,?,?,?)",
        (user_id, occasion, weather, json.dumps(items_dict), explanation, ai_score, confidence)
    )
    conn.commit()
    oid = c.lastrowid
    conn.close()
    return oid

def get_outfit_history(user_id, limit=20):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM outfits WHERE user_id=? ORDER BY outfit_id DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        try: d["items"] = json.loads(d["items_json"])
        except: d["items"] = {}
        result.append(d)
    return result

def rate_outfit(outfit_id, rating):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE outfits SET rating=? WHERE outfit_id=?", (rating, outfit_id))
    conn.commit()
    conn.close()

def toggle_outfit_favourite(outfit_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE outfits SET is_favourite=1-is_favourite WHERE outfit_id=?", (outfit_id,))
    conn.commit()
    conn.close()

def log_worn(user_id, outfit_id, occasion):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO worn_log (user_id,outfit_id,occasion) VALUES (?,?,?)", (user_id, outfit_id, occasion))
    conn.commit()
    conn.close()

# ── ALIASES (compatibility) ────────────────────────────
# Some app versions call these names — all point to same functions
def get_user(user_id=None):
    return get_or_create_user()

def get_or_create_default_user():
    return get_or_create_user()

def create_user(**kwargs):
    return get_or_create_user()

def get_all_wardrobe_items(user_id):
    return get_wardrobe(user_id)

def add_to_wardrobe(user_id, item_type, item_name, color="", color_family="Neutral", style="", notes=""):
    return add_wardrobe_item(user_id, item_type, item_name, color, color_family, style, notes)

def remove_wardrobe_item(item_id):
    return delete_wardrobe_item(item_id)

def get_saved_outfits(user_id, limit=20):
    return get_outfit_history(user_id, limit)

def save_look(user_id, occasion, weather, items_dict, explanation, ai_score=0, confidence=""):
    return save_outfit(user_id, occasion, weather, items_dict, explanation, ai_score, confidence)