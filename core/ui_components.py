import streamlit as st
import os
import base64

def set_page_config():
    st.set_page_config(
        page_title="DSS Platform - Requiem",
        page_icon="⭐️",
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
    background: linear-gradient(135deg, #FFDEC8, #e8f0e8, #FFD5D5);
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
    .logo-container {{
            font-family: {astra_font};
            font-size: 25px;
            letter-spacing: 0.8em; 
            text-align: center;
            color: #333;
            padding: 20px 0 10px 0;
            width: 100%;
            text-transform: uppercase;
            margin-top: -50px;
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
    st.markdown("""
    <style>
        /* Remove the red box-shadow/border when browser validation triggers */
        input:invalid {
            box-shadow: none !important;
            border-color: rgba(0,0,0,0.1) !important;
        }
        /* Ensure Streamlit's own focus color takes priority */
        .stTextInput input:focus {
            border-color: #E0E0E0 !important; 
            box-shadow: 0 0 0 1px #E0E0E0 !important;
        }
    </style>
    """, unsafe_allow_html=True)