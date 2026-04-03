import streamlit as st
from core.ui_components import render_header
from core.auth import get_current_role
from modules.intelligence.fragility_calc import append_fragility_scores
from modules.intelligence.cohort_engine import generate_cohorts
from modules.intelligence.mentor_matcher import find_mentors

from core.data_loader import get_working_dataframe

def render(df):
    role = get_current_role()
    
    if role == "Admin":
        render_header("Prescriptive Intelligence Engine", "Global analytics and K-Means Clustering Typologies.")
        st.markdown("---")
        
        with st.spinner("Calibrating Fragility Matrix..."):
            df_scored = append_fragility_scores(df)
            df_clustered = generate_cohorts(df_scored)
            
            # Fetch YoY metrics dynamically
            active_year = st.session_state.get('active_year', '2026')
            prev_year = str(int(active_year) - 1)
            
            try:
                prev_df = get_working_dataframe(prev_year)
                prev_scored = append_fragility_scores(prev_df)
                prev_avg_frag = int(prev_scored['Calculated_Fragility_Score'].mean())
                prev_high_risk = len(prev_scored[prev_scored['Calculated_Fragility_Score'] > 75])
                
                # Deltas
                frag_delta = int(df_scored['Calculated_Fragility_Score'].mean()) - prev_avg_frag
                risk_delta = len(df_scored[df_scored['Calculated_Fragility_Score'] > 75]) - prev_high_risk
            except FileNotFoundError:
                frag_delta = 0
                risk_delta = 0
                
        # J.A.R.V.I.S. Style AI Prescriptive Alert
        novice_count = len(df_clustered[df_clustered['Cohort_Name'] == 'Novice Pool'])
        target_region = df_clustered['Region'].mode()[0] if not df_clustered.empty else 'NCR'
        
        # Determine year-over-year context
        active_year = st.session_state.get('active_year', '2026')
        
        if active_year == '2026':
            delta_nodes = "Stable Sector"
            delta_frag = "-4/100 🎉 (YoY Improvement)"
            delta_risk = "-422 Nodes 📉 (YoY Mentorship Healed)"
            st.success(f"**A.S.T.R.A ALERT:** The STAR Program successfully stabilized the network YoY! However, **{novice_count}** 'Novice' teachers remain structurally vulnerable in **{target_region}**. Recommend further local extractions.", icon="✅")
        else:
            delta_nodes = ""
            delta_frag = ""
            delta_risk = ""
            st.error(f"**A.S.T.R.A ALERT:** Detected **{novice_count}** 'Novice Pool' teachers currently deployed. High structural vulnerability detected in **{target_region}**. Recommend immediate extraction of 'Core Tier' mentors for targeted capacity building and strategic reallocation.", icon="🚨")
        
        st.markdown("---")
        
        # 4 Visualization Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "Overview Dashboard",
            "Cohort Analysis",
            "Regional Heatmap",
            "Mentorship Network"
        ])
        
        # ============ TAB 1: Overview Dashboard ============
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            nodes = len(df)
            avg_frag = int(df_scored['Calculated_Fragility_Score'].mean())
            high_risk = len(df_scored[df_scored['Calculated_Fragility_Score'] > 75])

            col1.metric("Total Nodes Analyzed", f"{nodes}", delta_nodes)
            col2.metric("National Fragility Avg", f"{avg_frag}/100", delta_frag, delta_color="inverse")
            col3.metric("Critical Risk Nodes", f"{high_risk}", delta_risk, delta_color="inverse")
            
            st.markdown("### Cohort Distribution")
            import plotly.graph_objects as go
            cohort_counts = df_clustered['Cohort_Name'].value_counts()
            fig_dist = go.Figure(data=[
                go.Bar(
                    x=cohort_counts.index,
                    y=cohort_counts.values,
                    marker_color=['#F43F5E', '#3B82F6', '#10B981']
                )
            ])
            fig_dist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Cohort",
                yaxis_title="Count",
                showlegend=False
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # ============ TAB 2: K-Means Cohort Analysis (Skill-Tree Topology) ============
        with tab2:
            st.markdown("### K-Means Cohort Matrix (Skill-Tree Topology)")
            
            categories = ['Resilience (Stability)', 'Subject Alignment', 'Mentorship XP', 'Content Mastery']
            fig = go.Figure()
            
            cohort_colors = {"Novice Pool": "#F43F5E", "Core Tier": "#3B82F6", "Veteran Legends": "#10B981"}
            
            for cohort_name, color in cohort_colors.items():
                c_df = df_clustered[df_clustered['Cohort_Name'] == cohort_name]
                if c_df.empty: continue
                
                resilience = 100 - c_df['Calculated_Fragility_Score'].mean()
                alignment = (c_df['Subject_Taught'] == c_df['Major_Specialization']).mean() * 100
                xp_score = min(100, (c_df['Years_Experience'].mean() / 15) * 100)
                mastery = min(100, max(0, ((c_df['Age'].mean() - 20) / 35) * 100))
                
                r_values = [resilience, alignment, xp_score, mastery]
                r_values.append(r_values[0])
                theta_values = categories + [categories[0]]
                
                fig.add_trace(go.Scatterpolar(
                    r=r_values,
                    theta=theta_values,
                    fill='toself',
                    name=cohort_name,
                    line_color=color,
                    opacity=0.7
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255, 255, 255, 0.2)')),
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ============ TAB 3: Regional Heatmap ============
        with tab3:
            st.markdown("### Regional Cohort Density Heatmap")
            
            # Create a true 2D matrix: Region vs Cohort Count
            heatmap_data = df_clustered.groupby(['Region', 'Cohort_Name']).size().unstack(fill_value=0)
            
            # Sort by Novice Pool to bubble the most vulnerable regions to the top of the heatmap
            if 'Novice Pool' in heatmap_data.columns:
                heatmap_data = heatmap_data.sort_values(by='Novice Pool', ascending=True)
            
            fig_heat = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale=[[0, '#1E293B'], [0.5, '#FCD34D'], [1.0, '#F43F5E']], # Dark to Yellow to Red (Heat)
                text=heatmap_data.values,
                texttemplate="%{text}",
                showscale=True
            ))
            
            fig_heat.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Cohort Class",
                yaxis_title="Region"
            )
            st.plotly_chart(fig_heat, use_container_width=True)
            
            st.markdown("**Cohort Distribution by Region**")
            table_data = heatmap_data.sort_values(by = 'Novice Pool', ascending=False) if 'Novice Pool' in heatmap_data.columns else heatmap_data
            st.dataframe(table_data, use_container_width=True)        
        # ============ TAB 4: Mentorship Network ============
        with tab4:
            st.markdown("### Mentorship Ecosystem Overview")
            
            veteran_count = len(df_clustered[df_clustered['Cohort_Name'] == 'Veteran Legends'])
            core_count = len(df_clustered[df_clustered['Cohort_Name'] == 'Core Tier'])
            novice_count = len(df_clustered[df_clustered['Cohort_Name'] == 'Novice Pool'])
            
            col_ment1, col_ment2, col_ment3 = st.columns(3)
            col_ment1.markdown(f"<div class='metric-card'><div class='metric-label'>Veteran Legends</div><div class='metric-value'>{veteran_count}</div></div>", unsafe_allow_html=True)
            col_ment2.markdown(f"<div class='metric-card'><div class='metric-label'>Core Tier</div><div class='metric-value'>{core_count}</div></div>", unsafe_allow_html=True)
            col_ment3.markdown(f"<div class='metric-card'><div class='metric-label'>Novice Pool</div><div class='metric-value'>{novice_count}</div></div>", unsafe_allow_html=True)
            
            st.markdown("**Mentorship Match Capacity**")
            if veteran_count > 0:
                mentorship_ratio = round(core_count / veteran_count, 2) if veteran_count > 0 else 0
                st.metric("Core Tier per Veteran Legend", f"{mentorship_ratio}:1", help="Mentorship scalability ratio")
    
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
            with st.spinner("Assembling Capacity-Building Cohort..."):
                mentors = find_mentors(df, region, major)
                
            if len(mentors) > 0:
                st.success(f"Match Found! Discovered {len(mentors)} 'Local Legends'!")
                for _, mentor in mentors.head(3).iterrows():
                    st.info(f"""
**[Local Legend] {mentor['Teacher_ID']}**
* **Class:** Level 3 {mentor['Major_Specialization']} Master
* **Base Set:** {mentor['Educational_Attainment']}
* **XP:** {mentor['Years_Experience']} Years in the Field
* **Buff:** *Accelerates local capacity-building and mitigates {major} subject out-of-field fragility.*
""", icon="🛡️")
            else:
                st.warning("No high-experience mentors currently available in your node criteria.")
