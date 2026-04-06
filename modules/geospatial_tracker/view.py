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
        
    # --- EXACT IMAGE MATCH RESPONSIVE CSS INJECTION ---
    st.markdown("""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Inter:wght@400;500&display=swap");

    /* Force Light Beige Background to match image */
    .stApp { background-color: #F1EFE9 !important; }
    
    /* --- Vertical Tab Navigation Styling --- */
    div[role="radiogroup"] > label > div:first-child { display: none !important; }
    div[role="radiogroup"] { gap: 12px; margin-top: 50px; margin-left: -30px; }
    div[role="radiogroup"] label {
        display: flex; align-items: center; background-color: transparent;
        border-radius: 8px; padding: 5px 20px; margin: 0 !important;
        cursor: pointer !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform-origin: left center;
    }
    div[role="radiogroup"] label p { 
        font-family: 'Montserrat', sans-serif; font-size: 14px; font-weight: 600; 
        text-transform: uppercase; color: #888 !important; margin: 0 !important;
        padding-left: 15px; border-left: 3px solid transparent;
        transition: color 0.2s ease, border-color 0.2s ease; letter-spacing: 0.5px;
    }
    div[role="radiogroup"] label[data-checked="True"] {
        background-color: rgba(0,0,0,0.03); box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        transform: scale(1.05); 
    }
    div[role="radiogroup"] label[data-checked="True"] p {
        color: #000 !important; font-size: 18px; border-left: 3px solid #000; padding-left: 15px; 
    }
    div[role="radiogroup"] label:hover:not([data-checked="True"]) p {
        color: #333 !important; border-left: 3px solid rgba(0,0,0,0.2);
    }

    /* Custom White Metric Cards */
    .white-metric-card {
        background-color: rgb(255, 255, 255, 0.7); padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02); display: flex; flex-direction: column;
        justify-content: space-between; height: 100%;
    }
    
    /* A.S.T.R.A. High-Tech Glass Alerts */
    .astra-alert-success {
        background-color: rgba(209, 244, 217, 0.5); border: 1.5px solid rgba(31, 173, 102, 0.6);
        padding: 20px; border-radius: 12px; color: #166534; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(31, 173, 102, 0.2), 0 0 35px rgba(31, 173, 102, 0.15);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    }
    .astra-alert-success strong { font-weight: 700; color: #065f46; letter-spacing: 0.5px; }
    
    .astra-alert-error {
        background-color: rgba(254, 226, 226, 0.5); border: 1.5px solid rgba(236, 19, 19, 0.6);
        padding: 20px; border-radius: 12px; color: #991B1B; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(236, 19, 19, 0.25), 0 0 35px rgba(236, 19, 19, 0.18);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    }
    .astra-alert-error strong { font-weight: 700; color: #7f1d1d; letter-spacing: 0.5px; text-transform: uppercase; }

    .astra-alert-warning {
        background-color: rgba(254, 243, 199, 0.5); border: 1.5px solid rgba(245, 158, 11, 0.6);
        padding: 20px; border-radius: 12px; color: #92400E; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px; margin-top: 10px;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2), 0 0 35px rgba(245, 158, 11, 0.15);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    }
    .astra-alert-warning strong { font-weight: 700; color: #F6B802; letter-spacing: 0.5px; text-transform: uppercase; }

    .hero-subtitle{
    color: #666;
    font-family: 'Montserrat', sans-serif;
    font-size:18px;
    margin-bottom: 130px; /* Big gap for desktop layout */
}

/* Mobile View (Screens smaller than 768px) */
@media (max-width: 768px) {
    .hero-subtitle{
        margin-bottom: 20px !important;  /* Optional: shrink text slightly for mobile too */
    }
}
    /* Custom Input Labels */
    .stSelectbox label, .stCheckbox label { font-family: 'Montserrat', sans-serif !important; color: #44433E !important; font-weight: 600 !important; }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        div[role="radiogroup"] {
            display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
            overflow-x: auto; gap: 20px !important; margin-top: 20px !important;
            margin-left: 0 !important; padding-bottom: 5px; border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        div[role="radiogroup"]::-webkit-scrollbar { display: none; }
        div[role="radiogroup"] label { padding: 0 !important; background-color: transparent !important; white-space: nowrap !important; }
        div[role="radiogroup"] label p {
            font-size: 12px !important; letter-spacing: 1px; padding-left: 0 !important;
            padding-bottom: 8px !important; border-left: none !important;
            border-bottom: 3px solid transparent;
        }
        div[role="radiogroup"] label[data-checked="True" i] p { color: #000 !important; border-bottom: 3px solid #000 !important; }
        div[role="radiogroup"] label[data-checked="True" i] { transform: scale(1) !important; box-shadow: none !important; }
        .divider { display: none; }
    }

    div.stButton > button[kind="primary"] {
    background-color: #FAFAFA !important;
    color: black !important;
    border: 2px solid #E7E7E7 !important;
    border-radius: 8px !important;

}
    
    .divider { width: 1.5px; height: 100vh; background: rgba(224, 224, 224, 1); margin: 0 auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

    # --- 1. SELF-HEALING & NORMALIZATION ---
    df_internal = normalize_record_columns(df)

    # Ensure mandatory columns exist
    for target_col in ["subject_taught", "major_specialization", "region", "teacher_id", "years_experience"]:
        if target_col not in df_internal.columns:
            df_internal[target_col] = "not_specified"

    # --- LAYOUT ENGINE: Exact Image Split Structure ---
    left_col, div_col, right_col = st.columns([1, 0.1, 2.5], gap="small")
    
    with left_col:
        st.markdown("""
            <h1 style="color: #44433E; font-family: 'Montserrat', sans-serif; font-size: 3.3rem; line-height: 1.1; margin-bottom: 0px; margin-top: 0; font-weight: 600;">
        Deployment<br>Logistics Map
            </h1>
            <p class="hero-subtitle" style="font-size:1.5rem;">
                Geospatial deployment and vulnerability tracking.
            </p>
        """, unsafe_allow_html=True)
        
        # --- 2. VISUALIZATION MODE LOGIC (Now styled as the side navigation) ---
        v_modes = ["Total Workforce Density", "Underserved Hotspots (Out-of-Field)"]
        v_idx = v_modes.index(st.session_state.get('geo_view_mode', v_modes[0]))
        view_mode = st.radio("Navigation", v_modes, index=v_idx, label_visibility="collapsed")
        st.session_state['geo_view_mode'] = view_mode

    with div_col:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
    with right_col:
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
                
            st.markdown(f"""
            <div class="astra-alert-warning">
                <strong>AI Regional Suggestion:</strong> {override_msg}The system suggests prioritizing <strong>{priority_region}</strong>. Data indicates a <code>{priority_rate:.1f}%</code> out-of-field teaching vulnerability in this zone.
            </div>
            """, unsafe_allow_html=True)
        except:
            priority_region = "NCR"
            st.info("Awaiting more specific data for regional priority calculation.")

        map_df = df_internal.copy()
        if "Underserved" in view_mode:
            # Comparison logic: compare stripped, lowercased values to find true mismatches
            map_df = df_internal[
                df_internal['subject_taught'].str.strip().str.lower() != 
                df_internal['major_specialization'].str.strip().str.lower()
            ].copy()
        
        # Now pass it to the actual engine
        st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif; margin-top: 0;'>Regional Geospatial Map</h3>", unsafe_allow_html=True)
        render_map(map_df, arcs_df=st.session_state.get('routing_arcs_df'))
        
        st.markdown("<br><h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Dispatch Routing Algorithm</h3>", unsafe_allow_html=True)
        
        # --- 4. DISPATCH UI ---
        st.markdown('<div style="margin-bottom: 0px;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            region_options = list(REGION_COORDS.keys())
            source_options = ["Global Nearest (Any)"] + region_options
            s_idx = source_options.index(st.session_state.get('geo_source_region', source_options[0]))
            source_region = st.selectbox("Source Deployment Region", source_options, index=s_idx)
            st.session_state['geo_source_region'] = source_region
            
        with col2:
            default_index = region_options.index(priority_region) if priority_region in region_options else 0
            saved_target = st.session_state.get('geo_target_region')
            t_idx = region_options.index(saved_target) if saved_target in region_options else default_index
            target_region = st.selectbox("Target Deployment Zone", region_options, index=t_idx)
            st.session_state['geo_target_region'] = target_region
            
        with col3:
            subject_opts = ["Any", "Chemistry", "Physics", "Biology", "Mathematics", "General Science"]
            sub_idx = subject_opts.index(st.session_state.get('geo_subject', subject_opts[0]))
            subject = st.selectbox("Request Specialization", subject_opts, index=sub_idx)
            st.session_state['geo_subject'] = subject
            
            epicenter_val = st.session_state.get('geo_use_ai_epicenter', True)
            use_ai_epicenter = st.checkbox("Deploy to AI Epicenter", value=epicenter_val)
            st.session_state['geo_use_ai_epicenter'] = use_ai_epicenter
        st.markdown('</div>', unsafe_allow_html=True)
            
        # AI Epicenter logic
        epicenter_coords, epicenter_df = find_vulnerability_epicenter(df_internal, target_region)
        with st.expander("View AI Micro-Targeting Insight"):
            if epicenter_coords:
                st.info(generate_ai_assessment(epicenter_df, target_region))
            else:
                st.write(f"Not enough vulnerability data to run clustering algorithm in {target_region}.")
                
        if st.button("Trigger Dispatch Routing", type="primary", use_container_width=True):
            # Cannibalization Check
            if source_region != "Global Nearest (Any)":
                source_fragility = fragility_rates.get(source_region, 0) if 'fragility_rates' in locals() else 0
                if source_fragility > 20.0:
                    st.markdown(f"""
                    <div class="astra-alert-error">
                        <strong>Cannibalization Block:</strong> Cannot deploy resources out of {source_region}! Their internal fragility rate is <code>{source_fragility:.1f}%</code>, heavily exceeding the <code>20.0%</code> safety threshold. Deploying teachers out of this region would cascadingly collapse their network.
                    </div>
                    """, unsafe_allow_html=True)
                    st.stop()
                    
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
            st.markdown(f"""
            <div class="astra-alert-success" style="margin-top: 20px;">
                <strong>A.S.T.R.A DISPATCH:</strong> {st.session_state['dispatch_msg']}
            </div>
            """, unsafe_allow_html=True)
            
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