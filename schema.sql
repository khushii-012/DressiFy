-- ============================================
-- Dressify Database Schema
-- ============================================

-- ----------------------------
-- USER PROFILE
-- ----------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    gender TEXT,

    age INTEGER,

    height REAL,

    weight REAL,

    body_type TEXT,

    skin_tone TEXT,

    hair_length TEXT,

    hair_type TEXT,

    preferred_style TEXT,

    favorite_colors TEXT,

    budget TEXT,

    lifestyle TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- USER WARDROBE
-- ----------------------------
CREATE TABLE IF NOT EXISTS wardrobe (

    wardrobe_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    category TEXT,

    sub_category TEXT,

    item_name TEXT,

    color TEXT,

    style TEXT,

    season TEXT,

    occasion TEXT,

    image_path TEXT,

    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
);

-- ----------------------------
-- SAVED OUTFITS
-- ----------------------------
CREATE TABLE IF NOT EXISTS saved_outfits (

    outfit_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    outfit_name TEXT,

    topwear TEXT,

    bottomwear TEXT,

    footwear TEXT,

    accessories TEXT,

    hairstyle TEXT,

    occasion TEXT,

    style TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
);
-- =====================================
-- Wardrobe Categories
-- =====================================

CREATE TABLE IF NOT EXISTS wardrobe_categories (

    category_id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_name TEXT UNIQUE
);