import streamlit as st
import pandas as pd
import os

from core.ui_components import inject_astra_theme, inject_navbar_css

def initialize_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "username" not in st.session_state:
        st.session_state.username = ""
    
def get_current_role() -> str:
    return st.session_state.get('role', '')

def logout():
    st.session_state.authenticated = False
    st.session_state.role = ""
    st.session_state.username = ""

def render_sidebar_auth():
    st.sidebar.markdown("### Authentication Panel")
    st.sidebar.info(f"Logged in as: **{st.session_state.role}**\n\nUser Profile: `{st.session_state.username}`")
    if st.sidebar.button("Logout", use_container_width=True):
        logout()
        st.rerun()

def render_login_page():
    inject_navbar_css() # Call the sticky CSS
    # Render the actual Navbar HTML
    st.markdown(f"""
<div class="top-nav-wrapper">
<input type="checkbox" id="menu-toggle">
    <label for="menu-toggle" class="burger-icon">
        <i class="icon-menu"></i>
    </label>
    <div class="nav-container">
        <div class="nav-item-active">
            <div class="nav-icon"><i class="icon-cpu"></i></div>
            <div class="nav-text-wrapper">  
                <div class="nav-label">Intelligence Analytics</div>
            </div>
        </div>
        <div class="nav-divider"></div>
        <div class="nav-item">
            <div class="nav-icon"><i class="icon-map"></i></div>
            <div class="nav-text-wrapper">
                <div class="nav-label">Deployment Logistics Map</div>
            </div>
        </div>
        <div class="nav-divider"></div>
        <div class="nav-item">
            <div class="nav-icon"><i class="icon-waypoints"></i></div>
            <div class="nav-text-wrapper">
                <div class="nav-label">Obsidian Mentorship</div>
                <div class="nav-sublabel">Topology</div>
            </div>
        </div>
        <div class="nav-divider"></div>
        <div class="nav-item">
            <div class="nav-icon"><i class="icon-file-bar-chart-2"></i></div>
            <div class="nav-text-wrapper">
                <div class="nav-label">Ingestion Engine</div>
                <div class="nav-sublabel">(Schema Healer)</div>
            </div>
        </div>
    </div>
    <div class="account-wrapper">
        <input type="checkbox" id="account-toggle">
        <label for="account-toggle" class="account-trigger">
            <i class="icon-user"></i>
        </label>
        <div class="account-dropdown">
            <div class="dropdown-header">Authenticated As</div>
            <div class="dropdown-user-info">
                username
            </div>
            <div class="logout-btn" onclick="window.location.reload()">
                <i class="icon-log-out"></i> Logout
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    inject_astra_theme() 
    st.markdown('<div class="astra-title">ASTRA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="astra-subtitle">AI-DRIVEN SPATIAL TRACKING AND RESOURCE ALLOCATION SYSTEM</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("System Identifier", placeholder="Enter your ID or username")
            password = st.text_input("Password", type="password", placeholder="Enter your credentials")
            submitted = st.form_submit_button("Authenticate Access", use_container_width=True)
            
            if submitted:
                accounts_path = os.path.join("Dataset", "Data", "accounts.csv")
                if not os.path.exists(accounts_path):
                    st.error("Authentication database is offline.")
                    return
                    
                accounts_df = pd.read_csv(accounts_path)
                
                # Strip strings to prevent whitespace errors
                match = accounts_df[
                    (accounts_df['username'].astype(str).str.strip() == str(username).strip()) & 
                    (accounts_df['password'].astype(str).str.strip() == str(password).strip())
                ]
                
                if not match.empty:
                    st.session_state.authenticated = True
                    st.session_state.role = match.iloc[0]['role']
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Security sweep logged.")

