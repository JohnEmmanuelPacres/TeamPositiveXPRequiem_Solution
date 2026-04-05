import streamlit as st
import os
import base64

def set_page_config():
    st.set_page_config(
        page_title="DSS Platform - Requiem",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def inject_custom_css():
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .sub-header {
            font-size: 1.25rem;
            color: #6B7280;
            margin-top: 0px;
            padding-top: 0px;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #F3F4F6;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #3B82F6;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #111827;
        }
        .metric-label {
            font-size: 0.875rem;
            font-weight: 600;
            color: #4B5563;
            text-transform: uppercase;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header(title: str, subtitle: str):
    st.markdown(f"<div class='main-header'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{subtitle}</div>", unsafe_allow_html=True)
    
def load_font_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def inject_astra_theme():
    font_b64 = load_font_b64("core/font/Avenix-Regular.otf")
    
    if font_b64:
        font_face = f"""
        @font-face {{
            font-family: 'Avenix';
            src: url('data:font/truetype;base64,{font_b64}') format('truetype');
            font-weight: normal; font-style: normal;
        }}
        """
        astra_font = "'Avenix', sans-serif"
    else:
        font_face = ""
        astra_font = "'Montserrat', sans-serif"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Inter:wght@400;500&display=swap');
        {font_face}

        /* 1. Background Fade */
        [data-testid="stAppViewContainer"] {{
    background: linear-gradient(135deg, #FFF2DE, #e8f0e8, #FFD5D5);
    background-size: 200% 200%;
    min-height: 100vh;
    animation: gradientShift 15s ease infinite;
}}

@keyframes gradientShift {{
    0% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
    100% {{
        background-position: 0% 50%;
    }}
}}

        /* Hide Streamlit default elements */
        [data-testid="stHeader"], #MainMenu, footer {{ visibility: hidden; }}
        [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none; }}

        /* 2. ASTRA Title: Starts at center, then moves up */
        .astra-title {{
            font-family: {astra_font};
            font-size: 55px;
            letter-spacing: 8px;
            color: #2b2b2b;
            text-align: center;
            opacity: 0;
            animation: astraEntrance 3.5s ease-in-out forwards;
        }}

        /* 3. Subtitle: Follows the Title */
        .astra-subtitle {{
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 3px;
            color: #555;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 30px;
            opacity: 0;
            animation: subtitleEntrance 3.5s ease-in-out forwards;
        }}

        /* 4. Login Form: Appears only after the move-up */
        [data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            max-width: 450px;
            margin: 0 auto;
            opacity: 0;
            animation: formFadeIn 1s ease-out 3s forwards;
        }}

        /* --- THE ANIMATION SEQUENCES --- */

        @keyframes astraEntrance {{
            0% {{ opacity: 0; transform: translateY(100px); }}      
            20% {{ opacity: 1; transform: translateY(100px); }}     
            70% {{ opacity: 1; transform: translateY(100px); }}     
            100% {{ opacity: 1; transform: translateY(0); }}        
        }}

        @keyframes subtitleEntrance {{
            0% {{ opacity: 0; transform: translateY(100px); }}      
            30% {{ opacity: 0; transform: translateY(100px); }}     
            50% {{ opacity: 1; transform: translateY(100px); }}     
            70% {{ opacity: 1; transform: translateY(100px); }}     
            100% {{ opacity: 1; transform: translateY(0); }}        
        }}

        @keyframes formFadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Existing Label and Input Styles */
        [data-testid="stForm"] label {{
            font-family: 'Montserrat', sans-serif;
            font-size: 18px;
            font-weight: 600;
            color: #444;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        [data-testid="stFormSubmitButton"] button {{
            background-color: #2b2b2b !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            padding: 10px 20px !important;
            width: 100% !important;
            margin-top: 25px !important;
            transition: transform 0.1s ease !important;
        }}

        [data-testid="stFormSubmitButton"] button:active {{
            transform: scale(0.98) !important;
        }}

        /* Reset eye icon button styling */
        [data-testid="stForm"] button[title="Show password text"],
        [data-testid="stForm"] button[title="Hide password text"] {{
            background-color: transparent !important;
            color: #666 !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            width: auto !important;
            margin-right: 10px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def inject_navbar_css():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/font/lucide.min.css">
    <style>
    /* 1. PARENT WRAPPER */
    .top-nav-wrapper {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        z-index: 9999;
        width: 95%;
        max-width: 1200px;
    }
    /* 2. NAVIGATION CONTAINER */
    .nav-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        background: #F8F8F8; /* Light grey base like the image background */
        background: rgba(255, 255, 255, 0.98);
        padding: 4px;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        width: 95%;
        flex: 1;
    }
    .nav-item, .nav-item-active {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        padding: 8px 20px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        min-height: 45px;
        flex: 1 0 0; 
        min-width: 0;
    }
    /* Active State matching the image (light grey pill) */
    .nav-item-active { 
        background: #F1F1F1; 
        border-radius: 10px; 
    }
    .nav-icon i { 
        font-size: 18px; 
        color: #333; 
        display: flex; 
        align-items: center; 
    }
    .nav-text-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center; /* Center text under each other */
        justify-content: center;
    }
    .nav-label {
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #333;
        text-transform: uppercase;
        white-space: nowrap;
        line-height: 1.2;
        text-align: center;
    }
    .nav-sublabel {
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
        font-size: 9px;
        font-weight: 600;
        color: #333;
        text-transform: uppercase;
        margin-top: 1px;
        line-height: 1;
        text-align: center;
    }
    .nav-divider {
        width: 1.5px;
        height: 25px;
        background: #E0E0E0;
        margin: 0 5px;
    }
    /* 3. ACCOUNT BUBBLE */
    .account-wrapper { position: relative; }
    .account-trigger {
        width: 45px;
        height: 45px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
    }
    .account-trigger i { font-size: 20px; color: #333; }
    /* 3. BURGER MENU (Hidden by default) */
    #menu-toggle { display: none; }
    .burger-icon {
        display: none;
        width: 46px;
        height: 46px;
        background: white;
        border-radius: 12px;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.06);
    }
    /* 3. ACCOUNT DROPDOWN LOGIC */
    .account-wrapper { position: relative; flex-shrink: 0; }
    /* Hidden checkbox for toggle functionality */
    #account-toggle { display: none; }
    .account-trigger {
        width: 46px;
        height: 46px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.1s active;
    }
    .account-dropdown {
        position: absolute;
        top: 55px;
        right: 0;
        width: 220px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border: 1px solid rgba(0,0,0,0.08);
        display: none; /* Hidden by default */
        padding: 8px 0;
        z-index: 10000;
        animation: fadeIn 0.2s ease-out;
    }
    /* Toggle visibility when checkbox is checked */
    #account-toggle:checked ~ .account-dropdown {
        display: block;
    }
    .dropdown-header {
    font-family: 'Montserrat', 'Segoe UI', sans-serif;
        padding: 10px 16px;
        font-size: 9px;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700;
    }
    .dropdown-user-info {
    font-family: 'Montserrat', 'Segoe UI', sans-serif;
        padding: 5px 16px 12px 16px;
        font-size: 13px;
        font-weight: 600;
        color: #333;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #F0F0F0;
    }
    .logout-btn {
    font-family: 'Montserrat', 'Segoe UI', sans-serif;
        margin-top: 5px;
        padding: 12px 16px;
        font-size: 13px;
        color: #FF4B4B;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: background 0.2s;
    }
    .logout-btn:hover {
        background: #FFF5F5;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .nav-text-wrapper { display: none; }
        .nav-item, .nav-item-active { flex: none; width: 60px; }
    }
    /* FIX FOR MOBILE DESCRIPTION */
    @media (max-width: 850px) {
        .top-nav-wrapper { 
            justify-content: space-between; 
            padding: 0 15px; 
            width: 100%;
        }
        .burger-icon { display: flex; }
        .nav-container {
            display: none; 
            position: absolute;
            top: 65px;
            left: 15px; /* Align with burger */
            width: 320px; /* Force a wider container so text doesn't wrap */
            flex-direction: column !important; /* Stack items vertically */
            background: white;
            padding: 12px;
            border-radius: 16px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            border: 1px solid rgba(0,0,0,0.08);
            z-index: 10001;
        }
        #menu-toggle:checked ~ .nav-container {
            display: flex !important;
        }
        .nav-item, .nav-item-active {
            flex-direction: row !important; /* ICON AND TEXT SIDE-BY-SIDE */
            justify-content: flex-start !important;
            align-items: center !important;
            padding: 16px 20px !important;
            gap: 20px !important;
            width: 100%;
            border-bottom: 1px solid #f8f8f8;
            flex: none;
        }
        .nav-item:last-child { border-bottom: none; }
        .nav-text-wrapper {
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important; /* Left align text */
            text-align: left !important;
        }
        .nav-label {
            font-size: 12px !important;
            white-space: nowrap !important; /* Stop the "tight" wrapping */
            letter-spacing: 0.5px;
        }
        .nav-sublabel {
            font-size: 10px !important;
            margin-top: 2px;
        }
        .nav-divider { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)