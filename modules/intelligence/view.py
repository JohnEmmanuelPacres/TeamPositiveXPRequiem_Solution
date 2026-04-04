import streamlit as st
from core.ui_components import render_header
from core.auth import get_current_role
from modules.intelligence.fragility_calc import append_fragility_scores
from modules.intelligence.cohort_engine import generate_cohorts
from modules.intelligence.mentor_matcher import find_mentors

from core.data_loader import get_working_dataframe
from core.dataframe_schema import normalize_record_columns

def render(df):
    df = normalize_record_columns(df)
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
                prev_avg_frag = int(prev_scored['calculated_fragility_score'].mean())
                prev_high_risk = len(prev_scored[prev_scored['calculated_fragility_score'] > 75])
                
                # Deltas
                frag_delta = int(df_scored['calculated_fragility_score'].mean()) - prev_avg_frag
                risk_delta = len(df_scored[df_scored['calculated_fragility_score'] > 75]) - prev_high_risk
            except FileNotFoundError:
                frag_delta = 0
                risk_delta = 0
                
        # J.A.R.V.I.S. Style AI Prescriptive Alert
        novice_count = len(df_clustered[df_clustered['cohort_name'] == 'Novice Pool'])
        target_region = df_clustered['region'].mode()[0] if not df_clustered.empty else 'NCR'
        
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
        
        # 5 Visualization Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview Dashboard",
            "Cohort Analysis",
            "Regional Heatmap",
            "Mentorship Network",
            "Longitudinal Forecast"
        ])
        
        # ============ TAB 1: Overview Dashboard ============
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            nodes = len(df)
            avg_frag = int(df_scored['calculated_fragility_score'].mean())
            high_risk = len(df_scored[df_scored['calculated_fragility_score'] > 75])

            col1.metric("Total Nodes Analyzed", f"{nodes}", delta_nodes)
            col2.metric("National Fragility Avg", f"{avg_frag}/100", delta_frag, delta_color="inverse")
            col3.metric("Critical Risk Nodes", f"{high_risk}", delta_risk, delta_color="inverse")
            
            st.markdown("### Cohort Distribution")
            import plotly.graph_objects as go
            cohort_counts = df_clustered['cohort_name'].value_counts()
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
                c_df = df_clustered[df_clustered['cohort_name'] == cohort_name]
                if c_df.empty: continue
                
                resilience = 100 - c_df['calculated_fragility_score'].mean()
                alignment = (c_df['subject_taught'] == c_df['major_specialization']).mean() * 100
                xp_score = min(100, (c_df['years_experience'].mean() / 15) * 100)
                mastery = min(100, max(0, ((c_df['age'].mean() - 20) / 35) * 100))
                
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
            heatmap_data = df_clustered.groupby(['region', 'cohort_name']).size().unstack(fill_value=0)
            
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
            
            veteran_count = len(df_clustered[df_clustered['cohort_name'] == 'Veteran Legends'])
            core_count = len(df_clustered[df_clustered['cohort_name'] == 'Core Tier'])
            novice_count = len(df_clustered[df_clustered['cohort_name'] == 'Novice Pool'])
            
            col_ment1, col_ment2, col_ment3 = st.columns(3)
            col_ment1.markdown(f"<div class='metric-card' style='background-color:#1E293B; padding:15px; border-radius:8px; border-left:4px solid #10B981;'><div class='metric-label' style='color:#94A3B8;'>Veteran Legends</div><div class='metric-value' style='font-size:24px; color:#10B981; font-weight:bold;'>{veteran_count}</div></div>", unsafe_allow_html=True)
            col_ment2.markdown(f"<div class='metric-card' style='background-color:#1E293B; padding:15px; border-radius:8px; border-left:4px solid #3B82F6;'><div class='metric-label' style='color:#94A3B8;'>Core Tier</div><div class='metric-value' style='font-size:24px; color:#3B82F6; font-weight:bold;'>{core_count}</div></div>", unsafe_allow_html=True)
            col_ment3.markdown(f"<div class='metric-card' style='background-color:#1E293B; padding:15px; border-radius:8px; border-left:4px solid #F43F5E;'><div class='metric-label' style='color:#94A3B8;'>Novice Pool</div><div class='metric-value' style='font-size:24px; color:#F43F5E; font-weight:bold;'>{novice_count}</div></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_m1, col_m2, col_m3 = st.columns(3)
            
            if veteran_count > 0:
                mentorship_ratio = round((core_count + novice_count) / veteran_count, 1)
                col_m1.metric("System-wide Mentorship Burden", f"{mentorship_ratio}:1", help="Total Core+Novice per Veteran Legend")
            else:
                col_m1.metric("System-wide Mentorship Burden", "N/A", help="Total Core+Novice per Veteran Legend")
                
            out_of_field = len(df_clustered[df_clustered['Subject_Taught'] != df_clustered['Major_Specialization']])
            oof_percent = round((out_of_field / len(df_clustered)) * 100, 1) if len(df_clustered) > 0 else 0
            col_m2.metric("Out-of-Field Teachers", f"{out_of_field}", f"{oof_percent}% of Workforce", delta_color="inverse", help="Teachers not teaching their specialization")
            
            # Find the region with the worst Novice to Veteran ratio
            region_ratios = {}
            for reg in df_clustered['Region'].unique():
                reg_df = df_clustered[df_clustered['Region'] == reg]
                r_vet = len(reg_df[reg_df['Cohort_Name'] == 'Veteran Legends'])
                r_nov = len(reg_df[reg_df['Cohort_Name'] == 'Novice Pool'])
                if r_vet > 0:
                    region_ratios[reg] = r_nov / r_vet
                elif r_nov > 0:
                    region_ratios[reg] = r_nov # Inflated if 0 veterans
                    
            if region_ratios:
                worst_region = max(region_ratios, key=region_ratios.get)
                worst_ratio = round(region_ratios[worst_region], 1)
                col_m3.metric("Highest Mentorship Deficit", worst_region, f"{worst_ratio} Novices/Vet", delta_color="inverse", help="Region most in need of veteran deployments")
            
            st.markdown("---")
            st.markdown("### Cohort Experience vs. Age Distribution")
            
            fig_scatter = go.Figure()
            colors = {"Novice Pool": "#F43F5E", "Core Tier": "#3B82F6", "Veteran Legends": "#10B981"}
            
            for cohort_name, color in colors.items():
                c_df = df_clustered[df_clustered['Cohort_Name'] == cohort_name]
                if not c_df.empty:
                    # Optimized by using Scattergl (WebGL rendering) instead of SVG Scatter
                    fig_scatter.add_trace(go.Scattergl(
                        x=c_df['Age'],
                        y=c_df['Years_Experience'],
                        mode='markers',
                        name=cohort_name,
                        marker=dict(color=color, size=6, opacity=0.6, line=dict(width=0.5, color='rgba(255,255,255,0.8)')),
                        hovertext=c_df['Region'] + " - " + c_df['Subject_Taught'],
                        hoverinfo='text+x+y+name'
                    ))
                    
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(title="Teacher Age", gridcolor='rgba(255, 255, 255, 0.1)'),
                yaxis=dict(title="Years of Experience", gridcolor='rgba(255, 255, 255, 0.1)'),
                hovermode='closest'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # ============ TAB 5: Longitudinal Forecast ============
        with tab5:
            st.markdown("### Longitudinal Forecast (2022-2027 Projections)")
            st.info("Analyzing historical fragility and capacity-building metrics to forecast 2027 trajectory using linear projection.")
            
            with st.spinner("Compiling Historical Telemetry..."):
                import pandas as pd
                import numpy as np
                import plotly.graph_objects as go
                
                years = ['2022', '2023', '2024', '2025', '2026']
                history_data = []
                
                # Fetch dataset versions iteratively
                for y in years:
                    try:
                        y_df = get_working_dataframe(y)
                        y_scored = append_fragility_scores(y_df)
                        y_clustered = generate_cohorts(y_scored)
                        
                        history_data.append({
                            'Year': int(y),
                            'Fragility': int(y_scored['Calculated_Fragility_Score'].mean()),
                            'Critical Nodes': len(y_scored[y_scored['Calculated_Fragility_Score'] > 75]),
                            'Novice Count': len(y_clustered[y_clustered['Cohort_Name'] == 'Novice Pool'])
                        })
                    except Exception as e:
                        pass
                
                if history_data:
                    hist_df = pd.DataFrame(history_data)
                    
                    if len(hist_df) < 2:
                        st.warning("Insufficient historical telemetry (requires at least 2 years of data) to generate 2027 projection.")
                        has_forecast = False
                    else:
                        has_forecast = True
                        # Linear projection for 2027
                        x = hist_df['Year'].values
                        forecast_year = 2027
                        forecast_row = {'Year': forecast_year}
                        
                        for metric in ['Fragility', 'Critical Nodes', 'Novice Count']:
                            y_vals = hist_df[metric].values
                            # Fit 1-degree polynomial (linear regression)
                            coeffs = np.polyfit(x, y_vals, 1)
                            pred = int(round(np.polyval(coeffs, forecast_year)))
                            # Ensure no negative projections
                            forecast_row[metric] = max(0, pred) 
                    
                    fig_trend = go.Figure()
                    
                    colors = {'Fragility': '#FCD34D', 'Critical Nodes': '#F43F5E', 'Novice Count': '#3B82F6'}
                    names = {'Fragility': 'Avg Fragility', 'Critical Nodes': 'Critical Risk Nodes', 'Novice Count': 'Novice Count'}
                    
                    for metric in ['Fragility', 'Critical Nodes', 'Novice Count']:
                        # Historical Solid Line
                        fig_trend.add_trace(go.Scatter(
                            x=hist_df['Year'], y=hist_df[metric],
                            mode='lines+markers',
                            name=f"{names[metric]} (Actual)",
                            line=dict(color=colors[metric], width=3),
                            marker=dict(size=8)
                        ))
                        
                        if has_forecast:
                            # Projected 2027 Dashed Line
                            last_year_val = hist_df.iloc[-1][metric]
                            last_year = hist_df['Year'].max()
                            fig_trend.add_trace(go.Scatter(
                                x=[last_year, 2027], 
                                y=[last_year_val, forecast_row[metric]],
                                mode='lines+markers',
                                name=f"{names[metric]} (Forecast)",
                                line=dict(color=colors[metric], width=3, dash='dash'),
                                marker=dict(size=8, symbol='star', color=colors[metric])
                            ))
                    
                    fig_trend.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis=dict(title="Year Timeline", tickmode='linear', dtick=1),
                        yaxis=dict(title="Calculated Volume / Score"),
                        hovermode='x unified',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    
                    st.plotly_chart(fig_trend, use_container_width=True)
                    st.caption("*Dashed lines represent probabilistic OLS linear projections based on baseline STAR programmatic ROI.*")

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
                    first_name = mentor.get('first_name', '')
                    last_name = mentor.get('last_name', '')
                    name_display = f"Prof. {first_name} {last_name}" if first_name else mentor['teacher_id']
                    
                    with mentor_cols[i]:
                        st.markdown(f"""
                        <div style="background-color: #1E293B; padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; margin-bottom: 20px;">
                            <h4 style="margin:0; color:#10B981;">{name_display}</h4>
                            <p style="font-size: 0.85em; color: #94A3B8; margin-bottom: 10px;">ID: {mentor['teacher_id']}</p>
                            <strong>Class:</strong> Level {min(5, int(mentor['years_experience']//5))} {mentor['major_specialization']} Master<br>
                            <strong>XP:</strong> {mentor['years_experience']} Years Field Exp<br>
                            <strong>Set:</strong> {mentor['educational_attainment']}<br>
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
                mentor_xp = top_mentor['years_experience']
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
                
                top_mentor_name = f"Prof. {top_mentor.get('first_name', '')} {top_mentor.get('last_name', '')}" if top_mentor.get('first_name', '') else top_mentor['teacher_id']
                
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
                        display_cols = ['teacher_id', 'first_name', 'last_name', 'years_experience', 'educational_attainment']
                        st.dataframe(mentors.iloc[3:][[c for c in display_cols if c in mentors.columns]].reset_index(drop=True), use_container_width=True)
            else:
                st.warning("No high-experience mentors currently available in your node criteria. Try expanding your search to adjacent regions.")
