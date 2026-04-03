import streamlit as st
from core.ui_components import set_page_config, inject_custom_css
from core.auth import initialize_session, get_current_role, render_sidebar_auth
from core.data_loader import get_working_dataframe

# Page Setup
set_page_config()
inject_custom_css()

# Session Boot
initialize_session()
role = get_current_role()

# Load Global Shared State
if 'active_year' not in st.session_state:
    st.session_state['active_year'] = '2026'

def transition_timeframe():
    new_year = st.session_state["year_radio_key"].split(" ")[0]
    st.session_state['active_year'] = new_year
    st.session_state['working_df'] = get_working_dataframe(new_year)

# Sidebar Routing Logic
render_sidebar_auth()
st.sidebar.markdown("### Timeframe Simulator")

# Defined years with thematic labels
timeframes = {
    "2026": "2026 (Present AI Intervention)",
    "2025": "2025 (Initial Rollout Phase)",
    "2024": "2024 (Critical Shortage)",
    "2023": "2023 (Pandemic Recovery)",
    "2022": "2022 (Data Baseline)"
}

options_list = list(timeframes.values())
default_index = list(timeframes.keys()).index(st.session_state['active_year'])

st.sidebar.radio(
    "Select Timeline:", 
    options=options_list, 
    index=default_index,
    key="year_radio_key",
    on_change=transition_timeframe
)

if 'working_df' not in st.session_state:
    st.session_state['working_df'] = get_working_dataframe(st.session_state['active_year'])

df = st.session_state['working_df']

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")

if role == "Admin":
    options = [
        "Intelligence Analytics", 
        "Deployment Logistics Map", 
        "Obsidian Neural Network",
        "Ingestion Engine (Schema Healer)"
    ]
    selection = st.sidebar.radio("Go to module:", options)

    if selection == "Intelligence Analytics":
        from modules.intelligence.view import render as render_intel
        render_intel(df)
        
    elif selection == "Deployment Logistics Map":
        from modules.geospatial_tracker.view import render as render_geo
        render_geo(df)
        
    elif selection == "Obsidian Neural Network":
        from modules.network_dashboard.view import render as render_net
        render_net(df)
        
    elif selection == "Ingestion Engine (Schema Healer)":
        from modules.ingestion.view import render as render_ingest
        render_ingest()

else:
    # Teacher Role Views
    options = [
        "Career Skill-Tree (Analytics)",
        "Local Ecosystem (Network)"
    ]
    selection = st.sidebar.radio("Workspace:", options)

    if selection == "Career Skill-Tree (Analytics)":
        from modules.intelligence.view import render as render_intel
        render_intel(df)
        
    elif selection == "Local Ecosystem (Network)":
        # Simplified Neural Network passing regional filter requirement conceptually
        from modules.network_dashboard.graph_builder import build_pyvis_graph
        import streamlit.components.v1 as components
        
        st.markdown("<div class='main-header'>Local Ecosystem</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>A view of peers and mentors within your network cluster.</div>", unsafe_allow_html=True)
        
        # Teacher view receives a smaller scoped ecosystem
        html_data = build_pyvis_graph(df, limit=50) 
        components.html(html_data, height=500)
        
st.sidebar.markdown("---")
st.sidebar.caption("Prototype built for DOST Hackathon by Team PositiveXPRequiem")
