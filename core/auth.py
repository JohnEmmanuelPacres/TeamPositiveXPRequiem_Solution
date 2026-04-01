import streamlit as st

def initialize_session():
    if "role" not in st.session_state:
        st.session_state.role = "Admin"
    
def get_current_role() -> str:
    return st.session_state.get('role', 'Admin')

def toggle_role():
    if st.session_state.role == "Admin":
        st.session_state.role = "Teacher"
    else:
        st.session_state.role = "Admin"

def render_sidebar_auth():
    st.sidebar.markdown("### Authentication Panel")
    st.sidebar.info(f"Currently logged in as: **{st.session_state.role}**")
    if st.sidebar.button("Switch Role"):
        toggle_role()
        st.rerun()
