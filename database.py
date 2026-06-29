import sqlite3

DB_NAME = "fashion.db"

def initialize_database():
    create_tables()
# ---------------------------
# CONNECTION
# ---------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
# CREATE TABLES
# ---------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT DEFAULT 'User',
        age INTEGER DEFAULT 18,
        gender TEXT DEFAULT 'Female',
        skin_tone TEXT DEFAULT 'Medium',
        body_type TEXT DEFAULT 'Average',
        style_preference TEXT DEFAULT 'Casual'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wardrobe (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_type TEXT,
        category TEXT,
        color TEXT,
        style TEXT,
        image_path TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outfits (
        outfit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        occasion TEXT,
        items TEXT,
        rating INTEGER DEFAULT 0,
        explanation TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------------------
# USER
# ---------------------------
def get_or_create_default_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()

    if not user:
        cursor.execute("""
        INSERT INTO users (name, age, gender, skin_tone, body_type, style_preference)
        VALUES (?, ?, ?, ?, ?, ?)
        """, ("User", 18, "Female", "Medium", "Average", "Casual"))

        conn.commit()

        cursor.execute("SELECT * FROM users LIMIT 1")
        user = cursor.fetchone()

    conn.close()
    return dict(user)


def update_user(user_id, name, age, gender, skin_tone, body_type, style_preference):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET name=?, age=?, gender=?, skin_tone=?, body_type=?, style_preference=?
    WHERE user_id=?
    """, (name, age, gender, skin_tone, body_type, style_preference, user_id))

    conn.commit()
    conn.close()

def save_user(user_id, name, age, gender, skin_tone, body_type, style_preference):
    update_user(user_id, name, age, gender, skin_tone, body_type, style_preference)


# ---------------------------
# WARDROBE
# ---------------------------
def get_wardrobe(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM wardrobe WHERE user_id=?", (user_id,))
    items = cursor.fetchall()

    conn.close()
    return [dict(i) for i in items]


def add_wardrobe_item(user_id, item_type, category, color, style, image_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO wardrobe (user_id, item_type, category, color, style, image_path)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, item_type, category, color, style, image_path))

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return item_id


def delete_wardrobe_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM wardrobe WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()


# ---------------------------
# OUTFITS
# ---------------------------
def save_outfit(user_id, occasion, items, explanation):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO outfits (user_id, occasion, items, explanation)
    VALUES (?, ?, ?, ?)
    """, (user_id, occasion, items, explanation))

    conn.commit()
    outfit_id = cursor.lastrowid
    conn.close()

    return outfit_id


def get_outfit_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM outfits WHERE user_id=?
    ORDER BY outfit_id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def update_outfit_rating(outfit_id, rating):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE outfits SET rating=? WHERE outfit_id=?
    """, (rating, outfit_id))

    conn.commit()
    conn.close()