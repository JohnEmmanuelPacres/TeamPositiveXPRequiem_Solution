import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    render_header("Pillar 2: Ingestion Engine", "Semantic Data Fusion & Row Retrieval")
    
    uploaded_file = st.file_uploader("Upload Regional Dataset (CSV)", type="csv")
    
    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        st.write(f"📊 **File detected:** {len(raw_df)} records found.")

        if st.button("🚀 Run AI Semantic Fusion"):
            with st.status("Healing Data Structure...", expanded=True) as status:
                st.write("🧠 Step 1: Mapping columns via AI...")
                clean_df, mapping = ai_normalize_columns(raw_df)
                
                st.write("📍 Step 2: Injecting Map Coordinates...")
                clean_df = get_coordinates(clean_df)
                
                st.write("💾 Step 3: Synchronizing to Global Dashboard...")
                st.session_state['working_df'] = clean_df
                
                status.update(label="Healing Complete!", state="complete", expanded=False)

            st.success(f"Successfully retrieved and standardized **{len(clean_df)}** records.")
            
            # SHOW THE JSON MAPPING (This is what you asked for)
            st.subheader("🔗 AI Mapping Logic")
            st.info("The system mapped your original columns to the STAR Standard like this:")
            st.json(mapping)
            
            # PREVIEW
            st.subheader("✅ Cleaned Data Preview")
            st.dataframe(st.session_state['working_df'], use_container_width=True)
            st.balloons()