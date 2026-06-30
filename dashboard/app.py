import streamlit as st
from components.auth import check_auth

st.set_page_config(
    page_title="AgentGuard V3 - SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🛡️ AgentGuard V3 - SOC Dashboard")
    
    if check_auth():
        st.write("Welcome to the AgentGuard Security Operations Center.")
        st.write("Use the sidebar to navigate to KPIs, Incident Queue, or Live Logs.")
        
        if st.sidebar.button("Logout"):
            del st.session_state["token"]
            st.rerun()

if __name__ == "__main__":
    main()
