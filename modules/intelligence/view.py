import streamlit as st
from core.ui_components import render_header
from core.auth import get_current_role
from modules.intelligence.fragility_calc import append_fragility_scores
from modules.intelligence.cohort_engine import generate_cohorts
from modules.intelligence.mentor_matcher import find_mentors

def render(df):
    role = get_current_role()
    
    if role == "Admin":
        render_header("Prescriptive Intelligence Engine", "Global analytics and K-Means Clustering Typologies.")
        st.markdown("---")
        
        with st.spinner("Processing Matrix..."):
            df_scored = append_fragility_scores(df)
            df_clustered = generate_cohorts(df_scored)
            
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-card'><div class='metric-label'>Total Nodes Analyzed</div><div class='metric-value'>{len(df)}</div></div>", unsafe_allow_html=True)
        avg_frag = int(df_scored['Calculated_Fragility_Score'].mean())
        col2.markdown(f"<div class='metric-card'><div class='metric-label'>National Fragility Avg</div><div class='metric-value'>{avg_frag}/100</div></div>", unsafe_allow_html=True)
        high_risk = len(df_scored[df_scored['Calculated_Fragility_Score'] > 75])
        col3.markdown(f"<div class='metric-card'><div class='metric-label'>Critical Risk Nodes</div><div class='metric-value'>{high_risk}</div></div>", unsafe_allow_html=True)
        
        st.markdown("### K-Means Cohort Matrix")
        st.bar_chart(df_clustered['Cohort_Name'].value_counts(), color="#1E3A8A")
        
    else:
        # Teacher View
        render_header("Career Skill-Tree Matrix", "Your personal growth trajectory and local mentorship ecosystem.")
        st.markdown("---")
        
        st.subheader("Mentorship Matcher")
        st.info("Based on your Region (e.g., NCR) and Major (e.g., Physics), we identify 'Local Legends' who have >12 years of specialized field experience to guide you.")
        
        from core.data_loader import REGION_COORDS
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Your Region", list(REGION_COORDS.keys()))
        with col2:
            major = st.selectbox("Your Specialization", ["Physics", "Chemistry", "Biology", "Mathematics", "General Science"])
            
        if st.button("Find Local Mentors"):
            with st.spinner("Searching neural net for matches..."):
                mentors = find_mentors(df, region, major)
                
            if len(mentors) > 0:
                st.success(f"Discovered {len(mentors)} Mentorship Options!")
                for _, mentor in mentors.head(3).iterrows():
                    st.markdown(f"- **{mentor['Teacher_ID']}**: {mentor['Years_Experience']} Yrs Field Experience | Base: {mentor['Educational_Attainment']}")
            else:
                st.warning("No high-experience mentors currently available in your node criteria.")
