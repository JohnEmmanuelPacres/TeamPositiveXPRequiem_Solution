import streamlit as st
from core.ui_components import render_header
from core.auth import get_current_role
from modules.intelligence.fragility_calc import append_fragility_scores
from modules.intelligence.cohort_engine import generate_cohorts
from modules.intelligence.mentor_matcher import find_mentors

from core.data_loader import get_working_dataframe
from core.dataframe_schema import normalize_record_columns
import plotly.graph_objects as go

def render(df):
    df = normalize_record_columns(df)
    role = get_current_role()
    
    # --- EXACT IMAGE MATCH RESPONSIVE CSS INJECTION ---
    st.markdown("""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Inter:wght@400;500&display=swap");

    /* Force Light Beige Background to match image */
    .stApp { background-color: #F1EFE9 !important; }
    
  /* --- Vertical Tab Navigation Styling --- */

/* 1. Reset: Hide default radio elements globally in the group */
div[role="radiogroup"] > label > div:first-child { 
    display: none !important; 
}

/* 2. Container Setup: Add spacing between navigation items */
div[role="radiogroup"] { 
    gap: 12px; 
    margin-top: 200px;
    margin-left: -30px;
}

/* 3. The Label Button (Static / Inactive State) 
   We style the entire label container to look like a flat button. */
div[role="radiogroup"] label {
    display: flex;
    align-items: center;
    background-color: transparent;
    border-radius: 8px; /* Subtle rounded corner */
    padding: 5px 20px;
    margin: 0 !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: left center;
}

/* Inactive Text Styling: Match Montserrat and lighter gray from design */
div[role="radiogroup"] label p { 
    font-family: 'Montserrat', sans-serif; 
    font-size: 14px; /* Design uses larger font than previous step */
    font-weight: 700; 
    text-transform: uppercase; 
    color: #888 !important; /* Lighter gray for inactive items */
    margin: 0 !important;
    padding-left: 15px;
    border-left: 3px solid transparent;
    transition: color 0.2s ease, border-color 0.2s ease;
    letter-spacing: 0.5px;
}

/* 4. Active State: Bigger, Darker, and the Accent Line 
   This matches the interaction pattern from the previous request. */
div[role="radiogroup"] label[data-checked="True"] {
    background-color: rgba(0,0,0,0.03); /* Extremely subtle fill to define the shape */
    box-shadow: 0 4px 10px rgba(0,0,0,0.02); /* Soft depth */
    transform: scale(1.05); /* Scales the entire button up by 5% */
}

div[role="radiogroup"] label[data-checked="True"] p {
    color: #000 !important; /* Sharp, pure black */
    font-size: 18px; /* Physically larger font */
    border-left: 3px solid #000; /* Bold accent line from design image */
    padding-left: 15px; /* Adds space after the line */
}

/* Optional: Slight hover state for better usability */
div[role="radiogroup"] label:hover:not([data-checked="True"]) p {
    color: #333 !important;
    border-left: 3px solid rgba(0,0,0,0.2);
}

    /* Custom White Metric Cards (Bottom Right) */
    .white-metric-card {
        background-color: rgb(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 90%;
    }
    .wm-label {
    font-family: 'Montserrat', sans-serif;
        color: #6B7280;
        font-size: 15px;
        margin-bottom: 5px;
    }
    .wm-value {
    font-family: 'Montserrat', sans-serif;
        color: #111827;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .wm-pill {
    font-family: 'Montserrat', sans-serif;
        background-color: #E0FAD6;
        color: #1FAD66;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        width: fit-content;
    }
    .wm-pill-red {
        font-family: 'Montserrat', sans-serif;
        background-color: #FFF0F0;
        color: #EC1313;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        width: fit-content;
    }
    
    /* A.S.T.R.A. High-Tech Glass Alert */
.astra-alert-success {
    /* 1. Glass Effect: Light background with high transparency */
    background-color: rgba(209, 244, 217, 0.5); 
    
    /* 2. Frosted Border */
    border: 1.5px solid rgba(31, 173, 102, 0.6);
    
    padding: 20px;
    border-radius: 12px;
    color: #166534;
    font-family: 'Montserrat', sans-serif;
    font-size: 14px;
    margin-bottom: 30px;
    
    /* 3. The "Diamond Glow" Shadow
       This uses a very large blur (30px) and a negative spread (-2px) 
       to make the glow feel like it's radiating from behind the box. */
    box-shadow: 
        0 0 15px rgba(31, 173, 102, 0.2), 
        0 0 35px rgba(31, 173, 102, 0.15);

    /* 4. Backdrop Blur (Optional but recommended for the glass look) */
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* Matching the bold text style from your image */
.astra-alert-success strong {
    font-weight: 800;
    color: #065f46;
    letter-spacing: 0.5px;
}
    
    /* A.S.T.R.A. Critical Error Glass Alert */
.astra-alert-error {
    /* 1. Glass Effect: Light red with 50% transparency */
    background-color: rgba(254, 226, 226, 0.5); 
    
    /* 2. Frosted Red Border */
    border: 1.5px solid rgba(236, 19, 19, 0.6);
    
    padding: 20px;
    border-radius: 12px;
    color: #991B1B;
    font-family: 'Montserrat', sans-serif;
    font-size: 14px;
    margin-bottom: 30px;
    
    /* 3. The "Heat" Glow
       Layer 1: Sharp inner glow for the border
       Layer 2: Wide outer bloom for the "Warning" aura */
    box-shadow: 
        0 0 15px rgba(236, 19, 19, 0.25), 
        0 0 35px rgba(236, 19, 19, 0.18);

    /* 4. Maintaining UI Consistency */
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    transition: none !important;
}

/* Make error titles pop like the "Profit" text */
.astra-alert-error strong {
    font-weight: 800;
    color: #7f1d1d;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

    @media (max-width: 768px) {
        .white-metric-card { margin-bottom: 15px; }
    }

    .hero-subtitle{
    color: #666;
    font-family: 'Montserrat', sans-serif;
    font-size:18px;
    margin-bottom: 130px; /* Big gap for desktop layout */
}

/* Mobile View (Screens smaller than 768px) */
@media (max-width: 768px) {
    .hero-subtitle{
        margin-bottom: 20px !important;  /* Optional: shrink text slightly for mobile too */
    }
}
/* --- Horizontal Tab Navigation (Mobile) --- */
@media (max-width: 768px) {
    /* 1. Force the container into a single horizontal line */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* Prevents tabs from stacking */
        overflow-x: auto; /* Allows swiping if tabs are wide */
        gap: 20px !important;
        margin-top: 20px !important;
        margin-left: 0 !important;
        padding-bottom: 5px;
        border-bottom: 1px solid rgba(0,0,0,0.05); /* Subtle baseline */
    }

    /* Hide the scrollbar but keep the functionality (Chrome/Safari) */
    div[role="radiogroup"]::-webkit-scrollbar {
        display: none;
    }

    /* 2. Style labels as individual tabs */
    div[role="radiogroup"] label {
        padding: 0 !important;
        background-color: transparent !important;
        white-space: nowrap !important; /* Keeps text on one line */
    }

    /* 3. The Text and Bottom Accent */
    div[role="radiogroup"] label p {
        font-size: 12px !important; /* Smaller for mobile fit */
        letter-spacing: 1px;
        padding-left: 0 !important;
        padding-bottom: 8px !important; /* Space above the line */
        border-left: none !important; /* Kill the desktop vertical line */
        border-bottom: 3px solid transparent; /* Placeholder for active state */
        transition: all 0.2s ease;
    }

    /* 4. Active Tab State */
    div[role="radiogroup"] label[data-checked="True" i] p {
        color: #000 !important;
        border-bottom: 3px solid #000 !important; /* The horizontal "active" line */
    }

    /* 5. Scale down the "pop" effect for mobile touch */
    div[role="radiogroup"] label[data-checked="True" i] {
        transform: scale(1) !important; 
        box-shadow: none !important;
    }
}
.divider {
    width: 1.5px;
    height: 100vh; /* Uses viewport height so it stretches down the page */
    background: rgba(224, 224, 224, 0.8);
    margin: 0 auto; /* Centers the line in the small 0.1 column */
    display: block;
}

/* Hide divider on mobile so it doesn't look like a random line between stacked rows */
@media (max-width: 768px) {
    .divider {
        display: none;
    }
}
    </style>
    """, unsafe_allow_html=True)
    
    if role == "Admin":
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
                
                frag_delta = int(df_scored['calculated_fragility_score'].mean()) - prev_avg_frag
                risk_delta = len(df_scored[df_scored['calculated_fragility_score'] > 75]) - prev_high_risk
            except FileNotFoundError:
                frag_delta = 0
                risk_delta = 0
                
        novice_df = df_clustered[df_clustered['Cohort_Name'] == 'Novice Pool']
        novice_count = len(novice_df)
        target_region = novice_df['Region'].mode()[0] if not novice_df.empty else 'NCR'
        
        # --- SPLIT LAYOUT TO MATCH IMAGE EXACTLY ---
        left_col, div_col, right_col = st.columns([1, 0.1, 2.5], gap="small")
        
        with left_col:
            # Custom Large Title matching the image
            st.markdown("""
    <h1 style="color: #44433E; font-family: 'Montserrat', sans-serif; font-size: 3.5rem; line-height: 1.1; margin-bottom: 10px; margin-top: 0;">
        Intelligence<br>Analytics
    </h1>
    <p class="hero-subtitle" style="font-size:1.5rem;">
        Global analytics and K-Means<br>Clustering Typologies.
    </p>
""", unsafe_allow_html=True)
            
            # Vertical Menu (Radio buttons styled via CSS to look like tabs)
            tab_selection = st.radio(
                "Navigation",["Overview Dashboard", "Cohort Analysis", "Regional Heatmap", "Mentorship Network", "Longitudinal Forecast"],
                label_visibility="collapsed"
            )

        with div_col:
            # This renders your CSS divider
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
        with right_col:
            # J.A.R.V.I.S. Style Custom Alert Box
            if active_year == '2026':
                st.markdown(f"""
                <div class="astra-alert-success">
                    <strong>A.S.T.R.A ALERT:</strong> The STAR Program successfully stabilized the network YoY! However, <strong>{novice_count}</strong> 'Novice' teachers remain structurally vulnerable in <strong>{target_region}</strong>. Recommend further local extractions.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="astra-alert-error">
                    <strong>A.S.T.R.A ALERT:</strong> Detected <strong>{novice_count}</strong> 'Novice Pool' teachers currently deployed. High structural vulnerability detected in <strong>{target_region}</strong>. Recommend immediate extraction of 'Core Tier' mentors for targeted capacity building.
                </div>
                """, unsafe_allow_html=True)
            
            # ============ TAB 1: Overview Dashboard ============
            if tab_selection == "Overview Dashboard":
                st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Cohort Distribution</h3>", unsafe_allow_html=True)
                
                cohort_counts = df_clustered['cohort_name'].value_counts()
                fig_dist = go.Figure(data=[
                    go.Bar(
                        x=cohort_counts.index,
                        y=cohort_counts.values,
                        marker_color=['#F43F5E', '#3B82F6', '#10B981'],
                        opacity=0.9
                    )
                ])
                fig_dist.update_layout(
                    plot_bgcolor='rgba(0, 0, 0, 0)', # Beige chart box
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font=dict(color='#333'), # Dark font for light theme
                    xaxis=dict(automargin=True, gridcolor='rgba(0,0,0,0.05)'),
                    yaxis=dict(automargin=True, gridcolor='rgba(0,0,0,0.05)'),
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_dist, use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # The 3 White Custom Cards placed under the chart
                mc1, mc2, mc3 = st.columns(3)
                
                nodes = len(df)
                avg_frag = int(df_scored['calculated_fragility_score'].mean())
                high_risk = len(df_scored[df_scored['calculated_fragility_score'] > 75])
                
                delta_nodes = "↑ Stable Sector" if active_year == '2026' else "↓ Needs Attention"
                delta_pill = "wm-pill" if active_year == '2026' else "wm-pill-red"

                mc1.markdown(f"""
                <div class="white-metric-card">
                    <div class="wm-label">Total Nodes Analyzed</div>
                    <div class="wm-value">{nodes}</div>
                    <div><span class="{delta_pill}">{delta_nodes}</span></div>
                </div>
                """, unsafe_allow_html=True)

                mc2.markdown(f"""
                <div class="white-metric-card">
                    <div class="wm-label">National Fragility Avg</div>
                    <div class="wm-value">{avg_frag}/100</div>
                    <div><span class="{delta_pill}">{delta_nodes}</span></div>
                </div>
                """, unsafe_allow_html=True)

                mc3.markdown(f"""
                <div class="white-metric-card">
                    <div class="wm-label">Critical Risk Nodes</div>
                    <div class="wm-value">{high_risk}</div>
                    <div><span class="{delta_pill}">{delta_nodes}</span></div>
                </div>
                """, unsafe_allow_html=True)
        
            # ============ TAB 2: K-Means Cohort Analysis ============
            elif tab_selection == "Cohort Analysis":
                st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>K-Means Cohort Matrix (Skill-Tree Topology)</h3>", unsafe_allow_html=True)
                
                categories =['Resilience (Stability)', 'Subject Alignment', 'Mentorship XP', 'Content Mastery']
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
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(0, 0, 0, 0.1)')),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#333'), # Light theme compatible font
                    margin=dict(t=30, b=30, l=30, r=30)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # ============ TAB 3: Regional Heatmap ============
            elif tab_selection == "Regional Heatmap":
                st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Regional Cohort Density Heatmap</h3>", unsafe_allow_html=True)
                
                heatmap_data = df_clustered.groupby(['region', 'cohort_name']).size().unstack(fill_value=0)
                
                if 'Novice Pool' in heatmap_data.columns:
                    heatmap_data = heatmap_data.sort_values(by='Novice Pool', ascending=True)
                
                fig_heat = go.Figure(data=go.Heatmap(
                    z=heatmap_data.values,
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    colorscale=[[0, '#F1EFE9'],[0.5, '#FCD34D'],[1.0, '#F43F5E']], # Brightened heatmap scale
                    text=heatmap_data.values,
                    texttemplate="%{text}",
                    showscale=True
                ))
                
                fig_heat.update_layout(
                    plot_bgcolor='rgba(255,255,255,0.7)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#333'),
                    xaxis=dict(title="Cohort Class", automargin=True),
                    yaxis=dict(title="Region", automargin=True),
                    margin=dict(l=10, r=10, t=30, b=10)
                )
                st.plotly_chart(fig_heat, use_container_width=True)
                
                st.markdown("**Cohort Distribution by Region**")
                table_data = heatmap_data.sort_values(by = 'Novice Pool', ascending=False) if 'Novice Pool' in heatmap_data.columns else heatmap_data
                st.dataframe(table_data, use_container_width=True)        
                
            # ============ TAB 4: Mentorship Network ============
            elif tab_selection == "Mentorship Network":
                st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Mentorship Ecosystem Overview</h3>", unsafe_allow_html=True)
                
                veteran_count = len(df_clustered[df_clustered['cohort_name'] == 'Veteran Legends'])
                core_count = len(df_clustered[df_clustered['cohort_name'] == 'Core Tier'])
                novice_count = len(df_clustered[df_clustered['cohort_name'] == 'Novice Pool'])
                
                col_ment1, col_ment2, col_ment3 = st.columns(3)
                col_ment1.markdown(f"<div class='white-metric-card' style='border-left:4px solid #10B981;'><div class='wm-label'>Veteran Legends</div><div class='wm-value' style='color:#10B981;'>{veteran_count}</div></div>", unsafe_allow_html=True)
                col_ment2.markdown(f"<div class='white-metric-card' style='border-left:4px solid #3B82F6;'><div class='wm-label'>Core Tier</div><div class='wm-value' style='color:#3B82F6;'>{core_count}</div></div>", unsafe_allow_html=True)
                col_ment3.markdown(f"<div class='white-metric-card' style='border-left:4px solid #F43F5E;'><div class='wm-label'>Novice Pool</div><div class='wm-value' style='color:#F43F5E;'>{novice_count}</div></div>", unsafe_allow_html=True)
                
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
                
                region_ratios = {}
                for reg in df_clustered['Region'].unique():
                    reg_df = df_clustered[df_clustered['Region'] == reg]
                    r_vet = len(reg_df[reg_df['Cohort_Name'] == 'Veteran Legends'])
                    r_nov = len(reg_df[reg_df['Cohort_Name'] == 'Novice Pool'])
                    if r_vet > 0:
                        region_ratios[reg] = r_nov / r_vet
                    elif r_nov > 0:
                        region_ratios[reg] = r_nov 
                        
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
                        fig_scatter.add_trace(go.Scattergl(
                            x=c_df['Age'],
                            y=c_df['Years_Experience'],
                            mode='markers',
                            name=cohort_name,
                            marker=dict(color=color, size=6, opacity=0.6, line=dict(width=0.5, color='rgba(0,0,0,0.2)')),
                            hovertext=c_df['Region'] + " - " + c_df['Subject_Taught'],
                            hoverinfo='text+x+y+name'
                        ))
                        
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#333'),
                    xaxis=dict(title="Teacher Age", gridcolor='rgba(0, 0, 0, 0.05)', automargin=True),
                    yaxis=dict(title="Years of Experience", gridcolor='rgba(0, 0, 0, 0.05)', automargin=True),
                    hovermode='closest',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(l=10, r=10, t=30, b=10)
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # ============ TAB 5: Longitudinal Forecast ============
            elif tab_selection == "Longitudinal Forecast":
                st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Longitudinal Forecast (2022-2027)</h3>", unsafe_allow_html=True)
                st.info("Analyzing historical fragility and capacity-building metrics to forecast 2027 trajectory using linear projection.")
                
                with st.spinner("Compiling Historical Telemetry..."):
                    import pandas as pd
                    import numpy as np
                    
                    years =['2022', '2023', '2024', '2025', '2026']
                    history_data =[]
                    
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
                            x = hist_df['Year'].values
                            forecast_year = 2027
                            forecast_row = {'Year': forecast_year}
                            
                            for metric in['Fragility', 'Critical Nodes', 'Novice Count']:
                                y_vals = hist_df[metric].values
                                coeffs = np.polyfit(x, y_vals, 1)
                                pred = int(round(np.polyval(coeffs, forecast_year)))
                                forecast_row[metric] = max(0, pred) 
                        
                        fig_trend = go.Figure()
                        
                        colors = {'Fragility': '#F59E0B', 'Critical Nodes': '#F43F5E', 'Novice Count': '#3B82F6'}
                        names = {'Fragility': 'Avg Fragility', 'Critical Nodes': 'Critical Risk Nodes', 'Novice Count': 'Novice Count'}
                        
                        for metric in ['Fragility', 'Critical Nodes', 'Novice Count']:
                            fig_trend.add_trace(go.Scatter(
                                x=hist_df['Year'], y=hist_df[metric],
                                mode='lines+markers',
                                name=f"{names[metric]} (Actual)",
                                line=dict(color=colors[metric], width=3),
                                marker=dict(size=8)
                            ))
                            
                            if has_forecast:
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
                            font=dict(color='#333'),
                            xaxis=dict(title="Year Timeline", tickmode='linear', dtick=1, automargin=True, gridcolor='rgba(0,0,0,0.05)'),
                            yaxis=dict(title="Calculated Volume / Score", automargin=True, gridcolor='rgba(0,0,0,0.05)'),
                            hovermode='x unified',
                            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                            margin=dict(l=10, r=10, t=30, b=10)
                        )
                        
                        st.plotly_chart(fig_trend, use_container_width=True)
                        st.caption("*Dashed lines represent probabilistic OLS linear projections based on baseline STAR programmatic ROI.*")

    else:
        # Teacher View
        
        st.markdown("""
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Inter:wght@400;500&display=swap");

        /* Force Light Beige Background to match image */
        .stApp { background-color: #F1EFE9 !important; }

        /* Custom White Metric Cards */
        .white-metric-card {
            background-color: rgb(255, 255, 255, 0.7); padding: 20px; border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02); display: flex; flex-direction: column;
            justify-content: space-between; height: 100%;
        }

        /* A.S.T.R.A. High-Tech Glass Alerts */
        .astra-alert-success {
            background-color: rgba(209, 244, 217, 0.5); border: 1.5px solid rgba(31, 173, 102, 0.6);
            padding: 20px; border-radius: 12px; color: #166534; font-family: 'Montserrat', sans-serif;
            font-size: 14px; margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(31, 173, 102, 0.2), 0 0 35px rgba(31, 173, 102, 0.15);
            backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        }
        .astra-alert-success strong { font-weight: 800; color: #065f46; letter-spacing: 0.5px; }

        .astra-alert-warning {
            background-color: rgba(254, 243, 199, 0.5); border: 1.5px solid rgba(245, 158, 11, 0.6);
            padding: 20px; border-radius: 12px; color: #92400E; font-family: 'Montserrat', sans-serif;
            font-size: 14px; margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.2), 0 0 35px rgba(245, 158, 11, 0.15);
            backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        }
        .astra-alert-warning strong { font-weight: 800; color: #b45309; letter-spacing: 0.5px; text-transform: uppercase; }

        .astra-alert-info {
            background-color: rgba(219, 234, 254, 0.5); border: 1.5px solid rgba(59, 130, 246, 0.6);
            padding: 20px; border-radius: 12px; color: #1E3A8A; font-family: 'Montserrat', sans-serif;
            font-size: 14px; margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2), 0 0 35px rgba(59, 130, 246, 0.15);
            backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
        }
        .astra-alert-info strong { font-weight: 800; color: #1e40af; letter-spacing: 0.5px; }

        .hero-subtitle{ color: #666; font-family: 'Montserrat', sans-serif; font-size:18px; margin-bottom: 50px; }

        /* Custom Input Labels */
        .stSelectbox label, .stNumberInput label { font-family: 'Montserrat', sans-serif !important; color: #44433E !important; font-weight: 600 !important; }
.divider { width: 1.5px; height: 100vh; background: rgba(224, 224, 224, 0.8); margin: 0 auto; display: block; }
        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .divider { display: none; }
        }
        div.stButton > button[kind="primary"] {
    background-color: #FAFAFA !important;
    color: black !important;
    border: 2px solid #E7E7E7 !important;
    border-radius: 8px !important;

}
        </style>
        """, unsafe_allow_html=True)

        # UI State Management so results don't disappear if user clicks the expander
        if 'mentor_search_triggered' not in st.session_state:
            st.session_state['mentor_search_triggered'] = False

        # --- SPLIT LAYOUT ENGINE ---
        left_col, div_col, right_col = st.columns([1.2, 0.1, 2.5], gap="small")

        from core.data_loader import REGION_COORDS

        with left_col:
            # Custom Large Title matching the image
            st.markdown("""
                <h1 style="color: #44433E; font-family: 'Montserrat', sans-serif; font-size: 3.5rem; line-height: 1.1; margin-bottom: 10px; margin-top: 0;">
                    Career<br>Skill-Tree
                </h1>
                <p class="hero-subtitle" style="font-size:1.5rem;">
                    Your personal growth trajectory and local mentorship ecosystem.
                </p>
            """, unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #44433E; font-family: Montserrat, sans-serif; font-size: 1.2rem;'>Search Parameters</h4>", unsafe_allow_html=True)
            
            # Inputs stacked vertically in the left column for better fit
            region = st.selectbox("Your Region", list(REGION_COORDS.keys()))
            major = st.selectbox("Your Specialization", ["Physics", "Chemistry", "Biology", "Mathematics", "General Science"])
            current_xp = st.number_input("Your Current XP (Years)", min_value=0, max_value=40, value=2)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Find Local Mentors", type="primary", use_container_width=True):
                st.session_state['mentor_search_triggered'] = True

        with div_col:
            # Vertical Line CSS hook
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
        with right_col:
            # Always display the instruction alert at the top of the right column
            st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Mentorship Matcher</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class="astra-alert-info">
                <strong>A.S.T.R.A DIRECTIVE:</strong> Based on your Region and Major, we identify <strong>'Local Legends'</strong> who have >12 years of specialized field experience to guide you.
            </div>
            """, unsafe_allow_html=True)
            
            # Only render results if the button has been clicked
            if st.session_state['mentor_search_triggered']:
                with st.spinner("Assembling Capacity-Building Cohort..."):
                    mentors = find_mentors(df, region, major)
                    
                if len(mentors) > 0:
                    st.markdown(f"""
                    <div class="astra-alert-success">
                        <strong>MATCH FOUND:</strong> Discovered {len(mentors)} 'Local Legends' in {region} specializing in {major}.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Top 3 Recommended Mentors</h3>", unsafe_allow_html=True)
                    mentor_cols = st.columns(len(mentors.head(3)))
                    
                    for i, row_data in enumerate(mentors.head(3).iterrows()):
                        _, mentor = row_data
                        
                        first_name = mentor.get('first_name', '')
                        last_name = mentor.get('last_name', '')
                        name_display = f"Prof. {first_name} {last_name}" if first_name else mentor['teacher_id']
                        
                        with mentor_cols[i]:
                            st.markdown(f"""
                            <div class="white-metric-card" style="border-left: 4px solid #10B981; padding: 15px;">
                                <h5 style="margin:0; color:#10B981; font-family: 'Montserrat', sans-serif;">{name_display}</h5>
                                <p style="font-size: 0.85em; color: #666; margin-bottom: 10px; font-family: 'Montserrat', sans-serif;">ID: {mentor['teacher_id']}</p>
                                <div style="color: #333; font-size: 0.9em; line-height: 1.5; font-family: 'Inter', sans-serif;">
                                    <strong>Class:</strong> Level {min(5, int(mentor['years_experience']//5))} {mentor['major_specialization']} Master<br>
                                    <strong>XP:</strong> {mentor['years_experience']} Years Field Exp<br>
                                    <strong>Set:</strong> {mentor['educational_attainment']}<br>
                                </div>
                                <hr style="margin: 10px 0; border-color: #E5E7EB;">
                                <em style="font-size: 0.85em; color:#D97706; font-family: 'Inter', sans-serif;">Buff: Accelerates local capacity-building.</em>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("<br><h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Skill-Tree Compatibility (You vs. Top Mentor)</h3>", unsafe_allow_html=True)
                    
                    top_mentor = mentors.iloc[0]
                    categories =['Subject Alignment', 'Mentorship XP', 'Resilience', 'Content Mastery']
                    
                    fig = go.Figure()
                    
                    user_resilience = 60 + (current_xp * 2) 
                    user_values =[100, min(100, (current_xp / 15) * 100), min(100, user_resilience), min(100, 30 + (current_xp * 3))]
                    user_values.append(user_values[0])
                    
                    mentor_xp = top_mentor['years_experience']
                    mentor_values =[100, min(100, (mentor_xp / 15) * 100), 95, min(100, 50 + (mentor_xp * 2))]
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
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(0, 0, 0, 0.1)')),
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), 
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#333'),
                        margin=dict(t=30, b=30, l=10, r=10) 
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    if len(mentors) > 3:
                        with st.expander(f"View Full Directory: {len(mentors) - 3} Other Applicable Mentors in {region}"):
                            display_cols =['teacher_id', 'first_name', 'last_name', 'years_experience', 'educational_attainment']
                            st.dataframe(mentors.iloc[3:][[c for c in display_cols if c in mentors.columns]].reset_index(drop=True), use_container_width=True)
                else:
                    st.markdown("""
                    <div class="astra-alert-warning">
                        <strong>NO DIRECT MATCHES:</strong> No high-experience mentors currently available in your node criteria. Try expanding your search to adjacent regions.
                    </div>
                    """, unsafe_allow_html=True)