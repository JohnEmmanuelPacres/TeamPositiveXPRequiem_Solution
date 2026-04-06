import streamlit as st
import streamlit.components.v1 as components
from core.ui_components import set_page_config, inject_custom_css, inject_astra_theme
from core.auth import initialize_session, get_current_role, render_login_page, logout
from core.data_loader import get_working_dataframe
from core.dataframe_schema import normalize_record_columns

# Page Setup
set_page_config()
inject_custom_css()
inject_astra_theme() 

# --- MAGIC CSS: Make the Component Iframe Sticky & Click-through ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { visibility: hidden; }
    
    /* Reduced this to pull the dashboard up nicely under the navbar */
    .block-container { padding-top: 3.5rem !important; }
    
    iframe[title="navbar_component.custom_navbar"] {
        position: fixed;
        top: -50px;
        left: 0;
        width: 100vw;
        height: 350px !important; /* Forces iframe open for the dropdown */
        z-index: 9999;
        pointer-events: none; 
    }
    
    /* This perfectly kills the 350px "ghost" gap */
    div[data-testid="stElementContainer"]:has(iframe[title="navbar_component.custom_navbar"]) {
        height: 0px !important;
        margin-bottom: -350px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session Boot
initialize_session()

if not st.session_state.get('authenticated', False):
    render_login_page()
    st.stop()

role = get_current_role()
username = st.session_state.get('username', 'User')

if 'active_year' not in st.session_state:
    st.session_state['active_year'] = '2026'

if 'working_df' not in st.session_state:
    st.session_state['working_df'] = get_working_dataframe(st.session_state['active_year'])

df = normalize_record_columns(st.session_state['working_df'])
st.session_state['working_df'] = df

# --- MODULES ---
if role == "Admin":
    modules = {
        "Intelligence Analytics": {"icon": "icon-cpu", "sub": None, "display": "Intelligence Analytics", "module": lambda df: __import__('modules.intelligence.view', fromlist=['']).render(df)},
        "Deployment Logistics Map": {"icon": "icon-map", "sub": None, "display": "Deployment Logistics Map", "module": lambda df: __import__('modules.geospatial_tracker.view', fromlist=['']).render(df)},
        "Obsidian Mentorship Topology": {"icon": "icon-waypoints", "sub": "Topology", "display": "Obsidian Mentorship", "module": lambda df: __import__('modules.network_dashboard.view', fromlist=['']).render(df)},
        "Ingestion Engine (Schema Healer)": {"icon": "icon-file-bar-chart-2", "sub": "(Schema Healer)", "display": "Ingestion Engine", "module": lambda df: __import__('modules.ingestion.view', fromlist=['']).render()}
    }
else:
    modules = {
        "Career Skill-Tree (Analytics)": {"icon": "icon-cpu", "sub": "(Analytics)", "display": "Career Skill-Tree", "module": lambda df: __import__('modules.intelligence.view', fromlist=['']).render(df)},
        "Local Ecosystem (Network)": {"icon": "icon-waypoints", "sub": "(Network)", "display": "Local Ecosystem", "module": lambda df: __import__('modules.network_dashboard.view', fromlist=['']).render_teacher_view(df)}
    }

# SAFETY CHECK 1: Ensure session state exists and is valid for current role
if "current_nav" not in st.session_state or st.session_state.current_nav not in modules:
    st.session_state.current_nav = list(modules.keys())[0]

# --- BUILD THE HTML STRING ---
nav_items_html = ""
module_keys = list(modules.keys())

for i, mod_key in enumerate(module_keys):
    mod_data = modules[mod_key]
    is_active = (mod_key == st.session_state.current_nav)
    nav_class = "nav-item-active" if is_active else "nav-item"
    
    sublabel_html = f'<div class="nav-sublabel">{mod_data["sub"]}</div>' if mod_data.get("sub") else ""
    
    nav_items_html += f"""
    <div data-nav="{mod_key}" class="{nav_class}">
        <div class="nav-icon"><i class="{mod_data['icon']}"></i></div>
        <div class="nav-text-wrapper">  
            <div class="nav-label">{mod_data.get("display", mod_key)}</div>
            {sublabel_html}
        </div>
    </div>
    """
    if i < len(module_keys) - 1:
        nav_items_html += '<div class="nav-divider"></div>'

full_html = f"""
<div class="top-nav-wrapper">
    <input type="checkbox" id="menu-toggle">
    <label for="menu-toggle" class="burger-icon"><i class="icon-menu"></i></label>
    
    <div class="nav-container">
        {nav_items_html}
    </div>
    
    <div class="account-wrapper">
        <input type="checkbox" id="account-toggle">
        <label for="account-toggle" class="account-trigger"><i class="icon-user"></i></label>
        <div class="account-dropdown">
            <div class="dropdown-header">Authenticated As {role}</div>
            <div class="dropdown-user-info">{username}</div>
            <div data-nav="LOGOUT" class="logout-btn"><i class="icon-log-out"></i> Logout</div>
        </div>
    </div>
</div>
"""

# --- DECLARE & CALL THE CUSTOM COMPONENT ---
custom_navbar = components.declare_component("custom_navbar", path="navbar_component")
clicked_nav = custom_navbar(html=full_html, key="my_navbar")

# --- HANDLE NAVIGATION SAFELY ---
if clicked_nav and clicked_nav != st.session_state.get("last_clicked"):
    st.session_state.last_clicked = clicked_nav
    
    if clicked_nav == "LOGOUT":
        logout()
        # Clear navigation history completely on logout
        if "current_nav" in st.session_state:
            del st.session_state["current_nav"]
        st.rerun()
    elif clicked_nav in modules:
        st.session_state.current_nav = clicked_nav
        st.rerun()

# SAFETY CHECK 2: Double check before executing (Catches edge cases)
if st.session_state.current_nav not in modules:
    st.session_state.current_nav = list(modules.keys())[0]

# --- EXECUTE THE SELECTED MODULE ---
modules[st.session_state.current_nav]["module"](df)