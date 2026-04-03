import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    st.header("📥 Ingestion Engine")
    uploaded_file = st.file_uploader("Upload Data", type="csv")
    
    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        st.write(f"📄 Original File: {len(raw_df)} rows detected.")

        if st.button("🚀 Run AI Semantic Fusion"):
            with st.status("Processing...") as status:
                # Process data
                clean_df, mapping = ai_normalize_columns(raw_df)
                clean_df = get_coordinates(clean_df)
                
                # Save to Global State
                st.session_state['working_df'] = clean_df
                status.update(label="Healing Complete!", state="complete")

            st.success(f"Successfully processed {len(clean_df)} rows.")
            
            # Show the counts to prove it worked
            st.metric("Total Teachers Ingested", len(clean_df))
            
            with st.expander("Show Data Preview"):
                st.dataframe(clean_df) # This shows the scrollable table