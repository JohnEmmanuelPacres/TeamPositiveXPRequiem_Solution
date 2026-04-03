import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates, TARGET_SCHEMA

def render():
    render_header("Pillar 2: Ingestion Engine", "Semantic Data Fusion & Row Retrieval")
    
    uploaded_file = st.file_uploader("Upload Regional Dataset (CSV)", type="csv")
    
    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        st.write(f"📊 **File detected:** {len(raw_df)} records found.")

        # 1. RUN AI ANALYSIS
        if 'pending_mapping' not in st.session_state:
            with st.spinner("AI is translating and mapping headers..."):
                _, mapping = ai_normalize_columns(raw_df)
                st.session_state['pending_mapping'] = mapping

        # 2. LET USER VERIFY (Human-in-the-loop)
        st.subheader("🔗 AI Proposed Mapping")
        st.info("The Multilingual AI translated your headers. You can adjust them below if needed.")
        
        final_mapping = {}
        cols = st.columns(2)
        
        for i, (orig, suggested) in enumerate(st.session_state['pending_mapping'].items()):
            target_col = cols[i % 2].selectbox(
                f"Map: '{orig}' to...",
                options=["Ignore"] + TARGET_SCHEMA,
                index=TARGET_SCHEMA.index(suggested) + 1 if suggested in TARGET_SCHEMA else 0,
                key=f"map_{i}"
            )
            if target_col != "Ignore":
                final_mapping[orig] = target_col

        # 3. APPLY AND SYNC
        if st.button("🚀 Confirm & Sync to Dashboard"):
            with st.status("Finalizing Data Integration...") as status:
                # Rename columns based on the (potentially edited) mapping
                clean_df = raw_df.rename(columns=final_mapping)
                
                # Fill missing columns
                for col in TARGET_SCHEMA:
                    if col not in clean_df.columns:
                        clean_df[col] = "Not Specified"
                
                st.write("📍 Resolving Map Coordinates...")
                clean_df = get_coordinates(clean_df)
                
                st.session_state['working_df'] = clean_df
                status.update(label="Sync Complete!", state="complete")
                
            st.success(f"Standardized {len(clean_df)} records. The Map and Analytics are now live!")
            st.balloons()
            
            with st.expander("Preview Integrated Data"):
                st.dataframe(st.session_state['working_df'].head(10))