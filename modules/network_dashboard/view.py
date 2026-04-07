import streamlit as st
import streamlit.components.v1 as components
from core.ui_components import render_header
from modules.network_dashboard.graph_builder import build_pyvis_graph
from modules.network_dashboard.simulator import deploy_teacher
from core.data_loader import REGION_COORDS
from core.dataframe_schema import normalize_record_columns

def render(df):
    df = normalize_record_columns(df)
    
    # --- EXACT IMAGE MATCH RESPONSIVE CSS INJECTION ---
    st.markdown("""
    <style>
    /* Force Light Beige Background */
    .stApp { background-color: #F1EFE9 !important; }
    
    /* --- Vertical Tab Navigation Styling --- */
    div[role="radiogroup"] > label > div:first-child { display: none !important; }
    div[role="radiogroup"] { gap: 12px; margin-top: 50px; margin-left: -30px; }
    div[role="radiogroup"] label {
        display: flex; align-items: center; background-color: transparent;
        border-radius: 8px; padding: 5px 20px; margin: 0 !important;
        cursor: pointer !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform-origin: left center;
    }
    div[role="radiogroup"] label p { 
        font-family: 'Montserrat', sans-serif; font-size: 14px; font-weight: 600; 
        text-transform: uppercase; color: #888 !important; margin: 0 !important;
        padding-left: 15px; border-left: 3px solid transparent;
        transition: color 0.2s ease, border-color 0.2s ease; letter-spacing: 0.5px;
    }
    div[role="radiogroup"] label[data-checked="True"] {
        background-color: rgba(0,0,0,0.03); box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        transform: scale(1.05); 
    }
    div[role="radiogroup"] label[data-checked="True"] p {
        color: #000 !important; font-size: 18px; border-left: 3px solid #000; padding-left: 15px; 
    }
    div[role="radiogroup"] label:hover:not([data-checked="True"]) p {
        color: #333 !important; border-left: 3px solid rgba(0,0,0,0.2);
    }
     /* Mobile Responsiveness */
    @media (max-width: 768px) {
        div[role="radiogroup"] {
            display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
            overflow-x: auto; gap: 20px !important; margin-top: 20px !important;
            margin-left: 0 !important; padding-bottom: 5px; border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        div[role="radiogroup"]::-webkit-scrollbar { display: none; }
        div[role="radiogroup"] label { padding: 0 !important; background-color: transparent !important; white-space: nowrap !important; }
        div[role="radiogroup"] label p {
            font-size: 12px !important; letter-spacing: 1px; padding-left: 0 !important;
            padding-bottom: 8px !important; border-left: none !important;
            border-bottom: 3px solid transparent;
        }
        div[role="radiogroup"] label[data-checked="True" i] p { color: #000 !important; border-bottom: 3px solid #000 !important; }
        div[role="radiogroup"] label[data-checked="True" i] { transform: scale(1) !important; box-shadow: none !important; }
        .divider { display: none; }
    }

    /* Custom White Cards for Graph and UI */
    .white-metric-card {
         background-color: rgb(255, 255, 255, 0.7); padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02); height: 100%;
    }
    .wm-label { color: #6B7280; font-size: 13px; font-family: 'Montserrat', sans-serif; font-weight: 600; margin-bottom: 5px; text-transform: uppercase;}
    .wm-value { color: #10B981; font-size: 24px; font-weight: 700; }
    
    /* Graph Container */
    .graph-wrapper {
        background-color: #FFFFFF; border-radius: 12px; padding: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02); margin-bottom: 20px;
    }
    .hero-subtitle{
    color: #666;
    font-family: 'Montserrat', sans-serif;
    font-size:18px;
    margin-bottom: 150px; /* Big gap for desktop layout */
}
  .astra-alert-info {
        background-color: rgba(219, 234, 254, 0.5); border: 1.5px solid rgba(59, 130, 246, 0.6);
        padding: 20px; border-radius: 12px; color: #1E3A8A; font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2), 0 0 35px rgba(59, 130, 246, 0.15);
        backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    }
    .astra-alert-info strong { font-weight: 800; color: #1e40af; letter-spacing: 0.5px; }

/* Mobile View (Screens smaller than 768px) */
@media (max-width: 768px) {
    .hero-subtitle{
        margin-bottom: 20px !important;  /* Optional: shrink text slightly for mobile too */
    }
}

    .divider {
    width: 1.5px;
    height: 100vh; /* Uses viewport height so it stretches down the page */
    background: rgba(224, 224, 224, 0.8);
    margin: 0 auto; /* Centers the line in the small 0.1 column */
    display: block;
    margin-top: -100px;
}

/* Hide divider on mobile so it doesn't look like a random line between stacked rows */
@media (max-width: 768px) {
    .divider {
        display: none;
    }
}
div.stButton > button[kind="primary"] {
    background-color:rgba(0, 0, 0, 0.5); !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;

}
    </style>
    """, unsafe_allow_html=True)

    # --- SPLIT LAYOUT UI ---
    left_col, div_col, right_col = st.columns([1, 0.1, 2.5], gap="small")
    
    with left_col:
        st.markdown("""
            <h1 style="color: #44433E; font-family: 'Montserrat', sans-serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 20px; margin-top: -100px;">Obsidian<br>Mentorship</h1>
            <p class="hero-subtitle" style="font-size:1.5rem;">
        Interactive mapping of localized<br>teaching resources.
    </p>""", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif;'>Intervention Engine</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div class="astra-alert-info">
                Simulate re-assigning a teacher to fix regional fragility bottlenecks dynamically.
            </div>
            """, unsafe_allow_html=True)  
        if df.empty:
            st.warning("No teacher data available for simulation.")
        else:
                teacher_records = df.set_index("teacher_id").to_dict("index")
                def format_teacher_label(tid):
                    row = teacher_records[tid]
                    first = row.get("first_name", "")
                    last = row.get("last_name", "")
                    name_prefix = f"Prof. {first} {last}".strip()
                    name_display = f"{name_prefix} | " if name_prefix else ""
                    return f"{name_display}{tid} | Current: {row['region']} | {row['years_experience']} Yrs"
                
                st.markdown("<div class='wm-label'>1. Select Extraction Target</div>", unsafe_allow_html=True)
                teacher_id = st.selectbox(
                    "Select Global Teacher Node", 
                    options=df["teacher_id"].tolist(),
                    format_func=format_teacher_label,
                    label_visibility="collapsed"
                )

                st.markdown("<div class='wm-label'>2. Select Injection Target</div>", unsafe_allow_html=True)
                new_region = st.selectbox(
                    "Target Regional Hub:", 
                    list(REGION_COORDS.keys()),
                    label_visibility="collapsed"
                )

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Trigger Deployment Simulation", type="primary", use_container_width=True):
                    st.session_state['working_df'] = deploy_teacher(df, teacher_id, new_region)
                    
                    if 'regional_alerts' not in st.session_state:
                        st.session_state['regional_alerts'] = []
                    
                    row = df[df["teacher_id"] == teacher_id].iloc[0]
                    prof_name = f"Prof. {row.get('first_name', '')} {row.get('last_name', '')}".strip()
                    prof_name = prof_name if prof_name != "Prof." else teacher_id
                    
                    st.session_state['regional_alerts'].append({
                        "region": new_region,
                        "message": f"**INCOMING ALLY:** {prof_name} ({row['years_experience']} Yrs Exp, {row['major_specialization']}) has just been re-routed to the {new_region} ecosystem to assist with localized capacity building!"
                    })
                    
                    st.success(f"Successfully deployed {teacher_id} to {new_region}. Metrics recalculated.")
                    st.rerun()

                if st.button("Reset Deployment Simulation", use_container_width=True):
                    from core.data_loader import get_working_dataframe
                    active_year = st.session_state.get('active_year', '2026')
                    st.session_state['working_df'] = get_working_dataframe(active_year)
                    st.session_state['regional_alerts'] = [] 
                    st.success("Simulation reset. Teachers returned to original regions.")
                    st.rerun()

    with div_col:
        # This renders your CSS divider
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with right_col:
        # ============ TAB 1: Topological Map ============
            st.markdown("<h3 style='color: #44433E; font-family: Montserrat, sans-serif; margin-bottom: 5px; margin-top: -100px;'>Ecosystem Topology</h3>", unsafe_allow_html=True)
            
            # Map Controls
            control_col, info_col = st.columns([1, 1])
            with control_col:
                target_region = st.selectbox("Filter Topology by Region:", ["All Regions"] + list(REGION_COORDS.keys()))
            with info_col:
                st.markdown("<div style='font-size: 0.85rem; color: #666; padding-top: 5px;'><strong>Navigation:</strong><br>• Scroll to zoom in/out<br>• Click & drag to pan/move nodes</div>", unsafe_allow_html=True)

            if target_region == "All Regions":
                st.markdown("""
            <div class="astra-alert-info">
                <strong>Note:</strong> When viewing 'All Regions', the graph is limited to a global cross-section of 150 nodes to prevent browser crashing. Filter by a specific region for a complete local view.
            </div>
            """, unsafe_allow_html=True)
                working_df = df
                node_limit = 150 
            else:
                working_df = df[df['region'] == target_region]
                node_limit = 35 
                
            with st.spinner("Rendering Physics Sandbox..."):
                html_data = build_pyvis_graph(working_df, limit=node_limit)
                components.html(html_data, height=530)
                
            # Overflow
            overflow_count = len(working_df) - node_limit
            if overflow_count > 0:
                with st.expander(f"View {overflow_count} Additional Teachers (Hidden due to Node Density Limits)"):
                    st.dataframe(working_df.iloc[node_limit:][["teacher_id", "first_name", "last_name", "region", "major_specialization", "years_experience"]].reset_index(drop=True), use_container_width=True)

            # Clean Legend UI
            st.markdown("""
            <div class='white-metric-card' style='display: flex; justify-content: space-around; flex-wrap: wrap; padding: 15px;'>
                <div>
                    <div class='wm-label'>Node Shapes</div>
                    <div style='font-size: 13px; color: #444;'>⭐ Local Legend (15+ Yrs)<br>🔵 Standard Node<br>🔴 Region Hub</div>
                </div>
                <div>
                    <div class='wm-label'>Subject Colors (A-M)</div>
                    <div style='font-size: 13px; color: #444;'>🟦 Physics<br>🟩 Chemistry<br>🟧 Biology</div>
                </div>
                <div>
                    <div class='wm-label'>Subject Colors (N-Z)</div>
                    <div style='font-size: 13px; color: #444;'>🟪 Math<br>⬜ Gen Sci<br>⚪ Other</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_teacher_view(df):
    # --- EXACT IMAGE MATCH RESPONSIVE CSS INJECTION FOR TEACHER ---
    st.markdown("""
    <style>
    .stApp { background-color: #F1EFE9 !important; }
    div[role="radiogroup"] > label > div:first-child { display: none !important; }
    div[role="radiogroup"] { gap: 15px; margin-top: 50px; }
    div[role="radiogroup"] label p { 
        font-family: 'Montserrat', sans-serif; font-size: 12px; font-weight: 600; 
        text-transform: uppercase; color: #888 !important; padding-left: 15px;
        border-left: 2px solid transparent; transition: all 0.2s ease-in-out; margin: 0;
    }
    div[role="radiogroup"] label[data-checked="true"] p {
        color: #111 !important; font-size: 14px; font-weight: 800; 
        border-left: 3px solid #111; padding-left: 18px; 
    }
    .white-metric-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02); height: 100%;
        margin-bottom: 20px;
    }
    .wm-label { color: #6B7280; font-size: 13px; font-family: 'Montserrat', sans-serif; font-weight: 600; margin-bottom: 5px; text-transform: uppercase;}
    .wm-value { font-size: 28px; font-weight: 700; }
    .divider {
    width: 1.5px;
    height: 100vh; /* Uses viewport height so it stretches down the page */
    background: rgba(224, 224, 224, 0.8);
    margin: 0 auto; /* Centers the line in the small 0.1 column */
    display: block;
    margin-top: -100px;
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

/* Hide divider on mobile so it doesn't look like a random line between stacked rows */
@media (max-width: 768px) {
    .divider {
        display: none;
    }
}
    .graph-wrapper { background-color: #FFFFFF; border-radius: 12px; padding: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

    left_col, div_col, right_col = st.columns([1, 0.1, 2.5], gap="small")
    
    with left_col:
        st.markdown("""
            <h1 style="color: #44433E; font-family: 'Montserrat', sans-serif; font-size: 3.2rem; line-height: 1.1; margin-bottom: 20px; margin-top: -100px;">Local<br>Ecosystem</h1>
            <p class="hero-subtitle" style="font-size:1.3rem;">
            A topological view of your immediate<br>peers and accessible mentors.
            </p>""", unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 30px;' class='wm-label'>Operating Region</div>", unsafe_allow_html=True)
        teacher_region = st.selectbox("Your Operating Region:", list(REGION_COORDS.keys()), label_visibility="collapsed")

    with div_col:
        # This renders your CSS divider
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
    with right_col:
        st.markdown(f"<h3 style='color: #44433E; font-family: Montserrat, sans-serif; margin-top: -100px;'>Ecosystem Snapshot: {teacher_region}</h3>", unsafe_allow_html=True)
        
        regional_df = df[df['region'] == teacher_region].copy()

        if 'regional_alerts' in st.session_state:
            for alert in st.session_state['regional_alerts']:
                if alert['region'] == teacher_region:
                    st.success(alert['message'], icon="🤝")

        veteran_count = len(regional_df[regional_df['years_experience'] >= 15])
        standard_count = len(regional_df) - veteran_count
        
        # Display localized metrics
        mc1, mc2 = st.columns(2)
        mc1.markdown(f"""
        <div class="white-metric-card" style="border-left: 4px solid #10B981; margin-top: -50px;">
            <div class="wm-label">Available Local Legends</div>
            <div class="wm-value" style="color: #10B981;">{veteran_count}</div>
        </div>
        """, unsafe_allow_html=True)

        mc2.markdown(f"""
        <div class="white-metric-card" style="border-left: 4px solid #3B82F6; margin-top: -50px;">
            <div class="wm-label">Standard Peers</div>
            <div class="wm-value" style="color: #3B82F6;">{standard_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        with st.spinner("Rendering Private Network Topology..."):
            html_data = build_pyvis_graph(regional_df, limit=35) 
            components.html(html_data, height=520)
            
        overflow_count = len(regional_df) - 35
        if overflow_count > 0:
            with st.expander(f"View {overflow_count} Additional Regional Peers (Hidden to preserve graph performance)"):
                st.dataframe(regional_df.iloc[35:][["teacher_id", "first_name", "last_name", "major_specialization", "years_experience"]].reset_index(drop=True), use_container_width=True)
            
        st.markdown("""
        <div class='white-metric-card' style='display: flex; justify-content: space-around; flex-wrap: wrap; padding: 15px;'>
            <div>
                <div class='wm-label'>Node Shapes</div>
                <div style='font-size: 13px; color: #444;'>⭐ Local Legend (15+ Yrs)<br>🔵 Standard Node<br>🔴 Region Hub</div>
            </div>
            <div>
                <div class='wm-label'>Subject Colors (A-M)</div>
                <div style='font-size: 13px; color: #444;'>🟦 Physics<br>🟩 Chemistry<br>🟧 Biology</div>
            </div>
            <div>
                <div class='wm-label'>Subject Colors (N-Z)</div>
                <div style='font-size: 13px; color: #444;'>🟪 Math<br>⬜ Gen Sci<br>⚪ Other</div>
            </div>
        </div>
        """, unsafe_allow_html=True)