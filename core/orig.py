import streamlit as st
from core.ui_components import set_page_config, inject_custom_css
from core.auth import initialize_session, get_current_role, render_sidebar_auth, render_login_page
from core.data_loader import get_working_dataframe
from core.dataframe_schema import normalize_record_columns

# Page Setup
set_page_config()
inject_custom_css()

# Session Boot
initialize_session()

# --- AUTHENTICATION GATE ---
if not st.session_state.get('authenticated', False):
    render_login_page()
    st.stop()

role = get_current_role()

# --- TIMELINE LOGIC (Merged from your teammate's update) ---
if 'active_year' not in st.session_state:
    st.session_state['active_year'] = '2026'

def transition_timeframe():
    # Extracts the year (e.g., "2026") from the label
    new_year = st.session_state["year_radio_key"].split(" ")[0]
    st.session_state['active_year'] = new_year
    # Reloads the global dataframe based on the year
    st.session_state['working_df'] = get_working_dataframe(new_year)

# Load Global Shared State (if not already loaded)
if 'working_df' not in st.session_state:
    st.session_state['working_df'] = get_working_dataframe(st.session_state['active_year'])

# We pull from session_state so Pillar 2 (Ingestion) can update it live
df = normalize_record_columns(st.session_state['working_df'])
st.session_state['working_df'] = df

# Sidebar Authentication
render_sidebar_auth()

# --- SIDEBAR TIMELINE SELECTOR ---
st.sidebar.markdown("### Timeframe")
timeframes = {
    "2026": "2026 (Present AI Intervention)",
    "2025": "2025 (Initial Rollout Phase)",
    "2024": "2024 (Critical Shortage)",
    "2023": "2023 (Pandemic Recovery)",
    "2022": "2022 (Data Baseline)"
}

options_list = list(timeframes.values())
# Find index of current active year to set as default
try:
    default_index = list(timeframes.keys()).index(st.session_state['active_year'])
except ValueError:
    default_index = 0

if role == "Admin":
    st.sidebar.selectbox(
        "Select Timeline:", 
        options=options_list, 
        index=default_index,
        key="year_radio_key",
        on_change=transition_timeframe
    )
else:
    st.sidebar.markdown(f"**Current Year:** {timeframes[st.session_state['active_year']]}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")

if role == "Admin":
    # Dictionary mapping for Admin modules
    admin_modules = {
        "Intelligence Analytics": lambda df: __import__('modules.intelligence.view', fromlist=['']).render(df),
        "Deployment Logistics Map": lambda df: __import__('modules.geospatial_tracker.view', fromlist=['']).render(df),
        "Obsidian Mentorship Topology": lambda df: __import__('modules.network_dashboard.view', fromlist=['']).render(df),
        "Ingestion Engine (Schema Healer)": lambda df: __import__('modules.ingestion.view', fromlist=['']).render()
    }
    
    selection = st.sidebar.radio("Go to module:", list(admin_modules.keys()))
    
    # Execute the selected module rendering function
    admin_modules[selection](df)

else:
    # Dictionary mapping for Teacher Role modules
    teacher_modules = {
        "Career Skill-Tree (Analytics)": lambda df: __import__('modules.intelligence.view', fromlist=['']).render(df),
        "Local Ecosystem (Network)": lambda df: __import__('modules.network_dashboard.view', fromlist=['']).render_teacher_view(df)
    }
    
    selection = st.sidebar.radio("Workspace:", list(teacher_modules.keys()))
    
    # Execute the selected module rendering function
    teacher_modules[selection](df)
        
st.sidebar.markdown("---")
st.sidebar.caption("Prototype built for DOST Hackathon by Team PositiveXPRequiem")