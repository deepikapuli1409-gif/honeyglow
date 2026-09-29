import base64
from pathlib import Path

import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HoneyGlow | Personalized Skincare",
    page_icon="🍯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ASSETS
# =========================================================

BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"

HERO_IMAGE = ASSETS / "honeyglow_hero_image.png"
SKIN_IMAGE = ASSETS / "skin_icon.png"
LIP_IMAGE = ASSETS / "lip_icon.png"
EYE_IMAGE = ASSETS / "eye_icon.png"
BODY_IMAGE = ASSETS / "body_icon.png"


def img_tag(path, css=""):
    p = Path(path)
    if not p.exists():
        return ""
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f'<img src="data:image/png;base64,{b64}" style="{css}">'


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "Home",
    "care": None,
    "skin_type": None,
    "problems": [],
    "user_text": "",
    "results": [],
    "saved": [],
    "selected_product": None,
    "feedback": [],
    "profile": {
        "name": "",
        "age": "",
        "email": "",
        "phone": ""
    }
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CSS - GENERAL (other pages)
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=Poppins:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', Arial, Helvetica, sans-serif;
}

h1, h2, h3, h4, h5, h6 { color: #3a2418 !important; }
p, label, li { color: #3a2418 !important; }

.section-title {
    text-align: center;
    color: #3b2418 !important;
    font-size: 34px;
    font-weight: 800;
    margin-top: 30px;
}

.section-text {
    text-align: center;
    color: #6d5547 !important;
    font-size: 16px;
    margin-bottom: 25px;
}

.product-box {
    background: white;
    border: 1px solid #eadaca;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 6px 18px rgba(60, 40, 20, 0.06);
}

.product-name { font-size: 21px; font-weight: 800; color: #3d2519 !important; }
.product-brand { color: #a56825 !important; font-weight: 700; }
.product-info { color: #604d41 !important; font-size: 14px; line-height: 1.6; }

.match {
    background: #fff0b8;
    color: #704817 !important;
    padding: 6px 10px;
    border-radius: 15px;
    font-weight: 800;
    display: inline-block;
}

.stButton > button {
    background: #e7a52f !important;
    color: #2f1d12 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 10px 20px !important;
}

.stButton > button:hover {
    background: #d99017 !important;
    color: #ffffff !important;
}

input, textarea { color: #302018 !important; background: #ffffff !important; }
[data-baseweb="select"] * { color: #302018 !important; }

.footer {
    text-align: center;
    color: #795f4e !important;
    padding: 35px 10px;
    margin-top: 50px;
    border-top: 1px solid #eadaca;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# CSS - HONEYGLOW DESIGN (nav, hero, cards, steps)
# =========================================================

LEAF = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
        "<path d='M8 92C6 40 40 8 94 6C96 58 58 94 8 92Z' fill='%236f9a3c'/>"
        "<path d='M8 92L78 22' stroke='%23e6efc4' stroke-width='2.5' fill='none'/></svg>")

FLOWER = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
          "<g fill='white' stroke='%23efdfc2' stroke-width='1.5'>"
          "<circle cx='50' cy='22' r='17'/><circle cx='77' cy='42' r='17'/>"
          "<circle cx='67' cy='74' r='17'/><circle cx='33' cy='74' r='17'/>"
          "<circle cx='23' cy='42' r='17'/></g><circle cx='50' cy='50' r='11' fill='%23f2b632'/></svg>")

DRIP = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 60'>"
        "<path d='M0 0H340C330 0 328 14 318 14C306 14 306 34 296 34C286 34 288 12 270 12"
        "C250 12 252 46 238 46C224 46 228 10 200 10C170 10 176 26 160 26C144 26 146 8 120 8"
        "C90 8 96 38 78 38C62 38 66 12 40 12C20 12 22 30 0 30Z' fill='%23f2b632' opacity='.9'/></svg>")

HG_CSS = """
<style>
.stApp {
    background:
        radial-gradient(circle at 8% 92%, rgba(255,226,190,.55), transparent 35%),
        radial-gradient(circle at 95% 60%, rgba(255,236,200,.6), transparent 35%),
        linear-gradient(180deg, #fff9ee 0%, #fff4e4 50%, #fdeedd 100%);
}
header[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu { display: none !important; }
.block-container { padding-top: 1rem !important; max-width: 1250px; }

/* NAV */
.st-key-hg_nav { padding: 6px 4px 10px; }
.hg-logo { font-family: 'Playfair Display', Georgia, serif; font-weight: 900;
           font-size: 34px; color: #5b2d12; line-height: 1.1; }
.hg-logo span, .hg-logo-big span { color: #e0a01d; }
.st-key-hg_nav .stButton > button {
    background: transparent !important; color: #5b321c !important;
    box-shadow: none !important; border-radius: 999px !important;
    font-weight: 500 !important; padding: 8px 14px !important; border: none !important;
}
.st-key-hg_nav .stButton > button[data-testid="stBaseButton-primary"] {
    background: #fbd77a !important; font-weight: 600 !important;
}
.st-key-hg_nav .stButton > button:hover { background: #fde9b3 !important; color: #5b321c !important; }

/* HERO */
.st-key-hg_hero {
    position: relative; overflow: hidden; border-radius: 28px;
    padding: 40px 34px 34px 120px !important; margin: 10px 0 34px;
    border: 1px solid #f3dcae;
    background:
        url("__DRIP__") left 0 top 0 / 340px 60px no-repeat,
        url("__LEAF__") left -25px top 60px / 120px no-repeat,
        url("__FLOWER__") left 18px top 170px / 64px no-repeat,
        url("__LEAF__") left -20px bottom -25px / 130px no-repeat,
        url("__FLOWER__") left 70px bottom 14px / 50px no-repeat,
        url("__LEAF__") right -25px top -25px / 120px no-repeat,
        radial-gradient(circle at 75% 40%, #fff6d2 0%, rgba(255,246,210,0) 55%),
        linear-gradient(120deg, #fde7ae 0%, #fff0d0 45%, #ffe5cd 100%);
}
.hg-hero-text { position: relative; padding-top: 10px; }
.hg-bee { position: absolute; right: 30px; top: -6px; font-size: 30px; }
.hg-logo-big { font-family: 'Playfair Display', Georgia, serif; font-weight: 900;
               font-size: 76px; line-height: 1; color: #5b2d12; }
.hg-tagline { letter-spacing: 4px; font-weight: 600; font-size: 14px;
              color: #4a2a17; margin: 18px 0 14px; }
.hg-hero-p { font-size: 18px; line-height: 1.6; color: #5d493d !important; max-width: 470px; }
.hg-hero-img img {
    width: 100%; border-radius: 24px; display: block;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, #000 22%);
            mask-image: linear-gradient(to right, transparent 0%, #000 22%);
}
.st-key-hg_hero .stButton > button {
    background: #f6c453 !important; color: #3a2210 !important; border: none !important;
    border-radius: 999px !important; padding: 12px 34px !important; font-weight: 600 !important;
    box-shadow: 0 6px 16px rgba(230,160,30,.35) !important;
}
.st-key-hg_hero .stButton > button:hover { background: #eeb43a !important; color: #3a2210 !important; }

/* SECTION TITLES */
.hg-h2 { text-align: center; font-family: 'Playfair Display', Georgia, serif;
         font-weight: 700; font-size: 34px; color: #5b2d12; margin: 8px 0 22px; }
.hg-h2 span { font-size: 22px; margin: 0 12px; }

/* CATEGORY CARDS */
[class*="st-key-hg_card_"] {
    border-radius: 20px; padding: 24px 16px 22px !important; text-align: center;
    border: 1px solid rgba(214,170,110,.35); box-shadow: 0 8px 22px rgba(120,80,30,.08);
}
.st-key-hg_card_0 { background: #fdf0e0; }
.st-key-hg_card_1 { background: #fdebe4; }
.st-key-hg_card_2 { background: #eef3ee; }
.st-key-hg_card_3 { background: #edf3f1; }
.hg-ico { width: 96px; height: 96px; margin: 0 auto 10px; border-radius: 50%;
          background: rgba(255,255,255,.75); display: flex; align-items: center; justify-content: center; }
.hg-ico img { width: 72px; height: 72px; object-fit: contain; }
.hg-card-title { font-family: 'Playfair Display', Georgia, serif; font-weight: 700;
                 font-size: 24px; color: #4a2413; margin-bottom: 6px; }
.hg-card-text { font-size: 14px; line-height: 1.5; color: #6a5549 !important;
                min-height: 44px; margin-bottom: 8px; }
[class*="st-key-hg_card_"] .stButton { display: flex; justify-content: center; }
[class*="st-key-hg_card_"] .stButton > button {
    background: #f6c453 !important; color: #3a2210 !important; border-radius: 10px !important;
    font-size: 14px !important; font-weight: 600 !important; padding: 8px 18px !important;
}
[class*="st-key-hg_card_"] .stButton > button:hover { background: #eeb43a !important; color: #3a2210 !important; }

/* HOW IT WORKS */
.hg-works { margin-top: 34px; padding: 30px 20px 34px; border-radius: 28px;
            background: linear-gradient(180deg, rgba(255,240,205,.9), rgba(255,246,225,.6)); }
.hg-steps { display: flex; justify-content: center; align-items: center; gap: 22px; flex-wrap: wrap; }
.hg-step { display: flex; align-items: center; gap: 14px; max-width: 290px; }
.hg-step-ico { flex: 0 0 68px; width: 68px; height: 68px; border-radius: 50%; background: #fde7b5;
               display: flex; align-items: center; justify-content: center; font-size: 30px; }
.hg-step b { color: #4a2413; font-size: 16px; }
.hg-step p { margin: 3px 0 0; font-size: 13px; line-height: 1.45; color: #6a5549 !important; }
.hg-arrow { color: #f0a63a; font-size: 26px; }
</style>
""".replace("__LEAF__", LEAF).replace("__FLOWER__", FLOWER).replace("__DRIP__", DRIP)

st.markdown(HG_CSS, unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

CARE_TYPES = {
    "Skin Care": {
        "image": SKIN_IMAGE,
        "description": "Find products for acne, dark spots, dryness, oiliness and more.",
        "emoji": "🧴"
    },
    "Lip Care": {
        "image": LIP_IMAGE,
        "description": "Explore products for dry, chapped and dull lips.",
        "emoji": "💋"
    },
    "Eye Care": {
        "image": EYE_IMAGE,
        "description": "Explore gentle care options for common eye-area concerns.",
        "emoji": "👁️"
    },
    "Body Care": {
        "image": BODY_IMAGE,
        "description": "Find body-care products for dryness and uneven texture.",
        "emoji": "🧼"
    }
}

SKIN_TYPES = ["Normal", "Dry", "Oily", "Combination", "Sensitive"]

PROBLEMS = [
    "Acne & Pimples", "Blackheads", "Whiteheads", "Open / Large Pores",
    "Dark Spots", "Hyperpigmentation", "Post-Acne Marks", "Uneven Skin Tone",
    "Dull Skin", "Dryness", "Dehydrated Skin", "Excess Oil", "Redness",
    "Skin Sensitivity", "Fine Lines", "Wrinkles", "Premature Aging",
    "Sun Damage", "Rough / Uneven Texture", "Acne Scars"
]

PRODUCTS = [
    {
        "brand": "Minimalist",
        "name": "2% Salicylic Acid Face Serum",
        "category": "Skin Care",
        "skin": ["Oily", "Combination"],
        "problems": ["Acne & Pimples", "Blackheads", "Excess Oil"],
        "ingredients": "Salicylic Acid, Zinc PCA",
        "price": "₹549",
        "rating": 4.4,
        "reviews": 12500,
        "description": "A lightweight serum designed for oily and acne-prone skin.",
    },
    {
        "brand": "The Derma Co",
        "name": "2% Salicylic Acid Face Wash",
        "category": "Skin Care",
        "skin": ["Oily", "Combination"],
        "problems": ["Acne & Pimples", "Blackheads", "Excess Oil"],
        "ingredients": "Salicylic Acid, Witch Hazel",
        "price": "₹299",
        "rating": 4.3,
        "reviews": 18200,
        "description": "A cleansing formula for excess oil and blemish-prone skin.",
    },
    {
        "brand": "Dot & Key",
        "name": "Cica Calming Skin Repair Serum",
        "category": "Skin Care",
        "skin": ["Sensitive", "Dry", "Combination"],
        "problems": ["Redness", "Skin Sensitivity", "Dryness"],
        "ingredients": "Cica, Ceramides, Hyaluronic Acid",
        "price": "₹695",
        "rating": 4.5,
        "reviews": 8300,
        "description": "A soothing serum focused on hydration and skin comfort.",
    },
    {
        "brand": "Plum",
        "name": "10% Niacinamide Face Serum",
        "category": "Skin Care",
        "skin": ["Oily", "Combination", "Normal"],
        "problems": ["Dark Spots", "Excess Oil", "Uneven Skin Tone"],
        "ingredients": "Niacinamide, Rice Water",
        "price": "₹575",
        "rating": 4.4,
        "reviews": 9700,
        "description": "A brightening and balancing serum for uneven-looking skin.",
    },
    {
        "brand": "Foxtale",
        "name": "Daily Duet Cleanser",
        "category": "Skin Care",
        "skin": ["Oily", "Combination", "Normal"],
        "problems": ["Acne & Pimples", "Excess Oil", "Dull Skin"],
        "ingredients": "Niacinamide, Gentle Cleansers",
        "price": "₹349",
        "rating": 4.5,
        "reviews": 6200,
        "description": "A gentle daily cleanser designed for a fresh skin feel.",
    },
    {
        "brand": "Deconstruct",
        "name": "Brightening Serum",
        "category": "Skin Care",
        "skin": ["Normal", "Combination", "Oily"],
        "problems": ["Dark Spots", "Hyperpigmentation", "Dull Skin"],
        "ingredients": "Alpha Arbutin, Niacinamide",
        "price": "₹599",
        "rating": 4.3,
        "reviews": 5100,
        "description": "A simple brightening formula for uneven-looking skin.",
    },
    {
        "brand": "Dr. Sheth's",
        "name": "Centella & Niacinamide Serum",
        "category": "Skin Care",
        "skin": ["Sensitive", "Combination", "Oily"],
        "problems": ["Redness", "Acne & Pimples", "Uneven Skin Tone"],
        "ingredients": "Centella, Niacinamide",
        "price": "₹649",
        "rating": 4.4,
        "reviews": 4300,
        "description": "A calming serum combining soothing and balancing ingredients.",
    },
    {
        "brand": "Re'equil",
        "name": "Oil Control Face Wash",
        "category": "Skin Care",
        "skin": ["Oily", "Combination"],
        "problems": ["Excess Oil", "Acne & Pimples"],
        "ingredients": "Gentle Cleansing Agents, Botanical Extracts",
        "price": "₹450",
        "rating": 4.2,
        "reviews": 7300,
        "description": "A cleanser formulated for a clean, balanced skin feel.",
    },
    {
        "brand": "Aqualogica",
        "name": "Hydrate+ Face Moisturizer",
        "category": "Skin Care",
        "skin": ["Dry", "Normal", "Combination"],
        "problems": ["Dryness", "Dehydrated Skin"],
        "ingredients": "Hyaluronic Acid, Glycerin",
        "price": "₹499",
        "rating": 4.4,
        "reviews": 8100,
        "description": "A hydrating moisturizer for comfortable everyday use.",
    },
    {
        "brand": "Mamaearth",
        "name": "Vitamin C Face Serum",
        "category": "Skin Care",
        "skin": ["Normal", "Combination", "Oily"],
        "problems": ["Dull Skin", "Dark Spots", "Uneven Skin Tone"],
        "ingredients": "Vitamin C, Turmeric",
        "price": "₹599",
        "rating": 4.1,
        "reviews": 15200,
        "description": "A brightening-focused serum for dull-looking skin.",
    },
    {
        "brand": "Cetaphil",
        "name": "Gentle Skin Cleanser",
        "category": "Skin Care",
        "skin": ["Dry", "Sensitive", "Normal"],
        "problems": ["Dryness", "Skin Sensitivity", "Redness"],
        "ingredients": "Glycerin, Gentle Cleansing Agents",
        "price": "₹399",
        "rating": 4.6,
        "reviews": 22000,
        "description": "A gentle cleanser designed for sensitive and dry skin.",
    },
    {
        "brand": "CeraVe",
        "name": "Moisturising Cream",
        "category": "Skin Care",
        "skin": ["Dry", "Normal", "Sensitive"],
        "problems": ["Dryness", "Dehydrated Skin", "Skin Sensitivity"],
        "ingredients": "Ceramides, Hyaluronic Acid",
        "price": "₹899",
        "rating": 4.6,
        "reviews": 19800,
        "description": "A barrier-supporting moisturizer with ceramides and hydration.",
    },
    {
        "brand": "Neutrogena",
        "name": "Hydro Boost Water Gel",
        "category": "Skin Care",
        "skin": ["Oily", "Combination", "Normal"],
        "problems": ["Dehydrated Skin", "Dryness"],
        "ingredients": "Hyaluronic Acid, Glycerin",
        "price": "₹950",
        "rating": 4.5,
        "reviews": 17600,
        "description": "A lightweight gel moisturizer for hydrated-feeling skin.",
    },
    {
        "brand": "Bioderma",
        "name": "Atoderm Intensive Baume",
        "category": "Skin Care",
        "skin": ["Dry", "Sensitive"],
        "problems": ["Dryness", "Skin Sensitivity"],
        "ingredients": "Ceramides, Lipids",
        "price": "₹1099",
        "rating": 4.5,
        "reviews": 8400,
        "description": "A rich moisturizer for dry and sensitive skin.",
    },
    {
        "brand": "La Roche-Posay",
        "name": "Effaclar Duo",
        "category": "Skin Care",
        "skin": ["Oily", "Combination"],
        "problems": ["Acne & Pimples", "Blackheads", "Excess Oil"],
        "ingredients": "Salicylic Acid, Niacinamide",
        "price": "₹1450",
        "rating": 4.4,
        "reviews": 7100,
        "description": "A blemish-focused formula for oily and combination skin.",
    },
    {
        "brand": "COSRX",
        "name": "Advanced Snail 96 Mucin Essence",
        "category": "Skin Care",
        "skin": ["Dry", "Normal", "Combination"],
        "problems": ["Dehydrated Skin", "Uneven Skin Tone", "Dull Skin"],
        "ingredients": "Snail Mucin, Hyaluronic Acid",
        "price": "₹1250",
        "rating": 4.7,
        "reviews": 26500,
        "description": "A hydrating essence for a smoother, comfortable skin feel.",
    },
    {
        "brand": "Beauty of Joseon",
        "name": "Glow Serum",
        "category": "Skin Care",
        "skin": ["Normal", "Combination", "Dry"],
        "problems": ["Dull Skin", "Dark Spots", "Uneven Skin Tone"],
        "ingredients": "Propolis, Niacinamide",
        "price": "₹1150",
        "rating": 4.6,
        "reviews": 14300,
        "description": "A glow-focused serum combining propolis and niacinamide.",
    },
    {
        "brand": "The Ordinary",
        "name": "Alpha Arbutin 2% + HA",
        "category": "Skin Care",
        "skin": ["Normal", "Combination", "Oily"],
        "problems": ["Dark Spots", "Hyperpigmentation", "Uneven Skin Tone"],
        "ingredients": "Alpha Arbutin, Hyaluronic Acid",
        "price": "₹850",
        "rating": 4.5,
        "reviews": 16900,
        "description": "A targeted brightening serum for uneven-looking skin.",
    },
    {
        "brand": "Clinique",
        "name": "Moisture Surge 100H",
        "category": "Skin Care",
        "skin": ["Dry", "Normal", "Combination"],
        "problems": ["Dryness", "Dehydrated Skin"],
        "ingredients": "Hyaluronic Acid, Aloe",
        "price": "₹2200",
        "rating": 4.5,
        "reviews": 6200,
        "description": "A hydrating gel-cream for long-lasting moisture.",
    },

    # Lip
    {
        "brand": "Minimalist",
        "name": "Lip Treatment Balm",
        "category": "Lip Care",
        "skin": ["All"],
        "problems": ["Dryness"],
        "ingredients": "Ceramides, Squalane, Vitamin E",
        "price": "₹299",
        "rating": 4.4,
        "reviews": 3500,
        "description": "A nourishing balm for dry lips.",
    },
    {
        "brand": "Dot & Key",
        "name": "Gloss Boss Lip Balm",
        "category": "Lip Care",
        "skin": ["All"],
        "problems": ["Dryness"],
        "ingredients": "Shea Butter, Cocoa Butter",
        "price": "₹249",
        "rating": 4.3,
        "reviews": 4800,
        "description": "A moisturizing lip balm with a glossy finish.",
    },
    {
        "brand": "NIVEA",
        "name": "Original Care Lip Balm",
        "category": "Lip Care",
        "skin": ["All"],
        "problems": ["Dryness"],
        "ingredients": "Shea Butter, Oils",
        "price": "₹180",
        "rating": 4.4,
        "reviews": 12000,
        "description": "An everyday moisturizing lip balm.",
    },

    # Eye
    {
        "brand": "The Ordinary",
        "name": "Caffeine Solution 5% + EGCG",
        "category": "Eye Care",
        "skin": ["All"],
        "problems": ["Dull Skin"],
        "ingredients": "Caffeine, EGCG",
        "price": "₹750",
        "rating": 4.3,
        "reviews": 9200,
        "description": "A lightweight eye-area serum.",
    },
    {
        "brand": "Clinique",
        "name": "All About Eyes",
        "category": "Eye Care",
        "skin": ["All"],
        "problems": ["Dryness"],
        "ingredients": "Hydrating Ingredients, Antioxidants",
        "price": "₹2500",
        "rating": 4.5,
        "reviews": 5400,
        "description": "A moisturizing eye cream for the delicate eye area.",
    },

    # Body
    {
        "brand": "CeraVe",
        "name": "SA Smoothing Cream",
        "category": "Body Care",
        "skin": ["Dry", "Normal"],
        "problems": ["Rough / Uneven Texture", "Dryness"],
        "ingredients": "Salicylic Acid, Ceramides, Urea",
        "price": "₹1300",
        "rating": 4.5,
        "reviews": 7100,
        "description": "A smoothing body moisturizer for rough-feeling skin.",
    },
    {
        "brand": "Fixderma",
        "name": "Nigrifix Body Lotion",
        "category": "Body Care",
        "skin": ["Dry", "Normal", "Combination"],
        "problems": ["Rough / Uneven Texture", "Dryness"],
        "ingredients": "Lactic Acid, Urea",
        "price": "₹475",
        "rating": 4.3,
        "reviews": 3200,
        "description": "A body lotion designed for smoother-feeling skin.",
    },
    {
        "brand": "Vaseline",
        "name": "Advanced Repair Lotion",
        "category": "Body Care",
        "skin": ["Dry", "Normal"],
        "problems": ["Dryness"],
        "ingredients": "Glycerin, Petrolatum",
        "price": "₹350",
        "rating": 4.5,
        "reviews": 18500,
        "description": "An everyday moisturizing body lotion."
    }
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def go(page):
    st.session_state.page = page
    st.rerun()


def analyze_text(text):
    text_lower = text.lower()

    detected_skin = None
    detected_problems = []

    skin_words = {
        "oily": "Oily",
        "dry skin": "Dry",
        "dry": "Dry",
        "combination": "Combination",
        "sensitive": "Sensitive",
        "normal skin": "Normal"
    }

    for word, skin in skin_words.items():
        if word in text_lower:
            detected_skin = skin
            break

    keywords = {
        "pimples": "Acne & Pimples",
        "acne": "Acne & Pimples",
        "blackheads": "Blackheads",
        "whiteheads": "Whiteheads",
        "pores": "Open / Large Pores",
        "dark spots": "Dark Spots",
        "pigmentation": "Hyperpigmentation",
        "hyperpigmentation": "Hyperpigmentation",
        "acne marks": "Post-Acne Marks",
        "marks": "Post-Acne Marks",
        "uneven tone": "Uneven Skin Tone",
        "dull": "Dull Skin",
        "dryness": "Dryness",
        "dehydrated": "Dehydrated Skin",
        "oil": "Excess Oil",
        "redness": "Redness",
        "sensitive": "Skin Sensitivity",
        "fine lines": "Fine Lines",
        "wrinkles": "Wrinkles",
        "aging": "Premature Aging",
        "sun damage": "Sun Damage",
        "rough": "Rough / Uneven Texture",
        "acne scars": "Acne Scars"
    }

    for word, problem in keywords.items():
        if word in text_lower and problem not in detected_problems:
            detected_problems.append(problem)

    return detected_skin, detected_problems


def recommend_products(care, skin_type, problems, text):
    detected_skin, detected_problems = analyze_text(text)

    final_skin = skin_type or detected_skin
    final_problems = list(dict.fromkeys(problems + detected_problems))

    candidates = [p for p in PRODUCTS if p["category"] == care]

    scored = []

    for product in candidates:
        score = 0

        if final_skin:
            if final_skin in product["skin"] or "All" in product["skin"]:
                score += 35

        for problem in final_problems:
            if problem in product["problems"]:
                score += 15

        score += product["rating"] * 7
        score += (len(product["name"]) % 5)

        scored.append((score, product))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {**product, "match": min(98, round(score))}
        for score, product in scored[:8]
    ]


def product_icon(category):
    if category == "Skin Care":
        return "🧴"
    if category == "Lip Care":
        return "💋"
    if category == "Eye Care":
        return "👁️"
    return "🧼"


# =========================================================
# NAVIGATION
# =========================================================

NAV_ITEMS = [
    ("🏠 Home", "Home"),
    ("👤 Profile", "Profile"),
    ("🔖 Saved", "Saved"),
    ("💬 Feedback", "Feedback"),
]

with st.container(key="hg_nav"):
    nav_cols = st.columns([2.6, 1, 1, 1, 1.1])

    with nav_cols[0]:
        st.markdown(
            '<div class="hg-logo">Honey<span>Glow</span></div>',
            unsafe_allow_html=True
        )

    for col, (label, page_name) in zip(nav_cols[1:], NAV_ITEMS):
        with col:
            is_active = st.session_state.page == page_name
            if st.button(
                label,
                key=f"hg_nav_{page_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                go(page_name)


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    # ---------- HERO ----------
    with st.container(key="hg_hero"):
        left, right = st.columns([1.05, 0.95], vertical_alignment="center")

        with left:
            st.markdown(
                '<div class="hg-hero-text"><span class="hg-bee">🐝</span>'
                '<div class="hg-logo-big">Honey<span>Glow</span></div>'
                '<div class="hg-tagline">PERSONALIZED SKINCARE • POWERED BY NLP</div>'
                '<p class="hg-hero-p">Discover skincare recommendations made around '
                'your skin, your concerns and your preferences.</p></div>',
                unsafe_allow_html=True
            )

            if st.button("Get Started  →", key="hg_get_started"):
                go("Care")

        with right:
            hero = img_tag(HERO_IMAGE)
            st.markdown(
                f'<div class="hg-hero-img">{hero}</div>',
                unsafe_allow_html=True
            )

    # ---------- CATEGORY CARDS ----------
    st.markdown(
        '<div class="hg-h2"><span>🌿</span>What would you like to care for?'
        '<span>🌿</span></div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4, gap="medium")

    for i, (care, data) in enumerate(CARE_TYPES.items()):
        with cols[i]:
            with st.container(key=f"hg_card_{i}"):
                icon = img_tag(data["image"])
                st.markdown(
                    f'<div class="hg-ico">{icon}</div>'
                    f'<div class="hg-card-title">{care}</div>'
                    f'<div class="hg-card-text">{data["description"]}</div>',
                    unsafe_allow_html=True
                )

                if st.button(f"Explore {care} →", key=f"hg_explore_{i}"):
                    st.session_state.care = care
                    go("Care")

    # ---------- HOW IT WORKS ----------
    steps = [
        ("💬", "1. Tell Us", "Describe your skin type and concerns in simple words."),
        ("🧠", "2. NLP Understands", "HoneyGlow identifies important skin concerns from your text."),
        ("✨", "3. Get Recommendations", "Receive multiple products matched to your requirements."),
    ]

    parts = []
    for n, (ico, title, text) in enumerate(steps):
        parts.append(
            f'<div class="hg-step"><div class="hg-step-ico">{ico}</div>'
            f'<div><b>{title}</b><p>{text}</p></div></div>'
        )
        if n < len(steps) - 1:
            parts.append('<div class="hg-arrow">→</div>')

    st.markdown(
        '<div class="hg-works"><div class="hg-h2"><span>🌿</span>How HoneyGlow Works'
        '<span>🌿</span></div><div class="hg-steps">' + "".join(parts) + '</div></div>',
        unsafe_allow_html=True
    )


# =========================================================
# CARE SELECTION
# =========================================================

elif st.session_state.page == "Care":

    st.markdown(
        '<div class="section-title">What would you like to care for?</div>'
        '<div class="section-text">Choose one category to continue.</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    for i, (care, data) in enumerate(CARE_TYPES.items()):
        with cols[i]:

            if data["image"].exists():
                st.image(str(data["image"]), width=150)

            st.subheader(f"{data['emoji']} {care}")
            st.write(data["description"])

            if st.button(
                f"Select {care}",
                key=f"care_select_{care}",
                use_container_width=True
            ):
                st.session_state.care = care

                if care == "Skin Care":
                    go("SkinType")
                else:
                    st.session_state.skin_type = None
                    st.session_state.problems = []
                    go("Concern")


# =========================================================
# SKIN TYPE
# =========================================================

elif st.session_state.page == "SkinType":

    st.markdown(
        '<div class="section-title">What is your skin type?</div>'
        '<div class="section-text">'
        'Choose the option that best describes your skin.'
        '</div>',
        unsafe_allow_html=True
    )

    selected = st.radio(
        "Skin Type",
        SKIN_TYPES,
        index=SKIN_TYPES.index(st.session_state.skin_type)
        if st.session_state.skin_type in SKIN_TYPES else 0,
        horizontal=True
    )

    st.session_state.skin_type = selected

    if st.button("Continue →", use_container_width=True):
        go("Concern")


# =========================================================
# CONCERN
# =========================================================

elif st.session_state.page == "Concern":

    care = st.session_state.care

    st.markdown(
        f'<div class="section-title">{product_icon(care)} Tell us about your concern</div>'
        '<div class="section-text">'
        'Select one or more concerns. You can also describe them in your own words.'
        '</div>',
        unsafe_allow_html=True
    )

    if care == "Skin Care":

        selected_problems = st.multiselect(
            "Select your skin concerns",
            PROBLEMS,
            default=st.session_state.problems
        )

        st.session_state.problems = selected_problems

    else:

        selected_problems = st.multiselect(
            "Select concerns",
            [
                "Dryness",
                "Dehydrated Skin",
                "Dull Skin",
                "Rough / Uneven Texture",
                "Redness",
                "Skin Sensitivity"
            ],
            default=st.session_state.problems
        )

        st.session_state.problems = selected_problems

    st.write("### Describe your concern")

    user_text = st.text_area(
        "For example:",
        value=st.session_state.user_text,
        placeholder="I have oily skin, pimples and dark spots...",
        height=130
    )

    st.session_state.user_text = user_text

    if user_text.strip():

        detected_skin, detected_problems = analyze_text(user_text)

        if detected_skin:
            st.success(f"NLP detected skin type: {detected_skin}")

        if detected_problems:
            st.success(
                "NLP detected concerns: "
                + ", ".join(detected_problems)
            )

    if st.button(
        "✨ Get Personalized Recommendations",
        use_container_width=True
    ):

        results = recommend_products(
            care,
            st.session_state.skin_type,
            st.session_state.problems,
            st.session_state.user_text
        )

        st.session_state.results = results
        go("Results")


# =========================================================
# RESULTS
# =========================================================

elif st.session_state.page == "Results":

    st.markdown(
        '<div class="section-title">✨ Your Personalized Results</div>'
        '<div class="section-text">'
        'These products were matched to the information you provided.'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.results:

        st.warning("No recommendations found.")

        if st.button("Start Again"):
            go("Care")

    else:

        for index, product in enumerate(st.session_state.results):

            with st.container():

                col1, col2, col3 = st.columns([0.18, 0.57, 0.25])

                with col1:
                    st.markdown(
                        f"<div style='font-size:55px;text-align:center;'>"
                        f"{product_icon(product['category'])}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                with col2:

                    st.markdown(
                        f"""
                        <div class="product-box">
                        <div class="product-brand">{product['brand']}</div>
                        <div class="product-name">{product['name']}</div>
                        <div class="product-info">
                        ⭐ {product['rating']} ({product['reviews']:,} reviews)
                        <br>
                        💰 {product['price']}
                        <br>
                        🧪 {product['ingredients']}
                        <br><br>
                        {product['description']}
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:

                    st.markdown(
                        f'<div class="match">HoneyGlow Match: {product["match"]}%</div>',
                        unsafe_allow_html=True
                    )

                    st.write("")

                    if st.button(
                        "View Details",
                        key=f"details_{index}",
                        use_container_width=True
                    ):
                        st.session_state.selected_product = product
                        go("Product")

                    saved = product["name"] in [
                        p["name"] for p in st.session_state.saved
                    ]

                    save_text = "✓ Saved" if saved else "🔖 Save"

                    if st.button(
                        save_text,
                        key=f"save_{index}",
                        use_container_width=True
                    ):

                        if not saved:
                            st.session_state.saved.append(product)
                            st.success("Product saved!")
                        else:
                            st.info("Already saved.")

                st.divider()


# =========================================================
# PRODUCT DETAILS
# =========================================================

elif st.session_state.page == "Product":

    product = st.session_state.selected_product

    if product is None:

        st.warning("No product selected.")

        if st.button("Back to Results"):
            go("Results")

    else:

        if st.button("← Back to Results"):
            go("Results")

        st.markdown(
            f'<div class="section-title">{product["name"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="section-text">{product["brand"]}</div>',
            unsafe_allow_html=True
        )

        left, right = st.columns([0.35, 0.65])

        with left:
            st.markdown(
                f"""
                <div style="
                    background:#fff;
                    border:1px solid #eadaca;
                    border-radius:25px;
                    padding:60px 20px;
                    text-align:center;
                    font-size:100px;">
                    {product_icon(product["category"])}
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.subheader(product["name"])

            st.write(f"**Brand:** {product['brand']}")

            st.write(
                f"⭐ **{product['rating']} / 5** "
                f"from {product['reviews']:,} reviews"
            )

            st.write(f"### {product['price']}")

            st.write(
                f"**HoneyGlow Match: {product['match'] if 'match' in product else 90}%**"
            )

            st.write("### Key Ingredients")

            st.info(product["ingredients"])

            st.write("### About this product")

            st.write(product["description"])

            st.write("### Why HoneyGlow recommended it")

            st.write(
                "This product was selected because its category, "
                "skin compatibility, concerns and ingredient profile "
                "match information from your skincare journey."
            )

            save = st.button("🔖 Save Product", use_container_width=True)

            if save:

                existing = [p["name"] for p in st.session_state.saved]

                if product["name"] not in existing:
                    st.session_state.saved.append(product)
                    st.success("Saved to your collection.")
                else:
                    st.info("Already saved.")


# =========================================================
# SAVED
# =========================================================

elif st.session_state.page == "Saved":

    st.markdown(
        '<div class="section-title">🔖 Saved Products</div>'
        '<div class="section-text">'
        'Your saved skincare products in one place.'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.saved:

        st.info(
            "You haven't saved any products yet. "
            "Explore recommendations and save products you like."
        )

        if st.button("Explore Products"):
            go("Care")

    else:

        for index, product in enumerate(st.session_state.saved):

            st.markdown(
                f"""
                <div class="product-box">
                <div class="product-brand">{product['brand']}</div>
                <div class="product-name">
                {product_icon(product['category'])} {product['name']}
                </div>
                <div class="product-info">
                ⭐ {product['rating']} • {product['reviews']:,} reviews
                <br>
                💰 {product['price']}
                <br>
                🧪 {product['ingredients']}
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("View Product", key=f"saved_view_{index}"):
                st.session_state.selected_product = product
                go("Product")


# =========================================================
# PROFILE
# =========================================================

elif st.session_state.page == "Profile":

    st.markdown(
        '<div class="section-title">👤 Your HoneyGlow Profile</div>'
        '<div class="section-text">'
        'Keep your basic information and skincare preferences together.'
        '</div>',
        unsafe_allow_html=True
    )

    profile = st.session_state.profile

    name = st.text_input("Name", value=profile["name"])
    age = st.text_input("Age", value=profile["age"])
    email = st.text_input("Email", value=profile["email"])
    phone = st.text_input("Phone Number", value=profile["phone"])

    if st.button("Save Profile", use_container_width=True):

        st.session_state.profile = {
            "name": name,
            "age": age,
            "email": email,
            "phone": phone
        }

        st.success("Profile saved successfully!")

    st.divider()

    st.subheader("Skincare Preferences")

    if st.session_state.skin_type:
        st.write(f"**Selected Skin Type:** {st.session_state.skin_type}")
    else:
        st.write("No skin type selected yet.")

    if st.session_state.problems:
        st.write(
            "**Selected Concerns:** "
            + ", ".join(st.session_state.problems)
        )
    else:
        st.write("No concerns selected yet.")

    st.divider()

    st.subheader("Your Activity")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Saved Products", len(st.session_state.saved))

    with c2:
        st.metric("Recommendations", len(st.session_state.results))

    with c3:
        st.metric("Feedback", len(st.session_state.feedback))


# =========================================================
# FEEDBACK
# =========================================================

elif st.session_state.page == "Feedback":

    st.markdown(
        '<div class="section-title">💬 Share Your Feedback</div>'
        '<div class="section-text">'
        'Your feedback helps HoneyGlow understand what users find useful.'
        '</div>',
        unsafe_allow_html=True
    )

    feedback_rating = st.slider(
        "How useful was your HoneyGlow experience?",
        1,
        5,
        5
    )

    feedback_text = st.text_area(
        "Tell us more",
        placeholder="Example: The recommendations matched my concerns...",
        height=150
    )

    if st.button("Submit Feedback", use_container_width=True):

        sentiment = "Positive"

        negative_words = [
            "bad", "poor", "wrong", "not useful", "disappointed", "confusing"
        ]

        if any(word in feedback_text.lower() for word in negative_words):
            sentiment = "Needs Improvement"

        st.session_state.feedback.append(
            {
                "rating": feedback_rating,
                "text": feedback_text,
                "sentiment": sentiment
            }
        )

        st.success("Thank you! Your feedback has been recorded.")

        st.info(f"Feedback NLP signal: {sentiment}")

    if st.session_state.feedback:

        st.divider()

        st.subheader("Your Previous Feedback")

        for item in reversed(st.session_state.feedback):

            st.write(f"⭐ {item['rating']}/5 — {item['sentiment']}")

            if item["text"]:
                st.write(item["text"])


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🍯 <b>HoneyGlow</b><br>
        Personalized skincare recommendations powered by NLP.
    </div>
    """,
    unsafe_allow_html=True
)