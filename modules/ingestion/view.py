import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    render_header("Pillar 2: Ingestion Engine", "Automated Semantic Data Fusion")
    
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
                
                st.write("💾 Synchronizing to Global State...")
                st.session_state['working_df'] = clean_df
                status.update(label="Healing Complete!", state="complete", expanded=False)

            st.success(f"Integration successful! All **{len(clean_df)}** records are now standardized.")
            
            # Display rows in a large container
            st.subheader("✅ Standardized Dataset (Full Retrieval)")
            st.dataframe(clean_df, use_container_width=True, height=500)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔗 AI Mapping/Translation Results")
                st.json(mapping)
            with col2:
                st.subheader("💾 Export Ready")
                csv = clean_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Standardized CSV", data=csv, file_name="star_clean_data.csv", mime='text/csv')

            st.balloons()