import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Modern Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
def add_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    h1, h2, h3 {
        color: #00ffff;
        text-align: center;
    }
    
    .stButton > button {
        background-color: #00ffff;
        color: #1a1a1a;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #ff00ff;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #2a2a2a;
        color: #ffffff;
        border: 1px solid #00ffff;
        border-radius: 5px;
    }
    
    .stSelectbox > div > div > div {
        background-color: #2a2a2a;
        color: #ffffff;
        border: 1px solid #00ffff;
        border-radius: 5px;
    }
    
    .result {
        background-color: #2a2a2a;
        color: #00ffff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        margin-top: 20px;
        box-shadow: 0 0 10px #00ffff;
    }
    
    .category-card {
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
    }
    
    .category-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #888888;
    }
    
    /* Neon text effect */
    .neon-text {
        color: #fff;
        text-shadow:
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #0fa,
            0 0 82px #0fa,
            0 0 92px #0fa,
            0 0 102px #0fa,
            0 0 151px #0fa;
    }
    </style>
    """, unsafe_allow_html=True)

# Conversion functions
def convert_length(value, from_unit, to_unit):
    # Conversion factors to meters
    length_to_meters = {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1,
        "Kilometer": 1000,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Yard": 0.9144,
        "Mile": 1609.34
    }
    return value * length_to_meters[from_unit] / length_to_meters[to_unit]

def convert_weight(value, from_unit, to_unit):
    # Conversion factors to grams
    weight_to_grams = {
        "Milligram": 0.001,
        "Gram": 1,
        "Kilogram": 1000,
        "Ounce": 28.3495,
        "Pound": 453.592,
        "Stone": 6350.29
    }
    return value * weight_to_grams[from_unit] / weight_to_grams[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
    return value

def convert_volume(value, from_unit, to_unit):
    # Conversion factors to liters
    volume_to_liters = {
        "Milliliter": 0.001,
        "Liter": 1,
        "Cubic Meter": 1000,
        "Fluid Ounce (US)": 0.0295735,
        "Cup (US)": 0.236588,
        "Pint (US)": 0.473176,
        "Quart (US)": 0.946353,
        "Gallon (US)": 3.78541
    }
    return value * volume_to_liters[from_unit] / volume_to_liters[to_unit]

def convert_time(value, from_unit, to_unit):
    # Conversion factors to seconds
    time_to_seconds = {
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800,
        "Month (30 days)": 2592000,
        "Year (365 days)": 31536000
    }
    return value * time_to_seconds[from_unit] / time_to_seconds[to_unit]

# Unit categories
unit_categories = {
    "Length": {
        "units": ["Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot", "Yard", "Mile"],
        "convert_function": convert_length,
        "icon": "📏"
    },
    "Weight": {
        "units": ["Milligram", "Gram", "Kilogram", "Ounce", "Pound", "Stone"],
        "convert_function": convert_weight,
        "icon": "⚖️"
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "convert_function": convert_temperature,
        "icon": "🌡️"
    },
    "Volume": {
        "units": ["Milliliter", "Liter", "Cubic Meter", "Fluid Ounce (US)", "Cup (US)", "Pint (US)", "Quart (US)", "Gallon (US)"],
        "convert_function": convert_volume,
        "icon": "🧪"
    },
    "Time": {
        "units": ["Second", "Minute", "Hour", "Day", "Week", "Month (30 days)", "Year (365 days)"],
        "convert_function": convert_time,
        "icon": "⏱️"
    }
}

def home_page():
    st.markdown('<h1 class="neon-text">Modern Unit Converter</h1>', unsafe_allow_html=True)
    st.write("Welcome to the Modern Unit Converter. Choose a category to start converting!")

    cols = st.columns(len(unit_categories))
    for i, (category, info) in enumerate(unit_categories.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="category-card">
                <div class="category-icon">{info['icon']}</div>
                <h3>{category}</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Convert {category}", key=f"btn_{category}"):
                st.session_state.page = category
                st.rerun()

def converter_page(category):
    st.markdown(f'<h1 class="neon-text">{category} Converter</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        value = st.number_input("Enter value:", value=1.0, step=0.1)
        from_unit = st.selectbox("From:", unit_categories[category]["units"], key="from_unit")
    
    with col2:
        to_unit = st.selectbox("To:", unit_categories[category]["units"], key="to_unit")
    
    if st.button("Convert"):
        result = unit_categories[category]["convert_function"](value, from_unit, to_unit)
        st.markdown(f"""
        <div class="result">
            {value} {from_unit} = {result:.4f} {to_unit}
        </div>
        """, unsafe_allow_html=True)
    
    # Conversion table
    st.subheader("Conversion Table")
    table_values = [0.1, 1, 10, 100, 1000]
    df = pd.DataFrame({
        f"{from_unit}": table_values,
        f"{to_unit}": [unit_categories[category]["convert_function"](v, from_unit, to_unit) for v in table_values]
    })
    st.table(df)
    
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def main():
    add_custom_css()
    
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page in unit_categories:
        converter_page(st.session_state.page)
    
    st.markdown('<div class="footer">DEVELOPED BY RAFIHA SIDDIQUI</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

