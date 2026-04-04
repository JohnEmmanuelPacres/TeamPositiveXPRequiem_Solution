import streamlit as st
import pydeck as pdk
import pandas as pd
from core.ui_components import render_header
from modules.geospatial_tracker.map_engine import render_map
from modules.geospatial_tracker.routing import find_nearest_teacher
from core.data_loader import REGION_COORDS
from modules.geospatial_tracker.ai_assessment import find_vulnerability_epicenter, generate_ai_assessment
from core.dataframe_schema import normalize_record_columns
from modules.network_dashboard.simulator import deploy_teacher

def render(df):
    if 'routing_arcs_df' not in st.session_state:
        st.session_state['routing_arcs_df'] = None
        st.session_state['dispatch_results'] = None
        st.session_state['dispatch_msg'] = ""
        
    render_header("Deployment Logistics Map", "Geospatial deployment and vulnerability tracking.")

    # --- 1. SELF-HEALING & NORMALIZATION ---
    df_internal = normalize_record_columns(df)

    # Ensure mandatory columns exist
    for target_col in ["subject_taught", "major_specialization", "region", "teacher_id", "years_experience"]:
        if target_col not in df_internal.columns:
            df_internal[target_col] = "not_specified"

    # --- 2. VISUALIZATION MODE LOGIC ---
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("### Regional Geospatial Map")
    with col_b:
        view_mode = st.radio("Visualization Mode", ["Total Workforce Density", "Underserved Hotspots (Out-of-Field)"], horizontal=True, label_visibility="collapsed")
        
    map_df = df_internal.copy()
    if "Underserved" in view_mode:
        # Comparison logic: compare stripped, lowercased values to find true mismatches
        map_df = df_internal[
            df_internal['subject_taught'].str.strip().str.lower() != 
            df_internal['major_specialization'].str.strip().str.lower()
        ].copy()
    
    # Now pass it to the actual engine
    render_map(map_df, arcs_df=st.session_state.get('routing_arcs_df'))
    
    st.markdown("---")
    st.subheader("Dispatch Routing Algorithm")
    
    # Mathematical Priority Calculation
    try:
        # Use values comparison for fragility calculation
        mismatches_mask = df_internal['subject_taught'].str.strip().str.lower() != df_internal['major_specialization'].str.strip().str.lower()
        mismatches = df_internal[mismatches_mask].groupby('region').size()
        totals = df_internal.groupby('region').size()
        fragility_rates = (mismatches / totals * 100).fillna(0)
        
        if not fragility_rates.empty:
            priority_region = fragility_rates.idxmax()
            priority_rate = fragility_rates.max()
            
            # Contextual Override Logic
            if "BARMM" in fragility_rates.index and priority_region != "BARMM":
                barmm_rate = fragility_rates["BARMM"]
                if (priority_rate - barmm_rate) <= 2.0:
                    priority_region = "BARMM"
                    priority_rate = barmm_rate
                    override_msg = "*(Contextual AI Override Active: Structural priority factored)* "
                else:
                    override_msg = ""
            else:
                override_msg = ""
                
        else:
            priority_region = "NCR"
            priority_rate = 0
            override_msg = ""
            
        st.warning(f"**AI Regional Suggestion:** {override_msg}The system suggests prioritizing **{priority_region}**. Data indicates a `{priority_rate:.1f}%` out-of-field teaching vulnerability in this zone.")
    except:
        priority_region = "NCR"
        st.info("Awaiting more specific data for regional priority calculation.")

    # --- 4. DISPATCH UI ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        region_options = list(REGION_COORDS.keys())
        source_options = ["Global Nearest (Any)"] + region_options
        source_region = st.selectbox("Source Deployment Region", source_options, index=0)
        
    with col2:
        default_index = region_options.index(priority_region) if priority_region in region_options else 0
        target_region = st.selectbox("Target Deployment Zone", region_options, index=default_index)
        
    with col3:
        subject = st.selectbox("Request Specialization", ["Any", "Chemistry", "Physics", "Biology", "Mathematics", "General Science"])
        use_ai_epicenter = st.checkbox("Deploy to AI Epicenter", value=True)
        
    # AI Epicenter logic
    epicenter_coords, epicenter_df = find_vulnerability_epicenter(df_internal, target_region)
    with st.expander("View AI Micro-Targeting Insight"):
        if epicenter_coords:
            st.info(generate_ai_assessment(epicenter_df, target_region))
        else:
            st.write(f"Not enough vulnerability data to run clustering algorithm in {target_region}.")
            
    if st.button("Trigger Dispatch Routing"):
        # Cannibalization Check
        if source_region != "Global Nearest (Any)":
            source_fragility = fragility_rates.get(source_region, 0) if 'fragility_rates' in locals() else 0
            if source_fragility > 20.0:
                st.error(f"**Cannibalization Block:** Cannot deploy resources out of {source_region}! Their internal fragility rate is `{source_fragility:.1f}%`, heavily exceeding the `20.0%` safety threshold. Deploying teachers out of this region would cascadingly collapse their network.")
                return
                
        with st.spinner("Calculating geospatial routes..."):
            if use_ai_epicenter and epicenter_coords:
                target_lat, target_lon = epicenter_coords
                routing_msg = f"Routing Computed from {source_region} to AI Epicenter in {target_region}!"
            else:
                target_lat, target_lon = REGION_COORDS[target_region]
                routing_msg = f"Routing Computed from {source_region} to Regional Anchor {target_region}!"
                
            query_subject = None if subject == "Any" else subject
            results = find_nearest_teacher(df_internal, target_lat, target_lon, query_subject, source_region=source_region)
            
            # Construct Arc Data and Update State
            arcs_data = []
            updated_df = st.session_state.get('working_df', df_internal).copy()
            
            for _, row in results.iterrows():
                s_lat = row.get("latitude")
                s_lon = row.get("longitude")
                t_id = row.get("teacher_id")
                
                if s_lat and s_lon:
                    first = row.get("first_name", "")
                    last = row.get("last_name", "")
                    arcs_data.append({
                        "source_lon": s_lon, "source_lat": s_lat,
                        "target_lon": target_lon, "target_lat": target_lat,
                        "teacher_name": f"{first} {last}".strip(),
                        "route_info": f"{source_region} → {target_region}"
                    })
                    
                if t_id:
                    # Dynamically extract teacher and inject into new region to change fragility stats live
                    updated_df = deploy_teacher(updated_df, t_id, target_region)
            
            st.session_state['working_df'] = updated_df
            st.session_state['routing_arcs_df'] = pd.DataFrame(arcs_data)
            st.session_state['dispatch_results'] = results
            st.session_state['dispatch_msg'] = routing_msg
            st.rerun()
            
    if st.session_state.get('dispatch_results') is not None:
        st.success(st.session_state['dispatch_msg'])
        for _, row in st.session_state['dispatch_results'].iterrows():
            t_id = row.get('teacher_id') or 'Unknown'
            first = row.get('first_name') or ''
            last = row.get('last_name') or ''
            name = f"{first} {last}".strip()
            name_str = f" - *{name}*" if name else ""
            
            exp = row.get('years_experience') or 0
            spec = row.get('major_specialization') or 'N/A'
            st.markdown(f"**{t_id}**{name_str} | Spec: **{spec}** | Exp: {exp} yrs")
            
        st.markdown("---")
        if st.button("Reset Logistics Simulation", use_container_width=True):
            from core.data_loader import get_working_dataframe
            active_year = st.session_state.get('active_year', '2026')
            st.session_state['working_df'] = get_working_dataframe(active_year)
            st.session_state['routing_arcs_df'] = None
            st.session_state['dispatch_results'] = None
            st.rerun()