# 👗 DressiFy AI — Personal Fashion Stylist

> **An AI-powered outfit recommendation system that styles you based on your body type, skin tone, occasion, and personal wardrobe.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange?logo=google)](https://ai.google.dev)
[![SQLite](https://img.shields.io/badge/SQLite-Local%20DB-lightblue?logo=sqlite)](https://sqlite.org)

---

## ✨ Features

| Feature | Description |
|---|---|
| 👤 **User Profile** | Gender, age, body type, skin tone, preferred fit, favourite colours |
| 🎯 **12 Occasions** | College, Office, Interview, Wedding, Party, Date, Gym, Vacation + more |
| 🌦️ **Weather-Aware** | Sunny, Rainy, Winter, Humid, Windy — outfit adapts automatically |
| 🧥 **Personal Wardrobe** | Add your own clothes; AI styles outfits from what you own |
| 🧠 **Gemini AI Explanation** | Personalised explanation of why the outfit suits your body + skin tone |
| 💇 **Hairstyle Suggestions** | Occasion-based hair recommendations for Female & Male |
| 📜 **Outfit History** | Save outfits, rate them 1–5 stars, view past looks |
| 📊 **Fashion Catalogue** | 150+ items browseable by type, gender, occasion |
| 💾 **SQLite Database** | Persistent wardrobe + outfit history across sessions |

---

## 🗂️ Project Structure

```
DressiFy/
├── app.py                    # Main Streamlit app (UI + logic)
├── database.py               # SQLite CRUD — users, wardrobe, outfits
├── recommendation_engine.py  # Outfit generation + hairstyle logic
├── fashion_items.csv         # 150+ item dataset
├── requirements.txt
├── schema.sql                # DB schema reference
├── README.md
│
├── components/               # Reusable UI components
├── pages/                    # Multi-page modules (optional)
├── services/                 # External API services
├── utils/                    # Helper utilities
├── models/                   # ML model files
├── datasets/                 # Additional datasets
├── data/                     # Processed data
├── static/                   # Static assets (CSS, images)
└── user_data/                # User-generated content
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/khushii-012/DressiFy.git
cd DressiFy
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Gemini API Key (optional but recommended)
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```
> Get your free key at [Google AI Studio](https://aistudio.google.com). Without it, DressiFy uses smart fallback explanations.

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🧠 How It Works

```
User Profile Input
    ↓
Recommendation Engine
    ├─ Wardrobe DB → Match user's own clothes
    └─ Fashion CSV → Filter by gender / occasion / weather / body type / skin tone
            ↓
    Build Complete Outfit (Top + Bottom + Shoes + Accessories + Outerwear)
            ↓
    Gemini 1.5 Flash → Generate personalised style explanation
            ↓
    Hairstyle Suggestion (based on occasion vibe)
            ↓
    Display + Save to SQLite
```

---

## 📊 Dataset

`fashion_items.csv` contains **150+ clothing items** across 7 categories:

| Category | Count |
|---|---|
| Tops | 40 |
| Bottoms | 28 |
| Shoes | 27 |
| Accessories | 27 |
| Outerwear | 17 |
| Traditional | 12 |
| Dresses | 8 |

Each item is tagged with: `gender`, `style`, `occasion`, `weather`, `body_type`, `skin_tone`, `color_family`, `fit`, `description`

---

## 🛠️ Tech Stack

- **Frontend** — Streamlit (custom dark fashion CSS)
- **AI** — Google Gemini 1.5 Flash (outfit explanation)
- **Database** — SQLite (wardrobe + history persistence)
- **ML** — Pandas filtering + score-based ranking
- **Fonts** — Playfair Display + Inter (Google Fonts)

---

## 📸 App Screenshots

> *[Add screenshots here after deployment]*

---

## 🔮 Future Scope

- [ ] Image upload — analyse colour from photo
- [ ] Budget filter — recommend affordable alternatives
- [ ] WhatsApp daily outfit reminder (Twilio)
- [ ] Community looks — share outfits publicly
- [ ] Seasonal trend updates via web scraping

---

## 👩‍💻 Author

**Khushi** — B.Tech Computer Engineering, RTMNU Nagpur (2023–2027)  
Focused on AI/ML development and real-world impact apps.

---

## 📄 License

MIT License — feel free to fork and improve!
