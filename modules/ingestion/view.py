import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    if st.session_state.get('integration_success'):
        st.success("Integration successful! Records have been pushed to Active Memory.")
        st.balloons()
        st.session_state['integration_success'] = False
        
    render_header("Ingestion Engine", "Automated Semantic Data Fusion")
    
    st.info("💡 **Hackathon Feature:** This engine uses Multilingual AI to map Tagalog headers and automatically translate unknown columns to English.")

    uploaded_file = st.file_uploader("Upload Regional Dataset (CSV)", type="csv")
    
    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        st.write(f"📄 **Raw Data:** `{len(raw_df)}` records and `{len(raw_df.columns)}` columns detected.")

        if st.button("🚀 Execute AI Fusion"):
            with st.status("Healing Data Structure...", expanded=True) as status:
                st.write("🧠 Analyzing Meanings & Translating Headers...")
                clean_df, mapping = ai_normalize_columns(raw_df)
                
                st.write("📍 Injecting Geospatial Anchors...")
                clean_df = get_coordinates(clean_df)
                
                st.session_state['staged_df'] = clean_df
                st.session_state['staged_mapping'] = mapping
                status.update(label="Healing Complete & Data Staged!", state="complete", expanded=False)

    if 'staged_df' in st.session_state:
        clean_df = st.session_state['staged_df']
        mapping = st.session_state['staged_mapping']
        
        st.markdown("---")
        st.info(f"💾 **Session Restored:** Found uncommitted staged dataset ({len(clean_df)} records) waiting in Active Memory cache.")
        st.subheader("🛡️ Pipeline Quality Gates")
        
        # --- QUALITY CHECKS ---
        can_integrate = True
        
        # 1. Volume Threshold Check (Soft Warning)
        record_count = len(clean_df)
        if record_count < 500:
            st.warning(f"**Volume Warning:** Only `{record_count}` records detected. The Intelligence engines require at least `500` rows to generate statistically significant insights mimicking the benchmark dataset.")
        else:
            st.success(f"**Volume Check Passed:** `{record_count}` records detected. Optimal density achieved.")
            
        # 2. Critical Features Check (Hard Block)
        missing_criticals = []
        critical_features = ["region", "subject_taught", "major_specialization", "teacher_id"]
        
        for col in critical_features:
            if (clean_df[col] == "not_specified").all():
                missing_criticals.append(col)
                
        if missing_criticals:
            can_integrate = False
            st.error(f"**Structural Block:** The semantic engine could not locate equivalents for: `{', '.join(missing_criticals)}`")
            st.info("💡 **Action Required:** Please update your CSV to include these mandatory columns before integration. Without them, the Neural and Geospatial algorithms will encounter fatal runtime errors.")
        else:
            st.success("**Structural Check Passed:** All critical features successfully mapped by the AI.")
            
        # 3. Supplemental Features Check (Soft Warning)
        missing_supplemental = []
        supplemental_features = ["years_experience", "age", "educational_attainment"]
        for col in supplemental_features:
            if col in clean_df.columns and (clean_df[col] == "not_specified").all():
                missing_supplemental.append(col)
                
        if missing_supplemental:
            st.warning(f"**Feature Warning:** Missing analytical parameters: `{', '.join(missing_supplemental)}`. The system will substitute synthetic defaults, but strategic calculations may degrade.")
        
        # --- INTEGRATION STAGE ---
        if can_integrate:
            st.markdown("---")
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