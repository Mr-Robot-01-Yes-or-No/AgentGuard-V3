import streamlit as st
import httpx
from components.auth import check_auth, get_auth_headers, API_URL

if not check_auth():
    st.stop()

st.title("📊 Executive KPIs")

try:
    response = httpx.get(f"{API_URL}/dashboard/stats", headers=get_auth_headers())
    if response.status_code == 200:
        stats = response.json()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Requests", stats["total"])
        col2.metric("Blocked / Pending (RED)", stats["red"] + stats["pending"], delta_color="inverse")
        col3.metric("Warnings (YELLOW)", stats["yellow"], delta_color="off")
        col4.metric("Allowed (GREEN)", stats["green"], delta_color="normal")
        
    else:
        st.error("Failed to load KPIs.")
except Exception as e:
    st.error(f"Error connecting to backend: {e}")
