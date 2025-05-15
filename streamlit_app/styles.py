import streamlit as st

def load_css():
    """
    Memuat CSS styling yang lebih menarik dan konsisten untuk aplikasi.
    """
    st.markdown("""
    <style>
        /* Warna Utama dan Pallete */
        :root {
            --primary-color: #3A86FF;
            --primary-light: #61A0FF;
            --primary-dark: #2970E3;
            --secondary-color: #FF6B6B;
            --accent-color: #4CC9F0;
            --text-color: #333333;
            --text-light: #555555;
            --bg-color: #F8F9FA;
            --card-bg: #FFFFFF;
            --border-radius: 10px;
            --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            
            /* Warna risiko */
            --risk-very-low: #2DC653;
            --risk-low: #5097ED;
            --risk-high: #FF9F1C;
            --risk-very-high: #E63946;
        }
        
        /* Global Styling */
        .reportview-container {
            background-color: var(--bg-color);
        }
        
        .stApp {
            background-color: var(--bg-color);
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text-color);
            margin-bottom: 1rem;
        }
        
        p, li, div {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text-light);
        }
        
        /* Headers */
        .main-header {
            font-size: 2.5rem;
            color: #3A86FF;
            text-align: center;
            margin-bottom: 0.5rem;  /* Kurangi margin bottom */
            font-weight: 600;
            padding-bottom: 10px;   /* Tambahkan padding bottom */
            background: linear-gradient(90deg, #3A86FF, #4CC9F0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .sub-header {
            font-size: 1.8rem;
            color: var(--primary-dark);
            margin-top: 2rem;
            margin-bottom: 1.2rem;
            font-weight: 600;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(58, 134, 255, 0.2);
        }
        
        .section-header {
            font-size: 1.4rem;
            color: var(--primary-color);
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        /* Cards */
        .card {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 1.8rem;
            margin-bottom: 1.8rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        }
        
        /* Metrics */
        div[data-testid="metric-container"] {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            padding: 1.2rem;
            box-shadow: var(--box-shadow);
            border: 1px solid rgba(58, 134, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px);
        }
        
        div[data-testid="metric-container"] > label {
            font-size: 0.9rem !important;
            color: var(--text-light) !important;
            font-weight: 500 !important;
        }
        
        div[data-testid="metric-container"] > div[data-testid="stMetricValue"] > div {
            font-size: 1.8rem !important;
            color: var(--primary-color) !important;
            font-weight: 600 !important;
        }
        
        /* Risk Level Colors */
        .risk-very-high {
            color: var(--risk-very-high);
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .risk-high {
            color: var(--risk-high);
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .risk-low {
            color: var(--risk-low);
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .risk-very-low {
            color: var(--risk-very-low);
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: rgba(58, 134, 255, 0.1);
            border-radius: 8px 8px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color) !important;
            color: white !important;
        }
        
        /* Buttons */
        div[data-testid="stButton"] > button:first-child {
            background-color: var(--primary-color);
            color: white;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stButton"] > button:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(58, 134, 255, 0.4);
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: var(--card-bg);
            border-right: 1px solid rgba(0,0,0,0.05);
            padding: 1.5rem;
        }
        
        section[data-testid="stSidebar"] h3 {
            color: var(--primary-color);
            font-weight: 600;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
        }
        
        /* Select boxes */
        div[data-baseweb="select"] > div {
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.1);
            transition: border-color 0.3s ease;
        }
        
        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.2);
        }
        
        /* Number inputs */
        div[data-testid="stNumberInput"] input {
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.1);
            padding: 0.5rem;
            transition: border-color 0.3s ease;
        }
        
        div[data-testid="stNumberInput"] input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.2);
        }
        
        /* Sliders */
        div[data-testid="stSlider"] > div > div > div {
            background-color: var(--primary-light);
        }
        
        div[data-testid="stSlider"] > div > div > div > div {
            background-color: var(--primary-color);
        }
        
        /* Expanders */
        details {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: var(--box-shadow);
            margin-bottom: 1rem;
            overflow: hidden;
        }
        
        details > summary {
            padding: 1rem;
            cursor: pointer;
            font-weight: 500;
            color: var(--primary-color);
        }
        
        details[open] > summary {
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        
        /* Gauge chart container */
        .gauge-wrapper {
            text-align: center;
            padding: 1rem;
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: var(--box-shadow);
        }
        
        /* Info text */
        .info-text {
            line-height: 1.6;
            color: var(--text-light);
            font-size: 1rem;
        }
        
        /* Highlights */
        .highlight {
            color: var(--primary-color);
            font-weight: 500;
            text-decoration: underline dotted;
        }
        
        /* Risk factor cards */
        .risk-factor-card {
            text-align: center;
            padding: 1.2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            background-color: var(--card-bg);
            height: 100%;
            transition: transform 0.3s ease;
        }
        
        .risk-factor-card:hover {
            transform: translateY(-5px);
        }
        
        .risk-factor-header {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.8rem;
        }
        
        .risk-factor-content {
            background-color: #f5f5f5;
            border-radius: 8px;
            padding: 1rem;
            min-height: 100px;
            font-size: 0.9rem;
            line-height: 1.5;
            color: var(--text-light);
        }
        
        .risk-factor-impact {
            margin-top: 0.8rem;
            font-weight: 500;
            padding: 0.4rem;
            border-radius: 4px;
            background-color: rgba(0,0,0,0.05);
        }
        
        /* Data table styling */
        .stDataFrame {
            border-radius: var(--border-radius);
            overflow: hidden;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(0,0,0,0.1);
            font-size: 0.9rem;
            color: var(--text-light);
        }
        
        /* Widget labels */
        .stWidgetLabel {
            color: var(--text-color);
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        /* Responsive adjustments for mobile */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .sub-header {
                font-size: 1.5rem;
            }
            
            .card {
                padding: 1.2rem;
            }
            
            div[data-testid="metric-container"] > div[data-testid="stMetricValue"] > div {
                font-size: 1.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)