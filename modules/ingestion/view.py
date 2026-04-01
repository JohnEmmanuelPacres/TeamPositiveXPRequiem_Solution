import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import normalize_dataframe_columns

def render():
    render_header("Schema Healer", "Upload messy regional data sets to automatically map them to the system schema.")
    
    st.info("The Ingestion Engine uses 'thefuzz' to string-match drifty legacy column headers (e.g. 'Tcher_Lvl') to system standards (e.g. 'Certification_Level').")
    
    uploaded_file = st.file_uploader("Upload Fragmented Data (CSV)", type="csv")
    
    if uploaded_file is not None:
        try:
            # Emulate ingestion
            raw_df = pd.read_csv(uploaded_file)
            st.subheader("Raw Fragmented Columns detected:")
            st.write(raw_df.columns.tolist())
            
            with st.spinner("Healing Schema via String Tokenization..."):
                clean_df = normalize_dataframe_columns(raw_df)
                
            st.success("Successfully Normalized Columns!")
            st.write(clean_df.head(5))
        except Exception as e:
            st.error(f"Error reading file: {e}")
