import sqlite3
import json

DB_NAME = "fashion.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT    DEFAULT 'User',
        age        INTEGER DEFAULT 20,
        gender     TEXT    DEFAULT 'Female',
        skin_tone  TEXT    DEFAULT 'Wheatish',
        body_type  TEXT    DEFAULT 'All',
        preferred_fit TEXT DEFAULT 'Regular',
        fav_colors TEXT    DEFAULT '[]',
        style_pref TEXT    DEFAULT 'Casual'
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS wardrobe (
        item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        item_type  TEXT,
        item_name  TEXT,
        color      TEXT,
        style      TEXT,
        notes      TEXT DEFAULT ''
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS outfits (
        outfit_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER,
        occasion    TEXT,
        weather     TEXT,
        items_json  TEXT,
        explanation TEXT,
        rating      INTEGER DEFAULT 0,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()

# ── USER ──────────────────────────────
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

# ── WARDROBE ──────────────────────────
def get_wardrobe(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM wardrobe WHERE user_id=? ORDER BY item_type", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_wardrobe_item(user_id, item_type, item_name, color="", style="", notes=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO wardrobe (user_id,item_type,item_name,color,style,notes) VALUES (?,?,?,?,?,?)",
        (user_id, item_type, item_name, color, style, notes)
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

# ── OUTFITS ───────────────────────────
def save_outfit(user_id, occasion, weather, items_dict, explanation):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO outfits (user_id,occasion,weather,items_json,explanation) VALUES (?,?,?,?,?)",
        (user_id, occasion, weather, json.dumps(items_dict), explanation)
    )
    conn.commit()
    oid = c.lastrowid
    conn.close()
    return oid

def get_outfit_history(user_id, limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM outfits WHERE user_id=? ORDER BY outfit_id DESC LIMIT ?",
        (user_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["items"] = json.loads(d["items_json"])
        except:
            d["items"] = {}
        result.append(d)
    return result

def rate_outfit(outfit_id, rating):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE outfits SET rating=? WHERE outfit_id=?", (rating, outfit_id))
    conn.commit()
    conn.close()