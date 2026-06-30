import streamlit as st
import httpx
import pandas as pd
from components.auth import check_auth, get_auth_headers, API_URL

if not check_auth():
    st.stop()

st.title("📋 Live Logs (SIEM View)")

limit = st.slider("Number of logs to fetch", 10, 500, 50)

if st.button("Refresh"):
    st.rerun()

try:
    response = httpx.get(f"{API_URL}/dashboard/logs?limit={limit}", headers=get_auth_headers())
    if response.status_code == 200:
        logs = response.json()
        if not logs:
            st.info("No logs found.")
        else:
            df = pd.DataFrame(logs)
            st.dataframe(df[["id", "timestamp", "agent_id", "tool_name", "decision", "risk_score", "status", "correlation_id"]])
    else:
        st.error("Failed to load logs.")
except Exception as e:
    st.error(f"Error connecting to backend: {e}")
