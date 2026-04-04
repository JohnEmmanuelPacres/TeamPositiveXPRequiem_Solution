import streamlit as st
import pandas as pd
import os

def initialize_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "username" not in st.session_state:
        st.session_state.username = ""
    
def get_current_role() -> str:
    return st.session_state.get('role', '')

def logout():
    st.session_state.authenticated = False
    st.session_state.role = ""
    st.session_state.username = ""

def render_sidebar_auth():
    st.sidebar.markdown("### Authentication Panel")
    st.sidebar.info(f"Logged in as: **{st.session_state.role}**\n\nUser Profile: `{st.session_state.username}`")
    if st.sidebar.button("Logout", use_container_width=True):
        logout()
        st.rerun()

def render_login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>STAR Decision Support System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #888888;'>Secure Authentication Gateway</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("System Identifier", placeholder="Enter your ID or username")
            password = st.text_input("Password", type="password", placeholder="Enter your credentials")
            submitted = st.form_submit_button("Authenticate Access", use_container_width=True)
            
            if submitted:
                accounts_path = os.path.join("Dataset", "Data", "accounts.csv")
                if not os.path.exists(accounts_path):
                    st.error("Authentication database is offline.")
                    return
                    
                accounts_df = pd.read_csv(accounts_path)
                
                # Strip strings to prevent whitespace errors
                match = accounts_df[
                    (accounts_df['username'].astype(str).str.strip() == str(username).strip()) & 
                    (accounts_df['password'].astype(str).str.strip() == str(password).strip())
                ]
                
                if not match.empty:
                    st.session_state.authenticated = True
                    st.session_state.role = match.iloc[0]['role']
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Security sweep logged.")
