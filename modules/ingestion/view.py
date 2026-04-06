import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    if 'integration_success' not in st.session_state:
        st.session_state['integration_success'] = False

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
        font-family: 'Montserrat', sans-serif; font-size: 14px; font-weight: 700; 
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
        margin-top: -50px;
    }
    .astra-alert-success strong { font-weight: 800; color: #065f46; letter-spacing: 0.5px; }
    
    .astra-alert-error {
        background-color: rgba(254, 226, 226, 0.5); border: 1.5px solid rgba(236, 19, 19, 0.6);
        padding: 20px; border-radius: 12px; color: #991B1B; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(236, 19, 19, 0.25), 0 0 35px rgba(236, 19, 19, 0.18);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        margin-top: -50px;
    }
    .astra-alert-error strong { font-weight: 800; color: #7f1d1d; letter-spacing: 0.5px; text-transform: uppercase; }

    .astra-alert-warning {
        background-color: rgba(254, 243, 199, 0.5); border: 1.5px solid rgba(245, 158, 11, 0.6);
        padding: 20px; border-radius: 12px; color: #92400E; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2), 0 0 35px rgba(245, 158, 11, 0.15);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        margin-top: -50px;
    }
    .astra-alert-warning strong { font-weight: 800; color: #b45309; letter-spacing: 0.5px; text-transform: uppercase; }

    .astra-alert-info {
        background-color: rgba(219, 234, 254, 0.5); border: 1.5px solid rgba(59, 130, 246, 0.6);
        padding: 20px; border-radius: 12px; color: #1E3A8A; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2), 0 0 35px rgba(59, 130, 246, 0.15);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        margin-top: -50px;
    }
    .astra-alert-info strong { font-weight: 800; color: #1e40af; letter-spacing: 0.5px; }

    .hero-subtitle{ color: #666; font-family: 'Montserrat', sans-serif; font-size:18px; margin-bottom: 30px; }
.divider { width: 1.5px; height: 100vh; background: rgba(224, 224, 224, 0.8); margin: 0 auto; display: block; margin-top: -100px; }
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
        .divider {
        display: none;
        }
    }    
    
    </style>
    """, unsafe_allow_html=True)

    # --- SPLIT LAYOUT ENGINE ---
    left_col, div_col, right_col = st.columns([1, 0.1, 2.5], gap="small")

    with left_col:
        st.markdown("""
            <h1 style="color: #44433E; font-family: 'Montserrat', sans-serif; font-size: 3.5rem; line-height: 1.1; margin-bottom: 10px; margin-top: -100px;">
                Ingestion<br>Engine
            </h1>
            <p class="hero-subtitle" style="font-size:1.5rem;">
                Automated Semantic Data Fusion.
            </p>
        """, unsafe_allow_html=True)
        
        # Static Navigation Element to match the UI visual structure
        nav_options = ["Pipeline Console"]
        if 'staged_df' in st.session_state:
            nav_options.append("Quality Gates")
        
        v_mode = st.radio("Navigation", nav_options, label_visibility="collapsed")

    with div_col:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


    with right_col:
        if st.session_state.get('integration_success'):
            st.markdown("""
            <div class="astra-alert-success">
                <strong>SUCCESS:</strong> Integration successful! Records have been pushed to Active Memory.
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            st.session_state['integration_success'] = False

        if v_mode == "Pipeline Console":
            st.markdown("""
            <div class="astra-alert-info">
                <strong>💡 Hackathon Feature:</strong> This engine uses Multilingual AI to map Tagalog headers and automatically translate unknown columns to English.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif; margin-top: 0;'>Data Upload & Fusion</h3>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload Regional Dataset (CSV)", type="csv")
            
            if uploaded_file:
                raw_df = pd.read_csv(uploaded_file)
                st.write(f"📄 **Raw Data:** `{len(raw_df)}` records and `{len(raw_df.columns)}` columns detected.")

                if st.button("🚀 Execute AI Fusion", use_container_width=True, type="primary"):
                    with st.status("Healing Data Structure...", expanded=True) as status:
                        st.write("🧠 Analyzing Meanings & Translating Headers...")
                        clean_df, mapping = ai_normalize_columns(raw_df)
                        
                        st.write("📍 Injecting Geospatial Anchors...")
                        clean_df = get_coordinates(clean_df)
                        
                        st.session_state['staged_df'] = clean_df
                        st.session_state['staged_mapping'] = mapping
                        status.update(label="Healing Complete & Data Staged! Check Quality Gates.", state="complete", expanded=False)
                    st.rerun()

        if 'staged_df' in st.session_state and (v_mode == "Quality Gates" or v_mode == "Pipeline Console"):
            clean_df = st.session_state['staged_df']
            mapping = st.session_state['staged_mapping']
            
            if v_mode == "Pipeline Console":
                st.markdown("<hr style='opacity: 0.2;'>", unsafe_allow_html=True)
                
            st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>🛡️ Pipeline Quality Gates</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #666; font-family: Montserrat, sans-serif;'>💾 <strong>Session Restored:</strong> Found uncommitted staged dataset ({len(clean_df)} records) waiting in Active Memory cache.</p>", unsafe_allow_html=True)
            
            # --- QUALITY CHECKS ---
            can_integrate = True
            
            # 1. Volume Threshold Check (Soft Warning)
            record_count = len(clean_df)
            if record_count < 500:
                st.markdown(f"""
                <div class="astra-alert-warning">
                    <strong>Volume Warning:</strong> Only <code>{record_count}</code> records detected. The Intelligence engines require at least <code>500</code> rows to generate statistically significant insights mimicking the benchmark dataset.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="astra-alert-success">
                    <strong>Volume Check Passed:</strong> <code>{record_count}</code> records detected. Optimal density achieved.
                </div>
                """, unsafe_allow_html=True)
                
            # 2. Critical Features Check (Hard Block)
            missing_criticals = []
            critical_features = ["region", "subject_taught", "major_specialization", "teacher_id"]
            
            for col in critical_features:
                if (clean_df[col] == "not_specified").all():
                    missing_criticals.append(col)
                    
            if missing_criticals:
                can_integrate = False
                st.markdown(f"""
                <div class="astra-alert-error">
                    <strong>Structural Block:</strong> The semantic engine could not locate equivalents for: <code>{', '.join(missing_criticals)}</code><br><br>
                    <strong>Action Required:</strong> Please update your CSV to include these mandatory columns before integration. Without them, the Neural and Geospatial algorithms will encounter fatal runtime errors.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="astra-alert-success">
                    <strong>Structural Check Passed:</strong> All critical features successfully mapped by the AI.
                </div>
                """, unsafe_allow_html=True)
                
            # 3. Supplemental Features Check (Soft Warning)
            missing_supplemental = []
            supplemental_features = ["years_experience", "age", "educational_attainment"]
            for col in supplemental_features:
                if col in clean_df.columns and (clean_df[col] == "not_specified").all():
                    missing_supplemental.append(col)
                    
            if missing_supplemental:
                st.markdown(f"""
                <div class="astra-alert-warning">
                    <strong>Feature Warning:</strong> Missing analytical parameters: <code>{', '.join(missing_supplemental)}</code>. The system will substitute synthetic defaults, but strategic calculations may degrade.
                </div>
                """, unsafe_allow_html=True)
            
            # --- INTEGRATION STAGE ---
            if can_integrate:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✅ Confirm & Integrate into Global State", type="primary", use_container_width=True):
                    st.session_state['working_df'] = clean_df
                    
                    # Clean up session state explicitly to reset UI properly
                    if 'staged_df' in st.session_state:
                        del st.session_state['staged_df']
                    if 'staged_mapping' in st.session_state:
                        del st.session_state['staged_mapping']
                        
                    st.session_state['integration_success'] = True
                    st.rerun()
            
            with st.expander("🔍 View Standardized Output & AI Translations"):
                st.dataframe(clean_df, use_container_width=True, height=400)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.json(mapping)
                with col2:
                    csv = clean_df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Standardized Databank", data=csv, file_name="star_clean_data.csv", mime='text/csv')