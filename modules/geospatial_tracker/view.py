import streamlit as st
import pydeck as pdk
from core.ui_components import render_header
from modules.geospatial_tracker.map_engine import render_map
from modules.geospatial_tracker.routing import find_nearest_teacher

def render(df):
    render_header("Deployment Logistics Map", "Geospatial deployment and vulnerability tracking.")
    
    st.markdown("### Teacher Density Map")
    render_map(df)
    
    st.markdown("---")
    st.subheader("Dispatch Routing Algorithm")
    st.info("Simulates calculating distance to deploy teachers based on proximity and discipline match for emergency schooling zones.")
    
    col1, col2 = st.columns(2)
    with col1:
        target_lat = st.number_input("Target Latitude (e.g. 14.599)", value=14.5995, format="%.4f")
        target_lon = st.number_input("Target Longitude (e.g. 120.984)", value=120.9842, format="%.4f")
    with col2:
        subject = st.selectbox("Require Subject Specialization", ["Any", "Chemistry", "Physics", "Biology", "Mathematics", "General Science"])
        
    if st.button("Trigger Dispatch Routing"):
        with st.spinner("Finding nearest viable candidates..."):
            query_subject = None if subject == "Any" else subject
            results = find_nearest_teacher(df, target_lat, target_lon, query_subject)
            st.success("Routing Computed!")
            
            # Show candidates nicely
            for _, row in results.iterrows():
                st.markdown(f"**{row['Teacher_ID']}** (Exp: {row['Years_Experience']} yrs) | Spec: {row['Major_Specialization']} | Distance: `{row['Distance_from_target']:.2f}`")

