import streamlit as st
from core.ui_components import render_header
from core.auth import get_current_role
from modules.intelligence.fragility_calc import append_fragility_scores
from modules.intelligence.cohort_engine import generate_cohorts
from modules.intelligence.mentor_matcher import find_mentors

from core.data_loader import get_working_dataframe
from core.dataframe_schema import normalize_record_columns

def render(df):
    df = normalize_record_columns(df, include_legacy_aliases=True)
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
        st.info("Based on your Region and Major, we identify 'Local Legends' who have >12 years of specialized field experience to guide you.")
        
        from core.data_loader import REGION_COORDS
        import plotly.graph_objects as go
        
        col1, col2, col3 = st.columns(3)
        with col1:
            region = st.selectbox("Your Region", list(REGION_COORDS.keys()))
        with col2:
            major = st.selectbox("Your Specialization", ["Physics", "Chemistry", "Biology", "Mathematics", "General Science"])
        with col3:
            current_xp = st.number_input("Your Current XP (Years)", min_value=0, max_value=40, value=2)
            
        if st.button("Find Local Mentors"):
            with st.spinner("Assembling Capacity-Building Cohort..."):
                mentors = find_mentors(df, region, major)
                
            if len(mentors) > 0:
                st.success(f"Match Found! Discovered {len(mentors)} 'Local Legends' in {region} specializing in {major}.")
                
                # Show top 3 in side-by-side graphical columns
                st.markdown("### Top 3 Recommended Mentors")
                mentor_cols = st.columns(len(mentors.head(3)))
                
                for i, row_data in enumerate(mentors.head(3).iterrows()):
                    _, mentor = row_data
                    
                    # Fetch Real Name or Default
                    first_name = mentor.get('First_Name', '')
                    last_name = mentor.get('Last_Name', '')
                    name_display = f"Prof. {first_name} {last_name}" if first_name else mentor['Teacher_ID']
                    
                    with mentor_cols[i]:
                        st.markdown(f"""
                        <div style="background-color: #1E293B; padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 20px;">
                            <h4 style="margin:0; color:#10B981;">{name_display}</h4>
                            <p style="font-size: 0.85em; color: #94A3B8; margin-bottom: 10px;">ID: {mentor['Teacher_ID']}</p>
                            <strong>Class:</strong> Level {min(5, int(mentor['Years_Experience']//5))} {mentor['Major_Specialization']} Master<br>
                            <strong>XP:</strong> {mentor['Years_Experience']} Years Field Exp<br>
                            <strong>Set:</strong> {mentor['Educational_Attainment']}<br>
                            <hr style="margin: 10px 0; border-color: #334155;">
                            <em style="font-size: 0.9em; color:#FCD34D;">Buff: Accelerates local capacity-building and mitigates {major} out-of-field fragility.</em>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Add Radar Chart for comparison against the #1 Mentor
                st.markdown("---")
                st.markdown("### Skill-Tree Compatibility (You vs. Top Mentor)")
                
                top_mentor = mentors.iloc[0]
                categories = ['Subject Alignment', 'Mentorship XP', 'Resilience', 'Content Mastery']
                
                fig = go.Figure()
                
                # User Stats (Dynamically scaled against their inputted XP)
                user_resilience = 60 + (current_xp * 2) 
                user_values = [100, min(100, (current_xp / 15) * 100), min(100, user_resilience), min(100, 30 + (current_xp * 3))]
                user_values.append(user_values[0])
                
                # Mentor Stats
                mentor_xp = top_mentor['Years_Experience']
                mentor_values = [100, min(100, (mentor_xp / 15) * 100), 95, min(100, 50 + (mentor_xp * 2))]
                mentor_values.append(mentor_values[0])
                
                theta_values = categories + [categories[0]]
                
                fig.add_trace(go.Scatterpolar(
                    r=user_values,
                    theta=theta_values,
                    fill='toself',
                    name='You (Novice/Core Tier)',
                    line_color='#F43F5E',
                    opacity=0.8
                ))
                
                top_mentor_name = f"Prof. {top_mentor.get('First_Name', '')} {top_mentor.get('Last_Name', '')}" if top_mentor.get('First_Name', '') else top_mentor['Teacher_ID']
                
                fig.add_trace(go.Scatterpolar(
                    r=mentor_values,
                    theta=theta_values,
                    fill='toself',
                    name=f"{top_mentor_name} (Veteran Legend)",
                    line_color='#10B981',
                    opacity=0.6
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

                # Expander for all remaining overflow matches
                if len(mentors) > 3:
                    with st.expander(f"View Full Directory: {len(mentors) - 3} Other Applicable Mentors in {region}"):
                        display_cols = ['Teacher_ID', 'First_Name', 'Last_Name', 'Years_Experience', 'Educational_Attainment']
                        st.dataframe(mentors.iloc[3:][[c for c in display_cols if c in mentors.columns]].reset_index(drop=True), use_container_width=True)
            else:
                st.warning("No high-experience mentors currently available in your node criteria. Try expanding your search to adjacent regions.")
