import streamlit as st
import httpx
from components.auth import check_auth, get_auth_headers, API_URL
import json

if not check_auth():
    st.stop()

st.title("🚨 Incident Queue")
st.write("Review and approve/reject suspended agent actions.")

try:
    response = httpx.get(f"{API_URL}/dashboard/incidents/pending", headers=get_auth_headers())
    if response.status_code == 200:
        incidents = response.json()
        
        if not incidents:
            st.success("No pending incidents. Good job!")
            st.stop()
            
        for incident in incidents:
            with st.expander(f"Incident #{incident['id']} - {incident['tool_name']} (Risk: {incident['risk_score']})"):
                st.write(f"**Agent ID:** {incident['agent_id']}")
                st.write(f"**Timestamp:** {incident['timestamp']}")
                st.write(f"**Reason:** {incident['admin_notes']}")
                st.write(f"**MITRE:** {incident['mitre_mappings']}")
                st.write(f"**OWASP:** {incident['owasp_mappings']}")
                
                st.json(json.loads(incident['parameters']))
                
                col1, col2 = st.columns(2)
                if col1.button("Approve", key=f"approve_{incident['id']}", type="primary"):
                    res = httpx.post(f"{API_URL}/dashboard/incidents/{incident['id']}/approve", headers=get_auth_headers())
                    if res.status_code == 200:
                        st.success(f"Incident #{incident['id']} Approved!")
                        st.rerun()
                    else:
                        st.error(f"Failed to approve: {res.text}")
                
                if col2.button("Reject", key=f"reject_{incident['id']}"):
                    res = httpx.post(f"{API_URL}/dashboard/incidents/{incident['id']}/reject", headers=get_auth_headers())
                    if res.status_code == 200:
                        st.warning(f"Incident #{incident['id']} Rejected!")
                        st.rerun()
                    else:
                        st.error(f"Failed to reject: {res.text}")
    else:
        st.error("Failed to load incidents.")
except Exception as e:
    st.error(f"Error connecting to backend: {e}")
