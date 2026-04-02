import streamlit as st
import pydeck as pdk
from core.ui_components import render_header
from modules.geospatial_tracker.map_engine import render_map
from modules.geospatial_tracker.routing import find_nearest_teacher
from core.data_loader import REGION_COORDS
from modules.geospatial_tracker.ai_assessment import find_vulnerability_epicenter, generate_ai_assessment

def render(df):
    if 'routing_arcs_df' not in st.session_state:
        st.session_state['routing_arcs_df'] = None
        st.session_state['dispatch_results'] = None
        st.session_state['dispatch_msg'] = ""
        
    render_header("Deployment Logistics Map", "Geospatial deployment and vulnerability tracking.")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("### Regional Geospatial Map")
    with col_b:
        view_mode = st.radio("Visualization Mode", ["Total Workforce Density", "Underserved Hotspots (Out-of-Field)"], horizontal=True, label_visibility="collapsed")
        
    map_df = df.copy()
    if "Underserved" in view_mode:
        # Isolate the map to ONLY show vulnerable (structurally mismatched) teachers
        map_df = df[df['Subject_Taught'] != df['Major_Specialization']].copy()
        
    render_map(map_df, arcs_df=st.session_state.get('routing_arcs_df'))
    
    st.markdown("---")
    st.subheader("Dispatch Routing Algorithm")
    
    # Mathematical Priority Calculation
    mismatches = df[df['Subject_Taught'] != df['Major_Specialization']].groupby('Region').size()
    totals = df.groupby('Region').size()
    fragility_rates = (mismatches / totals * 100).fillna(0)
    priority_region = fragility_rates.idxmax()
    priority_rate = fragility_rates.max()
    
    st.warning(f"**AI Regional Suggestion:** The system suggests prioritizing **{priority_region}**. Data indicates a `{priority_rate:.1f}%` out-of-field teaching vulnerability in this macro-zone.")
    
    col1, col2 = st.columns(2)
    with col1:
        region_options = list(REGION_COORDS.keys())
        default_index = region_options.index(priority_region) if priority_region in region_options else 0
        target_region = st.selectbox("Target Deployment Zone", region_options, index=default_index)
        
    with col2:
        subject = st.selectbox("Require Subject Specialization", ["Any", "Chemistry", "Physics", "Biology", "Mathematics", "General Science"])
        use_ai_epicenter = st.checkbox("Deploy to specific AI-Discovered Epicenter", value=True)
        
    # AI Micro-Targeting Assessment Panel
    epicenter_coords, epicenter_df = find_vulnerability_epicenter(df, target_region)
    with st.expander("View AI Micro-Targeting Insight"):
        if epicenter_coords:
            st.info(generate_ai_assessment(epicenter_df, target_region))
        else:
            st.write(f"Not enough vulnerability data to run clustering algorithm in {target_region}.")
            
    if st.button("Trigger Dispatch Routing"):
        with st.spinner("Calculating geospatial routes..."):
            
            if use_ai_epicenter and epicenter_coords:
                target_lat, target_lon = epicenter_coords
                routing_msg = f"Routing Computed for AI Epicenter in {target_region} (Lat: {target_lat:.4f}, Lon: {target_lon:.4f})!"
            else:
                target_lat, target_lon = REGION_COORDS[target_region]
                routing_msg = f"Routing Computed for Regional Anchor {target_region} (Lat: {target_lat:.4f}, Lon: {target_lon:.4f})!"
                
            query_subject = None if subject == "Any" else subject
            results = find_nearest_teacher(df, target_lat, target_lon, query_subject)
            
            # Construct Arc Data for PyDeck lasers (Shooting outwards from Epicenter)
            arcs_data = []
            for _, row in results.iterrows():
                arcs_data.append({
                    "Source_Lon": target_lon,
                    "Source_Lat": target_lat,
                    "Target_Lon": row["Longitude"],
                    "Target_Lat": row["Latitude"]
                })
            
            import pandas as pd
            st.session_state['routing_arcs_df'] = pd.DataFrame(arcs_data)
            st.session_state['dispatch_results'] = results
            st.session_state['dispatch_msg'] = routing_msg
            st.rerun()
            
    # Draw Results globally so they survive the rerun
    if st.session_state.get('dispatch_results') is not None:
        st.success(st.session_state['dispatch_msg'])
        for _, row in st.session_state['dispatch_results'].iterrows():
            st.markdown(f"**{row['Teacher_ID']}** ({row['First_Name']} {row['Last_Name']} | Exp: {row['Years_Experience']} yrs) | Spec: **{row['Major_Specialization']}** | Distance: `{row['Distance_from_target']:.4f}`")

