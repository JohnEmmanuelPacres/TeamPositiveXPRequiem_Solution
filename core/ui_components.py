import streamlit as st

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
