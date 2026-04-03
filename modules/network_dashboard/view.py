import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from core.ui_components import render_header
from modules.network_dashboard.graph_builder import build_pyvis_graph
from modules.network_dashboard.simulator import deploy_teacher
from core.data_loader import REGION_COORDS

def render(df):
    render_header("Obsidian Neural Network", "Interactive mapping of localized teaching resources.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Ecosystem Topology")
        
        # --- Legend and Navigation Instructions ---
        with st.expander("📖 Graph Legend & Navigation Guide", expanded=False):
            st.markdown("""
            **How to Navigate:**
            - 🖱️ **Scroll** to zoom in/out.
            - ↕️↔️ **Click and drag** the background to pan around the map.
            - 👆 **Click and drag** a specific node (circle or star) to move it.
            - ℹ️ **Hover** over a node to see the teacher's ID and specialization.
            
            **Node Shapes:**
            - ⭐ **Star (Large):** **Local Legend** (15+ Years Experience) - Prime candidates for mentorship.
            - 🔵 **Circle:** Standard Teacher / Node.
            - 🔴 **Red Circle (Large):** Region Hub.
            
            **Subject Colors:**
            """)
            
            lscol1, lscol2, lscol3 = st.columns(3)
            with lscol1:
                st.markdown("🟦 **Physics**")
                st.markdown("🟩 **Chemistry**")
            with lscol2:
                st.markdown("🟧 **Biology**")
                st.markdown("🟪 **Mathematics**")
            with lscol3:
                st.markdown("⬜ **General Science**")
                st.markdown("⚪ **Other**")
        # ------------------------------------------

        with st.spinner("Rendering Physics Sandbox..."):
            html_data = build_pyvis_graph(df)
            components.html(html_data, height=650)
            
    with col2:
        st.markdown("### Intervention Engine")
        st.info("Simulate re-assigning a teacher to fix regional fragility bottlenecks dynamically.")
        
        # Select Teacher
        teacher_categories = df[df["Years_Experience"] >= 10].head(50) # Prefer experienced teachers
        
        # User Friendly formatting for the dropdown 
        def format_teacher_label(tid):
            row = teacher_categories[teacher_categories["Teacher_ID"] == tid].iloc[0]
            star = "⭐" if row["Years_Experience"] >= 15 else ""
            return f"{star} {tid} | {row['Major_Specialization']} ({row['Years_Experience']} Yrs Exp)"
        
        teacher_id = st.selectbox(
            "Select Teacher Node to Reassign", 
            options=teacher_categories["Teacher_ID"].tolist(),
            format_func=format_teacher_label
        )
        
        # Select Region
        new_region = st.selectbox("Target Regional Hub:", list(REGION_COORDS.keys()))
        
        if st.button("🚀 Trigger Deployment Simulation", width='stretch'):
            # Update the global working dataframe in session state
            st.session_state['working_df'] = deploy_teacher(df, teacher_id, new_region)
            st.success(f"Successfully deployed {teacher_id} to {new_region}. Metrics recalculated.")
            st.rerun()

