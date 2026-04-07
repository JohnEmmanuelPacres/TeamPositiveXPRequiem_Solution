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

# --- MAGIC CSS: Hide Sidebar & Setup Sticky Navbar ---
st.markdown("""
    <style>
    /* Hides default Streamlit header and sidebar entirely */
    [data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="collapsedControl"] { 
        display: none !important; 
    }
    
    .block-container { padding-top: 0rem !important; }
    
    iframe[title="navbar_component.custom_navbar"] { /* <--- CHANGE THIS FROM 20px TO 0px */
        left: 0;
        width: 100vw;
        height: 500px !important; 
        z-index: 9999;
        pointer-events: none; 
        background-color: #C41F1F;
    }
    
    /* Safely removes the ghost gap WITHOUT clipping the dropdown! */
    div[data-testid="stElementContainer"]:has(iframe[title="navbar_component.custom_navbar"]) {
        position: absolute !important;
        top: 0;
        left: 0;
        width: 100%;
        height: 0px !important;
        z-index: 9999;
        background-color: #301FC4;
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

# --- TIMELINE LOGIC ---
if 'active_year' not in st.session_state:
    st.session_state['active_year'] = '2026'

if 'working_df' not in st.session_state:
    st.session_state['working_df'] = get_working_dataframe(st.session_state['active_year'])

df = normalize_record_columns(st.session_state['working_df'])
st.session_state['working_df'] = df

timeframes = {
    "2026": "2026 (Present AI Intervention)",
    "2025": "2025 (Initial Rollout Phase)",
    "2024": "2024 (Critical Shortage)",
    "2023": "2023 (Pandemic Recovery)",
    "2022": "2022 (Data Baseline)"
}

# --- MODULES CONFIGURATION ---
if role == "Admin":
    modules = {
        "Intelligence Analytics": {"icon": "icon-cpu", "sub": None, "display": "Intelligence Analytics", "module": lambda df: __import__('modules.intelligence.view', fromlist=['']).render(df)},
        "Deployment Logistics Map": {"icon": "icon-map", "sub": None, "display": "Deployment Logistics Map", "module": lambda df: __import__('modules.geospatial_tracker.view', fromlist=['']).render(df)},
        "Obsidian Mentorship Topology": {"icon": "icon-waypoints", "sub": None, "display": "Obsidian Mentorship Topology", "module": lambda df: __import__('modules.network_dashboard.view', fromlist=['']).render(df)},
        "Ingestion Engine (Schema Healer)": {"icon": "icon-file-bar-chart-2", "sub": None, "display": "Ingestion Engine Schema Healer", "module": lambda df: __import__('modules.ingestion.view', fromlist=['']).render()}
    }
else:
    modules = {
        "Career Skill-Tree (Analytics)": {"icon": "icon-cpu", "sub": None, "display": "Career Skill-Tree Analytics", "module": lambda df: __import__('modules.intelligence.view', fromlist=['']).render(df)},
        "Local Ecosystem (Network)": {"icon": "icon-waypoints", "sub": None, "display": "Local Ecosystem Network", "module": lambda df: __import__('modules.network_dashboard.view', fromlist=['']).render_teacher_view(df)}
    }

if "current_nav" not in st.session_state or st.session_state.current_nav not in modules:
    st.session_state.current_nav = list(modules.keys())[0]

# --- BUILD DYNAMIC HTML FOR NAVBAR ---
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

# --- BUILD DYNAMIC TIMELINE DROPDOWN HTML ---
mobile_timeline_html = ""
desktop_timeline_html = ""

st.markdown("""
    <div class="logo-container">
        ASTRA
    </div>
""", unsafe_allow_html=True)

if role == "Admin":
    options_html = ""
    for year, label in timeframes.items():
        selected = "selected" if year == st.session_state['active_year'] else ""
        options_html += f'<option value="{year}" {selected}>{label}</option>'
    
    # Render inside the burger menu on mobile
    mobile_timeline_html = f"""
    <div class="mobile-timeline-wrapper">
        <div class="nav-divider-horizontal"></div>
        <div class="nav-label" style="text-align: left; padding: 10px 20px 5px 20px;">Select Timeline</div>
        <select data-timeline="true" class="timeline-select">{options_html}</select>
    </div>
    """
    
    # Render below the navbar on desktop
    desktop_timeline_html = f"""
    <div class="secondary-nav-wrapper">
        <select data-timeline="true" class="desktop-timeline">{options_html}</select>
    </div>
    """
else:
    # Teachers cannot change time, so they just see the label
    current_label = timeframes[st.session_state['active_year']]
    mobile_timeline_html = f"""
    <div class="mobile-timeline-wrapper">
        <div class="nav-divider-horizontal"></div>
        <div class="nav-label" style="text-align: left; padding: 10px 20px 5px 20px;">Timeline</div>
        <div style="padding: 0 20px 10px 20px; font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 600; color: #666;">{current_label}</div>
    </div>
    """
    desktop_timeline_html = f"""
    <div class="secondary-nav-wrapper">
        <div style="font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 600; color: #666; background: rgba(255,255,255,0.8); padding: 6px 12px; border-radius: 6px;">
            Active Year: {current_label}
        </div>
    </div>
    """

full_html = f"""
<div class="top-nav-wrapper">
    <input type="checkbox" id="menu-toggle">
    <label for="menu-toggle" class="burger-icon"><i class="icon-menu"></i></label>
    
    <div class="nav-container">
        {nav_items_html}
        {mobile_timeline_html}
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
{desktop_timeline_html}
"""

# --- DECLARE & CALL THE CUSTOM COMPONENT ---
custom_navbar = components.declare_component("custom_navbar", path="navbar_component")
clicked_nav = custom_navbar(html=full_html, key="my_navbar")

# --- HANDLE NAVIGATION SAFELY ---
if clicked_nav and clicked_nav != st.session_state.get("last_clicked"):
    st.session_state.last_clicked = clicked_nav
    
    # 1. Catch the Timeline Updates
    if clicked_nav.startswith("TIMELINE_"):
        new_year = clicked_nav.split("_")[1]
        st.session_state['active_year'] = new_year
        st.session_state['working_df'] = get_working_dataframe(new_year)
        st.rerun()
        
    # 2. Catch the Logout Event
    elif clicked_nav == "LOGOUT":
        logout()
        if "current_nav" in st.session_state:
            del st.session_state["current_nav"]
        st.rerun()
        
    # 3. Catch Page Switches
    elif clicked_nav in modules:
        st.session_state.current_nav = clicked_nav
        st.rerun()

if st.session_state.current_nav not in modules:
    st.session_state.current_nav = list(modules.keys())[0]

# --- EXECUTE THE SELECTED MODULE ---
modules[st.session_state.current_nav]["module"](df)