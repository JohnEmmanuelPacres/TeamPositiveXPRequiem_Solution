import streamlit as st
import streamlit.components.v1 as components
from core.ui_components import render_header
from modules.network_dashboard.graph_builder import build_pyvis_graph
from modules.network_dashboard.simulator import deploy_teacher

def render(df):
    render_header("Obsidian Neural Network", "Interactive mapping of localized teaching resources.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Ecosystem Topology")
        with st.spinner("Rendering Physics Sandbox..."):
            html_data = build_pyvis_graph(df)
            components.html(html_data, height=650)
            
    with col2:
        st.markdown("### Intervention Engine")
        st.info("Simulate re-assigning a teacher to fix regional fragility bottlenecks dynamically across all active session models.")
        
        from core.data_loader import REGION_COORDS
        teacher_id = st.selectbox("Select Teacher Node", df["Teacher_ID"].head(50))
        new_region = st.selectbox("Deploy To:", list(REGION_COORDS.keys()))
        
        if st.button("Trigger Deployment"):
            # Update the global working dataframe in session state
            st.session_state['working_df'] = deploy_teacher(df, teacher_id, new_region)
            st.success(f"Successfully simulated translating {teacher_id} to {new_region}.")
            st.rerun()
