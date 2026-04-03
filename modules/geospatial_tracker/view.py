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
    
    # --- START FIX: COLUMN VALIDATION (Lowercase synchronized) ---
    required_cols = ['subject_taught', 'major_specialization', 'region']
    has_required_data = all(col in df.columns for col in required_cols)
    
    if not has_required_data:
        st.error("⚠️ **Schema Mismatch Detected:** The current dataset is missing standardized columns (major_specialization or subject_taught).")
        st.info("Please go to the **Ingestion Engine (Schema Healer)** and run the AI Semantic Fusion to prepare the data.")
        # Provide a safe fallback for display purposes
        map_df = df.copy()
        view_mode = "Total Workforce Density"
    else:
        # --- END FIX ---
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("### Regional Geospatial Map")
        with col_b:
            view_mode = st.radio("Visualization Mode", ["Total Workforce Density", "Underserved Hotspots (Out-of-Field)"], horizontal=True, label_visibility="collapsed")
            
        map_df = df.copy()
        if "Underserved" in view_mode:
            # Isolate the map to ONLY show vulnerable (structurally mismatched) teachers
            map_df = df[df['subject_taught'] != df['major_specialization']].copy()
        
    render_map(map_df, arcs_df=st.session_state.get('routing_arcs_df'))
    
    st.markdown("---")
    st.subheader("Dispatch Routing Algorithm")
    
    # --- START FIX: CONDITIONAL MATH (Lowercase synchronized) ---
    if has_required_data:
        # Mathematical Priority Calculation
        mismatches = df[df['subject_taught'] != df['major_specialization']].groupby('region').size()
        totals = df.groupby('region').size()
        fragility_rates = (mismatches / totals * 100).fillna(0)
        
        if not fragility_rates.empty:
            priority_region = fragility_rates.idxmax()
            priority_rate = fragility_rates.max()
        else:
            priority_region = "NCR"
            priority_rate = 0
            
        st.warning(f"**AI Regional Suggestion:** The system suggests prioritizing **{priority_region}**. Data indicates a `{priority_rate:.1f}%` out-of-field teaching vulnerability in this macro-zone.")
    else:
        priority_region = "NCR"
        st.warning("Priority suggestions are unavailable until data is standardized via Ingestion Engine.")
    # --- END FIX ---
    
    col1, col2 = st.columns(2)
    with col1:
        region_options = list(REGION_COORDS.keys())
        # Safe handling of default index
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
            
            from modules.geospatial_tracker.routing import find_teachers_from_top_clusters
            results = find_teachers_from_top_clusters(df, target_region, target_lat, target_lon, query_subject)
            
            # Construct Arc Data for PyDeck lasers
            arcs_data = []
            for _, row in results.iterrows():
                # Ensure coordinates exist (Ingestion engine outputs lowercase 'latitude'/'longitude')
                source_lat = row.get("latitude") or row.get("Latitude")
                source_lon = row.get("longitude") or row.get("Longitude")
                
                if source_lat and source_lon:
                    arcs_data.append({
                        "Source_Lon": source_lon,
                        "Source_Lat": source_lat,
                        "Target_Lon": target_lon,
                        "Target_Lat": target_lat
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
            # Check for name and experience columns safely (lowercase)
            f_name = row.get('first_name') or row.get('First_Name') or 'N/A'
            l_name = row.get('last_name') or row.get('Last_Name') or ''
            t_id = row.get('teacher_id') or row.get('Teacher_ID') or 'Unknown'
            exp = row.get('years_experience') or row.get('Years_Experience') or 0
            spec = row.get('major_specialization') or row.get('Major_Specialization') or 'N/A'
            dist = row.get('distance_from_target') or row.get('Distance_from_target') or 0
            
            st.markdown(f"**{t_id}** ({f_name} {l_name} | Exp: {exp} yrs) | Spec: **{spec}** | Distance: `{dist:.4f}`")