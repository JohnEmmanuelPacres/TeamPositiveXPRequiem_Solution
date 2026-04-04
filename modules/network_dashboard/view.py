import streamlit as st
import streamlit.components.v1 as components
from core.ui_components import render_header
from modules.network_dashboard.graph_builder import build_pyvis_graph
from modules.network_dashboard.simulator import deploy_teacher
from core.data_loader import REGION_COORDS

def render(df):
    render_header("Obsidian Mentorship Topology", "Interactive mapping of localized teaching resources.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Ecosystem Topology")
        st.markdown("**How to Navigate:**")
        nav_cols = st.columns(2)
        with nav_cols[0]:
            st.markdown("<ul><li>Scroll to zoom in/out</li><li>Click and drag background to pan</li></ul>", unsafe_allow_html=True)
        with nav_cols[1]:
            st.markdown("<ul><li>Click and drag node to move</li><li>Hover for details</li></ul>", unsafe_allow_html=True)
            
        # Add region filter so the Admin view matches the localized teacher view density
        target_region = st.selectbox("Filter Topology by Region:", ["All Regions"] + list(REGION_COORDS.keys()))
        
        if target_region == "All Regions":
            st.info("**Note:** When viewing 'All Regions', the graph is limited to a global cross-section of 150 nodes to prevent browser crashing. For a complete local view, filter by a specific region above.")
            working_df = df
            node_limit = 150 # Global limit to avoid browser crash
        else:
            working_df = df[df['Region'] == target_region]
            node_limit = 35 # Localized limit to match Teacher view perfectly
            
        with st.spinner("Rendering Physics Sandbox..."):
            html_data = build_pyvis_graph(working_df, limit=node_limit)
            components.html(html_data, height=530)
            
        # Display overflow professors
        overflow_count = len(working_df) - node_limit
        if overflow_count > 0:
            with st.expander(f"View {overflow_count} Additional Teachers (Hidden due to Node Density Limits)"):
                st.dataframe(working_df.iloc[node_limit:][["Teacher_ID", "First_Name", "Last_Name", "Region", "Major_Specialization", "Years_Experience"]].reset_index(drop=True), use_container_width=True)

        # Legend below graph, horizontally compressed to avoid scrollbars
        legend_cols = st.columns([1, 1])
        with legend_cols[0]:
            st.markdown("**Node Shapes:**\n<ul style=\"list-style: none; padding-left: 0;\"><li>⭐ Star (Local Legend, 15+ Yrs Exp)</li><li>🔵 Circle (Standard)</li><li>🔴 Red Circle (Region Hub)</li></ul>", unsafe_allow_html=True)
        with legend_cols[1]:
            st.markdown("**Subjects:**")
            sub_cols = st.columns(2)
            with sub_cols[0]:
                st.markdown("<ul style=\"list-style: none; padding-left: 0;\"><li>🟦 Physics</li><li>🟩 Chemistry</li><li>🟧 Biology</li></ul>", unsafe_allow_html=True)
            with sub_cols[1]:
                st.markdown("<ul style=\"list-style: none; padding-left: 0;\"><li>🟪 Math</li><li>⬜ Gen Sci</li><li>⚪ Other</li></ul>", unsafe_allow_html=True)

    with col2:
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True) 
        st.markdown("### Intervention Engine")
        st.info("Simulate re-assigning a teacher to fix regional fragility bottlenecks dynamically.")
        
        # Select Teacher - use the entire global dataset so you can simulate extracting ANY node
        if df.empty:
            st.warning("No teacher data available for simulation.")
        else:
            # Create a speedy lookup dictionary so the global dropdown doesn't lag
            teacher_records = df.set_index("Teacher_ID").to_dict("index")
            def format_teacher_label(tid):
                row = teacher_records[tid]
                first = row.get("First_Name", "")
                last = row.get("Last_Name", "")
                name_prefix = f"Prof. {first} {last}".strip()
                name_display = f"{name_prefix} | " if name_prefix else ""
                return f"{name_display}{tid} | Current: {row['Region']} | {row['Years_Experience']} Yrs"
            
            teacher_id = st.selectbox(
                "Select Global Teacher Node to Extract & Reassign", 
                options=df["Teacher_ID"].tolist(),
                format_func=format_teacher_label
            )

            # Select Region
            new_region = st.selectbox("Target Regional Hub:", list(REGION_COORDS.keys()))

            if st.button("Trigger Deployment Simulation", use_container_width=True):
                # Update the global working dataframe in session state
                st.session_state['working_df'] = deploy_teacher(df, teacher_id, new_region)
                
                # Append a persistent notification event for the targeted Teacher view
                if 'regional_alerts' not in st.session_state:
                    st.session_state['regional_alerts'] = []
                
                row = df[df["Teacher_ID"] == teacher_id].iloc[0]
                prof_name = f"Prof. {row.get('First_Name', '')} {row.get('Last_Name', '')}".strip()
                prof_name = prof_name if prof_name != "Prof." else teacher_id
                
                st.session_state['regional_alerts'].append({
                    "region": new_region,
                    "message": f"**INCOMING ALLY:** {prof_name} ({row['Years_Experience']} Yrs Exp, {row['Major_Specialization']}) has just been re-routed to the {new_region} ecosystem to assist with localized capacity building!"
                })
                
                st.success(f"Successfully deployed {teacher_id} to {new_region}. Metrics recalculated.")
                st.rerun()

            st.markdown("---")
            if st.button("Reset Deployment Simulation", use_container_width=True):
                from core.data_loader import get_working_dataframe
                active_year = st.session_state.get('active_year', '2026')
                st.session_state['working_df'] = get_working_dataframe(active_year)
                st.session_state['regional_alerts'] = [] # Clear notifications on reset
                st.success("Simulation reset. Teachers returned to original regions.")
                st.rerun()



