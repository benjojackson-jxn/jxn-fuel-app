import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="JXN Fuel Calculator", page_icon="⚡")

# --- CUSTOM BRANDING (Electric Blue & Black) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Text Visibility - Forces all standard text to White */
    p, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Headers (Electric Blue) */
    h1, h2, h3, h4 {
        color: #009CDE !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #009CDE;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0084BD;
        color: white;
    }

    /* --- FORCE INPUTS TO DARK MODE (The Fix) --- */
    
    /* 1. The Select Box (Dropdown) & Text Inputs */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1E1E1E !important;
        color: white !important;
        border-color: #444444 !important;
    }
    
    /* 2. The Text INSIDE the Select Box */
    div[data-baseweb="select"] span {
        color: white !important;
    }

    /* 3. The Number Input Box */
    input[type="number"] {
        color: white !important;
        background-color: #1E1E1E !important;
    }

    /* 4. The Dropdown Menu Options (When you click it) */
    ul[data-baseweb="menu"] {
        background-color: #1E1E1E !important;
    }

    /* Info Box Styling */
    .stInfo {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border-left-color: #009CDE;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("⚡ JXN PERFORMANCE FUEL")
st.write("Calculate nutrition needs specifically for the **growing athlete**.")
st.markdown("---")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    sex = st.radio("Sex", ["Male", "Female"])
    age = st.slider("Age", 12, 18, 16)
    weight_lbs = st.number_input("Weight (lbs)", min_value=70, max_value=350, value=145)

with col2:
    # UPDATED: Labels based on Weekly Load / Schedule
    activity_profile = st.selectbox("Select Weekly Workload", 
        [
            "LEVEL 1: Standard (3-4x/week | Volleyball/Skill)", 
            "LEVEL 2: Heavy (5-6x/week | Hockey/Contact/Running)",
            "LEVEL 3: Peak (Tournament Weekend | Two-a-Days)"
        ])
    
    goal = st.radio("Primary Goal", ["Performance/Maintenance", "Gain Size/Growth Spurt"])

# --- THE LOGIC ENGINE ---

# 1. Convert Weight
weight_kg = weight_lbs / 2.20462

# 2. Base Metabolic Rate (Schofield Equation)
if sex == "Male":
    bmr = (17.686 * weight_kg) + 658.2
else:
    bmr = (13.384 * weight_kg) + 692.6

# 3. Load Multipliers (Tuned for Safety & Accuracy)
if "LEVEL 1" in activity_profile:
    # Standard Practice days. 
    multiplier = 1.65
    note = "Standard Load. Good for practice days or skill sports (Volleyball/Baseball)."

elif "LEVEL 2" in activity_profile:
    # This is the "Sweet Spot" for your Hockey players and Runners.
    multiplier = 1.9
    note = "High Load. Use this for Hockey season, heavy lifting blocks, or distance running."

else:
    # LEVEL 3 (Peak)
    # Lowered slightly to 2.1 to prevent massive over-estimation.
    multiplier = 2.1 
    note = "Peak Load. ONLY use this for 3-game tournament weekends or double-day camps."

tdee = bmr * multiplier

# 4. The Growth Surplus
if "Gain Size" in goal:
    tdee += 400

# 5. Macro Split (High Performance Bias)
# 50% Carbs (Fuel) / 25% Protein (Repair) / 25% Fat (Hormones)
protein_cals = tdee * 0.25
carb_cals = tdee * 0.50
fat_cals = tdee * 0.25

# 6. Hand Portion Conversion
# Protein: ~150 cals per Palm
# Carbs: ~120 cals per Cupped Hand
# Fats: ~100 cals per Thumb
palms = round(protein_cals / 150)
cupped_hands = round(carb_cals / 120)
thumbs = round(fat_cals / 100)

# --- OUTPUT DISPLAY ---
if st.button("CALCULATE MY NUMBERS 🚀"):
    st.markdown("---")
    
    # Total Calories Header
    st.subheader(f"🔥 Daily Target: {int(tdee)} Calories")
    
    # 1. DISPLAY THE NOTE (This is the new part)
    st.caption(f"ℹ️ **Why this amount?** {note}")

    # 2. Display Growth Buffer if selected
    if goal == "Gain Size/Growth Spurt":
        st.write("✅ *Includes +400 calorie surplus for growth.*")
    
    # The Hand Portion Grid
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"### 🥩 {palms}")
        st.write("**PALMS of Protein**")
        st.caption("Chicken, Beef, Eggs, Greek Yogurt, Fish")
        
    with c2:
        st.markdown(f"### 🍚 {cupped_hands}")
        st.write("**HANDFULS of Carbs**")
        st.caption("Rice, Potatoes, Oats, Pasta, Fruit, Bread")
        
    with c3:
        st.markdown(f"### 🥑 {thumbs}")
        st.write("**THUMBS of Fat**")
        st.caption("Butter, Oils, Nuts, Avocado, Cheese")

    st.markdown("---")
    
    # Meal Structure
    st.subheader("🍽 How to eat this in a day")
    
    p_meal = round(palms/4, 1)
    c_meal = round(cupped_hands/4, 1)
    f_meal = round(thumbs/4, 1)
    
    st.markdown(f"""
    **1️⃣ Breakfast:** {p_meal} Palms 🥩 | {c_meal} Carbs 🍚 | {f_meal} Thumbs 🥑
    
    **2️⃣ Lunch:** {p_meal} Palms 🥩 | {c_meal} Carbs 🍚 | {f_meal} Thumbs 🥑
    
    **3️⃣ Pre-Practice Snack:** {c_meal} Carbs 🍚 (Focus on Fruit/Granola here!)
    
    **4️⃣ Dinner:** {p_meal} Palms 🥩 | {c_meal} Carbs 🍚 | {f_meal} Thumbs 🥑
    """)
    
    st.info("💡 **Coach's Note:** These numbers are targets, not laws. If you are extra tired or hungry, eat more carbs. Listen to your body.")
