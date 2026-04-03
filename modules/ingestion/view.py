import streamlit as st
import pandas as pd
from core.ui_components import render_header
from modules.ingestion.schema_healer import ai_normalize_columns, get_coordinates

def render():
    render_header("Pillar 2: Ingestion Engine", "Automated Semantic Data Fusion")
    
    st.markdown("""
    ### 🤖 Autonomous Schema Resolver
    This engine uses **Multilingual AI** combined with **Pattern Recognition** to identify data columns, even if they are in Tagalog or have generic names.
    """)

    uploaded_file = st.file_uploader("Upload Regional Dataset (CSV)", type="csv")
    
    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        st.write(f"📊 **File detected:** {len(raw_df)} records.")

        if st.button("🚀 Execute AI Fusion"):
            with st.status("Analyzing Data Patterns...", expanded=True) as status:
                st.write("🧠 Reading Header Semantics & Cell Patterns...")
                # The heavy lifting
                clean_df, mapping = ai_normalize_columns(raw_df)
                
                st.write("📍 Injecting Geospatial Anchors...")
                clean_df = get_coordinates(clean_df)
                
                st.session_state['working_df'] = clean_df
                status.update(label="Healing Complete!", state="complete", expanded=False)

            st.success("Integration successful.")

            # Show the Proof
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader("🔗 Mapping Decisions")
                st.json(mapping)
            with col2:
                st.subheader("✅ Unified Data Preview")
                st.dataframe(clean_df.head(10))

            st.balloons()