import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    render_header("Pillar 2: Ingestion Engine", "Semantic Schema Healer & Data Fusion")
    
    st.markdown("""
    ### 🧠 How it works:
    This engine uses a **Local Sentence-Transformer (AI)** to find the mathematical meaning of messy column headers. 
    It bridges fragmented regional data into the **STAR-Standard Schema**.
    """)
    
    uploaded_file = st.file_uploader("Upload Fragmented Dataset (CSV)", type="csv")
    
    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Raw Data Input")
            st.caption(f"Detected {len(raw_df.columns)} columns")
            st.dataframe(raw_df.head(5), height=200)

        if st.button("🚀 Run AI Semantic Fusion"):
            with st.status("AI is reasoning through schema...", expanded=True) as status:
                
                st.write("Step 1: Computing Semantic Similarity...")
                clean_df, mapping = ai_normalize_columns(raw_df)
                
                st.write("Step 2: Resolving Geospatial Coordinates...")
                clean_df = get_coordinates(clean_df)
                
                st.write("Step 3: Injecting into Global State...")
                # CRITICAL: This updates the whole app's data
                st.session_state['working_df'] = clean_df
                
                status.update(label="Healing Complete!", state="complete", expanded=False)

            st.success("Dataset Unified & Lat/Lng Injected!")
            
            # Show the Mapping logic (Judges love this)
            with st.expander("View AI Mapping Logic (JSON)"):
                st.json(mapping)
                
            st.subheader("Healed STAR-Standard Dataset")
            st.dataframe(st.session_state['working_df'].head(10))
            
            st.balloons()